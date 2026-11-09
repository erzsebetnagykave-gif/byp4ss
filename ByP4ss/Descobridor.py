#!/usr/bin/env python3
# Descobridor — wrapper Python pro descobridor.so (C).
# Detecta padrao em sequencia numerica: linear, quadratico,
# exponencial, periodico, recursivo.
# Integra com RedeNeural (analisa Q-values).

import os
import sys
import re
import json
import ctypes


DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(DIR, "Descobridor", "descobridor.so")


class Descobridor:

    Lib = None

    @staticmethod
    def _Carregar():
        if Descobridor.Lib is not None:
            return Descobridor.Lib
        if not os.path.isfile(LIB_PATH):
            return None
        try:
            Lib = ctypes.CDLL(LIB_PATH)
            Lib.Descobridor_Analisar.argtypes = [
                ctypes.POINTER(ctypes.c_double), ctypes.c_int,
                ctypes.c_char_p, ctypes.c_int,
            ]
            Lib.Descobridor_Analisar.restype = ctypes.c_int
            Lib.Descobridor_Versao.restype = ctypes.c_char_p
            Descobridor.Lib = Lib
            return Lib
        except Exception:
            return None

    @staticmethod
    def Analisar(Seq):
        """Seq: list[float] -> dict {tipo, coeficientes/periodo, erro, n_pontos}."""
        Lib = Descobridor._Carregar()
        if Lib is None:
            return {"ok": False, "motivo": "lib_indisponivel",
                    "caminho": LIB_PATH}
        if not isinstance(Seq, (list, tuple)) or len(Seq) < 2:
            return {"ok": False, "motivo": "sequencia_invalida"}
        N = len(Seq)
        Arr = (ctypes.c_double * N)(*[float(x) for x in Seq])
        Buf = ctypes.create_string_buffer(512)
        Ok = Lib.Descobridor_Analisar(Arr, N, Buf, 512)
        try:
            D = json.loads(Buf.value.decode("utf-8", "replace"))
        except Exception as E:
            return {"ok": False, "motivo": f"json_invalido:{E}",
                    "raw": Buf.value.decode("utf-8", "replace")}
        D["ok"] = bool(Ok)
        D["n_pontos"] = N
        return D

    @staticmethod
    def AnalisarArquivo(Caminho, Padrao=r"\d+\.\d+|\d+"):
        """Extrai numeros do arquivo e analisa como sequencia."""
        if not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "arquivo_nao_encontrado"}
        try:
            with open(Caminho, "r", encoding="utf-8", errors="replace") as F:
                Texto = F.read()
        except Exception as E:
            return {"ok": False, "motivo": f"leitura_falhou:{type(E).__name__}",
                    "erro": str(E)}
        Numeros = re.findall(Padrao, Texto)
        if len(Numeros) < 2:
            return {"ok": False, "motivo": "sem_numeros_suficientes",
                    "encontrados": len(Numeros)}
        Seq = [float(x) for x in Numeros[:256]]
        R = Descobridor.Analisar(Seq)
        R["fonte"] = Caminho
        R["numeros_extraidos"] = len(Seq)
        return R

    @staticmethod
    def AnalisarQTable(CaminhoQTable=None):
        """Extrai Q-values do qtable.json e analisa como sequencia."""
        Caminho = CaminhoQTable or os.path.join(
            os.path.expanduser("~"), ".console", "qtable.json")
        if not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "qtable_nao_encontrada",
                    "caminho": Caminho}
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                P = json.load(F)
        except Exception as E:
            return {"ok": False, "motivo": f"json_invalido:{E}"}
        Dados = P.get("Dados") or {}
        Valores = []
        for H, Linha in Dados.items():
            if not isinstance(Linha, dict):
                continue
            for Acao, V in Linha.items():
                try:
                    Valores.append(float(V))
                except (TypeError, ValueError):
                    pass
        if len(Valores) < 2:
            return {"ok": False, "motivo": "qtable_vazia",
                    "n_valores": len(Valores)}
        R = Descobridor.Analisar(Valores)
        R["qtable"] = Caminho
        R["n_valores"] = len(Valores)
        return R

    @staticmethod
    def Versao():
        Lib = Descobridor._Carregar()
        if Lib is None:
            return "indisponivel"
        try:
            return Lib.Descobridor_Versao().decode("utf-8", "replace")
        except Exception:
            return "erro"

    @staticmethod
    def Info():
        return {
            "nome": "Descobridor",
            "versao": Descobridor.Versao(),
            "lib": LIB_PATH,
            "lib_existe": os.path.isfile(LIB_PATH),
            "detectores": ["linear", "quadratico", "exponencial",
                           "periodico", "recursivo"],
        }


