STUFFICK
Documento de Arquitetura e Especificacao

Versao 1.0

Este documento descreve a arquitetura completa de STUFFICK, um sistema de
coleta, correlacao e analise massiva de dados. O sistema e dividido em doze
modulos independentes. Cada modulo tem uma responsabilidade unica. Cada
modulo tem aproximadamente doze mil linhas de codigo quando implementado.

A linguagem principal e Rust. Onde fizer sentido, partes sao escritas em Go.
Onde fizer sentido, partes sao escritas em C puro. Nao existe dependencia de
bibliotecas externas de machine learning. Nao existe dependencia de servicos
de nuvem. Tudo roda localmente. Tudo roda em Termux no Android.

O documento esta dividido nas seguintes partes.

Parte 1, visao geral
Parte 2, camada de coleta, modulos 1 a 6
Parte 3, camada de analise, modulos 7 a 10
Parte 4, camada de consulta e exposicao, modulos 11 e 12
Parte 5, formato de dados
Parte 6, ordem de construcao
Parte 7, criterios de aceitacao


PARTE 1
VISAO GERAL


STUFFICK opera em tres camadas.

A primeira camada toca o mundo. Captura pacotes, le e-mails, resolve dominios,
correlaciona handles, atribui IPs. O resultado desta camada e um fluxo unico
de eventos enriquecidos.

A segunda camada analisa. Aprende o que e normal, agrupa entidades
semelhantes, classifica entidades em categorias, transforma tudo em sinais
acionaveis. O resultado desta camada e um fluxo de sinais.

A terceira camada consulta e expoe. Constroi e mantem o grafo, responde
consultas complexas, expoe tudo via HTTP e WebSocket.

A separacao em tres camadas permite que cada uma seja testada isoladamente.
A camada de analise pode ser testada com dados sinteticos, sem depender da
camada de coleta. A camada de consulta pode ser testada com o grafo vazio,
sem depender da camada de analise.

O sistema completo, quando maduro, permite responder perguntas como as
seguintes.

Quem e a pessoa por tras de um conjunto de handles.
Qual e o IP real por tras de uma VPN.
Qual e o e-mail real por tras de um dominio descartavel.
Qual e o dispositivo fisico por tras de um conjunto de sessoes.
Qual e o cluster de entidades que apareceu nos ultimos sete dias.
Qual e a entidade que mudou de comportamento ontem.
Qual e a cadeia de comando entre duas entidades.

Cada modulo e descrito em detalhe nas partes seguintes.


PRINCIPIOS DE PROJETO


Primeiro principio. Cada modulo tem uma responsabilidade unica. Um modulo
faz uma coisa. Um modulo faz essa coisa bem. Um modulo nao faz mais nada.

Segundo principio. Cada modulo e testavel isoladamente. Um modulo pode ser
testado com dados sinteticos. Um modulo pode ser testado com dados reais.
Um modulo pode ser testado com dados vazios.

Terceiro principio. Cada modulo e substituivel. Se um modulo precisa ser
reescrito, os outros modulos nao precisam saber. O contrato entre modulos e
o formato de dados que trafega entre eles.

Quarto principio. Cada modulo e observavel. Cada modulo emite metricas. Cada
modulo emite logs. Cada modulo emite alertas. Um operador consegue ver o que
esta acontecendo dentro de um modulo sem precisar abrir o codigo.

Quinto principio. Cada modulo e deterministico. Dado o mesmo input, o mesmo
modulo produz o mesmo output. Nao existe aleatoriedade nao controlada. Nao
existe estado escondido. Nao existe dependencia de ordem de execucao.

Sexto principio. Cada modulo e reversivel. Toda operacao de escrita pode ser
revertida. Toda operacao de modificacao tem um log. Um operador consegue
voltar ao estado anterior.

Setimo principio. Cada modulo e seguro por padrao. Nenhum modulo expoe dado
sensivel sem autenticacao. Nenhum modulo aceita input sem validacao. Nenhum
modulo confia em outro modulo sem verificacao.


PARTE 2
CAMADA DE COLETA
MODULOS 1 A 6


MODULO 1
PACKETCAPTUREENGINE

Responsabilidade

Capturar pacotes de rede em baixo nivel. Reconstruir streams. Extrair
informacao de camadas 2 a 7. Produzir fluxo de eventos crus.

Linguagem

Rust.

Linhas estimadas

Doze mil.

O que captura

Camada 2. Ethernet. MAC origem, MAC destino, EtherType, VLAN tag. Tambem
captura 802.1Q, 802.1X, LLDP, STP.

Camada 3. IPv4 e IPv6. Enderecos, fragmentacao, TTL, opcoes. Tambem captura
ICMP e ICMPv6.

Camada 4. TCP e UDP. Flags, sequencia, janela, portas. Tambem captura TCP
fingerprint via opcoes.

Camada 5 a 7. DNS, HTTP, HTTPS, SMTP, POP3, IMAP, FTP, Telnet, SSH, SMB,
DHCP, NTP, RDP, VNC, MQTT, Modbus, BACnet, DNP3, SIP, RTP, BitTorrent,
Bitcoin P2P, Tor, WireGuard, OpenVPN, IPSec.

O que faz com o que captura

