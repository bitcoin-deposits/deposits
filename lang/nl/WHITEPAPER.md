# bitcoin deposits
## samenvatting

een ideale peer-to-peer versie van elektronisch geld zou het mogelijk maken om online betalingen snel en met minimale voorbereiding rechtstreeks van de ene partij naar de andere te sturen. het lightning netwerk biedt een deel van de oplossing, maar de essentiële voordelen gaan verloren als een vertrouwde derde partij nodig is om de toestand namens jou te beheren. wij stellen een oplossing voor dit probleem voor met behulp van verifieerbare grootboeken en een web van onderpand. operators zenden grootboekupdates uit naar hun peers, waardoor een controleerbaar overzicht van rekeningen ontstaat. wallets zenden bewijs van oneerlijkheid uit naar die peers, die ervoor zorgen dat het grootboek een eerlijke operator behoudt. eenzijdige uitstap wordt vervangen door de garantie dat fondsen beschikbaar blijven zolang het netwerk dat ook doet. we komen uit bij een netwerk dat liquiditeitsbeheer delegeert, installatiekosten vermijdt, in staat is betalingen offline te ontvangen en onafhankelijk van de basislaag schaalt

## introductie

bitcoin deposits heeft als doel snelle en schaalbare sleutel-gecontroleerde fondsen te bieden, zonder vertrouwen, off-chain. on-chain activiteit schaalt met het aantal grootboeken en de frequentie van reserverotatie. doorvoer schaalt iets meer dan lineair met het aantal grootboeken in het netwerk, waardoor miljoenen transacties per seconde over biljoenen wallets plausibel zijn

er zijn expliciete afwegingen:
- geen eenzijdige uitstap: wanneer operators falen blijven fondsen in het netwerk
- geen privacy: verificatie vereist transparantie
- periodieke beschikbaarheid: een deposit is slechts zo beschikbaar als de operator. wallets zouden fondsen moeten spreiden om de beschikbaarheid te vergroten

we verwachten dat de wallet-ervaring vergelijkbaar zal zijn met een snelle basislaag, met betalingseconomie vergelijkbaar met het lightning netwerk

## grootboeken

een grootboek is een onveranderlijke keten van updates, die de hash van de vorige update bevat en ondertekend is door de operator van het grootboek. verschillende soorten updates hebben verschillende regels die bepalen wanneer en hoe ze gebruikt mogen worden. grootboeken zijn zelfbeschrijvend, hun updates zijn openbaar beschikbaar en niet te weerleggen, waardoor iedereen de conformiteit kan beoordelen

grootboeken hebben één actieve operator, maar worden coöperatief onderhouden door het mesh. elke operator kan er een aanmaken, maar mocht deze verdwijnen of oneerlijk worden, dan wordt een andere operator aangewezen, samen met reserves. de momenteel actieve operator wordt geïdentificeerd door de pubkey die is gebruikt om de meest recente mede-ondertekende update te ondertekenen

## deposits

een deposit is een stabiele rekening die fondsen kan verzenden en ontvangen, bestuurd door miniscript. bij opening wordt een tariefschema vastgesteld, evenals of het ontvangen van fondsen een door de wallet ondertekend verzoek vereist. een operator moet overdrachten tussen deposits op hetzelfde grootboek toestaan, evenals on-chain uitstappen. zij zouden deposits moeten toestaan om lightning facturen te betalen

het is naar eigen inzicht van de operator om on-chain financieringsaanbiedingen of lightning facturen aan te maken namens een deposit. als zij dit doen, moeten deze mede-ondertekend worden door een quorumlid, en de wallet moet deze handtekening verifiëren. aanbiedingen en facturen maken geen deel uit van het grootboek, dus het is de verantwoordelijkheid van de wallet om handtekeningen te verifiëren en ze als bewijs te bewaren

## tarieven

overdrachten tussen deposits, on-chain en via lightning hebben tarieven die worden betaald aan de operator van het grootboek. er zijn ook tarieven die periodiek worden toegepast op saldi met een gespecificeerde periode. alle worden onderhandeld wanneer een nieuwe deposit wordt geopend. tarieven kunnen worden gewijzigd na een gespecificeerd aantal blokken, met een gespecificeerde blokopzegtermijn en binnen een per-aanpassing percentagelimiet die bij opening is onderhandeld. het quorum mag weigeren updates mede te ondertekenen die onrendabele omstandigheden creëren waarvoor zij uiteindelijk verantwoordelijk zouden kunnen worden

## overdrachten

