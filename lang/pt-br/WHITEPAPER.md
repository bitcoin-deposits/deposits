# bitcoin deposits
## resumo

uma versao ideal de dinheiro eletronico ponto a ponto permitiria que pagamentos online fossem enviados diretamente de uma parte para outra de forma rapida e com preparacao minima. a lightning network fornece parte da solucao, mas os beneficios essenciais sao perdidos se um terceiro confiavel for necessario para gerenciar o estado em seu nome. propomos uma solucao para este problema usando livros-razao verificaveis e uma rede de garantias. operadores transmitem atualizacoes do livro-razao para seus pares, criando um registro auditavel de contas. carteiras transmitem evidencias de desonestidade para esses pares, que garantem que o livro-razao mantenha um operador honesto. a saida unilateral e substituida pela garantia de que os fundos permanecem disponiveis enquanto a rede existir. chegamos a uma rede que delega a manutencao de liquidez, evita taxas de configuracao, e capaz de receber pagamentos offline, e escala independentemente da camada base

## introducao

bitcoin deposits visa fornecer fundos rapidos e escalaveis controlados por chave, de forma trustless, off-chain. a atividade on-chain escala com o numero de livros-razao e a frequencia de rotacao de reservas. a capacidade de processamento escala ligeiramente acima de linearmente com o numero de livros-razao na rede, tornando plausivel milhoes de transacoes por segundo em trilhoes de carteiras

existem tradeoffs explicitos:
- sem saida unilateral: quando operadores falham, os fundos permanecem na rede
- sem privacidade: a verificacao requer transparencia
- disponibilidade intermitente: um deposito e tao disponivel quanto o operador. carteiras devem distribuir fundos para aumentar a disponibilidade

esperamos que a experiencia da carteira seja semelhante a uma camada base rapida, tendo uma economia de pagamentos semelhante a lightning network

## livros-razao

um livro-razao e uma cadeia imutavel de atualizacoes, contendo o hash da atualizacao anterior e assinada pelo operador do livro-razao. diferentes tipos de atualizacao tem regras diferentes que governam quando e como podem ser usados. livros-razao sao autodescritivos, suas atualizacoes sao publicamente disponiveis e irrefutaveis, permitindo que qualquer pessoa avalie a conformidade

livros-razao tem um unico operador ativo, mas sao mantidos cooperativamente pela malha. qualquer operador pode criar um, mas caso desapareca ou se torne desonesto, um operador diferente sera designado, junto com as reservas. o operador atualmente ativo e identificado pela chave publica usada para assinar a atualizacao co-assinada mais recente

## depositos

um deposito e uma conta estavel que pode enviar e receber fundos, controlada por miniscript. na abertura, uma tabela de taxas e estabelecida, assim como se o recebimento de fundos requer uma solicitacao assinada pela carteira. um operador deve permitir transferencias entre depositos no mesmo livro-razao, bem como saidas on-chain. eles devem permitir que depositos paguem faturas lightning

fica a criterio do operador criar ofertas de financiamento on-chain ou faturas lightning em nome de um deposito. se o fizerem, estas devem ser co-assinadas por um membro do quorum, e a carteira deve verificar esta assinatura. ofertas e faturas nao fazem parte do livro-razao, portanto e responsabilidade da carteira verificar assinaturas e rete-las como evidencia

## taxas

transferencias entre depositos, on-chain e atraves da lightning tem taxas pagas ao operador do livro-razao. tambem ha taxas aplicadas periodicamente a saldos com um periodo especificado. todas sao negociadas quando um novo deposito e aberto. as taxas podem ser alteradas apos um numero especificado de blocos, dado um aviso previo em blocos especificado e dentro de um limite percentual por ajuste negociado na abertura. o quorum pode recusar co-assinar atualizacoes que criem circunstancias nao lucrativas pelas quais poderiam ser responsabilizados

## transferencias

