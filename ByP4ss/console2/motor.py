import os
import sys
import json
import time
import threading
import subprocess
import re
import queue

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ideias import Ideias

BASE_DIR = "/data/data/com.termux/files/home/CyberneticCrown/CC/T0OLS/ByP4ss"
RUN_BIN = os.path.join(BASE_DIR, "Paleta", "run")

MAX_HISTORICO = 100
TIMEOUT_PADRAO = 60.0


class Evento:
    def __init__(self, tipo, dados):
        self.tipo = tipo
        self.dados = dados
        self.ts = time.time()


class Tarefa:
    def __init__(self, id_, item, args):
        self.id = id_
        self.item = item
        self.args = args
        self.inicio = time.monotonic()
        self.fim = None
        self.resultado = None
        self.erro = None
        self.processo = None
        self.cancelada = False

    def Duracao(self):
        fim = self.fim or time.monotonic()
        return round(fim - self.inicio, 2)

    def ToDict(self):
        return {
            "id": self.id,
            "comando": self.item.get("comando"),
            "alvo": self.args.get("alvo", ""),
            "duracao": self.Duracao(),
            "ok": self.resultado is not None and self.resultado.get("ok", False),
            "erro": self.erro,
            "cancelada": self.cancelada
        }


class EstadoMotor:
    def __init__(self):
        self.alvo = ""
        self.sessao = ""
        self.modo = "local"
        self.hosts = 0
        self.creds = 0
        self.shells = 0
        self.ultima = ""
        self.ultimo_status = ""
        self.ultimo_tempo = 0.0
        self.tarefas_ativas = 0

    def ToDict(self):
        return {
            "alvo": self.alvo,
            "sessao": self.sessao,
            "modo": self.modo,
            "hosts": self.hosts,
            "creds": self.creds,
            "shells": self.shells,
            "ultima": self.ultima,
            "ultimo_status": self.ultimo_status,
            "ultimo_tempo": self.ultimo_tempo,
            "tarefas_ativas": self.tarefas_ativas
        }


class ArgParser:

    @staticmethod
    def Extrair(query):
        """Extrai key=value da query. Ex: 'scan alvo=192.168.0.1 porta=80'"""
        args = {}
        if not query:
            return args
        tokens = query.split()
        for t in tokens:
            if "=" in t:
                k, v = t.split("=", 1)
                if k and v:
                    args[k.lower()] = v.strip('"').strip("'")
            elif "." in t and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", t):
                args["alvo"] = t
        return args

    @staticmethod
    def MontarQuery(item, args_extra):
        """Monta a query de novo baseado no item e args extraídos."""
        partes = [item.get("id", "")]
        for k, v in args_extra.items():
            partes.append(f"{k}={v}")
        return " ".join(partes)


class FilaTarefas:
    def __init__(self):
        self.fila = queue.Queue()
        self.lock = threading.Lock()
        self.rodando = True

    def Enfileirar(self, tarefa):
        with self.lock:
            self.fila.put(tarefa)

    def Proxima(self):
        try:
            return self.fila.get_nowait()
        except queue.Empty:
            return None

    def Tamanho(self):
        return self.fila.qsize()

    def Parar(self):
        with self.lock:
            self.rodando = False


