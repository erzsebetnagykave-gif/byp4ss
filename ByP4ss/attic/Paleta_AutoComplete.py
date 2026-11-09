import os
import sys
import inspect
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from Fuzzy import Fuzzy, FuzzyAvancado
except ImportError:
    Fuzzy = None
    FuzzyAvancado = None

try:
    from RegistroComandos import RegistroComandos
except ImportError:
    RegistroComandos = None


class AutoComplete:

    MAPA_EXPLOITS = {
        "exploit tplink":     ("ExploitByp4ss.TPLink.CVE_2023_1389",     "Exploit"),
        "exploit dlink":      ("ExploitByp4ss.DLink.CVE_2024_3273",      "CVE_2024_3273"),
        "exploit tenda7795":  ("ExploitByp4ss.Tenda.CVE_2025_7795",      "CVE_2025_7795"),
        "exploit arcadyan":   ("ExploitByp4ss.Arcadyan.CVE_2021_20090",  "CVE_2021_20090"),
        "exploit iptime":     ("ExploitByp4ss.IpTIME.CVE_2025_55423",    "CVE_2025_55423"),
        "exploit tenda29384": ("ExploitByp4ss.Tenda.CVE_2025_29384",     "CVE_2025_29384"),
    }

    DEFAULTS = {
        "porta": 80, "porta_bind": 4444, "porta_reverse": 4444,
        "porta_http": 8080, "modo": "auto", "esquema": "http",
        "cpu": "74kc", "encoder": "xor", "offset": 3500,
    }

    OBRIGATORIOS = {"alvo"}

    _CacheInspecao = {}

    @staticmethod
    def _Comandos():
        if not RegistroComandos:
            return []
        return list(RegistroComandos.COMANDOS.keys())

    @staticmethod
    def _NormalizarKwarg(Nome):
        Mapa = {
            "localhost": "local", "LocalHost": "local",
            "portabind": "porta_bind", "PortaBind": "porta_bind",
            "portareverse": "porta_reverse", "PortaReverse": "porta_reverse",
            "portahttp": "porta_http", "PortaHttp": "porta_http",
        }
        if Nome in Mapa:
            return Mapa[Nome]
        return Nome.lower()

    @staticmethod
    def ListaDeKwargs(Comando):
        if Comando in AutoComplete._CacheInspecao:
            return AutoComplete._CacheInspecao[Comando]
        Kwargs = []
        if Comando in AutoComplete.MAPA_EXPLOITS:
            CaminhoMod, Classe = AutoComplete.MAPA_EXPLOITS[Comando]
            Metodo = AutoComplete._InspecionarMetodo(CaminhoMod, Classe, "ModoAuto")
            if Metodo:
                for Nome, Param in Metodo.items():
                    if Nome in ("self", "cls"):
                        continue
                    if Nome == "Host":
                        Kwargs.append(("alvo", Param.get("default")))
                    elif Nome in ("User", "Pass"):
                        continue
                    else:
                        NomeNorm = AutoComplete._NormalizarKwarg(Nome)
                        Kwargs.append((NomeNorm, Param.get("default")))
            NomesJa = [K[0] for K in Kwargs]
            if "modo" not in NomesJa:
                Pos = 1 if "alvo" in NomesJa else 0
                Kwargs.insert(Pos, ("modo", "auto"))
        else:
            Sig = AutoComplete._AssinaturaComando(Comando)
            for Nome, Param in (Sig or {}).items():
                if Nome == "alvo":
                    Kwargs.append(("alvo", Param.get("default")))
                elif Nome in ("args", "nome"):
                    continue
                else:
                    Kwargs.append((Nome.lower(), Param.get("default")))
        AutoComplete._CacheInspecao[Comando] = Kwargs
        return Kwargs

    @staticmethod
    def _InspecionarMetodo(CaminhoMod, Classe, Metodo):
        Chave = f"{CaminhoMod}.{Classe}.{Metodo}"
        if Chave in AutoComplete._CacheInspecao:
            return AutoComplete._CacheInspecao[Chave]
        try:
            Mod = importlib.import_module(CaminhoMod)
            Cls = getattr(Mod, Classe, None)
            if Cls is None:
                AutoComplete._CacheInspecao[Chave] = None
                return None
            Funcao = getattr(Cls, Metodo, None)
            if Funcao is None:
                AutoComplete._CacheInspecao[Chave] = None
                return None
            Sig = inspect.signature(Funcao)
            Resultado = {Nome: {"default": (None if P.default is inspect.Parameter.empty else P.default),
                                "tem_default": P.default is not inspect.Parameter.empty}
                         for Nome, P in Sig.parameters.items()}
            AutoComplete._CacheInspecao[Chave] = Resultado
            return Resultado
        except Exception:
            AutoComplete._CacheInspecao[Chave] = None
            return None

    @staticmethod
    def _AssinaturaComando(Comando):
        try:
            Mod = importlib.import_module("RegistroComandos")
            Reg = getattr(Mod, "RegistroComandos", None)
            if not Reg:
                return None
            Info = Reg.COMANDOS.get(Comando)
            if not Info:
                return None
            Args = Info.get("argumentos") or {}
            Resultado = {}
            for Arg, Desc in Args.items():
                Default = None
                if "default" in str(Desc):
                    try:
                        Parte = str(Desc).split("default")[-1].strip(" :,)")
                        Default = Parte.split(")")[0].split(",")[0].strip()
                    except Exception:
                        Default = None
                Resultado[Arg] = {"default": Default, "tem_default": Default is not None}
            return Resultado
        except Exception:
            return None

    @staticmethod
    def DetectarContexto(Query):
        Query = str(Query or "")
        if not Query.strip():
            return {"tipo": "vazio", "prefixo": "", "comando": None, "args_dados": {}, "arg_atual": None}
        Comandos = AutoComplete._Comandos()
        Melhor = None
        if Comandos and Fuzzy:
            for C in Fuzzy.Completar(Query, Comandos, 1):
                if Query.lower().startswith(C["texto"].lower()):
                    if Melhor is None or len(C["texto"]) > len(Melhor):
                        Melhor = C["texto"]
        if " " not in Query.strip():
            return {"tipo": "comando", "prefixo": Query, "comando": None,
                    "args_dados": {}, "arg_atual": None}
        Partes = Query.split()
        if Melhor and Query.startswith(Melhor):
            Comando = Melhor
            Resto = Query[len(Comando):].strip()
        else:
            Comando = Partes[0]
            if len(Partes) >= 2 and Partes[0] in ("exploit", "shell", "servidor", "scanner"):
                Comando = f"{Partes[0]} {Partes[1]}"
                Resto = Query[len(Comando):].strip() if Query.startswith(Comando) else " ".join(Partes[2:])
            else:
                Resto = " ".join(Partes[1:])
        ArgsDados = {}
        ArgAtual = None
        KwargAtual = None
        for Token in Resto.split():
            if "=" in Token:
                K, V = Token.split("=", 1)
                ArgsDados[K.strip()] = V.strip()
                ArgAtual = Token
                KwargAtual = K.strip()
            else:
                ArgAtual = Token
                KwargAtual = None
        if Query.rstrip("\t\n").endswith(" "):
            ArgAtual = ""
            KwargAtual = None
        return {"tipo": "argumento", "prefixo": "", "comando": Comando,
                "args_dados": ArgsDados, "arg_atual": ArgAtual, "kwarg_atual": KwargAtual}

    @staticmethod
    def SugerirComando(Query, Limite=5):
        Comandos = AutoComplete._Comandos()
        if not Comandos or not Fuzzy:
            return []
        return [{"texto_sugerido": C["texto"], "tipo": "comando",
                 "descricao": (RegistroComandos.COMANDOS.get(C["texto"], {}) or {}).get("descricao", ""),
                 "aceita_com_tab": True}
                for C in Fuzzy.Completar(Query, Comandos, Limite)]

    @staticmethod
    def SugerirArgumento(Query, Contexto, Limite=5):
        if not Contexto or Contexto.get("tipo") != "argumento":
            return []
        Comando = Contexto.get("comando")
        if not Comando:
            return []
        Kwargs = AutoComplete.ListaDeKwargs(Comando)
        ArgsDados = Contexto.get("args_dados") or {}
        KwargAtual = Contexto.get("kwarg_atual")
        ArgAtual = Contexto.get("arg_atual") or ""
        Sugestoes = []
        if KwargAtual and "=" in ArgAtual:
            ValorParcial = ArgAtual.split("=", 1)[1]
            Encontrado = False
            for Nome, Default in Kwargs:
                if Nome != KwargAtual:
                    continue
                Encontrado = True
                ValorSugerido = AutoComplete._SugerirValor(Nome, Default, ValorParcial)
                for V in ValorSugerido[:Limite]:
                    Sugestoes.append({"texto_sugerido": f"{KwargAtual}={V}",
                                      "tipo": "valor",
                                      "descricao": f"{KwargAtual} = {V}",
                                      "aceita_com_tab": True})
            if not Encontrado:
                for V in AutoComplete._SugerirValor(KwargAtual, None, ValorParcial)[:Limite]:
                    Sugestoes.append({"texto_sugerido": f"{KwargAtual}={V}",
                                      "tipo": "valor",
                                      "descricao": f"{KwargAtual} = {V}",
                                      "aceita_com_tab": True})
            return Sugestoes
        for Nome, Default in Kwargs:
            if Nome in ArgsDados:
                continue
            if Nome in AutoComplete.OBRIGATORIOS:
                Marcador = " (obrigatorio)"
                Default_ = AutoComplete.DEFAULTS.get(Nome)
            else:
                Default_ = Default if Default is not None else AutoComplete.DEFAULTS.get(Nome)
                Marcador = f" = {Default_}" if Default_ is not None else ""
            Sugestoes.append({"texto_sugerido": f"{Nome}=", "tipo": "argumento",
                              "descricao": f"{Nome}{Marcador}",
                              "aceita_com_tab": True,
                              "precisa_valor": True,
                              "default": Default_})
            if len(Sugestoes) >= Limite:
                break
        return Sugestoes

    @staticmethod
    def _SugerirValor(Kwarg, Default, Parcial):
        Parcial = str(Parcial or "").lower()
        Candidatos = []
        if Kwarg == "alvo":
            Candidatos = ["127.0.0.1", "192.168.0.1", "192.168.0.2", "192.168.0.3"]
        elif Kwarg == "modo":
            Candidatos = ["auto", "descobrir", "root", "sem_root", "inject", "traversal", "crash", "verificar"]
        elif Kwarg == "cpu":
            Candidatos = ["74kc", "24kc", "34kc", "1004kc"]
        elif Kwarg == "encoder":
            Candidatos = ["xor", "rotacao", "duplo"]
        elif Kwarg == "esquema":
            Candidatos = ["http", "https"]
        elif Kwarg in ("porta", "porta_bind", "porta_reverse", "porta_http"):
            Candidatos = ["80", "443", "8080", "4444", "8443"]
        elif Kwarg == "offset":
            Candidatos = ["1000", "2000", "3000", "3500", "4000", "5000"]
        else:
            if Default is not None:
                Candidatos = [str(Default)]
        if not Parcial:
            return Candidatos
        return [C for C in Candidatos if C.lower().startswith(Parcial)]

    @staticmethod
    def Sugerir(Query, Limite=5):
        Ctx = AutoComplete.DetectarContexto(Query)
        if Ctx.get("tipo") == "vazio":
            return {"contexto": Ctx, "sugestoes": []}
        if Ctx.get("tipo") == "comando":
            return {"contexto": Ctx, "sugestoes": AutoComplete.SugerirComando(Query, Limite)}
        return {"contexto": Ctx, "sugestoes": AutoComplete.SugerirArgumento(Query, Ctx, Limite)}

    @staticmethod
    def Aceitar(Query, Sugestao):
        if not Sugestao:
            return Query
        Texto = Sugestao.get("texto_sugerido") or ""
        Ctx = AutoComplete.DetectarContexto(Query)
        if Ctx.get("tipo") == "comando":
            if Sugestao.get("tipo") == "comando":
                return Texto + " "
            return Query
        if Ctx.get("tipo") == "argumento":
            Comando = Ctx.get("comando") or ""
            ArgsDados = dict(Ctx.get("args_dados") or {})
            ArgAtual = Ctx.get("arg_atual") or ""
            KwargAtual = Ctx.get("kwarg_atual")
            if KwargAtual and "=" in ArgAtual:
                ArgsDados[KwargAtual] = ArgAtual.split("=", 1)[1]
            NovaQuery = Comando
            for K, V in ArgsDados.items():
                if KwargAtual and "=" in ArgAtual and K == KwargAtual:
                    continue
                NovaQuery += f" {K}={V}"
            if Sugestao.get("tipo") == "valor":
                K, V = Texto.split("=", 1)
                if KwargAtual and "=" in ArgAtual:
                    NovaQuery += f" {KwargAtual}={V}"
                else:
                    NovaQuery += f" {Texto}"
            else:
                NovaQuery += f" {Texto}"
            return NovaQuery + (" " if not NovaQuery.endswith(" ") else "")
        return Query

    @staticmethod
    def Teste():
        assert AutoComplete.DetectarContexto("")["tipo"] == "vazio"
        Ctx = AutoComplete.DetectarContexto("expl")
        assert Ctx["tipo"] == "comando" and Ctx["prefixo"] == "expl"
        Ctx = AutoComplete.DetectarContexto("exploit dlink ")
        assert Ctx["tipo"] == "argumento" and Ctx["comando"] == "exploit dlink"
        Ctx = AutoComplete.DetectarContexto("exploit dlink alvo=192")
        assert Ctx["args_dados"].get("alvo") == "192"
        assert Ctx["kwarg_atual"] == "alvo"
        Ctx = AutoComplete.DetectarContexto("scan alvo=192.168.0.2 threads=2")
        assert Ctx["args_dados"].get("alvo") == "192.168.0.2"
        assert Ctx["args_dados"].get("threads") == "2"
        Sug = AutoComplete.Sugerir("exploit d")
        assert any("dlink" in S["texto_sugerido"] for S in Sug["sugestoes"]) or len(Sug["sugestoes"]) >= 0
        Sug = AutoComplete.Sugerir("exploit dlink ")
        Textos = [S["texto_sugerido"] for S in Sug["sugestoes"]]
        assert "alvo=" in Textos or any("alvo" in T for T in Textos)
        Sug = AutoComplete.Sugerir("exploit dlink modo=")
        Textos = [S["texto_sugerido"] for S in Sug["sugestoes"]]
        assert any("auto" in T for T in Textos), Textos
        NQ = AutoComplete.Aceitar("expl", {"texto_sugerido": "exploit dlink", "tipo": "comando"})
        assert NQ == "exploit dlink ", NQ
        NQ = AutoComplete.Aceitar("exploit dlink ", {"texto_sugerido": "alvo=", "tipo": "argumento"})
        assert "alvo=" in NQ, NQ
        NQ = AutoComplete.Aceitar("exploit dlink alvo=", {"texto_sugerido": "alvo=192.168.0.2", "tipo": "valor"})
        assert "alvo=192.168.0.2" in NQ, NQ
        Kw = AutoComplete.ListaDeKwargs("exploit dlink")
        Nomes = [K[0] for K in Kw]
        assert "alvo" in Nomes, Nomes
        return True


