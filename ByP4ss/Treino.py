# Treino do ByP4ss — Q-Learning pro Agent B4S.
# Le as transicoes do B4SApi (Report/Api.py) e aprende uma QTable.
#
# Contrato:
#   from Treino import QTable, Treinar, Avaliar, MostrarQTable
#   q = QTable()
#   q.Carregar()
#   Treinar(q, episodios=100)
#   acao = q.Escolher(estado, B4SApi.Acoes())
#   q.Salvar()
#
# Formato do estado: vetor de 8 floats (contrato do Report/Dataset.py).
# Discretizacao: cada float arredondado pra 2 casas, virando hash string.
# QTable e dict esparso: cresce so com pares (estado, acao) visitados.

import os
import sys
import json
import math
import random
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from Report.Api import B4SApi
    B4S_DISPONIVEL = True
except Exception:
    B4SApi = None
    B4S_DISPONIVEL = False


def _ConsoleDir():
    return os.path.join(os.path.expanduser("~"), ".console")


def _QTablePath():
    return os.path.join(_ConsoleDir(), "qtable.json")


def _Timestamp():
    return datetime.now(timezone.utc).isoformat()


class QTable:
    """Q-Table esparsa. Estado e vetor de 8 floats, acao e string."""

    def __init__(self, Alpha=0.1, Gamma=0.9, Epsilon=0.1):
        self.Alpha = float(Alpha)
        self.Gamma = float(Gamma)
        self.Epsilon = float(Epsilon)
        self.Dados = {}
        self.Meta = {
            "criado_em": _Timestamp(),
            "total_updates": 0,
            "total_episodios": 0,
        }

    def Hash(self, Estado):
        if Estado is None:
            return "None"
        if isinstance(Estado, (list, tuple)):
            Partes = []
            for X in Estado:
                try:
                    V = round(float(X), 2)
                except (TypeError, ValueError):
                    V = 0.0
                Partes.append(f"{V:.2f}")
            return "|".join(Partes)
        return str(Estado)

    def Obter(self, Estado, Acao):
        H = self.Hash(Estado)
        return float(self.Dados.get(H, {}).get(Acao, 0.0))

    def Atualizar(self, Estado, Acao, Recompensa, ProximoEstado, Done):
        H = self.Hash(Estado)
        HProx = self.Hash(ProximoEstado)
        QAtual = self.Dados.get(H, {}).get(Acao, 0.0)
        if Done:
            QMaxProx = 0.0
        else:
            QMaxProx = max(self.Dados.get(HProx, {}).values(), default=0.0)
        Alvo = Recompensa + self.Gamma * QMaxProx
        QNovo = QAtual + self.Alpha * (Alvo - QAtual)
        self.Dados.setdefault(H, {})[Acao] = float(QNovo)
        self.Meta["total_updates"] += 1
        return QNovo

    def MelhorAcao(self, Estado, Acoes):
        if not Acoes:
            return None
        H = self.Hash(Estado)
        Linha = self.Dados.get(H, {})
        Melhor = None
        MelhorValor = -math.inf
        for A in Acoes:
            V = Linha.get(A, 0.0)
            if V > MelhorValor:
                MelhorValor = V
                Melhor = A
        return Melhor if Melhor is not None else Acoes[0]

    def Escolher(self, Estado, Acoes):
        if not Acoes:
            return None
        if random.random() < self.Epsilon:
            return random.choice(Acoes)
        return self.MelhorAcao(Estado, Acoes)

    def Salvar(self, Caminho=None):
        Caminho = Caminho or _QTablePath()
        try:
            os.makedirs(os.path.dirname(Caminho), mode=0o700, exist_ok=True)
            Payload = {
                "versao": 1,
                "meta": dict(self.Meta),
                "config": {"alpha": self.Alpha, "gamma": self.Gamma,
                           "epsilon": self.Epsilon},
                "dados": self.Dados,
                "salvo_em": _Timestamp(),
            }
            with open(Caminho, "w", encoding="utf-8") as F:
                json.dump(Payload, F, ensure_ascii=False, indent=2)
            try:
                os.chmod(Caminho, 0o600)
            except Exception:
                pass
            return {"ok": True, "caminho": Caminho,
                    "n_pares": self._ContarPares(),
                    "n_estados": len(self.Dados),
                    "tamanho_bytes": os.path.getsize(Caminho)}
        except Exception as E:
            return {"ok": False, "motivo": f"escrita_falhou:{type(E).__name__}",
                    "erro": str(E)}

    def Carregar(self, Caminho=None):
        Caminho = Caminho or _QTablePath()
        if not os.path.isfile(Caminho):
            return {"ok": False, "motivo": "arquivo_nao_encontrado",
                    "caminho": Caminho}
        try:
            with open(Caminho, "r", encoding="utf-8") as F:
                P = json.load(F)
            if not isinstance(P, dict):
                return {"ok": False, "motivo": "formato_invalido"}
            cfg = P.get("config") or {}
            self.Alpha = float(cfg.get("alpha", self.Alpha))
            self.Gamma = float(cfg.get("gamma", self.Gamma))
            self.Epsilon = float(cfg.get("epsilon", self.Epsilon))
            self.Dados = P.get("dados") or {}
            self.Meta = P.get("meta") or self.Meta
            return {"ok": True, "caminho": Caminho,
                    "n_pares": self._ContarPares(),
                    "n_estados": len(self.Dados)}
        except Exception as E:
            return {"ok": False, "motivo": f"leitura_falhou:{type(E).__name__}",
                    "erro": str(E)}

    def Info(self):
        return {
            "alpha": self.Alpha, "gamma": self.Gamma, "epsilon": self.Epsilon,
            "n_estados": len(self.Dados),
            "n_pares": self._ContarPares(),
            "total_updates": self.Meta.get("total_updates", 0),
            "total_episodios": self.Meta.get("total_episodios", 0),
        }

    def _ContarPares(self):
        return sum(len(V) for V in self.Dados.values())


