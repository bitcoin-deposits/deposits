# bitcoin deposits
## sammanfattning

en ideal peer-to-peer-version av elektroniska kontanter skulle tillata betalningar online att skickas direkt fran en part till en annan snabbt och med minimal forberedelse. lightning-natverket ger en del av losningen, men de vasentliga fordelarna gar forlorade om en betrodd tredje part kravs for att hantera tillstand a dina vagnar. vi foreslar en losning pa detta problem med verifierbara liggare och ett nat av sakerhet. operatorer sandar liggaruppdateringar till sina motparter, vilket skapar ett granskningsbart register over konton. planbocker sandar bevis pa oarlighet till dessa motparter, som sakerstraller att liggaren uppratthaller en arlig operator. ensidig utgang ersatts av garantin att medel forblir tillgangliga sa lange natverket gor det. vi anlandar till ett natverk som delegerar likviditetsunderhall, undviker installationsavgifter, kan ta emot betalningar offline och skalar oberoende av baslagret

## introduktion

bitcoin deposits siktar pa att tillhandahalla snabba och skalbara nyckelkontrollerade medel, tillitslos, off-chain. on-chain-aktivitet skalar med antalet liggare och frekvensen av reservrotation. genomstromning skalar nagot over linjart med antalet liggare i natverket, vilket gor miljontals transaktioner per sekund over biljoner planbocker rimligt

det finns uttryckliga avvagningar:
- ingen ensidig utgang: nar operatorer misslyckas stannar medlen i natverket
- ingen integritet: verifiering kraver transparens
- intermittent tillganglighet: en insattning ar bara sa tillganglig som operatoren. planbocker bor sprida ut medel for att oka tillgangligheten

vi forvantar oss att planbokerupplevelsen ska likna ett snabbt baslager, med betalningsekonomi liknande lightning-natverket

## liggare

en liggare ar en oforanderlig kedja av uppdateringar, innehallande hashen av den foregaende uppdateringen och signerad av liggarens operator. olika typer av uppdateringar har olika regler som styr nar och hur de kan anvandas. liggare ar sjalvbeskrivande, deras uppdateringar ar offentligt tillgangliga och obestridliga, vilket tillater vem som helst att utvardera overensstammelse

liggare har en enda aktiv operator, men underhalls samarbetande av natverket. vilken operator som helst kan skapa en, men skulle de forsvinna eller bli oarliga tilldelas en annan operator, tillsammans med reserver. den for narvarande aktiva operatoren identifieras av den publika nyckel som anvandes for att signera den senaste samundertecknade uppdateringen

## insattningar

en insattning ar ett stabilt konto som kan skicka och ta emot medel, styrt av miniscript. vid oppning etableras ett avgiftsschema, samt huruvida mottagande av medel kraver en planbokssignerad begaran. en operator maste tillata overfuringar mellan insattningar pa samma liggare samt on-chain-uttag. de bor tillata insattningar att betala lightning-fakturor

det ar operatorens bedomning att skapa on-chain-finansieringserbjudanden eller lightning-fakturor pa en insattnings vagnar. om de gor det bor dessa samundertecknas av en kvorummedlem, och planbokan bor verifiera denna signatur. erbjudanden och fakturor ar inte del av liggaren, sa det ar planbokens ansvar att verifiera signaturer och behalla dem som bevis

## avgifter

overfuringar mellan insattningar, on-chain och genom lightning har avgifter som betalas till liggarens operator. det finns aven avgifter som periodiskt tillampas pa saldon med en specificerad period. alla forhandlas nar en ny insattning oppnas. avgifter kan andras efter ett specificerat antal block, givet ett specificerat blockvarsel och inom en procentuell grans per justering som forhandlats vid oppning. kvorumet kan vagra att samunderteckna uppdateringar som skapar olonsamma omstandigheter som de i slutandan kan bli ansvariga for

## overfuringar

den grundlaggande formen av overforing ar en tvafasig operation mellan tva insattningar pa samma liggare: en insattning utfardar en begaran om att skicka medel. om det finns tillrackliga medel tillgangliga laggs ett las pa medlen med ett villkor for anvandning till liggaren. om villkoret for anvandning uppfylls fore en tidsgrans flyttas medlen fran avsandaren till mottagaren minus operatorens avgift. om tidsgransen nas friges laset, minus en mindre operatorsavgift. med miniscript-villkor for anvandning ar detta tillrackligt for att tillata vilken insattning som helst att tillhandahalla brygg- och likviditetstjanster till andra insattningar pa samma liggare

