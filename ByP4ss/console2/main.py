import os
import sys
import time
import signal
import threading
import select
import termios
import tty
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from caixa import Caixa
from paleta import Paleta
from motor import Motor

VERSAO = "1.0"
TITULO = "CBNC/ByP4ss v1.0"
FRAME_MS = 50
FPS_RENDER = 20.0

ESC_ALT_ON = "\033[?1049h"
ESC_ALT_OFF = "\033[?1049l"
ESC_CUR_ON = "\033[?25h"
ESC_CUR_OFF = "\033[?25l"
ESC_CLEAR = "\033[2J\033[H"
ESC_RESET = "\033[0m"
ESC_HOME = "\033[H"

TECLAS_SAIR = {"\x11", "\x03", "\x04"}


class SessaoUI:

    def __init__(self):
        self.rodando = True
        self.ultima_render = 0.0
        self.toast_texto = ""
        self.toast_ate = 0.0
        self.rodape_temp_texto = ""
        self.rodape_temp_ate = 0.0
        self.largura = 60
        self.altura = 20

    def MostrarToast(self, texto, duracao=2.5):
        self.toast_texto = texto
        self.toast_ate = time.monotonic() + duracao

    def ToastAtivo(self):
        if not self.toast_texto:
            return None
        if time.monotonic() > self.toast_ate:
            self.toast_texto = ""
            return None
        return self.toast_texto

    def MostrarRodapeTemp(self, texto, duracao=3.0):
        self.rodape_temp_texto = texto
        self.rodape_temp_ate = time.monotonic() + duracao

    def RodapeTempAtivo(self):
        if not self.rodape_temp_texto:
            return None
        if time.monotonic() > self.rodape_temp_ate:
            self.rodape_temp_texto = ""
            return None
        return self.rodape_temp_texto

    def DeveRenderizar(self):
        agora = time.monotonic()
        intervalo = 1.0 / FPS_RENDER
        if agora - self.ultima_render >= intervalo:
            self.ultima_render = agora
            return True
        return False


class Teclado:

    SEQUENCIAS_ANSI = {
        b"\x1b[A": "cima",
        b"\x1b[B": "baixo",
        b"\x1b[C": "direita",
        b"\x1b[D": "esquerda",
        b"\x1b[H": "home",
        b"\x1b[F": "end",
        b"\x1b[1~": "home",
        b"\x1b[4~": "end",
        b"\x1b[5~": "pgup",
        b"\x1b[6~": "pgdn",
        b"\x1b[3~": "delete",
        b"\x1bOP": "F1",
        b"\x1bOQ": "F2",
        b"\x1bOR": "F3",
        b"\x1bOS": "F4",
        b"\x1b[15~": "F5",
        b"\x1b[17~": "F6",
        b"\x1b[18~": "F7",
        b"\x1b[19~": "F8",
        b"\x1b[20~": "F9",
        b"\x1b[21~": "F10",
        b"\x1b[23~": "F11",
        b"\x1b[24~": "F12",
        b"\x1b[Z": "shift_tab",
    }

    @staticmethod
    def Decodificar(Bytes):
        if not Bytes:
            return None
        if len(Bytes) == 1:
            b = Bytes[0]
            if b == 0x0d or b == 0x0a:
                return "\r"
            if b == 0x7f or b == 0x08:
                return "\x7f"
            if b == 0x09:
                return "\t"
            if b == 0x1b:
                return "\x1b"
            if 0x20 <= b < 0x7f:
                return chr(b)
            return bytes([b]).decode("latin-1")
        if Bytes in Teclado.SEQUENCIAS_ANSI:
            return Teclado.SEQUENCIAS_ANSI[Bytes]
        return None


class TecladoTermios:

    def __init__(self, fd=0):
        self.fd = fd
        self.original = None
        self.buffer = b""
        self.rodando = False

    def Abrir(self):
        try:
            self.original = termios.tcgetattr(self.fd)
            tty.setraw(self.fd)
            self.rodando = True
            return True
        except Exception:
            self.original = None
            return False

    def Fechar(self):
        self.rodando = False
        if self.original is not None:
            try:
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self.original)
            except Exception:
                pass
            self.original = None

    def Ler(self, timeout_ms=50):
        if not self.rodando:
            return None
        try:
            prontos, _, _ = select.select([self.fd], [], [], timeout_ms / 1000.0)
        except Exception:
            return None
        if not prontos:
            return None
        try:
            dados = os.read(self.fd, 32)
        except Exception:
            return None
        if not dados:
            return None
        return self._DecodificarBytes(dados)

    def _DecodificarBytes(self, dados):
        if len(dados) == 1:
            return Teclado.Decodificar(dados)
        if dados[0] == 0x1b:
            if dados in Teclado.SEQUENCIAS_ANSI:
                return Teclado.SEQUENCIAS_ANSI[dados]
            for tamanho in (3, 4, 5, 6):
                if len(dados) >= tamanho:
                    prefixo = dados[:tamanho]
                    if prefixo in Teclado.SEQUENCIAS_ANSI:
                        self.buffer = dados[tamanho:]
                        return Teclado.SEQUENCIAS_ANSI[prefixo]
            return None
        return Teclado.Decodificar(dados[:1])


