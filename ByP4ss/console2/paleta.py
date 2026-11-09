import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ideias import Ideias

CUR_INVERT = "\033[7m"
CUR_RESET = "\033[0m"
CUR_DIM = "\033[2m"
CUR_BOLD = "\033[1m"
CUR_CINZA = "\033[90m"
CUR_CIANO = "\033[36m"
CUR_VERDE = "\033[32m"
CUR_AMARELO = "\033[33m"
CUR_VERMELHO = "\033[31m"
CUR_MAGENTA = "\033[35m"

MAX_ITENS_VISIVEIS = 14
MAX_HISTORICO = 50


class CentralRapida:

    ATALHOS_PADRAO = [
        ("F1", "scan", "scan"),
        ("F2", "cred", "cred"),
        ("F3", "exploit", "exploit"),
        ("F4", "cadeia", "cadeia"),
        ("F5", "sessoes", "sessao"),
    ]

    def __init__(self, on_atalho=None):
        self.atalhos = list(CentralRapida.ATALHOS_PADRAO)
        self.on_atalho = on_atalho

    def Disparar(self, tecla):
        for f, nome, comando in self.atalhos:
            if tecla == f:
                if self.on_atalho:
                    self.on_atalho(comando, nome)
                return True
        return False

    def Render(self, caixa, linha_base):
        partes = []
        for f, nome, _ in self.atalhos:
            partes.append(f"{CUR_DIM}[{f}]{CUR_RESET} {CUR_CIANO}{nome}{CUR_RESET}")
        texto = " " + "  ".join(partes)
        caixa.DesenharLinha(linha_base, texto)
        return texto


