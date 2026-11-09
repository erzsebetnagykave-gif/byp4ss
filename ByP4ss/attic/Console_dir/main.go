package main

import (
    "encoding/json"
    "fmt"
    "os"
    "os/exec"
    "path/filepath"
    "strings"
    "time"
)

const (
    Versao   = "1.0"
    BaseDir  = "/data/data/com.termux/files/home/CyberneticCrown/CC/T0OLS/ByP4ss"
    RunBin   = BaseDir + "/Paleta/run"
    StateBin = BaseDir + "/Paleta/state/state"
)

const (
    Reset      = "\033[0m"
    Bold       = "\033[1m"
    Dim        = "\033[2m"
    Invert     = "\033[7m"
    HideCursor = "\033[?25l"
    ShowCursor = "\033[?25h"
    ClearAll   = "\033[2J\033[H"
    Ciano      = "\033[36m"
    Cinza      = "\033[90m"
    Verde      = "\033[32m"
    Amarelo    = "\033[33m"
    Vermelho   = "\033[31m"
    Magenta    = "\033[35m"
    Azul       = "\033[34m"
)

var Salas = []string{"recon", "exploits", "sessions", "cadeia", "manifesto", "credenciais", "logs", "config"}

var CoresSala = map[string]string{
    "recon":       Azul,
    "exploits":    Amarelo,
    "sessions":    Verde,
    "cadeia":      Magenta,
    "manifesto":   Ciano,
    "credenciais": Verde,
    "logs":        Cinza,
    "config":      Ciano,
}

type Estado struct {
    SalaAtual   string
    Indice      int
    AlvoAtual   string
    Query       string
    Status      string
    Modo        string
    SessaoNome  string
    ShellsAtivas int
    Rodando     bool
    Largura     int
    Altura      int
}

type Resultado struct {
    Texto   string
    Detalhe string
    Ativo   bool
}

var CacheRecon []Resultado
var CacheExploits []Resultado
var CacheSessions []Resultado
var CacheCadeia []Resultado
var CacheManifesto []Resultado
var CacheCredenciais []Resultado
var CacheLogs []Resultado
var Configuracoes = map[string]string{
    "modo":          "local",
    "sessao_auto":   "true",
    "operador":      "false",
    "fantasma":      "false",
    "timeout_run":   "30",
}

func NovoEstado() *Estado {
    return &Estado{
        SalaAtual: "recon",
        Rodando:   true,
        Modo:      "local",
    }
}

func Stty(args ...string) string {
    c := exec.Command("stty", args...)
    c.Stdin = os.Stdin
    out, _ := c.Output()
    return strings.TrimSpace(string(out))
}

func SttyRun(args ...string) {
    c := exec.Command("stty", args...)
    c.Stdin = os.Stdin
    c.Run()
}

func AbrirTerminal() string {
    antigo := Stty("-g")
    SttyRun("raw", "-echo")
    os.Stdout.WriteString(HideCursor)
    os.Stdout.WriteString(ClearAll)
    return antigo
}

func FecharTerminal(antigo string) {
    os.Stdout.WriteString(ShowCursor)
    os.Stdout.WriteString(Reset)
    os.Stdout.WriteString(ClearAll)
    if antigo != "" {
        SttyRun(antigo)
    } else {
        SttyRun("sane")
    }
}

func Dimensoes() (int, int) {
    out := Stty("size")
    w, h := 80, 24
    if out != "" {
        parts := strings.Fields(out)
        if len(parts) == 2 {
            fmt.Sscanf(parts[0], "%d", &h)
            fmt.Sscanf(parts[1], "%d", &w)
        }
    }
    if w < 40 {
        w = 40
    }
    if h < 10 {
        h = 10
    }
    return w, h
}

func Visivel(s string) int {
    n := 0
    esc := false
    for _, r := range s {
        if r == '\033' {
            esc = true
            continue
        }
        if esc {
            if r == 'm' || r == 'K' || r == 'H' || r == 'J' {
                esc = false
            }
            continue
        }
        n++
    }
    return n
}

