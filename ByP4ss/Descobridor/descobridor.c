/* descobridor.c — 5 detectores de padrao em sequencias numericas.
 * C puro. Sem dependencia. Saida JSON.
 *
 * Detectores:
 *   linear:      y = a*x + b
 *   quadratico:  y = a*x^2 + b*x + c
 *   exponencial: y = a * b^x
 *   periodico:   y[i] = y[i % P]
 *   recursivo:   y[i] = a*y[i-1] + b*y[i-2]
 *
 * Compila: gcc -O2 -shared -fPIC -o descobridor.so descobridor.c */

#include <stdio.h>
#include <string.h>
#include <math.h>

#define MAX_N 256
#define TOLERANCIA 1e-6

/* ============================================================
 * UTIL
 * ============================================================ */

static int IgualA(double A, double B, double Tol) {
    double D = A - B;
    if (D < 0) D = -D;
    return D <= Tol;
}

/* ============================================================
 * DETECTOR 1: LINEAR (y = a*x + b)
 * ============================================================ */

static int DetectarLinear(const double* Seq, int N, double* A, double* B) {
    if (N < 2) return 0;
    double Diff = Seq[1] - Seq[0];
    for (int I = 2; I < N; I++) {
        double D = Seq[I] - Seq[I - 1];
        if (!IgualA(D, Diff, TOLERANCIA)) return 0;
    }
    *A = Diff;
    *B = Seq[0];
    return 1;
}

/* ============================================================
 * DETECTOR 2: QUADRATICO (y = a*x^2 + b*x + c)
 * Segunda diferenca constante = 2a
 * ============================================================ */

static int DetectarQuadratico(const double* Seq, int N, double* A, double* B, double* C) {
    if (N < 3) return 0;
    double Seg1 = (Seq[2] - Seq[1]) - (Seq[1] - Seq[0]);
    for (int I = 3; I < N; I++) {
        double Seg = (Seq[I] - Seq[I - 1]) - (Seq[I - 1] - Seq[I - 2]);
        if (!IgualA(Seg, Seg1, TOLERANCIA)) return 0;
    }
    *A = Seg1 / 2.0;
    if (IgualA(*A, 0.0, TOLERANCIA)) {
        // nao e quadratico de verdade, e linear
        return 0;
    }
    // c = Seq[0]; resolve b por Seq[1] - c - a
    *C = Seq[0];
    *B = Seq[1] - *A - *C;
    return 1;
}

/* ============================================================
 * DETECTOR 3: EXPONENCIAL (y = a * b^x)
 * Razao constante = b
 * ============================================================ */

static int DetectarExponencial(const double* Seq, int N, double* A, double* B) {
    if (N < 2) return 0;
    if (IgualA(Seq[0], 0.0, TOLERANCIA)) return 0;  // 0 nao pode ser base
    double Razao = Seq[1] / Seq[0];
    if (IgualA(Razao, 0.0, TOLERANCIA)) return 0;
    for (int I = 2; I < N; I++) {
        if (IgualA(Seq[I - 1], 0.0, TOLERANCIA)) return 0;
        double R = Seq[I] / Seq[I - 1];
        if (!IgualA(R, Razao, TOLERANCIA)) return 0;
    }
    *A = Seq[0];
    *B = Razao;
    return 1;
}

/* ============================================================
 * DETECTOR 4: PERIODICO (y[i] = y[i % P])
 * Testa P = 1..N/2
 * ============================================================ */

static int DetectarPeriodico(const double* Seq, int N, int* Periodo) {
    if (N < 4) return 0;
    for (int P = 1; P <= N / 2; P++) {
        int Bate = 1;
        for (int I = P; I < N; I++) {
            if (!IgualA(Seq[I], Seq[I % P], TOLERANCIA)) {
                Bate = 0;
                break;
            }
        }
        if (Bate) {
            *Periodo = P;
            return 1;
        }
    }
    return 0;
}

