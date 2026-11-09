#ifndef NETLINK_READER_HPP
#define NETLINK_READER_HPP

#include <string>
#include <vector>
#include <cstdint>

struct Interface {
    std::string Nome;
    std::string Mac;
    std::string Estado;
    int Mtu;
    std::vector<std::string> Ips;
};

struct Rota {
    std::string Destino;
    std::string Gateway;
    std::string Interface;
    int Metrica;
};

struct Vizinho {
    std::string Ip;
    std::string Mac;
    std::string Interface;
    std::string Estado;
};

class NetlinkReader {
public:
    NetlinkReader();
    ~NetlinkReader();

    bool Abrir();
    void Fechar();
    bool Ativo() const { return Fd >= 0; }

    std::vector<Interface> ListarInterfaces();
    std::vector<Rota> ListarRotas();
    std::vector<Vizinho> ListarVizinhos();

private:
    int Fd;
    uint32_t Seq;

    bool EnviarRequisicao(int Tipo, int Flags);
    bool LerResposta(void* Buffer, size_t Tamanho, int& PayloadLen);
    std::string ParsearAtributo(struct rtattr* Attr, int Tipo, int& Len);
};

#endif