de basisvorm van een overdracht is een tweefasige operatie tussen twee deposits op hetzelfde grootboek: een deposit geeft een verzoek uit om fondsen te verzenden. als er voldoende fondsen beschikbaar zijn, wordt een vergrendeling van de fondsen met een bestedingsvoorwaarde aan het grootboek toegevoegd. als aan de bestedingsvoorwaarde wordt voldaan vóór een timeout, worden fondsen verplaatst van de verzender naar de ontvanger minus de vergoeding van de operator. als de timeout wordt bereikt, wordt de vergrendeling opgeheven, minus een kleinere operatorvergoeding. met miniscript bestedingsvoorwaarden is dit voldoende om elke deposit in staat te stellen bruggen en liquiditeitsdiensten te bieden aan andere deposits op hetzelfde grootboek

## lightning

operators die een lightning kanaal hebben, kunnen deposits toestaan om te verzenden en ontvangen via het lightning netwerk. wanneer een deposit een lightning factuur aanvraagt, maakt de operator er een aan via hun lightning node, en vraagt quorumleden om deze mede te ondertekenen om te bewijzen dat zij zich ertoe verbinden de deposit te crediteren bij betaling. de wallet moet deze mede-ondertekende factuur als bewijs bewaren. wanneer een deposit betaling van een lightning factuur aanvraagt, betaalt de operator via hun lightning node en debiteert de deposit na het verkrijgen van de preimage

wanneer de betaler en de begunstigde deposits zijn bij dezelfde operator, kan de operator intern afrekenen zonder via lightning te routeren, en de betreffende deposits direct crediteren en debiteren. dit vermijdt routeringskosten en faalmodi terwijl dezelfde boekhoudkundige garanties behouden blijven

## koeriers

overdrachtverzoeken verplaatsen alleen fondsen tussen deposits op hetzelfde grootboek. om fondsen over grootboeken heen te verplaatsen, gebruiken wallets koeriers — diensten die deposits op meerdere grootboeken houden en overdrachten daartussen verzorgen. een koerier adverteert capaciteit en per-grootboek directionele tarieven op de relay. wanneer een wallet wil verzenden van grootboek A naar grootboek B, maakt het een overdrachtvergrendeling aan naar de deposit van de koerier en verzoekt dat de koerier er een aanmaakt van hun deposit op het bestemmingsgrootboek naar de begunstigde. zodra beide vergrendelingen zijn ingesteld, onthult de wallet de preimage aan de begunstigde, die de overdracht van de koerier voltooit. eenmaal onthuld, gebruikt de koerier dezelfde preimage om de overdracht van de verzender naar de koerier te voltooien

dit is een standaard hash time-locked contract patroon. we verwachten dat de uitgaande timeout van de koerier strikt eerder is dan de inkomende, zodat als de wallet nooit onthult, beide vergrendelingen verlopen en geen van beide partijen fondsen verliest. er is geen vertrouwen nodig buiten de timeoutgarantie die door operators wordt gehandhaafd

koeriers zouden per-grootboek tarieven moeten instellen: fee_in en fee_out voor elk grootboek dat zij bedienen. de wallet schat de routekosten als fee_out op de bron plus fee_in op de bestemming. koeriers kunnen tarieven per grootboek variëren op basis van beschikbare liquiditeit, waardoor hun posities op natuurlijke wijze worden herbalanceerd. wallets ontdekken koeriers via hun advertenties op de relay en selecteren op basis van tarief, capaciteit of dekking

## communicatie

alle communicatie tussen wallets en operators, en tussen operators onderling, gebruikt nostr relays. grootboekupdates worden gepubliceerd als duurzame events die relays bewaren, waardoor een permanent controleerbaar overzicht ontstaat. verzoeken en antwoorden tussen wallets en operators zijn vluchtige events met een korte relay TTL. operators adverteren hun voorwaarden als vervangbare events, waardoor wallets operators kunnen ontdekken en vergelijken zonder een gecentraliseerde directory

deze architectuur betekent dat wallets geen persistente verbindingen nodig hebben -- ze kunnen onbeperkt offline gaan en bijwerken door events opnieuw af te spelen vanaf elke relay die ze heeft. operators zijn bereikbaar via elke relay die zij monitoren, en de keuze van relay is een implementatiebeslissing, geen protocolbeperking

## reserves en onderpand

reserves worden gehouden in een utxo met een bedrag groter dan of gelijk aan de som van de verplichtingen van een grootboek, besteedbaar door een meerderheid van het quorum, met terugval naar de operator na een aanzienlijke periode

onderpand is het eigen kapitaal van de operator, gestort en vergrendeld op grootboeken van quorumleden. elk lid houdt een onderpanddeposit aan die de operator financiert en vergrendelt voor een gespecificeerde duur. de totale verplichtingen van een grootboek zijn beperkt tot tweemaal de kleinste onderpandvergrendeling die door een lid wordt gehouden, en de duur van het quorum is beperkt tot de kortste vergrendeltijd. dit zorgt ervoor dat het onderpandweb altijd voldoende dekking heeft om een bewaringsoverdracht te dekken. dezelfde onderpanddeposit kan meerdere grootboeken ondersteunen om de kapitaalefficiëntie te verbeteren, hoewel wallets de voorkeur zouden moeten geven aan operators met niet-overlappende onderpandbronnen

