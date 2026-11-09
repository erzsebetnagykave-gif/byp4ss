import sys
import os
import json
import time
import shutil
import argparse
import urllib.request
import urllib.error
import select
import termios
import tty
import signal
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from Sessao import Sessao
except ImportError:
    Sessao = None
try:
    from Analise import Analise
except ImportError:
    Analise = None
try:
    from RegistroComandos import RegistroComandos
except ImportError:
    RegistroComandos = None
try:
    from Cadeia import Cadeia
except ImportError:
    Cadeia = None
try:
    from Api import Api
except ImportError:
    Api = None
try:
    from Core.Engine import Engine
except ImportError:
    Engine = None


class Cor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    INVERT = "\033[7m"
    VERMELHO = "\033[31m"
    VERDE = "\033[32m"
    AMARELO = "\033[33m"
    AZUL = "\033[34m"
    MAGENTA = "\033[35m"
    CIANO = "\033[36m"
    CINZA = "\033[90m"
    FUNDO_AZUL = "\033[44m"
    FUNDO_CIANO = "\033[46m"
    FUNDO_VERDE = "\033[42m"
    FUNDO_AMARELO = "\033[43m"
    FUNDO_MAGENTA = "\033[45m"


class Render:

    LARGURA_MIN = 60
    ALTURA_MIN = 15

    @staticmethod
    def Dimensoes():
        try:
            T = shutil.get_terminal_size()
            return max(T.columns, Render.LARGURA_MIN), max(T.lines, Render.ALTURA_MIN)
        except Exception:
            return 80, 24

    @staticmethod
    def Limpar():
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    @staticmethod
    def IrPara(Linha, Coluna=1):
        sys.stdout.write(f"\033[{int(Linha)};{int(Coluna)}H")

    @staticmethod
    def Escrever(Texto, Cor_=None, SemQuebra=False):
        Prefixo = Cor_ if Cor_ else ""
        Sufixo = Cor.RESET if Cor_ else ""
        sys.stdout.write(Prefixo + Texto + Sufixo)
        if not SemQuebra:
            sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def LinhaHorizontal(Cor_=Cor.CINZA):
        L, _ = Render.Dimensoes()
        Render.Escrever("─" * L, Cor_, SemQuebra=False)

    @staticmethod
    def Centralizar(Texto, Largura=None):
        L, _ = Render.Dimensoes()
        Largura = Largura or L
        if len(Texto) >= Largura:
            return Texto[:Largura]
        Esq = (Largura - len(Texto)) // 2
        return " " * Esq + Texto

    @staticmethod
    def Visivel(Texto):
        import re
        return len(re.sub(r"\033\[[0-9;]*m", "", str(Texto)))

    @staticmethod
    def Truncar(Texto, Maximo):
        Texto = str(Texto)
        if Render.Visivel(Texto) <= Maximo:
            return Texto
        import re
        Limpo = re.sub(r"\033\[[0-9;]*m", "", Texto)
        return Limpo[: max(0, Maximo - 1)] + "…"


class Estado:

    VERSAO = "0.1"
    SALAS = ["rede", "exploits", "comandos", "cadeias", "estado", "federacao"]
    CORES_SALA = {
        "rede": Cor.AZUL,
        "exploits": Cor.AMARELO,
        "comandos": Cor.VERDE,
        "cadeias": Cor.MAGENTA,
        "estado": Cor.CIANO,
        "federacao": Cor.MAGENTA,
    }

    def __init__(self):
        self.SalaAtual = "rede"
        self.Selecionado = 0
        self.Historico = []
        self.Cache = {}
        self.Modo = "local"
        self.SessaoNome = None
        self.ShellsAtivas = 0
        self.AlvosConhecidos = 0
        self.Toast = None
        self.ToastAte = 0
        self.Rodando = True
        self.UltimaChave = None
        self.MensagemUsuario = ""

    def IrParaSala(self, Nome):
        if Nome not in Estado.SALAS:
            return False
        if self.SalaAtual != Nome:
            self.Selecionado = 0
            self.SalaAtual = Nome
        return True

    def ProximaSala(self):
        I = Estado.SALAS.index(self.SalaAtual)
        self.IrParaSala(Estado.SALAS[(I + 1) % len(Estado.SALAS)])

    def SalaAnterior(self):
        I = Estado.SALAS.index(self.SalaAtual)
        self.IrParaSala(Estado.SALAS[(I - 1) % len(Estado.SALAS)])

    def MostrarToast(self, Texto, Duracao=2.0):
        self.Toast = Texto
        self.ToastAte = time.time() + Duracao

    def ToastAtivo(self):
        if not self.Toast:
            return None
        if time.time() >= self.ToastAte:
            self.Toast = None
            return None
        return self.Toast

    def Registrar(self, Cmd, Ok, Extra=None):
        self.Historico.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "cmd": Cmd, "ok": bool(Ok), "extra": Extra or {}
        })
        if len(self.Historico) > 50:
            self.Historico = self.Historico[-50:]


class Cabecalho:

    @staticmethod
    def Desenhar(Est):
        L, _ = Render.Dimensoes()
        Render.IrPara(1, 1)
        Esquerda = f" {Cor.BOLD}BYPASS{Cor.RESET} v{Estado.VERSAO}"
        Direita = f"{Cor.CINZA}modo: {Est.Modo}{Cor.RESET} "
        Distancia = L - len(" BYPASS v0.1") - len(f"modo: {Est.Modo} ")
        Render.Escrever(Esquerda + " " * max(1, Distancia) + Direita, SemQuebra=True)
        Render.IrPara(2, 1)
        Render.LinhaHorizontal()

    @staticmethod
    def MenuBlocos(Est):
        L, _ = Render.Dimensoes()
        Render.IrPara(3, 1)
        Partes = []
        for Nome in Estado.SALAS:
            Cor_ = Estado.CORES_SALA.get(Nome, Cor.CINZA)
            if Nome == Est.SalaAtual:
                Partes.append(f"{Cor.INVERT}{Cor.BOLD} {Nome.upper()} {Cor.RESET}")
            else:
                Partes.append(f"{Cor_}{Cor.DIM} {Nome} {Cor.RESET}")
        Linha = "  ".join(Partes)
        Render.Escrever(Render.Truncar(Linha, L), SemQuebra=False)
        Render.IrPara(4, 1)
        Render.LinhaHorizontal()

    @staticmethod
    def Breadcrumb(Est, Extra=None):
        Render.IrPara(5, 1)
        Trilha = f"{Cor.BOLD}BYPASS{Cor.RESET} > {Estado.CORES_SALA.get(Est.SalaAtual, '')}{Est.SalaAtual}{Cor.RESET}"
        if Extra:
            Trilha += f" > {Extra}"
        Render.Escrever(Trilha)

    @staticmethod
    def Rodape(Est):
        L, A = Render.Dimensoes()
        Render.IrPara(A - 1, 1)
        Render.LinhaHorizontal()
        Render.IrPara(A, 1)
        Esq = (f"{Cor.VERDE}hosts: {Est.AlvosConhecidos}{Cor.RESET}  "
               f"{Cor.AMARELO}shells: {Est.ShellsAtivas}{Cor.RESET}  "
               f"{Cor.CINZA}sessao: {Est.SessaoNome or 'nova'}{Cor.RESET}")
        Dir = f"{Cor.CINZA}Ctrl+Q sair  ←→ salas  ↑↓ navegar{Cor.RESET}"
        Espaco = L - Render.Visivel(Esq) - Render.Visivel(Dir)
        Render.Escrever(Esq + " " * max(1, Espaco) + Dir, SemQuebra=False)

    @staticmethod
    def Toast(Est):
        T = Est.ToastAtivo()
        if not T:
            return
        L, A = Render.Dimensoes()
        Render.IrPara(A - 2, 1)
        Render.Escrever(f"{Cor.FUNDO_AMARELO}{Cor.BOLD} ✓ {T} {Cor.RESET}", SemQuebra=False)


class Teclado:

    @staticmethod
    def Abrir():
        try:
            Fd = sys.stdin.fileno()
            Antigo = termios.tcgetattr(Fd)
            tty.setraw(Fd)
            return {"ok": True, "fd": Fd, "antigo": Antigo}
        except Exception as E:
            return {"ok": False, "erro": str(E)}

    @staticmethod
    def Fechar(SessaoTeclado):
        if not SessaoTeclado or not SessaoTeclado.get("ok"):
            return
        try:
            termios.tcsetattr(SessaoTeclado["fd"], termios.TCSADRAIN, SessaoTeclado["antigo"])
        except Exception:
            pass

    @staticmethod
    def Ler(Timeout=0.1):
        try:
            Prontos, _, _ = select.select([sys.stdin], [], [], Timeout)
            if not Prontos:
                return None
            return sys.stdin.read(1)
        except Exception:
            return None

    @staticmethod
    def LerSequencia(Primeiro, Timeout=0.02):
        Sequencia = Primeiro
        while True:
            C = Teclado.Ler(Timeout)
            if not C:
                break
            Sequencia += C
            if len(Sequencia) > 8:
                break
        return Sequencia

    @staticmethod
    def Decodificar(Seq):
        Mapa = {
            "\x1b[A": "cima", "\x1b[B": "baixo", "\x1b[C": "direita", "\x1b[D": "esquerda",
            "\x1b[H": "home", "\x1b[F": "end", "\x1b[5~": "pgup", "\x1b[6~": "pgdown",
            "\t": "tab", "\r": "enter", "\n": "enter", "\x7f": "backspace", " ": "espaco",
            "\x11": "sair", "\x03": "sair", "\x04": "sair",
            "\x0e": "nova_sessao", "\x13": "salvar",
        }
        if Seq in Mapa:
            return Mapa[Seq]
        if len(Seq) == 1:
            return Seq
        return "desconhecido"


