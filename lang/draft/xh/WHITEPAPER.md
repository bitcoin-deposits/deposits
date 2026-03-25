# bitcoin deposits
## isishwankathelo

uhlobo olufanelekileyo lokuhlawula nge-imali ye-elektroniki phakathi kwabantu ababini lunokuvumela ukuba iintlawulo kwi-intanethi zithunyelwe ngqo komnye umntu zisuka komnye ngokukhawuleza nangokulungiselela okuncinci. i-lightning network inikezela inxalenye yesisombululo, kodwa uncedo olubalulekileyo luyalahleka ukuba kufuneka umntu wesithathu othembekileyo ukuba alawule imeko egameni lakho. siphakamisa isisombululo kule ngxaki sisebenzisa ii-ledger eziqinisekisekayo kunye newebhu ye-collateral. aba-operator bathunyelela izinto ezintsha zee-ledger kubalingane babo, besenza irekhodi elihlolekayo lee-akhawunti. ii-wallet zithumela ubungqina bokungathembeki kwabo balingane, abaqinisekisa ukuba i-ledger igcina u-operator othembekileyo. ukuphuma ngokuzimela kuthatyathelw'indawo sisiqinisekiso sokuba iimali zihlala zifumaneka logama uthungelwano lusenjalo. sifikelela kuthungelwano olunika uxanduva lokulondoloza imali engamanzi, lugwema iintlawulo zokuqalisa, lukwazi ukufumana iintlawulo ungekho kwi-intanethi, kwaye lukhula ngokuzimela kwisendlalelo sesiseko

## intshayelelo

bitcoin deposits ijolise ekunikezeleni iimali ezilawulwa ngezitshixo ezikhawulezayo nezikhulayo, ngaphandle kokuthemba, ngaphandle kwe-chain. umsebenzi we-on-chain ukhula kunye nenani lee-ledger nokuphindaphindwa kokutshintshwa kwezigcinelo. umthamo ukhula ngaphezulu kancinane kunokulinganayo nenani lee-ledger kuthungelwano, usenza izigidi zeetransekshoni ngesekoni kumazigidi-gidi ee-wallet zibe nokwenzeka

kukho izinto ezitshintshiswayo ngokucacileyo:
- akukho kuphuma ngokuzimela: xa aba-operator besilela iimali zihlala kuthungelwano
- akukho bucala: ukuqinisekisa kufuna ukucaca
- ukufumaneka okungaqhubekiyo: i-deposit ifumaneka ngokulingana no-operator. ii-wallet kufuneka zisasaze iimali ukuze zandise ukufumaneka

silindele ukuba amava e-wallet afane nesendlalelo sesiseko esikhawulezayo, sinee-ekonomiki yentlawulo efana ne-lightning network

## ii-ledger

i-ledger luluhlu olungaguqukiyo lwezinto ezintsha, oluqulathe i-hash yesinto esintsha sangaphambili kwaye lusayinwe ngu-operator we-ledger. iintlobo ezahlukeneyo zezinto ezintsha zinemithetho eyahlukeneyo elawula ukuba zingasetyenziswa nini kwaye njani. ii-ledger ziyazichaza ngokwazo, izinto ezintsha zazo zifumaneka esidlangalaleni kwaye azinakuphikwa, zivumela nabani na ukuba ahlole ukuthobela

ii-ledger zino-operator omnye osebenzayo, kodwa zigcinwa ngentsebenziswano yi-mesh. nawuphi na u-operator unokwenza enye, kodwa ukuba banyamalala okanye baba bangathembekanga u-operator owahlukileyo uya kunikwa, kunye nezigcinelo. u-operator osebenzayo ngoku uchongwa yi-pubkey esetyenziswe ukusayina isinto esintsha esisayinwe kunye okusandula ukwenziwa

## ii-deposit