Reconstroi streams TCP. Reconstroi fragmentos IP. Detecta protocolo em porta
nao padrao. Extrai credenciais em claro. Extrai hash NTLM. Extrai
certificados TLS. Extrai SNI. Extrai User-Agent. Extrai cookies. Extrai
headers de autorizacao. Detecta tunelamento. Detecta scan. Detecta flood.
Detecta exfiltracao. Detecta beacon C2.

Como captura

Socket AF_PACKET cru. Ring buffer PACKET_MMAP de sessenta e quatro megabytes.
Filtros BPF proprios. Modo promiscuo. Modo monitor em Wi-Fi. Modo espelho em
rede roteada. Fallback para pcap cru. Fallback para netfilter queue. Fallback
para proxy transparente.

Saida

Fluxo de RawEvent. Cada RawEvent tem campos ts_ns, camada, proto, src, dst,
payload, meta, credenciais. Consumido pelo Modulo 2, Modulo 3 e Modulo 5.


MODULO 2
EMAILEXTRACTOR

Responsabilidade

Extrair, normalizar e correlacionar e-mails de todas as fontes capturadas.

Linguagem

Rust.

Linhas estimadas

Doze mil.

O que extrai

De trafego SMTP, POP3 e IMAP. Enderecos de origem e destino. Assunto. Data.
Identificador de mensagem. Cabecalhos de resposta. Referencias. Corpo em
texto puro. Corpo em HTML. Anexos em base64. Anexos em quoted printable.
Anexos em uuencode. Cabecalhos Received. Cabecalhos X-Originating-IP.
Cabecalhos X-Sender-IP. Cabecalhos X-Mailer. Cabecalhos User-Agent.
Resultados de autenticacao SPF, DKIM e DMARC. Cabecalhos Return-Path.
Cabecalhos Reply-To. Cabecalhos Sender. Cabecalhos Bcc quando expostos.

De trafego HTTP. E-mail em formulario de login. E-mail em formulario de
cadastro. E-mail em formulario de contato. E-mail em URL. E-mail em header
de autorizacao. E-mail em cookie. E-mail em JSON de API.

De DNS. Registro MX. Registro TXT. Registro SOA.

De TLS e HTTPS. SNI de servidor de e-mail. Certificado com endereco de
e-mail no SAN.

De documentos e paginas. HTML de pagina de contato. HTML de pagina sobre.
HTML de pagina de equipe. Metadata de PDF. Rodape de PDF. Assinatura de PDF.
Metadata de DOCX. Metadata de XLSX. Metadata de PPTX. Assinatura de e-mail.
Fortuns. Pastebin. Redes sociais publicas.

De arquivos capturados. Arquivos eml. Arquivos mbox. Arquivos pst. Arquivos
ost. Arquivos msg. CSV com coluna de e-mail. JSON com coluna de e-mail. Log
de servidor. Log de erro. Backup exposto.

O que faz com o que extrai

Normaliza endereco. john+tag arroba gmail.com vira john arroba gmail.com.
john ponto doe arroba gmail.com vira johndoe arroba gmail.com. Valida SPF,
DKIM e DMARC sem consultar DNS externo. Verifica existencia via SMTP VRFY e
RCPT TO. Verifica descartavel via lista de trezentos dominios temporarios.
Verifica vazamento via hash SHA-256 da senha cruzado com banco proprio de
hashes vazados. Detecta padrao corporativo. Correlaciona entre multiplas
fontes. Reconstroi thread via In-Reply-To e References. Detecta spoofing.
Detecta phishing. Detecta lista de distribuicao. Detecta auto-reply. Detecta
e-mail de sistema. Detecta e-mail burner. Detecta e-mail ativo. Extrai nome
real de display name. Extrai telefone de assinatura. Extrai endereco fisico
de assinatura. Extrai endereco Bitcoin de assinatura. Extrai endereco
Ethereum de assinatura. Extrai links de redes sociais de assinatura. Calcula
score de confianca. Calcula score de importancia.

Saida

Fluxo de EmailEntity. Cada EmailEntity tem mais de oitenta campos.


MODULO 3
DOMAINRESOLVER

Responsabilidade

Resolver, enriquecer e mapear dominios.

Linguagem

Rust.

Linhas estimadas

Doze mil.

O que extrai

DNS proprio. Registros A, AAAA, MX, NS, TXT, SOA, CNAME, PTR, SRV, CAA, DS,
DNSKEY, NSEC, NSEC3. DNS sobre HTTPS. DNS sobre TLS. Zone transfer AXFR.
NSEC walking. Cache snooping. Wildcard detection. Fast flux detection.
Domain fronting detection.

WHOIS proprio para sessenta TLDs. Nome do registrante. E-mail do registrante.
Telefone do registrante. Endereco do registrante. Organizacao. Data de
criacao. Data de expiracao. Data de atualizacao. Nameservers. Status.
Historico de registrante.

RDAP. Mesmos dados em formato JSON estruturado.

Certificate Transparency logs. Todos os certificados emitidos para o dominio.
SANs. Issuer. Data de emissao. Subdomain enumeration passiva.

Reverse DNS e PTR. IP para hostname reverso.

ASN e BGP. IP para ASN. ASN para organizacao. ASN para pais. ASN para peers.

O que faz com o que extrai

Resolve em massa. Enumera subdominios via wordlist, brute force, Certificate
Transparency e NSEC. Detecta dominio recem registrado. Detecta dominio
expirado. Detecta dominio estacionado. Detecta DGA. Detecta homoglyph.
Detecta CDN. Detecta hosting. Detecta Tor hidden service. Detecta Namecoin.
Detecta ENS. Correlaciona dominios que compartilham nameservers, MX, IP ou
certificado. Mapeia infraestrutura compartilhada. Detecta sinkhole.

