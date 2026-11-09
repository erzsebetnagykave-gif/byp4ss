#!/usr/bin/env python3
# byp4ss_cli.py — CLI de operacao do ByP4ss (parte 1/4: casca visual).
# PascalCase em tudo que e nosso. stdlib fica como esta.

import os
import sys
import re
import json
import time
import shlex
import readline


# ============================================================
# CONSTANTES
# ============================================================

class Constantes:
    Versao = "1.0"
    Nome = "byp4ss"
    Autor = "CyberneticCrown"
    PromptBase = "agent.byp4ss"
    PromptSeta = "> "
    HistoricoPath = os.path.join(os.path.expanduser("~"), ".console", "byp4ss_history")
    HistoricoMax = 1000
    TimeoutPadrao = 30.0
    SpinnerFrames = ["|", "/", "-", "\\", "|", "/", "-", "\\"]
    SpinnerDelay = 0.12
    LarguraMinima = 60
    LarguraMaxima = 200
    Separador = "-"


# ============================================================
# CORES
# ============================================================

class Cores:
    Reset = "\033[0m"
    Bold = "\033[1m"
    Cinza = "\033[90m"
    CinzaBold = "\033[1;90m"
    Branco = "\033[97m"
    Ciano = "\033[36m"
    Verde = "\033[32m"
    Amarelo = "\033[33m"
    Vermelho = "\033[31m"
    VermelhoBold = "\033[1;31m"

    @staticmethod
    def Ativo(Forcar=None):
        if Forcar is not None:
            return bool(Forcar)
        if not sys.stdout.isatty():
            return False
        if os.environ.get("NO_COLOR"):
            return False
        if os.environ.get("TERM") == "dumb":
            return False
        return True


# ============================================================
# PARSER DE LINHA
# ============================================================

def ParserLinha(Linha):
    """ParserLinha('scan 192.168.0.1 porta=80') -> ('scan', {'alvo':'192.168.0.1','porta':'80'}, [])"""
    Linha = (Linha or "").strip()
    if not Linha:
        return "", {}, []
    try:
        Partes = shlex.split(Linha)
    except ValueError:
        Partes = Linha.split()
    if not Partes:
        return "", {}, []
    Comando = Partes[0].lower()
    Args = {}
    Extra = []
    for P in Partes[1:]:
        if "=" in P and not P.startswith("="):
            K, V = P.split("=", 1)
            if K:
                Args[K.lower()] = V
        elif "." in P and all(Parte.isdigit() for Parte in P.split(".") if Parte):
            if "alvo" not in Args:
                Args["alvo"] = P
            else:
                Extra.append(P)
        else:
            Extra.append(P)
    if Extra and "alvo" not in Args:
        Args["alvo"] = Extra[0]
        Extra = Extra[1:]
    return Comando, Args, Extra


def ParsearPortas(Texto, Default=None):
    """ParsearPortas('22,80,1-10') -> [1..10, 22, 80]"""
    if not Texto:
        return list(Default or [])
    Portas = set()
    for Parte in str(Texto).split(","):
        P = Parte.strip()
        if not P:
            continue
        if "-" in P:
            try:
                A, B = P.split("-", 1)
                Inicio = int(A)
                Fim = int(B)
                if 0 < Inicio <= Fim <= 65535:
                    Portas.update(range(Inicio, Fim + 1))
            except (ValueError, TypeError):
                pass
        else:
            try:
                V = int(P)
                if 0 < V <= 65535:
                    Portas.add(V)
            except (ValueError, TypeError):
                pass
    return sorted(Portas) if Portas else list(Default or [])


# ============================================================
# FORMATACAO (tabela + texto)
# ============================================================

class Formatar:

    @staticmethod
    def LarguraTerminal(Default=80):
        try:
            return max(Constantes.LarguraMinima,
                       min(shutil_terminal_width(), Constantes.LarguraMaxima))
        except Exception:
            return Default

    @staticmethod
    def Tabela(Cabecalho, Linhas, CoresStatus=None, CorPorLinha=None):
        """Cabecalho: [str]. Linhas: [[str]]. CorPorLinha: funcao que retorna cor."""
        if not Cabecalho:
            return ""
        if not Linhas:
            return Cores.Cinza + "(vazio)" + Cores.Reset if Cores.Ativo() else "(vazio)"
        N = len(Cabecalho)
        Larguras = [len(str(C)) for C in Cabecalho]
        for L in Linhas:
            for I in range(min(N, len(L))):
                Larguras[I] = max(Larguras[I], len(str(L[I])))
        UseCor = Cores.Ativo()
        Out = []
        CabFmt = "  ".join(C.ljust(Larguras[I]) for I, C in enumerate(Cabecalho))
        if UseCor:
            Out.append(Cores.CinzaBold + "  " + CabFmt + Cores.Reset)
            Out.append(Cores.Cinza + "  " + "  ".join("-" * Larguras[I] for I in range(N)) + Cores.Reset)
        else:
            Out.append("  " + CabFmt)
            Out.append("  " + "  ".join("-" * Larguras[I] for I in range(N)))
        for L in Linhas:
            Celulas = []
            for I in range(N):
                Valor = str(L[I]) if I < len(L) else ""
                Celulas.append(Valor.ljust(Larguras[I]))
            LinhaFmt = "  " + "  ".join(Celulas)
            if UseCor and CorPorLinha is not None:
                Cor = CorPorLinha(L)
                if Cor:
                    LinhaFmt = Cor + LinhaFmt + Cores.Reset
            Out.append(LinhaFmt)
        return "\n".join(Out)

    @staticmethod
    def Status(Texto, Tipo="info"):
        if not Cores.Ativo():
            return f"[{Tipo}] {Texto}"
        Mapa = {
            "ok": Cores.Verde, "err": Cores.Vermelho, "warn": Cores.Amarelo,
            "info": Cores.Cinza, "destaque": Cores.Ciano,
        }
        Cor = Mapa.get(Tipo, Cores.Cinza)
        return f"{Cor}[{Tipo}]{Cores.Reset} {Texto}"

    @staticmethod
    def Severidade(Texto, Severidade):
        if not Cores.Ativo():
            return Texto
        Mapa = {
            "critica": Cores.VermelhoBold, "alta": Cores.Vermelho,
            "media": Cores.Amarelo, "baixa": Cores.Cinza, "info": Cores.Cinza,
        }
        Cor = Mapa.get((Severidade or "").lower(), Cores.Cinza)
        return Cor + Texto + Cores.Reset

    @staticmethod
    def Truncar(Texto, Maximo):
        Texto = str(Texto)
        if len(Texto) <= Maximo:
            return Texto
        return Texto[: max(0, Maximo - 1)] + "…"