i-deposit yiakhawunti ezinzileyo enokuthumela nokufumana iimali, elawulwa nge-miniscript. ekuvulweni kusekwa ishedyuli yeentlawulo, kwakunye nokuba ukufumana iimali kufuna isicelo esisayinwe yi-wallet kusini na. u-operator kufuneka avumele ukudluliselwa phakathi kwee-deposit kwi-ledger enye kwakunye nokuphuma kwe-on-chain. kufanele bavumele ii-deposit ukuba zihlawule ii-invoyisi ze-lightning

kusesigqibeni so-operator ukwenza iziphakamiso zokuxhasa kwe-on-chain okanye ii-invoyisi ze-lightning egameni le-deposit. ukuba bayenza, ezi kufanele zisayinwe kunye lilungu le-quorum, kwaye i-wallet kufuneka iqinisekise olu sayino. iziphakamiso nee-invoyisi aziyonxalenye ye-ledger, ngoko luxanduva lwe-wallet ukuqinisekisa iisayino nokuzigcina njengobungqina

## iintlawulo

ukudluliselwa phakathi kwee-deposit, kwe-on-chain, nange-lightning kuneentlawulo ezihlawulwa ku-operator we-ledger. kukwakho neentlawulo ezisetyenziswa rhoqo kumabhalansi ngexesha elichaziweyo. zonke ziyaxoxwa xa kuvulwa i-deposit entsha. iintlawulo zingatshintshwa emva kwenani elichaziweyo leebloko, ngokunikwa isaziso esichaziweyo sebloko nangaphakathi komda wepesenti ngolungiso ngalunye oxoxwe ekuvulweni. i-quorum inokwala ukusayina kunye izinto ezintsha ezidalwa iimeko ezingenzisi nzuzo ezinokuphela zibuxanduva babo

## ukudluliselwa

uhlobo olusiseko lokudluliselwa lusebenza ngamanyathelo amabini phakathi kwee-deposit ezimbini kwi-ledger enye: i-deposit ikhupha isicelo sokuthumela iimali. ukuba kukho iimali ezaneleyo ezifumanekayo, isitshixo kwiimali esinomqathango wokuchitha sifakwa kwi-ledger. ukuba umqathango wokuchitha uzalisekile phambi kwexesha, iimali zisuka kumthumeli ziye kumfumani kukhutshwe intlawulo yo-operator. ukuba ixesha liyafikelelwa, isitshixo siyakhululwa, kukhutshwe intlawulo encinci yo-operator. ngemiqathango yokuchitha ye-miniscript, oku kwanele ukuvumela nayiphi na i-deposit ukuba inikezele iibhriji neenkonzo zemali engamanzi kwezinye ii-deposit kwi-ledger enye

## lightning

aba-operator abane-channel ye-lightning banokuvumela ii-deposit ukuba zithumele zifumane nge-lightning network. xa i-deposit icela i-invoyisi ye-lightning, u-operator uyenza nge-lightning node yakhe, acele amalungu e-quorum ukuba asayine kunye ukubonisa ukuba bazibophelele ukukhreditisha i-deposit ekuhlawulweni. i-wallet kufanele igcine le-invoyisi esayinwe kunye njengobungqina. xa i-deposit icela ukuhlawulwa kwe-invoyisi ye-lightning, u-operator uhlawula esebenzisa i-lightning node yakhe kwaye akhuphe kwi-deposit emva kokufumana i-preimage

xa umhlawuli nomfumani beyii-deposit ku-operator omnye, u-operator angazicwangcisa ngaphakathi ngaphandle kokudlula nge-lightning, akhreditishe kwaye akhuphe kwii-deposit ngokuthe ngqo. oku kuphepha iintlawulo zokuhamba neemeko zokusilela ngelixa kugcinwa iziqinisekiso ezifanayo zokubalwa

## ii-courier