class Paleta:

    TIPOS = ["comando", "alvo", "exploit", "cadeia", "sessao", "historico"]

    def __init__(self, caixa, on_enter=None, on_mudar_tipo=None):
        self.caixa = caixa
        self.on_enter = on_enter
        self.on_mudar_tipo = on_mudar_tipo
        self.tipo = "comando"
        self.query = ""
        self.itens_todos = []
        self.itens_filtrados = []
        self.selecionado = 0
        self.scroll = 0
        self.historico = []
        self.alvos_conhecidos = []
        self.sessoes_conhecidas = []
        self.exploits = self._ExploitsFixos()
        self.cadeias = self._CadeiasFixas()
        self.central = CentralRapida(on_atalho=self._AoAtalho)
        self.cursor_pisca = True
        self.ultimo_pisca = time.monotonic()
        self.CarregarTipo("comando")

    def _ExploitsFixos(self):
        return [
            {"id": "tplink", "nome": "TP-Link CVE-2023-1389", "tipo": "exploit", "descricao": "Command injection /cgi-bin/", "comando": "exploit", "args": ["tplink", "alvo"]},
            {"id": "dlink", "nome": "D-Link CVE-2024-3273", "tipo": "exploit", "descricao": "Auth bypass + injection", "comando": "exploit", "args": ["dlink", "alvo"]},
            {"id": "tenda7795", "nome": "Tenda CVE-2025-7795", "tipo": "exploit", "descricao": "DoS buffer overflow", "comando": "exploit", "args": ["tenda7795", "alvo"]},
            {"id": "arcadyan", "nome": "Arcadyan CVE-2021-20090", "tipo": "exploit", "descricao": "Traversal + injection", "comando": "exploit", "args": ["arcadyan", "alvo"]},
            {"id": "iptime", "nome": "ipTIME CVE-2025-55423", "tipo": "exploit", "descricao": "SSDP control URL", "comando": "exploit", "args": ["iptime", "alvo"]},
            {"id": "tenda29384", "nome": "Tenda CVE-2025-29384", "tipo": "exploit", "descricao": "MIPS stack overflow", "comando": "exploit", "args": ["tenda29384", "alvo"]},
        ]

    def _CadeiasFixas(self):
        return [
            {"id": "dlink_basico", "nome": "D-Link basico", "tipo": "cadeia", "descricao": "Auth bypass + reverse", "comando": "cadeia", "args": ["dlink_basico", "alvo"]},
            {"id": "tenda_overflow", "nome": "Tenda overflow", "tipo": "cadeia", "descricao": "MIPS overflow", "comando": "cadeia", "args": ["tenda_overflow", "alvo"]},
            {"id": "recon_auto", "nome": "Recon auto", "tipo": "cadeia", "descricao": "Analise + exploit auto", "comando": "cadeia", "args": ["recon_auto", "alvo"]},
            {"id": "scan_completo", "nome": "Scan completo", "tipo": "cadeia", "descricao": "scan + ssdp + httpauth", "comando": "cadeia", "args": ["scan_completo", "alvo"]},
        ]

    def CarregarTipo(self, tipo):
        if tipo not in Paleta.TIPOS:
            return False
        self.tipo = tipo
        self.query = ""
        self.selecionado = 0
        self.scroll = 0
        if tipo == "comando":
            self.itens_todos = [
                {"id": k, "nome": v["nome"], "tipo": v["tipo"], "descricao": v.get("descricao", ""), "comando": v["comando"], "args": v["args"]}
                for k, v in Ideias.Ataque().items()
            ]
        elif tipo == "alvo":
            self.itens_todos = [{"id": a, "nome": a, "tipo": "alvo", "descricao": "", "comando": "alvo", "args": []} for a in self.alvos_conhecidos]
        elif tipo == "exploit":
            self.itens_todos = list(self.exploits)
        elif tipo == "cadeia":
            self.itens_todos = list(self.cadeias)
        elif tipo == "sessao":
            self.itens_todos = [{"id": s, "nome": s, "tipo": "sessao", "descricao": "", "comando": "sessao", "args": []} for s in self.sessoes_conhecidas]
        elif tipo == "historico":
            self.itens_todos = [{"id": h["cmd"], "nome": h["cmd"], "tipo": "hist", "descricao": h.get("motivo", ""), "comando": h["cmd"], "args": []} for h in reversed(self.historico)]
        self._Filtrar()
        if self.on_mudar_tipo:
            self.on_mudar_tipo(tipo)
        return True

    def ProximoTipo(self):
        i = Paleta.TIPOS.index(self.tipo)
        self.CarregarTipo(Paleta.TIPOS[(i + 1) % len(Paleta.TIPOS)])

    def TipoAnterior(self):
        i = Paleta.TIPOS.index(self.tipo)
        self.CarregarTipo(Paleta.TIPOS[(i - 1 + len(Paleta.TIPOS)) % len(Paleta.TIPOS)])

    def _Filtrar(self):
        if not self.query:
            self.itens_filtrados = list(self.itens_todos)
        else:
            q = self.query.lower()
            self.itens_filtrados = []
            for it in self.itens_todos:
                txt = (it["id"] + " " + it["nome"] + " " + it.get("descricao", "") + " " + it["tipo"]).lower()
                if q in txt:
                    self.itens_filtrados.append(it)
        self.selecionado = 0
        self.scroll = 0

    def Mover(self, delta):
        if not self.itens_filtrados:
            return
        self.selecionado += delta
        if self.selecionado < 0:
            self.selecionado = 0
        if self.selecionado >= len(self.itens_filtrados):
            self.selecionado = len(self.itens_filtrados) - 1
        if self.selecionado < self.scroll:
            self.scroll = self.selecionado
        if self.selecionado >= self.scroll + MAX_ITENS_VISIVEIS:
            self.scroll = self.selecionado - MAX_ITENS_VISIVEIS + 1

    def Atual(self):
        if not self.itens_filtrados:
            return None
        if self.selecionado < 0 or self.selecionado >= len(self.itens_filtrados):
            return None
        return self.itens_filtrados[self.selecionado]

    def AdicionarAlvo(self, ip):
        if ip and ip not in self.alvos_conhecidos:
            self.alvos_conhecidos.append(ip)

    def AdicionarSessao(self, nome):
        if nome and nome not in self.sessoes_conhecidas:
            self.sessoes_conhecidas.append(nome)

    def RegistrarHistorico(self, cmd, motivo=""):
        self.historico.append({"cmd": cmd, "motivo": motivo, "ts": time.time()})
        if len(self.historico) > MAX_HISTORICO:
            self.historico = self.historico[-MAX_HISTORICO:]

    def _AoAtalho(self, comando, nome):
        item = {"id": nome, "nome": nome, "tipo": "atalho", "descricao": "", "comando": comando, "args": []}
        if self.on_enter:
            self.on_enter(item, self.query)

    def TeclaAtalho(self, tecla):
        return self.central.Disfarçar(tecla) if False else self.central.Disparar(tecla)

    def Tecla(self, tecla):
        if tecla == "\x1b[A":
            self.Mover(-1)
            return True
        if tecla == "\x1b[B":
            self.Mover(1)
            return True
        if tecla in ("\x1b[H",):
            self.selecionado = 0
            self.scroll = 0
            return True
        if tecla in ("\x1b[F",):
            self.selecionado = max(0, len(self.itens_filtrados) - 1)
            return True
        if tecla == "\t" or tecla == "\x14":
            self.ProximoTipo()
            return True
        if tecla == "\x1b[Z":
            self.TipoAnterior()
            return True
        if tecla == "\x7f" or tecla == "\x08":
            if self.query:
                self.query = self.query[:-1]
                self._Filtrar()
            return True
        if tecla in ("\r", "\n"):
            it = self.Atual()
            if it and self.on_enter:
                self.on_enter(it, self.query)
            return True
        if tecla == "\x1b":
            if self.query:
                self.query = ""
                self._Filtrar()
            return True
        if len(tecla) == 1 and 0x20 <= ord(tecla) < 0x7f:
            self.query += tecla
            self._Filtrar()
            return True
        return False

    def Autocompletar(self):
        it = self.Atual()
        if it:
            self.query = it["id"]
            self._Filtrar()
    def Tick(self):
        agora = time.monotonic()
        if agora - self.ultimo_pisca >= 0.5:
            self.cursor_pisca = not self.cursor_pisca
            self.ultimo_pisca = agora
            return True
        return False

    def Render(self):
        c = self.caixa

        # 1. Abas (linha 3)
        abas = []
        for t in self.TIPOS:
            if t == self.tipo:
                abas.append(f"{CUR_INVERT}{CUR_BOLD} {t} {CUR_RESET}")
            else:
                abas.append(f"{CUR_DIM} {t} {CUR_RESET}")
        c.DesenharLinha(3, " " + " ".join(abas))

        # 2. Input (linha 4)
        cursor = "█" if self.cursor_pisca else " "
        input_txt = f" Agent~Byp4ss# {CUR_CIANO}{self.query}{CUR_RESET}{cursor}"
        c.DesenharLinha(4, input_txt)

        # 3. Lista (linhas 6 a 19)
        for i in range(MAX_ITENS_VISIVEIS):
            c.LimparLinha(6 + i)

        inicio = self.scroll
        fim = min(inicio + MAX_ITENS_VISIVEIS, len(self.itens_filtrados))
        
        if not self.itens_filtrados:
            c.DesenharLinha(6, f"  {CUR_CINZA}(nenhum item){CUR_RESET}")
        else:
            for idx in range(inicio, fim):
                item = self.itens_filtrados[idx]
                linha = 6 + (idx - inicio)
                
                selecionado = (idx == self.selecionado)
                pref = "> " if selecionado else "  "
                cor = CUR_INVERT if selecionado else ""
                reset = CUR_RESET if selecionado else ""
                
                tipo_fmt = f"[{item['tipo']}]"
                id_fmt = f"{item['id']:15s}"
                nome_fmt = f"{item['nome'][:20]:20s}"
                desc_fmt = f"{CUR_DIM}{item.get('descricao', '')[:20]}{CUR_RESET}"
                
                texto = f"{pref}{cor}{tipo_fmt:14s} {id_fmt} {nome_fmt}{reset} {desc_fmt}"
                c.DesenharLinha(linha, texto)

            # Scroll indicator
            if len(self.itens_filtrados) > MAX_ITENS_VISIVEIS:
                pct = int((self.scroll / max(1, len(self.itens_filtrados) - MAX_ITENS_VISIVEIS)) * 100)
                c.DesenharLinha(5, f" {CUR_CINZA}scroll: {self.scroll}/{len(self.itens_filtrados)} ({pct}%){CUR_RESET}")

        # 4. Central Rápida (linha 18)
        self.central.Render(c, 18)

        # 5. Info (linha 19)
        info = f" tipo: {self.tipo} | itens: {len(self.itens_filtrados)} | alvos: {len(self.alvos_conhecidos)} | sessões: {len(self.sessoes_conhecidas)} "
        c.DesenharInfo(info)

    def RenderTitulo(self):
        self.caixa.DesenharTitulo(f"CBNC/ByP4ss v1.0 — {self.tipo}")


