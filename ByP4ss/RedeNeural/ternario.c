/* ternario.c — Tensor + Atencao em C puro.
 * Sem BLAS. Sem numpy. Sem math.h (exp e sqrt proprios).
 * Compilado como .so, chamado do Python via ctypes. */

#include <stdlib.h>
#include <string.h>

/* ============================================================
 * MATEMATICA PROPRIA (sem math.h)
 * ============================================================ */

/* sqrt via Newton-Raphson. 5 iteracoes. Converge pra 1e-9. */
double Ternario_Sqrt(double X) {
    if (X <= 0.0) return 0.0;
    double R = X;
    for (int I = 0; I < 5; I++) {
        R = 0.5 * (R + X / R);
    }
    return R;
}

/* exp via Taylor + range reduction.
 * exp(x) = 2^k * exp(r), r = x - k*ln2, |r| < ln2/2
 * exp(r) = sum(r^n / n!), n=0..12
 * 2^k = bit shift (union com long long). */
double Ternario_Exp(double X) {
    if (X > 709.0) return 1e308;
    if (X < -709.0) return 0.0;
    const double LN2 = 0.6931471805599453;
    const double INV_LN2 = 1.4426950408889634;
    int K = (int)(X * INV_LN2 + (X >= 0 ? 0.5 : -0.5));
    double R = X - K * LN2;
    double Termo = 1.0;
    double Soma = 1.0;
    for (int N = 1; N <= 12; N++) {
        Termo *= R / N;
        Soma += Termo;
    }
    /* 2^K via manipulacao de bits (IEEE 754 double) */
    union { double D; long long I; } U;
    int KAbs = K >= 0 ? K : -K;
    U.I = ((long long)(1023 + KAbs)) << 52;
    if (K >= 0) return Soma * U.D;
    return Soma / U.D;
}

/* ============================================================
 * MATMUL com cache tiling (blocos de 64)
 * ============================================================ */

void Ternario_Matmul(
    const double* A, const double* B, double* C,
    int M, int K, int N
) {
    /* Zera C */
    for (int I = 0; I < M * N; I++) C[I] = 0.0;

    /* Cache tiling: 64x64 blocos (cabem em L1) */
    const int BLOCO = 64;
    for (int I0 = 0; I0 < M; I0 += BLOCO) {
        int I1 = I0 + BLOCO < M ? I0 + BLOCO : M;
        for (int J0 = 0; J0 < N; J0 += BLOCO) {
            int J1 = J0 + BLOCO < N ? J0 + BLOCO : N;
            for (int K0 = 0; K0 < K; K0 += BLOCO) {
                int K1 = K0 + BLOCO < K ? K0 + BLOCO : K;
                for (int I = I0; I < I1; I++) {
                    for (int J = J0; J < J1; J++) {
                        double Soma = C[I * N + J];
                        for (int Kk = K0; Kk < K1; Kk++) {
                            Soma += A[I * K + Kk] * B[Kk * N + J];
                        }
                        C[I * N + J] = Soma;
                    }
                }
            }
        }
    }
}

/* ============================================================
 * TRANSPOSE com cache blocking
 * ============================================================ */

void Ternario_Transpose(
    const double* A, double* Out, int M, int N
) {
    const int BLOCO = 64;
    for (int I0 = 0; I0 < M; I0 += BLOCO) {
        int I1 = I0 + BLOCO < M ? I0 + BLOCO : M;
        for (int J0 = 0; J0 < N; J0 += BLOCO) {
            int J1 = J0 + BLOCO < N ? J0 + BLOCO : N;
            for (int I = I0; I < I1; I++) {
                for (int J = J0; J < J1; J++) {
                    Out[J * M + I] = A[I * N + J];
                }
            }
        }
    }
}

/* ============================================================
 * SOFTMAX por linha (exp proprio)
 * ============================================================ */

void Ternario_Softmax(
    const double* X, double* Out, int M, int N
) {
    for (int I = 0; I < M; I++) {
        double Max = X[I * N];
        for (int J = 1; J < N; J++) {
            if (X[I * N + J] > Max) Max = X[I * N + J];
        }
        double Soma = 0.0;
        for (int J = 0; J < N; J++) {
            Out[I * N + J] = Ternario_Exp(X[I * N + J] - Max);
            Soma += Out[I * N + J];
        }
        if (Soma > 0.0) {
            for (int J = 0; J < N; J++) {
                Out[I * N + J] /= Soma;
            }
        }
    }
}

/* ============================================================
 * ATENCAO (self-attention escalonada, 1 head, tudo em C)
 * ============================================================
 * X: (seq_len, d_model)
 * Wq, Wk, Wv: (d_model, d_model)
 * Output: (seq_len, d_model)
 * Pesos: (seq_len, seq_len) — attention weights
 */

int Ternario_Attention(
    const double* X, int SeqLen, int DModel,
    const double* Wq, const double* Wk, const double* Wv,
    double* Output, double* PesosOut
) {
    /* Q = X @ Wq, K = X @ Wk, V = X @ Wv — cada um (seq_len, d_model) */
    double* Q = (double*)malloc(SeqLen * DModel * sizeof(double));
    double* K = (double*)malloc(SeqLen * DModel * sizeof(double));
    double* V = (double*)malloc(SeqLen * DModel * sizeof(double));
    if (!Q || !K || !V) { free(Q); free(K); free(V); return -1; }

    Ternario_Matmul(X, Wq, Q, SeqLen, DModel, DModel);
    Ternario_Matmul(X, Wk, K, SeqLen, DModel, DModel);
    Ternario_Matmul(X, Wv, V, SeqLen, DModel, DModel);

    /* K^T */
    double* KT = (double*)malloc(DModel * SeqLen * sizeof(double));
    if (!KT) { free(Q); free(K); free(V); return -1; }
    Ternario_Transpose(K, KT, SeqLen, DModel);

    /* Scores = Q @ KT / sqrt(d_model) */
    double* Scores = (double*)malloc(SeqLen * SeqLen * sizeof(double));
    if (!Scores) { free(Q); free(K); free(V); free(KT); return -1; }
    Ternario_Matmul(Q, KT, Scores, SeqLen, DModel, SeqLen);
    double Escala = Ternario_Sqrt((double)DModel);
    for (int I = 0; I < SeqLen * SeqLen; I++) {
        Scores[I] /= Escala;
    }

    /* Pesos = softmax(Scores) */
    double* Pesos = (double*)malloc(SeqLen * SeqLen * sizeof(double));
    if (!Pesos) { free(Q); free(K); free(V); free(KT); free(Scores); return -1; }
    Ternario_Softmax(Scores, Pesos, SeqLen, SeqLen);

    /* Output = Pesos @ V */
    Ternario_Matmul(Pesos, V, Output, SeqLen, SeqLen, DModel);

    /* Copia pesos pra saida se pedido */
    if (PesosOut) {
        memcpy(PesosOut, Pesos, SeqLen * SeqLen * sizeof(double));
    }

    free(Q); free(K); free(V); free(KT); free(Scores); free(Pesos);
    return 0;
}

/* ============================================================
 * INFO (versao)
 * ============================================================ */

const char* Ternario_Versao(void) {
    return "ternario 0.1.0 (C puro, sem BLAS, sem math.h)";
}

int Ternario_Info(void) {
    return 100;
}
