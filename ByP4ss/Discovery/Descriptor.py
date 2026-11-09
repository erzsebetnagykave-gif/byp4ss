# Descriptor do ByP4ss
# Le o descritor UPnP e extrai o control_url do WANIPConnection

import urllib.request
import xml.etree.ElementTree as ET

from Core.Constants import Constants
from Core.Config import Config
from Core.Log import Log


class Descriptor:

    @staticmethod
    def Baixar(Url, Timeout=None):
        Timeout = Timeout or Config.TimeoutHTTP
        try:
            Req = urllib.request.Request(
                Url,
                headers={"User-Agent": Constants.HTTP_HEADERS_PADRAO["User-Agent"]},
            )
            with urllib.request.urlopen(Req, timeout=Timeout) as F:
                return {"ok": True, "conteudo": F.read().decode("utf-8", errors="replace")}
        except Exception as E:
            return {"ok": False, "erro": str(E)}

    @staticmethod
    def Parsear(Conteudo):
        Resultado = {
            "ok": False,
            "fabricante": "",
            "modelo": "",
            "nome": "",
            "servicos": [],
            "control_urls": {},
            "motivo": "",
        }
        try:
            Raiz = ET.fromstring(Conteudo)
        except ET.ParseError as E:
            Resultado["motivo"] = f"xml_invalido: {E}"
            return Resultado

        Espaco = ""
        if Raiz.tag.startswith("{"):
            Espaco = Raiz.tag.split("}")[0] + "}"

        for Tag, Chave in [("manufacturer", "fabricante"),
                          ("modelName", "modelo"),
                          ("friendlyName", "nome")]:
            El = Raiz.find(f".//{Espaco}{Tag}")
            if El is not None and El.text:
                Resultado[Chave] = El.text.strip()

        for Servico in Raiz.iter(f"{Espaco}service"):
            Tipo = Servico.find(f"{Espaco}serviceType")
            ControlUrl = Servico.find(f"{Espaco}controlURL")
            ScpdUrl = Servico.find(f"{Espaco}SCPDURL")
            EventSub = Servico.find(f"{Espaco}eventSubURL")
            Item = {
                "tipo": Tipo.text.strip() if Tipo is not None and Tipo.text else "",
                "control_url": ControlUrl.text.strip() if ControlUrl is not None and ControlUrl.text else "",
                "scpd_url": ScpdUrl.text.strip() if ScpdUrl is not None and ScpdUrl.text else "",
                "event_sub": EventSub.text.strip() if EventSub is not None and EventSub.text else "",
            }
            Resultado["servicos"].append(Item)
            if Item["tipo"]:
                Resultado["control_urls"][Item["tipo"]] = Item["control_url"]

        if Resultado["control_urls"]:
            Resultado["ok"] = True
        else:
            Resultado["motivo"] = "sem_servicos"

        return Resultado

    @staticmethod
    def NormalizarUrl(Base, Relativo):
        if not Relativo:
            return None
        if Relativo.startswith("http://") or Relativo.startswith("https://"):
            return Relativo
        if not Base:
            return None
        if Relativo.startswith("/"):
            M = Base.split("//", 1)
            if len(M) == 2:
                Host = M[1].split("/")[0]
                return f"http://{Host}{Relativo}"
        return Base.rstrip("/") + "/" + Relativo.lstrip("/")

    @staticmethod
    def EncontrarControlUrl(Parsed, Base=None):
        if not Parsed.get("ok"):
            return None
        Preferencias = [
            Constants.UPNP_NS_WANIP,
            Constants.UPNP_NS_WANPPP,
            Constants.UPNP_NS_LAYER3,
        ]
        for Tipo in Preferencias:
            if Tipo in Parsed["control_urls"]:
                Url = Parsed["control_urls"][Tipo]
                return Descriptor.NormalizarUrl(Base, Url)
        for Tipo, Url in Parsed["control_urls"].items():
            if "WAN" in Tipo or "Layer3" in Tipo:
                return Descriptor.NormalizarUrl(Base, Url)
        return None

    @staticmethod
    def EncontrarScpdUrl(Parsed, Base=None):
        if not Parsed.get("ok"):
            return None
        Preferencias = [
            Constants.UPNP_NS_WANIP,
            Constants.UPNP_NS_WANPPP,
            Constants.UPNP_NS_LAYER3,
        ]
        for Servico in Parsed["servicos"]:
            for Tipo in Preferencias:
                if Servico["tipo"] == Tipo and Servico.get("scpd_url"):
                    return Descriptor.NormalizarUrl(Base, Servico["scpd_url"])
        return None

    @staticmethod
    def Analisar(UrlLocal):
        Log.Debug("descriptor analisar", {"url": UrlLocal})
        Resultado = {
            "ok": False,
            "url": UrlLocal,
            "fabricante": "",
            "modelo": "",
            "nome": "",
            "servicos": [],
            "control_url": None,
            "scpd_url": None,
            "motivo": "",
        }
        if not UrlLocal:
            Resultado["motivo"] = "sem_url"
            return Resultado

        Baixado = Descriptor.Baixar(UrlLocal)
        if not Baixado.get("ok"):
            Resultado["motivo"] = f"download_falhou: {Baixado.get('erro', '')}"
            Log.Aviso("descriptor download falhou", Resultado)
            return Resultado

        Parseado = Descriptor.Parsear(Baixado["conteudo"])
        if not Parseado.get("ok"):
            Resultado["motivo"] = Parseado.get("motivo", "")
            Log.Aviso("descriptor parse falhou", Resultado)
            return Resultado

        Resultado["fabricante"] = Parseado["fabricante"]
        Resultado["modelo"] = Parseado["modelo"]
        Resultado["nome"] = Parseado["nome"]
        Resultado["servicos"] = Parseado["servicos"]
        Resultado["control_url"] = Descriptor.EncontrarControlUrl(Parseado, UrlLocal)
        Resultado["scpd_url"] = Descriptor.EncontrarScpdUrl(Parseado, UrlLocal)

        if Resultado["control_url"]:
            Resultado["ok"] = True
        else:
            Resultado["motivo"] = "sem_control_url"

        Log.Descoberta("Descriptor", UrlLocal, "analisado", {
            "fabricante": Resultado["fabricante"],
            "modelo": Resultado["modelo"],
            "control_url": Resultado["control_url"],
        })

        return Resultado

    @staticmethod
    def Info():
        return {
            "nome": "Descriptor",
            "timeout": Config.TimeoutHTTP,
        }
