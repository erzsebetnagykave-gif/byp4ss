# CveMatch do ByP4ss
# Correlaciona fingerprint (do ServiceFingerprint) + portas abertas
# com uma tabela de CVEs conhecidas.
# Chamado por Core.Engine.Discover: Mod.CveMatch.Correlacionar(Fingerprint, Portas)
#
# Nao faz rede. Nao executa nada. So cruza dados locais com tabela.
# Retorna lista de CVEs sugeridas, com exploit_id quando ha exploit no ByP4ss.

from Core.Log import Log


class CveMatch:

    CVES = [
        {
            "id": "CVE-2023-1389",
            "fabricante": "tplink",
            "portas": [80, 443, 8080],
            "severidade": "critica",
            "cvss": 9.8,
            "descricao": "Command injection em /cgi-bin/luci (TP-Link Archer AX21)",
            "exploit_id": "tplink",
            "tipo": "command_injection",
        },
        {
            "id": "CVE-2024-3273",
            "fabricante": "dlink",
            "portas": [80, 443, 8080],
            "severidade": "critica",
            "cvss": 9.8,
            "descricao": "Auth bypass (messagebus) + command injection em nas_sharing.cgi (D-Link)",
            "exploit_id": "dlink",
            "tipo": "auth_bypass_injection",
        },
        {
            "id": "CVE-2025-7795",
            "fabricante": "tenda",
            "portas": [80, 8080],
            "severidade": "alta",
            "cvss": 7.5,
            "descricao": "Buffer overflow em /goform/fromP2pListFilter (Tenda, DoS)",
            "exploit_id": "tenda7795",
            "tipo": "buffer_overflow_dos",
        },
        {
            "id": "CVE-2025-29384",
            "fabricante": "tenda",
            "portas": [80, 8080],
            "severidade": "critica",
            "cvss": 9.8,
            "descricao": "Stack overflow MIPS em /goform/AdvSetMacMtuWan (Tenda)",
            "exploit_id": "tenda29384",
            "tipo": "stack_overflow_mips",
        },
        {
            "id": "CVE-2021-20090",
            "fabricante": "arcadyan",
            "portas": [80, 443, 8080],
            "severidade": "critica",
            "cvss": 9.8,
            "descricao": "Path traversal + command injection em apply_abstract.cgi (Arcadyan)",
            "exploit_id": "arcadyan",
            "tipo": "traversal_injection",
        },
        {
            "id": "CVE-2025-55423",
            "fabricante": "iptime",
            "portas": [1900, 80, 8080],
            "severidade": "alta",
            "cvss": 8.1,
            "descricao": "SSDP control URL malicioso (ipTIME)",
            "exploit_id": "iptime",
            "tipo": "ssdp_control_url",
        },
        {
            "id": "CVE-2016-6255",
            "fabricante": None,
            "portas": [1900],
            "severidade": "media",
            "cvss": 6.5,
            "descricao": "UPnP control URL permite download de arquivo arbitrario",
            "exploit_id": None,
            "tipo": "upnp_generic",
        },
        {
            "id": "CVE-2020-13848",
            "fabricante": None,
            "portas": [52869],
            "severidade": "media",
            "cvss": 5.9,
            "descricao": "UPnP SUBSCRIBE sem autenticacao causa DoS (libupnp)",
            "exploit_id": None,
            "tipo": "upnp_dos",
        },
        {
            "id": "CVE-2020-13849",
            "fabricante": None,
            "portas": [52869],
            "severidade": "media",
            "cvss": 5.9,
            "descricao": "UPnP GET com path longo causa crash (libupnp)",
            "exploit_id": None,
            "tipo": "upnp_crash",
        },
    ]

    SEVERIDADES = ["info", "baixa", "media", "alta", "critica"]
    PESOS = {"info": 1, "baixa": 2, "media": 4, "alta": 7, "critica": 10}

    @staticmethod
    def Correlacionar(Fingerprint, Portas):
        if not isinstance(Fingerprint, dict):
            Fingerprint = {}
        PortasNormalizadas = CveMatch._NormalizarPortas(Portas)
        PortasAbertas = {P["porta"] for P in PortasNormalizadas if P.get("estado") == "aberta" or "porta" in P}
        if not PortasAbertas:
            PortasAbertas = {P["porta"] for P in PortasNormalizadas}
        FabDetectado = (Fingerprint.get("fabricante") or "").lower()
        FabChave = CveMatch._NormalizarFabricante(FabDetectado)
        Servidores = CveMatch._ExtrairServidores(Fingerprint)
        CVEs = []
        Vistos = set()
        for Cve in CveMatch.CVES:
            Bate = False
            Motivo = None
            if Cve["fabricante"]:
                if FabChave == Cve["fabricante"]:
                    if any(P in PortasAbertas for P in Cve["portas"]):
                        Bate = True
                        Motivo = f"fabricante={Cve['fabricante']} porta={Cve['portas']}"
            else:
                if any(P in PortasAbertas for P in Cve["portas"]):
                    Bate = True
                    Motivo = f"porta={Cve['portas']} (generica)"
            if not Bate and Servidores:
                for Servidor in Servidores:
                    if Cve["fabricante"] and Cve["fabricante"] in Servidor.lower():
                        if any(P in PortasAbertas for P in Cve["portas"]):
                            Bate = True
                            Motivo = f"servidor={Servidor}"
                            break
            if Bate and Cve["id"] not in Vistos:
                Vistos.add(Cve["id"])
                CVEs.append({
                    "id": Cve["id"],
                    "fabricante": Cve["fabricante"],
                    "severidade": Cve["severidade"],
                    "cvss": Cve["cvss"],
                    "peso": CveMatch.PESOS.get(Cve["severidade"], 1),
                    "descricao": Cve["descricao"],
                    "exploit_id": Cve["exploit_id"],
                    "exploit_disponivel": Cve["exploit_id"] is not None,
                    "tipo": Cve["tipo"],
                    "motivo": Motivo,
                    "portas_sugeridas": [P for P in Cve["portas"] if P in PortasAbertas],
                })
        CVEs.sort(key=lambda C: (-CveMatch.PESOS.get(C["severidade"], 1), C["id"]))
        Log.Descoberta("CveMatch", Fingerprint.get("alvo", "?"), "cves", {
            "total": len(CVEs),
            "com_exploit": sum(1 for C in CVEs if C["exploit_disponivel"]),
        })
        return {"ok": True, "cves": CVEs, "total": len(CVEs),
                "fabricante_detectado": FabDetectado or None,
                "portas_abertas": sorted(PortasAbertas)}

    @staticmethod
    def _NormalizarPortas(Portas):
        if not Portas:
            return []
        Out = []
        for Item in Portas:
            if isinstance(Item, dict):
                P = Item.get("porta")
                if P is not None:
                    Out.append({"porta": int(P), "estado": Item.get("estado", "aberta")})
            elif isinstance(Item, int):
                Out.append({"porta": Item, "estado": "aberta"})
        return Out

    @staticmethod
    def _NormalizarFabricante(Fabricante):
        if not Fabricante:
            return None
        Mapa = {
            "tp-link": "tplink", "tplink": "tplink",
            "d-link": "dlink", "dlink": "dlink",
            "tenda": "tenda",
            "arcadyan": "arcadyan",
            "iptime": "iptime",
            "zte": "zte", "huawei": "huawei",
            "mikrotik": "mikrotik", "cisco": "cisco",
            "netgear": "netgear", "asus": "asus",
            "linksys": "linksys", "ubiquiti": "ubiquiti",
            "fortinet": "fortinet", "openwrt": "openwrt",
        }
        F = Fabricante.lower().strip()
        return Mapa.get(F, F)

    @staticmethod
    def _ExtrairServidores(Fingerprint):
        Servidores = []
        for P in Fingerprint.get("portas") or []:
            if isinstance(P, dict):
                S = P.get("servidor")
                if S:
                    Servidores.append(str(S).lower())
                M = P.get("modelo")
                if M:
                    Servidores.append(str(M).lower())
        return Servidores

    @staticmethod
    def PorFabricante(Fabricante, Portas):
        FabChave = CveMatch._NormalizarFabricante(Fabricante)
        PortasSet = {CveMatch._ExtrairPorta(P) for P in (Portas or [])}
        Out = []
        for Cve in CveMatch.CVES:
            if Cve["fabricante"] == FabChave:
                if any(P in PortasSet for P in Cve["portas"]):
                    Out.append(dict(Cve))
        return Out

    @staticmethod
    def _ExtrairPorta(Item):
        if isinstance(Item, dict):
            return Item.get("porta")
        if isinstance(Item, int):
            return Item
        return None

    @staticmethod
    def Todas():
        return [dict(C) for C in CveMatch.CVES]

    @staticmethod
    def PorSeveridade(Severidade):
        return [dict(C) for C in CveMatch.CVES if C["severidade"] == Severidade]

    @staticmethod
    def Info():
        return {
            "nome": "CveMatch",
            "total_cves": len(CveMatch.CVES),
            "por_severidade": {
                S: sum(1 for C in CveMatch.CVES if C["severidade"] == S)
                for S in CveMatch.SEVERIDADES
            },
            "com_exploit": sum(1 for C in CveMatch.CVES if C["exploit_id"]),
        }


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 2 and sys.argv[1] == "teste":
        Alvo = sys.argv[2]
        Fab = sys.argv[3] if len(sys.argv) > 3 else None
        Portas = [int(X) for X in sys.argv[4].split(",")] if len(sys.argv) > 4 else [80, 1900]
        Fake = {"alvo": Alvo, "fabricante": Fab, "portas": [{"porta": P} for P in Portas]}
        print(f"correlacionando {Alvo} (fabricante={Fab}) portas={Portas}")
        R = CveMatch.Correlacionar(Fake, Portas)
        print(json.dumps(R, indent=2, ensure_ascii=False, default=str))
