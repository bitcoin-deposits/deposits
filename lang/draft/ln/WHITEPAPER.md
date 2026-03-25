# bitcoin deposits
## mokuse

mbongwana ya malamu mpenza ya mbongo ya elektroniki na kati ya bato mibale ekoki kopesa nzela ete mafuta ya internet etindama mbala moko uta na moto moko epai ya mosusu nokinoki mpe na bobongisami ya moke. lightning network epesi ndambo ya eyano, kasi litomba na yango ya ntina ebunga soki esengeli kozala na moto ya misato oyo baboti ye motema mpo na kobatela esika na nkombo na yo. topesi eyano na likambo oyo na nzela ya ledger oyo ekoki kotalama mpe réseau ya collateral. operator bapalanganisaka ba mise à jour ya ledger epai ya baninga na bango, basalaka lisolo oyo ekoki kotalama ya ba compte. wallet epalanganisaka bilembeteli ya bokosi epai ya baninga yango, oyo bandimisaka ete ledger ebateli operator ya sembo. kobima na ngambo moko ebongwanami na ndanga ete mbongo ezali disponible ntango nyonso oyo réseau ezali. tokomi na réseau oyo epesi mosala ya kobatela liquidité na moto mosusu, eboyaka ba frais ya kobanda, ekoki kozwa mafuta ntango ozali hors ligne, mpe ekoki kokola na ndenge oyo ekeseni na couche ya moboko

## ebandeli

bitcoin deposits elingi kopesa mbongo oyo ekontrolami na fungola nokinoki mpe oyo ekoki kokola, na ndenge ya kotia motema te, libanda ya chaîne. mosala ya chaîne ekoli elongo na motango ya ledger mpe mbala boni reserves ebongwanaka. débit ekoli mwa moke na likoló ya ligne droite elongo na motango ya ledger na réseau, kosala ete bamilio ya transactions na segonde na kati ya trilio ya wallet ekoka

ezali na ba compromis oyo emonisami polele:
- kobima na ngambo moko te: ntango operator bakweyi mbongo etikalaka na réseau
- sekele te: vérification esengeli bosembo
- disponibilité oyo ekatanaka: deposit ezali kaka disponible ndenge operator azali. wallet esengeli kopalanganisa mbongo mpo na kobakisa disponibilité

tozali kokanisa ete expérience ya wallet ekokesana te na couche ya moboko ya nokinoki, na économie ya mafuta oyo ekokani na lightning network

## ledger

ledger ezali chaîne ya mise à jour oyo ekoki kobongwana te, ezali na hash ya mise à jour ya liboso mpe esignée na operator ya ledger. ndenge ekeseni ya mise à jour ezali na mibeko ekeseni oyo etambolisaka ntango nini mpe ndenge nini ekoki kosalelama. ledger emimonisaka yango moko, mise à jour na yango ezali ya bato nyonso mpe ekoki koboyama te, kopesa nzela na moto nyonso mpo na kotala soki elandaka mibeko

ledger ezali na operator moko oyo azali kosala, kasi ebatelama na lisanga ya réseau. operator nyonso akoki kosala moko, kasi soki alimwi to akomi mokosi operator mosusu akopesama, elongo na reserves. operator oyo azali kosala sikoyo ayebani na pubkey oyo esalelamaki mpo na kosigner mise à jour ya suka oyo esignée na bato mibale

## deposit

deposit ezali compte ya kobongwana te oyo ekoki kotinda mpe kozwa mbongo, ekontrolami na miniscript. na ntango ya kofungola, programme ya frais etiamaka, mpe soki kozwa mbongo esengeli requête oyo esignée na wallet. operator asengeli kopesa nzela na transfert entre deposit na ledger moko mpe kobima na chaîne. basengeli kopesa nzela na deposit mpo na kofuta facture ya lightning

