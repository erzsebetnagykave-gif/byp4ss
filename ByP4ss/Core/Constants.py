# Constantes do ByP4ss
# 300 linhas (parte 1 de 2)


import os
# ============================================================
# VERSAO E IDENTIDADE
# ============================================================

VERSAO = "1.0.0"
NOME = "ByP4ss"
AUTOR = "CyberneticCrown"
ANO = "2026"

# ============================================================
# ALVOS PADRAO
# ============================================================

ALVO_PADRAO = "192.168.0.1"
ALVO_LOCALHOST = "127.0.0.1"
ALVO_BROADCAST = "255.255.255.255"

# ============================================================
# PORTAS COMUNS (ordenadas por probabilidade em roteadores)
# ============================================================

PORTAS_CRITICAS = [22, 23, 53, 80, 443, 8080, 8443, 1900, 52869, 7547]
PORTAS_TELNET = [23, 2323, 23231, 8023]
PORTAS_SSH = [22, 2222, 22222, 8022]
PORTAS_HTTP = [80, 8080, 8000, 8888, 8081]
PORTAS_HTTPS = [443, 8443, 4443, 9443]
PORTAS_DNS = [53, 5353]
PORTAS_UPNP = [1900, 2869, 5000, 52869, 49152, 49153]
PORTAS_TR069 = [7547, 7567, 8089]
PORTAS_SNMP = [161, 162]
PORTAS_TODAS = list(range(1, 1001)) + [1900, 2000, 3000, 5000, 52869, 7547, 8080, 8443]

# ============================================================
# TIMEOUTS (em segundos)
# ============================================================

TIMEOUT_SSDP = 2.0
TIMEOUT_TCP = 1.5
TIMEOUT_UDP = 1.0
TIMEOUT_HTTP = 3.0
TIMEOUT_HTTPS = 5.0
TIMEOUT_TELNET = 3.0
TIMEOUT_SSH = 3.0
TIMEOUT_DNS = 2.0
TIMEOUT_UPNP = 5.0
TIMEOUT_VERIFY = 3.0
TIMEOUT_PADRAO = 5.0

# ============================================================
# THREADS
# ============================================================

THREADS_PADRAO = 10
THREADS_PORTS = 20
THREADS_FUZZ = 10
THREADS_BRUTE = 5
THREADS_MAX = 50

# ============================================================
# SSDP (Simple Service Discovery Protocol)
# ============================================================

SSDP_MULTICAST = "239.255.255.250"
SSDP_PORTA = 1900
SSDP_M_SEARCH = (
    'M-SEARCH * HTTP/1.1\r\n'
    'HOST: 239.255.255.250:1900\r\n'
    'MAN: "ssdp:discover"\r\n'
    'MX: 2\r\n'
    'ST: ssdp:all\r\n'
    'USER-AGENT: ByP4ss/1.0\r\n'
    '\r\n'
).encode()
SSDP_M_SEARCH_IGD = (
    'M-SEARCH * HTTP/1.1\r\n'
    'HOST: 239.255.255.250:1900\r\n'
    'MAN: "ssdp:discover"\r\n'
    'MX: 2\r\n'
    'ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n'
    'USER-AGENT: ByP4ss/1.0\r\n'
    '\r\n'
).encode()
SSDP_M_SEARCH_WAN = (
    'M-SEARCH * HTTP/1.1\r\n'
    'HOST: 239.255.255.250:1900\r\n'
    'MAN: "ssdp:discover"\r\n'
    'MX: 2\r\n'
    'ST: urn:schemas-upnp-org:service:WANIPConnection:1\r\n'
    'USER-AGENT: ByP4ss/1.0\r\n'
    '\r\n'
).encode()

# ============================================================
# UPNP (Universal Plug and Play)
# ============================================================

