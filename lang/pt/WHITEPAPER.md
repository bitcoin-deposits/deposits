# bitcoin deposits
## resumo

uma versao ideal de dinheiro eletronico peer-to-peer permitiria que pagamentos online fossem enviados diretamente de uma parte para outra de forma rapida e com preparacao minima. a lightning network fornece parte da solucao, mas os beneficios essenciais perdem-se se for necessario um terceiro de confianca para gerir o estado em seu nome. propomos uma solucao para este problema utilizando livros-razao verificaveis e uma teia de colateral. os operadores transmitem atualizacoes do livro-razao aos seus pares, criando um registo auditavel de contas. as carteiras transmitem evidencias de desonestidade a esses pares, que garantem que o livro-razao mantem um operador honesto. a saida unilateral e substituida pela garantia de que os fundos permanecem disponiveis enquanto a rede existir. chegamos a uma rede que delega a manutencao de liquidez, evita taxas de configuracao, e capaz de receber pagamentos offline, e escala independentemente da camada base

## introducao

bitcoin deposits visa fornecer fundos rapidos e escalaveis controlados por chave, de forma trustless, off-chain. a atividade on-chain escala com o numero de livros-razao e a frequencia de rotacao de reservas. o throughput escala ligeiramente acima de linearmente com o numero de livros-razao na rede, tornando plausivel milhoes de transacoes por segundo atraves de trilioes de carteiras

existem compromissos explicitos:
- sem saida unilateral: quando os operadores falham, os fundos permanecem na rede
- sem privacidade: a verificacao requer transparencia
- disponibilidade intermitente: um deposito e tao disponivel quanto o operador. as carteiras devem distribuir os fundos para aumentar a disponibilidade

esperamos que a experiencia da carteira seja semelhante a uma camada base rapida, com economia de pagamentos semelhante a da lightning network

## livros-razao

um livro-razao e uma cadeia imutavel de atualizacoes, contendo o hash da atualizacao anterior e assinada pelo operador do livro-razao. diferentes tipos de atualizacao tem regras diferentes que governam quando e como podem ser utilizados. os livros-razao sao autodescritivos, as suas atualizacoes sao publicamente disponiveis e irrefutaveis, permitindo que qualquer pessoa avalie a conformidade

os livros-razao tem um unico operador ativo, mas sao mantidos cooperativamente pela malha. qualquer operador pode criar um, mas caso desapareca ou se torne desonesto, um operador diferente sera designado, juntamente com as reservas. o operador atualmente ativo e identificado pela chave publica que foi utilizada para assinar a atualizacao co-assinada mais recente

## depositos

um deposito e uma conta estavel que pode enviar e receber fundos, controlada por miniscript. na abertura, e estabelecido um plano de taxas, assim como se a rececao de fundos requer um pedido assinado pela carteira. um operador deve permitir transferencias entre depositos no mesmo livro-razao, bem como saidas on-chain. devem permitir que os depositos paguem faturas lightning

fica ao criterio do operador criar ofertas de financiamento on-chain ou faturas lightning em nome de um deposito. se o fizer, estas devem ser co-assinadas por um membro do quorum, e a carteira deve verificar esta assinatura. ofertas e faturas nao fazem parte do livro-razao, portanto e responsabilidade da carteira verificar as assinaturas e rete-las como evidencia

## taxas

transferencias entre depositos, on-chain e atraves de lightning tem taxas pagas ao operador do livro-razao. existem tambem taxas aplicadas periodicamente aos saldos com um periodo especificado. todas sao negociadas quando um novo deposito e aberto. as taxas podem ser alteradas apos um numero especificado de blocos, dado um aviso de um numero especificado de blocos e dentro de um limite percentual por ajuste negociado na abertura. o quorum pode recusar co-assinar atualizacoes que criem circunstancias nao lucrativas pelas quais poderiam ser responsabilizados

## transferencias