def shutil_terminal_width():
    import shutil
    return shutil.get_terminal_size().columns


# ============================================================
# HISTORICO
# ============================================================

class Historico:

    def __init__(self, Caminho=None):
        self.Caminho = Caminho or Constantes.HistoricoPath
        self.Entradas = []

    def Carregar(self):
        if not os.path.isfile(self.Caminho):
            return {"Ok": True, "Total": 0, "Motivo": "arquivo_novo"}
        try:
            readline.read_history_file(self.Caminho)
            self.Entradas = list(readline.get_history_item(I + 1)
                                 for I in range(readline.get_current_history_length())
                                 if readline.get_history_item(I + 1))
            return {"Ok": True, "Total": len(self.Entradas)}
        except Exception as E:
            return {"Ok": False, "Motivo": f"leitura_falhou:{type(E).__name__}",
                    "Erro": str(E), "Total": 0}

    def Salvar(self):
        try:
            os.makedirs(os.path.dirname(self.Caminho), mode=0o700, exist_ok=True)
            readline.set_history_length(Constantes.HistoricoMax)
            readline.write_history_file(self.Caminho)
            try:
                os.chmod(self.Caminho, 0o600)
            except Exception:
                pass
            return {"Ok": True, "Caminho": self.Caminho}
        except Exception as E:
            return {"Ok": False, "Motivo": f"escrita_falhou:{type(E).__name__}",
                    "Erro": str(E)}

    def Adicionar(self, Linha):
        Linha = (Linha or "").strip()
        if not Linha:
            return
        if self.Entradas and self.Entradas[-1] == Linha:
            return
        self.Entradas.append(Linha)
        if len(self.Entradas) > Constantes.HistoricoMax:
            self.Entradas = self.Entradas[-Constantes.HistoricoMax:]
        try:
            readline.add_history(Linha)
        except Exception:
            pass

    def Ultimas(self, N=10):
        return list(self.Entradas[-N:])


# ============================================================
# STATUS BAR
# ============================================================

class Status:

    @staticmethod
    def Barra(Estado):
        """Estado: {'Modo': 'local', 'Alvo': '192.168.0.1', 'Ultimo': 'scan', 'DuracaoS': 2.3, 'QTable': 4, 'ComandoAtual': None}"""
        if not isinstance(Estado, dict):
            return ""
        Partes = []
        Modo = Estado.get("Modo")
        if Modo:
            Partes.append(f"[{Modo}]")
        Alvo = Estado.get("Alvo")
        if Alvo:
            Partes.append(f"[alvo: {Alvo}]")
        Ultimo = Estado.get("Ultimo")
        if Ultimo:
            Dur = Estado.get("DuracaoS")
            if Dur is not None:
                Partes.append(f"[{Ultimo} {Dur}s]")
            else:
                Partes.append(f"[{Ultimo}]")
        QTable = Estado.get("QTable")
        if QTable is not None:
            Partes.append(f"[qtable: {QTable}p]")
        if Estado.get("ComandoAtual"):
            Partes.append(f"[{Estado['ComandoAtual']}]")
        Texto = " ".join(Partes) if Partes else "[byp4ss]"
        if Cores.Ativo():
            return Cores.Cinza + Texto + Cores.Reset
        return Texto


# ============================================================
# CLI (Main + Teste)
# ============================================================

