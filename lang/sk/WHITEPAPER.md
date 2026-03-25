# bitcoin deposits
## abstrakt

ideálna peer-to-peer verzia elektronickej hotovosti by umožňovala odosielanie online platieb priamo od jednej strany k druhej rýchlo a s minimálnou prípravou. lightning network poskytuje čiastočné riešenie, no podstatné výhody sa strácajú, ak je na správu stavu vo vašom mene potrebná dôveryhodná tretia strana. navrhujeme riešenie tohto problému pomocou overiteľných účtovných kníh a siete kolaterálov. operátori vysielajú aktualizácie účtovných kníh svojim peerom, čím vytvárajú auditovateľný záznam účtov. peňaženky vysielajú dôkazy o nečestnosti týmto peerom, ktorí zabezpečujú, aby účtovná kniha udržiavala čestného operátora. jednostranný odchod je nahradený zárukou, že prostriedky zostávajú dostupné tak dlho, ako je dostupná sieť. výsledkom je sieť, ktorá deleguje údržbu likvidity, vyhýba sa poplatkom za nastavenie, je schopná prijímať platby offline a škáluje sa nezávisle od základnej vrstvy

## úvod

bitcoin deposits si kladie za cieľ poskytovať rýchle a škálovateľné prostriedky kontrolované kľúčmi, bez potreby dôvery, mimo reťazec. aktivita na reťazci sa škáluje s počtom účtovných kníh a frekvenciou rotácie rezerv. priepustnosť sa škáluje mierne nadlineárne s počtom účtovných kníh v sieti, čo robí milióny transakcií za sekundu naprieč biliónmi peňaženiek uskutočniteľnými

existujú explicitné kompromisy:
- žiadny jednostranný odchod: keď operátori zlyhajú, prostriedky zostávajú v sieti
- žiadne súkromie: overovanie vyžaduje transparentnosť
- občasná dostupnosť: vklad je dostupný len natoľko, nakoľko je dostupný operátor. peňaženky by mali rozložiť prostriedky na zvýšenie dostupnosti

očakávame, že používateľský zážitok z peňaženky bude podobný rýchlej základnej vrstve s ekonomikou platieb podobnou lightning network

## účtovné knihy

účtovná kniha je nemenný reťazec aktualizácií, obsahujúci hash predchádzajúcej aktualizácie a podpísaný operátorom účtovnej knihy. rôzne typy aktualizácií majú rôzne pravidlá upravujúce kedy a ako môžu byť použité. účtovné knihy sú sebaopisné, ich aktualizácie sú verejne dostupné a nepopierateľné, čo umožňuje komukoľvek vyhodnotiť súlad

účtovné knihy majú jedného aktívneho operátora, ale sú kooperatívne udržiavané sieťou. akýkoľvek operátor môže vytvoriť účtovnú knihu, no ak by zmizol alebo sa stal nečestným, bude priradený iný operátor spolu s rezervami. aktuálne aktívny operátor je identifikovaný verejným kľúčom, ktorý bol použitý na podpísanie najnovšej spoločne podpísanej aktualizácie

## vklady

vklad je stabilný účet, ktorý môže odosielať a prijímať prostriedky, kontrolovaný pomocou miniscript. pri otvorení sa stanoví poplatkový plán, ako aj to, či prijatie prostriedkov vyžaduje požiadavku podpísanú peňaženkou. operátor musí umožniť prevody medzi vkladmi na tej istej účtovnej knihe, ako aj odchody na reťazci. mal by umožniť vkladom platiť lightning faktúry

je na uvážení operátora vytvoriť ponuky financovania na reťazci alebo lightning faktúry v mene vkladu. ak tak urobí, tieto by mali byť spoločne podpísané členom kvóra a peňaženka by mala overiť tento podpis. ponuky a faktúry nie sú súčasťou účtovnej knihy, takže je zodpovednosťou peňaženky overiť podpisy a uchovať ich ako dôkaz

## poplatky