a forma basica de transferencia e uma operacao em duas fases entre dois depositos no mesmo livro-razao: um deposito emite um pedido para enviar fundos. se houver fundos suficientes disponiveis, um bloqueio sobre os fundos com uma condicao de gasto e adicionado ao livro-razao. se a condicao de gasto for cumprida antes de um timeout, os fundos movem-se do remetente para o destinatario menos a taxa do operador. se o timeout for atingido, o bloqueio e libertado, menos uma taxa de operador mais pequena. com condicoes de gasto miniscript, isto e suficiente para permitir que qualquer deposito forneca pontes e servicos de liquidez a outros depositos no mesmo livro-razao

## lightning

operadores que tenham um canal lightning podem permitir que os depositos enviem e recebam atraves da lightning network. quando um deposito solicita uma fatura lightning, o operador cria uma atraves do seu no lightning, pede aos membros do quorum que a co-assinem para provar que estao comprometidos em creditar o deposito apos o pagamento. a carteira deve reter esta fatura co-assinada como evidencia. quando um deposito solicita o pagamento de uma fatura lightning, o operador paga utilizando o seu no lightning e debita o deposito apos obter o preimage

quando o pagador e o beneficiario sao depositos no mesmo operador, o operador pode liquidar internamente sem encaminhar atraves de lightning, creditando e debitando os respetivos depositos diretamente. isto evita taxas de encaminhamento e modos de falha, mantendo as mesmas garantias contabilisticas

## correios

os pedidos de transferencia apenas movem fundos entre depositos no mesmo livro-razao. para mover fundos entre livros-razao, as carteiras utilizam correios — servicos que detem depositos em multiplos livros-razao e transportam transferencias entre eles. um correio anuncia capacidade e taxas direcionais por livro-razao no relay. quando uma carteira quer enviar do livro-razao A para o livro-razao B, cria um bloqueio de transferencia para o deposito do correio e solicita que o correio crie um do seu deposito no livro-razao de destino para o beneficiario. uma vez que ambos os bloqueios estejam estabelecidos, a carteira revela o preimage ao beneficiario, que completa a transferencia do correio. uma vez revelado, o correio utiliza este mesmo preimage para completar a transferencia do remetente para o correio

este e um padrao standard de contrato hash time-locked. esperamos que o timeout de saida do correio seja estritamente anterior ao de entrada, garantindo que se a carteira nunca revelar, ambos os bloqueios expiram e nenhuma das partes perde fundos. nao e necessaria confianca para alem da garantia de timeout aplicada pelos operadores

os correios devem definir taxas por livro-razao: fee_in e fee_out para cada livro-razao que servem. a carteira estima o custo da rota como fee_out na origem mais fee_in no destino. os correios podem variar as taxas por livro-razao com base na liquidez disponivel, reequilibrando naturalmente as suas posicoes. as carteiras descobrem correios atraves dos seus anuncios no relay e selecionam com base em taxa, capacidade ou cobertura

## comunicacao

toda a comunicacao entre carteiras e operadores, e entre operadores, utiliza relays nostr. as atualizacoes do livro-razao sao publicadas como eventos duraveis que os relays retem, criando um registo auditavel permanente. pedidos e respostas entre carteiras e operadores sao eventos efemeros com um TTL curto no relay. os operadores anunciam os seus termos como eventos substituiveis, permitindo que as carteiras descubram e comparem operadores sem um diretorio centralizado

esta arquitetura significa que as carteiras nao necessitam de ligacoes persistentes — podem ficar offline indefinidamente e recuperar reproduzindo eventos a partir de qualquer relay que os tenha. os operadores podem ser contactados atraves de qualquer relay que monitorizem, e a escolha do relay e uma decisao de implementacao, nao uma restricao do protocolo

## reservas e colateral

as reservas sao mantidas num utxo com um montante maior ou igual a soma das obrigacoes de um livro-razao, gastavel por uma maioria do quorum, com recurso ao operador apos um periodo significativo

o colateral e o capital proprio do operador, depositado e bloqueado em livros-razao de membros do quorum. cada membro detem um deposito de colateral que o operador financia e bloqueia por uma duracao especificada. as obrigacoes totais de um livro-razao sao limitadas ao dobro do menor bloqueio de colateral detido por qualquer membro, e a duracao do quorum e limitada ao menor tempo de bloqueio. isto garante que a teia de colateral tem sempre suporte suficiente para cobrir uma transferencia de custodia. o mesmo deposito de colateral pode suportar multiplos livros-razao para melhorar a eficiencia de capital, embora as carteiras devam preferir operadores com fontes de colateral nao sobrepostas