UPNP_NS_WANIP = "urn:schemas-upnp-org:service:WANIPConnection:1"
UPNP_NS_WANPPP = "urn:schemas-upnp-org:service:WANPPPConnection:1"
UPNP_NS_LAYER3 = "urn:schemas-upnp-org:service:Layer3Forwarding:1"
UPNP_NS_DEVICE = "urn:schemas-upnp-org:device:InternetGatewayDevice:1"
UPNP_NS_WANDEVICE = "urn:schemas-upnp-org:device:WANDevice:1"

UPNP_ACOES = [
    "AddPortMapping",
    "AddAnyPortMapping",
    "DeletePortMapping",
    "DeletePortMappingRange",
    "GetGenericPortMappingEntry",
    "GetSpecificPortMappingEntry",
    "GetExternalIPAddress",
    "GetStatusInfo",
    "GetConnectionTypeInfo",
]

UPNP_SOAP_HEADER = (
    '<?xml version="1.0"?>\n'
    '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
    's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\n'
    '  <s:Body>\n'
)

UPNP_SOAP_FOOTER = (
    '  </s:Body>\n'
    '</s:Envelope>\n'
)

UPNP_ADD_MAPPING = (
    '    <u:{acao} xmlns:u="{ns}">\n'
    '      <NewRemoteHost></NewRemoteHost>\n'
    '      <NewExternalPort>{externa}</NewExternalPort>\n'
    '      <NewProtocol>{protocolo}</NewProtocol>\n'
    '      <NewInternalPort>{interna}</NewInternalPort>\n'
    '      <NewInternalClient>{cliente}</NewInternalClient>\n'
    '      <NewEnabled>1</NewEnabled>\n'
    '      <NewPortMappingDescription>ByP4ss</NewPortMappingDescription>\n'
    '      <NewLeaseDuration>{lease}</NewLeaseDuration>\n'
    '    </u:{acao}>\n'
)

UPNP_DELETE_MAPPING = (
    '    <u:DeletePortMapping xmlns:u="{ns}">\n'
    '      <NewRemoteHost></NewRemoteHost>\n'
    '      <NewExternalPort>{externa}</NewExternalPort>\n'
    '      <NewProtocol>{protocolo}</NewProtocol>\n'
    '    </u:DeletePortMapping>\n'
)

UPNP_STATUS_OK = 200
UPNP_STATUS_ERRO = 500
UPNP_LEASE_0 = 0
UPNP_LEASE_1H = 3600
UPNP_LEASE_24H = 86400
UPNP_LEASE_7D = 604800

# ============================================================
# HTTP
# ============================================================

HTTP_METODOS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH", "HEAD"]
HTTP_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) AppleWebKit/605.1.15",
    "curl/8.0",
    "Wget/1.21",
    "python-requests/2.31",
    "ByP4ss/1.0",
]
HTTP_HEADERS_PADRAO = {
    "User-Agent": "ByP4ss/1.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
    "Cache-Control": "no-cache",
}
HTTP_PATHS_ADMIN = [
    "/", "/admin", "/admin/", "/login", "/login/", "/login.html", "/login.asp",
    "/admin/login", "/admin/login.html", "/admin/login.asp", "/manager",
    "/management", "/management.html", "/setup", "/setup.html", "/config",
    "/config.html", "/cgi-bin/", "/cgi-bin/login", "/cgi-bin/admin",
    "/index.html", "/index.asp", "/home", "/home.html", "/dashboard",
    "/status", "/status.html", "/system", "/system.html", "/main.html",
]
HTTP_PATHS_TRAVERSAL = [
    "/admin", "/admin/", "/admin/.", "/admin/..", "/admin/../admin",
    "/admin/./admin", "/admin/%2e%2e/admin", "/admin/.;/",
    "/admin/..;/", "/admin/..%2fadmin", "/admin/%2e%2e%2fadmin",
    "/./admin", "/.//admin", "//admin", "///admin", "/%2e/admin",
    "/admin%00", "/admin%20", "/admin%09", "/admin?", "/admin#",
]

# ============================================================
# TELNET
# ============================================================

