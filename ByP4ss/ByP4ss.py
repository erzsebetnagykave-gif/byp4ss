#!/usr/bin/env python3
# ByP4ss — CLI completa (fachada fina)
# Cada flag delega pra um modulo existente. Sem logica pesada aqui.
#
# Flags de pipeline (Engine):
#   --all         discover + bypass + fuzz + verify + report
#   --discover    so discover
#   --bypass      so bypass
#   --fuzz        so fuzz
#   --verify      so verify
#   --report      so report
#
# Flags de ferramenta:
#   --scan        chama Scanner/scanner.cpp (compila se preciso)
#   --manifesto   Manifesto.Listar / Buscar / Aplicar
#   --sessao      Sessao.Listar / Carregar / Salvar
#   --api         Api.Iniciar (foreground, Ctrl+C pra sair)
#   --chain       Cadeia.Templates / Executar
#   --treinar     Treino.Treinar (Q-Learning)
#   --qtable      Treino.MostrarQTable
#
# Argumentos globais:
#   --alvo, --portas, --threads, --timeout, --verbose, --json

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Core.Config import Config
from Core.Log import Log
from Core.Engine import Engine
from Core.Constants import Constants
try:
    from Discovery.SqliScan import SqliScan
except Exception:
    SqliScan = None


def _ParsearPortas(Texto, Default=None):
    if not Texto:
        return Default or Constants.PORTAS_CRITICAS
    Out = []
    for Parte in str(Texto).split(","):
        P = Parte.strip()
        if not P:
            continue
        if "-" in P:
            try:
                A, B = P.split("-", 1)
                Inicio, Fim = int(A), int(B)
                if Inicio > 0 and Fim >= Inicio and Fim <= 65535:
                    Out.extend(range(Inicio, Fim + 1))
            except (ValueError, TypeError):
                pass
        else:
            try:
                V = int(P)
                if 0 < V <= 65535:
                    Out.append(V)
            except (ValueError, TypeError):
                pass
    return sorted(set(Out)) or (Default or Constants.PORTAS_CRITICAS)


def _AplicarConfig(Args):
    Config.Alvo = Args.alvo or Config.Alvo
    if Args.portas:
        Config.Portas = _ParsearPortas(Args.portas)
    if Args.threads:
        Config.Threads = int(Args.threads)
        Config.ThreadsPorts = int(Args.threads)
        Config.ThreadsFuzz = int(Args.threads)
    if Args.timeout:
        Config.Timeout = float(Args.timeout)
        Config.TimeoutTCP = float(Args.timeout)
        Config.TimeoutHTTP = float(Args.timeout)
        Config.TimeoutVerify = float(Args.timeout)
    Config.Verbose = bool(Args.verbose)
    Config.Json = bool(Args.json)


def _Imprimir(Resultado, Args):
    if Args.json:
        print(json.dumps(Resultado, indent=2, ensure_ascii=False, default=str))
    else:
        Ok = Resultado.get("ok") if isinstance(Resultado, dict) else bool(Resultado)
        print(f"[{'ok' if Ok else 'erro'}] {type(Resultado).__name__}")
        if isinstance(Resultado, dict):
            for K, V in Resultado.items():
                if K in ("ok",):
                    continue
                if isinstance(V, (list, dict)):
                    print(f"  {K}: {len(V) if isinstance(V, list) else 'dict'}")
                else:
                    print(f"  {K}: {V}")


def _CmdPipeline(Args, Fases):
    _AplicarConfig(Args)
    if not Args.alvo:
        print("[erro] --alvo obrigatorio", file=sys.stderr)
        return 2
    Log.Iniciar(Config)
    Engine.Iniciar(Config)
    Resultados = {}
    try:
        if "discover" in Fases:
            Resultados["discover"] = Engine.Discover(Args.alvo)
        if "bypass" in Fases:
            Resultados["bypass"] = Engine.Bypass(Args.alvo)
        if "fuzz" in Fases:
            Resultados["fuzz"] = Engine.Fuzz(Args.alvo)
        if "verify" in Fases:
            Resultados["verify"] = Engine.Verify(Args.alvo)
        if "report" in Fases:
            Resultados["report"] = Engine.Report()
    except KeyboardInterrupt:
        print("\n[interrompido]", file=sys.stderr)
    finally:
        Engine.Finalizar()
        Log.Finalizar()
    if Args.json:
        print(json.dumps(Resultados, indent=2, ensure_ascii=False, default=str))
    else:
        for Fase, R in Resultados.items():
            print(f"  [{Fase}] ok={bool(R) if not isinstance(R, dict) else R.get('ok')}")
    return 0