Saida

Fluxo de DomainEntity. Cada DomainEntity tem mais de sessenta campos. Arestas
de dominio para dominio quando compartilham infraestrutura.


MODULO 4
HANDLECORRELATOR

Responsabilidade

Extrair, normalizar e correlacionar handles em todas as plataformas. Um
handle e qualquer identificador publico de uma pessoa ou entidade. Pode ser
nome de usuario, apelido, pseudonimo, identificador de conta.

Linguagem

Rust.

Linhas estimadas

Doze mil.

O que extrai

De trafego HTTP capturado. Handle em URL. Handle em header customizado.
Handle em JSON de API. Handle em HTML. Handle em cookie.

De e-mail capturado. Handle em assinatura. Handle em corpo. Handle em
display name.

De TLS e HTTPS. SNI de subdominio que contem handle.

De fontes publicas. Twitter e X. Reddit. GitHub. GitLab. Bitbucket. Stack
Overflow. Mastodon. Discord. Telegram. Matrix. IRC. Fortuns phpBB. Fortuns
vBulletin. Fortuns Discourse. Pastebin. HackerNews. LinkedIn. Facebook.
Instagram. TikTok. Steam. Xbox Live. PlayStation Network. Riot Games.

O que faz com o que extrai

Normaliza handle. John underscore Doe, john hyphen doe, johndoe e JohnDoe
viram o mesmo fingerprint canonico.

Correlaciona handles que pertencem ao mesmo dono por seis criterios.

Criterio um, similaridade de string. Levenshtein. Jaro Winkler. Soundex.
Metaphone.

Criterio dois, similaridade de padrao. Regex match. CamelCase pattern. Typo
consistente.

Criterio tres, similaridade temporal. Handles criados proximos. Handles
ativos proximos.

Criterio quatro, similaridade comportamental. Mesmo horario de uso. Mesmo
jargao. Mesmos typos.

Criterio cinco, similaridade de rede. Mesmos contatos. Mesmos IPs.

Criterio seis, similaridade de bio. Mesmo texto. Mesmo link. Mesmo avatar
hash.

Extrai avatar. Calcula hash MD5 do pixel. Cruza entre plataformas. Detecta
avatar identico em duas ou mais plataformas.

Detecta username squatting. Handle que imita outro por um caractere.

Detecta conta fake. Criada ha menos de sete dias. Sem historico. Baixo
alcance.

Detecta conta burner. Usada uma vez. Abandonada.

Detecta sockpuppet. Multiplas contas. Mesmo IP. Mesma bio.

Detecta puppet. Mesmo dono. Persona diferente.

Correlaciona handle com e-mail. Handle com telefone. Handle com endereco
Bitcoin. Handle com endereco Ethereum.

Correlaciona handle com IP via atividade temporal. Correlaciona handle com
dispositivo via User-Agent unico. Correlaciona handle com localizacao via
timezone e horario de uso.

Constroi cadeia. Handle aponta para handle aponta para e-mail aponta para
handle aponta para telefone.

Detecta nome real. John Doe disfarcado de arroba j ponto doe.

Extrai handle de signature em e-mail. Extrai handle de footnote em texto.
Detecta handle mencionado em texto que nao e URL. Detecta mencao de handle
com arroba em conteudo. Detecta hashtag em conteudo para correlacao por
interesse.

Agrupa handles por cluster. Mesma pessoa. Mesma familia. Mesmo grupo.

Detecta roster. Lista de handles que sempre aparecem juntos.

Detecta hub handle. Mencionado por muitos. Menciona poucos.

Detecta bridge handle. Conecta dois clusters.

Saida

Fluxo de HandleEntity. Cada HandleEntity tem mais de cinquenta campos.
Arestas de handle para handle, handle para email, handle para ip.


MODULO 5
IPATTRIBUTOR

Responsabilidade

Atribuir endereco IP a entidade. Pessoa, organizacao ou dispositivo. Com
score de confianca.

Linguagem

Rust.

Linhas estimadas

Doze mil.

O que extrai

De trafego capturado. IPs de origem e destino. Portas. Protocolos. TLS JA3
fingerprint do ClientHello. TLS JA3S fingerprint do ServerHello. SSH HASSH
fingerprint. HTTP User-Agent. TCP fingerprint via opcoes SYN.

De fontes publicas. GeoIP construido de ARIN, RIPE, APNIC, LACNIC e AFRINIC.
ASN via dumps BGP. Organizacao dona do IP. Pais. Cidade. Hosting ou
residencial. Tor exit node via lista propria e heuristica. VPN via lista de
duzentos provedores. Proxy aberto via scan ativo.

De scan passivo. Banner de servico. Versao de SSH. Versao de HTTP. Versao
de SMTP. Certificado TLS. Issuer. SAN. Validade. Dominios hospedados via
SNI reverso. Portas abertas via SYN-ACK observado.

O que faz com o que extrai

Atribui IP a entidade. Com score de confianca.

Detecta Tor. Exit node. Relay. Hidden service.

Detecta VPN. Comercial. Corporativa.

Detecta proxy. Aberto. Residencial. Datacenter.

Detecta hosting. AWS. GCP. Azure. DigitalOcean. OVH. Hetzner. Linode. Vultr.

