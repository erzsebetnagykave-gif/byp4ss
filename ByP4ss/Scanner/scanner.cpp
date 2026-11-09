#include <arpa/inet.h>
#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <fstream>
#include <iostream>
#include <map>
#include <net/if.h>
#include <netdb.h>
#include <netinet/in.h>
#include <poll.h>
#include <sstream>
#include <regex>
#include <string>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
#include <vector>

const int TIMEOUT_MS  = 400;
const int PORTAS[]    = {22, 23, 53, 80, 81, 139, 443, 445, 554, 1900, 5000, 8080, 8443, 9000, 9100, 52869};
const int N_PORTAS    = sizeof(PORTAS) / sizeof(PORTAS[0]);
const int HOSTS_TOTAL = 254;

struct Alvo {
    std::string Ip;
    std::string Hostname;
    std::vector<int> PortasAbertas;
    std::string Tipo;
    std::string Banners;
    std::string Fabricante;
    std::string OsEstimado;
    int Ttl = 0;
    bool Vivo = false;
};

std::string Executar(const std::string& Cmd) {
    std::string Out;
    FILE* Pipe = popen(Cmd.c_str(), "r");
    if (!Pipe) return Out;
    char Buf[256];
    while (fgets(Buf, sizeof(Buf), Pipe)) Out += Buf;
    pclose(Pipe);
    return Out;
}

std::string DetectarInterface() {
    std::string Saida = Executar("ip route get 8.8.8.8 2>/dev/null | head -1");
    size_t Pos = Saida.find("dev ");
    if (Pos == std::string::npos) return "wlan0";
    Pos += 4;
    size_t Fim = Saida.find(' ', Pos);
    return Saida.substr(Pos, Fim - Pos);
}

std::string DetectarIpLocal() {
    int Sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (Sock < 0) return "";
    struct sockaddr_in Dest;
    memset(&Dest, 0, sizeof(Dest));
    Dest.sin_family = AF_INET;
    Dest.sin_port = htons(53);
    inet_pton(AF_INET, "8.8.8.8", &Dest.sin_addr);
    std::string Ip;
    if (connect(Sock, (struct sockaddr*)&Dest, sizeof(Dest)) == 0) {
        struct sockaddr_in Local;
        socklen_t Len = sizeof(Local);
        if (getsockname(Sock, (struct sockaddr*)&Local, &Len) == 0) {
            char Buf[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &Local.sin_addr, Buf, sizeof(Buf));
            Ip = Buf;
        }
    }
    close(Sock);
    return Ip;
}

std::string CalcularRede(const std::string& Ip) {
    size_t P1 = Ip.find('.');
    if (P1 == std::string::npos) return "";
    size_t P2 = Ip.find('.', P1 + 1);
    if (P2 == std::string::npos) return "";
    size_t P3 = Ip.find('.', P2 + 1);
    if (P3 == std::string::npos) return "";
    return Ip.substr(0, P3);
}

bool TcpConnect(const std::string& Ip, int Porta, int TimeoutMs) {
    int Sock = socket(AF_INET, SOCK_STREAM, 0);
    if (Sock < 0) return false;
    struct sockaddr_in Dest;
    memset(&Dest, 0, sizeof(Dest));
    Dest.sin_family = AF_INET;
    Dest.sin_port = htons(Porta);
    inet_pton(AF_INET, Ip.c_str(), &Dest.sin_addr);
    int Flags = fcntl(Sock, F_GETFL, 0);
    fcntl(Sock, F_SETFL, Flags | O_NONBLOCK);
    int R = connect(Sock, (struct sockaddr*)&Dest, sizeof(Dest));
    if (R < 0 && errno != EINPROGRESS) {
        close(Sock);
        return false;
    }
    struct pollfd Pfd;
    Pfd.fd = Sock;
    Pfd.events = POLLOUT;
    int Pr = poll(&Pfd, 1, TimeoutMs);
    bool Ok = false;
    if (Pr > 0) {
        int Err = 0;
        socklen_t Len = sizeof(Err);
        getsockopt(Sock, SOL_SOCKET, SO_ERROR, &Err, &Len);
        Ok = (Err == 0);
    }
    close(Sock);
    return Ok;
}

