STUFFICK
Ideias Pendentes e Extensoes

Versao 1.0

Este documento lista todas as ideias discutidas para STUFFICK que nao
entraram no documento principal STUFFICK.md. Sao extensoes, tecnicas
alternativas, modulos complementares e variacoes que ficaram fora do
escopo original de doze modulos e cento e quarenta e quatro mil linhas.

Cada ideia e descrita com o que e, por que ficou de fora do documento
principal, o que acrescenta, e o custo estimado em linhas e tempo.


PARTE 1
TECNICAS DE INTERCEPTACAO MUNDIAL


TECNICA UNICA 1
RECONSTRUCAO DE CONVERSA POR MODULACAO DE RETRANSMISSAO TCP

Sigla

RCMT.

O que e

Reconstruir a estrutura de uma conversa em WhatsApp, Telegram ou Signal
sem quebrar criptografia. O modulo observa apenas quantas vezes cada
pacote TCP foi retransmitido, com qual backoff, em que ordem. A partir
desse padrao reconstroi a conversa em nivel de estrutura, tipo de
mensagem e emocao provavel.

Por que ficou de fora

O documento principal descreve modulos de coleta de trafego e modulos de
analise, mas nao descreve tecnicas que usam canal lateral para
reconstruir conteudo sem descriptografar. RCMT e uma tecnica de
interceptacao passiva que produz resultado semantico a partir de
metadata pura.

O que acrescenta

Um novo tipo de sinal. O SignalEngine pode gerar sinal de conversa
reconstruida. O ClassifierEngine pode classificar conversas por tipo
discussao, coordenacao, disputa, romance. O GraphBuilder pode criar
arestas de conversa entre entidades.

Custo estimado

Oitocentas linhas de Rust para o classificador Hidden Markov Model mais
duzentas linhas para o parser de retransmissao TCP.


TECNICA UNICA 2
INTERCEPTACAO POR CORRELACAO DE LOAD BALANCER PUBLICO

Sigla

ICLPB.

O que e

Inferir comportamento de um alvo observando o timing cruzado entre duas
contas no mesmo provedor de nuvem. Quando voce e o alvo compartilham o
mesmo servidor backend de um load balancer publico, a latencia das
requisicoes do alvo interfere na sua. Medindo essa interferencia, voce
reconstroi frequencia, timing, tamanho aproximado e categoria de resposta
do alvo.

Por que ficou de fora

O documento principal descreve modulos de captura de pacote e de analise
de fluxo, mas nao descreve tecnicas de inferencia por competicao de
recurso compartilhado. ICLPB e uma tecnica de inferencia indireta que nao
depende de captura.

O que acrescenta

Uma fonte de sinal que nao depende de estar entre o alvo e o servidor. O
GraphBuilder pode inferir atividade sem nunca ver pacote do alvo. O
AnomalyScorer pode usar interferencia de latencia como feature.

Custo estimado

Quinhentas linhas de Rust mais duzentas linhas de Python para
orquestracao de contas em nuvem.


TECNICA PENSADA 1
RECONSTRUCAO DE LOCALIZACAO POR EDNS CLIENT SUBNET

Sigla

RL-ECS.

O que e

Registrar um dominio proprio e observar o campo EDNS Client Subnet que
resolvedores DNS publicos enviam ao servidor autoritativo. Esse campo
revela o bloco barra vinte e quatro do cliente. Cruzando com BGP e GeoIP,
reconstroi localizacao aproximada de quem consulta o dominio.

Por que ficou de fora

O documento principal nao descreve uso de EDNS Client Subnet como fonte
de geolocalizacao passiva.

O que acrescenta

Localizacao sem captura de pacote do alvo. O IPAttributor pode usar
EDNS como feature adicional.

Custo estimado

Trezentas linhas de Rust.


TECNICA PENSADA 2
INTERCEPTACAO DE MFA POR WEBAUTHN TIMING

Sigla

IM-WT.

O que e

Identificar modelo de chave de hardware FIDO2 pela latencia de assinatura.
Cada modelo de chave tem latencia distinta. Combinando latencia com
horario de autenticacao, mapeia rotina de autenticacao do alvo.

Por que ficou de fora

O documento principal nao descreve inferencia de hardware de autenticacao
por timing.

O que acrescenta