# ============================================================
# TESTES
# ============================================================

class CaixaMock:
    def __init__(self, largura=60, altura=20):
        self.largura = largura
        self.altura = altura
        self.linhas = {}
        self.titulo = ""
        self.info = ""
        self.rodape = ""

    def DesenharLinha(self, linha, texto, cor=None):
        self.linhas[linha] = texto

    def DesenharInfo(self, texto):
        self.info = texto

    def DesenharRodape(self, texto):
        self.rodape = texto

    def DesenharTitulo(self, titulo):
        self.titulo = titulo

    def LimparLinha(self, linha):
        self.linhas.pop(linha, None)


def TestePaleta():
    print("=== TESTE PALETA ===\n")

    c = CaixaMock(60, 20)
    p = Paleta(c)

    print("[1] CarregarTipo inicial (comando)")
    assert p.tipo == "comando"
    assert len(p.itens_todos) == 15, f"esperado 15, obtido {len(p.itens_todos)}"
    print(f"    tipo: {p.tipo}, itens: {len(p.itens_todos)}")

    print("\n[2] Filtrar")
    p.query = "scan"
    p._Filtrar()
    assert len(p.itens_filtrados) >= 1
    print(f"    'scan' -> {len(p.itens_filtrados)} itens")
    p.query = ""
    p._Filtrar()
    assert len(p.itens_filtrados) == 15

    print("\n[3] Mover")
    p.Mover(3)
    assert p.selecionado == 3
    p.Mover(-10)
    assert p.selecionado == 0
    p.Mover(100)
    assert p.selecionado == 14
    print(f"    após Mover(100): {p.selecionado} (max)")

    print("\n[4] Proximo/Anterior Tipo")
    p.CarregarTipo("comando")
    p.ProximoTipo()
    assert p.tipo == "alvo"
    p.ProximoTipo()
    assert p.tipo == "exploit"
    p.TipoAnterior()
    assert p.tipo == "alvo"
    print("    ciclos de tipo OK")

    print("\n[5] Teclas: Tab (autocomplete), Ctrl+T (mudar tipo)")
    p.CarregarTipo("comando")
    p.query = "expl"
    p._Filtrar()
    p.selecionado = 0
    p.Autocompletar()
    assert p.query != "", p.query
    print(f"    Autocompletar -> query: '{p.query}'")
    
    tipo_antes = p.tipo
    p.Tecla("\x14") # ctrl+t muda tipo
    assert p.tipo != tipo_antes, f"Ctrl+T nao mudou tipo (era {tipo_antes}, ficou {p.tipo})"
    print(f"    Ctrl+T -> tipo: {p.tipo}")

    print("\n[6] TeclaAtalho (F1-F5)")
    resultados = []
    p.on_enter = lambda item, q: resultados.append(item)
    p.TeclaAtalho("F1")
    p.TeclaAtalho("F2")
    p.TeclaAtalho("F3")
    assert len(resultados) == 3
    print(f"    F1-F3 -> {[r['comando'] for r in resultados]}")

    print("\n[7] Render (mock)")
    p.CarregarTipo("comando")
    p.Render()
    assert 3 in c.linhas, "aba nao renderizada"
    assert 4 in c.linhas, "input nao renderizado"
    assert 6 in c.linhas, "item 0 nao renderizado"
    assert 18 in c.linhas, "central nao renderizada"
    assert "tipo: comando" in c.info
    print("    ok, linhas renderizadas")
    for i in [3, 4, 6, 7, 18]:
        if i in c.linhas:
            texto_limpo = c.linhas[i]
            import re
            texto_limpo = re.sub(r"\033\[[0-9;]*[a-zA-Z]", "", texto_limpo)
            print(f"    [{i}] {texto_limpo[:60]}")

    print("\nTESTE OK")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        TestePaleta()
    else:
        print("uso: python3 paleta.py teste")
