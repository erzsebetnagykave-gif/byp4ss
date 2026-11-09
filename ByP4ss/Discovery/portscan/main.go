// portscan — motor de port scan universal do ByP4ss
// Go puro, stdlib apenas
// Universal: funciona em qualquer roteador (ZTE, Huawei, TP-Link, MikroTik, Cisco, OpenWrt)

package main

import (
"crypto/tls"
	"encoding/json"
"flag"
"fmt"
"net"
"os"
"sort"
"strings"
"sync"
"time"
)

type Estado string

const (
EstadoAberta   Estado = "aberta"
EstadoFechada  Estado = "fechada"
EstadoFiltrada Estado = "filtrada"
EstadoRecusada Estado = "recusada"
EstadoErro     Estado = "erro"
)

type Resultado struct {
Porta     int     `json:"porta"`
Estado    Estado  `json:"estado"`
Servico   string  `json:"servico"`
Banner    string  `json:"banner"`
Latencia  float64 `json:"latencia"`
Erro      string  `json:"erro"`
Protocolo string  `json:"protocolo"`
}

type Relatorio struct {
Alvo       string      `json:"alvo"`
Vendor     string      `json:"vendor"`
Modelo     string      `json:"modelo"`
So         string      `json:"so"`
Total      int         `json:"total"`
Abertas    int         `json:"abertas"`
Fechadas   int         `json:"fechadas"`
Filtradas  int         `json:"filtradas"`
Recusadas  int         `json:"recusadas"`
Erros      int         `json:"erros"`
Inicio     string      `json:"inicio"`
Fim        string      `json:"fim"`
Duracao    float64     `json:"duracao"`
Resultados []Resultado `json:"resultados"`
}

type Scanner struct {
Alvo    string
Timeout time.Duration
Threads int
Resultados []Resultado
Mu      sync.Mutex
Wg      sync.WaitGroup
}

func NewScanner(Alvo string, Timeout time.Duration, Threads int) *Scanner {
return &Scanner{Alvo: Alvo, Timeout: Timeout, Threads: Threads}
}

func (S *Scanner) AddResultado(R Resultado) {
S.Mu.Lock()
defer S.Mu.Unlock()
S.Resultados = append(S.Resultados, R)
}

func (S *Scanner) ScanPorta(Porta int) {
Inicio := time.Now()
Endereco := fmt.Sprintf("%s:%d", S.Alvo, Porta)
Conn, Erro := net.DialTimeout("tcp", Endereco, S.Timeout)
Latencia := time.Since(Inicio).Seconds()

R := Resultado{Porta: Porta, Latencia: Latencia, Protocolo: "tcp"}

if Erro != nil {
if NetErr, Ok := Erro.(net.Error); Ok && NetErr.Timeout() {
R.Estado = EstadoFiltrada
} else if OpErr, Ok := Erro.(*net.OpError); Ok {
Msg := OpErr.Err.Error()
if strings.Contains(Msg, "refused") {
R.Estado = EstadoRecusada
} else if strings.Contains(Msg, "no route") || strings.Contains(Msg, "unreachable") {
R.Estado = EstadoFiltrada
} else {
R.Estado = EstadoFechada
}
R.Erro = Msg
} else {
R.Estado = EstadoErro
R.Erro = Erro.Error()
}
S.AddResultado(R)
return
}
defer Conn.Close()

R.Estado = EstadoAberta
R.Servico = DetectarServico(Porta)

Conn.SetReadDeadline(time.Now().Add(500 * time.Millisecond))
Buffer := make([]byte, 1024)
N, _ := Conn.Read(Buffer)
if N > 0 {
R.Banner = LimparBanner(string(Buffer[:N]))
}

S.AddResultado(R)
}

func (S *Scanner) ScanPortas(Portas []int) {
Semaforo := make(chan struct{}, S.Threads)
for _, Porta := range Portas {
S.Wg.Add(1)
Semaforo <- struct{}{}
go func(P int) {
defer S.Wg.Done()
defer func() { <-Semaforo }()
S.ScanPorta(P)
}(Porta)
}
S.Wg.Wait()
}