Detecta residencial. ISP versus hosting.

Detecta mobile. Operadora.

Detecta CGNAT. NAT de operadora. IP compartilhado.

Detecta IP spoofado. TTL anomalo. Opcoes TCP estranhas.

Constroi historico de uso. Mudanca de dono. Mudanca de ASN.

Calcula score de reputacao de zero a cem. Construido de eventos.

Mapeia IP para dispositivo. Via DHCP. Via ARP. Via User-Agent.

Mapeia IP para MAC. Via ARP. Via IPv6 EUI-64.

Mapeia IP para hostname. Via PTR. Via DHCP.

Mapeia IP para servicos abertos. Via scan passivo.

Mapeia IP para certificado TLS. Via handshake capturado.

Mapeia IP para dominios hospedados. Via SNI reverso.

Detecta IP em lista de C2 conhecido. Lista propria. Construida sozinha.

Detecta IP em lista de sinkhole. Idem.

Correlaciona IP com e-mail via sessao autenticada. Correlaciona IP com
handle via sessao. Correlaciona IP com dispositivo via JA3.

Detecta mesmo dispositivo com IP diferente via fingerprint.

Detecta mesmo IP com dispositivos diferentes via fingerprint.

Detecta roaming. Dispositivo muda IP mas mantem fingerprint.

Detecta bridge IP. Conecta dois clusters.

Saida

Fluxo de IPEntity. Cada IPEntity tem mais de setenta campos. Arestas de ip
para dispositivo. Arestas de ip para pessoa. Arestas de ip para organizacao.


MODULO 6
FUSIONENGINE

Responsabilidade

Unificar os cinco fluxos de coleta em um fluxo unico de eventos
enriquecidos. Resolver entidade. Desduplicar. Cruzar informacao.

Linguagem

Rust.

Linhas estimadas

Doze mil.

Por que existe

Sem o FusionEngine cada coletor fala uma lingua. O EmailExtractor ve um
endereco de e-mail. O IPAttributor ve um IP. O DomainResolver ve um dominio.
O HandleCorrelator ve um handle. O FusionEngine diz que todos esses dados
apontam para a mesma pessoa.

O que faz

Desduplica. Mesmo evento capturado duas vezes vira um evento. Mesmo e-mail
capturado em duas fontes vira uma entidade. Mesmo IP em dois eventos vira
uma entidade.

Enriquece cruzado. Pacote DNS mais pacote TLS vira a informacao de que um
IP visitou um dominio via HTTPS. E-mail mais SMTP vira a informacao de que
esse e-mail foi enviado por esse IP. HTTP mais User-Agent vira a informacao
de que esse handle acessou esse servico desse dispositivo. WHOIS mais DNS
vira a informacao de que esse dominio e registrado por essa organizacao com
esses nameservers. JA3 mais IP vira a informacao de que esse IP tem esses
dispositivos conectados. GeoIP mais ASN vira a informacao de que esse IP e
da AWS em Sao Paulo. Tor directory mais IP vira a informacao de que esse IP
e exit node ha tres dias. Avatar hash mais handle vira a informacao de que
essas tres contas usam o mesmo avatar.

Correlaciona temporal. Eventos do mesmo IP em janela de cinco minutos viram
sessao. Eventos do mesmo e-mail em janela de uma hora viram conversa.
Eventos do mesmo handle em janela de um dia viram atividade diaria. Eventos
do mesmo cluster em janela de sete dias viram campanha.

Correlaciona por fingerprint. JA3 identico em dois IPs vira mesmo
dispositivo. User-Agent identico em dois handles vira mesmo browser. Avatar
hash identico em duas plataformas vira mesmo dono. Bio identica em dois
perfis vira mesma pessoa. Padrao de timing identico vira mesmo bot.

Resolve entidade. Dado um evento de e-mail enviado para IP, resolve a
entidade pessoa. Entidade pessoa pode ter tres e-mails, dois handles,
quatro IPs e cinco dispositivos. Cada associacao tem confianca entre zero
e um. Associacao fraca fica como suspeita. Associacao forte fica como
confirmada.

Normaliza tempo. Timestamps de fontes diferentes viram UTC nanossegundo.
Timezone detectado por IP ou por padrao de atividade. Sincronizacao de
relogio assumindo NTP dos servidores.

O que nao faz

Nao decide se e interessante. Isso e responsabilidade do AnomalyScorer.
Nao agrupa em cluster. Isso e responsabilidade do ClusterEngine. Nao
classifica em categoria. Isso e responsabilidade do ClassifierEngine. Nao
emite alerta. Isso e responsabilidade do SignalEngine.

O FusionEngine so produz o fluxo mais limpo, enriquecido, desduplicado e
resolvido em entidade. Para que os modulos de analise possam operar.

Saida

Fluxo de EnrichedEvent. Cada EnrichedEvent tem campos ts, tipo,
entidade_src, entidade_dst, atributo, valor, features, confianca e fontes.
E o formato unico que alimenta o resto do sistema.


PARTE 3
CAMADA DE ANALISE
MODULOS 7 A 10


A camada de analise recebe o fluxo de EnrichedEvent produzido pelo
FusionEngine. Ela aprende o que e normal, agrupa entidades semelhantes,
classifica entidades em categorias e transforma tudo em sinais acionaveis.
Nenhum modelo pre-treinado e usado. Nenhuma biblioteca externa de machine
learning e usada. Cada algoritmo e escrito de baixo para cima, em Rust,
sem dependencia.


