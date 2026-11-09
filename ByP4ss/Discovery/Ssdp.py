# Ssdp do ByP4ss
# Descoberta de dispositivos UPnP via SSDP

import socket
import re
import time

from Core.Constants import Constants
from Core.Config import Config
from Core.Log import Log


class Ssdp:

    @staticmethod
    def EnviarMSearch(Mensagem, Timeout=None):
        Timeout = Timeout or Config.TimeoutSSDP
        Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        Sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        Sock.settimeout(Timeout)
        try:
            Sock.sendto(Mensagem, (Constants.SSDP_MULTICAST, Constants.SSDP_PORTA))
        except OSError as E:
            Sock.close()
            return {"ok": False, "erro": str(E)}
        Respostas = []
        Fim = time.time() + Timeout
        while time.time() < Fim:
            try:
                Dados, Endereco = Sock.recvfrom(65535)
                Respostas.append({
                    "ip": Endereco[0],
                    "porta": Endereco[1],
                    "resposta": Dados.decode("utf-8", errors="replace"),
                })
            except socket.timeout:
                break
            except OSError:
                break
        Sock.close()
        return {"ok": True, "respostas": Respostas}

    @staticmethod
    def ParseResposta(Texto):
        Resultado = {"headers": {}, "raw": Texto}
        Linhas = Texto.split("\r\n")
        if Linhas:
            Resultado["status"] = Linhas[0]
        for Linha in Linhas[1:]:
            if ":" in Linha:
                Chave, Valor = Linha.split(":", 1)
                Resultado["headers"][Chave.strip().upper()] = Valor.strip()
        return Resultado

    @staticmethod
    def ExtrairLocal(Headers):
        for Chave in ["LOCATION", "location", "Location"]:
            if Chave in Headers:
                return Headers[Chave]
        return None

    @staticmethod
    def ExtrairServidor(Headers):
        for Chave in ["SERVER", "server", "Server"]:
            if Chave in Headers:
                return Headers[Chave]
        return ""

    @staticmethod
    def ExtrairST(Headers):
        for Chave in ["ST", "st", "St"]:
            if Chave in Headers:
                return Headers[Chave]
        return ""

    @staticmethod
    def ExtrairUSN(Headers):
        for Chave in ["USN", "usn", "Usn"]:
            if Chave in Headers:
                return Headers[Chave]
        return ""

    @staticmethod
    def ResolverLocal(Local):
        if not Local:
            return None
        M = re.match(r"http://([^/:]+)(?::(\d+))?(/.*)?", Local)
        if not M:
            return None
        Host = M.group(1)
        Porta = int(M.group(2)) if M.group(2) else 80
        Caminho = M.group(3) or "/"
        return {"host": Host, "porta": Porta, "caminho": Caminho, "url": Local}

    @staticmethod
    def Descobrir(Alvo):
        Log.Debug("ssdp descobrir", {"alvo": Alvo})

        Resultado = {
            "alvo": Alvo,
            "ok": False,
            "respostas": [],
            "local": None,
            "servidor": "",
            "control_url": None,
            "st": "",
            "usn": "",
            "motivo": "",
        }

        R1 = Ssdp.EnviarMSearch(Constants.SSDP_M_SEARCH_IGD)
        if R1.get("ok") and R1.get("respostas"):
            for Resp in R1["respostas"]:
                if Resp["ip"] != Alvo:
                    continue
                Parse = Ssdp.ParseResposta(Resp["resposta"])
                Local = Ssdp.ExtrairLocal(Parse["headers"])
                Servidor = Ssdp.ExtrairServidor(Parse["headers"])
                St = Ssdp.ExtrairST(Parse["headers"])
                Usn = Ssdp.ExtrairUSN(Parse["headers"])
                Resultado["respostas"].append({
                    "ip": Resp["ip"],
                    "porta": Resp["porta"],
                    "local": Local,
                    "servidor": Servidor,
                    "st": St,
                    "usn": Usn,
                })
                Resultado["local"] = Local
                Resultado["servidor"] = Servidor
                Resultado["st"] = St
                Resultado["usn"] = Usn

        if not Resultado["respostas"]:
            R2 = Ssdp.EnviarMSearch(Constants.SSDP_M_SEARCH_WAN)
            if R2.get("ok") and R2.get("respostas"):
                for Resp in R2["respostas"]:
                    if Resp["ip"] != Alvo:
                        continue
                    Parse = Ssdp.ParseResposta(Resp["resposta"])
                    Local = Ssdp.ExtrairLocal(Parse["headers"])
                    Servidor = Ssdp.ExtrairServidor(Parse["headers"])
                    St = Ssdp.ExtrairST(Parse["headers"])
                    Usn = Ssdp.ExtrairUSN(Parse["headers"])
                    Resultado["respostas"].append({
                        "ip": Resp["ip"],
                        "porta": Resp["porta"],
                        "local": Local,
                        "servidor": Servidor,
                        "st": St,
                        "usn": Usn,
                    })
                    Resultado["local"] = Local
                    Resultado["servidor"] = Servidor
                    Resultado["st"] = St
                    Resultado["usn"] = Usn

        if not Resultado["respostas"]:
            R3 = Ssdp.EnviarMSearch(Constants.SSDP_M_SEARCH)
            if R3.get("ok") and R3.get("respostas"):
                for Resp in R3["respostas"]:
                    if Resp["ip"] != Alvo:
                        continue
                    Parse = Ssdp.ParseResposta(Resp["resposta"])
                    Local = Ssdp.ExtrairLocal(Parse["headers"])
                    Servidor = Ssdp.ExtrairServidor(Parse["headers"])
                    St = Ssdp.ExtrairST(Parse["headers"])
                    Usn = Ssdp.ExtrairUSN(Parse["headers"])
                    Resultado["respostas"].append({
                        "ip": Resp["ip"],
                        "porta": Resp["porta"],
                        "local": Local,
                        "servidor": Servidor,
                        "st": St,
                        "usn": Usn,
                    })
                    Resultado["local"] = Local
                    Resultado["servidor"] = Servidor
                    Resultado["st"] = St
                    Resultado["usn"] = Usn

        if not Resultado["respostas"]:
            Resultado["motivo"] = "sem_resposta_ssdp"
            Log.Debug("ssdp sem resposta", {"alvo": Alvo})
            return Resultado

        if Resultado["local"]:
            Resolvido = Ssdp.ResolverLocal(Resultado["local"])
            if Resolvido:
                Resultado["control_url"] = Ssdp.MontarControlUrl(Resultado["local"], Resolvido)
                Resultado["ok"] = True
            else:
                Resultado["motivo"] = "local_invalido"
                Log.Aviso("ssdp local invalido", {"local": Resultado["local"]})
        else:
            Resultado["motivo"] = "sem_local"

        Log.Debug("ssdp resposta", {
            "ok": Resultado["ok"],
            "servidor": Resultado["servidor"],
            "st": Resultado["st"],
        })

        return Resultado

    @staticmethod
    def MontarControlUrl(Local, Resolvido):
        if not Resolvido:
            return None
        Host = Resolvido["host"]
        Porta = Resolvido["porta"]
        return f"http://{Host}:{Porta}/"

    @staticmethod
    def CarregarDescritor(Url, Timeout=None):
        Timeout = Timeout or Config.TimeoutHTTP
        import urllib.request
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
    def Info():
        return {
            "nome": "Ssdp",
            "multicast": Constants.SSDP_MULTICAST,
            "porta": Constants.SSDP_PORTA,
            "timeout": Config.TimeoutSSDP,
        }