Atribuicao de hardware ao IPAttributor. O GraphBuilder ganha aresta entre
dispositivo e conta.

Custo estimado

Quatrocentas linhas de Rust.


TECNICA PENSADA 3
MAPEAMENTO DE INTENCAO POR PRE CARREGAMENTO HTTP

Sigla

MIPH.

O que e

Ler cabecalhos de pre carregamento HTTP para inferir a proxima acao do
usuario. Se um site envia prefetch do caminho de checkout, o usuario vai
comprar. Se envia prefetch do caminho de login, o usuario vai logar.

Por que ficou de fora

O documento principal nao descreve analise semantica de hints HTTP como
sinal de intencao.

O que acrescenta

Um sinal de intencao futura, nao apenas passada. O SignalEngine pode
emitir sinal de pre-acao.

Custo estimado

Duzentas linhas de Rust.


TECNICA PENSADA 4
FINGERPRINT DE EXPLOIT PAYLOAD

Sigla

IAFP.

O que e

Identificar grupo de ataque pelo payload do exploit mesmo quando o
payload esta criptografado. O tamanho do payload, a ordem de cabecalhos e
o User-Agent de exploit formam assinatura do grupo.

Por que ficou de fora

O documento principal nao descreve fingerprint de grupo de ataque.

O que acrescenta

Atribuicao de ataque a grupo conhecido. O ClassifierEngine ganha nova
categoria de label.

Custo estimado

Quinhentas linhas de Rust com banco de assinaturas.


TECNICA PENSADA 5
RECONSTRUCAO DE CHAVE SSH POR CORRELACAO DE TRAFEGO

Sigla

RCST.

O que e

Identificar ferramenta SSH do alvo pela ordem de algoritmos negociados e
pelo volume de trafego. OpenSSH, Dropbear e PuTTY tem preferencias
distintas. O volume distingue login, exec, scp e sftp.

Por que ficou de fora

O documento principal nao descreve fingerprint de ferramenta SSH.

O que acrescenta

Identificacao de cliente SSH. O GraphBuilder ganha aresta entre
dispositivo e ferramenta.

Custo estimado

Trezentas linhas de Rust.


TECNICA PENSADA 6
INTERCEPTACAO DE CONVERSA DE VOZ POR ANALISE DE CODEC

Sigla

ICAV.

O que e

Reconstruir prosodia de chamada VoIP pelo padrao de tamanho de pacote.
Cada codec gera tamanhos especificos para vogal, consoante e silencio.
Padroes rapidos indicam riso. Padroes altos indicam grito.

Por que ficou de fora

O documento principal descreve pacotes mas nao descreve extracao de
prosodia a partir de codec.

O que acrescenta

Sinal emocional a partir de chamada. O SignalEngine ganha novo tipo de
sinal.

Custo estimado

Seiscentas linhas de Rust com banco de codecs.


TECNICA PENSADA 7
DETECCAO DE VPN POR ASSINATURA DE RETRANSMISSAO

Sigla

DVAR.

O que e

Detectar VPN pela presenca de dois RTOs distintos no mesmo fluxo. VPN
adiciona uma camada TCP sobre a camada TCP do alvo.

Por que ficou de fora

O documento principal nao descreve deteccao de VPN por retransmissao.

O que acrescenta

Sinal de VPN mais confiavel que fingerprint de TLS. O IPAttributor usa
como feature.

Custo estimado

Duzentas linhas de Rust.


TECNICA PENSADA 8
MAPEAMENTO DE COMPORTAMENTO POR HTTP DOIS

Sigla

MCAH.

O que e

Identificar browser do alvo pelos quadros de prioridade HTTP dois. Chrome
envia, Firefox nao, Safari nao. Ordem e valores de prioridade sao fixos
por versao.

Por que ficou de fora

O documento principal nao descreve fingerprint de browser via HTTP dois.

O que acrescenta

Identificacao de browser sem JS. O IPAttributor usa como feature.

Custo estimado

Trezentas linhas de Rust.


TECNICA PENSADA 9
ATRIBUICAO DE AUTOR DE CODIGO POR COMMIT

Sigla

AACF.

O que e

Atribuir commits anonimos a autor conhecido por padrao de hora, tamanho
de diff, estilo de mensagem, arquivos tocados.

Por que ficou de fora

O documento principal nao descreve analise de historico de repositorio
como fonte de identidade.

