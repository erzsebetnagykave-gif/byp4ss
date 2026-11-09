#!/usr/bin/env python3
# RedeNeural — rede neural propria com atencao + acao + aprendizado.
# Python puro. Zero dependencia externa. Deterministico.
# Bloco 1/3: Tensor + Atencao.

import os
import sys
import math
import json


# ============================================================
# TENSOR
# ============================================================

class Tensor:
    """Tensor 2D (ou 1D como (n, 1)). Sem numpy. Deterministico."""

    def __init__(self, Dados, Shape):
        if not isinstance(Dados, list):
            Dados = list(Dados)
        if not isinstance(Shape, tuple):
            Shape = tuple(Shape)
        if len(Shape) == 1:
            Shape = (Shape[0], 1)
        if len(Shape) != 2:
            raise ValueError(f"Shape deve ser 2D, veio {Shape}")
        Esperado = Shape[0] * Shape[1]
        if len(Dados) != Esperado:
            raise ValueError(f"Shape {Shape} precisa {Esperado} dados, veio {len(Dados)}")
        self.Dados = [float(x) for x in Dados]
        self.Shape = Shape

    @staticmethod
    def Zeros(Shape):
        Linhas, Colunas = Shape if len(Shape) == 2 else (Shape[0], 1)
        return Tensor([0.0] * (Linhas * Colunas), (Linhas, Colunas))

    @staticmethod
    def Aleatorio(Shape, Seed=42):
        """Deterministico — LCG proprio, nao usa random.random()."""
        Linhas, Colunas = Shape if len(Shape) == 2 else (Shape[0], 1)
        N = Linhas * Colunas
        Estado = Seed & 0xFFFFFFFF
        Dados = []
        for _ in range(N):
            Estado = (1103515245 * Estado + 12345) & 0x7FFFFFFF
            Dados.append((Estado / 0x7FFFFFFF) - 0.5)
        return Tensor(Dados, (Linhas, Colunas))

    def Get(self, I, J):
        return self.Dados[I * self.Shape[1] + J]

    def Set(self, I, J, V):
        self.Dados[I * self.Shape[1] + J] = float(V)

    def Matmul(self, Outro):
        if self.Shape[1] != Outro.Shape[0]:
            raise ValueError(f"matmul: {self.Shape} x {Outro.Shape} incompativeis")
        M, K = self.Shape
        _, N = Outro.Shape
        Out = Tensor.Zeros((M, N))
        for I in range(M):
            for J in range(N):
                Soma = 0.0
                for Kk in range(K):
                    Soma += self.Get(I, Kk) * Outro.Get(Kk, J)
                Out.Set(I, J, Soma)
        return Out

    def Transpose(self):
        M, N = self.Shape
        Out = Tensor.Zeros((N, M))
        for I in range(M):
            for J in range(N):
                Out.Set(J, I, self.Get(I, J))
        return Out

    def Somar(self, Outro):
        if self.Shape != Outro.Shape:
            raise ValueError(f"soma: {self.Shape} != {Outro.Shape}")
        Out = Tensor.Zeros(self.Shape)
        for I in range(len(self.Dados)):
            Out.Dados[I] = self.Dados[I] + Outro.Dados[I]
        return Out

    def Escalar(self, E):
        Out = Tensor.Zeros(self.Shape)
        for I in range(len(self.Dados)):
            Out.Dados[I] = self.Dados[I] * float(E)
        return Out

    def Softmax(self):
        """Softmax por linha (cada linha soma 1)."""
        M, N = self.Shape
        Out = Tensor.Zeros(self.Shape)
        for I in range(M):
            Linha = [self.Get(I, J) for J in range(N)]
            Max = max(Linha)
            Exps = [math.exp(x - Max) for x in Linha]
            Soma = sum(Exps)
            for J in range(N):
                Out.Set(I, J, Exps[J] / Soma)
        return Out

    def Relu(self):
        Out = Tensor.Zeros(self.Shape)
        for I in range(len(self.Dados)):
            Out.Dados[I] = max(0.0, self.Dados[I])
        return Out

    def Soma(self):
        return sum(self.Dados)

    def Media(self):
        return sum(self.Dados) / len(self.Dados) if self.Dados else 0.0

    def ToList(self):
        return list(self.Dados)

    def __repr__(self):
        return f"Tensor({self.Shape}, {[round(x, 3) for x in self.Dados[:8]]}...)"


