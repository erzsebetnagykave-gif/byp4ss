# Findings do ByP4ss
# Transforma o dict bruto de Engine._Resultados em lista de achados
# com severidade. Chamado por Core.Engine.Report: Mod.Findings.Coletar(Resultados)
#
# Nao faz I/O, nao faz rede. So parsing + classificacao.
# O Export (bloco 2B) e quem escreve em disco.

from datetime import datetime, timezone

from Core.Log import Log


class Findings:

    _Cache = []

    SEVERIDADES = ["info", "baixa", "media", "alta", "critica"]
    PESOS = {"info": 1, "baixa": 2, "media": 4, "alta": 7, "critica": 10}

    @staticmethod
    def Timestamp():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def Coletar(Resultados):
        if not isinstance(Resultados, dict):
            return {"ok": False, "motivo": "resultados_invalidos",
                    "achados": [], "total": 0}
        Achados = []
        for Fase, Lista in Resultados.items():
            if not isinstance(Lista, list):
                continue
            for Item in Lista:
                if not isinstance(Item, dict):
                    continue
                Achados.extend(Findings._Extrair(Fase, Item))
        Findings._Cache = Achados
        Resumo = Findings.Resumo()
        Log.Info("findings coletados", {
            "total": len(Achados),
            "por_tipo": Resumo["por_tipo"],
            "por_severidade": Resumo["por_severidade"],
        })
        return {"ok": True, "achados": Achados, "total": len(Achados),
                "resumo": Resumo, "timestamp": Findings.Timestamp()}

    @staticmethod
    def _Extrair(Fase, Item):
        Achados = []
        Alvo = Item.get("alvo") or Item.get("host") or "?"
        if Fase == "discover":
            Achados.extend(Findings._ExtrairDiscover(Alvo, Item))
        elif Fase == "bypass":
            Achados.extend(Findings._ExtrairBypass(Alvo, Item))
        elif Fase == "fuzz":
            Achados.extend(Findings._ExtrairFuzz(Alvo, Item))
        elif Fase == "verify":
            Achados.extend(Findings._ExtrairVerify(Alvo, Item))
        return Achados

    @staticmethod
    def _ExtrairDiscover(Alvo, Item):
        Achados = []
        for Porta in Item.get("portas") or []:
            if not isinstance(Porta, dict):
                continue
            if Porta.get("estado") != "aberta":
                continue
            Servico = Porta.get("servico") or "desconhecido"
            Banner = Porta.get("banner") or ""
            Descricao = f"porta {Porta.get('porta')} aberta ({Servico})"
            if Banner:
                Descricao += f" banner={Banner[:60]}"
            Achados.append(Findings._Novo(
                "porta_aberta", Alvo, "info", Descricao,
                {"porta": Porta.get("porta"), "servico": Servico,
                 "banner": Banner[:200] if Banner else ""},
            ))
        Ssdp = Item.get("ssdp")
        if isinstance(Ssdp, dict) and Ssdp.get("ok"):
            Achados.append(Findings._Novo(
                "ssdp_descoberto", Alvo, "info",
                f"UPnP detectado em {Ssdp.get('local') or Ssdp.get('control_url') or '?'}",
                {"local": Ssdp.get("local"), "servidor": Ssdp.get("servidor"),
                 "st": Ssdp.get("st"), "control_url": Ssdp.get("control_url")},
            ))
        Fp = Item.get("fingerprint")
        if isinstance(Fp, dict) and Fp.get("ok"):
            Achados.append(Findings._Novo(
                "fingerprint", Alvo, "info",
                f"fabricante={Fp.get('fabricante', '?')} modelo={Fp.get('modelo', '?')}",
                Fp,
            ))
        for Cve in Item.get("cves") or []:
            if not isinstance(Cve, dict):
                continue
            Sev = Cve.get("severidade", "media")
            if Sev not in Findings.SEVERIDADES:
                Sev = "media"
            Achados.append(Findings._Novo(
                "cve_sugerida", Alvo, Sev,
                f"{Cve.get('id', '?')}: {Cve.get('descricao', Cve.get('motivo', ''))[:80]}",
                Cve,
            ))
        return Achados

    @staticmethod
    def _ExtrairBypass(Alvo, Item):
        Achados = []
        for Mod in ("upnp", "httpauth", "telnet", "dnsrebind"):
            R = Item.get(Mod)
            if not isinstance(R, dict):
                continue
            if Findings._ModuloFaltando(R):
                continue
            if R.get("ok"):
                Extra = {}
                if Mod == "upnp":
                    Extra = {"porta": R.get("porta_externa"),
                             "protocolo": R.get("protocolo")}
                elif Mod == "httpauth":
                    Extra = {"achados": len(R.get("achados") or [])}
                elif Mod == "telnet":
                    Extra = {"user": R.get("user"), "porta": R.get("porta")}
                elif Mod == "dnsrebind":
                    Extra = {"dominio": R.get("dominio")}
                Achados.append(Findings._Novo(
                    f"bypass_{Mod}", Alvo, "alta",
                    f"bypass {Mod} bem-sucedido", Extra,
                ))
            else:
                Motivo = R.get("motivo") or R.get("erro") or "?"
                Achados.append(Findings._Novo(
                    f"bypass_{Mod}_falhou", Alvo, "info",
                    f"bypass {Mod} falhou: {str(Motivo)[:80]}",
                    {"motivo": Motivo},
                ))
        return Achados

    @staticmethod
    def _ModuloFaltando(R):
        if not isinstance(R, dict):
            return False
        Motivo = str(R.get("motivo") or R.get("erro") or "").lower()
        if not Motivo:
            return False
        return (Motivo == "modulo_nao_implementado"
                or Motivo.startswith("modulo_indisponivel")
                or Motivo.startswith("modulo_faltando"))

    @staticmethod
    def _ExtrairFuzz(Alvo, Item):
        Achados = []
        Crashes = Item.get("crashes") or []
        for Crash in Crashes:
            if not isinstance(Crash, dict):
                continue
            Input = Crash.get("input") or Crash.get("payload") or "?"
            Achados.append(Findings._Novo(
                "crash", Alvo, "critica",
                f"crash com input {str(Input)[:40]}",
                Crash,
            ))
        Anomalias = Item.get("anomalias") or []
        for A in Anomalias:
            if not isinstance(A, dict):
                continue
            Achados.append(Findings._Novo(
                "anomalia_fuzz", Alvo, "media",
                f"anomalia em {A.get('tipo', '?')}",
                A,
            ))
        return Achados

    @staticmethod
    def _ExtrairVerify(Alvo, Item):
        Achados = []
        for Porta in Item.get("portas_ok") or []:
            Achados.append(Findings._Novo(
                "porta_verificada", Alvo, "info",
                f"porta {Porta} confirmada aberta", {"porta": Porta},
            ))
        for Porta in Item.get("servicos_ok") or []:
            Achados.append(Findings._Novo(
                "servico_verificado", Alvo, "baixa",
                f"servico em {Porta} respondendo", {"porta": Porta},
            ))
        for Porta in Item.get("exploits_ok") or []:
            Achados.append(Findings._Novo(
                "exploit_verificado", Alvo, "critica",
                f"exploit em {Porta} confirmado (shell provavel)",
                {"porta": Porta},
            ))
        return Achados

    @staticmethod
    def _Novo(Tipo, Alvo, Severidade, Descricao, Dados):
        if Severidade not in Findings.SEVERIDADES:
            Severidade = "info"
        return {
            "tipo": Tipo,
            "alvo": Alvo,
            "severidade": Severidade,
            "peso": Findings.PESOS[Severidade],
            "descricao": Descricao,
            "dados": Dados or {},
            "timestamp": Findings.Timestamp(),
        }

    @staticmethod
    def Resumo():
        Achados = Findings._Cache
        PorSev = {S: 0 for S in Findings.SEVERIDADES}
        PorTipo = {}
        PesoTotal = 0
        for A in Achados:
            S = A.get("severidade", "info")
            if S in PorSev:
                PorSev[S] += 1
            T = A.get("tipo", "?")
            PorTipo[T] = PorTipo.get(T, 0) + 1
            PesoTotal += A.get("peso", 1)
        return {
            "total": len(Achados),
            "por_severidade": PorSev,
            "por_tipo": PorTipo,
            "peso_total": PesoTotal,
            "max_severidade": Findings._MaxSeveridade(PorSev),
        }

    @staticmethod
    def _MaxSeveridade(PorSev):
        for S in reversed(Findings.SEVERIDADES):
            if PorSev.get(S, 0) > 0:
                return S
        return None

    @staticmethod
    def Cache():
        return list(Findings._Cache)

    @staticmethod
    def Filtrar(Severidade=None, Tipo=None, Alvo=None):
        R = list(Findings._Cache)
        if Severidade:
            R = [A for A in R if A.get("severidade") == Severidade]
        if Tipo:
            R = [A for A in R if A.get("tipo") == Tipo]
        if Alvo:
            R = [A for A in R if A.get("alvo") == Alvo]
        return R

    @staticmethod
    def Info():
        return {
            "nome": "Findings",
            "severidades": Findings.SEVERIDADES,
            "pesos": Findings.PESOS,
        }


