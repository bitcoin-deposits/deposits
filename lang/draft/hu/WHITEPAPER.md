# bitcoin deposits
## absztrakt

az elektronikus készpénz ideális peer-to-peer változata lehetővé tenné, hogy az online fizetéseket közvetlenül egyik féltől a másiknak küldjék, gyorsan és minimális előfeltétellel. a lightning hálózat a megoldás egy részét nyújtja, de az alapvető előnyök elvesznek, ha egy megbízott harmadik félre van szükség az állapot kezeléséhez az ön érdekében. a problémára verifikálható főkönyvek és egy biztosítéki háló használatával javaslunk megoldást. az operátorok főkönyv-frissítéseket közvetítenek társaiknak, auditálható számlanyilvántartást hozva létre. a tárcák a tisztességtelenség bizonyítékait továbbítják ezeknek a társaknak, akik biztosítják, hogy a főkönyv tisztességes operátort tartson fenn. az egyoldalú kilépést az a garancia váltja fel, hogy a pénzeszközök mindaddig elérhetőek maradnak, ameddig a hálózat is az. így egy olyan hálózathoz jutunk, amely delegálja a likviditáskarbantartást, elkerüli a beállítási díjakat, képes offline fizetések fogadására, és a bázisrétegtől függetlenül skálázódik

## bevezetés

a bitcoin deposits célja gyors és skálázható, kulcs által vezérelt pénzeszközök biztosítása, bizalom nélkül, láncen kívül. a láncbeli aktivitás a főkönyvek számával és a tartalékrotációk gyakoriságával skálázódik. az átviteli kapacitás a hálózatban lévő főkönyvek számánál kicsivel jobban, mint lineárisan skálázódik, így másodpercenkénti milliók tranzakciója trilliók tárcáival megvalósítható

explicit kompromisszumok vannak:
- nincs egyoldalú kilépés: ha az operátorok meghibásodnak, a pénzeszközök a hálózatban maradnak
- nincs adatvédelem: a verifikációhoz átláthatóság szükséges
- időszakos elérhetőség: egy betét csak annyira elérhető, mint az operátor. a tárcáknak érdemes elosztaniuk a pénzeszközöket az elérhetőség növelése érdekében

arra számítunk, hogy a tárcaélménye hasonló lesz egy gyors bázisréteghez, fizetési gazdaságtanban a lightning hálózathoz hasonlóan

## főkönyvek

a főkönyv frissítések megváltoztathatatlan lánca, amely tartalmazza az előző frissítés hash-ét, és amelyet a főkönyv operátora ír alá. a különböző típusú frissítésekre különböző szabályok vonatkoznak arra nézve, mikor és hogyan használhatóak. a főkönyvek önleíróak, frissítéseik nyilvánosan elérhetőek és nem tagadhatóak, így bárki értékelheti a megfelelőséget

a főkönyveknek egyetlen aktív operátoruk van, de a háló együttesen tartja fenn őket. bármely operátor létrehozhat egyet, de ha eltűnne vagy tisztességtelenné válna, másik operátor kerül kijelölésre, a tartalékokkal együtt. a jelenleg aktív operátort az a nyilvános kulcs azonosítja, amellyel a legutolsó közösen aláírt frissítés történt

## betétek

a betét egy stabil számla, amely pénzeszközöket tud küldeni és fogadni, miniscript által vezérelt. megnyitáskor díjszerkezet kerül megállapításra, valamint az, hogy a pénzeszközök fogadásához szükséges-e a tárca által aláírt kérés. az operátornak lehetővé kell tennie az átutalásokat az ugyanazon a főkönyvön lévő betétek között, valamint a láncbeli kilépéseket. lehetővé kell tenniük a betétek számára a lightning számlák kifizetését is

az operátor megítélése alapján hozhat létre láncbeli finanszírozási ajánlatokat vagy lightning számlákat egy betét nevében. ha így tesz, ezeket egy kvórumtagnak társaláírással kell ellátnia, és a tárcának ellenőriznie kell ezt az aláírást. az ajánlatok és számlák nem részei a főkönyvnek, így a tárca felelőssége az aláírások ellenőrzése és bizonyítékként való megőrzése