func Truncar(s string, max int) string {
    if max < 2 {
        return ""
    }
    if Visivel(s) <= max {
        return s
    }
    var b strings.Builder
    vis := 0
    esc := false
    for _, r := range s {
        if r == '\033' {
            esc = true
            b.WriteRune(r)
            continue
        }
        if esc {
            b.WriteRune(r)
            if r == 'm' || r == 'K' || r == 'H' || r == 'J' {
                esc = false
            }
            continue
        }
        if vis >= max-1 {
            b.WriteString("…")
            b.WriteString(Reset)
            return b.String()
        }
        b.WriteRune(r)
        vis++
    }
    return b.String()
}

func Ir(row, col int) string {
    return fmt.Sprintf("\033[%d;%dH", row, col)
}

type Canvas struct {
    buf strings.Builder
    w   int
    h   int
}

func NovoCanvas(w, h int) *Canvas {
    c := &Canvas{w: w, h: h}
    c.buf.WriteString(HideCursor)
    c.buf.WriteString(ClearAll)
    return c
}

func (c *Canvas) Ir(row, col int) {
    c.buf.WriteString(Ir(row, col))
}

func (c *Canvas) Write(s string) {
    c.buf.WriteString(s)
}

func (c *Canvas) Linha(row int) {
    c.Ir(row, 1)
    c.Write(strings.Repeat("─", c.w-1))
}

func (c *Canvas) Preenchido(row, col int, esq, dir string, largura int) {
    c.Ir(row, col)
    visEsq := Visivel(esq)
    visDir := Visivel(dir)
    gap := largura - visEsq - visDir
    if gap < 1 {
        c.Write(Truncar(esq+dir, largura))
        return
    }
    c.Write(esq)
    c.Write(strings.Repeat(" ", gap))
    c.Write(dir)
}

func (c *Canvas) Flush() {
    c.buf.WriteString(ShowCursor)
    os.Stdout.WriteString(c.buf.String())
    c.buf.Reset()
}

func DesenharHeader(c *Canvas, e *Estado) {
    c.Ir(1, 1)
    titulo := Bold + "BYPASS" + Reset + " v" + Versao
    dir := fmt.Sprintf("[%d/%d %s]", indiceSala(e.SalaAtual)+1, len(Salas), e.SalaAtual)
    c.Preenchido(1, 1, " "+titulo, dir+" ", c.w-1)
    c.Linha(2)
}

func DesenharMenu(c *Canvas, e *Estado) {
    c.Ir(3, 1)
    partes := []string{}
    for _, sala := range Salas {
        cor := CoresSala[sala]
        if sala == e.SalaAtual {
            partes = append(partes, cor+Bold+Invert+" "+strings.ToUpper(sala)+" "+Reset)
        } else {
            partes = append(partes, cor+Dim+" "+sala+" "+Reset)
        }
    }
    c.Write(Truncar(strings.Join(partes, " "), c.w-1))
    c.Linha(4)
}

func DesenharBreadcrumb(c *Canvas, e *Estado) {
    c.Ir(5, 1)
    cor := CoresSala[e.SalaAtual]
    c.Write(Bold + "BYPASS" + Reset + " > " + cor + e.SalaAtual + Reset)
}

func DesenharStatus(c *Canvas, e *Estado) {
    c.Linha(c.h - 1)
    c.Ir(c.h, 1)
    if e.Status != "" {
        c.Write(Truncar(" "+Dim+e.Status+Reset, c.w-1))
        return
    }
    esq := fmt.Sprintf(" %s[modo %s]%s", Cinza, e.Modo, Reset)
    if e.AlvoAtual != "" {
        esq += fmt.Sprintf(" %s[alvo %s]%s", Ciano, e.AlvoAtual, Reset)
    }
    if e.SessaoNome != "" {
        esq += fmt.Sprintf(" %s[sessao %s]%s", Verde, e.SessaoNome, Reset)
    }
    dir := Dim + "Ctrl+T sala | ↑↓ navega | Enter exec | Ctrl+S salva | Ctrl+Q sai" + Reset
    c.Preenchido(c.h, 1, esq, dir+" ", c.w-1)
}

