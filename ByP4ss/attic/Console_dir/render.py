import os
import re
import shutil
import subprocess
import sys
import time


CORES = {
    "reset":  "\033[0m",
    "bold":   "\033[1m",
    "dim":    "\033[2m",
    "invert": "\033[7m",
    "cinza":  "\033[90m",
    "ciano":  "\033[36m",
    "verde":  "\033[32m",
    "amarelo":"\033[33m",
    "vermelho":"\033[31m",
    "magenta":"\033[35m",
    "azul":   "\033[34m",
    "hide":   "\033[?25l",
    "show":   "\033[?25h",
    "clear":  "\033[2J\033[H",
}


SALAS = ["recon", "exploits", "sessions", "cadeia",
         "manifesto", "credenciais", "logs", "config"]

CORES_SALA = {
    "recon":       "azul",
    "exploits":    "amarelo",
    "sessions":    "verde",
    "cadeia":      "magenta",
    "manifesto":   "ciano",
    "credenciais": "verde",
    "logs":        "cinza",
    "config":      "ciano",
}

RE_ANSI = re.compile(r"\033\[[0-9;?]*[a-zA-Z]")


def Cor(nome):
    return CORES.get(nome, "")


def Colorir(texto, cor):
    return Cor(cor) + texto + Cor("reset")


def Visivel(s):
    return len(RE_ANSI.sub("", s))


def Truncar(s, maximo):
    if maximo < 2:
        return ""
    if Visivel(s) <= maximo:
        return s
    vis = 0
    esc = False
    out = []
    for ch in s:
        if ch == "\033":
            esc = True
            out.append(ch)
            continue
        if esc:
            out.append(ch)
            if ch in "mKHJ":
                esc = False
            continue
        if vis >= maximo - 1:
            out.append("…")
            out.append(Cor("reset"))
            return "".join(out)
        out.append(ch)
        vis += 1
    return "".join(out)


def Dimensoes():
    try:
        t = shutil.get_terminal_size()
        w, h = t.columns, t.lines
    except Exception:
        w, h = 80, 24
    if w < 40:
        w = 40
    if h < 10:
        h = 10
    return w, h


def Ir(linha, coluna):
    return f"\033[{linha};{coluna}H"


class Canvas:

    def __init__(self, w=None, h=None):
        self.w, self.h = Dimensoes() if w is None or h is None else (w, h)
        self.buf = [CORES["hide"], CORES["clear"]]

    def Ir(self, linha, coluna):
        self.buf.append(Ir(linha, coluna))

    def Write(self, s):
        self.buf.append(s)

    def LinhaHorizontal(self, linha, char="─"):
        self.Ir(linha, 1)
        self.Write(char * (self.w - 1))

    def Preenchido(self, linha, coluna, esq, dir_, largura):
        self.Ir(linha, coluna)
        vis_esq = Visivel(esq)
        vis_dir = Visivel(dir_)
        gap = largura - vis_esq - vis_dir
        if gap < 1:
            self.Write(Truncar(esq + dir_, largura))
            return
        self.Write(esq)
        self.Write(" " * gap)
        self.Write(dir_)

    def Flush(self):
        self.buf.append(CORES["show"])
        sys.stdout.write("".join(self.buf))
        sys.stdout.flush()
        self.buf = []


def DesenharHeader(c, estado):
    titulo = Colorir("BYPASS", "bold") + " v1.0"
    idx = SALAS.index(estado.get("sala", "recon")) + 1
    direita = f"[{idx}/{len(SALAS)} {estado.get('sala', 'recon')}]"
    c.Preenchido(1, 1, " " + titulo, " " + direita + " ", c.w - 1)
    c.LinhaHorizontal(2)


def DesenharMenu(c, estado):
    c.Ir(3, 1)
    partes = []
    for sala in SALAS:
        cor = CORES_SALA.get(sala, "cinza")
        if sala == estado.get("sala"):
            partes.append(Colorir(" " + sala.upper() + " ", cor))
            partes[-1] = Cor("invert") + Cor("bold") + partes[-1] + Cor("reset")
        else:
            partes.append(Colorir(" " + sala + " ", cor) if False else Cor(cor) + Cor("dim") + " " + sala + " " + Cor("reset"))
    linha = " ".join(partes)
    c.Write(Truncar(linha, c.w - 1))
    c.LinhaHorizontal(4)


