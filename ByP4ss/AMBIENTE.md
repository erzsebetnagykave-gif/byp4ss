# AMBIENTE.md — o que o ByP4ss verifica (e o que não verifica)

Este documento lista **o que o ByP4ss pode verificar** e **o que não pode**.
Não contém suposições. O que está marcado como "fornecido pelo operador" não foi verificado pelo ByP4ss.

## O que o ByP4ss VERIFICA (fato)

### Rede local (via `Scanner/scanner.cpp`)
- Port scan TCP + ICMP + mDNS em /24
- DNS reverso (hostname)
- Detecção de fabricante por banner / header HTTP
- Estimativa de OS por TTL
- Fabricante: TP-Link, D-Link, Tenda, Arcadyan, ipTIME, ZTE, Huawei, MikroTik, Cisco, Netgear, Asus, Linksys, Ubiquiti, Fortinet, OpenWrt

### Descoberta (via `Discovery/`)
- `PortScan.py`: portas abertas com latência e banner
- `Ssdp.py`: M-SEARCH UPnP, retorna `LOCATION`, `SERVER`, `ST`, `USN`
- `Descriptor.py`: parse do descritor UPnP, extrai `control_url`
- `ServiceFingerprint.py`: identifica serviço em cada porta (banner + HTTP HEAD + TLS)
- `CveMatch.py`: correlaciona fingerprint + porta com 9 CVEs conhecidas
- `SqliScan.py`: SQLi (error-based, time-based, boolean) — 12 params × 21 payloads

### Bypass (via `Bypass/`)
- `UpnpBypass.py`: AddPortMapping via SOAP
- `HttpAuth.py`: path traversal em auth HTTP (84 variações)
- `TelnetBrute.py`: brute force Telnet (15 credenciais: YAML + K1ELI genérico)
- `DnsRebind.py`: detecta SSRF via DNS rebinding (9 endpoints, `nip.io`/`sslip.io`)

### Fuzz (via `Fuzz/`)
- `FuzzHttp`: mutação de método/header HTTP
- `FuzzCrlf`: CRLF injection
- `FuzzSqli`: SQLi (error/time/boolean)
- `FuzzPath`: path traversal
- `FuzzXss`: XSS refletido
- `FuzzNullspace`: inputs vazios/nulos/Unicode malformado
- `FuzzMetamorph`: 20 sintaxes SQL equivalentes
- `FuzzResonance`: variância de latência/tamanho
- `FuzzOracle`: comparação com baseline local

### Verificação (via `Verify/`)
- `PortVerify.py`: porta TCP abriu
- `ServiceVerify.py`: serviço responde (banner/HTTP/TLS)
- `ExploitVerify.py`: shell aberto (echo com marcador único)

### Report (via `Report/`)
- `Findings.py`: transforma resultados em achados com severidade
- `Export.py`: JSON, MD, CSV
- `Dataset.py`: JSONL com 8 features + recompensa (pro B4S)
- `Ambiente.py`: estado consolidado (pro B4S)
- `Api.py`: API do Agent B4S (`UltimaTransicao`, `Transicoes`, `VetorEstado`)

## O que o ByP4ss NÃO verifica

- **Tráfego encriptado** sem chave (TLS é opaco)
- **Comando executado** por exploit (só verifica se shell abriu, não o que rodou)
- **Firmware real** (só o que responde via HTTP/SSDP)
- **Modelo/fabricante exato** (via banner, não via firmware)
- **Credencial válida em SSH/HTTP** (só em Telnet via `TelnetBrute`)
- **Root** (precisa de root pro scanner.cpp em raw socket)
- **IPv6** (só IPv4)
- **CGNAT** (não vê tráfego atrás de NAT do provedor)

## Contexto fornecido pelo operador (NÃO verificado pelo ByP4ss)

Esta seção é **opcional**. Contém o que o operador relatou, mas o ByP4ss não tem como verificar.

