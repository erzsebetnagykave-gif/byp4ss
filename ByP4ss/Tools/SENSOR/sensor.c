/* SENSOR — leitura direta de hardware e rede
 * Camada 1: SysfsReader (lê /sys/class/, /proc/, /sys/devices/)
 * C puro, zero dependência externa. Parte 1 de 3 (300 linhas).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>
#include <sys/utsname.h>
#include <sys/statvfs.h>
#include <sys/sysinfo.h>

#define MAX_STR 512
#define MAX_LINHAS 128

/* ---- Leitura de arquivo genérica ---- */

static int LerArquivo(const char *Caminho, char *Buffer, size_t Tamanho) {
    int Fd = open(Caminho, O_RDONLY);
    if (Fd < 0) return -1;
    ssize_t N = read(Fd, Buffer, Tamanho - 1);
    close(Fd);
    if (N < 0) return -1;
    Buffer[N] = '\0';
    while (N > 0 && (Buffer[N-1] == '\n' || Buffer[N-1] == '\r' || Buffer[N-1] == ' ')) {
        Buffer[--N] = '\0';
    }
    return (int)N;
}

static int LerLinha(const char *Caminho, const char *Chave, char *Saida, size_t Tamanho) {
    FILE *F = fopen(Caminho, "r");
    if (!F) return -1;
    char Linha[MAX_STR];
    int Achou = 0;
    while (fgets(Linha, sizeof(Linha), F)) {
        if (strncmp(Linha, Chave, strlen(Chave)) == 0) {
            char *P = Linha + strlen(Chave);
            while (*P == ':' || *P == ' ' || *P == '\t') P++;
            char *Fim = P + strlen(P) - 1;
            while (Fim > P && (*Fim == '\n' || *Fim == '\r' || *Fim == ' ')) {
                *Fim-- = '\0';
            }
            strncpy(Saida, P, Tamanho - 1);
            Saida[Tamanho - 1] = '\0';
            Achou = 1;
            break;
        }
    }
    fclose(F);
    return Achou ? 0 : -1;
}

/* ---- CPU ---- */

static int SensorCpu(char *Saida, size_t Tamanho) {
    char Modelo[MAX_STR] = "desconhecido";
    char Cores[MAX_STR] = "0";
    char Freq[MAX_STR] = "0";

    LerLinha("/proc/cpuinfo", "model name", Modelo, sizeof(Modelo));
    if (strcmp(Modelo, "desconhecido") == 0) {
        LerLinha("/proc/cpuinfo", "Hardware", Modelo, sizeof(Modelo));
    }
    if (strcmp(Modelo, "desconhecido") == 0) {
        LerLinha("/proc/cpuinfo", "Processor", Modelo, sizeof(Modelo));
    }

    int NCores = 0;
    DIR *D = opendir("/sys/devices/system/cpu");
    if (D) {
        struct dirent *E;
        while ((E = readdir(D))) {
            if (strncmp(E->d_name, "cpu", 3) == 0 && E->d_name[3] >= '0' && E->d_name[3] <= '9') {
                NCores++;
            }
        }
        closedir(D);
    }
    snprintf(Cores, sizeof(Cores), "%d", NCores);

    char Caminho[256];
    snprintf(Caminho, sizeof(Caminho), "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq");
    char FreqKHz[MAX_STR];
    if (LerArquivo(Caminho, FreqKHz, sizeof(FreqKHz)) > 0) {
        long KHz = atol(FreqKHz);
        snprintf(Freq, sizeof(Freq), "%ld", KHz / 1000);
    }

    snprintf(Saida, Tamanho, "%s|%s|%s", Modelo, Cores, Freq);
    return 0;
}

/* ---- RAM ---- */