izicelo zokudluliselwa zishukumisa iimali kuphela phakathi kwee-deposit kwi-ledger enye. ukushukumisa iimali phakathi kwee-ledger, ii-wallet zisebenzisa ii-courier — iinkonzo ezibamba ii-deposit kwii-ledger ezininzi kwaye zithwale ukudluliselwa phakathi kwazo. i-courier ibhengeza umthamo neentlawulo zangalelo cala nge-ledger kwi-relay. xa i-wallet ifuna ukuthumela kwi-ledger A iye kwi-ledger B, yenza isitshixo sokudluliselwa kwi-deposit ye-courier kwaye icele ukuba i-courier yenze esinye kwi-deposit yabo kwi-ledger yendawo ekuya kuyo kumfumani. xa zombini izitshixo zisekiwe i-wallet ityhila i-preimage kumfumani, ogqibezela ukudluliselwa okuvela kwi-courier. xa ityholwe, i-courier isebenzisa le preimage inye ukugqibezela ukudluliselwa okusuka kumthumeli kuye kwi-courier

lo ngumkhwa osemgangathweni we-hash time-locked contract. silindele ukuba ixesha lokuphelelwa le-courier lokuphumayo libe ngaphambi ngokuqinileyo kwelokungena, ukuqinisekisa ukuba ukuba i-wallet ayityhili, zombini izitshixo ziyaphelelwa kwaye akukho mntu ulahlekelwayo ziimali. akufuneki kuthenjwa ngaphandle kwesiqinisekiso sexesha esinyanzeliswa ngaba-operator

ii-courier kufanele zisete iintlawulo nge-ledger: fee_in kunye ne-fee_out kwi-ledger nganye abayisebenzisayo. i-wallet ilinganisela indleko yendlela njenge-fee_out kumthombo kunye ne-fee_in kwindawo ekuya kuyo. ii-courier zingatshintsha iintlawulo nge-ledger ngokusekelwe kwimali engamanzi efumanekayo, zilinganisa ngokwendalo izikhundla zazo. ii-wallet zifumana ii-courier ngokubhengeza kwabo kwi-relay kwaye zikhethe ngokusekelwe kwiintlawulo, umthamo, okanye ukufika

## unxibelelwano

lonke unxibelelwano phakathi kwee-wallet naba-operator, naphakathi kwaba-operator, lusebenzisa ii-nostr relay. izinto ezintsha zee-ledger zipapashwa njengeziganeko ezihlala zikhona ezigcinwa zii-relay, zisenza irekhodi elisisigxina elihlolekayo. izicelo neempendulo phakathi kwee-wallet naba-operator zizinto ezenzeka okwexeshana ezine-TTL emfutshane ye-relay. aba-operator babhengezelwa imigaqo yabo njengeziganeko ezitshintshekayo, zivumela ii-wallet ukuba zifumane zithelekise aba-operator ngaphandle kweedirekhtri ezigxilileyo

le yakhiwo ithetha ukuba ii-wallet azifuni zinxibelelwano ezisigxina -- zinokuphuma kwi-intanethi ngokungapheli kwaye zifumane ngokuphinda zidlale iziganeko kwi-relay enayo. aba-operator bafumaneka ngayo nayiphi na i-relay abayijongileyo, kwaye ukukhetha i-relay sisigqibo sokusebenzisa, hayi isithintelo seprothokholi

## izigcinelo ne-collateral

izigcinelo zigcinwa kwi-UTXO enesichaphaza esilingana okanye esingaphezulu kwesilinganiso sezibophelelo ze-ledger, echithwa liqela elininzi le-quorum, elinokusetyenziswa ngu-operator emva kwexesha elide

i-collateral yimali yo-operator ngokwakhe, efakiweyo netshixiweyo kwii-ledger zamalungu e-quorum. ilungu ngalinye libamba i-deposit ye-collateral exhaswe ngu-operator kwaye itshixwe ixesha elichaziweyo. izibophelelo ze-ledger zilinganiselwa kabini kwe-collateral esona sincinane sesitshixo esigcinwe lilungu, kwaye ixesha le-quorum lilinganiselwa kwixesha elona lifutshane lesitshixo. oku kuqinisekisa ukuba iwebhu ye-collateral isoloko inemali eyaneleyo yokugquma ukudluliselwa kwelondolozo. i-deposit enye ye-collateral inokuxhasa ii-ledger ezininzi ukuphucula ukusebenza kwemali, nangona ii-wallet kufanele zikhethe aba-operator abanemithombo ye-collateral engagqithaniyo