# ============================================================
# ATENCAO (self-attention escalonada, 1 head)
# ============================================================

class Atencao:
    """Self-attention escalonada. 1 head. Deterministico."""

    def __init__(self, DModel):
        self.DModel = DModel
        self.Wq = Tensor.Aleatorio((DModel, DModel), Seed=11)
        self.Wk = Tensor.Aleatorio((DModel, DModel), Seed=22)
        self.Wv = Tensor.Aleatorio((DModel, DModel), Seed=33)
        self.UltimoQ = None
        self.UltimoK = None
        self.UltimoV = None
        self.UltimosPesos = None
        self.UltimoOutput = None

    def Forward(self, X):
        """X: (seq_len, d_model) -> (seq_len, d_model)."""
        if X.Shape[1] != self.DModel:
            raise ValueError(f"atencao: esperado d_model={self.DModel}, veio {X.Shape}")
        Q = X.Matmul(self.Wq)
        K = X.Matmul(self.Wk)
        V = X.Matmul(self.Wv)
        self.UltimoQ, self.UltimoK, self.UltimoV = Q, K, V
        Escala = math.sqrt(self.DModel)
        Scores = Q.Matmul(K.Transpose()).Escalar(1.0 / Escala)
        Pesos = Scores.Softmax()
        self.UltimosPesos = Pesos
        Output = Pesos.Matmul(V)
        self.UltimoOutput = Output
        return Output

    def Pesos(self):
        return self.UltimosPesos

    def Output(self):
        return self.UltimoOutput

    def Info(self):
        return {
            "d_model": self.DModel,
            "wq_shape": self.Wq.Shape,
            "wk_shape": self.Wk.Shape,
            "wv_shape": self.Wv.Shape,
        }


# ============================================================
# TESTE (bloco 1)
# ============================================================

def RodarTeste():
    print("=== TESTE RedeNeural v1 (Tensor + Atencao) ===")
    print()

    print("[1] Tensor.from_list")
    T = Tensor([1, 2, 3, 4], (2, 2))
    assert T.Shape == (2, 2)
    assert T.Get(0, 0) == 1.0
    assert T.Get(1, 1) == 4.0
    print(f"  {T}")

    print("[2] Tensor.Zeros")
    Z = Tensor.Zeros((3, 3))
    assert Z.Shape == (3, 3)
    assert Z.Soma() == 0.0
    print(f"  shape={Z.Shape}, soma=0")

    print("[3] Tensor.Matmul (2,3)x(3,2) -> (2,2)")
    A = Tensor([1, 2, 3, 4, 5, 6], (2, 3))
    B = Tensor([1, 2, 3, 4, 5, 6], (3, 2))
    C = A.Matmul(B)
    assert C.Shape == (2, 2)
    assert C.Get(0, 0) == 22.0, C.Get(0, 0)
    assert C.Get(1, 1) == 64.0, C.Get(1, 1)
    print(f"  C={C}")

    print("[4] Tensor.Transpose (2,3) -> (3,2)")
    Tr = A.Transpose()
    assert Tr.Shape == (3, 2)
    assert Tr.Get(0, 0) == 1.0
    assert Tr.Get(2, 1) == 6.0
    print(f"  shape={Tr.Shape}")

    print("[5] Tensor.Softmax soma 1")
    S = Tensor([1.0, 2.0, 3.0], (1, 3))
    Sm = S.Softmax()
    assert abs(Sm.Soma() - 1.0) < 1e-9, Sm.Soma()
    print(f"  softmax soma={Sm.Soma():.6f}")

    print("[6] Atencao.Forward sequencia 8x8")
    Att = Atencao(8)
    X = Tensor.Aleatorio((8, 8), Seed=99)
    Out = Att.Forward(X)
    assert Out.Shape == (8, 8)
    print(f"  output shape={Out.Shape}")

    print("[7] Atencao deterministica (mesmo input = mesmo output)")
    Att2 = Atencao(8)
    Out2 = Att2.Forward(X)
    for I in range(len(Out.Dados)):
        assert abs(Out.Dados[I] - Out2.Dados[I]) < 1e-9, f"diferenca em {I}"
    print(f"  deterministico OK")

    print("[8] Atencao.Pesos soma 1 por linha")
    P = Att.Pesos()
    assert P.Shape == (8, 8)
    for I in range(8):
        Soma = sum(P.Get(I, J) for J in range(8))
        assert abs(Soma - 1.0) < 1e-6, f"linha {I} soma {Soma}"
    print(f"  pesos somam 1 por linha OK")

    print()
    print("TESTE OK bloco 1/3")
    return 0