func DesenharRecon(c *Canvas, e *Estado) {
    c.Ir(7, 1)
    c.Write(Amarelo + Bold + "RECON" + Reset + "  " + Cinza + "Enter=scan | s=scan sub-rede | a=alvo" + Reset)
    if len(CacheRecon) == 0 {
        c.Ir(9, 1)
        c.Write(Cinza + "sem dados. Enter para escanear (alvo: 127.0.0.1)" + Reset)
        return
    }
    c.Ir(9, 1)
    c.Write(Cinza + fmt.Sprintf("hosts: %d", len(CacheRecon)) + Reset)
    maxLin := c.h - 11
    for i, r := range CacheRecon {
        if i >= maxLin {
            break
        }
        c.Ir(10+i, 1)
        pref := "  "
        if i == e.Indice {
            pref = Invert + "> " + Reset
        }
        linha := pref + r.Texto
        if r.Detalhe != "" {
            pad := c.w - 1 - Visivel(linha) - Visivel(r.Detalhe) - 1
            if pad > 0 {
                linha += strings.Repeat(" ", pad) + Dim + r.Detalhe + Reset
            }
        }
        c.Write(Truncar(linha, c.w-1))
    }
}

func DesenharExploits(c *Canvas, e *Estado) {
    c.Ir(7, 1)
    c.Write(Amarelo + Bold + "EXPLOITS" + Reset + "  " + Cinza + "Enter=executa | F5=recon_auto | l=lista" + Reset)
    if len(CacheExploits) == 0 {
        c.Ir(9, 1)
        c.Write(Cinza + "Enter para listar exploits do Engine" + Reset)
        return
    }
    c.Ir(9, 1)
    c.Write(Cinza + fmt.Sprintf("exploits: %d", len(CacheExploits)) + Reset)
    maxLin := c.h - 11
    for i, r := range CacheExploits {
        if i >= maxLin {
            break
        }
        c.Ir(10+i, 1)
        pref := "  "
        if i == e.Indice {
            pref = Invert + "> " + Reset
        }
        linha := pref + r.Texto
        if r.Detalhe != "" {
            pad := c.w - 1 - Visivel(linha) - Visivel(r.Detalhe) - 1
            if pad > 0 {
                linha += strings.Repeat(" ", pad) + Dim + r.Detalhe + Reset
            }
        }
        c.Write(Truncar(linha, c.w-1))
    }
}

func DesenharSessions(c *Canvas, e *Estado) {
    c.Ir(7, 1)
    c.Write(Verde + Bold + "SESSIONS" + Reset + "  " + Cinza + "Enter=carrega | d=deleta | n=nova" + Reset)
    if len(CacheSessions) == 0 {
        c.Ir(9, 1)
        c.Write(Cinza + "sem sessoes. Ctrl+S na sala principal para criar." + Reset)
        return
    }
    c.Ir(9, 1)
    c.Write(Cinza + fmt.Sprintf("sessoes: %d", len(CacheSessions)) + Reset)
    maxLin := c.h - 11
    for i, r := range CacheSessions {
        if i >= maxLin {
            break
        }
        c.Ir(10+i, 1)
        pref := "  "
        if i == e.Indice {
            pref = Invert + "> " + Reset
        }
        linha := pref + r.Texto
        if r.Detalhe != "" {
            pad := c.w - 1 - Visivel(linha) - Visivel(r.Detalhe) - 1
            if pad > 0 {
                linha += strings.Repeat(" ", pad) + Dim + r.Detalhe + Reset
            }
        }
        c.Write(Truncar(linha, c.w-1))
    }
}

func DesenharCadeia(c *Canvas, e *Estado) {
    c.Ir(7, 1)
    c.Write(Magenta + Bold + "CADEIA" + Reset + "  " + Cinza + "Enter=executa | F5=recon_auto | v=valida" + Reset)
    if len(CacheCadeia) == 0 {
        c.Ir(9, 1)
        c.Write(Cinza + "Enter para carregar templates do Cadeia" + Reset)
        return
    }
    c.Ir(9, 1)
    c.Write(Cinza + fmt.Sprintf("templates: %d", len(CacheCadeia)) + Reset)
    maxLin := c.h - 11
    for i, r := range CacheCadeia {
        if i >= maxLin {
            break
        }
        c.Ir(10+i, 1)
        pref := "  "
        if i == e.Indice {
            pref = Invert + "> " + Reset
        }
        linha := pref + r.Texto
        if r.Detalhe != "" {
            pad := c.w - 1 - Visivel(linha) - Visivel(r.Detalhe) - 1
            if pad > 0 {
                linha += strings.Repeat(" ", pad) + Dim + r.Detalhe + Reset
            }
        }
        c.Write(Truncar(linha, c.w-1))
    }
}

