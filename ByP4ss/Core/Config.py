# Config do ByP4ss
# Gerencia configuracao em runtime

import os
import json
from Core.Constants import Constants


class Config:

    Alvo = Constants.ALVO_PADRAO
    Porta = 23
    PortaInterna = 23
    Protocolo = "TCP"
    Timeout = Constants.TIMEOUT_PADRAO
    TimeoutSSDP = Constants.TIMEOUT_SSDP
    TimeoutTCP = Constants.TIMEOUT_TCP
    TimeoutHTTP = Constants.TIMEOUT_HTTP
    TimeoutTelnet = Constants.TIMEOUT_TELNET
    TimeoutDNS = Constants.TIMEOUT_DNS
    TimeoutUPNP = Constants.TIMEOUT_UPNP
    TimeoutVerify = Constants.TIMEOUT_VERIFY

    Threads = Constants.THREADS_PADRAO
    ThreadsPorts = Constants.THREADS_PORTS
    ThreadsFuzz = Constants.THREADS_FUZZ
    ThreadsBrute = Constants.THREADS_BRUTE

    Verbose = False
    Json = False
    DryRun = False
    Salvar = True
    Modo = "normal"

    ModoParanoid = False
    ModoFurtivo = False
    ModoAgressivo = False

    Portas = Constants.PORTAS_CRITICAS
    PortasExtras = Constants.PORTAS_TODAS

    FuzzIteracoes = Constants.FUZZ_ITERACOES
    FuzzSemente = Constants.FUZZ_SEMENTE
    FuzzAmostras = Constants.FUZZ_RESONANCE_AMOSTRAS

    HoneypotLimite = Constants.HONEYPOT_SCORE_LIMITE
    HoneypotAbortar = True

    CveAtivo = True
    CveDbPath = ""
    CveLimite = 50

    DirTmp = Constants.DIR_TMP
    DirReports = Constants.DIR_REPORTS
    DirLogs = Constants.DIR_LOGS
    DirCache = Constants.DIR_CACHE

    UserAgent = Constants.HTTP_HEADERS_PADRAO["User-Agent"]
    Headers = dict(Constants.HTTP_HEADERS_PADRAO)

    DicionarioCred = list(Constants.DIC_CREDENCIAIS)
    DicionarioPortas = list(Constants.DIC_PORTS_WORDLIST)

    Chamadas = 0
    InicioTs = 0.0
    FimTs = 0.0

    Encontrados = []
    Erros = []
    Alertas = []

    @staticmethod
    def Iniciar(Args=None):
        if Args is not None:
            Config.AplicarArgs(Args)
        Config.CriarDirs()
        Config.Chamadas = 0
        Config.Encontrados = []
        Config.Erros = []
        Config.Alertas = []

    @staticmethod
    def AplicarArgs(Args):
        if hasattr(Args, "alvo") and Args.alvo:
            Config.Alvo = Args.alvo
        if hasattr(Args, "porta") and Args.porta:
            Config.Porta = Args.porta
            Config.PortaInterna = Args.porta
        if hasattr(Args, "protocolo") and Args.protocolo:
            Config.Protocolo = Args.protocolo
        if hasattr(Args, "timeout") and Args.timeout:
            Config.Timeout = Args.timeout
        if hasattr(Args, "threads") and Args.threads:
            Config.Threads = Args.threads
            Config.ThreadsPorts = Args.threads
            Config.ThreadsFuzz = Args.threads
        if hasattr(Args, "verbose"):
            Config.Verbose = Args.verbose
        if hasattr(Args, "json"):
            Config.Json = Args.json
        if hasattr(Args, "dry_run"):
            Config.DryRun = Args.dry_run
        if hasattr(Args, "modo") and Args.modo:
            Config.Modo = Args.modo
            Config.AplicarModo(Args.modo)

    @staticmethod
    def AplicarModo(Modo):
        Config.ModoParanoid = False
        Config.ModoFurtivo = False
        Config.ModoAgressivo = False
        if Modo == "paranoid":
            Config.ModoParanoid = True
            Config.Threads = 1
            Config.ThreadsPorts = 1
            Config.ThreadsFuzz = 1
            Config.Timeout = Config.Timeout * 2
        elif Modo == "furtivo":
            Config.ModoFurtivo = True
            Config.Threads = 3
            Config.ThreadsPorts = 3
            Config.ThreadsFuzz = 3
        elif Modo == "agressivo":
            Config.ModoAgressivo = True
            Config.Threads = 50
            Config.ThreadsPorts = 50
            Config.ThreadsFuzz = 20

    @staticmethod
    def CriarDirs():
        for D in [Config.DirTmp, Config.DirReports, Config.DirLogs, Config.DirCache]:
            os.makedirs(D, exist_ok=True)

    @staticmethod
    def LimparCache():
        for F in os.listdir(Config.DirCache):
            try:
                os.remove(os.path.join(Config.DirCache, F))
            except OSError:
                pass

    @staticmethod
    def ToDict():
        return {
            "alvo": Config.Alvo,
            "porta": Config.Porta,
            "protocolo": Config.Protocolo,
            "timeout": Config.Timeout,
            "threads": Config.Threads,
            "verbose": Config.Verbose,
            "json": Config.Json,
            "dry_run": Config.DryRun,
            "modo": Config.Modo,
            "modo_paranoid": Config.ModoParanoid,
            "modo_furtivo": Config.ModoFurtivo,
            "modo_agressivo": Config.ModoAgressivo,
            "fuzz_iteracoes": Config.FuzzIteracoes,
            "fuzz_semente": Config.FuzzSemente,
            "honeypot_limite": Config.HoneypotLimite,
            "honeypot_abortar": Config.HoneypotAbortar,
            "cve_ativo": Config.CveAtivo,
            "cve_db_path": Config.CveDbPath,
            "cve_limite": Config.CveLimite,
            "dir_tmp": Config.DirTmp,
            "dir_reports": Config.DirReports,
            "dir_logs": Config.DirLogs,
            "dir_cache": Config.DirCache,
            "user_agent": Config.UserAgent,
        }

    @staticmethod
    def ToJson(Indent=2):
        return json.dumps(Config.ToDict(), indent=Indent, ensure_ascii=False)

    @staticmethod
    def DoArquivo(Path):
        try:
            with open(Path, "r", encoding="utf-8") as F:
                Dados = json.load(F)
        except (OSError, json.JSONDecodeError):
            return False
        Config.AplicarDict(Dados)
        return True

    @staticmethod
    def AplicarDict(Dados):
        Mapa = {
            "alvo": "Alvo", "porta": "Porta", "protocolo": "Protocolo",
            "timeout": "Timeout", "threads": "Threads", "verbose": "Verbose",
            "json": "Json", "dry_run": "DryRun", "modo": "Modo",
            "fuzz_iteracoes": "FuzzIteracoes", "fuzz_semente": "FuzzSemente",
            "honeypot_limite": "HoneypotLimite", "honeypot_abortar": "HoneypotAbortar",
            "cve_ativo": "CveAtivo", "cve_db_path": "CveDbPath", "cve_limite": "CveLimite",
            "dir_tmp": "DirTmp", "dir_reports": "DirReports",
            "dir_logs": "DirLogs", "dir_cache": "DirCache",
            "user_agent": "UserAgent",
        }
        for K, V in Dados.items():
            if K in Mapa:
                setattr(Config, Mapa[K], V)

    @staticmethod
    def AdicionarEncontrado(Item):
        Config.Encontrados.append(Item)

    @staticmethod
    def AdicionarErro(Erro):
        Config.Erros.append(Erro)

    @staticmethod
    def AdicionarAlerta(Alerta):
        Config.Alertas.append(Alerta)

    @staticmethod
    def ContarEncontrados():
        return len(Config.Encontrados)

    @staticmethod
    def ContarErros():
        return len(Config.Erros)

    @staticmethod
    def ContarAlertas():
        return len(Config.Alertas)

    @staticmethod
    def Info():
        return {
            "versao": Constants.VERSAO,
            "nome": Constants.NOME,
            "alvo": Config.Alvo,
            "modo": Config.Modo,
            "threads": Config.Threads,
            "timeout": Config.Timeout,
            "encontrados": Config.ContarEncontrados(),
            "erros": Config.ContarErros(),
            "alertas": Config.ContarAlertas(),
        }