prevody medzi vkladmi, na reťazci a cez lightning majú poplatky platené operátorovi účtovnej knihy. existujú aj poplatky periodicky uplatňované na zostatky so stanoveným obdobím. všetky sú dohodnuté pri otvorení nového vkladu. poplatky môžu byť zmenené po stanovenom počte blokov, s daným blokovým upozornením a v rámci percentuálneho limitu na úpravu dohodnutého pri otvorení. kvórum môže odmietnuť spoločne podpísať aktualizácie, ktoré vytvárajú neziskové okolnosti, za ktoré by v konečnom dôsledku mohli niesť zodpovednosť

## prevody

základná forma prevodu je dvojfázová operácia medzi dvoma vkladmi na tej istej účtovnej knihe: vklad vystaví požiadavku na odoslanie prostriedkov. ak sú k dispozícii dostatočné prostriedky, k účtovnej knihe sa pripojí zámok na prostriedky s podmienkou minutia. ak je podmienka minutia splnená pred vypršaním časového limitu, prostriedky sa presunú od odosielateľa k príjemcovi mínus poplatok operátora. ak je dosiahnutý časový limit, zámok sa uvoľní mínus menší poplatok operátora. s podmienkami minutia v miniscript je to dostatočné na to, aby akýkoľvek vklad mohol poskytovať mosty a služby likvidity iným vkladom na tej istej účtovnej knihe

## lightning

operátori s lightning kanálom môžu umožniť vkladom odosielať a prijímať cez lightning network. keď vklad požiada o lightning faktúru, operátor ju vytvorí prostredníctvom svojho lightning uzla a požiada členov kvóra o spoločný podpis, čím preukáže, že sú odhodlaní pripísať vkladu prostriedky po zaplatení. peňaženka by si mala uchovať túto spoločne podpísanú faktúru ako dôkaz. keď vklad požiada o zaplatenie lightning faktúry, operátor zaplatí pomocou svojho lightning uzla a odpíše z vkladu po získaní preimage

keď sú platiteľ aj príjemca vkladmi u toho istého operátora, operátor môže vyrovnať interne bez smerovania cez lightning, priamo pripísaním a odpísaním príslušných vkladov. tým sa vyhnú poplatkom za smerovanie a režimom zlyhania pri zachovaní rovnakých účtovných záruk

## kuriéri

požiadavky na prevod presúvajú prostriedky iba medzi vkladmi na tej istej účtovnej knihe. na presun prostriedkov medzi účtovnými knihami peňaženky používajú kuriérov — služby, ktoré majú vklady na viacerých účtovných knihách a prenášajú prevody medzi nimi. kuriér inzeruje kapacitu a smerové poplatky pre jednotlivé účtovné knihy na relé. keď chce peňaženka poslať z účtovnej knihy A na účtovnú knihu B, vytvorí zámok prevodu na vklad kuriéra a požiada kuriéra, aby vytvoril zámok zo svojho vkladu na cieľovej účtovnej knihe pre príjemcu. akonáhle sú oba zámky vytvorené, peňaženka odhalí preimage príjemcovi, ktorý dokončí prevod od kuriéra. po odhalení kuriér použije ten istý preimage na dokončenie prevodu od odosielateľa ku kuriérovi

toto je štandardný vzor hash time-locked kontraktu. očakávame, že časový limit odchádzajúceho prevodu kuriéra bude striktne skorší ako prichádzajúci, čím sa zabezpečí, že ak peňaženka nikdy neodhalí preimage, oba zámky vypršia a žiadna strana nestratí prostriedky. nie je potrebná žiadna dôvera nad rámec záruky časového limitu vynucovanej operátormi