a forma basica de transferencia e uma operacao em duas fases entre dois depositos no mesmo livro-razao: um deposito emite uma solicitacao para enviar fundos. se houver fundos suficientes disponiveis, um bloqueio sobre os fundos com uma condicao de gasto e adicionado ao livro-razao. se a condicao de gasto for cumprida antes de um tempo limite, os fundos sao movidos do remetente para o destinatario menos a taxa do operador. se o tempo limite for atingido, o bloqueio e liberado, menos uma taxa menor do operador. com condicoes de gasto miniscript, isso e suficiente para permitir que qualquer deposito forneca pontes e servicos de liquidez para outros depositos no mesmo livro-razao

## lightning

operadores que possuem um canal lightning podem permitir que depositos enviem e recebam pela lightning network. quando um deposito solicita uma fatura lightning, o operador cria uma atraves de seu no lightning, pede aos membros do quorum que a co-assinem para provar que estao comprometidos em creditar o deposito apos o pagamento. a carteira deve reter esta fatura co-assinada como evidencia. quando um deposito solicita o pagamento de uma fatura lightning, o operador paga usando seu no lightning e debita o deposito apos obter o preimage

quando o pagador e o beneficiario sao depositos no mesmo operador, o operador pode liquidar internamente sem rotear pela lightning, creditando e debitando os respectivos depositos diretamente. isso evita taxas de roteamento e modos de falha, mantendo as mesmas garantias contabeis

## couriers

solicitacoes de transferencia movem fundos apenas entre depositos no mesmo livro-razao. para mover fundos entre livros-razao, carteiras usam couriers -- servicos que mantem depositos em multiplos livros-razao e transportam transferencias entre eles. um courier anuncia capacidade e taxas direcionais por livro-razao no relay. quando uma carteira quer enviar do livro-razao A para o livro-razao B, ela cria um bloqueio de transferencia para o deposito do courier e solicita que o courier crie um do seu deposito no livro-razao de destino para o beneficiario. uma vez que ambos os bloqueios estejam estabelecidos, a carteira revela o preimage ao beneficiario, que completa a transferencia do courier. uma vez revelado, o courier usa este mesmo preimage para completar a transferencia do remetente para o courier

este e um padrao de contrato hash time-locked padrao. esperamos que o tempo limite de saida do courier seja estritamente anterior ao de entrada, garantindo que se a carteira nunca revelar, ambos os bloqueios expirem e nenhuma das partes perca fundos. nenhuma confianca e necessaria alem da garantia de tempo limite aplicada pelos operadores

couriers devem definir taxas por livro-razao: fee_in e fee_out para cada livro-razao que atendem. a carteira estima o custo da rota como fee_out na origem mais fee_in no destino. couriers podem variar taxas por livro-razao com base na liquidez disponivel, reequilibrando naturalmente suas posicoes. carteiras descobrem couriers atraves de seus anuncios no relay e selecionam com base em taxa, capacidade ou cobertura

## comunicacao

toda comunicacao entre carteiras e operadores, e entre operadores, usa relays nostr. atualizacoes de livros-razao sao publicadas como eventos duraveis que os relays retem, criando um registro permanente auditavel. solicitacoes e respostas entre carteiras e operadores sao eventos efemeros com um TTL curto no relay. operadores anunciam seus termos como eventos substituiveis, permitindo que carteiras descubram e comparem operadores sem um diretorio centralizado

esta arquitetura significa que carteiras nao precisam de conexoes persistentes -- podem ficar offline indefinidamente e se atualizar reproduzindo eventos de qualquer relay que os tenha. operadores podem ser alcancados atraves de qualquer relay que monitorem, e a escolha do relay e uma decisao de implantacao, nao uma restricao do protocolo

## reservas e garantias

reservas sao mantidas em um utxo com um valor maior ou igual a soma das obrigacoes de um livro-razao, gastavel por uma maioria do quorum, com fallback para o operador apos um periodo significativo

garantia e o capital proprio do operador, depositado e bloqueado nos livros-razao dos membros do quorum. cada membro detem um deposito de garantia que o operador financia e bloqueia por uma duracao especificada. as obrigacoes totais de um livro-razao sao limitadas ao dobro do menor bloqueio de garantia detido por qualquer membro, e a duracao do quorum e limitada ao menor tempo de bloqueio. isso garante que a rede de garantias sempre tenha respaldo suficiente para cobrir uma transferencia de custodia. o mesmo deposito de garantia pode respaldar multiplos livros-razao para melhorar a eficiencia de capital, embora carteiras devam preferir operadores com fontes de garantia nao sobrepostas

