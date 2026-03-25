# bitcoin deposits
## santrauka

ideali lygiavertė elektroninių grynųjų pinigų versija leistų internetinius mokėjimus siųsti tiesiogiai iš vienos šalies kitai greitai ir su minimaliu pasiruošimu. lightning tinklas suteikia dalį sprendimo, tačiau esminiai privalumai prarandami, jei reikia patikimos trečiosios šalies, kuri valdytų būseną jūsų vardu. siūlome šios problemos sprendimą naudojant patikrinamus registrus ir užstato tinklą. operatoriai transliuoja registro atnaujinimus savo partneriams, sukurdami audituojamą sąskaitų įrašą. piniginės transliuoja nesąžiningumo įrodymus tiems partneriams, kurie užtikrina, kad registras išlaikytų sąžiningą operatorių. vienašalis pasitraukimas pakeičiamas garantija, kad lėšos lieka prieinamos tol, kol veikia tinklas. gauname tinklą, kuris deleguoja likvidumo palaikymą, vengia sąrankos mokesčių, gali priimti mokėjimus neprisijungus ir plečiasi nepriklausomai nuo bazinio sluoksnio

## įvadas

bitcoin deposits siekia užtikrinti greitus ir keičiamo masto raktais kontroliuojamus fondus, be pasitikėjimo, už grandinės ribų. veikla grandinėje kinta priklausomai nuo registrų skaičiaus ir rezervų rotacijos dažnumo. pralaidumas didėja šiek tiek daugiau nei tiesiškai su registrų skaičiumi tinkle, todėl milijonai operacijų per sekundę per trilijonus piniginių yra įmanomi

yra aiškūs kompromisai:
- jokio vienašalio pasitraukimo: kai operatoriai žlunga, lėšos lieka tinkle
- jokio privatumo: verifikavimas reikalauja skaidrumo
- pertraukiamas prieinamumas: depozitas yra tiek prieinamas, kiek prieinamas operatorius. piniginės turėtų paskirstyti lėšas, kad padidintų prieinamumą

tikimės, kad piniginės patirtis bus panaši į greitą bazinį sluoksnį su mokėjimo ekonomika, panašia į lightning tinklą

## registrai

registras yra nekintama atnaujinimų grandinė, turinti ankstesnio atnaujinimo hash ir pasirašyta registro operatoriaus. skirtingi atnaujinimų tipai turi skirtingas taisykles, reglamentuojančias kada ir kaip jie gali būti naudojami. registrai yra save aprašantys, jų atnaujinimai viešai prieinami ir neatšaukiami, leidžiant bet kam įvertinti atitikimą

registrai turi vieną aktyvų operatorių, tačiau yra bendrai palaikomi tinklo. bet kuris operatorius gali sukurti registrą, tačiau jei jis dingsta arba tampa nesąžiningas, bus paskirtas kitas operatorius kartu su rezervais. šiuo metu aktyvus operatorius identifikuojamas pagal viešąjį raktą, kuris buvo naudotas pasirašyti naujausiam bendrai pasirašytam atnaujinimui

## depozitai

depozitas yra stabili sąskaita, galinti siųsti ir gauti lėšas, valdoma miniscript. atidarant nustatomas mokesčių grafikas, taip pat ar lėšų gavimui reikia piniginės pasirašyto prašymo. operatorius privalo leisti pervedimus tarp depozitų tame pačiame registre, taip pat išvedimus į grandinę. jie turėtų leisti depozitams apmokėti lightning sąskaitas faktūras

operatoriaus nuožiūra yra kurti finansavimo pasiūlymus grandinėje arba lightning sąskaitas faktūras depozito vardu. jei jie tai daro, tai turėtų būti bendrai pasirašyta kvorumo nario, o piniginė turėtų patikrinti šį parašą. pasiūlymai ir sąskaitos faktūros nėra registro dalis, todėl piniginės atsakomybė yra patikrinti parašus ir saugoti juos kaip įrodymus

## mokesčiai

