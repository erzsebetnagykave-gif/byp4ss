# Base de credenciais do K1ELI (parte 1 de 2)
# 300 linhas de credenciais conhecidas (fabricantes, firmware, vazamentos)
# Sem hardcoded no codigo do brute force — o K1ELI le daqui

BASE = {}

# ============================================================
# ZTE (F6600P, F670L, H298A, etc)
# ============================================================

BASE["zte"] = [
    ("admin", "admin"), ("admin", "Zte521"), ("admin", "zte521"),
    ("admin", "ZTE521"), ("admin", "1234"), ("admin", "12345"),
    ("admin", "123456"), ("admin", "admin123"), ("admin", "password"),
    ("admin", ""), ("root", "root"), ("root", "Zte521"),
    ("root", "zte521"), ("root", "admin"), ("root", "password"),
    ("root", ""), ("user", "user"), ("user", "Zte521"),
    ("support", "support"), ("zte", "zte"), ("ZTE", "ZTE"),
    ("admin", "zte"), ("guest", "guest"), ("telecom", "telecom"),
]

# ============================================================
# HUAWEI (HG8245, HG8145, HG8247, etc)
# ============================================================

BASE["huawei"] = [
    ("admin", "admin"), ("admin", "Admin@huawei"), ("admin", "Admin@123"),
    ("admin", "huawei"), ("admin", "Huawei@123"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "password"),
    ("admin", ""), ("root", "root"), ("root", "admin"),
    ("root", "huawei"), ("root", "Huawei@123"), ("root", "password"),
    ("telecomadmin", "admintelecom"), ("telecomadmin", "nE7jA%5m"),
    ("telecomadmin", "telecomadmin"), ("telecomadmin", "admintelecom"),
    ("telecomadmin", "Admin@huawei"), ("telecomadmin", "12345678"),
    ("telecom", "telecom"), ("user", "user"), ("guest", "guest"),
    ("CMCCAdmin", "aDm8H%MdA"), ("CMCCAdmin", "admin"),
    ("CUAdmin", "CUAdmin"), ("CUAdmin", "CUAdmin@123"),
]

# ============================================================
# TP-LINK (Archer, TL-WR, TL-WR940N, etc)
# ============================================================

BASE["tplink"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "12345678"),
    ("admin", ""), ("admin", "tplink"), ("admin", "TP-Link"),
    ("admin", "Admin@123"), ("admin", "admin123"), ("admin", "root"),
    ("root", "root"), ("root", "admin"), ("root", ""),
    ("user", "user"), ("guest", "guest"),
]

# ============================================================
# D-LINK (DIR-*, DSL-*, etc)
# ============================================================

BASE["dlink"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", ""),
    ("admin", "1234"), ("admin", "12345"), ("admin", "123456"),
    ("admin", "12345678"), ("admin", "dlink"), ("admin", "d-link"),
    ("admin", "Admin"), ("root", "root"), ("root", "admin"),
    ("user", "user"), ("guest", "guest"), ("support", "support"),
]

# ============================================================
# CISCO (RV, WAG, EPC, etc)
# ============================================================

BASE["cisco"] = [
    ("admin", "admin"), ("admin", "cisco"), ("admin", "Cisco"),
    ("admin", "password"), ("admin", "1234"), ("admin", "12345"),
    ("admin", "123456"), ("admin", ""), ("cisco", "cisco"),
    ("cisco", "Cisco"), ("root", "root"), ("root", "cisco"),
    ("user", "user"), ("guest", "guest"),
]

# ============================================================
# MIKROTIK (RouterOS, hEX, etc)
# ============================================================

BASE["mikrotik"] = [
    ("admin", ""), ("admin", "admin"), ("admin", "password"),
    ("admin", "1234"), ("admin", "12345"), ("admin", "123456"),
    ("admin", "mikrotik"), ("admin", "MikroTik"), ("root", "root"),
    ("root", "admin"), ("user", "user"), ("guest", "guest"),
]