MODULO 7
ANOMALYSCORER

Responsabilidade

Aprender o que e normal e marcar o que nao e. Produzir score de anomalia
para cada entidade com explicacao detalhada.

Linguagem

Rust.

Linhas estimadas

Doze mil.

Features por entidade

Aproximadamente duzentas features sao computadas para cada entidade.

Frequencia temporal por hora, dia, semana e mes.

Entropia de destinos.

Diversidade de protocolos.

Padrao de burst. Silencio seguido de rajada.

Similaridade Jaccard com vizinhos.

Centralidade no grafo. PageRank, betweenness e closeness.

Embedding estrutural de sessenta e quatro dimensoes via random walk.
Algoritmo proprio. Nao usa node2vec.

Padrao de timing. Jitter. RTT medio. Variancia.

Padrao de tamanho. Bytes por evento. Distribuicao.

Padrao de horario. Timezone inferido.

Padrao de dispositivo. Fingerprint. Mudancas.

Padrao de conteudo. Tipo de payload. Entropia do payload.

Padrao de relacionamento. Quem fala com quem. Quem fala com ele.

Padrao de localizacao. Geografico. Mudancas.

Modelos usados

Cinco modelos. Cada um captura um tipo diferente de anomalia. O score
final e o ensemble dos cinco.

Modelo um, autoencoder esparso.

Arquitetura de duzentas para sessenta e quatro para duzentas. ReLU. Tres
camadas. Backpropagation escrita a mao. Otimizador Adam proprio.
Regularizacao L1 para esparsidade. Treinamento incremental online. Score
de anomalia igual ao erro de reconstrucao.

Modelo dois, Isolation Forest.

Constroi N arvores aleatorias. Score igual a profundidade media que o
ponto e isolado. Complementa o autoencoder. Captura anomalias globais.

Modelo tres, Local Outlier Factor.

Densidade local versus vizinhos. Detecta anomalia local que nao seria
detectada globalmente.

Modelo quatro, Matrix Profile.

Detecta motif e discord em series temporais. Encontra a serie que tem um
padrao que nao bate com nada.

Modelo cinco, One-Class SVM.

Fronteira de decisao nao linear via kernel RBF. Score igual a distancia
da fronteira.

Ensemble

Os cinco scores sao combinados com pesos aprendidos. Os pesos sao ajustados
ao longo do tempo com base em feedback do analista.

Explicabilidade

Para cada anomalia, o modulo retorna. Quais features contribuiram mais.
Quais features estao no percentil noventa e nove. Qual vizinho mais proximo
e por que nao e proximo. Qual baseline foi usado.

Saida

Fluxo de AnomalySignal. Cada sinal tem entidade, score, explicacao e top
features.


MODULO 8
CLUSTERENGINE

Responsabilidade

Agrupar entidades similares. Aprender novos clusters. Dissolver antigos
clusters. Detectar mudancas em clusters existentes.

Linguagem

Rust.

Linhas estimadas

Doze mil.

Algoritmos base

Quatro algoritmos de clustering. Cada um tem um proposito.

Algoritmo um, DBSCAN.

Distancia euclidiana em sessenta e quatro dimensoes usando o embedding do
autoencoder. Parametros eps e min_samples aprendidos automaticamente.
Deteccao de ruido. Pontos que nao pertencem a nenhum cluster ficam
marcados.

Algoritmo dois, HDBSCAN.

Hierarquia de densidade. Extracao automatica do numero de clusters.
Estabilidade do cluster. Probabilidade de pertencer.

Algoritmo tres, K-means mais mais.

Inicializacao k-means mais mais. Numero k escolhido por silhouette score.
Atualizacao incremental quando novas entidades chegam.

Algoritmo quatro, Gaussian Mixture Model.

Algoritmo EM de expectativa e maximizacao. Numero de componentes via BIC.
Probabilidade de pertencer a cada cluster.

Clustering temporal

Detecta clusters que existem ha trinta dias continuos.

Detecta clusters emergentes. Criados ha menos de sete dias. Crescendo.

Detecta clusters dissolvidos. Perderam mais de oitenta por cento dos
membros.

Detecta clusters mutantes. Mudaram de composicao em mais de cinquenta por
cento.

Clustering por multiplas dimensoes

Por comportamento usando features de timing.

Por infraestrutura usando features de rede.

Por conteudo usando features de payload.

Por relacionamento usando features de grafo.

Por identidade usando features de string.

Merge e split

Se dois clusters ficam proximos, propoe merge.

Se um cluster fica bimodal, propoe split.

Decisao automatica com confianca.

Rotulacao automatica de cluster

Nome automatico no formato regiao fonte periodo. Exemplo gmail brasil
dois mil e vinte e seis primeiro trimestre.

Top cinco entidades mais centrais.

Top cinco features discriminativas.

Marcacao de cluster novo ou evolucao de cluster existente.

Anomalia de cluster

Cluster com um membro muito diferente dos outros. Outlier interno.

Cluster que cresce rapido. Interessante.

Cluster que muda de comportamento. Suspeito.

Saida

Fluxo de ClusterSignal. Cada sinal tem cluster_id, tipo novo emergente
mutante ou dissolvido, membros, features e confianca.


MODULO 9
CLASSIFIERENGINE

Responsabilidade

Classificar entidades em categorias com explicabilidade completa.
Aprender com feedback do analista. Detectar drift.

