# bitcoin deposits
## sažetak

idealna peer-to-peer verzija elektroničkog novca omogućila bi slanje online plaćanja izravno od jedne strane drugoj, brzo i uz minimalnu pripremu. lightning mreža pruža dio rješenja, no ključne prednosti se gube ako je potrebna pouzdana treća strana za upravljanje stanjem u vaše ime. predlažemo rješenje ovog problema korištenjem provjerljivih knjiga i mreže kolaterala. operateri emitiraju ažuriranja knjiga svojim vršnjacima, stvarajući revizijski zapis računa. novčanici emitiraju dokaze o nepoštenju tim vršnjacima, koji osiguravaju da knjiga održava poštenog operatera. jednostrani izlazak zamijenjen je jamstvom da sredstva ostaju dostupna sve dok to čini i mreža. dolazimo do mreže koja delegira održavanje likvidnosti, izbjegava naknade za postavljanje, sposobna je primati plaćanja izvan mreže i skalira se neovisno o osnovnom sloju

## uvod

bitcoin deposits ima za cilj pružiti brza i skalabilna sredstva kontrolirana ključevima, bez potrebe za povjerenjem, izvan lanca. aktivnost na lancu skalira se s brojem knjiga i učestalošću rotacije rezervi. propusnost skalira nešto iznad linearno s brojem knjiga u mreži, čineći milijune transakcija u sekundi preko trilijuna novčanika vjerojatnim

postoje eksplicitni kompromisi:
- nema jednostranog izlaska: kada operateri zakažu, sredstva ostaju u mreži
- nema privatnosti: verifikacija zahtijeva transparentnost
- povremena dostupnost: depozit je dostupan samo koliko i operater. novčanici bi trebali raspodijeliti sredstva kako bi povećali dostupnost

očekujemo da će iskustvo novčanika biti slično brzom osnovnom sloju, s ekonomikom plaćanja sličnom lightning mreži

## knjige

knjiga je nepromjenjivi lanac ažuriranja, koji sadrži hash prethodnog ažuriranja i potpisan od strane operatera knjige. različite vrste ažuriranja imaju različita pravila koja reguliraju kada i kako se mogu koristiti. knjige su samoopisne, njihova ažuriranja javno dostupna i neporeciva, omogućujući svakome da procijeni usklađenost

knjige imaju jednog aktivnog operatera, ali ih kooperativno održava mreža. bilo koji operater može stvoriti jednu, no ako nestane ili postane nepošten, bit će dodijeljen drugi operater, zajedno s rezervama. trenutno aktivni operater identificiran je javnim ključem koji je korišten za potpisivanje najnovijeg zajednički potpisanog ažuriranja

## depoziti

depozit je stabilan račun koji može slati i primati sredstva, kontroliran pomoću miniscript. pri otvaranju se uspostavlja raspored naknada, kao i to zahtijeva li primanje sredstava zahtjev potpisan od strane novčanika. operater mora dopustiti prijenose između depozita na istoj knjizi kao i izlaske na lanac. trebao bi dopustiti depozitima da plaćaju lightning fakture

na diskreciji je operatera stvaranje ponuda za financiranje na lancu ili lightning faktura u ime depozita. ako to učine, ove bi trebale biti zajednički potpisane od strane člana kvoruma, a novčanik bi trebao verificirati taj potpis. ponude i fakture nisu dio knjige, pa je odgovornost novčanika da verificira potpise i zadrži ih kao dokaz

## naknade

prijenosi između depozita, na lancu i kroz lightning imaju naknade koje se plaćaju operateru knjige. postoje i naknade koje se periodički primjenjuju na stanja s određenim periodom. sve se dogovaraju kada se otvori novi depozit. naknade se mogu promijeniti nakon određenog broja blokova, uz određenu obavijest u blokovima i unutar postotnog ograničenja po prilagodbi dogovorenog pri otvaranju. kvorum može odbiti zajednički potpisati ažuriranja koja stvaraju neprofitabilne okolnosti za koje bi u konačnici mogli biti odgovorni

## prijenosi

osnovni oblik prijenosa je dvofazna operacija između dva depozita na istoj knjizi: depozit izdaje zahtjev za slanje sredstava. ako su dostupna dovoljna sredstva, zaključavanje sredstava s uvjetom trošenja dodaje se knjizi. ako je uvjet trošenja ispunjen prije isteka vremena, sredstva se prebacuju od pošiljatelja primatelju umanjeno za naknadu operatera. ako istekne vrijeme, zaključavanje se otpušta, umanjeno za manju naknadu operatera. s miniscript uvjetima trošenja, ovo je dovoljno da bilo koji depozit pruža mostove i usluge likvidnosti drugim depozitima na istoj knjizi