pervedimai tarp depozitų, grandinėje ir per lightning turi mokesčius, mokamus registro operatoriui. taip pat yra mokesčiai, periodiškai taikomi likučiams su nurodytu periodu. visi jie derinami atidarant naują depozitą. mokesčiai gali būti keičiami po nurodyto blokų skaičiaus, su nurodytu blokų pranešimu ir per koregavimo procentine riba, suderinta atidarant. kvorumas gali atsisakyti bendrai pasirašyti atnaujinimus, kurie sukuria nuostolingas aplinkybes, už kurias jie galiausiai galėtų būti atsakingi

## pervedimai

pagrindinė pervedimo forma yra dviejų fazių operacija tarp dviejų depozitų tame pačiame registre: depozitas pateikia prašymą siųsti lėšas. jei yra pakankamai lėšų, registro prie lėšų pridedamas užraktas su išleidimo sąlyga. jei išleidimo sąlyga įvykdoma iki laiko limito, lėšos perkeliamos iš siuntėjo gavėjui atėmus operatoriaus mokestį. jei pasiekiamas laiko limitas, užraktas atleidžiamas atėmus mažesnį operatoriaus mokestį. su miniscript išleidimo sąlygomis to pakanka, kad bet kuris depozitas galėtų teikti tiltų ir likvidumo paslaugas kitiems depozitams tame pačiame registre

## lightning

operatoriai, turintys lightning kanalą, gali leisti depozitams siųsti ir gauti per lightning tinklą. kai depozitas prašo lightning sąskaitos faktūros, operatorius ją sukuria per savo lightning mazgą, prašo kvorumo narių bendrai ją pasirašyti, kad įrodytų savo įsipareigojimą kredituoti depozitą gavus mokėjimą. piniginė turėtų saugoti šią bendrai pasirašytą sąskaitą faktūrą kaip įrodymą. kai depozitas prašo apmokėti lightning sąskaitą faktūrą, operatorius sumoka naudodamas savo lightning mazgą ir debetuoja depozitą gavęs preimage

kai mokėtojas ir gavėjas yra depozitai to paties operatoriaus, operatorius gali atsiskaityti viduje nesiųsdamas per lightning, tiesiogiai kredituodamas ir debetuodamas atitinkamus depozitus. tai padeda išvengti maršrutizavimo mokesčių ir gedimo režimų, kartu išlaikant tas pačias apskaitos garantijas

## kurjeriai

pervedimo prašymai perkelia lėšas tik tarp depozitų tame pačiame registre. norint perkelti lėšas tarp registrų, piniginės naudoja kurjerius — paslaugas, kurios turi depozitus keliuose registruose ir perkelia pervedimus tarp jų. kurjeris skelbia pajėgumą ir kryptines mokesčius kiekvienam registrui perdavimo tinkle. kai piniginė nori siųsti iš registro A į registrą B, ji sukuria pervedimo užraktą kurjerio depozitui ir prašo, kad kurjeris sukurtų užraktą iš savo depozito paskirties registre gavėjui. kai abu užraktai nustatyti, piniginė atskleidžia preimage gavėjui, kuris užbaigia pervedimą iš kurjerio. atskleidus, kurjeris naudoja tą patį preimage užbaigti pervedimą iš siuntėjo kurjeriui

tai standartinis hash laiko apribotas sutarties šablonas. tikimės, kad kurjerio išeinantis laiko limitas bus griežtai ankstesnis nei įeinantis, užtikrinant, kad jei piniginė niekada neatskleidžia, abu užraktai baigia galioti ir nė viena šalis nepraranda lėšų. pasitikėjimo nereikia, išskyrus laiko limito garantiją, kurią užtikrina operatoriai

kurjeriai turėtų nustatyti mokesčius kiekvienam registrui: fee_in ir fee_out kiekvienam aptarnaujamam registrui. piniginė apskaičiuoja maršruto kainą kaip fee_out šaltinyje plius fee_in paskirtyje. kurjeriai gali keisti mokesčius pagal registrą atsižvelgdami į turimą likvidumą, natūraliai perbalancuodami savo pozicijas. piniginės atranda kurjerius per jų skelbimus perdavimo tinkle ir renkasi pagal mokestį, pajėgumą arba aprėptį