def _CmdScan(Args):
    from subprocess import run, CalledProcessError
    Raiz = os.path.dirname(os.path.abspath(__file__))
    Fonte = os.path.join(Raiz, "Scanner", "scanner.cpp")
    Bin = os.path.join(Raiz, "Scanner", "scanner")
    if not os.path.isfile(Fonte):
        print(f"[erro] {Fonte} nao existe", file=sys.stderr)
        return 1
    if not os.path.isfile(Bin) or os.path.getmtime(Fonte) > os.path.getmtime(Bin):
        print(f"[info] compilando {Fonte}...", file=sys.stderr)
        try:
            Compilar = run(["g++", "-O2", "-std=c++17", "-o", Bin, Fonte],
                           capture_output=True, text=True, timeout=60)
            if Compilar.returncode != 0:
                print(f"[erro] compilacao falhou:", file=sys.stderr)
                print(Compilar.stderr[:1000], file=sys.stderr)
                return 1
            os.chmod(Bin, 0o755)
            print(f"[ok] compilado: {Bin}", file=sys.stderr)
        except FileNotFoundError:
            print("[erro] g++ nao instalado. pkg install g++", file=sys.stderr)
            return 1
        except Exception as E:
            print(f"[erro] {type(E).__name__}: {E}", file=sys.stderr)
            return 1
    Argumentos = [Bin]
    if Args.json:
        Argumentos.append("--json")
    try:
        run(Argumentos, timeout=300)
        return 0
    except KeyboardInterrupt:
        return 130
    except Exception as E:
        print(f"[erro] {type(E).__name__}: {E}", file=sys.stderr)
        return 1


def _CmdManifesto(Args):
    from Manifesto import Manifesto, Motor
    Acao = Args.manifesto
    if Acao == "list":
        R = Manifesto.Listar()
        _Imprimir(R, Args)
    elif Acao == "descobrir":
        R = Manifesto.Descobrir()
        _Imprimir(R, Args)
    elif Acao == "aplicar" and Args.manifesto_id:
        R = Motor.Aplicar(Args.manifesto_id)
        _Imprimir(R, Args)
    elif Acao == "reverter" and Args.manifesto_id:
        R = Motor.Reverter(Args.manifesto_id)
        _Imprimir(R, Args)
    elif Acao == "status":
        R = Motor.ListarAplicados()
        _Imprimir(R, Args)
    else:
        print("[erro] uso: --manifesto=list|descobrir|aplicar|reverter|status [--manifesto-id=X]",
              file=sys.stderr)
        return 2
    return 0


def _CmdSessao(Args):
    from Sessao import Sessao
    Acao = Args.sessao
    if Acao == "list":
        R = Sessao.Listar()
        _Imprimir(R, Args)
    elif Acao == "show" and Args.sessao_nome:
        R = Sessao.Carregar(Args.sessao_nome)
        _Imprimir(R, Args)
    elif Acao == "rm" and Args.sessao_nome:
        R = Sessao.Apagar(Args.sessao_nome)
        _Imprimir(R, Args)
    else:
        print("[erro] uso: --sessao=list|show|rm [--sessao-nome=X]", file=sys.stderr)
        return 2
    return 0


def _CmdApi(Args):
    from Api import Api
    R = Api.Iniciar(Escuta="127.0.0.1", Porta=Args.api_porta or 8765)
    if not R.get("ok"):
        print(f"[erro] {R.get('motivo')}", file=sys.stderr)
        return 1
    print(f"[ok] api em http://127.0.0.1:{R.get('porta')}")
    print(f"  token: {R.get('token', '?')[:16]}...")
    print(f"  Ctrl+C pra sair")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        Api.Parar()
        print("\n[ok] api derrubada")
        return 0


def _CmdChain(Args):
    from Cadeia import Cadeia
    if Args.chain == "list":
        R = Cadeia.Templates()
        _Imprimir(R, Args)
    elif Args.chain == "run" and Args.chain_nome:
        if not Args.alvo:
            print("[erro] --alvo obrigatorio pra --chain=run", file=sys.stderr)
            return 2
        R = Cadeia.Executar(Args.chain_nome, Args.alvo)
        _Imprimir(R, Args)
    else:
        print("[erro] uso: --chain=list|run --chain-nome=X --alvo=Y", file=sys.stderr)
        return 2
    return 0


def _CmdTreinar(Args):
    try:
        from Treino import QTable, Treinar
    except Exception as E:
        print(f"[erro] Treino.py indisponivel: {E}", file=sys.stderr)
        return 1
    Q = QTable()
    Carregou = Q.Carregar()
    if Carregou.get("ok"):
        print(f"[info] qtable carregada: {Carregou.get('n_pares')} pares")
    R = Treinar(Q, Episodios=Args.treinar or 100, Verbose=Args.verbose)
    if not R.get("ok"):
        print(f"[erro] {R.get('motivo')}", file=sys.stderr)
        return 1
    Salvo = Q.Salvar()
    if Args.json:
        print(json.dumps({"treino": R, "salvo": Salvo},
                         indent=2, ensure_ascii=False, default=str))
    else:
        print(f"[ok] treino: {R.get('episodios')} ep, "
              f"{R.get('transicoes_processadas')} updates, "
              f"{R.get('n_pares_final')} pares")
        print(f"[ok] salvo: {Salvo.get('caminho')} ({Salvo.get('n_pares')} pares)")
    return 0


