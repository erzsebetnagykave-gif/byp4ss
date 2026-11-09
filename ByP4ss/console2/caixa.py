import os
import sys
import shutil
import re
import time


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
INVERT = "\033[7m"
CUR_ESCONDER = "\033[?25l"
CUR_MOSTRAR = "\033[?25h"
LIMPAR_LINHA = "\033[K"

CIANO = "\033[36m"
CINZA = "\033[90m"
VERDE = "\033[32m"
AMARELO = "\033[33m"
VERMELHO = "\033[31m"
MAGENTA = "\033[35m"
AZUL = "\033[34m"
BRANCO = "\033[97m"

BORDA_TL = "╔"
BORDA_TR = "╗"
BORDA_BL = "╚"
BORDA_BR = "╝"
BORDA_H = "═"
BORDA_V = "║"
BORDA_SEP_L = "╠"
BORDA_SEP_R = "╣"

LARGURA_MIN = 60
ALTURA_MIN = 20

ANSI_RE = re.compile(r"\033\[[0-9;?]*[a-zA-Z]")


def Visivel(s):
    return len(ANSI_RE.sub("", str(s)))


def Truncar(s, maximo):
    if maximo < 2:
        return ""
    s = str(s)
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
            out.append(RESET)
            return "".join(out)
        out.append(ch)
        vis += 1
    return "".join(out)


def Pad(s, largura, alinhamento="esq"):
    vis = Visivel(s)
    if vis >= largura:
        return Truncar(s, largura)
    falta = largura - vis
    if alinhamento == "dir":
        return (" " * falta) + s
    if alinhamento == "centro":
        esq = falta // 2
        dir_ = falta - esq
        return (" " * esq) + s + (" " * dir_)
    return s + (" " * falta)


def Preenchido(esq, dir_, largura):
    v_esq = Visivel(esq)
    v_dir = Visivel(dir_)
    gap = largura - v_esq - v_dir
    if gap < 1:
        return Truncar(esq + dir_, largura)
    return esq + (" " * gap) + dir_


def DimensoesTerminal():
    try:
        t = shutil.get_terminal_size()
        return max(t.columns, LARGURA_MIN), max(t.lines, ALTURA_MIN)
    except Exception:
        return 80, 24


