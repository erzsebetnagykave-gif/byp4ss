# Dataset do ByP4ss
# Transforma os findings em dataset JSONL pra treinar o Agent B4S.
# Chamado por Core.Engine.Report: (opcional) Mod.Dataset.Salvar(Resultados)
#
# Formato de cada linha:
#   {"features": [8 floats], "label": str, "recompensa": float,
#    "severidade": str, "alvo": str, "tipo": str,
#    "contexto": {...}, "ts": iso}
#
# As 8 features sao fixas (contrato do B4S):
#   0. porta/65535
#   1. aberta (0/1)
#   2. latencia (0-1, cap 1s)
#   3. confianca (0-1)
#   4. severidade (0-1)
#   5. tempo_rel (0-1, cap 60s)
#   6. tentativas (0-1, cap 5)
#   7. sucesso_anterior (0/1)
#
# Recompensas sao fixas por tipo (Q-Learning ajusta depois).

import os
import json
from datetime import datetime, timezone

from Core.Config import Config
from Core.Log import Log


class Dataset:

    NOME_ARQUIVO = "report.dataset.jsonl"
    N_FEATURES = 8

    RECOMPENSAS = {
        "porta_aberta": 1.0,
        "porta_verificada": 1.0,
        "servico_verificado": 2.0,
        "ssdp_descoberto": 2.0,
        "fingerprint": 3.0,
        "cve_sugerida": 5.0,
        "anomalia_fuzz": 10.0,
        "bypass_upnp": 15.0,
        "bypass_httpauth": 15.0,
        "bypass_telnet": 15.0,
        "bypass_dnsrebind": 15.0,
        "crash": 30.0,
        "exploit_verificado": 100.0,
        "bypass_upnp_falhou": -1.0,
        "bypass_httpauth_falhou": -1.0,
        "bypass_telnet_falhou": -1.0,
        "bypass_dnsrebind_falhou": -1.0,
    }

    SEV_NUMERICO = {
        "info": 0.0, "baixa": 0.25, "media": 0.5, "alta": 0.75, "critica": 1.0,
    }

    TIPOS_ABERTOS = {
        "porta_aberta", "porta_verificada", "servico_verificado",
        "exploit_verificado", "ssdp_descoberto",
    }

    TIPOS_CONFIANCA_ALTA = {"fingerprint", "cve_sugerida"}
    TIPOS_CONFIANCA_MEDIA = {
        "bypass_upnp", "bypass_httpauth", "bypass_telnet", "bypass_dnsrebind",
        "exploit_verificado", "servico_verificado",
    }

    TIPOS_SUCESSO = {
        "bypass_upnp", "bypass_httpauth", "bypass_telnet", "bypass_dnsrebind",
        "exploit_verificado", "crash",
    }

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def Salvar(Resultados, Caminho=None):
        if not isinstance(Resultados, dict):
            return {"ok": False, "motivo": "resultados_invalidos", "n": 0}
        Achados = Dataset._ExtrairAchados(Resultados)
        if not Achados:
            return {"ok": False, "motivo": "sem_achados", "n": 0,
                    "aviso": "arquivo nao alterado (Salvar nao trunca sem achado)"}
        if not Dataset._GarantirDir():
            return {"ok": False, "motivo": "dir_indisponivel", "n": 0}
        Caminho = Caminho or Dataset._Caminho()
        Linhas = Dataset._MontarLinhas(Achados)
        try:
            with open(Caminho, "w", encoding="utf-8") as F:
                for Linha in Linhas:
                    F.write(json.dumps(Linha, ensure_ascii=False) + "\n")
            Tamanho = os.path.getsize(Caminho)
            Log.Info("dataset salvo", {
                "caminho": Caminho, "n": len(Linhas), "bytes": Tamanho,
            })
            return {"ok": True, "caminho": Caminho, "n": len(Linhas),
                    "tamanho_bytes": Tamanho, "formato": "jsonl"}
        except Exception as E:
            Log.Erro("dataset falhou", {"erro": str(E)})
            return {"ok": False, "motivo": f"escrita_falhou:{type(E).__name__}",
                    "erro": str(E), "n": 0}

    @staticmethod
    def Carregar(Caminho=None):
        Caminho = Caminho or Dataset._Caminho()
        if not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "arquivo_nao_encontrado",
                    "features": [], "labels": [], "rewards": [], "n": 0}
        Features = []
        Labels = []
        Rewards = []
        Meta = []
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                for Linha in F:
                    Linha = Linha.strip()
                    if not Linha:
                        continue
                    D = json.loads(Linha)
                    Feats = D.get("features")
                    if not isinstance(Feats, list) or len(Feats) != Dataset.N_FEATURES:
                        continue
                    Features.append(Feats)
                    Labels.append(D.get("label", ""))
                    Rewards.append(float(D.get("recompensa", 0.0)))
                    Meta.append({"alvo": D.get("alvo"), "tipo": D.get("tipo"),
                                 "severidade": D.get("severidade")})
            return {"ok": True, "caminho": Caminho,
                    "features": Features, "labels": Labels,
                    "rewards": Rewards, "meta": Meta,
                    "n": len(Features),
                    "n_features": Dataset.N_FEATURES}
        except Exception as E:
            return {"ok": False, "motivo": f"leitura_falhou:{type(E).__name__}",
                    "erro": str(E), "features": [], "labels": [],
                    "rewards": [], "n": 0}

    @staticmethod
    def Features(Achado, TsReferencia=None):
        if not isinstance(Achado, dict):
            return [0.0] * Dataset.N_FEATURES
        Dados = Achado.get("dados") or {}
        Tipo = Achado.get("tipo", "")
        Porta = Dados.get("porta")
        try:
            PortaInt = int(Porta) if Porta is not None else 0
        except (TypeError, ValueError):
            PortaInt = 0
        F0 = min(max(PortaInt / 65535.0, 0.0), 1.0)
        F1 = 1.0 if Tipo in Dataset.TIPOS_ABERTOS else 0.0
        Latencia = Dados.get("latencia")
        try:
            Lat = float(Latencia) if Latencia is not None else 0.1
        except (TypeError, ValueError):
            Lat = 0.1
        F2 = min(max(Lat, 0.0), 1.0)
        F3 = Dataset._Confianca(Tipo, Dados)
        Sev = Achado.get("severidade", "info")
        F4 = Dataset.SEV_NUMERICO.get(Sev, 0.0)
        F5 = Dataset._TempoRelativo(Achado, TsReferencia)
        Tent = Dados.get("tentativas") or Dados.get("tentativa")
        try:
            TentInt = int(Tent) if Tent is not None else 0
        except (TypeError, ValueError):
            TentInt = 0
        F6 = min(max(TentInt / 5.0, 0.0), 1.0)
        F7 = 1.0 if Dados.get("_sucesso_anterior") else 0.0
        return [round(F, 4) for F in (F0, F1, F2, F3, F4, F5, F6, F7)]

    @staticmethod
    def _Confianca(Tipo, Dados):
        if Tipo in Dataset.TIPOS_CONFIANCA_ALTA:
            return 1.0
        if Tipo in Dataset.TIPOS_CONFIANCA_MEDIA:
            return 0.7
        if Tipo.endswith("_falhou"):
            return 0.3
        return 0.5

    @staticmethod
    def _TempoRelativo(Achado, TsReferencia):
        Ts = Achado.get("timestamp")
        if not Ts or not TsReferencia:
            return 0.0
        try:
            T1 = datetime.fromisoformat(Ts.replace("Z", "+00:00"))
            T0 = datetime.fromisoformat(TsReferencia.replace("Z", "+00:00"))
            Delta = (T1 - T0).total_seconds()
            return min(max(Delta / 60.0, 0.0), 1.0)
        except Exception:
            return 0.0

    @staticmethod
    def Recompensa(Tipo):
        return Dataset.RECOMPENSAS.get(Tipo, 0.0)

    @staticmethod
    def _ExtrairAchados(Resultados):
        if not isinstance(Resultados, dict):
            return []
        F = Resultados.get("findings")
        if isinstance(F, dict):
            return F.get("achados") or []
        if isinstance(F, list):
            return F
        return []

    @staticmethod
    def _MontarLinhas(Achados):
        if not Achados:
            return []
        TsPrimeiro = Achados[0].get("timestamp") if Achados else None
        SucessoAnterior = {}
        Linhas = []
        for A in Achados:
            if not isinstance(A, dict):
                continue
            Alvo = A.get("alvo", "?")
            Dados = dict(A.get("dados") or {})
            Dados["_sucesso_anterior"] = SucessoAnterior.get(Alvo, False)
            AComFlags = dict(A)
            AComFlags["dados"] = Dados
            Feats = Dataset.Features(AComFlags, TsPrimeiro)
            Tipo = A.get("tipo", "")
            Linha = {
                "features": Feats,
                "label": Tipo,
                "recompensa": Dataset.Recompensa(Tipo),
                "severidade": A.get("severidade", "info"),
                "alvo": Alvo,
                "tipo": Tipo,
                "contexto": {K: V for K, V in Dados.items() if not K.startswith("_")},
                "ts": A.get("timestamp", ""),
            }
            Linhas.append(Linha)
            if Tipo in Dataset.TIPOS_SUCESSO:
                SucessoAnterior[Alvo] = True
            elif Tipo.endswith("_falhou"):
                SucessoAnterior[Alvo] = False
        return Linhas

    @staticmethod
    def _GarantirDir():
        try:
            os.makedirs(Config.DirReports, exist_ok=True)
            return True
        except OSError:
            return False

    @staticmethod
    def _Caminho():
        return os.path.join(Config.DirReports, Dataset.NOME_ARQUIVO)

    @staticmethod
    def Info():
        return {
            "nome": "Dataset",
            "n_features": Dataset.N_FEATURES,
            "arquivo": Dataset.NOME_ARQUIVO,
            "recompensas": dict(Dataset.RECOMPENSAS),
            "severidades": dict(Dataset.SEV_NUMERICO),
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
        R = Dataset.Salvar(Resultados)
        print(json.dumps(R, indent=2, ensure_ascii=False))
        if not R["ok"]:
            sys.exit(1)
        C = Dataset.Carregar()
        print()
        print(f"[ok] {C['n']} exemplos, {C['n_features']} features")
        for I, (Feat, Lbl, Rew) in enumerate(zip(C["features"], C["labels"], C["rewards"])):
            print(f"  [{I}] label={Lbl:30s} reward={Rew:+7.2f} features={Feat}")
        print()
        print("=== recompensas por tipo ===")
        for T, R_ in Dataset.RECOMPENSAS.items():
            print(f"  {T:30s} {R_:+7.2f}")
    else:
        print("uso: python3 Report/Dataset.py teste")
