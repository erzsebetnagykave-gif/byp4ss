# Ambiente do ByP4ss
# Gera report.ambiente.json — estado consolidado do alvo no formato
# que o Q-Learning consome direto como OBSERVACAO.
#
# Formato (contrato B4S):
#   {
#     "alvo": str,
#     "modo": str,
#     "timestamp": iso,
#     "observacao": {
#       "portas_abertas": [int],
#       "portas_fechadas": [int],
#       "servicos": {"porta": "servico"},
#       "fabricante": str|None,
#       "modelo": str|None,
#       "os": str|None,
#       "cves_sugeridas": [str],
#       "credenciais_total": int,
#       "sessoes_abertas": int,
#       "ultima_acao": str,
#       "ultimo_ok": bool,
#       "ultima_severidade": str|None,
#     },
#     "acoes_disponiveis": [15 strings],
#     "acoes_ja_executadas": [str],
#     "recompensa_acumulada": float,
#     "terminou": bool,
#     "motivo_termino": str|None,
#   }

import os
import json
from datetime import datetime, timezone

from Core.Config import Config
from Core.Log import Log


class Ambiente:

    NOME_ARQUIVO = "report.ambiente.json"

    ACOES_PALETA = [
        "scan", "analise", "ssdp", "cred",
        "shell_rev", "shell_bind",
        "exploit_tplink", "exploit_dlink", "exploit_tenda7795",
        "exploit_arcadyan", "exploit_iptime", "exploit_tenda29384",
        "chain", "upnp", "httpauth",
    ]

    FASES_PARA_ACOES = {
        "discover": ["scan", "analise", "ssdp"],
        "bypass": ["upnp", "httpauth"],
        "fuzz": [],
        "verify": [],
        "report": [],
    }

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def Salvar(Resultados, Caminho=None, Terminou=True, MotivoTermino=None):
        if not isinstance(Resultados, dict):
            return {"ok": False, "motivo": "resultados_invalidos"}
        if not Ambiente._GarantirDir():
            return {"ok": False, "motivo": "dir_indisponivel"}
        Caminho = Caminho or Ambiente._Caminho()
        Payload = Ambiente.Observacao(Resultados, Terminou=Terminou,
                                       MotivoTermino=MotivoTermino)
        try:
            with open(Caminho, "w", encoding="utf-8") as F:
                json.dump(Payload, F, ensure_ascii=False, indent=2)
            Tamanho = os.path.getsize(Caminho)
            Log.Info("ambiente salvo", {
                "caminho": Caminho, "bytes": Tamanho,
                "portas_abertas": len(Payload["observacao"]["portas_abertas"]),
                "acoes_ja": len(Payload["acoes_ja_executadas"]),
            })
            return {"ok": True, "caminho": Caminho, "tamanho_bytes": Tamanho,
                    "formato": "ambiente"}
        except Exception as E:
            Log.Erro("ambiente falhou", {"erro": str(E)})
            return {"ok": False, "motivo": f"escrita_falhou:{type(E).__name__}",
                    "erro": str(E)}

    @staticmethod
    def Observacao(Resultados, Terminou=True, MotivoTermino=None):
        if not isinstance(Resultados, dict):
            Resultados = {}
        Achados = Ambiente._ExtrairAchados(Resultados)
        Fases = Resultados.get("fases") or {}
        PortasAbertas = sorted(set(Ambiente._Portas(Achados, "porta_aberta")))
        PortasFechadas = sorted(set(Ambiente._Portas(Achados, "porta_fechada")))
        Servicos = Ambiente._Servicos(Achados)
        Fabricante, Modelo, Os = Ambiente._Fingerprint(Achados)
        Cves = Ambiente._Cves(Achados)
        Credenciais = Ambiente._Contar(Achados, prefixo="credencial")
        Sessoes = Ambiente._Contar(Achados, prefixo="sessao") + Ambiente._Contar(Achados, tipo="exploit_verificado")
        Ultima = Achados[-1] if Achados else {}
        Recompensa = Ambiente._RecompensaTotal(Resultados)
        AcoesJa = Ambiente._InferirAcoesJa(Fases, Achados)
        return {
            "alvo": Ambiente._Alvo(Resultados, Achados),
            "modo": Resultados.get("modo") or "local",
            "timestamp": Ambiente.Timestamp(),
            "observacao": {
                "portas_abertas": PortasAbertas,
                "portas_fechadas": PortasFechadas,
                "servicos": Servicos,
                "fabricante": Fabricante,
                "modelo": Modelo,
                "os": Os,
                "cves_sugeridas": Cves,
                "credenciais_total": Credenciais,
                "sessoes_abertas": Sessoes,
                "ultima_acao": Ultima.get("tipo") or "?",
                "ultimo_ok": Ultima.get("severidade") != "info" or not Ultima.get("tipo", "").endswith("_falhou"),
                "ultima_severidade": Ultima.get("severidade"),
            },
            "acoes_disponiveis": list(Ambiente.ACOES_PALETA),
            "acoes_ja_executadas": AcoesJa,
            "recompensa_acumulada": round(Recompensa, 2),
            "terminou": bool(Terminou),
            "motivo_termino": MotivoTermino,
        }

    @staticmethod
    def Carregar(Caminho=None):
        Caminho = Caminho or Ambiente._Caminho()
        if not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "arquivo_nao_encontrado"}
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                D = json.load(F)
            if not isinstance(D, dict):
                return {"ok": False, "motivo": "formato_invalido"}
            return {"ok": True, "caminho": Caminho,
                    "alvo": D.get("alvo"),
                    "modo": D.get("modo"),
                    "observacao": D.get("observacao") or {},
                    "acoes_disponiveis": D.get("acoes_disponiveis") or [],
                    "acoes_ja_executadas": D.get("acoes_ja_executadas") or [],
                    "recompensa_acumulada": float(D.get("recompensa_acumulada", 0.0)),
                    "terminou": bool(D.get("terminou", True)),
                    "motivo_termino": D.get("motivo_termino")}
        except Exception as E:
            return {"ok": False, "motivo": f"leitura_falhou:{type(E).__name__}",
                    "erro": str(E)}

    @staticmethod
    def Acoes():
        return list(Ambiente.ACOES_PALETA)

    @staticmethod
    def _Alvo(Resultados, Achados):
        if isinstance(Resultados.get("alvo"), str) and Resultados["alvo"]:
            return Resultados["alvo"]
        if Achados:
            return Achados[0].get("alvo", "?")
        return "?"

    @staticmethod
    def _ExtrairAchados(Resultados):
        F = Resultados.get("findings") if isinstance(Resultados, dict) else None
        if isinstance(F, dict):
            return F.get("achados") or []
        if isinstance(F, list):
            return F
        return []

    @staticmethod
    def _Portas(Achados, Tipo):
        Out = []
        for A in Achados:
            if A.get("tipo") == Tipo:
                D = A.get("dados") or {}
                P = D.get("porta")
                if P is not None:
                    try:
                        Out.append(int(P))
                    except (TypeError, ValueError):
                        pass
        return Out

    @staticmethod
    def _Servicos(Achados):
        Out = {}
        for A in Achados:
            if A.get("tipo") in ("porta_aberta", "servico_verificado"):
                D = A.get("dados") or {}
                P = D.get("porta")
                S = D.get("servico")
                if P is not None and S:
                    Out[str(P)] = S
        return Out

    @staticmethod
    def _Fingerprint(Achados):
        for A in Achados:
            if A.get("tipo") != "fingerprint":
                continue
            D = A.get("dados") or {}
            Fab = D.get("fabricante")
            Mod = D.get("modelo")
            Os = D.get("os")
            if Fab or Mod or Os:
                return Fab, Mod, Os
        return None, None, None

    @staticmethod
    def _Cves(Achados):
        Out = []
        for A in Achados:
            if A.get("tipo") == "cve_sugerida":
                D = A.get("dados") or {}
                Id = D.get("id")
                if Id:
                    Out.append(Id)
        return sorted(set(Out))

    @staticmethod
    def _Contar(Achados, tipo=None, prefixo=None):
        N = 0
        for A in Achados:
            T = A.get("tipo", "")
            if tipo and T == tipo:
                N += 1
            elif prefixo and T.startswith(prefixo):
                N += 1
        return N

    @staticmethod
    def _RecompensaTotal(Resultados):
        R = 0.0
        for A in Ambiente._ExtrairAchados(Resultados):
            R += float(A.get("peso", 1)) * 1.0
        DS = Resultados.get("dataset") if isinstance(Resultados, dict) else None
        if isinstance(DS, dict) and "rewards" in DS:
            R = sum(float(X) for X in DS["rewards"])
        return R

    @staticmethod
    def _InferirAcoesJa(Fases, Achados):
        if not isinstance(Fases, dict):
            Fases = {}
        Ja = set()
        for Fase, Lista in Fases.items():
            if not isinstance(Lista, list) or not Lista:
                continue
            for Acao in Ambiente.FASES_PARA_ACOES.get(Fase, []):
                Ja.add(Acao)
        for A in Achados:
            T = A.get("tipo", "")
            if T.startswith("bypass_"):
                Mod = T.replace("bypass_", "").replace("_falhou", "")
                if Mod in Ambiente.ACOES_PALETA:
                    Ja.add(Mod)
        return sorted(Ja)

    @staticmethod
    def _GarantirDir():
        try:
            os.makedirs(Config.DirReports, exist_ok=True)
            return True
        except OSError:
            return False

    @staticmethod
    def _Caminho():
        return os.path.join(Config.DirReports, Ambiente.NOME_ARQUIVO)

    @staticmethod
    def Info():
        return {
            "nome": "Ambiente",
            "arquivo": Ambiente.NOME_ARQUIVO,
            "acoes": list(Ambiente.ACOES_PALETA),
            "total_acoes": len(Ambiente.ACOES_PALETA),
        }


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        Rep = os.path.join(Config.DirReports, "report.json")
        if not os.path.isfile(Rep):
            print(f"[erro] {Rep} nao existe. Rode: python3 ByP4ss.py 127.0.0.1 --all")
            sys.exit(1)
        with open(Rep, "r", encoding="utf-8") as F:
            Resultados = json.load(F)
        R = Ambiente.Salvar(Resultados, Terminou=True, MotivoTermino="report_ok")
        print(json.dumps(R, indent=2, ensure_ascii=False))
        if not R["ok"]:
            sys.exit(1)
        C = Ambiente.Carregar()
        print()
        print(f"[ok] alvo: {C['alvo']}")
        print(f"[ok] portas_abertas: {C['observacao'].get('portas_abertas')}")
        print(f"[ok] fabricante: {C['observacao'].get('fabricante')}")
        print(f"[ok] acoes_disponiveis: {len(C['acoes_disponiveis'])}")
        print(f"[ok] acoes_ja: {C['acoes_ja_executadas']}")
        print(f"[ok] recompensa: {C['recompensa_acumulada']}")
        print(f"[ok] terminou: {C['terminou']}")
    else:
        print("uso: python3 Report/Ambiente.py teste")