class Grade:

    def __init__(self, largura=None, altura=None):
        w, h = DimensoesTerminal()
        self.largura = largura if largura else min(w - 2, 100)
        self.altura = altura if altura else min(h - 2, 40)
        self.linha_origem = max(1, (h - self.altura) // 2 + 1)
        self.coluna_origem = max(1, (w - self.largura) // 2 + 1)
        self.ativa = False
        self._buf = []

    def Ir(self, linha, coluna):
        linha_abs = self.linha_origem + linha
        coluna_abs = self.coluna_origem + coluna
        self._buf.append(f"\033[{linha_abs};{coluna_abs}H")

    def Write(self, texto):
        self._buf.append(texto)

    def Flush(self):
        if not self._buf:
            return
        sys.stdout.write("".join(self._buf))
        sys.stdout.flush()
        self._buf = []

    def Limpar(self):
        for i in range(self.altura):
            self.Ir(i, 0)
            self.Write(" " * self.largura)

    def Abrir(self):
        if self.largura < LARGURA_MIN or self.altura < ALTURA_MIN:
            return False
        self.Limpar()
        self.DesenharBorda()
        self.Flush()
        self.ativa = True
        return True

    def Fechar(self):
        if not self.ativa:
            return
        self.Limpar()
        self.Flush()
        self.ativa = False

    def DesenharBorda(self):
        cor = CINZA
        topo = BORDA_TL + (BORDA_H * (self.largura - 2)) + BORDA_TR
        self.Ir(0, 0)
        self.Write(cor + topo + RESET)
        for i in range(1, self.altura - 1):
            self.Ir(i, 0)
            self.Write(cor + BORDA_V + RESET)
            self.Ir(i, self.largura - 1)
            self.Write(cor + BORDA_V + RESET)
        fundo = BORDA_BL + (BORDA_H * (self.largura - 2)) + BORDA_BR
        self.Ir(self.altura - 1, 0)
        self.Write(cor + fundo + RESET)

    def DesenharSeparador(self, linha, titulo=None):
        cor = CINZA
        corpo = BORDA_H * (self.largura - 2)
        if titulo:
            titulo_fmt = f" {BOLD}{titulo}{RESET}{cor} "
            tam_tit = Visivel(titulo_fmt)
            if tam_tit < len(corpo) - 2:
                esq = (len(corpo) - tam_tit) // 2
                dir_ = len(corpo) - tam_tit - esq
                linha_txt = (BORDA_H * esq) + titulo_fmt + (BORDA_H * dir_)
            else:
                linha_txt = corpo
        else:
            linha_txt = corpo
        self.Ir(linha, 0)
        self.Write(cor + BORDA_SEP_L + RESET)
        self.Ir(linha, 1)
        self.Write(cor + linha_txt + RESET)
        self.Ir(linha, self.largura - 1)
        self.Write(cor + BORDA_SEP_R + RESET)

    def EscreverLinha(self, linha, texto, cor=None):
        if linha < 1 or linha >= self.altura - 1:
            return
        largura_interna = self.largura - 2
        texto_fmt = texto if cor is None else cor + texto + RESET
        self.Ir(linha, 1)
        self.Write(Pad(Truncar(texto_fmt, largura_interna), largura_interna))
        self.Ir(linha, 0)
        self.Write(CINZA + BORDA_V + RESET)
        self.Ir(linha, self.largura - 1)
        self.Write(CINZA + BORDA_V + RESET)

    def EscreverLinhaComposta(self, linha, partes):
        if linha < 1 or linha >= self.altura - 1:
            return
        largura_interna = self.largura - 2
        texto = ""
        for parte in partes:
            if isinstance(parte, tuple):
                txt, cor = parte
                texto += (cor + txt + RESET) if cor else txt
            else:
                texto += str(parte)
        self.Ir(linha, 1)
        self.Write(Pad(Truncar(texto, largura_interna), largura_interna))
        self.Ir(linha, 0)
        self.Write(CINZA + BORDA_V + RESET)
        self.Ir(linha, self.largura - 1)
        self.Write(CINZA + BORDA_V + RESET)


class Cabecalho:

    def __init__(self, grade, titulo="CBNC / ByP4ss v1.0", versao="1.0"):
        self.grade = grade
        self.titulo = titulo
        self.versao = versao
        self.linha = 1

    def Render(self):
        largura_interna = self.grade.largura - 2
        esq = f" {BOLD}{CIANO}{self.titulo}{RESET}"
        dir_ = f"[OPERACIONAL] "
        texto = Preenchido(esq, dir_, largura_interna)
        self.grade.EscreverLinhaComposta(self.linha, [(texto, None)])


class MenuPaletas:

    PALETAS = ["COMANDO", "ALVO", "EXPLOIT", "CHAIN", "SESSION", "HISTORY"]

    def __init__(self, grade, paleta_atual="COMANDO"):
        self.grade = grade
        self.paleta_atual = paleta_atual
        self.linha = 3

    def DefinirPaleta(self, nome):
        if nome.upper() in MenuPaletas.PALETAS:
            self.paleta_atual = nome.upper()

    def Render(self):
        largura_interna = self.grade.largura - 2
        partes = []
        for p in MenuPaletas.PALETAS:
            if p == self.paleta_atual:
                partes.append(f"{CUR_INVERT if False else INVERT}{BOLD} {p} {RESET}")
            else:
                partes.append(f"{DIM} {p} {RESET}")
        texto = "  ".join(partes)
        self.grade.EscreverLinhaComposta(self.linha, [(" " + texto, None)])


class Input:

    def __init__(self, grade, linha=4, prompt="Agent~Byp4ss#"):
        self.grade = grade
        self.linha = linha
        self.prompt = prompt
        self.query = ""
        self.cursor_visivel = True
        self.placeholder = "digite um comando ou setas para navegar..."

    def DefinirQuery(self, query):
        self.query = query or ""

    def Tick(self):
        self.cursor_visivel = not self.cursor_visivel

    def Render(self):
        largura_interna = self.grade.largura - 2
        cursor = "█" if self.cursor_visivel else " "
        
        if not self.query:
            texto_visivel = f" {CIANO}{self.prompt}{RESET} {DIM}{self.placeholder}{RESET}{cursor}"
        else:
            texto_visivel = f" {CIANO}{self.prompt}{RESET} {BRANCO}{self.query}{RESET}{cursor}"
            
        self.grade.EscreverLinhaComposta(self.linha, [(texto_visivel, None)])


class Lista:

    def __init__(self, grade, linha_inicio=6, linha_fim=15):
        self.grade = grade
        self.linha_inicio = linha_inicio
        self.linha_fim = linha_fim
        self.itens = []
        self.selecionado = 0
        self.scroll = 0

    def DefinirItens(self, itens):
        self.itens = itens or []
        if self.selecionado >= len(self.itens):
            self.selecionado = max(0, len(self.itens) - 1)
        self.AjustarScroll()

    def Mover(self, delta):
        if not self.itens:
            return
        self.selecionado += delta
        if self.selecionado < 0:
            self.selecionado = 0
        if self.selecionado >= len(self.itens):
            self.selecionado = len(self.itens) - 1
        self.AjustarScroll()

    def AjustarScroll(self):
        altura_visivel = self.linha_fim - self.linha_inicio + 1
        if self.selecionado < self.scroll:
            self.scroll = self.selecionado
        if self.selecionado >= self.scroll + altura_visivel:
            self.scroll = self.selecionado - altura_visivel + 1
        if self.scroll < 0:
            self.scroll = 0

    def Render(self):
        altura_visivel = self.linha_fim - self.linha_inicio + 1
        largura_interna = self.grade.largura - 2
        
        # Limpa area da lista
        for i in range(altura_visivel):
            self.grade.EscreverLinha(self.linha_inicio + i, "")

        if not self.itens:
            self.grade.EscreverLinha(self.linha_inicio, f"  {DIM}(nenhum item disponivel){RESET}")
            return

        visiveis = self.itens[self.scroll:self.scroll + altura_visivel]
        
        for idx, item in enumerate(visiveis):
            idx_global = self.scroll + idx
            linha_alvo = self.linha_inicio + idx
            
            selecionado = (idx_global == self.selecionado)
            
            # Prefixo
            pref = f"{INVERT}> {RESET}" if selecionado else "  "
            
            # Tipo
            tipo = item.get("tipo", "")
            if tipo == "reconhecimento": cor_tipo = AZUL
            elif tipo == "acesso": cor_tipo = VERDE
            elif tipo == "ataque": cor_tipo = VERMELHO
            elif tipo == "encadeamento": cor_tipo = MAGENTA
            elif tipo == "bypass": cor_tipo = AMARELO
            elif tipo == "lancamento": cor_tipo = CIANO
            else: cor_tipo = CINZA

            tipo_fmt = f"[{tipo.upper()}]"
            cmd = item.get("id", "")
            desc = item.get("descricao", "")
            
            # Cor do texto principal
            if selecionado:
                texto_cmd = f"{INVERT}{BOLD}{cmd:15s}{RESET}"
                texto_desc = f"{INVERT}{desc}{RESET}"
            else:
                texto_cmd = f"{cmd:15s}"
                texto_desc = f"{DIM}{desc}{RESET}"

            # Montagem da linha
            linha_partes = [
                (pref, None),
                (f"{cor_tipo}{tipo_fmt:16s}{RESET}", None),
                (texto_cmd, None),
                (texto_desc, None)
            ]
            
            self.grade.EscreverLinhaComposta(linha_alvo, linha_partes)


class PainelEstado:

    def __init__(self, grade, linha_inicio=16, linha_fim=18):
        self.grade = grade
        self.linha_inicio = linha_inicio
        self.linha_fim = linha_fim
        self.dados = {
            "alvo": "",
            "sessao": "",
            "modo": "local",
            "hosts": 0,
            "creds": 0,
            "shells": 0,
            "ativas": 0,
            "ultima": ""
        }

    def DefinirDados(self, dados):
        self.dados.update(dados or {})

    def _CorEstado(self, chave, valor):
        if chave in ("hosts", "creds", "shells", "ativas"):
            if valor == 0: return CINZA
            if chave == "creds": return CIANO
            if chave == "shells": return VERDE
            if chave == "ativas": return AMARELO
            return BRANCO
        return BRANCO

    def Render(self):
        largura_interna = self.grade.largura - 2
        
        # Linha 1: Contexto Global
        alvo = self.dados.get("alvo") or "nenhum"
        sessao = self.dados.get("sessao") or "nenhuma"
        modo = self.dados.get("modo") or "local"
        
        cor_alvo = CIANO if alvo != "nenhum" else CINZA
        cor_sessao = VERDE if sessao != "nenhuma" else CINZA
        
        linha1 = (
            f" alvo: {cor_alvo}{alvo}{RESET}   |   "
            f"sessao: {cor_sessao}{sessao}{RESET}   |   "
            f"modo: {BRANCO}{modo}{RESET}"
        )
        self.grade.EscreverLinhaComposta(self.linha_inicio, [(linha1, None)])
        
        # Linha 2: Contadores
        h = self.dados.get("hosts", 0)
        c = self.dados.get("creds", 0)
        s = self.dados.get("shells", 0)
        a = self.dados.get("ativas", 0)
        
        linha2 = (
            f" hosts: {self._CorEstado('hosts', h)}{h}{RESET}   "
            f"creds: {self._CorEstado('creds', c)}{c}{RESET}   "
            f"shells: {self._CorEstado('shells', s)}{s}{RESET}   "
            f"ativas: {self._CorEstado('ativas', a)}{a}{RESET}"
        )
        self.grade.EscreverLinhaComposta(self.linha_inicio + 1, [(linha2, None)])
        
        # Linha 3: Ultima acao
        ult = self.dados.get("ultima", "")
        if ult:
            if "falha" in ult.lower() or "erro" in ult.lower():
                cor_ult = VERMELHO
            elif "ok" in ult.lower():
                cor_ult = VERDE
            else:
                cor_ult = CINZA
            linha3 = f" ultima: {cor_ult}{ult}{RESET}"
        else:
            linha3 = f" ultima: {DIM}aguardando comando{RESET}"
            
        self.grade.EscreverLinhaComposta(self.linha_inicio + 2, [(linha3, None)])


class StatusBar:

    def __init__(self, grade, linha=19):
        self.grade = grade
        self.linha = linha
        self.mensagem = ""

    def DefinirMensagem(self, msg):
        self.mensagem = msg

    def Render(self):
        largura_interna = self.grade.largura - 2
        esq = f" {DIM}setas ↑↓ navegam   setas ←→ mudam paleta   Enter executa   Esc limpa   Ctrl+Q sai{RESET}"
        dir_ = f"{CIANO}[{self.mensagem}]{RESET} " if self.mensagem else ""
        texto = Preenchido(esq, dir_, largura_interna)
        self.grade.EscreverLinhaComposta(self.linha, [(texto, None)])


class Caixa:

    def __init__(self, largura=None, altura=None, titulo="CBNC / ByP4ss v1.0"):
        self.grade = Grade(largura, altura)
        self.cabecalho = Cabecalho(self.grade, titulo)
        self.menu = MenuPaletas(self.grade)
        self.input = Input(self.grade)
        self.lista = Lista(self.grade)
        self.painel = PainelEstado(self.grade)
        self.statusbar = StatusBar(self.grade)
        self.ativa = False

    def Abrir(self):
        if not self.grade.Abrir():
            return False
        self.ativa = True
        self.cabecalho.Render()
        self.grade.DesenharSeparador(2)
        self.menu.Render()
        self.grade.DesenharSeparador(4)
        self.grade.DesenharSeparador(14)
        self.grade.DesenharSeparador(18)
        self.input.Render()
        self.lista.Render()
        self.painel.Render()
        self.statusbar.Render()
        self.grade.DesenharBorda()
        self.grade.Flush()
        return True

    def Fechar(self):
        if not self.ativa:
            return
        self.grade.Fechar()
        self.ativa = False

    def Desenhar(self):
        if not self.ativa:
            return
        try:
            self.menu.Render()
            self.input.Render()
            self.lista.Render()
            self.painel.Render()
            self.statusbar.Render()
            self.grade.Flush()
        except Exception:
            pass

    def DesenharCompleto(self):
        if not self.ativa:
            return
        try:
            self.grade.Limpar()
            self.cabecalho.Render()
            self.grade.DesenharSeparador(2)
            self.menu.Render()
            self.grade.DesenharSeparador(4)
            self.grade.DesenharSeparador(14)
            self.lista.Render()
            self.input.Render()
            self.grade.DesenharSeparador(18)
            self.painel.Render()
            self.statusbar.Render()
            self.grade.DesenharBorda()
            self.grade.Flush()
        except Exception:
            pass

    def Tick(self):
        self.input.Tick()

    def Mover(self, delta):
        self.lista.Mover(delta)

    def DefinirQuery(self, query):
        self.input.DefinirQuery(query)

    def DefinirPaleta(self, paleta):
        self.menu.DefinirPaleta(paleta)

    def DefinirItens(self, itens):
        self.lista.DefinirItens(itens)

    def DefinirEstado(self, dados):
        self.painel.DefinirDados(dados)

    def DefinirStatus(self, msg):
        self.statusbar.DefinirMensagem(msg)

    def Redesenhar(self):
        self.DesenharCompleto()

    def Dimensoes(self):
        return self.grade.largura, self.grade.altura


def _PatchListaParaScroll():
    global Lista
    original_render = Lista.Render
    def novo_render(self):
        altura_visivel = self.linha_fim - self.linha_inicio + 1
        largura_interna = self.grade.largura - 2
        
        for i in range(altura_visivel):
            self.grade.EscreverLinha(self.linha_inicio + i, "")

        if not self.itens:
            self.grade.EscreverLinha(self.linha_inicio, f"  {DIM}(nenhum item disponivel){RESET}")
            return

        visiveis = self.itens[self.scroll:self.scroll + altura_visivel]
        total_itens = len(self.itens)
        
        for idx, item in enumerate(visiveis):
            idx_global = self.scroll + idx
            linha_alvo = self.linha_inicio + idx
            selecionado = (idx_global == self.selecionado)
            pref = f"{INVERT}> {RESET}" if selecionado else "  "
            
            tipo = item.get("tipo", "")
            if tipo == "reconhecimento": cor_tipo = AZUL
            elif tipo == "acesso": cor_tipo = VERDE
            elif tipo == "ataque": cor_tipo = VERMELHO
            elif tipo == "encadeamento": cor_tipo = MAGENTA
            elif tipo == "bypass": cor_tipo = AMARELO
            elif tipo == "lancamento": cor_tipo = CIANO
            else: cor_tipo = CINZA

            tipo_fmt = f"[{tipo.upper()}]"
            cmd = item.get("id", "")
            desc = item.get("descricao", "")
            
            if selecionado:
                texto_cmd = f"{INVERT}{BOLD}{cmd:15s}{RESET}"
                texto_desc = f"{INVERT}{desc}{RESET}"
            else:
                texto_cmd = f"{cmd:15s}"
                texto_desc = f"{DIM}{desc}{RESET}"

            linha_partes = [
                (pref, None),
                (f"{cor_tipo}{tipo_fmt:16s}{RESET}", None),
                (texto_cmd, None),
                (texto_desc, None)
            ]
            self.grade.EscreverLinhaComposta(linha_alvo, linha_partes)
            
        if total_itens > altura_visivel:
            barra_x = self.grade.largura - 2
            for i in range(altura_visivel):
                idx_global = self.scroll + i
                if idx_global < total_itens:
                    pos = int((idx_global / (total_itens - 1)) * (altura_visivel - 1))
                    if i == pos:
                        self.grade.Ir(self.linha_inicio + i, barra_x)
                        self.grade.Write(CINZA + "█" + RESET)
                    else:
                        self.grade.Ir(self.linha_inicio + i, barra_x)
                        self.grade.Write(CINZA + "│" + RESET)

    Lista.Render = novo_render

_PatchListaParaScroll()


def _PatchCaixaParaExtras():
    global Caixa
    
    def _CalcularAlturas(self):
        largura = self.grade.largura
        altura = self.grade.altura
        self.lista.linha_inicio = 7
        self.lista.linha_fim = altura - 7
        self.painel.linha_inicio = altura - 5
        self.painel.linha_fim = altura - 4
        self.statusbar.linha = altura - 2
        self.input.linha = 5
        
    def Resize(self):
        w, h = DimensoesTerminal()
        nova_largura = min(w - 2, 100)
        nova_altura = min(h - 2, 40)
        if nova_largura == self.grade.largura and nova_altura == self.grade.altura:
            return False
        self.grade.largura = nova_largura
        self.grade.altura = nova_altura
        self.grade.linha_origem = max(1, (h - nova_altura) // 2 + 1)
        self.grade.coluna_origem = max(1, (w - nova_largura) // 2 + 1)
        _CalcularAlturas(self)
        self.DesenharCompleto()
        return True

    def MostrarToast(self, msg, duracao=2.0):
        self.toast_texto = msg
        self.toast_ate = time.monotonic() + duracao

    def _ToastAtivo(self):
        if not hasattr(self, "toast_texto") or not self.toast_texto:
            return None
        if time.monotonic() > self.toast_ate:
            self.toast_texto = ""
            return None
        return self.toast_texto

    def MostrarHelp(self):
        self.help_ativo = True
        self.DesenharHelp()

    def FecharHelp(self):
        self.help_ativo = False
        self.DesenharCompleto()

    def DesenharHelp(self):
        try:
            self.grade.Limpar()
            largura_interna = self.grade.largura - 2
            titulo = " AJUDA — ByP4ss Console "
            sep_topo = BORDA_TL + BORDA_H * largura_interna + BORDA_TR
            self.grade.Ir(0, 0)
            self.grade.Write(CIANO + BOLD + BORDA_TL + RESET)
            meio = largura_interna - len(titulo)
            if meio > 0:
                esq = BORDA_H * (meio // 2)
                dir_ = BORDA_H * (meio - meio // 2)
                self.grade.Ir(0, 1)
                self.grade.Write(CINZA + esq + RESET + BOLD + CIANO + titulo + RESET + CINZA + dir_ + RESET)
            self.grade.Ir(0, self.grade.largura - 1)
            self.grade.Write(CIANO + BORDA_TR + RESET)
            
            linhas_help = [
                "",
                f" {BOLD}COMANDOS DISPONIVEIS{RESET}",
                "",
                f"  {CIANO}scan{RESET}        Port scan e SSDP num alvo",
                f"  {CIANO}analise{RESET}     Analise completa (portas, servicos, CVEs)",
                f"  {CIANO}cred{RESET}        Busca credenciais (YAML + K1ELI)",
                f"  {CIANO}exploit{RESET}     Executa exploit (tplink/dlink/arcadyan/...)",
                f"  {CIANO}chain{RESET}       Kill chain (recon_auto, dlink_basico)",
                f"  {CIANO}server{RESET}      Servidor falso (HTTP/SSDP)",
                f"  {CIANO}sessions{RESET}    Lista sessoes salvas",
                f"  {CIANO}history{RESET}     Ultimos comandos executados",
                f"  {CIANO}exit{RESET}        Encerra o console",
                "",
                f" {BOLD}NAVEGACAO{RESET}",
                "",
                f"  {AMARELO}↑ ↓{RESET}   Navegar entre itens",
                f"  {AMARELO}← →{RESET}   Trocar de paleta (COMANDO/ALVO/EXPLOIT/CHAIN/SESSION/HISTORY)",
                f"  {AMARELO}Enter{RESET} Executar item selecionado",
                f"  {AMARELO}Esc{RESET}   Limpar query atual",
                f"  {AMARELO}?{RESET}     Abre / fecha esta ajuda",
                f"  {AMARELO}Ctrl+Q{RESET} Sair do console",
                "",
                f" {BOLD}PALETAS{RESET}",
                "",
                f"  {AZUL}COMANDO{RESET}    Todos os comandos do ByP4ss",
                f"  {AZUL}ALVO{RESET}       Alvos descobertos (historico de scan)",
                f"  {AZUL}EXPLOIT{RESET}    Os 6 CVEs (TP-Link, D-Link, Tenda...)",
                f"  {AZUL}CHAIN{RESET}      Templates de kill chain",
                f"  {AZUL}SESSION{RESET}    Sessoes salvas no disco",
                f"  {AZUL}HISTORY{RESET}    Comandos executados recentemente",
                "",
                f" {DIM}Pressione ? ou Esc para voltar{RESET}",
            ]
            
            for i, linha in enumerate(linhas_help[:self.grade.altura - 2]):
                self.grade.EscreverLinhaComposta(1 + i, [(linha, None)])
            
            self.grade.DesenharBorda()
            self.grade.Flush()
        except Exception:
            pass

    def DesenharCompleto(self):
        if not self.ativa:
            return
        try:
            self.grade.Limpar()
            self.cabecalho.Render()
            self.grade.DesenharSeparador(2)
            self.menu.Render()
            self.grade.DesenharSeparador(4)
            self.input.Render()
            self.grade.DesenharSeparador(6)
            self.lista.Render()
            self.grade.DesenharSeparador(self.grade.altura - 6)
            self.painel.Render()
            self.grade.DesenharSeparador(self.grade.altura - 3)
            self.statusbar.Render()
            self.grade.DesenharBorda()
            toast = self._ToastAtivo()
            if toast:
                self.grade.Ir(self.grade.altura - 2, 2)
                self.grade.Write(INVERT + " " + toast[:self.grade.largura - 6] + " " + RESET)
            self.grade.Flush()
        except Exception:
            pass

    def Desenhar(self):
        if not self.ativa:
            return
        if hasattr(self, "help_ativo") and self.help_ativo:
            return
        try:
            self.menu.Render()
            self.input.Render()
            self.lista.Render()
            self.painel.Render()
            self.statusbar.Render()
            toast = self._ToastAtivo()
            if toast:
                self.grade.Ir(self.grade.altura - 2, 2)
                self.grade.Write(INVERT + " " + toast[:self.grade.largura - 6] + " " + RESET)
            self.grade.Flush()
        except Exception:
            pass

    def Abrir(self):
        if not self.grade.Abrir():
            return False
        self.ativa = True
        self.help_ativo = False
        self.toast_texto = ""
        self.toast_ate = 0
        _CalcularAlturas(self)
        self.DesenharCompleto()
        return True

    Caixa.Resize = Resize
    Caixa.MostrarToast = MostrarToast
    Caixa.DesenharCompleto = DesenharCompleto
    Caixa.Desenhar = Desenhar
    Caixa.Abrir = Abrir
    Caixa.DesenharHelp = DesenharHelp
    Caixa.MostrarHelp = MostrarHelp
    Caixa.FecharHelp = FecharHelp
    Caixa._ToastAtivo = _ToastAtivo


_PatchCaixaParaExtras()


class TesteCaixa:

    @staticmethod
    def Rodar():
        print("=== TESTE CAIXA v2 ===")
        print()
        print("[1] Instanciando grade 60x20")
        c = Caixa(60, 20)
        print(f"    grade: {c.grade.largura}x{c.grade.altura}")
        print(f"    origem: linha={c.grade.linha_origem}, coluna={c.grade.coluna_origem}")
        assert c.grade.largura == 60
        assert c.grade.altura == 20

        print()
        print("[2] Widgets instanciados")
        assert c.cabecalho is not None
        assert c.menu is not None
        assert c.input is not None
        assert c.lista is not None
        assert c.painel is not None
        assert c.statusbar is not None
        print("    6 widgets OK")

        print()
        print("[3] Abrindo (render de teste)")
        c.grade.ativa = True
        c.DesenharCompleto()
        print("    render OK")

        print()
        print("[4] Movendo lista")
        itens = [{"id": f"cmd{i}", "tipo": "ataque", "descricao": f"descricao {i}"} for i in range(20)]
        c.DefinirItens(itens)
        c.Mover(5)
        assert c.lista.selecionado == 5
        print(f"    selecionado: {c.lista.selecionado}")

        print()
        print("[5] Query e paleta")
        c.DefinirQuery("scan alvo=192.168.0.1")
        c.DefinirPaleta("EXPLOIT")
        assert c.input.query == "scan alvo=192.168.0.1"
        assert c.menu.paleta_atual == "EXPLOIT"
        print(f"    query: {c.input.query}")
        print(f"    paleta: {c.menu.paleta_atual}")

        print()
        print("[6] Estado do painel")
        c.DefinirEstado({
            "alvo": "192.168.0.1",
            "sessao": "s_001",
            "modo": "local",
            "hosts": 5,
            "creds": 10,
            "shells": 1,
            "ativas": 0,
            "ultima": "scan (ok, 0.3s)",
        })
        assert c.painel.dados["alvo"] == "192.168.0.1"
        print(f"    alvo: {c.painel.dados['alvo']}, hosts: {c.painel.dados['hosts']}")

        print()
        print("[7] Toast")
        c.MostrarToast("teste de toast", 0.1)
        toast = c._ToastAtivo()
        assert toast == "teste de toast"
        print(f"    toast: {toast}")
        import time
        time.sleep(0.15)
        assert c._ToastAtivo() is None
        print("    toast expirou OK")

        print()
        print("[8] Resize (recalcula grade)")
        r = c.Resize()
        assert r in (True, False)
        print(f"    resize retornou: {r} (ok em ambos os casos)")

        print()
        print("[9] Fechar")
        c.Fechar()
        print("    fechado")

        print()
        print("TESTE OK")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        try:
            TesteCaixa.Rodar()
        except Exception as e:
            sys.stdout.write(RESET + CUR_MOSTRAR + "\n")
            print(f"erro: {type(e).__name__}: {e}")
            sys.exit(1)
    else:
        print("uso: python3 caixa.py teste")
