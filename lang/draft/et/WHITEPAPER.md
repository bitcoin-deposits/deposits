# bitcoin deposits
## kokkuvõte

ideaalne peer-to-peer elektrooniline sularaha võimaldaks veebimakseid saata otse ühelt osapoolelt teisele kiiresti ja minimaalse ettevalmistusega. lightning võrk pakub osalist lahendust, kuid olulised eelised kaovad, kui usaldusväärne kolmas osapool peab teie nimel olekut haldama. me pakume selle probleemi lahenduseks kontrollitavaid pearaamatuid ja tagatiste võrku. operaatorid edastavad pearaamatu värskendusi oma võrdsetele, luues kontrollitava kontode kirje. rahakotid edastavad ebaaususe tõendeid neile võrdsetele, kes tagavad, et pearaamat hoiab operaatori ausana. ühepoolne väljumine asendatakse garantiiga, et vahendid jäävad kättesaadavaks seni, kuni võrk toimib. me jõuame võrguni, mis delegeerib likviidsuse haldamise, väldib seadistustasusid, suudab makseid vastu võtta võrguväliselt ja skaleerub põhikihist sõltumatult

## sissejuhatus

bitcoin deposits eesmärk on pakkuda kiiret ja skaleeruvat võtmega kontrollitavat rahastamist, usalduseta, ahelaväliselt. ahelasisene tegevus skaleerub pearaamatute arvu ja reservide rotatsiooni sagedusega. läbilaskse skaleerub veidi üle lineaarselt pearaamatute arvuga võrgus, muutes miljonid tehingud sekundis triljonite rahakottide üleselt usutavaks

on selged kompromissid:
- ühepoolne väljumine puudub: kui operaatorid ebaõnnistuvad, jäävad vahendid võrku
- privaatsus puudub: kontrollimine nõuab läbipaistvust
- katkendlik kättesaadavus: deposiit on ainult nii kättesaadav kui operaator. rahakotid peaksid vahendeid hajutama, et suurendada kättesaadavust

me eeldame, et rahakoti kasutuskogemus sarnaneb kiirele põhikihile, omades makseökonoomikat, mis sarnaneb lightning võrgule

## pearaamatud

pearaamat on muutumatu värskenduste ahel, mis sisaldab eelmise värskenduse hash'i ja on allkirjastatud pearaamatu operaatori poolt. erinevatel värskendustüüpidel on erinevad reeglid, mis reguleerivad millal ja kuidas neid saab kasutada. pearaamatud on enesekirjeldavad, nende värskendused on avalikult kättesaadavad ja eitamatud, võimaldades igaühel hinnata vastavust

pearaamatutel on üks aktiivne operaator, kuid neid hoitakse koostöös võrgu poolt. iga operaator võib ühe luua, kuid kui nad peaksid kaduma või muutuma ebaausaks, määratakse uus operaator koos reservidega. hetkel aktiivne operaator tuvastatakse avaliku võtmega, mida kasutati viimase kaasallkirjastatud värskenduse allkirjastamiseks

## deposiidid

deposiit on stabiilne konto, mis saab saata ja vastu võtta vahendeid, kontrollituna miniscript'iga. avamisel kehtestatakse tasugraafik, samuti see, kas vahendite vastuvõtmine nõuab rahakoti allkirjastatud päringut. operaator peab lubama ülekandeid deposiitide vahel samal pearaamatul ning ahelasiseseid väljumisi. nad peaksid lubama deposiitidel maksta lightning arveid

operaatori otsustada on, kas luua ahelasiseseid rahastamispakkumisi või lightning arveid deposiidi nimel. kui nad seda teevad, peaksid need olema kvoorumi liikme poolt kaasallkirjastatud ja rahakott peaks seda allkirja kontrollima. pakkumised ja arved ei ole pearaamatu osa, seega on rahakoti kohustus allkirju kontrollida ja neid tõendina säilitada

## tasud

ülekanded deposiitide vahel, ahelasiseselt ja lightning'i kaudu on tasulised, tasud makstakse pearaamatu operaatorile. samuti on tasud, mida rakendatakse perioodiliselt saldodele kindlaksmääratud perioodiga. kõik on läbiräägitud uue deposiidi avamisel. tasusid saab muuta pärast kindlaksmääratud arvu plokke, arvestades kindlaksmääratud plokiteatamist ja avamisel läbiräägitud kohandamise protsendilimiiti. kvoorum võib keelduda kaasallkirjastamast värskendusi, mis loovad kahjumlikke olusid, mille eest nad võimalikel vastutavad

## ülekanded