func DesenharManifesto(c *Canvas, e *Estado) {
    c.Ir(7, 1)
    c.Write(Ciano + Bold + "MANIFESTO" + Reset + "  " + Cinza + "Enter=aplica | r=reverte | d=diff" + Reset)
    if len(CacheManifesto) == 0 {
        c.Ir(9, 1)
        c.Write(Cinza + "Enter para listar manifestos do catalogo" + Reset)
        return
    }
    c.Ir(9, 1)
    c.Write(Cinza + fmt.Sprintf("manifestos: %d", len(CacheManifesto)) + Reset)
    maxLin := c.h - 11
    for i, r := range CacheManifesto {
        if i >= maxLin {
            break
        }
        c.Ir(10+i, 1)
        pref := "  "
        if i == e.Indice {
            pref = Invert + "> " + Reset
        }
        linha := pref + r.Texto
        if r.Detalhe != "" {
            pad := c.w - 1 - Visivel(linha) - Visivel(r.Detalhe) - 1
            if pad > 0 {
                linha += strings.Repeat(" ", pad) + Dim + r.Detalhe + Reset
            }
        }
        c.Write(Truncar(linha, c.w-1))
    }
}

func DesenharCredenciais(c *Canvas, e *Estado) {
    c.Ir(7, 1)
    c.Write(Verde + Bold + "CREDENCIAIS" + Reset + "  " + Cinza + "Enter=busca alvo | y=carrega YAML" + Reset)
    if len(CacheCredenciais) == 0 {
        c.Ir(9, 1)
        if e.AlvoAtual == "" {
            c.Write(Cinza + "defina alvo primeiro (recon)" + Reset)
        } else {
            c.Write(Cinza + "Enter para buscar credenciais de " + e.AlvoAtual + Reset)
        }
        return
    }
    c.Ir(9, 1)
    c.Write(Cinza + fmt.Sprintf("credenciais: %d para %s", len(CacheCredenciais), e.AlvoAtual) + Reset)
    maxLin := c.h - 11
    for i, r := range CacheCredenciais {
        if i >= maxLin {
            break
        }
        c.Ir(10+i, 1)
        pref := "  "
        if i == e.Indice {
            pref = Invert + "> " + Reset
        }
        linha := pref + r.Texto
        if r.Detalhe != "" {
            pad := c.w - 1 - Visivel(linha) - Visivel(r.Detalhe) - 1
            if pad > 0 {
                linha += strings.Repeat(" ", pad) + Dim + r.Detalhe + Reset
            }
        }
        c.Write(Truncar(linha, c.w-1))
    }
}

func DesenharLogs(c *Canvas, e *Estado) {
    c.Ir(7, 1)
    c.Write(Cinza + Bold + "LOGS" + Reset + "  " + Cinza + "Enter=recarrega | c=limpa | f=filtro" + Reset)
    if len(CacheLogs) == 0 {
        c.Ir(9, 1)
        c.Write(Cinza + "sem eventos. Enter para carregar logs recentes." + Reset)
        return
    }
    c.Ir(9, 1)
    c.Write(Cinza + fmt.Sprintf("eventos: %d", len(CacheLogs)) + Reset)
    maxLin := c.h - 11
    for i, r := range CacheLogs {
        if i >= maxLin {
            break
        }
        c.Ir(10+i, 1)
        pref := "  "
        if i == e.Indice {
            pref = Invert + "> " + Reset
        }
        c.Write(Truncar(pref+r.Texto, c.w-1))
    }
}

func DesenharConfig(c *Canvas, e *Estado) {
    c.Ir(7, 1)
    c.Write(Ciano + Bold + "CONFIG" + Reset + "  " + Cinza + "Enter=alterna | s=salva config" + Reset)
    c.Ir(9, 1)
    c.Write(Cinza + "configuracoes:" + Reset)
    chaves := []string{"modo", "sessao_auto", "operador", "fantasma", "timeout_run"}
    for i, k := range chaves {
        c.Ir(10+i, 1)
        pref := "  "
        if i == e.Indice {
            pref = Invert + "> " + Reset
        }
        linha := pref + k + " = " + Bold + Configuracoes[k] + Reset
        c.Write(Truncar(linha, c.w-1))
    }
}