def MainLoop(Est):
    T = Teclado.Abrir()
    if not T.get("ok"):
        print("terminal nao suporta raw mode:", T.get("erro"))
        return 1
    signal.signal(signal.SIGWINCH, lambda *A: None)
    try:
        Render.Limpar()
        while Est.Rodando:
            Render.Limpar()
            L, A = Render.Dimensoes()
            Cabecalho.Desenhar(Est)
            Cabecalho.MenuBlocos(Est)
            Cabecalho.Breadcrumb(Est)
            DespacharSala(Est, A)
            Cabecalho.Rodape(Est)
            Cabecalho.Toast(Est)
            C = Teclado.Ler(0.2)
            if C:
                Seq = Teclado.LerSequencia(C)
                Acao = Teclado.Decodificar(Seq)
                DespacharAcao(Est, Acao, Char=C)
    finally:
        Teclado.Fechar(T)
        Render.Limpar()
        print(f"{Cor.BOLD}BYPASS{Cor.RESET} v{Estado.VERSAO} — bye.")
    return 0


def BypassCentral():
    Checagens = []
    for Nome, Modulo in [
        ("Sessao", Sessao), ("Analise", Analise), ("RegistroComandos", RegistroComandos),
        ("Cadeia", Cadeia), ("Api", Api), ("Engine", Engine),
    ]:
        Checagens.append((Nome, Modulo is not None))
    Falhas = [N for N, Ok in Checagens if not Ok]
    return {"ok": len(Falhas) == 0, "checagens": Checagens, "falhas": Falhas}