static int SensorMemoria(char *Saida, size_t Tamanho) {
    char Total[MAX_STR] = "0";
    char Livre[MAX_STR] = "0";
    char Disponivel[MAX_STR] = "0";

    LerLinha("/proc/meminfo", "MemTotal:", Total, sizeof(Total));
    LerLinha("/proc/meminfo", "MemFree:", Livre, sizeof(Livre));
    LerLinha("/proc/meminfo", "MemAvailable:", Disponivel, sizeof(Disponivel));

    long TotalKb = atol(Total);
    long LivreKb = atol(Livre);
    long DispKb = atol(Disponivel);
    if (DispKb == 0) DispKb = LivreKb;

    snprintf(Saida, Tamanho, "%ld|%ld|%ld", TotalKb / 1024, LivreKb / 1024, DispKb / 1024);
    return 0;
}

/* ---- Disco ---- */

static int SensorDisco(const char *Caminho, char *Saida, size_t Tamanho) {
    struct statvfs St;
    if (statvfs(Caminho, &St) != 0) {
        snprintf(Saida, Tamanho, "0|0|0");
        return -1;
    }
    unsigned long long Total = (unsigned long long)St.f_blocks * St.f_frsize;
    unsigned long long Livre = (unsigned long long)St.f_bavail * St.f_frsize;
    unsigned long long Usado = Total - (unsigned long long)St.f_bfree * St.f_frsize;
    snprintf(Saida, Tamanho, "%llu|%llu|%llu", Total / (1024*1024), Usado / (1024*1024), Livre / (1024*1024));
    return 0;
}

/* ---- Bateria ---- */

static int SensorBateria(char *Saida, size_t Tamanho) {
    char Capacidade[MAX_STR] = "0";
    char Status[MAX_STR] = "desconhecido";
    char Temp[MAX_STR] = "0";
    char Voltagem[MAX_STR] = "0";

    const char *Bases[] = {
        "/sys/class/power_supply/battery",
        "/sys/class/power_supply/BAT0",
        "/sys/class/power_supply/BAT1",
        NULL
    };

    int Achou = 0;
    for (int I = 0; Bases[I]; I++) {
        char Caminho[256];
        snprintf(Caminho, sizeof(Caminho), "%s/capacity", Bases[I]);
        if (LerArquivo(Caminho, Capacidade, sizeof(Capacidade)) > 0) {
            Achou = 1;
            snprintf(Caminho, sizeof(Caminho), "%s/status", Bases[I]);
            LerArquivo(Caminho, Status, sizeof(Status));
            snprintf(Caminho, sizeof(Caminho), "%s/temp", Bases[I]);
            LerArquivo(Caminho, Temp, sizeof(Temp));
            snprintf(Caminho, sizeof(Caminho), "%s/voltage_now", Bases[I]);
            LerArquivo(Caminho, Voltagem, sizeof(Voltagem));
            break;
        }
    }

    if (!Achou) {
        snprintf(Saida, Tamanho, "0|desconhecido|0|0");
        return -1;
    }

    long TempC = atol(Temp) / 10;
    long VoltMv = atol(Voltagem) / 1000;
    snprintf(Saida, Tamanho, "%s|%s|%ld|%ld", Capacidade, Status, TempC, VoltMv);
    return 0;
}

/* ---- Temperatura (thermal zones) ---- */

static int SensorTemperatura(char *Saida, size_t Tamanho) {
    DIR *D = opendir("/sys/class/thermal");
    if (!D) {
        snprintf(Saida, Tamanho, "0");
        return -1;
    }

    long MaxTemp = 0;
    char Zona[MAX_STR];
    struct dirent *E;
    while ((E = readdir(D))) {
        if (strncmp(E->d_name, "thermal_zone", 12) == 0) {
            char Caminho[256];
            snprintf(Caminho, sizeof(Caminho), "/sys/class/thermal/%s/temp", E->d_name);
            if (LerArquivo(Caminho, Zona, sizeof(Zona)) > 0) {
                long T = atol(Zona) / 1000;
                if (T > MaxTemp) MaxTemp = T;
            }
        }
    }
    closedir(D);

    snprintf(Saida, Tamanho, "%ld", MaxTemp);
    return 0;
}