class Cli:

    @staticmethod
    def Main():
        import argparse
        P = argparse.ArgumentParser(
            prog="byp4ss_cli",
            description="ByP4ss CLI de operacao (interativo)",
        )
        P.add_argument("--exec", default=None, dest="Exec",
                       help="executa 1 comando e sai")
        P.add_argument("--json", action="store_true",
                       help="saida JSON")
        P.add_argument("--no-color", action="store_true", dest="NoColor",
                       help="sem ANSI")
        P.add_argument("--verbose", action="store_true")
        P.add_argument("--teste", action="store_true")
        Args = P.parse_args()
        if Args.NoColor:
            os.environ["NO_COLOR"] = "1"
        if Args.teste:
            return Cli.RodarTeste()
        if Args.Exec:
            print(Formatar.Status(f"exec: {Args.Exec} (parte 2/4 implementa)", "warn"))
            return 0
        print(Formatar.Status(f"byp4ss {Constantes.Versao} — CLI interativa (parte 1/4)", "info"))
        print(Formatar.Status("loop chega na parte 4/4", "warn"))
        return 0

    @staticmethod
    def RodarTeste():
        print("=== TESTE byp4ss_cli v1 (casca) ===")
        print()
        # 1. Cores
        print("[1] Cores")
        assert Cores.Reset == "\033[0m"
        assert Cores.Verde == "\033[32m"
        assert Cores.VermelhoBold == "\033[1;31m"
        print(f"  Cinza={Cores.Cinza!r} Verde={Cores.Verde!r}")
        # 2. ParserLinha
        print("[2] ParserLinha")
        Cmd, Args, Extra = ParserLinha("scan 192.168.0.1 porta=80 threads=20")
        assert Cmd == "scan", Cmd
        assert Args.get("alvo") == "192.168.0.1", Args
        assert Args.get("porta") == "80", Args
        assert Args.get("threads") == "20", Args
        Cmd, Args, Extra = ParserLinha("")
        assert Cmd == "" and Args == {} and Extra == []
        Cmd, Args, Extra = ParserLinha("exploit tplink alvo=10.0.0.1")
        assert Cmd == "exploit", Cmd
        assert Args.get("alvo") == "10.0.0.1"
        assert "tplink" in Extra, Extra
        print(f"  'scan 192.168.0.1 porta=80' -> {Cmd=} {Args=} {Extra=}")
        # 3. ParsearPortas
        print("[3] ParsearPortas")
        assert ParsearPortas("22,80,443") == [22, 80, 443]
        assert ParsearPortas("1-5") == [1, 2, 3, 4, 5]
        assert ParsearPortas("22,80,1-3") == [1, 2, 3, 22, 80]
        assert ParsearPortas("") == []
        assert ParsearPortas("", Default=[22]) == [22]
        print(f"  '22,80,1-3' -> {ParsearPortas('22,80,1-3')}")
        # 4. Tabela
        print("[4] Tabela")
        T = Formatar.Tabela(["PORT", "STATE", "SERVICE"],
                             [["22", "open", "ssh"], ["80", "open", "http"]])
        assert "PORT" in T
        assert "22" in T
        assert "ssh" in T
        print(f"  {len(T.splitlines())} linhas geradas")
        # 5. Status
        print("[5] Status")
        S = Formatar.Status("escaneando 192.168.0.1", "info")
        assert "escaneando" in S
        S2 = Formatar.Status("erro", "err")
        assert "erro" in S2
        print(f"  info: {S!r}")
        print(f"  err:  {S2!r}")
        # 6. Severidade
        print("[6] Severidade")
        Sev = Formatar.Severidade("critica", "critica")
        assert "critica" in Sev
        Sev2 = Formatar.Severidade("info", "info")
        assert "info" in Sev2
        print(f"  critica: {Sev!r}")
        # 7. Historico
        print("[7] Historico")
        H = Historico(Caminho="/tmp/byp4ss_test_history")
        H.Entradas = ["scan 192.168.0.1", "cred 192.168.0.1"]
        assert len(H.Ultimas(5)) == 2
        assert H.Ultimas(1) == ["cred 192.168.0.1"]
        print(f"  entradas: {H.Ultimas(5)}")
        # 8. Status bar
        print("[8] Status bar")
        B = Status.Barra({"Modo": "local", "Alvo": "192.168.0.1",
                          "Ultimo": "scan", "DuracaoS": 2.3, "QTable": 4})
        assert "local" in B
        assert "192.168.0.1" in B
        print(f"  barra: {B!r}")
        print()
        print("TESTE OK")
        return 0


# ============================================================
# BLOCO 2/4 — COMPLETER, SPINNER, OUTPUT, STATUS DINAMICO
# ============================================================

class Completer:
    """Tab completion: comandos + subcomandos + args + paths."""

    ComandosBase = [
        "scan", "analise", "cred", "exploit", "sqli",
        "chain", "upnp", "httpauth", "shell", "servidor",
        "treinar", "qtable", "api", "sessao", "manifesto",
        "status", "help", "clear", "sair", "exit", "quit",
    ]

    Subcomandos = {
        "exploit": ["tplink", "dlink", "tenda7795", "tenda29384",
                    "arcadyan", "iptime"],
        "chain": ["list", "run"],
        "shell": ["reverse", "bind"],
        "servidor": ["http", "ssdp"],
        "sessao": ["list", "save", "load"],
        "manifesto": ["list", "apply", "reverter", "status"],
        "api": ["start", "stop"],
        "qtable": ["reset"],
        "treinar": [],
    }

    ArgsComuns = ["alvo=", "porta=", "threads=", "timeout=", "modo=", "json="]

    def __init__(self):
        self.ComandoAtual = ""
        self.SubcomandoAtual = ""

    def Complete(self, Texto, Estado):
        Buffer = readline.get_line_buffer()
        Partes = Buffer[:readline.get_endidx()].split()
        if not Partes:
            return [C for C in Completer.ComandosBase if C.startswith(Texto)]
        if len(Partes) == 1 and not Buffer.endswith(" "):
            return [C for C in Completer.ComandosBase if C.startswith(Texto)]
        Cmd = Partes[0].lower()
        if Cmd in Completer.Subcomandos and (len(Partes) == 1 or (len(Partes) >= 2 and Buffer.endswith(" "))):
            Subs = Completer.Subcomandos[Cmd]
            if len(Partes) == 1 or (len(Partes) == 2 and not Buffer.endswith(" ")):
                return [S for S in Subs if S.startswith(Texto)]
        if "=" in Texto and not Texto.endswith("="):
            Prefixo = Texto.split("=", 1)[0] + "="
            ValorParcial = Texto.split("=", 1)[1]
            return []
        if Texto.endswith("=") or not Texto:
            return list(Completer.ArgsComuns)
        return [A for A in Completer.ArgsComuns if A.startswith(Texto)]

    def Instalar(self):
        try:
            readline.set_completer(self.Complete)
            readline.parse_and_bind("tab: complete")
            try:
                readline.set_completer_delims(" \t\n;|&")
            except Exception:
                pass
            return {"Ok": True}
        except Exception as E:
            return {"Ok": False, "Motivo": f"readline_falhou:{type(E).__name__}",
                    "Erro": str(E)}


