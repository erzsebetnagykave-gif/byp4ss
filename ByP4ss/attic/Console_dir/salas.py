import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assinc import Motor


def Resultado(texto, detalhe="", ativo=True, dados=None):
    return {"texto": texto, "detalhe": detalhe, "ativo": ativo, "dados": dados or {}}


def ExtrairCredenciais(resp):
    out = []
    if not isinstance(resp, dict):
        return out
    r = resp.get("resultado") or {}
    if not isinstance(r, dict):
        return out
    for c in r.get("credenciais") or []:
        if isinstance(c, dict):
            u = c.get("user", "")
            p = c.get("pass", "")
            if u:
                out.append(Resultado(f"{u} : {p}", "", True, c))
    return out


def ExtrairSessoes(resp):
    out = []
    if not isinstance(resp, dict) or not resp.get("ok"):
        return out
    for s in resp.get("sessoes") or []:
        if isinstance(s, dict):
            nome = s.get("nome", "")
            idade = s.get("idade_s", 0)
            tam = s.get("tamanho", 0)
            out.append(Resultado(nome, f"{tam}b, {idade}s", True, s))
    return out


def ExtrairManifestos(resp):
    out = []
    if not isinstance(resp, dict) or not resp.get("ok"):
        return out
    for m in resp.get("manifestos") or []:
        if isinstance(m, dict):
            nome = m.get("id", "")
            desc = m.get("descricao", "")
            out.append(Resultado(nome, desc, True, m))
    return out


def Resumo(resp):
    if not isinstance(resp, dict):
        return "resposta invalida"
    if resp.get("ok"):
        r = resp.get("resultado") or {}
        tot = r.get("total") if isinstance(r, dict) else None
        if tot:
            return f"OK total={tot}"
        return "OK"
    m = resp.get("motivo") or resp.get("erro") or "falha"
    return "FALHA: " + str(m)[:60]


class SalaBase:
    nome = "base"
    dica = ""

    def __init__(self):
        self.itens = []
        self.callback = None

    def Entrar(self, estado, clientes, callback):
        self.callback = callback
        self.itens = []
        callback(self.nome, [])

    def Enter(self, estado, clientes, item):
        return None

    def TeclaExtra(self, estado, clientes, tecla, callback):
        return False

    def Entregar(self, itens):
        self.itens = itens
        if self.callback:
            self.callback(self.nome, itens)


class SalaRecon(SalaBase):
    nome = "recon"
    dica = "Enter=scan | a=alvo"

    def Entrar(self, estado, clientes, callback):
        self.callback = callback
        if not estado.alvo:
            callback(self.nome, [Resultado("(defina alvo: a)", "", False)])
            return
        callback(self.nome, [Resultado("escaneando " + estado.alvo + "...", "", False)])
        Motor.Executar(
            "recon-scan",
            lambda: clientes.Executar("analise", estado.alvo, timeout=60),
            callback=lambda t: self._AoTerminar(t, estado),
        )

    def _AoTerminar(self, tarefa, estado):
        if tarefa.erro:
            self.Entregar([Resultado("erro: " + tarefa.erro, "", False)])
            return
        resp = tarefa.resultado or {}
        host = estado.alvo
        portas = []
        fab = ""
        if isinstance(resp, dict) and resp.get("ok"):
            r = resp.get("resultado") or {}
            if isinstance(r, dict):
                portas = r.get("portas_abertas") or []
                fab = r.get("fabricante") or ""
        itens = [Resultado(host, f"{fab} [{','.join(str(p) for p in portas)}]", True)]
        self.Entregar(itens)

    def Enter(self, estado, clientes, item):
        if not estado.alvo:
            estado.status = "defina alvo primeiro (a)"
            return
        self.Entrar(estado, clientes, self.callback)

    def TeclaExtra(self, estado, clientes, tecla, callback):
        if tecla == "a":
            estado.status = "alvo atual: " + (estado.alvo or "(vazio)")
            return True
        return False