## díjak

a betétek közötti, láncbeli és lightning-on keresztüli átutalásoknak díjai vannak, amelyeket a főkönyv operátorának fizetnek. emellett meghatározott időszakonként egyenlegekre alkalmazott díjak is vannak. mindezek tárgyalásra kerülnek új betét nyitásakor. a díjak meghatározott számú blokk után, meghatározott blokkos értesítéssel és a nyitáskor tárgyalt módosításonkénti százalékos határon belül változtathatóak. a kvórum megtagadhatja a nyereségtelen körülményeket létrehozó frissítések társaláírását, amelyekért végső soron felelősek lehetnének

## átutalások

az átutalás alapvető formája egy kétfázisú művelet két betét között ugyanazon a főkönyvön: egy betét kiadja a pénzküldés kérelmét. ha elegendő pénzeszköz áll rendelkezésre, a pénzeszközökre vonatkozó zárolást egy költési feltétellel a főkönyvhöz fűzi. ha a költési feltétel határidő előtt teljesül, a pénzeszközök az operátori díj levonása után a küldőtől a címzetthez kerülnek. ha lejár a határidő, a zárolást feloldják, kisebb operátori díj levonása mellett. miniscript költési feltételekkel ez elégséges ahhoz, hogy bármely betét hidakat és likviditási szolgáltatásokat nyújtson más, ugyanazon főkönyvön lévő betéteknek

## lightning

a lightning csatornával rendelkező operátorok lehetővé tehetik a betétek számára a lightning hálózaton keresztüli küldést és fogadást. amikor egy betét lightning számlát kér, az operátor létrehozza azt a lightning csomópontján keresztül, és megkéri a kvórumtagokat, hogy társaláírják, bizonyítva elkötelezettségüket a betét jóváírása iránt fizetés esetén. a tárcának meg kell őriznie ezt a társaláírt számlát bizonyítékként. amikor egy betét lightning számla kifizetését kéri, az operátor a lightning csomópontján keresztül fizet, és a preimage megszerzése után megterheli a betétet

amikor a fizető és a kedvezményezett ugyanazon operátor betétjei, az operátor belsőleg is rendezhet anélkül, hogy a lightning hálózaton keresztül irányítana, közvetlenül jóváírva és megterhelve az adott betéteket. ez elkerüli az irányítási díjakat és hibamódokat, miközben fenntartja ugyanazokat a könyvviteli garanciákat

## futárok

az átutalási kérések csak ugyanazon főkönyvön lévő betétek között mozgatnak pénzeszközöket. főkönyvek közötti pénzküldéshez a tárcák futárokat használnak — olyan szolgáltatásokat, amelyek több főkönyvön rendelkeznek betétekkel és átutalásokat közvetítenek köztük. a futár hirdet kapacitást és főkönyvenkénti irányú díjakat a relayn. amikor egy tárca az A főkönyvről a B főkönyvre akar küldeni, zárolási átutalást hoz létre a futár betétjére, és kéri a futártól, hogy a cél főkönyvön lévő betétjéről hozzon létre egyet a címzett felé. mindkét zárolás létrejötte után a tárca feltárja a preimage-et a címzettnek, aki befejezi az átutalást a futártól. feltárás után a futár ugyanezt a preimage-et használja a küldőtől a futárhoz történő átutalás befejezésére

ez egy szabványos hash idő-zárolású szerződés minta. arra számítunk, hogy a futár kimenő időkorlátja szigorúan korábbi lesz, mint a bejövő, biztosítva, hogy ha a tárca soha nem tárja fel, mindkét zárolat lejár és egyik fél sem veszít pénzeszközöket. nem szükséges bizalom az operátorok által biztosított időkorlát garanciáján túlmenően

a futároknak főkönyvenkénti díjakat kell megadniuk: fee_in és fee_out minden általuk kiszolgált főkönyvre. a tárca az útvonal költségét a forráson lévő fee_out és a célon lévő fee_in összegeként becsüli. a futárok a rendelkezésre álló likviditás alapján főkönyvenkénti változtathatják a díjakat, természetes módon újraegyensúlyozva pozícióikat. a tárcák a futárokat hirdetéseiken keresztül fedezik fel a relay-en, és díj, kapacitás vagy lefedettség alapján választanak