class Spinner:
    """Thread que mostra |/-\\ enquanto comando executa. Para quando Terminar()."""

    def __init__(self, Ativo=None):
        self.Ativo = Cores.Ativo() if Ativo is None else bool(Ativo)
        self.Rodando = False
        self._Thread = None
        self._Evento = None

    def Iniciar(self, Texto=""):
        if not self.Ativo or not sys.stdout.isatty():
            return
        import threading
        self.Rodando = True
        self._Evento = threading.Event()
        def Loop():
            I = 0
            while self.Rodando:
                Frame = Constantes.SpinnerFrames[I % len(Constantes.SpinnerFrames)]
                sys.stdout.write(f"\r{Cores.Ciano}{Frame}{Cores.Reset} {Texto}   ")
                sys.stdout.flush()
                I += 1
                time.sleep(Constantes.SpinnerDelay)
                if self._Evento.is_set():
                    break
        self._Thread = threading.Thread(target=Loop, daemon=True)
        self._Thread.start()

    def Terminar(self):
        if not self.Ativo or not sys.stdout.isatty():
            return
        self.Rodando = False
        if self._Evento is not None:
            self._Evento.set()
        if self._Thread is not None:
            try:
                self._Thread.join(timeout=1.0)
            except Exception:
                pass
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()


class Output:
    """Imprime resultado. --json -> JSON cru. Senao, tabela/formatado."""

    @staticmethod
    def Auto(Resultado, Json=False):
        if Json:
            return Output.Json(Resultado)
        if not isinstance(Resultado, dict):
            print(Formatar.Status(str(Resultado), "info"))
            return
        Ok = Resultado.get("ok") if "ok" in Resultado else Resultado.get("Ok")
        Tipo = "ok" if Ok else "err"
        Motivo = Resultado.get("motivo") or Resultado.get("Motivo")
        if not Ok and Motivo:
            print(Formatar.Status(f"falhou: {Motivo}", "err"))
            return
        Tempo = Resultado.get("tempo_ms") or Resultado.get("duracao_s") or Resultado.get("DuracaoS")
        if Tempo is not None:
            Unidade = "ms" if "tempo_ms" in Resultado else "s"
            print(Formatar.Status(f"{Tempo}{Unidade}", Tipo))
        else:
            print(Formatar.Status("ok", Tipo))
        for Chave in ("total", "Total", "portas_abertas", "PortasAbertas", "templates",
                     "credenciais", "Credenciais", "vulneraveis", "Vulneraveis"):
            if Chave in Resultado:
                V = Resultado[Chave]
                if isinstance(V, list):
                    Output.Lista(Chave, V)
                else:
                    print(f"  {Chave}: {V}")
        if "episodios" in Resultado:
            print(f"  episodios: {Resultado['episodios']}")
            print(f"  updates: {Resultado.get('transicoes_processadas')}")
            print(f"  pares: {Resultado.get('n_pares_final')}")

    @staticmethod
    def Json(Resultado):
        try:
            print(json.dumps(Resultado, indent=2, ensure_ascii=False, default=str))
        except Exception:
            print(str(Resultado))

    @staticmethod
    def Lista(Nome, Itens):
        if not Itens:
            return
        if isinstance(Itens[0], dict):
            Cabecalho = list(Itens[0].keys())[:6]
            Linhas = [[str(Item.get(C, ""))[:40] for C in Cabecalho] for Item in Itens]
            print(Formatar.Tabela(Cabecalho, Linhas))
        else:
            for Item in Itens[:20]:
                print(f"  {Item}")
            if len(Itens) > 20:
                print(f"  ... (+{len(Itens) - 20})")


class StatusDinamico:
    """Thread que atualiza status bar a cada 500ms (só TTY)."""

    def __init__(self):
        self.Estado = {"Modo": "local"}
        self.Rodando = False
        self._Thread = None

    def Atualizar(self, **Kwargs):
        self.Estado.update(Kwargs)

    def Iniciar(self):
        if not sys.stdout.isatty():
            return
        import threading
        self.Rodando = True
        def Loop():
            while self.Rodando:
                time.sleep(0.5)
        self._Thread = threading.Thread(target=Loop, daemon=True)
        self._Thread.start()

    def Parar(self):
        self.Rodando = False

    def Render(self):
        Barra = Status.Barra(self.Estado)
        return Barra