# ============================================================
# BLOCO 2/3 — MLP + BACKPROP + QTABLE
# ============================================================

import random
import hashlib


class MLP:
    """MLP 8 -> 16 -> 15. ReLU escondido. Backprop manual (chain rule)."""

    def __init__(self, DEntrada=8, DEscondido=16, DSaida=15, Seed=42):
        self.DEntrada = DEntrada
        self.DEscondido = DEscondido
        self.DSaida = DSaida
        # Pesos determinísticos (LCG)
        self.W1 = self._Aleatorio((DEntrada, DEscondido), Seed)
        self.B1 = self._Aleatorio((1, DEscondido), Seed + 1)
        self.W2 = self._Aleatorio((DEscondido, DSaida), Seed + 2)
        self.B2 = self._Aleatorio((1, DSaida), Seed + 3)

    def _Aleatorio(self, Shape, Seed):
        M, N = Shape
        Estado = Seed & 0xFFFFFFFF
        Dados = []
        for _ in range(M * N):
            Estado = (1103515245 * Estado + 12345) & 0x7FFFFFFF
            Dados.append((Estado / 0x7FFFFFFF - 0.5) * 0.5)
        return Tensor(Dados, Shape)

    def Forward(self, X):
        """X: Tensor (1, DEntrada) -> Tensor (1, DSaida)."""
        self.X = X
        self.HPre = X.Matmul(self.W1).Somar(self.B1)
        self.H = self.HPre.Relu()
        self.Y = self.H.Matmul(self.W2).Somar(self.B2)
        return self.Y

    def Backprop(self, Target, Lr=0.01):
        """Target: lista de DSaida floats. Atualiza pesos. Retorna loss (MSE)."""
        YLista = self.Y.ToList()
        GradY = [YLista[i] - float(Target[i]) for i in range(self.DSaida)]
        Loss = sum(g * g for g in GradY) / self.DSaida
        # grad_W2 = H^T @ grad_y
        GradYT = Tensor(GradY, (1, self.DSaida))
        GradW2 = self.H.Transpose().Matmul(GradYT)
        GradB2 = GradYT
        # grad_h = grad_y @ W2^T
        GradH = GradYT.Matmul(self.W2.Transpose())
        # relu derivate
        HPreLista = self.HPre.ToList()
        GradHLista = GradH.ToList()
        for i in range(len(GradHLista)):
            if HPreLista[i] <= 0.0:
                GradHLista[i] = 0.0
        GradH = Tensor(GradHLista, self.H.Shape)
        # grad_W1 = X^T @ grad_h
        GradW1 = self.X.Transpose().Matmul(GradH)
        GradB1 = GradH
        # Atualiza (gradient descent)
        self.W1 = self.W1.Somar(GradW1.Escalar(-Lr))
        self.B1 = self.B1.Somar(GradB1.Escalar(-Lr))
        self.W2 = self.W2.Somar(GradW2.Escalar(-Lr))
        self.B2 = self.B2.Somar(GradB2.Escalar(-Lr))
        return Loss


