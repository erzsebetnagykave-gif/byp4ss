import json
import os


TIPOS_ATAQUE = [
    "reconhecimento",
    "acesso",
    "ataque",
    "encadeamento",
    "bypass",
    "lancamento",
]

IDEIAS_VISUAIS = {
    "borda_dupla":       {"nome": "Borda dupla Unicode",        "aplicada": True},
    "borda_simples":     {"nome": "Borda simples",               "aplicada": True},
    "titulo_central":    {"nome": "Titulo centralizado",         "aplicada": True},
    "titulo_invert":     {"nome": "Titulo invertido",            "aplicada": True},
    "ponteiro_pisca":    {"nome": "Ponteiro piscante 500ms",     "aplicada": True},
    "cores_por_sala":    {"nome": "Cores por sala",              "aplicada": True},
    "item_invert":       {"nome": "Item selecionado invertido",  "aplicada": True},
    "scroll_barra":      {"nome": "Barra de scroll lateral",     "aplicada": True},
    "contador":          {"nome": "Contador N/total",            "aplicada": True},
    "breadcrumb":        {"nome": "Breadcrumb no rodape",        "aplicada": True},
    "toast_topo":        {"nome": "Toast 2s no topo",            "aplicada": True},
    "spinner_status":    {"nome": "Spinner 4 frames",            "aplicada": True},
    "destaque_match":    {"nome": "Destaque do match fuzzy",     "aplicada": True},
    "indent_visual":     {"nome": "Indentacao visual",           "aplicada": True},
    "icone_por_tipo":    {"nome": "Icone por tipo",              "aplicada": True},
    "grade_2_colunas":   {"nome": "Grade 2 colunas",             "aplicada": False},
    "linha_dupla":       {"nome": "Linha dupla entre itens",     "aplicada": False},
    "animacao_cursor":   {"nome": "Cursor com fade",             "aplicada": False},
    "barra_progresso":   {"nome": "Barra de progresso",          "aplicada": True},
    "badge_estado":      {"nome": "Badge de estado",             "aplicada": True},
    "tooltip_item":      {"nome": "Tooltip item focado",         "aplicada": True},
    "numeracao":         {"nome": "Numeracao automatica",        "aplicada": True},
    "agrupamento":       {"nome": "Agrupamento por tipo",        "aplicada": True},
    "filtro_tipo":       {"nome": "Filtro por tipo",             "aplicada": True},
    "historico_visual":  {"nome": "Historico visual",            "aplicada": True},
    "modo_compacto":     {"nome": "Modo compacto (1 linha)",     "aplicada": False},
    "modo_expandido":    {"nome": "Modo expandido (3 linhas)",   "aplicada": True},
    "cor_alerta":        {"nome": "Cor de alerta",               "aplicada": True},
    "cor_ok":            {"nome": "Cor de OK",                   "aplicada": True},
    "cor_falha":         {"nome": "Cor de falha",                "aplicada": True},
    "cor_info":          {"nome": "Cor de info",                 "aplicada": True},
    "cor_disabled":      {"nome": "Cor de desativado",           "aplicada": True},
    "cor_hover":         {"nome": "Cor de hover",                "aplicada": True},
    "highlight_match":   {"nome": "Highlight do match",          "aplicada": True},
    "query_limpa_x":     {"nome": "Botao limpar query",          "aplicada": False},
    "cache_indicador":   {"nome": "Indicador de cache",          "aplicada": True},
    "sync_indicador":    {"nome": "Indicador de sync",           "aplicada": True},
    "latencia_item":     {"nome": "Latencia por item",           "aplicada": True},
    "origem_item":       {"nome": "Origem do item",              "aplicada": True},
    "autor_item":        {"nome": "Autor do item",               "aplicada": False},
    "versao_item":       {"nome": "Versao do item",              "aplicada": False},
    "confianca_item":    {"nome": "Confianca do item",           "aplicada": True},
    "prioridade_item":   {"nome": "Prioridade do item",          "aplicada": True},
    "categoria_item":    {"nome": "Categoria do item",           "aplicada": True},
    "dica_rodape":       {"nome": "Dica contextual rodape",      "aplicada": True},
    "atalhos_rodape":    {"nome": "Atalhos no rodape",           "aplicada": True},
}


