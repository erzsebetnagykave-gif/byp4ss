# Api do ByP4ss pra o Agent B4S.
# Desacopla o B4S do formato de arquivo: ele chama B4SApi.CarregarDataset()
# e recebe {"features": [...], "labels": [...], ...}, sem saber se veio
# de JSONL, CSV ou SQLite.
#
# Uso tipico (Treino.py do Q-Learning):
#   from Report.Api import B4SApi
#   tudo = B4SApi.CarregarTudo()
#   ds = tudo["dataset"]  # {"features": [[...]], "labels": [...], ...}
#   amb = tudo["ambiente"]
#   estado, acao, reward, proximo_estado, done = B4SApi.UltimaTransicao()
#   acoes = B4SApi.Acoes()

import os
import json

from Core.Config import Config
from Report.Dataset import Dataset
from Report.Ambiente import Ambiente


class B4SApi:

    @staticmethod
    def _ReportPath(Nome):
        return os.path.join(Config.DirReports, Nome)

    @staticmethod
    def _LerJson(Caminho):
        if not os.path.isfile(Caminho):
            return None
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                return json.load(F)
        except Exception:
            return None

    @staticmethod
    def CarregarDataset(Caminho=None):
        return Dataset.Carregar(Caminho)

    @staticmethod
    def CarregarAmbiente(Caminho=None):
        return Ambiente.Carregar(Caminho)

    @staticmethod
    def CarregarReport():
        Caminho = B4SApi._ReportPath("report.json")
        return B4SApi._LerJson(Caminho)

    @staticmethod
    def CarregarTudo():
        return {
            "dataset": B4SApi.CarregarDataset(),
            "ambiente": B4SApi.CarregarAmbiente(),
            "report": B4SApi.CarregarReport(),
        }

    @staticmethod
    def Observacao():
        amb = B4SApi.CarregarAmbiente()
        if not amb.get("ok"):
            return {"ok": False, "motivo": amb.get("motivo", "ambiente_indisponivel"),
                    "observacao": {}, "acoes_disponiveis": Ambiente.Acoes(),
                    "recompensa_acumulada": 0.0, "terminou": False}
        return {
            "ok": True,
            "alvo": amb.get("alvo"),
            "modo": amb.get("modo"),
            "observacao": amb.get("observacao") or {},
            "acoes_disponiveis": amb.get("acoes_disponiveis") or Ambiente.Acoes(),
            "acoes_ja_executadas": amb.get("acoes_ja_executadas") or [],
            "recompensa_acumulada": amb.get("recompensa_acumulada", 0.0),
            "terminou": amb.get("terminou", False),
            "motivo_termino": amb.get("motivo_termino"),
        }

    @staticmethod
    def Acoes():
        return Ambiente.Acoes()

    @staticmethod
    def Recompensa(tipo):
        return Dataset.Recompensa(tipo)

    @staticmethod
    def Recompensas():
        return dict(Dataset.RECOMPENSAS)

    @staticmethod
    def Features(achado):
        return Dataset.Features(achado)

    @staticmethod
    def UltimaTransicao():
        ds = B4SApi.CarregarDataset()
        amb = B4SApi.CarregarAmbiente()
        if not ds.get("ok") or ds.get("n", 0) == 0:
            return (None, None, 0.0, None, True)
        Feats = ds.get("features") or []
        Labels = ds.get("labels") or []
        Rewards = ds.get("rewards") or []
        N = len(Feats)
        I = N - 1
        Estado = Feats[I - 1] if I >= 1 else Feats[I]
        Acao = Labels[I]
        Recompensa_ = Rewards[I]
        if I >= 1:
            Proximo = Feats[I]
        else:
            if amb.get("ok"):
                Proximo = Estado
            else:
                Proximo = Feats[I]
        Terminou = bool(amb.get("terminou", True)) if amb.get("ok") else True
        return (Estado, Acao, Recompensa_, Proximo, Terminou)

    @staticmethod
    def Transicoes(Todas=True):
        ds = B4SApi.CarregarDataset()
        amb = B4SApi.CarregarAmbiente()
        if not ds.get("ok") or ds.get("n", 0) == 0:
            return []
        Feats = ds.get("features") or []
        Labels = ds.get("labels") or []
        Rewards = ds.get("rewards") or []
        TerminouFinal = bool(amb.get("terminou", True)) if amb.get("ok") else True
        N = len(Feats)
        Out = []
        for I in range(N):
            Estado = Feats[I - 1] if I >= 1 else Feats[0]
            Proximo = Feats[I]
            Done = (I == N - 1) and TerminouFinal
            Out.append((Estado, Labels[I], Rewards[I], Proximo, Done))
        return Out

    @staticmethod
    def VetorEstado():
        amb = B4SApi.Observacao()
        if not amb.get("ok"):
            return [0.0] * 8
        O = amb.get("observacao") or {}
        Portas = O.get("portas_abertas") or []
        Primeira = Portas[0] if Portas else 0
        F0 = min(max(Primeira / 65535.0, 0.0), 1.0)
        F1 = 1.0 if Portas else 0.0
        F2 = 0.5
        F3 = 1.0 if O.get("fabricante") else 0.0
        Sev = O.get("ultima_severidade") or "info"
        MapaSev = {"info": 0.0, "baixa": 0.25, "media": 0.5, "alta": 0.75, "critica": 1.0}
        F4 = MapaSev.get(Sev, 0.0)
        F5 = 0.5
        Creds = O.get("credenciais_total") or 0
        F6 = min(max(Creds / 10.0, 0.0), 1.0)
        F7 = 1.0 if O.get("ultimo_ok") else 0.0
        return [round(F, 4) for F in (F0, F1, F2, F3, F4, F5, F6, F7)]

    @staticmethod
    def Info():
        return {
            "nome": "B4SApi",
            "metodos": [
                "CarregarDataset", "CarregarAmbiente", "CarregarReport",
                "CarregarTudo", "Observacao", "Acoes", "Recompensa",
                "Recompensas", "Features", "UltimaTransicao", "Transicoes",
                "VetorEstado", "Info",
            ],
            "n_features": 8,
            "total_acoes": len(Ambiente.Acoes()),
            "diretorio": Config.DirReports,
        }


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        print("=== B4SApi.Info ===")
        print(json.dumps(B4SApi.Info(), indent=2, ensure_ascii=False))
        print()
        print("=== CarregarTudo ===")
        T = B4SApi.CarregarTudo()
        print(f"  dataset.ok: {T['dataset'].get('ok')} n={T['dataset'].get('n', 0)}")
        print(f"  ambiente.ok: {T['ambiente'].get('ok')}")
        print(f"  report: {T['report'] is not None}")
        print()
        print("=== Observacao ===")
        O = B4SApi.Observacao()
        print(f"  alvo: {O.get('alvo')}")
        print(f"  portas: {O['observacao'].get('portas_abertas')}")
        print(f"  acoes_disponiveis: {len(O.get('acoes_disponiveis', []))}")
        print(f"  recompensa: {O.get('recompensa_acumulada')}")
        print()
        print("=== Acoes ===")
        A = B4SApi.Acoes()
        print(f"  total: {len(A)}")
        print(f"  primeiras 5: {A[:5]}")
        print()
        print("=== Recompensa ===")
        for T in ["porta_aberta", "cve_sugerida", "exploit_verificado", "bypass_upnp_falhou"]:
            print(f"  {T:25s} {B4SApi.Recompensa(T):+7.2f}")
        print()
        print("=== UltimaTransicao ===")
        Trans = B4SApi.UltimaTransicao()
        Estado, Acao, Rwd, Proximo, Done = Trans
        print(f"  estado: {Estado}")
        print(f"  acao: {Acao}")
        print(f"  recompensa: {Rwd}")
        print(f"  proximo: {Proximo}")
        print(f"  done: {Done}")
        print()
        print("=== Transicoes (todas) ===")
        Ts = B4SApi.Transicoes()
        print(f"  total: {len(Ts)}")
        for I, (S, A_, R_, S2, D) in enumerate(Ts):
            print(f"  [{I}] acao={A_:25s} reward={R_:+7.2f} done={D}")
        print()
        print("=== VetorEstado ===")
        V = B4SApi.VetorEstado()
        print(f"  {V}")
    else:
        print("uso: python3 Report/Api.py teste")