# ============================================================
# NETGEAR (R*, D*, WNDR*, etc)
# ============================================================

BASE["netgear"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "12345678"),
    ("admin", ""), ("admin", "netgear"), ("admin", "Netgear"),
    ("admin", "Admin@123"), ("root", "root"), ("root", "admin"),
    ("user", "user"), ("guest", "guest"),
]

# ============================================================
# ASUS (RT-*, DSL-*, etc)
# ============================================================

BASE["asus"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", ""),
    ("admin", "asus"), ("admin", "Asus"), ("root", "root"),
    ("root", "admin"), ("user", "user"), ("guest", "guest"),
]

# ============================================================
# LINKSYS (EA*, WRT*, etc)
# ============================================================

BASE["linksys"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", ""), ("admin", "linksys"), ("admin", "Linksys"),
    ("root", "root"), ("root", "admin"), ("user", "user"),
    ("guest", "guest"),
]

# ============================================================
# UBIQUITI (UniFi, EdgeRouter, etc)
# ============================================================

BASE["ubiquiti"] = [
    ("ubnt", "ubnt"), ("admin", "admin"), ("admin", "ubnt"),
    ("root", "root"), ("root", "ubnt"), ("admin", "password"),
    ("admin", "1234"), ("admin", "12345"), ("admin", "123456"),
    ("admin", ""), ("user", "user"), ("guest", "guest"),
]

# ============================================================
# RUCKUS (ZoneDirector, R*, etc)
# ============================================================

BASE["ruckus"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "ruckus"),
    ("admin", "Ruckus"), ("admin", "Ruckus1"), ("admin", ""),
    ("root", "root"), ("user", "user"), ("guest", "guest"),
]

# ============================================================
# ARUBA (Instant, OS, etc)
# ============================================================

BASE["aruba"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "aruba"),
    ("admin", "Aruba"), ("admin", "Aruba123"), ("admin", ""),
    ("root", "root"), ("user", "user"), ("guest", "guest"),
]

# ============================================================
# FORTINET (FortiGate, FortiWiFi, etc)
# ============================================================

BASE["fortinet"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "fortinet"),
    ("admin", "Fortinet"), ("admin", "Fortinet123"), ("admin", ""),
    ("maintainer", "maintainer"), ("maintainer", "bcpbFGFN+"),
    ("admin", "Admin@123"), ("admin", "fortigate"),
]

# ============================================================
# PFSENSE (firewall)
# ============================================================

BASE["pfsense"] = [
    ("admin", "pfsense"), ("admin", "PfSense"), ("admin", "password"),
    ("admin", "admin"), ("admin", ""), ("root", "root"),
    ("root", "pfsense"),
]

# ============================================================
# OPNSENSE (firewall)
# ============================================================

BASE["opnsense"] = [
    ("root", "opnsense"), ("root", "Opnsense"), ("root", "password"),
    ("root", "root"), ("root", ""), ("admin", "admin"),
]

# ============================================================
# PFBOXE (firewall alternativo)
# ============================================================

BASE["pfsense_alt"] = [
    ("admin", "pfSense"), ("admin", "pfsense"), ("admin", "admin"),
]

# ============================================================
# ZYXEL (NBG, VMG, etc)
# ============================================================

BASE["zyxel"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "zyxel"),
    ("admin", "Zyxel"), ("admin", ""), ("root", "root"),
    ("root", "zyxel"),
]

# ============================================================
# TECHNICOLOR (TG*, etc)
# ============================================================

BASE["technicolor"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "technicolor"),
    ("admin", "1234"), ("admin", "12345"), ("admin", ""),
    ("root", "root"), ("user", "user"),
]

# ============================================================
# SAGEMCOM (F*, etc)
# ============================================================

BASE["sagemcom"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "sagemcom"),
    ("admin", "1234"), ("admin", "12345"), ("admin", "123456"),
    ("admin", ""), ("root", "root"),
]