class Renderizador:

    def __init__(self, caixa, paleta, motor, sessao_ui):
        self.caixa = caixa
        self.paleta = paleta
        self.motor = motor
        self.sessao = sessao_ui
        self.ultimo_info = ""
        self.ultimo_rodape = ""

    def DesenharTudo(self):
        try:
            self.paleta.Render()
        except Exception:
            pass
        self._DesenharInfo()
        self._DesenharRodape()
        self._DesenharToast()
        try:
            self.caixa.DesenharCompleto()
        except Exception:
            pass

    def _DesenharInfo(self):
        info = self.motor.EstadoFormatado()
        if info != self.ultimo_info:
            try:
                e = self.motor.Estado()
                self.caixa.DefinirEstado({
                    "alvo": e.get("alvo", ""),
                    "sessao": e.get("sessao", ""),
                    "modo": e.get("modo", "local"),
                    "hosts": e.get("hosts", 0),
                    "creds": e.get("creds", 0),
                    "shells": e.get("shells", 0),
                    "ativas": e.get("tarefas_ativas", 0),
                    "ultima": info,
                })
                self.ultimo_info = info
            except Exception:
                pass

    def _DesenharRodape(self):
        temp = self.sessao.RodapeTempAtivo()
        if temp:
            rodape = temp
        else:
            rodape = "Ctrl+Q sai | Tab tipo | Enter exec | Esc limpa | F1-F5 atalhos"
        if rodape != self.ultimo_rodape:
            try:
                self.caixa.DefinirStatus(rodape)
                self.ultimo_rodape = rodape
            except Exception:
                pass

    def _DesenharToast(self):
        toast = self.sessao.ToastAtivo()
        if toast:
            try:
                self.caixa.MostrarToast(toast, 1.0)
            except Exception:
                pass