class QTable:
    """Q-Learning tabular. Estado = hash de string. Acao = string."""

    def __init__(self, Alpha=0.1, Gamma=0.9, Epsilon=0.1):
        self.Alpha = float(Alpha)
        self.Gamma = float(Gamma)
        self.Epsilon = float(Epsilon)
        self.Dados = {}
        self.Meta = {"Updates": 0}

    def Hash(self, Estado):
        if isinstance(Estado, (list, tuple)):
            S = "|".join(f"{float(x):.3f}" for x in Estado)
        else:
            S = str(Estado)
        return hashlib.sha256(S.encode("utf-8")).hexdigest()[:16]

    def Obter(self, Estado, Acao):
        H = self.Hash(Estado)
        return float(self.Dados.get(H, {}).get(Acao, 0.0))

    def Atualizar(self, Estado, Acao, Recompensa, Proximo, Done):
        H = self.Hash(Estado)
        HProx = self.Hash(Proximo)
        QAtual = self.Dados.get(H, {}).get(Acao, 0.0)
        if Done:
            QMaxProx = 0.0
        else:
            QMaxProx = max(self.Dados.get(HProx, {}).values(), default=0.0)
        Alvo = Recompensa + self.Gamma * QMaxProx
        QNovo = QAtual + self.Alpha * (Alvo - QAtual)
        self.Dados.setdefault(H, {})[Acao] = float(QNovo)
        self.Meta["Updates"] = self.Meta.get("Updates", 0) + 1
        return QNovo

    def Escolher(self, Estado, Acoes):
        if not Acoes:
            return None
        if random.random() < self.Epsilon:
            return random.choice(Acoes)
        return self.MelhorAcao(Estado, Acoes)

    def MelhorAcao(self, Estado, Acoes):
        if not Acoes:
            return None
        H = self.Hash(Estado)
        Linha = self.Dados.get(H, {})
        Melhor = None
        MelhorV = float("-inf")
        for A in Acoes:
            V = Linha.get(A, 0.0)
            if V > MelhorV:
                MelhorV = V
                Melhor = A
        return Melhor if Melhor is not None else Acoes[0]

    def Salvar(self, Caminho):
        try:
            with open(Caminho, "w", encoding="utf-8") as F:
                json.dump({
                    "Versao": 1,
                    "Config": {"Alpha": self.Alpha, "Gamma": self.Gamma, "Epsilon": self.Epsilon},
                    "Meta": self.Meta,
                    "Dados": self.Dados,
                }, F, ensure_ascii=False, indent=2)
            return {"ok": True, "caminho": Caminho, "n_estados": len(self.Dados)}
        except Exception as E:
            return {"ok": False, "motivo": f"{type(E).__name__}:{E}"}

    def Carregar(self, Caminho):
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                P = json.load(F)
            self.Alpha = P.get("Config", {}).get("Alpha", self.Alpha)
            self.Gamma = P.get("Config", {}).get("Gamma", self.Gamma)
            self.Epsilon = P.get("Config", {}).get("Epsilon", self.Epsilon)
            self.Meta = P.get("Meta", self.Meta)
            self.Dados = P.get("Dados", {})
            return {"ok": True, "n_estados": len(self.Dados)}
        except Exception as E:
            return {"ok": False, "motivo": f"{type(E).__name__}:{E}"}