func DesenharSala(c *Canvas, e *Estado) {
    switch e.SalaAtual {
    case "recon":
        DesenharRecon(c, e)
    case "exploits":
        DesenharExploits(c, e)
    case "sessions":
        DesenharSessions(c, e)
    case "cadeia":
        DesenharCadeia(c, e)
    case "manifesto":
        DesenharManifesto(c, e)
    case "credenciais":
        DesenharCredenciais(c, e)
    case "logs":
        DesenharLogs(c, e)
    case "config":
        DesenharConfig(c, e)
    default:
        c.Ir(7, 1)
        c.Write(Cinza + "sala " + e.SalaAtual + " — proxima entrega" + Reset)
    }
}

func Render(e *Estado) {
    w, h := Dimensoes()
    e.Largura = w
    e.Altura = h
    c := NovoCanvas(w, h)
    DesenharHeader(c, e)
    DesenharMenu(c, e)
    DesenharBreadcrumb(c, e)
    DesenharSala(c, e)
    DesenharStatus(c, e)
    c.Flush()
}

func indiceSala(nome string) int {
    for i, s := range Salas {
        if s == nome {
            return i
        }
    }
    return 0
}

func ChamarRun(cmd string, alvo string) map[string]interface{} {
    if _, err := os.Stat(RunBin); err != nil {
        return map[string]interface{}{"ok": false, "motivo": "run_ausente"}
    }
    req := map[string]interface{}{"op": "executar", "cmd": cmd}
    if alvo != "" {
        req["args"] = map[string]string{"alvo": alvo}
    }
    b, _ := json.Marshal(req)
    c := exec.Command(RunBin)
    c.Dir = BaseDir
    c.Stdin = strings.NewReader(string(b) + "\n")
    out, err := c.Output()
    if err != nil {
        return map[string]interface{}{"ok": false, "motivo": "run_exec_falhou"}
    }
    var resp map[string]interface{}
    if err := json.Unmarshal(out, &resp); err != nil {
        return map[string]interface{}{"ok": false, "motivo": "resposta_invalida"}
    }
    return resp
}

func LerTecla(ch <-chan byte, timeout time.Duration) (string, bool) {
    select {
    case b, ok := <-ch:
        if !ok {
            return "QUIT", true
        }
        if b == 0x1b {
            seq := []byte{b}
            for i := 0; i < 2; i++ {
                select {
                case nb, ok := <-ch:
                    if !ok {
                        return string(seq), true
                    }
                    seq = append(seq, nb)
                case <-time.After(15 * time.Millisecond):
                    return string(seq), true
                }
            }
            return string(seq), true
        }
        return string([]byte{b}), true
    case <-time.After(timeout):
        return "", false
    }
}

func ProcessarTecla(e *Estado, k string) bool {
    switch k {
    case "QUIT", "\x03", "\x04", "\x11":
        return false
    case "\t", "\x14":
        idx := indiceSala(e.SalaAtual)
        idx = (idx + 1) % len(Salas)
        e.SalaAtual = Salas[idx]
        e.Indice = 0
        e.Status = ""
    case "\x1b[Z":
        idx := indiceSala(e.SalaAtual)
        idx = (idx - 1 + len(Salas)) % len(Salas)
        e.SalaAtual = Salas[idx]
        e.Indice = 0
        e.Status = ""
    case "\x1b[A":
        if e.Indice > 0 {
            e.Indice--
        }
    case "\x1b[B":
        max := 0
        switch e.SalaAtual {
        case "recon":
            max = len(CacheRecon) - 1
        case "exploits":
            max = len(CacheExploits) - 1
        case "sessions":
            max = len(CacheSessions) - 1
        case "cadeia":
            max = len(CacheCadeia) - 1
        case "manifesto":
            max = len(CacheManifesto) - 1
        case "credenciais":
            max = len(CacheCredenciais) - 1
        case "logs":
            max = len(CacheLogs) - 1
        case "config":
            max = 4
        }
        if e.Indice < max {
            e.Indice++
        }
    case "\r", "\n":
        ProcessarEnter(e)
    case "s":
        if e.SalaAtual == "config" {
            SalvarSessao(e)
        }
    case "\x13":
        SalvarSessao(e)
    }
    return true
}