IDEIAS_ATAQUE = {
    "scan": {
        "nome": "Scan de rede",
        "tipo": "reconhecimento",
        "comando": "scan",
        "args": ["alvo"],
        "descricao": "Port scan + SSDP num alvo",
    },
    "analise": {
        "nome": "Analise consolidada",
        "tipo": "reconhecimento",
        "comando": "analise",
        "args": ["alvo"],
        "descricao": "Portas, servicos, fabricante, CVEs",
    },
    "ssdp": {
        "nome": "SSDP discovery",
        "tipo": "reconhecimento",
        "comando": "ssdp",
        "args": ["alvo"],
        "descricao": "Descobre UPnP via M-SEARCH",
    },
    "cred": {
        "nome": "Buscar credenciais",
        "tipo": "acesso",
        "comando": "cred",
        "args": ["alvo"],
        "descricao": "Credenciais do YAML + K1ELI",
    },
    "shell_rev": {
        "nome": "Reverse shell",
        "tipo": "acesso",
        "comando": "shell",
        "args": ["reverse", "local", "porta"],
        "descricao": "Reverse shell em 7 protocolos",
    },
    "shell_bind": {
        "nome": "Bind shell",
        "tipo": "acesso",
        "comando": "shell",
        "args": ["bind", "porta"],
        "descricao": "Bind shell em 4 protocolos",
    },
    "exploit": {
        "nome": "Executar exploit",
        "tipo": "ataque",
        "comando": "exploit",
        "args": ["id", "alvo"],
        "descricao": "Um dos 6 CVEs do Engine",
    },
    "tenda_ovfl": {
        "nome": "Tenda overflow",
        "tipo": "ataque",
        "comando": "exploit",
        "args": ["tenda29384", "alvo"],
        "descricao": "Stack overflow MIPS",
    },
    "dlink_basico": {
        "nome": "Chain D-Link basico",
        "tipo": "ataque",
        "comando": "cadeia",
        "args": ["dlink_basico", "alvo"],
        "descricao": "Auth bypass + reverse",
    },
    "recon_auto": {
        "nome": "Recon automatico",
        "tipo": "encadeamento",
        "comando": "cadeia",
        "args": ["recon_auto", "alvo"],
        "descricao": "Analise + exploit auto",
    },
    "cadeia": {
        "nome": "Kill chain",
        "tipo": "encadeamento",
        "comando": "cadeia",
        "args": ["nome", "alvo"],
        "descricao": "Executa cadeia de templates",
    },
    "upnp": {
        "nome": "UPnP bypass",
        "tipo": "bypass",
        "comando": "upnp",
        "args": ["alvo", "porta"],
        "descricao": "AddPortMapping no firewall",
    },
    "httpauth": {
        "nome": "Path traversal auth",
        "tipo": "bypass",
        "comando": "httpauth",
        "args": ["alvo", "caminho"],
        "descricao": "Traversal no /admin",
    },
    "servidor_http": {
        "nome": "Servidor HTTP falso",
        "tipo": "lancamento",
        "comando": "servidor",
        "args": ["http", "porta"],
        "descricao": "Sobe HTTP falso local",
    },
    "servidor_ssdp": {
        "nome": "Servidor SSDP falso",
        "tipo": "lancamento",
        "comando": "servidor",
        "args": ["ssdp", "porta"],
        "descricao": "Sobe SSDP falso local",
    },
}