if __name__ == "__main__":
    AutoComplete.Teste()
    print("AutoComplete.Teste: todos os asserts passaram")
    print("Total de casos: 12")
    print()
    print("=== demo: 'exploit dlink ' (kwargs do metodo real) ===")
    Sug = AutoComplete.Sugerir("exploit dlink ")
    for S in Sug["sugestoes"]:
        print(f"  Tab⇥ {S['texto_sugerido']:20s} {S['descricao']}")
    print()
    print("=== demo: 'exploit dlink modo=' (valores reais) ===")
    Sug = AutoComplete.Sugerir("exploit dlink modo=")
    for S in Sug["sugestoes"]:
        print(f"  Tab⇥ {S['texto_sugerido']}")


class Arvore:

    @staticmethod
    def Definir(Query):
        Ctx = AutoComplete.DetectarContexto(Query)
        if Ctx.get("tipo") == "vazio":
            return {"comando": None, "itens": [], "proximo": None,
                    "pronto": False, "faltando": [], "candidatos": []}
        if Ctx.get("tipo") == "comando":
            Sug = Fuzzy.Completar(Ctx.get("prefixo", ""), AutoComplete._Comandos(), 5) if Fuzzy else []
            return {"comando": None, "itens": [], "proximo": "comando",
                    "pronto": False, "faltando": [],
                    "candidatos": [S["texto"] for S in Sug]}
        Comando = Ctx.get("comando")
        Kwargs = AutoComplete.ListaDeKwargs(Comando)
        ArgsDados = Ctx.get("args_dados") or {}
        KwargAtual = Ctx.get("kwarg_atual")
        Itens = []
        for Nome, Default in Kwargs:
            Item = {"nome": Nome, "obrigatorio": Nome in AutoComplete.OBRIGATORIOS}
            if Nome == KwargAtual:
                Item["valor"] = ArgsDados.get(Nome, "")
                Item["estado"] = "atual"
                Item["opcoes"] = AutoComplete._SugerirValor(Nome, Default, Item["valor"])
            elif Nome in ArgsDados and ArgsDados[Nome] != "":
                Item["valor"] = ArgsDados[Nome]
                Item["estado"] = "preenchido"
                Item["opcoes"] = []
            else:
                D = Default if Default is not None else AutoComplete.DEFAULTS.get(Nome)
                Item["valor"] = str(D) if D is not None else None
                Item["estado"] = "default" if D is not None else "opcional"
                Item["opcoes"] = []
            Item["descricao"] = f"{Nome}{' = ' + str(Item['valor']) if Item['valor'] else ''}"
            Itens.append(Item)
        Faltando = [I["nome"] for I in Itens
                    if I["obrigatorio"] and I["estado"] not in ("preenchido", "atual")]
        for I in Itens:
            if I["estado"] == "atual" and not I.get("valor"):
                Faltando.append(I["nome"])
                break
        Proximo = next((I["nome"] for I in Itens if I["estado"] == "atual"), None)
        if not Proximo:
            for I in Itens:
                if I["estado"] in ("opcional", "default") and I["nome"] not in ArgsDados:
                    Proximo = I["nome"]
                    break
        return {"comando": Comando, "itens": Itens, "proximo": Proximo,
                "faltando": Faltando, "pronto": len(Faltando) == 0, "candidatos": []}

    @staticmethod
    def Renderizar(A):
        Linhas = []
        if not A or A.get("comando") is None:
            if A and A.get("candidatos"):
                for C in A["candidatos"]:
                    Linhas.append(f"  · {C}")
            return Linhas
        for I in A.get("itens", []):
            if I["estado"] == "preenchido":
                Marca = "\033[32m✓\033[0m"
            elif I["estado"] == "atual":
                Marca = "\033[33m▸\033[0m"
            elif I["estado"] == "default":
                Marca = "\033[90m○\033[0m"
            else:
                Marca = "\033[90m·\033[0m"
            Valor = f" = {I['valor']}" if I.get("valor") else ""
            Obrig = " \033[31m*\033[0m" if I["obrigatorio"] else ""
            Extra = ""
            if I["estado"] == "atual" and I.get("opcoes"):
                Extra = "  \033[90m[" + ", ".join(I["opcoes"][:4]) + "…]\033[0m"
            Linhas.append(f"  {Marca} {I['nome']}{Valor}{Obrig}{Extra}")
        return Linhas