# ============================================================
# NOKIA (Alcatel, etc)
# ============================================================

BASE["nokia"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "nokia"),
    ("admin", "Nokia"), ("admin", "1234"), ("admin", "12345"),
    ("admin", ""), ("root", "root"),
]

# ============================================================
# ALCATEL (Home, etc)
# ============================================================

BASE["alcatel"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "alcatel"),
    ("admin", "Alcatel"), ("admin", "1234"), ("admin", "12345"),
    ("admin", ""), ("root", "root"),
]

# ============================================================
# FIBERHOME (HG*, etc)
# ============================================================

BASE["fiberhome"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "fiberhome"),
    ("admin", "Fiberhome"), ("admin", "1234"), ("admin", "12345"),
    ("admin", "123456"), ("admin", ""), ("root", "root"),
    ("telecomadmin", "admintelecom"),
]

# ============================================================
# GENERICO — credenciais comuns em qualquer roteador
# ============================================================

BASE["generico"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "12345678"),
    ("admin", "admin123"), ("admin", "root"), ("admin", "toor"),
    ("admin", ""), ("admin", "Admin"), ("admin", "Password"),
    ("admin", "Admin@123"), ("admin", "P@ssw0rd"), ("admin", "P@ssword"),
    ("root", "root"), ("root", "toor"), ("root", "password"),
    ("root", "admin"), ("root", "1234"), ("root", "12345"),
    ("root", ""), ("user", "user"), ("user", "password"),
    ("user", "1234"), ("user", ""), ("guest", "guest"),
    ("guest", ""), ("guest", "password"), ("support", "support"),
    ("support", "password"), ("operator", "operator"),
    ("operator", "password"), ("test", "test"), ("test", "password"),
    ("demo", "demo"), ("public", "public"), ("private", "private"),
    ("cisco", "cisco"), ("cisco", "Cisco"), ("root", "Zte521"),
    ("root", "huawei"), ("admin", "Zte521"), ("admin", "huawei"),
]

# ============================================================
# DICIONARIO DE CREDENCIAIS DERIVADAS DO MAC
# (usado pelo generate cred from mac_prefix)
# ============================================================

BASE["mac_derivadas"] = [
    ("admin", "{mac_prefix}"),
    ("admin", "{mac_prefix}2020"),
    ("admin", "{mac_prefix}2021"),
    ("admin", "{mac_prefix}2022"),
    ("admin", "{mac_prefix}2023"),
    ("admin", "{mac_prefix}2024"),
    ("admin", "{mac_prefix}admin"),
    ("admin", "admin{mac_prefix}"),
    ("root", "{mac_prefix}"),
    ("root", "{mac_prefix}2021"),
    ("user", "{mac_prefix}"),
]

# ============================================================
# DICIONARIO DE CREDENCIAIS DERIVADAS DO SERIAL
# (usado pelo generate cred from serial_prefix)
# ============================================================

BASE["serial_derivadas"] = [
    ("admin", "{serial_prefix}"),
    ("admin", "{serial_prefix}2020"),
    ("admin", "{serial_prefix}2021"),
    ("admin", "{serial_prefix}2022"),
    ("admin", "{serial_prefix}2023"),
    ("admin", "{serial_prefix}2024"),
    ("admin", "{serial_prefix}admin"),
    ("admin", "admin{serial_prefix}"),
    ("root", "{serial_prefix}"),
    ("root", "{serial_prefix}2021"),
]

# ============================================================
# DICIONARIO DE CREDENCIAIS DERIVADAS DO ANO
# (usado pelo generate year)
# ============================================================

BASE["ano_derivadas"] = [
    ("admin", "2018"), ("admin", "2019"), ("admin", "2020"),
    ("admin", "2021"), ("admin", "2022"), ("admin", "2023"),
    ("admin", "2024"), ("admin", "2025"), ("admin", "2026"),
    ("root", "2018"), ("root", "2019"), ("root", "2020"),
    ("root", "2021"), ("root", "2022"), ("root", "2023"),
    ("root", "2024"), ("root", "2025"), ("root", "2026"),
]

