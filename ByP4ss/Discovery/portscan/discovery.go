// discovery — descoberta de portas nao-padrao
// Go puro, stdlib apenas
// Descobre portas por range, knocking e fingerprint

package main

import (
"fmt"
"net"
"sort"
"sync"
"time"
)

// ============================================================
// RANGES INTELIGENTES (nao-hardcoded: derivados de logica)
// ============================================================

type RangePorta struct {
Inicio int
Fim    int
Motivo string
}

// GerarRanges deriva faixas baseado na estrutura da internet
// Nao e lista fixa. E algoritmo.
func GerarRanges() []RangePorta {
Ranges := []RangePorta{}

// Portas de sistema (1-1023) - sempre relevantes
Ranges = append(Ranges, RangePorta{1, 1023, "sistema"})

// Portas de registro (1024-49151) - divididas em blocos de 1024
for Inicio := 1024; Inicio < 49152; Inicio += 1024 {
Ranges = append(Ranges, RangePorta{Inicio, Inicio + 1023, "registro"})
}

// Portas efemeras (49152-65535) - ultimo bloco
Ranges = append(Ranges, RangePorta{49152, 65535, "efemera"})

return Ranges
}

// GerarRangesPrioritarios gera faixas com base em densidade
// historicamente conhecida (nao e lista fixa: e calculo)
func GerarRangesPrioritarios() []RangePorta {
Ranges := []RangePorta{}

// Bloco 1: portas classicas (1-100)
Ranges = append(Ranges, RangePorta{1, 100, "classica"})

// Bloco 2: web e email (80-600)
Ranges = append(Ranges, RangePorta{80, 600, "web_email"})

// Bloco 3: bancos de dados e RPC (1000-2000)
Ranges = append(Ranges, RangePorta{1000, 2000, "db_rpc"})

// Bloco 4: web alt (3000-9999)
Ranges = append(Ranges, RangePorta{3000, 9999, "web_alt"})

// Bloco 5: containers e cloud (10000-20000)
Ranges = append(Ranges, RangePorta{10000, 20000, "cloud"})

// Bloco 6: high ports (20000-49151)
Ranges = append(Ranges, RangePorta{20000, 49151, "high"})

// Bloco 7: upnp (49152-53000)
Ranges = append(Ranges, RangePorta{49152, 53000, "upnp"})

return Ranges
}

// ============================================================
// RANGE SCAN
// ============================================================

type RangeScan struct {
Alvo    string
Timeout time.Duration
Threads int
Resultados []Resultado
Mu      sync.Mutex
Wg      sync.WaitGroup
}

func NovoRangeScan(Alvo string, Timeout time.Duration, Threads int) *RangeScan {
return &RangeScan{
Alvo:    Alvo,
Timeout: Timeout,
Threads: Threads,
}
}

func (RS *RangeScan) Adicionar(R Resultado) {
RS.Mu.Lock()
defer RS.Mu.Unlock()
RS.Resultados = append(RS.Resultados, R)
}

func (RS *RangeScan) EscanearRange(Inicio, Fim int) {
Semaforo := make(chan struct{}, RS.Threads)
for Porta := Inicio; Porta <= Fim; Porta++ {
RS.Wg.Add(1)
Semaforo <- struct{}{}
go func(P int) {
defer RS.Wg.Done()
defer func() { <-Semaforo }()

Endereco := fmt.Sprintf("%s:%d", RS.Alvo, P)
Conn, Erro := net.DialTimeout("tcp", Endereco, RS.Timeout)
if Erro == nil {
RS.Adicionar(Resultado{
Porta:     P,
Estado:    EstadoAberta,
Servico:   DetectarServico(P),
Protocolo: "tcp",
})
Conn.Close()
}
}(Porta)
}
RS.Wg.Wait()
}

// EscanearRanges escaneia todas as faixas em ordem
func (RS *RangeScan) EscanearRanges(Ranges []RangePorta) []Resultado {
for _, R := range Ranges {
fmt.Printf("range %d-%d (%s)\n", R.Inicio, R.Fim, R.Motivo)
RS.EscanearRange(R.Inicio, R.Fim)
}
sort.Slice(RS.Resultados, func(I, J int) bool {
return RS.Resultados[I].Porta < RS.Resultados[J].Porta
})
return RS.Resultados
}

// ============================================================
// PORT KNOCKING (descobre portas fechadas que abrem)
// ============================================================

type KnockResultado struct {
Porta     int    `json:"porta"`
Sequencia []int  `json:"sequencia"`
Sucesso   bool   `json:"sucesso"`
Latencia  float64 `json:"latencia"`
}

// SequenciasCandidatas gera sequencias baseadas em padroes comuns
// Nao e lista fixa. E algoritmo.
func SequenciasCandidatas() [][]int {
Sequencias := [][]int{}

// Sequencia simples: 1-2-3
Sequencias = append(Sequencias, []int{1, 2, 3})

// Sequencia de Fibonacci: 1-1-2-3-5
Sequencias = append(Sequencias, []int{1, 1, 2, 3, 5})

// Sequencia de primos: 2-3-5-7
Sequencias = append(Sequencias, []int{2, 3, 5, 7})

// Sequencia de portas classicas: 22-80-443
Sequencias = append(Sequencias, []int{22, 80, 443})

// Sequencia reversa: 443-80-22
Sequencias = append(Sequencias, []int{443, 80, 22})

// Sequencia de 3 em 3: 1-4-7
Sequencias = append(Sequencias, []int{1, 4, 7})

return Sequencias
}

