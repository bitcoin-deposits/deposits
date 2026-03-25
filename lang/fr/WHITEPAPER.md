# bitcoin deposits
## resume

une version ideale de pair-a-pair de monnaie electronique permettrait d'envoyer des paiements en ligne directement d'une partie a une autre, rapidement et avec une preparation minimale. le lightning network fournit une partie de la solution, mais les avantages essentiels sont perdus si un tiers de confiance est necessaire pour gerer l'etat en votre nom. nous proposons une solution a ce probleme en utilisant des registres verifiables et un reseau de garanties. les operateurs diffusent les mises a jour des registres a leurs pairs, creant un historique verifiable des comptes. les portefeuilles diffusent les preuves de malhonnetete a ces pairs, qui s'assurent que le registre maintient un operateur honnete. la sortie unilaterale est remplacee par la garantie que les fonds restent disponibles tant que le reseau l'est. nous aboutissons a un reseau qui delegue la maintenance de la liquidite, evite les frais d'installation, est capable de recevoir des paiements hors ligne, et evolue independamment de la couche de base

## introduction

bitcoin deposits vise a fournir des fonds rapides et evolutifs controles par cle, sans tiers de confiance, hors chaine. l'activite sur la chaine evolue avec le nombre de registres et la frequence de rotation des reserves. le debit evolue legerement au-dessus de lineairement avec le nombre de registres dans le reseau, rendant plausibles des millions de transactions par seconde a travers des milliers de milliards de portefeuilles

il y a des compromis explicites :
- pas de sortie unilaterale : quand les operateurs echouent, les fonds restent dans le reseau
- pas de confidentialite : la verification exige la transparence
- disponibilite intermittente : un depot n'est disponible qu'autant que l'operateur l'est. les portefeuilles devraient repartir les fonds pour augmenter la disponibilite

nous nous attendons a ce que l'experience du portefeuille soit similaire a une couche de base rapide, avec une economie de paiement similaire au lightning network

## registres

un registre est une chaine immuable de mises a jour, contenant le hash de la mise a jour precedente et signee par l'operateur du registre. differents types de mises a jour ont des regles differentes regissant quand et comment ils peuvent etre utilises. les registres sont auto-descriptifs, leurs mises a jour sont publiquement disponibles et non repudiables, permettant a quiconque d'evaluer la conformite

les registres ont un seul operateur actif, mais sont maintenus cooperativement par le maillage. tout operateur peut en creer un, mais s'il disparait ou devient malhonnete, un operateur different sera assigne, avec les reserves. l'operateur actuellement actif est identifie par la cle publique qui a ete utilisee pour signer la mise a jour co-signee la plus recente

## depots

un depot est un compte stable qui peut envoyer et recevoir des fonds, controle par miniscript. a l'ouverture, un bareme de frais est etabli, ainsi que la question de savoir si la reception de fonds necessite une requete signee par le portefeuille. un operateur doit permettre les transferts entre depots sur le meme registre ainsi que les sorties sur la chaine. il devrait permettre aux depots de payer des factures lightning

il est a la discretion de l'operateur de creer des offres de financement sur la chaine ou des factures lightning au nom d'un depot. s'il le fait, celles-ci devraient etre co-signees par un membre du quorum, et le portefeuille devrait verifier cette signature. les offres et factures ne font pas partie du registre, il est donc de la responsabilite du portefeuille de verifier les signatures et de les conserver comme preuves

## frais

les transferts entre depots, sur la chaine et via lightning ont des frais payes a l'operateur du registre. il y a aussi des frais periodiquement appliques aux soldes avec une periode specifiee. tous sont negocies lors de l'ouverture d'un nouveau depot. les frais peuvent etre modifies apres un nombre specifie de blocs, moyennant un preavis d'un nombre specifie de blocs et dans une limite de pourcentage par ajustement negociee a l'ouverture. le quorum peut refuser de co-signer des mises a jour qui creent des circonstances non rentables dont il pourrait en fin de compte etre responsable

## transferts

