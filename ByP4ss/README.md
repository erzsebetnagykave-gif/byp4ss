# ByP4ss

Ferramenta de descoberta e exploração de vulnerabilidades em roteadores.
Python 3.10+ (principal), Go (SQLi + TUI), Rust (fuzzy), C++ (scanner), C (sensores).

**Estado:** 0.1.0 — pipeline completo, CLI interativa, TUI opcional, framework B4S pronto.

## O que faz

- **Descoberta:** port scan TCP + SSDP/UPnP + fingerprint de serviço + correlação CVE + SQLi
- **Bypass:** UPnP AddPortMapping, HTTP auth path traversal, Telnet brute force, DNS rebinding (SSRF)
- **Fuzz:** 9 técnicas (HTTP mutation, CRLF, SQLi, path traversal, XSS, nullspace, metamorph, resonance, oracle)
- **Verificação:** porta aberta, serviço responde, shell aberto
- **Relatório:** JSON + MD + CSV + dataset JSONL (pro B4S) + ambiente JSON
- **6 exploits:** TP-Link, D-Link, Tenda 7795, Tenda 29384, Arcadyan, ipTIME
- **9 auxiliares:** Base64 evasivo, MIPS shellcode, reverse shell (7 protocolos), bind shell (4 protocolos), SSDP falso, HTTP falso, CGI scanner, CGI rules, path scanner

## Instalação

### Termux / Linux
```bash
# Python 3.10+ (já vem)
pkg install python

# Go (pro --sqli, opcional)
pkg install golang
cd Discovery/sqliscan && go build -o sqliscan main.go

# g++ (pro --scan, opcional)
pkg install clang
cd Scanner && g++ -O2 -std=c++17 -o scanner scanner.cpp
```

macOS

```bash
brew install python go
```

Uso rápido

```bash
# Pipeline completo (discover + bypass + fuzz + verify + report)
python3 ByP4ss.py 192.168.0.1 --all

# Só descoberta
python3 ByP4ss.py 192.168.0.1 --discover

# SQLi
python3 ByP4ss.py 192.168.0.1 --sqli

# CLI interativa (prompt agent.byp4ss >)
python3 byp4ss_cli.py

# TUI (console2)
cd console2 && python3 main.py

# Teste de integração (prova que roda)
python3 TesteIntegracao.py
```

Todos os comandos (ByP4ss.py)

Flag O que faz
--all discover + bypass + fuzz + verify + report
--discover port scan + SSDP + fingerprint + CVE
--bypass UPnP + HTTP auth + Telnet + DNS rebind
--fuzz 9 técnicas de fuzzing
--verify porta, serviço, shell
--report JSON + MD + CSV + dataset + ambiente
--scan scanner.cpp (compila se necessário)
--sqli SQL injection scan (Go, fallback Python)
--chain list / --chain run kill chain (4 templates)
--sessao list/show/rm sessões salvas
--manifesto list/aplicar/reverter manifestos de código
--api servidor REST (127.0.0.1:8765)
--treinar [N] Q-Learning (default 100 episódios)
--qtable mostra QTable treinada

Args globais: --alvo, --portas (22,80,443 ou 1-1000), --threads, --timeout, --verbose, --json.

CLI interativa (byp4ss_cli.py)

```bash
python3 byp4ss_cli.py
# Prompt: agent.byp4ss >
```

20 comandos: scan, analise, cred, sqli, exploit, chain, upnp, httpauth, shell, servidor, treinar, qtable, api, sessao, manifesto, status, help, clear, sair.

Tab completa comandos + subcomandos + args. Histórico em ~/.console/byp4ss_history.

TUI (console2/)

```bash
cd console2 && python3 main.py
```

Grade com bordas, 6 abas (comando/alvo/exploit/cadeia/sessão/histórico), paleta com filtro, toast, help. Requer TTY.

Estrutura

```
ByP4ss/
├── ByP4ss.py                 CLI de flags (14 comandos)
├── byp4ss_cli.py             CLI interativa (agent.byp4ss >)
├── TesteIntegracao.py        prova que o pipeline roda
├── Treino.py                 Q-Learning (QTable + replay)
├── AMBIENTE.md               o que verifica e o que não verifica
├── Core/                     Engine, Config, Log, Constants
├── Discovery/                PortScan, Ssdp, Descriptor, ServiceFingerprint, CveMatch, SqliScan
│   └── sqliscan/main.go      motor SQLi em Go
├── Bypass/                   UpnpBypass, HttpAuth, TelnetBrute, DnsRebind
├── Fuzz/                     FuzzEngine + 8 técnicas
├── Verify/                   PortVerify, ServiceVerify, ExploitVerify
├── Report/                   Findings, Export, Dataset, Ambiente, Api (B4S)
├── ExploitByp4ss/            6 exploits + 9 auxiliares + credenciais.yaml
├── Scanner/scanner.cpp       scan de rede em C++
├── Tools/                    K1ELI (brute force), SENSOR (hardware)
├── console2/                 TUI Python
└── Paleta/                   TUI Go (independente do ByP4ss)
```

Limitações

· Contra 127.0.0.1 fechado, --all retorna achados vazios (correto — não tem porta aberta).
· Contra alvo externo (ex: 8.8.8.8), --all demora ~50-60s porque bypass/fuzz batem timeout.
· Fuzz contra porta fechada retorna crashes: [], anomalias: [].
· DnsRebind só retorna ok: True se o alvo acessar 127.0.0.1 (não se nip.io resolver).
· Report.dataset.jsonl só tem exemplos se houver achados.
· Não verifica tráfego encriptado sem chave, comando executado (só shell aberto), firmware real, IPv6, CGNAT.
· Sem root, scanner.cpp só faz TCP connect + ICMP DGRAM (não raw socket).

O que NÃO faz (fora do escopo)

· ❌ Treinar LLM
· ❌ Gerar código
· ❌ Conversar
· ❌ AGI

Para o Agent B4S (rede neural própria), ver CC/CrownML/ (em construção).

Ver também

· AMBIENTE.md — o que verifica e o que não verifica
· TesteIntegracao.py — prova que o pipeline roda
· console2/main.py --teste — teste headless da TUI
· Treino.py teste — teste do Q-Learning

Status

· 0.0.1 — pipeline completo (Verify + Report + Discovery + Fuzz 9/9 + Bypass 4/4)
· 0.1.0 — CLI interativa + TesteIntegracao + AMBIENTE + --sqli (fechado agora)
· 0.2.0 (planejada) — RoteadorFalso (valida exploits), AgentB4SS, CrownML

Licença

Uso pessoal. Autor: CyberneticCrown (2026).
