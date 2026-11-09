# FuzzEngine do ByP4ss
# Orquestrador: chama as tecnicas de fuzz, agrega crashes + anomalias.
# Chamado por Core.Engine.Fuzz: Mod.FuzzEngine.Executar(Alvo, Iteracoes)
#
# Nao executa nada malicioso. So manda payload HTTP, le resposta, mede anomalia.
# Contra 127.0.0.1 fechado, todas as tecnicas retornam vazio (esperado).

import time

from Core.Config import Config
from Core.Log import Log

try:
    from Fuzz.FuzzHttp import FuzzHttp
except Exception:
    FuzzHttp = None
try:
    from Fuzz.FuzzCrlf import FuzzCrlf
except Exception:
    FuzzCrlf = None

try:
    from Fuzz.FuzzSqli import FuzzSqli
except Exception:
    FuzzSqli = None

try:
    from Fuzz.FuzzPath import FuzzPath
except Exception:
    FuzzPath = None

try:
    from Fuzz.FuzzXss import FuzzXss
except Exception:
    FuzzXss = None

try:
    from Fuzz.FuzzNullspace import FuzzNullspace
except Exception:
    FuzzNullspace = None

try:
    from Fuzz.FuzzMetamorph import FuzzMetamorph
except Exception:
    FuzzMetamorph = None

try:
    from Fuzz.FuzzResonance import FuzzResonance
except Exception:
    FuzzResonance = None

try:
    from Fuzz.FuzzOracle import FuzzOracle
except Exception:
    FuzzOracle = None


class FuzzEngine:

    ITERACOES_PADRAO = 100
    TIMEOUT_TECNICA = 60.0

    @staticmethod
    def Executar(Alvo, Iteracoes=None):
        Iteracoes = int(Iteracoes or FuzzEngine.ITERACOES_PADRAO)
        if Iteracoes < 1:
            Iteracoes = FuzzEngine.ITERACOES_PADRAO
        if Iteracoes > 500:
            Iteracoes = 500
        Resultado = {
            "ok": True,
            "alvo": Alvo,
            "iteracoes": Iteracoes,
            "crashes": [],
            "anomalias": [],
            "tecnicas": {},
            "duracao_s": 0.0,
        }
        if not Alvo:
            Resultado["ok"] = False
            Resultado["motivo"] = "alvo_ausente"
            return Resultado
        Tecnicas = FuzzEngine._ListarTecnicas()
        if not Tecnicas:
            Resultado["ok"] = False
            Resultado["motivo"] = "sem_tecnicas"
            return Resultado
        Log.Info("fuzz iniciado", {"alvo": Alvo, "iteracoes": Iteracoes,
                                     "tecnicas": len(Tecnicas)})
        Inicio = time.monotonic()
        for Nome, Tecnica in Tecnicas:
            if time.monotonic() - Inicio > FuzzEngine.TIMEOUT_TECNICA:
                Resultado["tecnicas"][Nome] = {"ok": False, "motivo": "timeout_global"}
                break
            try:
                R = Tecnica.Testar(Alvo, Iteracoes)
                if not isinstance(R, dict):
                    R = {"ok": False, "motivo": "retorno_invalido"}
            except Exception as E:
                R = {"ok": False, "motivo": f"excecao:{type(E).__name__}",
                     "erro": str(E)}
            Resultado["tecnicas"][Nome] = {
                "ok": R.get("ok", False),
                "crashes": len(R.get("crashes") or []),
                "anomalias": len(R.get("anomalias") or []),
                "duracao_s": R.get("duracao_s", 0.0),
                "motivo": R.get("motivo", ""),
            }
            Resultado["crashes"].extend(R.get("crashes") or [])
            Resultado["anomalias"].extend(R.get("anomalias") or [])
        Resultado["duracao_s"] = round(time.monotonic() - Inicio, 2)
        Log.Info("fuzz concluido", {
            "alvo": Alvo, "crashes": len(Resultado["crashes"]),
            "anomalias": len(Resultado["anomalias"]),
            "duracao_s": Resultado["duracao_s"],
        })
        return Resultado

    @staticmethod
    def _ListarTecnicas():
        Lista = []
        if FuzzHttp is not None:
            Lista.append(("http", FuzzHttp))
        if FuzzCrlf is not None:
            Lista.append(("crlf", FuzzCrlf))
        if FuzzSqli is not None:
            Lista.append(("sqli", FuzzSqli))
        if FuzzPath is not None:
            Lista.append(("path", FuzzPath))
        if FuzzXss is not None:
            Lista.append(("xss", FuzzXss))
        if FuzzNullspace is not None:
            Lista.append(("nullspace", FuzzNullspace))
        if FuzzMetamorph is not None:
            Lista.append(("metamorph", FuzzMetamorph))
        if FuzzResonance is not None:
            Lista.append(("resonance", FuzzResonance))
        if FuzzOracle is not None:
            Lista.append(("oracle", FuzzOracle))
        return Lista

    @staticmethod
    def Info():
        Lista = FuzzEngine._ListarTecnicas()
        return {
            "nome": "FuzzEngine",
            "iteracoes_padrao": FuzzEngine.ITERACOES_PADRAO,
            "timeout_tecnica": FuzzEngine.TIMEOUT_TECNICA,
            "tecnicas": [N for N, _ in Lista],
            "total_tecnicas": len(Lista),
        }


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        Alvo = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
        It = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        print(f"fuzz {Alvo} iteracoes={It}")
        R = FuzzEngine.Executar(Alvo, It)
        print(json.dumps(R, indent=2, ensure_ascii=False, default=str))
    else:
        print("uso: python3 Fuzz/FuzzEngine.py teste [alvo] [iteracoes]")