la forme de base d'un transfert est une operation en deux phases entre deux depots sur le meme registre : un depot emet une requete d'envoi de fonds. s'il y a suffisamment de fonds disponibles, un verrou sur les fonds avec une condition de depense est ajoute au registre. si la condition de depense est remplie avant l'expiration du delai, les fonds passent de l'expediteur au destinataire moins les frais de l'operateur. si le delai est atteint, le verrou est libere, moins des frais d'operateur plus faibles. avec les conditions de depense miniscript, cela est suffisant pour permettre a tout depot de fournir des ponts et des services de liquidite a d'autres depots sur le meme registre

## lightning

les operateurs ayant un canal lightning peuvent permettre aux depots d'envoyer et de recevoir via le lightning network. quand un depot demande une facture lightning, l'operateur en cree une via son noeud lightning, demande aux membres du quorum de la co-signer pour prouver qu'ils s'engagent a crediter le depot lors du paiement. le portefeuille devrait conserver cette facture co-signee comme preuve. quand un depot demande le paiement d'une facture lightning, l'operateur paie via son noeud lightning et debite le depot apres avoir obtenu le preimage

quand le payeur et le beneficiaire sont des depots chez le meme operateur, l'operateur peut regler en interne sans passer par lightning, creditant et debitant les depots respectifs directement. cela evite les frais de routage et les modes de defaillance tout en maintenant les memes garanties comptables

## coursiers

les requetes de transfert ne deplacent des fonds qu'entre depots sur le meme registre. pour deplacer des fonds entre registres, les portefeuilles utilisent des coursiers — des services qui detiennent des depots sur plusieurs registres et transportent les transferts entre eux. un coursier annonce sa capacite et ses frais directionnels par registre sur le relais. quand un portefeuille veut envoyer du registre A au registre B, il cree un verrou de transfert vers le depot du coursier et demande que le coursier en cree un depuis son depot sur le registre de destination vers le beneficiaire. une fois les deux verrous etablis, le portefeuille revele le preimage au beneficiaire, qui complete le transfert depuis le coursier. une fois revele, le coursier utilise ce meme preimage pour completer le transfert de l'expediteur vers le coursier

il s'agit d'un schema standard de contrat a verrou temporel par hash. nous nous attendons a ce que le delai d'expiration sortant du coursier soit strictement anterieur a l'entrant, garantissant que si le portefeuille ne revele jamais, les deux verrous expirent et aucune partie ne perd de fonds. aucune confiance n'est requise au-dela de la garantie de delai appliquee par les operateurs

les coursiers devraient fixer des frais par registre : fee_in et fee_out pour chaque registre qu'ils desservent. le portefeuille estime le cout de la route comme fee_out sur la source plus fee_in sur la destination. les coursiers peuvent varier les frais par registre en fonction de la liquidite disponible, reequilibrant naturellement leurs positions. les portefeuilles decouvrent les coursiers via leurs annonces sur le relais et selectionnent en fonction des frais, de la capacite ou de la couverture

## communication

toute communication entre portefeuilles et operateurs, et entre operateurs, utilise des relais nostr. les mises a jour de registres sont publiees comme des evenements durables que les relais conservent, creant un historique permanent et verifiable. les requetes et reponses entre portefeuilles et operateurs sont des evenements ephemeres avec un TTL de relais court. les operateurs annoncent leurs conditions comme des evenements remplacables, permettant aux portefeuilles de decouvrir et comparer les operateurs sans repertoire centralise

cette architecture signifie que les portefeuilles n'ont pas besoin de connexions persistantes -- ils peuvent se deconnecter indefiniment et se rattraper en rejouant les evenements depuis n'importe quel relais qui les possede. les operateurs peuvent etre contactes via n'importe quel relais qu'ils surveillent, et le choix du relais est une decision de deploiement, pas une contrainte du protocole

## reserves et garanties

les reserves sont detenues dans un utxo avec un montant superieur ou egal a la somme des obligations d'un registre, depensable par une majorite du quorum, avec un repli vers l'operateur apres une periode significative

la garantie est le propre capital de l'operateur, depose et verrouille sur les registres des membres du quorum. chaque membre detient un depot de garantie que l'operateur finance et verrouille pour une duree specifiee. les obligations totales d'un registre sont limitees au double du plus petit verrou de garantie detenu par tout membre, et la duree du quorum est limitee au temps de verrouillage le plus court. cela garantit que le reseau de garanties dispose toujours d'un soutien suffisant pour couvrir un transfert de garde. le meme depot de garantie peut soutenir plusieurs registres pour ameliorer l'efficacite du capital, bien que les portefeuilles devraient preferer les operateurs avec des sources de garantie non chevauchantes