bool PingIcmp(const std::string& Ip, int TimeoutMs) {
    int Sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_ICMP);
    if (Sock < 0) return false;
    struct timeval Tv;
    Tv.tv_sec = 0;
    Tv.tv_usec = TimeoutMs * 1000;
    setsockopt(Sock, SOL_SOCKET, SO_RCVTIMEO, &Tv, sizeof(Tv));
    unsigned char Pacote[8];
    Pacote[0] = 8;
    Pacote[1] = 0;
    Pacote[2] = 0;
    Pacote[3] = 0;
    Pacote[4] = 0xab;
    Pacote[5] = 0xcd;
    Pacote[6] = 0x00;
    Pacote[7] = 0x01;
    unsigned int Soma = 0;
    for (int I = 0; I < 8; I += 2) {
        Soma += (Pacote[I] << 8) | Pacote[I + 1];
    }
    Soma = (Soma >> 16) + (Soma & 0xffff);
    Soma += (Soma >> 16);
    unsigned short Check = ~Soma;
    Pacote[2] = (Check >> 8) & 0xff;
    Pacote[3] = Check & 0xff;
    struct sockaddr_in Dest;
    memset(&Dest, 0, sizeof(Dest));
    Dest.sin_family = AF_INET;
    inet_pton(AF_INET, Ip.c_str(), &Dest.sin_addr);
    if (sendto(Sock, Pacote, 8, 0, (struct sockaddr*)&Dest, sizeof(Dest)) < 0) {
        close(Sock);
        return false;
    }
    unsigned char Resposta[128];
    struct sockaddr_in Origem;
    socklen_t Len = sizeof(Origem);
    int R = recvfrom(Sock, Resposta, sizeof(Resposta), 0, (struct sockaddr*)&Origem, &Len);
    close(Sock);
    return R > 0;
}

std::string DnsReverso(const std::string& Ip, int TimeoutMs) {
    struct sockaddr_in Sa;
    memset(&Sa, 0, sizeof(Sa));
    Sa.sin_family = AF_INET;
    inet_pton(AF_INET, Ip.c_str(), &Sa.sin_addr);
    char Host[NI_MAXHOST];
    int R = getnameinfo((struct sockaddr*)&Sa, sizeof(Sa), Host, sizeof(Host), NULL, 0, NI_NAMEREQD);
    if (R == 0) return std::string(Host);
    return "";
}

std::string InferirTipo(const std::vector<int>& Portas) {
    auto Tem = [&](int P) -> bool {
        for (int X : Portas) if (X == P) return true;
        return false;
    };
    if (Tem(80) || Tem(443) || Tem(8080) || Tem(8443)) {
        if (Tem(1900) || Tem(52869)) return "Roteador";
        if (Tem(554)) return "Camera IP";
        if (Tem(9100)) return "Impressora";
        if (Tem(5000)) return "NAS/Servidor";
        return "Web";
    }
    if (Tem(22)) return "Servidor SSH";
    if (Tem(23)) return "Telnet/IoT";
    if (Tem(139) || Tem(445)) return "Windows/SMB";
    if (Tem(53)) return "DNS";
    if (Portas.empty()) return "Desconhecido";
    return "IoT";
}

std::string TcpBanner(const std::string& Ip, int Porta, int TimeoutMs) {
    int Sock = socket(AF_INET, SOCK_STREAM, 0);
    if (Sock < 0) return "";
    struct timeval Tv;
    Tv.tv_sec = 0;
    Tv.tv_usec = TimeoutMs * 1000;
    setsockopt(Sock, SOL_SOCKET, SO_RCVTIMEO, &Tv, sizeof(Tv));
    struct sockaddr_in Dest;
    memset(&Dest, 0, sizeof(Dest));
    Dest.sin_family = AF_INET;
    Dest.sin_port = htons(Porta);
    inet_pton(AF_INET, Ip.c_str(), &Dest.sin_addr);
    int Flags = fcntl(Sock, F_GETFL, 0);
    fcntl(Sock, F_SETFL, Flags | O_NONBLOCK);
    int R = connect(Sock, (struct sockaddr*)&Dest, sizeof(Dest));
    if (R < 0 && errno != EINPROGRESS) {
        close(Sock);
        return "";
    }
    struct pollfd Pfd;
    Pfd.fd = Sock;
    Pfd.events = POLLOUT;
    if (poll(&Pfd, 1, TimeoutMs) <= 0) {
        close(Sock);
        return "";
    }
    fcntl(Sock, F_SETFL, Flags);
    if (Porta == 80 || Porta == 8080 || Porta == 81 || Porta == 5000 || Porta == 9000) {
        const char* Req = "HEAD / HTTP/1.0\r\nHost: local\r\nUser-Agent: CBNC/1.0\r\n\r\n";
        send(Sock, Req, strlen(Req), 0);
    }
    char Buf[1024];
    int Recebido = recv(Sock, Buf, sizeof(Buf) - 1, 0);
    close(Sock);
    if (Recebido <= 0) return "";
    Buf[Recebido] = 0;
    return std::string(Buf, Recebido);
}