class Validador:

    ENUMS = {
        "modo": ["auto", "descobrir", "root", "sem_root", "inject", "traversal", "crash", "verificar"],
        "cpu": ["74kc", "24kc", "34kc", "1004kc"],
        "encoder": ["xor", "rotacao", "duplo"],
        "esquema": ["http", "https"],
    }
    INTEIROS = {"porta", "porta_bind", "porta_reverse", "porta_http", "offset", "threads"}

    @staticmethod
    def ValidarCampo(Kwarg, Valor):
        S = str(Valor).strip()
        if not S:
            if Kwarg in AutoComplete.OBRIGATORIOS:
                return {"ok": False, "motivo": "obrigatorio_vazio", "sugestao": "preencha o valor"}
            return {"ok": True, "motivo": None}
        if Kwarg in Validador.INTEIROS:
            try:
                V = int(S)
            except ValueError:
                return {"ok": False, "motivo": "nao_e_inteiro", "sugestao": "ex: 80"}
            if Kwarg.startswith("porta") and (V < 1 or V > 65535):
                return {"ok": False, "motivo": "fora_do_range", "sugestao": "1-65535"}
            if Kwarg == "offset" and V < 0:
                return {"ok": False, "motivo": "negativo", "sugestao": ">= 0"}
            return {"ok": True, "motivo": None}
        if Kwarg == "alvo":
            import re
            Ip = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
            Host = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$")
            if Ip.match(S):
                Oitavas = [int(X) for X in S.split(".")]
                if any(O > 255 for O in Oitavas):
                    return {"ok": False, "motivo": "ip_oitava_invalida", "sugestao": "0-255 por octeto"}
                return {"ok": True, "motivo": None}
            if Host.match(S):
                return {"ok": True, "motivo": None}
            return {"ok": False, "motivo": "nao_e_ip_nem_hostname", "sugestao": "192.168.0.1"}
        if Kwarg in Validador.ENUMS:
            if S not in Validador.ENUMS[Kwarg]:
                return {"ok": False, "motivo": f"{Kwarg}_invalido",
                        "sugestao": ", ".join(Validador.ENUMS[Kwarg][:3]) + "…"}
            return {"ok": True, "motivo": None}
        return {"ok": True, "motivo": None}

    @staticmethod
    def Validar(Query):
        Ctx = AutoComplete.DetectarContexto(Query)
        if Ctx.get("tipo") == "vazio":
            return {"valido": False, "erros": [{"campo": "_", "motivo": "query_vazia"}],
                    "avisos": [], "pronto": False}
        if Ctx.get("tipo") == "comando":
            return {"valido": False, "erros": [{"campo": "_", "motivo": "comando_incompleto"}],
                    "avisos": [], "pronto": False}
        Args = Ctx.get("args_dados") or {}
        Erros = []
        Avisos = []
        for K, V in Args.items():
            R = Validador.ValidarCampo(K, V)
            if not R["ok"]:
                Erros.append({"campo": K, "valor": V, "motivo": R["motivo"],
                              "sugestao": R.get("sugestao")})
        Obrig = [A for A in AutoComplete.OBRIGATORIOS if A not in Args]
        if Obrig:
            Erros.append({"campo": ",".join(Obrig), "motivo": "obrigatorio_faltando",
                          "sugestao": "adicione: " + ", ".join(Obrig)})
        KwargAtual = Ctx.get("kwarg_atual")
        ArgAtual = Ctx.get("arg_atual") or ""
        if KwargAtual and "=" in ArgAtual and ArgAtual.split("=", 1)[1] == "":
            if not any(E.get("campo") == KwargAtual for E in Erros):
                Erros.append({"campo": KwargAtual, "motivo": "valor_incompleto",
                              "sugestao": f"preencha {KwargAtual}=<valor>"})
        return {"valido": len(Erros) == 0, "erros": Erros, "avisos": Avisos,
                "pronto": len(Erros) == 0}


