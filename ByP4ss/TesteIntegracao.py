#!/usr/bin/env python3
# TesteIntegracao — roda o ByP4ss do inicio ao fim contra 127.0.0.1.
# Prova que o pipeline fecha: discover -> bypass -> fuzz -> verify -> report.
# Nao executa exploit. So fases passivas.

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Core.Config import Config
from Core.Log import Log
from Core.Engine import Engine


class TesteIntegracao:

    ALVO = "127.0.0.1"
    PORTAS = [53, 80, 443]
    TIMEOUT = 1.0

    @staticmethod
    def Rodar(Alvo=None, Json=False):
        Alvo = Alvo or TesteIntegracao.ALVO
        Inicio = time.monotonic()
        Config.Alvo = Alvo
        Config.Portas = TesteIntegracao.PORTAS
        Config.Threads = 1
        Config.ThreadsPorts = 1
        Config.ThreadsFuzz = 1
        Config.Timeout = TesteIntegracao.TIMEOUT
        Config.TimeoutTCP = TesteIntegracao.TIMEOUT
        Config.TimeoutSSDP = 0.5
        Config.TimeoutHTTP = TesteIntegracao.TIMEOUT
        Config.TimeoutVerify = TesteIntegracao.TIMEOUT
        Config.Salvar = True
        Config.FuzzIteracoes = 5
        Log.Iniciar(Config)
        Engine.Iniciar(Config)
        Etapas = []
        try:
            D = Engine.Discover(Alvo)
            Etapas.append({"fase": "discover", "ok": bool(D),
                           "portas": len(D.get("portas_abertas") or []) if D else 0})
        except Exception as E:
            Etapas.append({"fase": "discover", "ok": False,
                           "erro": f"{type(E).__name__}:{E}"})
        try:
            B = Engine.Bypass(Alvo)
            Etapas.append({"fase": "bypass", "ok": bool(B)})
        except Exception as E:
            Etapas.append({"fase": "bypass", "ok": False,
                           "erro": f"{type(E).__name__}:{E}"})
        try:
            F = Engine.Fuzz(Alvo)
            Tecnicas = 0
            if F and isinstance(F.get("tecnicas"), dict):
                Tecnicas = len(F["tecnicas"])
            Etapas.append({"fase": "fuzz", "ok": bool(F), "tecnicas": Tecnicas})
        except Exception as E:
            Etapas.append({"fase": "fuzz", "ok": False,
                           "erro": f"{type(E).__name__}:{E}"})
        try:
            V = Engine.Verify(Alvo)
            Etapas.append({"fase": "verify", "ok": bool(V)})
        except Exception as E:
            Etapas.append({"fase": "verify", "ok": False,
                           "erro": f"{type(E).__name__}:{E}"})
        try:
            R = Engine.Report()
            Etapas.append({"fase": "report", "ok": bool(R)})
        except Exception as E:
            Etapas.append({"fase": "report", "ok": False,
                           "erro": f"{type(E).__name__}:{E}"})
        finally:
            try:
                Engine.Finalizar()
            except Exception:
                pass
            try:
                Log.Finalizar()
            except Exception:
                pass
        Arquivos = TesteIntegracao._VerificarArquivos()
        Resultado = {
            "ok": all(E.get("ok") for E in Etapas) and Arquivos.get("ok"),
            "alvo": Alvo,
            "etapas": Etapas,
            "arquivos": Arquivos,
            "duracao_s": round(time.monotonic() - Inicio, 2),
        }
        if Json:
            print(json.dumps(Resultado, indent=2, ensure_ascii=False, default=str))
        else:
            TesteIntegracao._Imprimir(Resultado)
        return Resultado

    @staticmethod
    def _VerificarArquivos():
        Rep = Config.DirReports
        Esperados = [
            "report.json",
            "report.md",
            "report.csv",
            "report.dataset.jsonl",
            "report.ambiente.json",
        ]
        Encontrados = {}
        Faltando = []
        for A in Esperados:
            P = os.path.join(Rep, A)
            if os.path.isfile(P):
                Encontrados[A] = os.path.getsize(P)
            else:
                Faltando.append(A)
        return {"ok": len(Faltando) == 0,
                "encontrados": Encontrados,
                "faltando": Faltando,
                "total": len(Encontrados)}

    @staticmethod
    def _Imprimir(R):
        print()
        print(f"=== TESTE INTEGRACAO ({R['alvo']}) ===")
        print()
        for E in R.get("etapas") or []:
            Marca = "ok" if E.get("ok") else "FALHOU"
            Extra = ""
            if "portas" in E:
                Extra = f" ({E['portas']} portas)"
            if "tecnicas" in E:
                Extra = f" ({E['tecnicas']} tecnicas)"
            if "erro" in E:
                Extra = f" ({E['erro'][:50]})"
            print(f"  [{Marca}] {E.get('fase')}{Extra}")
        print()
        A = R.get("arquivos") or {}
        print(f"=== ARQUIVOS em reports/ ===")
        for Nome, Tam in (A.get("encontrados") or {}).items():
            print(f"  [ok] {Nome}: {Tam} bytes")
        if A.get("faltando"):
            for F in A["faltando"]:
                print(f"  [FALTA] {F}")
        print()
        print(f"duracao: {R.get('duracao_s')}s")
        print(f"resultado: {'TESTE OK' if R.get('ok') else 'TESTE FALHOU'}")


def Main():
    import argparse
    P = argparse.ArgumentParser(prog="TesteIntegracao")
    P.add_argument("--alvo", default=None)
    P.add_argument("--json", action="store_true")
    Args = P.parse_args()
    R = TesteIntegracao.Rodar(Args.alvo, Args.json)
    return 0 if R.get("ok") else 1


if __name__ == "__main__":
    sys.exit(Main())