/* ---- Hardware (DMI / device-tree) ---- */

static void RodarProp(const char *Prop, char *Saida, size_t Tamanho) {
    char Cmd[256];
    snprintf(Cmd, sizeof(Cmd), "getprop %s 2>/dev/null", Prop);
    FILE *P = popen(Cmd, "r");
    if (!P) return;
    if (fgets(Saida, Tamanho, P)) {
        Saida[strcspn(Saida, "\n")] = '\0';
        Saida[strcspn(Saida, "\r")] = '\0';
    }
    pclose(P);
}

static int SensorHardware(char *Saida, size_t Tamanho) {
    char Fabricante[MAX_STR] = "desconhecido";
    char Modelo[MAX_STR] = "desconhecido";
    char Serial[MAX_STR] = "desconhecido";
    char Bios[MAX_STR] = "desconhecido";

    RodarProp("ro.product.manufacturer", Fabricante, sizeof(Fabricante));
    RodarProp("ro.product.model", Modelo, sizeof(Modelo));
    RodarProp("ro.serialno", Serial, sizeof(Serial));
    RodarProp("ro.build.version.release", Bios, sizeof(Bios));

    if (strcmp(Modelo, "desconhecido") == 0 || Modelo[0] == '\0') {
        LerArquivo("/sys/class/dmi/id/sys_vendor", Fabricante, sizeof(Fabricante));
        LerArquivo("/sys/class/dmi/id/product_name", Modelo, sizeof(Modelo));
        LerArquivo("/sys/class/dmi/id/product_serial", Serial, sizeof(Serial));
        LerArquivo("/sys/class/dmi/id/bios_version", Bios, sizeof(Bios));
    }

    if (strcmp(Modelo, "desconhecido") == 0 || Modelo[0] == '\0') {
        LerArquivo("/proc/device-tree/model", Modelo, sizeof(Modelo));
        LerArquivo("/proc/device-tree/manufacturer", Fabricante, sizeof(Fabricante));
    }

    snprintf(Saida, Tamanho, "%s|%s|%s|%s", Fabricante, Modelo, Serial, Bios);
    return 0;
}

/* ---- Kernel ---- */

static int SensorKernel(char *Saida, size_t Tamanho) {
    struct utsname U;
    if (uname(&U) != 0) {
        snprintf(Saida, Tamanho, "desconhecido");
        return -1;
    }
    snprintf(Saida, Tamanho, "%s|%s|%s|%s", U.sysname, U.release, U.version, U.machine);
    return 0;
}

/* ---- Uptime ---- */

static int SensorUptime(char *Saida, size_t Tamanho) {
    struct sysinfo S;
    if (sysinfo(&S) != 0) {
        snprintf(Saida, Tamanho, "0");
        return -1;
    }
    snprintf(Saida, Tamanho, "%ld", S.uptime);
    return 0;
}

/* ---- Interface de rede (MAC, estado, MTU) ---- */

static int SensorInterface(const char *Nome, char *Saida, size_t Tamanho) {
    char Caminho[256];
    char Mac[MAX_STR] = "00:00:00:00:00:00";
    char Estado[MAX_STR] = "desconhecido";
    char Mtu[MAX_STR] = "0";

    snprintf(Caminho, sizeof(Caminho), "/sys/class/net/%s/address", Nome);
    LerArquivo(Caminho, Mac, sizeof(Mac));

    snprintf(Caminho, sizeof(Caminho), "/sys/class/net/%s/operstate", Nome);
    LerArquivo(Caminho, Estado, sizeof(Estado));

    snprintf(Caminho, sizeof(Caminho), "/sys/class/net/%s/mtu", Nome);
    LerArquivo(Caminho, Mtu, sizeof(Mtu));

    snprintf(Saida, Tamanho, "%s|%s|%s|%s", Nome, Mac, Estado, Mtu);
    return 0;
}