## kommunikáció

a tárcák és operátorok, valamint az operátorok közötti minden kommunikáció nostr relay-eket használ. a főkönyv-frissítések tartós eseményekként kerülnek publikálásra, amelyeket a relay-ek megtartanak, állandó auditálható nyilvántartást hozva létre. a tárcák és operátorok közötti kérések és válaszok rövid relay TTL-lel rendelkező rövidéletű események. az operátorok a feltételeiket cserélhető eseményekként hirdetik, lehetővé téve a tárcák számára az operátorok felfedezését és összehasonlítását centralizált jegyzék nélkül

ez az architektúra azt jelenti, hogy a tárcáknak nincs szükségük állandó kapcsolatra -- tetszőleges ideig offline lehetnek, és bármely relay eseményeinek újrajátszásával felzárkózhatnak. az operátorok bármely általuk figyelt relay-en elérhetőek, és a relay választása üzembehelyezési döntés, nem protokoll korlátozás

## tartalékok és biztosíték

a tartalékokat egy utxo-ban tartják, amelynek összege nagyobb vagy egyenlő a főkönyv kötelezettségeinek összegével, a kvórum többsége által költhető, az operátor általi visszatéréssel egy jelentős időszak után

a biztosíték az operátor saját tőkéje, amely kvórumtagi főkönyvekre kerül elhelyezésre és zárolásra. minden tag egy biztosítéki betétet tart, amelyet az operátor finanszíroz és meghatározott időtartamra zárol. egy főkönyv összes kötelezettsége bármely tag által tartott legkisebb biztosítéki zárolat kétszeresére korlátozott, és a kvórum időtartama a legrövidebb zárolási időre korlátozott. ez biztosítja, hogy a biztosítéki háló mindig elegendő fedezettel rendelkezzen a felügyeleti átvitelhez. ugyanaz a biztosítéki betét több főkönyvet is fedezhet a tőkehatékonyság javítása érdekében, bár a tárcáknak érdemes az át nem fedő biztosítéki forrásokkal rendelkező operátorokat részesíteni előnyben

a kötelezettségek új finanszírozási ajánlatok vagy számlák létrehozásakor kerülnek érvényre. az operátor nem hozhat létre olyan ajánlatokat vagy számlákat, amelyek a főkönyv összes kötelezettségeit a tartalékok fölé vagy a legkisebb biztosítéki zárolat kétszerese fölé emelnék, amelyik alacsonyabb

## kvórum

az operátorok más operátorokat kérnek fel a kvórumukhoz való csatlakozásra azzal, hogy biztosítékot helyeznek el és zárolnak a tag főkönyvén. a kérés tartalmazza a biztosítéki kötelezettségvállalást (összeg és zárolási időtartam) és a tag feltételeit: minimális díjszerkezeteket, amelyeknek a főkönyv betétjeinek meg kell felelniük. minden tagnak saját főkönyvet kell üzemeltetnie, és elkobozhatja az operátor biztosítékát, ha az operátor bizonyítottan nem megfelelő. a tagok a kvórumtagságuk idejére díjszerkezeti korlátokat szabnak — az operátor nem nyithat a legszigorúbb tag minimumainál alacsonyabb díjú betéteket, megvédve a tagokat a nyereségtelen kötelezettségek átöröklésétől felügyeleti átvitel után

a kvórum létrehozása után a tartalékokat új multisig utxo-ba forgatják. a tagok társaláírják az érvényes frissítéseket és részt vesznek a helyreállításban, ha az operátor nem megfelelő frissítéseket ír alá. a nagyobb kvórumok növelik a kommunikációs költségeket, de csökkentik az operátori kockázatot, növelik az elérhetőséget, és megnehezítik és megdrágítják az összejátszást. a tárcáknak érdemes a nagyobb kvórumokat részesíteni előnyben

