import re


class Fuzzy:

    RE_ANSI = re.compile(r"\033\[[0-9;]*m")
    COR_MATCH = "\033[1;33m"
    RESET = "\033[0m"

    @staticmethod
    def _Norm(Texto):
        return str(Texto).lower()

    @staticmethod
    def _Iniciais(Texto):
        return "".join(P[0] for P in Texto.split() if P)

    @staticmethod
    def _FuzzyOrdem(Query, Candidato):
        i = 0
        for Ch in Candidato:
            if i < len(Query) and Ch == Query[i]:
                i += 1
        return i == len(Query)

    @staticmethod
    def Pontuar(Query, Candidato):
        if not Query:
            return 50
        Q = Fuzzy._Norm(Query)
        C = Fuzzy._Norm(Candidato)
        if not C:
            return 0
        if Q == C:
            return 100
        if C.startswith(Q):
            Dist = (len(C) - len(Q)) / max(len(C), 1)
            return max(70, int(95 - 30 * Dist))
        if Fuzzy._Iniciais(C).startswith(Q):
            return 75
        Pos = C.find(Q)
        if Pos >= 0:
            Dist = Pos / max(len(C), 1)
            return max(50, int(70 - 20 * Dist))
        if Fuzzy._FuzzyOrdem(Q, C):
            return 40
        return 0

    @staticmethod
    def _Posicoes(Query, Candidato):
        if not Query:
            return []
        Q = Fuzzy._Norm(Query)
        C = Fuzzy._Norm(Candidato)
        Pos = C.find(Q)
        if Pos >= 0:
            return [(Pos, Pos + len(Q))]
        Posicoes = []
        i = 0
        for Idx, Ch in enumerate(C):
            if i < len(Q) and Ch == Q[i]:
                Posicoes.append((Idx, Idx + 1))
                i += 1
        return Posicoes

    @staticmethod
    def Rankear(Query, Lista):
        Resultados = []
        for Item in Lista:
            Texto = Item if isinstance(Item, str) else str(Item)
            Score = Fuzzy.Pontuar(Query, Texto)
            if Score > 0:
                Resultados.append({
                    "item": Item,
                    "texto": Texto,
                    "score": Score,
                    "posicoes": Fuzzy._Posicoes(Query, Texto),
                })
        Resultados.sort(key=lambda X: -X["score"])
        return Resultados

    @staticmethod
    def Completar(Query, Lista, Limite=5):
        if not Query:
            return []
        Q = Fuzzy._Norm(Query)
        Candidatos = []
        for Item in Lista:
            Texto = Item if isinstance(Item, str) else str(Item)
            if Fuzzy._Norm(Texto).startswith(Q):
                Candidatos.append({
                    "item": Item,
                    "texto": Texto,
                    "score": Fuzzy.Pontuar(Query, Texto),
                })
        Candidatos.sort(key=lambda X: -X["score"])
        return Candidatos[:Limite]

    @staticmethod
    def _Mesclar(Posicoes):
        if not Posicoes:
            return []
        Mescladas = [Posicoes[0]]
        for Inicio, Fim in Posicoes[1:]:
            if Mescladas[-1][1] == Inicio:
                Mescladas[-1] = (Mescladas[-1][0], Fim)
            else:
                Mescladas.append((Inicio, Fim))
        return Mescladas

    @staticmethod
    def Highlight(Query, Candidato, Cor=None):
        if not Query or not Candidato:
            return Candidato
        Cor = Cor or Fuzzy.COR_MATCH
        Mescladas = Fuzzy._Mesclar(Fuzzy._Posicoes(Query, Candidato))
        if not Mescladas:
            return Candidato
        Partes = []
        Cursor = 0
        for Inicio, Fim in Mescladas:
            if Inicio > Cursor:
                Partes.append(Candidato[Cursor:Inicio])
            Partes.append(Cor + Candidato[Inicio:Fim] + Fuzzy.RESET)
            Cursor = Fim
        if Cursor < len(Candidato):
            Partes.append(Candidato[Cursor:])
        return "".join(Partes)

    @staticmethod
    def Visivel(Texto):
        return len(Fuzzy.RE_ANSI.sub("", str(Texto)))

    @staticmethod
    def TruncarAnsiSeguro(Texto, Maximo, Marcador="…"):
        Texto = str(Texto)
        if Fuzzy.Visivel(Texto) <= Maximo:
            return Texto
        SemAnsi = Fuzzy.RE_ANSI.sub("", Texto)
        Corte = SemAnsi[: max(0, Maximo - len(Marcador))] + Marcador
        return Corte

    @staticmethod
    def Teste():
        Candidatos = [
            "exploit dlink", "exploit tenda29384", "exploit arcadyan",
            "exploit iptime", "exploit tplink", "exploit tenda7795",
            "scan", "cred", "ssdp", "analise", "cadeia", "fed",
        ]
        R = Fuzzy.Completar("exploit d", Candidatos, 3)
        assert len(R) == 1 and R[0]["texto"] == "exploit dlink", R
        R = Fuzzy.Completar("exploit ", Candidatos, 10)
        assert len(R) == 6, R
        R = Fuzzy.Completar("sc", Candidatos)
        assert len(R) == 1 and R[0]["texto"] == "scan"
        R = Fuzzy.Rankear("edl", Candidatos)
        assert R and R[0]["texto"] == "exploit dlink", R
        R = Fuzzy.Rankear("xyz", Candidatos)
        assert R == [], R
        H = Fuzzy.Highlight("exploit", "exploit dlink")
        assert Fuzzy.Visivel(H) == Fuzzy.Visivel("exploit dlink")
        assert "\033[" in H
        L = Fuzzy.TruncarAnsiSeguro("\033[1;31mtexto colorido bem comprido\033[0m", 10)
        assert Fuzzy.Visivel(L) <= 10
        assert "\033[" in L or L.endswith("…")
        assert Fuzzy.Pontuar("exploit dlink", "exploit dlink") == 100
        assert Fuzzy.Pontuar("expl", "exploit dlink") > 60
        assert Fuzzy.Pontuar("", "qualquer") == 50
        assert Fuzzy.Pontuar("zzz", "abc") == 0
        return True


