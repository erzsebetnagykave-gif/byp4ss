import sys
import os
import json

BASE_DIR = "/data/data/com.termux/files/home/CyberneticCrown/CC/T0OLS/ByP4ss"
sys.path.insert(0, BASE_DIR)

try:
    from Manifesto import Manifesto, Motor
    PRONTO = True
    ERRO_IMPORT = None
except Exception as e:
    PRONTO = False
    ERRO_IMPORT = f"{type(e).__name__}: {e}"


def Resp(d):
    print(json.dumps(d, default=str), flush=True)


def Main():
    if not PRONTO:
        for linha in sys.stdin:
            Resp({"ok": False, "motivo": "manifesto_import_falhou", "erro": ERRO_IMPORT})
        return
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha:
            continue
        try:
            req = json.loads(linha)
        except Exception as e:
            Resp({"ok": False, "motivo": "json_invalido", "erro": str(e)})
            continue
        op = req.get("op", "")
        try:
            if op == "ping":
                Resp({"pong": True})
            elif op == "listar":
                Resp(Manifesto.Listar())
            elif op == "listar_aplicados":
                Resp(Motor.ListarAplicados())
            elif op == "aplicar":
                Resp(Motor.Aplicar(req.get("id", "")))
            elif op == "reverter":
                Resp(Motor.Reverter(req.get("id", "")))
            elif op == "diff":
                Resp(Motor.Diff(req.get("id", "")))
            elif op == "verificar":
                Resp(Motor.Verificar(req.get("id", "")))
            else:
                Resp({"ok": False, "motivo": "op_desconhecida:" + op})
        except Exception as e:
            Resp({"ok": False, "motivo": "erro:" + type(e).__name__, "erro": str(e)})


if __name__ == "__main__":
    Main()