static int ListarInterfaces(char *Saida, size_t Tamanho) {
    DIR *D = opendir("/sys/class/net");
    if (!D) {
        snprintf(Saida, Tamanho, "");
        return -1;
    }

    Saida[0] = '\0';
    size_t Pos = 0;
    struct dirent *E;
    while ((E = readdir(D))) {
        if (E->d_name[0] == '.') continue;
        char Info[MAX_STR];
        SensorInterface(E->d_name, Info, sizeof(Info));
        int N = snprintf(Saida + Pos, Tamanho - Pos, "%s\n", Info);
        if (N < 0 || (size_t)N >= Tamanho - Pos) break;
        Pos += N;
    }
    closedir(D);
    return 0;
}

/* ---- Wi-Fi ---- */

static int SensorWifi(char *Saida, size_t Tamanho) {
    char Ssid[MAX_STR] = "desconhecido";
    char Bssid[MAX_STR] = "00:00:00:00:00:00";
    char Frequencia[MAX_STR] = "0";
    char Sinal[MAX_STR] = "0";

    DIR *D = opendir("/sys/class/net");
    if (!D) {
        snprintf(Saida, Tamanho, "desconhecido|00:00:00:00:00:00|0|0");
        return -1;
    }

    char Wireless[MAX_STR] = "";
    struct dirent *E;
    while ((E = readdir(D))) {
        if (E->d_name[0] == '.') continue;
        if (strncmp(E->d_name, "wlan", 4) == 0 || strncmp(E->d_name, "wlp", 3) == 0) {
            strncpy(Wireless, E->d_name, sizeof(Wireless) - 1);
            break;
        }
    }
    closedir(D);

    if (Wireless[0] == '\0') {
        snprintf(Saida, Tamanho, "desconhecido|00:00:00:00:00:00|0|0");
        return -1;
    }

    char Caminho[256];
    snprintf(Caminho, sizeof(Caminho), "/sys/class/net/%s/wireless/status", Wireless);
    LerArquivo(Caminho, Ssid, sizeof(Ssid));

    snprintf(Caminho, sizeof(Caminho), "/sys/class/net/%s/address", Wireless);
    LerArquivo(Caminho, Bssid, sizeof(Bssid));

    snprintf(Caminho, sizeof(Caminho), "/sys/class/net/%s/wireless/frequency", Wireless);
    LerArquivo(Caminho, Frequencia, sizeof(Frequencia));

    snprintf(Caminho, sizeof(Caminho), "/sys/class/net/%s/wireless/signal", Wireless);
    LerArquivo(Caminho, Sinal, sizeof(Sinal));

    snprintf(Saida, Tamanho, "%s|%s|%s|%s", Ssid, Bssid, Frequencia, Sinal);
    return 0;
}

/* ---- API pública ---- */

int SensorLer(const char *Tipo, char *Saida, size_t Tamanho) {
    if (strcmp(Tipo, "cpu") == 0) return SensorCpu(Saida, Tamanho);
    if (strcmp(Tipo, "mem") == 0) return SensorMemoria(Saida, Tamanho);
    if (strcmp(Tipo, "bateria") == 0) return SensorBateria(Saida, Tamanho);
    if (strcmp(Tipo, "temp") == 0) return SensorTemperatura(Saida, Tamanho);
    if (strcmp(Tipo, "hw") == 0) return SensorHardware(Saida, Tamanho);
    if (strcmp(Tipo, "kernel") == 0) return SensorKernel(Saida, Tamanho);
    if (strcmp(Tipo, "uptime") == 0) return SensorUptime(Saida, Tamanho);
    if (strcmp(Tipo, "wifi") == 0) return SensorWifi(Saida, Tamanho);
    if (strcmp(Tipo, "ifaces") == 0) return ListarInterfaces(Saida, Tamanho);
    if (strcmp(Tipo, "disco") == 0) return SensorDisco("/", Saida, Tamanho);
    snprintf(Saida, Tamanho, "desconhecido");
    return -1;
}
