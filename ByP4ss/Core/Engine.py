# Engine do ByP4ss
# Orquestrador tolerante a ImportError
# Toda fase retorna dict. Se modulo falta, registra e continua.

import time
import importlib

from Core.Constants import Constants
from Core.Config import Config
from Core.Log import Log


class Engine:

    _Iniciado = False
    _Resultados = {}
    _Estado = {}
    _ModulosDisponiveis = {}

    @staticmethod
    def _CarregarModulo(CaminhoCompleto):
        if CaminhoCompleto in Engine._ModulosDisponiveis:
            return Engine._ModulosDisponiveis[CaminhoCompleto]
        try:
            Modulo = importlib.import_module(CaminhoCompleto)
            Engine._ModulosDisponiveis[CaminhoCompleto] = Modulo
            return Modulo
        except ImportError as E:
            Log.Aviso("modulo nao disponivel", {
                "modulo": CaminhoCompleto,
                "erro": str(E),
            })
            Engine._ModulosDisponiveis[CaminhoCompleto] = None
            return None

    @staticmethod
    def Iniciar(Cfg=None):
        Engine._Iniciado = True
        Engine._Resultados = {
            "discover": [],
            "bypass": [],
            "fuzz": [],
            "verify": [],
            "report": [],
        }
        Engine._Estado = {
            "iniciado_em": time.time(),
            "alvo": getattr(Cfg, "Alvo", Constants.ALVO_PADRAO) if Cfg else Constants.ALVO_PADRAO,
            "fase_atual": "init",
            "fases_concluidas": [],
        }
        Log.Info("engine iniciado", {"alvo": Engine._Estado["alvo"]})

    @staticmethod
    def Finalizar():
        Engine._Estado["finalizado_em"] = time.time()
        Engine._Estado["duracao"] = round(
            Engine._Estado["finalizado_em"] - Engine._Estado["iniciado_em"], 3
        )
        Log.Info("engine finalizado", Engine.Stats())
        Log.Finalizar()
        Engine._Iniciado = False

    @staticmethod
    def _Registrar(Fase, Resultado):
        if Fase in Engine._Resultados:
            Engine._Resultados[Fase].append(Resultado)
        Engine._Estado["fase_atual"] = Fase

    @staticmethod
    def _MarcarFase(Fase):
        if Fase not in Engine._Estado["fases_concluidas"]:
            Engine._Estado["fases_concluidas"].append(Fase)

    @staticmethod
    def _ModuloFalta(Nome, Resultado):
        Resultado[Nome] = {"ok": False, "motivo": "modulo_nao_implementado"}
        Log.Aviso("modulo faltando", {"modulo": Nome})

    @staticmethod
    def Discover(Alvo):
        Engine._Estado["fase_atual"] = "discover"
        Log.Info("discover iniciado", {"alvo": Alvo})

        Resultados = {
            "alvo": Alvo,
            "ssdp": None,
            "portas": [],
            "fingerprint": None,
            "cves": [],
            "status": Constants.STATUS_OK,
        }

        Mod = Engine._CarregarModulo("Discovery.Ssdp")
        if Mod:
            try:
                Resultados["ssdp"] = Mod.Ssdp.Descobrir(Alvo)
                if Resultados["ssdp"] and Resultados["ssdp"].get("ok"):
                    Log.Descoberta("Ssdp", Alvo, "upnp", Resultados["ssdp"])
            except Exception as E:
                Log.Erro("ssdp falhou", {"erro": str(E)})
        else:
            Engine._ModuloFalta("ssdp", Resultados)

        Mod = Engine._CarregarModulo("Discovery.PortScan")
        if Mod:
            try:
                Resultados["portas"] = Mod.PortScan.Escanear(
                    Alvo, Config.Portas, Config.ThreadsPorts
                )
                Log.Descoberta("PortScan", Alvo, "portas", {
                    "total": len(Resultados["portas"]),
                })
            except Exception as E:
                Log.Erro("portscan falhou", {"erro": str(E)})
        else:
            Engine._ModuloFalta("portscan", Resultados)

        Mod = Engine._CarregarModulo("Discovery.ServiceFingerprint")
        if Mod:
            try:
                Resultados["fingerprint"] = Mod.ServiceFingerprint.Identificar(
                    Alvo, Resultados["portas"]
                )
            except Exception as E:
                Log.Erro("fingerprint falhou", {"erro": str(E)})
        else:
            Engine._ModuloFalta("fingerprint", Resultados)

        Mod = Engine._CarregarModulo("Discovery.CveMatch")
        if Mod:
            try:
                Resultados["cves"] = Mod.CveMatch.Correlacionar(
                    Resultados["fingerprint"] or {}, Resultados["portas"]
                )
            except Exception as E:
                Log.Erro("cve match falhou", {"erro": str(E)})
        else:
            Engine._ModuloFalta("cvematch", Resultados)

        Engine._Registrar("discover", Resultados)
        Engine._MarcarFase("discover")
        Config.AdicionarEncontrado(Resultados)

        return Resultados

    @staticmethod
    def Bypass(Alvo, Porta=None):
        Engine._Estado["fase_atual"] = "bypass"
        Porta = Porta or Config.Porta
        Log.Info("bypass iniciado", {"alvo": Alvo, "porta": Porta})

        Resultados = {
            "alvo": Alvo,
            "porta": Porta,
            "upnp": None,
            "httpauth": None,
            "telnet": None,
            "dnsrebind": None,
            "status": Constants.STATUS_OK,
        }

        DiscoverResult = None
        if Engine._Resultados["discover"]:
            DiscoverResult = Engine._Resultados["discover"][-1]

        Mod = Engine._CarregarModulo("Bypass.UpnpBypass")
        if Mod:
            try:
                ControlUrl = None
                if DiscoverResult and DiscoverResult.get("ssdp"):
                    ControlUrl = DiscoverResult["ssdp"].get("control_url")
                Resultados["upnp"] = Mod.UpnpBypass.Tentar(Alvo, ControlUrl, Porta)
                if Resultados["upnp"].get("ok"):
                    Resultados["status"] = Constants.STATUS_EXPLORADO
                    Log.Bypass("UpnpBypass", Alvo, True, Resultados["upnp"])
            except Exception as E:
                Log.Erro("upnp falhou", {"erro": str(E)})
        else:
            Engine._ModuloFalta("upnp", Resultados)

        Mod = Engine._CarregarModulo("Bypass.HttpAuth")
        if Mod:
            try:
                Resultados["httpauth"] = Mod.HttpAuth.TestarTraversal(Alvo, "/")
                if Resultados["httpauth"].get("ok"):
                    Resultados["status"] = Constants.STATUS_EXPLORADO
            except Exception as E:
                Log.Erro("httpauth falhou", {"erro": str(E)})
        else:
            Engine._ModuloFalta("httpauth", Resultados)

        Mod = Engine._CarregarModulo("Bypass.TelnetBrute")
        if Mod:
            try:
                Resultados["telnet"] = Mod.TelnetBrute.Tentar(Alvo, Porta)
            except Exception as E:
                Log.Erro("telnet falhou", {"erro": str(E)})
        else:
            Engine._ModuloFalta("telnet", Resultados)

        Mod = Engine._CarregarModulo("Bypass.DnsRebind")
        if Mod:
            try:
                Resultados["dnsrebind"] = Mod.DnsRebind.Tentar(Alvo)
            except Exception as E:
                Log.Erro("dnsrebind falhou", {"erro": str(E)})
        else:
            Engine._ModuloFalta("dnsrebind", Resultados)

        Engine._Registrar("bypass", Resultados)
        Engine._MarcarFase("bypass")
        Config.AdicionarEncontrado(Resultados)

        return Resultados

    @staticmethod
    def Fuzz(Alvo):
        Engine._Estado["fase_atual"] = "fuzz"
        Log.Info("fuzz iniciado", {"alvo": Alvo})

        Resultados = {
            "alvo": Alvo,
            "iteracoes": 0,
            "crashes": [],
            "anomalias": [],
            "status": Constants.STATUS_OK,
        }

        Mod = Engine._CarregarModulo("Fuzz.FuzzEngine")
        if Mod:
            try:
                R = Mod.FuzzEngine.Executar(Alvo, Config.FuzzIteracoes)
                Resultados.update(R)
                if Resultados.get("crashes"):
                    Resultados["status"] = Constants.STATUS_VULNERAVEL
            except Exception as E:
                Log.Erro("fuzz falhou", {"erro": str(E)})
        else:
            Engine._ModuloFalta("fuzz", Resultados)

        Engine._Registrar("fuzz", Resultados)
        Engine._MarcarFase("fuzz")

        return Resultados

    @staticmethod
    def Verify(Alvo):
        Engine._Estado["fase_atual"] = "verify"
        Log.Info("verify iniciado", {"alvo": Alvo})

        Resultados = {
            "alvo": Alvo,
            "portas_ok": [],
            "servicos_ok": [],
            "exploits_ok": [],
            "status": Constants.STATUS_OK,
        }

        BypassResult = None
        if Engine._Resultados["bypass"]:
            BypassResult = Engine._Resultados["bypass"][-1]

        if BypassResult:
            Porta = BypassResult.get("porta")

            Mod = Engine._CarregarModulo("Verify.PortVerify")
            if Mod:
                try:
                    if Mod.PortVerify.Verificar(Alvo, Porta):
                        Resultados["portas_ok"].append(Porta)
                except Exception as E:
                    Log.Erro("portverify falhou", {"erro": str(E)})

            Mod = Engine._CarregarModulo("Verify.ServiceVerify")
            if Mod:
                try:
                    if Mod.ServiceVerify.Verificar(Alvo, Porta):
                        Resultados["servicos_ok"].append(Porta)
                except Exception as E:
                    Log.Erro("serviceverify falhou", {"erro": str(E)})

            Mod = Engine._CarregarModulo("Verify.ExploitVerify")
            if Mod:
                try:
                    if Mod.ExploitVerify.Verificar(Alvo, Porta):
                        Resultados["exploits_ok"].append(Porta)
                        Resultados["status"] = Constants.STATUS_EXPLORADO
                except Exception as E:
                    Log.Erro("exploitverify falhou", {"erro": str(E)})
            else:
                Engine._ModuloFalta("exploitverify", Resultados)

        Engine._Registrar("verify", Resultados)
        Engine._MarcarFase("verify")
        Config.AdicionarEncontrado(Resultados)

        return Resultados

    @staticmethod
    def Report():
        Engine._Estado["fase_atual"] = "report"
        Log.Info("report iniciado")

        Resultados = {
            "gerado_em": time.time(),
            "fases": {K: list(V) for K, V in Engine._Resultados.items()},
            "resumo": Engine.Resumo(),
            "status": Constants.STATUS_OK,
        }

        Mod = Engine._CarregarModulo("Report.Findings")
        if Mod:
            try:
                Coletado = Mod.Findings.Coletar(Engine._Resultados)
                if isinstance(Coletado, dict):
                    Resultados["findings"] = Coletado
                    Log.Info("findings anexados", {
                        "total": Coletado.get("total", 0),
                    })
            except Exception as E:
                Log.Erro("findings falhou", {"erro": str(E)})

        if Config.Salvar:
            Mod = Engine._CarregarModulo("Report.Export")
            if Mod:
                try:
                    Mod.Export.SalvarJson(Resultados)
                    Mod.Export.SalvarMd(Resultados)
                    if hasattr(Mod.Export, "SalvarCsv"):
                        Mod.Export.SalvarCsv(Resultados)
                except Exception as E:
                    Log.Erro("export falhou", {"erro": str(E)})

        Engine._Registrar("report", Resultados)
        Engine._MarcarFase("report")

        return Resultados

    @staticmethod
    def Resumo():
        return {
            "discover": len(Engine._Resultados["discover"]),
            "bypass": len(Engine._Resultados["bypass"]),
            "fuzz": len(Engine._Resultados["fuzz"]),
            "verify": len(Engine._Resultados["verify"]),
            "report": len(Engine._Resultados["report"]),
            "encontrados": Config.ContarEncontrados(),
            "erros": Config.ContarErros(),
            "alertas": Config.ContarAlertas(),
        }

    @staticmethod
    def Stats():
        return {
            "estado": dict(Engine._Estado),
            "resultados": {K: len(V) for K, V in Engine._Resultados.items()},
            "log": Log.Stats(),
        }

    @staticmethod
    def Estado():
        return dict(Engine._Estado)

    @staticmethod
    def Resultados(Fase=None):
        if Fase:
            return list(Engine._Resultados.get(Fase, []))
        return dict(Engine._Resultados)


    MapaExploits = {
        "tplink":     ("ExploitByp4ss.TPLink.CVE_2023_1389",     "Exploit"),
        "dlink":      ("ExploitByp4ss.DLink.CVE_2024_3273",      "CVE_2024_3273"),
        "tenda7795":  ("ExploitByp4ss.Tenda.CVE_2025_7795",      "CVE_2025_7795"),
        "arcadyan":   ("ExploitByp4ss.Arcadyan.CVE_2021_20090",  "CVE_2021_20090"),
        "iptime":     ("ExploitByp4ss.IpTime.CVE_2025_55423",    "CVE_2025_55423"),
        "tenda29384": ("ExploitByp4ss.Tenda.CVE_2025_29384",     "CVE_2025_29384"),
    }

    MapaModos = {
        "auto":       "ModoAuto",
        "descobrir":  "Descobrir",
        "root":       "ExploitRoot",
        "sem_root":   "ExploitSemRoot",
        "inject":     "ExploitCommandInjection",
        "traversal":  "ExploitPathTraversal",
        "verificar":  "VerificarExecucao",
        "crash":      "CrashProgressivo",
    }

    @staticmethod
    def _CarregarExploit(ExploitId):
        Info = Engine.MapaExploits.get(ExploitId)
        if not Info:
            return {"ok": False, "motivo": f"exploit_id_invalido:{ExploitId}"}
        CaminhoModulo, Classe = Info
        try:
            Modulo = importlib.import_module(CaminhoModulo)
            if not hasattr(Modulo, Classe):
                return {"ok": False, "motivo": f"classe_nao_encontrada:{Classe}"}
            return {"ok": True, "classe": getattr(Modulo, Classe), "caminho": CaminhoModulo}
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{type(E).__name__}", "erro": str(E)}

    @staticmethod
    def Exploit(ExploitId, Alvo, **Kwargs):
        Carregado = Engine._CarregarExploit(ExploitId)
        if not Carregado["ok"]:
            return {"ok": False, "cve": ExploitId, "alvo": Alvo, "motivo": Carregado["motivo"]}
        Classe = Carregado["classe"]
        Modo = Kwargs.pop("modo", "auto")
        Metodo = Engine.MapaModos.get(Modo, "ModoAuto")
        if not hasattr(Classe, Metodo):
            return {"ok": False, "cve": ExploitId, "alvo": Alvo,
                    "motivo": f"metodo_nao_encontrado:{Metodo}"}
        try:
            Resultado = getattr(Classe, Metodo)(Alvo, **Kwargs)
        except TypeError:
            Resultado = getattr(Classe, Metodo)(Alvo)
        except Exception as E:
            return {"ok": False, "cve": ExploitId, "alvo": Alvo,
                    "motivo": f"excecao:{type(E).__name__}", "erro": str(E)}
        try:
            Engine._Registrar("exploit", {"id": ExploitId, "alvo": Alvo, "ok": Resultado.get("ok")})
        except Exception:
            pass
        return {"ok": bool(Resultado.get("ok")), "cve": ExploitId, "alvo": Alvo,
                "modo": Modo, "resultado": Resultado,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    @staticmethod
    def Credenciais(Alvo):
        try:
            Modulo = importlib.import_module("ExploitByp4ss.CredLoader")
        except Exception as E:
            return {"ok": False, "alvo": Alvo, "motivo": "credl_import_falhou",
                    "erro": str(E), "credenciais": [], "total": 0}
        Loader = getattr(Modulo, "CredLoader", None)
        if Loader is None:
            return {"ok": False, "alvo": Alvo, "motivo": "credl_classe_ausente",
                    "credenciais": [], "total": 0}
        import os
        Caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                "ExploitByp4ss", "credenciais.yaml"))
        if not os.path.isfile(Caminho):
            return {"ok": False, "alvo": Alvo, "motivo": "yaml_indisponivel",
                    "credenciais": [], "total": 0}
        try:
            R = Loader.Carregar(Caminho)
            if not R.get("ok"):
                return {"ok": False, "alvo": Alvo, "motivo": R.get("erro", "carregar_falhou"),
                        "credenciais": [], "total": 0}
            Creds = Loader.Buscar(R["dados"], Alvo) or []
            return {"ok": True, "alvo": Alvo, "credenciais": Creds,
                    "total": len(Creds), "avisos": []}
        except Exception as E:
            return {"ok": False, "alvo": Alvo, "motivo": f"excecao:{type(E).__name__}",
                    "erro": str(E), "credenciais": [], "total": 0}

    @staticmethod
    def Scan(Alvo, Portas=None, Threads=10):
        Resultado = {"ok": False, "alvo": Alvo, "portas_abertas": [], "ssdp": None, "total": 0}
        try:
            PS = importlib.import_module("Discovery.PortScan")
            PortScan = getattr(PS, "PortScan", None)
            if PortScan is not None and hasattr(PortScan, "Escanear"):
                Portas = Portas or [21, 22, 23, 53, 80, 443, 8080, 8443]
                R = PortScan.Escanear(Alvo, Portas, Threads)
                Abertas = []
                if isinstance(R, list):
                    for Item in R:
                        if isinstance(Item, dict):
                            if Item.get("estado") == "aberta" and Item.get("porta") is not None:
                                Abertas.append(Item["porta"])
                            elif Item.get("aberta") is True and Item.get("porta") is not None:
                                Abertas.append(Item["porta"])
                        elif isinstance(Item, int):
                            Abertas.append(Item)
                elif isinstance(R, dict):
                    for Item in (R.get("portas") or R.get("abertas") or []):
                        if isinstance(Item, dict) and Item.get("porta") is not None:
                            if Item.get("estado") == "aberta" or Item.get("aberta") is True:
                                Abertas.append(Item["porta"])
                        elif isinstance(Item, int):
                            Abertas.append(Item)
                Resultado["portas_abertas"] = Abertas
                Resultado["total"] = len(Abertas)
                Resultado["ok"] = True
        except Exception as E:
            Resultado["erro_portscan"] = f"{type(E).__name__}:{E}"
        try:
            SS = importlib.import_module("Discovery.Ssdp")
            Ssdp = getattr(SS, "Ssdp", None)
            if Ssdp is not None and hasattr(Ssdp, "Descobrir"):
                Resultado["ssdp"] = Ssdp.Descobrir(Alvo)
        except Exception as E:
            Resultado["erro_ssdp"] = f"{type(E).__name__}:{E}"
        return Resultado

    @staticmethod
    def ReportIntegrado():
        Eventos = []
        try:
            if hasattr(Log, "Eventos"):
                Eventos = Log.Eventos() or []
        except Exception:
            Eventos = []
        PorNivel = {}
        for E in Eventos:
            N = str(E.get("nivel") or E.get("level") or "info")
            PorNivel[N] = PorNivel.get(N, 0) + 1
        return {"ok": True, "total_eventos": len(Eventos),
                "por_nivel": PorNivel, "ultimos": Eventos[-50:]}