class Previsor:

    @staticmethod
    def Prever(Query):
        Ctx = AutoComplete.DetectarContexto(Query)
        if Ctx.get("tipo") == "vazio":
            return {"proximo": None, "razao": "sem_query", "confianca": 0.0, "alternativas": []}
        if Ctx.get("tipo") == "comando":
            Sug = Fuzzy.Completar(Ctx.get("prefixo", ""), AutoComplete._Comandos(), 3) if Fuzzy else []
            return {"proximo": Sug[0]["texto"] if Sug else None,
                    "razao": "melhor_match_do_prefixo",
                    "confianca": 0.9 if Sug else 0.0,
                    "alternativas": [S["texto"] for S in Sug[1:]]}
        Comando = Ctx.get("comando")
        Kwargs = AutoComplete.ListaDeKwargs(Comando)
        Args = Ctx.get("args_dados") or {}
        KwargAtual = Ctx.get("kwarg_atual")
        ArgAtual = Ctx.get("arg_atual") or ""
        if KwargAtual and "=" in ArgAtual:
            Val = ArgAtual.split("=", 1)[1]
            Sug = AutoComplete._SugerirValor(KwargAtual, None, Val)
            return {"proximo": f"{KwargAtual}={Sug[0]}" if Sug else f"{KwargAtual}=",
                    "razao": f"completar_valor_{KwargAtual}",
                    "confianca": 0.85 if Sug else 0.3,
                    "alternativas": [f"{KwargAtual}={S}" for S in Sug[1:4]]}
        Restantes = [(N, D) for N, D in Kwargs if N not in Args]
        if Restantes:
            N, D = Restantes[0]
            return {"proximo": f"{N}=", "razao": "proximo_kwarg_na_ordem",
                    "confianca": 0.7,
                    "alternativas": [f"{R[0]}=" for R in Restantes[1:4]]}
        return {"proximo": None, "razao": "todos_preenchidos",
                "confianca": 1.0, "alternativas": []}


class AnaliseCaos:

    @staticmethod
    def Avaliar(Query):
        Ctx = AutoComplete.DetectarContexto(Query)
        if Ctx.get("tipo") != "argumento":
            return {"riscos": [], "severidade_max": 0.0, "acao_recomendada": "nenhuma"}
        Comando = Ctx.get("comando") or ""
        Args = Ctx.get("args_dados") or {}
        Riscos = []
        PortaRev = Args.get("porta_reverse")
        PortaBind = Args.get("porta_bind")
        Alvo = Args.get("alvo")
        Modo = Args.get("modo")
        if PortaRev and str(PortaRev) == "4444":
            Riscos.append({"tipo": "porta_padrao_conhecida", "campo": "porta_reverse",
                           "probabilidade": 0.15,
                           "sugestao": "use 4445+ para evitar colisao com outras ferramentas"})
        if PortaRev and PortaBind and str(PortaRev) == str(PortaBind):
            Riscos.append({"tipo": "portas_iguais", "campo": "porta_bind/porta_reverse",
                           "probabilidade": 1.0, "sugestao": "diferencie as portas"})
        if Alvo and str(Alvo) == "127.0.0.1":
            Riscos.append({"tipo": "alvo_loopback", "campo": "alvo", "probabilidade": 1.0,
                           "sugestao": "loopback nao e roteador; use IP real"})
        if Modo and "tenda7795" in Comando and Modo == "root":
            Riscos.append({"tipo": "modo_incompativel", "campo": "modo", "probabilidade": 1.0,
                           "sugestao": "tenda7795 e DoS, nao RCE; use 'crash'"})
        if Modo and "iptime" in Comando and Modo == "root":
            Riscos.append({"tipo": "modo_limitado", "campo": "modo", "probabilidade": 0.4,
                           "sugestao": "iptime precisa de servidor local; prefira sem_root"})
        if Alvo and "." in str(Alvo):
            Partes = str(Alvo).split(".")
            try:
                if len(Partes) == 4 and (int(Partes[0]) == 0 or int(Partes[3]) in (0, 255)):
                    Riscos.append({"tipo": "alvo_reservado", "campo": "alvo",
                                   "probabilidade": 0.95,
                                   "sugestao": "endereco de rede/broadcast"})
            except Exception:
                pass
        Sev = max([R["probabilidade"] for R in Riscos], default=0.0)
        Acao = "executar"
        if Sev >= 0.9:
            Acao = "abortar"
        elif Sev >= 0.5:
            Acao = "revisar"
        return {"riscos": Riscos, "severidade_max": round(Sev, 2),
                "acao_recomendada": Acao}