# ============================================================
# PADROES COMUNS (para generate cred from common_patterns)
# ============================================================

BASE["padroes_comuns"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "12345678"),
    ("admin", "admin123"), ("admin", "Admin@123"), ("admin", ""),
    ("root", "root"), ("root", "toor"), ("root", "password"),
    ("root", "admin"), ("root", ""), ("user", "user"),
    ("guest", "guest"), ("support", "support"), ("test", "test"),
]

# ============================================================
# FIM DA BASE DE CREDENCIAIS (parte 1 de 2)
# ============================================================

def Estatisticas():
    Total = 0
    Por_Fabricante = {}
    for Fabricante, Lista in BASE.items():
        Total += len(Lista)
        Por_Fabricante[Fabricante] = len(Lista)
    return {
        "total": Total,
        "fabricantes": len(BASE),
        "por_fabricante": Por_Fabricante,
    }

# ============================================================
# PARTE 2 — VAZAMENTOS, FIRMWARE, OPERADORAS, IOT, SCADA
# ============================================================

# ============================================================
# VAZAMENTOS REAIS (Collection#1, RockYou, AntiPublic, Cit0day)
# Top 100 senhas mais comuns (posição real dos leaks)
# ============================================================

BASE["vazamentos_top100"] = [
    ("admin", "123456"), ("admin", "password"), ("admin", "12345678"),
    ("admin", "qwerty"), ("admin", "123456789"), ("admin", "12345"),
    ("admin", "1234"), ("admin", "111111"), ("admin", "1234567"),
    ("admin", "dragon"), ("admin", "123123"), ("admin", "baseball"),
    ("admin", "abc123"), ("admin", "football"), ("admin", "monkey"),
    ("admin", "letmein"), ("admin", "696969"), ("admin", "shadow"),
    ("admin", "master"), ("admin", "666666"), ("admin", "qwertyuiop"),
    ("admin", "123321"), ("admin", "mustang"), ("admin", "1234567890"),
    ("admin", "michael"), ("admin", "654321"), ("admin", "pussy"),
    ("admin", "superman"), ("admin", "1qaz2wsx"), ("admin", "7777777"),
    ("admin", "fuckyou"), ("admin", "121212"), ("admin", "000000"),
    ("admin", "qazwsx"), ("admin", "123qwe"), ("admin", "killer"),
    ("admin", "trustno1"), ("admin", "jordan"), ("admin", "jennifer"),
    ("admin", "zxcvbnm"), ("admin", "asdfgh"), ("admin", "hunter"),
    ("admin", "buster"), ("admin", "soccer"), ("admin", "harley"),
    ("admin", "batman"), ("admin", "andrew"), ("admin", "tigger"),
    ("admin", "sunshine"), ("admin", "iloveyou"), ("admin", "fuckme"),
    ("admin", "2000"), ("admin", "charlie"), ("admin", "robert"),
    ("admin", "thomas"), ("admin", "hockey"), ("admin", "ranger"),
    ("admin", "daniel"), ("admin", "starwars"), ("admin", "klaster"),
    ("admin", "112233"), ("admin", "george"), ("admin", "asshole"),
    ("admin", "computer"), ("admin", "michelle"), ("admin", "jessica"),
    ("admin", "pepper"), ("admin", "1111"), ("admin", "zxcvbn"),
    ("admin", "555555"), ("admin", "11111111"), ("admin", "131313"),
    ("admin", "freedom"), ("admin", "777777"), ("admin", "pass"),
    ("admin", "fuck"), ("admin", "maggie"), ("admin", "159753"),
    ("admin", "aaaaaa"), ("admin", "ginger"), ("admin", "princess"),
    ("admin", "joshua"), ("admin", "cheese"), ("admin", "amanda"),
    ("admin", "summer"), ("admin", "love"), ("admin", "ashley"),
    ("admin", "6969"), ("admin", "nicole"), ("admin", "chelsea"),
    ("admin", "biteme"), ("admin", "matthew"), ("admin", "access"),
    ("admin", "yankees"), ("admin", "987654321"), ("admin", "dallas"),
    ("admin", "austin"), ("admin", "thunder"), ("admin", "taylor"),
    ("admin", "matrix"), ("admin", "william"), ("admin", "corvette"),
    ("admin", "hello"), ("admin", "martin"), ("admin", "heather"),
    ("admin", "secret"), ("admin", "fucker"), ("admin", "merlin"),
    ("admin", "diamond"), ("admin", "1234qwer"), ("admin", "gfhjkm"),
    ("admin", "hammer"), ("admin", "silver"), ("admin", "222222"),
    ("admin", "88888888"), ("admin", "anthony"), ("admin", "justin"),
    ("admin", "test"), ("admin", "bailey"), ("admin", "q1w2e3r4t5"),
    ("admin", "patrick"), ("admin", "internet"), ("admin", "scooter"),
    ("admin", "orange"), ("admin", "11111"), ("admin", "golfer"),
    ("admin", "cookie"), ("admin", "richard"), ("admin", "samantha"),
    ("admin", "bigdog"), ("admin", "guitar"), ("admin", "jackson"),
    ("admin", "whatever"), ("admin", "mickey"), ("admin", "chicken"),
    ("admin", "sparky"), ("admin", "snoopy"), ("admin", "maverick"),
    ("admin", "phoenix"), ("admin", "camaro"), ("admin", "sexy"),
    ("admin", "peanut"), ("admin", "morgan"), ("admin", "welcome"),
    ("admin", "falcon"), ("admin", "cowboy"), ("admin", "ferrari"),
    ("admin", "samsung"), ("admin", "andrea"), ("admin", "smokey"),
    ("admin", "steelers"), ("admin", "joseph"), ("admin", "mercedes"),
    ("admin", "dakota"), ("admin", "arsenal"), ("admin", "eagles"),
    ("admin", "melissa"), ("admin", "boomer"), ("admin", "booboo"),
    ("admin", "spider"), ("admin", "nascar"), ("admin", "monster"),
    ("admin", "tigers"), ("admin", "yellow"), ("admin", "xxxxxx"),
    ("admin", "123123123"), ("admin", "gateway"), ("admin", "marina"),
    ("admin", "diablo"), ("admin", "bulldog"), ("admin", "qwer1234"),
    ("admin", "compaq"), ("admin", "purple"), ("admin", "hardcore"),
    ("admin", "banana"), ("admin", "junior"), ("admin", "hannah"),
    ("admin", "123654"), ("admin", "porsche"), ("admin", "lakers"),
    ("admin", "iceman"), ("admin", "money"), ("admin", "cowboys"),
    ("admin", "987654"), ("admin", "london"), ("admin", "tennis"),
    ("admin", "999999"), ("admin", "ncc1701"), ("admin", "coffee"),
    ("admin", "scooby"), ("admin", "0000"), ("admin", "miller"),
    ("admin", "boston"), ("admin", "q1w2e3r4"), ("admin", "fuckoff"),
    ("admin", "brandon"), ("admin", "yamaha"), ("admin", "chester"),
    ("admin", "mother"), ("admin", "forever"), ("admin", "johnny"),
    ("admin", "edward"), ("admin", "333333"), ("admin", "oliver"),
    ("admin", "redsox"), ("admin", "player"), ("admin", "nikita"),
    ("admin", "knight"), ("admin", "fender"), ("admin", "barney"),
    ("admin", "midnight"), ("admin", "please"), ("admin", "brandy"),
    ("admin", "chicago"), ("admin", "badboy"), ("admin", "iwantu"),
    ("admin", "slayer"), ("admin", "rangers"), ("admin", "charles"),
    ("admin", "angel"), ("admin", "flower"), ("admin", "bigdaddy"),
    ("admin", "rabbit"), ("admin", "wizard"), ("admin", "bigdick"),
    ("admin", "jasper"), ("admin", "enter"), ("admin", "rachel"),
    ("admin", "chris"), ("admin", "steven"), ("admin", "winner"),
    ("admin", "adidas"), ("admin", "victoria"), ("admin", "natasha"),
    ("admin", "1q2w3e4r"), ("admin", "jasmine"), ("admin", "winter"),
    ("admin", "prince"), ("admin", "panties"), ("admin", "marine"),
    ("admin", "ghbdtn"), ("admin", "fishing"), ("admin", "cocacola"),
    ("admin", "casper"), ("admin", "james"), ("admin", "232323"),
    ("admin", "raiders"), ("admin", "888888"), ("admin", "marlboro"),
    ("admin", "gandalf"), ("admin", "asdfasdf"), ("admin", "crystal"),
    ("admin", "87654321"), ("admin", "12344321"), ("admin", "sexsex"),
    ("admin", "golden"), ("admin", "blowme"), ("admin", "bigtits"),
    ("admin", "8675309"), ("admin", "panther"), ("admin", "lauren"),
    ("admin", "angela"), ("admin", "bitch"), ("admin", "spanky"),
    ("admin", "thx1138"), ("admin", "angels"), ("admin", "madison"),
    ("admin", "winston"), ("admin", "shannon"), ("admin", "mike"),
    ("admin", "toyota"), ("admin", "blondes"), ("admin", "sierra"),
    ("admin", "scorpio"), ("admin", "qwerty123"), ("admin", "rooster"),
    ("admin", "pepper"), ("admin", "virginia"), ("admin", "blazer"),
    ("admin", "tesla"), ("admin", "mountain"), ("admin", "1qazxsw2"),
    ("admin", "passwd"), ("admin", "danielle"), ("admin", "123abc"),
    ("admin", "casper"), ("admin", "dexter"), ("admin", "viking"),
    ("admin", "1234abcd"), ("admin", "sniper"), ("admin", "rebecca"),
    ("admin", "a123456"), ("admin", "passport"), ("admin", "vision"),
    ("admin", "hunter2"),
]