def DesenharBreadcrumb(c, estado):
    cor = CORES_SALA.get(estado.get("sala", "recon"), "cinza")
    c.Ir(5, 1)
    c.Write(Colorir("BYPASS", "bold") + " > " + Colorir(estado.get("sala", "recon"), cor))


def DesenharStatus(c, estado):
    c.LinhaHorizontal(c.h - 1)
    c.Ir(c.h, 1)
    status = estado.get("status", "")
    if status:
        c.Write(Truncar(" " + Cor("dim") + status + Cor("reset"), c.w - 1))
        return
    partes = []
    partes.append(Colorir("[modo " + estado.get("modo", "local") + "]", "cinza"))
    if estado.get("alvo"):
        partes.append(Colorir("[alvo " + estado["alvo"] + "]", "ciano"))
    if estado.get("sessao"):
        partes.append(Colorir("[sessao " + estado["sessao"] + "]", "verde"))
    if estado.get("tarefas_ativas"):
        partes.append(Colorir(f"[{estado['tarefas_ativas']} rodando]", "amarelo"))
    esq = " " + " ".join(partes)
    dir_ = Cor("dim") + "Ctrl+T sala | ↑↓ | Enter | / prompt | Ctrl+Q sai" + Cor("reset")
    c.Preenchido(c.h, 1, esq, " " + dir_ + " ", c.w - 1)


def Render(estado):
    c = Canvas()
    DesenharHeader(c, estado)
    DesenharMenu(c, estado)
    DesenharBreadcrumb(c, estado)
    Conteudo(c, estado)
    DesenharStatus(c, estado)
    c.Flush()


def Conteudo(c, estado):
    sala = estado.get("sala", "recon")
    cor = CORES_SALA.get(sala, "cinza")
    c.Ir(7, 1)
    titulo = " " + sala.upper() + " "
    c.Write(Cor(cor) + Cor("bold") + titulo + Cor("reset") + "  " +
            Cor("dim") + estado.get("dica", "") + Cor("reset"))
    itens = estado.get("itens", [])
    if not itens:
        c.Ir(9, 1)
        c.Write(Cor("cinza") + "  (vazio)" + Cor("reset"))
        return
    idx = estado.get("indice", 0)
    max_lin = c.h - 11
    for i, item in enumerate(itens[:max_lin]):
        c.Ir(10 + i, 1)
        pref = "  "
        if i == idx:
            pref = Cor("invert") + " > " + Cor("reset")
        linha = pref + item.get("texto", "")
        detalhe = item.get("detalhe", "")
        if detalhe:
            pad = c.w - 1 - Visivel(linha) - Visivel(detalhe) - 1
            if pad > 0:
                linha += " " * pad + Cor("dim") + detalhe + Cor("reset")
        c.Write(Truncar(linha, c.w - 1))


def TesteRender():
    print("=== TESTE RENDER ===\n")

    print("[1] Visivel")
    assert Visivel("abc") == 3
    assert Visivel("\033[1mabc\033[0m") == 3
    assert Visivel("\033[?25labc\033[?25h") == 3
    print("    ok")

    print("[2] Truncar")
    assert Truncar("abc", 10) == "abc"
    t = Truncar("abcdefghij", 5)
    assert Visivel(t) <= 5
    assert "…" in t
    print(f"    'abcdefghij' (10) -> '{t}' (visible={Visivel(t)})")

    print("[3] Dimensoes")
    w, h = Dimensoes()
    print(f"    {w}x{h}")
    assert w >= 40 and h >= 10

    print("[4] Canvas basico")
    c = Canvas(80, 24)
    c.Ir(1, 1)
    c.Write("teste")
    c.LinhaHorizontal(2)
    c.Flush()
    print("    ok (output acima)")

    print("[5] Render com estado")
    estado = {
        "sala": "recon",
        "modo": "local",
        "alvo": "192.168.0.2",
        "sessao": "auto_20261107",
        "dica": "Enter=scan",
        "itens": [
            {"texto": "192.168.0.1", "detalhe": "roteador"},
            {"texto": "192.168.0.2", "detalhe": "dlink"},
            {"texto": "192.168.0.5", "detalhe": "notebook"},
        ],
        "indice": 1,
    }
    Render(estado)
    print("\n    ok (render acima)")

    print("\nTESTE OK")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        TesteRender()
    else:
        print("uso: python3 render.py teste")