func ProcessarEnter(e *Estado) {
    switch e.SalaAtual {
    case "recon":
        if len(CacheRecon) == 0 {
            e.Status = "escanear 127.0.0.1..."
            resp := ChamarRun("analise", "127.0.0.1")
            if ok, _ := resp["ok"].(bool); ok {
                CacheRecon = []Resultado{{Texto: "127.0.0.1", Detalhe: "local", Ativo: true}}
                e.Status = "scan ok"
            } else {
                e.Status = "scan falhou: " + obterString(resp, "motivo")
            }
            return
        }
        r := CacheRecon[e.Indice]
        e.AlvoAtual = r.Texto
        e.Status = "alvo: " + r.Texto
    case "exploits":
        if len(CacheExploits) == 0 {
            e.Status = "listando exploits..."
            resp := ChamarRun("analise", "")
            _ = resp
            CacheExploits = []Resultado{
                {Texto: "exploit tplink", Detalhe: "CVE-2023-1389", Ativo: true},
                {Texto: "exploit dlink", Detalhe: "CVE-2024-3273", Ativo: true},
                {Texto: "exploit tenda7795", Detalhe: "CVE-2025-7795", Ativo: true},
                {Texto: "exploit arcadyan", Detalhe: "CVE-2021-20090", Ativo: true},
                {Texto: "exploit iptime", Detalhe: "CVE-2025-55423", Ativo: true},
                {Texto: "exploit tenda29384", Detalhe: "CVE-2025-29384", Ativo: true},
            }
            e.Status = "6 exploits listados"
            return
        }
        r := CacheExploits[e.Indice]
        if e.AlvoAtual == "" {
            e.Status = "defina alvo primeiro (sala recon)"
            return
        }
        e.Status = "executando " + r.Texto + "..."
        resp := ChamarRun(r.Texto, e.AlvoAtual)
        e.Status = "→ " + r.Texto + " | " + resumoMapa(resp)
    case "sessions":
        if len(CacheSessions) == 0 {
            CarregarSessoes()
            if len(CacheSessions) == 0 {
                e.Status = "sem sessoes salvas"
            } else {
                e.Status = fmt.Sprintf("%d sessoes carregadas", len(CacheSessions))
            }
            return
        }
        r := CacheSessions[e.Indice]
        e.SessaoNome = r.Texto
        e.Status = "sessao selecionada: " + r.Texto
    case "cadeia":
        if len(CacheCadeia) == 0 {
            resp := ChamarRun("cadeia", "")
            if resp != nil {
                CacheCadeia = ListaCadeia()
            }
            e.Status = fmt.Sprintf("%d templates", len(CacheCadeia))
            return
        }
        r := CacheCadeia[e.Indice]
        if e.AlvoAtual == "" {
            e.Status = "defina alvo primeiro (recon)"
            return
        }
        e.Status = "executando cadeia " + r.Texto + "..."
        resp := ChamarRun("cadeia", e.AlvoAtual)
        e.Status = "→ " + r.Texto + " | " + resumoMapa(resp)
    case "manifesto":
        if len(CacheManifesto) == 0 {
            CacheManifesto = ListaManifestos()
            e.Status = fmt.Sprintf("%d manifestos", len(CacheManifesto))
            return
        }
        r := CacheManifesto[e.Indice]
        e.Status = "aplicando " + r.Texto + "..."
        resp := ChamarRun("manifesto apply "+r.Texto, "")
        e.Status = "→ " + r.Texto + " | " + resumoMapa(resp)
    case "credenciais":
        if e.AlvoAtual == "" {
            e.Status = "defina alvo primeiro (recon)"
            return
        }
        e.Status = "buscando credenciais de " + e.AlvoAtual + "..."
        resp := ChamarRun("cred", e.AlvoAtual)
        if ok, _ := resp["ok"].(bool); ok {
            CacheCredenciais = ExtrairCredenciais(resp)
            e.Status = fmt.Sprintf("%d credenciais", len(CacheCredenciais))
        } else {
            e.Status = "→ cred | " + resumoMapa(resp)
        }
    case "logs":
        CacheLogs = CarregarLogs()
        e.Status = fmt.Sprintf("%d eventos", len(CacheLogs))
    case "config":
        chaves := []string{"modo", "sessao_auto", "operador", "fantasma", "timeout_run"}
        if e.Indice < len(chaves) {
            k := chaves[e.Indice]
            if Configuracoes[k] == "true" {
                Configuracoes[k] = "false"
            } else if Configuracoes[k] == "false" {
                Configuracoes[k] = "true"
            }
            e.Status = k + " = " + Configuracoes[k]
        }
    }
}

