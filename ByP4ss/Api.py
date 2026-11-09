import sys
import os
import json
import time
import socket
import argparse
import threading
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from RegistroComandos import RegistroComandos
except ImportError:
    RegistroComandos = None

try:
    from Cadeia import Cadeia
except ImportError:
    Cadeia = None

try:
    from Sessao import Sessao
except ImportError:
    Sessao = None

try:
    from Analise import Analise
except ImportError:
    Analise = None

try:
    from Core.Engine import Engine
except ImportError:
    Engine = None


class Api:

    VERSAO = "0.1"
    TOKEN_PATH = os.path.join(os.path.expanduser("~"), ".console", "token")
    INICIO = time.time()
    Servidor = None
    Porta = None
    Escuta = None
    Token = None
    ThreadRef = None

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def UptimeSegundos():
        return round(time.time() - Api.INICIO, 2)

    @staticmethod
    def GarantirToken(TokenForcado=None):
        if TokenForcado:
            Api.Token = TokenForcado
            return {"ok": True, "token": TokenForcado, "origem": "cli"}
        if os.path.isfile(Api.TOKEN_PATH):
            try:
                with open(Api.TOKEN_PATH, "r", encoding="utf-8") as F:
                    T = F.read().strip()
                if T:
                    Api.Token = T
                    return {"ok": True, "token": T, "origem": "arquivo"}
            except Exception:
                pass
        try:
            T = os.urandom(24).hex()
            os.makedirs(os.path.dirname(Api.TOKEN_PATH), mode=0o700, exist_ok=True)
            with open(Api.TOKEN_PATH, "w", encoding="utf-8") as F:
                F.write(T)
            try:
                os.chmod(Api.TOKEN_PATH, 0o600)
            except Exception:
                pass
            Api.Token = T
            return {"ok": True, "token": T, "origem": "gerado", "caminho": Api.TOKEN_PATH}
        except Exception as E:
            return {"ok": False, "motivo": f"token_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def ListarSalas():
        return {"ok": True, "salas": [
            {"nome": "rede", "tipo": "analise", "comandos": ["scan", "ssdp", "analise"]},
            {"nome": "exploits", "tipo": "exploits", "comandos": [
                "exploit tplink", "exploit dlink", "exploit tenda7795",
                "exploit arcadyan", "exploit iptime", "exploit tenda29384"]},
            {"nome": "comandos", "tipo": "ferramenta", "comandos":
                sorted(RegistroComandos.COMANDOS.keys()) if RegistroComandos else []},
            {"nome": "cadeias", "tipo": "kill_chain", "comandos": []},
            {"nome": "estado", "tipo": "sessao", "comandos": []},
        ], "total": 5}

    @staticmethod
    def EstadoSala(Nome):
        if Nome == "rede":
            return {"ok": True, "sala": "rede", "estado": {
                "tem_analise": Analise is not None,
                "tem_portscan": Analise is not None,
            }}
        if Nome == "exploits":
            return {"ok": True, "sala": "exploits", "estado": {
                "exploits_disponiveis": ["tplink", "dlink", "tenda7795",
                                          "arcadyan", "iptime", "tenda29384"],
                "total": 6,
            }}
        if Nome == "comandos":
            R = RegistroComandos.Listar() if RegistroComandos else {"comandos": [], "total": 0}
            return {"ok": True, "sala": "comandos", "estado": {"comandos": R["comandos"],
                                                                "total": R["total"]}}
        if Nome == "cadeias":
            R = Cadeia.Templates() if Cadeia else {"templates": []}
            return {"ok": True, "sala": "cadeias", "estado": {"templates": R["templates"],
                                                               "total": len(R["templates"])}}
        if Nome == "estado":
            S = Sessao.Listar() if Sessao else {"sessoes": [], "total": 0}
            R = Engine.ReportIntegrado() if Engine else {"ok": False}
            return {"ok": True, "sala": "estado", "estado": {
                "sessoes": S.get("sessoes", []), "total_sessoes": S.get("total", 0),
                "ultimos_eventos": len(R.get("ultimos", [])) if R.get("ok") else 0,
            }}
        return {"ok": False, "motivo": f"sala_nao_encontrada:{Nome}"}

    @staticmethod
    def ExecutarAcao(Sala, Cmd, Args):
        if RegistroComandos is None:
            return {"ok": False, "motivo": "RegistroComandos_indisponivel"}
        if Sala:
            Salas = {S["nome"]: S for S in Api.ListarSalas()["salas"]}
            if Sala not in Salas:
                return {"ok": False, "motivo": f"sala_nao_encontrada:{Sala}"}
            if Sala in ("rede", "exploits", "comandos"):
                Permitidos = Salas[Sala]["comandos"]
                if Permitidos and Cmd not in Permitidos:
                    return {"ok": False, "motivo": f"comando_nao_permitido_na_sala:{Cmd}"}
        R = RegistroComandos.Executar(Cmd, Args or {})
        return R

    @staticmethod
    def Rotas():
        return [
            ("GET",  "/",                       "info da API"),
            ("GET",  "/api/info",               "versao, hostname, uptime"),
            ("GET",  "/api/health",             "saude"),
            ("GET",  "/api/salas",              "lista de salas"),
            ("GET",  "/api/salas/{nome}",       "estado de uma sala"),
            ("POST", "/api/salas/{nome}/acao",  "executa comando na sala"),
            ("GET",  "/api/comandos",           "lista os 18 comandos"),
            ("POST", "/api/comandos/{nome}",    "executa comando"),
        ]

    @staticmethod
    def _Handler():
        class Handler(BaseHTTPRequestHandler):

            def log_message(self, Formato, *Args):
                return

            def _Auth(self):
                Cabecalho = self.headers.get("Authorization", "")
                Esperado = f"Bearer {Api.Token}" if Api.Token else None
                if not Esperado or Cabecalho != Esperado:
                    return False
                return True

            def _Responder(self, Status, Corpo):
                try:
                    Bytes = json.dumps(Corpo, ensure_ascii=False).encode("utf-8")
                    self.send_response(Status)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Content-Length", str(len(Bytes)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(Bytes)
                except Exception:
                    pass

            def _LerCorpo(self):
                Tamanho = int(self.headers.get("Content-Length", 0) or 0)
                if Tamanho <= 0:
                    return {}
                try:
                    Dados = self.rfile.read(Tamanho).decode("utf-8", "replace")
                    return json.loads(Dados) if Dados else {}
                except Exception:
                    return {}

            def do_GET(self):
                Caminho = urllib.parse.urlparse(self.path).path.rstrip("/") or "/"
                if Caminho == "/":
                    self._Responder(200, {"api": "ByP4ss", "versao": Api.VERSAO,
                                          "rotas": [{"metodo": M, "rota": R, "desc": D}
                                                    for M, R, D in Api.Rotas()]})
                    return
                if not self._Auth():
                    self._Responder(401, {"ok": False, "motivo": "token_invalido"})
                    return
                if Caminho == "/api/info":
                    self._Responder(200, {"ok": True, "api": "ByP4ss", "versao": Api.VERSAO,
                                          "hostname": socket.gethostname(),
                                          "porta": Api.Porta, "uptime_s": Api.UptimeSegundos()})
                    return
                if Caminho == "/api/health":
                    self._Responder(200, {"ok": True, "uptime_s": Api.UptimeSegundos()})
                    return
                if Caminho == "/api/salas":
                    self._Responder(200, Api.ListarSalas())
                    return
                if Caminho.startswith("/api/salas/"):
                    Nome = Caminho.split("/api/salas/", 1)[1]
                    if "/" in Nome:
                        self._Responder(400, {"ok": False, "motivo": "rota_invalida"})
                        return
                    self._Responder(200, Api.EstadoSala(Nome))
                    return
                if Caminho == "/api/comandos":
                    R = RegistroComandos.Listar() if RegistroComandos else {"comandos": [], "total": 0}
                    self._Responder(200, R)
                    return
                self._Responder(404, {"ok": False, "motivo": "rota_nao_encontrada", "caminho": Caminho})

            def do_POST(self):
                if not self._Auth():
                    self._Responder(401, {"ok": False, "motivo": "token_invalido"})
                    return
                Caminho = urllib.parse.urlparse(self.path).path.rstrip("/")
                Corpo = self._LerCorpo()
                if Caminho.startswith("/api/salas/") and Caminho.endswith("/acao"):
                    Nome = Caminho[len("/api/salas/"):-len("/acao")]
                    if not Nome or "/" in Nome:
                        self._Responder(400, {"ok": False, "motivo": "rota_invalida"})
                        return
                    Cmd = Corpo.get("cmd", "")
                    Args = Corpo.get("args", {})
                    if not Cmd:
                        self._Responder(400, {"ok": False, "motivo": "cmd_ausente"})
                        return
                    R = Api.ExecutarAcao(Nome, Cmd, Args)
                    self._Responder(200 if R.get("ok") else 400, R)
                    return
                if Caminho.startswith("/api/comandos/"):
                    Nome = Caminho[len("/api/comandos/"):]
                    if not Nome or "/" in Nome:
                        self._Responder(400, {"ok": False, "motivo": "rota_invalida"})
                        return
                    Args = Corpo.get("args", {})
                    R = Api.ExecutarAcao(None, Nome, Args)
                    self._Responder(200 if R.get("ok") else 400, R)
                    return
                self._Responder(404, {"ok": False, "motivo": "rota_nao_encontrada", "caminho": Caminho})

        return Handler

    @staticmethod
    def Iniciar(Escuta="0.0.0.0", Porta=8765, Token=None, TokenForcado=False):
        if Api.Servidor is not None:
            return {"ok": True, "porta": Api.Porta, "ja_rodando": True}
        T = Api.GarantirToken(Token if not TokenForcado else Token)
        if not T.get("ok"):
            return {"ok": False, "motivo": "token_falhou", "detalhe": T}
        try:
            Handler = Api._Handler()
            Api.Servidor = ThreadingHTTPServer((Escuta, int(Porta)), Handler)
            Api.Servidor.daemon_threads = True
            Api.Porta = int(Porta)
            Api.Escuta = Escuta
        except Exception as E:
            Api.Servidor = None
            return {"ok": False, "motivo": f"bind_falhou:{type(E).__name__}", "erro": str(E)}
        T = None

        def Rodar():
            try:
                Api.Servidor.serve_forever()
            except Exception:
                pass

        Api.ThreadRef = threading.Thread(target=Rodar, daemon=True)
        Api.ThreadRef.start()
        return {"ok": True, "porta": Api.Porta, "escuta": Api.Escuta,
                "token": Api.Token, "token_caminho": Api.TOKEN_PATH,
                "token_origem": T or "desconhecido"}

    @staticmethod
    def Parar():
        if Api.Servidor is None:
            return {"ok": True, "motivo": "nao_estava_rodando"}
        try:
            Api.Servidor.shutdown()
            Api.Servidor.server_close()
        except Exception:
            pass
        Api.Servidor = None
        Api.ThreadRef = None
        return {"ok": True, "parado": True}

    @staticmethod
    def Main():
        P = argparse.ArgumentParser(prog="Api")
        P.add_argument("--escutar", default="127.0.0.1")
        P.add_argument("--porta", type=int, default=8765)
        P.add_argument("--token", default=None)
        P.add_argument("--rodar", action="store_true", help="mantem rodando ate Ctrl+C")
        Args = P.parse_args()

        R = Api.Iniciar(Args.escutar, Args.porta, Args.token)
        print(json.dumps(R, indent=2, ensure_ascii=False))
        if not R.get("ok"):
            return 1
        if not Args.rodar:
            Api.Parar()
            return 0
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            Api.Parar()
            return 0


if __name__ == "__main__":
    raise SystemExit(Api.Main())