class Ideias:

    @staticmethod
    def Visual():
        return dict(IDEIAS_VISUAIS)

    @staticmethod
    def Ataque():
        return dict(IDEIAS_ATAQUE)

    @staticmethod
    def TiposAtaque():
        return list(TIPOS_ATAQUE)

    @staticmethod
    def ListarPorTipo(tipo):
        return {
            k: v for k, v in IDEIAS_ATAQUE.items()
            if v.get("tipo") == tipo
        }

    @staticmethod
    def Obter(id_):
        return IDEIAS_ATAQUE.get(id_)

    @staticmethod
    def Buscar(query):
        q = query.lower().strip()
        if not q:
            return list(IDEIAS_ATAQUE.items())
        out = []
        for k, v in IDEIAS_ATAQUE.items():
            texto = (k + " " + v.get("nome", "") + " " + v.get("descricao", "") + " " + v.get("tipo", "")).lower()
            if q in texto:
                out.append((k, v))
        return out

    @staticmethod
    def VisualAplicadas():
        return {k: v for k, v in IDEIAS_VISUAIS.items() if v.get("aplicada")}

    @staticmethod
    def VisualPendentes():
        return {k: v for k, v in IDEIAS_VISUAIS.items() if not v.get("aplicada")}

    @staticmethod
    def ValidarArgs(id_, args_dados):
        info = IDEIAS_ATAQUE.get(id_)
        if not info:
            return {"ok": False, "motivo": f"ideia_desconhecida:{id_}"}
        esperados = info.get("args", [])
        faltando = [a for a in esperados if a not in args_dados]
        if faltando:
            return {"ok": False, "motivo": "args_faltando", "faltando": faltando}
        return {"ok": True, "comando": info["comando"], "args": esperados}

    @staticmethod
    def ToDict():
        return {
            "tipos": TIPOS_ATAQUE,
            "visuais_total": len(IDEIAS_VISUAIS),
            "visuais_aplicadas": len([v for v in IDEIAS_VISUAIS.values() if v["aplicada"]]),
            "visuais_pendentes": len([v for v in IDEIAS_VISUAIS.values() if not v["aplicada"]]),
            "ataques_total": len(IDEIAS_ATAQUE),
        }


def TesteIdeias():
    print("=== TESTE IDEIAS ===\n")

    print("[1] Visuais")
    v = Ideias.Visual()
    assert len(v) == 45, f"esperado 45, obtido {len(v)}"
    aplicadas = Ideias.VisualAplicadas()
    pendentes = Ideias.VisualPendentes()
    print(f"    total: {len(v)}")
    print(f"    aplicadas: {len(aplicadas)}")
    print(f"    pendentes: {len(pendentes)}")
    assert len(aplicadas) + len(pendentes) == 45

    print("\n[2] Ataques")
    a = Ideias.Ataque()
    assert len(a) == 15, f"esperado 15, obtido {len(a)}"
    print(f"    total: {len(a)}")
    por_tipo = {}
    for k, info in a.items():
        t = info.get("tipo")
        por_tipo[t] = por_tipo.get(t, 0) + 1
    for t in TIPOS_ATAQUE:
        print(f"    {t}: {por_tipo.get(t, 0)}")

    print("\n[3] Buscar")
    r = Ideias.Buscar("scan")
    assert len(r) >= 1
    print(f"    'scan': {len(r)} resultados")
    r = Ideias.Buscar("shell")
    print(f"    'shell': {len(r)} resultados")
    r = Ideias.Buscar("")
    assert len(r) == 15
    print(f"    '': {len(r)} resultados (todos)")

    print("\n[4] ListarPorTipo")
    for t in TIPOS_ATAQUE:
        lista = Ideias.ListarPorTipo(t)
        print(f"    {t}: {len(lista)}")

    print("\n[5] ValidarArgs")
    v1 = Ideias.ValidarArgs("scan", {"alvo": "192.168.0.1"})
    assert v1["ok"]
    print(f"    scan + alvo: ok")
    v2 = Ideias.ValidarArgs("scan", {})
    assert not v2["ok"]
    print(f"    scan sem alvo: {v2['motivo']} (faltando: {v2['faltando']})")
    v3 = Ideias.ValidarArgs("inexistente", {})
    assert not v3["ok"]
    print(f"    inexistente: {v3['motivo']}")

    print("\n[6] ToDict")
    d = Ideias.ToDict()
    print(f"    {json.dumps(d, ensure_ascii=False, indent=2)}")

    print("\nTESTE OK")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        TesteIdeias()
    else:
        print("uso: python3 ideias.py teste")
