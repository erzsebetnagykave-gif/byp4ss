#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pty.h>
#include <utmp.h>
#include <sys/select.h>
#include <sys/ioctl.h>
#include <sys/wait.h>
#include <termios.h>
#include <signal.h>
#include <time.h>
#include <fcntl.h>
#include <errno.h>

#define MAX_BUF 8192

static int master_fd = -1;
static pid_t child_pid = -1;
static struct termios orig_termios;
static FILE *log_json = NULL;
static FILE *log_raw = NULL;
static char sessao_id[64];

void timestamp(char *buf, size_t max) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    struct tm *tm = gmtime(&ts.tv_sec);
    snprintf(buf, max, "%04d-%02d-%02dT%02d:%02d:%02d.%03ldZ",
             tm->tm_year + 1900, tm->tm_mon + 1, tm->tm_mday,
             tm->tm_hour, tm->tm_min, tm->tm_sec, ts.tv_nsec / 1000000);
}

void json_escape(const char *src, int len, char *dst, int max_dst) {
    int j = 0;
    for (int i = 0; i < len && j < max_dst - 6; i++) {
        unsigned char c = src[i];
        if (c == '"') { dst[j++] = '\\'; dst[j++] = '"'; }
        else if (c == '\\') { dst[j++] = '\\'; dst[j++] = '\\'; }
        else if (c == '\n') { dst[j++] = '\\'; dst[j++] = 'n'; }
        else if (c == '\r') { dst[j++] = '\\'; dst[j++] = 'r'; }
        else if (c == '\t') { dst[j++] = '\\'; dst[j++] = 't'; }
        else if (c < 32) { j += snprintf(dst + j, max_dst - j, "\\u%04x", c); }
        else { dst[j++] = c; }
    }
    dst[j] = 0;
}

void restaurar_terminal() {
    tcsetattr(STDIN_FILENO, TCSANOW, &orig_termios);
}

void handler_sinal(int sig) {
    if (child_pid > 0) {
        kill(child_pid, sig);
    }
    if (sig == SIGWINCH) {
        struct winsize ws;
        if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws) == 0) {
            ioctl(master_fd, TIOCSWINSZ, &ws);
        }
    }
}

void extrair_coordenadas(const char *buf, int len) {
    // regex manual simples: \x1b[<num>;<num>H
    for (int i = 0; i < len - 2; i++) {
        if (buf[i] == '\x1b' && buf[i+1] == '[') {
            int j = i + 2;
            int linha = 0, coluna = 0, tem_linha = 0, tem_coluna = 0;
            while (j < len && buf[j] >= '0' && buf[j] <= '9') {
                linha = linha * 10 + (buf[j] - '0');
                tem_linha = 1;
                j++;
            }
            if (j < len && buf[j] == ';') {
                j++;
                while (j < len && buf[j] >= '0' && buf[j] <= '9') {
                    coluna = coluna * 10 + (buf[j] - '0');
                    tem_coluna = 1;
                    j++;
                }
                if (j < len && buf[j] == 'H' && tem_linha && tem_coluna) {
                    printf("\033[90m[coord]\033[0m linha=%d coluna=%d\n", linha, coluna);
                    fflush(stdout);
                }
            }
        }
    }
}

void registrar_saida(const char *buf, int len) {
    if (log_raw) {
        fwrite("<OUT>", 1, 5, log_raw);
        fwrite(buf, 1, len, log_raw);
        fwrite("\n", 1, 1, log_raw);
        fflush(log_raw);
    }
    if (log_json) {
        char ts[64], esc[4096];
        timestamp(ts, sizeof(ts));
        json_escape(buf, len, esc, sizeof(esc));
        fprintf(log_json, "{\"ts\":\"%s\",\"tipo\":\"saida\",\"bytes\":%d,\"raw\":\"%s\"}\n", ts, len, esc);
        fflush(log_json);
    }
}

void registrar_entrada(const char *buf, int len) {
    if (log_raw) {
        fwrite("<IN>", 1, 4, log_raw);
        fwrite(buf, 1, len, log_raw);
        fwrite("\n", 1, 1, log_raw);
        fflush(log_raw);
    }
    if (log_json) {
        char ts[64], esc[4096];
        timestamp(ts, sizeof(ts));
        json_escape(buf, len, esc, sizeof(esc));
        fprintf(log_json, "{\"ts\":\"%s\",\"tipo\":\"entrada\",\"bytes\":%d,\"raw\":\"%s\"}\n", ts, len, esc);
        fflush(log_json);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "uso: %s <comando> [args...]\n", argv[0]);
        return 1;
    }

    tcgetattr(STDIN_FILENO, &orig_termios);

    // arquivos de log
    char base_dir[256];
    snprintf(base_dir, sizeof(base_dir), "%s/logs/trace", getenv("HOME") ? getenv("HOME") : ".");
    snprintf(sessao_id, sizeof(sessao_id), "trace_%ld", time(NULL));
    
    char path_json[512], path_raw[512];
    snprintf(path_json, sizeof(path_json), "%s/%s.jsonl", base_dir, sessao_id);
    snprintf(path_raw, sizeof(path_raw), "%s/%s.raw", base_dir, sessao_id);
    
    log_json = fopen(path_json, "w");
    log_raw = fopen(path_raw, "w");

    // avisa o terminal que vai entrar em alternate screen
    printf("\033[?1049h\033[H\033[2J");
    fflush(stdout);

    struct winsize ws;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws);

    child_pid = forkpty(&master_fd, NULL, &orig_termios, &ws);
    if (child_pid < 0) {
        perror("forkpty");
        return 1;
    }

    if (child_pid == 0) {
        // filho: executa o comando
        execvp(argv[1], &argv[1]);
        perror("execvp");
        _exit(127);
    }

    // pai: monitora
    signal(SIGWINCH, handler_sinal);
    signal(SIGINT, handler_sinal);
    signal(SIGTERM, handler_sinal);

    char buf[MAX_BUF];
    int running = 1;

    while (running) {
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(STDIN_FILENO, &fds);
        FD_SET(master_fd, &fds);

        struct timeval tv = {0, 100000};
        int max_fd = (master_fd > STDIN_FILENO ? master_fd : STDIN_FILENO) + 1;
        
        int ret = select(max_fd, &fds, NULL, NULL, &tv);
        if (ret < 0) {
            if (errno == EINTR) continue;
            break;
        }

        if (FD_ISSET(STDIN_FILENO, &fds)) {
            int n = read(STDIN_FILENO, buf, sizeof(buf));
            if (n > 0) {
                registrar_entrada(buf, n);
                write(master_fd, buf, n);
            } else {
                break;
            }
        }

        if (FD_ISSET(master_fd, &fds)) {
            int n = read(master_fd, buf, sizeof(buf));
            if (n > 0) {
                registrar_saida(buf, n);
                write(STDOUT_FILENO, buf, n);
                extrair_coordenadas(buf, n);
            } else {
                running = 0;
            }
        }

        int status;
        if (waitpid(child_pid, &status, WNOHANG) == child_pid) {
            running = 0;
        }
    }

    // sai do alternate screen
    printf("\033[?1049l\033[?25h\033[0m\n");
    fflush(stdout);
    
    if (log_json) fclose(log_json);
    if (log_raw) fclose(log_raw);

    printf("[trace] sessao: %s\n", sessao_id);
    printf("[trace] jsonl: %s\n", path_json);
    printf("[trace] raw:   %s\n", path_raw);

    return 0;
}