# ============================================================
# OPERADORAS BRASILEIRAS (Claro, Vivo, TIM, Oi)
# Credenciais de firmware de ONT/roteador fornecido por operadora
# ============================================================

BASE["operadoras_br"] = [
    # Claro / NET
    ("admin", "claro"), ("admin", "Claro"), ("admin", "CLARO"),
    ("admin", "net"), ("admin", "Net"), ("admin", "NET"),
    ("admin", "virtua"), ("admin", "Virtua"), ("admin", "VIRTUA"),
    ("admin", "claro123"), ("admin", "net123"), ("admin", "virtua123"),
    ("technician", "technician"), ("tech", "tech"),
    ("claro", "claro"), ("net", "net"),

    # Vivo / Telefonica / GVT
    ("admin", "vivo"), ("admin", "Vivo"), ("admin", "VIVO"),
    ("admin", "telefonica"), ("admin", "Telefonica"), ("admin", "TELEFONICA"),
    ("admin", "gvt"), ("admin", "Gvt"), ("admin", "GVT"),
    ("admin", "vivo123"), ("admin", "gvt123"),
    ("vivo", "vivo"), ("telefonica", "telefonica"),
    ("support", "support"), ("suporte", "suporte"),

    # TIM / Live TIM
    ("admin", "tim"), ("admin", "Tim"), ("admin", "TIM"),
    ("admin", "livetim"), ("admin", "LiveTim"), ("admin", "Live TIM"),
    ("admin", "tim123"), ("admin", "livetim123"),
    ("tim", "tim"),

    # Oi / Oi Fibra
    ("admin", "oi"), ("admin", "Oi"), ("admin", "OI"),
    ("admin", "oifibra"), ("admin", "OiFibra"), ("admin", "Oi Fibra"),
    ("admin", "oi123"), ("admin", "oifibra123"),
    ("oi", "oi"),

    # Algar / Sercomtel / Copel
    ("admin", "algar"), ("admin", "Algar"), ("admin", "ALGAR"),
    ("admin", "sercomtel"), ("admin", "Sercomtel"),
    ("admin", "copel"), ("admin", "Copel"),
]