## komunikacija

visa komunikacija tarp piniginių ir operatorių bei tarp operatorių naudoja nostr perdavimo taškus. registro atnaujinimai skelbiami kaip ilgalaikiai įvykiai, kuriuos perdavimo taškai saugo, sukuriant nuolatinį audituojamą įrašą. prašymai ir atsakymai tarp piniginių ir operatorių yra trumpalaikiai įvykiai su trumpu perdavimo taško TTL. operatoriai skelbia savo sąlygas kaip pakeičiamus įvykius, leisdami piniginėms atrasti ir palyginti operatorius be centralizuoto katalogo

ši architektūra reiškia, kad piniginėms nereikia nuolatinių ryšių — jos gali būti neprisijungusios neribotą laiką ir pasivyti atkurdamos įvykius iš bet kurio perdavimo taško, kuris juos turi. operatorius galima pasiekti per bet kurį perdavimo tašką, kurį jie stebi, o perdavimo taško pasirinkimas yra diegimo sprendimas, o ne protokolo apribojimas

## rezervai ir užstatas

rezervai laikomi utxo su suma, lygia arba didesne nei registro įsipareigojimų suma, kurią gali leisti kvorumo dauguma, su atsargine galimybe operatoriui po reikšmingo laikotarpio

užstatas yra operatoriaus nuosavas kapitalas, deponuotas ir užrakintas kvorumo narių registruose. kiekvienas narys turi užstato depozitą, kurį operatorius finansuoja ir užrakina nurodytam laikotarpiui. registro bendri įsipareigojimai ribojami dviguba mažiausio bet kurio nario turimo užstato užrakto suma, o kvorumo trukmė ribojama trumpiausiu užrakto laiku. tai užtikrina, kad užstato tinklas visada turi pakankamai padengimo saugojimo perdavimui. tas pats užstato depozitas gali padengti kelis registrus siekiant pagerinti kapitalo efektyvumą, nors piniginės turėtų teikti pirmenybę operatoriams su nepersidengiančiais užstato šaltiniais

įsipareigojimai užtikrinami kuriant naujus finansavimo pasiūlymus ar sąskaitas faktūras. operatorius negali kurti pasiūlymų ar sąskaitų faktūrų, kurie stumtų registro bendrus įsipareigojimus virš rezervų arba virš dvigubos mažiausio užstato užrakto sumos, priklausomai nuo to, kuri yra mažesnė

## kvorumas

operatoriai prašo kitų operatorių prisijungti prie jų kvorumo deponuodami ir užrakindami užstatą nario registre. prašymas apima užstato įsipareigojimą (sumą ir užrakto trukmę) ir nario sąlygas: minimalius mokesčių grafikus, kuriuos turi atitikti registro depozitai. kiekvienas narys privalo valdyti savo registrą ir gali konfiskuoti operatoriaus užstatą, jei operatorius įrodytas neatitinkančiu. nariai nurodo mokesčių grafikų ribas savo kvorumo narystės metu — operatorius negali atidaryti depozitų su mokesčiais žemesniais nei griežčiausio nario minimumai, apsaugodamas narius nuo nuostolingų įsipareigojimų paveldėjimo po saugojimo perdavimo

kai kvorumas suformuotas, rezervai perkeliami į naują multisig utxo. nariai bendrai pasirašo galiojančius atnaujinimus ir dalyvauja atkūrime, jei operatorius pasirašo neatitinkančius. didesni kvorumai didina komunikacijos apkrovą, bet mažina operatoriaus riziką, didina prieinamumą ir apsunkina bei pabrangina sąmokslą. piniginės turėtų teikti pirmenybę didesniems kvorumams

## ekonominė atgrasymas

