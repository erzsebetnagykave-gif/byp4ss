import json
import os
import select
import subprocess
import sys


BASE_DIR = "/data/data/com.termux/files/home/CyberneticCrown/CC/T0OLS/ByP4ss"
STATE_BIN = os.path.join(BASE_DIR, "Paleta", "state", "state")
RUN_BIN = os.path.join(BASE_DIR, "Paleta", "run")
MANIFESTO_SERVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manifesto_server.py")


class Cliente:

    def __init__(self, nome, argv, cwd=None):
        self.nome = nome
        self.argv = argv
        self.cwd = cwd or BASE_DIR
        self.proc = None
        self.erro = None
        self.timeout_padrao = 30

    def Abrir(self):
        try:
            self.proc = subprocess.Popen(
                self.argv,
                cwd=self.cwd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                bufsize=1,
                universal_newlines=True,
            )
            return True
        except Exception as e:
            self.erro = f"{type(e).__name__}: {e}"
            self.proc = None
            return False

    def Vivo(self):
        return self.proc is not None and self.proc.poll() is None

    def Chamar(self, req, timeout=None):
        timeout = timeout if timeout is not None else self.timeout_padrao
        if not self.Vivo():
            if not self.Abrir():
                return {"ok": False, "motivo": "cliente_nao_abriu", "erro": self.erro}
        try:
            linha = json.dumps(req, ensure_ascii=False) + "\n"
            self.proc.stdin.write(linha)
            self.proc.stdin.flush()
        except Exception as e:
            return {"ok": False, "motivo": f"escrita_falhou:{type(e).__name__}", "erro": str(e)}
        try:
            r, _, _ = select.select([self.proc.stdout], [], [], timeout)
            if not r:
                return {"ok": False, "motivo": "timeout", "timeout_s": timeout}
            resp = self.proc.stdout.readline()
            if not resp:
                return {"ok": False, "motivo": "resposta_vazia"}
            return json.loads(resp)
        except Exception as e:
            return {"ok": False, "motivo": f"leitura_falhou:{type(e).__name__}", "erro": str(e)}

    def Fechar(self):
        if self.proc and self.proc.poll() is None:
            try:
                self.proc.stdin.close()
            except Exception:
                pass
            try:
                self.proc.terminate()
                self.proc.wait(timeout=2)
            except Exception:
                try:
                    self.proc.kill()
                except Exception:
                    pass
        self.proc = None


class Clientes:

    def __init__(self):
        self.state = Cliente("state", [STATE_BIN])
        self.run = Cliente("run", [RUN_BIN])
        self.manifesto = Cliente("manifesto", [sys.executable, MANIFESTO_SERVER])
        self.manifesto.timeout_padrao = 60

    def Abrir(self):
        return {
            "state":     self.state.Abrir(),
            "run":       self.run.Abrir(),
            "manifesto": self.manifesto.Abrir(),
        }

    def Fechar(self):
        self.state.Fechar()
        self.run.Fechar()
        self.manifesto.Fechar()

    def Ping(self):
        r = {}
        r["state"] = self.state.Chamar({"op": "ping"}, timeout=3).get("pong", False)
        r["run"] = self.run.Chamar({"op": "ping"}, timeout=3).get("pong", False)
        if not r["state"] or not r["run"]:
            r["manifesto"] = False
            return r
        r["manifesto"] = self.manifesto.Chamar({"op": "ping"}, timeout=15).get("pong", False)
        return r

    def PaletaListar(self):
        return self.state.Chamar({"op": "paleta_listar"}, timeout=5)

    def PaletaCarregar(self, nome):
        return self.state.Chamar({"op": "paleta_carregar", "nome": nome}, timeout=20)

    def SessaoListar(self):
        return self.state.Chamar({"op": "sessao_listar"}, timeout=5)

    def SessaoSalvar(self, nome, estado):
        return self.state.Chamar({"op": "sessao_salvar", "nome": nome, "estado": estado}, timeout=5)

    def SessaoCarregar(self, nome):
        return self.state.Chamar({"op": "sessao_carregar", "nome": nome}, timeout=5)

    def AlvoAtual(self):
        return self.state.Chamar({"op": "alvo_atual"}, timeout=3)

    def DefinirAlvo(self, alvo):
        return self.state.Chamar({"op": "alvo_atual", "definir": alvo}, timeout=3)

    def Executar(self, cmd, alvo="", args_extra=None, timeout=120):
        req = {"op": "executar", "cmd": cmd}
        args = {}
        if alvo:
            args["alvo"] = alvo
        if args_extra:
            args.update(args_extra)
        if args:
            req["args"] = args
        return self.run.Chamar(req, timeout=timeout)

    def ManifestoListar(self):
        return self.manifesto.Chamar({"op": "listar"}, timeout=15)

    def ManifestoAplicar(self, id_):
        return self.manifesto.Chamar({"op": "aplicar", "id": id_}, timeout=60)

    def ManifestoReverter(self, id_):
        return self.manifesto.Chamar({"op": "reverter", "id": id_}, timeout=60)

    def ManifestoDiff(self, id_):
        return self.manifesto.Chamar({"op": "diff", "id": id_}, timeout=15)


def TesteClientes():
    print("=== TESTE CLIENTES v2 ===\n")

    c = Clientes()
    print("[1] Abrindo 3 subprocessos...")
    r = c.Abrir()
    for nome, ok in r.items():
        print(f"    {nome}: {'ok' if ok else 'FALHOU'}")

    print("\n[2] Ping (com timeout)")
    p = c.Ping()
    for nome, ok in p.items():
        print(f"    {nome}: {'pong' if ok else 'off/timeout'}")

    print("\n[3] state.paleta_listar")
    r = c.PaletaListar()
    print(f"    ok={r.get('ok')} total={r.get('total')}")

    print("\n[4] state.paleta_carregar comando")
    r = c.PaletaCarregar("comando")
    print(f"    ok={r.get('ok')} total={r.get('total', '?')}")
    if r.get("itens"):
        for it in r["itens"][:3]:
            print(f"      - {it.get('chave')}")

    print("\n[5] run.executar cred alvo=192.168.0.2")
    r = c.Executar("cred", "192.168.0.2")
    print(f"    ok={r.get('ok')} nome={r.get('nome')}")
    if r.get("resultado") and isinstance(r["resultado"], dict):
        rr = r["resultado"]
        creds = rr.get("credenciais", [])
        print(f"    total creds: {len(creds)}")

    print("\n[6] state.alvo_atual (definir + ler)")
    c.DefinirAlvo("192.168.0.2")
    r = c.AlvoAtual()
    print(f"    alvo_atual={r.get('alvo_atual')}")

    print("\n[7] manifesto.listar")
    r = c.ManifestoListar()
    print(f"    ok={r.get('ok')} total={r.get('total', 0)} motivo={r.get('motivo', '')}")

    print("\n[8] Fechando")
    c.Fechar()
    print("    ok")
    print("\nTESTE OK")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        TesteClientes()
    else:
        print("uso: python3 clientes.py teste")