les obligations sont appliquees lors de la creation de nouvelles offres de financement ou factures. l'operateur ne peut pas creer d'offres ou de factures qui pousseraient les obligations totales du registre au-dessus des reserves ou au-dessus du double du plus petit verrou de garantie, selon le montant le plus bas

## quorum

les operateurs demandent a d'autres operateurs de rejoindre leur quorum en deposant et verrouillant des garanties sur le registre du membre. la demande inclut l'engagement de garantie (montant et duree de verrouillage) et les conditions du membre : baremes de frais minimaux que les depots sur le registre doivent respecter. chaque membre doit operer son propre registre et peut confisquer la garantie de l'operateur si celui-ci est prouve non conforme. les membres specifient des limites sur les baremes de frais pendant leur participation au quorum -- l'operateur ne peut pas ouvrir de depots avec des frais inferieurs aux minimums du membre le plus strict, protegeant les membres contre l'heritage d'obligations non rentables apres un transfert de garde

une fois le quorum etabli, les reserves sont transferees dans un nouveau utxo multisig. les membres co-signent les mises a jour valides et participent a la recuperation si l'operateur signe des mises a jour non conformes. des quorums plus grands augmentent la charge de communication mais reduisent le risque de l'operateur, augmentent la disponibilite et rendent la collusion plus difficile et couteuse. les portefeuilles devraient preferer des quorums plus grands

## dissuasion economique

le protocole remplace la sortie unilaterale par la dissuasion economique. les membres du quorum sont directement incites a agir contre la malhonnetete. pendant les operations normales, ils gagnent des frais modestes sur les garanties, mais en cas de comportement prouvablement non conforme, ils peuvent confisquer la totalite du depot de garantie de l'operateur sur leur registre

quand un portefeuille suspecte une censure, il peut escalader la requete aux membres du quorum via une livraison certifiee. le membre integre le hash de la requete dans son propre registre moyennant des frais modiques, creant une preuve causalement ancree. si l'operateur ne traite pas la requete, le membre dispose a la fois de la preuve et de l'incitation economique pour initier un litige

la fraude aux factures lightning suit le meme schema de dissuasion. l'operateur sait si un preimage a ete recu, mais le portefeuille ne le sait pas. cependant, tout payeur pourrait fournir le preimage au portefeuille. un seul vol confirme declenche un litige, la saisie des reserves et la confiscation des garanties. la recompense du vol d'un seul paiement est bornee, mais le risque est existentiel, rendant le vol via lightning economiquement irrationnel bien que formellement impouvable sans cooperation d'un tiers

le mode de defaillance pour la censure et la dissuasion lightning est la collusion unanime du quorum. le protocole ne peut pas proteger contre un quorum qui coopere pour voler, mais le reseau de garanties assure que la collusion coute plus qu'elle ne rapporte. la transparence du reseau permet aux portefeuilles et aux marches de decouverte d'identifier les structures de quorum suspectes avant de deposer des fonds

## temps

le temps absolu est mesure par rapport a la couche de base. les tolerances ne peuvent pas depasser un nombre raisonnable de confirmations afin de maintenir la stabilite lors des reorganisations de chaine

lorsque des tolerances plus elevees sont requises, nous nous appuyons sur l'ordonnancement causal. un registre cryptographique est une chaine de merkle. chaque mise a jour prouve qu'elle a ete creee apres toutes les mises a jour precedentes, mais ne fournit aucune garantie sur les informations en dehors de la chaine. afin de construire un ordonnancement distribue, nous exigeons que les co-signatures incluent le hash de la derniere mise a jour du registre du co-signataire. ce hash est ensuite incorpore dans le hash de la mise a jour courante, devenant partie de la chaine ainsi que de toutes les autres chaines pour lesquelles l'operateur du registre co-signe, creant un reseau de causalite. cela ne peut pas prouver le temps explicitement, mais peut prouver que certaines informations ont ete creees dans un ordre specifique

## preuves de fraude