class Console:

    def __init__(self):
        self.caixa = None
        self.paleta = None
        self.motor = None
        self.teclado = None
        self.renderizador = None
        self.sessao = SessaoUI()
        self.ultima_tecla = ""
        self.render_manual = False

    def Iniciar(self):
        sys.stdout.write(ESC_ALT_ON + ESC_CLEAR + ESC_CUR_OFF)
        sys.stdout.flush()
        try:
            self.caixa = Caixa(60, 20, TITULO)
            if not self.caixa.Abrir():
                return False
            self.paleta = Paleta(
                self.caixa,
                on_enter=self._AoEnter,
                on_mudar_tipo=self._AoMudarTipo,
            )
            self.motor = Motor(on_evento=self._AoEventoMotor)
            self.renderizador = Renderizador(
                self.caixa, self.paleta, self.motor, self.sessao
            )
            self.teclado = TecladoTermios()
            if not self.teclado.Abrir():
                return False
            signal.signal(signal.SIGWINCH, self._AoResize)
            signal.signal(signal.SIGINT, self._AoSinal)
            signal.signal(signal.SIGTERM, self._AoSinal)
            self.paleta.Render()
            self.renderizador.DesenharTudo()
            return True
        except Exception as e:
            self._LogErro(f"iniciar_falhou:{type(e).__name__}:{e}")
            return False

    def Rodar(self):
        try:
            while self.sessao.rodando:
                tecla = self.teclado.Ler(FRAME_MS)
                if tecla:
                    self.ultima_tecla = tecla
                    self._ProcessarTecla(tecla)
                self._Tick()
                if self.sessao.DeveRenderizar():
                    self.renderizador.DesenharTudo()
        finally:
            self.Fechar()

    def Fechar(self):
        self.sessao.rodando = False
        try:
            if self.motor:
                self.motor.CancelarTudo()
        except Exception:
            pass
        try:
            if self.caixa:
                self.caixa.Fechar()
        except Exception:
            pass
        try:
            if self.teclado:
                self.teclado.Fechar()
        except Exception:
            pass
        sys.stdout.write(ESC_CUR_ON + ESC_RESET + ESC_ALT_OFF + ESC_HOME)
        sys.stdout.flush()

    def _ProcessarTecla(self, tecla):
        if tecla in TECLAS_SAIR:
            self.sessao.rodando = False
            return
        if tecla == "F5":
            self.sessao.MostrarToast("F5: atualizando", 1.5)
            self.paleta.CarregarTipo(self.paleta.tipo)
            return
        if tecla in ("F1", "F2", "F3", "F4"):
            if self.paleta.TeclaAtalho(tecla):
                return
        if tecla == "shift_tab":
            self.paleta.TipoAnterior()
            self.sessao.MostrarToast(f"paleta: {self.paleta.tipo}", 1.0)
            return
        try:
            consumiu = self.paleta.Tecla(tecla)
        except Exception as e:
            self._LogErro(f"paleta_tecla:{type(e).__name__}")
            consumiu = False
        if consumiu:
            return
        if tecla in ("cima", "baixo", "home", "end", "pgup", "pgdn"):
            return

    def _Tick(self):
        try:
            self.paleta.Tick()
        except Exception:
            pass
        if self.sessao.ToastAtivo():
            self.sessao.MostrarToast(self.sessao.ToastAtivo(), 0.0)

    def _AoEnter(self, item, query):
        try:
            r = self.motor.Executar(item, query)
        except Exception as e:
            self.sessao.MostrarToast(f"erro motor: {type(e).__name__}", 2.0)
            return
        if not r.get("ok"):
            self.sessao.MostrarToast(r.get("msg") or r.get("motivo") or "erro", 2.5)
            return
        try:
            self.paleta.RegistrarHistorico(item.get("id", "?"), "")
        except Exception:
            pass
        self.sessao.MostrarToast(f"executando {item.get('id')}...", 1.5)

    def _AoMudarTipo(self, tipo):
        try:
            # titulo e do Cabecalho, nao do caixa
            pass
        except Exception:
            pass
        self.sessao.MostrarRodapeTemp(f"paleta: {tipo}", 1.5)

    def _AoEventoMotor(self, evento):
        if evento.tipo == "tarefa_finalizada":
            d = evento.dados or {}
            cmd = d.get("comando", "?")
            if d.get("ok"):
                self.sessao.MostrarToast(f"{cmd}: ok ({d.get('duracao')}s)", 2.0)
            else:
                self.sessao.MostrarToast(f"{cmd}: falha ({d.get('erro') or '?'})", 2.5)
        elif evento.tipo == "tarefa_iniciada":
            d = evento.dados or {}
            self.sessao.MostrarRodapeTemp(f"▶ {d.get('comando', '?')}", 2.0)

    def _AoResize(self, *args):
        self.render_manual = True
        try:
            self.caixa.Resize()
        except Exception:
            pass

    def _AoSinal(self, signum, frame):
        self.sessao.rodando = False

    def _LogErro(self, msg):
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base, "main_erros.log")
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {msg}\n")
        except Exception:
            pass


class _CaixaMock:

    def __init__(self, largura=60, altura=20):
        self.largura = largura
        self.altura = altura
        self.linhas = {}
        self.titulo = ""
        self.info = ""
        self.rodape = ""
        self.estado = {}
        self.toast = ""
        self.help_ativo = False
        self.chamadas = 0

    def Abrir(self):
        return True

    def Fechar(self):
        pass

    # --- API antiga (mantida por compatibilidade com testes existentes) ---
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

    def Redesenhar(self):
        self.chamadas += 1

    # --- API nova (caixa.py pos-patch) ---
    def Desenhar(self):
        self.chamadas += 1

    def DesenharCompleto(self):
        self.chamadas += 1

    def DesenharHelp(self):
        self.help_ativo = True

    def MostrarHelp(self):
        self.help_ativo = True

    def FecharHelp(self):
        self.help_ativo = False

    def MostrarToast(self, msg, duracao=2.0):
        self.toast = msg

    def _ToastAtivo(self):
        return self.toast or None

    def DefinirEstado(self, dados):
        self.estado.update(dados or {})

    def DefinirStatus(self, msg):
        self.rodape = msg

    def DefinirQuery(self, q):
        pass

    def DefinirItens(self, itens):
        self.linhas["itens"] = itens

    def DefinirPaleta(self, p):
        pass

    def Resize(self):
        return False

    def Mover(self, delta):
        pass

    def Tick(self):
        pass

    def Dimensoes(self):
        return (self.largura, self.altura)