# ============================================================
# FIRMWARE ESPECIFICO (por versao)
# ============================================================

BASE["firmware_2020"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "admin123"),
    ("admin", "Admin@123"), ("admin", ""), ("root", "root"),
    ("root", "toor"), ("root", "admin"), ("root", ""),
    ("user", "user"), ("guest", "guest"),
]

BASE["firmware_2021"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "12345678"),
    ("admin", "admin123"), ("admin", "Admin@123"), ("admin", "Admin@2021"),
    ("admin", ""), ("root", "root"), ("root", "toor"),
    ("root", "admin"), ("root", ""), ("user", "user"),
    ("guest", "guest"),
]

BASE["firmware_2022"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "12345678"),
    ("admin", "admin123"), ("admin", "Admin@123"), ("admin", "Admin@2022"),
    ("admin", "Admin@2021"), ("admin", ""), ("root", "root"),
    ("root", "toor"), ("root", "admin"), ("root", ""),
    ("user", "user"), ("guest", "guest"),
]

BASE["firmware_2023"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "12345678"),
    ("admin", "admin123"), ("admin", "Admin@123"), ("admin", "Admin@2023"),
    ("admin", "Admin@2022"), ("admin", ""), ("root", "root"),
    ("root", "toor"), ("root", "admin"), ("root", ""),
    ("user", "user"), ("guest", "guest"),
]

