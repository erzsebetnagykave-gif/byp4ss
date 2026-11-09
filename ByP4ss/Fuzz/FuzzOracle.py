# FuzzOracle do ByP4ss
# Compara resposta de payload com baseline local. Detecta anomalia.
# Chamado por FuzzEngine: Mod.Testar(Alvo, Iteracoes) -> dict
#
# Baseline local (nao Shodan/Censys). Primeira request vira referencia.

import time
import socket
import urllib.parse

from Core.Config import Config
from Core.Log import Log


class FuzzOracle:

    PATH = "/"
    PARAM = "q"
    PAYLOADS = [
        "'", "\"", "`", ";", "|", "&", "$", "(", ")", "{", "}",
        "<", ">", "?", "!", "*", "%", "\x00", "..", "../",
        "A" * 500, "A" * 2000,
    ]
    TIMEOUT = 2.0
    LIMIAR_DIFERENCA = 500

    @staticmethod
    def Testar(Alvo, Iteracoes):
        Resultado = {
            "ok": True, "tecnica": "oracle",
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
        Baseline = FuzzOracle._UmaRequest(Alvo, Porta, "baseline")
        if not Baseline.get("ok"):
            Resultado["ok"] = False
            Resultado["motivo"] = "baseline_falhou"
            Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
            return Resultado
        Resultado["baseline"] = {
            "status": Baseline.get("status", 0),
            "tamanho": Baseline.get("tamanho", 0),
        }
        Count = 0
        for Payload in FuzzOracle.PAYLOADS:
            if Count >= Resultado["iteracoes"]:
                break
            R = FuzzOracle._UmaRequest(Alvo, Porta, Payload)
            Count += 1
            FuzzOracle._Registrar(R, Baseline, Payload, Resultado)
        Resultado["iteracoes"] = Count
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        return Resultado

    @staticmethod
    def _UmaRequest(Alvo, Porta, Payload):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzOracle.TIMEOUT)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            ValorEnc = urllib.parse.quote(Payload, safe="")
            Req = (f"GET {FuzzOracle.PATH}?{FuzzOracle.PARAM}={ValorEnc} HTTP/1.0\r\n"
                   f"Host: {Alvo}\r\nConnection: close\r\n\r\n")
            Sock.sendall(Req.encode("utf-8", errors="replace"))
            Dados = Sock.recv(8192)
            return {
                "ok": True,
                "status": FuzzOracle._Status(Dados),
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
    def _Registrar(R, Baseline, Payload, Resultado):
        if not R.get("ok"):
            if R.get("motivo") == "timeout":
                Resultado["anomalias"].append({
                    "tipo": "oracle_timeout", "payload": Payload[:40],
                })
            return
        Diferenca = abs(R.get("tamanho", 0) - Baseline.get("tamanho", 0))
        StatusDiferente = R.get("status", 0) != Baseline.get("status", 0)
        if Diferenca > FuzzOracle.LIMIAR_DIFERENCA:
            Resultado["crashes"].append({
                "tipo": "oracle_diferenca",
                "payload": Payload[:40],
                "baseline_tamanho": Baseline.get("tamanho", 0),
                "teste_tamanho": R.get("tamanho", 0),
                "diferenca": Diferenca,
            })
        elif StatusDiferente:
            Resultado["anomalias"].append({
                "tipo": "oracle_status_diferente",
                "payload": Payload[:40],
                "baseline_status": Baseline.get("status", 0),
                "teste_status": R.get("status", 0),
            })

    @staticmethod
    def Info():
        return {"nome": "FuzzOracle", "payloads": len(FuzzOracle.PAYLOADS),
                "baseline": "local"}
