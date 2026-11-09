import sys
import os
import json
import time
import argparse
import importlib
import inspect
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class RegistroComandos:

    COMANDOS = {
        "scan": {
            "descricao": "Port scan + SSDP num alvo",
            "argumentos": {"alvo": "str (obrigatorio)", "portas": "list[int] (opcional)", "threads": "int (opcional, default 10)"},
            "metodo": ("Core.Engine", "Engine", "Scan", {}),
            "grupo": "discovery",
        },
        "ssdp": {
            "descricao": "Descobre UPnP via SSDP",
            "argumentos": {"alvo": "str (obrigatorio)"},
            "metodo": ("Discovery.Ssdp", "Ssdp", "Descobrir", {}),
            "grupo": "discovery",
        },
        "upnp": {
            "descricao": "AddPortMapping via UPnP bypass",
            "argumentos": {"alvo": "str (obrigatorio)", "porta": "int (opcional, default 23)"},
            "metodo": ("Bypass.UpnpBypass", "UpnpBypass", "Tentar", {}),
            "grupo": "bypass",
        },
        "httpauth": {
            "descricao": "Path traversal em auth HTTP",
            "argumentos": {"alvo": "str (obrigatorio)", "caminho": "str (opcional, default /admin)"},
            "metodo": ("Bypass.HttpAuth", "HttpAuth", "TestarTraversal", {}),
            "grupo": "bypass",
        },
        "cred": {
            "descricao": "Busca credenciais do alvo no YAML",
            "argumentos": {"alvo": "str (obrigatorio)"},
            "metodo": ("Core.Engine", "Engine", "Credenciais", {}),
            "grupo": "analise",
        },
        "analise": {
            "descricao": "Scan consolidado: portas + SSDP + fabricante + CVEs sugeridas",
            "argumentos": {"alvo": "str (obrigatorio)", "portas": "list[int] (opcional)", "threads": "int (opcional, default 10)"},
            "metodo": ("Analise", "Analise", "EscanearAlvo", {}),
            "grupo": "analise",
        },
        "exploit tplink": {
            "descricao": "Roda exploit do TP-Link CVE-2023-1389",
            "argumentos": {"alvo": "str (obrigatorio)", "modo": "str (opcional)", "local": "str (opcional)", "porta": "int (opcional)"},
            "metodo": ("Core.Engine", "Engine", "Exploit", {"id": "tplink"}),
            "grupo": "exploits",
        },
        "exploit dlink": {
            "descricao": "Roda exploit do D-Link CVE-2024-3273",
            "argumentos": {"alvo": "str (obrigatorio)", "modo": "str (opcional)", "local": "str (opcional)", "porta": "int (opcional)"},
            "metodo": ("Core.Engine", "Engine", "Exploit", {"id": "dlink"}),
            "grupo": "exploits",
        },
        "exploit tenda7795": {
            "descricao": "Roda exploit do Tenda CVE-2025-7795 (DoS)",
            "argumentos": {"alvo": "str (obrigatorio)", "modo": "str (opcional)", "porta": "int (opcional)"},
            "metodo": ("Core.Engine", "Engine", "Exploit", {"id": "tenda7795"}),
            "grupo": "exploits",
        },
        "exploit arcadyan": {
            "descricao": "Roda exploit do Arcadyan CVE-2021-20090",
            "argumentos": {"alvo": "str (obrigatorio)", "modo": "str (opcional)", "local": "str (opcional)", "porta": "int (opcional)"},
            "metodo": ("Core.Engine", "Engine", "Exploit", {"id": "arcadyan"}),
            "grupo": "exploits",
        },
        "exploit iptime": {
            "descricao": "Roda exploit do ipTIME CVE-2025-55423",
            "argumentos": {"alvo": "str (obrigatorio)", "modo": "str (opcional)", "local": "str (opcional)", "porta": "int (opcional)"},
            "metodo": ("Core.Engine", "Engine", "Exploit", {"id": "iptime"}),
            "grupo": "exploits",
        },
        "exploit tenda29384": {
            "descricao": "Roda exploit do Tenda CVE-2025-29384 (MIPS overflow)",
            "argumentos": {"alvo": "str (obrigatorio)", "modo": "str (opcional)", "local": "str (opcional)", "cpu": "str (opcional)", "encoder": "str (opcional)"},
            "metodo": ("Core.Engine", "Engine", "Exploit", {"id": "tenda29384"}),
            "grupo": "exploits",
        },
        "shell reverse": {
            "descricao": "Abre reverse shell TCP contra um host local",
            "argumentos": {"host": "str (obrigatorio)", "porta": "int (obrigatorio)"},
            "metodo": ("ExploitByp4ss.Aux1l14r3s.Shells.ReverseShell", "ReverseShell", "Tcp", {}),
            "grupo": "shells",
        },
        "shell bind": {
            "descricao": "Abre bind shell TCP numa porta",
            "argumentos": {"porta": "int (opcional, default 4444)", "senha": "str (opcional)"},
            "metodo": ("ExploitByp4ss.Aux1l14r3s.Shells.BindShell", "BindShell", "Tcp", {}),
            "grupo": "shells",
        },
        "servidor ssdp": {
            "descricao": "Sobe servidor SSDP falso",
            "argumentos": {"interface": "str (opcional)", "porta": "int (opcional, default 1900)"},
            "metodo": ("ExploitByp4ss.Aux1l14r3s.Servers.SsdpFalso", "SsdpFalso", "IniciarSsdp", {}),
            "grupo": "servers",
        },
        "servidor http": {
            "descricao": "Sobe servidor HTTP falso",
            "argumentos": {"interface": "str (opcional)", "porta": "int (opcional, default 8080)"},
            "metodo": ("ExploitByp4ss.Aux1l14r3s.Servers.SsdpFalso", "SsdpFalso", "IniciarHttp", {}),
            "grupo": "servers",
        },
        "scanner cgi": {
            "descricao": "Escanear endpoints CGI do alvo",
            "argumentos": {"alvo": "str (obrigatorio)", "esquema": "str (opcional)", "porta": "int (opcional)"},
            "metodo": ("ExploitByp4ss.Aux1l14r3s.Scanners.CgiScanner", "CgiScanner", "Escanear", {}),
            "grupo": "scanners",
        },
        "scanner path": {
            "descricao": "Escanear paths + traversal do alvo",
            "argumentos": {"alvo": "str (obrigatorio)", "esquema": "str (opcional)", "porta": "int (opcional)", "threads": "int (opcional)"},
            "metodo": ("ExploitByp4ss.Aux1l14r3s.Scanners.PathScanner", "PathScanner", "Escanear", {}),
            "grupo": "scanners",
        },
    }

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _Importar(Caminho, Classe):
        try:
            M = importlib.import_module(Caminho)
            return getattr(M, Classe, None)
        except Exception:
            return None

    @staticmethod
    def Listar(Grupo=None):
        Itens = []
        for Nome, Info in sorted(RegistroComandos.COMANDOS.items()):
            if Grupo and Info.get("grupo") != Grupo:
                continue
            Itens.append({"nome": Nome, "descricao": Info["descricao"],
                          "argumentos": Info["argumentos"], "grupo": Info["grupo"]})
        return {"ok": True, "comandos": Itens, "total": len(Itens), "grupo": Grupo}

    @staticmethod
    def Buscar(Nome):
        Info = RegistroComandos.COMANDOS.get(Nome)
        if not Info:
            return {"ok": False, "motivo": f"comando_nao_encontrado:{Nome}"}
        return {"ok": True, "nome": Nome, "descricao": Info["descricao"],
                "argumentos": Info["argumentos"], "grupo": Info["grupo"],
                "metodo_real": Info["metodo"]}

    @staticmethod
    def _NormalizarArgs(Funcao, Args):
        try:
            Parametros = inspect.signature(Funcao).parameters
        except Exception:
            return dict(Args)
        Aceitos = set(Parametros.keys())
        Normalizados = {}
        for K, V in Args.items():
            if K in Aceitos:
                Normalizados[K] = V
            elif K and K[0].islower() and (K[0].upper() + K[1:]) in Aceitos:
                Normalizados[K[0].upper() + K[1:]] = V
        return Normalizados

    @staticmethod
    def Executar(Nome, Args=None):
        Args = Args or {}
        Info = RegistroComandos.COMANDOS.get(Nome)
        if not Info:
            return {"ok": False, "nome": Nome, "motivo": f"comando_nao_encontrado:{Nome}"}
        Caminho, Classe, Metodo, Fixos = Info["metodo"]
        Inicio = time.monotonic()
        Cls = RegistroComandos._Importar(Caminho, Classe)
        if Cls is None:
            return {"ok": False, "nome": Nome,
                    "motivo": f"modulo_indisponivel:{Caminho}.{Classe}",
                    "tempo_ms": round((time.monotonic() - Inicio) * 1000.0, 2)}
        Funcao = getattr(Cls, Metodo, None)
        if Funcao is None:
            return {"ok": False, "nome": Nome,
                    "motivo": f"metodo_indisponivel:{Metodo}",
                    "tempo_ms": round((time.monotonic() - Inicio) * 1000.0, 2)}
        Argumentos = {**Fixos, **Args}
        AlvoExtraido = Argumentos.pop("alvo", None)
        AlvoExtraido = Argumentos.pop("Alvo", AlvoExtraido)
        IdExtraido = Argumentos.pop("id", None)
        ArgsNormalizados = RegistroComandos._NormalizarArgs(Funcao, Argumentos)
        try:
            if IdExtraido is not None and AlvoExtraido is not None:
                Resultado = Funcao(IdExtraido, AlvoExtraido, **ArgsNormalizados)
            elif AlvoExtraido is not None:
                Resultado = Funcao(AlvoExtraido, **ArgsNormalizados)
            else:
                Resultado = Funcao(**ArgsNormalizados)
        except TypeError as E:
            return {"ok": False, "nome": Nome, "motivo": f"assinatura_incompativel",
                    "erro": str(E),
                    "tempo_ms": round((time.monotonic() - Inicio) * 1000.0, 2)}
        except Exception as E:
            return {"ok": False, "nome": Nome, "motivo": f"excecao:{type(E).__name__}",
                    "erro": str(E),
                    "tempo_ms": round((time.monotonic() - Inicio) * 1000.0, 2)}
        Ok = bool(Resultado.get("ok")) if isinstance(Resultado, dict) else bool(Resultado)
        return {"ok": Ok, "nome": Nome, "resultado": Resultado,
                "tempo_ms": round((time.monotonic() - Inicio) * 1000.0, 2),
                "timestamp": RegistroComandos.Timestamp()}

    @staticmethod
    def Ajuda(Nome=None):
        if Nome:
            Info = RegistroComandos.COMANDOS.get(Nome)
            if not Info:
                return {"ok": False, "motivo": f"comando_nao_encontrado:{Nome}"}
            Linhas = [f"comando: {Nome}", f"descricao: {Info['descricao']}",
                      f"grupo: {Info['grupo']}", "argumentos:"]
            for Arg, Desc in Info["argumentos"].items():
                Linhas.append(f"  {Arg}: {Desc}")
            return {"ok": True, "texto": "\n".join(Linhas)}
        Grupos = {}
        for Nome, Info in sorted(RegistroComandos.COMANDOS.items()):
            Grupos.setdefault(Info["grupo"], []).append(Nome)
        Linhas = ["comandos disponiveis (por grupo):"]
        for G in sorted(Grupos.keys()):
            Linhas.append(f"  [{G}]")
            for C in Grupos[G]:
                Linhas.append(f"    {C}")
        return {"ok": True, "texto": "\n".join(Linhas)}

    @staticmethod
    def Main():
        P = argparse.ArgumentParser(prog="RegistroComandos")
        Sub = P.add_subparsers(dest="cmd")
        L = Sub.add_parser("list")
        L.add_argument("--grupo", default=None)
        L.add_argument("--json", action="store_true")
        S = Sub.add_parser("show")
        S.add_argument("nome")
        R = Sub.add_parser("run")
        R.add_argument("nome")
        R.add_argument("args", nargs="*", help="key=value ...")
        R.add_argument("--json", action="store_true")
        H = Sub.add_parser("help")
        H.add_argument("nome", nargs="?", default=None)
        Args = P.parse_args()

        if Args.cmd == "list":
            Res = RegistroComandos.Listar(Args.grupo)
            if Args.json:
                print(json.dumps(Res, indent=2, ensure_ascii=False))
            else:
                for C in Res["comandos"]:
                    print(f"  [{C['grupo']}] {C['nome']:22s} {C['descricao']}")
            return 0
        elif Args.cmd == "show":
            Res = RegistroComandos.Buscar(Args.nome)
            print(json.dumps(Res, indent=2, ensure_ascii=False))
            return 0 if Res.get("ok") else 1
        elif Args.cmd == "run":
            Argumentos = {}
            for Par in Args.args:
                if "=" in Par:
                    K, V = Par.split("=", 1)
                    try:
                        Argumentos[K] = json.loads(V)
                    except Exception:
                        Argumentos[K] = V
            Res = RegistroComandos.Executar(Args.nome, Argumentos)
            if Args.json:
                print(json.dumps(Res, indent=2, ensure_ascii=False))
            else:
                print(f"[{'ok' if Res.get('ok') else 'erro'}] {Res.get('nome')} "
                      f"({Res.get('tempo_ms')}ms)")
                if not Res.get("ok"):
                    print(f"  motivo: {Res.get('motivo')}  erro: {Res.get('erro')}")
                else:
                    print(f"  resultado: {json.dumps(Res.get('resultado'), ensure_ascii=False)[:500]}")
            return 0 if Res.get("ok") else 1
        elif Args.cmd == "help":
            Res = RegistroComandos.Ajuda(Args.nome)
            print(Res.get("texto", Res.get("motivo")))
            return 0 if Res.get("ok") else 1
        else:
            P.print_help()
            return 2


if __name__ == "__main__":
    raise SystemExit(RegistroComandos.Main())