as obrigacoes sao aplicadas ao criar novas ofertas de financiamento ou faturas. o operador nao pode criar ofertas ou faturas que empurrem as obrigacoes totais do livro-razao acima das reservas ou acima do dobro do menor bloqueio de colateral, o que for menor

## quorum

os operadores solicitam a outros operadores que se juntem ao seu quorum depositando e bloqueando colateral no livro-razao do membro. o pedido inclui o compromisso de colateral (montante e duracao do bloqueio) e os termos do membro: planos de taxas minimas que os depositos no livro-razao devem cumprir. cada membro deve operar o seu proprio livro-razao e pode confiscar o colateral do operador se este for comprovadamente nao conforme. os membros especificam limites nos planos de taxas durante a sua participacao no quorum — o operador nao pode abrir depositos com taxas abaixo dos minimos do membro mais restritivo, protegendo os membros de herdar obrigacoes nao lucrativas apos uma transferencia de custodia

uma vez estabelecido o quorum, as reservas sao rotacionadas para um novo utxo multisig. os membros co-assinam atualizacoes validas e participam na recuperacao se o operador assinar atualizacoes nao conformes. quorums maiores aumentam a sobrecarga de comunicacao mas reduzem o risco do operador, aumentam a disponibilidade e tornam a conluio mais dificil e dispendiosa. as carteiras devem preferir quorums maiores

## dissuasao economica

o protocolo substitui a saida unilateral por dissuasao economica. os membros do quorum sao diretamente incentivados a agir contra a desonestidade. durante as operacoes normais, ganham taxas modestas sobre o colateral, mas em caso de comportamento comprovadamente nao conforme, podem confiscar o deposito de colateral completo do operador no seu livro-razao

quando uma carteira suspeita de censura, pode escalar o pedido aos membros do quorum atraves de entrega certificada. o membro incorpora o hash do pedido no seu proprio livro-razao por uma pequena taxa, criando evidencia causalmente ancorada. se o operador nao processar o pedido, o membro tem tanto a evidencia como o incentivo economico para iniciar uma disputa

a fraude em faturas lightning segue o mesmo padrao de dissuasao. o operador sabe se um preimage foi recebido, mas a carteira nao. no entanto, qualquer pagador pode fornecer o preimage a carteira. um unico roubo confirmado desencadeia disputa, apreensao de reservas e confisco de colateral. a recompensa de roubar um unico pagamento e limitada, mas o risco e existencial, tornando o roubo lightning economicamente irracional apesar de ser formalmente nao demonstravel sem cooperacao de terceiros

o modo de falha tanto para a censura como para a dissuasao lightning e a conluio unanime do quorum. o protocolo nao pode proteger contra um quorum que coopera para roubar, mas a teia de colateral garante que a conluio custa mais do que ganha. a transparencia da rede permite que carteiras e mercados de descoberta identifiquem estruturas de quorum suspeitas antes de depositar fundos

## tempo

o tempo absoluto e medido em relacao a camada base. as tolerancias nao podem exceder um numero razoavel de confirmacoes de modo a manter a estabilidade durante reorganizacoes da cadeia

onde sao necessarias tolerancias mais elevadas, recorremos a ordenacao causal. um livro-razao criptografico e uma cadeia merkle. cada atualizacao prova que foi criada apos todas as atualizacoes anteriores, mas nao fornece garantias sobre informacao fora da cadeia. para construir uma ordenacao distribuida, exigimos que as co-assinaturas incluam o hash da atualizacao mais recente do livro-razao do co-signatario. esse hash e entao incorporado no hash da atualizacao atual, tornando-se parte da cadeia assim como parte de todas as outras cadeias para as quais o operador do livro-razao co-assina, criando uma teia de causalidade. isto nao consegue provar o tempo explicitamente, mas consegue provar que certas informacoes foram criadas numa ordem especifica

## provas de fraude