izibophelelo zinyanzeliswa xa kuchongwa iziphakamiso ezintsha zokuxhasa okanye ii-invoyisi. u-operator akanakwenza iziphakamiso okanye ii-invoyisi ezinokutyhalela izibophelelo ze-ledger ngaphezu kwezigcinelo okanye ngaphezu kabini kwe-collateral esona sincinane sesitshixo, nayiphi na encinci

## quorum

aba-operator bacela aba-operator abanye ukuba bajoyine i-quorum yabo ngokufaka nokutshixa i-collateral kwi-ledger yelungu. isicelo siquka isibophelelo se-collateral (isixa nexesha lesitshixo) nemigaqo yelungu: iishedyuli ezincinci zeentlawulo ezimele zihlangatyezwe zii-deposit kwi-ledger. ilungu ngalinye kufuneka lisebenzise i-ledger yalo kwaye linokuhluthwa i-collateral yo-operator ukuba u-operator uboniswe ukuba akathobeli. amalungu achaza imida kwishedyuli zeentlawulo ngexesha lobulungu babo be-quorum -- u-operator akanakuvula ii-deposit ezinemintlawulo engaphantsi kweyona mincinci yelungu elingqongqo, ekhusela amalungu ekufumaneni izibophelelo ezingenzisi nzuzo emva kokudluliselwa kwelondolozo

xa i-quorum isekiwe, izigcinelo zitshintshwa kuya kwi-multisig UTXO entsha. amalungu asayina kunye izinto ezintsha ezisemthethweni kwaye athatha inxaxheba ekufumaneni kwakhona ukuba u-operator usayina ezingathobeli. ii-quorum ezinkulu zandisa umthwalo wonxibelelwano kodwa zinciphise umngcipheko wo-operator, zandise ukufumaneka, kwaye zenze ukubambisana kunzima nokuneendleko. ii-wallet kufanele zikhethe ii-quorum ezinkulu

## ukuthintela ngee-ekonomiki

iphrothokholi itshintsha ukuphuma ngokuzimela ngokuthintela ngee-ekonomiki. amalungu e-quorum anyanzeliswa ngokuthe ngqo ukuba asebenze ngokuchasene nokungathembeki. ngexesha lemisebenzi eqhelekileyo afumana iintlawulo ezincinci kwi-collateral, kodwa xa kukho ukuziphatha okungathobeli okubonakalisekayo banokuhluthwa i-collateral yonke yo-operator kwi-ledger yabo

xa i-wallet ikrokrela ukuvalwa, inokunyusela isicelo kumalungu e-quorum ngokuthumela okuqinisekisiweyo. ilungu lifaka i-hash yesicelo kwi-ledger yabo ngentlawulo encinci, lidale ubungqina obusekwe kwisizathu. ukuba u-operator uyasilela ukuqhuba isicelo, ilungu linobungqina kunye nesizathu se-ekonomiki sokuqalisa impikiswano

ubuqhetseba be-invoyisi ye-lightning bulandela umkhwa ofanayo wokuthintela. u-operator uyazi ukuba i-preimage ifunyenwe, kodwa i-wallet ayazi. nangona kunjalo nawuphi na umhlawuli anganikezela i-preimage kwi-wallet. ubusela obunye obuqinisekisiweyo buqalisa impikiswano, ukuthinjwa kwezigcinelo, nokuhluthwa kwe-collateral. umvuzo wokuba ngamaqhetseba kwintlawulo enye unomda, kodwa umngcipheko uphela wonke, usenza ubusela nge-lightning lungabi nangqiqo ye-ekonomiki nangona lungabonakaliseki ngokusemthethweni ngaphandle kokusebenziswana nomntu wesithathu