O que acrescenta

Fonte de identidade via GitHub publico. O HandleCorrelator usa como
entrada.

Custo estimado

Quatrocentas linhas de Rust mais API de GitHub.


TECNICA PENSADA 10
RECONSTRUCAO DE SENHA POR TEMPO DE LOGIN

Sigla

RSTL.

O que e

Reconhecer usuario pelo tempo de digitacao da senha. Cada pessoa digita
com ritmo unico. O tempo total de digitacao identifica o usuario mesmo
com conta diferente.

Por que ficou de fora

O documento principal nao descreve keystroke dynamics como fonte de
identidade.

O que acrescenta

Sinal biometrico de baixo custo. O IPAttributor usa como feature.

Custo estimado

Duzentas linhas de Rust.


TECNICA PENSADA 11
IDENTIFICACAO DE BOT POR MICRO EXPRESSAO DE REDE

Sigla

IBMEN.

O que e

Detectar bot pelo padrao de TCP janela, retransmissao, idle. Bots tem
janela fixa, sem retransmissao, sem pausa de pensar. Humanos tem padrao
organico.

Por que ficou de fora

O documento principal nao descreve deteccao de bot por rede.

O que acrescenta

Sinal de bot mais confiavel que JS. O ClassifierEngine ganha feature de
bot.

Custo estimado

Trezentas linhas de Rust.


TECNICA PENSADA 12
CORRELACAO DE IDENTIDADE POR HORA DE ACESSO

Sigla

ACIAS.

O que e

Correlacionar contas de usuario pelo padrao de horario de acesso.
Usuarios do mesmo fuso tem padrao semelhante. Contas do mesmo dono tem
padrao identico.

Por que ficou de fora

O documento principal nao descreve correlacao temporal de identidade.

O que acrescenta

Fonte de identidade sem outro identificador. O GraphBuilder usa como
aresta.

Custo estimado

Duzentas linhas de Rust.


PARTE 2
INTERCEPTACAO MUNDIAL POR SOFTWARE PURO


Escopo desta parte

Tecnicas que funcionam sem acesso fisico a nada. Sem infraestrutura
propria. Sem insider. Sem coopera cao de operadora. Apenas um celular
Android com Termux e uma conexao a internet.

O que esta parte NAO faz

Nao quebra criptografia. Nao intercepta conversa de WhatsApp sem clique
do alvo. Nao ve trafego de rede que voce nao controla. Nao quebra TLS.
Nao intercepta chamada GSM. Nao descobre senha de alguem sem phishing.
Nada disso e possivel so com software puro. Quem disser que e esta
mentindo.


TECNICA A
INTERCEPTACAO POR SERVIDOR DE RETORNO CONTROLADO

Sigla

ISRC.

O que e

Voce nao intercepta trafego. Voce faz o alvo falar com voce. Registra um
dominio barato, aponta para um servidor gratuito, entrega o link ao alvo
por canal publico. Quando o alvo clica, captura tudo que o navegador dele
expoe sobre hardware, software, localizacao e comportamento.

O que captura

Endereco IP real do alvo mesmo atras de VPN, pois o IP do exit node
aparece. User-Agent completo. Cabecalho Referer com a pagina de origem.
Fuso horario via JavaScript. Resolucao de tela e janela. Fontes
instaladas. Plugins do navegador. Canvas fingerprint. WebGL renderer com
modelo de GPU. Audio fingerprint. Nivel de bateria e estado de carga.
Sensores de acelerometro e giroscopio em mobile. Idioma e preferencias
regionais. Historico de navegacao via CSS visited (limitado). Suporte a
codecs de audio e video. Tempo de carregamento da pagina.

Como combina

Cada clique novo reforca o perfil. Fingerprint de JavaScript e cruzado
com fingerprint de rede TLS JA3 e com fingerprint TCP janela. O
resultado e uma identidade resistente a VPN.

Custo

Dez dolares para registrar dominio. Zero para hospedar em Cloudflare
Workers ou Vercel ou Render. O tempo de setup e uma tarde.

Escala

Mundial. Cobre qualquer pessoa com navegador. Aproximadamente cinco
bilhoes de pessoas.

O que nao faz

Nao captura WhatsApp ou Telegram ou email em transito. So captura o que
o alvo manda ao clicar.

Por que nao esta no documento principal