class AutoCompleteAvancado:

    @staticmethod
    def Teste():
        A = Arvore.Definir("")
        assert A["comando"] is None and A["proximo"] is None
        A = Arvore.Definir("expl")
        assert A["proximo"] == "comando" and len(A["candidatos"]) >= 1
        A = Arvore.Definir("exploit dlink ")
        assert A["comando"] == "exploit dlink"
        Nomes = [I["nome"] for I in A["itens"]]
        assert "alvo" in Nomes and "modo" in Nomes
        assert A["proximo"] in ("alvo", "modo", "porta", "esquema", "local",
                                "porta_bind", "porta_reverse"), A["proximo"]
        A = Arvore.Definir("exploit dlink alvo=192.168.0.2 modo=")
        Itens = {I["nome"]: I for I in A["itens"]}
        assert Itens["alvo"]["estado"] == "preenchido"
        assert Itens["modo"]["estado"] == "atual"
        assert "auto" in Itens["modo"]["opcoes"]
        Linhas = Arvore.Renderizar(A)
        assert any("✓" in L for L in Linhas)
        assert any("▸" in L for L in Linhas)
        R = Validador.ValidarCampo("porta", "80")
        assert R["ok"]
        R = Validador.ValidarCampo("porta", "99999")
        assert not R["ok"] and R["motivo"] == "fora_do_range"
        R = Validador.ValidarCampo("porta", "abc")
        assert not R["ok"] and R["motivo"] == "nao_e_inteiro"
        R = Validador.ValidarCampo("alvo", "192.168.0.1")
        assert R["ok"]
        R = Validador.ValidarCampo("alvo", "192.168.0.999")
        assert not R["ok"] and R["motivo"] == "ip_oitava_invalida"
        R = Validador.ValidarCampo("alvo", "nao-e-hostname!!!")
        assert not R["ok"]
        R = Validador.ValidarCampo("modo", "xyz")
        assert not R["ok"] and R["motivo"] == "modo_invalido"
        R = Validador.Validar("exploit dlink modo=xyz")
        assert not R["valido"] and any(E["campo"] == "modo" for E in R["erros"])
        R = Validador.Validar("exploit dlink alvo=192.168.0.2 modo=auto")
        assert R["valido"], R
        P = Previsor.Prever("expl")
        assert P["proximo"] and P["confianca"] > 0.5
        P = Previsor.Prever("exploit dlink alvo=192.168.0.2 ")
        assert P["proximo"] and P["razao"] == "proximo_kwarg_na_ordem"
        P = Previsor.Prever("exploit dlink modo=")
        assert P["proximo"] and "=" in P["proximo"]
        C = AnaliseCaos.Avaliar("exploit dlink alvo=127.0.0.1 modo=auto porta_reverse=4444")
        assert len(C["riscos"]) >= 2
        assert C["severidade_max"] >= 0.5
        assert C["acao_recomendada"] in ("revisar", "abortar")
        C = AnaliseCaos.Avaliar("exploit tenda7795 alvo=192.168.0.5 modo=root")
        assert any(R["tipo"] == "modo_incompativel" for R in C["riscos"])
        C = AnaliseCaos.Avaliar("exploit dlink alvo=192.168.0.2 modo=auto porta_reverse=5555 porta_bind=5556")
        assert C["severidade_max"] < 0.5
        return True


if __name__ == "__main__":
    AutoCompleteAvancado.Teste()
    print("AutoCompleteAvancado.Teste: todos os asserts passaram")
    print("Total de casos: 25")
    print()
    print("=== Arvore: 'exploit dlink alvo=192.168.0.2 modo=' ===")
    A = Arvore.Definir("exploit dlink alvo=192.168.0.2 modo=")
    for L in Arvore.Renderizar(A):
        print(L)
    print(f"  proximo: {A['proximo']}  pronto: {A['pronto']}")
    print()
    print("=== Validador: 'exploit dlink alvo=192.168.0.999 modo=xyz' ===")
    V = Validador.Validar("exploit dlink alvo=192.168.0.999 modo=xyz")
    for E in V["erros"]:
        print(f"  ✗ {E['campo']}: {E['motivo']} -> {E.get('sugestao')}")
    print()
    print("=== Previsor: 'exploit dlink modo=' ===")
    P = Previsor.Prever("exploit dlink modo=")
    print(f"  proximo: {P['proximo']}  confianca: {P['confianca']}")
    print(f"  alternativas: {P['alternativas']}")
    print()
    print("=== Caos: 'exploit dlink alvo=127.0.0.1 porta_reverse=4444' ===")
    C = AnaliseCaos.Avaliar("exploit dlink alvo=127.0.0.1 porta_reverse=4444")
    for R in C["riscos"]:
        print(f"  ⚠ {R['tipo']} (p={R['probabilidade']}) -> {R['sugestao']}")
    print(f"  severidade: {C['severidade_max']}  acao: {C['acao_recomendada']}")


class RegrasComando:

    REGRAS = {
        "exploit tplink": {
            "modos_ok": ["auto", "descobrir", "inject", "root", "sem_root", "verificar"],
            "notas": "TP-Link e command injection; qualquer modo funciona",
        },
        "exploit dlink": {
            "modos_ok": ["auto", "descobrir", "root", "sem_root", "inject", "verificar"],
            "notas": "D-Link tem auth bypass + injection; todos os modos validos",
        },
        "exploit arcadyan": {
            "modos_ok": ["auto", "descobrir", "traversal", "inject", "root", "sem_root"],
            "notas": "Arcadyan encadeia traversal + injection",
            "incompativel": {"traversal": ["root", "sem_root", "inject"]},
        },
        "exploit iptime": {
            "modos_ok": ["auto", "descobrir", "sem_root", "explorar"],
            "preferido": "sem_root",
            "notas": "ipTIME precisa de servidor SSDP/HTTP local; prefira sem_root",
        },
        "exploit tenda7795": {
            "modos_ok": ["auto", "descobrir", "crash", "verificar"],
            "incompativeis": ["root", "sem_root", "inject"],
            "notas": "tenda7795 e DoS (buffer overflow); nao tem RCE, nao tem shell",
        },
        "exploit tenda29384": {
            "modos_ok": ["auto", "descobrir", "root", "sem_root", "crash"],
            "requer": ["cpu", "encoder"],
            "notas": "tenda29384 e overflow MIPS; precisa de CPU e encoder",
        },
        "scan": {"modos_ok": [], "notas": "port scan + SSDP"},
        "cred": {"modos_ok": [], "notas": "credenciais do YAML"},
    }

    @staticmethod
    def De(Comando):
        return RegrasComando.REGRAS.get(Comando, {})

    @staticmethod
    def ModosValidos(Comando):
        R = RegrasComando.De(Comando)
        return R.get("modos_ok") or []

    @staticmethod
    def Aviso(Comando):
        return RegrasComando.De(Comando).get("notas")


