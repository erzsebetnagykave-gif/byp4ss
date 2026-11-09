# FormParser — parseia formulário de login de qualquer roteador
# 300 linhas (parte 1 de 2)
# Le HTML, acha form, campos, CSRF, action, method

import re
import urllib.request
import urllib.error
import ssl
import html
import json

from Core.Constants import Constants
from Core.Config import Config
from Core.Log import Log


class FormParser:

    @staticmethod
    def _Ctx():
        Ctx = ssl.create_default_context()
        Ctx.check_hostname = False
        Ctx.verify_mode = ssl.CERT_NONE
        return Ctx

    @staticmethod
    def Fetch(Url, Metodo="GET", Dados=None, Headers=None, Timeout=None):
        Timeout = Timeout or Config.TimeoutHTTP
        Headers = Headers or {
            "User-Agent": Constants.HTTP_HEADERS_PADRAO["User-Agent"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
            "Connection": "close",
        }
        try:
            Req = urllib.request.Request(Url, data=Dados, headers=Headers, method=Metodo)
            Ctx = FormParser._Ctx()
            with urllib.request.urlopen(Req, timeout=Timeout, context=Ctx) as F:
                Corpo = F.read().decode("utf-8", errors="replace")
                return {
                    "ok": True,
                    "status": F.status,
                    "headers": dict(F.headers),
                    "corpo": Corpo,
                    "url_final": F.url,
                }
        except urllib.error.HTTPError as E:
            Corpo = E.read().decode("utf-8", errors="replace") if hasattr(E, "read") else ""
            return {
                "ok": False,
                "status": E.code,
                "headers": dict(E.headers) if E.headers else {},
                "corpo": Corpo,
                "url_final": E.url if hasattr(E, "url") else Url,
            }
        except Exception as E:
            return {"ok": False, "erro": str(E), "status": 0, "corpo": ""}

    @staticmethod
    def ExtrairForms(Html):
        Forms = []
        Padrao = re.compile(r"<form\b([^>]*)>(.*?)</form>", re.DOTALL | re.IGNORECASE)
        for M in Padrao.finditer(Html):
            Atributos = M.group(1)
            Corpo = M.group(2)
            Action = FormParser._ExtrairAtributo(Atributos, "action") or ""
            Method = (FormParser._ExtrairAtributo(Atributos, "method") or "GET").upper()
            Id = FormParser._ExtrairAtributo(Atributos, "id") or ""
            Name = FormParser._ExtrairAtributo(Atributos, "name") or ""
            Inputs = FormParser._ExtrairInputs(Corpo)
            Forms.append({
                "action": html.unescape(Action),
                "method": Method,
                "id": Id,
                "name": Name,
                "inputs": Inputs,
            })
        return Forms

    @staticmethod
    def _ExtrairAtributo(Texto, Nome):
        Padrao = re.compile(rf"{Nome}\s*=\s*[\"']([^\"']*)[\"']", re.IGNORECASE)
        M = Padrao.search(Texto)
        if M:
            return M.group(1).strip()
        Padrao2 = re.compile(rf"{Nome}\s*=\s*([^\s>]+)", re.IGNORECASE)
        M2 = Padrao2.search(Texto)
        if M2:
            return M2.group(1).strip()
        return None

    @staticmethod
    def _ExtrairInputs(CorpoForm):
        Inputs = []
        Padrao = re.compile(r"<input\b([^>]*?)/?>", re.DOTALL | re.IGNORECASE)
        for M in Padrao.finditer(CorpoForm):
            Atributos = M.group(1)
            Tipo = (FormParser._ExtrairAtributo(Atributos, "type") or "text").lower()
            Nome = FormParser._ExtrairAtributo(Atributos, "name") or ""
            Id = FormParser._ExtrairAtributo(Atributos, "id") or ""
            Valor = FormParser._ExtrairAtributo(Atributos, "value") or ""
            Placeholder = FormParser._ExtrairAtributo(Atributos, "placeholder") or ""
            Required = "required" in Atributos.lower()
            if not Nome and not Id:
                continue
            Inputs.append({
                "tipo": Tipo,
                "name": Nome,
                "id": Id,
                "value": html.unescape(Valor),
                "placeholder": html.unescape(Placeholder),
                "required": Required,
            })
        return Inputs

    @staticmethod
    def IdentificarCampos(Form):
        Username = None
        Password = None
        Csrf = None
        Outros = []
        for Input in Form["inputs"]:
            Nome = Input["name"].lower()
            Id = Input["id"].lower()
            Tipo = Input["tipo"]
            Combinado = Nome + " " + Id
            if Tipo == "password" or "password" in Combinado or "passwd" in Combinado or "senha" in Combinado:
                if not Password:
                    Password = Input
                continue
            if any(P in Combinado for P in ("user", "usuario", "login", "account", "email", "usr", "name")):
                if not Username and "pass" not in Combinado:
                    Username = Input
                else:
                    Outros.append(Input)
                continue
            if "csrf" in Combinado or "token" in Combinado or "nonce" in Combinado:
                Csrf = Input
                continue
            if Tipo in ("hidden", "submit", "button", "checkbox", "radio"):
                Outros.append(Input)
                continue
            Outros.append(Input)
        return {
            "username": Username,
            "password": Password,
            "csrf": Csrf,
            "outros": Outros,
        }

    @staticmethod
    def Parsear(Url):
        Log.Info("formparser iniciado", {"url": Url})
        Resultado = {
            "ok": False,
            "url": Url,
            "forms": [],
            "form_login": None,
            "campos": None,
            "motivo": "",
        }
        Resp = FormParser.Fetch(Url)
        if not Resp.get("ok") and Resp.get("status") not in (200, 401, 403):
            Resultado["motivo"] = Resp.get("erro", "fetch_falhou")
            return Resultado
        Corpo = Resp.get("corpo", "")
        if not Corpo:
            Resultado["motivo"] = "sem_conteudo"
            return Resultado

        Forms = FormParser.ExtrairForms(Corpo)
        Resultado["forms"] = Forms
        if not Forms:
            Resultado["motivo"] = "sem_form"
            return Resultado

        FormLogin = FormParser._EscolherFormLogin(Forms)
        if not FormLogin:
            Resultado["motivo"] = "sem_form_login"
            return Resultado

        Resultado["form_login"] = FormLogin
        Resultado["campos"] = FormParser.IdentificarCampos(FormLogin)
        Resultado["ok"] = True
        Resultado["url_final"] = Resp.get("url_final", Url)
        Log.Descoberta("FormParser", Url, "form_encontrado", {
            "action": FormLogin.get("action"),
            "method": FormLogin.get("method"),
            "inputs": len(FormLogin.get("inputs", [])),
        })
        return Resultado

    @staticmethod
    def _EscolherFormLogin(Forms):
        Melhor = None
        MelhorScore = 0
        for Form in Forms:
            Score = 0
            TemSenha = False
            TemUsuario = False
            for Input in Form["inputs"]:
                if Input["tipo"] == "password":
                    Score += 10
                    TemSenha = True
                Nome = Input["name"].lower() + " " + Input["id"].lower()
                if "user" in Nome or "usuario" in Nome or "login" in Nome:
                    Score += 5
                    TemUsuario = True
            if Form["method"] == "POST":
                Score += 3
            Action = Form["action"].lower()
            if "login" in Action or "auth" in Action or "entrar" in Action:
                Score += 5
            if TemSenha:
                if Score > MelhorScore:
                    MelhorScore = Score
                    Melhor = Form
        return Melhor

    @staticmethod
    def MontarDados(Form, Campos, Usuario, Senha, CsrfValor=None):
        Dados = []
        for Input in Form["inputs"]:
            Nome = Input["name"]
            if not Nome:
                continue
            if Campos["username"] and Input is Campos["username"]:
                Dados.append((Nome, Usuario))
            elif Campos["password"] and Input is Campos["password"]:
                Dados.append((Nome, Senha))
            elif Campos["csrf"] and Input is Campos["csrf"]:
                Dados.append((Nome, CsrfValor or Input["value"]))
            else:
                Dados.append((Nome, Input["value"]))
        return Dados

    @staticmethod
    def TentarLogin(Url, Usuario, Senha, CsrfValor=None, Extra=None):
        Parse = FormParser.Parsear(Url)
        if not Parse.get("ok"):
            return {"ok": False, "motivo": Parse.get("motivo"), "sucesso": False}

        Form = Parse["form_login"]
        Campos = Parse["campos"]
        if not Campos.get("password"):
            return {"ok": False, "motivo": "sem_campo_senha", "sucesso": False}

        Dados = FormParser.MontarDados(Form, Campos, Usuario, Senha, CsrfValor)
        if Extra:
            Dados.extend(Extra)
        import urllib.parse
        DadosStr = urllib.parse.urlencode(Dados).encode("utf-8")

        UrlFinal = Parse.get("url_final", Url)
        Action = Form["action"]
        if Action and Action not in ("", "#"):
            if Action.startswith("/"):
                Base = re.match(r"(https?://[^/]+)", UrlFinal)
                if Base:
                    UrlLogin = Base.group(1) + Action
                else:
                    UrlLogin = UrlFinal.rstrip("/") + Action
            elif Action.startswith("http"):
                UrlLogin = Action
            else:
                UrlLogin = UrlFinal.rstrip("/") + "/" + Action
        else:
            UrlLogin = UrlFinal

        Headers = {
            "User-Agent": Constants.HTTP_HEADERS_PADRAO["User-Agent"],
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Connection": "close",
        }

        Resp = FormParser.Fetch(UrlLogin, Metodo="POST", Dados=DadosStr, Headers=Headers)
        Sucesso = FormParser._PareceSucesso(Resp, Usuario, Senha)
        return {
            "ok": True,
            "sucesso": Sucesso,
            "status": Resp.get("status"),
            "url_login": UrlLogin,
            "corpo_trecho": Resp.get("corpo", "")[:500],
            "headers_resposta": Resp.get("headers", {}),
        }

    @staticmethod
    def _PareceSucesso(Resp, Usuario, Senha):
        if not Resp.get("ok"):
            return False
        Status = Resp.get("status", 0)
        if Status == 200:
            Corpo = Resp.get("corpo", "").lower()
            PalavrasErro = [
                "senha inválida", "senha invalida", "senha incorreta",
                "usuario invalido", "usuario inválido", "usuário inválido",
                "usuario incorreto", "usuário incorreto",
                "invalid password", "invalid user", "login failed",
                "login fail", "authentication failed", "falha na autenticação",
                "falha na autenticacao", "acesso negado", "access denied",
                "credenciais invalidas", "credenciais inválidas",
                "incorrect username", "incorrect password", "wrong password",
            ]
            for P in PalavrasErro:
                if P in Corpo:
                    return False
            PalavrasSucesso = [
                "logout", "logoff", "sair", "encerrar", "bem-vindo", "bem vindo",
                "welcome", "dashboard", "painel", "home", "main", "configura",
                "admin", "usuário", "usuario",
            ]
            for P in PalavrasSucesso:
                if P in Corpo:
                    return True
        return False

    @staticmethod
    def Info():
        return {
            "nome": "FormParser",
            "capacidades": [
                "extrair_forms",
                "identificar_campos",
                "montar_post",
                "detectar_csrf",
                "testar_login",
            ],
            "protocolos": ["http_form", "https_form"],
        }

    @staticmethod
    def _ExtrairInputsSoltos(Html):
        Inputs = []
        Padrao = re.compile(r"<input\b([^>]*?)/?>", re.DOTALL | re.IGNORECASE)
        for M in Padrao.finditer(Html):
            Atributos = M.group(1)
            Tipo = (FormParser._ExtrairAtributo(Atributos, "type") or "text").lower()
            Nome = FormParser._ExtrairAtributo(Atributos, "name") or ""
            Id = FormParser._ExtrairAtributo(Atributos, "id") or ""
            Valor = FormParser._ExtrairAtributo(Atributos, "value") or ""
            if not Nome and not Id:
                continue
            Inputs.append({
                "tipo": Tipo,
                "name": Nome,
                "id": Id,
                "value": html.unescape(Valor),
                "placeholder": "",
                "required": False,
            })
        return Inputs

    @staticmethod
    def _ProcurarEndpointJS(Html, ScriptsJs):
        Endpoints = set()
        for Texto in [Html] + ScriptsJs:
            for M in re.finditer(r'["\']([^"\']*(?:login|auth|entrar|submit|doLogin)[^"\']*)["\']', Texto, re.IGNORECASE):
                Url = M.group(1)
                if len(Url) < 100 and (Url.startswith("/") or Url.startswith("http")):
                    Endpoints.add(Url)
            for M in re.finditer(r'["\']([^"\']*\.(?:cgi|gch|asp|jsp|php))["\']', Texto, re.IGNORECASE):
                Url = M.group(1)
                if len(Url) < 100:
                    Endpoints.add(Url)
        return sorted(Endpoints)

    @staticmethod
    def _ExtrairScriptsInline(Html):
        Padrao = re.compile(r"<script\b[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)
        Scripts = []
        for M in Padrao.finditer(Html):
            Conteudo = M.group(1).strip()
            if Conteudo:
                Scripts.append(Conteudo)
        return Scripts

    @staticmethod
    def _BaixarScriptsExternos(Html, Url):
        Scripts = []
        Padrao = re.compile(r'<script[^>]*src=["\']([^"\']+)["\']', re.IGNORECASE)
        for M in Padrao.finditer(Html):
            Src = M.group(1)
            if Src.startswith("http"):
                UrlScript = Src
            elif Src.startswith("/"):
                Base = re.match(r"(https?://[^/]+)", Url)
                UrlScript = Base.group(1) + Src if Base else Url.rstrip("/") + Src
            else:
                UrlScript = Url.rstrip("/") + "/" + Src
            Resp = FormParser.Fetch(UrlScript)
            if Resp.get("ok"):
                Scripts.append(Resp.get("corpo", ""))
        return Scripts

    @staticmethod
    def ParsearSpa(Url):
        Log.Info("formparser spa iniciado", {"url": Url})
        Resultado = {
            "ok": False,
            "url": Url,
            "inputs_soltos": [],
            "endpoints": [],
            "form_implicito": None,
            "campos": None,
            "motivo": "",
        }
        Resp = FormParser.Fetch(Url)
        if not Resp.get("ok") and Resp.get("status") not in (200, 401, 403):
            Resultado["motivo"] = Resp.get("erro", "fetch_falhou")
            return Resultado
        Html = Resp.get("corpo", "")
        if not Html:
            Resultado["motivo"] = "sem_conteudo"
            return Resultado

        Inputs = FormParser._ExtrairInputsSoltos(Html)
        Resultado["inputs_soltos"] = Inputs

        ScriptsInline = FormParser._ExtrairScriptsInline(Html)
        ScriptsExternos = FormParser._BaixarScriptsExternos(Html, Url)
        TodosScripts = ScriptsInline + ScriptsExternos

        Endpoints = FormParser._ProcurarEndpointJS(Html, TodosScripts)
        Resultado["endpoints"] = Endpoints

        FormVirtual = {
            "action": "",
            "method": "POST",
            "id": "",
            "name": "",
            "inputs": Inputs,
            "virtual": True,
        }
        Resultado["form_implicito"] = FormVirtual
        Resultado["campos"] = FormParser.IdentificarCampos(FormVirtual)
        Resultado["ok"] = True
        Resultado["url_final"] = Resp.get("url_final", Url)
        Resultado["cookies_iniciais"] = Resp.get("headers", {}).get("Set-Cookie", "")

        Log.Descoberta("FormParser", Url, "spa_detectado", {
            "inputs": len(Inputs),
            "endpoints": len(Endpoints),
        })
        return Resultado

    @staticmethod
    def TentarLoginSpa(Url, Usuario, Senha, Endpoint=None, Cookies=None, CsrfValor=None):
        Parse = FormParser.ParsearSpa(Url)
        if not Parse.get("ok"):
            return {"ok": False, "motivo": Parse.get("motivo"), "sucesso": False}

        Form = Parse["form_implicito"]
        Campos = Parse["campos"]
        if not Campos.get("password"):
            return {"ok": False, "motivo": "sem_campo_senha", "sucesso": False}

        if not Endpoint:
            Endpoints = Parse.get("endpoints", [])
            for E in Endpoints:
                if "login" in E.lower() or "auth" in E.lower():
                    Endpoint = E
                    break
            if not Endpoint and Endpoints:
                Endpoint = Endpoints[0]

        if not Endpoint:
            return {"ok": False, "motivo": "sem_endpoint", "sucesso": False}

        Dados = FormParser.MontarDados(Form, Campos, Usuario, Senha, CsrfValor)

        import urllib.parse
        DadosStr = urllib.parse.urlencode(Dados).encode("utf-8")

        UrlFinal = Parse.get("url_final", Url)
        if Endpoint.startswith("http"):
            UrlLogin = Endpoint
        elif Endpoint.startswith("/"):
            Base = re.match(r"(https?://[^/]+)", UrlFinal)
            UrlLogin = Base.group(1) + Endpoint if Base else UrlFinal.rstrip("/") + Endpoint
        else:
            UrlLogin = UrlFinal.rstrip("/") + "/" + Endpoint

        Headers = {
            "User-Agent": Constants.HTTP_HEADERS_PADRAO["User-Agent"],
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/json,*/*;q=0.8",
            "Connection": "close",
            "Referer": UrlFinal,
        }
        if Cookies:
            Headers["Cookie"] = Cookies

        Resp = FormParser.Fetch(UrlLogin, Metodo="POST", Dados=DadosStr, Headers=Headers)
        Sucesso = FormParser._PareceSucesso(Resp, Usuario, Senha)
        return {
            "ok": True,
            "sucesso": Sucesso,
            "status": Resp.get("status"),
            "url_login": UrlLogin,
            "endpoint_usado": Endpoint,
            "corpo_trecho": Resp.get("corpo", "")[:500],
        }

    @staticmethod
    def Info():
        return {
            "nome": "FormParser",
            "capacidades": [
                "extrair_forms",
                "extrair_inputs_soltos",
                "procurar_endpoint_js",
                "parsear_spa",
                "tentar_login_form",
                "tentar_login_spa",
            ],
            "protocolos": ["http_form", "https_form", "http_spa", "https_spa"],
        }