kuriéri by mali nastaviť poplatky pre jednotlivé účtovné knihy: fee_in a fee_out pre každú účtovnú knihu, ktorú obsluhujú. peňaženka odhaduje náklady na trasu ako fee_out na zdrojovej plus fee_in na cieľovej účtovnej knihe. kuriéri môžu meniť poplatky podľa účtovnej knihy na základe dostupnej likvidity, čím prirodzene vyvažujú svoje pozície. peňaženky objavujú kuriérov prostredníctvom ich inzerátov na relé a vyberajú na základe poplatku, kapacity alebo pokrytia

## komunikácia

všetka komunikácia medzi peňaženkami a operátormi a medzi operátormi navzájom používa nostr relé. aktualizácie účtovných kníh sú publikované ako trvalé udalosti, ktoré relé uchovávajú, čím vytvárajú permanentný auditovateľný záznam. požiadavky a odpovede medzi peňaženkami a operátormi sú efemérne udalosti s krátkym relé TTL. operátori inzerujú svoje podmienky ako nahraditeľné udalosti, čo umožňuje peňaženkám objavovať a porovnávať operátorov bez centralizovaného adresára

táto architektúra znamená, že peňaženky nepotrebujú trvalé pripojenia — môžu ísť offline na neurčito a dobehnúť prehrátím udalostí z akéhokoľvek relé, ktoré ich má. operátorov možno zastihnúť cez akékoľvek relé, ktoré monitorujú, a výber relé je rozhodnutím nasadenia, nie obmedzením protokolu

## rezervy a kolaterál

rezervy sú držané v utxo s čiastkou väčšou alebo rovnou súčtu záväzkov účtovnej knihy, míňateľné väčšinou kvóra, s návratom k operátorovi po významnom období

kolaterál je vlastný kapitál operátora, uložený a uzamknutý na účtovných knihách členov kvóra. každý člen drží kolaterálny vklad, ktorý operátor financuje a uzamkne na stanovenú dobu. celkové záväzky účtovnej knihy sú obmedzené na dvojnásobok najmenšieho kolaterálneho zámku drženého akýmkoľvek členom a trvanie kvóra je obmedzené najkratším časom zámku. tým sa zabezpečí, že sieť kolaterálov má vždy dostatočné krytie na pokrytie prevodu správy. ten istý kolaterálny vklad môže kryť viacero účtovných kníh na zlepšenie kapitálovej efektívnosti, hoci peňaženky by mali uprednostňovať operátorov s neprekrývajúcimi sa zdrojmi kolaterálu

záväzky sú vynucované pri vytváraní nových ponúk financovania alebo faktúr. operátor nemôže vytvárať ponuky alebo faktúry, ktoré by posunuli celkové záväzky účtovnej knihy nad rezervy alebo nad dvojnásobok najmenšieho kolaterálneho zámku, podľa toho, čo je nižšie

## kvórum

operátori žiadajú iných operátorov o vstup do ich kvóra uložením a uzamknutím kolaterálu na účtovnej knihe člena. požiadavka obsahuje kolaterálny záväzok (čiastku a dobu uzamknutia) a podmienky člena: minimálne poplatkové plány, ktoré musia vklady na účtovnej knihe spĺňať. každý člen musí prevádzkovať vlastnú účtovnú knihu a môže skonfiškovanť kolaterál operátora, ak sa preukáže, že operátor nekoná v súlade. členovia stanovujú limity na poplatkové plány počas svojho členstva v kvóre — operátor nemôže otvárať vklady s poplatkami pod minimami najprísnejšieho člena, čím chráni členov pred zdedením neziskových záväzkov po prevode správy

po vytvorení kvóra sa rezervy rotujú do nového multisig utxo. členovia spoločne podpisujú platné aktualizácie a zúčastňujú sa obnovy, ak operátor podpíše nekonformné. väčšie kvóra zvyšujú komunikačnú réžiu, ale znižujú riziko operátora, zvyšujú dostupnosť a robia tajnú dohodu ťažšou a nákladnejšou. peňaženky by mali uprednostňovať väčšie kvóra

## ekonomické odstrašenie