class SalaExploits(SalaBase):
    nome = "exploits"
    dica = "Enter=executa | l=lista"

    def Entrar(self, estado, clientes, callback):
        self.callback = callback
        self.itens = [
            Resultado("exploit tplink", "CVE-2023-1389", True),
            Resultado("exploit dlink", "CVE-2024-3273", True),
            Resultado("exploit tenda7795", "CVE-2025-7795", True),
            Resultado("exploit arcadyan", "CVE-2021-20090", True),
            Resultado("exploit iptime", "CVE-2025-55423", True),
            Resultado("exploit tenda29384", "CVE-2025-29384", True),
        ]
        callback(self.nome, self.itens)

    def Enter(self, estado, clientes, item):
        if not item:
            return
        cmd = item["texto"]
        if not estado.alvo:
            estado.status = "defina alvo primeiro (recon)"
            return
        estado.status = "executando " + cmd + "..."
        Motor.Executar(
            "exploit",
            lambda: clientes.Executar(cmd, estado.alvo, timeout=300),
            callback=lambda t: self._AoTerminar(t, estado),
        )

    def _AoTerminar(self, tarefa, estado):
        if tarefa.erro:
            estado.status = "erro: " + tarefa.erro
            return
        estado.status = Resumo(tarefa.resultado)


class SalaSessions(SalaBase):
    nome = "sessions"
    dica = "Enter=seleciona | n=nova"

    def Entrar(self, estado, clientes, callback):
        self.callback = callback
        Motor.Executar(
            "sessions-list",
            lambda: clientes.SessaoListar(),
            callback=self._AoTerminar,
        )

    def _AoTerminar(self, tarefa):
        itens = ExtrairSessoes(tarefa.resultado)
        if not itens:
            itens = [Resultado("(sem sessoes)", "", False)]
        self.Entregar(itens)

    def Enter(self, estado, clientes, item):
        if item and item["ativo"]:
            estado.sessao = item["texto"]
            estado.status = "sessao: " + estado.sessao

    def TeclaExtra(self, estado, clientes, tecla, callback):
        if tecla == "n":
            estado.sessao = ""
            estado.status = "nova sessao"
            return True
        return False


class SalaCadeia(SalaBase):
    nome = "cadeia"
    dica = "Enter=executa | v=valida"

    def Entrar(self, estado, clientes, callback):
        self.callback = callback
        Motor.Executar(
            "cadeia-templates",
            lambda: carregar_templates(),
            callback=self._AoTerminar,
        )

    def _AoTerminar(self, tarefa):
        if tarefa.erro:
            self.Entregar([Resultado("erro: " + tarefa.erro, "", False)])
            return
        self.Entregar(tarefa.resultado or [])

    def Enter(self, estado, clientes, item):
        if not item:
            return
        if not estado.alvo:
            estado.status = "defina alvo primeiro"
            return
        estado.status = "executando cadeia " + item["texto"] + "..."
        Motor.Executar(
            "cadeia-run",
            lambda: clientes.Executar("cadeia", estado.alvo, timeout=600),
            callback=lambda t: self._AoTerminarRun(t, estado),
        )

    def _AoTerminarRun(self, tarefa, estado):
        if tarefa.erro:
            estado.status = "erro: " + tarefa.erro
            return
        estado.status = Resumo(tarefa.resultado)


def carregar_templates():
    import subprocess
    import json
    BASE_DIR = "/data/data/com.termux/files/home/CyberneticCrown/CC/T0OLS/ByP4ss"
    py = (
        "import sys, json;"
        "sys.path.insert(0, '" + BASE_DIR + "');"
        "from Cadeia import Cadeia;"
        "r = Cadeia.Templates();"
        "print(json.dumps([{'nome': t['nome'], 'descricao': t.get('descricao','')} "
        "for t in r.get('templates', [])]))"
    )
    try:
        out = subprocess.check_output([sys.executable, "-c", py], cwd=BASE_DIR, timeout=15)
        dados = json.loads(out.decode("utf-8", "replace"))
        return [Resultado(t["nome"], t["descricao"], True) for t in dados]
    except Exception as e:
        return [Resultado("erro templates", str(e), False)]


class SalaManifesto(SalaBase):
    nome = "manifesto"
    dica = "Enter=aplica | r=reverte"

    def Entrar(self, estado, clientes, callback):
        self.callback = callback
        Motor.Executar(
            "manifesto-list",
            lambda: clientes.ManifestoListar(),
            callback=self._AoTerminar,
        )

    def _AoTerminar(self, tarefa):
        itens = ExtrairManifestos(tarefa.resultado)
        if not itens:
            itens = [Resultado("(sem manifestos)", "", False)]
        self.Entregar(itens)

    def Enter(self, estado, clientes, item):
        if not item:
            return
        nome = item["texto"]
        estado.status = "aplicando " + nome + "..."
        Motor.Executar(
            "manifesto-apply",
            lambda: clientes.ManifestoAplicar(nome),
            callback=lambda t: self._AoT(t, estado, "aplicar"),
        )

    def _AoT(self, tarefa, estado, acao):
        if tarefa.erro:
            estado.status = "erro " + acao + ": " + tarefa.erro
            return
        estado.status = acao + ": " + Resumo(tarefa.resultado)

    def TeclaExtra(self, estado, clientes, tecla, callback):
        if tecla == "r" and self.itens and estado.indice < len(self.itens):
            item = self.itens[estado.indice]
            if item["ativo"]:
                Motor.Executar(
                    "manifesto-revert",
                    lambda: clientes.ManifestoReverter(item["texto"]),
                    callback=lambda t: self._AoT(t, estado, "reverter"),
                )
                return True
        return False