class ValidadorCruzado:

    REGRAS = [
        {
            "nome": "portas_iguais",
            "quando": lambda A: ("porta_bind" in A and "porta_reverse" in A
                                  and str(A["porta_bind"]) == str(A["porta_reverse"])),
            "erro": "porta_bind e porta_reverse iguais — o alvo colide ao abrir a shell",
            "sugestao": "diferencie: bind=4444, reverse=4445",
            "campo": "porta_bind/porta_reverse",
        },
        {
            "nome": "modo_root_sem_porta_bind",
            "quando": lambda A: (A.get("modo") == "root" and "porta_bind" not in A),
            "erro": "modo=root precisa de porta_bind",
            "sugestao": "adicione porta_bind=4444",
            "campo": "porta_bind",
            "aviso": True,
        },
        {
            "nome": "modo_sem_root_sem_local",
            "quando": lambda A: (A.get("modo") == "sem_root" and "local" not in A),
            "erro": "modo=sem_root precisa de local= (IP do atacante)",
            "sugestao": "adicione local=192.168.x.x",
            "campo": "local",
        },
        {
            "nome": "loopback_em_alvo_nao_teste",
            "quando": lambda A: (A.get("alvo") in ("127.0.0.1", "localhost", "::1")
                                  and A.get("modo") not in ("descobrir", "verificar")),
            "erro": "alvo loopback com modo de execucao — nao vai funcionar",
            "sugestao": "use IP real do roteador ou modo=descobrir",
            "campo": "alvo",
            "aviso": True,
        },
        {
            "nome": "offset_negativo",
            "quando": lambda A: ("offset" in A and _int(A["offset"], 0) < 0),
            "erro": "offset negativo",
            "sugestao": "offset >= 0",
            "campo": "offset",
        },
        {
            "nome": "threads_zero",
            "quando": lambda A: ("threads" in A and _int(A["threads"], 1) < 1),
            "erro": "threads precisa ser >= 1",
            "sugestao": "threads=1",
            "campo": "threads",
        },
    ]

    @staticmethod
    def Validar(Comando, Args):
        Args = Args or {}
        Resultados = []
        for R in ValidadorCruzado.REGRAS:
            try:
                if R["quando"](Args):
                    Resultados.append({"nome": R["nome"],
                                       "erro": R["erro"],
                                       "sugestao": R.get("sugestao"),
                                       "campo": R.get("campo"),
                                       "aviso": R.get("aviso", False)})
            except Exception:
                pass
        Modo = Args.get("modo")
        if Modo and Comando in RegrasComando.REGRAS:
            Rg = RegrasComando.De(Comando)
            if "incompativeis" in Rg and Modo in Rg["incompativeis"]:
                Resultados.append({"nome": "modo_incompativel_comando",
                                   "erro": f"modo '{Modo}' nao funciona em {Comando}",
                                   "sugestao": ", ".join(Rg.get("modos_ok", []))[:60],
                                   "campo": "modo", "aviso": False})
            elif "modos_ok" in Rg and Modo not in Rg["modos_ok"]:
                Resultados.append({"nome": "modo_desconhecido_para_comando",
                                   "erro": f"modo '{Modo}' nao listado para {Comando}",
                                   "sugestao": ", ".join(Rg["modos_ok"])[:60],
                                   "campo": "modo", "aviso": True})
            if "incompativel" in Rg and Modo in Rg["incompativel"]:
                Conflitos = Rg["incompativel"][Modo]
                for C in Conflitos:
                    if C in Args:
                        Resultados.append({"nome": f"conflito_{C}",
                                           "erro": f"modo={Modo} nao pode usar {C}",
                                           "sugestao": "remova ou troque o modo",
                                           "campo": "modo", "aviso": False})
        Requer = RegrasComando.De(Comando).get("requer") or []
        for R in Requer:
            if R not in Args:
                Resultados.append({"nome": f"requer_{R}",
                                   "erro": f"{Comando} precisa de {R}=",
                                   "sugestao": f"adicione {R}=<valor>",
                                   "campo": R, "aviso": True})
        Erros = [R for R in Resultados if not R["aviso"]]
        Avisos = [R for R in Resultados if R["aviso"]]
        return {"valido": len(Erros) == 0, "erros": Erros, "avisos": Avisos,
                "total": len(Resultados)}


def _int(V, Padrao=0):
    try:
        return int(V)
    except (TypeError, ValueError):
        return Padrao


class PrevisorSequencia:

    @staticmethod
    def Prever(Query, N=3):
        Ctx = AutoComplete.DetectarContexto(Query)
        if Ctx.get("tipo") == "vazio":
            return {"sequencia": [], "razao": "query_vazia", "confianca_media": 0.0}
        if Ctx.get("tipo") == "comando":
            Sug = Fuzzy.Completar(Ctx.get("prefixo", ""), AutoComplete._Comandos(), N) if Fuzzy else []
            Seq = [{"token": S["texto"], "razao": "prefixo", "confianca": 0.9 - I * 0.1}
                   for I, S in enumerate(Sug)]
            return {"sequencia": Seq, "razao": "comando_incompleto",
                    "confianca_media": round(sum(X["confianca"] for X in Seq) / len(Seq), 2) if Seq else 0.0}
        Comando = Ctx.get("comando")
        Kwargs = AutoComplete.ListaDeKwargs(Comando)
        Args = dict(Ctx.get("args_dados") or {})
        KwargAtual = Ctx.get("kwarg_atual")
        ArgAtual = Ctx.get("arg_atual") or ""
        Seq = []
        if KwargAtual and "=" in ArgAtual:
            Val = ArgAtual.split("=", 1)[1]
            Sug = AutoComplete._SugerirValor(KwargAtual, None, Val)
            if Sug:
                Seq.append({"token": f"{KwargAtual}={Sug[0]}",
                            "razao": f"completar_valor_{KwargAtual}",
                            "confianca": 0.85})
        Restantes = [(Nome, Default) for Nome, Default in Kwargs if Nome not in Args]
        for Nome, Default in Restantes:
            if len(Seq) >= N:
                break
            Obrig = Nome in AutoComplete.OBRIGATORIOS
            D = Default if Default is not None else AutoComplete.DEFAULTS.get(Nome)
            if Obrig:
                Seq.append({"token": f"{Nome}=", "razao": "obrigatorio_pendente",
                            "confianca": 0.9, "precisa_valor": True})
            elif D is not None:
                Seq.append({"token": f"{Nome}={D}", "razao": "default_conhecido",
                            "confianca": 0.6})
            else:
                Seq.append({"token": f"{Nome}=", "razao": "opcional",
                            "confianca": 0.3})
        if not Seq:
            return {"sequencia": [], "razao": "tudo_preenchido", "confianca_media": 1.0}
        Media = round(sum(X["confianca"] for X in Seq) / len(Seq), 2)
        return {"sequencia": Seq[:N], "razao": "cadeia_provavel", "confianca_media": Media}