TELNET_OPCOES = [1, 3, 5, 24, 31, 32, 33, 34, 35, 36, 37, 38, 39]
TELNET_IAC = 255
TELNET_DONT = 254
TELNET_DO = 253
TELNET_WONT = 252
TELNET_WILL = 251
TELNET_SB = 250
TELNET_SE = 240
TELNET_NOP = 241

# ============================================================
# DNS
# ============================================================

DNS_TIPOS = {
    "A": 1, "NS": 2, "CNAME": 5, "SOA": 6, "PTR": 12, "MX": 15,
    "TXT": 16, "AAAA": 28, "SRV": 33, "ANY": 255,
}
DNS_CLASSES = {"IN": 1, "CH": 3, "HS": 4, "ANY": 255}
DNS_RCODES = {
    0: "NOERROR", 1: "FORMERR", 2: "SERVFAIL", 3: "NXDOMAIN",
    4: "NOTIMP", 5: "REFUSED",
}
DNS_SERVER_PADRAO = "8.8.8.8"
DNS_PORTAS = [53, 5353]

# ============================================================
# DNS REBINDING
# ============================================================

DNS_REBIND_TTL_CURTO = 1
DNS_REBIND_TTL_MEDIO = 5
DNS_REBIND_TTL_LONGO = 60
DNS_REBIND_DOMINIOS = [
    "rebind.network", "1u.ms", "nip.io", "sslip.io",
    "xip.io", "vcap.me", "lvh.me", "localtest.me",
]
DNS_REBIND_PAYLOADS = [
    "127.0.0.1", "localhost", "0.0.0.0", "0", "[::1]",
    "127.1", "127.0.1", "2130706433", "0177.0.0.1",
    "0x7f.0.0.1", "127.0.0.1.nip.io", "127.0.0.1.sslip.io",
]

# ============================================================
# FINGERPRINT (TEMPORAL / ENTROPIA / NEGATIVE)
# ============================================================

FINGERPRINT_AMOSTRAS = 100
FINGERPRINT_VARIANCIA_MIN = 0.1
FINGERPRINT_VARIANCIA_MAX = 10.0
FINGERPRINT_ENTROPIA_MIN = 0.0
FINGERPRINT_ENTROPIA_MAX = 8.0
FINGERPRINT_LATENCIA_LAN = (0.1, 5.0)
FINGERPRINT_LATENCIA_WAN = (10.0, 300.0)
FINGERPRINT_LATENCIA_SUSPEITA = 0.05
FINGERPRINT_LATENCIA_HONEYPOT = 0.01

FINGERPRINT_MODELOS = {
    "zte_f6600p": {
        "vendor": "ZTE", "tipo": "ONT GPON",
        "portas": [53, 80, 443, 52869],
        "certificado": "ZTE", "upnp": "Portable SDK for UPnP devices/2.0.01",
        "latencia_tipica": 1.5,
    },
    "huawei_hg8245": {
        "vendor": "Huawei", "tipo": "ONT GPON",
        "portas": [23, 53, 80, 443, 7547],
        "certificado": "Huawei", "upnp": "Huawei",
        "latencia_tipica": 2.0,
    },
    "tp_link_archer": {
        "vendor": "TP-Link", "tipo": "Router",
        "portas": [23, 80, 443, 1900],
        "certificado": "TP-Link", "upnp": "TP-Link",
        "latencia_tipica": 3.0,
    },
    "mikrotik_routeros": {
        "vendor": "MikroTik", "tipo": "Router",
        "portas": [22, 23, 80, 443, 8291],
        "certificado": "MikroTik", "upnp": "MikroTik",
        "latencia_tipica": 1.0,
    },
    "cisco_ios": {
        "vendor": "Cisco", "tipo": "Router",
        "portas": [22, 23, 80, 443, 161],
        "certificado": "Cisco", "upnp": "",
        "latencia_tipica": 5.0,
    },
    "openwrt_generic": {
        "vendor": "OpenWrt", "tipo": "Router",
        "portas": [22, 80, 443, 1900],
        "certificado": "OpenWrt", "upnp": "Portable SDK for UPnP devices",
        "latencia_tipica": 2.0,
    },
}

