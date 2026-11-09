import sys
import os
import json
import time
import glob
import shutil
import argparse
from datetime import datetime, timezone


class Sessao:

    BASE = os.path.join(os.path.expanduser("~"), ".console", "sessoes")
    SUFIXO = ".json"

    @staticmethod
    def GarantirBase():
        try:
            os.makedirs(Sessao.BASE, mode=0o700, exist_ok=True)
            try:
                os.chmod(Sessao.BASE, 0o700)
            except Exception:
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def CaminhoDe(Nome):
        if not Nome or "/" in Nome or "\\" in Nome or ".." in Nome:
            return None
        if Nome.endswith(Sessao.SUFIXO):
            Nome = Nome[: -len(Sessao.SUFIXO)]
        return os.path.join(Sessao.BASE, Nome + Sessao.SUFIXO)

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def IdadeSegundos(Iso):
        try:
            Quando = datetime.fromisoformat(Iso.replace("Z", "+00:00"))
            Agora = datetime.now(timezone.utc)
            return round((Agora - Quando).total_seconds(), 2)
        except Exception:
            return None

    @staticmethod
    def Salvar(Nome, Estado):
        if not Sessao.GarantirBase():
            return {"ok": False, "motivo": "base_indisponivel"}
        Caminho = Sessao.CaminhoDe(Nome)
        if Caminho is None:
            return {"ok": False, "motivo": f"nome_invalido:{Nome}"}
        Payload = {"nome": Nome, "timestamp": Sessao.Timestamp(), "estado": Estado}
        try:
            with open(Caminho, "w", encoding="utf-8") as F:
                json.dump(Payload, F, ensure_ascii=False, indent=2)
            try:
                os.chmod(Caminho, 0o600)
            except Exception:
                pass
            Tamanho = os.path.getsize(Caminho)
            return {"ok": True, "caminho": Caminho, "tamanho_bytes": Tamanho,
                    "timestamp": Payload["timestamp"]}
        except Exception as E:
            return {"ok": False, "motivo": f"gravacao_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def Carregar(Nome):
        Caminho = Sessao.CaminhoDe(Nome)
        if Caminho is None:
            return {"ok": False, "motivo": f"nome_invalido:{Nome}"}
        if not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "sessao_nao_encontrada"}
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                Payload = json.load(F)
            if not isinstance(Payload, dict):
                return {"ok": False, "motivo": "formato_invalido"}
            Timestamp = Payload.get("timestamp", "")
            return {"ok": True, "nome": Payload.get("nome", Nome),
                    "estado": Payload.get("estado", {}),
                    "timestamp": Timestamp,
                    "idade_segundos": Sessao.IdadeSegundos(Timestamp)}
        except Exception as E:
            return {"ok": False, "motivo": f"leitura_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def Listar():
        if not Sessao.GarantirBase():
            return {"ok": False, "motivo": "base_indisponivel", "sessoes": []}
        Encontradas = []
        try:
            for Caminho in sorted(glob.glob(os.path.join(Sessao.BASE, "*" + Sessao.SUFIXO)),
                                  key=os.path.getmtime, reverse=True):
                try:
                    with open(Caminho, "r", encoding="utf-8") as F:
                        Payload = json.load(F)
                    Nome = Payload.get("nome") or os.path.basename(Caminho)[:-len(Sessao.SUFIXO)]
                    Timestamp = Payload.get("timestamp", "")
                    Encontradas.append({
                        "nome": Nome,
                        "timestamp": Timestamp,
                        "idade_segundos": Sessao.IdadeSegundos(Timestamp),
                        "tamanho_bytes": os.path.getsize(Caminho),
                    })
                except Exception:
                    pass
            return {"ok": True, "sessoes": Encontradas, "total": len(Encontradas)}
        except Exception as E:
            return {"ok": False, "motivo": f"listagem_falhou:{type(E).__name__}",
                    "erro": str(E), "sessoes": []}

    @staticmethod
    def Apagar(Nome):
        Caminho = Sessao.CaminhoDe(Nome)
        if Caminho is None:
            return {"ok": False, "motivo": f"nome_invalido:{Nome}"}
        if not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "sessao_nao_encontrada"}
        try:
            os.remove(Caminho)
            return {"ok": True, "removido": Caminho}
        except Exception as E:
            return {"ok": False, "motivo": f"remocao_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def Exportar(Nome, CaminhoDestino):
        Origem = Sessao.CaminhoDe(Nome)
        if Origem is None:
            return {"ok": False, "motivo": f"nome_invalido:{Nome}"}
        if not os.path.isfile(Origem):
            return {"ok": False, "motivo": "sessao_nao_encontrada"}
        if not CaminhoDestino:
            return {"ok": False, "motivo": "destino_vazio"}
        try:
            shutil.copy2(Origem, CaminhoDestino)
            return {"ok": True, "origem": Origem, "destino": CaminhoDestino,
                    "tamanho_bytes": os.path.getsize(CaminhoDestino)}
        except Exception as E:
            return {"ok": False, "motivo": f"export_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def Importar(CaminhoOrigem, Nome=None):
        if not CaminhoOrigem or not os.path.isfile(CaminhoOrigem):
            return {"ok": False, "motivo": "origem_invalida"}
        if not Sessao.GarantirBase():
            return {"ok": False, "motivo": "base_indisponivel"}
        if Nome is None:
            Nome = datetime.now(timezone.utc).strftime("importada_%Y%m%d_%H%M%S")
        Caminho = Sessao.CaminhoDe(Nome)
        if Caminho is None:
            return {"ok": False, "motivo": f"nome_invalido:{Nome}"}
        try:
            with open(CaminhoOrigem, "r", encoding="utf-8") as F:
                Payload = json.load(F)
            if not isinstance(Payload, dict):
                return {"ok": False, "motivo": "formato_invalido"}
            Payload["nome"] = Nome
            Payload["timestamp"] = Sessao.Timestamp()
            with open(Caminho, "w", encoding="utf-8") as F:
                json.dump(Payload, F, ensure_ascii=False, indent=2)
            try:
                os.chmod(Caminho, 0o600)
            except Exception:
                pass
            return {"ok": True, "nome": Nome, "tamanho_bytes": os.path.getsize(Caminho)}
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def Diferenciar(EstadoAntigo, EstadoAtual):
        if not isinstance(EstadoAntigo, dict) or not isinstance(EstadoAtual, dict):
            return {"ok": False, "motivo": "estados_precisam_ser_dict"}
        ChavesAntigas = set(EstadoAntigo.keys())
        ChavesAtuais = set(EstadoAtual.keys())
        Adicionados = sorted(ChavesAtuais - ChavesAntigas)
        Removidos = sorted(ChavesAntigas - ChavesAtuais)
        Modificados = sorted([K for K in (ChavesAntigas & ChavesAtuais)
                              if EstadoAntigo[K] != EstadoAtual[K]])
        return {"ok": True, "adicionados": Adicionados, "removidos": Removidos,
                "modificados": Modificados, "total_mudancas": len(Adicionados) + len(Removidos) + len(Modificados)}

    @staticmethod
    def Main():
        P = argparse.ArgumentParser(prog="Sessao")
        Sub = P.add_subparsers(dest="cmd")
        Sub.add_parser("list")
        Show = Sub.add_parser("show")
        Show.add_argument("nome")
        Rm = Sub.add_parser("rm")
        Rm.add_argument("nome")
        Exp = Sub.add_parser("export")
        Exp.add_argument("nome")
        Exp.add_argument("destino")
        Imp = Sub.add_parser("import")
        Imp.add_argument("origem")
        Imp.add_argument("--nome", default=None)
        Args = P.parse_args()

        if Args.cmd == "list":
            R = Sessao.Listar()
            if not R.get("ok"):
                print(f"[erro] {R.get('motivo')}", file=sys.stderr)
                return 1
            if not R["sessoes"]:
                print("(nenhuma sessao)")
                return 0
            for S in R["sessoes"]:
                Idade = S.get("idade_segundos")
                IdadeStr = f"{int(Idade)}s atras" if Idade is not None else "?"
                print(f"  {S['nome']}  [{IdadeStr}, {S['tamanho_bytes']}b]")
            return 0
        elif Args.cmd == "show":
            R = Sessao.Carregar(Args.nome)
            if not R.get("ok"):
                print(f"[erro] {R.get('motivo')}", file=sys.stderr)
                return 1
            print(json.dumps(R, indent=2, ensure_ascii=False))
            return 0
        elif Args.cmd == "rm":
            R = Sessao.Apagar(Args.nome)
            print(f"[{'ok' if R.get('ok') else 'erro'}] {R}")
            return 0 if R.get("ok") else 1
        elif Args.cmd == "export":
            R = Sessao.Exportar(Args.nome, Args.destino)
            print(f"[{'ok' if R.get('ok') else 'erro'}] {R}")
            return 0 if R.get("ok") else 1
        elif Args.cmd == "import":
            R = Sessao.Importar(Args.origem, Args.nome)
            print(f"[{'ok' if R.get('ok') else 'erro'}] {R}")
            return 0 if R.get("ok") else 1
        else:
            P.print_help()
            return 2


if __name__ == "__main__":
    raise SystemExit(Sessao.Main())