def _CmdQTable(Args):
    try:
        from Treino import QTable, MostrarQTable
    except Exception as E:
        print(f"[erro] Treino.py indisponivel: {E}", file=sys.stderr)
        return 1
    Q = QTable()
    R = Q.Carregar()
    if not R.get("ok"):
        print(f"[erro] {R.get('motivo')}", file=sys.stderr)
        return 1
    MostrarQTable(Q, Top=Args.qtable_top or 10)
    return 0


def Main():
    P = argparse.ArgumentParser(
        prog="ByP4ss",
        description="Ferramenta de descoberta e exploracao de vulnerabilidades em roteadores.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    P.add_argument("alvo_pos", nargs="?", default=None,
                   help="IP ou hostname do alvo (posicional)")
    P.add_argument("--alvo", default=None, help="IP ou hostname do alvo")
    P.add_argument("--portas", default=None, help="ex: 22,80,443 ou 1-1000")
    P.add_argument("--threads", type=int, default=None)
    P.add_argument("--timeout", type=float, default=None)
    P.add_argument("--verbose", action="store_true")
    P.add_argument("--json", action="store_true")

    P.add_argument("--sqli", action="store_true",
                        help="SQL injection scan no alvo")
    P.add_argument("--all", action="store_true",
                   help="discover + bypass + fuzz + verify + report")
    P.add_argument("--discover", action="store_true")
    P.add_argument("--bypass", action="store_true")
    P.add_argument("--fuzz", action="store_true")
    P.add_argument("--verify", action="store_true")
    P.add_argument("--report", action="store_true")

    P.add_argument("--scan", action="store_true",
                   help="chama Scanner/scanner.cpp (compila se preciso)")

    P.add_argument("--manifesto", default=None,
                   choices=["list", "descobrir", "aplicar", "reverter", "status"])
    P.add_argument("--manifesto-id", default=None)

    P.add_argument("--sessao", default=None,
                   choices=["list", "show", "rm"])
    P.add_argument("--sessao-nome", default=None)

    P.add_argument("--api", action="store_true")
    P.add_argument("--api-porta", type=int, default=8765)

    P.add_argument("--chain", default=None, choices=["list", "run"])
    P.add_argument("--chain-nome", default=None)

    P.add_argument("--treinar", type=int, nargs="?", const=100, default=None,
                   help="treina QTable (default 100 episodios)")
    P.add_argument("--qtable", action="store_true", help="mostra QTable")
    P.add_argument("--qtable-top", type=int, default=10)

    Args = P.parse_args()
    Args.alvo = Args.alvo or Args.alvo_pos

    if Args.sqli:
        if SqliScan is None:
            print("[erro] SqliScan indisponivel", file=sys.stderr)
            return 1
        if not Args.alvo:
            print("[erro] --alvo obrigatorio pra --sqli", file=sys.stderr)
            return 2
        Porta = int(Args.portas) if Args.portas and str(Args.portas).isdigit() else 80
        R = SqliScan.Escanear(Args.alvo, Porta)
        if Args.json:
            print(json.dumps(R, indent=2, ensure_ascii=False, default=str))
        else:
            print(f"[sqli] total={R.get('total', 0)} via={R.get('via', '?')} duracao={R.get('duracao_s', 0)}s")
            for V in (R.get('vulneraveis') or [])[:10]:
                print(f"  {V.get('param')}: {V.get('tipo')} - {V.get('evidencia', '')[:60]}")
        return 0 if R.get('ok') else 1

    if Args.scan:
        return _CmdScan(Args)
    if Args.manifesto:
        return _CmdManifesto(Args)
    if Args.sessao:
        return _CmdSessao(Args)
    if Args.api:
        return _CmdApi(Args)
    if Args.chain:
        return _CmdChain(Args)
    if Args.treinar is not None:
        return _CmdTreinar(Args)
    if Args.qtable:
        return _CmdQTable(Args)

    Fases = []
    if Args.all:
        Fases = ["discover", "bypass", "fuzz", "verify", "report"]
    else:
        if Args.discover: Fases.append("discover")
        if Args.bypass:   Fases.append("bypass")
        if Args.fuzz:     Fases.append("fuzz")
        if Args.verify:   Fases.append("verify")
        if Args.report:   Fases.append("report")
    if Fases:
        return _CmdPipeline(Args, Fases)

    P.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(Main())