def RodarTesteBloco2():
    print("=== TESTE RedeNeural v2 (MLP + Backprop + QTable) ===")
    print()

    print("[1] MLP.Forward (1,8) -> (1,15)")
    M = MLP(8, 16, 15, Seed=42)
    X = Tensor.Aleatorio((1, 8), Seed=99)
    Y = M.Forward(X)
    assert Y.Shape == (1, 15), Y.Shape
    print(f"  output shape={Y.Shape}")

    print("[2] MLP determinístico")
    M2 = MLP(8, 16, 15, Seed=42)
    Y2 = M2.Forward(X)
    for I in range(len(Y.Dados)):
        assert abs(Y.Dados[I] - Y2.Dados[I]) < 1e-9
    print(f"  deterministico OK")

    print("[3] Backprop reduz loss (100 iterações, target fixo)")
    M3 = MLP(8, 16, 15, Seed=42)
    Target = [1.0] + [0.0] * 14
    LossInicial = None
    for It in range(100):
        Y = M3.Forward(X)
        Loss = M3.Backprop(Target, Lr=0.05)
        if It == 0:
            LossInicial = Loss
    assert Loss < LossInicial, f"loss nao reduziu: {LossInicial} -> {Loss}"
    print(f"  loss: {LossInicial:.4f} -> {Loss:.4f} (reduziu)")

    print("[4] QTable.Atualizar move Q-value")
    Q = QTable(Alpha=0.5, Gamma=0.9, Epsilon=0.0)
    Estado = [0.0, 1.0, 0.5]
    Q.Atualizar(Estado, "scan", 10.0, [0.0, 1.0, 0.5], True)
    V = Q.Obter(Estado, "scan")
    assert abs(V - 5.0) < 1e-9, V
    print(f"  Q(scan) = {V} (esperado 5.0)")

    print("[5] QTable.Escolher epsilon=0 (argmax)")
    Q2 = QTable(Alpha=0.1, Gamma=0.9, Epsilon=0.0)
    Q2.Dados[Q2.Hash([1.0, 0.0])] = {"scan": 1.0, "cred": 9.0, "upnp": 3.0}
    A = Q2.Escolher([1.0, 0.0], ["scan", "cred", "upnp"])
    assert A == "cred", A
    print(f"  escolheu: {A}")

    print("[6] QTable.Escolher epsilon=1 (explora)")
    Q3 = QTable(Epsilon=1.0)
    Vistas = set()
    for _ in range(50):
        Vistas.add(Q3.Escolher([0.0], ["a", "b", "c"]))
    assert len(Vistas) >= 2, Vistas
    print(f"  acoes vistas: {sorted(Vistas)}")

    print("[7] QTable.Salvar + Carregar")
    import tempfile
    Tmp = tempfile.mktemp(suffix="_qtable.json")
    Q4 = QTable(Alpha=0.1, Gamma=0.9, Epsilon=0.1)
    Q4.Atualizar([0.5, 0.5], "cred", 10.0, [0.0, 0.0], True)
    R = Q4.Salvar(Tmp)
    assert R.get("ok"), R
    Q5 = QTable()
    R = Q5.Carregar(Tmp)
    assert R.get("ok"), R
    assert abs(Q5.Obter([0.5, 0.5], "cred") - Q4.Obter([0.5, 0.5], "cred")) < 1e-9
    os.remove(Tmp)
    print(f"  salvo/carregado: {R.get('n_estados')} estados")

    print("[8] QTable.MelhorAcao (argmax)")
    Q6 = QTable()
    Q6.Dados[Q6.Hash([1.0, 1.0])] = {"a": 1.0, "b": 5.0, "c": 3.0}
    A = Q6.MelhorAcao([1.0, 1.0], ["a", "b", "c"])
    assert A == "b", A
    print(f"  melhor: {A}")

    print()
    print("TESTE OK bloco 2/3")
    return 0


if __name__ == "__main__":
    sys.exit(RodarTesteBloco2())


# ============================================================
# BLOCO 3/3 — ORQUESTRADOR + CLI + TESTE FINAL
# ============================================================