func CarregarSessoes() {
    req := `{"op":"sessao_listar"}`
    c := exec.Command(StateBin)
    c.Dir = BaseDir
    c.Stdin = strings.NewReader(req + "\n")
    out, err := c.Output()
    if err != nil {
        return
    }
    var resp struct {
        Sessoes []struct {
            Nome    string `json:"nome"`
            Tamanho int64  `json:"tamanho"`
            IdadeS  int64  `json:"idade_s"`
        } `json:"sessoes"`
    }
    if err := json.Unmarshal(out, &resp); err != nil {
        return
    }
    CacheSessions = nil
    for _, s := range resp.Sessoes {
        CacheSessions = append(CacheSessions, Resultado{
            Texto:   s.Nome,
            Detalhe: fmt.Sprintf("%d bytes, %ds", s.Tamanho, s.IdadeS),
            Ativo:   true,
        })
    }
}

func ListaCadeia() []Resultado {
    cmd := exec.Command("python3", "-c", `
import sys, json
sys.path.insert(0, "`+BaseDir+`")
from Cadeia import Cadeia
r = Cadeia.Templates()
print(json.dumps([{"nome": t["nome"], "descricao": t.get("descricao", "")} for t in r.get("templates", [])]))
`)
    cmd.Dir = BaseDir
    out, err := cmd.Output()
    if err != nil {
        return nil
    }
    var ts []struct {
        Nome      string `json:"nome"`
        Descricao string `json:"descricao"`
    }
    if err := json.Unmarshal(out, &ts); err != nil {
        return nil
    }
    var res []Resultado
    for _, t := range ts {
        res = append(res, Resultado{Texto: t.Nome, Detalhe: t.Descricao, Ativo: true})
    }
    return res
}

func ListaManifestos() []Resultado {
    dir := filepath.Join(os.Getenv("HOME"), ".console", "manifests")
    entradas, err := os.ReadDir(dir)
    if err != nil {
        return nil
    }
    var res []Resultado
    for _, e := range entradas {
        if e.IsDir() || !strings.HasSuffix(e.Name(), ".json") {
            continue
        }
        nome := strings.TrimSuffix(e.Name(), ".json")
        info, _ := e.Info()
        tam := int64(0)
        if info != nil {
            tam = info.Size()
        }
        res = append(res, Resultado{Texto: nome, Detalhe: fmt.Sprintf("%d bytes", tam), Ativo: true})
    }
    return res
}

func ExtrairCredenciais(resp map[string]interface{}) []Resultado {
    var out []Resultado
    if r, ok := resp["resultado"].(map[string]interface{}); ok {
        if creds, ok := r["credenciais"].([]interface{}); ok {
            for _, c := range creds {
                if m, ok := c.(map[string]interface{}); ok {
                    u, _ := m["user"].(string)
                    p, _ := m["pass"].(string)
                    if u != "" {
                        out = append(out, Resultado{Texto: u + " : " + p, Detalhe: "", Ativo: true})
                    }
                }
            }
        }
    }
    return out
}

func CarregarLogs() []Resultado {
    dir := filepath.Join(BaseDir, "logs")
    entradas, err := os.ReadDir(dir)
    if err != nil {
        return nil
    }
    var arquivos []string
    for _, e := range entradas {
        if !e.IsDir() && strings.HasSuffix(e.Name(), ".jsonl") {
            arquivos = append(arquivos, filepath.Join(dir, e.Name()))
        }
    }
    if len(arquivos) == 0 {
        return nil
    }
    f, err := os.Open(arquivos[len(arquivos)-1])
    if err != nil {
        return nil
    }
    defer f.Close()
    var linhas []string
    buf := make([]byte, 1)
    linha := ""
    for {
        n, err := f.Read(buf)
        if err != nil || n == 0 {
            if linha != "" {
                linhas = append(linhas, linha)
            }
            break
        }
        if buf[0] == '\n' {
            if linha != "" {
                linhas = append(linhas, linha)
            }
            linha = ""
        } else {
            linha += string(buf[0])
        }
    }
    if len(linhas) > 100 {
        linhas = linhas[len(linhas)-100:]
    }
    var out []Resultado
    for _, l := range linhas {
        if len(l) > 200 {
            l = l[:200] + "…"
        }
        out = append(out, Resultado{Texto: l, Detalhe: "", Ativo: true})
    }
    return out
}

