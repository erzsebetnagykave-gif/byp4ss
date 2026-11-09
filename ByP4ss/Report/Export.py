# Export do ByP4ss
# Escreve relatorio em JSON / Markdown / CSV em reports/.
# Chamado por Core.Engine.Report: Mod.Export.SalvarJson(Resultados), SalvarMd(Resultados)
#
# Recebe o dict que o Engine.Report ja montou:
#   {"gerado_em", "fases", "resumo", "status"}
# E o Resultados que o Findings montou (opcional, via Resultados["findings"]).

import os
import json
import csv
from datetime import datetime, timezone

from Core.Config import Config
from Core.Constants import Constants
from Core.Log import Log


class Export:

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _GarantirDir():
        try:
            os.makedirs(Config.DirReports, exist_ok=True)
            return True
        except OSError:
            return False

    @staticmethod
    def _Caminho(Nome):
        return os.path.join(Config.DirReports, Nome)

    @staticmethod
    def SalvarJson(Resultados, Caminho=None):
        if not Export._GarantirDir():
            return {"ok": False, "motivo": "dir_indisponivel"}
        Caminho = Caminho or Export._Caminho(Constants.ARQ_EXPORT_JSON)
        try:
            Payload = dict(Resultados) if isinstance(Resultados, dict) else {"resultados": Resultados}
            Payload["_exportado_em"] = Export.Timestamp()
            Payload["_versao"] = Constants.VERSAO
            Payload["_nome"] = Constants.NOME
            with open(Caminho, "w", encoding="utf-8") as F:
                json.dump(Payload, F, ensure_ascii=False, indent=2, default=str)
            Tamanho = os.path.getsize(Caminho)
            Log.Info("export json", {"caminho": Caminho, "bytes": Tamanho})
            return {"ok": True, "caminho": Caminho, "tamanho_bytes": Tamanho,
                    "formato": "json"}
        except Exception as E:
            Log.Erro("export json falhou", {"erro": str(E)})
            return {"ok": False, "motivo": f"escrita_falhou:{type(E).__name__}",
                    "erro": str(E)}

    @staticmethod
    def SalvarMd(Resultados, Caminho=None):
        if not Export._GarantirDir():
            return {"ok": False, "motivo": "dir_indisponivel"}
        Caminho = Caminho or Export._Caminho(Constants.ARQ_EXPORT_MD)
        try:
            Linhas = Export._MontarMd(Resultados)
            Texto = "\n".join(Linhas) + "\n"
            with open(Caminho, "w", encoding="utf-8") as F:
                F.write(Texto)
            Tamanho = os.path.getsize(Caminho)
            Log.Info("export md", {"caminho": Caminho, "bytes": Tamanho})
            return {"ok": True, "caminho": Caminho, "tamanho_bytes": Tamanho,
                    "formato": "md", "linhas": len(Linhas)}
        except Exception as E:
            Log.Erro("export md falhou", {"erro": str(E)})
            return {"ok": False, "motivo": f"escrita_falhou:{type(E).__name__}",
                    "erro": str(E)}

    @staticmethod
    def SalvarCsv(Resultados, Caminho=None):
        if not Export._GarantirDir():
            return {"ok": False, "motivo": "dir_indisponivel"}
        Caminho = Caminho or Export._Caminho(Constants.ARQ_EXPORT_CSV)
        try:
            Achados = Export._Achados(Resultados)
            with open(Caminho, "w", encoding="utf-8", newline="") as F:
                W = csv.writer(F)
                W.writerow(["timestamp", "tipo", "alvo", "severidade",
                            "peso", "descricao"])
                for A in Achados:
                    W.writerow([
                        A.get("timestamp", ""),
                        A.get("tipo", ""),
                        A.get("alvo", ""),
                        A.get("severidade", ""),
                        A.get("peso", 1),
                        A.get("descricao", ""),
                    ])
            Tamanho = os.path.getsize(Caminho)
            Log.Info("export csv", {"caminho": Caminho, "bytes": Tamanho})
            return {"ok": True, "caminho": Caminho, "tamanho_bytes": Tamanho,
                    "formato": "csv", "linhas": len(Achados) + 1}
        except Exception as E:
            Log.Erro("export csv falhou", {"erro": str(E)})
            return {"ok": False, "motivo": f"escrita_falhou:{type(E).__name__}",
                    "erro": str(E)}

    @staticmethod
    def SalvarTudo(Resultados):
        R = {
            "json": Export.SalvarJson(Resultados),
            "md": Export.SalvarMd(Resultados),
            "csv": Export.SalvarCsv(Resultados),
        }
        try:
            from Report.Dataset import Dataset
            R["dataset"] = Dataset.Salvar(Resultados)
        except Exception as E:
            R["dataset"] = {"ok": False, "motivo": f"import_falhou:{type(E).__name__}",
                            "erro": str(E)}
        try:
            from Report.Ambiente import Ambiente
            R["ambiente"] = Ambiente.Salvar(Resultados)
        except Exception as E:
            R["ambiente"] = {"ok": False, "motivo": f"import_falhou:{type(E).__name__}",
                             "erro": str(E)}
        Oks = [K for K, V in R.items() if V.get("ok")]
        return {"ok": len(Oks) == len(R), "formatos": R,
                "total": len(Oks), "esperado": len(R),
                "falharam": [K for K, V in R.items() if not V.get("ok")]}

    @staticmethod
    def _Achados(Resultados):
        if not isinstance(Resultados, dict):
            return []
        F = Resultados.get("findings") or Resultados.get("achados")
        if isinstance(F, dict):
            return F.get("achados") or []
        if isinstance(F, list):
            return F
        return []

    @staticmethod
    def _MontarMd(Resultados):
        L = []
        L.append("# ByP4ss — Relatorio")
        L.append("")
        L.append(f"**Versao:** {Constants.VERSAO}")
        L.append(f"**Gerado em:** {Export.Timestamp()}")
        Gerado = Resultados.get("gerado_em") if isinstance(Resultados, dict) else None
        if Gerado:
            L.append(f"**Sessao:** {Gerado}")
        L.append("")

        Resumo = {}
        if isinstance(Resultados, dict):
            Resumo = Resultados.get("resumo") or {}
        if Resumo:
            L.append("## Resumo")
            L.append("")
            for K, V in Resumo.items():
                L.append(f"- **{K}:** {V}")
            L.append("")

        Findings = Resultados.get("findings") if isinstance(Resultados, dict) else None
        if isinstance(Findings, dict):
            FResumo = Findings.get("resumo") or {}
            if FResumo:
                L.append("## Achados por severidade")
                L.append("")
                PorSev = FResumo.get("por_severidade") or {}
                for Sev in ["critica", "alta", "media", "baixa", "info"]:
                    Qtd = PorSev.get(Sev, 0)
                    if Qtd > 0:
                        L.append(f"- **{Sev}:** {Qtd}")
                L.append("")
                L.append(f"- **peso_total:** {FResumo.get('peso_total', 0)}")
                Max = FResumo.get("max_severidade")
                if Max:
                    L.append(f"- **max_severidade:** {Max}")
                L.append("")
            Achados = Findings.get("achados") or []
            if Achados:
                L.append("## Achados detalhados")
                L.append("")
                L.append("| Severidade | Tipo | Alvo | Descricao |")
                L.append("|---|---|---|---|")
                for A in Achados:
                    Desc = str(A.get("descricao", "")).replace("|", "\\|")
                    L.append(f"| {A.get('severidade', '?')} | "
                             f"{A.get('tipo', '?')} | "
                             f"{A.get('alvo', '?')} | {Desc} |")
                L.append("")

        Fases = {}
        if isinstance(Resultados, dict):
            Fases = Resultados.get("fases") or {}
        if Fases:
            L.append("## Fases executadas")
            L.append("")
            for Fase, Lista in Fases.items():
                Qtd = len(Lista) if isinstance(Lista, list) else 0
                Status = "OK" if Qtd > 0 else "vazio"
                L.append(f"- **{Fase}:** {Qtd} resultado(s) — {Status}")
            L.append("")

        L.append("---")
        L.append("")
        L.append(f"_Gerado por ByP4ss {Constants.VERSAO} — {Constants.AUTOR}_")
        return L

    @staticmethod
    def Info():
        return {
            "nome": "Export",
            "formatos": ["json", "md", "csv"],
            "dir": Config.DirReports,
            "arquivos": {
                "json": Constants.ARQ_EXPORT_JSON,
                "md": Constants.ARQ_EXPORT_MD,
                "csv": Constants.ARQ_EXPORT_CSV,
            },
        }