# ============================================================
# BLOCO 3/4 — HANDLERS DE COMANDO
# ============================================================

class Handlers:
    """Cada handler chama um modulo real do ByP4ss. Sem stub."""

    @staticmethod
    def Executar(Comando, Args, Extra, Estado):
        Cmd = (Comando or "").lower()
        if not Cmd:
            return {"ok": False, "motivo": "comando_vazio"}
        CmdPascal = Cmd[0].upper() + Cmd[1:] if len(Cmd) > 1 else Cmd.upper()
        Handler = getattr(Handlers, f"_Cmd_{CmdPascal}", None)
        if Handler is None:
            Handler = getattr(Handlers, f"_Cmd_{Cmd}", None)
        if Handler is None:
            return {"ok": False, "motivo": f"comando_desconhecido:{Cmd}"}
        try:
            return Handler(Args, Extra, Estado)
        except Exception as E:
            return {"ok": False, "motivo": f"excecao:{type(E).__name__}",
                    "erro": str(E)}

    # ---------- scan / analise / cred ----------

    @staticmethod
    def _Cmd_Scan(Args, Extra, Estado):
        try:
            from Core.Engine import Engine
            from Core.Config import Config
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        Alvo = Args.get("alvo")
        if not Alvo:
            return {"ok": False, "motivo": "alvo_ausente"}
        Portas = ParsearPortas(Args.get("portas"), None)
        if Portas:
            Config.Portas = Portas
        Config.Threads = int(Args.get("threads", Config.Threads))
        Config.Timeout = float(Args.get("timeout", Config.Timeout))
        Config.Salvar = True
        if not Engine._Iniciado:
            Engine.Iniciar(Config)
        R = Engine.Discover(Alvo)
        return {"ok": True, "alvo": Alvo,
                "portas_abertas": R.get("portas_abertas") or [],
                "ssdp": R.get("ssdp"),
                "fingerprint": R.get("fingerprint"),
                "cves_sugeridas": R.get("cves_sugeridas") or []}

    @staticmethod
    def _Cmd_Analise(Args, Extra, Estado):
        try:
            from Analise import Analise
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        Alvo = Args.get("alvo")
        if not Alvo:
            return {"ok": False, "motivo": "alvo_ausente"}
        return Analise.EscanearAlvo(Alvo)

    @staticmethod
    def _Cmd_Cred(Args, Extra, Estado):
        try:
            from Core.Engine import Engine
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        Alvo = Args.get("alvo")
        if not Alvo:
            return {"ok": False, "motivo": "alvo_ausente"}
        R = Engine.Credenciais(Alvo)
        return {"ok": R.get("ok", False), "alvo": Alvo,
                "credenciais": R.get("credenciais") or [],
                "total": R.get("total", 0),
                "motivo": R.get("motivo")}

    # ---------- sqli ----------

    @staticmethod
    def _Cmd_Sqli(Args, Extra, Estado):
        try:
            from Discovery.SqliScan import SqliScan
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        Alvo = Args.get("alvo")
        if not Alvo:
            return {"ok": False, "motivo": "alvo_ausente"}
        Porta = int(Args.get("porta", 80))
        return SqliScan.Escanear(Alvo, Porta)

    # ---------- exploit ----------

    @staticmethod
    def _Cmd_Exploit(Args, Extra, Estado):
        try:
            from Core.Engine import Engine
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        if not Extra:
            return {"ok": False, "motivo": "exploit_id_ausente",
                    "comandos": ["tplink", "dlink", "tenda7795",
                                "tenda29384", "arcadyan", "iptime"]}
        ExploitId = Extra[0].lower()
        Alvo = Args.get("alvo")
        if not Alvo:
            return {"ok": False, "motivo": "alvo_ausente"}
        Modo = Args.get("modo", "auto")
        return Engine.Exploit(ExploitId, Alvo, modo=Modo)

    # ---------- chain ----------

    @staticmethod
    def _Cmd_Chain(Args, Extra, Estado):
        try:
            from Cadeia import Cadeia
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        Sub = Extra[0].lower() if Extra else "list"
        if Sub == "list":
            return Cadeia.Templates()
        if Sub == "run":
            Nome = Extra[1] if len(Extra) > 1 else None
            Alvo = Args.get("alvo")
            if not Nome or not Alvo:
                return {"ok": False, "motivo": "chain_nome_e_alvo_obrigatorios"}
            return Cadeia.Executar(Nome, Alvo)
        return {"ok": False, "motivo": f"chain_sub_desconhecido:{Sub}"}

    # ---------- bypass ----------

    @staticmethod
    def _Cmd_Upnp(Args, Extra, Estado):
        try:
            from Bypass.UpnpBypass import UpnpBypass
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        Alvo = Args.get("alvo")
        if not Alvo:
            return {"ok": False, "motivo": "alvo_ausente"}
        Porta = int(Args.get("porta", 23))
        return UpnpBypass.Tentar(Alvo, Porta=Porta)

    @staticmethod
    def _Cmd_Httpauth(Args, Extra, Estado):
        try:
            from Bypass.HttpAuth import HttpAuth
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        Alvo = Args.get("alvo")
        if not Alvo:
            return {"ok": False, "motivo": "alvo_ausente"}
        Caminho = Args.get("caminho", "/admin")
        return HttpAuth.TestarTraversal(Alvo, Caminho)

    # ---------- shells ----------

    @staticmethod
    def _Cmd_Shell(Args, Extra, Estado):
        Sub = Extra[0].lower() if Extra else None
        if Sub == "reverse":
            try:
                from ExploitByp4ss.Aux1l14r3s.Shells.ReverseShell import ReverseShell
            except Exception as E:
                return {"ok": False, "motivo": f"import_falhou:{E}"}
            Host = Args.get("host")
            Porta = int(Args.get("porta", 4444))
            if not Host:
                return {"ok": False, "motivo": "host_ausente"}
            try:
                Ok = ReverseShell.Tcp(Host, Porta)
                return {"ok": bool(Ok), "host": Host, "porta": Porta,
                        "protocolo": "tcp"}
            except Exception as E:
                return {"ok": False, "motivo": f"excecao:{type(E).__name__}",
                        "erro": str(E)}
        if Sub == "bind":
            try:
                from ExploitByp4ss.Aux1l14r3s.Shells.BindShell import BindShell
            except Exception as E:
                return {"ok": False, "motivo": f"import_falhou:{E}"}
            Porta = int(Args.get("porta", 4444))
            try:
                R = BindShell.Tcp(Porta)
                if R:
                    return {"ok": True, "porta": R.get("porta"),
                            "protocolo": "tcp"}
                return {"ok": False, "motivo": "bind_falhou"}
            except Exception as E:
                return {"ok": False, "motivo": f"excecao:{type(E).__name__}",
                        "erro": str(E)}
        return {"ok": False, "motivo": f"shell_sub_desconhecido:{Sub}",
                "opcoes": ["reverse", "bind"]}

    # ---------- servidores ----------

    @staticmethod
    def _Cmd_Servidor(Args, Extra, Estado):
        Sub = Extra[0].lower() if Extra else None
        try:
            from ExploitByp4ss.Aux1l14r3s.Servers.SsdpFalso import SsdpFalso
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        if Sub == "http":
            Porta = int(Args.get("porta", 8080))
            try:
                R = SsdpFalso.IniciarHttp(Porta=Porta)
                return {"ok": True, "porta": Porta, "tipo": "http",
                        "detalhe": R}
            except Exception as E:
                return {"ok": False, "motivo": f"excecao:{type(E).__name__}",
                        "erro": str(E)}
        if Sub == "ssdp":
            Porta = int(Args.get("porta", 1900))
            try:
                R = SsdpFalso.IniciarSsdp(Porta=Porta)
                return {"ok": True, "porta": Porta, "tipo": "ssdp",
                        "detalhe": R}
            except Exception as E:
                return {"ok": False, "motivo": f"excecao:{type(E).__name__}",
                        "erro": str(E)}
        return {"ok": False, "motivo": f"servidor_sub_desconhecido:{Sub}",
                "opcoes": ["http", "ssdp"]}

    # ---------- treino / qtable ----------

    @staticmethod
    def _Cmd_Treinar(Args, Extra, Estado):
        try:
            from Treino import QTable, Treinar
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        N = 100
        if Extra:
            try:
                N = int(Extra[0])
            except (ValueError, IndexError):
                pass
        Q = QTable()
        Q.Carregar()
        R = Treinar(Q, Episodios=N)
        if R.get("ok"):
            R["salvo"] = Q.Salvar()
        return R

    @staticmethod
    def _Cmd_Qtable(Args, Extra, Estado):
        Sub = Extra[0].lower() if Extra else None
        if Sub == "reset":
            Caminho = os.path.join(os.path.expanduser("~"),
                                   ".console", "qtable.json")
            if os.path.isfile(Caminho):
                try:
                    os.remove(Caminho)
                    return {"ok": True, "removido": Caminho}
                except Exception as E:
                    return {"ok": False, "motivo": f"remove_falhou:{E}"}
            return {"ok": True, "motivo": "nao_existia"}
        try:
            from Treino import QTable, MostrarQTable
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        Q = QTable()
        R = Q.Carregar()
        if not R.get("ok"):
            return {"ok": False, "motivo": R.get("motivo")}
        MostrarQTable(Q, Top=10)
        return {"ok": True, "n_pares": Q._ContarPares(),
                "n_estados": len(Q.Dados)}

    # ---------- api ----------

    @staticmethod
    def _Cmd_Api(Args, Extra, Estado):
        Sub = Extra[0].lower() if Extra else "start"
        try:
            from Api import Api
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        if Sub == "start":
            Porta = int(Args.get("porta", 8765))
            R = Api.Iniciar(Escuta="127.0.0.1", Porta=Porta)
            return R
        if Sub == "stop":
            return Api.Parar()
        return {"ok": False, "motivo": f"api_sub_desconhecido:{Sub}",
                "opcoes": ["start", "stop"]}

    # ---------- sessao ----------

    @staticmethod
    def _Cmd_Sessao(Args, Extra, Estado):
        Sub = Extra[0].lower() if Extra else "list"
        try:
            from Sessao import Sessao
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        if Sub == "list":
            return Sessao.Listar()
        if Sub == "save":
            Nome = Extra[1] if len(Extra) > 1 else None
            if not Nome:
                return {"ok": False, "motivo": "nome_ausente"}
            Estado_ = {"modo": Estado.get("Modo", "local"),
                       "alvo": Estado.get("Alvo", "")}
            return Sessao.Salvar(Nome, Estado_)
        if Sub == "load":
            Nome = Extra[1] if len(Extra) > 1 else None
            if not Nome:
                return {"ok": False, "motivo": "nome_ausente"}
            return Sessao.Carregar(Nome)
        return {"ok": False, "motivo": f"sessao_sub_desconhecido:{Sub}",
                "opcoes": ["list", "save", "load"]}

    # ---------- manifesto ----------

    @staticmethod
    def _Cmd_Manifesto(Args, Extra, Estado):
        Sub = Extra[0].lower() if Extra else "list"
        try:
            from Manifesto import Manifesto, Motor
        except Exception as E:
            return {"ok": False, "motivo": f"import_falhou:{E}"}
        if Sub == "list":
            return Manifesto.Listar()
        if Sub == "apply":
            Id = Extra[1] if len(Extra) > 1 else None
            if not Id:
                return {"ok": False, "motivo": "manifesto_id_ausente"}
            return Motor.Aplicar(Id)
        if Sub == "reverter":
            Id = Extra[1] if len(Extra) > 1 else None
            if not Id:
                return {"ok": False, "motivo": "manifesto_id_ausente"}
            return Motor.Reverter(Id)
        if Sub == "status":
            return Motor.ListarAplicados()
        return {"ok": False, "motivo": f"manifesto_sub_desconhecido:{Sub}",
                "opcoes": ["list", "apply", "reverter", "status"]}

    # ---------- status / help / clear / sair ----------

    @staticmethod
    def _Cmd_Status(Args, Extra, Estado):
        return {"ok": True, "estado": dict(Estado)}

    @staticmethod
    def _Cmd_Help(Args, Extra, Estado):
        Linhas = []
        try:
            from RegistroComandos import RegistroComandos
            R = RegistroComandos.Ajuda()
            if R.get("texto"):
                Linhas.append(R["texto"])
        except Exception:
            pass
        Linhas.append("")
        Linhas.append("comandos da CLI:")
        Linhas.append("  scan <alvo>                  — port scan + ssdp")
        Linhas.append("  analise <alvo>               — analise consolidada")
        Linhas.append("  cred <alvo>                  — credenciais")
        Linhas.append("  sqli <alvo> [porta=80]       — sql injection")
        Linhas.append("  exploit <id> <alvo>          — exploit (tplink, dlink, ...)")
        Linhas.append("  chain list                   — templates de kill chain")
        Linhas.append("  chain run <nome> <alvo>      — executa cadeia")
        Linhas.append("  upnp <alvo>                  — upnp bypass")
        Linhas.append("  httpauth <alvo>              — http auth bypass")
        Linhas.append("  shell reverse <host> <porta> — reverse shell")
        Linhas.append("  shell bind <porta>           — bind shell")
        Linhas.append("  servidor http|ssdp [porta=]  — servidor falso")
        Linhas.append("  treinar [N]                  — Q-Learning (default 100)")
        Linhas.append("  qtable [reset]               — mostra/limpa QTable")
        Linhas.append("  api start|stop [porta=]      — API REST")
        Linhas.append("  sessao list|save|load        — sessoes")
        Linhas.append("  manifesto list|apply|reverter — manifestos")
        Linhas.append("  status                       — estado atual")
        Linhas.append("  help / ?                     — ajuda")
        Linhas.append("  clear                        — limpa tela")
        Linhas.append("  sair / exit / quit           — encerra")
        return {"ok": True, "texto": "\n".join(Linhas)}

    @staticmethod
    def _Cmd_Clear(Args, Extra, Estado):
        return {"ok": True, "ansi_clear": True}

    @staticmethod
    def _Cmd_Sair(Args, Extra, Estado):
        return {"ok": True, "sair": True}

    _Cmd_Exit = _Cmd_Sair
    _Cmd_Quit = _Cmd_Sair