ülekande põhivorm on kahefaasiline operatsioon kahe deposiidi vahel samal pearaamatul: deposiit esitab päringu vahendite saatmiseks. kui piisavalt vahendeid on saadaval, lisatakse pearaamatule vahendite lukk koos kulutamistingimusega. kui kulutamistingimus täidetakse enne aegumist, liiguvad vahendid saatjalt saajale, millest on maha arvatud operaatori tasu. kui aegumine saabub, vabastatakse lukk, millest on maha arvatud väiksem operaatori tasu. miniscript kulutamistingimustega on see piisav, et võimaldada igal deposiidil pakkuda silla- ja likviidsusteenuseid teistele deposiitidele samal pearaamatul

## lightning

operaatorid, kellel on lightning kanal, võivad lubada deposiitidel saata ja vastu võtta lightning võrgu kaudu. kui deposiit taotleb lightning arvet, loob operaator selle oma lightning sõlme kaudu, palub kvoorumi liikmetel seda kaasallkirjastada, et tõestada nende pühendumust deposiidi krediteerimisele makse laekumisel. rahakott peaks seda kaasallkirjastatud arvet tõendina säilitama. kui deposiit taotleb lightning arve maksmist, maksab operaator oma lightning sõlme kaudu ja debiteerib deposiidi pärast preimage'i saamist

kui maksja ja saaja on deposiidid samal operaatoril, võib operaator arveldada sisemiselt ilma lightning'i kaudu marsruutimata, krediteerides ja debiteerides vastavaid deposiite otse. see väldib marsruutimistasusid ja tõkkerežiime, säilitades samad arvestusgarantiid

## kullerid

ülekandepäringud liigutavad vahendeid ainult deposiitide vahel samal pearaamatul. vahendite liigutamiseks üle pearaamatute kasutavad rahakotid kullereid -- teenuseid, mis hoiavad deposiite mitmel pearaamatul ja kannavad ülekandeid nende vahel. kuller reklaamib mahutavust ja pearaamatupõhiseid suunatasusid releel. kui rahakott soovib saata pearaamatust A pearaamatusse B, loob ta ülekande luku kulleri deposiidile ja palub kulleril luua ühe oma deposiidist sihtpearaamatul saajale. kui mõlemad lukud on kehtestatud, paljastab rahakott preimage'i saajale, kes viib lõheb kulleri ülekande. kui paljastatud, kasutab kuller sama preimage'i, et viia lõheb ülekanne saatjalt kullerile

see on standardne hash time-locked contract muster. me eeldame, et kulleri väljaminev aegumine on rangelt varasem kui sissetulev, tagades, et kui rahakott ei paljasta kunagi, aeguvad mõlemad lukud ja kumbki osapool ei kaota vahendeid. usaldust ei ole vaja peale operaatorite poolt tagatud aegumisgarantii

kullerid peaksid seadma pearaamatupõhised tasud: fee_in ja fee_out iga pearaamatu jaoks, mida nad teenindavad. rahakott hindab marsruudi kulu kui fee_out lähtepearaamatul pluss fee_in sihtpearaamatul. kullerid võivad tasusid pearaamatu põhiselt varieerida saadaoleva likviidsuse alusel, tasakaalustades loomulikult oma positsioone. rahakotid avastavad kullereid nende reklaamide kaudu releel ja valivad tasu, mahutavuse või katvuse alusel

## kommunikatsioon

kogu suhtlus rahakottide ja operaatorite vahel ning operaatorite vahel kasutab nostr releesid. pearaamatu värskendused avaldatakse kestvate sündmustena, mida releed säilivad, luues püsiva kontrollitava kirje. päringud ja vastused rahakottide ja operaatorite vahel on efemeersed sündmused lühikese relee TTL-iga. operaatorid reklaamivad oma tingimusi asendatavate sündmustena, võimaldades rahakottidel operaatoreid avastada ja võrrelda ilma tsentraliseeritud kataloogita

see arhitektuur tähendab, et rahakotid ei vaja püsivaid ühendusi -- nad võivad minna määramata ajaks võrguväliseks ja järele jõuda, taasesitades sündmusi igast releest, millel need on. operaatoritega saab ühendust võtta iga relee kaudu, mida nad jälgivad, ja relee valik on juurutamisotsus, mitte protokolli piirang

## reservid ja tagatis

reserve hoitakse utxo's summaga, mis on suurem või võrdne pearaamatu kohustuste summaga, kulutatav kvoorumi enamuse poolt, tagavarana operaatorile pärast olulist perioodi

tagatis on operaatori enda kapital, deponeeritud ja lukustatud kvoorumi liikmete pearaamatutele. iga liige hoiab tagatisdeposiiti, mille operaator rahastab ja lukustab kindlaksmääratud ajaks. pearaamatu kogukohustused on piiratud kahekordse vähimseima tagatisluku summaga, mida hoiab ükskõik liige, ja kvoorumi kestus on piiratud lühima lukustusajaga. see tagab, et tagatiste võrk omab alati piisavalt toetust hoolduse ülekandmise katmiseks. sama tagatisdeposiit võib toetada mitut pearaamatut kapitali efektiivsuse parandamiseks, kuigi rahakotid peaksid eelistama operaatoreid mittekattuvate tagatisallikatega