if __name__ == "__main__":
    import json as J
    Fake = {
        "gerado_em": Export.Timestamp(),
        "fases": {"discover": [1, 2, 3], "bypass": [1], "verify": [1, 2]},
        "resumo": {"encontrados": 3, "erros": 0, "alertas": 1},
        "status": "OK",
        "findings": {
            "achados": [
                {"tipo": "porta_aberta", "alvo": "127.0.0.1",
                 "severidade": "info", "peso": 1,
                 "descricao": "porta 80 aberta (http)",
                 "timestamp": Export.Timestamp()},
                {"tipo": "cve_sugerida", "alvo": "127.0.0.1",
                 "severidade": "critica", "peso": 10,
                 "descricao": "CVE-2023-1389: command injection",
                 "timestamp": Export.Timestamp()},
                {"tipo": "exploit_verificado", "alvo": "127.0.0.1",
                 "severidade": "critica", "peso": 10,
                 "descricao": "exploit em 4444 confirmado",
                 "timestamp": Export.Timestamp()},
            ],
            "resumo": {
                "total": 3,
                "por_severidade": {"info": 1, "critica": 2,
                                    "baixa": 0, "media": 0, "alta": 0},
                "peso_total": 21,
                "max_severidade": "critica",
            },
        },
    }
    R = Export.SalvarTudo(Fake)
    print(J.dumps(R, indent=2, ensure_ascii=False))
    assert R["ok"], R
    print()
    print(f"[ok] {R['total']}/3 formatos salvos")
    for Fmt, Info in R["formatos"].items():
        print(f"  {Fmt}: {Info.get('caminho')} ({Info.get('tamanho_bytes')} bytes)")