# ============================================================
# BLOCO 4/4 — LOOP INTERATIVO, MAIN, TESTE INTEGRADO
# ============================================================

class LoopInterativo:
    """Prompt agent.byp4ss > com histórico, Tab, spinner."""

    @staticmethod
    def Prompt():
        UseCor = Cores.Ativo()
        if UseCor:
            return f"{Cores.Cinza}{Constantes.PromptBase}{Cores.Reset} {Cores.Bold}>{Cores.Reset} "
        return f"{Constantes.PromptBase} > "

    @staticmethod
    def Executar(Estado, CompleterInst, HistoricoInst, Args):
        CompleterInst.Instalar()
        HistoricoInst.Carregar()
        UseCor = Cores.Ativo()
        print(Formatar.Status(f"{Constantes.Nome} {Constantes.Versao} — type help for commands", "info"))
        if UseCor:
            print(Cores.Cinza + "  " + Constantes.Separador * 50 + Cores.Reset)
        print()
        while True:
            try:
                Linha = input(LoopInterativo.Prompt())
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print()
                continue
            Linha = Linha.strip()
            if not Linha:
                continue
            HistoricoInst.Adicionar(Linha)
            Comando, ArgsCmd, Extra = ParserLinha(Linha)
            if not Comando:
                continue
            if Comando in ("sair", "exit", "quit", "q"):
                break
            if Comando == "clear":
                sys.stdout.write("\033[2J\033[H")
                sys.stdout.flush()
                continue
            SpinnerInst = Spinner()
            Inicio = time.monotonic()
            SpinnerInst.Iniciar(f"executando {Comando}...")
            try:
                Resultado = Handlers.Executar(Comando, ArgsCmd, Extra, Estado)
            except Exception as E:
                Resultado = {"ok": False, "motivo": f"excecao:{type(E).__name__}",
                             "erro": str(E)}
            Duracao = round(time.monotonic() - Inicio, 2)
            SpinnerInst.Terminar()
            if isinstance(Resultado, dict):
                Resultado.setdefault("duracao_s", Duracao)
            if Resultado.get("ansi_clear"):
                sys.stdout.write("\033[2J\033[H")
                sys.stdout.flush()
                continue
            if Resultado.get("sair"):
                break
            Estado["Ultimo"] = Comando
            Estado["DuracaoS"] = Duracao
            if ArgsCmd.get("alvo"):
                Estado["Alvo"] = ArgsCmd["alvo"]
            Output.Auto(Resultado, Json=Args.Json)
            if Resultado.get("ok") and UseCor:
                print(Cores.Cinza + "  " + Constantes.Separador * 30 + Cores.Reset)
        HistoricoInst.Salvar()
        print(Formatar.Status("bye.", "info"))
        return 0


