# FuzzResonance do ByP4ss
# Mede latencia + tamanho de 10 requests identicas. Detecta instabilidade.
# Chamado por FuzzEngine: Mod.Testar(Alvo, Iteracoes) -> dict

import time
import socket
import statistics

from Core.Config import Config
from Core.Log import Log


class FuzzResonance:

    AMOSTRAS = 10
    TIMEOUT = 2.0
    LIMIAR_CV = 0.5
    LIMIAR_LATENCIA = 1.0

    @staticmethod
    def Testar(Alvo, Iteracoes):
        Resultado = {
            "ok": True, "tecnica": "resonance",
            "iteracoes": int(Iteracoes or 100),
            "crashes": [], "anomalias": [],
            "duracao_s": 0.0,
        }
        if not Alvo:
            Resultado["ok"] = False
            Resultado["motivo"] = "alvo_ausente"
            return Resultado
        Inicio = time.monotonic()
        Amostras = min(FuzzResonance.AMOSTRAS, Resultado["iteracoes"])
        Tamanhos = []
        Latencias = []
        Status = []
        for _ in range(Amostras):
            R = FuzzResonance._UmaAmostra(Alvo, 80)
            if not R.get("ok"):
                continue
            Tamanhos.append(R.get("tamanho", 0))
            Latencias.append(R.get("latencia", 0.0))
            Status.append(R.get("status", 0))
        Resultado["iteracoes"] = len(Tamanhos)
        if len(Tamanhos) >= 3:
            Media = statistics.mean(Tamanhos)
            Stdev = statistics.stdev(Tamanhos)
            CV = (Stdev / Media) if Media > 0 else 0.0
            Resultado["estatisticas"] = {
                "tamanho_media": round(Media, 1),
                "tamanho_stdev": round(Stdev, 1),
                "tamanho_cv": round(CV, 3),
                "latencia_media": round(statistics.mean(Latencias), 3),
                "latencia_stdev": round(statistics.stdev(Latencias), 3),
            }
            if CV > FuzzResonance.LIMIAR_CV:
                Resultado["anomalias"].append({
                    "tipo": "resonance_tamanho_instavel",
                    "cv": round(CV, 3),
                    "min": min(Tamanhos), "max": max(Tamanhos),
                })
            MaxLat = max(Latencias)
            if MaxLat > FuzzResonance.LIMIAR_LATENCIA:
                Resultado["anomalias"].append({
                    "tipo": "resonance_latencia_alta",
                    "max_latencia": round(MaxLat, 2),
                })
            if len(set(Status)) > 1:
                Resultado["anomalias"].append({
                    "tipo": "resonance_status_instavel",
                    "status_distintos": sorted(set(Status)),
                })
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        return Resultado

    @staticmethod
    def _UmaAmostra(Alvo, Porta):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzResonance.TIMEOUT)
        Inicio = time.monotonic()
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            Req = (f"GET / HTTP/1.0\r\nHost: {Alvo}\r\n"
                   f"Connection: close\r\n\r\n")
            Sock.sendall(Req.encode("utf-8", errors="replace"))
            Dados = Sock.recv(8192)
            return {
                "ok": True,
                "status": FuzzResonance._Status(Dados),
                "tamanho": len(Dados),
                "latencia": round(time.monotonic() - Inicio, 3),
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
    def Info():
        return {"nome": "FuzzResonance", "amostras": FuzzResonance.AMOSTRAS,
                "limiar_cv": FuzzResonance.LIMIAR_CV}
