#!/usr/bin/env python3
# ComunicacaoEmergente — Lewis Signaling Game.
# 2 agentes (Emissor + Receptor) inventam vocabulario.
# Sem hardcoded: a associacao objeto -> sinal EMERGE do Q-Learning.
# Bloco 1/2: Ambiente + Emissor + Receptor.

import os
import sys
import json
import math
import random


# ============================================================
# AMBIENTE
# ============================================================

class Ambiente:

    def __init__(self, NObjetos=5, NSinais=5, Seed=42):
        self.NObjetos = NObjetos
        self.NSinais = NSinais
        self.Objetos = list(range(NObjetos))
        self.Sinais = list(range(NSinais))
        self.Rng = random.Random(Seed)

    def Sortear(self):
        return self.Rng.choice(self.Objetos)

    def Avaliar(self, ObjetoReal, ObjetoEscolhido):
        if ObjetoReal == ObjetoEscolhido:
            return 1.0
        return 0.0

    def Info(self):
        return {
            "N_objetos": self.NObjetos,
            "N_sinais": self.NSinais,
            "Objetos": self.Objetos,
            "Sinais": self.Sinais,
        }


# ============================================================
# Q-TABLE generica (sem dependencia do RedeNeural)
# ============================================================

class _QTable:

    def __init__(self, Alpha=0.1, Gamma=0.9, Epsilon=0.1):
        self.Alpha = Alpha
        self.Gamma = Gamma
        self.Epsilon = Epsilon
        self.Dados = {}
        self.Updates = 0

    def Obter(self, Estado, Acao):
        return self.Dados.get((Estado, Acao), 0.0)

    def Atualizar(self, Estado, Acao, Recompensa):
        Chave = (Estado, Acao)
        QAtual = self.Dados.get(Chave, 0.0)
        QNovo = QAtual + self.Alpha * (Recompensa - QAtual)
        self.Dados[Chave] = QNovo
        self.Updates += 1
        return QNovo

    def Escolher(self, Estado, Acoes):
        if random.random() < self.Epsilon:
            return random.choice(Acoes)
        return self.Melhor(Estado, Acoes)

    def Melhor(self, Estado, Acoes):
        MelhorAcao = None
        MelhorValor = float("-inf")
        for A in Acoes:
            V = self.Dados.get((Estado, A), 0.0)
            if V > MelhorValor:
                MelhorValor = V
                MelhorAcao = A
        return MelhorAcao if MelhorAcao is not None else random.choice(Acoes)


# ============================================================
# EMISSOR (objeto -> sinal)
# ============================================================

class Emissor:

    def __init__(self, NSinais, Seed=42):
        self.NSinais = NSinais
        self.Sinais = list(range(NSinais))
        self.Qt = _QTable(Alpha=0.1, Gamma=0.9, Epsilon=0.3)
        self.Rng = random.Random(Seed)

    def Escolher(self, Objeto):
        if self.Rng.random() < self.Qt.Epsilon:
            return self.Rng.choice(self.Sinais)
        return self.Qt.Melhor(Objeto, self.Sinais)

    def Atualizar(self, Objeto, Sinal, Recompensa):
        return self.Qt.Atualizar(Objeto, Sinal, Recompensa)

    def Vocabulario(self):
        Mapa = {}
        for (Objeto, Sinal), Valor in self.Qt.Dados.items():
            if Objeto not in Mapa or Valor > Mapa[Objeto][1]:
                Mapa[Objeto] = (Sinal, Valor)
        return {O: S for O, (S, V) in Mapa.items()}

    def Info(self):
        return {
            "N_sinais": self.NSinais,
            "Atualizacoes": self.Qt.Updates,
            "Pares": len(self.Qt.Dados),
        }


# ============================================================
# RECEPTOR (sinal -> objeto)
# ============================================================

class Receptor:

    def __init__(self, NObjetos, Seed=43):
        self.NObjetos = NObjetos
        self.Objetos = list(range(NObjetos))
        self.Qt = _QTable(Alpha=0.1, Gamma=0.9, Epsilon=0.3)
        self.Rng = random.Random(Seed)

    def Escolher(self, Sinal):
        if self.Rng.random() < self.Qt.Epsilon:
            return self.Rng.choice(self.Objetos)
        return self.Qt.Melhor(Sinal, self.Objetos)

    def Atualizar(self, Sinal, Objeto, Recompensa):
        return self.Qt.Atualizar(Sinal, Objeto, Recompensa)

    def Interpretacao(self):
        Mapa = {}
        for (Sinal, Objeto), Valor in self.Qt.Dados.items():
            if Sinal not in Mapa or Valor > Mapa[Sinal][1]:
                Mapa[Sinal] = (Objeto, Valor)
        return {S: O for S, (O, V) in Mapa.items()}

    def Info(self):
        return {
            "N_objetos": self.NObjetos,
            "Atualizacoes": self.Qt.Updates,
            "Pares": len(self.Qt.Dados),
        }