## lightning

operatorer som har en lightning-kanal kan tillata insattningar att skicka och ta emot over lightning-natverket. nar en insattning begar en lightning-faktura skapar operatoren en genom sin lightning-nod, ber kvorummedlemmar att samunderteckna den for att bevisa att de ar engagerade i att kreditera insattningen vid betalning. planbokan bor behalla denna samundertecknade faktura som bevis. nar en insattning begar betalning av en lightning-faktura betalar operatoren med sin lightning-nod och debiterar insattningen efter att ha erhållit preimage

nar betalaren och betalningsmottagaren ar insattningar hos samma operator kan operatoren reglera internt utan att dirigera genom lightning, och kreditera och debitera respektive insattningar direkt. detta undviker dirigeringsavgifter och felscenarier samtidigt som samma redovisningsgarantier uppratthalls

## kurirer

overfuringsbegaran flyttar bara medel mellan insattningar pa samma liggare. for att flytta medel mellan liggare anvander planbocker kurirer -- tjanster som har insattningar pa flera liggare och transporterar overfuringar mellan dem. en kurir annonserar kapacitet och riktningsbestamda avgifter per liggare pa relat. nar en planboka vill skicka fran liggare A till liggare B skapar den ett overfuringslas till kurirens insattning och begar att kuriren skapar ett fran sin insattning pa destinationsliggaren till betalningsmottagaren. nar bada lasen ar etablerade avsllojar planbokan preimage till betalningsmottagaren, som fullfoljer overfuringen fran kuriren. nar den avslojats anvander kuriren samma preimage for att fullfolja overfuringen fran avsandaren till kuriren

detta ar ett standard hash-tidslast kontraktmonster. vi forvantar oss att kurirens utgaende tidsgrans ar strikt tidigare an den ingaende, vilket sakerstraller att om planbokan aldrig avslojar sa foraller bada lasen och ingen part forlorar medel. inget fortroende kravs utover tidsgransgarantin som uppratthalls av operatorer

kurirer bor satta avgifter per liggare: fee_in och fee_out for varje liggare de betjanar. planbokan uppskattar ruttkostnaden som fee_out pa kallan plus fee_in pa destinationen. kurirer kan variera avgifter per liggare baserat pa tillganglig likviditet, vilket naturligt ombalanserar deras positioner. planbocker upptacker kurirer genom deras annonser pa relat och valjer baserat pa avgift, kapacitet eller tackning

## kommunikation

all kommunikation mellan planbocker och operatorer, och mellan operatorer, anvander nostr-relan. liggaruppdateringar publiceras som varaktiga handelser som relan behaller, vilket skapar ett permanent granskningsbart register. begaran och svar mellan planbocker och operatorer ar flyktiga handelser med kort TTL pa relat. operatorer annonserar sina villkor som utbytbara handelser, vilket tillater planbocker att upptacka och jamfora operatorer utan en centraliserad katalog

denna arkitektur innebar att planbocker inte behover nagon persistent anslutning -- de kan ga offline pa obegransad tid och komma ikapp genom att spela upp handelser fran vilken rela som helst som har dem. operatorer kan nas genom vilken rela de overvakar, och valet av rela ar ett driftsbeslut, inte en protokollbegransning

## reserver och sakerhet

reserver halls i en utxo med ett belopp storre an eller lika med summan av en liggares forpliktelser, spendbart av en majoritet av kvorumet, med reservlosning till operatoren efter en betydande period

sakerhet ar operatorens eget kapital, insatt och last pa kvorummedlemmars liggare. varje medlem har en sakerhetsinsattning som operatoren finansierar och laser for en specificerad varaktighet. en liggares totala forpliktelser ar begransade till dubbla det minsta sakerhetslåset som nagon medlem innehar, och kvorumets varaktighet ar begransad till den kortaste lastiden. detta sakerstraller att sakerhetsnatverket alltid har tillracklig tackning for att hantera en vardnadsoverforing. samma sakerhetsinsattning kan backa flera liggare for att forbattra kapitaleffektiviteten, aven om planbocker bor foredra operatorer med icke-overlappande sakerhetskallor