if __name__ == "__main__":
    Fuzzy.Teste()
    print("Fuzzy.Teste: todos os asserts passaram")
    print("Total de casos: 12")


class FuzzyAvancado:

    _CachePontuar = {}
    _CacheMax = 4096
    _CacheHits = 0
    _CacheMisses = 0

    @staticmethod
    def PontuarCache(Query, Candidato):
        Chave = (Query, Candidato)
        Cache = FuzzyAvancado._CachePontuar
        if Chave in Cache:
            FuzzyAvancado._CacheHits += 1
            return Cache[Chave]
        FuzzyAvancado._CacheMisses += 1
        Score = Fuzzy.Pontuar(Query, Candidato)
        if len(Cache) >= FuzzyAvancado._CacheMax:
            Cache.clear()
        Cache[Chave] = Score
        return Score

    @staticmethod
    def LimparCache():
        FuzzyAvancado._CachePontuar.clear()
        FuzzyAvancado._CacheHits = 0
        FuzzyAvancado._CacheMisses = 0

    @staticmethod
    def CacheInfo():
        Total = FuzzyAvancado._CacheHits + FuzzyAvancado._CacheMisses
        Taxa = (FuzzyAvancado._CacheHits / Total * 100.0) if Total > 0 else 0.0
        return {"tamanho": len(FuzzyAvancado._CachePontuar),
                "hits": FuzzyAvancado._CacheHits,
                "misses": FuzzyAvancado._CacheMisses,
                "taxa_acerto": round(Taxa, 2)}

    @staticmethod
    def Tokenizar(Query):
        if not Query:
            return []
        Partes = []
        Buffer = ""
        for Ch in str(Query):
            if Ch in " \t\n":
                if Buffer:
                    Partes.append(Buffer)
                    Buffer = ""
            else:
                Buffer += Ch
        if Buffer:
            Partes.append(Buffer)
        Tokens = []
        for P in Partes:
            if "=" in P and P.count("=") == 1:
                K, V = P.split("=", 1)
                Tokens.append({"texto": P, "tipo": "kwarg", "chave": K, "valor": V})
            elif ":" in P and P.count(":") == 1:
                K, V = P.split(":", 1)
                Tokens.append({"texto": P, "tipo": "kwarg", "chave": K, "valor": V})
            else:
                Tokens.append({"texto": P, "tipo": "palavra", "chave": None, "valor": P})
        return Tokens

    @staticmethod
    def PontuarMultiToken(Query, Candidato, RequerTodos=True):
        Tokens = FuzzyAvancado.Tokenizar(Query)
        if not Tokens:
            return 50
        Scores = [Fuzzy.Pontuar(T["texto"], Candidato) for T in Tokens]
        if RequerTodos and any(S == 0 for S in Scores):
            return 0
        return int(sum(Scores) / len(Scores))

    @staticmethod
    def RankearMultiToken(Query, Lista, RequerTodos=True):
        Tokens = FuzzyAvancado.Tokenizar(Query)
        Resultados = []
        for Item in Lista:
            Texto = Item if isinstance(Item, str) else str(Item)
            Score = FuzzyAvancado.PontuarMultiToken(Query, Texto, RequerTodos)
            if Score > 0:
                Posicoes = []
                for T in Tokens:
                    Posicoes.extend(Fuzzy._Posicoes(T["texto"], Texto))
                Resultados.append({"item": Item, "texto": Texto, "score": Score,
                                   "posicoes": Fuzzy._Mesclar(Posicoes),
                                   "tokens": [T["texto"] for T in Tokens]})
        Resultados.sort(key=lambda X: -X["score"])
        return Resultados

    @staticmethod
    def PontuarCampos(Item, Query, Campos):
        if not isinstance(Item, dict):
            return Fuzzy.Pontuar(Query, str(Item))
        Total = 0
        PesoTotal = 0
        for Campo, Peso in Campos.items():
            Valor = Item.get(Campo)
            if Valor is None:
                continue
            Total += Fuzzy.Pontuar(Query, str(Valor)) * Peso
            PesoTotal += Peso
        return int(Total / PesoTotal) if PesoTotal else 0

    @staticmethod
    def RankearCampos(Query, Lista, Campos):
        Resultados = []
        ChavePrincipal = next(iter(Campos)) if Campos else None
        for Item in Lista:
            Score = FuzzyAvancado.PontuarCampos(Item, Query, Campos)
            if Score > 0:
                Texto = str(Item.get(ChavePrincipal, "")) if isinstance(Item, dict) else str(Item)
                Resultados.append({"item": Item, "texto": Texto, "score": Score,
                                   "posicoes": Fuzzy._Posicoes(Query, Texto)})
        Resultados.sort(key=lambda X: -X["score"])
        return Resultados

    @staticmethod
    def CalcularBoost(Item, Historico=None, Favoritos=None):
        Boost = 0
        Chave = Item if isinstance(Item, str) else str(Item)
        if Favoritos and Chave in Favoritos:
            Boost += 30
        if Historico:
            Recente = Historico[-20:]
            if Chave in Recente:
                Boost += 20
                Freq = Recente.count(Chave)
                Boost += min((Freq - 1) * 5, 15)
            for I, H in enumerate(reversed(Historico[-10:])):
                if H == Chave:
                    Boost += max(0, 10 - I)
                    break
        return min(Boost, 55)

    @staticmethod
    def RankearComposto(Query, Lista, Historico=None, Favoritos=None, PesoFuzzy=0.7):
        Resultados = []
        for Item in Lista:
            Texto = Item if isinstance(Item, str) else str(Item)
            FS = FuzzyAvancado.PontuarCache(Query, Texto)
            if FS == 0:
                continue
            B = FuzzyAvancado.CalcularBoost(Item, Historico, Favoritos)
            Composto = int(FS * PesoFuzzy + B * (1 - PesoFuzzy))
            Resultados.append({"item": Item, "texto": Texto, "score": FS,
                               "boost": B, "composto": Composto,
                               "posicoes": Fuzzy._Posicoes(Query, Texto)})
        Resultados.sort(key=lambda X: (-X["composto"], -X["score"]))
        return Resultados

    @staticmethod
    def HighlightMultiToken(Query, Candidato, Cor=None):
        if not Query or not Candidato:
            return Candidato
        Cor = Cor or Fuzzy.COR_MATCH
        Tokens = FuzzyAvancado.Tokenizar(Query)
        Posicoes = []
        for T in Tokens:
            Posicoes.extend(Fuzzy._Posicoes(T["texto"], Candidato))
        if not Posicoes:
            return Candidato
        Mescladas = Fuzzy._Mesclar(sorted(Posicoes))
        Partes = []
        Cursor = 0
        for Inicio, Fim in Mescladas:
            if Inicio > Cursor:
                Partes.append(Candidato[Cursor:Inicio])
            Partes.append(Cor + Candidato[Inicio:Fim] + Fuzzy.RESET)
            Cursor = Fim
        if Cursor < len(Candidato):
            Partes.append(Candidato[Cursor:])
        return "".join(Partes)

    @staticmethod
    def _Bigramas(Texto):
        Texto = Fuzzy._Norm(Texto)
        if len(Texto) < 2:
            return set()
        return set(Texto[i:i+2] for i in range(len(Texto) - 1))

    @staticmethod
    def Sugerir(Query, Lista, Limite=3):
        if not Query:
            return []
        Diretos = Fuzzy.Rankear(Query, Lista)
        if Diretos:
            return [{"item": D["item"], "texto": D["texto"], "score": D["score"]}
                    for D in Diretos[:Limite]]
        QueryBigramas = FuzzyAvancado._Bigramas(Query)
        if not QueryBigramas:
            return []
        Sugestoes = []
        for Item in Lista:
            Texto = Item if isinstance(Item, str) else str(Item)
            Bigramas = FuzzyAvancado._Bigramas(Texto)
            if not Bigramas:
                continue
            Intersecao = Bigramas & QueryBigramas
            Similaridade = len(Intersecao) / len(QueryBigramas)
            if Similaridade >= 0.4:
                Sugestoes.append({"item": Item, "texto": Texto,
                                  "score": int(Similaridade * 100)})
        Sugestoes.sort(key=lambda X: -X["score"])
        return Sugestoes[:Limite]

    @staticmethod
    def LimitarPorCategoria(Lista, Chave, MaxPorCategoria=3):
        Contagem = {}
        Resultado = []
        for Item in Lista:
            Cat = Item.get(Chave, "_") if isinstance(Item, dict) else "_"
            if Contagem.get(Cat, 0) >= MaxPorCategoria:
                continue
            Contagem[Cat] = Contagem.get(Cat, 0) + 1
            Resultado.append(Item)
        return Resultado

    @staticmethod
    def RankingEstavel(Lista, Desempate=None):
        if not Desempate:
            return Lista
        return sorted(Lista, key=lambda X: (X.get("score", 0), Desempate(X)), reverse=True)

    @staticmethod
    def Teste():
        FuzzyAvancado.LimparCache()
        assert FuzzyAvancado.CacheInfo()["tamanho"] == 0
        S1 = FuzzyAvancado.PontuarCache("a", "abc")
        S2 = FuzzyAvancado.PontuarCache("a", "abc")
        assert S1 == S2
        Info = FuzzyAvancado.CacheInfo()
        assert Info["hits"] == 1 and Info["misses"] == 1
        T = FuzzyAvancado.Tokenizar("exploit dlink alvo=192.168.0.2")
        assert len(T) == 3
        assert T[0]["tipo"] == "palavra"
        assert T[2]["tipo"] == "kwarg"
        assert T[2]["chave"] == "alvo" and T[2]["valor"] == "192.168.0.2"
        T = FuzzyAvancado.Tokenizar("fed host:porta")
        assert T[1]["tipo"] == "kwarg" and T[1]["chave"] == "host"
        assert FuzzyAvancado.Tokenizar("") == []
        Cands = ["exploit dlink", "exploit tenda", "scan", "cred"]
        R = FuzzyAvancado.RankearMultiToken("exploit tenda", Cands)
        assert R[0]["texto"] == "exploit tenda", R
        assert FuzzyAvancado.RankearMultiToken("exploit xx", Cands) == []
        Item1 = {"nome": "exploit dlink", "descricao": "D-Link RCE", "grupo": "exploits"}
        assert FuzzyAvancado.PontuarCampos(Item1, "dlink", {"nome": 3, "descricao": 1}) > 0
        R = FuzzyAvancado.RankearCampos("dlink", [Item1], {"nome": 3, "descricao": 1})
        assert len(R) == 1
        B1 = FuzzyAvancado.CalcularBoost("scan", ["cred", "scan"], None)
        B2 = FuzzyAvancado.CalcularBoost("scan", ["cred"], None)
        B3 = FuzzyAvancado.CalcularBoost("scan", None, {"scan"})
        assert B1 > B2 and B3 > B2
        assert FuzzyAvancado.CalcularBoost("x", None, {"x"}) == 30
        R = FuzzyAvancado.RankearComposto("scan", ["scan", "scope", "cred"], Historico=["scan"])
        assert R[0]["texto"] == "scan" and R[0]["boost"] > 0
        H = FuzzyAvancado.HighlightMultiToken("scan cred", "scan e cred")
        assert "\033[" in H
        S = FuzzyAvancado.Sugerir("exploitt", ["exploit dlink", "exploit tenda", "scan"])
        assert S and "exploit" in S[0]["texto"]
        Lista = [{"cat": "A", "n": "a1"}, {"cat": "A", "n": "a2"},
                 {"cat": "A", "n": "a3"}, {"cat": "A", "n": "a4"},
                 {"cat": "B", "n": "b1"}]
        L = FuzzyAvancado.LimitarPorCategoria(Lista, "cat", 2)
        assert len(L) == 3
        Es = [{"score": 80, "n": 1}, {"score": 80, "n": 2}, {"score": 90, "n": 3}]
        Est = FuzzyAvancado.RankingEstavel(Es, lambda X: X["n"])
        assert Est[0]["n"] == 3
        assert FuzzyAvancado.CacheInfo()["taxa_acerto"] > 0
        return True


if __name__ == "__main__":
    FuzzyAvancado.Teste()
    print("FuzzyAvancado.Teste: todos os asserts passaram")
    print("Total de casos: 22")