podemos provar varios tipos de fraude expondo informacao que foi criada na ordem errada. onde a informacao nao e incluida pelas operacoes normais da rede, pode ser introduzida clandestinamente criando atividade que inclua um hash da evidencia. uma vez incorporada numa atualizacao assinada pelo operador, a evidencia e revelada como tendo sido criada num lugar nao conforme na ordenacao:

- um operador, tendo oferecido creditar um deposito com fundos enviados on-chain para um endereco especifico, assina uma atualizacao do livro-razao que nao contem o credito apropriado, mas contem uma cadeia que revela algum hash de bloco que excede o numero de confirmacoes permitidas antes do credito

- um operador, tendo criado uma fatura lightning em nome de um deposito, assina uma atualizacao do livro-razao que nao creditou o deposito apesar do preimage ter sido revelado na cadeia

- uma co-assinatura que declara que o hash atual do livro-razao e um que precede o seu proprio hash posterior na cadeia

- um membro do quorum de um livro-razao contestado que estava ativo mas nao agiu em conformidade com a prova de fraude dentro de um numero de blocos

- assinar ou co-assinar atualizacoes do livro-razao nao conformes

uma prova de fraude consiste na evidencia e numa cadeia causal que liga o hash incorporado ao livro-razao do operador acusado. a cadeia e uma sequencia de atualizacoes co-assinadas, cada uma incluindo um member_ledger_hash do livro-razao do elo anterior. os verificadores percorrem a cadeia sem pesquisar, confirmando que cada elo e uma atualizacao assinada e que o hash da prova corresponde aos dados incorporados

## recuperacao

uma vez que um livro-razao se tenha tornado indisponivel ou nao conforme, os membros do quorum podem criar a sua propria continuacao do livro-razao a partir da ultima atualizacao conforme. devem estabelecer um novo quorum e fornecer atestacoes de colateral. os membros devem entao coordenar-se para gastar a saida de reservas anterior numa lotaria das potenciais cadeias seguintes. o vencedor desta lotaria adiciona uma atualizacao de aquisicao a sua cadeia, e os outros adicionam uma cedencia. as carteiras continuam a enderegar o mesmo livro-razao, aceitando apenas respostas co-assinadas pelo quorum. periodicamente, e quando nenhuma resposta tem a co-assinatura esperada, a carteira deve consultar a rede e reproduzir as atualizacoes do livro-razao para identificar alteracoes na custodia

quando a nao conformidade parece acidental (por exemplo, um livro-razao ficou indisponivel durante um certo numero de blocos) a mudanca de custodia deve ser respeitosa: apenas o montante de reservas necessario para cobrir as obrigacoes do livro-razao e enviado para a lotaria, e o troco e devolvido a chave publica do operador. o controlo do colateral nao e afetado

quando existe prova de nao conformidade, o montante em excesso das reservas necessarias e dividido igualmente entre os membros do quorum, e o colateral mantido nos livros-razao dos membros pode ser confiscado

## saude da rede

um ataque direto e formar ilhas de operadores em conluio. apos acumular obrigacoes substanciais nos seus livros-razao, coordenam a saida, roubando fundos que excedem o colateral perdido. a rede pode defender-se contra isto, exceto em regioes onde o valor interno excede o colateral que a liga a rede nao conluiante. racios de colateral mais elevados e quorums maiores e mais diversificados reduzem a probabilidade de formacao destes bolsos, mas podem formar-se propositadamente e nao podemos esperar que cada carteira avalie toda a rede. em vez disso, os mercados de descoberta devem publicar metricas de responsabilizacao dos operadores baseadas em analises de grafos, tais como algoritmos prize-collecting

## conclusao

propomos uma rede de colateral que requer conluio para roubar, mas a conluio aumenta o colateral em risco mais rapidamente do que aumenta o valor a ser roubado. utilizamos esta rede para proteger livros-razao criptograficos suportados por reservas totais. estes livros-razao servem contas em nome de carteiras offline em troca de taxas pre-negociadas. as primitivas do livro-razao suportam condicoes de gasto miniscript suficientes para contratos inteligentes basicos. a rede escala de forma quase linear, permitindo que uma rede grande forneca milhares de milhoes de carteiras e volume de transacoes superior ao das redes de pagamento tradicionais