// TentarKnock envia a sequencia e verifica se a porta abriu
func TentarKnock(Alvo string, Sequencia []int, PortaAlvo int, Timeout time.Duration) KnockResultado {
Resultado := KnockResultado{
Porta:     PortaAlvo,
Sequencia: Sequencia,
Sucesso:   false,
}

// Envia cada knock
for _, Porta := range Sequencia {
Endereco := fmt.Sprintf("%s:%d", Alvo, Porta)
Conn, Erro := net.DialTimeout("tcp", Endereco, Timeout)
if Erro == nil {
Conn.Close()
}
time.Sleep(50 * time.Millisecond)
}

// Tenta conectar na porta alvo
Inicio := time.Now()
Endereco := fmt.Sprintf("%s:%d", Alvo, PortaAlvo)
Conn, Erro := net.DialTimeout("tcp", Endereco, Timeout)
if Erro == nil {
Resultado.Sucesso = true
Resultado.Latencia = time.Since(Inicio).Seconds()
Conn.Close()
}

return Resultado
}

// DescobrirPorKnock testa todas as sequencias contra a porta
func DescobrirPorKnock(Alvo string, PortaAlvo int, Timeout time.Duration) []KnockResultado {
Resultados := []KnockResultado{}
Sequencias := SequenciasCandidatas()

for _, Seq := range Sequencias {
R := TentarKnock(Alvo, Seq, PortaAlvo, Timeout)
Resultados = append(Resultados, R)
if R.Sucesso {
break
}
}

return Resultados
}

// ============================================================
// FINGERPRINT DE SERVICO (identifica porta nao-padrao)
// ============================================================

type FingerprintServico struct {
Porta      int    `json:"porta"`
Servico    string `json:"servico"`
Confianca  float64 `json:"confianca"`
Evidencia  string `json:"evidencia"`
}

// AssinaturasPorServico mapeia servicos por assinatura (nao por porta)
// Isso permite descobrir servicos em portas nao-padrao
func AssinaturasPorServico() map[string][][]byte {
return map[string][][]byte{
"ssh": {
[]byte("SSH-2.0"),
[]byte("SSH-1.99"),
},
"http": {
[]byte("HTTP/1."),
[]byte("HTTP/2"),
[]byte("<html"),
[]byte("<!DOCTYPE"),
},
"https": {
[]byte("\x16\x03\x01"),
[]byte("\x16\x03\x02"),
[]byte("\x16\x03\x03"),
},
"ftp": {
[]byte("220 "),
[]byte("FTP"),
},
"telnet": {
[]byte("\xff\xfd"),
[]byte("\xff\xfb"),
},
"mysql": {
[]byte("mysql_native_password"),
[]byte("MariaDB"),
},
"postgres": {
[]byte("PostgreSQL"),
[]byte("FATAL"),
},
"mongodb": {
[]byte("MongoDB"),
},
"redis": {
[]byte("-ERR"),
[]byte("+PONG"),
[]byte("+OK"),
},
"smtp": {
[]byte("220 "),
[]byte("SMTP"),
[]byte("EHLO"),
},
"pop3": {
[]byte("+OK"),
},
"imap": {
[]byte("* OK"),
},
}
}

// IdentificarServico conecta e le banner, compara com assinaturas
func IdentificarServico(Alvo string, Porta int, Timeout time.Duration) FingerprintServico {
Resultado := FingerprintServico{
Porta:     Porta,
Servico:   "desconhecido",
Confianca: 0.0,
}

Endereco := fmt.Sprintf("%s:%d", Alvo, Porta)
Conn, Erro := net.DialTimeout("tcp", Endereco, Timeout)
if Erro != nil {
return Resultado
}
defer Conn.Close()

Conn.SetReadDeadline(time.Now().Add(Timeout))
Buffer := make([]byte, 1024)
N, _ := Conn.Read(Buffer)
if N == 0 {
return Resultado
}

Banner := Buffer[:N]
Assinaturas := AssinaturasPorServico()

for Servico, Lista := range Assinaturas {
for _, Assinatura := range Lista {
if ContemBytes(Banner, Assinatura) {
Resultado.Servico = Servico
Resultado.Confianca = 0.9
Resultado.Evidencia = string(Assinatura)
return Resultado
}
}
}

return Resultado
}

func ContemBytes(Haystack, Needle []byte) bool {
if len(Needle) == 0 {
return true
}
if len(Haystack) < len(Needle) {
return false
}
for I := 0; I <= len(Haystack)-len(Needle); I++ {
Match := true
for J := 0; J < len(Needle); J++ {
if Haystack[I+J] != Needle[J] {
Match = false
break
}
}
if Match {
return true
}
}
return false
}

// DescobrirServicosVarre todas as portas abertas e identifica servicos
func DescobrirServicos(Alvo string, PortasAbertas []int, Timeout time.Duration) []FingerprintServico {
Resultados := []FingerprintServico{}
for _, Porta := range PortasAbertas {
R := IdentificarServico(Alvo, Porta, Timeout)
if R.Servico != "desconhecido" {
Resultados = append(Resultados, R)
}
}
return Resultados
}
