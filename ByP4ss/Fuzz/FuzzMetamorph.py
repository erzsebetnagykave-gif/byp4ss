# FuzzMetamorph do ByP4ss
# Mesma query SQL em 20 sintaxes. Detecta se o servidor normaliza.
# Chamado por FuzzEngine: Mod.Testar(Alvo, Iteracoes) -> dict

import time
import socket
import urllib.parse

from Core.Config import Config
from Core.Log import Log


class FuzzMetamorph:

    PATH = "/"
    PARAM = "id"

    VARIANTES = [
        "1",
        " 1",
        "1 ",
        "1\t",
        "1\n",
        "1\r\n",
        "0x31",
        "1e0",
        "01",
        "+1",
        "-1",
        "'1'",
        "\"1\"",
        "`1`",
        "(1)",
        "((1))",
        "1/**/",
        "/**/1",
        "1--",
        "1#",
        "1;",
    ]
    TIMEOUT = 2.0
    LIMIAR_DIFERENCA = 100

    @staticmethod
    def Testar(Alvo, Iteracoes):
        Resultado = {
            "ok": True, "tecnica": "metamorph",
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
        Respostas = []
        Count = 0
        for Variante in FuzzMetamorph.VARIANTES:
            if Count >= Resultado["iteracoes"]:
                break
            R = FuzzMetamorph._TestarVariante(Alvo, Porta, Variante)
            Count += 1
            if R.get("ok"):
                Respostas.append({"variante": Variante, "tamanho": R.get("tamanho", 0),
                                  "status": R.get("status", 0)})
        Resultado["iteracoes"] = Count
        if len(Respostas) >= 2:
            Tamanhos = [R["tamanho"] for R in Respostas]
            MinT, MaxT = min(Tamanhos), max(Tamanhos)
            if MaxT - MinT > FuzzMetamorph.LIMIAR_DIFERENCA:
                Resultado["anomalias"].append({
                    "tipo": "metamorph_diferenca",
                    "min": MinT, "max": MaxT,
                    "variantes_distintas": len(set(Tamanhos)),
                })
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        return Resultado

    @staticmethod
    def _TestarVariante(Alvo, Porta, Variante):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzMetamorph.TIMEOUT)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            ValorEnc = urllib.parse.quote(Variante, safe="")
            Req = (f"GET {FuzzMetamorph.PATH}?{FuzzMetamorph.PARAM}={ValorEnc} HTTP/1.0\r\n"
                   f"Host: {Alvo}\r\nConnection: close\r\n\r\n")
            Sock.sendall(Req.encode("utf-8", errors="replace"))
            Dados = Sock.recv(8192)
            return {"ok": True, "status": FuzzMetamorph._Status(Dados),
                    "tamanho": len(Dados)}
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
        return {"nome": "FuzzMetamorph", "variantes": len(FuzzMetamorph.VARIANTES)}