func (S *Scanner) ScanPortaUdp(Porta int) {
Inicio := time.Now()
Endereco := fmt.Sprintf("%s:%d", S.Alvo, Porta)
Conn, Erro := net.DialTimeout("udp", Endereco, S.Timeout)

R := Resultado{Porta: Porta, Protocolo: "udp", Latencia: time.Since(Inicio).Seconds()}

if Erro != nil {
R.Estado = EstadoErro
R.Erro = Erro.Error()
S.AddResultado(R)
return
}
defer Conn.Close()

Conn.SetWriteDeadline(time.Now().Add(S.Timeout))
_, Erro = Conn.Write([]byte{0, 0, 0, 0})
if Erro != nil {
R.Estado = EstadoErro
R.Erro = Erro.Error()
S.AddResultado(R)
return
}

Buffer := make([]byte, 1024)
Conn.SetReadDeadline(time.Now().Add(S.Timeout))
N, Erro := Conn.Read(Buffer)

if Erro != nil {
if NetErr, Ok := Erro.(net.Error); Ok && NetErr.Timeout() {
R.Estado = EstadoFiltrada
} else {
R.Estado = EstadoRecusada
R.Erro = Erro.Error()
}
} else {
R.Estado = EstadoAberta
R.Servico = DetectarServico(Porta)
R.Banner = LimparBanner(string(Buffer[:N]))
}

S.AddResultado(R)
}

func (S *Scanner) ScanPortasUdp(Portas []int) {
Semaforo := make(chan struct{}, S.Threads)
for _, Porta := range Portas {
S.Wg.Add(1)
Semaforo <- struct{}{}
go func(P int) {
defer S.Wg.Done()
defer func() { <-Semaforo }()
S.ScanPortaUdp(P)
}(Porta)
}
S.Wg.Wait()
}

