# UpnpBypass do ByP4ss
# 600 linhas (parte 1 de 2)
# Motor proprio de UPnP (sem miniupnpc)
# Le regras existentes, adiciona/remove port mapping

import socket
import urllib.request
import urllib.error
import re
import time
import json

from Core.Constants import Constants
from Core.Config import Config
from Core.Log import Log


class UpnpBypass:

    _CacheDescritor = {}
    _CacheServico = {}

    @staticmethod
    def DescobrirControlUrl(Alvo):
        if Alvo in UpnpBypass._CacheDescritor:
            return UpnpBypass._CacheDescritor[Alvo]

        Local = None
        try:
            from Discovery.Ssdp import Ssdp
            SsdpResult = Ssdp.Descobrir(Alvo)
            if SsdpResult and SsdpResult.get("ok") and SsdpResult.get("local"):
                Local = SsdpResult["local"]
        except Exception as E:
            Log.Erro("upnp ssdp falhou", {"erro": str(E)})

        if not Local:
            for Porta in Constants.PORTAS_UPNP:
                for Caminho in ["/gatedesc.xml", "/rootDesc.xml", "/description.xml", "/upnp/desc.xml", "/"]:
                    Tentativa = f"http://{Alvo}:{Porta}{Caminho}"
                    if UpnpBypass._TestarDescritor(Tentativa):
                        Local = Tentativa
                        break
                if Local:
                    break

        if Local:
            try:
                from Discovery.Descriptor import Descriptor
                Analise = Descriptor.Analisar(Local)
                if Analise and Analise.get("ok") and Analise.get("control_url"):
                    UpnpBypass._CacheDescritor[Alvo] = Analise["control_url"]
                    return Analise["control_url"]
            except Exception as E:
                Log.Erro("upnp descriptor falhou", {"erro": str(E)})

        UpnpBypass._CacheDescritor[Alvo] = Local
        return Local

    @staticmethod
    def _TestarDescritor(Url):
        try:
            Req = urllib.request.Request(
                Url,
                headers={"User-Agent": Constants.HTTP_HEADERS_PADRAO["User-Agent"]},
            )
            with urllib.request.urlopen(Req, timeout=Config.TimeoutHTTP) as F:
                Conteudo = F.read(4096).decode("utf-8", errors="replace")
                if "<root" in Conteudo.lower() and "service" in Conteudo.lower():
                    return True
        except Exception:
            pass
        return False

    @staticmethod
    def AnalisarDescritor(Url):
        if not Url:
            return None
        if Url in UpnpBypass._CacheServico:
            return UpnpBypass._CacheServico[Url]

        try:
            Req = urllib.request.Request(
                Url,
                headers={"User-Agent": Constants.HTTP_HEADERS_PADRAO["User-Agent"]},
            )
            with urllib.request.urlopen(Req, timeout=Config.TimeoutHTTP) as F:
                Conteudo = F.read().decode("utf-8", errors="replace")
        except Exception as E:
            Log.Aviso("upnp descritor falhou", {"url": Url, "erro": str(E)})
            return None

        Servicos = []
        Padrao = re.compile(
            r"<service>(.*?)</service>",
            re.DOTALL | re.IGNORECASE,
        )
        for M in Padrao.finditer(Conteudo):
            Bloco = M.group(1)
            Tipo = UpnpBypass._ExtrairTag(Bloco, "serviceType")
            ControlUrl = UpnpBypass._ExtrairTag(Bloco, "controlURL")
            ScpdUrl = UpnpBypass._ExtrairTag(Bloco, "SCPDURL")
            if Tipo and ControlUrl:
                Servicos.append({
                    "tipo": Tipo,
                    "control_url": UpnpBypass._Normalizar(Url, ControlUrl),
                    "scpd_url": UpnpBypass._Normalizar(Url, ScpdUrl) if ScpdUrl else None,
                })

        Base = Url.rsplit("/", 1)[0] if "/" in Url else Url
        Fabricante = UpnpBypass._ExtrairTag(Conteudo, "manufacturer")
        Modelo = UpnpBypass._ExtrairTag(Conteudo, "modelName")
        Nome = UpnpBypass._ExtrairTag(Conteudo, "friendlyName")

        Resultado = {
            "url": Url,
            "base": Base,
            "fabricante": Fabricante or "",
            "modelo": Modelo or "",
            "nome": Nome or "",
            "servicos": Servicos,
        }
        UpnpBypass._CacheServico[Url] = Resultado
        return Resultado

    @staticmethod
    def _ExtrairTag(Bloco, Tag):
        Padrao = re.compile(rf"<{Tag}[^>]*>(.*?)</{Tag}>", re.DOTALL | re.IGNORECASE)
        M = Padrao.search(Bloco)
        if M:
            return M.group(1).strip()
        Padrao2 = re.compile(rf"<{Tag}[^>]*/>", re.DOTALL | re.IGNORECASE)
        if Padrao2.search(Bloco):
            return ""
        return None

    @staticmethod
    def _Normalizar(Base, Url):
        if not Url:
            return None
        if Url.startswith("http://") or Url.startswith("https://"):
            return Url
        if not Base:
            return Url
        if Url.startswith("/"):
            M = re.match(r"https?://([^/]+)", Base)
            if M:
                return f"http://{M.group(1)}{Url}"
        return Base.rstrip("/") + "/" + Url.lstrip("/")

    @staticmethod
    def EncontrarServicoWan(Analise):
        if not Analise or not Analise.get("servicos"):
            return None
        Preferencias = [
            Constants.UPNP_NS_WANIP,
            Constants.UPNP_NS_WANPPP,
            Constants.UPNP_NS_LAYER3,
        ]
        for Pref in Preferencias:
            for Servico in Analise["servicos"]:
                if Servico["tipo"] == Pref:
                    return Servico
        for Servico in Analise["servicos"]:
            if "WAN" in Servico["tipo"] or "Layer3" in Servico["tipo"]:
                return Servico
        return None

    @staticmethod
    def EnviarSoap(ControlUrl, ServicoTipo, Acao, Corpo):
        if not ControlUrl:
            return {"ok": False, "erro": "sem_control_url"}

        Envelope = (
            '<?xml version="1.0"?>\n'
            '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
            's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\n'
            '<s:Body>\n'
            f'{Corpo}\n'
            '</s:Body>\n'
            '</s:Envelope>\n'
        ).encode("utf-8")

        Headers = {
            "Content-Type": 'text/xml; charset="utf-8"',
            "SOAPAction": f'"{ServicoTipo}#{Acao}"',
            "User-Agent": Constants.HTTP_HEADERS_PADRAO["User-Agent"],
            "Connection": "close",
        }

        try:
            Req = urllib.request.Request(
                ControlUrl,
                data=Envelope,
                headers=Headers,
                method="POST",
            )
            with urllib.request.urlopen(Req, timeout=Config.TimeoutUPNP) as F:
                Resposta = F.read().decode("utf-8", errors="replace")
                return {
                    "ok": True,
                    "status": F.status,
                    "resposta": Resposta[:2000],
                }
        except urllib.error.HTTPError as E:
            return {
                "ok": False,
                "status": E.code,
                "erro": f"http_{E.code}",
                "resposta": E.read().decode("utf-8", errors="replace")[:2000],
            }
        except Exception as E:
            return {"ok": False, "erro": str(E)}

    @staticmethod
    def MontarAddPortMapping(ServicoTipo, PortaExterna, PortaInterna, Cliente, Protocolo, Lease):
        Acao = "AddPortMapping"
        Corpo = (
            f'<u:{Acao} xmlns:u="{ServicoTipo}">\n'
            f'  <NewRemoteHost></NewRemoteHost>\n'
            f'  <NewExternalPort>{PortaExterna}</NewExternalPort>\n'
            f'  <NewProtocol>{Protocolo}</NewProtocol>\n'
            f'  <NewInternalPort>{PortaInterna}</NewInternalPort>\n'
            f'  <NewInternalClient>{Cliente}</NewInternalClient>\n'
            f'  <NewEnabled>1</NewEnabled>\n'
            f'  <NewPortMappingDescription>ByP4ss</NewPortMappingDescription>\n'
            f'  <NewLeaseDuration>{Lease}</NewLeaseDuration>\n'
            f'</u:{Acao}>\n'
        )
        return Acao, Corpo

    @staticmethod
    def MontarDeletePortMapping(ServicoTipo, PortaExterna, Protocolo):
        Acao = "DeletePortMapping"
        Corpo = (
            f'<u:{Acao} xmlns:u="{ServicoTipo}">\n'
            f'  <NewRemoteHost></NewRemoteHost>\n'
            f'  <NewExternalPort>{PortaExterna}</NewExternalPort>\n'
            f'  <NewProtocol>{Protocolo}</NewProtocol>\n'
            f'</u:{Acao}>\n'
        )
        return Acao, Corpo

    @staticmethod
    def MontarGetGeneric(ServicoTipo, Indice):
        Acao = "GetGenericPortMappingEntry"
        Corpo = (
            f'<u:{Acao} xmlns:u="{ServicoTipo}">\n'
            f'  <NewPortMappingIndex>{Indice}</NewPortMappingIndex>\n'
            f'</u:{Acao}>\n'
        )
        return Acao, Corpo

    @staticmethod
    def MontarGetExternalIp(ServicoTipo):
        Acao = "GetExternalIPAddress"
        Corpo = (
            f'<u:{Acao} xmlns:u="{ServicoTipo}">\n'
            f'</u:{Acao}>\n'
        )
        return Acao, Corpo

    @staticmethod
    def LerRegras(Alvo):
        Url = UpnpBypass.DescobrirControlUrl(Alvo)
        if not Url:
            return {"ok": False, "erro": "sem_descritor", "regras": []}

        Analise = UpnpBypass.AnalisarDescritor(Url)
        Servico = UpnpBypass.EncontrarServicoWan(Analise)
        if not Servico:
            return {"ok": False, "erro": "sem_wan_service", "regras": []}

        Regras = []
        for Indice in range(100):
            Acao, Corpo = UpnpBypass.MontarGetGeneric(Servico["tipo"], Indice)
            R = UpnpBypass.EnviarSoap(Servico["control_url"], Servico["tipo"], Acao, Corpo)
            if not R.get("ok"):
                break
            Resposta = R.get("resposta", "")
            PortaExt = UpnpBypass._ExtrairResposta(Resposta, "NewExternalPort")
            PortaInt = UpnpBypass._ExtrairResposta(Resposta, "NewInternalPort")
            Cliente = UpnpBypass._ExtrairResposta(Resposta, "NewInternalClient")
            Protocolo = UpnpBypass._ExtrairResposta(Resposta, "NewProtocol")
            Descricao = UpnpBypass._ExtrairResposta(Resposta, "NewPortMappingDescription")
            Enabled = UpnpBypass._ExtrairResposta(Resposta, "NewEnabled")
            if PortaExt is None:
                break
            Regras.append({
                "indice": Indice,
                "porta_externa": PortaExt,
                "porta_interna": PortaInt,
                "cliente": Cliente,
                "protocolo": Protocolo,
                "descricao": Descricao,
                "habilitado": Enabled,
            })

        Log.Descoberta("UpnpBypass", Alvo, "regras_lidas", {"total": len(Regras)})
        return {"ok": True, "regras": Regras, "servico": Servico, "url": Url}

    @staticmethod
    def _ExtrairResposta(Xml, Tag):
        Padrao = re.compile(rf"<{Tag}[^>]*>(.*?)</{Tag}>", re.DOTALL | re.IGNORECASE)
        M = Padrao.search(Xml)
        if M:
            return M.group(1).strip()
        return None

    @staticmethod
    def GetExternalIp(Alvo):
        Url = UpnpBypass.DescobrirControlUrl(Alvo)
        if not Url:
            return {"ok": False, "erro": "sem_descritor"}
        Analise = UpnpBypass.AnalisarDescritor(Url)
        Servico = UpnpBypass.EncontrarServicoWan(Analise)
        if not Servico:
            return {"ok": False, "erro": "sem_wan_service"}

        Acao, Corpo = UpnpBypass.MontarGetExternalIp(Servico["tipo"])
        R = UpnpBypass.EnviarSoap(Servico["control_url"], Servico["tipo"], Acao, Corpo)
        if R.get("ok"):
            Ip = UpnpBypass._ExtrairResposta(R.get("resposta", ""), "NewExternalIPAddress")
            return {"ok": True, "ip": Ip}
        return R

    @staticmethod
    def AdicionarRegra(Alvo, PortaExterna, PortaInterna, Protocolo="TCP",
                       Cliente=None, Lease=0, Tentar3=True):
        Cliente = Cliente or Alvo
        Url = UpnpBypass.DescobrirControlUrl(Alvo)
        if not Url:
            return {"ok": False, "erro": "sem_descritor"}

        Analise = UpnpBypass.AnalisarDescritor(Url)
        Servico = UpnpBypass.EncontrarServicoWan(Analise)
        if not Servico:
            return {"ok": False, "erro": "sem_wan_service"}

        Tentativas = []
        if Tentar3:
            Combos = [
                (Lease, Constants.UPNP_LEASE_0),
                (Constants.UPNP_LEASE_1H, Constants.UPNP_LEASE_1H),
                (Constants.UPNP_LEASE_24H, Constants.UPNP_LEASE_24H),
            ]
        else:
            Combos = [(Lease, Lease)]

        for Tentativa, (LeaseT, _) in enumerate(Combos):
            Acao, Corpo = UpnpBypass.MontarAddPortMapping(
                Servico["tipo"], PortaExterna, PortaInterna, Cliente, Protocolo, LeaseT
            )
            R = UpnpBypass.EnviarSoap(
                Servico["control_url"], Servico["tipo"], Acao, Corpo
            )
            Tentativas.append({
                "tentativa": Tentativa + 1,
                "lease": LeaseT,
                "status": R.get("status", 0),
                "ok": R.get("ok", False),
            })
            if R.get("ok"):
                Log.Bypass("UpnpBypass", Alvo, True, {
                    "porta_externa": PortaExterna,
                    "porta_interna": PortaInterna,
                    "protocolo": Protocolo,
                    "lease": LeaseT,
                })
                return {
                    "ok": True,
                    "porta_externa": PortaExterna,
                    "porta_interna": PortaInterna,
                    "protocolo": Protocolo,
                    "cliente": Cliente,
                    "lease": LeaseT,
                    "tentativas": Tentativas,
                }

            Codigo = R.get("status", 0)
            if Codigo in (718, 724, 725):
                Log.Aviso("upnp conflito, tentando delete + add", {"porta": PortaExterna})
                UpnpBypass.RemoverRegra(Alvo, PortaExterna, Protocolo)
                time.sleep(0.3)
                Acao2, Corpo2 = UpnpBypass.MontarAddPortMapping(
                    Servico["tipo"], PortaExterna, PortaInterna, Cliente, Protocolo, LeaseT
                )
                R2 = UpnpBypass.EnviarSoap(
                    Servico["control_url"], Servico["tipo"], Acao2, Corpo2
                )
                if R2.get("ok"):
                    Log.Bypass("UpnpBypass", Alvo, True, {
                        "porta_externa": PortaExterna,
                        "metodo": "delete_add",
                    })
                    return {
                        "ok": True,
                        "porta_externa": PortaExterna,
                        "porta_interna": PortaInterna,
                        "protocolo": Protocolo,
                        "cliente": Cliente,
                        "lease": LeaseT,
                        "metodo": "delete_add",
                    }

        Log.Bypass("UpnpBypass", Alvo, False, {"porta": PortaExterna})
        return {
            "ok": False,
            "erro": "todas_tentativas_falharam",
            "tentativas": Tentativas,
            "porta_externa": PortaExterna,
        }

    @staticmethod
    def RemoverRegra(Alvo, PortaExterna, Protocolo="TCP"):
        Url = UpnpBypass.DescobrirControlUrl(Alvo)
        if not Url:
            return {"ok": False, "erro": "sem_descritor"}
        Analise = UpnpBypass.AnalisarDescritor(Url)
        Servico = UpnpBypass.EncontrarServicoWan(Analise)
        if not Servico:
            return {"ok": False, "erro": "sem_wan_service"}

        Acao, Corpo = UpnpBypass.MontarDeletePortMapping(
            Servico["tipo"], PortaExterna, Protocolo
        )
        R = UpnpBypass.EnviarSoap(Servico["control_url"], Servico["tipo"], Acao, Corpo)
        if R.get("ok"):
            Log.Info("upnp regra removida", {"porta": PortaExterna})
        return R

    @staticmethod
    def VerificarPorta(Alvo, Porta, Timeout=2.0):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(Timeout)
        try:
            Codigo = Sock.connect_ex((Alvo, Porta))
            if Codigo == 0:
                return True
        except socket.error:
            pass
        finally:
            try:
                Sock.close()
            except socket.error:
                pass
        return False

    @staticmethod
    def Tentar(Alvo, ControlUrl=None, Porta=None):
        Porta = Porta or Config.Porta
        Log.Info("upnp bypass iniciado", {"alvo": Alvo, "porta": Porta})

        Resultado = {
            "ok": False,
            "alvo": Alvo,
            "porta": Porta,
            "descritor": None,
            "servico": None,
            "regras_antes": [],
            "adicionado": None,
            "verificado": False,
            "motivo": "",
        }

        Url = ControlUrl or UpnpBypass.DescobrirControlUrl(Alvo)
        Resultado["descritor"] = Url
        if not Url:
            Resultado["motivo"] = "sem_descritor"
            Log.Aviso("upnp bypass sem descritor", Resultado)
            return Resultado

        Analise = UpnpBypass.AnalisarDescritor(Url)
        if not Analise:
            Resultado["motivo"] = "descritor_invalido"
            return Resultado

        Servico = UpnpBypass.EncontrarServicoWan(Analise)
        if not Servico:
            Resultado["motivo"] = "sem_wan_service"
            return Resultado

        Resultado["servico"] = Servico["tipo"]

        RegrasAtuais = UpnpBypass.LerRegras(Alvo)
        if RegrasAtuais.get("ok"):
            Resultado["regras_antes"] = RegrasAtuais.get("regras", [])

        Adicao = UpnpBypass.AdicionarRegra(
            Alvo,
            PortaExterna=Porta,
            PortaInterna=Porta,
            Protocolo=Config.Protocolo,
            Cliente=Alvo,
            Lease=Constants.UPNP_LEASE_0,
        )
        Resultado["adicionado"] = Adicao

        if not Adicao.get("ok"):
            Resultado["motivo"] = Adicao.get("erro", "add_falhou")
            return Resultado

        time.sleep(0.5)

        Resultado["verificado"] = UpnpBypass.VerificarPorta(Alvo, Porta)
        if Resultado["verificado"]:
            Resultado["ok"] = True
            Log.Bypass("UpnpBypass", Alvo, True, {
                "porta": Porta,
                "verificado": True,
            })
        else:
            Resultado["motivo"] = "porta_nao_abriu"
            Log.Aviso("upnp adicionou mas porta nao abriu", {"porta": Porta})

        return Resultado

    @staticmethod
    def Info():
        return {
            "nome": "UpnpBypass",
            "metodos": [
                "AddPortMapping",
                "DeletePortMapping",
                "GetGenericPortMappingEntry",
                "GetExternalIPAddress",
            ],
            "timeout": Config.TimeoutUPNP,
        }

    @staticmethod
    def TentarAddAny(Alvo, PortaExterna, PortaInterna, Protocolo="TCP", Cliente=None, Lease=0):
        Cliente = Cliente or Alvo
        Url = UpnpBypass.DescobrirControlUrl(Alvo)
        if not Url:
            return {"ok": False, "erro": "sem_descritor"}

        Analise = UpnpBypass.AnalisarDescritor(Url)
        Servico = UpnpBypass.EncontrarServicoWan(Analise)
        if not Servico:
            return {"ok": False, "erro": "sem_wan_service"}

        Acao = "AddAnyPortMapping"
        Corpo = (
            f'<u:{Acao} xmlns:u="{Servico["tipo"]}">\n'
            f'  <NewRemoteHost></NewRemoteHost>\n'
            f'  <NewExternalPort>{PortaExterna}</NewExternalPort>\n'
            f'  <NewProtocol>{Protocolo}</NewProtocol>\n'
            f'  <NewInternalPort>{PortaInterna}</NewInternalPort>\n'
            f'  <NewInternalClient>{Cliente}</NewInternalClient>\n'
            f'  <NewEnabled>1</NewEnabled>\n'
            f'  <NewPortMappingDescription>ByP4ss</NewPortMappingDescription>\n'
            f'  <NewLeaseDuration>{Lease}</NewLeaseDuration>\n'
            f'</u:{Acao}>\n'
        )
        return UpnpBypass.EnviarSoap(Servico["control_url"], Servico["tipo"], Acao, Corpo)
