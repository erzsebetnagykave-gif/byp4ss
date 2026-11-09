# PortVerify do ByP4ss
# Verifica se uma porta TCP abriu apos um exploit.
# Chamado por Core.Engine.Verify: Mod.PortVerify.Verificar(Alvo, Porta) -> bool
#
# Estrategia: tentativa multipla com backoff, porque muitos exploits
# abrem a porta com delay (kernel aceita conexao antes do servidor
# estar realmente escutando). Retry por ~5s cobre o caso comum.

import socket
import time

from Core.Config import Config
from Core.Log import Log


class PortVerify:

    TENTATIVAS = 3
    INTERVALO = 0.8
    TIMEOUT = 1.5

    @staticmethod
    def Verificar(Alvo, Porta, Timeout=None, Tentativas=None, Intervalo=None):
        if not Alvo or not Porta:
            return False
        try:
            PortaInt = int(Porta)
        except (TypeError, ValueError):
            return False
        if PortaInt < 1 or PortaInt > 65535:
            return False
        Timeout = Timeout or PortVerify.TIMEOUT
        Tentativas = Tentativas or PortVerify.TENTATIVAS
        Intervalo = Intervalo or PortVerify.INTERVALO
        for Tentativa in range(Tentativas):
            if PortVerify._Testar(Alvo, PortaInt, Timeout):
                Log.Verificacao("PortVerify", Alvo, True, {
                    "porta": PortaInt,
                    "tentativa": Tentativa + 1,
                    "total_tentativas": Tentativas,
                })
                return True
            if Tentativa < Tentativas - 1:
                time.sleep(Intervalo)
        Log.Verificacao("PortVerify", Alvo, False, {
            "porta": PortaInt,
            "tentativas": Tentativas,
        })
        return False

    @staticmethod
    def _Testar(Alvo, Porta, Timeout):
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.settimeout(Timeout)
        try:
            Codigo = Sock.connect_ex((Alvo, Porta))
            return Codigo == 0
        except (socket.error, OSError):
            return False
        finally:
            try:
                Sock.close()
            except (socket.error, OSError):
                pass

    @staticmethod
    def Aguardar(Alvo, Porta, EsperaMax=None, Intervalo=None):
        EsperaMax = EsperaMax or 10.0
        Intervalo = Intervalo or 0.5
        Inicio = time.monotonic()
        while time.monotonic() - Inicio < EsperaMax:
            if PortVerify._Testar(Alvo, int(Porta), 1.0):
                return True
            time.sleep(Intervalo)
        return False

    @staticmethod
    def Varias(Alvo, Portas, Timeout=None):
        Abertas = []
        Fechadas = []
        for P in Portas:
            if PortVerify.Verificar(Alvo, P, Timeout):
                Abertas.append(int(P))
            else:
                Fechadas.append(int(P))
        return {"abertas": Abertas, "fechadas": Fechadas,
                "total": len(Portas), "sucesso": len(Abertas)}

    @staticmethod
    def Info():
        return {
            "nome": "PortVerify",
            "metodo": "tcp_connect_ex",
            "tentativas": PortVerify.TENTATIVAS,
            "timeout": PortVerify.TIMEOUT,
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "teste":
        Alvo = sys.argv[2]
        Portas = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [22, 80, 443, 8080]
        print(f"verificando {Alvo} portas={Portas}")
        R = PortVerify.Varias(Alvo, Portas)
        print(f"abertas: {R['abertas']}")
        print(f"fechadas: {R['fechadas']}")