Linguagem

Rust.

Linhas estimadas

Doze mil.

Categorias

Sete categorias. Ruido. Interessante. Critico. Ameaca. Oportunidade.
Investigacao. Arquivado.

Algoritmos base

Cinco algoritmos. Cada um tem um proposito.

Algoritmo um, regressao logistica multinomial.

Softmax com backpropagation manual. SGD puro. Treino online um exemplo por
vez. Labels sao as sete categorias. Retorna probabilidade calibrada.

Algoritmo dois, random forest.

Cem arvores. Profundidade maxima quinze. Bagging e feature randomness.
Importancia de feature via Gini.

Algoritmo tres, gradient boosting.

Modelo leve tipo XGBoost. Arvores de decisao como base. Otimizacao de
gradiente. Retorna score continuo.

Algoritmo quatro, naive Bayes.

Para classificacao rapida de baixo custo. Texto mais features numericas.
Retorna probabilidade simples.

Algoritmo cinco, k vizinhos mais proximos.

Distancia euclidiana ou cosseno. Vote por maioria com k igual a cinco.
Explicacao baseada em vizinhos.

Ensemble

Voto majoritario dos cinco classificadores com confianca calibrada. Se os
cinco discordam, entidade fica marcada como ambigua.

Active learning

Detecta entidade na fronteira. Confianca entre quarenta e sessenta por
cento. Pede feedback ao analista. Aprende com um exemplo por vez.

Drift detection

Distribuicao dos labels muda ao longo do tempo. Se muda, alerta. Modelo
ficou obsoleto. Retreina automaticamente.

Explicabilidade

Para cada classificacao, retorna. Top cinco features mais importantes.
Contribuicao de cada feature positiva ou negativa. Top tres vizinhos mais
proximos com seus labels. Confianca calibrada alem do softmax. Contrafactual.
O que mudaria a classificacao.

Saida

Fluxo de ClassifiedEntity. Cada entidade tem label, confidence, explanation
e counterfactual.


MODULO 10
SIGNALENGINE

Responsabilidade

Transformar anomalias, clusters e classificacoes em sinais acionaveis com
prioridade, confianca e explicacao.

Linguagem

Rust.

Linhas estimadas

Doze mil.

Regras contextuais

Duzentas regras curadas. Cada regra combina multiplas fontes de sinal. As
regras sao escritas em formato declarativo simples, sem dependencia externa.

Exemplos de regras.

IP que e Tor exit e contem e-mail marcado como alvo gera alerta.

Cluster novo com membros no Brasil gera sinal de revisao.

Entidade com anomalia acima de zero ponto nove e classificacao critico gera
sinal urgente.

Entidade com burst acima de dez vezes e silencio maior que trinta dias
gera sinal de reativacao.

Dominio recem registrado com e-mail marcado como alvo gera sinal de
phishing.

Score de sinal

Cada sinal tem prioridade entre zero e cem. A prioridade combina anomalia,
cluster tipo, label e regra contextual. Funcao de prioridade e monotona,
nao decrescente em cada argumento.

Deduplicacao

Se tres sinais apontam para a mesma entidade, agrupa em um sinal composto.
Se dois sinais contradizem, marca como conflito.

Cadeia de sinais

Sinal de IP suspeito mais sinal de e-mail com IP gera sinal de IP e e-mail
juntos indicando pessoa. Cadeia continua ate estabilizar.

Confianca calibrada

Baseada em forca das features, consenso de modelos e historico do analista.
Confianca de noventa e cinco por cento e rara. So sinais muito claros
atingem esse nivel.

Explicabilidade

Para cada sinal, retorna. O que foi detectado. Por que e importante. Quais
features contribuiram. Quem ja viu no historico. O que fazer, acao sugerida.

Feedback loop

Analista marca sinal como util ou ruido. Reforca ou desconta o sinal.
Aprende ao longo do tempo. O sinal aprendido influencia a prioridade de
sinais futuros.

Canais de alerta

Console na linha de status.

Log em arquivo.

Arquivo JSONL exportavel.

HTTP para envio externo.

Saida

Fluxo de Signal. Cada sinal tem id, tipo, entidades, prioridade, confianca,
explicacao e acao sugerida.


PARTE 4
CAMADA DE CONSULTA E EXPOSICAO
MODULOS 11 E 12


A camada de consulta recebe o grafo e os sinais. Ela mantem o grafo,
responde consultas complexas e expoe tudo via HTTP e WebSocket. E a camada
que fala com o operador humano.


MODULO 11
GRAPHBAULDER

Nome tecnico alternativo

GraphStore.

Responsabilidade

Construir e manter o grafo de entidades. Responder consultas estruturais
sobre o grafo. Versionar o estado. Exportar em multiplos formatos.

Linguagem

Rust.

Linhas estimadas

Doze mil.

O que armazena

Nos do grafo. Entidades dos tipos e-mail, handle, IP, dominio, MAC,
dispositivo, telefone, endereco Bitcoin, endereco Ethereum e hash de
arquivo.

Arestas do grafo. Eventos com timestamp, tipo, peso e confianca.

Armazenamento

Log estruturado mais indice invertido. Nao usa banco relacional. Nao usa
banco de grafo externo.

Compressao de series temporais via delta e varint.

Janela deslizante. Ultimos noventa dias em memoria. Mais antigos em disco
comprimido.

Propagacao de identidade