BASE["firmware_2024"] = [
    ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
    ("admin", "12345"), ("admin", "123456"), ("admin", "12345678"),
    ("admin", "admin123"), ("admin", "Admin@123"), ("admin", "Admin@2024"),
    ("admin", "Admin@2023"), ("admin", ""), ("root", "root"),
    ("root", "toor"), ("root", "admin"), ("root", ""),
    ("user", "user"), ("guest", "guest"),
]

# ============================================================
# IOT — CAMERAS, DVRs, NVRs, IMPRESSORAS, SMART TVs
# ============================================================

BASE["iot_cameras"] = [
    ("admin", "admin"), ("admin", "12345"), ("admin", "password"),
    ("admin", "admin123"), ("admin", "123456"), ("admin", ""),
    ("root", "root"), ("root", "admin"), ("root", "pass"),
    ("root", "password"), ("root", "12345"), ("root", "xc3511"),
    ("root", "vizxv"), ("root", "hi3518"), ("root", "hi3516"),
    ("root", "jvbzd"), ("root", "anko"), ("root", "zlxx."),
    ("root", "7ujMko0admin"), ("root", "system"), ("root", "ikwb"),
    ("root", "dreambox"), ("root", "user"), ("root", "realtek"),
    ("root", "00000000"), ("root", "meinsm"), ("admin", "meinsm"),
    ("admin", "xc3511"), ("admin", "vizxv"), ("admin", "hi3518"),
    ("admin", "888888"), ("admin", "666666"), ("admin", "supervisor"),
    ("supervisor", "supervisor"), ("supervisor", "zy123456"),
    ("supervisor", "system"), ("service", "service"),
    ("admin", "service"), ("root", "service"), ("default", "default"),
    ("guest", "guest"), ("guest", ""), ("admin", "guest"),
    ("user", "user"), ("user", "pass"), ("admin", "1111111"),
    ("admin", "1234"), ("admin", "123456789"), ("admin", "1234567890"),
    ("admin", "ipcam"), ("admin", "camera"), ("admin", "cam"),
    ("root", "camera"), ("root", "cam"), ("root", "ipcam"),
    ("admin", "swann"), ("admin", "swann123"), ("admin", "Swan"),
    ("admin", "dahua"), ("admin", "Dahua"), ("admin", "dahua123"),
    ("admin", "123456789a"),
    ("admin", "888888"), ("admin", "666666"), ("admin", "999999"),
]