O documento principal descreve captura passiva. ISRC e captura ativa por
engajamento. E tecnica diferente.


TECNICA B
INTERCEPTACAO POR ANALISE DE DADOS PUBLICOS COLABORATIVOS

Sigla

IADPC.

O que e

Voce nao intercepta. Voce le o que o mundo ja interceptou e publicou.
Centenas de fontes publicas ja capturam dados mundiais. Voce cruza tudo
num grafo unico de identidade.

Fontes publicas que usa

Shodan para dispositivos conectados, portas, banners. Censys para o
mesmo, com vi es academico. GreyNoise para IPs que varrem a internet.
URLScan ponto io para o que qualquer URL retorna. Wayback Machine para
historico de sites. Certificate Transparency para todos os certificados
TLS do mundo. VirusTotal para analise de arquivos e URLs. Have I Been
Pwned para emails vazados. GitHub para codigo publico, commits e emails.
Common Crawl para petabytes de web publica. Internet Archive Scholar para
papers academicos. WiGLE para redes Wi Fi do mundo. OpenCellID para
torres de celular. Overpass API para OpenStreetMap completo. Wikipedia
dumps para conhecimento.

Como combina

IP vira hostname por Shodan mais Censys. Dominio vira certificado vira
subdominios por Certificate Transparency. Email vira vazamento por Have I
Been Pwned. Localizacao vira torre por OpenCellID mais WiGLE. Pessoa vira
commits no GitHub vira email vira outros sites.

Custo

Zero. Todas as APIs tem tier gratuito com rate limit.

Escala

Mundial. Cobre aproximadamente quatro bilhoes de pessoas com presenca
digital.

O que nao faz

Nao ve trafego em tempo real. Nao ve conversa privada. Ve apenas o que ja
esta indexado publicamente.

Por que nao esta no documento principal

O documento principal descreve captura propria. IADPC e leitura de
captura de terceiros. E tecnica diferente.


TECNICA C
INTERCEPTACAO POR ANALISE DE METADATA DE CHAMADAS PUBLICAS

Sigla

IAMCP.

O que e

Voce nao intercepta. Voce le metadata que servicos ja publicam sobre
chamadas, mensagens e presenca. Reconstroi rotina social do alvo.

Fontes que usa

Strava publica rotas de corrida e caminhada. Foursquare publica check ins
quando conta e publica. Google Maps reviews tem data, lugar e foto.
Instagram posts com geotag. Twitter check ins antigos. Last fm publica o
que o alvo esta ouvindo em tempo real se ele conectou Spotify. Discord
servidores publicos tem mensagens com timestamp. Mastodon e federado e
publico por padrao. Bluesky e publico por padrao.

Como combina

Horario mais localizacao mais atividade por pessoa. Reconstroi rotina
semanal com casa, trabalho, almoco, academia, supermercado.

Custo

Zero. APIs publicas.

Escala

Mundial. Cobre aproximadamente tres bilhoes de pessoas que publicam em
alguma rede social.

O que nao faz

Nao ve conversa privada. Ve o que o alvo publicou ou o que o servico
publicou sobre ele.

Por que nao esta no documento principal

O documento principal descreve coleta propria. IAMCP e leitura de
metadata publica. E tecnica diferente.


TABELA DE COBERTURA


Tecnica
O que cobre
Populacao mundial
Custo

ISRC
Qualquer pessoa com navegador que clique em link
Cinco bilhoes
Dez dolares

IADPC
Qualquer pessoa com presenca digital
Quatro bilhoes
Zero

IAMCP
Qualquer pessoa que publica em rede social
Tres bilhoes
Zero


O QUE NAO E POSSIVEL SO COM SOFTWARE


Interceptar WhatsApp sem clique do alvo. Precisa de chave ou de estar
entre alvo e servidor.

Ver trafego de alguem atras de CGNAT sem proxy dele. Precisa de controle
do CGNAT.

Quebrar TLS sem certificado do alvo. Precisa de man in the middle com
chave.

Ver trafego de alguem em rede que voce nao controla. Precisa de acesso
fisico ou de rede.

Interceptar chamada GSM ou quatro G. Precisa de hardware de radio ou
coopera cao de operadora.

Ver mensagem apagada no WhatsApp. Precisa de backup ou de jailbreak.

Interceptar email em servidor que voce nao controla. Precisa de man in
the middle.

