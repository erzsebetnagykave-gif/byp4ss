#!/usr/bin/env python3
# Recompensa — sistema de recompensa pra RedeNeural.
# Externa (por achado) + Intrinseca (curiosidade) - Penalidade (custo).
# Python puro. Zero dependencia.

import os
import sys
import json
import math


class Tabela:
    """Recompensas fixas por tipo de achado."""

    RECOMPENSAS = {
        "porta_aberta": 1.0,
        "porta_verificada": 1.0,
        "servico_verificado": 2.0,
        "ssdp_descoberto": 2.0,
        "fingerprint": 3.0,
        "cve_sugerida": 5.0,
        "anomalia_fuzz": 10.0,
        "bypass_upnp": 15.0,
        "bypass_httpauth": 15.0,
        "bypass_telnet": 15.0,
        "bypass_dnsrebind": 15.0,
        "crash": 30.0,
        "exploit_verificado": 100.0,
        "bypass_upnp_falhou": -1.0,
        "bypass_httpauth_falhou": -1.0,
        "bypass_telnet_falhou": -1.0,
        "bypass_dnsrebind_falhou": -1.0,
        "erro": -5.0,
        "timeout": -2.0,
    }

    CUSTOS_ACAO = {
        "scan": 0.1,
        "analise": 0.2,
        "ssdp": 0.05,
        "cred": 0.5,
        "sqli": 0.5,
        "exploit": 1.0,
        "bypass": 1.0,
        "shell": 5.0,
        "chain": 2.0,
        "fuzz": 0.3,
        "verify": 0.1,
    }

    @staticmethod
    def Recompensa(Tipo):
        return float(Tabela.RECOMPENSAS.get(Tipo, 0.0))

    @staticmethod
    def CustoAcao(Acao):
        Base = Acao.split()[0].split("_")[0] if Acao else ""
        return float(Tabela.CUSTOS_ACAO.get(Base, 0.2))


class Recompensa:
    """Sistema de recompensa: externa + intrinseca - penalidade."""

    PESO_CURIOSIDADE = 0.3
    CUSTO_PASSO = 0.01

    Visitas = {}
    QVariancia = {}
    Passos = 0
    TotalAcumulado = 0.0
    Historico = []

    @staticmethod
    def Reset():
        Recompensa.Visitas = {}
        Recompensa.QVariancia = {}
        Recompensa.Passos = 0
        Recompensa.TotalAcumulado = 0.0
        Recompensa.Historico = []
        return {"ok": True}

    @staticmethod
    def _Hash(Estado):
        if isinstance(Estado, (list, tuple)):
            return "|".join(f"{float(x):.2f}" for x in Estado)
        return str(Estado)

    @staticmethod
    def Externa(Achado):
        """Achado: dict com 'tipo', ou string com o tipo."""
        if isinstance(Achado, dict):
            Tipo = Achado.get("tipo") or Achado.get("Tipo") or ""
        else:
            Tipo = str(Achado)
        return Tabela.Recompensa(Tipo)

    @staticmethod
    def Intrinseca(Estado, Acao):
        """Curiosidade: novidade do estado + incerteza da acao."""
        H = Recompensa._Hash(Estado)
        # Novidade: 1 na primeira visita, cai com repeticoes
        Visitas = Recompensa.Visitas.get(H, 0)
        Novidade = 1.0 / (1.0 + Visitas)
        Recompensa.Visitas[H] = Visitas + 1
        # Incerteza: variancia do Q-value da acao nesse estado
        Chave = (H, Acao)
        Hist = Recompensa.QVariancia.get(Chave, [])
        if len(Hist) < 2:
            Incerteza = 0.5
        else:
            Media = sum(Hist) / len(Hist)
            Var = sum((x - Media) ** 2 for x in Hist) / len(Hist)
            Incerteza = min(1.0, math.sqrt(Var))
        return 0.5 * Novidade + 0.5 * Incerteza

    @staticmethod
    def RegistrarQ(Estado, Acao, Q):
        H = Recompensa._Hash(Estado)
        Chave = (H, Acao)
        Hist = Recompensa.QVariancia.get(Chave, [])
        Hist.append(float(Q))
        if len(Hist) > 10:
            Hist = Hist[-10:]
        Recompensa.QVariancia[Chave] = Hist

    @staticmethod
    def Penalidade(Acao, Passos=None):
        """Custo de acao + custo de passo."""
        if Passos is None:
            Passos = Recompensa.Passos
        CustoAcao = Tabela.CustoAcao(Acao)
        CustoPasso = Recompensa.CUSTO_PASSO * Passos
        return CustoAcao + CustoPasso

    @staticmethod
    def Total(Achado, Estado, Acao, Passos=None):
        """Recompensa total: externa + intrinseca*peso - penalidade."""
        Ext = Recompensa.Externa(Achado)
        Intr = Recompensa.Intrinseca(Estado, Acao)
        Pen = Recompensa.Penalidade(Acao, Passos)
        Total = Ext + Intr * Recompensa.PESO_CURIOSIDADE - Pen
        Recompensa.Passos += 1
        Recompensa.TotalAcumulado += Total
        Recompensa.Historico.append({
            "Achado": Achado if isinstance(Achado, str) else Achado.get("tipo", "?"),
            "Externa": round(Ext, 3),
            "Intrinseca": round(Intr, 3),
            "Penalidade": round(Pen, 3),
            "Total": round(Total, 3),
            "Acumulado": round(Recompensa.TotalAcumulado, 3),
        })
        if len(Recompensa.Historico) > 1000:
            Recompensa.Historico = Recompensa.Historico[-1000:]
        return Total

    @staticmethod
    def Info():
        return {
            "TotalAcumulado": round(Recompensa.TotalAcumulado, 3),
            "Passos": Recompensa.Passos,
            "EstadosVisitados": len(Recompensa.Visitas),
            "ParesQA": len(Recompensa.QVariancia),
            "PesoCuriosidade": Recompensa.PESO_CURIOSIDADE,
            "CustoPasso": Recompensa.CUSTO_PASSO,
        }

    @staticmethod
    def Ultimos(N=10):
        return Recompensa.Historico[-N:]