BASE["iot_impressoras"] = [
    ("admin", "admin"), ("admin", "1234"), ("admin", "12345"),
    ("admin", "123456"), ("admin", ""), ("admin", "password"),
    ("admin", "Admin"), ("admin", "Admin@123"), ("admin", "administrator"),
    ("root", "root"), ("root", ""), ("root", "admin"),
    ("user", "user"), ("guest", "guest"), ("public", "public"),
    ("supervisor", "supervisor"), ("sa", ""), ("sa", "sa"),
    ("sa", "password"), ("sa", "admin"), ("sa", "administrator"),
]

BASE["iot_smarttv"] = [
    ("admin", "admin"), ("admin", "1234"), ("admin", "12345"),
    ("admin", "123456"), ("admin", ""), ("admin", "password"),
    ("root", "root"), ("root", "admin"), ("root", ""),
    ("user", "user"), ("guest", "guest"), ("pi", "raspberry"),
    ("admin", "samsung"), ("admin", "Samsung"), ("admin", "samsung123"),
    ("admin", "lg"), ("admin", "LG"), ("admin", "lg123"),
    ("admin", "sony"), ("admin", "Sony"), ("admin", "sony123"),
    ("admin", "philips"), ("admin", "Philips"),
    ("admin", "tcl"), ("admin", "TCL"), ("admin", "tcl123"),
]

# ============================================================
# SCADA / ICS — PLCs, RTUs, HMIs
# ============================================================

BASE["scada"] = [
    ("admin", "admin"), ("admin", "1234"), ("admin", "12345"),
    ("admin", "123456"), ("admin", ""), ("admin", "password"),
    ("admin", "scada"), ("admin", "SCADA"), ("admin", "scada123"),
    ("admin", "siemens"), ("admin", "Siemens"),
    ("admin", "schneider"), ("admin", "Schneider"),
    ("admin", "rockwell"), ("admin", "Rockwell"),
    ("admin", "abb"), ("admin", "ABB"),
    ("admin", "honeywell"), ("admin", "Honeywell"),
    ("admin", "mitsubishi"), ("admin", "Mitsubishi"),
    ("admin", "omron"), ("admin", "Omron"),
    ("admin", "ge"), ("admin", "GE"),
    ("admin", "emerson"), ("admin", "Emerson"),
    ("admin", "yokogawa"), ("admin", "Yokogawa"),
    ("admin", "phoenix"), ("admin", "Phoenix"),
    ("admin", "wago"), ("admin", "Wago"),
    ("admin", "beckhoff"), ("admin", "Beckhoff"),
    ("admin", "bachmann"), ("admin", "Bachmann"),
    ("root", "root"), ("root", "siemens"), ("root", "schneider"),
    ("operator", "operator"), ("operator", "admin"),
    ("operator", "1234"), ("operator", ""), ("operator", "password"),
    ("guest", "guest"), ("guest", ""), ("user", "user"),
    ("service", "service"), ("maintenance", "maintenance"),
    ("siemens", "siemens"), ("schneider", "schneider"),
    ("rockwell", "rockwell"), ("abb", "abb"),
]

# ============================================================
# FIM DA PARTE 2 — BASE DE CREDENCIAIS
# ============================================================

def Total():
    return sum(len(L) for L in BASE.values())

def Por_Fabricante():
    return {K: len(V) for K, V in BASE.items()}

def Fabricantes():
    return sorted(BASE.keys())
