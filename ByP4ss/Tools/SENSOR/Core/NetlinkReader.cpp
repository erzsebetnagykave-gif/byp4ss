#include "NetlinkReader.hpp"

#include <cstring>
#include <cstdio>
#include <cerrno>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <linux/if_link.h>
#include <linux/neighbour.h>
#include <net/if.h>
#include <arpa/inet.h>

#define BUF_SIZE 32768

NetlinkReader::NetlinkReader() : Fd(-1), Seq(0) {}
NetlinkReader::~NetlinkReader() { Fechar(); }

bool NetlinkReader::Abrir() {
    Fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
    if (Fd < 0) return false;
    return true;
}

void NetlinkReader::Fechar() {
    if (Fd >= 0) { close(Fd); Fd = -1; }
}

bool NetlinkReader::EnviarRequisicao(int Tipo, int Flags) {
    if (Fd < 0) return false;

    struct {
        struct nlmsghdr Nlh;
        struct rtgenmsg Rt;
    } Req;

    std::memset(&Req, 0, sizeof(Req));
    Req.Nlh.nlmsg_len = NLMSG_LENGTH(sizeof(struct rtgenmsg));
    Req.Nlh.nlmsg_type = Tipo;
    Req.Nlh.nlmsg_flags = NLM_F_REQUEST | NLM_F_DUMP | Flags;
    Req.Nlh.nlmsg_seq = ++Seq;
    Req.Rt.rtgen_family = AF_UNSPEC;

    struct sockaddr_nl Sa;
    std::memset(&Sa, 0, sizeof(Sa));
    Sa.nl_family = AF_NETLINK;

    ssize_t N = sendto(Fd, &Req, Req.Nlh.nlmsg_len, 0, (struct sockaddr*)&Sa, sizeof(Sa));
    return N >= 0;
}

bool NetlinkReader::LerResposta(void* Buffer, size_t Tamanho, int& PayloadLen) {
    if (Fd < 0) return false;
    ssize_t N = recv(Fd, Buffer, Tamanho, 0);
    if (N <= 0) return false;
    PayloadLen = (int)N;
    return true;
}

std::string NetlinkReader::ParsearAtributo(struct rtattr* Attr, int Tipo, int& Len) {
    Len = RTA_PAYLOAD(Attr);
    std::string Resultado;
    if ((int)Attr->rta_type != Tipo) return Resultado;
    char *Ptr = (char*)RTA_DATA(Attr);
    Resultado.assign(Ptr, Len);
    return Resultado;
}

std::vector<Interface> NetlinkReader::ListarInterfaces() {
    std::vector<Interface> Resultado;
    if (!Abrir()) return Resultado;
    if (!EnviarRequisicao(RTM_GETLINK, 0)) { Fechar(); return Resultado; }

    char Buffer[BUF_SIZE];
    int Len;
    while (LerResposta(Buffer, sizeof(Buffer), Len)) {
        struct nlmsghdr *Nlh = (struct nlmsghdr*)Buffer;
        for (; NLMSG_OK(Nlh, Len); Nlh = NLMSG_NEXT(Nlh, Len)) {
            if (Nlh->nlmsg_type == NLMSG_DONE) { Fechar(); return Resultado; }
            if (Nlh->nlmsg_type == NLMSG_ERROR) { Fechar(); return Resultado; }
            if (Nlh->nlmsg_type != RTM_NEWLINK) continue;

            struct ifinfomsg *Ifi = (struct ifinfomsg*)NLMSG_DATA(Nlh);
            Interface Iface;
            Iface.Mtu = 0;
            Iface.Estado = (Ifi->ifi_flags & IFF_UP) ? "up" : "down";

            int AttrLen = Nlh->nlmsg_len - NLMSG_LENGTH(sizeof(struct ifinfomsg));
            struct rtattr *Attr = IFLA_RTA(Ifi);
            for (; RTA_OK(Attr, AttrLen); Attr = RTA_NEXT(Attr, AttrLen)) {
                if (Attr->rta_type == IFLA_IFNAME) {
                    Iface.Nome.assign((char*)RTA_DATA(Attr), RTA_PAYLOAD(Attr) - 1);
                } else if (Attr->rta_type == IFLA_ADDRESS) {
                    unsigned char *M = (unsigned char*)RTA_DATA(Attr);
                    char MacBuf[32];
                    std::snprintf(MacBuf, sizeof(MacBuf), "%02x:%02x:%02x:%02x:%02x:%02x",
                        M[0], M[1], M[2], M[3], M[4], M[5]);
                    Iface.Mac = MacBuf;
                } else if (Attr->rta_type == IFLA_MTU) {
                    Iface.Mtu = *(int*)RTA_DATA(Attr);
                }
            }
            if (!Iface.Nome.empty()) Resultado.push_back(Iface);
        }
    }
    Fechar();
    return Resultado;
}