/* ============================================================
 * DETECTOR 5: RECURSIVO (y[i] = a*y[i-1] + b*y[i-2])
 * Resolve sistema 2x2 por Cramer.
 * ============================================================ */

static int DetectarRecursivo(const double* Seq, int N, double* A, double* B) {
    if (N < 4) return 0;
    // equacoes:
    //   Seq[2] = a*Seq[1] + b*Seq[0]
    //   Seq[3] = a*Seq[2] + b*Seq[1]
    // det = Seq[1]*Seq[1] - Seq[0]*Seq[2]
    double Det = Seq[1] * Seq[1] - Seq[0] * Seq[2];
    if (IgualA(Det, 0.0, TOLERANCIA)) return 0;
    double A_ = (Seq[2] * Seq[1] - Seq[0] * Seq[3]) / Det;
    double B_ = (Seq[1] * Seq[3] - Seq[2] * Seq[2]) / Det;
    // valida em todos os pontos
    for (int I = 4; I < N; I++) {
        double Esperado = A_ * Seq[I - 1] + B_ * Seq[I - 2];
        if (!IgualA(Seq[I], Esperado, TOLERANCIA)) return 0;
    }
    *A = A_;
    *B = B_;
    return 1;
}

/* ============================================================
 * API: Analisar
 * Retorna JSON string na saida.
 * Retorno: 1 se detectou, 0 se nao.
 * ============================================================ */

int Descobridor_Analisar(const double* Seq, int N, char* Saida, int MaxSaida) {
    if (!Seq || !Saida || N < 2) {
        snprintf(Saida, MaxSaida,
            "{\"tipo\":\"invalido\",\"motivo\":\"sequencia_muito_curta\"}");
        return 0;
    }
    Saida[0] = 0;

    /* LINEAR */
    {
        double A, B;
        if (DetectarLinear(Seq, N, &A, &B)) {
            snprintf(Saida, MaxSaida,
                "{\"tipo\":\"linear\",\"coeficientes\":[%.6f,%.6f],"
                "\"erro\":0.0,\"n_pontos\":%d}",
                A, B, N);
            return 1;
        }
    }
    /* QUADRATICO */
    {
        double A, B, C;
        if (DetectarQuadratico(Seq, N, &A, &B, &C)) {
            snprintf(Saida, MaxSaida,
                "{\"tipo\":\"quadratico\",\"coeficientes\":[%.6f,%.6f,%.6f],"
                "\"erro\":0.0,\"n_pontos\":%d}",
                A, B, C, N);
            return 1;
        }
    }
    /* EXPONENCIAL */
    {
        double A, B;
        if (DetectarExponencial(Seq, N, &A, &B)) {
            snprintf(Saida, MaxSaida,
                "{\"tipo\":\"exponencial\",\"coeficientes\":[%.6f,%.6f],"
                "\"erro\":0.0,\"n_pontos\":%d}",
                A, B, N);
            return 1;
        }
    }
    /* PERIODICO */
    {
        int P;
        if (DetectarPeriodico(Seq, N, &P)) {
            snprintf(Saida, MaxSaida,
                "{\"tipo\":\"periodico\",\"periodo\":%d,"
                "\"erro\":0.0,\"n_pontos\":%d}",
                P, N);
            return 1;
        }
    }
    /* RECURSIVO */
    {
        double A, B;
        if (DetectarRecursivo(Seq, N, &A, &B)) {
            snprintf(Saida, MaxSaida,
                "{\"tipo\":\"recursivo\",\"coeficientes\":[%.6f,%.6f],"
                "\"erro\":0.0,\"n_pontos\":%d}",
                A, B, N);
            return 1;
        }
    }

    snprintf(Saida, MaxSaida,
        "{\"tipo\":\"sem_padrao\",\"motivo\":\"nenhum_detector_bateu\","
        "\"n_pontos\":%d}", N);
    return 0;
}

const char* Descobridor_Versao(void) {
    return "descobridor 0.1.0 (5 detectores em C)";
}