## gazdasági elrettentés

a protokoll az egyoldalú kilépést gazdasági elrettentéssel váltja fel. a kvórumtagok közvetlenül érdekeltek a tisztességtelenség elleni fellépésben. normál működés során szerény díjakat keresnek a biztosítékon, de bizonyíthatóan nem megfelelő viselkedés esetén elkobozhatják az operátor teljes biztosítéki betétjét a főkönyvükön

amikor egy tárca cenzúrát gyanít, a kérést igazolt kézbesítéssel a kvórumtagokhoz továbbíthatja. a tag kis díjért beágyazza a kérés hash-ét a saját főkönyvébe, okozatilag lehorgonyzott bizonyítékot teremtve. ha az operátor nem dolgozza fel a kérést, a tagnak megvan mind a bizonyítéka, mind a gazdasági ösztönzője a vita kezdeményezéséhez

a lightning számlacsalás ugyanezt az elrettentő mintát követi. az operátor tudja, hogy kapott-e preimage-et, de a tárca nem. ugyanakkor bármely fizető megadhatja a preimage-et a tárcának. egyetlen megerősített lopás vitát, tartalékok lefoglalását és biztosíték elkobzását váltja ki. az egyetlen fizetés ellopásának jutalma korlátozott, de a kockázat létfontosságú, így a lightning lopás gazdaságilag irracionálissá válik, annak ellenére, hogy harmadik fél közreműködése nélkül formálisan nem bizonyítható

mind a cenzúra, mind a lightning elrettentés hibamódja az egyhangú kvórum összejátszás. a protokoll nem tud védeni egy olyan kvórum ellen, amely együttműködik a lopással, de a biztosítéki háló biztosítja, hogy az összejátszás többe kerüljön, mint amennyit hoz. a hálózat átláthatósága lehetővé teszi a tárcák és a felfedező piacok számára, hogy gyanús kvórumszerkezeteket azonosítsanak a pénzeszközök elhelyezése előtt

## idő

az abszolút időt a bázisréteghez mérjük. a tűrések nem haladhatják meg a megerősítések ésszerű számát a láncújraszerveződések alatti stabilitás fenntartása érdekében

ahol magasabb tűrések szükségesek, ott okozati sorrendiségre támaszkodunk. a kriptográfiai főkönyv egy merkle lánc. minden frissítés bizonyítja, hogy az összes előtte lévő frissítés után készült, de nem nyújt garanciákat a láncon kívüli információkról. az elosztott sorrend kialakításához megköveteljük, hogy a társaláírások tartalmazzák a társaláíró főkönyvének legutolsó frissítési hash-ét. ez a hash aztán beépül az aktuális frissítés hash-ébe, a lánc részévé válva, valamint minden más lánc részévé is, amelyhez a főkönyv operátor társaláírást ad, okozati hálót hozva létre. ez nem képes az idő explicit bizonyítására, de képes bizonyítani, hogy bizonyos információk meghatározott sorrendben készültek

## csalásbizonylatok

különféle típusú csalásokat bizonyíthatunk olyan információk feltárásával, amelyek rossz sorrendben készültek. ahol az információt a normál hálózati műveletek nem tartalmazzák, becsempészhető a bizonyíték hash-ét tartalmazó aktivitás létrehozásával. miután beépült az operátor által aláírt frissítésbe, a bizonyíték feltárul mint ami a sorrendben nem megfelelő helyen készült:

- egy operátor, aki felajánlotta egy betétnek a láncra küldött pénzeszközök jóváírását egy adott címre, olyan főkönyv-frissítést ír alá, amely nem tartalmazza a megfelelő jóváírást, de tartalmaz egy láncot, amely feltárja a jóváírás előtt engedélyezett megerősítések számát meghaladó blokk hash-t

- egy operátor, aki lightning számlát hozott létre egy betét nevében, olyan főkönyv-frissítést ír alá, amely nem írta jóvá a betétet annak ellenére, hogy a preimage feltárult a láncban

- egy társaláírás, amely az aktuális főkönyv hash-t olyannak deklarálja, amely megelőzi a saját későbbi hash-ét a láncban