## lightning

operateri koji imaju lightning kanal mogu dopustiti depozitima slanje i primanje putem lightning mreže. kada depozit zatraži lightning fakturu, operater je stvara putem svog lightning čvora, traži od članova kvoruma da je zajednički potpišu kako bi dokazali da su predani pripisivanju sredstava depozitu nakon plaćanja. novčanik bi trebao zadržati ovu zajednički potpisanu fakturu kao dokaz. kada depozit zatraži plaćanje lightning fakture, operater plaća koristeći svoj lightning čvor i tereti depozit nakon dobivanja preimage

kada su platitelj i primatelj depoziti na istom operateru, operater može podmiriti interno bez usmjeravanja kroz lightning, pripisujući i tereteći odgovarajuće depozite izravno. ovo izbjegava naknade za usmjeravanje i načine neuspjeha uz održavanje istih računovodstvenih jamstava

## kuriri

zahtjevi za prijenos prebacuju sredstva samo između depozita na istoj knjizi. za prebacivanje sredstava između knjiga, novčanici koriste kurire — usluge koje drže depozite na više knjiga i prenose sredstva između njih. kurir oglašava kapacitet i smjerne naknade po knjizi na releju. kada novčanik želi poslati s knjige A na knjigu B, stvara zaključavanje prijenosa na depozit kurira i traži da kurir stvori jedno sa svog depozita na odredišnoj knjizi prema primatelju. nakon što su oba zaključavanja uspostavljena, novčanik otkriva preimage primatelju, koji dovršava prijenos od kurira. nakon otkrivanja, kurir koristi isti preimage za dovršavanje prijenosa od pošiljatelja kuriru

ovo je standardni hash time-locked contract obrazac. očekujemo da će odlazni vremenski istek kurira biti strogo raniji od dolaznog, osiguravajući da ako novčanik nikada ne otkrije, oba zaključavanja isteknu i nijedna strana ne gubi sredstva. nije potrebno povjerenje osim jamstva vremenskog isteka koje provode operateri

kuriri bi trebali postaviti naknade po knjizi: fee_in i fee_out za svaku knjigu koju opslužuju. novčanik procjenjuje trošak rute kao fee_out na izvoru plus fee_in na odredištu. kuriri mogu varirati naknade po knjizi na temelju dostupne likvidnosti, prirodno rebalansirajući svoje pozicije. novčanici otkrivaju kurire putem njihovih oglasa na releju i biraju na temelju naknada, kapaciteta ili pokrivenosti

## komunikacija

sva komunikacija između novčanika i operatera, te između operatera, koristi nostr releje. ažuriranja knjiga objavljuju se kao trajni događaji koje releji zadržavaju, stvarajući trajni revizijski zapis. zahtjevi i odgovori između novčanika i operatera su efemerni događaji s kratkim TTL na releju. operateri oglašavaju svoje uvjete kao zamjenjive događaje, omogućujući novčanicima da otkriju i usporede operatere bez centraliziranog imenika

ova arhitektura znači da novčanici ne trebaju trajne veze -- mogu otići izvan mreže neograničeno i nadoknaditi propušteno ponovnim reprodukciranjem događaja s bilo kojeg releja koji ih ima. operaterima se može pristupiti putem bilo kojeg releja koji nadziru, a izbor releja je odluka implementacije, a ne ograničenje protokola

## rezerve i kolateral

rezerve se drže u utxo s iznosom većim ili jednakim zbroju obveza knjige, potrošivim od strane većine kvoruma, s povratom operateru nakon značajnog razdoblja

kolateral je vlastiti kapital operatera, položen i zaključan na knjigama članova kvoruma. svaki član drži kolateralni depozit koji operater financira i zaključava na određeno trajanje. ukupne obveze knjige ograničene su na dvostruku vrijednost najmanjeg kolateralnog zaključavanja koje drži bilo koji član, a trajanje kvoruma ograničeno je na najkraće vrijeme zaključavanja. ovo osigurava da mreža kolaterala uvijek ima dovoljno pokrića za prijenos skrbništva. isti kolateralni depozit može podupirati više knjiga radi poboljšanja kapitalne učinkovitosti, iako bi novčanici trebali preferirati operatere s nepreklapajućim izvorima kolaterala