ezali na bokateli ya operator mpo na kosala offre ya financement na chaîne to facture ya lightning na nkombo ya deposit. soki asali yango, esengeli kosignama na membre ya quorum, mpe wallet esengeli kovérifier signature oyo. offre mpe facture ezali te ndambo ya ledger, yango wana ezali mokumba ya wallet mpo na kovérifier signature mpe kobomba yango lokola bilembeteli

## frais

transfert entre deposit, na chaîne, mpe na nzela ya lightning ezali na frais oyo efutami na operator ya ledger. ezali mpe na frais oyo etiamaka mbala na mbala na solde na eleko oyo ekatami. nyonso enegociami ntango deposit ya sika efungwami. frais ekoki kobongwana nsima ya motango ya blocs oyo ekatami, na avertissement ya blocs oyo ekatami mpe na ndelo ya pourcentage ya kobongola oyo enegociami na ntango ya kofungola. quorum ekoki koboya kosigner mise à jour oyo esalaka makambo oyo ezangi bénéfice oyo bakoki kozwa mokumba na nsuka

## transfert

ndenge ya moboko ya transfert ezali mosala ya étapes mibale entre deposit mibale na ledger moko: deposit etindaka requête ya kotinda mbongo. soki mbongo ekoki, verrou na mbongo na condition ya kolekisa ebakisami na ledger. soki condition ya kolekisa ekokisami liboso ya ntango ya koleka, mbongo elongwaka na motindi epai ya mozwi minus frais ya operator. soki ntango ya koleka ekoki, verrou efungwami, minus frais ya moke ya operator. na condition ya kolekisa ya miniscript, yango ekoki mpo na kopesa nzela na deposit nyonso mpo na kopesa pont mpe service ya liquidité na deposit mosusu na ledger moko

## lightning

operator oyo bazali na canal ya lightning bakoki kopesa nzela na deposit mpo na kotinda mpe kozwa na lightning network. ntango deposit esengaka facture ya lightning, operator asalaka yango na nzela ya lightning node na ye, asengaka membre ya quorum mpo na cosigner yango mpo na kolakisa ete batiami na mokano ya kocréditer deposit ntango efutami. wallet esengeli kobatela facture oyo cosignée lokola bilembeteli. ntango deposit esengaka kofuta facture ya lightning, operator afutaka na nzela ya lightning node na ye mpe alongolaka na deposit nsima ya kozwa preimage

ntango mofuti mpe mozwi bazali deposit na operator moko, operator akoki koregler na kati kozanga koleka na lightning, kocréditer mpe kolongola na deposit oyo etali yango mbala moko. yango eboyaka frais ya routage mpe ba likambo ya kolonga te ntango ebatelaka ndanga ya comptabilité

## courier

requête ya transfert elongolaka kaka mbongo entre deposit na ledger moko. mpo na kolongola mbongo na ledger ekeseni, wallet esalelaka courier — service oyo ebatelaka deposit na ledger mingi mpe ememaka transfert entre yango. courier epalanganisaka capacité mpe frais ya direction na ledger na relay. ntango wallet elingi kotinda uta na ledger A epai ya ledger B, esalaka verrou ya transfert na deposit ya courier mpe esengaka ete courier esala moko uta na deposit na ye na ledger ya destination epai ya mozwi. ntango verrou mibale etiami, wallet emonisaka preimage na mozwi, oyo akokisaka transfert uta na courier. nsima ya komonisama, courier asalelaka preimage yango moko mpo na kokokisa transfert uta na motindi epai ya courier

oyo ezali modèle standard ya hash time-locked contract. tozali kokanisa ete ntango ya koleka ya kobima ya courier ekozala liboso mpenza na oyo ya kokota, kondimisaka ete soki wallet emonisi ata moke te, verrou mibale esilaka mpe moto moko te abungisaka mbongo. motema esengeli te libanda ya ndanga ya ntango oyo operator akokisaka