protokol nahrádza jednostranný odchod ekonomickým odstrašením. členovia kvóra sú priamo motivovaní konať proti nečestnosti. počas bežných operácií zarábajú skromné poplatky z kolaterálu, ale v prípade preukázateľne nekonformného správania môžu skonfiškovanť celý kolaterálny vklad operátora na svojej účtovnej knihe

keď peňaženka má podozrenie na cenzúru, môže eskalovať požiadavku na členov kvóra prostredníctvom certifikovaného doručenia. člen vloží hash požiadavky do svojej vlastnej účtovnej knihy za malý poplatok, čím vytvorí kauzálne ukotvený dôkaz. ak operátor požiadavku nespracuje, člen má dôkaz aj ekonomickú motiváciu na začatie sporu

podvod s lightning faktúrami sleduje rovnaký vzor odstrašenia. operátor vie, či bol preimage prijatý, ale peňaženka nie. avšak akýkoľvek platiteľ môže poskytnúť preimage peňaženke. jediná potvrdená krádež spustí spor, zaistenie rezerv a konfišku kolaterálu. odmena za ukradnutie jednej platby je ohraničená, ale riziko je existenčné, čo robí krádež cez lightning ekonomicky iracionálnou napriek tomu, že je formálne nedokázateľná bez spolupráce tretej strany

režim zlyhania pre cenzúru aj odstrašenie cez lightning je jednomyseľná tajná dohoda kvóra. protokol nemôže chrániť pred kvórom, ktoré spolupracuje na krádeži, ale sieť kolaterálov zabezpečuje, že tajná dohoda stojí viac, než koľko prinesie. transparentnosť siete umožňuje peňaženkám a trhom objavovania identifikovať podozrivé štruktúry kvóra pred uložením prostriedkov

## čas

absolútny čas sa meria voči základnej vrstve. tolerancie nesmú prekročiť rozumný počet potvrdení, aby sa zachovala stabilita počas reorganizácií reťazca

kde sú potrebné vyššie tolerancie, spoliehame sa na kauzálne usporiadanie. kryptografická účtovná kniha je merkle reťazec. každá aktualizácia dokazuje, že bola vytvorená po všetkých aktualizáciách pred ňou, ale neposkytuje žiadne záruky o informáciách mimo reťazca. na vytvorenie distribuovaného usporiadania vyžadujeme, aby spoločné podpisy obsahovali najnovší hash aktualizácie z účtovnej knihy spolupodpisovateľa. tento hash sa potom začlení do hashu aktuálnej aktualizácie a stane sa súčasťou reťazca, ako aj súčasťou všetkých ostatných reťazcov, pre ktoré operátor účtovnej knihy spoločne podpisuje, čím sa vytvorí sieť kauzality. toto nedokáže explicitne dokázať čas, ale dokáže to dokázať, že určité informácie boli vytvorené v konkrétnom poradí

## dôkazy podvodu

môžeme dokázať rôzne typy podvodu odhalením informácií, ktoré boli vytvorené v nesprávnom poradí. ak informácie nie sú zahrnuté bežnými sieťovými operáciami, môžu byť prepašované vytvorením aktivity, ktorá zahŕňa hash dôkazu. po začlenení do aktualizácie podpísanej operátorom sa dôkaz odhalí ako vytvorený na nekonformnom mieste v usporiadaní:

- operátor, ktorý ponúkol pripísanie prostriedkov na vklad zaslaných na reťazci na konkrétnu adresu, podpíše aktualizáciu účtovnej knihy, ktorá neobsahuje príslušný kredit, ale obsahuje reťazec odhaľujúci nejaký hash bloku presahujúci počet potvrdení povolených pred pripísaním

- operátor, ktorý vytvoril lightning faktúru v mene vkladu, podpíše aktualizáciu účtovnej knihy, ktorá nepripísala vkladu prostriedky napriek tomu, že preimage bol odhalený v reťazci

- spoločný podpis, ktorý deklaruje aktuálny hash účtovnej knihy ako taký, ktorý predchádza ich vlastnému neskoršiemu hashu v reťazci