obveze se provode pri stvaranju novih ponuda za financiranje ili faktura. operater ne može stvarati ponude ili fakture koje bi gurnule ukupne obveze knjige iznad rezervi ili iznad dvostruke vrijednosti najmanjeg kolateralnog zaključavanja, što god je manje

## kvorum

operateri traže od drugih operatera da se pridruže njihovom kvorumu polaganjem i zaključavanjem kolaterala na knjizi člana. zahtjev uključuje obvezu kolaterala (iznos i trajanje zaključavanja) i uvjete člana: minimalne rasporede naknada koje depoziti na knjizi moraju ispunjavati. svaki član mora upravljati vlastitom knjigom i može zaplijeniti kolateral operatera ako je operater dokazano neusklađen. članovi specificiraju ograničenja rasporeda naknada tijekom svog članstva u kvorumu -- operater ne može otvoriti depozite s naknadama ispod najstrožih minimuma članova, štiteći članove od nasljeđivanja neprofitabilnih obveza nakon prijenosa skrbništva

nakon uspostave kvoruma, rezerve se rotiraju u novi multisig utxo. članovi zajednički potpisuju valjana ažuriranja i sudjeluju u oporavku ako operater potpiše neusklađena. veći kvorumi povećavaju komunikacijske troškove, ali smanjuju rizik operatera, povećavaju dostupnost i čine tajni dogovor težim i skupljim. novčanici bi trebali preferirati veće kvorume

## ekonomsko odvraćanje

protokol zamjenjuje jednostrani izlazak ekonomskim odvraćanjem. članovi kvoruma izravno su poticani da djeluju protiv nepoštenja. tijekom normalnih operacija zarađuju skromne naknade na kolateralu, ali u slučaju dokazivo neusklađenog ponašanja mogu zaplijeniti potpuni kolateralni depozit operatera na svojoj knjizi

kada novčanik posumnja na cenzuru, može eskalirati zahtjev članovima kvoruma putem certificirane dostave. član ugrađuje hash zahtjeva u vlastitu knjigu uz malu naknadu, stvarajući kauzalno usidreni dokaz. ako operater ne obradi zahtjev, član ima i dokaz i ekonomski poticaj za pokretanje spora

prijevara s lightning fakturama slijedi isti obrazac odvraćanja. operater zna je li preimage primljen, ali novčanik ne zna. međutim, bilo koji platitelj može pružiti preimage novčaniku. jedna potvrđena krađa pokreće spor, zapljenu rezervi i konfiskaciju kolaterala. nagrada za krađu jednog plaćanja je ograničena, ali rizik je egzistencijalan, čineći lightning krađu ekonomski iracionalnom unatoč tome što je formalno nedokaziva bez suradnje treće strane

način neuspjeha za odvraćanje od cenzure i lightning prijevare je jednoglasni tajni dogovor kvoruma. protokol ne može zaštititi od kvoruma koji surađuje u krađi, ali mreža kolaterala osigurava da tajni dogovor košta više nego što donosi. transparentnost mreže omogućuje novčanicima i tržištima otkrivanja da identificiraju sumnjive strukture kvoruma prije polaganja sredstava

## vrijeme

apsolutno vrijeme mjeri se prema osnovnom sloju. tolerancije ne mogu premašiti razuman broj potvrda kako bi se održala stabilnost tijekom reorganizacija lanca

gdje su potrebne veće tolerancije, oslanjamo se na kauzalno uređivanje. kriptografska knjiga je merkle lanac. svako ažuriranje dokazuje da je stvoreno nakon svih ažuriranja prije njega, ali ne pruža jamstva o informacijama izvan lanca. kako bismo konstruirali distribuirano uređivanje, zahtijevamo da zajednički potpisi uključuju najnoviji hash ažuriranja s knjige zajedničkog potpisnika. taj hash se zatim ugrađuje u hash trenutnog ažuriranja, postajući dio lanca kao i dio svih drugih lanaca za koje operater knjige zajednički potpisuje, stvarajući mrežu kauzalnosti. ovo ne može eksplicitno dokazati vrijeme, ali može dokazati da su određeni dijelovi informacija stvoreni u specifičnom redoslijedu

## dokazi prijevare