def _TransicoesDoB4S():
    if not B4S_DISPONIVEL or B4SApi is None:
        return []
    try:
        return B4SApi.Transicoes()
    except Exception:
        return []


def Treinar(Q, Episodios=100, Verbose=False, MaxEpisodiosSemNova=20):
    if Q is None:
        return {"ok": False, "motivo": "qtable_none"}
    Transicoes = _TransicoesDoB4S()
    if not Transicoes:
        return {"ok": False, "motivo": "sem_transicoes",
                "aviso": "rode python3 ByP4ss.py <alvo> --all antes"}
    RecompensaTotal = 0.0
    UpdatesTotal = 0
    SemNova = 0
    ParesAntes = Q._ContarPares()
    Inicio = time.monotonic()
    for Ep in range(Episodios):
        RecEp = 0.0
        for (Estado, Acao, R, Proximo, Done) in Transicoes:
            Q.Atualizar(Estado, Acao, R, Proximo, Done)
            RecEp += R
            UpdatesTotal += 1
        RecompensaTotal += RecEp
        Q.Meta["total_episodios"] = Q.Meta.get("total_episodios", 0) + 1
        ParesAgora = Q._ContarPares()
        if ParesAgora == ParesAntes:
            SemNova += 1
        else:
            SemNova = 0
            ParesAntes = ParesAgora
        if Verbose and (Ep + 1) % max(1, Episodios // 10) == 0:
            print(f"  ep {Ep+1}/{Episodios}: rec={RecEp:+.2f} "
                  f"total={RecompensaTotal:+.2f} pares={ParesAgora}")
        if SemNova >= MaxEpisodiosSemNova:
            if Verbose:
                print(f"  convergiu em {Ep+1} episodios (sem novos pares)")
            break
    Duracao = round(time.monotonic() - Inicio, 3)
    return {
        "ok": True,
        "episodios": Q.Meta.get("total_episodios", 0),
        "transicoes_processadas": UpdatesTotal,
        "recompensa_total": round(RecompensaTotal, 4),
        "duracao_s": Duracao,
        "n_pares_final": Q._ContarPares(),
        "n_estados_final": len(Q.Dados),
        "info": Q.Info(),
    }


def Avaliar(Q):
    if Q is None:
        return {"ok": False, "motivo": "qtable_none"}
    Transicoes = _TransicoesDoB4S()
    if not Transicoes:
        return {"ok": False, "motivo": "sem_transicoes"}
    EpsilonOrig = Q.Epsilon
    Q.Epsilon = 0.0
    RecTotal = 0.0
    Escolhas = []
    for (Estado, AcaoTreino, R, Proximo, Done) in Transicoes:
        Acao = Q.MelhorAcao(Estado, B4SApi.Acoes())
        Escolhas.append({"estado_hash": Q.Hash(Estado),
                         "acao_treino": AcaoTreino, "acao_qtable": Acao,
                         "match": Acao == AcaoTreino, "reward": R})
        RecTotal += R
    Q.Epsilon = EpsilonOrig
    Acertos = sum(1 for E in Escolhas if E["match"])
    return {
        "ok": True,
        "transicoes": len(Escolhas),
        "acertos": Acertos,
        "taxa_acerto": round(Acertos / max(1, len(Escolhas)), 3),
        "recompensa_total": round(RecTotal, 4),
        "escolhas": Escolhas,
    }


def MostrarQTable(Q, Top=10):
    if Q is None:
        return {"ok": False, "motivo": "qtable_none"}
    Itens = []
    for H, Linha in Q.Dados.items():
        for Acao, Valor in Linha.items():
            Itens.append({"estado": H, "acao": Acao, "valor": float(Valor)})
    Itens.sort(key=lambda X: -X["valor"])
    Top_ = Itens[:Top]
    print(f"=== QTable ({len(Q.Dados)} estados, {len(Itens)} pares) ===")
    for I, It in enumerate(Top_, 1):
        print(f"  {I:2d}. {It['acao']:25s} q={It['valor']:+.4f}  estado={It['estado'][:40]}")
    if len(Itens) > Top:
        print(f"  ... (+{len(Itens) - Top} pares)")
    return {"ok": True, "n_pares": len(Itens), "top": Top_}


def Main():
    import argparse
    P = argparse.ArgumentParser(prog="Treino",
                                description="Q-Learning do ByP4ss (Agent B4S)")
    Sub = P.add_subparsers(dest="cmd")
    T = Sub.add_parser("treinar", help="treina a qtable")
    T.add_argument("--episodios", type=int, default=100)
    T.add_argument("--verbose", action="store_true")
    T.add_argument("--alpha", type=float, default=0.1)
    T.add_argument("--gamma", type=float, default=0.9)
    T.add_argument("--epsilon", type=float, default=0.1)
    A = Sub.add_parser("avaliar", help="avalia qtable treinada")
    M = Sub.add_parser("mostrar", help="mostra top da qtable")
    M.add_argument("--top", type=int, default=10)
    R = Sub.add_parser("reset", help="apaga qtable")
    Sub.add_parser("teste", help="testa tudo")
    Args = P.parse_args()

    if Args.cmd == "treinar":
        Q = QTable(Alpha=Args.alpha, Gamma=Args.gamma, Epsilon=Args.epsilon)
        Q.Carregar()
        print(f"QTable antes: {Q.Info()}")
        R_ = Treinar(Q, Episodios=Args.episodios, Verbose=Args.verbose)
        print(json.dumps(R_, indent=2, ensure_ascii=False))
        if R_.get("ok"):
            S = Q.Salvar()
            print(f"salvo: {S}")
        return 0 if R_.get("ok") else 1
    if Args.cmd == "avaliar":
        Q = QTable()
        C = Q.Carregar()
        if not C.get("ok"):
            print(f"[erro] {C.get('motivo')} — rode treinar primeiro")
            return 1
        R_ = Avaliar(Q)
        print(json.dumps(R_, indent=2, ensure_ascii=False))
        return 0 if R_.get("ok") else 1
    if Args.cmd == "mostrar":
        Q = QTable()
        C = Q.Carregar()
        if not C.get("ok"):
            print(f"[erro] {C.get('motivo')}")
            return 1
        R_ = MostrarQTable(Q, Top=Args.top)
        return 0 if R_.get("ok") else 1
    if Args.cmd == "reset":
        Caminho = _QTablePath()
        if os.path.isfile(Caminho):
            os.remove(Caminho)
            print(f"[ok] qtable apagada: {Caminho}")
        else:
            print(f"[info] nao existia: {Caminho}")
        return 0
    if Args.cmd == "teste":
        return RodarTeste()
    P.print_help()
    return 2


def RodarTeste():
    print("=== TESTE Treino v1 ===")
    print()

    print("[1] QTable com hash de estado")
    Q = QTable()
    H = Q.Hash([0.1, 0.2, 0.3])
    assert H == "0.10|0.20|0.30", H
    H2 = Q.Hash([1.0, 0.0])
    assert H2 == "1.00|0.00", H2
    print(f"  hash([0.1,0.2,0.3]) = {H}")
    print(f"  hash([1.0,0.0]) = {H2}")

    print()
    print("[2] Obter e Atualizar")
    Q2 = QTable(Alpha=0.5, Gamma=0.9, Epsilon=0.0)
    Est = [1.0, 0.0]
    Q2.Atualizar(Est, "scan", 1.0, [0.0, 0.0], True)
    V = Q2.Obter(Est, "scan")
    assert abs(V - 0.5) < 1e-6, V
    print(f"  q(scan) = {V:.4f} (esperado 0.5)")

    print()
    print("[3] MelhorAcao")
    Q3 = QTable()
    Q3.Dados["0.00|1.00"] = {"scan": 1.0, "cred": 5.0, "upnp": 3.0}
    Est = [0.0, 1.0]
    Melhor = Q3.MelhorAcao(Est, ["scan", "cred", "upnp"])
    assert Melhor == "cred", Melhor
    print(f"  melhor acao = {Melhor}")

    print()
    print("[4] Salvar e Carregar")
    import tempfile
    Tmp = tempfile.mktemp(suffix="_qtable.json")
    Q4 = QTable(Alpha=0.2, Gamma=0.8, Epsilon=0.15)
    Q4.Atualizar([0.5, 0.5], "cred", 10.0, [0.0, 0.0], True)
    S = Q4.Salvar(Tmp)
    assert S["ok"], S
    Q5 = QTable()
    C = Q5.Carregar(Tmp)
    assert C["ok"], C
    assert C["n_pares"] >= 1
    assert abs(Q5.Obter([0.5, 0.5], "cred") - Q4.Obter([0.5, 0.5], "cred")) < 1e-9
    os.remove(Tmp)
    print(f"  salvo e carregado: {C['n_pares']} pares")

    print()
    print("[5] Escolher com epsilon=0 (deterministico)")
    Q6 = QTable(Epsilon=0.0)
    Q6.Dados["1.00|0.00"] = {"scan": 1.0, "cred": 9.0}
    R = Q6.Escolher([1.0, 0.0], ["scan", "cred"])
    assert R == "cred", R
    print(f"  escolheu: {R}")

    print()
    print("[6] Escolher com epsilon=1 (aleatorio)")
    Q7 = QTable(Epsilon=1.0)
    Vistas = set()
    for _ in range(100):
        Vistas.add(Q7.Escolher([1.0, 0.0], ["scan", "cred", "upnp"]))
    assert len(Vistas) >= 2, Vistas
    print(f"  acoes vistas: {sorted(Vistas)}")

    print()
    print("[7] Treinar (com transicoes reais do B4SApi)")
    if not B4S_DISPONIVEL:
        print("  [skip] B4SApi indisponivel")
    else:
        Q8 = QTable()
        R_ = Treinar(Q8, Episodios=10, Verbose=False)
        if R_.get("ok"):
            print(f"  episodios: {R_['episodios']}")
            print(f"  updates: {R_['transicoes_processadas']}")
            print(f"  pares: {R_['n_pares_final']}")
            assert R_["transicoes_processadas"] > 0
        else:
            print(f"  [skip] {R_.get('motivo')}")

    print()
    print("[8] Avaliar")
    if B4S_DISPONIVEL:
        Q9 = QTable()
        Treinar(Q9, Episodios=5)
        R_ = Avaliar(Q9)
        if R_.get("ok"):
            print(f"  transicoes: {R_['transicoes']}")
            print(f"  taxa_acerto: {R_['taxa_acerto']}")

    print()
    print("[9] Info")
    I = Q.Info()
    assert "alpha" in I
    print(f"  {I}")

    print()
    print("TESTE OK")
    return 0


if __name__ == "__main__":
    sys.exit(Main())