courier basengeli kotia frais na ledger: fee_in mpe fee_out mpo na ledger mokomoko oyo basalelaka. wallet etali motuya ya nzela lokola fee_out na source plus fee_in na destination. courier bakoki kobongola frais na ndenge ya ledger na kotalela liquidité oyo ezali, na ndenge ya korebalancer positions na bango na ndenge ya naturel. wallet bakuti courier na nzela ya annonce na bango na relay mpe baponaka na kotalela frais, capacité, to couverture

## communication

communication nyonso entre wallet mpe operator, mpe entre operator, esalelaka nostr relay. mise à jour ya ledger ebimisami lokola événement ya libela oyo relay ebatelaka, kosala lisolo ya libela oyo ekoki kotalama. requête mpe réponse entre wallet mpe operator ezali événement ya ntango mokuse na TTL ya mokuse na relay. operator epalanganisaka condition na bango lokola événement oyo ekoki kozongisama, kopesa nzela na wallet mpo na kokuta mpe kokokanisa operator kozanga répertoire ya kati

architecture oyo elakisi ete wallet esengeli te connexion ya libela -- bakoki kokende hors ligne mpo na ntango molai mpe kozonga na kotambwisa événement uta na relay nyonso oyo ezali na yango. operator bakoki kokomama na nzela ya relay nyonso oyo batalaka, mpe boponi ya relay ezali ekateli ya déploiement, te contrainte ya protocole

## reserves mpe collateral

reserves ebombami na UTXO na montant oyo eleki to ekokani na somme ya obligation ya ledger, oyo ekoki kolekisama na majorité ya quorum, na recours na operator nsima ya ntango molai

collateral ezali capital ya operator ye moko, oyo atiami mpe everrouillée na ledger ya membre ya quorum. membre mokomoko abatelaka deposit ya collateral oyo operator afinancaka mpe averrouillaka mpo na ntango oyo ekatami. obligation ya mobimba ya ledger ekoki koleka te mbala mibale ya verrou ya moke mpenza ya collateral oyo ebombami na membre nyonso, mpe ntango ya quorum ekoki koleka te ntango ya moke mpenza ya verrou. yango endimisaka ete réseau ya collateral ezali ntango nyonso na soutien ekoki mpo na kozipa transfert ya garde. deposit moko ya collateral ekoki kosalela mpo na ledger mingi mpo na kobongisa efficacité ya capital, atako wallet basengeli kolinga operator na source ya collateral oyo ekokangani te

obligation ekokisami ntango basalaka offre ya financement to facture ya sika. operator akoki te kosala offre to facture oyo ekotindika obligation ya mobimba ya ledger na likoló ya reserves to na likoló ya mbala mibale ya verrou ya moke mpenza ya collateral, oyo nyonso ezali na nse

## quorum

operator basengaka operator mosusu mpo na kokota na quorum na bango na kotia mpe koverrouiller collateral na ledger ya membre. requête esangisaka engagement ya collateral (montant mpe ntango ya verrou) mpe condition ya membre: programme ya frais ya minimum oyo deposit na ledger esengeli kokokisa. membre mokomoko asengeli kotambwisa ledger na ye mpe akoki kobotola collateral ya operator soki operator amonisami ete alandaka mibeko te. membre batiaka ndelo na programme ya frais na ntango ya bozwi na bango ya quorum -- operator akoki te kofungola deposit na frais na nse ya minimum ya membre ya makasi mpenza, kobatela membre uta na kozwa obligation oyo ezangi bénéfice nsima ya transfert ya garde

ntango quorum etiami, reserves ebongwanaka na UTXO ya sika ya multisig. membre basignaka mise à jour ya malamu mpe basanganaka na kozongisa soki operator asigni oyo elandaka mibeko te. quorum ya monene ebakisaka mosala ya communication kasi ekitisaka risque ya operator, ebakisaka disponibilité, mpe esalaka ete collusion ekoma makasi mpe ntalo. wallet basengeli kolinga quorum ya monene

## koboya ya ekonomiki