- člen kvóra spornej účtovnej knihy, ktorý bol aktívny, ale nekonal v súlade s dôkazom podvodu v rámci stanoveného počtu blokov

- podpísanie alebo spoločné podpísanie nekonformných aktualizácií účtovnej knihy

dôkaz podvodu pozostáva z dôkazu a kauzálneho reťazca spájajúceho vložený hash s účtovnou knihou obvineného operátora. reťazec je postupnosť spoločne podpísaných aktualizácií, z ktorých každá obsahuje member_ledger_hash z účtovnej knihy predchádzajúceho článku. overovatelia prechádzajú reťazec bez vyhľadávania, potvrdzujúc, že každý článok je podpísaná aktualizácia a že hash dôkazu zodpovedá vloženým údajom

## obnova

keď sa účtovná kniha stane nedostupnou alebo nekonformnou, členovia kvóra môžu vytvoriť vlastné pokračovanie účtovnej knihy od poslednej konformnej aktualizácie. musia vytvoriť nové kvórum a poskytnúť atestácie kolaterálu. členovia musia následne koordinovať minutie predchádzajúceho výstupu rezerv do lotérie potenciálnych ďalších reťazcov. víťaz tejto lotérie pripojí aktualizáciu akvizície ku svojmu reťazcu a ostatní pripoija výnos. peňaženky naďalej adresujú tú istú účtovnú knihu, akceptujúc iba odpovede spoločne podpísané kvórom. periodicky a keď odpovede nemajú očakávaný spoločný podpis, peňaženka by mala dotazovať sieť a prehrať aktualizácie účtovnej knihy na identifikáciu zmien v správe

keď sa nekonformnosť javí ako náhodná (napr. účtovná kniha sa stala nedostupnou na určitý počet blokov), zmena správy musí byť ohľaduplná: len množstvo rezerv potrebné na pokrytie záväzkov účtovnej knihy sa odošle do lotérie a zvyšok sa vráti na verejný kľúč operátora. kontrola kolaterálu nie je ovplyvnená

keď existuje dôkaz o nekonformnosti, suma presahujúca nevyhnutné rezervy sa rovnomerne rozdelí medzi členov kvóra a kolaterál držaný na účtovných knihách členov je povolené skonfiškovanť

## zdravie siete

jedným priamočiarym útokom je vytvorenie ostrovov tajne spolupracujúcich operátorov. po vybudovaní značných záväzkov naprieč ich účtovnými knihami koordinujú odchod, čím ukradnú prostriedky prevyšujúce stratený kolaterál. sieť sa môže brániť proti tomuto útoku, okrem oblastí, kde interná hodnota prevyšuje kolaterál spájajúci ju s nespolupracujúcou sieťou. vyššie kolaterálne pomery a väčšie, rozmanitejšie kvóra znižujú pravdepodobnosť formovania týchto vreciek, ale môžu sa vytvoriť úmyselne a nemôžeme očakávať, že každá peňaženka vyhodnotí celú sieť. namiesto toho by trhy objavovania mali publikovať metriky zodpovednosti operátorov založené na grafových analýzach, ako sú algoritmy zbierania cien

## záver

navrhujeme kolaterálnu sieť, ktorá vyžaduje tajnú dohodu na krádež, ale tajná dohoda zvyšuje ohrozený kolaterál rýchlejšie, než zvyšuje hodnotu, ktorú je možné ukradnúť. túto sieť používame na zabezpečenie kryptografických účtovných kníh krytých plnými rezervami. tieto účtovné knihy obsluhujú účty v mene offline peňaženiek výmenou za vopred dohodnuté poplatky. primitívy účtovnej knihy podporujú podmienky minutia v miniscript dostatočné pre základné smart kontrakty. sieť sa škáluje takmer lineárne, čo umožňuje veľkej sieti poskytnúť miliardy peňaženiek a objem transakcií prevyšujúci tradičné platobné siete