class RedeNeural:
    """Orquestrador: atencao + MLP + QTable."""

    def __init__(self, DEntrada=8, DEscondido=16, NAcoes=15, Seed=42):
        self.DEntrada = DEntrada
        self.DEscondido = DEscondido
        self.NAcoes = NAcoes
        self.At = Atencao(DEntrada)
        self.Mlp = MLP(DEntrada, DEscondido, NAcoes, Seed=Seed)
        self.Qt = QTable(Alpha=0.1, Gamma=0.9, Epsilon=0.1)
        self.Acoes = [f"acao_{i}" for i in range(NAcoes)]
        self.EstadoAtual = [0.0] * DEntrada

    def Observar(self, Estado):
        T = Tensor(Estado, (1, self.DEntrada))
        self.EstadoAtual = list(Estado)
        return T

    def Prever(self, Estado):
        T = Tensor(Estado, (1, self.DEntrada))
        Y = self.Mlp.Forward(T)
        return Y.ToList()

    def Escolher(self, Estado, Acoes=None):
        Acoes = Acoes or self.Acoes
        return self.Qt.Escolher(Estado, Acoes)

    def Atualizar(self, Estado, Acao, Recompensa, Proximo, Done):
        QNovo = self.Qt.Atualizar(Estado, Acao, Recompensa, Proximo, Done)
        # MLP aprende a prever QNovo
        Y = self.Mlp.Forward(Tensor(Estado, (1, self.DEntrada)))
        YLista = Y.ToList()
        Idx = self.Acoes.index(Acao) if Acao in self.Acoes else 0
        Target = list(YLista)
        Target[Idx] = QNovo
        Loss = self.Mlp.Backprop(Target, Lr=0.01)
        return {"QNovo": QNovo, "Loss": Loss}

    def TreinarBatch(self, Batch, Epocas=1):
        LossTotal = 0.0
        for _ in range(Epocas):
            for (S, A, R, SP, D) in Batch:
                R_ = self.Atualizar(S, A, R, SP, D)
                LossTotal += R_["Loss"]
        return {"LossTotal": LossTotal, "N": len(Batch) * Epocas}

    def Salvar(self, Caminho):
        R = self.Qt.Salvar(Caminho)
        if not R.get("ok"):
            return R
        try:
            CaminhoPesos = Caminho + ".pesos.json"
            with open(CaminhoPesos, "w", encoding="utf-8") as F:
                json.dump({
                    "W1": self.Mlp.W1.ToList(), "B1": self.Mlp.B1.ToList(),
                    "W2": self.Mlp.W2.ToList(), "B2": self.Mlp.B2.ToList(),
                }, F)
            R["pesos"] = CaminhoPesos
        except Exception as E:
            R["aviso"] = f"pesos_nao_salvos:{E}"
        return R

    def Carregar(self, Caminho):
        R = self.Qt.Carregar(Caminho)
        if not R.get("ok"):
            return R
        try:
            CaminhoPesos = Caminho + ".pesos.json"
            with open(CaminhoPesos, "r", encoding="utf-8") as F:
                P = json.load(F)
            self.Mlp.W1 = Tensor(P["W1"], (self.DEntrada, self.DEscondido))
            self.Mlp.B1 = Tensor(P["B1"], (1, self.DEscondido))
            self.Mlp.W2 = Tensor(P["W2"], (self.DEscondido, self.NAcoes))
            self.Mlp.B2 = Tensor(P["B2"], (1, self.NAcoes))
            R["pesos"] = CaminhoPesos
        except Exception as E:
            R["aviso"] = f"pesos_nao_carregados:{E}"
        return R

    def Info(self):
        return {
            "d_entrada": self.DEntrada,
            "d_escondido": self.DEscondido,
            "n_acoes": self.NAcoes,
            "atencao": self.At.Info(),
            "qtable_estados": len(self.Qt.Dados),
            "qtable_updates": self.Qt.Meta.get("Updates", 0),
        }