protocole ebongolaka kobima na ngambo moko na koboya ya ekonomiki. membre ya quorum batindami mbala moko mpo na kosala likambo na bokosi. na ntango ya mosala ya seko bazwaka frais ya moke na collateral, kasi soki ezali na comportement oyo emonisami ete elandaka mibeko te bakoki kobotola deposit mobimba ya collateral ya operator na ledger na bango

ntango wallet ekanisaka censure, ekoki komata na requête epai ya membre ya quorum na nzela ya livraison certifiée. membre atiaka hash ya requête na ledger na ye mpo na frais ya moke, kosala bilembeteli oyo ezali na lien ya cause. soki operator asali te requête, membre azali na bilembeteli mpe na litomba ya ekonomiki mpo na kobanda likambo

bokosi ya facture ya lightning elandaka modèle moko ya koboya. operator ayebi soki preimage ekomaki, kasi wallet eyebi te. nzokande mofuti nyonso akoki kopesa preimage na wallet. boyibi moko oyo endimisami ebandisaka likambo, kobotola reserves, mpe kobotola collateral. litomba ya koyiba mafuta moko ekangami, kasi risque ezali ya liwa, kosala ete boyibi ya lightning ezanga makanisi ya ekonomiki atako ekoki komonisama te na ndenge ya formel kozanga lisalisi ya moto ya misato

ndenge ya kolonga te mpo na censure mpe koboya ya lightning ezali collusion ya quorum mobimba. protocole ekoki te kobatela likambo na quorum oyo esangani mpo na koyiba, kasi réseau ya collateral endimisaka ete collusion ezali na ntalo mingi koleka oyo ekoki kozwama. bosembo ya réseau epesaka nzela na wallet mpe marché ya kokuta mpo na koyeba structure ya quorum oyo ezali na ntembe liboso ya kotia mbongo

## ntango

ntango ya solo emesamaka na couche ya moboko. tolérance ekoki koleka te motango ya confirmation oyo ekoki mpo na kobatela stabilité na ntango ya réorganisation ya chaîne

esika tolérance ya likolo esengelaka, totielaka na ordre ya cause. ledger ya cryptographie ezali chaîne ya merkle. mise à jour mokomoko emonisaka ete esalemaki nsima ya mise à jour nyonso liboso na yango, kasi epesaka ndanga te mpo na information libanda ya chaîne. mpo na kosala ordre oyo epalanganisami, tosengaka ete co-signature esangisa hash ya mise à jour ya suka uta na ledger ya co-signeur. hash yango ekotisami na hash ya mise à jour ya sikoyo, ekomi ndambo ya chaîne mpe ndambo ya chaîne nyonso mosusu oyo operator ya ledger a-co-signe, kosala réseau ya cause. yango ekoki te komonisa ntango na ndenge ya polele, kasi ekoki komonisa ete information mosusu esalemaki na ordre moko boye

## bilembeteli ya bokosi

tokoki komonisa ndenge ekeseni ya bokosi na komonisa information oyo esalemaki na ordre ya mabe. esika information ezali te na mosala ya seko ya réseau, ekoki kokotisama na nse na kosala mosala oyo esangisaka hash ya bilembeteli. ntango ekotisami na mise à jour oyo esignée na operator, bilembeteli emonisami ete esalemaki na esika oyo elandaka mibeko te na ordre:

- operator, oyo apesaki mpo na kocréditer deposit na mbongo oyo etindami na chaîne na adresse moko, asigni mise à jour ya ledger oyo ezangi crédit oyo ebongi, kasi ezali na chaîne oyo emonisaka hash ya bloki oyo eleki motango ya confirmation oyo epesami liboso ya crédit

- operator, oyo asalaki facture ya lightning na nkombo ya deposit, asigni mise à jour ya ledger oyo ecrédité te deposit atako preimage emonisami na chaîne

- co-signature oyo elobaka ete hash ya ledger ya sikoyo ezali moko oyo eyaka liboso ya hash na bango ya nsima na chaîne

