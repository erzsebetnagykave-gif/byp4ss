import os
import pty
import select
import signal
import subprocess
import sys
import termios
import time
import tty

TRACE_DIR = "/data/data/com.termux/files/home/CyberneticCrown/CC/T0OLS/ByP4ss/logs/trace"

def main():
    if len(sys.argv) < 2:
        print("uso: python3 trace.py <comando> [args...]")
        sys.exit(1)

    os.makedirs(TRACE_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(TRACE_DIR, f"trace_{ts}.jsonl")
    raw_path = os.path.join(TRACE_DIR, f"trace_{ts}.raw")

    master, slave = pty.openpty()
    proc = subprocess.Popen(sys.argv[1:], stdin=slave, stdout=slave, stderr=slave, close_fds=True)
    os.close(slave)

    log_f = open(log_path, "w")
    raw_f = open(raw_path, "wb")

    old_term = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)

    try:
        while True:
            r, _, _ = select.select([master, sys.stdin], [], [], 0.1)
            if master in r:
                try:
                    data = os.read(master, 4096)
                except OSError:
                    break
                if not data:
                    break
                raw_f.write(data)
                raw_f.flush()
            if sys.stdin in r:
                try:
                    data = os.read(sys.stdin.fileno(), 1024)
                except OSError:
                    break
                if not data:
                    break
                try:
                    os.write(master, data)
                except OSError:
                    pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_term)
        log_f.close()
        raw_f.close()
        proc.terminate()

    print(f"\n[trace] log salvo em: {log_path}")
    print(f"[trace] para ler: cat {log_path} | jq .")

if __name__ == "__main__":
    main()
