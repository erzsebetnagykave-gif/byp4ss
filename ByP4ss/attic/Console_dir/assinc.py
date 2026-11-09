import threading
import time
import uuid


class Tarefa:
    def __init__(self, nome, fn, args=(), kwargs=None):
        self.id = str(uuid.uuid4())[:8]
        self.nome = nome
        self.fn = fn
        self.args = args
        self.kwargs = kwargs or {}
        self.inicio = time.monotonic()
        self.fim = None
        self.resultado = None
        self.erro = None
        self.cancelada = False
        self._cancelar = threading.Event()

    def Cancelar(self):
        self.cancelada = True
        self._cancelar.set()

    def DeveCancelar(self):
        return self._cancelar.is_set()

    def Duracao(self):
        fim = self.fim or time.monotonic()
        return round(fim - self.inicio, 2)

    def Rodar(self):
        try:
            self.resultado = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self.erro = f"{type(e).__name__}: {e}"
        finally:
            self.fim = time.monotonic()


class MotorAsync:
    def __init__(self):
        self.tarefas = {}
        self.lock = threading.Lock()
        self.concluidas = []

    def Executar(self, nome, fn, args=(), kwargs=None, callback=None):
        t = Tarefa(nome, fn, args, kwargs)
        with self.lock:
            self.tarefas[t.id] = t

        def Wrapper():
            t.Rodar()
            with self.lock:
                self.concluidas.append(t.id)
            if callback:
                try:
                    callback(t)
                except Exception:
                    pass

        th = threading.Thread(target=Wrapper, daemon=True)
        th.start()
        return t.id

    def Ativas(self):
        with self.lock:
            return [t for t in self.tarefas.values() if t.fim is None]

    def Total(self):
        with self.lock:
            return len(self.tarefas)

    def EmAndamento(self):
        return len(self.Ativas()) > 0

    def Colher(self, maximo=50):
        with self.lock:
            ids = list(self.concluidas)
            self.concluidas.clear()
        out = []
        for tid in ids[:maximo]:
            t = self.tarefas.get(tid)
            if t:
                out.append(t)
        return out

    def Cancelar(self, tid):
        with self.lock:
            t = self.tarefas.get(tid)
        if t:
            t.Cancelar()
            return True
        return False

    def CancelarTodas(self):
        with self.lock:
            todas = list(self.tarefas.values())
        for t in todas:
            if t.fim is None:
                t.Cancelar()

    def Limpar(self, antes_de_segundos=300):
        agora = time.monotonic()
        with self.lock:
            para_remover = [
                tid for tid, t in self.tarefas.items()
                if t.fim is not None and (agora - t.fim) > antes_de_segundos
            ]
            for tid in para_remover:
                del self.tarefas[tid]
        return len(para_remover)

    def Spinner(self):
        frames = "◐◓◑◒"
        idx = int(time.monotonic() * 8) % len(frames)
        return frames[idx]


Motor = MotorAsync()


def TesteAsync():
    print("=== TESTE MOTOR ASYNC ===\n")

    def Soma(a, b):
        time.sleep(0.5)
        return a + b

    def Falha():
        time.sleep(0.2)
        raise ValueError("erro_intencional")

    def Lenta():
        time.sleep(3)
        return "demorou"

    print("[1] Executar rapido")
    tid = Motor.Executar("soma", Soma, (2, 3))
    print(f"    iniciado id={tid}")
    for _ in range(10):
        if not Motor.EmAndamento():
            break
        print(f"    {Motor.Spinner()} rodando...")
        time.sleep(0.1)
    resultados = Motor.Colher()
    for t in resultados:
        if t.nome == "soma":
            print(f"    [{t.id}] {t.nome}: resultado={t.resultado} duracao={t.Duracao()}s")
    print()

    print("[2] Executar com erro")
    Motor.Executar("falha", Falha)
    for _ in range(10):
        if not Motor.EmAndamento():
            break
        time.sleep(0.1)
    for t in Motor.Colher():
        if t.nome == "falha":
            print(f"    [{t.id}] {t.nome}: erro={t.erro} duracao={t.Duracao()}s")
    print()

    print("[3] Duas em paralelo")
    Motor.Executar("lenta_1", Lenta)
    Motor.Executar("lenta_2", Lenta)
    print(f"    ativas: {len(Motor.Ativas())}")
    time.sleep(0.3)
    print(f"    ativas apos 0.3s: {len(Motor.Ativas())}")
    print("    cancelando todas...")
    Motor.CancelarTodas()
    time.sleep(0.3)
    for t in Motor.Colher():
        if t.nome.startswith("lenta"):
            print(f"    [{t.id}] {t.nome}: cancelada={t.cancelada}")
    print()

    print("[4] Limpeza")
    removidas = Motor.Limpar(antes_de_segundos=0)
    print(f"    removidas: {removidas}")
    print(f"    total restante: {Motor.Total()}")
    print()
    print("TESTE OK")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        TesteAsync()
    else:
        print("uso: python3 async.py teste")