func (S *Scanner) DetectarVendor() (string, string) {
Vendor := "desconhecido"
Modelo := "desconhecido"

Vendors := map[string]string{
"zte": "ZTE", "huawei": "Huawei", "tp-link": "TP-Link",
"tplink": "TP-Link", "d-link": "D-Link", "dlink": "D-Link",
"mikrotik": "MikroTik", "routeros": "MikroTik", "cisco": "Cisco",
"netgear": "Netgear", "asus": "Asus", "linksys": "Linksys",
"openwrt": "OpenWrt", "dd-wrt": "DD-WRT", "ubiquiti": "Ubiquiti",
"ruckus": "Ruckus", "aruba": "Aruba", "juniper": "Juniper",
"fortinet": "Fortinet", "fortigate": "Fortinet",
"palo alto": "Palo Alto", "pfsense": "pfSense", "zyxel": "Zyxel",
"technicolor": "Technicolor", "sagemcom": "Sagemcom",
"nokia": "Nokia", "alcatel": "Alcatel", "fiberhome": "Fiberhome",
}

// Tentar HTTPS com handshake TLS real (revela o certificado)
Config := &tls.Config{InsecureSkipVerify: true}
EnderecoTls := fmt.Sprintf("%s:443", S.Alvo)
Dialer := &net.Dialer{Timeout: S.Timeout}
ConnTls, Erro := tls.DialWithDialer(Dialer, "tcp", EnderecoTls, Config)
if Erro == nil {
Estado := ConnTls.ConnectionState()
if len(Estado.PeerCertificates) > 0 {
Cert := Estado.PeerCertificates[0]
Assunto := strings.ToLower(Cert.Subject.String())
Emissor := strings.ToLower(Cert.Issuer.String())
Combinado := Assunto + " " + Emissor

for Assinatura, Nome := range Vendors {
if strings.Contains(Combinado, Assinatura) {
Vendor = Nome
break
}
}

// Extrair CN do certificado (geralmente modelo ou IP)
Cn := Cert.Subject.CommonName
if len(Cn) > 0 && len(Cn) < 80 && Cn != S.Alvo {
Modelo = Cn
}
}
ConnTls.Close()
}

// Se ainda desconhecido, tentar HTTP (seguindo redirect)
if Vendor == "desconhecido" {
for _, Porta := range []int{80, 8080} {
Endereco := fmt.Sprintf("%s:%d", S.Alvo, Porta)
Conn, Erro := net.DialTimeout("tcp", Endereco, S.Timeout)
if Erro != nil {
continue
}

Conn.SetDeadline(time.Now().Add(S.Timeout))
Conn.Write([]byte("GET / HTTP/1.0\r\nHost: " + S.Alvo + "\r\nUser-Agent: Mozilla/5.0\r\n\r\n"))

Buffer := make([]byte, 8192)
N, _ := Conn.Read(Buffer)
Conn.Close()

if N == 0 {
continue
}

Resposta := strings.ToLower(string(Buffer[:N]))
RespostaOriginal := string(Buffer[:N])

for Assinatura, Nome := range Vendors {
if strings.Contains(Resposta, Assinatura) {
Vendor = Nome
break
}
}

// Headers que revelam o vendor
if Vendor == "desconhecido" {
if strings.Contains(Resposta, "server: zte") || strings.Contains(Resposta, "server:zte") {
Vendor = "ZTE"
} else if strings.Contains(Resposta, "realm=") {
Idx := strings.Index(Resposta, "realm=")
if Idx > 0 && Idx+50 < len(Resposta) {
Realm := Resposta[Idx : Idx+50]
for Assinatura, Nome := range Vendors {
if strings.Contains(Realm, Assinatura) {
Vendor = Nome
break
}
}
}
}
}

if Vendor != "desconhecido" {
Idx := strings.Index(RespostaOriginal, "<title>")
if Idx >= 0 {
Fim := strings.Index(RespostaOriginal[Idx:], "</title>")
if Fim > 0 && len(Modelo) == 0 {
Titulo := RespostaOriginal[Idx+7 : Idx+Fim]
if len(Titulo) < 80 {
Modelo = strings.TrimSpace(Titulo)
}
}
}
break
}
}
}

return Vendor, Modelo
}

func (S *Scanner) DetectarSo() string {
Endereco := fmt.Sprintf("%s:80", S.Alvo)
Conn, Erro := net.DialTimeout("tcp", Endereco, S.Timeout)
if Erro != nil {
return "desconhecido"
}
defer Conn.Close()

return "Linux" // roteadores são Linux por padrão
}

func (S *Scanner) GerarRelatorio(Inicio time.Time) Relatorio {
Fim := time.Now()
Vendor, Modelo := S.DetectarVendor()
So := S.DetectarSo()

Rel := Relatorio{
Alvo:       S.Alvo,
Vendor:     Vendor,
Modelo:     Modelo,
So:         So,
Total:      len(S.Resultados),
Inicio:     Inicio.Format("2006-01-02 15:04:05"),
Fim:        Fim.Format("2006-01-02 15:04:05"),
Duracao:    Fim.Sub(Inicio).Seconds(),
Resultados: S.Resultados,
}

for _, R := range S.Resultados {
switch R.Estado {
case EstadoAberta:
Rel.Abertas++
case EstadoFechada:
Rel.Fechadas++
case EstadoFiltrada:
Rel.Filtradas++
case EstadoRecusada:
Rel.Recusadas++
case EstadoErro:
Rel.Erros++
}
}

Filtrados := []Resultado{}
for _, R := range Rel.Resultados {
if R.Estado == EstadoAberta || R.Estado == EstadoFiltrada {
Filtrados = append(Filtrados, R)
}
}
Rel.Resultados = Filtrados

sort.Slice(Rel.Resultados, func(I, J int) bool {
return Rel.Resultados[I].Porta < Rel.Resultados[J].Porta
})

return Rel
}