class SalaCredenciais(SalaBase):
    nome = "credenciais"
    dica = "Enter=busca alvo"

    def Entrar(self, estado, clientes, callback):
        self.callback = callback
        if not estado.alvo:
            callback(self.nome, [Resultado("(defina alvo na recon)", "", False)])
            return
        Motor.Executar(
            "cred-busca",
            lambda: clientes.Executar("cred", estado.alvo, timeout=60),
            callback=self._AoTerminar,
        )

    def _AoTerminar(self, tarefa):
        itens = ExtrairCredenciais(tarefa.resultado)
        if not itens:
            itens = [Resultado("(nenhuma credencial)", "", False)]
        self.Entregar(itens)

    def Enter(self, estado, clientes, item):
        if item and item["ativo"]:
            estado.status = "cred: " + item["texto"]


class SalaLogs(SalaBase):
    nome = "logs"
    dica = "Enter=recarrega | c=limpa"

    def Entrar(self, estado, clientes, callback):
        self.callback = callback
        itens = carregar_logs()
        callback(self.nome, itens)

    def Enter(self, estado, clientes, item):
        if item:
            estado.status = item["texto"][:100]

    def TeclaExtra(self, estado, clientes, tecla, callback):
        if tecla == "c":
            self.Entregar([])
            estado.status = "logs limpos"
            return True
        return False


def carregar_logs():
    BASE_DIR = "/data/data/com.termux/files/home/CyberneticCrown/CC/T0OLS/ByP4ss"
    dir_logs = os.path.join(BASE_DIR, "logs")
    if not os.path.isdir(dir_logs):
        return [Resultado("(sem logs)", "", False)]
    arquivos = sorted(
        os.path.join(dir_logs, f) for f in os.listdir(dir_logs)
        if f.endswith(".jsonl")
    )
    if not arquivos:
        return [Resultado("(sem logs)", "", False)]
    try:
        with open(arquivos[-1], "r", encoding="utf-8") as f:
            linhas = f.readlines()[-100:]
        return [Resultado(l.strip()[:200], "", True) for l in linhas if l.strip()]
    except Exception as e:
        return [Resultado("erro logs", str(e), False)]


class SalaConfig(SalaBase):
    nome = "config"
    dica = "Enter=alterna | s=salva"

    def Entrar(self, estado, clientes, callback):
        self.callback = callback
        self.atualizar(estado)

    def atualizar(self, estado):
        itens = []
        for k in ["modo", "sessao_auto", "operador", "fantasma", "timeout_run", "federacao"]:
            v = estado.config.get(k, "")
            itens.append(Resultado(k, v, True, {"chave": k}))
        if self.callback:
            self.callback(self.nome, itens)

    def Enter(self, estado, clientes, item):
        if not item:
            return
        chave = item["dados"].get("chave", "")
        if chave:
            novo = estado.AlternarConfig(chave)
            if novo is not None:
                estado.status = f"{chave} = {novo}"
                self.atualizar(estado)

    def TeclaExtra(self, estado, clientes, tecla, callback):
        if tecla == "s":
            ok = estado.SalvarConfig()
            estado.status = "config salva" if ok else "erro ao salvar"
            return True
        return False


SALAS = {
    "recon":       SalaRecon(),
    "exploits":    SalaExploits(),
    "sessions":    SalaSessions(),
    "cadeia":      SalaCadeia(),
    "manifesto":   SalaManifesto(),
    "credenciais": SalaCredenciais(),
    "logs":        SalaLogs(),
    "config":      SalaConfig(),
}


def TesteSalas():
    print("=== TESTE SALAS ===\n")
    for nome, sala in SALAS.items():
        print(f"  {nome}: dica='{sala.dica}'")
    print(f"\n  total: {len(SALAS)}")
    print("TESTE OK")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        TesteSalas()
    else:
        print("uso: python3 salas.py teste")