Se dois nos aparecem juntos tres vezes em contextos unicos, o grafo une
os dois nos em uma entidade superior. A uniao tem confianca. Uniao fraca
fica como sugestao. Uniao forte fica como fato.

Score de forca de aresta

Frequencia multiplicada por diversidade multiplicada por recencia
multiplicada por peso do evento.

Deteccao de estrutura

Deteccao de comunidade via Louvain proprio.

Deteccao de ponte entre duas comunidades.

Deteccao de hub com alta centralidade.

Deteccao de ilha. Componente conexo isolado.

Deteccao de ciclo. Triangulacao suspeita.

Deteccao de cadeia. Cadeia de comando.

Deteccao de same-actor. Mesma pessoa com multiplas personas via subgrafo
isomorfo.

Deteccao de bot. No com padrao muito regular via entropia temporal.

Deteccao de sockpuppet. Multiplos nos com mesmo IP e mesmo horario.

Deteccao de hub and spoke. Comando e controle com clientes.

Deteccao de mesh. Botnet ponto a ponto.

Deteccao de split. Grupo que se separou recentemente.

Deteccao de merge. Dois grupos que se juntaram recentemente.

Deteccao de drift. Entidade mudou de comportamento ao longo do tempo.

Deteccao de reactivation. Entidade silenciosa voltou.

Deteccao de cold start. Entidade nova sem historico.

Consulta

Funcao vizinhos. Retorna vizinhos de uma entidade ate profundidade N.

Funcao caminho. Retorna caminho entre duas entidades.

Funcao subgrafo. Retorna subgrafo que satisfaz criterio.

Funcao timeline. Retorna linha do tempo de uma entidade.

Funcao diff. Retorna diferenca entre dois snapshots temporais.

Indices

Indice invertido de entidade para eventos.

Indice invertido de evento para entidades.

Indice invertido de propriedade para entidades. Exemplo pais Brasil
retorna IPs. ASN numero retorna IPs. Dominio de e-mail gmail retorna
e-mails.

Versionamento

Snapshot periodico. Rollback para snapshot anterior.

Multi-tenant

Compartimentos isolados. Um compartimento nao ve dados de outro.

Saida

Grafo consultavel, exportavel, versionado.


MODULO 12
APIEXPOSER

Responsabilidade

Expor grafo, sinais, consultas, treino e metricas via HTTP, WebSocket e
gRPC. E a interface entre STUFFICK e o operador humano ou outro sistema.

Linguagem

Rust e Go.

Linhas estimadas

Doze mil.

Protocolos

HTTP versao um ponto um.

HTTP versao dois.

WebSocket para push de sinais em tempo real.

gRPC para alta performance binaria.

Endpoints HTTP

Metodo GET em barra api entidades. Lista entidades.

Metodo GET em barra api entidades barra id. Retorna uma entidade.

Metodo GET em barra api entidades barra id barra graph. Retorna subgrafo
ao redor da entidade.

Metodo GET em barra api entidades barra id barra timeline. Retorna linha
do tempo.

Metodo GET em barra api entidades barra id barra diff. Retorna diferenca
entre dois momentos.

Metodo GET em barra api sinais. Lista sinais.

Metodo GET em barra api sinais barra id. Retorna um sinal.

Metodo POST em barra api sinais barra id barra feedback. Marca sinal como
util ou ruido.

Metodo GET em barra api clusters. Lista clusters.

Metodo GET em barra api clusters barra id. Retorna um cluster.

Metodo GET em barra api anomalias. Lista anomalias.

Metodo POST em barra api query. Executa consulta em DSL.

Metodo GET em barra api models. Retorna status dos modelos.

Metodo POST em barra api models barra id barra retrain. Forca retreino.

Metodo GET em barra api health. Retorna saude do sistema.

Endpoints WebSocket

Caminho ws sinais. Stream de sinais em tempo real.

Caminho ws eventos. Stream de eventos enriquecidos.

Caminho ws logs. Stream de logs do sistema.

Autenticacao

Bearer token.

Mutual TLS com certificado cliente.

OAuth2 opcional.

Rate limiting

Por IP.

Por token.

Por endpoint.

Logging

Estruturado em JSONL. Cada requisicao vira uma linha. Cada erro vira uma
linha.

Metricas

Estilo Prometheus. Sem depender de Prometheus. Metricas de requisicoes
por segundo. Latencia por endpoint. Erros por tipo. Uso de memoria. Uso
de CPU. Uso de disco.

Backpressure

Se cliente lento, dropa. Nao bloqueia o resto do sistema.

Compressao

gzip.

zstd.

CORS

Configuravel.

OpenAPI

Especificacao gerada automaticamente a partir das rotas registradas.

Documentacao

HTML interativo. Um operador pode explorar a API pelo navegador.

Saida

API HTTP mais WebSocket mais gRPC com autenticacao, metricas e logs.


PARTE 5
FORMATO DE DADOS


Todos os fluxos entre modulos usam JSON Lines. Uma linha por evento. Sem
envelopes aninhados. Cada linha e um objeto JSON completo.

Evento cru

Campos obrigatorios. ts com nanossegundo UTC. camada com numero de um a
sete. proto com nome do protocolo. src com entidade de origem. dst com
entidade de destino. payload com bytes em base64. meta com objeto de
metadados.

Campos opcionais. credenciais quando capturadas. erro quando houve erro.

Entidade enriquecida

