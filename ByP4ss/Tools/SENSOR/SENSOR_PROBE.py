# SENSOR_PROBE — testa todas as fontes de sensores
# Com root, sem root, com termux-api, sem termux-api.
# Reporta o que funciona e o que nao funciona.

import os
import sys
import json
import subprocess
import shutil

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(DIR)))


class Probe:
    Resultados = {}

    @staticmethod
    def _Existe(Cmd):
        return shutil.which(Cmd) is not None

    @staticmethod
    def _Rodar(Cmd, Timeout=3):
        try:
            Saida = subprocess.check_output(Cmd, shell=True, timeout=Timeout, stderr=subprocess.DEVNULL)
            return Saida.decode("utf-8", errors="replace").strip()
        except Exception:
            return None

    @staticmethod
    def _Ler(Caminho):
        try:
            with open(Caminho, "r") as F:
                return F.read().strip()
        except Exception:
            return None

    @staticmethod
    def _Root():
        try:
            Saida = subprocess.check_output("id -u", shell=True, timeout=2, stderr=subprocess.DEVNULL)
            return Saida.decode().strip() == "0"
        except Exception:
            return False

    @staticmethod
    def TestarWifi():
        R = {"ssid": None, "bssid": None, "sinal": None, "fonte": None, "testes": []}

        # 1. termux-api
        if Probe._Existe("termux-wifi-connectioninfo"):
            S = Probe._Rodar("termux-wifi-connectioninfo")
            if S:
                try:
                    J = json.loads(S)
                    R["ssid"] = J.get("ssid")
                    R["bssid"] = J.get("bssid")
                    R["sinal"] = J.get("rssi")
                    R["fonte"] = "termux-api"
                    R["testes"].append("termux-api: OK")
                except Exception:
                    R["testes"].append("termux-api: JSON invalido")
            else:
                R["testes"].append("termux-api: sem resposta")
        else:
            R["testes"].append("termux-api: nao instalado")

        # 2. getprop (wifi.interface)
        S = Probe._Rodar("getprop wifi.interface")
        if S:
            R["testes"].append(f"getprop wifi.interface: {S}")

        # 3. /proc/net/wireless
        S = Probe._Ler("/proc/net/wireless")
        if S:
            R["testes"].append(f"/proc/net/wireless: OK ({len(S)} bytes)")
            if R["sinal"] is None:
                for Linha in S.split("\n"):
                    if "wlan" in Linha:
                        P = Linha.split()
                        if len(P) >= 4:
                            try:
                                R["sinal"] = int(P[3].rstrip("."))
                                R["fonte"] = "proc"
                                R["testes"].append(f"proc sinal: {R['sinal']}")
                            except ValueError:
                                pass
        else:
            R["testes"].append("/proc/net/wireless: bloqueado")

        # 4. /sys/class/net/wlan0/wireless/
        if os.path.exists("/sys/class/net/wlan0/wireless"):
            R["testes"].append("/sys/class/net/wlan0/wireless: existe")
        else:
            R["testes"].append("/sys/class/net/wlan0/wireless: bloqueado")

        # 5. iw dev (se existir)
        if Probe._Existe("iw"):
            S = Probe._Rodar("iw dev wlan0 link")
            if S and "SSID" in S:
                R["testes"].append("iw dev: OK")
                for L in S.split("\n"):
                    if "SSID" in L:
                        R["ssid"] = L.split(":", 1)[1].strip()
                        R["fonte"] = "iw"
            else:
                R["testes"].append("iw dev: bloqueado")
        else:
            R["testes"].append("iw dev: nao instalado")

        # 6. dumpsys wifi (root)
        if Probe._Root():
            S = Probe._Rodar("dumpsys wifi | grep -E 'mWifiInfo|SSID' | head -5")
            if S:
                R["testes"].append(f"dumpsys wifi (root): OK")
                for L in S.split("\n"):
                    if "SSID" in L and R["ssid"] is None:
                        R["ssid"] = L.split("SSID:", 1)[-1].strip().strip('"')
                        R["fonte"] = "dumpsys"
        else:
            R["testes"].append("dumpsys wifi: sem root")

        return R

    @staticmethod
    def TestarBateria():
        R = {"nivel": None, "status": None, "temp": None, "fonte": None, "testes": []}

        # 1. termux-api
        if Probe._Existe("termux-battery-status"):
            S = Probe._Rodar("termux-battery-status")
            if S:
                try:
                    J = json.loads(S)
                    R["nivel"] = J.get("percentage")
                    R["status"] = J.get("status")
                    R["temp"] = J.get("temperature")
                    R["fonte"] = "termux-api"
                    R["testes"].append("termux-api: OK")
                except Exception:
                    R["testes"].append("termux-api: JSON invalido")
            else:
                R["testes"].append("termux-api: sem resposta")
        else:
            R["testes"].append("termux-api: nao instalado")

        # 2. /sys/class/power_supply/
        for Base in ["/sys/class/power_supply/battery", "/sys/class/power_supply/BAT0"]:
            if os.path.exists(Base):
                Cap = Probe._Ler(f"{Base}/capacity")
                if Cap:
                    R["nivel"] = int(Cap)
                    R["fonte"] = "sys"
                    R["testes"].append(f"{Base}: OK")
                    break
            else:
                R["testes"].append(f"{Base}: bloqueado")

        # 3. dumpsys battery (root)
        if Probe._Root():
            S = Probe._Rodar("dumpsys battery")
            if S:
                R["testes"].append("dumpsys battery (root): OK")
                for L in S.split("\n"):
                    if "level:" in L and R["nivel"] is None:
                        R["nivel"] = int(L.split(":")[1].strip())
                        R["fonte"] = "dumpsys"
                    if "temperature:" in L and R["temp"] is None:
                        R["temp"] = int(L.split(":")[1].strip()) / 10
        else:
            R["testes"].append("dumpsys battery: sem root")

        return R

    @staticmethod
    def TestarRede():
        R = {"ip": None, "gateway": None, "arp": [], "fonte": None, "testes": []}

        # 1. getprop (dhcp)
        S = Probe._Rodar("getprop | grep -E 'dhcp|gateway' | head -10")
        if S:
            R["testes"].append(f"getprop dhcp: {len(S.splitlines())} linhas")

        # 2. /proc/net/route
        S = Probe._Ler("/proc/net/route")
        if S and len(S) > 50:
            R["testes"].append("/proc/net/route: OK")
            for L in S.split("\n")[1:]:
                P = L.split()
                if len(P) >= 3 and P[1] == "00000000":
                    try:
                        Gw = int(P[2], 16)
                        Ip = ".".join(str((Gw >> (8 * I)) & 0xFF) for I in range(4))
                        R["gateway"] = Ip
                        R["fonte"] = "proc"
                    except ValueError:
                        pass
        else:
            R["testes"].append("/proc/net/route: bloqueado")

        # 3. /proc/net/arp
        S = Probe._Ler("/proc/net/arp")
        if S and len(S) > 50:
            R["testes"].append("/proc/net/arp: OK")
            for L in S.split("\n")[1:]:
                P = L.split()
                if len(P) >= 4:
                    R["arp"].append({"ip": P[0], "mac": P[3]})
        else:
            R["testes"].append("/proc/net/arp: bloqueado")

        # 4. mini_ip (netlink, se compilado)
        MiniIp = os.path.join(os.path.dirname(DIR), "Discovery", "portscan", "mini_ip")
        if os.path.exists(MiniIp):
            S = Probe._Rodar(f"{MiniIp} route show")
            if S and "default" in S:
                R["testes"].append("mini_ip: OK")
                for L in S.split("\n"):
                    if "default" in L:
                        P = L.split()
                        if "via" in P:
                            R["gateway"] = P[P.index("via") + 1]
                            R["fonte"] = "netlink"
        else:
            R["testes"].append("mini_ip: nao compilado")

        return R

    @staticmethod
    def TestarHardware():
        R = {"fabricante": None, "modelo": None, "fonte": None, "testes": []}

        # 1. getprop
        Fab = Probe._Rodar("getprop ro.product.manufacturer")
        Mod = Probe._Rodar("getprop ro.product.model")
        if Fab or Mod:
            R["fabricante"] = Fab
            R["modelo"] = Mod
            R["fonte"] = "getprop"
            R["testes"].append("getprop: OK")
        else:
            R["testes"].append("getprop: sem resposta")

        # 2. /sys/class/dmi/id/
        if os.path.exists("/sys/class/dmi/id/product_name"):
            Mod = Probe._Ler("/sys/class/dmi/id/product_name")
            if Mod:
                R["modelo"] = Mod
                R["fonte"] = "dmi"
                R["testes"].append("dmi: OK")
        else:
            R["testes"].append("dmi: bloqueado")

        return R

    @staticmethod
    def Executar():
        Probe.Resultados = {
            "root": Probe._Root(),
            "termux_api": {
                "battery": Probe._Existe("termux-battery-status"),
                "wifi": Probe._Existe("termux-wifi-connectioninfo"),
                "location": Probe._Existe("termux-location"),
            },
            "wifi": Probe.TestarWifi(),
            "bateria": Probe.TestarBateria(),
            "rede": Probe.TestarRede(),
            "hardware": Probe.TestarHardware(),
        }
        return Probe.Resultados


if __name__ == "__main__":
    R = Probe.Executar()
    print(json.dumps(R, indent=2, ensure_ascii=False))