forpliktelser uppratthalls nar nya finansieringserbjudanden eller fakturor skapas. operatoren kan inte skapa erbjudanden eller fakturor som skulle driva liggarens totala forpliktelser over reserverna eller over dubbla det minsta sakerhetslåset, beroende pa vilket som ar lagre

## kvorum

operatorer begar att andra operatorer gar med i deras kvorum genom att satta in och lasa sakerhet pa medlemmens liggare. begaran inkluderar sakerhetsataganandet (belopp och lasvaraktighet) och medlemmens villkor: minimiavgiftsscheman som insattningar pa liggaren maste uppfylla. varje medlem maste driva sin egen liggare och kan beslagta operatorens sakerhet om operatoren bevisas icke-overensstammande. medlemmar specificerar granser for avgiftsscheman under sitt kvorummedlemskap -- operatoren kan inte oppna insattningar med avgifter under den striktaste medlemmens minimum, vilket skyddar medlemmar fran att arva olonsamma forpliktelser efter en vardnadsoverforing

nar kvorumet ar etablerat roteras reserver till en ny multisig utxo. medlemmar samundertecknar giltiga uppdateringar och deltar i aterhemtning om operatoren signerar icke-overensstammande uppdateringar. storre kvorum okar kommunikationskostnaden men minskar operatorsrisk, okar tillganglighet och gor samverkan svarare och dyrare. planbocker bor foredra storre kvorum

## ekonomisk avskrackning

protokollet ersatter ensidig utgang med ekonomisk avskrackning. kvorummedlemmar ar direkt motiverade att agera mot oarlighet. under normal drift tjanar de blygsamma avgifter pa sakerhet, men vid bevisbart icke-overensstammande beteende kan de beslagta operatorens fulla sakerhetsinsattning pa sin liggare

nar en planboka misstenker censur kan den eskalera begaran till kvorummedlemmar via certifierad leverans. medlemmen baddar in begaran-hashen i sin egen liggare mot en liten avgift, vilket skapar kausalt forankrat bevis. om operatoren misslyckas med att behandla begaran har medlemmen bade beviset och det ekonomiska incitamentet att initiera en tvist

lightning-fakturabedragerier foljer samma avskrackningsmonster. operatoren vet om en preimage mottogs, men planbokan vet inte. dock kan vilken betalare som helst tillhandahalla preimage till planbokan. en enda bekraftad stold utloser tvist, beslag av reserver och beslagtagning av sakerhet. beloningen for att stjala en enda betalning ar begransad, men risken ar existentiell, vilket gor lightning-stold ekonomiskt irrationell trots att det formellt ar obevisbart utan tredje parts samarbete

felscenarierna for bade censur- och lightning-avskrackning ar enhallilg kvorumsamverkan. protokollet kan inte skydda mot ett kvorum som samarbetar for att stjala, men sakerhetsnatverket sakerstraller att samverkan kostar mer an det ger. natverkets transparens tillater planbocker och upptacktsmarknader att identifiera misstankta kvorumstrukturer innan medel satts in

## tid

absolut tid mats mot baslagret. toleranser kan inte overskrida ett rimligt antal bekraftelser for att uppratthalla stabilitet under kedjereorganisationer

dar hogre toleranser kravs forlitar vi oss pa kausal ordning. en kryptografisk liggare ar en merkle-kedja. varje uppdatering bevisar att den skapades efter alla uppdateringar fore den, men ger inga garantier om information utanfor kedjan. for att konstruera en distribuerad ordning kraver vi att samunderteckningar inkluderar den senaste uppdateringshashen fran samundertecknarens liggare. den hashen inkorporeras sedan i den aktuella uppdateringens hash, och blir en del av kedjan samt en del av alla andra kedjor som liggaroperatoren samundertecknar for, vilket skapar ett nat av kausalitet. detta kan inte bevisa tid explicit, men kan bevisa att vissa informationsbitar skapades i en specifik ordning

## bedrageribevis

