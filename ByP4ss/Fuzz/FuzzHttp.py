# FuzzHttp do ByP4ss
# Muta metodo e headers HTTP, mede anomalia de resposta.
# Chamado por FuzzEngine: Mod.Testar(Alvo, Iteracoes) -> dict

import time
import socket
import urllib.request
import urllib.error

from Core.Config import Config
from Core.Log import Log


class FuzzHttp:

    METODOS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "TRACE", "HEAD"]
    PATHS = ["/", "/index.html", "/admin", "/api", "/%00", "/../", "/..;/"]
    HEADERS_MUTADOS = [
        ("Content-Length", "-1"),
        ("Content-Length", "99999999"),
        ("Transfer-Encoding", "chunked"),
        ("Transfer-Encoding", "gzip, chunked"),
        ("Host", ""),
        ("Host", "a" * 2000),
        ("X-Forwarded-For", "127.0.0.1"),
        ("X-Forwarded-For", "127.0.0.1, 127.0.0.1"),
        ("X-Original-URL", "/admin"),
        ("X-Rewrite-URL", "/admin"),
        ("Authorization", "Basic " + "A" * 2000),
        ("User-Agent", "\x00\x01\x02\x03"),
    ]
    TIMEOUT = 1.5

    @staticmethod
    def Testar(Alvo, Iteracoes):
        Resultado = {
            "ok": True,
            "tecnica": "http",
            "iteracoes": int(Iteracoes or 100),
            "crashes": [],
            "anomalias": [],
            "duracao_s": 0.0,
        }
        if not Alvo:
            Resultado["ok"] = False
            Resultado["motivo"] = "alvo_ausente"
            return Resultado
        Inicio = time.monotonic()
        Porta = 80
        Baseline = FuzzHttp._Baseline(Alvo, Porta)
        Count = 0
        for Metodo in FuzzHttp.METODOS:
            for Path in FuzzHttp.PATHS:
                if Count >= Resultado["iteracoes"]:
                    break
                R = FuzzHttp._TestarMetodo(Alvo, Porta, Metodo, Path)
                Count += 1
                FuzzHttp._Registrar(R, Baseline, Metodo, Path, Resultado)
            if Count >= Resultado["iteracoes"]:
                break
        for H, V in FuzzHttp.HEADERS_MUTADOS:
            if Count >= Resultado["iteracoes"]:
                break
            R = FuzzHttp._TestarHeader(Alvo, Porta, H, V)
            Count += 1
            FuzzHttp._Registrar(R, Baseline, "HEADER:" + H, V[:40], Resultado)
        Resultado["iteracoes"] = Count
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        return Resultado

    @staticmethod
    def _Baseline(Alvo, Porta):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzHttp.TIMEOUT)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "status": 0, "tamanho": 0}
            Req = f"GET / HTTP/1.0\r\nHost: {Alvo}\r\n\r\n".encode()
            Sock.sendall(Req)
            Dados = Sock.recv(4096)
            return {"ok": True, "status": 200, "tamanho": len(Dados)}
        except Exception:
            return {"ok": False, "status": 0, "tamanho": 0}
        finally:
            try: Sock.close()
            except Exception: pass

    @staticmethod
    def _TestarMetodo(Alvo, Porta, Metodo, Path):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzHttp.TIMEOUT)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            Req = f"{Metodo} {Path} HTTP/1.1\r\nHost: {Alvo}\r\nConnection: close\r\n\r\n"
            Sock.sendall(Req.encode("utf-8", errors="replace"))
            Dados = Sock.recv(4096)
            return {"ok": True, "status": FuzzHttp._StatusDe(Dados), "tamanho": len(Dados)}
        except socket.timeout:
            return {"ok": False, "motivo": "timeout"}
        except Exception as E:
            return {"ok": False, "motivo": type(E).__name__}
        finally:
            try: Sock.close()
            except Exception: pass

    @staticmethod
    def _TestarHeader(Alvo, Porta, Header, Valor):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzHttp.TIMEOUT)
        try:
            if Sock.connect_ex((Alvo, Porta)) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            Req = (f"GET / HTTP/1.1\r\nHost: {Alvo}\r\n"
                   f"{Header}: {Valor}\r\nConnection: close\r\n\r\n")
            Sock.sendall(Req.encode("utf-8", errors="replace"))
            Dados = Sock.recv(4096)
            return {"ok": True, "status": FuzzHttp._StatusDe(Dados), "tamanho": len(Dados)}
        except socket.timeout:
            return {"ok": False, "motivo": "timeout"}
        except Exception as E:
            return {"ok": False, "motivo": type(E).__name__}
        finally:
            try: Sock.close()
            except Exception: pass

    @staticmethod
    def _StatusDe(Dados):
        if not Dados:
            return 0
        try:
            Primeira = Dados.split(b"\r\n", 1)[0].decode("utf-8", errors="replace")
            Partes = Primeira.split()
            if len(Partes) >= 2:
                return int(Partes[1])
        except Exception:
            pass
        return 0

    @staticmethod
    def _Registrar(R, Baseline, Metodo, Path, Resultado):
        if not R.get("ok"):
            if R.get("motivo") == "timeout":
                Resultado["anomalias"].append({
                    "tipo": "timeout", "metodo": Metodo, "path": str(Path)[:40],
                })
            return
        Status = R.get("status", 0)
        if Status >= 500:
            Resultado["crashes"].append({
                "tipo": "http_5xx", "status": Status,
                "metodo": Metodo, "path": str(Path)[:40],
            })
        elif Status == 0 and Baseline.get("ok"):
            Resultado["anomalias"].append({
                "tipo": "resposta_vazia", "metodo": Metodo, "path": str(Path)[:40],
            })

    @staticmethod
    def Info():
        return {
            "nome": "FuzzHttp", "metodos": FuzzHttp.METODOS,
            "paths": len(FuzzHttp.PATHS), "headers": len(FuzzHttp.HEADERS_MUTADOS),
        }
