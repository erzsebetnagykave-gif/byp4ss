# FuzzNullspace do ByP4ss
# Testa inputs vazios, nulos, unicode malformado, bytes altos.
# Chamado por FuzzEngine: Mod.Testar(Alvo, Iteracoes) -> dict
#
# Detecta 5xx, timeout, ou resposta vazia em input edge.

import time
import socket

from Core.Config import Config
from Core.Log import Log


class FuzzNullspace:

    PATHS = ["/", "/index.php", "/api", "/admin"]
    PARAMS = ["id", "page", "name", "q"]

    PAYLOADS = [
        "",
        "%00",
        "%2500",
        "%00%00%00%00",
        "%C0%AF",
        "%E0%80%AF",
        "%F0%80%80%AF",
        "%FF",
        "%FE%FF",
        "%EF%BB%BF",
        "-1",
        "0",
        "9999999999999999",
        "999999999999999999999999999999",
        "NaN",
        "Infinity",
        "null",
        "undefined",
        "true",
        "false",
        "[]",
        "{}",
        "%20" * 100,
        "A" * 8192,
        "A" * 65536,
        "%41" * 2048,
    ]
    TIMEOUT = 2.0

    @staticmethod
    def Testar(Alvo, Iteracoes):
        Resultado = {
            "ok": True, "tecnica": "nullspace",
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
        for Path in FuzzNullspace.PATHS:
            for Payload in FuzzNullspace.PAYLOADS:
                if Count >= Resultado["iteracoes"]:
                    break
                Param = FuzzNullspace.PARAMS[Count % len(FuzzNullspace.PARAMS)]
                R = FuzzNullspace._TestarPayload(Alvo, Porta, Path, Param, Payload)
                Count += 1
                FuzzNullspace._Registrar(R, Payload, Path, Param, Resultado)
            if Count >= Resultado["iteracoes"]:
                break
        Resultado["iteracoes"] = Count
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        return Resultado

    @staticmethod
    def _TestarPayload(Alvo, Porta, Path, Param, Payload):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzNullspace.TIMEOUT)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            Sep = "&" if "?" in Path else "?"
            AlvoUrl = f"{Path}{Sep}{Param}={Payload}"
            Req = (f"GET {AlvoUrl} HTTP/1.0\r\n"
                   f"Host: {Alvo}\r\nConnection: close\r\n\r\n")
            Sock.sendall(Req.encode("latin-1", errors="replace"))
            Dados = Sock.recv(8192)
            return {
                "ok": True,
                "status": FuzzNullspace._Status(Dados),
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
    def _Registrar(R, Payload, Path, Param, Resultado):
        if not R.get("ok"):
            if R.get("motivo") == "timeout":
                Resultado["anomalias"].append({
                    "tipo": "nullspace_timeout", "path": Path, "param": Param,
                    "payload_len": len(Payload), "payload_preview": Payload[:30],
                })
            return
        Status = R.get("status", 0)
        Tamanho = R.get("tamanho", 0)
        if Status >= 500:
            Resultado["crashes"].append({
                "tipo": "nullspace_5xx", "path": Path, "param": Param,
                "payload_len": len(Payload), "payload_preview": Payload[:30],
                "status": Status,
            })
        elif Status == 0 and Tamanho == 0:
            Resultado["anomalias"].append({
                "tipo": "nullspace_resposta_vazia", "path": Path, "param": Param,
                "payload_len": len(Payload),
            })
        elif Tamanho > 10000 and len(Payload) > 1000:
            Resultado["anomalias"].append({
                "tipo": "nullspace_reflexao_grande", "path": Path, "param": Param,
                "tamanho": Tamanho,
            })

    @staticmethod
    def Info():
        return {"nome": "FuzzNullspace", "payloads": len(FuzzNullspace.PAYLOADS),
                "paths": len(FuzzNullspace.PATHS)}