def TesteHeadless():
    print("=== TESTE HEADLESS MAIN ===\n")

    print("[1] SessaoUI basica")
    s = SessaoUI()
    assert s.rodando
    s.MostrarToast("teste", 0.1)
    assert s.ToastAtivo() == "teste"
    time.sleep(0.15)
    assert s.ToastAtivo() is None
    print("    ok")

    print("\n[2] Teclado decodifica sequencias ANSI")
    assert Teclado.Decodificar(b"\x1b[A") == "cima"
    assert Teclado.Decodificar(b"\x1b[B") == "baixo"
    assert Teclado.Decodificar(b"\x1bOP") == "F1"
    assert Teclado.Decodificar(b"\r") == "\r"
    assert Teclado.Decodificar(b"a") == "a"
    assert Teclado.Decodificar(b"\t") == "\t"
    print("    ok")

    print("\n[3] Console com mocks (sem tty)")
    import motor as M
    orig_popen = M.subprocess.Popen

    class FakeProc:
        def __init__(self, cmd, **kw):
            self.returncode = 0
        def communicate(self, input=None, timeout=None):
            try:
                req = json.loads(input.strip())
                cmd = req.get("cmd", "")
                if "scan" in cmd:
                    return (json.dumps({"ok": True, "resultado": {"total": 5, "alvo": "192.168.0.1"}}), "")
                if "cred" in cmd:
                    return (json.dumps({"ok": True, "resultado": {"total": 10}}), "")
                if "exploit" in cmd:
                    return (json.dumps({"ok": True, "resultado": {"total": 1, "sessao": "s_001"}}), "")
                return (json.dumps({"ok": False, "motivo": "cmd_desconhecido"}), "")
            except Exception as e:
                return (json.dumps({"ok": False, "motivo": "input_invalido", "erro": str(e)}), "")
        def terminate(self):
            self.returncode = -15
        def kill(self):
            self.returncode = -9
        def poll(self):
            return self.returncode

    M.subprocess.Popen = FakeProc
    try:
        caixa = _CaixaMock()
        paleta = Paleta(caixa, on_enter=None, on_mudar_tipo=None)
        motor = M.Motor(on_evento=None)
        ui = SessaoUI()
        rend = Renderizador(caixa, paleta, motor, ui)

        print("[4] Paleta carrega comando")
        assert paleta.tipo == "comando"
        assert len(paleta.itens_filtrados) == 15
        print(f"    tipo={paleta.tipo} itens={len(paleta.itens_filtrados)}")

        print("\n[5] Renderizador desenha tudo")
        rend.DesenharTudo()
        assert 3 in caixa.linhas, "abas nao renderizadas"
        assert caixa.chamadas > 0, "caixa.Redesenhar nao chamada"
        print(f"    caixa.Redesenhar chamada {caixa.chamadas}x")

        print("\n[6] Paleta navega e Enter executa")
        paleta.query = "scan"
        paleta._Filtrar()
        paleta.selecionado = 0
        item = paleta.Atual()
        assert item is not None
        motor.Executar(item, "scan alvo=192.168.0.1")
        time.sleep(0.4)
        estado = motor.Estado()
        assert estado["hosts"] == 5
        print(f"    hosts={estado['hosts']} alvo={estado['alvo']}")

        print("\n[7] SessaoUI toast expira")
        ui.MostrarToast("teste", 0.1)
        time.sleep(0.15)
        assert ui.ToastAtivo() is None
        print("    ok")

        print("\n[8] Tecla de sair")
        assert "\x11" in TECLAS_SAIR
        assert "\x03" in TECLAS_SAIR
        print("    Ctrl+Q e Ctrl+C saem")

        print("\nHEADLESS OK")
    finally:
        M.subprocess.Popen = orig_popen


def MostrarAjuda():
    print(f"{TITULO}")
    print()
    print("uso: python3 main.py [comando]")
    print()
    print("comandos:")
    print("  (sem argumento)  abre o console TUI")
    print("  teste            testa headless (sem tela)")
    print("  ajuda            mostra esta ajuda")
    print("  versao           mostra versao")
    print()
    print("atalhos no console:")
    print("  Ctrl+Q / Ctrl+C  sai")
    print("  Tab / Ctrl+T     cicla tipo de paleta")
    print("  Shift+Tab        paleta anterior")
    print("  Up/Down          navega")
    print("  Enter            executa")
    print("  Esc              limpa query")
    print("  F1-F4            atalhos da central rapida")
    print("  F5               recarrega paleta")


def Main():
    args = sys.argv[1:]
    if not args:
        console = Console()
        if not console.Iniciar():
            sys.stderr.write("falha ao iniciar console\n")
            return 1
        try:
            console.Rodar()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            sys.stderr.write(f"erro fatal: {type(e).__name__}: {e}\n")
            console.Fechar()
            return 1
        return 0
    cmd = args[0]
    if cmd == "teste":
        TesteHeadless()
        return 0
    if cmd in ("ajuda", "-h", "--help"):
        MostrarAjuda()
        return 0
    if cmd in ("versao", "-v", "--version"):
        print(TITULO)
        return 0
    MostrarAjuda()
    return 2


if __name__ == "__main__":
    import json
    sys.exit(Main())