int PingComTtl(const std::string& Ip, int TimeoutMs) {
    int Sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (Sock < 0) {
        Sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_ICMP);
        if (Sock < 0) return 0;
    }
    struct timeval Tv;
    Tv.tv_sec = 0;
    Tv.tv_usec = TimeoutMs * 1000;
    setsockopt(Sock, SOL_SOCKET, SO_RCVTIMEO, &Tv, sizeof(Tv));
    unsigned char Pacote[8] = {8, 0, 0, 0, 0xab, 0xcd, 0x00, 0x01};
    unsigned int Soma = 0;
    for (int I = 0; I < 8; I += 2) Soma += (Pacote[I] << 8) | Pacote[I + 1];
    Soma = (Soma >> 16) + (Soma & 0xffff);
    Soma += (Soma >> 16);
    unsigned short Check = ~Soma;
    Pacote[2] = (Check >> 8) & 0xff;
    Pacote[3] = Check & 0xff;
    struct sockaddr_in Dest;
    memset(&Dest, 0, sizeof(Dest));
    Dest.sin_family = AF_INET;
    inet_pton(AF_INET, Ip.c_str(), &Dest.sin_addr);
    if (sendto(Sock, Pacote, 8, 0, (struct sockaddr*)&Dest, sizeof(Dest)) < 0) {
        close(Sock);
        return 0;
    }
    unsigned char Resp[128];
    struct sockaddr_in Origem;
    socklen_t Len = sizeof(Origem);
    int R = recvfrom(Sock, Resp, sizeof(Resp), 0, (struct sockaddr*)&Origem, &Len);
    close(Sock);
    if (R < 20) return 0;
    return Resp[8];
}

std::string ExtrairHeader(const std::string& Banner, const std::string& NomeHeader) {
    std::string Lower = NomeHeader;
    for (auto& C : Lower) C = tolower(C);
    std::string Copia = Banner;
    for (auto& C : Copia) C = tolower(C);
    size_t Pos = Copia.find(Lower + ":");
    if (Pos == std::string::npos) return "";
    Pos += Lower.length() + 1;
    while (Pos < Banner.length() && (Banner[Pos] == ' ' || Banner[Pos] == '\t')) Pos++;
    size_t Fim = Banner.find('\r', Pos);
    if (Fim == std::string::npos) Fim = Banner.find('\n', Pos);
    if (Fim == std::string::npos) Fim = Banner.length();
    return Banner.substr(Pos, Fim - Pos);
}

std::string DetectarFabricante(const std::string& Banners, const std::vector<int>& Portas) {
    std::string Lower = Banners;
    for (auto& C : Lower) C = tolower(C);

    if (Lower.find("tp-link") != std::string::npos) return "TP-Link";
    if (Lower.find("tplink") != std::string::npos) return "TP-Link";
    if (Lower.find("d-link") != std::string::npos) return "D-Link";
    if (Lower.find("dlink") != std::string::npos) return "D-Link";
    if (Lower.find("tenda") != std::string::npos) return "Tenda";
    if (Lower.find("iptime") != std::string::npos) return "ipTIME";
    if (Lower.find("arcadyan") != std::string::npos) return "Arcadyan";
    if (Lower.find("zte") != std::string::npos) return "ZTE";
    if (Lower.find("huawei") != std::string::npos) return "Huawei";
    if (Lower.find("mikrotik") != std::string::npos) return "MikroTik";
    if (Lower.find("cisco") != std::string::npos) return "Cisco";
    if (Lower.find("netgear") != std::string::npos) return "Netgear";
    if (Lower.find("asus") != std::string::npos) return "Asus";
    if (Lower.find("linksys") != std::string::npos) return "Linksys";
    if (Lower.find("ubiquiti") != std::string::npos) return "Ubiquiti";
    if (Lower.find("fortinet") != std::string::npos) return "Fortinet";
    if (Lower.find("openwrt") != std::string::npos) return "OpenWrt";
    if (Lower.find("dropbear") != std::string::npos) return "IoT (Dropbear)";
    if (Lower.find("busybox") != std::string::npos) return "IoT (BusyBox)";
    if (Lower.find("mini_httpd") != std::string::npos) return "IoT (mini_httpd)";
    if (Lower.find("lighttpd") != std::string::npos) return "Embedded (lighttpd)";
    if (Lower.find("apache") != std::string::npos) return "Servidor (Apache)";
    if (Lower.find("nginx") != std::string::npos) return "Servidor (nginx)";

    bool TemUpnp = false;
    for (int P : Portas) if (P == 1900 || P == 52869) TemUpnp = true;
    if (TemUpnp) return "Roteador (UPnP)";

    return "";
}

