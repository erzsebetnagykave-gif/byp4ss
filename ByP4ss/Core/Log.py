# Log do ByP4ss
# Log local (nao depende do Kirja)

import os
import sys
import time
import json
from datetime import datetime

from Core.Constants import Constants
from Core.Config import Config


class Log:

    _Iniciado = False
    _Arquivo = None
    _Buffer = []
    _Contadores = {}
    _Inicio = 0.0

    @staticmethod
    def Iniciar(Cfg=None):
        Log._Iniciado = True
        Log._Inicio = time.time()
        Log._Buffer = []
        Log._Contadores = {
            "debug": 0, "info": 0, "aviso": 0, "erro": 0, "critico": 0,
        }

        if Cfg is not None and getattr(Cfg, "Salvar", True):
            try:
                os.makedirs(Cfg.DirLogs, exist_ok=True)
                Caminho = os.path.join(Cfg.DirLogs, Constants.ARQ_LOG)
                Log._Arquivo = open(Caminho, "a", encoding="utf-8")
            except OSError:
                Log._Arquivo = None

        Log.Debug("log iniciado", {"versao": Constants.VERSAO})

    @staticmethod
    def Finalizar():
        if Log._Arquivo is not None:
            try:
                Log._Arquivo.close()
            except OSError:
                pass
            Log._Arquivo = None
        Log._Iniciado = False

    @staticmethod
    def _Timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    @staticmethod
    def _Decorrido():
        if Log._Inicio == 0.0:
            return 0.0
        return time.time() - Log._Inicio

    @staticmethod
    def _NivelCor(Nivel):
        Cores = {
            "debug": 244, "info": 39, "aviso": 220,
            "erro": 196, "critico": 196,
        }
        return Cores.get(Nivel, 39)

    @staticmethod
    def _Prefixo(Nivel):
        Prefixos = {
            "debug": "[dbg]", "info": "[inf]", "aviso": "[wrn]",
            "erro": "[err]", "critico": "[CRT]",
        }
        return Prefixos.get(Nivel, "[???]")

    @staticmethod
    def _Console(Nivel, Mensagem, Extra):
        Cor = Log._NivelCor(Nivel)
        Prefixo = Log._Prefixo(Nivel)
        Decorrido = Log._Decorrido()
        Ts = Log._Timestamp()
        Linha = f"\033[38;5;{Cor}m{Prefixo}\033[0m {Ts} +{Decorrido:.3f}s {Mensagem}"
        if Extra:
            Linha += " " + json.dumps(Extra, ensure_ascii=False, default=str)
        try:
            sys.stderr.write(Linha + "\n")
            sys.stderr.flush()
        except OSError:
            pass

    @staticmethod
    def _Persistir(Nivel, Mensagem, Extra):
        if Log._Arquivo is None:
            return
        Registro = {
            "ts": Log._Timestamp(),
            "decorrido": round(Log._Decorrido(), 3),
            "nivel": Nivel,
            "msg": Mensagem,
        }
        if Extra:
            Registro["extra"] = Extra
        try:
            Log._Arquivo.write(json.dumps(Registro, ensure_ascii=False, default=str) + "\n")
            Log._Arquivo.flush()
        except OSError:
            pass

    @staticmethod
    def _BufferAdd(Nivel, Mensagem, Extra):
        Log._Buffer.append({
            "ts": Log._Timestamp(),
            "decorrido": round(Log._Decorrido(), 3),
            "nivel": Nivel,
            "msg": Mensagem,
            "extra": Extra or {},
        })
        if len(Log._Buffer) > 5000:
            Log._Buffer = Log._Buffer[-5000:]

    @staticmethod
    def Debug(Mensagem, Extra=None):
        if not Log._Iniciado:
            return
        Log._Contadores["debug"] += 1
        if Config.Verbose:
            Log._Console("debug", Mensagem, Extra)
        Log._BufferAdd("debug", Mensagem, Extra)
        Log._Persistir("debug", Mensagem, Extra)

    @staticmethod
    def Info(Mensagem, Extra=None):
        if not Log._Iniciado:
            return
        Log._Contadores["info"] += 1
        Log._Console("info", Mensagem, Extra)
        Log._BufferAdd("info", Mensagem, Extra)
        Log._Persistir("info", Mensagem, Extra)

    @staticmethod
    def Aviso(Mensagem, Extra=None):
        if not Log._Iniciado:
            return
        Log._Contadores["aviso"] += 1
        Log._Console("aviso", Mensagem, Extra)
        Log._BufferAdd("aviso", Mensagem, Extra)
        Log._Persistir("aviso", Mensagem, Extra)

    @staticmethod
    def Erro(Mensagem, Extra=None):
        if not Log._Iniciado:
            return
        Log._Contadores["erro"] += 1
        Log._Console("erro", Mensagem, Extra)
        Log._BufferAdd("erro", Mensagem, Extra)
        Log._Persistir("erro", Mensagem, Extra)

    @staticmethod
    def Critico(Mensagem, Extra=None):
        if not Log._Iniciado:
            return
        Log._Contadores["critico"] += 1
        Log._Console("critico", Mensagem, Extra)
        Log._BufferAdd("critico", Mensagem, Extra)
        Log._Persistir("critico", Mensagem, Extra)

    @staticmethod
    def Alvo(Inicio, Fim, Resultado, Extra=None):
        Payload = {
            "inicio": Inicio,
            "fim": Fim,
            "resultado": Resultado,
        }
        if Extra:
            Payload["extra"] = Extra
        Log.Info("alvo processado", Payload)

    @staticmethod
    def Descoberta(Modulo, Alvo, Achado, Extra=None):
        Payload = {"modulo": Modulo, "alvo": Alvo, "achado": Achado}
        if Extra:
            Payload["extra"] = Extra
        Log.Info("descoberta", Payload)

    @staticmethod
    def Bypass(Modulo, Alvo, Sucesso, Extra=None):
        Nivel = "info" if Sucesso else "aviso"
        Payload = {"modulo": Modulo, "alvo": Alvo, "sucesso": Sucesso}
        if Extra:
            Payload["extra"] = Extra
        if Nivel == "info":
            Log.Info("bypass tentado", Payload)
        else:
            Log.Aviso("bypass falhou", Payload)

    @staticmethod
    def Fuzz(Modulo, Alvo, Crash, Extra=None):
        Nivel = "critico" if Crash else "debug"
        Payload = {"modulo": Modulo, "alvo": Alvo, "crash": Crash}
        if Extra:
            Payload["extra"] = Extra
        if Nivel == "critico":
            Log.Critico("fuzz crash", Payload)
        else:
            Log.Debug("fuzz iteracao", Payload)

    @staticmethod
    def Verificacao(Modulo, Alvo, Ok, Extra=None):
        Payload = {"modulo": Modulo, "alvo": Alvo, "ok": Ok}
        if Extra:
            Payload["extra"] = Extra
        Log.Info("verificacao", Payload)

    @staticmethod
    def Contadores():
        return dict(Log._Contadores)

    @staticmethod
    def Buffer(N=100):
        if N <= 0:
            return list(Log._Buffer)
        return Log._Buffer[-N:]

    @staticmethod
    def BufferJson(N=100, Indent=2):
        return json.dumps(Log.Buffer(N), indent=Indent, ensure_ascii=False, default=str)

    @staticmethod
    def Limpar():
        Log._Buffer = []
        for K in Log._Contadores:
            Log._Contadores[K] = 0

    @staticmethod
    def Stats():
        Total = sum(Log._Contadores.values())
        return {
            "total": Total,
            "por_nivel": dict(Log._Contadores),
            "buffer_size": len(Log._Buffer),
            "iniciado": Log._Iniciado,
            "arquivo": Log._Arquivo is not None,
            "decorrido": round(Log._Decorrido(), 3),
        }