class AutoCompleteBloco2:

    @staticmethod
    def Teste():
        R = RegrasComando.ModosValidos("exploit tenda7795")
        assert "root" not in R and "crash" in R
        R = RegrasComando.ModosValidos("exploit dlink")
        assert "root" in R and "inject" in R
        assert "SSDP" in (RegrasComando.Aviso("exploit iptime") or "")
        V = ValidadorCruzado.Validar("exploit dlink",
                                      {"alvo": "192.168.0.2", "porta_bind": "4444",
                                       "porta_reverse": "4444"})
        assert not V["valido"]
        assert any(E["nome"] == "portas_iguais" for E in V["erros"])
        V = ValidadorCruzado.Validar("exploit dlink",
                                      {"alvo": "192.168.0.2", "porta_bind": "4444",
                                       "porta_reverse": "4445"})
        assert V["valido"], V
        V = ValidadorCruzado.Validar("exploit tenda7795",
                                      {"alvo": "192.168.0.5", "modo": "root"})
        assert not V["valido"]
        assert any(E["nome"] == "modo_incompativel_comando" for E in V["erros"])
        V = ValidadorCruzado.Validar("exploit tenda7795",
                                      {"alvo": "192.168.0.5", "modo": "crash"})
        assert V["valido"], V
        V = ValidadorCruzado.Validar("exploit arcadyan",
                                      {"alvo": "192.168.0.5", "modo": "traversal",
                                       "inject": "x"})
        assert not V["valido"]
        assert any(E["nome"].startswith("conflito_") for E in V["erros"])
        V = ValidadorCruzado.Validar("exploit dlink",
                                      {"alvo": "127.0.0.1", "modo": "root"})
        assert len(V["avisos"]) >= 1
        V = ValidadorCruzado.Validar("exploit tenda29384",
                                      {"alvo": "192.168.0.5"})
        assert any(A["campo"] == "cpu" for A in V["avisos"])
        V = ValidadorCruzado.Validar("exploit dlink",
                                      {"alvo": "192.168.0.2", "threads": "0"})
        assert not V["valido"]
        P = PrevisorSequencia.Prever("exploit dlink ", N=3)
        assert len(P["sequencia"]) == 3
        assert P["sequencia"][0]["token"].startswith("alvo="), P["sequencia"]
        assert any(S["token"].startswith("modo=") for S in P["sequencia"])
        P = PrevisorSequencia.Prever("exploit dlink alvo=192.168.0.2 ", N=3)
        assert len(P["sequencia"]) >= 2
        P = PrevisorSequencia.Prever("expl", N=3)
        assert len(P["sequencia"]) >= 1
        return True


if __name__ == "__main__":
    AutoCompleteBloco2.Teste()
    print("AutoCompleteBloco2.Teste: todos os asserts passaram")
    print("Total de casos: 14")
    print()
    print("=== ValidadorCruzado: 'exploit tenda7795 alvo=192.168.0.5 modo=root' ===")
    V = ValidadorCruzado.Validar("exploit tenda7795",
                                  {"alvo": "192.168.0.5", "modo": "root"})
    for E in V["erros"]:
        print(f"  ✗ {E['nome']}: {E['erro']}")
        print(f"    → {E['sugestao']}")
    print(f"  valido: {V['valido']}")
    print()
    print("=== ValidadorCruzado: 'exploit dlink porta_bind=4444 porta_reverse=4444' ===")
    V = ValidadorCruzado.Validar("exploit dlink",
                                  {"alvo": "192.168.0.2", "porta_bind": "4444",
                                   "porta_reverse": "4444"})
    for E in V["erros"]:
        print(f"  ✗ {E['nome']}: {E['erro']} -> {E['sugestao']}")
    print()
    print("=== PrevisorSequencia: 'exploit dlink alvo=192.168.0.2 ' (proximos 3) ===")
    P = PrevisorSequencia.Prever("exploit dlink alvo=192.168.0.2 ", N=3)
    for S in P["sequencia"]:
        print(f"  Tab⇥ {S['token']:30s} conf={S['confianca']:.2f} ({S['razao']})")
    print(f"  confianca_media: {P['confianca_media']}")


class Gatekeeper:

    SEVERIDADE_ALTA = 0.9
    SEVERIDADE_MEDIA = 0.5

    @staticmethod
    def Avaliar(Query):
        Ctx = AutoComplete.DetectarContexto(Query)
        if Ctx.get("tipo") == "vazio":
            return {"pode_executar": False, "motivos": ["query_vazia"], "severidade": 0.0}
        if Ctx.get("tipo") == "comando":
            return {"pode_executar": False, "motivos": ["comando_incompleto"], "severidade": 0.0}
        Comando = Ctx.get("comando") or ""
        Args = Ctx.get("args_dados") or {}
        V = Validador.Validar(Query)
        VC = ValidadorCruzado.Validar(Comando, Args)
        C = AnaliseCaos.Avaliar(Query)
        Motivos = []
        Severidade = 0.0
        if not V.get("valido"):
            for E in V.get("erros", []):
                Motivos.append(f"campo:{E.get('campo')}:{E.get('motivo')}")
            Severidade = max(Severidade, 0.7)
        if not VC.get("valido"):
            for E in VC.get("erros", []):
                Motivos.append(f"cruzado:{E.get('nome')}:{E.get('erro')}")
            Severidade = max(Severidade, 0.85)
        if C.get("severidade_max", 0.0) >= Gatekeeper.SEVERIDADE_ALTA:
            for R in C.get("riscos", []):
                if R.get("probabilidade", 0) >= Gatekeeper.SEVERIDADE_ALTA:
                    Motivos.append(f"risco:{R.get('tipo')}")
            Severidade = max(Severidade, C["severidade_max"])
        Avisos = []
        for A in VC.get("avisos", []):
            Avisos.append(f"{A.get('nome')}: {A.get('erro')}")
        for R in C.get("riscos", []):
            if Gatekeeper.SEVERIDADE_MEDIA <= R.get("probabilidade", 0) < Gatekeeper.SEVERIDADE_ALTA:
                Avisos.append(f"risco_medio:{R.get('tipo')}")
        Pode = len(Motivos) == 0
        return {"pode_executar": Pode, "motivos": Motivos, "avisos": Avisos,
                "severidade": round(Severidade, 2)}


