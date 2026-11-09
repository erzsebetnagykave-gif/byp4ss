# SENSOR — wrapper Python
# Hardware via /sys + /proc + getprop
# Rede via Netlink (libnetlink.so) — sem /proc, sem iproute2
# Sem dependencia externa. So C e stdlib.

import ctypes
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
LIB_SENSOR = os.path.join(DIR, "libsensor.so")
LIB_NETLINK = os.path.join(DIR, "Core", "libnetlink.so")


class Sensor:

    _LibSensor = None
    _LibNetlink = None

    @staticmethod
    def CarregarSensor():
        if Sensor._LibSensor is not None:
            return Sensor._LibSensor
        if not os.path.exists(LIB_SENSOR):
            return None
        try:
            Lib = ctypes.CDLL(LIB_SENSOR)
            Lib.SensorLer.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
            Lib.SensorLer.restype = ctypes.c_int
            Sensor._LibSensor = Lib
            return Lib
        except OSError:
            return None

    @staticmethod
    def CarregarNetlink():
        if Sensor._LibNetlink is not None:
            return Sensor._LibNetlink
        if not os.path.exists(LIB_NETLINK):
            return None
        try:
            Lib = ctypes.CDLL(LIB_NETLINK)
            Lib.NetlinkCriar.restype = ctypes.c_void_p
            Lib.NetlinkDestruir.argtypes = [ctypes.c_void_p]
            Lib.NetlinkListarInterfaces.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
            Lib.NetlinkListarInterfaces.restype = ctypes.c_int
            Lib.NetlinkListarRotas.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
            Lib.NetlinkListarRotas.restype = ctypes.c_int
            Lib.NetlinkListarVizinhos.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
            Lib.NetlinkListarVizinhos.restype = ctypes.c_int
            Sensor._LibNetlink = Lib
            return Lib
        except OSError:
            return None

    @staticmethod
    def Ler(Tipo):
        Lib = Sensor.CarregarSensor()
        if Lib is None:
            return None
        Buf = ctypes.create_string_buffer(16384)
        R = Lib.SensorLer(Tipo.encode(), Buf, ctypes.sizeof(Buf))
        if R != 0:
            return None
        return Buf.value.decode("utf-8", errors="replace")

    @staticmethod
    def Cpu():
        S = Sensor.Ler("cpu")
        if not S:
            return None
        P = S.split("|")
        return {
            "modelo": P[0] if len(P) > 0 else "desconhecido",
            "cores": int(P[1]) if len(P) > 1 and P[1].isdigit() else 0,
            "freq_mhz": int(P[2]) if len(P) > 2 and P[2].isdigit() else 0,
        }

    @staticmethod
    def Memoria():
        S = Sensor.Ler("mem")
        if not S:
            return None
        P = S.split("|")
        if len(P) < 3:
            return None
        return {
            "total_mb": int(P[0]),
            "livre_mb": int(P[1]),
            "disponivel_mb": int(P[2]),
        }

    @staticmethod
    def Bateria():
        S = Sensor.Ler("bateria")
        if not S:
            return None
        P = S.split("|")
        if len(P) < 4:
            return None
        Nivel = int(P[0]) if P[0].isdigit() else 0
        if Nivel == 0 and P[1] == "desconhecido":
            return None
        return {
            "nivel": Nivel,
            "status": P[1],
            "temp_c": int(P[2]) if P[2].lstrip("-").isdigit() else 0,
            "voltagem_mv": int(P[3]) if P[3].isdigit() else 0,
        }

    @staticmethod
    def Temperatura():
        S = Sensor.Ler("temp")
        if not S:
            return None
        T = int(S) if S.isdigit() else 0
        return T if T > 0 else None

    @staticmethod
    def Hardware():
        S = Sensor.Ler("hw")
        if not S:
            return None
        P = S.split("|")
        if len(P) < 4:
            return None
        if P[0] == "desconhecido" and P[1] == "desconhecido":
            return None
        return {
            "fabricante": P[0],
            "modelo": P[1],
            "serial": P[2],
            "bios": P[3],
        }

    @staticmethod
    def Kernel():
        S = Sensor.Ler("kernel")
        if not S:
            return None
        P = S.split("|")
        if len(P) < 4:
            return None
        return {
            "sysname": P[0],
            "release": P[1],
            "version": P[2],
            "machine": P[3],
        }

    @staticmethod
    def Uptime():
        S = Sensor.Ler("uptime")
        if not S:
            return None
        return int(S) if S.isdigit() else 0

    @staticmethod
    def Disco():
        S = Sensor.Ler("disco")
        if not S:
            return None
        P = S.split("|")
        if len(P) < 3:
            return None
        return {
            "total_mb": int(P[0]),
            "usado_mb": int(P[1]),
            "livre_mb": int(P[2]),
        }

    @staticmethod
    def InterfacesNetlink():
        Lib = Sensor.CarregarNetlink()
        if Lib is None:
            return []
        N = Lib.NetlinkCriar()
        Buf = ctypes.create_string_buffer(32768)
        Lib.NetlinkListarInterfaces(N, Buf, ctypes.sizeof(Buf))
        Lib.NetlinkDestruir(N)
        Resultado = []
        for Linha in Buf.value.decode("utf-8", errors="replace").strip().split("\n"):
            if not Linha:
                continue
            P = Linha.split("|")
            if len(P) >= 4:
                Resultado.append({
                    "nome": P[0],
                    "mac": P[1],
                    "estado": P[2],
                    "mtu": int(P[3]) if P[3].isdigit() else 0,
                })
        return Resultado

    @staticmethod
    def Interfaces():
        Ifaces = Sensor.InterfacesNetlink()
        if Ifaces:
            return Ifaces
        Ifaces = []
        for I in Sensor.Ler("ifaces").strip().split("\n") if Sensor.Ler("ifaces") else []:
            if not I:
                continue
            P = I.split("|")
            if len(P) >= 4:
                Ifaces.append({
                    "nome": P[0],
                    "mac": P[1],
                    "estado": P[2],
                    "mtu": int(P[3]) if P[3].isdigit() else 0,
                })
        return Ifaces

    @staticmethod
    def RotasNetlink():
        Lib = Sensor.CarregarNetlink()
        if Lib is None:
            return []
        N = Lib.NetlinkCriar()
        Buf = ctypes.create_string_buffer(32768)
        Lib.NetlinkListarRotas(N, Buf, ctypes.sizeof(Buf))
        Lib.NetlinkDestruir(N)
        Resultado = []
        for Linha in Buf.value.decode("utf-8", errors="replace").strip().split("\n"):
            if not Linha:
                continue
            P = Linha.split("|")
            if len(P) >= 4:
                Resultado.append({
                    "destino": P[0],
                    "gateway": P[1],
                    "interface": P[2],
                    "metrica": int(P[3]) if P[3].isdigit() else 0,
                })
        return Resultado

    @staticmethod
    def Rotas():
        return Sensor.RotasNetlink()

    @staticmethod
    def VizinhosNetlink():
        Lib = Sensor.CarregarNetlink()
        if Lib is None:
            return []
        N = Lib.NetlinkCriar()
        Buf = ctypes.create_string_buffer(32768)
        Lib.NetlinkListarVizinhos(N, Buf, ctypes.sizeof(Buf))
        Lib.NetlinkDestruir(N)
        Resultado = []
        for Linha in Buf.value.decode("utf-8", errors="replace").strip().split("\n"):
            if not Linha:
                continue
            P = Linha.split("|")
            if len(P) >= 4:
                Resultado.append({
                    "ip": P[0],
                    "mac": P[1],
                    "interface": P[2],
                    "estado": P[3],
                })
        return Resultado

    @staticmethod
    def Vizinhos():
        return Sensor.VizinhosNetlink()

    @staticmethod
    def Arp():
        return Sensor.VizinhosNetlink()

    @staticmethod
    def Gateway(Interface=None):
        Rotas = Sensor.Rotas()
        for R in Rotas:
            if R["destino"] == "default" and R["gateway"]:
                if Interface is None or R["interface"] == Interface:
                    return R["gateway"]
        return None

    @staticmethod
    def InterfacesUnicas():
        Vistos = set()
        Unicas = []
        for R in Sensor.Rotas():
            Iface = R["interface"]
            if Iface and Iface not in Vistos:
                Vistos.add(Iface)
                Unicas.append(Iface)
        return sorted(Unicas)

    @staticmethod
    def Wifi():
        S = Sensor.Ler("wifi")
        if not S:
            return None
        P = S.split("|")
        if len(P) < 4:
            return None
        if P[0] == "desconhecido" and P[3] == "0":
            return None
        return {
            "ssid": P[0],
            "bssid": P[1],
            "frequencia": P[2],
            "sinal": P[3],
        }

    @staticmethod
    def SnapshotCompleto():
        return {
            "cpu": Sensor.Cpu(),
            "mem": Sensor.Memoria(),
            "bateria": Sensor.Bateria(),
            "temp": Sensor.Temperatura(),
            "hw": Sensor.Hardware(),
            "kernel": Sensor.Kernel(),
            "uptime": Sensor.Uptime(),
            "wifi": Sensor.Wifi(),
            "ifaces": Sensor.Interfaces(),
            "interfaces_unicas": Sensor.InterfacesUnicas(),
            "rotas": Sensor.Rotas(),
            "vizinhos": Sensor.Vizinhos(),
            "gateway": Sensor.Gateway(),
            "disco": Sensor.Disco(),
        }

    @staticmethod
    def SnapshotRede():
        return {
            "interfaces": Sensor.InterfacesUnicas(),
            "rotas": Sensor.Rotas(),
            "vizinhos": Sensor.Vizinhos(),
            "gateway": Sensor.Gateway(),
            "gateway_wifi": Sensor.Gateway("ap0"),
        }