verplichtingen worden gehandhaafd bij het aanmaken van nieuwe financieringsaanbiedingen of facturen. de operator kan geen aanbiedingen of facturen aanmaken die de totale verplichtingen van het grootboek boven de reserves of boven tweemaal de kleinste onderpandvergrendeling zouden brengen, welke van de twee lager is

## quorum

operators verzoeken andere operators om tot hun quorum toe te treden door onderpand te storten en te vergrendelen op het grootboek van het lid. het verzoek bevat de onderpandverbintenis (bedrag en vergrendelduur) en de voorwaarden van het lid: minimumtariefschema's waaraan deposits op het grootboek moeten voldoen. elk lid moet zijn eigen grootboek beheren en mag het onderpand van de operator confisqueren als de operator bewezen niet-conform is. leden specificeren limieten op tariefschema's tijdens hun quorumlidmaatschap -- de operator kan geen deposits openen met tarieven onder de strengste minima van een lid, waardoor leden worden beschermd tegen het erven van onrendabele verplichtingen na een bewaringsoverdracht

zodra het quorum is ingesteld, worden reserves geroteerd naar een nieuwe multisig utxo. leden mede-ondertekenen geldige updates en nemen deel aan herstel als de operator niet-conforme updates ondertekent. grotere quorums verhogen de communicatie-overhead maar verminderen het operatorrisico, verhogen de beschikbaarheid en maken samenspanning moeilijker en duurder. wallets zouden de voorkeur moeten geven aan grotere quorums

## economische afschrikking

het protocol vervangt eenzijdige uitstap door economische afschrikking. quorumleden worden direct gestimuleerd om tegen oneerlijkheid op te treden. tijdens normale operaties verdienen zij bescheiden vergoedingen op onderpand, maar bij bewezen niet-conform gedrag kunnen zij het volledige onderpand van de operator op hun grootboek confisqueren

wanneer een wallet censuur vermoedt, kan het het verzoek escaleren naar quorumleden via gecertificeerde bezorging. het lid neemt de verzoek-hash op in hun eigen grootboek voor een klein tarief, waardoor causaal verankerd bewijs ontstaat. als de operator het verzoek niet verwerkt, heeft het lid zowel het bewijs als de economische prikkel om een geschil te starten

lightning factuurfraude volgt hetzelfde afschrikkingspatroon. de operator weet of een preimage is ontvangen, maar de wallet weet dat niet. echter, elke betaler kan de preimage aan de wallet verstrekken. een enkele bevestigde diefstal leidt tot een geschil, inbeslagname van reserves en confiscatie van onderpand. de beloning van het stelen van een enkele betaling is begrensd, maar het risico is existentieel, waardoor lightning-diefstal economisch irrationeel wordt ondanks dat het formeel niet te bewijzen is zonder medewerking van derden

de faalmodus voor zowel censuur- als lightning-afschrikking is unanieme quorumsamenspanning. het protocol kan niet beschermen tegen een quorum dat samenwerkt om te stelen, maar het web van onderpand zorgt ervoor dat samenspanning meer kost dan het oplevert. de transparantie van het netwerk stelt wallets en ontdekkingsmarkten in staat verdachte quorumstructuren te identificeren voordat fondsen worden gestort

## tijd

absolute tijd wordt gemeten aan de hand van de basislaag. toleranties mogen een redelijk aantal bevestigingen niet overschrijden om stabiliteit tijdens keten-reorganisaties te handhaven

waar hogere toleranties vereist zijn, vertrouwen we op causale ordening. een cryptografisch grootboek is een merkle keten. elke update bewijst dat deze is aangemaakt na alle updates ervoor, maar biedt geen garanties over informatie buiten de keten. om een gedistribueerde ordening te construeren, vereisen we dat mede-ondertekeningen de laatste update-hash van het grootboek van de mede-ondertekenaar bevatten. die hash wordt vervolgens opgenomen in de hash van de huidige update en wordt deel van de keten, evenals deel van alle andere ketens waarvoor de grootboekoperator mede-ondertekent, waardoor een web van causaliteit ontstaat. dit is niet in staat om tijd expliciet te bewijzen, maar is wel in staat om te bewijzen dat bepaalde stukken informatie in een specifieke volgorde zijn aangemaakt

## fraudebewijzen