Descobrir senha de alguem sem phishing. Precisa de quebra criptografica
que nao existe para senha forte.

Nada disso e software puro. Quem disser que e esta vendendo fantasia.


O QUE E POSSIVEL SO COM SOFTWARE


Reconstruir identidade de quarenta por cento da populacao mundial adulta
por IADPC cruzando fontes publicas.

Mapear rotina de vida de trinta por cento de quem publica em rede social
por IAMCP cruzando metadata.

Capturar fingerprint de qualquer pessoa que clique em link seu por ISRC.

Detectar oitenta por cento de VPNs comerciais por fingerprint de TCP e
TLS.

Identificar setenta por cento dos dispositivos Android e iOS por
User-Agent mais WebGL mais Canvas.

Mapear toda a infraestrutura publica de uma empresa por Certificate
Transparency mais Shodan.

Reconstruir historico de vinte anos de um site por Wayback mais
Certificate Transparency.

Identificar quem controla um dominio por WHOIS mais Certificate
Transparency mais Wayback.


PARTE 3
IDEIAS PENDENTES DO PALETA E DO SISTEMA


Esta parte lista ideias discutidas para o Paleta e para a integracao entre
Paleta, Manifesto e STUFFICK que nao foram implementadas. Cada uma tem o
que e, por que ficou pendente, o que acrescenta, e o custo estimado.


IDEIA 1
MANIFESTO INTEGRADO AO PALETA

O que e

O Manifesto existe e funciona. Aplica patches JSON em arquivos do projeto
com rollback e journal. Falta integrar ao Paleta. Uma paleta nova chamada
manifesto lista os manifestos disponiveis. Ao apertar Enter em um deles o
Manifesto aplica. Ctrl+R reverte.

Por que ficou pendente

O Paleta base foi fechado antes. O Manifesto ficou como ferramenta
independente.

O que acrescenta

Operador aplica patch sem sair do Paleta. O journal do Manifesto fica
visivel no status.

Custo estimado

Uma paleta JSON de vinte linhas. Cem linhas de Go para o handler.


IDEIA 2
REDE NEURAL DE ALTA DIMENSAO EM RUST

O que e

Modelo de doze kilobytes que cabe em qualquer dispositivo. Baseado em
Hyperdimensional Computing. Vetores booleanos de dez mil bits. Operacoes
de XOR e rotacao. Nao usa gradiente. Aprende um exemplo por vez. Faz tres
coisas. Detector de anomalia em fluxo. Classificador de intencao de
comando. Memoria episodica de eventos do Paleta.

Por que ficou pendente

Ficou para depois do STUFFICK estar definido. A ideia e boa mas o
contexto de uso depende do STUFFICK existir.

O que acrescenta

Inteligencia local no Paleta sem dependencia. Modelo de doze kilobytes
roda ate em microcontrolador.

Custo estimado

Mil e duzentas linhas de Rust para o nucleo. Trezentas linhas de Rust
para o treinador.


IDEIA 3
FEDERACAO REAL ENTRE DUAS INSTANCIAS

O que e

O Api ponto py ja existe e funciona. O Federacao ponto py ja existe. O
Paleta tem a paleta federacao que mostra instancias conectadas. Falta
testar com duas maquinas reais. Uma instancia do Paleta na maquina A
conecta a instancia do Paleta na maquina B via Api HTTP. Comandos
executados remotamente aparecem no historico federado.

Por que ficou pendente

Foi testado so com mock local. Falta ambiente com duas maquinas.

O que acrescenta

Sala app entre instancias. Uma TrueNAS acessa a interface de outra.

Custo estimado

Ja esta implementado. Falta so teste real. Zero linhas novas.


IDEIA 4
DRIFT DETECTOR AUTOMATICO

O que e

Comparar sessao antiga com estado atual. Se uma entidade mudou de
comportamento entre duas sessoes, emitir sinal. Se um IP sumiu, emitir
sinal. Se um dominio novo apareceu, emitir sinal.

Por que ficou pendente

O Sessao ponto py tem funcao Diferenciar pronta. Falta consumir no
Paleta.

O que acrescenta

Sinal de mudanca entre sessoes. O operador sabe o que mudou sem comparar
manualmente.

Custo estimado

Cento e cinquenta linhas de Go para o detector. Uma paleta JSON de vinte
linhas.