nous pouvons prouver divers types de fraude en exposant des informations qui ont ete creees dans le mauvais ordre. lorsque l'information n'est pas incluse par les operations normales du reseau, elle peut etre introduite clandestinement en creant une activite qui inclut un hash de la preuve. une fois incorporee dans une mise a jour signee par l'operateur, la preuve est revelee comme ayant ete creee a un endroit non conforme dans l'ordonnancement :

- un operateur, ayant offert de crediter un depot avec des fonds envoyes sur la chaine a une adresse specifique, signe une mise a jour du registre qui ne contient pas le credit approprie, mais contient une chaine revelant un hash de bloc depassant le nombre de confirmations autorisees avant le credit

- un operateur, ayant cree une facture lightning au nom d'un depot, signe une mise a jour du registre qui n'a pas credite le depot malgre le preimage revele dans la chaine

- une co-signature qui declare que le hash du registre actuel est un hash qui precede leur propre hash ulterieur dans la chaine

- un membre du quorum d'un registre conteste qui etait actif mais n'a pas agi conformement a la preuve de fraude dans un certain nombre de blocs

- signer ou co-signer des mises a jour de registre non conformes

une preuve de fraude consiste en la preuve et une chaine causale reliant le hash integre au registre de l'operateur accuse. la chaine est une sequence de mises a jour co-signees, chacune incluant un member_ledger_hash du registre du maillon precedent. les verificateurs parcourent la chaine sans recherche, confirmant que chaque maillon est une mise a jour signee et que le hash de la preuve correspond aux donnees integrees

## recuperation

une fois qu'un registre est devenu indisponible ou non conforme, les membres du quorum peuvent creer leur propre continuation du registre a partir de la derniere mise a jour conforme. ils doivent etablir un nouveau quorum et fournir des attestations de garantie. les membres doivent ensuite se coordonner pour depenser la sortie de reserves precedente vers une loterie des chaines potentielles suivantes. le gagnant de cette loterie ajoute une mise a jour d'acquisition a sa chaine, et les autres ajoutent un abandon. les portefeuilles continuent de s'adresser au meme registre, n'acceptant que les reponses co-signees par le quorum. periodiquement, et lorsqu'aucune reponse n'a la co-signature attendue, le portefeuille devrait interroger le reseau et rejouer les mises a jour du registre pour identifier les changements de garde

lorsque la non-conformite semble accidentelle (par exemple, un registre est devenu indisponible pendant un certain nombre de blocs), le changement de garde doit etre respectueux : seul le montant de reserves necessaire pour couvrir les obligations du registre est envoye a la loterie, et le change est renvoye a la cle publique de l'operateur. le controle des garanties n'est pas affecte

lorsqu'une preuve de non-conformite existe, le montant excedant les reserves necessaires est reparti egalement entre les membres du quorum, et les garanties detenues sur les registres des membres peuvent etre confisquees

## sante du reseau

une attaque directe consiste a former des ilots d'operateurs complices. apres avoir accumule des obligations substantielles a travers leurs registres, ils se coordonnent pour sortir, volant des fonds qui depassent les garanties perdues. le reseau peut se defendre contre cela, sauf dans les regions ou la valeur interne depasse la garantie les reliant au reseau non complice. des ratios de garantie plus eleves et des quorums plus grands et plus diversifies reduisent la probabilite de formation de ces poches, mais elles peuvent se former intentionnellement et nous ne pouvons pas attendre de chaque portefeuille qu'il evalue l'ensemble du reseau. les marches de decouverte devraient plutot publier des metriques de responsabilite des operateurs basees sur des analyses de graphe telles que des algorithmes de collecte de prix

## conclusion

nous proposons un reseau de garanties qui necessite la collusion pour voler, mais la collusion augmente les garanties a risque plus vite qu'elle n'augmente la valeur a voler. nous utilisons ce reseau pour securiser des registres cryptographiques soutenus par des reserves completes. ces registres gerent des comptes au nom de portefeuilles hors ligne en echange de frais pre-negocies. les primitives du registre supportent des conditions de depense miniscript suffisantes pour des contrats intelligents de base. le reseau evolue de maniere quasi lineaire, permettant a un grand reseau de fournir des milliards de portefeuilles et un volume de transactions superieur a celui des reseaux de paiement traditionnels