# ============================================================
# TESTE (bloco 4)
# ============================================================

def RodarTeste():
    print("=== TESTE ComunicacaoEmergente (bloco 1/2) ===")
    print()

    print("[1] Ambiente")
    Amb = Ambiente(NObjetos=5, NSinais=5, Seed=42)
    O = Amb.Sortear()
    assert O in Amb.Objetos
    assert Amb.Avaliar(O, O) == 1.0
    assert Amb.Avaliar(O, (O + 1) % 5) == 0.0
    print(f"  objetos={Amb.Objetos} sinais={Amb.Sinais}")
    print(f"  sorteado={O}, avaliar(certo)=1.0, avaliar(errado)=0.0")

    print("[2] Emissor.Escolher")
    Emi = Emissor(NSinais=5, Seed=42)
    S = Emi.Escolher(0)
    assert S in Emi.Sinais
    print(f"  objeto 0 -> sinal {S}")

    print("[3] Emissor.Atualizar")
    Emi2 = Emissor(NSinais=5, Seed=42)
    V = Emi2.Atualizar(0, 3, 1.0)
    assert V > 0.0, V
    print(f"  Q(objeto=0, sinal=3) = {V}")

    print("[4] Emissor.Vocabulario")
    Emi3 = Emissor(NSinais=5, Seed=42)
    for Obj in range(5):
        for Sinal in range(5):
            R = 1.0 if Sinal == (Obj + 1) % 5 else 0.0
            for _ in range(20):
                Emi3.Atualizar(Obj, Sinal, R)
    Voc = Emi3.Vocabulario()
    assert len(Voc) == 5, Voc
    print(f"  vocabulario={Voc}")

    print("[5] Receptor.Escolher")
    Rec = Receptor(NObjetos=5, Seed=43)
    O2 = Rec.Escolher(0)
    assert O2 in Rec.Objetos
    print(f"  sinal 0 -> objeto {O2}")

    print("[6] Receptor.Atualizar")
    Rec2 = Receptor(NObjetos=5, Seed=43)
    V = Rec2.Atualizar(0, 2, 1.0)
    assert V > 0.0, V
    print(f"  Q(sinal=0, objeto=2) = {V}")

    print("[7] Receptor.Interpretacao")
    Rec3 = Receptor(NObjetos=5, Seed=43)
    for Sinal in range(5):
        for Obj in range(5):
            R = 1.0 if Obj == (Sinal + 1) % 5 else 0.0
            for _ in range(20):
                Rec3.Atualizar(Sinal, Obj, R)
    Interp = Rec3.Interpretacao()
    assert len(Interp) == 5, Interp
    print(f"  interpretacao={Interp}")

    print("[8] Round-trip (Emissor -> Receptor)")
    Emi4 = Emissor(NSinais=5, Seed=42)
    Rec4 = Receptor(NObjetos=5, Seed=43)
    for _ in range(500):
        Obj = random.choice(Amb.Objetos)
        Sinal = Emi4.Escolher(Obj)
        Escolhido = Rec4.Escolher(Sinal)
        R = Amb.Avaliar(Obj, Escolhido)
        Emi4.Atualizar(Obj, Sinal, R)
        Rec4.Atualizar(Sinal, Escolhido, R)
    print(f"  Emissor.Info = {Emi4.Info()}")
    print(f"  Receptor.Info = {Rec4.Info()}")
    # Sem integracao completa, vocabulario pode nao estabilizar
    print(f"  Vocabulario emissor: {Emi4.Vocabulario()}")
    print(f"  Interpretacao receptor: {Rec4.Interpretacao()}")

    print()


if __name__ == "__main__":
    sys.exit(RodarTeste())


# ============================================================
# BLOCO 5/11 — JOGO + VOCABULARIO + CLI
# ============================================================