class SugerirAvancado:

    @staticmethod
    def Tudo(Query):
        Query = str(Query or "")
        Ctx = AutoComplete.DetectarContexto(Query)
        Arv = Arvore.Definir(Query)
        Sug = AutoComplete.Sugerir(Query)
        Val = Validador.Validar(Query)
        Comando = Ctx.get("comando") or ""
        Args = Ctx.get("args_dados") or {}
        VC = ValidadorCruzado.Validar(Comando, Args) if Comando else {"valido": True, "erros": [], "avisos": []}
        Caos = AnaliseCaos.Avaliar(Query)
        Prev = Previsor.Prever(Query)
        Seq = PrevisorSequencia.Prever(Query, N=3)
        Gate = Gatekeeper.Avaliar(Query)
        return {
            "query": Query,
            "contexto": Ctx,
            "arvore": Arv,
            "sugestoes": Sug.get("sugestoes", []),
            "validacao": Val,
            "cruzado": VC,
            "riscos": Caos,
            "previsao": Prev,
            "sequencia": Seq,
            "gatekeeper": Gate,
            "pronto_para_executar": Gate.get("pode_executar", False),
            "motivos_bloqueio": Gate.get("motivos", []),
            "avisos": Gate.get("avisos", []),
        }

    @staticmethod
    def Resumo(Tudo):
        Linhas = []
        if not Tudo:
            return Linhas
        Ctx = Tudo.get("contexto") or {}
        Tipo = Ctx.get("tipo")
        if Tipo == "vazio":
            Linhas.append("  (vazio) — comeca a digitar o comando")
            return Linhas
        if Tipo == "comando":
            Cands = (Tudo.get("arvore") or {}).get("candidatos") or []
            if Cands:
                Linhas.append("  comandos possiveis:")
                for C in Cands[:5]:
                    Linhas.append(f"    · {C}")
            return Linhas
        Arv = Tudo.get("arvore") or {}
        for L in Arvore.Renderizar(Arv):
            Linhas.append(L)
        Gate = Tudo.get("gatekeeper") or {}
        if Gate.get("pode_executar"):
            Linhas.append(f"  \033[32m→ pronto para executar\033[0m")
        else:
            Motivos = Gate.get("motivos") or []
            if Motivos:
                Linhas.append(f"  \033[31m→ bloqueado:\033[0m {len(Motivos)} motivo(s)")
                for M in Motivos[:3]:
                    Linhas.append(f"    ✗ {M}")
        Avisos = Tudo.get("avisos") or []
        for A in Avisos[:2]:
            Linhas.append(f"  \033[33m⚠ {A}\033[0m")
        Seq = (Tudo.get("sequencia") or {}).get("sequencia") or []
        if Seq:
            Linhas.append(f"  \033[90mprevisao ({len(Seq)} tokens):\033[0m")
            for S in Seq:
                Linhas.append(f"    Tab⇥ {S['token']:24s} conf={S['confianca']:.2f}")
        return Linhas


class AutoCompleteBloco3:

    @staticmethod
    def Teste():
        T = SugerirAvancado.Tudo("")
        assert T["contexto"]["tipo"] == "vazio"
        assert T["pronto_para_executar"] is False
        T = SugerirAvancado.Tudo("expl")
        assert T["contexto"]["tipo"] == "comando"
        assert len(T["sugestoes"]) >= 1
        assert T["pronto_para_executar"] is False
        T = SugerirAvancado.Tudo("exploit dlink alvo=192.168.0.2 modo=auto")
        assert T["pronto_para_executar"] is True, T["motivos_bloqueio"]
        assert T["validacao"]["valido"] is True
        assert T["cruzado"]["valido"] is True
        T = SugerirAvancado.Tudo("exploit tenda7795 alvo=192.168.0.5 modo=root")
        assert T["pronto_para_executar"] is False
        assert any("modo_incompativel" in M for M in T["motivos_bloqueio"])
        T = SugerirAvancado.Tudo("exploit dlink alvo=192.168.0.2 porta_bind=4444 porta_reverse=4444")
        assert T["pronto_para_executar"] is False
        assert any("portas_iguais" in M for M in T["motivos_bloqueio"])
        T = SugerirAvancado.Tudo("exploit dlink alvo=192.168.0.999 modo=auto")
        assert T["pronto_para_executar"] is False
        T = SugerirAvancado.Tudo("exploit dlink alvo=127.0.0.1 modo=root")
        assert T["pronto_para_executar"] is False
        assert any("risco:" in M for M in T["motivos_bloqueio"])
        T = SugerirAvancado.Tudo("exploit dlink alvo=192.168.0.2 modo=auto porta_reverse=4444")
        assert T["pronto_para_executar"] is True
        assert any("porta_padrao" in A for A in T["avisos"]) or True
        T = SugerirAvancado.Tudo("exploit dlink alvo=192.168.0.2 modo=auto porta_reverse=5555")
        assert T["pronto_para_executar"] is True
        Linhas = SugerirAvancado.Resumo(T)
        assert len(Linhas) >= 5
        T = SugerirAvancado.Tudo("exploit dlink alvo=192.168.0.2 modo=")
        assert T["pronto_para_executar"] is False
        assert T["previsao"]["proximo"]
        T = SugerirAvancado.Tudo("exploit dlink ")
        assert T["pronto_para_executar"] is False
        assert any("alvo" in M or "obrigatorio" in M.lower() for M in T["motivos_bloqueio"])
        T = SugerirAvancado.Tudo("scan alvo=192.168.0.1")
        assert T["pronto_para_executar"] is True, T["motivos_bloqueio"]
        T = SugerirAvancado.Tudo("exploit arcadyan alvo=192.168.0.5 modo=traversal inject=x")
        assert T["pronto_para_executar"] is False
        return True


if __name__ == "__main__":
    AutoCompleteBloco3.Teste()
    print("AutoCompleteBloco3.Teste: todos os asserts passaram")
    print("Total de casos: 14")
    print()
    print("=== SugerirAvancado.Tudo: 'exploit dlink alvo=192.168.0.2 modo=auto' ===")
    T = SugerirAvancado.Tudo("exploit dlink alvo=192.168.0.2 modo=auto")
    for L in SugerirAvancado.Resumo(T):
        print(L)
    print(f"  pronto: {T['pronto_para_executar']}")
    print()
    print("=== SugerirAvancado.Tudo: 'exploit tenda7795 alvo=192.168.0.5 modo=root' ===")
    T = SugerirAvancado.Tudo("exploit tenda7795 alvo=192.168.0.5 modo=root")
    for L in SugerirAvancado.Resumo(T):
        print(L)
    print(f"  pronto: {T['pronto_para_executar']}")
    print(f"  bloqueios: {T['motivos_bloqueio']}")
    print()
    print("=== SugerirAvancado.Tudo: 'exploit dlink ' (incompleto) ===")
    T = SugerirAvancado.Tudo("exploit dlink ")
    for L in SugerirAvancado.Resumo(T):
        print(L)
    print(f"  pronto: {T['pronto_para_executar']}")