def Main():
    P = argparse.ArgumentParser(prog="Console")
    P.add_argument("comando", nargs="?", default=None, choices=["bypass", "servidor", "status"])
    P.add_argument("--modo", default="local", choices=["local", "servidor", "federado"])
    P.add_argument("--porta-api", type=int, default=8765)
    P.add_argument("--escutar-api", default="127.0.0.1")
    Args = P.parse_args()

    if Args.comando == "bypass":
        R = BypassCentral()
        for Nome, Ok in R["checagens"]:
            Marca = f"{Cor.VERDE}ok{Cor.RESET}" if Ok else f"{Cor.VERMELHO}falta{Cor.RESET}"
            print(f"  {Nome:20s} {Marca}")
        if not R["ok"]:
            print(f"\n{Cor.VERMELHO}base incompleta: {', '.join(R['falhas'])}{Cor.RESET}")
            return 1
        Est = Estado()
        Est.Modo = Args.modo
        if Sessao:
            Lista = Sessao.Listar()
            if Lista.get("ok") and Lista.get("total", 0) > 0:
                Ultima = Lista["sessoes"][0]
                Est.SessaoNome = Ultima["nome"]
                Est.MostrarToast(f"retomada: {Ultima['nome']} (Ctrl+N nova)")
        if Args.modo in ("servidor", "federado"):
            Srv = Servidor.Iniciar(Args.escutar_api, Args.porta_api)
            if Srv.get("ok"):
                Est.Cache["api_rodando"] = True
                Est.Cache["api_porta"] = Srv.get("porta")
                Est.MostrarToast(f"api :{Srv.get('porta')} ativa")
            else:
                Est.MostrarToast(f"api nao subiu: {Srv.get('motivo')}")
        try:
            return MainLoop(Est)
        finally:
            if Est.Cache.get("api_rodando"):
                Servidor.Parar()
            SalvarAuto.Rodar(Est, "saida")

    if Args.comando == "servidor":
        R = Servidor.Iniciar(Args.escutar_api, Args.porta_api)
        if not R.get("ok"):
            print(f"{Cor.VERMELHO}api nao subiu: {R.get('motivo')}{Cor.RESET}")
            return 1
        Info = R.get("info") or {}
        print(f"{Cor.VERDE}api em http://{Info.get('escuta')}:{Info.get('porta')}{Cor.RESET}")
        print(f"token: {Api.Token if Api else '?'}")
        print(f"{Cor.CINZA}Ctrl+C para derrubar{Cor.RESET}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            Servidor.Parar()
            print(f"{Cor.CINZA}api derrubada{Cor.RESET}")
            return 0

    if Args.comando == "status":
        R = Servidor.Status()
        print(json.dumps(R, indent=2, ensure_ascii=False))
        return 0 if R.get("rodando") else 1

    print("uso: python3 Console.py bypass|servidor|status [--modo local|servidor|federado]")
    return 2




class Badge:

    @staticmethod
    def Sugerido(Motivo=None):
        if Motivo:
            return f"{Cor.FUNDO_VERDE}{Cor.BOLD} → sugerido {Cor.RESET}"
        return f"{Cor.FUNDO_VERDE}{Cor.BOLD} → {Cor.RESET}"

    @staticmethod
    def PlanoB(Motivo=None):
        Texto = f" (plano B: {Motivo})" if Motivo else " (plano B)"
        return f"{Cor.CINZA}{Texto}{Cor.RESET}"

    @staticmethod
    def Ok():
        return f"{Cor.VERDE}✓{Cor.RESET}"

    @staticmethod
    def Falha():
        return f"{Cor.VERMELHO}✗{Cor.RESET}"

    @staticmethod
    def Ocioso():
        return f"{Cor.CINZA}○{Cor.RESET}"

    @staticmethod
    def Aviso():
        return f"{Cor.AMARELO}⚠{Cor.RESET}"


class Spinner:

    FRAMES = ["◐", "◓", "◑", "◒"]

    @staticmethod
    def Mostrar(Tempo=0.8, Texto="carregando"):
        L, A = Render.Dimensoes()
        Inicio = time.time()
        I = 0
        while time.time() - Inicio < Tempo:
            Frame = Spinner.FRAMES[I % 4]
            Render.IrPara(A - 2, 1)
            Render.Escrever(f"{Cor.CIANO}{Frame}{Cor.RESET} {Texto}...", SemQuebra=False)
            time.sleep(0.08)
            I += 1
        Render.IrPara(A - 2, 1)
        Render.Escrever(" " * 40, SemQuebra=False)


class CompletarTab:

    @staticmethod
    def Completar(Texto, Est):
        Texto = Texto.strip()
        if not Texto:
            return []
        if RegistroComandos is None:
            return []
        Nomes = list(RegistroComandos.COMANDOS.keys())
        if " " in Texto:
            Prefixo, Resto = Texto.rsplit(" ", 1)
            Candidatos = [N for N in Nomes if N.startswith(Prefixo + " ")]
            if Candidatos:
                return [C.replace(Prefixo + " ", "") for C in Candidatos if C.startswith(Prefixo + " " + Resto)]
            return []
        return [N for N in Nomes if N.startswith(Texto)]


class SalaRede:

    @staticmethod
    def Desenhar(Est, Altura):
        L, _ = Render.Dimensoes()
        Render.IrPara(7, 1)
        Render.Escrever(f"{Cor.BOLD}{Cor.AZUL}REDE{Cor.RESET}  "
                        f"{Cor.CINZA}Enter=scan | s=scan sub-rede | r=refresh{Cor.RESET}")
        Cache = Est.Cache.get("rede") or {}
        if not Cache.get("ok"):
            Render.IrPara(9, 1)
            Render.Escrever(f"{Cor.CINZA}sem dados. Enter para escanear (alvo: 127.0.0.1){Cor.RESET}")
            return
        Hosts = Cache.get("hosts") or []
        if not Hosts:
            Render.IrPara(9, 1)
            Render.Escrever(f"{Cor.CINZA}nenhum host encontrado em {Cache.get('subrede')}{Cor.RESET}")
            return
        Render.IrPara(9, 1)
        Render.Escrever(f"{Cor.CINZA}hosts: {len(Hosts)}{Cor.RESET}")
        Linha = 10
        for I, H in enumerate(Hosts[:Altura - 12]):
            if Linha > Altura - 3:
                break
            Render.IrPara(Linha, 1)
            Selecionado = I == Est.Selecionado
            Pref = f"{Cor.INVERT}{Cor.BOLD}>{Cor.RESET}" if Selecionado else " "
            Ip = H.get("ip", "?")
            Fab = H.get("fabricante") or "?"
            Portas = ",".join(str(P) for P in (H.get("portas_abertas") or []))
            BadgeStr = ""
            Cves = H.get("cves_sugeridas") or []
            if Cves:
                BadgeStr = " " + Badge.Sugerido(Cves[0].get("id"))
            Render.Escrever(f" {Pref} {Cor.AZUL}{Ip:16s}{Cor.RESET}  "
                            f"{Fab:10s}  {Cor.CINZA}[{Portas}]{Cor.RESET}{BadgeStr}",
                            SemQuebra=False)
            Linha += 1

    @staticmethod
    def Acao(Est, Acao_):
        if Acao_ == "enter":
            Alvo = "127.0.0.1"
            Spinner.Mostrar(0.5, f"escanear {Alvo}")
            if Analise:
                R = Analise.EscanearAlvo(Alvo, [22, 80, 443], 2)
                Est.Cache["rede"] = {"ok": R.get("ok"),
                                      "hosts": [{"ip": Alvo, "portas_abertas": R.get("portas_abertas", []),
                                                 "fabricante": R.get("fabricante"),
                                                 "cves_sugeridas": R.get("cves_sugeridas", [])}]}
                Est.AlvosConhecidos = 1 if R.get("ok") else 0
                Est.MostrarToast(f"scan: {Alvo} portas={R.get('portas_abertas')}")
            else:
                Est.MostrarToast("Analise indisponivel")
            return True
        if Acao_ == "s":
            Spinner.Mostrar(0.5, "escanear rede")
            if Analise:
                R = Analise.EscanearRede("192.168.0.0/30", None, 2)
                Est.Cache["rede"] = R
                Est.AlvosConhecidos = R.get("total", 0)
                Est.MostrarToast(f"rede: {R.get('total', 0)} hosts")
            return True
        if Acao_ == "r":
            Est.Cache.pop("rede", None)
            Est.MostrarToast("cache limpo")
            return True
        return False


class SalaExploits:

    EXPLOITS = [
        ("tplink", "CVE-2023-1389", "TP-Link Archer AX21"),
        ("dlink", "CVE-2024-3273", "D-Link DNS-320L"),
        ("arcadyan", "CVE-2021-20090", "Arcadyan ARV"),
        ("iptime", "CVE-2025-55423", "ipTIME"),
        ("tenda7795", "CVE-2025-7795", "Tenda AC9 (DoS)"),
        ("tenda29384", "CVE-2025-29384", "Tenda AC9 (MIPS)"),
    ]

    PLANO_B = {
        "dlink": "arcadyan (mesmo /cgi-bin/)",
        "arcadyan": "dlink (mesma injection)",
        "tenda29384": "tenda7795 (mesmo modelo, DoS)",
    }

    @staticmethod
    def Desenhar(Est, Altura):
        Render.IrPara(7, 1)
        Render.Escrever(f"{Cor.BOLD}{Cor.AMARELO}EXPLOITS{Cor.RESET}  "
                        f"{Cor.CINZA}Enter=executar | F5=recon_auto{Cor.RESET}")
        Alvo = Est.Cache.get("alvo_atual") or "127.0.0.1"
        CvesSugeridas = set()
        RedeCache = Est.Cache.get("rede") or {}
        for H in (RedeCache.get("hosts") or []):
            if H.get("ip") == Alvo:
                for C in (H.get("cves_sugeridas") or []):
                    CvesSugeridas.add(C.get("id"))
                break
        Render.IrPara(9, 1)
        Render.Escrever(f"{Cor.CINZA}alvo: {Alvo}  | sugeridos: {len(CvesSugeridas)}{Cor.RESET}")
        Linha = 10
        for I, (Id, Cve, Modelo) in enumerate(SalaExploits.EXPLOITS):
            if Linha > Altura - 3:
                break
            Render.IrPara(Linha, 1)
            Selecionado = I == Est.Selecionado
            Pref = f"{Cor.INVERT}{Cor.BOLD}>{Cor.RESET}" if Selecionado else " "
            Sugerido = Id in CvesSugeridas
            B = " " + Badge.Sugerido() if Sugerido else ""
            PlanoB = ""
            if Sugerido and Id in SalaExploits.PLANO_B:
                PlanoB = Badge.PlanoB(SalaExploits.PLANO_B[Id])
            EstadoAtual = Est.Cache.get(f"exploit_{Id}") or {}
            Marcador = Badge.Ocioso()
            if EstadoAtual.get("ok") is True:
                Marcador = Badge.Ok()
            elif EstadoAtual.get("ok") is False:
                Marcador = Badge.Falha()
            Render.Escrever(f" {Pref} {Marcador} {Cor.AMARELO}{Id:12s}{Cor.RESET}  "
                            f"{Cor.CINZA}{Cve:16s}{Cor.RESET} {Modelo}{B}{PlanoB}",
                            SemQuebra=False)
            Linha += 1

    @staticmethod
    def Acao(Est, Acao_):
        if not SalaExploits.EXPLOITS:
            return False
        if Acao_ == "enter":
            Indice = min(Est.Selecionado, len(SalaExploits.EXPLOITS) - 1)
            Id, Cve, Modelo = SalaExploits.EXPLOITS[Indice]
            Alvo = Est.Cache.get("alvo_atual") or "127.0.0.1"
            Spinner.Mostrar(0.5, f"executar {Id}")
            if Engine:
                R = Engine.Exploit(Id, Alvo, modo="descobrir")
                Est.Cache[f"exploit_{Id}"] = R
                Est.Registrar(f"exploit {Id}", R.get("ok"), {"alvo": Alvo})
                Motivo = (R.get("resultado") or {}).get("motivo") or R.get("motivo") or "?"
                Est.MostrarToast(f"{Id}: {'ok' if R.get('ok') else 'falha'} — {Motivo[:40]}")
            return True
        if Acao_ == "F5":
            Spinner.Mostrar(1.0, "recon_auto")
            if Cadeia:
                Info = Cadeia.Templates()
                Template = [T for T in Info["templates"] if T["nome"] == "recon_auto"]
                if Template:
                    Alvo = Est.Cache.get("alvo_atual") or "127.0.0.1"
                    R = Cadeia.Executar(Template[0]["blocos"], Alvo)
                    Est.Registrar("recon_auto", R.get("ok"))
                    Est.MostrarToast(f"recon_auto: {R.get('estado')}")
            return True
        return False


class SalaComandos:

    @staticmethod
    def Desenhar(Est, Altura):
        Render.IrPara(7, 1)
        Modo = Est.Cache.get("modo_fantasma") and " FANTASMA" or ""
        Render.Escrever(f"{Cor.BOLD}{Cor.VERDE}COMANDOS{Cor.RESET}  "
                        f"{Cor.CINZA}Tab=completar | G=fantasma | Enter=executar{Modo}{Cor.RESET}")
        Render.IrPara(8, 1)
        Buffer = Est.Cache.get("buffer_cmd") or ""
        Cursor = f"{Cor.INVERT} {Cor.RESET}"
        Render.Escrever(f" {Cor.VERDE}>{Cor.RESET} {Buffer}{Cursor}")
        if not RegistroComandos:
            return
        Todos = sorted(RegistroComandos.COMANDOS.keys())
        Filtrados = [N for N in Todos if not Buffer or N.startswith(Buffer.split()[0])] if Buffer else Todos
        Render.IrPara(10, 1)
        Render.Escrever(f"{Cor.CINZA}comandos: {len(Filtrados)}/{len(Todos)}{Cor.RESET}")
        Linha = 11
        for I, Nome in enumerate(Filtrados[:Altura - 13]):
            Render.IrPara(Linha, 1)
            Selecionado = I == Est.Selecionado
            Pref = f"{Cor.INVERT}{Cor.BOLD}>{Cor.RESET}" if Selecionado else " "
            Info = RegistroComandos.COMANDOS.get(Nome, {})
            Grupo = Info.get("grupo", "?")
            Desc = Render.Truncar(Info.get("descricao", ""), 50)
            Render.Escrever(f" {Pref} {Cor.VERDE}{Nome:22s}{Cor.RESET}  "
                            f"{Cor.CINZA}[{Grupo:10s}]{Cor.RESET} {Desc}",
                            SemQuebra=False)
            Linha += 1

    @staticmethod
    def Acao(Est, Acao_):
        if Acao_ == "G":
            Est.Cache["modo_fantasma"] = not Est.Cache.get("modo_fantasma", False)
            Est.MostrarToast("fantasma ON" if Est.Cache["modo_fantasma"] else "fantasma OFF")
            return True
        if Acao_ == "tab":
            Buffer = Est.Cache.get("buffer_cmd") or ""
            Candidatos = CompletarTab.Completar(Buffer, Est)
            if len(Candidatos) == 1:
                Prefixo = Buffer.rsplit(" ", 1)[0] + " " if " " in Buffer else ""
                Est.Cache["buffer_cmd"] = Prefixo + Candidatos[0]
                Est.MostrarToast(f"-> {Candidatos[0]}")
            elif len(Candidatos) > 1:
                Est.MostrarToast(f"{len(Candidatos)} opcoes: {', '.join(Candidatos[:3])}...")
            return True
        return False

    @staticmethod
    def TeclaCaractere(Est, Char):
        Buffer = Est.Cache.get("buffer_cmd") or ""
        if Char in ("\x7f", "backspace"):
            Est.Cache["buffer_cmd"] = Buffer[:-1]
            return True
        if len(Char) == 1 and Char.isprintable():
            Est.Cache["buffer_cmd"] = Buffer + Char
            return True
        return False

    @staticmethod
    def Enter(Est):
        Buffer = (Est.Cache.get("buffer_cmd") or "").strip()
        if not Buffer:
            return True
        Partes = Buffer.split()
        if len(Partes) >= 2:
            Cmd = f"{Partes[0]} {Partes[1]}" if Partes[0] in ("exploit", "shell", "servidor", "scanner") else Partes[0]
            Resto = Partes[2:]
        else:
            Cmd = Partes[0]
            Resto = []
        Args = {}
        for Par in Resto:
            if "=" in Par:
                K, V = Par.split("=", 1)
                Args[K] = V
            elif Cmd in ("exploit tplink", "exploit dlink", "exploit arcadyan", "exploit iptime",
                         "exploit tenda7795", "exploit tenda29384", "scan", "analise", "cred", "ssdp"):
                Args["alvo"] = Par
        Spinner.Mostrar(0.4, f"executar {Cmd}")
        if RegistroComandos:
            R = RegistroComandos.Executar(Cmd, Args)
            Est.Registrar(Cmd, R.get("ok"), Args)
            Motivo = (R.get("resultado") or {}).get("motivo") if isinstance(R.get("resultado"), dict) else None
            Est.MostrarToast(f"{Cmd}: {'ok' if R.get('ok') else 'falha'} — {(R.get('motivo') or Motivo or '')[:40]}")
        Est.Cache["buffer_cmd"] = ""
        return True


def DespacharSala(Est, Altura):
    if Est.SalaAtual == "rede":
        SalaRede.Desenhar(Est, Altura)
    elif Est.SalaAtual == "exploits":
        SalaExploits.Desenhar(Est, Altura)
    elif Est.SalaAtual == "comandos":
        SalaComandos.Desenhar(Est, Altura)
    elif Est.SalaAtual == "cadeias":
        SalaCadeias.Desenhar(Est, Altura)
    elif Est.SalaAtual == "estado":
        SalaEstado.Desenhar(Est, Altura)
    elif Est.SalaAtual == "federacao":
        SalaFederacao.Desenhar(Est, Altura)


def DespacharAcao(Est, Acao_, Char=None):
    if Acao_ == "sair":
        Est.Rodando = False
        return True
    if Acao_ == "direita":
        Est.ProximaSala()
        return True
    if Acao_ == "esquerda":
        Est.SalaAnterior()
        return True
    if Acao_ == "cima":
        Est.Selecionado = max(0, Est.Selecionado - 1)
        return True
    if Acao_ == "baixo":
        Est.Selecionado += 1
        return True
    if Acao_ == "salvar":
        if Sessao:
            R = Sessao.Salvar(f"auto_{int(time.time())}",
                              {"sala": Est.SalaAtual, "historico": Est.Historico[-10:]})
            Est.MostrarToast(f"salvo: {R.get('caminho') or R.get('motivo')}")
        return True
    if Acao_ == "nova_sessao":
        Est.MostrarToast("nova sessao")
        return True
    if Acao_ == "O":
        ModoOperador.Toggle(Est)
        return True
    if Char == "F" and Est.SalaAtual != "federacao" and "prompt_fed" not in Est.Cache:
        return SalaFederacao.PromptAbrir(Est)
    if Est.SalaAtual == "rede" and SalaRede.Acao(Est, Acao_):
        return True
    if Est.SalaAtual == "exploits" and SalaExploits.Acao(Est, Acao_):
        return True
    if Est.SalaAtual == "comandos":
        if SalaComandos.Acao(Est, Acao_):
            return True
        if Acao_ == "enter":
            return SalaComandos.Enter(Est)
        if Char:
            return SalaComandos.TeclaCaractere(Est, Char)
        return False
    if Est.SalaAtual == "cadeias" and SalaCadeias.Acao(Est, Acao_):
        return True
    if Est.SalaAtual == "estado" and SalaEstado.Acao(Est, Acao_):
        return True
    if Est.SalaAtual == "federacao":
        if SalaFederacao.Acao(Est, Acao_):
            return True
        if "prompt_fed" in Est.Cache and Char:
            return SalaFederacao.PromptTecla(Est, Char)
        return False
    return False


class RenderCadeia:

    @staticmethod
    def Bloco(Indice, Bloco, Estado_, TempoMs=None):
        Estados = {
            "ocioso": (Cor.CINZA, "○"),
            "rodando": (Cor.AMARELO, "◐"),
            "ok": (Cor.VERDE, "✓"),
            "falha": (Cor.VERMELHO, "✗"),
            "pulado": (Cor.CINZA, "⋯"),
        }
        Cor_, Icone = Estados.get(Estado_, (Cor.CINZA, "?"))
        Cmd = Bloco.get("cmd", "?")
        Desc = Bloco.get("descricao", "")
        Cond = Bloco.get("condicional", "sempre")
        Extra = ""
        if Cond != "sempre":
            Extra = f" {Cor.CINZA}[{Cond}]{Cor.RESET}"
        Tempo = f" {Cor.CINZA}{int(TempoMs)}ms{Cor.RESET}" if TempoMs else ""
        return (f"  [{Indice}] {Cor_}{Icone}{Cor.RESET} "
                f"{Cor.BOLD}{Cmd:22s}{Cor.RESET} {Cor.CINZA}{Desc}{Cor.RESET}{Extra}{Tempo}")

    @staticmethod
    def Cadeia(Blocos, Estados, Tempos=None):
        Tempos = Tempos or {}
        Linhas = []
        for I, B in enumerate(Blocos):
            E = Estados.get(I, "ocioso")
            T = Tempos.get(I)
            Linhas.append(RenderCadeia.Bloco(I, B, E, T))
        return Linhas


class DriftDetector:

    @staticmethod
    def Comparar(SessaoAntiga, Alvo):
        if not SessaoAntiga or not Alvo:
            return {"ok": False, "motivo": "sessao_ou_alvo_ausente"}
        EstadoSalvo = (SessaoAntiga.get("estado") or {})
        HostsSalvos = EstadoSalvo.get("hosts") or []
        HostSalvo = next((H for H in HostsSalvos if H.get("ip") == Alvo), None)
        if not HostSalvo:
            return {"ok": False, "motivo": "alvo_nao_estava_na_sessao"}
        if not Analise:
            return {"ok": False, "motivo": "Analise_indisponivel"}
        Atual = Analise.EscanearAlvo(Alvo, [22, 80, 443], 2)
        PortasAntigas = set(HostSalvo.get("portas_abertas") or [])
        PortasNovas = set(Atual.get("portas_abertas") or [])
        FabAntigo = HostSalvo.get("fabricante")
        FabNovo = Atual.get("fabricante")
        Mudancas = []
        for P in sorted(PortasAntigas - PortasNovas):
            Mudancas.append({"tipo": "porta_fechou", "porta": P})
        for P in sorted(PortasNovas - PortasAntigas):
            Mudancas.append({"tipo": "porta_abriu", "porta": P})
        if FabAntigo != FabNovo:
            Mudancas.append({"tipo": "fabricante_mudou", "antes": FabAntigo, "depois": FabNovo})
        return {"ok": True, "alvo": Alvo, "mudancas": Mudancas,
                "total_mudancas": len(Mudancas),
                "sem_mudancas": len(Mudancas) == 0}


class SalaCadeias:

    @staticmethod
    def _Templates():
        if not Cadeia:
            return []
        R = Cadeia.Templates()
        return R.get("templates") or []

    @staticmethod
    def _ValidarTemplate(Template):
        if not Cadeia:
            return {"ok": False, "motivo": "Cadeia_indisponivel"}
        return Cadeia.Validar(Template.get("blocos") or [])

    @staticmethod
    def Desenhar(Est, Altura):
        Render.IrPara(7, 1)
        Render.Escrever(f"{Cor.BOLD}{Cor.MAGENTA}CADEIAS{Cor.RESET}  "
                        f"{Cor.CINZA}Enter=executar | F8=passo | V=validar{Cor.RESET}")
        Templates = SalaCadeias._Templates()
        if not Templates:
            Render.IrPara(9, 1)
            Render.Escrever(f"{Cor.CINZA}Cadeia indisponivel{Cor.RESET}")
            return
        Render.IrPara(8, 1)
        Render.Escrever(f"{Cor.CINZA}templates: {len(Templates)}{Cor.RESET}")
        Linha = 10
        for I, T in enumerate(Templates[:Altura - 14]):
            Render.IrPara(Linha, 1)
            Selecionado = I == Est.Selecionado
            Pref = f"{Cor.INVERT}{Cor.BOLD}>{Cor.RESET}" if Selecionado else " "
            V = SalaCadeias._ValidarTemplate(T)
            Icone = Badge.Ok() if V.get("ok") else Badge.Aviso()
            Nome = T.get("nome", "?")
            Desc = T.get("descricao", "")
            NumBlocos = len(T.get("blocos") or [])
            Render.Escrever(f" {Pref} {Icone} {Cor.MAGENTA}{Nome:20s}{Cor.RESET} "
                            f"{Cor.CINZA}({NumBlocos} blocos){Cor.RESET}  {Desc}",
                            SemQuebra=False)
            if Selecionado and V.get("avisos"):
                for Aviso in V["avisos"][:2]:
                    Linha += 1
                    Render.IrPara(Linha, 1)
                    Render.Escrever(f"       {Cor.AMARELO}⚠ {Aviso}{Cor.RESET}", SemQuebra=False)
            if Selecionado:
                ExecucaoAtual = Est.Cache.get(f"cadeia_{Nome}_resultado")
                if ExecucaoAtual:
                    BlocosExec = ExecucaoAtual.get("blocos_resultado") or []
                    Estados = {B["indice"]: B["estado"] for B in BlocosExec}
                    Tempos = {B["indice"]: B.get("tempo_ms") for B in BlocosExec}
                    LinhasBlocos = RenderCadeia.Cadeia(T.get("blocos") or [], Estados, Tempos)
                    for LB in LinhasBlocos:
                        Linha += 1
                        if Linha > Altura - 4:
                            break
                        Render.IrPara(Linha, 1)
                        Render.Escrever(LB, SemQuebra=False)
            Linha += 2

    @staticmethod
    def Acao(Est, Acao_):
        Templates = SalaCadeias._Templates()
        if not Templates:
            return False
        Indice = min(Est.Selecionado, len(Templates) - 1)
        T = Templates[Indice]
        Nome = T.get("nome", "?")
        if Acao_ == "enter":
            Alvo = Est.Cache.get("alvo_atual") or "127.0.0.1"
            Spinner.Mostrar(0.5, f"cadeia {Nome}")
            R = Cadeia.Executar(T.get("blocos") or [], Alvo)
            Est.Cache[f"cadeia_{Nome}_resultado"] = R
            Est.Registrar(f"cadeia {Nome}", R.get("ok"))
            Est.MostrarToast(f"{Nome}: {R.get('estado')} ({R.get('tempo_total_ms')}ms)")
            return True
        if Acao_ == "V":
            V = SalaCadeias._ValidarTemplate(T)
            if V.get("ok"):
                Est.MostrarToast(f"{Nome}: valido, {V.get('total_blocos')} blocos")
            else:
                Erros = V.get("erros") or ["?"]
                Est.MostrarToast(f"{Nome}: {Erros[0][:50]}")
            return True
        if Acao_ == "F8":
            Alvo = Est.Cache.get("alvo_atual") or "127.0.0.1"
            Blocos = T.get("blocos") or []
            IndiceAtual = Est.Cache.get(f"cadeia_{Nome}_passo", -1) + 1
            if IndiceAtual >= len(Blocos):
                Est.MostrarToast(f"{Nome}: fim da cadeia")
                Est.Cache[f"cadeia_{Nome}_passo"] = -1
                return True
            SubBlocos = [Blocos[IndiceAtual]]
            R = Cadeia.Executar(SubBlocos, Alvo)
            Est.Cache[f"cadeia_{Nome}_passo"] = IndiceAtual
            BlocoResultado = (R.get("blocos_resultado") or [{}])[0]
            Estados = Est.Cache.setdefault(f"cadeia_{Nome}_estados", {})
            Estados[IndiceAtual] = BlocoResultado.get("estado", "ocioso")
            Est.MostrarToast(f"passo {IndiceAtual}/{len(Blocos)}: {BlocoResultado.get('estado')}")
            return True
        return False


class SalaEstado:

    @staticmethod
    def Desenhar(Est, Altura):
        Render.IrPara(7, 1)
        Render.Escrever(f"{Cor.BOLD}{Cor.CIANO}ESTADO{Cor.RESET}  "
                        f"{Cor.CINZA}D=drift | s=salvar sessao | L=limpar cache{Cor.RESET}")
        Linha = 9
        Render.IrPara(Linha, 1)
        Render.Escrever(f"{Cor.BOLD}sessoes{Cor.RESET}")
        Linha += 1
        if Sessao:
            R = Sessao.Listar()
            Sessoes = R.get("sessoes") or []
            if not Sessoes:
                Render.IrPara(Linha, 1)
                Render.Escrever(f"  {Cor.CINZA}nenhuma sessao salva{Cor.RESET}")
            else:
                for S in Sessoes[:3]:
                    if Linha > Altura - 12:
                        break
                    Render.IrPara(Linha, 1)
                    Idade = S.get("idade_segundos")
                    IdadeStr = f"{int(Idade)}s" if Idade else "?"
                    Render.Escrever(f"  {Cor.CIANO}•{Cor.RESET} {S['nome']:32s} "
                                    f"{Cor.CINZA}[{IdadeStr}, {S['tamanho_bytes']}b]{Cor.RESET}",
                                    SemQuebra=False)
                    Linha += 1
        else:
            Render.IrPara(Linha, 1)
            Render.Escrever(f"  {Cor.VERMELHO}Sessao indisponivel{Cor.RESET}")
            Linha += 1
        Linha += 1
        Render.IrPara(Linha, 1)
        Render.Escrever(f"{Cor.BOLD}ultimas acoes{Cor.RESET}")
        Linha += 1
        if Est.Historico:
            for H in Est.Historico[-4:]:
                if Linha > Altura - 6:
                    break
                Marca = Badge.Ok() if H.get("ok") else Badge.Falha()
                Render.IrPara(Linha, 1)
                Ts = (H.get("ts") or "")[11:19]
                Render.Escrever(f"  {Marca} {Cor.CINZA}{Ts}{Cor.RESET}  {H.get('cmd')}",
                                SemQuebra=False)
                Linha += 1
        else:
            Render.IrPara(Linha, 1)
            Render.Escrever(f"  {Cor.CINZA}nenhuma acao{Cor.RESET}")
            Linha += 1
        Linha += 1
        Fed = HistoricoFederado.Ultimos(3)
        if Fed:
            Linha += 1
            Render.IrPara(Linha, 1)
            Render.Escrever(f"{Cor.BOLD}historico federado{Cor.RESET}")
            Linha += 1
            for H in Fed:
                if Linha > Altura - 3:
                    break
                Marca = Badge.Ok() if H.get("ok") else Badge.Falha()
                Render.IrPara(Linha, 1)
                Ts = (H.get("ts") or "")[11:19]
                Render.Escrever(f"  {Marca} {Cor.CINZA}{Ts} {H.get('prefixo')}{Cor.RESET}  {H.get('cmd')}",
                                SemQuebra=False)
                Linha += 1
        Drift = Est.Cache.get("drift_resultado")
        if Drift and Drift.get("ok"):
            Render.IrPara(Linha, 1)
            Render.Escrever(f"{Cor.BOLD}drift ({Drift.get('alvo')}){Cor.RESET}")
            Linha += 1
            if Drift.get("sem_mudancas"):
                Render.IrPara(Linha, 1)
                Render.Escrever(f"  {Cor.VERDE}sem mudancas{Cor.RESET}")
            else:
                for M in (Drift.get("mudancas") or [])[:Altura - Linha - 2]:
                    Render.IrPara(Linha, 1)
                    if M["tipo"] == "porta_fechou":
                        Render.Escrever(f"  {Cor.VERMELHO}✗ porta {M['porta']} fechou{Cor.RESET}",
                                        SemQuebra=False)
                    elif M["tipo"] == "porta_abriu":
                        Render.Escrever(f"  {Cor.VERDE}✓ porta {M['porta']} abriu{Cor.RESET}",
                                        SemQuebra=False)
                    elif M["tipo"] == "fabricante_mudou":
                        Render.Escrever(f"  {Cor.AMARELO}⚠ fabricante: "
                                        f"{M['antes']} -> {M['depois']}{Cor.RESET}",
                                        SemQuebra=False)
                    Linha += 1

    @staticmethod
    def Acao(Est, Acao_):
        if Acao_ == "D":
            if not Sessao or not Analise:
                Est.MostrarToast("Sessao/Analise indisponivel")
                return True
            Lista = Sessao.Listar()
            Sessoes = Lista.get("sessoes") or []
            if not Sessoes:
                Est.MostrarToast("nenhuma sessao pra comparar")
                return True
            Alvo = Est.Cache.get("alvo_atual") or "127.0.0.1"
            R = Sessao.Carregar(Sessoes[0]["nome"])
            if not R.get("ok"):
                Est.MostrarToast(f"erro: {R.get('motivo')}")
                return True
            Drift = DriftDetector.Comparar(R, Alvo)
            Est.Cache["drift_resultado"] = Drift
            if Drift.get("ok"):
                Est.MostrarToast(f"drift: {Drift.get('total_mudancas')} mudancas em {Alvo}")
            else:
                Est.MostrarToast(f"drift: {Drift.get('motivo')}")
            return True
        if Acao_ == "L":
            Est.Cache.pop("drift_resultado", None)
            Est.MostrarToast("cache limpo")
            return True
        return False


class Federacao:

    INSTANCIAS = {}
    PROXIMO_ID = 1

    @staticmethod
    def _CorPorHost(Host):
        Cores = [Cor.CIANO, Cor.MAGENTA, Cor.AZUL, Cor.VERDE, Cor.AMARELO]
        try:
            H = sum(ord(C) for C in Host)
            return Cores[H % len(Cores)]
        except Exception:
            return Cor.CINZA

    @staticmethod
    def Conectar(Host, Porta, Token, Timeout=5):
        if not Host or not Porta or not Token:
            return {"ok": False, "motivo": "host_porta_token_obrigatorios"}
        Url = f"http://{Host}:{int(Porta)}/api/health"
        Req = urllib.request.Request(Url)
        Req.add_header("Authorization", f"Bearer {Token}")
        Inicio = time.monotonic()
        try:
            with urllib.request.urlopen(Req, timeout=Timeout) as Resp:
                Corpo = json.loads(Resp.read().decode("utf-8"))
        except urllib.error.HTTPError as E:
            return {"ok": False, "motivo": f"http_{E.code}"}
        except urllib.error.URLError as E:
            return {"ok": False, "motivo": f"url_{getattr(E, 'reason', 'erro')}"}
        except Exception as E:
            return {"ok": False, "motivo": f"geral_{type(E).__name__}", "erro": str(E)}
        Latencia = round((time.monotonic() - Inicio) * 1000.0, 2)
        Id = f"inst_{Federacao.PROXIMO_ID}"
        Federacao.PROXIMO_ID += 1
        Info = {
            "id": Id, "host": Host, "porta": int(Porta), "token": Token,
            "latencia_ms": Latencia, "uptime_s": Corpo.get("uptime_s"),
            "cor": Federacao._CorPorHost(Host),
            "versao": Corpo.get("versao") or "?",
            "conectado_em": datetime.now(timezone.utc).isoformat(),
        }
        Federacao.INSTANCIAS[Id] = Info
        return {"ok": True, "id": Id, "instancia": Info}

    @staticmethod
    def Desconectar(Id):
        if Id not in Federacao.INSTANCIAS:
            return {"ok": False, "motivo": "instancia_nao_encontrada"}
        Removida = Federacao.INSTANCIAS.pop(Id)
        return {"ok": True, "removida": Removida}

    @staticmethod
    def ListarInstancias():
        return {"ok": True, "instancias": list(Federacao.INSTANCIAS.values()),
                "total": len(Federacao.INSTANCIAS)}

    @staticmethod
    def _Get(Instancia, Rota, Timeout=5):
        Url = f"http://{Instancia['host']}:{int(Instancia['porta'])}{Rota}"
        Req = urllib.request.Request(Url)
        Req.add_header("Authorization", f"Bearer {Instancia['token']}")
        try:
            with urllib.request.urlopen(Req, timeout=Timeout) as R:
                return {"ok": True, "status": R.status, "corpo": json.loads(R.read().decode("utf-8"))}
        except urllib.error.HTTPError as E:
            try:
                return {"ok": False, "status": E.code, "corpo": json.loads(E.read().decode("utf-8"))}
            except Exception:
                return {"ok": False, "status": E.code, "motivo": "http_error"}
        except Exception as E:
            return {"ok": False, "motivo": f"{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def _Post(Instancia, Rota, Corpo, Timeout=10):
        Url = f"http://{Instancia['host']}:{int(Instancia['porta'])}{Rota}"
        Dados = json.dumps(Corpo).encode("utf-8")
        Req = urllib.request.Request(Url, data=Dados, method="POST",
                                      headers={"Content-Type": "application/json"})
        Req.add_header("Authorization", f"Bearer {Instancia['token']}")
        Inicio = time.monotonic()
        try:
            with urllib.request.urlopen(Req, timeout=Timeout) as R:
                return {"ok": True, "status": R.status, "corpo": json.loads(R.read().decode("utf-8")),
                        "latencia_ms": round((time.monotonic() - Inicio) * 1000.0, 2)}
        except urllib.error.HTTPError as E:
            try:
                return {"ok": False, "status": E.code, "corpo": json.loads(E.read().decode("utf-8")),
                        "latencia_ms": round((time.monotonic() - Inicio) * 1000.0, 2)}
            except Exception:
                return {"ok": False, "status": E.code, "motivo": "http_error"}
        except Exception as E:
            return {"ok": False, "motivo": f"{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def ListarSalasRemotas(Instancia):
        return Federacao._Get(Instancia, "/api/salas")

    @staticmethod
    def EstadoSalaRemota(Instancia, Sala):
        return Federacao._Get(Instancia, f"/api/salas/{Sala}")

    @staticmethod
    def ExecutarRemoto(Instancia, Sala, Cmd, Args=None):
        R = Federacao._Post(Instancia, f"/api/salas/{Sala}/acao",
                            {"cmd": Cmd, "args": Args or {}})
        try:
            HistoricoFederado.Registrar(Instancia, Cmd, R.get("ok"),
                                        R.get("latencia_ms"))
        except Exception:
            pass
        return R

    @staticmethod
    def AguardarInstancia(Instancia, Tentativas=5, EsperaMs=200):
        for _ in range(Tentativas):
            R = Federacao._Get(Instancia, "/api/health", Timeout=2)
            if R.get("ok"):
                return R
            time.sleep(EsperaMs / 1000.0)
        return {"ok": False, "motivo": "timeout_health"}


class SalaFederacao:

    @staticmethod
    def Desenhar(Est, Altura):
        Render.IrPara(7, 1)
        Render.Escrever(f"{Cor.BOLD}{Cor.MAGENTA}FEDERACAO{Cor.RESET}  "
                        f"{Cor.CINZA}F=adicionar | Enter=entrar | d=remover{Cor.RESET}")
        Prompt = Est.Cache.get("prompt_fed")
        if Prompt is not None:
            Render.IrPara(8, 1)
            Render.Escrever(f" {Cor.MAGENTA}fed>{Cor.RESET} {Prompt}{Cor.INVERT} {Cor.RESET}")
        Locais = Api is not None and Api.Servidor is not None
        CorLocal = Cor.VERDE if Locais else Cor.CINZA
        Render.IrPara(9, 1)
        Render.Escrever(f"{CorLocal}● local{Cor.RESET}  "
                        f"{Cor.CINZA}{'porta ' + str(Api.Porta) if Locais else 'api nao iniciada'}{Cor.RESET}")
        R = Federacao.ListarInstancias()
        Instancias = R.get("instancias") or []
        Render.IrPara(11, 1)
        Render.Escrever(f"{Cor.BOLD}remotas ({len(Instancias)}){Cor.RESET}")
        if not Instancias:
            Render.IrPara(12, 1)
            Render.Escrever(f"  {Cor.CINZA}F para adicionar (host:porta token){Cor.RESET}")
            return
        Linha = 12
        for I, Inst in enumerate(Instancias[:Altura - 15]):
            if Linha > Altura - 3:
                break
            Render.IrPara(Linha, 1)
            Selecionado = I == Est.Selecionado
            Pref = f"{Cor.INVERT}{Cor.BOLD}>{Cor.RESET}" if Selecionado else " "
            Cor_ = Inst.get("cor") or Cor.CIANO
            Lat = Inst.get("latencia_ms", 0)
            Id = Inst.get("id", "?")
            Host = Inst.get("host", "?")
            Porta = Inst.get("porta", 0)
            Versao = Inst.get("versao", "?")
            Render.Escrever(f" {Pref} {Cor_}●{Cor.RESET} {Id:8s} "
                            f"{Cor.BOLD}{Host}:{Porta}{Cor.RESET}  "
                            f"{Cor.CINZA}v{Versao} {int(Lat)}ms{Cor.RESET}",
                            SemQuebra=False)
            Linha += 1

    @staticmethod
    def PromptAbrir(Est):
        Est.Cache["prompt_fed"] = ""
        Est.Selecionado = 0
        return True

    @staticmethod
    def PromptTecla(Est, Char):
        if "prompt_fed" not in Est.Cache:
            return False
        if Char in ("\x7f", "backspace"):
            Est.Cache["prompt_fed"] = Est.Cache["prompt_fed"][:-1]
            return True
        if len(Char) == 1 and Char.isprintable():
            Est.Cache["prompt_fed"] += Char
            return True
        return False

    @staticmethod
    def PromptEnter(Est):
        Texto = (Est.Cache.get("prompt_fed") or "").strip()
        Est.Cache.pop("prompt_fed", None)
        if not Texto:
            return True
        Partes = Texto.split()
        if len(Partes) < 2:
            Est.MostrarToast("formato: host:porta token")
            return True
        HostPorta = Partes[0]
        Token = Partes[1]
        if ":" not in HostPorta:
            Est.MostrarToast("formato: host:porta token")
            return True
        Host, PortaStr = HostPorta.rsplit(":", 1)
        try:
            Porta = int(PortaStr)
        except ValueError:
            Est.MostrarToast("porta invalida")
            return True
        Spinner.Mostrar(0.4, f"conectar {Host}:{Porta}")
        R = Federacao.Conectar(Host, Porta, Token)
        if R.get("ok"):
            Inst = R["instancia"]
            Est.MostrarToast(f"conectado: {Host}:{Porta} ({int(Inst['latencia_ms'])}ms)")
            Est.Registrar(f"fed {Host}:{Porta}", True)
        else:
            Est.MostrarToast(f"falha: {R.get('motivo')}")
        return True

    @staticmethod
    def Acao(Est, Acao_):
        if "prompt_fed" in Est.Cache:
            if Acao_ == "enter":
                return SalaFederacao.PromptEnter(Est)
            return False
        if Acao_ == "F":
            return SalaFederacao.PromptAbrir(Est)
        Instancias = Federacao.ListarInstancias()["instancias"]
        if not Instancias:
            return False
        Indice = min(Est.Selecionado, len(Instancias) - 1)
        Inst = Instancias[Indice]
        if Acao_ == "enter":
            Spinner.Mostrar(0.3, f"salas remotas de {Inst['host']}")
            R = Federacao.ListarSalasRemotas(Inst)
            if R.get("ok"):
                Salas = (R.get("corpo") or {}).get("salas") or []
                Est.Cache["salas_remotas"] = {"instancia": Inst, "salas": Salas}
                Est.MostrarToast(f"{Inst['host']}: {len(Salas)} salas")
            else:
                Est.MostrarToast(f"erro: {R.get('motivo')}")
            return True
        if Acao_ == "d":
            R = Federacao.Desconectar(Inst["id"])
            if R.get("ok"):
                Est.MostrarToast(f"desconectado: {Inst['host']}")
            return True
        return False


def RenderRodapeFederado(Est):
    if not Federacao.INSTANCIAS:
        return
    L, A = Render.Dimensoes()
    Partes = [f"{Cor.VERDE}local{Cor.RESET}"]
    for Inst in list(Federacao.INSTANCIAS.values())[:2]:
        Cor_ = Inst.get("cor") or Cor.CIANO
        Partes.append(f"{Cor_}{Inst['host']}:{Inst['porta']}{Cor.RESET}")
    Linha = "  ".join(Partes)
    Render.IrPara(A - 1, 1)
    Render.Escrever(f"{Cor.CINZA}nos: {Linha}{Cor.RESET}", SemQuebra=False)


def FederacaoAutoTeste():
    if not Api:
        return {"ok": False, "motivo": "Api_indisponivel"}
    R1 = Api.Iniciar(Escuta="127.0.0.1", Porta=8765)
    if not R1.get("ok"):
        return {"ok": False, "motivo": "api1_falhou", "detalhe": R1}
    Inst2 = {
        "id": "auto", "host": "127.0.0.1", "porta": 8765,
        "token": R1["token"], "latencia_ms": 0, "versao": Api.VERSAO,
        "cor": Cor.CIANO,
    }
    H = Federacao.AguardarInstancia(Inst2, Tentativas=3)
    if not H.get("ok"):
        Api.Parar()
        return {"ok": False, "motivo": "health_falhou", "detalhe": H}
    Salas = Federacao.ListarSalasRemotas(Inst2)
    if not Salas.get("ok"):
        Api.Parar()
        return {"ok": False, "motivo": "salas_falhou", "detalhe": Salas}
    Cmd = Federacao.ExecutarRemoto(Inst2, "comandos", "cred", {"alvo": "192.168.0.2"})
    Api.Parar()
    return {
        "ok": Cmd.get("ok"),
        "token_recebido": bool(R1.get("token")),
        "health_uptime": H.get("corpo", {}).get("uptime_s"),
        "salas_total": len((Salas.get("corpo") or {}).get("salas") or []),
        "cmd_remoto_ok": Cmd.get("ok"),
        "cmd_remoto_total_creds": (Cmd.get("corpo") or {}).get("resultado", {}).get("total"),
        "latencia_ms": Cmd.get("latencia_ms"),
    }


class HashCurto:

    @staticmethod
    def De(Texto):
        if not Texto:
            return "--------"
        try:
            import hashlib
            H = hashlib.sha256(str(Texto).encode("utf-8", "replace")).hexdigest()
            return H[:8]
        except Exception:
            return "errohash"


class ModoOperador:

    @staticmethod
    def IpLocal():
        try:
            S = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            S.settimeout(0.5)
            S.connect(("8.8.8.8", 80))
            Ip = S.getsockname()[0]
            S.close()
            return Ip
        except Exception:
            try:
                return socket.gethostbyname(socket.gethostname())
            except Exception:
                return "127.0.0.1"

    @staticmethod
    def HoraUtc():
        return datetime.now(timezone.utc).strftime("%H:%M:%SZ")

    @staticmethod
    def HoraLocal():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def Contexto(Est):
        Ultimo = Est.Historico[-1] if Est.Historico else {}
        Cmd = Ultimo.get("cmd") or "—"
        Ts = Ultimo.get("ts") or ""
        Hash = HashCurto.De(f"{Cmd}|{Ts}")
        Ip = Est.Cache.get("ip_local") or ModoOperador.IpLocal()
        Est.Cache["ip_local"] = Ip
        return {
            "utc": ModoOperador.HoraUtc(),
            "local": ModoOperador.HoraLocal(),
            "ip": Ip,
            "ultimo_cmd": Cmd,
            "ultimo_hash": Hash,
            "historico_total": len(Est.Historico),
        }

    @staticmethod
    def Toggle(Est):
        Est.Cache["modo_operador"] = not Est.Cache.get("modo_operador", False)
        Est.MostrarToast("operador ON" if Est.Cache["modo_operador"] else "operador OFF")


class RenderOperador:

    @staticmethod
    def Desenhar(Est):
        if not Est.Cache.get("modo_operador"):
            return
        L, A = Render.Dimensoes()
        Ctx = ModoOperador.Contexto(Est)
        Linha1 = (f"{Cor.CINZA}utc {Ctx['utc']}  "
                  f"local {Ctx['local']}  "
                  f"ip {Ctx['ip']}  "
                  f"hash {Cor.AMARELO}{Ctx['ultimo_hash']}{Cor.RESET}{Cor.CINZA}  "
                  f"hist {Ctx['historico_total']}{Cor.RESET}")
        Render.IrPara(A - 2, 1)
        if Est.ToastAtivo():
            return
        Render.Escrever(Render.Truncar(Linha1, L), SemQuebra=False)


class HistoricoFederado:

    MAXIMO = 40

    @staticmethod
    def Registrar(Instancia, Cmd, Ok, TempoMs=None, Extra=None):
        Est = Instancia.get("estado") if isinstance(Instancia, dict) else None
        Host = Instancia.get("host", "?") if isinstance(Instancia, dict) else "?"
        Porta = Instancia.get("porta", 0) if isinstance(Instancia, dict) else 0
        Prefixo = f"@{Host}:{Porta}"
        HistoricoFederado.Lista().append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "prefixo": Prefixo, "cmd": Cmd, "ok": bool(Ok),
            "tempo_ms": TempoMs, "extra": Extra or {},
        })
        while len(HistoricoFederado.Lista()) > HistoricoFederado.MAXIMO:
            HistoricoFederado.Lista().pop(0)
        return {"ok": True, "total": len(HistoricoFederado.Lista())}

    _BUF = []

    @staticmethod
    def Lista():
        return HistoricoFederado._BUF

    @staticmethod
    def Ultimos(N=5):
        return HistoricoFederado.Lista()[-N:]

    @staticmethod
    def Limpar():
        HistoricoFederado._BUF = []
        return {"ok": True}


class AnimacaoSaida:

    @staticmethod
    def Rodar(Est, Duracao=0.2):
        L, A = Render.Dimensoes()
        Quadros = 4
        Delays = Duracao / max(1, Quadros)
        for Q in range(Quadros):
            Cobertos = int((Q + 1) * A / Quadros)
            for Linha in range(A - Cobertos + 1, A + 1):
                if Linha < 1:
                    continue
                Render.IrPara(Linha, 1)
                sys.stdout.write(" " * L)
            sys.stdout.flush()
            time.sleep(Delays)
        Render.Limpar()


class SalvarAuto:

    @staticmethod
    def Rodar(Est, Motivo="saida"):
        if not Sessao:
            return {"ok": False, "motivo": "Sessao_indisponivel"}
        if Est.Cache.get("modo_fantasma"):
            return {"ok": True, "motivo": "fantasma_nao_salva"}
        Nome = f"auto_{int(time.time())}"
        Estado_ = {
            "sala": Est.SalaAtual,
            "historico": Est.Historico[-20:],
            "historico_federado": HistoricoFederado.Ultimos(10),
            "cache_resumo": {
                "modo": Est.Modo,
                "alvos_conhecidos": Est.AlvosConhecidos,
                "shells_ativas": Est.ShellsAtivas,
                "motivo": Motivo,
            },
        }
        R = Sessao.Salvar(Nome, Estado_)
        if R.get("ok"):
            Est.SessaoNome = Nome
        return R


class IntegracaoServidor:

    @staticmethod
    def SubirApi(Escuta="127.0.0.1", Porta=8765):
        if not Api:
            return {"ok": False, "motivo": "Api_indisponivel"}
        if Api.Servidor is not None:
            return {"ok": True, "ja_rodando": True, "porta": Api.Porta}
        return Api.Iniciar(Escuta=Escuta, Porta=Porta)

    @staticmethod
    def DerrubarApi():
        if not Api:
            return {"ok": True, "motivo": "Api_indisponivel"}
        return Api.Parar()

    @staticmethod
    def InfoApi():
        if not Api:
            return {"rodando": False, "motivo": "Api_indisponivel"}
        if Api.Servidor is None:
            return {"rodando": False}
        return {"rodando": True, "porta": Api.Porta, "escuta": Api.Escuta,
                "uptime_s": Api.UptimeSegundos(),
                "token_tamanho": len(Api.Token) if Api.Token else 0}


def PatchIntegracaoFinal():
    Caminho = "Console.py"
    Src = open(Caminho, "r", encoding="utf-8").read()
    Modificacoes = 0

    Antigo1 = '''    if Acao_ == "nova_sessao":
        Est.MostrarToast("nova sessao")
        return True
    if Acao_ == "O":
        ModoOperador.Toggle(Est)
        return True
    if Char == "F" and Est.SalaAtual != "federacao" and "prompt_fed" not in Est.Cache:
        return SalaFederacao.PromptAbrir(Est)'''

    Novo1 = '''    if Acao_ == "nova_sessao":
        Est.MostrarToast("nova sessao")
        return True
    if Acao_ == "O":
        ModoOperador.Toggle(Est)
        return True
    if Char == "F" and Est.SalaAtual != "federacao" and "prompt_fed" not in Est.Cache:
        return SalaFederacao.PromptAbrir(Est)
    if Acao_ == "O":
        ModoOperador.Toggle(Est)
        return True
    if Char == "F" and Est.SalaAtual != "federacao" and "prompt_fed" not in Est.Cache:
        return SalaFederacao.PromptAbrir(Est)'''

    if Antigo1 in Src:
        Src = Src.replace(Antigo1, Novo1)
        Modificacoes += 1

    Antigo2 = '''        Drift = Est.Cache.get("drift_resultado")
        if Drift and Drift.get("ok"):'''

    Novo2 = '''        Fed = HistoricoFederado.Ultimos(3)
        if Fed:
            Linha += 1
            Render.IrPara(Linha, 1)
            Render.Escrever(f"{Cor.BOLD}historico federado{Cor.RESET}")
            Linha += 1
            for H in Fed:
                if Linha > Altura - 3:
                    break
                Marca = Badge.Ok() if H.get("ok") else Badge.Falha()
                Render.IrPara(Linha, 1)
                Ts = (H.get("ts") or "")[11:19]
                Render.Escrever(f"  {Marca} {Cor.CINZA}{Ts} {H.get('prefixo')}{Cor.RESET}  {H.get('cmd')}",
                                SemQuebra=False)
                Linha += 1
        Drift = Est.Cache.get("drift_resultado")
        if Drift and Drift.get("ok"):'''

    if Antigo2 in Src:
        Src = Src.replace(Antigo2, Novo2, 1)
        Modificacoes += 1

    Antigo3 = '''    def ExecutarRemoto(Instancia, Sala, Cmd, Args=None):
        R = Federacao._Post(Instancia, f"/api/salas/{Sala}/acao",
                            {"cmd": Cmd, "args": Args or {}})
        try:
            HistoricoFederado.Registrar(Instancia, Cmd, R.get("ok"),
                                        R.get("latencia_ms"))
        except Exception:
            pass
        return R'''

    Novo3 = '''    def ExecutarRemoto(Instancia, Sala, Cmd, Args=None):
        R = Federacao._Post(Instancia, f"/api/salas/{Sala}/acao",
                            {"cmd": Cmd, "args": Args or {}})
        try:
            HistoricoFederado.Registrar(Instancia, Cmd, R.get("ok"),
                                        R.get("latencia_ms"))
        except Exception:
            pass
        return R'''

    if Antigo3 in Src:
        Src = Src.replace(Antigo3, Novo3)
        Modificacoes += 1

    open(Caminho, "w", encoding="utf-8").write(Src)
    return {"ok": True, "modificacoes": Modificacoes}


class Servidor:

    @staticmethod
    def Iniciar(Escuta="127.0.0.1", Porta=8765):
        R = IntegracaoServidor.SubirApi(Escuta, Porta)
        if R.get("ok"):
            Info = IntegracaoServidor.InfoApi()
            return {"ok": True, "porta": Info.get("porta"), "info": Info}
        return {"ok": False, "motivo": R.get("motivo") or "desconhecido", "detalhe": R}

    @staticmethod
    def Status():
        return IntegracaoServidor.InfoApi()

    @staticmethod
    def Parar():
        return IntegracaoServidor.DerrubarApi()


def PatchMainServidor():
    Caminho = "Console.py"
    Src = open(Caminho, "r", encoding="utf-8").read()

    Antigo = '''def Main():
    P = argparse.ArgumentParser(prog="Console")
    P.add_argument("comando", nargs="?", default=None, choices=["bypass", "servidor", "status"])
    P.add_argument("--modo", default="local", choices=["local", "servidor", "federado"])
    P.add_argument("--porta-api", type=int, default=8765)
    P.add_argument("--escutar-api", default="127.0.0.1")
    Args = P.parse_args()

    if Args.comando == "bypass":
        R = BypassCentral()
        for Nome, Ok in R["checagens"]:
            Marca = f"{Cor.VERDE}ok{Cor.RESET}" if Ok else f"{Cor.VERMELHO}falta{Cor.RESET}"
            print(f"  {Nome:20s} {Marca}")
        if not R["ok"]:
            print(f"\\n{Cor.VERMELHO}base incompleta: {', '.join(R['falhas'])}{Cor.RESET}")
            return 1
        Est = Estado()
        Est.Modo = Args.modo
        if Sessao:
            Lista = Sessao.Listar()
            if Lista.get("ok") and Lista.get("total", 0) > 0:
                Ultima = Lista["sessoes"][0]
                Est.SessaoNome = Ultima["nome"]
                Est.MostrarToast(f"retomada: {Ultima['nome']} (Ctrl+N nova)")
        if Args.modo in ("servidor", "federado"):
            Srv = Servidor.Iniciar(Args.escutar_api, Args.porta_api)
            if Srv.get("ok"):
                Est.Cache["api_rodando"] = True
                Est.Cache["api_porta"] = Srv.get("porta")
                Est.MostrarToast(f"api :{Srv.get('porta')} ativa")
            else:
                Est.MostrarToast(f"api nao subiu: {Srv.get('motivo')}")
        try:
            return MainLoop(Est)
        finally:
            if Est.Cache.get("api_rodando"):
                Servidor.Parar()
            SalvarAuto.Rodar(Est, "saida")

    if Args.comando == "servidor":
        R = Servidor.Iniciar(Args.escutar_api, Args.porta_api)
        if not R.get("ok"):
            print(f"{Cor.VERMELHO}api nao subiu: {R.get('motivo')}{Cor.RESET}")
            return 1
        Info = R.get("info") or {}
        print(f"{Cor.VERDE}api em http://{Info.get('escuta')}:{Info.get('porta')}{Cor.RESET}")
        print(f"token: {Api.Token if Api else '?'}")
        print(f"{Cor.CINZA}Ctrl+C para derrubar{Cor.RESET}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            Servidor.Parar()
            print(f"{Cor.CINZA}api derrubada{Cor.RESET}")
            return 0

    if Args.comando == "status":
        R = Servidor.Status()
        print(json.dumps(R, indent=2, ensure_ascii=False))
        return 0 if R.get("rodando") else 1

    print("uso: python3 Console.py bypass|servidor|status [--modo local|servidor|federado]")
    return 2'''

    Novo = '''def Main():
    P = argparse.ArgumentParser(prog="Console")
    P.add_argument("comando", nargs="?", default=None, choices=["bypass", "servidor", "status"])
    P.add_argument("--modo", default="local", choices=["local", "servidor", "federado"])
    P.add_argument("--porta-api", type=int, default=8765)
    P.add_argument("--escutar-api", default="127.0.0.1")
    Args = P.parse_args()

    if Args.comando == "servidor":
        R = Servidor.Iniciar(Args.escutar_api, Args.porta_api)
        if not R.get("ok"):
            print(f"{Cor.VERMELHO}api nao subiu: {R.get('motivo')}{Cor.RESET}")
            return 1
        Info = R.get("info") or {}
        print(f"{Cor.VERDE}api em http://{Info.get('escuta')}:{Info.get('porta')}{Cor.RESET}")
        print(f"token: {Api.Token if Api else '?'}")
        print(f"{Cor.CINZA}Ctrl+C para derrubar{Cor.RESET}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            Servidor.Parar()
            print(f"{Cor.CINZA}api derrubada{Cor.RESET}")
            return 0

    if Args.comando == "status":
        R = Servidor.Status()
        print(json.dumps(R, indent=2, ensure_ascii=False))
        return 0 if R.get("rodando") else 1

    if Args.comando == "bypass":
        R = BypassCentral()
        for Nome, Ok in R["checagens"]:
            Marca = f"{Cor.VERDE}ok{Cor.RESET}" if Ok else f"{Cor.VERMELHO}falta{Cor.RESET}"
            print(f"  {Nome:20s} {Marca}")
        if not R["ok"]:
            print(f"\\n{Cor.VERMELHO}base incompleta: {', '.join(R['falhas'])}{Cor.RESET}")
            return 1
        Est = Estado()
        Est.Modo = Args.modo
        if Sessao:
            Lista = Sessao.Listar()
            if Lista.get("ok") and Lista.get("total", 0) > 0:
                Ultima = Lista["sessoes"][0]
                Est.SessaoNome = Ultima["nome"]
                Est.MostrarToast(f"retomada: {Ultima['nome']} (Ctrl+N nova)")
        if Args.modo in ("servidor", "federado"):
            Srv = Servidor.Iniciar(Args.escutar_api, Args.porta_api)
            if Srv.get("ok"):
                Est.Cache["api_rodando"] = True
                Est.Cache["api_porta"] = Srv.get("porta")
                Est.MostrarToast(f"api :{Srv.get('porta')} ativa")
            else:
                Est.MostrarToast(f"api nao subiu: {Srv.get('motivo')}")
        try:
            return MainLoop(Est)
        finally:
            if Est.Cache.get("api_rodando"):
                Servidor.Parar()
            SalvarAuto.Rodar(Est, "saida")

    print("uso: python3 Console.py bypass|servidor|status [--modo local|servidor|federado]")
    return 2'''

    if Antigo not in Src:
        return {"ok": False, "motivo": "bloco_Main_nao_encontrado"}
    Src = Src.replace(Antigo, Novo)

    Antigo2 = '''    finally:
        Teclado.Fechar(T)
        Render.Limpar()
        print(f"{Cor.BOLD}BYPASS{Cor.RESET} v{Estado.VERSAO} — bye.")
    return 0'''

    Novo2 = '''    finally:
        Teclado.Fechar(T)
        AnimacaoSaida.Rodar(Est, 0.2)
        SalvarAuto.Rodar(Est, "sinal")
        Render.Limpar()
        print(f"{Cor.BOLD}BYPASS{Cor.RESET} v{Estado.VERSAO} — bye.")
    return 0'''

    if Antigo2 in Src:
        Src = Src.replace(Antigo2, Novo2)

    Antigo3 = '''            Cabecalho.Rodape(Est)
            Cabecalho.Toast(Est)'''

    Novo3 = '''            Cabecalho.Rodape(Est)
            Cabecalho.Toast(Est)
            RenderOperador.Desenhar(Est)
            if Est.Cache.get("api_rodando"):
                L_, A_ = Render.Dimensoes()
                Render.IrPara(A_, 1)
                Render.Escrever(f"{Cor.VERDE}api :{Est.Cache.get('api_porta')}{Cor.RESET}", SemQuebra=False)'''

    if Antigo3 in Src:
        Src = Src.replace(Antigo3, Novo3)

    open(Caminho, "w", encoding="utf-8").write(Src)
    return {"ok": True}

if __name__ == "__main__":
    raise SystemExit(Main())