func SalvarSessao(e *Estado) {
    if e.SessaoNome == "" {
        ts := time.Now().Format("20060102_150405")
        e.SessaoNome = "console_" + ts
    }
    estado := map[string]interface{}{
        "sala_atual": e.SalaAtual,
        "alvo_atual": e.AlvoAtual,
        "modo":       e.Modo,
        "config":     Configuracoes,
        "historico":  []string{},
    }
    b, _ := json.Marshal(estado)
    req := fmt.Sprintf(`{"op":"sessao_salvar","nome":"%s","estado":%s}`, e.SessaoNome, string(b))
    c := exec.Command(StateBin)
    c.Dir = BaseDir
    c.Stdin = strings.NewReader(req + "\n")
    if _, err := c.Output(); err != nil {
        e.Status = "erro ao salvar sessao"
        return
    }
    e.Status = "sessao salva: " + e.SessaoNome
}

func obterString(m map[string]interface{}, k string) string {
    if v, ok := m[k].(string); ok {
        return v
    }
    return ""
}

func resumoMapa(m map[string]interface{}) string {
    if ok, _ := m["ok"].(bool); ok {
        total := 0
        if t, ok := m["total"].(float64); ok {
            total = int(t)
        }
        if total > 0 {
            return fmt.Sprintf("OK total=%d", total)
        }
        return "OK"
    }
    if s := obterString(m, "motivo"); s != "" {
        return "FALHA: " + s
    }
    return "FALHA"
}

func VerificarBase() error {
    faltas := []string{}
    for _, p := range []string{RunBin, StateBin} {
        if _, err := os.Stat(p); err != nil {
            faltas = append(faltas, filepath.Base(p))
        }
    }
    if len(faltas) > 0 {
        return fmt.Errorf("faltam: %s", strings.Join(faltas, ", "))
    }
    return nil
}

func RodarConsole() int {
    if err := VerificarBase(); err != nil {
        fmt.Fprintf(os.Stderr, "erro: %v\n", err)
        return 1
    }
    antigo := AbrirTerminal()
    defer FecharTerminal(antigo)

    teclas := make(chan byte, 64)
    go func() {
        buf := make([]byte, 1)
        for {
            n, err := os.Stdin.Read(buf)
            if err != nil || n == 0 {
                close(teclas)
                return
            }
            teclas <- buf[0]
        }
    }()

    e := NovoEstado()
    for e.Rodando {
        Render(e)
        k, ok := LerTecla(teclas, 50*time.Millisecond)
        if !ok {
            continue
        }
        if !ProcessarTecla(e, k) {
            e.Rodando = false
        }
    }
    return 0
}

func MostrarAjuda() {
    fmt.Println("uso: console [comando]")
    fmt.Println()
    fmt.Println("comandos:")
    fmt.Println("  bypass        abre o console (padrao)")
    fmt.Println("  ajuda         mostra esta ajuda")
    fmt.Println("  versao        mostra versao")
    fmt.Println()
    fmt.Println("atalhos no console:")
    fmt.Println("  Ctrl+T        proxima sala")
    fmt.Println("  Shift+Ctrl+T  sala anterior")
    fmt.Println("  ↑↓            navega")
    fmt.Println("  Enter         executa")
    fmt.Println("  Ctrl+S        salva sessao")
    fmt.Println("  Ctrl+Q        sai")
}

func Main() int {
    args := os.Args[1:]
    cmd := "bypass"
    if len(args) > 0 {
        cmd = args[0]
    }
    switch cmd {
    case "bypass", "":
        return RodarConsole()
    case "ajuda", "-h", "--help":
        MostrarAjuda()
        return 0
    case "versao", "-v", "--version":
        fmt.Printf("Console %s\n", Versao)
        return 0
    default:
        fmt.Fprintf(os.Stderr, "comando desconhecido: %s\n", cmd)
        MostrarAjuda()
        return 2
    }
}

func main() {
    os.Exit(Main())
}