def RodarTesteFinal():
    print("=== TESTE FINAL RedeNeural ===")
    print()
    R = RedeNeural(8, 16, 15, Seed=42)
    print(f"[0] Info: {R.Info()}")
    print()

    print("[1] Observar (1,8)")
    T = R.Observar([0.1] * 8)
    assert T.Shape == (1, 8), T.Shape
    print(f"  shape={T.Shape}")

    print("[2] Prever 15 Q-values")
    Q = R.Prever([0.1] * 8)
    assert len(Q) == 15, len(Q)
    print(f"  Q-values[0:3]={[round(x, 3) for x in Q[:3]]}")

    print("[3] Escolher epsilon=0 (argmax)")
    R.Qt.Epsilon = 0.0
    R.Qt.Dados[R.Qt.Hash([0.1] * 8)] = {"acao_0": 1.0, "acao_5": 9.0, "acao_10": 3.0}
    A = R.Escolher([0.1] * 8)
    assert A == "acao_5", A
    print(f"  escolheu: {A}")

    print("[4] Escolher epsilon=1 (explora)")
    R.Qt.Epsilon = 1.0
    Vistas = set()
    for _ in range(50):
        Vistas.add(R.Escolher([0.2] * 8))
    assert len(Vistas) >= 2, Vistas
    print(f"  acoes vistas: {len(Vistas)}")

    print("[5] Atualizar (QTable + Backprop)")
    R.Qt.Epsilon = 0.1
    Est = [0.5] * 8
    Res = R.Atualizar(Est, "acao_0", 10.0, Est, True)
    assert Res["QNovo"] == 1.0, Res["QNovo"]  # 0.1 * 10 = 1.0
    print(f"  QNovo={Res['QNovo']}, loss={Res['Loss']:.4f}")

    print("[6] TreinarBatch (10 iterações)")
    Batch = [
        ([0.1] * 8, "acao_0", 1.0, [0.2] * 8, False),
        ([0.2] * 8, "acao_1", 2.0, [0.3] * 8, False),
        ([0.3] * 8, "acao_2", 5.0, [0.4] * 8, False),
    ]
    R2 = RedeNeural(8, 16, 15, Seed=42)
    Res = R2.TreinarBatch(Batch, Epocas=10)
    assert Res["N"] == 30, Res["N"]
    print(f"  LossTotal={Res['LossTotal']:.4f}, N={Res['N']}")

    print("[7] Salvar + Carregar")
    import tempfile
    Tmp = tempfile.mktemp(suffix="_rede.json")
    S = R.Salvar(Tmp)
    assert S.get("ok"), S
    R3 = RedeNeural(8, 16, 15, Seed=42)
    C = R3.Carregar(Tmp)
    assert C.get("ok"), C
    print(f"  salvo/carregado: {C.get('n_estados')} estados")
    for P in (Tmp, Tmp + ".pesos.json"):
        if os.path.isfile(P):
            os.remove(P)

    print("[8] Info final")
    I = R.Info()
    assert I["n_acoes"] == 15
    assert I["qtable_updates"] >= 1
    print(f"  {I}")

    print()
    print("TESTE OK RedeNeural (bloco 3/3)")
    return 0


def Main():
    import argparse
    P = argparse.ArgumentParser(prog="RedeNeural")
    P.add_argument("--teste", action="store_true")
    P.add_argument("--info", action="store_true")
    P.add_argument("--estado", default=None,
                   help="8 floats separados por virgula")
    P.add_argument("--salvar", default=None)
    Args = P.parse_args()
    if Args.teste:
        return RodarTesteBloco2()
    if Args.info:
        R = RedeNeural()
        print(json.dumps(R.Info(), indent=2, ensure_ascii=False))
        return 0
    if Args.estado:
        try:
            Vals = [float(x.strip()) for x in Args.estado.split(",")]
            if len(Vals) != 8:
                print(f"[erro] --estado precisa 8 floats, veio {len(Vals)}")
                return 2
            R = RedeNeural()
            Q = R.Prever(Vals)
            A = R.Escolher(Vals)
            print(json.dumps({"Q_values": Q, "acao": A}, indent=2))
            return 0
        except ValueError as E:
            print(f"[erro] {E}")
            return 2
    P.print_help()
    return 2


if __name__ == "__main__":
    import sys as S
    if S.argv[1:] and S.argv[1] == "final":
        S.exit(RodarTesteFinal())
    S.exit(Main())