std::vector<Rota> NetlinkReader::ListarRotas() {
    std::vector<Rota> Resultado;
    if (!Abrir()) return Resultado;
    if (!EnviarRequisicao(RTM_GETROUTE, 0)) { Fechar(); return Resultado; }

    char Buffer[BUF_SIZE];
    int Len;
    while (LerResposta(Buffer, sizeof(Buffer), Len)) {
        struct nlmsghdr *Nlh = (struct nlmsghdr*)Buffer;
        for (; NLMSG_OK(Nlh, Len); Nlh = NLMSG_NEXT(Nlh, Len)) {
            if (Nlh->nlmsg_type == NLMSG_DONE) { Fechar(); return Resultado; }
            if (Nlh->nlmsg_type == NLMSG_ERROR) { Fechar(); return Resultado; }
            if (Nlh->nlmsg_type != RTM_NEWROUTE) continue;

            struct rtmsg *Rtm = (struct rtmsg*)NLMSG_DATA(Nlh);
            Rota R;
            R.Metrica = 0;
            R.Destino = "default";

            int AttrLen = Nlh->nlmsg_len - NLMSG_LENGTH(sizeof(struct rtmsg));
            struct rtattr *Attr = RTM_RTA(Rtm);
            for (; RTA_OK(Attr, AttrLen); Attr = RTA_NEXT(Attr, AttrLen)) {
                if (Attr->rta_type == RTA_GATEWAY) {
                    struct in_addr A;
                    std::memcpy(&A, RTA_DATA(Attr), 4);
                    R.Gateway = inet_ntoa(A);
                } else if (Attr->rta_type == RTA_OIF) {
                    int Oif = *(int*)RTA_DATA(Attr);
                    char Nome[IF_NAMESIZE];
                    if (if_indextoname(Oif, Nome)) R.Interface = Nome;
                } else if (Attr->rta_type == RTA_DST) {
                    struct in_addr A;
                    std::memcpy(&A, RTA_DATA(Attr), 4);
                    R.Destino = inet_ntoa(A);
                } else if (Attr->rta_type == RTA_PRIORITY) {
                    R.Metrica = *(int*)RTA_DATA(Attr);
                }
            }
            Resultado.push_back(R);
        }
    }
    Fechar();
    return Resultado;
}

