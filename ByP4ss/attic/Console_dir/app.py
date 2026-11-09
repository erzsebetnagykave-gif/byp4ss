import os
import select
import sys
import termios
import time
import tty

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assinc import Motor
from estado import Estado, SALAS
from render import Render
from clientes import Clientes
from salas import SALAS as SALAS_INST


FRAME = 50
QUIT_KEYS = {"\x03", "\x04", "\x11", "QUIT"}


class App:

    def __init__(self):
        self.estado = Estado()
        self.clientes = Clientes()
        self.rodando = True
        self.ultimo_render = 0
        self.original_termios = None
        self.chaves = None
        self.iniciado = False

    def Iniciar(self):
        self._AbrirTerminal()
        self._AbrirClientes()
        self._BootSessao()
        self._EntrarSala()
        self.iniciado = True

    def _AbrirTerminal(self):
        try:
            self.original_termios = termios.tcgetattr(sys.stdin.fileno())
            tty.setraw(sys.stdin.fileno())
        except Exception:
            self.original_termios = None
        sys.stdout.write("\033[?25l\033[2J\033[H")
        sys.stdout.flush()
        import threading
        self.chaves = []
        def LerChaves():
            buf = sys.stdin.buffer
            while True:
                try:
                    c = buf.read(1)
                except Exception:
                    break
                if not c:
                    break
                self.chaves.append(c)
        t = threading.Thread(target=LerChaves, daemon=True)
        t.start()

    def _FecharTerminal(self):
        sys.stdout.write("\033[?25h\033[0m\033[2J\033[H")
        sys.stdout.flush()
        if self.original_termios is not None:
            try:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.original_termios)
            except Exception:
                pass

    def _AbrirClientes(self):
        try:
            self.clientes.Abrir()
        except Exception:
            pass

    def _FecharClientes(self):
        try:
            self.clientes.Fechar()
        except Exception:
            pass

    def _BootSessao(self):
        try:
            r = self.clientes.SessaoListar()
            if isinstance(r, dict) and r.get("ok"):
                sessoes = r.get("sessoes") or []
                if sessoes:
                    self.estado.status = f"{len(sessoes)} sessoes anteriores (Ctrl+R retomar)"
        except Exception:
            pass

    def _SalaAtual(self):
        return SALAS_INST.get(self.estado.sala)

    def _EntrarSala(self):
        sala = self._SalaAtual()
        if not sala:
            return
        def Callback(nome, itens):
            self.estado.DefinirItens(nome, itens)
            Motor = self._Refresh
            self._Refresh()
        try:
            sala.Entrar(self.estado, self.clientes, Callback)
        except Exception as e:
            self.estado.status = f"erro ao entrar em {self.estado.sala}: {e}"

    def _Refresh(self):
        try:
            Render(self.estado.ToDict())
        except Exception as e:
            self.estado.status = f"erro render: {e}"

    def _LerChave(self, timeout=FRAME / 1000.0):
        if not self.chaves:
            time.sleep(timeout)
            return None
        # Agrupa bytes disponiveis (para setas)
        inicio = time.monotonic()
        while time.monotonic() - inicio < 0.02:
            if len(self.chaves) >= 3:
                break
            time.sleep(0.005)
        # Pega 1 tecla (ou sequencia de 3 se comeca com ESC)
        prim = self.chaves.pop(0)
        if prim == b"\x1b":
            seq = prim
            for _ in range(2):
                if not self.chaves:
                    time.sleep(0.01)
                    if not self.chaves:
                        break
                seq += self.chaves.pop(0)
            return seq.decode("utf-8", "replace")
        return prim.decode("utf-8", "replace")

    def _ProcessarChave(self, k):
        if k in QUIT_KEYS:
            self.rodando = False
            return
        if k == "\t" or k == "\x14":
            self.estado.ProximaSala()
            self._EntrarSala()
            return
        if k == "\x1b[Z":
            self.estado.SalaAnterior()
            self._EntrarSala()
            return
        if k == "\x1b[A":
            self.estado.Mover(-1)
            return
        if k == "\x1b[B":
            self.estado.Mover(1)
            return
        if k in ("\x1b[H",):
            self.estado.indice = 0
            return
        if k in ("\x1b[F",):
            itens = self.estado.ItensSala()
            self.estado.indice = max(0, len(itens) - 1)
            return
        if k in ("\r", "\n"):
            self._ProcessarEnter()
            return
        if k == "\x13":
            self._SalvarSessao()
            return
        if k == "\x12":
            self._CarregarSessao()
            return
        if k == "\x0f":
            self._ToggleOperador()
            return
        if k == "\x1b":
            self.estado.status = ""
            return
        # Tecla extra da sala
        sala = self._SalaAtual()
        if sala and len(k) == 1:
            try:
                if sala.TeclaExtra(self.estado, self.clientes, k, lambda n, i: (self.estado.DefinirItens(n, i), self._Refresh())):
                    return
            except Exception:
                pass

    def _ProcessarEnter(self):
        item = self.estado.ItemAtual()
        if not item:
            return
        sala = self._SalaAtual()
        if not sala:
            return
        try:
            sala.Enter(self.estado, self.clientes, item)
        except Exception as e:
            self.estado.status = f"erro: {e}"

    def _SalvarSessao(self):
        nome = self.estado.sessao or ("console_" + time.strftime("%Y%m%d_%H%M%S"))
        self.estado.sessao = nome
        estado = self.estado.Snapshot()
        try:
            r = self.clientes.SessaoSalvar(nome, estado)
            if isinstance(r, dict) and r.get("ok"):
                self.estado.status = f"sessao salva: {nome}"
            else:
                self.estado.status = f"erro ao salvar: {r.get('motivo', '?')}"
        except Exception as e:
            self.estado.status = f"erro ao salvar: {e}"

    def _CarregarSessao(self):
        try:
            r = self.clientes.SessaoListar()
            if not isinstance(r, dict) or not r.get("ok"):
                self.estado.status = "sem sessoes"
                return
            sessoes = r.get("sessoes") or []
            if not sessoes:
                self.estado.status = "sem sessoes"
                return
            nome = sessoes[0]["nome"]
            c = self.clientes.SessaoCarregar(nome)
            if not isinstance(c, dict) or not c.get("ok"):
                self.estado.status = f"erro ao carregar: {c.get('motivo', '?')}"
                return
            estado = c.get("estado") or {}
            if isinstance(estado, str):
                import json
                try:
                    estado = json.loads(estado)
                except Exception:
                    estado = {}
            if isinstance(estado, dict):
                if "alvo_atual" in estado and estado["alvo_atual"]:
                    self.estado.DefinirAlvo(estado["alvo_atual"])
                if "sala" in estado and estado["sala"] in SALAS:
                    self.estado.sala = estado["sala"]
                if "config" in estado and isinstance(estado["config"], dict):
                    self.estado.config.update(estado["config"])
            self.estado.sessao = nome
            self.estado.status = f"sessao retomada: {nome}"
            self._EntrarSala()
        except Exception as e:
            self.estado.status = f"erro ao retomar: {e}"

    def _ToggleOperador(self):
        atual = self.estado.config.get("operador", "false")
        novo = "false" if atual == "true" else "true"
        self.estado.config["operador"] = novo
        self.estado.status = f"operador = {novo}"

    def _ColherTarefas(self):
        try:
            concluidas = Motor.Colher()
            ativas = Motor.Ativas()
            self.estado.tarefas_ativas = len(ativas)
            for t in concluidas:
                if t.erro:
                    self.estado.status = f"{t.nome}: {t.erro[:60]}"
        except Exception:
            pass

    def Rodar(self):
        if not self.iniciado:
            self.Iniciar()
        try:
            while self.rodando:
                self._ColherTarefas()
                self._Refresh()
                k = self._LerChave()
                if k is None:
                    continue
                self._ProcessarChave(k)
        finally:
            self._FecharClientes()
            self._FecharTerminal()
        return 0


def RodarHeadless(max_iter=10):
    print("=== APP HEADLESS ===\n")
    app = App()
    app.estado.DefinirItens("recon", [
        {"texto": "192.168.0.1", "detalhe": "roteador"},
        {"texto": "192.168.0.2", "detalhe": "dlink"},
    ])
    for i in range(max_iter):
        app._ColherTarefas()
        print(f"[{i}] sala={app.estado.sala} itens={len(app.estado.ItensSala())} ativas={app.estado.tarefas_ativas}")
        app.estado.Mover(1)
        time.sleep(0.05)
    print("\nHEADLESS OK")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "teste":
        RodarHeadless()
    elif args and args[0] == "headless":
        RodarHeadless(20)
    else:
        try:
            sys.exit(App().Rodar())
        except KeyboardInterrupt:
            sys.exit(0)