# ============================================================
# HONEYPOT DETECTION
# ============================================================

HONEYPOT_SCORE_LIMITE = 0.7
HONEYPOT_FEATURES = [
    "latencia_baixa", "resposta_consistente", "versao_antiga",
    "certificado_auto_assinado", "dns_reverso_vazio",
    "asn_residencial", "timezone_inconsistente",
    "padrao_erro", "resposta_perfeita",
]
HONEYPOT_PESOS = {
    "latencia_baixa": 0.20, "resposta_consistente": 0.15,
    "versao_antiga": 0.10, "certificado_auto_assinado": 0.05,
    "dns_reverso_vazio": 0.10, "asn_residencial": 0.05,
    "timezone_inconsistente": 0.10, "padrao_erro": 0.15,
    "resposta_perfeita": 0.10,
}

# ============================================================
# FUZZING
# ============================================================

FUZZ_ITERACOES = 10000
FUZZ_SEMENTE = 0xB1F4
FUZZ_MAX_INPUT = 65536
FUZZ_MIN_INPUT = 0
FUZZ_RESONANCE_AMOSTRAS = 1000
FUZZ_RESONANCE_FFT_JANELA = 256
FUZZ_RESONANCE_LIMIAR = 0.3
FUZZ_NULLSPACE_BYTES = [0x00, 0x41, 0x7F, 0xFF, 0x0A, 0x0D, 0x20]
FUZZ_METAMORPH_REGRAS = {
    "sql": ["SELECT * FROM {t}", "SELECT * FROM (SELECT * FROM {t}) AS x",
            "SELECT * FROM {t} WHERE 1=1", "SELECT * FROM {t} UNION SELECT * FROM {t}"],
    "http": ["GET /{p} HTTP/1.1", "GET /{p} HTTP/1.0", "GET /{p} HTTP/2",
             "GET /{p}?x=1 HTTP/1.1", "GET /{p}#x HTTP/1.1"],
    "json": ['{"k":"v"}', '{"k": "v"}', '{"k" : "v"}', '{"k":"v","k":"v"}',
             '{"k":{"k":"v"}}', '[{"k":"v"}]'],
    "xml": ["<r><k>v</k></r>", "<r><k>v</k><k>v</k></r>", "<r><k/></r>",
            "<?xml version='1.0'?><r><k>v</k></r>"],
    "js": ["alert(1)", "eval('1')", "Function('return 1')()",
           "setTimeout('1',0)", "atob('MQ==')"],
}

# ============================================================
# DICIONARIOS
# ============================================================

DIC_CREDENCIAIS = [
    ("admin", "admin"), ("admin", ""), ("admin", "password"),
    ("admin", "1234"), ("admin", "12345"), ("admin", "123456"),
    ("admin", "admin123"), ("admin", "root"), ("admin", "toor"),
    ("root", "root"), ("root", ""), ("root", "password"),
    ("root", "1234"), ("root", "12345"), ("root", "123456"),
    ("root", "admin"), ("root", "toor"), ("root", "Zte521"),
    ("root", "zte521"), ("root", "ZTE521"), ("root", "huawei"),
    ("root", "vizxv"), ("root", "xc3511"), ("root", "hi3518"),
    ("root", "juantech"), ("root", "888888"), ("root", "54321"),
    ("root", "7ujMko0admin"), ("root", "anko"), ("root", "realtek"),
    ("root", "solokey"), ("root", "system"), ("root", "default"),
    ("root", "user"), ("root", "guest"), ("root", "test"),
    ("support", "support"), ("user", "user"), ("guest", "guest"),
    ("supervisor", "supervisor"), ("manager", "manager"),
    ("cisco", "cisco"), ("ubnt", "ubnt"), ("pi", "raspberry"),
    ("admin", "5up"), ("admin", "Zte521"), ("admin", "zte521"),
]

