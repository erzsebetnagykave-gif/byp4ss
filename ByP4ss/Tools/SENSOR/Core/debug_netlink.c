#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/socket.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <arpa/inet.h>

int main() {
    int Fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
    if (Fd < 0) {
        printf("socket() falhou: %s\n", strerror(errno));
        return 1;
    }
    printf("socket() ok, fd=%d\n", Fd);

    struct {
        struct nlmsghdr Nlh;
        struct rtgenmsg Rt;
    } Req;
    memset(&Req, 0, sizeof(Req));
    Req.Nlh.nlmsg_len = NLMSG_LENGTH(sizeof(struct rtgenmsg));
    Req.Nlh.nlmsg_type = RTM_GETROUTE;
    Req.Nlh.nlmsg_flags = NLM_F_REQUEST | NLM_F_DUMP;
    Req.Nlh.nlmsg_seq = 1;
    Req.Rt.rtgen_family = AF_UNSPEC;

    struct sockaddr_nl Sa;
    memset(&Sa, 0, sizeof(Sa));
    Sa.nl_family = AF_NETLINK;

    ssize_t N = sendto(Fd, &Req, Req.Nlh.nlmsg_len, 0, (struct sockaddr*)&Sa, sizeof(Sa));
    if (N < 0) {
        printf("sendto() falhou: %s (errno=%d)\n", strerror(errno), errno);
        close(Fd);
        return 1;
    }
    printf("sendto() ok, enviou %zd bytes\n", N);

    char Buffer[32768];
    N = recv(Fd, Buffer, sizeof(Buffer), 0);
    if (N < 0) {
        printf("recv() falhou: %s (errno=%d)\n", strerror(errno), errno);
        close(Fd);
        return 1;
    }
    printf("recv() ok, recebeu %zd bytes\n", N);

    struct nlmsghdr *Nlh = (struct nlmsghdr*)Buffer;
    int Len = (int)N;
    int Count = 0;
    for (; NLMSG_OK(Nlh, Len); Nlh = NLMSG_NEXT(Nlh, Len)) {
        if (Nlh->nlmsg_type == NLMSG_DONE) {
            printf("NLMSG_DONE (fim)\n");
            break;
        }
        if (Nlh->nlmsg_type == NLMSG_ERROR) {
            struct nlmsgerr *Err = (struct nlmsgerr*)NLMSG_DATA(Nlh);
            printf("NLMSG_ERROR: %s (errno=%d)\n", strerror(-Err->error), -Err->error);
            break;
        }
        if (Nlh->nlmsg_type == RTM_NEWROUTE) {
            Count++;
            struct rtmsg *Rtm = (struct rtmsg*)NLMSG_DATA(Nlh);
            printf("RTM_NEWROUTE #%d: family=%d dst_len=%d\n", Count, Rtm->rtm_family, Rtm->rtm_dst_len);
        }
    }
    printf("Total de rotas: %d\n", Count);
    close(Fd);
    return 0;
}