func ParsePortas(Texto string) []int {
Portas := []int{}
for _, Parte := range strings.Split(Texto, ",") {
Parte = strings.TrimSpace(Parte)
if strings.Contains(Parte, "-") {
Limites := strings.SplitN(Parte, "-", 2)
if len(Limites) == 2 {
var Inicio, Fim int
fmt.Sscanf(Limites[0], "%d", &Inicio)
fmt.Sscanf(Limites[1], "%d", &Fim)
if Inicio > 0 && Fim < 65536 && Inicio <= Fim {
for P := Inicio; P <= Fim; P++ {
Portas = append(Portas, P)
}
}
}
} else {
var P int
fmt.Sscanf(Parte, "%d", &P)
if P > 0 && P < 65536 {
Portas = append(Portas, P)
}
}
}
return Portas
}

func LimparBanner(B string) string {
Limpo := []byte{}
for _, C := range []byte(B) {
if C == '\r' || C == '\n' {
if len(Limpo) > 0 && Limpo[len(Limpo)-1] != ' ' {
Limpo = append(Limpo, ' ')
}
} else if C >= 32 && C < 127 {
Limpo = append(Limpo, C)
}
}
if len(Limpo) > 200 {
Limpo = Limpo[:200]
}
return string(Limpo)
}

func DetectarServico(Porta int) string {
Mapa := map[int]string{
21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
69: "tftp", 80: "http", 110: "pop3", 111: "rpcbind",
123: "ntp", 135: "msrpc", 137: "netbios-ns", 139: "netbios-ssn",
143: "imap", 161: "snmp", 179: "bgp", 389: "ldap", 443: "https",
445: "microsoft-ds", 500: "isakmp", 514: "syslog", 515: "printer",
548: "afp", 554: "rtsp", 587: "submission", 623: "ipmi",
636: "ldaps", 873: "rsync", 990: "ftps", 993: "imaps",
995: "pop3s", 1080: "socks", 1194: "openvpn", 1433: "mssql",
1521: "oracle", 1723: "pptp", 1900: "upnp", 2000: "cisco-sccp",
2049: "nfs", 2375: "docker", 2376: "docker-ssl", 3000: "grafana",
3306: "mysql", 3389: "rdp", 4443: "https-alt", 5000: "upnp-alt",
5060: "sip", 5222: "xmpp", 5432: "postgres", 5900: "vnc",
5984: "couchdb", 6379: "redis", 6443: "k8s-api", 7001: "weblogic",
7547: "tr-069", 8000: "http-alt", 8008: "http-alt",
8080: "http-alt", 8081: "http-alt", 8086: "influxdb",
8089: "splunk", 8123: "polipo", 8291: "mikrotik",
8443: "https-alt", 8500: "consul", 8888: "http-alt",
9000: "http-alt", 9090: "prometheus", 9200: "elasticsearch",
9300: "elasticsearch", 9443: "https-alt", 10000: "webmin",
11211: "memcached", 15672: "rabbitmq", 27017: "mongodb",
27018: "mongodb", 49152: "upnp", 49153: "upnp", 52869: "upnp",
}
if S, Ok := Mapa[Porta]; Ok {
return S
}
return "desconhecido"
}

var PortasCriticas = []int{
21, 22, 23, 25, 53, 69, 80, 110, 111, 123, 135, 137, 138, 139, 143,
161, 162, 179, 389, 443, 445, 500, 514, 515, 548, 554, 587, 623,
636, 873, 990, 993, 995, 1080, 1194, 1433, 1521, 1723, 1900, 2000,
2049, 2082, 2083, 2375, 2376, 3000, 3306, 3389, 4443, 5000, 5060,
5222, 5432, 5900, 5984, 6379, 6443, 7001, 7547, 8000, 8008, 8080,
8081, 8086, 8089, 8123, 8291, 8443, 8500, 8888, 9000, 9090,
9200, 9300, 9443, 10000, 11211, 15672, 27017, 27018, 49152,
49153, 52869,
}

