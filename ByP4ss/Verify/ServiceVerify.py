# ServiceVerify do ByP4ss
# Verifica se um servico esta REALMENTE respondendo (nao so a porta aberta).
# Chamado por Core.Engine.Verify: Mod.ServiceVerify.Verificar(Alvo, Porta) -> bool
#
# Porta aberta != servico funcionando. Pode ser firewall com PORT DROP
# virando ACCEPT, pode ser kernel com listen backlog cheio, pode ser
# honeypot que aceita e nao responde. Este modulo testa o protocolo.

import socket
import ssl

from Core.Config import Config
from Core.Log import Log


class ServiceVerify:

    BANNERS = {
        21: [b"220", b"FTP"],
        22: [b"SSH-2.0", b"SSH-1.99"],
        23: [b"login:", b"Login:", b"Password:", b"#" * 3],
        25: [b"220", b"SMTP"],
        80: [b"HTTP/1.", b"<html", b"<!DOCTYPE", b"<HTML"],
        110: [b"+OK", b"POP3"],
        143: [b"* OK", b"IMAP"],
        3306: [b"mysql_native_password", b"MariaDB"],
        5432: [b"PostgreSQL", b"FATAL"],
        6379: [b"-ERR", b"+PONG", b"+OK"],
        8080: [b"HTTP/1.", b"<html", b"<!DOCTYPE"],
        8443: [b"HTTP/1.", b"\x16\x03"],
    }

    @staticmethod
    def Verificar(Alvo, Porta, Timeout=None):
        if not Alvo or not Porta:
            return False
        try:
            PortaInt = int(Porta)
        except (TypeError, ValueError):
            return False
        Timeout = Timeout or 2.0
        if PortaInt == 443 or PortaInt == 8443:
            R = ServiceVerify._Tls(Alvo, PortaInt, Timeout)
        elif PortaInt in (80, 8080, 8000, 8888):
            R = ServiceVerify._Http(Alvo, PortaInt, Timeout)
        else:
            R = ServiceVerify._Banner(Alvo, PortaInt, Timeout)
        Log.Verificacao("ServiceVerify", Alvo, R, {"porta": PortaInt})
        return R

    @staticmethod
    def _Banner(Alvo, Porta, Timeout):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(Timeout)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return False
            Sock.settimeout(1.5)
            Banner = b""
            try:
                Banner = Sock.recv(1024)
            except socket.timeout:
                pass
            if not Banner:
                try:
                    Sock.sendall(b"\r\n\r\n")
                    Banner = Sock.recv(1024)
                except (socket.timeout, OSError):
                    pass
            if not Banner:
                return False
            Padroes = ServiceVerify.BANNERS.get(Porta, [])
            if not Padroes:
                return True
            return any(P in Banner for P in Padroes)
        except (socket.error, OSError):
            return False
        finally:
            try:
                Sock.close()
            except (socket.error, OSError):
                pass

    @staticmethod
    def _Http(Alvo, Porta, Timeout):
        import urllib.request
        import urllib.error
        Url = f"http://{Alvo}:{Porta}/"
        try:
            Req = urllib.request.Request(Url, headers={"User-Agent": "ByP4ss/1.0"})
            with urllib.request.urlopen(Req, timeout=Timeout) as F:
                return F.status in (200, 301, 302, 401, 403)
        except urllib.error.HTTPError as E:
            return E.code in (401, 403)
        except Exception:
            return False

    @staticmethod
    def _Tls(Alvo, Porta, Timeout):
        Ctx = ssl.create_default_context()
        Ctx.check_hostname = False
        Ctx.verify_mode = ssl.CERT_NONE
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(Timeout)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return False
            with Ctx.wrap_socket(Sock, server_hostname=Alvo) as SslSock:
                Versao = SslSock.version()
                return bool(Versao)
        except (ssl.SSLError, socket.error, OSError):
            return False
        finally:
            try:
                Sock.close()
            except (socket.error, OSError):
                pass

    @staticmethod
    def Info():
        return {
            "nome": "ServiceVerify",
            "metodos": ["banner", "http", "tls"],
            "portas_com_banner": sorted(ServiceVerify.BANNERS.keys()),
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "teste":
        Alvo = sys.argv[2]
        Porta = int(sys.argv[3]) if len(sys.argv) > 3 else 80
        print(f"verificando servico {Alvo}:{Porta}")
        R = ServiceVerify.Verificar(Alvo, Porta)
        print("ativo" if R else "inativo")