- Rede chamada "Dimora Guest" (operador)
- Roteador `192.168.0.1` reportado como ZTE F6600P (não verificado por banner)
- MAC `d8:9a:0d:a5:1d:a7` (operador, não verificado por scanner)
- "Empresa de fachada" (fora do escopo técnico)

## Como usar

```bash
# 1. Rodar o teste de integração (prova que o pipeline roda)
python3 TesteIntegracao.py

# 2. Rodar o ByP4ss contra um alvo (com flags)
python3 ByP4ss.py 192.168.0.1 --all

# 3. Rodar a CLI interativa
python3 byp4ss_cli.py

# 4. Rodar a TUI (console2)
cd console2 && python3 main.py
### Report (via `Report/`)
- `Findings.py`: transforma resultados em achados com severidade
- `Export.py`: JSON, MD, CSV
- `Dataset.py`: JSONL com 8 features + recompensa (pro B4S)
- `Ambiente.py`: estado consolidado (pro B4S)
- `Api.py`: API do Agent B4S (`UltimaTransicao`, `Transicoes`, `VetorEstado`)

## O que o ByP4ss NÃO verifica

- **Tráfego encriptado** sem chave (TLS é opaco)
- **Comando executado** por exploit (só verifica se shell abriu, não o que rodou)
- **Firmware real** (só o que responde via HTTP/SSDP)
- **Modelo/fabricante exato** (via banner, não via firmware)
- **Credencial válida em SSH/HTTP** (só em Telnet via `TelnetBrute`)
- **Root** (precisa de root pro scanner.cpp em raw socket)
- **IPv6** (só IPv4)
- **CGNAT** (não vê tráfego atrás de NAT do provedor)

## Contexto fornecido pelo operador (NÃO verificado pelo ByP4ss)

Esta seção é **opcional**. Contém o que o operador relatou, mas o ByP4ss não tem como verificar.

- Rede chamada "Dimora Guest" (operador)
- Roteador `192.168.0.1` reportado como ZTE F6600P (não verificado por banner)
- MAC `d8:9a:0d:a5:1d:a7` (operador, não verificado por scanner)
- "Empresa de fachada" (fora do escopo técnico)

## Como usar

```bash
# 1. Rodar o teste de integração (prova que o pipeline roda)
python3 TesteIntegracao.py

# 2. Rodar o ByP4ss contra um alvo (com flags)
python3 ByP4ss.py 192.168.0.1 --all

# 3. Rodar a CLI interativa
python3 byp4ss_cli.py

# 4. Rodar a TUI (console2)
cd console2 && python3 main.py
```

Limitações conhecidas

· --all contra alvo externo (ex: 8.8.8.8) demora ~50-60s porque faz 84 requests HTTP que batem timeout.
· Fuzz contra porta 80 fechada retorna crashes: [], anomalias: [] (esperado).
· DnsRebind só retorna ok: True se o alvo acessar 127.0.0.1 (não se nip.io resolver).
· Report.dataset.jsonl só tem exemplos se findings tiver achados (porta aberta, fingerprint, bypass, etc).
· AgentB4SS (ainda não implementado) vai precisar do RoteadorFalso pra treinar com sinal real.

Status do ByP4ss

· 0.0.1: fechada (pipeline rodando)
· 0.1.0: em fechamento (falta --sqli no CLI principal, README.md atualizado)
· 0.2.0: planejada (RoteadorFalso, AgentB4SS)
  MDEOF
  python3 -c "import ast; ast.parse(open('TesteIntegracao.py').read()); print('[ok] TesteIntegracao.py')"
  wc -l TesteIntegracao.py AMBIENTE.md

```

## O que esperar

```

[ok] TesteIntegracao.py
~185 TesteIntegracao.py
~120 AMBIENTE.md

```

**Total: ~305 linhas** (eu estimei 280, deu ~305 com os dois).

## Teste do `TesteIntegracao` (1 comando, ~25s)

```bash
cd ~/CyberneticCrown/CC/T0OLS/ByP4ss
python3 TesteIntegracao.py

EOF