obrigacoes sao aplicadas ao criar novas ofertas de financiamento ou faturas. o operador nao pode criar ofertas ou faturas que empurrem as obrigacoes totais do livro-razao acima das reservas ou acima do dobro do menor bloqueio de garantia, o que for menor

## quorum

operadores solicitam que outros operadores se juntem ao seu quorum depositando e bloqueando garantia no livro-razao do membro. a solicitacao inclui o compromisso de garantia (valor e duracao do bloqueio) e os termos do membro: tabelas minimas de taxas que os depositos no livro-razao devem atender. cada membro deve operar seu proprio livro-razao e pode confiscar a garantia do operador se o operador for comprovadamente nao conforme. membros especificam limites nas tabelas de taxas durante sua participacao no quorum -- o operador nao pode abrir depositos com taxas abaixo dos minimos do membro mais rigoroso, protegendo os membros de herdar obrigacoes nao lucrativas apos uma transferencia de custodia

uma vez que o quorum e estabelecido, as reservas sao rotacionadas para um novo utxo multisig. membros co-assinam atualizacoes validas e participam da recuperacao se o operador assinar atualizacoes nao conformes. quorums maiores aumentam a sobrecarga de comunicacao, mas reduzem o risco do operador, aumentam a disponibilidade e tornam a conluio mais dificil e cara. carteiras devem preferir quorums maiores

## dissuasao economica

o protocolo substitui a saida unilateral por dissuasao economica. membros do quorum sao diretamente incentivados a agir contra a desonestidade. durante operacoes normais, eles ganham taxas modestas sobre a garantia, mas no caso de comportamento comprovadamente nao conforme, podem confiscar o deposito de garantia completo do operador em seu livro-razao

quando uma carteira suspeita de censura, pode escalar a solicitacao para membros do quorum via entrega certificada. o membro incorpora o hash da solicitacao em seu proprio livro-razao por uma pequena taxa, criando evidencia causalmente ancorada. se o operador falhar em processar a solicitacao, o membro tem tanto a evidencia quanto o incentivo economico para iniciar uma disputa

fraude em faturas lightning segue o mesmo padrao de dissuasao. o operador sabe se um preimage foi recebido, mas a carteira nao. no entanto, qualquer pagador pode fornecer o preimage a carteira. um unico roubo confirmado desencadeia disputa, apreensao de reservas e confisco de garantia. a recompensa de roubar um unico pagamento e limitada, mas o risco e existencial, tornando o roubo via lightning economicamente irracional apesar de ser formalmente improvavel sem cooperacao de terceiros

o modo de falha tanto para censura quanto para dissuasao lightning e a conluio unanime do quorum. o protocolo nao pode proteger contra um quorum que coopera para roubar, mas a rede de garantias assegura que a conluio custa mais do que ganha. a transparencia da rede permite que carteiras e mercados de descoberta identifiquem estruturas de quorum suspeitas antes de depositar fundos

## tempo

o tempo absoluto e medido contra a camada base. tolerancias nao podem exceder um numero razoavel de confirmacoes para manter a estabilidade durante reorganizacoes da cadeia

onde tolerancias maiores sao necessarias, dependemos de ordenacao causal. um livro-razao criptografico e uma cadeia merkle. cada atualizacao prova que foi criada apos todas as atualizacoes anteriores, mas nao fornece garantias sobre informacoes fora da cadeia. para construir uma ordenacao distribuida, exigimos que co-assinaturas incluam o hash da atualizacao mais recente do livro-razao do co-assinante. esse hash e entao incorporado ao hash da atualizacao atual, tornando-se parte da cadeia, bem como parte de todas as outras cadeias para as quais o operador do livro-razao co-assina, criando uma rede de causalidade. isso nao e capaz de provar o tempo explicitamente, mas e capaz de provar que certas informacoes foram criadas em uma ordem especifica

## provas de fraude