indlela yokusilela kokubini ukuvalwa nokuthintela kwe-lightning kukubambisana kuphelele kwe-quorum. iphrothokholi ayinakukukhusela kwi-quorum esebenza kunye ukuba, kodwa iwebhu ye-collateral iqinisekisa ukuba ukubambisana kuneendleko ezingaphezulu kokunyusa. ukucaca kothungelwano kuvumela ii-wallet neemarike zokufumana ukuba zichonge izakhiwo ze-quorum ezikrokrelekayo phambi kokufaka iimali

## ixesha

ixesha elingundoqo lilinganiswa ngesendlalelo sesiseko. ukubekezela akunakugqitha inani elifanelekileyo lokuqinisekiswa ukuze kugcinwe uzinzo ngexesha lokutshintshwa kwechayini

apho kufuneka ukubekezela okukhulu ngakumbi sixhomekeka kwisicwangciso sokubangela. i-ledger ye-khriptografi yichayini ye-merkle. isinto esintsha nganye sibonisa ukuba senziwe emva kwazo zonke izinto ezintsha phambi kwaso, kodwa akuniki ziqinisekiso malunga nolwazi ngaphandle kwechayini. ukwakha isicwangciso esisasaziweyo, sifuna ukuba iisayino ezenziwe kunye ziquke i-hash yesinto esintsha sokugqibela kwi-ledger yomsayini. lo hash ufakwa kwi-hash yesinto esintsha sangoku, usiba yinxalenye yechayini kwakunye neyazo zonke ezinye iichayini u-operator we-ledger abasayinela zona kunye, kudale iwebhu yokubangela. oku akukwazi kubonisa ixesha ngokucacileyo, kodwa kukwazi kubonisa ukuba iziqwenga ezithile zolwazi zenziwe ngoluhlu oluthile

## ubungqina bobuqhetseba

sinokubonisa iintlobo ezahlukeneyo zobuqhetseba ngokuveza ulwazi olwenziwe ngoluhlu olungalunganga. apho ulwazi lungafakwanga yimisebenzi eqhelekileyo yothungelwano, lungangeniswa ngokufihlekileyo ngokudala umsebenzi oqulathe i-hash yobungqina. xa ufakiwe kwisinto esintsha esisayinwe ngu-operator, ubungqina butyhilwa njengobwenziwe kwindawo engathobeli kwisicwangciso:

- u-operator, ethe wanikela ngokukhreditisha i-deposit ngemali ethunyelwe kwe-on-chain kwidilesi ethile, usayina isinto esintsha se-ledger esingaqulathe ikhredithi efanelekileyo, kodwa siqulathe ichayini eveza i-hash yebloko engaphezulu kwenani lokuqinisekiswa ekuvumelweyo phambi kwekhredithi

- u-operator, ethe wenza i-invoyisi ye-lightning egameni le-deposit, usayina isinto esintsha se-ledger esingakhreditishanga i-deposit nangona i-preimage ityholwe kwichayini

- isayino ekunye ethi i-hash ye-ledger yangoku yenye ephambili kwi-hash yayo kamva kwichayini

- ilungu le-quorum ye-ledger ephikisiweyo ebelisebenza kodwa alizange lenze ngokuhambelana nobungqina bobuqhetseba ngaphakathi kwenani leebloko

- ukusayina okanye ukusayina kunye izinto ezintsha ze-ledger ezingathobeli

ubungqina bobuqhetseba buqulathe ubungqina kunye nechayini yokubangela exhumanisa i-hash efakiweyo kwi-ledger yo-operator otyholwayo. ichayini luluhlu lwezinto ezintsha ezisayinwe kunye, nganye iqulathe i-member_ledger_hash evela kwilinki yangaphambili ye-ledger. abaqinisekisi bahamba ichayini ngaphandle kokukhangela, beqinisekisa ukuba ilinki nganye sisinto esintsha esisayinwe, nokuba i-hash yobungqina iyahambelana nedatha efakiweyo