var PortasWeb = []int{80, 443, 8000, 8008, 8080, 8081, 8086, 8089, 8443, 8888, 9000, 9443}
var PortasBancoDados = []int{1433, 1521, 3306, 5432, 5984, 6379, 9200, 9300, 11211, 15672, 27017, 27018}
var PortasUpnp = []int{1900, 2869, 5000, 52869, 49152, 49153}
var PortasTelnet = []int{23, 2323, 23231, 8023}
var PortasSsh = []int{22, 2222, 22222, 8022}
var PortasUdpDefault = []int{53, 67, 68, 69, 123, 137, 138, 161, 162, 500, 514, 520, 623, 1900, 4500, 5353, 52869}

func WordlistRoteador() []int {
Portas := []int{}
Portas = append(Portas, PortasCriticas...)
Portas = append(Portas, PortasWeb...)
Portas = append(Portas, PortasBancoDados...)
Portas = append(Portas, PortasUpnp...)
Portas = append(Portas, PortasTelnet...)
Portas = append(Portas, PortasSsh...)
Vistos := map[int]bool{}
Unicos := []int{}
for _, P := range Portas {
if !Vistos[P] {
Vistos[P] = true
Unicos = append(Unicos, P)
}
}
sort.Ints(Unicos)
return Unicos
}

func SelecionarPortas(Modo string) []int {
switch Modo {
case "web":
return PortasWeb
case "bd":
return PortasBancoDados
case "upnp":
return PortasUpnp
case "telnet":
return PortasTelnet
case "ssh":
return PortasSsh
case "criticas":
return PortasCriticas
case "roteador":
return WordlistRoteador()
case "full":
Portas := []int{}
for P := 1; P <= 1024; P++ {
Portas = append(Portas, P)
}
return Portas
case "1-65535":
Portas := []int{}
for P := 1; P <= 65535; P++ {
Portas = append(Portas, P)
}
return Portas
default:
return PortasCriticas
}
}

func main() {
Alvo := flag.String("alvo", "127.0.0.1", "IP alvo")
Portas := flag.String("portas", "", "Lista de portas (sobrepoe modo)")
Modo := flag.String("modo", "criticas", "Modo: criticas, web, bd, upnp, telnet, ssh, roteador, full, 1-65535")
TimeoutMs := flag.Int("timeout", 1500, "Timeout em ms")
Threads := flag.Int("threads", 100, "Numero de threads")
Udp := flag.Bool("udp", false, "Incluir scan UDP")
So := flag.Bool("so", false, "Incluir deteccao de SO")
Saida := flag.String("saida", "", "Arquivo de saida (vazio = stdout)")
flag.Parse()

var ListaPortas []int
if *Portas != "" {
ListaPortas = ParsePortas(*Portas)
} else {
ListaPortas = SelecionarPortas(*Modo)
}

if len(ListaPortas) == 0 {
fmt.Fprintf(os.Stderr, "erro: nenhuma porta valida\n")
os.Exit(1)
}

Timeout := time.Duration(*TimeoutMs) * time.Millisecond
Inicio := time.Now()

Sc := NewScanner(*Alvo, Timeout, *Threads)

if *So {
SoInfo := Sc.DetectarSo()
fmt.Fprintf(os.Stderr, "so: %s\n", SoInfo)
}

Sc.ScanPortas(ListaPortas)

if *Udp {
Sc.ScanPortasUdp(PortasUdpDefault)
}

Rel := Sc.GerarRelatorio(Inicio)
Dados, Erro := json.MarshalIndent(Rel, "", "  ")
if Erro != nil {
fmt.Fprintf(os.Stderr, "erro json: %v\n", Erro)
os.Exit(1)
}

if *Saida != "" {
os.WriteFile(*Saida, Dados, 0644)
} else {
fmt.Println(string(Dados))
}
}