- egy vitatott főkönyv kvórumának tagja, aki aktív volt, de nem a csalásbizonylat szerint járt el meghatározott számú blokkon belül

- nem megfelelő főkönyv-frissítések aláírása vagy társaláírása

a csalásbizonylat a bizonyítékból és a beágyazott hash-t a vádlott operátor főkönyvével összekötő okozati láncból áll. a lánc társaláírt frissítések sorozata, amelyek mindegyike tartalmaz egy member_ledger_hash-t az előző láncszem főkönyvéből. az ellenőrök végigjárják a láncot keresés nélkül, megerősítik, hogy minden szem aláírt frissítés, és hogy a bizonylat hash-e megegyezik a beágyazott adatokkal

## helyreállítás

miután egy főkönyv elérhetetlenné válik vagy nem megfelelő, a kvórumtagok létrehozhatják a főkönyv saját folytatását az utolsó megfelelő frissítéstől. új kvórumot kell létrehozniuk és biztosítéki igazolásokat kell nyújtaniuk. a tagoknak ezután koordinálniuk kell az előző tartalék kimenet elköltéséhez a lehetséges következő láncok sorsolására. a sorsolás nyertese egy átvételi frissítést fűz a láncához, a többiek pedig egy átengedési frissítést. a tárcák továbbra is ugyanazt a főkönyvet címzik, és csak a kvórum által társaláírt válaszokat fogadják el. időszakosan, és amikor a válaszok nem tartalmazzák az elvárt társaláírást, a tárcának le kell kérdeznie a hálózatot és újra kell játszania a főkönyv-frissítéseket a felügyeleti változások azonosítása érdekében

amikor a nem megfelelés véletlennek tűnik (pl. egy főkönyv meghatározott számú blokkra elérhetetlenné vált), a felügyeleti változásnak tisztelettudónak kell lennie: csak a főkönyv kötelezettségeinek fedezéséhez szükséges tartalékmennyiség kerül a sorsolásba, és a visszajáró az operátor nyilvános kulcsára kerül visszaküldésre. a biztosíték feletti irányítás nem változik

amikor nem megfelelőséget bizonyító bizonylat létezik, a szükséges tartalékok feletti összeg egyenlően oszlik el a kvórum tagjai között, és a tag-főkönyveken tartott biztosíték elkobozhatóvá válik

## hálózati egészség

egy egyértelmű támadás az összejátszó operátorok szigeteinek kialakítása. miután jelentős kötelezettségeket építettek fel főkönyveiken, koordináltan lépnek ki, ellopva a biztosítéki veszteséget meghaladó pénzeszközöket. a hálózat védekezhet ez ellen, kivéve azokban a régiókban, ahol a belső érték meghaladja a nem összejátszó hálózathoz kapcsolódó biztosítékot. a magasabb biztosítéki arányok és a nagyobb, sokszínűbb kvórumok csökkentik e zsebek kialakulásának valószínűségét, de szándékosan is létrejöhetnek, és nem várhatjuk el minden tárcától, hogy értékelje az egész hálózatot. ehelyett a felfedező piacoknak operátori elszámoltathatósági metrikákat kell közzétennie gráf-elemzések alapján, például díj-gyűjtő algoritmusok segítségével

## következtetés

egy olyan biztosítéki hálózatot javasolunk, amelyhez összejátszás szükséges a lopáshoz, de az összejátszás gyorsabban növeli a kockáztatott biztosítékot, mint az eltulajdonítható értéket. ezt a hálózatot teljes tartalékkal fedezett kriptográfiai főkönyvek biztosítására használjuk. ezek a főkönyvek offline tárcák számára szolgáltatnak számlákat előre megtárgyalt díjak fejében. a főkönyvi primitívek miniscript költési feltételeket támogatnak, amelyek az alapvető okosszerződésekhez elegendőek. a hálózat közel lineárisan skálázódik, lehetővé téve, hogy egy nagy hálózat milliárdnyi tárcát és a hagyományos fizetési hálózatokat meghaladó tranzakcióvolument biztosítson