možemo dokazati različite vrste prijevare izlaganjem informacija koje su stvorene u pogrešnom redoslijedu. gdje informacije nisu uključene normalnim mrežnim operacijama, mogu se prokrijumčariti stvaranjem aktivnosti koja uključuje hash dokaza. nakon ugradnje u ažuriranje potpisano od strane operatera, dokaz se otkriva kao stvoren na neusklađenom mjestu u redoslijedu:

- operater, koji je ponudio da pripiše sredstva depozitu poslana na lancu na određenu adresu, potpisuje ažuriranje knjige koje ne sadrži odgovarajuće pripisivanje, ali sadrži lanac koji otkriva neki hash bloka koji premašuje broj potvrda dopuštenih prije pripisivanja

- operater, koji je stvorio lightning fakturu u ime depozita, potpisuje ažuriranje knjige koje nije pripisalo sredstva depozitu unatoč tome što je preimage otkriven u lancu

- zajednički potpis koji deklarira da je trenutni hash knjige onaj koji prethodi njihovom kasnijem hashu u lancu

- član kvoruma osporavane knjige koji je bio aktivan ali nije postupio u skladu s dokazom prijevare unutar određenog broja blokova

- potpisivanje ili zajedničko potpisivanje neusklađenih ažuriranja knjige

dokaz prijevare sastoji se od dokaza i kauzalnog lanca koji povezuje ugrađeni hash s knjigom optuženog operatera. lanac je niz zajednički potpisanih ažuriranja, od kojih svaki uključuje member_ledger_hash s knjige prethodne karike. verifikatori prolaze lancem bez pretraživanja, potvrđujući da je svaka karika potpisano ažuriranje i da hash dokaza odgovara ugrađenim podacima

## oporavak

nakon što knjiga postane nedostupna ili neusklađena, članovi kvoruma mogu stvoriti vlastiti nastavak knjige od zadnjeg usklađenog ažuriranja. moraju uspostaviti novi kvorum i pružiti atestacije kolaterala. članovi se zatim moraju koordinirati da potroše prethodni izlaz rezervi na lutriju potencijalnih sljedećih lanaca. pobjednik ove lutrije dodaje ažuriranje akvizicije svom lancu, a ostali dodaju ustupanje. novčanici nastavljaju obraćati se istoj knjizi, prihvaćajući samo odgovore zajednički potpisane od strane kvoruma. povremeno, i kada odgovori nemaju očekivani zajednički potpis, novčanik bi trebao upitati mrežu i ponoviti ažuriranja knjige kako bi identificirao promjene u skrbništvu

kada neusklađenost djeluje slučajno (npr. knjiga je postala nedostupna na određeni broj blokova) promjena skrbništva mora biti obzirna: samo iznos rezervi potreban za pokriće obveza knjige šalje se na lutriju, a ostatak se vraća na javni ključ operatera. kontrola kolaterala ostaje nepromijenjena

kada postoji dokaz neusklađenosti, iznos koji prelazi potrebne rezerve dijeli se jednako među članovima kvoruma, a kolateral koji se drži na knjigama članova dopušteno je zaplijeniti

## zdravlje mreže

jedan jednostavan napad je formiranje otoka koluzivnih operatera. nakon izgradnje značajnih obveza na svojim knjigama, koordiniraju izlazak, kradući sredstva koja premašuju izgubljeni kolateral. mreža se može obraniti od ovoga, osim u regijama gdje interna vrijednost premašuje kolateral koji je povezuje s nekoluzivnom mrežom. viši omjeri kolaterala i veći, raznovrsniji kvorumi smanjuju vjerojatnost formiranja ovih džepova, ali mogu se formirati namjerno i ne možemo očekivati da će svaki novčanik evaluirati cijelu mrežu. umjesto toga, tržišta otkrivanja trebala bi objavljivati metrike odgovornosti operatera temeljene na analizama grafova kao što su prize-collecting algoritmi

## zaključak

predlažemo kolateralnu mrežu koja zahtijeva tajni dogovor za krađu, ali tajni dogovor povećava kolateral u opasnosti brže nego što povećava vrijednost koja se može ukrasti. koristimo ovu mrežu za osiguranje kriptografskih knjiga podržanih punim rezervama. ove knjige opslužuju račune u ime izvanmrežnih novčanika u zamjenu za unaprijed dogovorene naknade. primitivi knjige podržavaju miniscript uvjete trošenja dovoljne za osnovne pametne ugovore. mreža skalira gotovo linearno, omogućujući velikoj mreži da pruži milijarde novčanika i obujam transakcija koji premašuje tradicionalne platne mreže