Campos obrigatorios. ts com nanossegundo UTC. tipo com tipo de evento.
entidade_src com identificador canonico. entidade_dst com identificador
canonico. atributo com nome do atributo. valor com valor do atributo.
features com objeto de features pre calculadas. confianca com numero
entre zero e um. fontes com lista de coletores que contribuiram.

Sinal

Campos obrigatorios. id com identificador unico. tipo com tipo de sinal.
entidades com lista de entidades envolvidas. prioridade com numero entre
zero e cem. confianca com numero entre zero e um. explicacao com texto
curto. acao_sugerida com texto curto.

Campos opcionais. features_top com lista de features mais relevantes.
historico com lista de sinais anteriores relacionados.


PARTE 6
ORDEM DE CONSTRUCAO


A construcao segue a ordem das camadas, de tras para frente. Primeiro a
analise. Depois a coleta. Depois a consulta. Depois a exposicao.

Motivo. A camada de analise e testavel com dados sinteticos. Nao depende
da camada de coleta. Uma vez testada, a camada de coleta alimenta a
camada de analise com dados reais. A camada de consulta consome o
resultado da analise. A camada de exposicao consome tudo.

Ordem dos modulos

Fase um. AnomalyScorer, ClusterEngine, ClassifierEngine e SignalEngine.
Quatro modulos. Total quarenta e oito mil linhas.

Fase dois. PacketCaptureEngine, EmailExtractor, DomainResolver,
HandleCorrelator, IPAttributor e FusionEngine. Seis modulos. Total
setenta e dois mil linhas.

Fase tres. GraphBuilder. Doze mil linhas.

Fase quatro. QueryEngine. Doze mil linhas.

Fase cinco. APIExposer. Doze mil linhas.

Ordem de testes

Cada modulo tem testes unitarios. Cada modulo tem testes de integracao.
Cada modulo tem teste end to end com dados sinteticos.

Cada fase so avanca quando a anterior passa em todos os testes.

Cada modulo entrega. Codigo. Testes. Documentacao de uso. Metrica de
performance. Metrica de precisao quando aplicavel.


PARTE 7
CRITERIOS DE ACEITACAO


O sistema completo so e considerado aceito quando satisfaz todos os
criterios abaixo.

Criterio um. Todos os doze modulos compilam sem erro. Sem warning.

Criterio dois. Todos os testes unitarios passam. Cobertura acima de
oitenta por cento.

Criterio tres. Todos os testes de integracao passam. Fluxo completo
desde a captura ate o sinal funciona end to end.

Criterio quatro. Com dados sinteticos, o AnomalyScorer detecta as cinco
anomalias escondidas com precisao acima de noventa por cento e revocacao
acima de noventa por cento.

Criterio cinco. Com dados sinteticos, o ClusterEngine identifica os tres
clusters embutidos com pureza acima de noventa e cinco por cento.

Criterio seis. Com dados sinteticos, o ClassifierEngine atinge acuracia
acima de noventa por cento nas sete categorias.

Criterio sete. Com dados reais de rede local, o PacketCaptureEngine
captura cem por cento dos pacotes sem perda.

Criterio oito. Com dados reais de e-mail, o EmailExtractor extrai cem por
cento dos enderecos validos presentes nos arquivos de teste.

Criterio nove. Com dados reais de dominio, o DomainResolver resolve cem
por cento dos dominios registrados.

Criterio dez. Com dados reais de handle, o HandleCorrelator correlaciona
handles do mesmo dono com precisao acima de oitenta por cento.

Criterio onze. Com dados reais de IP, o IPAttributor atribui IP a pessoa
correta com precisao acima de oitenta por cento.

Criterio doze. O FusionEngine combina os cinco fluxos sem perder evento.
Sem duplicar evento.

Criterio treze. O GraphBuilder responde consulta de vizinhos em menos de
cem milissegundos para entidade com cem mil arestas.

Criterio quatorze. O QueryEngine responde consulta DSL em menos de
quinhentos milissegundos para grafo com um milhao de nos.

Criterio quinze. O APIExposer atende mil requisicoes por segundo em
hardware modesto.

Criterio dezesseis. Todo o sistema cabe em cem megabytes de memoria para
um milhao de eventos.

Criterio dezessete. Todo o sistema roda em Termux no Android sem
dependencia externa.

Criterio dezoito. Nenhum modulo depende de servico de nuvem. Nenhum
modulo envia dado para fora sem comando explicito do operador.

Criterio dezenove. Todo sinal tem explicacao. Nenhum sinal e caixa preta.

Criterio vinte. Todo modelo pode ser revertido ao estado anterior. Todo
treinamento tem snapshot antes e depois.


FIM DO DOCUMENTO


Este documento descreve a arquitetura completa de STUFFICK. Implementacao
segue a ordem de construcao definida na Parte 6. Cada modulo e construido
isoladamente, testado isoladamente e integrado ao todo quando aprovado.

A camada de analise vem primeiro. Ela prova que o machine learning proprio
funciona. A camada de coleta vem depois. Ela alimenta a analise com dados
reais. A camada de consulta e exposicao vem por ultimo. Ela entrega o
sistema ao operador.

O sistema nao e XKeyscore. O sistema e uma evolucao de XKeyscore. Faz o
que XKeyscore fazia e faz mais. Aprende sozinho. Explica cada decisao.
Roda em um dispositivo. Nao depende de nuvem. Nao depende de modelo
pre treinado.