kohustused jõustatakse uute rahastamispakkumiste või arvete loomisel. operaator ei saa luua pakkumisi või arveid, mis lükaks pearaamatu kogukohustused üle reservide või üle kahekordse vähimseima tagatisluku, olenevalt kumb on madalam

## kvoorum

operaatorid paluvad teistel operaatoritel liituda nende kvoorumiga, deponeerides ja lukustades tagatise liikme pearaamatule. päring sisaldab tagatiskohustust (summa ja lukustuskestus) ja liikme tingimusi: miinimumtasugraafikuid, mida pearaamatu deposiidid peavad täitma. iga liige peab opereerima oma pearaamatut ja võib operaatori tagatise konfiskeerida, kui operaator osutub mittevastavaks. liikmed määravad tasugraafikute piirangud oma kvoorumiliikmuse ajal -- operaator ei saa avada deposiite tasudega, mis jäävad alla rangeima liikme miinimumide, kaitstes liikmeid kahjumlike kohustuste pärimise eest pärast hoolduse ülekandmist

kui kvoorum on loodud, pööratakse reservid uude multisig utxo'sse. liikmed kaasallkirjastavad kehtivaid värskendusi ja osalevad taastamises, kui operaator allkirjastab mittevastavaid. suuremad kvoorumid suurendavad suhtluskoormust, kuid vähendavad operaatoririski, suurendavad kättesaadavust ja muudavad kokkumängimise raskemaks ja kulukamaks. rahakotid peaksid eelistama suuremaid kvoorumeid

## majanduslik heidutus

protokoll asendab ühepoolse väljumise majandusliku heidutusega. kvoorumi liikmed on otseselt motiveeritud ebaaususe vastu tegutsema. tavapärastel operatsioonidel teenivad nad tagasihoidlikke tasusid tagatiselt, kuid tõestatavalt mittevastavat käitumisel on neil õigus konfiskeerida operaatori kogu tagatisdeposiit oma pearaamatul

kui rahakott kahtlustab tsensuuri, võib ta päringu eskaleerida kvoorumi liikmetele sertifitseeritud kohaletoimetamise kaudu. liige manustab päringu hash'i oma pearaamatusse väikse tasu eest, luues põhjuslikult ankurdatud tõendi. kui operaator ei töötle päringut, on liikmel nii tõend kui ka majanduslik motivatsioon vaidluse algatamiseks

lightning arvepettus järgib sama heidutusmustrit. operaator teab, kas preimage laekus, kuid rahakott ei tea. siiski võib iga maksja anda preimage'i rahakotile. üks kinnitatud vargus käivitab vaidluse, reservide arestimise ja tagatise konfiskeerimise. varastamise tasu on piiratud, kuid risk on eksistentsiaalne, muutes lightning varguse majanduslikult irratsionaalseks, hoolimata sellest, et see on formaalselt tõestamatu ilma kolmanda osapoole koostööta

nii tsensuuri kui ka lightning heidutuse tõkkerežiim on ühehääleline kvoorumi kokkumängimine. protokoll ei suuda kaitsta kvoorumi eest, mis teeb koostööd varastamiseks, kuid tagatiste võrk tagab, et kokkumängimine maksab rohkem kui see toob. võrgu läbipaistvus võimaldab rahakottidel ja avastusturgudel tuvastada kahtlasi kvoorumistruktuure enne vahendite deponeerimist

## aeg

absoluutset aega mõõdetakse põhikihi suhtes. tolerantsid ei tohi ületada mõistlikku kinnituste arvu, et säilitada stabiilsus ahela ümberkorralduste ajal

kus on vajalikud kõrgemad tolerantsid, toetume põhjuslikule järjestamisele. krüptograafiline pearaamat on merkle ahel. iga värskendus tõestab, et see loodi pärast kõiki eelnevaid värskendusi, kuid ei anna garantiid ahelavälise teabe kohta. hajutatud järjestuse loomiseks nõuame, et kaasallkirjad sisaldaksid viimast värskenduse hash'i kaasallkirjastaja pearaamatust. see hash lisatakse seejärel praeguse värskenduse hash'i, saades osaks ahelast ning kõigi teiste ahelate osaks, mille jaoks pearaamatu operaator kaasallkirjastab, luues põhjuslikkuse võrgu. see ei suuda aega selgesõnaliselt tõestada, kuid suudab tõestada, et teatud teabetükid loodi kindlas järjekorras

## pettusetõendid

