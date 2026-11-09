# backends.py — backends pra RedeNeural.
# BackendC: chama .so via ctypes (rapido, matmul em C puro).
# BackendPython: fallback (Tensor do bloco 1).

import os
import ctypes


DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(DIR, "ternario.so")


class BackendC:
    def __init__(self, Caminho=None):
        Caminho = Caminho or LIB_PATH
        if not os.path.isfile(Caminho):
            raise FileNotFoundError(f"{Caminho} nao existe")
        self.Lib = ctypes.CDLL(Caminho)
        self._Configurar()
        self.Disponivel = True

    def _Configurar(self):
        DP = ctypes.POINTER(ctypes.c_double)
        self.Lib.Ternario_Matmul.argtypes = [DP, DP, DP, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.Lib.Ternario_Matmul.restype = None
        self.Lib.Ternario_Transpose.argtypes = [DP, DP, ctypes.c_int, ctypes.c_int]
        self.Lib.Ternario_Transpose.restype = None
        self.Lib.Ternario_Softmax.argtypes = [DP, DP, ctypes.c_int, ctypes.c_int]
        self.Lib.Ternario_Softmax.restype = None
        self.Lib.Ternario_Attention.argtypes = [
            DP, ctypes.c_int, ctypes.c_int,
            DP, DP, DP,
            DP, DP,
        ]
        self.Lib.Ternario_Attention.restype = ctypes.c_int
        self.Lib.Ternario_Sqrt.argtypes = [ctypes.c_double]
        self.Lib.Ternario_Sqrt.restype = ctypes.c_double
        self.Lib.Ternario_Exp.argtypes = [ctypes.c_double]
        self.Lib.Ternario_Exp.restype = ctypes.c_double
        self.Lib.Ternario_Versao.restype = ctypes.c_char_p

    def _Array(self, Dados):
        N = len(Dados)
        Arr = (ctypes.c_double * N)(*[float(x) for x in Dados])
        return Arr

    def Matmul(self, A, ShapeA, B, ShapeB):
        M, K = ShapeA
        K2, N = ShapeB
        if K != K2:
            raise ValueError(f"matmul: {ShapeA} x {ShapeB} incompativeis")
        arrA = self._Array(A)
        arrB = self._Array(B)
        arrC = (ctypes.c_double * (M * N))()
        self.Lib.Ternario_Matmul(arrA, arrB, arrC, M, K, N)
        return list(arrC)

    def Transpose(self, A, ShapeA):
        M, N = ShapeA
        arrA = self._Array(A)
        arrOut = (ctypes.c_double * (N * M))()
        self.Lib.Ternario_Transpose(arrA, arrOut, M, N)
        return list(arrOut), (N, M)

    def Softmax(self, A, ShapeA):
        M, N = ShapeA
        arrA = self._Array(A)
        arrOut = (ctypes.c_double * (M * N))()
        self.Lib.Ternario_Softmax(arrA, arrOut, M, N)
        return list(arrOut)

    def Sqrt(self, X):
        return float(self.Lib.Ternario_Sqrt(ctypes.c_double(X)))

    def Exp(self, X):
        return float(self.Lib.Ternario_Exp(ctypes.c_double(X)))

    def Attention(self, X, ShapeX, Wq, Wk, Wv, ShapeW):
        SeqLen, DModel = ShapeX
        arrX = self._Array(X)
        arrQ = self._Array(Wq)
        arrK = self._Array(Wk)
        arrV = self._Array(Wv)
        arrOut = (ctypes.c_double * (SeqLen * DModel))()
        arrPesos = (ctypes.c_double * (SeqLen * SeqLen))()
        R = self.Lib.Ternario_Attention(
            arrX, SeqLen, DModel,
            arrQ, arrK, arrV,
            arrOut, arrPesos,
        )
        if R != 0:
            raise RuntimeError(f"attention falhou: {R}")
        return list(arrOut), list(arrPesos)

    def Versao(self):
        return self.Lib.Ternario_Versao().decode("utf-8", "replace")


def CompilarC():
    """Compila ternario.c -> ternario.so se nao existir."""
    import subprocess
    CaminhoC = os.path.join(DIR, "ternario.c")
    if not os.path.isfile(CaminhoC):
        return {"ok": False, "motivo": "ternario.c nao existe"}
    if os.path.isfile(LIB_PATH):
        return {"ok": True, "ja_compilado": True, "caminho": LIB_PATH}
    try:
        R = subprocess.run(
            ["gcc", "-O3", "-march=native", "-shared", "-fPIC",
             "-o", LIB_PATH, CaminhoC],
            capture_output=True, text=True, timeout=60,
        )
        if R.returncode != 0:
            return {"ok": False, "motivo": "gcc_falhou", "erro": R.stderr[:500]}
        return {"ok": True, "caminho": LIB_PATH}
    except FileNotFoundError:
        return {"ok": False, "motivo": "gcc_nao_instalado"}
    except Exception as E:
        return {"ok": False, "motivo": f"excecao:{type(E).__name__}", "erro": str(E)}


def EscolherBackend():
    """Tenta C, cai pra Python."""
    R = CompilarC()
    if R.get("ok"):
        try:
            return BackendC()
        except Exception as E:
            return {"Erro": str(E), "Backend": "python"}
    return {"Erro": R.get("motivo"), "Backend": "python"}


def RodarTeste():
    print("=== TESTE BackendC ===")
    print()
    R = CompilarC()
    print(f"[1] Compilar: {R}")
    if not R.get("ok"):
        print("[aviso] C indisponivel, teste abortado")
        return 1
    B = BackendC()
    print(f"[2] Versao: {B.Versao()}")
    print()
    print("[3] Sqrt (Newton-Raphson)")
    for X in [4.0, 9.0, 2.0, 0.25]:
        R_ = B.Sqrt(X)
        Esperado = X ** 0.5
        assert abs(R_ - Esperado) < 1e-6, f"sqrt({X}) = {R_} != {Esperado}"
        print(f"  sqrt({X}) = {R_:.6f}")
    print()
    print("[4] Exp (Taylor + range reduction)")
    for X in [0.0, 1.0, 2.0, -1.0]:
        R_ = B.Exp(X)
        Esperado = 2.718281828459045 ** X
        assert abs(R_ - Esperado) / max(1e-9, abs(Esperado)) < 1e-6, f"exp({X}) = {R_} != {Esperado}"
        print(f"  exp({X}) = {R_:.6f}")
    print()
    print("[5] Matmul (2,3)x(3,2)")
    A = [1, 2, 3, 4, 5, 6]
    B_ = [1, 2, 3, 4, 5, 6]
    C = B.Matmul(A, (2, 3), B_, (3, 2))
    assert C[0] == 22.0, C[0]
    assert C[3] == 64.0, C[3]
    print(f"  C = {[round(x, 1) for x in C]}")
    print()
    print("[6] Transpose (2,3) -> (3,2)")
    T, S = B.Transpose(A, (2, 3))
    assert S == (3, 2)
    assert T[0] == 1.0
    assert T[5] == 6.0
    print(f"  shape = {S}, dados = {T}")
    print()
    print("[7] Softmax soma 1")
    S_ = B.Softmax([1.0, 2.0, 3.0], (1, 3))
    assert abs(sum(S_) - 1.0) < 1e-9, sum(S_)
    print(f"  softmax = {[round(x, 4) for x in S_]} soma={sum(S_):.6f}")
    print()
    print("[8] Attention seq 8x8 d_model 8")
    import random
    random.seed(99)
    X = [random.uniform(-0.5, 0.5) for _ in range(64)]
    Wq = [random.uniform(-0.5, 0.5) for _ in range(64)]
    Wk = [random.uniform(-0.5, 0.5) for _ in range(64)]
    Wv = [random.uniform(-0.5, 0.5) for _ in range(64)]
    Out, Pesos = B.Attention(X, (8, 8), Wq, Wk, Wv, (8, 8))
    assert len(Out) == 64
    assert len(Pesos) == 64
    # Pesos devem somar 1 por linha
    for I in range(8):
        Soma = sum(Pesos[I * 8 + J] for J in range(8))
        assert abs(Soma - 1.0) < 1e-6, f"linha {I} soma {Soma}"
    print(f"  output 64 vals, pesos 64 vals, pesos somam 1 por linha")
    print()
    print("TESTE OK BackendC")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(RodarTeste())
