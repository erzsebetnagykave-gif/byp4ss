import sys
import os
import json
import time
import socket
import argparse
import importlib
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from Core.Engine import Engine
except ImportError:
    Engine = None


class Analise:

    PORTAS_PADRAO = [21, 22, 23, 53, 80, 443, 8080, 8443, 1900, 5000, 52869]
    ASSINATURAS_FABRICANTE = [
        ("dlink",      ["dlink", "d-link", "dns-", "nas_sharing"]),
        ("tenda",      ["tenda", "ac9", "ac15", "ac6", "w20e"]),
        ("tplink",     ["tp-link", "tplink", "archer", "tl-wr", "tl-wa"]),
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
    ]
    MODELO_PARA_EXPLOIT = {
        "dlink":      "dlink",
        "tenda":      "tenda7795",
        "tplink":     "tplink",
        "arcadyan":   "arcadyan",
        "iptime":     "iptime",
    }

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def ImportarModulo(Caminho, Classe):
        try:
            M = importlib.import_module(Caminho)
            return getattr(M, Classe, None)
        except Exception:
            return None

    @staticmethod
    def DetectarFabricante(Alvo=None, Ssdp=None, Descritor=None, CorpoHtml=None, Headers=None):
        Fontes = []
        if Ssdp:
            for K in ("servidor", "server", "fabricante", "manufacturer", "modelo", "model", "model_name"):
                V = Ssdp.get(K) if isinstance(Ssdp, dict) else None
                if V:
                    Fontes.append(("ssdp", str(V)))
        if Descritor:
            for K in ("fabricante", "manufacturer", "modelo", "model", "model_name"):
                V = Descritor.get(K) if isinstance(Descritor, dict) else None
                if V:
                    Fontes.append(("descritor", str(V)))
        if CorpoHtml:
            Fontes.append(("html", str(CorpoHtml)[:4096]))
        if Headers:
            for K, V in Headers.items():
                if str(K).lower() == "server":
                    Fontes.append(("header", str(V)))
        Fabricante = None
        Modelo = None
        FonteFinal = None
        for Fonte, Texto in Fontes:
            Lower = Texto.lower()
            for Fab, Chaves in Analise.ASSINATURAS_FABRICANTE:
                for Chave in Chaves:
                    if Chave in Lower:
                        Fabricante = Fab
                        FonteFinal = Fonte
                        break
                if Fabricante:
                    break
            if Fabricante:
                for Fab, Chaves in Analise.ASSINATURAS_FABRICANTE:
                    if Fab != Fabricante:
                        continue
                    for Chave in Chaves:
                        if Chave in Lower and len(Chave) > 3:
                            Modelo = Chave
                            break
                break
        return {"ok": bool(Fabricante), "fabricante": Fabricante, "modelo": Modelo,
                "fonte": FonteFinal, "fontes_consultadas": len(Fontes)}

    @staticmethod
    def SugerirExploits(Fabricante, Modelo, PortasAbertas=None):
        PortasAbertas = PortasAbertas or []
        Sugestoes = []
        if Fabricante and Fabricante in Analise.MODELO_PARA_EXPLOIT:
            Id = Analise.MODELO_PARA_EXPLOIT[Fabricante]
            Sugestoes.append({"id": Id, "fabricante": Fabricante, "modelo": Modelo,
                              "prioridade": 1, "motivo": "fabricante_detectado"})
        if Fabricante == "tenda" and (80 in PortasAbertas):
            Sugestoes.append({"id": "tenda29384", "fabricante": "tenda", "modelo": Modelo,
                              "prioridade": 2, "motivo": "tenda_com_http"})
        if 80 not in PortasAbertas and 443 not in PortasAbertas and 8080 not in PortasAbertas:
            for S in Sugestoes:
                S["prioridade"] += 1
                S["motivo"] += ":sem_http"
        Vistos = set()
        Finais = []
        for S in sorted(Sugestoes, key=lambda X: X["prioridade"]):
            if S["id"] in Vistos:
                continue
            Vistos.add(S["id"])
            Finais.append(S)
        return {"ok": bool(Finais), "exploits": Finais, "total": len(Finais)}

    @staticmethod
    def EscanearAlvo(Alvo, Portas=None, Threads=10, Timeout=3):
        Portas = Portas or Analise.PORTAS_PADRAO
        Resultado = {"ok": False, "alvo": Alvo, "portas_abertas": [], "ssdp": None,
                     "descritor": None, "credenciais": [], "fabricante": None,
                     "modelo": None, "cves_sugeridas": [], "timestamp": Analise.Timestamp()}

        PortScanCls = Analise.ImportarModulo("Discovery.PortScan", "PortScan")
        if PortScanCls is not None and hasattr(PortScanCls, "Escanear"):
            try:
                R = PortScanCls.Escanear(Alvo, Portas, Threads)
                Abertas = []
                if isinstance(R, list):
                    for I in R:
                        if isinstance(I, dict):
                            if I.get("estado") == "aberta" and I.get("porta") is not None:
                                Abertas.append(I["porta"])
                            elif I.get("aberta") is True and I.get("porta") is not None:
                                Abertas.append(I["porta"])
                        elif isinstance(I, int):
                            Abertas.append(I)
                elif isinstance(R, dict):
                    for I in (R.get("portas") or R.get("abertas") or []):
                        if isinstance(I, dict) and I.get("porta") is not None:
                            if I.get("estado") == "aberta" or I.get("aberta") is True:
                                Abertas.append(I["porta"])
                        elif isinstance(I, int):
                            Abertas.append(I)
                Resultado["portas_abertas"] = sorted(set(Abertas))
                Resultado["ok"] = True
            except Exception as E:
                Resultado["erro_portscan"] = f"{type(E).__name__}:{E}"

        SsdpCls = Analise.ImportarModulo("Discovery.Ssdp", "Ssdp")
        if SsdpCls is not None and hasattr(SsdpCls, "Descobrir"):
            try:
                Resultado["ssdp"] = SsdpCls.Descobrir(Alvo)
            except Exception as E:
                Resultado["erro_ssdp"] = f"{type(E).__name__}:{E}"

        DescritorCls = Analise.ImportarModulo("Discovery.Descriptor", "Descriptor")
        if DescritorCls is not None and hasattr(DescritorCls, "Analisar"):
            Local = None
            if isinstance(Resultado.get("ssdp"), dict):
                Local = Resultado["ssdp"].get("local") or Resultado["ssdp"].get("descritor")
            if Local:
                try:
                    Resultado["descritor"] = DescritorCls.Analisar(Local)
                except Exception as E:
                    Resultado["erro_descriptor"] = f"{type(E).__name__}:{E}"

        if Engine is not None and hasattr(Engine, "Credenciais"):
            try:
                C = Engine.Credenciais(Alvo)
                if C.get("ok"):
                    Resultado["credenciais"] = C.get("credenciais", [])
            except Exception as E:
                Resultado["erro_credenciais"] = f"{type(E).__name__}:{E}"

        Fab = Analise.DetectarFabricante(Alvo, Resultado.get("ssdp"), Resultado.get("descritor"))
        if Fab.get("ok"):
            Resultado["fabricante"] = Fab["fabricante"]
            Resultado["modelo"] = Fab["modelo"]

        S = Analise.SugerirExploits(Resultado["fabricante"], Resultado["modelo"], Resultado["portas_abertas"])
        Resultado["cves_sugeridas"] = S.get("exploits", [])

        return Resultado

    @staticmethod
    def EscanearRede(Subrede=None, Portas=None, Threads=10, Timeout=3):
        Alvos = []
        if Subrede:
            try:
                Base = Subrede.rsplit(".", 1)[0]
                Alvos = [f"{Base}.{N}" for N in range(1, 255)]
            except Exception:
                Alvos = [Subrede]
        if not Alvos:
            return {"ok": False, "motivo": "subrede_vazia", "hosts": [], "total": 0}
        Hosts = []
        SsdpCls = Analise.ImportarModulo("Discovery.Ssdp", "Ssdp")
        Descobertos = set()
        if SsdpCls is not None and hasattr(SsdpCls, "Descobrir"):
            for A in Alvos[:1]:
                try:
                    R = SsdpCls.Descobrir(A)
                    if isinstance(R, dict) and R.get("ok"):
                        Ip = R.get("ip") or R.get("host") or A
                        Descobertos.add(str(Ip))
                except Exception:
                    pass
        Lista = sorted(Descobertos) if Descobertos else Alvos[:32]
        for A in Lista:
            try:
                R = Analise.EscanearAlvo(A, Portas, Threads, Timeout)
                if R.get("ok") and (R.get("portas_abertas") or R.get("ssdp")):
                    Hosts.append({"ip": A, "portas_abertas": R.get("portas_abertas", []),
                                  "fabricante": R.get("fabricante"), "modelo": R.get("modelo"),
                                  "credenciais_total": len(R.get("credenciais", [])),
                                  "cves_sugeridas": R.get("cves_sugeridas", [])})
            except Exception:
                pass
        return {"ok": True, "subrede": Subrede, "hosts": Hosts, "total": len(Hosts),
                "timestamp": Analise.Timestamp()}

    @staticmethod
    def CompararAnalises(Antiga, Nova):
        if not isinstance(Antiga, dict) or not isinstance(Nova, dict):
            return {"ok": False, "motivo": "analises_precisam_ser_dict"}
        HostsA = {H.get("ip"): H for H in (Antiga.get("hosts") or []) if H.get("ip")}
        HostsN = {H.get("ip"): H for H in (Nova.get("hosts") or []) if H.get("ip")}
        Adicionados = sorted(set(HostsN.keys()) - set(HostsA.keys()))
        Removidos = sorted(set(HostsA.keys()) - set(HostsN.keys()))
        PortasAbertasNovas = []
        PortasFechadas = []
        for Ip in sorted(set(HostsA.keys()) & set(HostsN.keys())):
            PA = set(HostsA[Ip].get("portas_abertas", []))
            PN = set(HostsN[Ip].get("portas_abertas", []))
            for P in (PN - PA):
                PortasAbertasNovas.append({"ip": Ip, "porta": P})
            for P in (PA - PN):
                PortasFechadas.append({"ip": Ip, "porta": P})
        Total = len(Adicionados) + len(Removidos) + len(PortasAbertasNovas) + len(PortasFechadas)
        return {"ok": True, "hosts_novos": Adicionados, "hosts_sumidos": Removidos,
                "portas_abertas_novas": PortasAbertasNovas, "portas_fechadas": PortasFechadas,
                "total_mudancas": Total, "timestamp": Analise.Timestamp()}

    @staticmethod
    def Main():
        P = argparse.ArgumentParser(prog="Analise")
        Sub = P.add_subparsers(dest="cmd")
        A = Sub.add_parser("alvo")
        A.add_argument("alvo")
        A.add_argument("--portas", default=None)
        A.add_argument("--threads", type=int, default=10)
        A.add_argument("--json", action="store_true")
        R = Sub.add_parser("rede")
        R.add_argument("subrede")
        R.add_argument("--threads", type=int, default=10)
        R.add_argument("--json", action="store_true")
        D = Sub.add_parser("diff")
        D.add_argument("antiga")
        D.add_argument("nova")
        Args = P.parse_args()

        if Args.cmd == "alvo":
            Portas = [int(X.strip()) for X in Args.portas.split(",")] if Args.portas else None
            Res = Analise.EscanearAlvo(Args.alvo, Portas, Args.threads)
        elif Args.cmd == "rede":
            Res = Analise.EscanearRede(Args.subrede, None, Args.threads)
        elif Args.cmd == "diff":
            try:
                with open(Args.antiga, "r", encoding="utf-8") as F:
                    Ant = json.load(F)
                with open(Args.nova, "r", encoding="utf-8") as F:
                    Nov = json.load(F)
            except Exception as E:
                print(f"[erro] {E}", file=sys.stderr)
                return 2
            Res = Analise.CompararAnalises(Ant, Nov)
        else:
            P.print_help()
            return 2

        if getattr(Args, "json", False):
            print(json.dumps(Res, indent=2, ensure_ascii=False))
        else:
            if Args.cmd == "diff":
                print(f"hosts_novos: {Res.get('hosts_novos')}")
                print(f"hosts_sumidos: {Res.get('hosts_sumidos')}")
                print(f"portas_abertas_novas: {Res.get('portas_abertas_novas')}")
                print(f"portas_fechadas: {Res.get('portas_fechadas')}")
                print(f"total_mudancas: {Res.get('total_mudancas')}")
            elif Args.cmd == "rede":
                print(f"subrede: {Res.get('subrede')}  total: {Res.get('total')}")
                for H in Res.get("hosts", []):
                    print(f"  {H['ip']}  portas={H.get('portas_abertas')}  fab={H.get('fabricante')}")
            else:
                print(f"alvo: {Res.get('alvo')}")
                print(f"portas_abertas: {Res.get('portas_abertas')}")
                print(f"fabricante: {Res.get('fabricante')}  modelo: {Res.get('modelo')}")
                print(f"credenciais: {len(Res.get('credenciais', []))}")
                print(f"cves_sugeridas: {[S.get('id') for S in Res.get('cves_sugeridas', [])]}")
        return 0 if Res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(Analise.Main())