podemos provar varios tipos de fraude expondo informacoes que foram criadas na ordem errada. onde informacoes nao sao incluidas por operacoes normais da rede, podem ser introduzidas criando atividade que inclua um hash da evidencia. uma vez incorporada em uma atualizacao assinada pelo operador, a evidencia e revelada como tendo sido criada em um lugar nao conforme na ordenacao:

- um operador, tendo oferecido creditar um deposito com fundos enviados on-chain para um endereco especifico, assina uma atualizacao do livro-razao que nao contem o credito apropriado, mas contem uma cadeia revelando algum hash de bloco que excede o numero de confirmacoes permitidas antes do credito

- um operador, tendo criado uma fatura lightning em nome de um deposito, assina uma atualizacao do livro-razao que nao creditou o deposito apesar do preimage ter sido revelado na cadeia

- uma co-assinatura que declara o hash atual do livro-razao como sendo um que precede seu proprio hash posterior na cadeia

- um membro do quorum de um livro-razao contestado que estava ativo mas nao agiu de acordo com a prova de fraude dentro de um numero de blocos

- assinar ou co-assinar atualizacoes de livro-razao nao conformes

uma prova de fraude consiste na evidencia e em uma cadeia causal conectando o hash incorporado ao livro-razao do operador acusado. a cadeia e uma sequencia de atualizacoes co-assinadas, cada uma incluindo um member_ledger_hash do livro-razao do elo anterior. verificadores percorrem a cadeia sem buscar, confirmando que cada elo e uma atualizacao assinada, e que o hash da prova corresponde aos dados incorporados

## recuperacao

uma vez que um livro-razao se tornou indisponivel ou nao conforme, membros do quorum podem criar sua propria continuacao do livro-razao a partir da ultima atualizacao conforme. eles devem estabelecer um novo quorum e fornecer atestacoes de garantia. os membros devem entao coordenar para gastar a saida de reservas anterior em uma loteria das possiveis proximas cadeias. o vencedor desta loteria adiciona uma atualizacao de aquisicao a sua cadeia, e os outros adicionam uma atualizacao de cessao. carteiras continuam a enderecarem o mesmo livro-razao, aceitando apenas respostas co-assinadas pelo quorum. periodicamente, e quando nenhuma resposta tem a co-assinatura esperada, a carteira deve consultar a rede e reproduzir atualizacoes do livro-razao para identificar mudancas na custodia

quando a nao conformidade parece acidental (ex., um livro-razao ficou indisponivel por um certo numero de blocos) a mudanca de custodia deve ser respeitosa: apenas o valor de reservas necessario para cobrir as obrigacoes do livro-razao e enviado para a loteria, e o troco e enviado de volta para a chave publica do operador. o controle da garantia nao e afetado

quando existe prova de nao conformidade, o valor em excesso das reservas necessarias e dividido igualmente entre os membros do quorum, e a garantia mantida nos livros-razao dos membros pode ser confiscada

## saude da rede

um ataque direto e formar ilhas de operadores em conluio. apos construir obrigacoes substanciais em seus livros-razao, eles coordenam a saida, roubando fundos que excedem a garantia perdida. a rede pode se defender contra isso, exceto em regioes onde o valor interno excede a garantia que a conecta a rede nao conluiada. maiores proporcoes de garantia e quorums maiores e mais diversos reduzem a probabilidade dessas bolsas se formarem, mas podem se formar propositalmente e nao podemos esperar que toda carteira avalie a rede inteira. em vez disso, mercados de descoberta devem publicar metricas de responsabilidade de operadores baseadas em analises de grafo, como algoritmos de coleta de premios

## conclusao

propomos uma rede de garantias que requer conluio para roubar, mas a conluio aumenta a garantia em risco mais rapido do que aumenta o valor a ser roubado. usamos esta rede para proteger livros-razao criptograficos respaldados por reservas integrais. estes livros-razao atendem contas em nome de carteiras offline em troca de taxas pre-negociadas. primitivas do livro-razao suportam condicoes de gasto miniscript suficientes para contratos inteligentes basicos. a rede escala de forma quase linear, permitindo que uma grande rede forneca bilhoes de carteiras e volume de transacoes superior ao das redes de pagamento tradicionais