std::string DetectarOs(int Ttl) {
    if (Ttl == 0) return "";
    if (Ttl <= 64)  return "Linux";
    if (Ttl <= 128) return "Windows";
    if (Ttl <= 255) return "Cisco/BSD";
    return "";
}

std::string Cor(const std::string& Nome) {
    if (Nome == "verde")    return "\033[32m";
    if (Nome == "amarelo")  return "\033[33m";
    if (Nome == "vermelho") return "\033[31m";
    if (Nome == "ciano")    return "\033[36m";
    if (Nome == "cinza")    return "\033[90m";
    if (Nome == "bold")     return "\033[1m";
    if (Nome == "reset")    return "\033[0m";
    return "";
}

void Cabecalho(const std::string& Interface, const std::string& IpLocal, const std::string& Rede) {
    std::cout << Cor("bold") << "SCANNER CBNC" << Cor("reset") << "  "
              << Cor("cinza") << "v1.0" << Cor("reset") << "\n";
    std::cout << Cor("cinza") << "interface: " << Cor("reset") << Interface
              << Cor("cinza") << "  ip local: " << Cor("reset") << IpLocal
              << Cor("cinza") << "  rede: " << Cor("reset") << Rede << ".0/24\n";
    std::cout << "\n";
}

void Rodape(int Vivos, int Portas) {
    std::cout << "\n" << Cor("cinza")
              << "total: " << Vivos << " hosts vivos, " << Portas << " portas abertas"
              << Cor("reset") << "\n";
}