std::vector<Vizinho> NetlinkReader::ListarVizinhos() {
    std::vector<Vizinho> Resultado;
    if (!Abrir()) return Resultado;
    if (!EnviarRequisicao(RTM_GETNEIGH, 0)) { Fechar(); return Resultado; }

    char Buffer[BUF_SIZE];
    int Len;
    while (LerResposta(Buffer, sizeof(Buffer), Len)) {
        struct nlmsghdr *Nlh = (struct nlmsghdr*)Buffer;
        for (; NLMSG_OK(Nlh, Len); Nlh = NLMSG_NEXT(Nlh, Len)) {
            if (Nlh->nlmsg_type == NLMSG_DONE) { Fechar(); return Resultado; }
            if (Nlh->nlmsg_type == NLMSG_ERROR) { Fechar(); return Resultado; }
            if (Nlh->nlmsg_type != RTM_NEWNEIGH) continue;

            struct ndmsg *Ndm = (struct ndmsg*)NLMSG_DATA(Nlh);
            Vizinho V;

            int AttrLen = Nlh->nlmsg_len - NLMSG_LENGTH(sizeof(struct ndmsg));
            struct rtattr *Attr = (struct rtattr*)((char*)Ndm + NLMSG_ALIGN(sizeof(struct ndmsg)));
            for (; RTA_OK(Attr, AttrLen); Attr = RTA_NEXT(Attr, AttrLen)) {
                if (Attr->rta_type == NDA_DST) {
                    struct in_addr A;
                    std::memcpy(&A, RTA_DATA(Attr), 4);
                    V.Ip = inet_ntoa(A);
                } else if (Attr->rta_type == NDA_LLADDR) {
                    unsigned char *M = (unsigned char*)RTA_DATA(Attr);
                    char MacBuf[32];
                    std::snprintf(MacBuf, sizeof(MacBuf), "%02x:%02x:%02x:%02x:%02x:%02x",
                        M[0], M[1], M[2], M[3], M[4], M[5]);
                    V.Mac = MacBuf;
                }
            }
            char Nome[IF_NAMESIZE];
            if (if_indextoname(Ndm->ndm_ifindex, Nome)) V.Interface = Nome;
            if (Ndm->ndm_state & NUD_REACHABLE) V.Estado = "reachable";
            else if (Ndm->ndm_state & NUD_STALE) V.Estado = "stale";
            else V.Estado = "unknown";
            if (!V.Ip.empty()) Resultado.push_back(V);
        }
    }
    Fechar();
    return Resultado;
}

extern "C" {
    NetlinkReader* NetlinkCriar() { return new NetlinkReader(); }
    void NetlinkDestruir(NetlinkReader* N) { delete N; }
    int NetlinkListarInterfaces(NetlinkReader* N, char* Saida, size_t Tamanho) {
        auto Ifaces = N->ListarInterfaces();
        size_t Pos = 0; Saida[0] = '\0';
        for (auto &I : Ifaces) {
            int Written = std::snprintf(Saida + Pos, Tamanho - Pos, "%s|%s|%s|%d\n",
                I.Nome.c_str(), I.Mac.c_str(), I.Estado.c_str(), I.Mtu);
            if (Written < 0 || (size_t)Written >= Tamanho - Pos) break;
            Pos += Written;
        }
        return (int)Pos;
    }
    int NetlinkListarRotas(NetlinkReader* N, char* Saida, size_t Tamanho) {
        auto Rotas = N->ListarRotas();
        size_t Pos = 0; Saida[0] = '\0';
        for (auto &R : Rotas) {
            int Written = std::snprintf(Saida + Pos, Tamanho - Pos, "%s|%s|%s|%d\n",
                R.Destino.c_str(), R.Gateway.c_str(), R.Interface.c_str(), R.Metrica);
            if (Written < 0 || (size_t)Written >= Tamanho - Pos) break;
            Pos += Written;
        }
        return (int)Pos;
    }
    int NetlinkListarVizinhos(NetlinkReader* N, char* Saida, size_t Tamanho) {
        auto Vizinhos = N->ListarVizinhos();
        size_t Pos = 0; Saida[0] = '\0';
        for (auto &V : Vizinhos) {
            int Written = std::snprintf(Saida + Pos, Tamanho - Pos, "%s|%s|%s|%s\n",
                V.Ip.c_str(), V.Mac.c_str(), V.Interface.c_str(), V.Estado.c_str());
            if (Written < 0 || (size_t)Written >= Tamanho - Pos) break;
            Pos += Written;
        }
        return (int)Pos;
    }
}