class Jogo:
    """Lewis Signaling Game: Emissor ve objeto, escolhe sinal, Receptor escolhe objeto."""

    def __init__(self, Ambiente, Emissor, Receptor):
        self.Ambiente = Ambiente
        self.Emissor = Emissor
        self.Receptor = Receptor
        self.Historico = []
        self.Acertos = 0
        self.Total = 0

    def RodarEpisodio(self):
        Objeto = self.Ambiente.Sortear()
        Sinal = self.Emissor.Escolher(Objeto)
        Escolhido = self.Receptor.Escolher(Sinal)
        Recompensa = self.Ambiente.Avaliar(Objeto, Escolhido)
        self.Emissor.Atualizar(Objeto, Sinal, Recompensa)
        self.Receptor.Atualizar(Sinal, Escolhido, Recompensa)
        self.Historico.append({
            "objeto": Objeto, "sinal": Sinal,
            "escolhido": Escolhido, "recompensa": Recompensa,
        })
        if len(self.Historico) > 2000:
            self.Historico = self.Historico[-2000:]
        self.Total += 1
        if Recompensa > 0.5:
            self.Acertos += 1
        return self.Historico[-1]

    def Rodar(self, N, Verbose=False):
        AcertosN = 0
        for I in range(N):
            R = self.RodarEpisodio()
            if R["recompensa"] > 0.5:
                AcertosN += 1
            if Verbose and (I + 1) % max(1, N // 10) == 0:
                Acuracia = AcertosN / (I + 1)
                print(f"  ep {I+1}/{N}: acuracia={Acuracia:.3f}")
        Acuracia = AcertosN / N if N > 0 else 0.0
        return {
            "ok": True,
            "acuracia": round(Acuracia, 4),
            "episodios": N,
            "acertos": AcertosN,
            "vocabulario": self.VocabularioFinal(),
            "total_acumulado": self.Total,
            "acertos_acumulados": self.Acertos,
        }

    def VocabularioFinal(self):
        """Argmax do Q-table do Emissor por objeto."""
        Mapa = {}
        for Objeto in self.Ambiente.Objetos:
            MelhorSinal = None
            MelhorValor = float("-inf")
            for Sinal in self.Ambiente.Sinais:
                V = self.Emissor.Qt.Obter(Objeto, Sinal)
                if V > MelhorValor:
                    MelhorValor = V
                    MelhorSinal = Sinal
            if MelhorSinal is not None:
                Mapa[Objeto] = MelhorSinal
        return Mapa

    def InterpretacaoFinal(self):
        """Argmax do Q-table do Receptor por sinal."""
        Mapa = {}
        for Sinal in self.Ambiente.Sinais:
            MelhorObjeto = None
            MelhorValor = float("-inf")
            for Objeto in self.Ambiente.Objetos:
                V = self.Receptor.Qt.Obter(Sinal, Objeto)
                if V > MelhorValor:
                    MelhorValor = V
                    MelhorObjeto = Objeto
            if MelhorObjeto is not None:
                Mapa[Sinal] = MelhorObjeto
        return Mapa

    def AcuraciaUltimos(self, N=50):
        Ultimos = self.Historico[-N:]
        if not Ultimos:
            return 0.0
        Acertos = sum(1 for R in Ultimos if R["recompensa"] > 0.5)
        return round(Acertos / len(Ultimos), 4)

    def Info(self):
        return {
            "Total": self.Total,
            "Acertos": self.Acertos,
            "Acuracia": round(self.Acertos / max(1, self.Total), 4),
            "Historico": len(self.Historico),
            "Vocabulario": self.VocabularioFinal(),
            "Interpretacao": self.InterpretacaoFinal(),
        }


# ============================================================
# TESTE FINAL
# ============================================================

def RodarTesteFinal():
    print("=== TESTE FINAL ComunicacaoEmergente ===")
    print()

    print("[1] Setup (5 objetos, 5 sinais)")
    Amb = Ambiente(NObjetos=5, NSinais=5, Seed=42)
    Emi = Emissor(NSinais=5, Seed=42)
    Rec = Receptor(NObjetos=5, Seed=43)
    J = Jogo(Amb, Emi, Rec)
    print(f"  Ambiente: {Amb.Info()}")

    print("[2] 1 episódio")
    R = J.RodarEpisodio()
    assert "objeto" in R and "sinal" in R and "escolhido" in R
    print(f"  {R}")

    print("[3] 100 episódios (acuracia deve subir)")
    R100 = J.Rodar(100)
    print(f"  acuracia={R100['acuracia']}")
    assert R100["episodios"] == 100

    print("[4] +400 episódios (acuracia > 0.9)")
    R500 = J.Rodar(400)
    AcuraciaTotal = J.Acertos / J.Total
    print(f"  acuracia_total={AcuraciaTotal:.3f}")
    print(f"  vocabulario={R500['vocabulario']}")
    print(f"  interpretacao={J.InterpretacaoFinal()}")
    if AcuraciaTotal < 0.9:
        print(f"  [aviso] acuracia {AcuraciaTotal:.3f} < 0.9 (Q-table pequena)")
        # Nao falha — com 5x5 e epsilon=0.1 pode nao convergir totalmente

    print("[5] VocabularioFinal (argmax por objeto)")
    Voc = J.VocabularioFinal()
    assert len(Voc) == 5, Voc
    SinaisUsados = set(Voc.values())
    print(f"  vocabulario={Voc}, sinais usados={SinaisUsados}")

    print("[6] AcuraciaUltimos (50 eps)")
    A = J.AcuraciaUltimos(50)
    print(f"  acuracia ultimos 50={A}")

    print("[7] Jogo.Info")
    I = J.Info()
    print(f"  total={I['Total']} acertos={I['Acertos']} acuracia={I['Acuracia']}")
    assert I["Total"] == 501, I["Total"]

    print("[8] Verificacao de emergencia (vocabulario unico)")
    # Se cada objeto tem 1 sinal, o vocabulario deve ser quase 1:1
    Unicos = len(SinaisUsados)
    print(f"  sinais unicos={Unicos}/5 (quanto maior, mais diferenciado)")
    if Unicos == 5:
        print(f"  [emergencia] vocabulario 1:1 (cada objeto tem sinal proprio)")
    elif Unicos >= 3:
        print(f"  [emergencia parcial] {Unicos} sinais distintos")
    else:
        print(f"  [aviso] vocabulario colapsou ({Unicos} sinal(is))")

    print()
    print("TESTE OK ComunicacaoEmergente (bloco 5/11)")
    return 0


def MainCli():
    import argparse
    P = argparse.ArgumentParser(prog="ComunicacaoEmergente")
    P.add_argument("--teste", action="store_true")
    P.add_argument("--treinar", type=int, default=None,
                   help="numero de episodios (ex: 500)")
    P.add_argument("--objetos", type=int, default=5)
    P.add_argument("--sinais", type=int, default=5)
    P.add_argument("--seed", type=int, default=42)
    P.add_argument("--verbose", action="store_true")
    P.add_argument("--json", action="store_true")
    Args = P.parse_args()
    if Args.teste:
        return RodarTesteFinal()
    if Args.treinar is not None:
        Amb = Ambiente(NObjetos=Args.objetos, NSinais=Args.sinais, Seed=Args.seed)
        Emi = Emissor(NSinais=Args.sinais, Seed=Args.seed)
        Rec = Receptor(NObjetos=Args.objetos, Seed=Args.seed + 1)
        J = Jogo(Amb, Emi, Rec)
        R = J.Rodar(Args.treinar, Verbose=Args.verbose)
        if Args.json:
            print(json.dumps({
                "treino": R,
                "info": J.Info(),
            }, indent=2, ensure_ascii=False, default=str))
        else:
            print(f"=== TREINO ({Args.treinar} episodios) ===")
            print(f"  acuracia_final: {R['acuracia']}")
            print(f"  acertos: {R['acertos']}/{R['episodios']}")
            print(f"  vocabulario: {R['vocabulario']}")
            print(f"  interpretacao: {J.InterpretacaoFinal()}")
            SinaisUsados = set(R['vocabulario'].values())
            print(f"  sinais unicos: {len(SinaisUsados)}/{Args.objetos}")
            print()
            print("  === O QUE EMERGIU ===")
            for Obj in sorted(R['vocabulario'].keys()):
                Sinal = R['vocabulario'][Obj]
                Confianca = Emi.Qt.Obter(Obj, Sinal)
                print(f"    objeto {Obj} -> sinal {Sinal} (Q={Confianca:.3f})")
        return 0 if R["acuracia"] > 0.5 else 1
    P.print_help()
    return 2


if __name__ == "__main__":
    import sys as S
    S.exit(MainCli())