int main(int Argc, char** Argv) {
    std::string Interface = DetectarInterface();
    std::string IpLocal   = DetectarIpLocal();
    if (IpLocal.empty()) {
        std::cerr << Cor("vermelho") << "erro: nao consegui detectar IP local" << Cor("reset") << "\n";
        return 1;
    }
    std::string Rede = CalcularRede(IpLocal);
    if (Rede.empty()) {
        std::cerr << Cor("vermelho") << "erro: nao consegui calcular rede" << Cor("reset") << "\n";
        return 1;
    }

    Cabecalho(Interface, IpLocal, Rede);
    std::cout << Cor("cinza")
              << "IP               Hostname                 Portas                Tipo\n"
              << "---------------------------------------------------------------------------\n"
              << Cor("reset");

    std::vector<Alvo> Alvos;
    int Vivos = 0;
    int TotalPortas = 0;

    for (int I = 1; I <= HOSTS_TOTAL; I++) {
        std::stringstream Ss;
        Ss << Rede << "." << I;
        std::string Ip = Ss.str();

        if (Ip == IpLocal) continue;

        bool Vivo = false;

        if (!Vivo) Vivo = PingIcmp(Ip, TIMEOUT_MS);
        if (!Vivo) Vivo = TcpConnect(Ip, 80, TIMEOUT_MS);
        if (!Vivo) Vivo = TcpConnect(Ip, 443, TIMEOUT_MS);
        if (!Vivo) Vivo = TcpConnect(Ip, 22, TIMEOUT_MS);

        if (!Vivo) continue;

        Alvo A;
        A.Ip = Ip;
        A.Vivo = true;

        for (int K = 0; K < N_PORTAS; K++) {
            if (TcpConnect(Ip, PORTAS[K], TIMEOUT_MS)) {
                A.PortasAbertas.push_back(PORTAS[K]);
            }
        }

        A.Hostname = DnsReverso(Ip, TIMEOUT_MS);

        for (int P : A.PortasAbertas) {
            if (P == 80 || P == 22 || P == 443 || P == 8080 || P == 81 || P == 5000) {
                std::string B = TcpBanner(Ip, P, TIMEOUT_MS);
                if (!B.empty()) {
                    if (!A.Banners.empty()) A.Banners += " | ";
                    A.Banners += B.substr(0, 120);
                    break;
                }
            }
        }

        A.Fabricante = DetectarFabricante(A.Banners, A.PortasAbertas);
        A.Ttl = PingComTtl(Ip, TIMEOUT_MS);
        A.OsEstimado = DetectarOs(A.Ttl);
        A.Tipo = InferirTipo(A.PortasAbertas);

        Alvos.push_back(A);
        Vivos++;
        TotalPortas += A.PortasAbertas.size();

        std::string IpFmt = A.Ip;
        while (IpFmt.length() < 17) IpFmt += " ";

        std::string HostFmt = A.Hostname.empty() ? "-" : A.Hostname;
        if (HostFmt.length() > 24) HostFmt = HostFmt.substr(0, 21) + "...";
        while (HostFmt.length() < 25) HostFmt += " ";

        std::string PortasStr;
        for (size_t K = 0; K < A.PortasAbertas.size(); K++) {
            if (K > 0) PortasStr += ",";
            PortasStr += std::to_string(A.PortasAbertas[K]);
        }
        if (PortasStr.empty()) PortasStr = "-";
        if (PortasStr.length() > 20) PortasStr = PortasStr.substr(0, 17) + "...";
        while (PortasStr.length() < 21) PortasStr += " ";

        std::string CorTipo = "ciano";
        if (A.Tipo == "Roteador")  CorTipo = "amarelo";
        if (A.Tipo == "Servidor SSH") CorTipo = "verde";
        if (A.Tipo == "Windows/SMB")  CorTipo = "azul";
        if (A.Tipo == "Desconhecido") CorTipo = "cinza";

        std::cout << A.Ip << " " << HostFmt << " " << PortasStr
                  << Cor(CorTipo) << A.Tipo << Cor("reset");

        if (!A.Fabricante.empty()) {
            std::cout << "  " << Cor("magenta") << "[" << A.Fabricante << "]" << Cor("reset");
        }
        if (!A.OsEstimado.empty()) {
            std::cout << " " << Cor("cinza") << A.OsEstimado << " (ttl=" << A.Ttl << ")" << Cor("reset");
        }
        std::cout << "\n";

        if (!A.Banners.empty()) {
            std::string Banner = A.Banners;
            for (auto& C : Banner) if (C == '\r' || C == '\n') C = ' ';
            if (Banner.length() > 100) Banner = Banner.substr(0, 97) + "...";
            std::cout << "  " << Cor("cinza") << "  " << Banner << Cor("reset") << "\n";
        }
        std::cout.flush();
    }

    Rodape(Vivos, TotalPortas);

    if (Argc > 1 && std::string(Argv[1]) == "--json") {
        std::cout << "\n" << Cor("cinza") << "json:" << Cor("reset") << "\n{\n  \"rede\": \"" << Rede << ".0/24\",\n";
        std::cout << "  \"interface\": \"" << Interface << "\",\n";
        std::cout << "  \"hosts\": [\n";
        for (size_t I = 0; I < Alvos.size(); I++) {
            std::cout << "    {\"ip\": \"" << Alvos[I].Ip
                      << "\", \"hostname\": \"" << Alvos[I].Hostname
                      << "\", \"tipo\": \"" << Alvos[I].Tipo
                      << "\", \"fabricante\": \"" << Alvos[I].Fabricante
                      << "\", \"os\": \"" << Alvos[I].OsEstimado
                      << "\", \"ttl\": " << Alvos[I].Ttl
                      << ", \"portas\": [";
            for (size_t K = 0; K < Alvos[I].PortasAbertas.size(); K++) {
                if (K > 0) std::cout << ",";
                std::cout << Alvos[I].PortasAbertas[K];
            }
            std::cout << "]}" << (I + 1 < Alvos.size() ? "," : "") << "\n";
        }
        std::cout << "  ]\n}\n";
    }

    return 0;
}
