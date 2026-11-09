# ServiceFingerprint do ByP4ss
# Identifica QUAL servico esta em cada porta aberta (nao so "porta 80").
# Chamado por Core.Engine.Discover: Mod.ServiceFingerprint.Identificar(Alvo, Portas)
#
# Recebe a lista de portas abertas que o PortScan ja filtrou, e enriquece
# cada uma com fabricante/modelo/os. Usa 3 camadas:
#   1. banner grab (TCP, le 1KB)
#   2. HTTP HEAD (portas web)
#   3. TLS handshake (portas https, le certificado)
#
# Nao depende de ferramenta externa. So stdlib.

import socket
import ssl
import re

from Core.Config import Config
from Core.Log import Log


class ServiceFingerprint:

    ASSINATURAS_FABRICANTE = [
        ("tplink",     ["tp-link", "tplink", "archer", "tl-wr", "tl-wa"]),
        ("dlink",      ["d-link", "dlink", "dns-", "nas_sharing"]),
        ("tenda",      ["tenda", "ac9", "ac15", "ac6", "w20e"]),
        ("arcadyan",   ["arcadyan", "arv", "prv", "vrv", "smartrg"]),
        ("iptime",     ["iptime", "efm", "a2004", "a3004", "n6004", "ax2004"]),
        ("zte",        ["zte", "f6600", "f670", "h298"]),
        ("huawei",     ["huawei", "hg8245", "hg8145"]),
        ("mikrotik",   ["mikrotik", "routeros"]),
        ("cisco",      ["cisco", "rv340", "rv042"]),
        ("netgear",    ["netgear", "r7000", "r6400"]),
        ("asus",       ["asus", "rt-ac", "rt-ax"]),
        ("linksys",    ["linksys", "ea7500", "wrt1900"]),
        ("ubiquiti",   ["ubiquiti", "ubnt", "edgerouter"]),
        ("fortinet",   ["fortinet", "fortigate"]),
        ("openwrt",    ["openwrt", "luci"]),
    ]

    FABRICANTE_BONITO = {
        "tplink": "TP-Link", "dlink": "D-Link", "tenda": "Tenda",
        "arcadyan": "Arcadyan", "iptime": "ipTIME", "zte": "ZTE",
        "huawei": "Huawei", "mikrotik": "MikroTik", "cisco": "Cisco",
        "netgear": "Netgear", "asus": "Asus", "linksys": "Linksys",
        "ubiquiti": "Ubiquiti", "fortinet": "Fortinet", "openwrt": "OpenWrt",
    }

    PORTAS_HTTP = (80, 8000, 8080, 8081, 8888)
    PORTAS_HTTPS = (443, 8443, 9443)
    PORTAS_SSH = (22, 2222)
    PORTAS_TELNET = (23, 2323)
    PORTAS_UPNP = (1900, 5000, 52869)

    @staticmethod
    def Identificar(Alvo, Portas, Timeout=None):
        if not Alvo:
            return {"ok": False, "motivo": "alvo_ausente",
                    "fabricante": None, "modelo": None, "os": None,
                    "portas": [], "total_identificadas": 0}
        Timeout = Timeout or 2.0
        Resultado = {
            "ok": True, "alvo": Alvo,
            "fabricante": None, "modelo": None, "os": None,
            "portas": [], "total_identificadas": 0,
        }
        PortasLista = ServiceFingerprint._NormalizarPortas(Portas)
        FabricantesDetectados = {}
        for Item in PortasLista:
            Porta = Item["porta"]
            Info = dict(Item)
            Info["servico"] = Info.get("servico") or ServiceFingerprint._ServicoPorPorta(Porta)
            Extra = ServiceFingerprint._IdentificarPorta(Alvo, Porta, Info["servico"], Timeout)
            if Extra:
                for K, V in Extra.items():
                    if V and not Info.get(K):
                        Info[K] = V
                Fab = Extra.get("fabricante")
                if Fab:
                    FabricantesDetectados[Fab] = FabricantesDetectados.get(Fab, 0) + 1
            Resultado["portas"].append(Info)
        if FabricantesDetectados:
            MaisComum = max(FabricantesDetectados.items(), key=lambda X: X[1])[0]
            Resultado["fabricante"] = ServiceFingerprint.FABRICANTE_BONITO.get(MaisComum, MaisComum)
        Modelos = [P.get("modelo") for P in Resultado["portas"] if P.get("modelo")]
        if Modelos:
            Resultado["modelo"] = Modelos[0]
        Os = [P.get("os") for P in Resultado["portas"] if P.get("os")]
        if Os:
            Resultado["os"] = Os[0]
        Resultado["total_identificadas"] = sum(
            1 for P in Resultado["portas"] if P.get("fabricante") or P.get("servico")
        )
        Log.Descoberta("ServiceFingerprint", Alvo, "fingerprint", {
            "fabricante": Resultado["fabricante"],
            "modelo": Resultado["modelo"],
            "os": Resultado["os"],
            "portas": len(Resultado["portas"]),
            "identificadas": Resultado["total_identificadas"],
        })
        return Resultado

    @staticmethod
    def _NormalizarPortas(Portas):
        if not Portas:
            return []
        Out = []
        for Item in Portas:
            if isinstance(Item, dict):
                P = Item.get("porta")
                if P is not None:
                    Out.append(dict(Item))
            elif isinstance(Item, int):
                Out.append({"porta": Item})
        return Out

    @staticmethod
    def _ServicoPorPorta(Porta):
        Mapa = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
            80: "http", 110: "pop3", 143: "imap", 443: "https",
            445: "smb", 1433: "mssql", 1521: "oracle", 1900: "upnp",
            3306: "mysql", 3389: "rdp", 5000: "upnp-alt", 5432: "postgres",
            6379: "redis", 7547: "tr069", 8080: "http-alt", 8443: "https-alt",
            9100: "printer", 27017: "mongodb", 52869: "upnp",
        }
        return Mapa.get(Porta, "desconhecido")

    @staticmethod
    def _IdentificarPorta(Alvo, Porta, Servico, Timeout):
        Extra = {}
        try:
            if Porta in ServiceFingerprint.PORTAS_HTTPS:
                Http = ServiceFingerprint._HttpHead(Alvo, Porta, Timeout, Esquema="https")
                Tls = ServiceFingerprint._TlsCertificado(Alvo, Porta, Timeout)
                Extra.update(Http or {})
                Extra.update(Tls or {})
            elif Porta in ServiceFingerprint.PORTAS_HTTP:
                Http = ServiceFingerprint._HttpHead(Alvo, Porta, Timeout, Esquema="http")
                Extra.update(Http or {})
            elif Porta in ServiceFingerprint.PORTAS_SSH:
                Banner = ServiceFingerprint._Banner(Alvo, Porta, Timeout, Enviar=None)
                Extra.update(ServiceFingerprint._ParseBanner(Banner))
            elif Porta in ServiceFingerprint.PORTAS_TELNET:
                Banner = ServiceFingerprint._Banner(Alvo, Porta, Timeout, Enviar=b"\r\n")
                Extra.update(ServiceFingerprint._ParseBanner(Banner))
            else:
                Banner = ServiceFingerprint._Banner(Alvo, Porta, Timeout, Enviar=None)
                Extra.update(ServiceFingerprint._ParseBanner(Banner))
        except Exception:
            pass
        return Extra

    @staticmethod
    def _Banner(Alvo, Porta, Timeout, Enviar=None):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(Timeout)
        try:
            if Sock.connect_ex((Alvo, int(Porta))) != 0:
                return b""
            Sock.settimeout(1.5)
            if Enviar:
                try:
                    Sock.sendall(Enviar)
                except (socket.timeout, OSError):
                    pass
            Buffer = b""
            try:
                Buffer = Sock.recv(1024)
            except socket.timeout:
                pass
            return Buffer
        except (socket.error, OSError):
            return b""
        finally:
            try:
                Sock.close()
            except (socket.error, OSError):
                pass

    @staticmethod
    def _HttpHead(Alvo, Porta, Timeout, Esquema="http"):
        import urllib.request
        import urllib.error
        Ctx = None
        if Esquema == "https":
            Ctx = ssl.create_default_context()
            Ctx.check_hostname = False
            Ctx.verify_mode = ssl.CERT_NONE
        Url = f"{Esquema}://{Alvo}:{Porta}/"
        try:
            Req = urllib.request.Request(Url, method="HEAD",
                headers={"User-Agent": "ByP4ss/1.0", "Accept": "*/*"})
            with urllib.request.urlopen(Req, timeout=Timeout, context=Ctx) as F:
                Headers = {K.lower(): V for K, V in F.headers.items()}
                return ServiceFingerprint._ParseHeaders(Headers)
        except urllib.error.HTTPError as E:
            Headers = {K.lower(): V for K, V in (E.headers or {}).items()}
            return ServiceFingerprint._ParseHeaders(Headers)
        except Exception:
            return {}

    @staticmethod
    def _ParseHeaders(Headers):
        Extra = {}
        Server = Headers.get("server", "")
        Powered = Headers.get("x-powered-by", "")
        Auth = Headers.get("www-authenticate", "")
        Combinado = (Server + " " + Powered + " " + Auth).lower()
        Fabricante = ServiceFingerprint._DetectarFabricante(Combinado)
        if Fabricante:
            Extra["fabricante"] = Fabricante
        if Server:
            Extra["servidor"] = Server[:100]
        Modelo = ServiceFingerprint._ExtrairModelo(Server) or ServiceFingerprint._ExtrairModelo(Combinado)
        if Modelo:
            Extra["modelo"] = Modelo
        Os = ServiceFingerprint._OsPorServer(Server)
        if Os:
            Extra["os"] = Os
        return Extra

    @staticmethod
    def _TlsCertificado(Alvo, Porta, Timeout):
        Ctx = ssl.create_default_context()
        Ctx.check_hostname = False
        Ctx.verify_mode = ssl.CERT_NONE
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(Timeout)
        try:
            if Sock.connect_ex((Alvo, int(Porta))) != 0:
                return {}
            with Ctx.wrap_socket(Sock, server_hostname=Alvo) as SslSock:
                Cert = SslSock.getpeercert()
                if not Cert:
                    return {}
                Texto = str(Cert).lower()
                Extra = {}
                Fab = ServiceFingerprint._DetectarFabricante(Texto)
                if Fab:
                    Extra["fabricante"] = Fab
                Subject = dict(X[0] for X in Cert.get("subject", []))
                Cn = Subject.get("commonName", "")
                if Cn and len(Cn) < 80:
                    Extra["modelo"] = Cn
                return Extra
        except Exception:
            return {}
        finally:
            try:
                Sock.close()
            except (socket.error, OSError):
                pass

    @staticmethod
    def _ParseBanner(Banner):
        Extra = {}
        if not Banner:
            return Extra
        try:
            Texto = Banner.decode("utf-8", errors="replace")
        except Exception:
            return Extra
        Baixo = Texto.lower()
        Fab = ServiceFingerprint._DetectarFabricante(Baixo)
        if Fab:
            Extra["fabricante"] = Fab
        if "ssh-2.0" in Baixo or "ssh-1.99" in Baixo:
            Extra["os"] = "Linux"
            Extra["servidor"] = "OpenSSH"
        elif "ssh" in Baixo:
            Extra["servidor"] = "SSH"
        if "dropbear" in Baixo:
            Extra["servidor"] = "Dropbear"
            Extra["os"] = "Embedded Linux"
        if "busybox" in Baixo:
            Extra["os"] = "Embedded Linux"
        if "mini_httpd" in Baixo:
            Extra["servidor"] = "mini_httpd"
        if "lighttpd" in Baixo:
            Extra["servidor"] = "lighttpd"
        Modelo = ServiceFingerprint._ExtrairModelo(Texto)
        if Modelo:
            Extra["modelo"] = Modelo
        return Extra

    @staticmethod
    def _DetectarFabricante(Texto):
        if not Texto:
            return None
        Baixo = Texto.lower()
        for Nome, Chaves in ServiceFingerprint.ASSINATURAS_FABRICANTE:
            for Chave in Chaves:
                if Chave in Baixo:
                    return Nome
        return None

    @staticmethod
    def _ExtrairModelo(Texto):
        if not Texto:
            return None
        Padroes = [
            r"(archer\s+[a-z0-9\-]+)",
            r"(tl-wr[a-z0-9\-]+)",
            r"(dns-[a-z0-9\-]+)",
            r"(dir-[a-z0-9\-]+)",
            r"(ac[0-9]{2,4})",
            r"(hg[0-9]{4,5})",
            r"(f6[0-9]{3,4}[a-z]?)",
            r"(rv[0-9]{3})",
            r"(r7[0-9]{3})",
            r"(rt-[a-z0-9]+)",
            r"(a[0-9]{4})",
            r"(efm[a-z0-9\-]*)",
        ]
        Baixo = Texto.lower()
        for Padrao in Padroes:
            M = re.search(Padrao, Baixo)
            if M:
                return M.group(1).upper()
        return None

    @staticmethod
    def _OsPorServer(Server):
        if not Server:
            return None
        S = Server.lower()
        if "linux" in S or "ubuntu" in S or "debian" in S:
            return "Linux"
        if "windows" in S or "microsoft" in S:
            return "Windows"
        if "routeros" in S or "mikrotik" in S:
            return "RouterOS"
        if "openwrt" in S:
            return "OpenWrt"
        return None

    @staticmethod
    def Info():
        return {
            "nome": "ServiceFingerprint",
            "fabricantes": [N for N, _ in ServiceFingerprint.ASSINATURAS_FABRICANTE],
            "portas_http": list(ServiceFingerprint.PORTAS_HTTP),
            "portas_https": list(ServiceFingerprint.PORTAS_HTTPS),
        }


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 2 and sys.argv[1] == "teste":
        Alvo = sys.argv[2]
        Portas = [int(X) for X in sys.argv[3].split(",")] if len(sys.argv) > 3 else [80, 443, 8080]
        print(f"fingerprint de {Alvo} portas={Portas}")
        R = ServiceFingerprint.Identificar(Alvo, Portas)
        print(json.dumps(R, indent=2, ensure_ascii=False, default=str))