protokolas pakeičia vienašalį pasitraukimą ekonominiu atgrasinimu. kvorumo nariai yra tiesiogiai skatinami veikti prieš nesąžiningumą. įprastų operacijų metu jie uždirba kuklias palūkanas už užstatą, tačiau įrodomai neatitinkančio elgesio atveju jie gali konfiskuoti visą operatoriaus užstato depozitą savo registre

kai piniginė įtaria cenzūrą, ji gali eskaluoti prašymą kvorumo nariams per patvirtintą pristatymą. narys įterpia prašymo hash į savo registrą už nedidelį mokestį, sukurdamas priežastiškai įtvirtintą įrodymą. jei operatorius neapdoroja prašymo, narys turi ir įrodymą, ir ekonominę paskatą inicijuoti ginčą

lightning sąskaitos faktūros sukčiavimas seka tą patį atgrasymo modelį. operatorius žino, ar preimage buvo gautas, bet piniginė nežino. tačiau bet kuris mokėtojas gali pateikti preimage piniginei. vienas patvirtintas vagystės atvejis sukelia ginčą, rezervų areštą ir užstato konfiskavimą. vagystės iš vieno mokėjimo atlygis yra ribotas, bet rizika yra egzistencinė, todėl lightning vagystė yra ekonomiškai neracionali, nors formaliai neįrodoma be trečiosios šalies bendradarbiavimo

nesėkmės režimas tiek cenzūros, tiek lightning atgrasymo atveju yra vienbalsis kvorumo sąmokslas. protokolas negali apsaugoti nuo kvorumo, kuris bendradarbiauja vagydamas, tačiau užstato tinklas užtikrina, kad sąmokslas kainuoja daugiau nei duoda. tinklo skaidrumas leidžia piniginėms ir atradimo rinkoms identifikuoti įtartinas kvorumo struktūras prieš deponuojant lėšas

## laikas

absoliutus laikas matuojamas pagal bazinį sluoksnį. tolerancijos negali viršyti pagrįsto patvirtinimų skaičiaus, siekiant išlaikyti stabilumą grandinės reorganizacijų metu

kai reikia didesnių tolerancijų, remiamės priežastiniu eiliškumu. kriptografinis registras yra merkle grandinė. kiekvienas atnaujinimas įrodo, kad jis buvo sukurtas po visų ankstesnių atnaujinimų, bet nesuteikia garantijų apie informaciją už grandinės ribų. norint sukonstruoti paskirstytą eiliškumą, reikalaujame, kad bendri parašai apimtų naujausią atnaujinimo hash iš bendrą parašą suteikiančio registro. tas hash tada įtraukiamas į dabartinio atnaujinimo hash, tapdamas grandinės dalimi, taip pat visų kitų grandinių, kurioms registro operatorius bendrai pasirašo, dalimi, sukuriant priežastingumo tinklą. tai negali aiškiai įrodyti laiko, tačiau gali įrodyti, kad tam tikra informacija buvo sukurta konkrečia tvarka

## sukčiavimo įrodymai

galime įrodyti įvairių tipų sukčiavimą atskleisdami informaciją, kuri buvo sukurta neteisinga tvarka. kai informacija nėra įtraukiama įprastomis tinklo operacijomis, ji gali būti įnešta sukuriant veiklą, kuri apima įrodymų hash. kai tai įtraukiama į operatoriaus pasirašytą atnaujinimą, atskleidžiama, kad įrodymai buvo sukurti neatitinkančioje eiliškumo vietoje:

- operatorius, pasiūlęs kredituoti depozitą lėšomis, siųstomis grandinėje į konkretų adresą, pasirašo registro atnaujinimą, kuriame nėra atitinkamo kredito, bet yra grandinė, atskleidžianti tam tikrą bloko hash, viršijantį leistinų patvirtinimų skaičių prieš kreditavimą

- operatorius, sukūręs lightning sąskaitą faktūrą depozito vardu, pasirašo registro atnaujinimą, kuriame depozitas nekredituotas, nors preimage buvo atskleistas grandinėje