DIC_UPNP_DESCRICAO = ["ByP4ss", "libupnp", "MiniUPnPd", "upnp", "igd"]
DIC_PORTS_WORDLIST = [22, 23, 53, 80, 443, 1900, 2000, 5000, 52869, 7547, 8080, 8443]

DIC_TELNET_PROMPTS = [b"login:", b"Login:", b"LOGIN:", b"Username:", b"User:",
                      b"user:", b"#", b"$", b">", b"Password:", b"password:"]

# ============================================================
# STATUS CODES
# ============================================================

STATUS_OK = 0
STATUS_ERRO = 1
STATUS_TIMEOUT = 2
STATUS_RECUSADO = 3
STATUS_FILTRADO = 4
STATUS_FECHADO = 5
STATUS_ABERTO = 6
STATUS_SUSPEITO = 7
STATUS_VULNERAVEL = 8
STATUS_EXPLORADO = 9
STATUS_HONEYPOT = 10

STATUS_NOMES = {
    0: "OK", 1: "ERRO", 2: "TIMEOUT", 3: "RECUSADO", 4: "FILTRADO",
    5: "FECHADO", 6: "ABERTO", 7: "SUSPEITO", 8: "VULNERAVEL",
    9: "EXPLORADO", 10: "HONEYPOT",
}

# ============================================================
# SEVERIDADE
# ============================================================

SEV_CRITICA = "critica"
SEV_ALTA = "alta"
SEV_MEDIA = "media"
SEV_BAIXA = "baixa"
SEV_INFO = "info"

SEV_PESOS = {"critica": 10, "alta": 7, "media": 4, "baixa": 2, "info": 1}

SEV_CORES = {"critica": 196, "alta": 208, "media": 220, "baixa": 46, "info": 39}

# ============================================================
# PATH E DIRETORIOS
# ============================================================

DIR_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_TMP = os.path.join(DIR_RAIZ, "tmp")
DIR_REPORTS = os.path.join(DIR_RAIZ, "reports")
DIR_LOGS = os.path.join(DIR_RAIZ, "logs")
DIR_CACHE = os.path.join(DIR_RAIZ, "cache")

ARQ_LOG = "byp4ss.log"
ARQ_FINDINGS = "findings.json"
ARQ_EXPORT_JSON = "report.json"
ARQ_EXPORT_MD = "report.md"
ARQ_EXPORT_CSV = "report.csv"

# ============================================================
# FIM DAS CONSTANTES
# ============================================================

# ============================================================
# CLASSE CONSTANTS (agrupa tudo como atributos)
# ============================================================