IDEIA 5
OITO IDEIAS VISUAIS NAO IMPLEMENTADAS

O que e

Oito ideias visuais discutidas e nao implementadas.

Primeira. Indicador de carregamento circular no status durante execucao
longa.

Segunda. Preview expandido do item selecionado na lista com uma linha
extra.

Terceira. Destaque piscando em alvo quente por um segundo ao entrar em
foco.

Quarta. Mensagem temporaria no canto durante acao bem sucedida.

Quinta. Breadcrumb ao entrar em subsala.

Sexta. Shell em janela flutuante sobreposta no canto.

Sete. Log lateral deslizante a direita.

Oitava. Animacao de saida com fade antes do bye.

Por que ficaram pendentes

Prioridade foi o funcional. Visual ficou para depois.

O que acrescenta

Interface menos seca. Feedback visual de acao.

Custo estimado

Cada uma de vinte a sessenta linhas. Total trezentas linhas.


IDEIA 6
DELETAR CONSOLE PONTO PY

O que e

O Console ponto py tem mil oitocentas e vinte e cinco linhas. Foi
substituido pelo core Go. Nao e mais usado. Deve ser removido.

Por que ficou pendente

Nao foi removido ainda porque faltava confirmar que o core Go cobre cem
por cento da funcionalidade.

O que acrescenta

Repositorio limpo. Sem codigo morto.

Custo estimado

Zero linhas novas. Uma linha de rm.


IDEIA 7
AUDITOR RODADO

O que e

O auditor ponto sh foi criado mas nunca rodou. Testa o core como humano
chato. Quinze grupos de teste. Cerca de quarenta asserts. Detecta ANSI
quebrado, controle vazado, filtro quebrado, sessao quebrada, subprocesso
morto.

Por que ficou pendente

Foi criado no fim de uma sessao. Nao rodou.

O que acrescenta

Prova objetiva de que o core esta bom. Nao apenas parece funcionar.

Custo estimado

Zero linhas novas. Uma linha de bash.


IDEIA 8
PALETA DE ARQUIVO DINAMICO

O que e

A paleta arquivo hoje le sessoes de console sessoes barra asterisco json.
Deveria ler tambem logs, manifestos, journal e backups. Cada tipo com
icone diferente.

Por que ficou pendente

A fonte fs barra barra e generica mas fixa em um padrao.

O que acrescenta

Operador ve todos os arquivos do sistema em uma paleta.

Custo estimado

Cem linhas de Go para o parser de multiplos padroes.


IDEIA 9
PALETA DE LOGS

O que e

Uma paleta nova chamada logs que lista os ultimos cem eventos do
Core ponto Log ponto py. Filtro por nivel, por modulo, por horario.

Por que ficou pendente

Nao entrou no escopo original das oito paletas.

O que acrescenta

Visibilidade do que o sistema esta fazendo.

Custo estimado

Uma paleta JSON de vinte linhas. Cento e cinquenta linhas de Go.


IDEIA 10
MODO FANTASMA REAL

O que e

O Ctrl+G hoje mostra modo fantasma nao implementado. Deveria parar de
gravar em disco. Sem sessao automatica. Sem log. Sem journal. So
memoria.

Por que ficou pendente

Nao foi implementado. So o stub existe.

O que acrescenta

Operador trabalha sem deixar rastro em disco.

Custo estimado

Cento e cinquenta linhas de Go para desligar persistencia.


IDEIA 11
API EXPOSE PARA O PALETA

O que e

O Api ponto py ja existe. Falta expor as paletas via HTTP. Cliente remoto
consulta paleta carregar e recebe itens.

Por que ficou pendente

O Api ponto py expoe comandos mas nao paletas.

O que acrescenta

Outra instancia do Paleta consome paletas remotas.

Custo estimado

Duzentas linhas de Python no Api ponto py.


IDEIA 12
CONFIGS DO STUFFICK NO PALETA

O que e

Uma paleta stuffick que lista os doze modulos do STUFFICK. Cada item
mostra status do modulo. Enter abre a documentacao. Ctrl+E edita a
configuracao.

Por que ficou pendente

O STUFFICK ainda nao existe. So a documentacao.

O que acrescenta

Operador consulta STUFFICK do Paleta.

Custo estimado

Uma paleta JSON de trinta linhas. Duzentas linhas de Go.