class Main:

    @staticmethod
    def Run():
        import argparse
        P = argparse.ArgumentParser(
            prog="byp4ss_cli",
            description="ByP4ss — CLI de operacao (agent.byp4ss >)",
        )
        P.add_argument("--exec", default=None, dest="Exec",
                       help="executa 1 comando e sai")
        P.add_argument("--json", action="store_true", dest="Json",
                       help="saida JSON")
        P.add_argument("--no-color", action="store_true", dest="NoColor")
        P.add_argument("--verbose", action="store_true")
        P.add_argument("--teste", action="store_true")
        Args = P.parse_args()
        if Args.NoColor:
            os.environ["NO_COLOR"] = "1"
        if Args.teste:
            return Main.TesteIntegracao()
        if Args.Exec:
            Estado = {"Modo": "local", "Alvo": ""}
            Comando, ArgsCmd, Extra = ParserLinha(Args.Exec)
            if not Comando:
                print(Formatar.Status("comando vazio", "err"))
                return 1
            try:
                Resultado = Handlers.Executar(Comando, ArgsCmd, Extra, Estado)
            except Exception as E:
                Resultado = {"ok": False, "motivo": f"excecao:{type(E).__name__}",
                             "erro": str(E)}
            Output.Auto(Resultado, Json=Args.Json)
            return 0 if Resultado.get("ok") else 1
        Estado = {"Modo": "local", "Alvo": ""}
        CompleterInst = Completer()
        HistoricoInst = Historico()
        return LoopInterativo.Executar(Estado, CompleterInst, HistoricoInst, Args)

    @staticmethod
    def TesteIntegracao():
        print("=== TESTE INTEGRACAO byp4ss_cli ===")
        print()
        Estado = {"Modo": "local", "Alvo": ""}
        # 1. scan
        print("[1] scan 127.0.0.1")
        R = Handlers.Executar("scan", {"alvo": "127.0.0.1", "portas": "53", "threads": "1"}, [], Estado)
        assert R.get("ok"), R
        assert "fingerprint" in R
        print(f"  ok, {len(R.get('portas_abertas', []))} portas")
        # 2. sqli
        print("[2] sqli 127.0.0.1")
        R = Handlers.Executar("sqli", {"alvo": "127.0.0.1", "porta": "80"}, [], Estado)
        assert R.get("ok"), R
        assert "total" in R
        print(f"  ok, via {R.get('via')}, total {R.get('total')}")
        # 3. cred
        print("[3] cred 127.0.0.1")
        R = Handlers.Executar("cred", {"alvo": "127.0.0.1"}, [], Estado)
        assert isinstance(R, dict)
        print(f"  ok={R.get('ok')}, total={R.get('total', 0)}")
        # 4. chain list
        print("[4] chain list")
        R = Handlers.Executar("chain", {}, ["list"], Estado)
        assert R.get("ok"), R
        N_Templates = len(R.get("templates") or [])
        print(f"  templates: {N_Templates}")
        # 5. sessao list
        print("[5] sessao list")
        R = Handlers.Executar("sessao", {}, ["list"], Estado)
        assert R.get("ok"), R
        print(f"  sessoes: {R.get('total')}")
        # 6. manifesto list
        print("[6] manifesto list")
        R = Handlers.Executar("manifesto", {}, ["list"], Estado)
        assert R.get("ok"), R
        print(f"  manifestos: {R.get('total')}")
        # 7. help
        print("[7] help")
        R = Handlers.Executar("help", {}, [], Estado)
        assert R.get("ok"), R
        assert "scan" in R.get("texto", "")
        print(f"  {len(R.get('texto', '').splitlines())} linhas")
        # 8. comando desconhecido
        print("[8] comando desconhecido")
        R = Handlers.Executar("xyzabc", {}, [], Estado)
        assert R.get("ok") is False
        assert "comando_desconhecido" in R.get("motivo", "")
        print(f"  {R.get('motivo')}")
        print()
        print("TESTE OK byp4ss_cli")
        return 0


if __name__ == "__main__":
    sys.exit(Main.Run())