class Constants:
    VERSAO = VERSAO
    NOME = NOME
    AUTOR = AUTOR
    ANO = ANO

    ALVO_PADRAO = ALVO_PADRAO
    ALVO_LOCALHOST = ALVO_LOCALHOST
    ALVO_BROADCAST = ALVO_BROADCAST

    PORTAS_CRITICAS = PORTAS_CRITICAS
    PORTAS_TELNET = PORTAS_TELNET
    PORTAS_SSH = PORTAS_SSH
    PORTAS_HTTP = PORTAS_HTTP
    PORTAS_HTTPS = PORTAS_HTTPS
    PORTAS_DNS = PORTAS_DNS
    PORTAS_UPNP = PORTAS_UPNP
    PORTAS_TR069 = PORTAS_TR069
    PORTAS_SNMP = PORTAS_SNMP
    PORTAS_TODAS = PORTAS_TODAS

    TIMEOUT_SSDP = TIMEOUT_SSDP
    TIMEOUT_TCP = TIMEOUT_TCP
    TIMEOUT_UDP = TIMEOUT_UDP
    TIMEOUT_HTTP = TIMEOUT_HTTP
    TIMEOUT_HTTPS = TIMEOUT_HTTPS
    TIMEOUT_TELNET = TIMEOUT_TELNET
    TIMEOUT_SSH = TIMEOUT_SSH
    TIMEOUT_DNS = TIMEOUT_DNS
    TIMEOUT_UPNP = TIMEOUT_UPNP
    TIMEOUT_VERIFY = TIMEOUT_VERIFY
    TIMEOUT_PADRAO = TIMEOUT_PADRAO

    THREADS_PADRAO = THREADS_PADRAO
    THREADS_PORTS = THREADS_PORTS
    THREADS_FUZZ = THREADS_FUZZ
    THREADS_BRUTE = THREADS_BRUTE
    THREADS_MAX = THREADS_MAX

    SSDP_MULTICAST = SSDP_MULTICAST
    SSDP_PORTA = SSDP_PORTA
    SSDP_M_SEARCH = SSDP_M_SEARCH
    SSDP_M_SEARCH_IGD = SSDP_M_SEARCH_IGD
    SSDP_M_SEARCH_WAN = SSDP_M_SEARCH_WAN

    UPNP_NS_WANIP = UPNP_NS_WANIP
    UPNP_NS_WANPPP = UPNP_NS_WANPPP
    UPNP_NS_LAYER3 = UPNP_NS_LAYER3
    UPNP_NS_DEVICE = UPNP_NS_DEVICE
    UPNP_NS_WANDEVICE = UPNP_NS_WANDEVICE
    UPNP_ACOES = UPNP_ACOES
    UPNP_SOAP_HEADER = UPNP_SOAP_HEADER
    UPNP_SOAP_FOOTER = UPNP_SOAP_FOOTER
    UPNP_ADD_MAPPING = UPNP_ADD_MAPPING
    UPNP_DELETE_MAPPING = UPNP_DELETE_MAPPING
    UPNP_STATUS_OK = UPNP_STATUS_OK
    UPNP_STATUS_ERRO = UPNP_STATUS_ERRO
    UPNP_LEASE_0 = UPNP_LEASE_0
    UPNP_LEASE_1H = UPNP_LEASE_1H
    UPNP_LEASE_24H = UPNP_LEASE_24H
    UPNP_LEASE_7D = UPNP_LEASE_7D

    HTTP_METODOS = HTTP_METODOS
    HTTP_USER_AGENTS = HTTP_USER_AGENTS
    HTTP_HEADERS_PADRAO = HTTP_HEADERS_PADRAO
    HTTP_PATHS_ADMIN = HTTP_PATHS_ADMIN
    HTTP_PATHS_TRAVERSAL = HTTP_PATHS_TRAVERSAL

    TELNET_OPCOES = TELNET_OPCOES
    TELNET_IAC = TELNET_IAC
    TELNET_DONT = TELNET_DONT
    TELNET_DO = TELNET_DO
    TELNET_WONT = TELNET_WONT
    TELNET_WILL = TELNET_WILL
    TELNET_SB = TELNET_SB
    TELNET_SE = TELNET_SE
    TELNET_NOP = TELNET_NOP

    DNS_TIPOS = DNS_TIPOS
    DNS_CLASSES = DNS_CLASSES
    DNS_RCODES = DNS_RCODES
    DNS_SERVER_PADRAO = DNS_SERVER_PADRAO
    DNS_PORTAS = DNS_PORTAS

    DNS_REBIND_TTL_CURTO = DNS_REBIND_TTL_CURTO
    DNS_REBIND_TTL_MEDIO = DNS_REBIND_TTL_MEDIO
    DNS_REBIND_TTL_LONGO = DNS_REBIND_TTL_LONGO
    DNS_REBIND_DOMINIOS = DNS_REBIND_DOMINIOS
    DNS_REBIND_PAYLOADS = DNS_REBIND_PAYLOADS

    FINGERPRINT_AMOSTRAS = FINGERPRINT_AMOSTRAS
    FINGERPRINT_VARIANCIA_MIN = FINGERPRINT_VARIANCIA_MIN
    FINGERPRINT_VARIANCIA_MAX = FINGERPRINT_VARIANCIA_MAX
    FINGERPRINT_ENTROPIA_MIN = FINGERPRINT_ENTROPIA_MIN
    FINGERPRINT_ENTROPIA_MAX = FINGERPRINT_ENTROPIA_MAX
    FINGERPRINT_LATENCIA_LAN = FINGERPRINT_LATENCIA_LAN
    FINGERPRINT_LATENCIA_WAN = FINGERPRINT_LATENCIA_WAN
    FINGERPRINT_LATENCIA_SUSPEITA = FINGERPRINT_LATENCIA_SUSPEITA
    FINGERPRINT_LATENCIA_HONEYPOT = FINGERPRINT_LATENCIA_HONEYPOT
    FINGERPRINT_MODELOS = FINGERPRINT_MODELOS

    HONEYPOT_SCORE_LIMITE = HONEYPOT_SCORE_LIMITE
    HONEYPOT_FEATURES = HONEYPOT_FEATURES
    HONEYPOT_PESOS = HONEYPOT_PESOS

    FUZZ_ITERACOES = FUZZ_ITERACOES
    FUZZ_SEMENTE = FUZZ_SEMENTE
    FUZZ_MAX_INPUT = FUZZ_MAX_INPUT
    FUZZ_MIN_INPUT = FUZZ_MIN_INPUT
    FUZZ_RESONANCE_AMOSTRAS = FUZZ_RESONANCE_AMOSTRAS
    FUZZ_RESONANCE_FFT_JANELA = FUZZ_RESONANCE_FFT_JANELA
    FUZZ_RESONANCE_LIMIAR = FUZZ_RESONANCE_LIMIAR
    FUZZ_NULLSPACE_BYTES = FUZZ_NULLSPACE_BYTES
    FUZZ_METAMORPH_REGRAS = FUZZ_METAMORPH_REGRAS

    DIC_CREDENCIAIS = DIC_CREDENCIAIS
    DIC_UPNP_DESCRICAO = DIC_UPNP_DESCRICAO
    DIC_PORTS_WORDLIST = DIC_PORTS_WORDLIST
    DIC_TELNET_PROMPTS = DIC_TELNET_PROMPTS

    STATUS_OK = STATUS_OK
    STATUS_ERRO = STATUS_ERRO
    STATUS_TIMEOUT = STATUS_TIMEOUT
    STATUS_RECUSADO = STATUS_RECUSADO
    STATUS_FILTRADO = STATUS_FILTRADO
    STATUS_FECHADO = STATUS_FECHADO
    STATUS_ABERTO = STATUS_ABERTO
    STATUS_SUSPEITO = STATUS_SUSPEITO
    STATUS_VULNERAVEL = STATUS_VULNERAVEL
    STATUS_EXPLORADO = STATUS_EXPLORADO
    STATUS_HONEYPOT = STATUS_HONEYPOT
    STATUS_NOMES = STATUS_NOMES

    SEV_CRITICA = SEV_CRITICA
    SEV_ALTA = SEV_ALTA
    SEV_MEDIA = SEV_MEDIA
    SEV_BAIXA = SEV_BAIXA
    SEV_INFO = SEV_INFO
    SEV_PESOS = SEV_PESOS
    SEV_CORES = SEV_CORES

    DIR_RAIZ = DIR_RAIZ
    DIR_TMP = DIR_TMP
    DIR_REPORTS = DIR_REPORTS
    DIR_LOGS = DIR_LOGS
    DIR_CACHE = DIR_CACHE

    ARQ_LOG = ARQ_LOG
    ARQ_FINDINGS = ARQ_FINDINGS
    ARQ_EXPORT_JSON = ARQ_EXPORT_JSON
    ARQ_EXPORT_MD = ARQ_EXPORT_MD
    ARQ_EXPORT_CSV = ARQ_EXPORT_CSV