me saame tõestada erinevaid pettuseliike, paljastades teavet, mis on loodud vales järjekorras. kus teavet ei kaasata tavavõrguoperatsioonide käigus, saab seda sisse smugeldada, luues tegevust, mis sisaldab tõendi hash'i. kui see on lisatud operaatori allkirjastatud värskendusse, paljastatakse tõend kui loodud mittevastavalt kohalt järjestuses:

- operaator, olles pakkunud deposiidile krediteerimist vahenditega, mis on saadetud ahelasiseselt konkreetsele aadressile, allkirjastab pearaamatu värskenduse, mis ei sisalda vastavat krediteerimist, kuid sisaldab ahelat, mis paljastab mingi ploki hash'i, mis ületab enne krediteerimist lubatud kinnituste arvu

- operaator, olles loonud lightning arve deposiidi nimel, allkirjastab pearaamatu värskenduse, mis ei ole deposiiti krediteerinud hoolimata sellest, et preimage on ahelas paljastatud

- kaasallkiri, mis deklareerib praeguse pearaamatu hash'i olevat see, mis eelneb nende enda hilisemale hash'ile ahelas

- selle kvoorumi liige, kelle vaidlustatud pearaamat oli aktiivne, kuid kes ei tegutsenud kooskõlas pettusetõendiga teatud arvu plokkide jooksul

- mittevastavate pearaamatu värskenduste allkirjastamine või kaasallkirjastamine

pettusetõend koosneb tõenditest ja põhjuslikust ahelast, mis ühendab manustatud hash'i süüdistatava operaatori pearaamatuga. ahel on järjestus kaasallkirjastatud värskendustest, millest igaüks sisaldab member_ledger_hash'i eelmise lüli pearaamatust. kontrollijad kõnnivad ahela läbi ilma otsimata, kinnitades, et iga lüli on allkirjastatud värskendus ja et tõendava hash vastab manustatud andmetele

## taastamine

kui pearaamat on muutunud kättesaamatuks või mittevastavaks, võivad kvoorumi liikmed luua oma jätku pearaamatule viimasest vastavast värskendusest. nad peavad looma uue kvoorumi ja esitama tagatiskinnitused. liikmed peavad seejärel koordineerima eelmise reservide väljundi kulutamist võimalike järgmiste ahelate loteriiks. selle loterii võitja lisab oma ahelale omandamise värskenduse ja teised lisavad loovutuse. rahakotid jätkavad sama pearaamatu poole pöördumist, aktsepteerides ainult kvoorumi kaasallkirjastatud vastuseid. perioodiliselt ja kui vastusel puudub oodatud kaasallkiri, peaks rahakott pärima tegema võrgult ja taasesitama pearaamatu värskendusi, et tuvastada hoolduse muutusi

kui mittevastavus tundub juhuslik (nt pearaamat on muutunud kättesaamatuks teatud arvu plokkide jooksul), peab hoolduse vahetus olema lugupidav: ainult reservide summa, mis on vajalik pearaamatu kohustuste katmiseks, saadetakse loteriisse, ja tagasi saadetakse operaatori avalikule võtmele. tagatise kontroll ei muutu

kui mittevastavuse tõend on olemas, jaotatakse vajalikest reservidest ületav summa võrdselt kvoorumi liikmete vahel ja kvoorumi liikmete pearaamatutele lukustatud tagatise konfiskeerimine lubatakse

## võrgu tervis

üks lihtne rünnak on moodustada kokkumängvate operaatorite saari. pärast oluliste kohustuste kogumist oma pearaamatutele koordineerivad nad väljumist, varastades vahendeid, mis ületavad kaotatud tagatist. võrk suudab selle vastu kaitsta, välja arvatud piirkondades, kus sisemine väärtus ületab seda mittekollaboreeriva võrguga ühendava tagatise. kõrgemad tagatismäärad ja suuremad, mitmekesisemad kvoorumid vähendavad nende taskute tekkimise tõenäosust, kuid nad võivad tekkida tahtlikult ja me ei saa eeldada, et iga rahakott hindab kogu võrku. selle asemel peaksid avastusturud avaldama operaatori vastutavuse mõõdikuid graafianalüüside, nagu auhindade kogumise algoritmide põhjal

## kokkuvõte

me pakume tagatisevõrku, mis nõuab varastamiseks kokkumängimist, kuid kokkumängimine suurendab ohustatud tagatist kiiremini kui varastatavat väärtust. me kasutame seda võrku krüptograafiliste pearaamatute turvamiseks, mida toetavad täisreservid. need pearaamatud teenindavad kontosid võrguväliste rahakottide nimel eelläbiräägitud tasude eest. pearaamatu primitiivid toetavad miniscript kulutamistingimusi, mis on piisavad põhitarklepinguteks. võrk skaleerub peaaegu lineaarselt, võimaldades suurel võrgul pakkuda miljardeid rahakotte ja tehingumahtusid, mis ületavad traditsioonilisi maksevõrkusid
