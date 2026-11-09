import json
import os
import time


BASE_DIR = "/data/data/com.termux/files/home/CyberneticCrown/CC/T0OLS/ByP4ss"
SESSOES_DIR = os.path.expanduser("~/.console/sessoes")
CONFIG_DIR = os.path.expanduser("~/.console")
CONFIG_FILE = os.path.join(CONFIG_DIR, "console_config.json")

SALAS = ["recon", "exploits", "sessions", "cadeia",
         "manifesto", "credenciais", "logs", "config"]

DICAS = {
    "recon":       "Enter=scan | s=sub-rede | a=alvo",
    "exploits":    "Enter=executa | l=lista | F5=recon_auto",
    "sessions":    "Enter=carrega | d=deleta | n=nova",
    "cadeia":      "Enter=executa | v=valida | F5=recon_auto",
    "manifesto":   "Enter=aplica | r=reverte | d=diff",
    "credenciais": "Enter=busca alvo | y=carrega YAML",
    "logs":        "Enter=recarrega | c=limpa | f=filtro",
    "config":      "Enter=alterna | s=salva config",
}

CONFIG_PADRAO = {
    "modo":          "local",
    "sessao_auto":   "true",
    "operador":      "false",
    "fantasma":      "false",
    "timeout_run":   "30",
    "federacao":     "",
}


class Estado:

    def __init__(self):
        self.sala = "recon"
        self.indice = 0
        self.alvo = ""
        self.query = ""
        self.status = ""
        self.sessao = ""
        self.historico = []
        self.config = dict(CONFIG_PADRAO)
        self.itens = {}
        self.tarefas_ativas = 0
        self.rodando = True
        self._carregar_config()

    def _carregar_config(self):
        if not os.path.isfile(CONFIG_FILE):
            return
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
            for k in CONFIG_PADRAO:
                if k in dados:
                    self.config[k] = dados[k]
        except Exception:
            pass

    def SalvarConfig(self):
        try:
            os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def AlternarConfig(self, chave):
        if chave not in self.config:
            return None
        v = self.config[chave]
        if v == "true":
            self.config[chave] = "false"
        elif v == "false":
            self.config[chave] = "true"
        return self.config[chave]

    def SalaAtual(self):
        return self.sala

    def IrParaSala(self, nome):
        if nome in SALAS:
            self.sala = nome
            self.indice = 0
            self.status = ""
            return True
        return False

    def ProximaSala(self):
        i = SALAS.index(self.sala)
        self.sala = SALAS[(i + 1) % len(SALAS)]
        self.indice = 0
        self.status = ""

    def SalaAnterior(self):
        i = SALAS.index(self.sala)
        self.sala = SALAS[(i - 1) % len(SALAS)]
        self.indice = 0
        self.status = ""

    def DefinirAlvo(self, alvo):
        self.alvo = alvo
        self.status = "alvo: " + alvo

    def ItensSala(self):
        return self.itens.get(self.sala, [])

    def DefinirItens(self, sala, itens):
        self.itens[sala] = itens
        self.indice = 0

    def Mover(self, delta):
        itens = self.ItensSala()
        if not itens:
            return
        self.indice += delta
        if self.indice < 0:
            self.indice = 0
        if self.indice >= len(itens):
            self.indice = len(itens) - 1

    def ItemAtual(self):
        itens = self.ItensSala()
        if not itens or self.indice < 0 or self.indice >= len(itens):
            return None
        return itens[self.indice]

    def Registrar(self, cmd, ok=True, extra=None):
        self.historico.append({
            "ts":     time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "cmd":    cmd,
            "ok":     bool(ok),
            "extra":  extra or {},
        })
        if len(self.historico) > 500:
            self.historico = self.historico[-500:]

    def Snapshot(self):
        return {
            "sala":       self.sala,
            "alvo":       self.alvo,
            "modo":       self.config.get("modo", "local"),
            "sessao":     self.sessao,
            "historico":  self.historico[-50:],
            "config":     self.config,
            "ts":         time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    def ToDict(self):
        return {
            "sala":          self.sala,
            "indice":        self.indice,
            "alvo":          self.alvo,
            "query":         self.query,
            "status":        self.status,
            "sessao":        self.sessao,
            "modo":          self.config.get("modo", "local"),
            "dica":          DICAS.get(self.sala, ""),
            "itens":         self.ItensSala(),
            "tarefas_ativas": self.tarefas_ativas,
        }


def TesteEstado():
    print("=== TESTE ESTADO ===\n")

    e = Estado()
    print(f"[1] Iniciado: sala={e.sala} alvo='{e.alvo}' config_chaves={len(e.config)}")
    assert e.sala == "recon"

    print("[2] Navegacao")
    e.ProximaSala()
    assert e.sala == "exploits"
    e.ProximaSala()
    assert e.sala == "sessions"
    e.SalaAnterior()
    assert e.sala == "exploits"
    print(f"    após navegar: {e.sala}")
    e.IrParaSala("logs")
    assert e.sala == "logs"
    print(f"    após IrParaSala: {e.sala}")

    print("[3] Alvo")
    e.DefinirAlvo("192.168.0.2")
    assert e.alvo == "192.168.0.2"
    print(f"    alvo: {e.alvo}")

    print("[4] Itens + navegacao")
    e.DefinirItens("logs", [
        {"texto": "evento1", "detalhe": ""},
        {"texto": "evento2", "detalhe": ""},
        {"texto": "evento3", "detalhe": ""},
    ])
    assert len(e.ItensSala()) == 3
    e.Mover(2)
    assert e.indice == 2
    e.Mover(10)
    assert e.indice == 2
    e.Mover(-10)
    assert e.indice == 0
    print(f"    itens=3, indice final={e.indice}, item={e.ItemAtual()['texto']}")

    print("[5] Config alterna")
    antes = e.config["modo"]
    e.AlternarConfig("modo")
    print(f"    modo: {antes} -> {e.config['modo']}")
    e.AlternarConfig("modo")

    print("[6] Salvar config")
    ok = e.SalvarConfig()
    print(f"    salvo: {ok} em {CONFIG_FILE}")
    assert ok
    assert os.path.isfile(CONFIG_FILE)

    print("[7] Historico")
    e.Registrar("cred", True, {"alvo": "192.168.0.2"})
    e.Registrar("exploit dlink", False, {"motivo": "alvo_nao_reconhecido"})
    assert len(e.historico) == 2
    print(f"    historico: {len(e.historico)} eventos")

    print("[8] Snapshot")
    s = e.Snapshot()
    assert "sala" in s and "alvo" in s and "config" in s
    print(f"    snapshot chaves: {list(s.keys())}")

    print("[9] ToDict (para render)")
    d = e.ToDict()
    assert "sala" in d and "itens" in d and "dica" in d
    print(f"    todict chaves: {list(d.keys())}")

    print("\nTESTE OK")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        TesteEstado()
    else:
        print("uso: python3 estado.py teste")