## ukufumana kwakhona

xa i-ledger ingasafumaneki okanye ingathobeli, amalungu e-quorum anokwenza ukuqhubekeka kwabo kwi-ledger ukusuka kwisinto esintsha sokugqibela esithobela. kufuneka baseke i-quorum entsha baze banikezele ngeziqinisekiso ze-collateral. amalungu kufuneka adibanise ekuchitheni izigcinelo zangaphambili ziye kwilothari yeechayini ezinokuba ezilandelayo. owoyisileyo kule lothari ufaka isinto esintsha sokufumana kwichayini yabo, nabanye bafake isinto sokuyekelela. ii-wallet ziqhubeka zibhekisa kwi-ledger enye, zamkela kuphela iimpendulo ezisayinwe kunye yi-quorum. ngamaxesha athile, naxa iimpendulo zingenawo isayino ekunye elindelweyo, i-wallet kufuneka ibuze uthungelwano kwaye iphinde idlale izinto ezintsha ze-ledger ukuchonga utshintsho lolondolozo

xa ukungathobeli kubonakala kungenganjongo (umz., i-ledger ayifumaneki inani elichaziweyo leebloko) utshintsho lolondolozo kufuneka luhloniphe: kuphela isixa sezigcinelo esifunekayo ukugquma izibophelelo ze-ledger esithunyelwa kwilothari, notshintsho lubuyiselwe kwi-pubkey yo-operator. ulawulo lwe-collateral aluchaphazeleki

xa ubungqina bokungathobeli bukhona, isixa esingaphezulu kwezigcinelo ezifunekayo sahlulwa ngokulinganayo phakathi kwamalungu e-quorum, kwaye i-collateral egcinwe kwii-ledger zamalungu ivunyelwa ukuba ihluthwe

## impilo yothungelwano

uhlaselo olulula kukwakha iziqithi zaba-operator ababambisanayo. emva kokwakha izibophelelo ezibalulekileyo kwii-ledger zabo, badibanisa ukuphuma, bebe iimali ezingaphezulu kwe-collateral elahlekileyo. uthungelwano lunokuzivikela koku, ngaphandle kwemimandla apho ixabiso langaphakathi lingaphezulu kwe-collateral elixhumanisa kothungelwano olungabambisaniyo. izinga eliphezulu le-collateral nee-quorum ezinkulu nezahlukeneyo zinciphisa amathuba okuba ezi zipokotho zidaleke, kodwa zinokudalwa ngenjongo kwaye asinakuthemba ukuba yonke i-wallet ihlola lonke uthungelwano. endaweni yoko iimakethe zokufumana kufanele zipapashe imimiselo yoxanduva lo-operator ngokusekelwe kwizicatshulwa zomzobo ezinjenge-algoritimu ze-prize-collecting

## isiphelo

siphakamisa uthungelwano lwe-collateral olufuna ukubambisana ukuba, kodwa ukubambisana kunyusa i-collateral esengozini ngokukhawuleza kunexabiso eliza kubiwa. sisebenzisa olu thungelwano ukukhusela ii-ledger ze-khriptografi ezixhaswe zizigcinelo ezipheleleyo. ezi ledger zisebenzela iiakhawunti egameni lee-wallet ezingekho kwi-intanethi ngokutshintshana neentlawulo ezixoxwe kwangaphambili. izinto ezisiseko ze-ledger zixhasa imiqathango yokuchitha ye-miniscript eyaneleyo kwiikhontrakhthi ezilula ze-smart. uthungelwano lukhula ngokusondelana nokulinganayo, luvumela uthungelwano olukhulu ukuba lunikezele iibhiliyoni zee-wallet nomthamo wetransekshoni ongaphezulu koothungelwano bentlawulo bemveli
