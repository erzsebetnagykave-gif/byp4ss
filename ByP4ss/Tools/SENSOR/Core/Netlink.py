# Netlink.py — wrapper Python do libnetlink.so
# Le rede (interfaces, rotas, vizinhos) via NETLINK_ROUTE
# Sem /proc/net, sem iproute2, sem termux-api

import ctypes
import os

DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(DIR, "libnetlink.so")


class Netlink:

    _Lib = None

    @staticmethod
    def Carregar():
        if Netlink._Lib is not None:
            return Netlink._Lib
        if not os.path.exists(LIB_PATH):
            return None
        try:
            Lib = ctypes.CDLL(LIB_PATH)
            Lib.NetlinkCriar.restype = ctypes.c_void_p
            Lib.NetlinkDestruir.argtypes = [ctypes.c_void_p]
            Lib.NetlinkListarInterfaces.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
            Lib.NetlinkListarInterfaces.restype = ctypes.c_int
            Lib.NetlinkListarRotas.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
            Lib.NetlinkListarRotas.restype = ctypes.c_int
            Lib.NetlinkListarVizinhos.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t]
            Lib.NetlinkListarVizinhos.restype = ctypes.c_int
            Netlink._Lib = Lib
            return Lib
        except OSError:
            return None

    @staticmethod
    def Interfaces():
        Lib = Netlink.Carregar()
        if Lib is None:
            return []
        N = Lib.NetlinkCriar()
        Buf = ctypes.create_string_buffer(16384)
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
    def Rotas():
        Lib = Netlink.Carregar()
        if Lib is None:
            return []
        N = Lib.NetlinkCriar()
        Buf = ctypes.create_string_buffer(16384)
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
    def Vizinhos():
        Lib = Netlink.Carregar()
        if Lib is None:
            return []
        N = Lib.NetlinkCriar()
        Buf = ctypes.create_string_buffer(16384)
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
    def Gateway():
        Rotas = Netlink.Rotas()
        for R in Rotas:
            if R["destino"] == "default" and R["gateway"]:
                return R["gateway"]
        return None

    @staticmethod
    def Snapshot():
        return {
            "interfaces": Netlink.Interfaces(),
            "rotas": Netlink.Rotas(),
            "vizinhos": Netlink.Vizinhos(),
            "gateway": Netlink.Gateway(),
        }


if __name__ == "__main__":
    import json
    print(json.dumps(Netlink.Snapshot(), indent=2, ensure_ascii=False))