def RodarTeste():
    print("=== TESTE Recompensa ===")
    print()

    print("[1] Tabela.Recompensa por tipo")
    assert Tabela.Recompensa("porta_aberta") == 1.0
    assert Tabela.Recompensa("exploit_verificado") == 100.0
    assert Tabela.Recompensa("bypass_upnp_falhou") == -1.0
    assert Tabela.Recompensa("desconhecido") == 0.0
    print(f"  porta_aberta={Tabela.Recompensa('porta_aberta')}, "
          f"exploit={Tabela.Recompensa('exploit_verificado')}")

    print("[2] Tabela.CustoAcao")
    assert Tabela.CustoAcao("scan") == 0.1
    assert Tabela.CustoAcao("exploit tplink") == 1.0
    assert Tabela.CustoAcao("shell reverse") == 5.0
    print(f"  scan={Tabela.CustoAcao('scan')}, "
          f"exploit={Tabela.CustoAcao('exploit tplink')}, "
          f"shell={Tabela.CustoAcao('shell reverse')}")

    print("[3] Externa")
    Recompensa.Reset()
    assert Recompensa.Externa({"tipo": "porta_aberta"}) == 1.0
    assert Recompensa.Externa({"tipo": "crash"}) == 30.0
    assert Recompensa.Externa("bypass_upnp") == 15.0
    print(f"  porta_aberta=+1, crash=+30, bypass_upnp=+15")

    print("[4] Intrinseca — novidade cai com visita")
    Recompensa.Reset()
    Est = [0.1] * 8
    I1 = Recompensa.Intrinseca(Est, "scan")
    I2 = Recompensa.Intrinseca(Est, "scan")
    I3 = Recompensa.Intrinseca(Est, "scan")
    assert I1 > I2 > I3, (I1, I2, I3)
    print(f"  1a={I1:.3f}, 2a={I2:.3f}, 3a={I3:.3f} (cai)")

    print("[5] Penalidade cresce com acao e passos")
    Recompensa.Reset()
    P1 = Recompensa.Penalidade("scan", 1)
    P2 = Recompensa.Penalidade("exploit", 1)
    P3 = Recompensa.Penalidade("scan", 10)
    assert P1 < P2, (P1, P2)
    assert P1 < P3, (P1, P3)
    print(f"  scan(1)={P1:.3f}, exploit(1)={P2:.3f}, scan(10)={P3:.3f}")

    print("[6] Total — externa + intrinseca - penalidade")
    Recompensa.Reset()
    Est = [0.5] * 8
    T1 = Recompensa.Total({"tipo": "porta_aberta"}, Est, "scan")
    T2 = Recompensa.Total({"tipo": "bypass_upnp_falhou"}, Est, "bypass")
    assert T1 > 0.5, T1
    assert T2 < 0.0, T2
    print(f"  porta_aberta={T1:.3f}, bypass_falhou={T2:.3f}")

    print("[7] RegistrarQ (variancia)")
    Recompensa.Reset()
    Recompensa.RegistrarQ(Est, "scan", 1.0)
    Recompensa.RegistrarQ(Est, "scan", 2.0)
    Recompensa.RegistrarQ(Est, "scan", 3.0)
    I = Recompensa.Intrinseca(Est, "scan")
    assert I > 0.0, I
    print(f"  intrinseca pos-variacao={I:.3f}")

    print("[8] Info + Historico")
    Recompensa.Reset()
    for Tipo in ("porta_aberta", "fingerprint", "cve_sugerida"):
        Recompensa.Total({"tipo": Tipo}, Est, "scan")
    I = Recompensa.Info()
    assert I["Passos"] == 3, I["Passos"]
    assert I["TotalAcumulado"] > 0, I["TotalAcumulado"]
    H = Recompensa.Ultimos(3)
    assert len(H) == 3
    print(f"  Info={I}")
    print(f"  Ultimos tipos={[h['Achado'] for h in H]}")

    print()
    print("TESTE OK Recompensa")
    return 0


def Main():
    import argparse
    P = argparse.ArgumentParser(prog="Recompensa")
    P.add_argument("--teste", action="store_true")
    P.add_argument("--info", action="store_true")
    P.add_argument("--tabela", action="store_true")
    Args = P.parse_args()
    if Args.teste:
        return RodarTeste()
    if Args.info:
        print(json.dumps(Recompensa.Info(), indent=2, ensure_ascii=False))
        return 0
    if Args.tabela:
        print("=== RECOMPENSAS ===")
        for Tipo, Valor in sorted(Tabela.RECOMPENSAS.items()):
            print(f"  {Tipo:30s} {Valor:+.1f}")
        print()
        print("=== CUSTOS DE ACAO ===")
        for Acao, Valor in sorted(Tabela.CUSTOS_ACAO.items()):
            print(f"  {Acao:20s} {Valor:.2f}")
        return 0
    P.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(Main())