if __name__ == "__main__":
    import json
    Fake = {
        "discover": [{
            "alvo": "192.168.0.1",
            "portas": [
                {"porta": 80, "estado": "aberta", "servico": "http", "banner": "TP-Link"},
                {"porta": 22, "estado": "fechada", "servico": "ssh"},
            ],
            "ssdp": {"ok": True, "local": "http://192.168.0.1:1900/"},
            "fingerprint": {"ok": True, "fabricante": "TP-Link", "modelo": "Archer AX21"},
            "cves": [{"id": "CVE-2023-1389", "severidade": "critica",
                      "descricao": "Command injection"}],
        }],
        "bypass": [{"alvo": "192.168.0.1",
                    "upnp": {"ok": True, "porta_externa": 23, "protocolo": "TCP"},
                    "httpauth": {"ok": False, "motivo": "nenhum_bypass"}}],
        "verify": [{"alvo": "192.168.0.1", "portas_ok": [80],
                    "servicos_ok": [80], "exploits_ok": [4444]}],
    }
    R = Findings.Coletar(Fake)
    assert R["ok"], R
    assert R["total"] >= 6, R["total"]
    print(f"[ok] {R['total']} achados")
    print(json.dumps(R["resumo"], indent=2, ensure_ascii=False))
    print()
    print(f"[ok] cache: {len(Findings.Cache())}")
    print(f"[ok] criticos: {len(Findings.Filtrar(Severidade='critica'))}")
    print(f"[ok] porta_aberta: {len(Findings.Filtrar(Tipo='porta_aberta'))}")
