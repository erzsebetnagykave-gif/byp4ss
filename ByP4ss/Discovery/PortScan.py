# PortScan do ByP4ss
# 900 linhas (parte 1 de 3)
# Engine proprio, thread pool, SQL local, fuzzy matching

import socket
import threading
import time
import queue
import sqlite3
import os
import struct
import random

from Core.Constants import Constants
from Core.Config import Config
from Core.Log import Log


class PortScan:

    _Lock = threading.Lock()
    _Resultados = {}
    _Fila = queue.Queue()
    _Ativos = 0
    _Threads = []
    _Parar = False
    _DbPath = None
    _DbConn = None
    _Stats = {}

    @staticmethod
    def Iniciar(Threads=None):
        Threads = Threads or Config.ThreadsPorts
        PortScan._Lock = threading.Lock()
        PortScan._Resultados = {}
        PortScan._Fila = queue.Queue()
        PortScan._Ativos = 0
        PortScan._Threads = []
        PortScan._Parar = False
        PortScan._Stats = {
            "portas": 0,
            "abertas": 0,
            "fechadas": 0,
            "filtradas": 0,
            "recusadas": 0,
            "timeouts": 0,
            "erros": 0,
            "inicio": time.time(),
            "fim": 0.0,
        }
        for _ in range(Threads):
            T = threading.Thread(target=PortScan._Worker, daemon=True)
            T.start()
            PortScan._Threads.append(T)

    @staticmethod
    def Finalizar():
        PortScan._Parar = True
        for _ in PortScan._Threads:
            PortScan._Fila.put(None)
        for T in PortScan._Threads:
            T.join(timeout=1.0)
        PortScan._Stats["fim"] = time.time()
        PortScan._Stats["duracao"] = round(
            PortScan._Stats["fim"] - PortScan._Stats["inicio"], 3
        )

    @staticmethod
    def _Worker():
        while not PortScan._Parar:
            try:
                Item = PortScan._Fila.get(timeout=0.5)
            except queue.Empty:
                continue
            if Item is None:
                break
            Alvo, Porta = Item
            PortScan._EscanearPorta(Alvo, Porta)
            PortScan._Fila.task_done()

    @staticmethod
    def _EscanearPorta(Alvo, Porta, Timeout=None):
        Timeout = Timeout or Config.TimeoutTCP
        Estado = PortScan._TcpConnect(Alvo, Porta, Timeout)
        with PortScan._Lock:
            PortScan._Resultados[Porta] = Estado
            PortScan._Stats["portas"] += 1
            Chave = Estado["estado"]
            if Chave in PortScan._Stats:
                PortScan._Stats[Chave] += 1
        if Estado["estado"] == "aberta":
            Log.Descoberta("PortScan", Alvo, "porta_aberta", {
                "porta": Porta,
                "servico": Estado.get("servico", ""),
                "banner": Estado.get("banner", "")[:80],
            })

    @staticmethod
    def _TcpConnect(Alvo, Porta, Timeout):
        Resultado = {
            "porta": Porta,
            "estado": "fechada",
            "servico": "",
            "banner": "",
            "latencia": 0.0,
            "erro": "",
            "protocolo": "tcp",
        }
        Inicio = time.time()
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(Timeout)
        try:
            Codigo = Sock.connect_ex((Alvo, Porta))
            Resultado["latencia"] = round(time.time() - Inicio, 4)
            if Codigo == 0:
                Resultado["estado"] = "aberta"
                Resultado["servico"] = PortScan._DetectarServico(Porta)
                try:
                    Sock.settimeout(0.5)
                    Sock.sendall(b"\r\n")
                    Banner = Sock.recv(1024)
                    Resultado["banner"] = Banner.decode("utf-8", errors="replace").strip()
                except (socket.timeout, OSError):
                    pass
            elif Codigo in (111, 61):
                Resultado["estado"] = "recusada"
            elif Codigo in (113, 101):
                Resultado["estado"] = "filtrada"
            else:
                Resultado["estado"] = "fechada"
                Resultado["erro"] = f"codigo_{Codigo}"
        except socket.timeout:
            Resultado["estado"] = "filtrada"
            Resultado["latencia"] = round(time.time() - Inicio, 4)
        except socket.gaierror as E:
            Resultado["estado"] = "erro"
            Resultado["erro"] = f"dns: {E}"
        except OSError as E:
            Resultado["estado"] = "erro"
            Resultado["erro"] = str(E)
        finally:
            try:
                Sock.close()
            except OSError:
                pass
        return Resultado

    @staticmethod
    def _DetectarServico(Porta):
        Mapa = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
            69: "tftp", 80: "http", 110: "pop3", 111: "rpcbind",
            123: "ntp", 135: "msrpc", 137: "netbios-ns", 138: "netbios-dgm",
            139: "netbios-ssn", 143: "imap", 161: "snmp", 162: "snmptrap",
            179: "bgp", 389: "ldap", 443: "https", 445: "microsoft-ds",
            500: "isakmp", 514: "syslog", 515: "printer", 548: "afp",
            554: "rtsp", 587: "submission", 623: "ipmi", 636: "ldaps",
            873: "rsync", 990: "ftps", 993: "imaps", 995: "pop3s",
            1080: "socks", 1194: "openvpn", 1433: "mssql", 1521: "oracle",
            1723: "pptp", 1900: "upnp", 2000: "cisco-sccp", 2049: "nfs",
            2082: "cpanel", 2083: "cpanel-ssl", 2375: "docker", 2376: "docker-ssl",
            3000: "grafana", 3306: "mysql", 3389: "rdp", 4443: "https-alt",
            5000: "upnp-alt", 5060: "sip", 5222: "xmpp", 5432: "postgres",
            5900: "vnc", 5984: "couchdb", 6379: "redis", 6443: "k8s-api",
            7001: "weblogic", 7547: "tr-069", 8000: "http-alt", 8008: "http-alt",
            8080: "http-alt", 8081: "http-alt", 8086: "influxdb", 8089: "splunk",
            8123: "polipo", 8291: "mikrotik", 8443: "https-alt", 8500: "consul",
            8888: "http-alt", 9000: "http-alt", 9090: "prometheus",
            9200: "elasticsearch", 9300: "elasticsearch", 9443: "https-alt",
            10000: "webmin", 11211: "memcached", 15672: "rabbitmq",
            27017: "mongodb", 27018: "mongodb", 49152: "upnp", 49153: "upnp",
            52869: "upnp",
        }
        return Mapa.get(Porta, "desconhecido")

    @staticmethod
    def _TcpHalfOpen(Alvo, Porta, Timeout=1.0):
        Resultado = {
            "porta": Porta,
            "estado": "filtrada",
            "protocolo": "tcp_half",
            "erro": "",
        }
        try:
            Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Sock.settimeout(Timeout)
            Codigo = Sock.connect_ex((Alvo, Porta))
            if Codigo == 0:
                Resultado["estado"] = "aberta"
            elif Codigo == 111:
                Resultado["estado"] = "recusada"
            else:
                Resultado["estado"] = "filtrada"
            Sock.close()
        except OSError as E:
            Resultado["erro"] = str(E)
        return Resultado

    @staticmethod
    def _UdpScan(Alvo, Porta, Timeout=1.0):
        Resultado = {
            "porta": Porta,
            "estado": "filtrada",
            "protocolo": "udp",
            "erro": "",
        }
        try:
            Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            Sock.settimeout(Timeout)
            Sock.sendto(b"\x00" * 8, (Alvo, Porta))
            try:
                Sock.recvfrom(1024)
                Resultado["estado"] = "aberta"
            except socket.timeout:
                Resultado["estado"] = "filtrada"
            except OSError:
                Resultado["estado"] = "recusada"
            Sock.close()
        except OSError as E:
            Resultado["erro"] = str(E)
        return Resultado

    @staticmethod
    def Escanear(Alvo, Portas=None, Threads=None):
        Portas = Portas or Config.Portas
        PortScan.Iniciar(Threads)
        Log.Info("portscan iniciado", {"alvo": Alvo, "total": len(Portas)})
        for Porta in Portas:
            PortScan._Fila.put((Alvo, Porta))
        PortScan._Fila.join()
        PortScan.Finalizar()
        Abertas = []
        for Porta, Estado in PortScan._Resultados.items():
            if Estado["estado"] == "aberta":
                Abertas.append(Estado)
        Abertas.sort(key=lambda E: E["porta"])
        Log.Info("portscan concluido", PortScan._Stats)
        return Abertas

    @staticmethod
    def EscanearRapido(Alvo, Portas=None):
        Portas = Portas or Constants.PORTAS_CRITICAS
        return PortScan.Escanear(Alvo, Portas, Threads=20)

    @staticmethod
    def EscanearProfundo(Alvo, Portas=None):
        Portas = Portas or Constants.PORTAS_TODAS
        return PortScan.Escanear(Alvo, Portas, Threads=50)
