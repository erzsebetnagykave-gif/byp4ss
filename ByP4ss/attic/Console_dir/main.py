import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assinc import Motor, TesteAsync
from app import App, RodarHeadless


VERSAO = "1.0"


def MostrarAjuda():
    print(f"Console {VERSAO}")
    print()
    print("uso: python3 main.py [comando]")
    print()
    print("comandos:")
    print("  bypass        abre o console TUI")
    print("  teste-async   testa o motor async")
    print("  teste-app     testa o loop headless")
    print("  versao        mostra versao")
    print("  ajuda         mostra esta ajuda")
    print()
    print("atalhos no console:")
    print("  Ctrl+T        proxima sala")
    print("  Shift+Ctrl+T  sala anterior")
    print("  Up/Down       navega")
    print("  Enter         executa")
    print("  Ctrl+S        salva sessao")
    print("  Ctrl+R        retoma sessao")
    print("  Ctrl+O        toggle operador")
    print("  Ctrl+Q        sai")


def MostrarVersao():
    print(f"Console {VERSAO}")
    print(f"Python {sys.version.split()[0]}")


def Main():
    args = sys.argv[1:]
    cmd = args[0] if args else "ajuda"
    if cmd == "bypass":
        app = App()
        try:
            return app.Rodar()
        except KeyboardInterrupt:
            return 0
    if cmd == "teste-async":
        TesteAsync()
        return 0
    if cmd == "teste-app":
        RodarHeadless()
        return 0
    if cmd in ("ajuda", "-h", "--help"):
        MostrarAjuda()
        return 0
    if cmd in ("versao", "-v", "--version"):
        MostrarVersao()
        return 0
    print(f"comando desconhecido: {cmd}", file=sys.stderr)
    MostrarAjuda()
    return 2


if __name__ == "__main__":
    sys.exit(Main())