vi kan bevisa olika typer av bedragerier genom att avsloja information som har skapats i fel ordning. dar information inte inkluderas av normala natverksoperationer kan den smugglas in genom att skapa aktivitet som inkluderar en hash av beviset. nar den vl inkorporerats i en uppdatering signerad av operatoren avslojas beviset som skapat pa en icke-overensstammande plats i ordningen:

- en operator, som har erbjudit att kreditera en insattning med medel skickade on-chain till en specifik adress, signerar en liggaruppdatering som inte innehaller den lampliga krediteringen, men innehaller en kedja som avslojar nagon block-hash som overskrider antalet bekraftelser som tillatits fore kreditering

- en operator, som har skapat en lightning-faktura pa en insattnings vagnar, signerar en liggaruppdatering som inte har krediterat insattningen trots att preimage har avslojats i kedjan

- en samunderteckning som deklarerar den aktuella liggare-hashen som en som foregår deras egen senare hash i kedjan

- en medlem av kvorumet for en omtvistad liggare som var aktiv men inte agerade i enlighet med bedrageribevis inom ett antal block

- signering eller samundertecknande av icke-overensstammande liggaruppdateringar

ett bedrageribevis bestar av beviset och en kausal kedja som forbinder den inbaddade hashen till den anklagade operatorens liggare. kedjan ar en sekvens av samundertecknade uppdateringar, var och en inkluderande en member_ledger_hash fran den foregaende lankens liggare. verifierare vandrar kedjan utan att soka, bekraftar att varje lank ar en signerad uppdatering, och att bevishashen matchar den inbaddade datan

## aterhemtning

nar en liggare har blivit otillganglig eller icke-overensstammande kan kvorummedlemmar skapa sin egen fortsattning av liggaren fran den senaste overensstammande uppdateringen. de maste etablera ett nytt kvorum och tillhandahalla sakerhetsintyg. medlemmar maste sedan koordinera for att spendera den foregaende reservutgangen till ett lotteri av de potentiella nasta kedjorna. vinnaren av detta lotteri lagger till en forvarvuppdatering till sin kedja, och de andra lagger till en avkastning. planbocker fortsatter att adressera samma liggare och accepterar bara svar samundertecknade av kvorumet. periodvis, och nar inga svar har den forvantade samunderteckningen, bor planbokan fraga natverket och spela upp liggaruppdateringar for att identifiera andringar i vardnad

nar icke-overensstammelse verkar oavsiktlig (t.ex. en liggare har blivit otillganglig under ett visst antal block) maste bytet av vardnad vara respektfullt: bara den mangd reserver som kravs for att tacka liggarens forpliktelser skickas till lotteriet, och vaxel skickas tillbaka till operatorens publika nyckel. kontroll over sakerhet paverkas inte

nar bevis pa icke-overensstammelse finns delas beloppet utover nodvandiga reserver lika mellan kvorumets medlemmar, och sakerhet pa medlemsliggare tillets att beslagtas

## natverkshalsa

en enkel attack ar att bilda oar av samverkande operatorer. efter att ha byggt betydande forpliktelser over sina liggare koordinerar de for att ga ut och stjala medel som overstiger den forlorade sakerheten. natverket kan forsvara sig mot detta, utom i regioner dar det interna vardet overstiger sakerheten som forbinder det till det icke-samverkande natverket. hogre sakerhetsforhallanden och storre, mer diversifierade kvorum minskar sannolikheten for att dessa fickor bildas, men de kan bildas avsiktligt och vi kan inte forvanta oss att varje planboka utvarderar hela natverket. istallet bor upptacktsmarknader publicera matt pa operatorsansvarighet baserat pa grafanalyser sasom prissamlingsalgoritmer

## slutsats

vi foreslar ett sakerhetsnatverk som kraver samverkan for att stjala, men samverkan okar sakerheten i riskzonen snabbare an det okar vardet som kan stjalas. vi anvander detta natverk for att sakra kryptografiska liggare backade av fulla reserver. dessa liggare betjanar konton pa uppdrag av offline-planbocker i utbyte mot forforhandlade avgifter. liggare-primitiver stoder miniscript-villkor for anvandning som ar tillrackliga for grundlaggande smarta kontrakt. natverket skalar nara linjart, vilket tillater ett stort natverk att tillhandahalla miljarder planbocker och transaktionsvolymer som overstiger traditionella betalningsnatverk