class Motor:

    def __init__(self, on_evento=None):
        self.estado = EstadoMotor()
        self.on_evento = on_evento
        self.tarefas = {}
        self.historico = []
        self._lock = threading.Lock()
        self._proximo_id = 1
        self._threads = []
        self.fila = FilaTarefas()
        
        # Worker da Fila
        self._worker_thread = threading.Thread(target=self._LoopWorker, daemon=True)
        self._worker_thread.start()
        
        # Observer/Publisher para UI
        self._iniciado = False

    def _AoEvento(self, tipo, dados):
        if self.on_evento:
            try:
                self.on_evento(Evento(tipo, dados))
            except Exception:
                pass

    def _NovoId(self):
        with self._lock:
            i = self._proximo_id
            self._proximo_id += 1
            return f"t_{i}"

    def Executar(self, item, query):
        # 1. Validação baseada na paleta
        info = Ideias.Obter(item.get("id"))
        args_extra = ArgParser.Extrair(query)
        
        if info:
            # Se a ideia exige alvo e o usuário não passou, tenta pegar do estado global
            args_esperados = info.get("args", [])
            if "alvo" in args_esperados and "alvo" not in args_extra:
                if self.estado.alvo:
                    args_extra["alvo"] = self.estado.alvo
                else:
                    return {"ok": False, "motivo": "alvo_ausente", "msg": "Defina um alvo (ex: scan 192.168.0.1)"}

        # 2. Cria tarefa
        tid = self._NovoId()
        tarefa = Tarefa(tid, item, args_extra)
        
        with self._lock:
            self.tarefas[tid] = tarefa
            self.estado.tarefas_ativas += 1
            
        self.fila.Enfileirar(tarefa)
        self._AoEvento("tarefa_criada", tarefa.ToDict())
        
        return {"ok": True, "id": tid}

    def _LoopWorker(self):
        while self.fila.rodando:
            tarefa = self.fila.Proxima()
            if not tarefa:
                time.sleep(0.1)
                continue
            
            if tarefa.cancelada:
                self._FinalizarTarefa(tarefa, {"ok": False, "motivo": "cancelada"})
                continue

            self._ExecutarProcesso(tarefa)

    def _ExecutarProcesso(self, tarefa):
        self._AoEvento("tarefa_iniciada", tarefa.ToDict())
        cmd = tarefa.item.get("comando", "")
        args = tarefa.args.copy()
        if tarefa.item.get("id") and tarefa.item.get("tipo") == "exploit":
            args["exploit_id"] = tarefa.item.get("id")
            
        req = {"op": "executar", "cmd": cmd, "args": args}
        req_json = json.dumps(req)
        
        try:
            proc = subprocess.Popen(
                [RUN_BIN],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            tarefa.processo = proc
            out, err = proc.communicate(input=req_json + "\n", timeout=TIMEOUT_PADRAO)
            
            if err:
                self._AoEvento("log", {"msg": err.strip()})
                
            try:
                res = json.loads(out)
                self._FinalizarTarefa(tarefa, res)
            except json.JSONDecodeError:
                self._FinalizarTarefa(tarefa, {"ok": False, "motivo": "resposta_invalida", "raw": out})
                
        except subprocess.TimeoutExpired:
            proc.kill()
            self._FinalizarTarefa(tarefa, {"ok": False, "motivo": "timeout"})
        except Exception as e:
            self._FinalizarTarefa(tarefa, {"ok": False, "motivo": f"excecao:{type(e).__name__}", "erro": str(e)})

    def _FinalizarTarefa(self, tarefa, resultado):
        tarefa.fim = time.monotonic()
        tarefa.resultado = resultado
        
        with self._lock:
            if self.estado.tarefas_ativas > 0:
                self.estado.tarefas_ativas -= 1
            
            self.estado.ultima = tarefa.item.get("id", "?")
            self.estado.ultimo_tempo = tarefa.Duracao()
            
            if resultado.get("ok"):
                self.estado.ultimo_status = "ok"
            else:
                self.estado.ultimo_status = f"falha:{resultado.get('motivo', '?')}"
            
            # Auto-Discovery
            res_data = resultado.get("resultado") or {}
            cmd_id = tarefa.item.get("id", "")
            tipo = tarefa.item.get("tipo", "")
            if isinstance(res_data, dict):
                tot = res_data.get("total", 0)
                if isinstance(tot, (int, float)):
                    tot = int(tot)
                    if cmd_id == "cred" or "cred" in cmd_id:
                        self.estado.creds += tot
                    elif cmd_id == "scan" or "scan" in cmd_id:
                        self.estado.hosts = max(self.estado.hosts, tot)
                    elif tipo == "ataque" or "exploit" in cmd_id:
                        self.estado.shells += tot
                sessao_nova = res_data.get("sessao")
                if isinstance(sessao_nova, str) and sessao_nova:
                    self.estado.sessao = sessao_nova
                alvo_novo = res_data.get("alvo")
                if isinstance(alvo_novo, str) and alvo_novo:
                    self.estado.alvo = alvo_novo
            # Se exploit ok sem total mas com sessao explicita, conta como 1
            if not resultado.get("ok") is False and tipo == "ataque" and not res_data.get("total"):
                if res_data.get("sessao"):
                    self.estado.shells += 1

            # Histórico
            self.historico.append({
                "ts": time.time(),
                "cmd": tarefa.item.get("id", "?"),
                "args": tarefa.args,
                "ok": resultado.get("ok", False),
                "motivo": resultado.get("motivo", ""),
                "tempo": tarefa.Duracao()
            })
            if len(self.historico) > MAX_HISTORICO:
                self.historico = self.historico[-MAX_HISTORICO:]
                
        self._AoEvento("tarefa_finalizada", tarefa.ToDict())
    def Cancelar(self, tid):
        with self._lock:
            t = self.tarefas.get(tid)
            if not t:
                return {"ok": False, "motivo": "tarefa_nao_encontrada"}
            t.cancelada = True
            if t.processo and t.processo.poll() is None:
                try:
                    t.processo.terminate()
                except Exception:
                    pass
            return {"ok": True, "cancelada": tid}

    def CancelarTudo(self):
        with self._lock:
            ids = list(self.tarefas.keys())
        for tid in ids:
            self.Cancelar(tid)
        return {"ok": True, "total": len(ids)}

    def Ativas(self):
        with self._lock:
            return [t.ToDict() for t in self.tarefas.values() if t.fim is None]

    def Estado(self):
        with self._lock:
            return self.estado.ToDict()

    def EstadoFormatado(self):
        with self._lock:
            e = self.estado
            partes = []
            if e.alvo:
                partes.append(f"alvo={e.alvo}")
            if e.sessao:
                partes.append(f"sessao={e.sessao}")
            partes.append(f"hosts={e.hosts}")
            partes.append(f"creds={e.creds}")
            partes.append(f"shells={e.shells}")
            if e.ultima:
                partes.append(f"ult: {e.ultima} ({e.ultimo_status}, {e.ultimo_tempo}s)")
            if e.tarefas_ativas:
                partes.append(f"ativas={e.tarefas_ativas}")
            return " | ".join(partes)

    def UltimoResultado(self):
        with self._lock:
            if not self.historico:
                return ""
            h = self.historico[-1]
            status = "OK" if h["ok"] else f"FALHA: {h.get('motivo', '?')}"
            return f"{h['cmd']}: {status} ({h['tempo']}s)"

    def Historico(self, n=10):
        with self._lock:
            return list(reversed(self.historico[-n:]))

    def LimparHistorico(self):
        with self._lock:
            self.historico = []
        return {"ok": True}

    def LimparTarefas(self):
        with self._lock:
            self.tarefas = {
                k: v for k, v in self.tarefas.items()
                if v.fim is None
            }
        return {"ok": True}

    def DefinirAlvo(self, alvo):
        with self._lock:
            self.estado.alvo = alvo
        self._AoEvento("alvo_mudou", {"alvo": alvo})

    def DefinirSessao(self, sessao):
        with self._lock:
            self.estado.sessao = sessao
        self._AoEvento("sessao_mudou", {"sessao": sessao})


# ============================================================
# TESTES (mock do binario RUN_BIN)
# ============================================================

class _RunMock:
    """Mock que simula o binario Paleta/run (sem subprocess)."""
    def __init__(self, respostas):
        self.respostas = respostas
        self.chamadas = []
    
    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Use Executar direto no Motor pra testar")


def TesteMotor():
    print("=== TESTE MOTOR ===\n")
    import motor as M

    # Patch: substitui subprocess.Popen por mock
    orig_popen = M.subprocess.Popen

    class FakeProc:
        def __init__(self, cmd, **kw):
            self.returncode = 0
        def communicate(self, input=None, timeout=None):
            # Le o JSON do input, decide a resposta
            try:
                req = json.loads(input.strip())
                cmd = req.get("cmd", "")
                if "scan" in cmd:
                    return (json.dumps({"ok": True, "resultado": {"total": 5, "alvo": "192.168.0.1"}}), "")
                elif "cred" in cmd:
                    return (json.dumps({"ok": True, "resultado": {"total": 10}}), "")
                elif "exploit" in cmd:
                    return (json.dumps({"ok": True, "resultado": {"total": 1, "sessao": "s_001"}}), "")
                else:
                    return (json.dumps({"ok": False, "motivo": "comando_desconhecido"}), "")
            except Exception as e:
                return (json.dumps({"ok": False, "motivo": "input_invalido", "erro": str(e)}), "")
        def terminate(self): self.returncode = -15
        def kill(self): self.returncode = -9
        def poll(self): return self.returncode

    M.subprocess.Popen = FakeProc

    try:
        print("[1] Executar sem alvo (bloqueia)")
        motor = M.Motor()
        r = motor.Executar({"id": "scan", "comando": "scan", "tipo": "reconhecimento"}, "scan")
        assert not r["ok"] or r.get("id"), r
        print(f"    scan sem alvo: {r}")

        print("\n[2] Executar com alvo via query")
        r = motor.Executar({"id": "scan", "comando": "scan", "tipo": "reconhecimento"}, "scan alvo=192.168.0.1")
        assert r["ok"]
        tid = r["id"]
        print(f"    tarefa: {tid}")

        time.sleep(0.3)

        print("\n[3] Estado apos scan")
        estado = motor.Estado()
        print(f"    hosts: {estado['hosts']}, alvo: {estado['alvo']}, ult: {estado['ultima']}")
        assert estado["hosts"] == 5, f"esperado 5, obtido {estado['hosts']}"
        assert estado["alvo"] == "192.168.0.1"

        print("\n[4] Executar cred")
        motor.Executar({"id": "cred", "comando": "cred", "tipo": "acesso"}, "cred alvo=192.168.0.1")
        time.sleep(0.3)
        estado = motor.Estado()
        print(f"    creds: {estado['creds']}")
        assert estado["creds"] == 10

        print("\n[5] EstadoFormatado")
        fmt = motor.EstadoFormatado()
        print(f"    {fmt}")
        assert "alvo=192.168.0.1" in fmt
        assert "hosts=5" in fmt
        assert "creds=10" in fmt

        print("\n[6] UltimoResultado")
        ult = motor.UltimoResultado()
        print(f"    {ult}")
        assert "cred" in ult
        assert "OK" in ult

        print("\n[7] Historico")
        h = motor.Historico(5)
        print(f"    {len(h)} entradas")
        assert len(h) >= 2

        print("\n[8] Ativas (deve estar vazio)")
        ativas = motor.Ativas()
        print(f"    ativas: {len(ativas)}")
        assert len(ativas) == 0

        print("\n[9] Filtrar alvo na query")
        args = M.ArgParser.Extrair("scan alvo=10.0.0.1 porta=80")
        print(f"    {args}")
        assert args["alvo"] == "10.0.0.1"
        assert args["porta"] == "80"

        print("\n[10] ArgParser com IP solto")
        args = M.ArgParser.Extrair("scan 192.168.0.5")
        print(f"    {args}")
        assert args["alvo"] == "192.168.0.5"

        print("\n[11] Cancelar (sem tarefa)")
        r = motor.Cancelar("naoexiste")
        assert not r["ok"]
        print(f"    {r}")

        print("\n[12] LimparHistorico")
        motor.LimparHistorico()
        assert len(motor.Historico(10)) == 0
        print("    ok")

        print("\n[13] DefinirAlvo / DefinirSessao")
        motor.DefinirAlvo("10.0.0.1")
        motor.DefinirSessao("s_999")
        e = motor.Estado()
        assert e["alvo"] == "10.0.0.1"
        assert e["sessao"] == "s_999"
        print(f"    {motor.EstadoFormatado()}")

        print("\n[14] Executar exploit")
        motor.Executar({"id": "tplink", "comando": "exploit", "tipo": "ataque"}, "exploit tplink alvo=10.0.0.1")
        time.sleep(0.3)
        e = motor.Estado()
        print(f"    shells: {e['shells']}")
        assert e["shells"] == 1

        print("\nTESTE OK")
    finally:
        M.subprocess.Popen = orig_popen


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        TesteMotor()
    else:
        print("uso: python3 motor.py teste")