- membre ya quorum ya ledger oyo ezali na likambo oyo azalaki actif kasi asalaki te na kotalela bilembeteli ya bokosi na kati ya motango ya blocs

- kosigner to co-signer mise à jour ya ledger oyo elandaka mibeko te

bilembeteli ya bokosi esangisaka bilembeteli mpe chaîne ya cause oyo ekangaka hash oyo ekotisami na ledger ya operator oyo afundami. chaîne ezali molongo ya mise à jour oyo co-signée, mokomoko esangisaka member_ledger_hash uta na ledger ya lien ya liboso. vérificateur batambolaka na chaîne kozanga koluka, kondimisaka ete lien mokomoko ezali mise à jour oyo esignée, mpe ete hash ya bilembeteli ekokani na donnée oyo ekotisami

## kozongisa

ntango ledger ekomi disponible te to elandaka mibeko te, membre ya quorum bakoki kosala kokoba na bango moko ya ledger uta na mise à jour ya suka oyo elandaka mibeko. basengeli kotia quorum ya sika mpe kopesa attestation ya collateral. membre basengeli koordoner mpo na kolekisa sortie ya reserves ya liboso na loterie ya chaîne oyo ekoki kolanda. molongi ya loterie oyo abakisaka mise à jour ya kozwa na chaîne na ye, mpe basusu babakisaka mise à jour ya kopesa. wallet ekobaka kolobela ledger yango moko, kondimaka kaka réponse oyo co-signée na quorum. mbala na mbala, mpe ntango réponse ezali na co-signature te oyo esengelaki, wallet esengeli kotuna réseau mpe kotambwisa mise à jour ya ledger mpo na koyeba changement ya garde

ntango kozanga kolanda mibeko emonani lokola accident (ndakisa, ledger ekomi disponible te mpo na motango ya blocs) changement ya garde esengeli kozala na limemya: kaka montant ya reserves oyo esengeli mpo na kozipa obligation ya ledger etindami na loterie, mpe mbongwana ezongisami na pubkey ya operator. kontrol ya collateral ebongwani te

ntango bilembeteli ya kozanga kolanda mibeko ezali, montant oyo eleki reserves oyo esengeli ekabolami na ndenge ya kokesana na membre ya quorum, mpe collateral oyo ebombami na ledger ya membre ekoki kobotolama

## santé ya réseau

lifulú moko ya polele ezali kosala esanga ya operator oyo basangani. nsima ya kotonga obligation ya monene na ledger na bango, baordoner mpo na kobima, koyiba mbongo oyo eleki collateral oyo ebungisami. réseau ekoki komibatela na likambo oyo, longola na région esika motuya ya kati eleki collateral oyo ekangaka yango na réseau oyo esangani te. ratio ya collateral ya likolo mpe quorum ya monene mpe ya ndenge mingi ekitisaka likoki ya poche oyo kosalama, kasi ekoki kosalama na mokano mpe tokoki te kozela ete wallet nyonso etala réseau mobimba. na esika na yango marché ya kokuta basengeli kobimisa métrique ya responsabilité ya operator na base ya analyse ya graphe lokola algorithme ya kozwa prix

## bosukisi

topesi réseau ya collateral oyo esengeli collusion mpo na koyiba, kasi collusion ebakisaka collateral oyo ezali na risque nokinoki koleka oyo ebakisaka motuya oyo ekoki koyibama. tosalelaka réseau oyo mpo na kobatela ledger ya cryptographie oyo esungamaka na reserves ya mobimba. ledger oyo esalaka compte na nkombo ya wallet hors ligne na échange ya frais oyo enegociami liboso. primitive ya ledger esungaka condition ya kolekisa ya miniscript oyo ekoki mpo na contrat ya makanisi ya moboko. réseau ekoli penepene na ligne droite, kopesa nzela na réseau ya monene mpo na kopesa bamiliare ya wallet mpe volume ya transaction oyo eleki réseau ya mafuta ya bonkoko