- bendras parašas, kuris deklaruoja dabartinį registro hash kaip tokį, kuris eina prieš jų pačių vėlesnį hash grandinėje

- ginčijamo registro kvorumo narys, kuris buvo aktyvus, bet neveikė pagal sukčiavimo įrodymą per nurodytą blokų skaičių

- neatitinkančių registro atnaujinimų pasirašymas arba bendras pasirašymas

sukčiavimo įrodymas susideda iš įrodymų ir priežastinės grandinės, jungiančios įterptą hash su kaltinamo operatoriaus registru. grandinė yra bendrai pasirašytų atnaujinimų seka, kiekvienas apimantis member_ledger_hash iš ankstesnės grandies registro. tikrintojai eina grandine neieškodami, patvirtindami, kad kiekviena grandis yra pasirašytas atnaujinimas ir kad įrodymo hash atitinka įterptus duomenis

## atkūrimas

kai registras tampa neprieinamas arba neatitinkantis, kvorumo nariai gali sukurti savo registro tęsinį nuo paskutinio atitinkančio atnaujinimo. jie turi suformuoti naują kvorumą ir pateikti užstato patvirtinimus. nariai tada turi koordinuotis, kad išleistų ankstesnį rezervų išvestį į galimų kitų grandinių loteriją. šios loterijos laimėtojas prideda įsigijimo atnaujinimą prie savo grandinės, o kiti prideda atsitraukimo atnaujinimą. piniginės ir toliau kreipiasi į tą patį registrą, priimdamos tik atsakymus, bendrai pasirašytus kvorumo. periodiškai, ir kai jokie atsakymai neturi tikėtino bendro parašo, piniginė turėtų užklausti tinklą ir atkurti registro atnaujinimus, kad nustatytų saugojimo pasikeitimus

kai neatitikimas atrodo atsitiktinis (pvz., registras tapo neprieinamas tam tikram blokų skaičiui), saugojimo perdavimas turi būti pagarbis: tik rezervų suma, reikalinga padengti registro įsipareigojimus, siunčiama į loteriją, o grąža siunčiama atgal operatoriaus viešajam raktui. užstato kontrolė nepasikeičia

kai egzistuoja neatitikimo įrodymas, suma, viršijanti būtinus rezervus, dalijama po lygiai tarp kvorumo narių, o užstatas, laikomas narių registruose, gali būti konfiskuotas

## tinklo sveikata

viena paprasta ataka yra suformuoti sąmokslaujančių operatorių salas. sukaupus reikšmingus įsipareigojimus savo registruose, jie koordinuojasi pasitraukti, pavogdami lėšas, viršijančias prarastą užstatą. tinklas gali nuo to apsiginti, išskyrus regionuose, kur vidinė vertė viršija užstatą, jungiantį jį su nesąmokslaujančiu tinklu. didesni užstato santykiai ir didesni, įvairesni kvorumai mažina tokių kišenių formavimosi tikimybę, tačiau jie gali formuotis tyčia ir negalime tikėtis, kad kiekviena piniginė įvertins visą tinklą. vietoj to atradimo rinkos turėtų skelbti operatorių atskaitomybės metrikas, pagrįstas grafų analizėmis, tokiomis kaip prizų rinkimo algoritmai

## išvada

siūlome užstato tinklą, kuris reikalauja sąmokslo vagystei, tačiau sąmokslas didina riziką prarandamą užstatą greičiau nei didina vagiamą vertę. naudojame šį tinklą kriptografinių registrų, padengtų pilnais rezervais, apsaugai. šie registrai aptarnauja sąskaitas neprisijungusių piniginių vardu mainais už iš anksto suderintus mokesčius. registro primityvai palaiko miniscript išleidimo sąlygas, pakankamas pagrindiniams išmaniesiems kontraktams. tinklas plečiasi beveik tiesiškai, leisdamas dideliam tinklui teikti milijardus piniginių ir operacijų apimtis, viršijančias tradicinių mokėjimų tinklus