we kunnen verschillende soorten fraude bewijzen door informatie bloot te leggen die in de verkeerde volgorde is aangemaakt. waar informatie niet wordt opgenomen door normale netwerkoperaties, kan deze worden binnengesmokkeld door activiteit te creëren die een hash van het bewijs bevat. eenmaal opgenomen in een update ondertekend door de operator, wordt het bewijs onthuld als zijnde aangemaakt op een niet-conforme plek in de volgorde:

- een operator, die heeft aangeboden een deposit te crediteren met fondsen die on-chain naar een specifiek adres zijn gestuurd, ondertekent een grootboekupdate die niet de juiste creditering bevat, maar wel een keten bevat die een blokhash onthult die het aantal toegestane bevestigingen vóór creditering overschrijdt

- een operator, die een lightning factuur heeft aangemaakt namens een deposit, ondertekent een grootboekupdate die de deposit niet heeft gecrediteerd ondanks dat de preimage in de keten is onthuld

- een mede-ondertekening die verklaart dat de huidige grootboek-hash er een is die voorafgaat aan hun eigen latere hash in de keten

- een lid van het quorum van een betwist grootboek dat actief was maar niet heeft gehandeld in overeenstemming met bewijs van fraude binnen een aantal blokken

- het ondertekenen of mede-ondertekenen van niet-conforme grootboekupdates

een fraudebewijs bestaat uit het bewijs en een causale keten die de ingebedde hash verbindt met het grootboek van de beschuldigde operator. de keten is een reeks mede-ondertekende updates, die elk een member_ledger_hash van het grootboek van de vorige schakel bevatten. verificateurs lopen de keten af zonder te zoeken, bevestigen dat elke schakel een ondertekende update is, en dat de bewijs-hash overeenkomt met de ingebedde gegevens

## herstel

zodra een grootboek onbeschikbaar of niet-conform is geworden, kunnen quorumleden hun eigen voortzetting van het grootboek aanmaken vanaf de laatste conforme update. zij moeten een nieuw quorum instellen en onderpandattestaties verstrekken. leden moeten vervolgens coördineren om de vorige reserves-output te besteden aan een loterij van de mogelijke volgende ketens. de winnaar van deze loterij voegt een acquisitie-update toe aan hun keten, en de anderen voegen een afstand-update toe. wallets blijven hetzelfde grootboek adresseren en accepteren alleen antwoorden die mede-ondertekend zijn door het quorum. periodiek, en wanneer geen antwoorden de verwachte mede-ondertekening hebben, moet de wallet het netwerk bevragen en grootboekupdates opnieuw afspelen om veranderingen in bewaring te identificeren

wanneer niet-conformiteit per ongeluk lijkt (bijv. een grootboek is voor een bepaald aantal blokken onbeschikbaar geworden) moet de verandering in bewaring respectvol zijn: alleen het bedrag aan reserves dat nodig is om de verplichtingen van het grootboek te dekken wordt naar de loterij gestuurd, en wisselgeld wordt teruggestuurd naar de pubkey van de operator. controle over onderpand wordt niet beïnvloed

wanneer bewijs van niet-conformiteit bestaat, wordt het bedrag boven de noodzakelijke reserves gelijk verdeeld onder leden van het quorum, en mag onderpand dat op grootboeken van leden wordt gehouden worden geconfisqueerd

## netwerkgezondheid

een eenvoudige aanval is het vormen van eilanden van samenwerkende operators. nadat zij aanzienlijke verplichtingen over hun grootboeken hebben opgebouwd, coördineren zij om te vertrekken en stelen fondsen die het verloren onderpand overschrijden. het netwerk kan zich hiertegen verdedigen, behalve in regio's waar de interne waarde het onderpand dat het verbindt met het niet-samenwerkende netwerk overschrijdt. hogere onderpandverhoudingen en grotere, meer diverse quorums verminderen de kans dat deze enclaves ontstaan, maar ze kunnen opzettelijk worden gevormd en we kunnen niet verwachten dat elke wallet het gehele netwerk evalueert. in plaats daarvan zouden ontdekkingsmarkten metrieken van operatorverantwoordelijkheid moeten publiceren op basis van grafanalyses zoals prize-collecting algoritmen

## conclusie

wij stellen een onderpandnetwerk voor dat samenspanning vereist om te stelen, maar samenspanning verhoogt het onderpand in gevaar sneller dan het de te stelen waarde verhoogt. wij gebruiken dit netwerk om cryptografische grootboeken te beveiligen die worden gedekt door volledige reserves. deze grootboeken bedienen rekeningen namens offline wallets in ruil voor vooraf onderhandelde tarieven. grootboekprimitieven ondersteunen miniscript bestedingsvoorwaarden die voldoende zijn voor eenvoudige slimme contracten. het netwerk schaalt bijna lineair, waardoor een groot netwerk miljarden wallets en transactievolumes kan bieden die die van traditionele betalingsnetwerken overtreffen