def RodarTeste():
    print("=== TESTE Descobridor ===")
    print()
    print(f"[0] Versao: {Descobridor.Versao()}")
    I = Descobridor.Info()
    if not I["lib_existe"]:
        print(f"[erro] lib nao existe: {LIB_PATH}")
        print("       compile com: gcc -O2 -shared -fPIC -o descobridor.so descobridor.c -lm")
        return 1
    print()

    Casos = [
        ("linear",      [2, 4, 6, 8, 10]),
        ("quadratico",  [1, 4, 9, 16, 25]),
        ("exponencial", [2, 4, 8, 16, 32]),
        ("periodico",   [1, 2, 3, 1, 2, 3]),
        ("recursivo",   [1, 1, 2, 3, 5, 8]),
        ("sem_padrao",  [3, 1, 4, 1, 5, 9]),
    ]
    for I, (Esperado, Seq) in enumerate(Casos, 1):
        R = Descobridor.Analisar(Seq)
        Tipo = R.get("tipo", "?")
        Marca = "ok" if Tipo == Esperado else f"esperado={Esperado}"
        print(f"[{I}] {str(Seq):30s} -> {Tipo:12s} {Marca}")
        if Tipo != Esperado and Esperado != "sem_padrao":
            print(f"    detalhes: {R}")
            return 1

    print()
    print("[7] AnalisarArquivo (logs/byp4ss.log, primeiros 50 numeros)")
    Log = os.path.join(DIR, "logs", "byp4ss.log")
    if os.path.isfile(Log):
        R = Descobridor.AnalisarArquivo(Log)
        print(f"  tipo={R.get('tipo', '?')} n={R.get('numeros_extraidos', 0)}")
    else:
        print(f"  [skip] {Log} nao existe")

    print()
    print("[8] AnalisarQTable")
    R = Descobridor.AnalisarQTable()
    if R.get("ok") is not None and "tipo" in R:
        print(f"  tipo={R.get('tipo')} n_valores={R.get('n_valores')}")
    else:
        print(f"  {R.get('motivo', R)}")

    print()
    print("TESTE OK Descobridor")
    return 0


def Main():
    import argparse
    P = argparse.ArgumentParser(prog="Descobridor")
    P.add_argument("--teste", action="store_true")
    P.add_argument("--seq", default=None,
                   help="sequencia: 2,4,6,8,10")
    P.add_argument("--arquivo", default=None)
    P.add_argument("--qtable", action="store_true")
    P.add_argument("--info", action="store_true")
    Args = P.parse_args()
    if Args.teste:
        return RodarTeste()
    if Args.info:
        print(json.dumps(Descobridor.Info(), indent=2, ensure_ascii=False))
        return 0
    if Args.seq:
        try:
            Seq = [float(x.strip()) for x in Args.seq.split(",") if x.strip()]
        except ValueError:
            print("[erro] --seq invalido")
            return 2
        R = Descobridor.Analisar(Seq)
        print(json.dumps(R, indent=2, ensure_ascii=False))
        return 0
    if Args.arquivo:
        R = Descobridor.AnalisarArquivo(Args.arquivo)
        print(json.dumps(R, indent=2, ensure_ascii=False))
        return 0
    if Args.qtable:
        R = Descobridor.AnalisarQTable()
        print(json.dumps(R, indent=2, ensure_ascii=False))
        return 0
    P.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(Main())
