# bitcoin deposits
## isifinyezo

inguqulo ephelelayo yemali yedijithali phakathi kwabantu ababili ingavumela ukukhokha nge-inthanethi kuthunyelwe ngqo kumuntu ngamunye ngokushesha nangokulangazelelwa okuncane. i-lightning network inikeza ingxenye yesixazululo, kodwa izinzuzo ezibalulekile ziyalahleka uma kudingeka umuntu wesithathu othembekile ukuze aphathe isimo egameni lakho. siphakamisa isixazululo salenkinga sisebenzisa ama-ledger aqinisekisekayo nenethiwekhi ye-collateral. ama-operator asakaza izibuyekezo zama-ledger kubalingane babo, okudala irekhodi elihlolekayo lama-akhawunti. ama-wallet asakaza ubufakazi bokungathembeki kulabo balingane, abaqinisekisa ukuthi i-ledger igcina u-operator othembekile. ukuphuma ngasohlangothini olulodwa kuthathelwa indawo yisiqiniseko sokuthi imali ihlala itholakala uma nje inethiwekhi isebenza. sifika kunethiwekhi enikezela ukuphathwa kokutholakala kwemali, igwema izindleko zokusethwa, ikwazi ukwamukela ukukhokha ungekho ku-inthanethi, futhi ikhula ngokuzimela esendlaleni sesiseko

## isingeniso

bitcoin deposits ihlose ukuhlinzeka ngemali esheshayo nekhulayo elawulwa ngokhiye, ngokungathembi muntu, ngaphandle kwe-chain. umsebenzi we-on-chain ukhula ngenani lama-ledger kanye nokushintshwa kwezimali ezigciniwe. umthamo ukhula ngaphezudlana kokufanayo nenani lama-ledger kunethiwekhi, okwenza izigidi zemisebenzi ngomzuzwana kuzigidigidi zama-wallet kube yinto engenzeka

kunokushintshisana okusobala:
- akukho ukuphuma ngasohlangothini olulodwa: lapho ama-operator ehluleka imali ihlala kunethiwekhi
- akukho ubumfihlo: ukuqinisekiswa kudinga ukusobala
- ukutholakala okungahlali njalo: i-deposit itholakala kuphela uma u-operator etholakala. ama-wallet kufanele asakaze imali ukuze akhulise ukutholakala

silindele ukuthi isipiliyoni se-wallet sifane nesendlalelo sesiseko esisheshayo, sinezindleko zokukhokha ezifana ne-lightning network

## ama-ledger

i-ledger iwuchungechunge olungaguquki lwezibuyekezo, oluqukethe i-hash yesibuyekezo sangaphambilini futhi lusayinwe ngu-operator we-ledger. izinhlobo ezahlukene zezibuyekezo zinemithetho ehlukene elawula ukuthi zingasetshenziswa nini futhi kanjani. ama-ledger azichaza wona, izibuyekezo zawo zitholakala emphakathini futhi aziphikiseki, okuvumela noma ubani ukuthi ahlole ukuhambisana

ama-ledger ane-operator eyodwa esebenzayo, kodwa agcinwa ngokubambisana yi-mesh. noma iyiphi i-operator ingadala elilodwa, kodwa uma inyamalala noma ingathembekanga u-operator ohlukile uzonikwa, kanye nezimali ezigciniwe. u-operator osebenza njengamanje uchongwa nge-pubkey esetshenziselwe ukusayina isibuyekezo sakamuva esisayinwe ngokubambisana

## ama-deposit

i-deposit iyi-akhawunti ezinzile engathumela futhi yamukele imali, elawulwa nge-miniscript. ekuvulweni isheduli yezindleko imiswa, kanye nokuthi ukwamukela imali kudinga isicelo esisayinwe yi-wallet yini noma cha. u-operator kumele avumele ukudluliswa phakathi kwama-deposit ku-ledger elifanayo kanye nokuphuma kwe-on-chain. kufanele avumele ama-deposit ukukhokha ama-invoice e-lightning

kusesandleni se-operator ukudala iziphakamiso zokuxhaswa kwe-on-chain noma ama-invoice e-lightning egameni le-deposit. uma ekwenza, lezi kufanele zisayinwe ngokubambisana yilunga le-quorum, futhi i-wallet kufanele iqinisekise lesi sayino. iziphakamiso nama-invoice akuyona ingxenye ye-ledger, ngakho kuwumthwalo we-wallet ukuqinisekisa izisayino nokuzigcina njengobufakazi

## izindleko

ukudluliswa phakathi kwama-deposit, i-on-chain, nange-lightning kunezindleko ezikhokhelwa u-operator we-ledger. kukhona nezindleko ezifakwa ngezikhathi ezithile emananini esikhathi esicacisiwe. zonke zixoxisanwa lapho i-deposit entsha ivulwa. izindleko zingashintshwa emva kwenani elicacisiwe lamablokhi, ngokwaziswa ngebhlokhi elicacisiwe nangaphakathi komkhawulo wephesenti ngokushintsha ngakunye oxoxisanwe ngawo ekuvulweni. i-quorum ingala ukusayina ngokubambisana izibuyekezo ezidala izimo ezingenanzuzo ezingagcina zibe wumthwalo wazo

## ukudluliswa

uhlobo oluyisisekelo lokudluliswa luwumsebenzi onamabanga amabili phakathi kwama-deposit amabili ku-ledger elifanayo: i-deposit ikhipha isicelo sokuthumela imali. uma kunemali eyanele etholakalayo, ukukhiya kwemali okunombandela wokusetshenziswa kunezelelwa ku-ledger. uma umbandela wokusetshenziswa ugcwaliswa ngaphambi kwesikhathi, imali isuka kumthumeli iye kumamukeli kususwe indleko ye-operator. uma isikhathi sifikiwe, ukukhiya kukhululwa, kususwe indleko encane ye-operator. ngemibandela yokusetshenziswa ye-miniscript, lokhu kwanele ukuvumela noma iyiphi i-deposit ukuthi ihlinzeke ngamabhuloho nezinsizakalo zokutholakala kwemali kwamanye ama-deposit ku-ledger elifanayo

## lightning

ama-operator ane-channel ye-lightning angavumela ama-deposit ukuthumela nokwamukela nge-lightning network. lapho i-deposit icela i-invoice ye-lightning, u-operator uyidala nge-node yakhe ye-lightning, acele amalunga e-quorum ukuthi ayisayine ngokubambisana ukufakazela ukuthi azibophezele ukukhredithi i-deposit lapho kukhokhelwa. i-wallet kufanele igcine le-invoice esayinwe ngokubambisana njengobufakazi. lapho i-deposit icela ukukhokha i-invoice ye-lightning, u-operator ukhokha esebenzisa i-node yakhe ye-lightning bese ekhipha ku-deposit emva kokuthola i-preimage

lapho umkhokhi nomamukeli beyii-deposit ku-operator ofanayo, u-operator angaxazulula ngaphakathi ngaphandle kokudlulisa nge-lightning, akhredithe futhi akhiphe kuma-deposit athintekayo ngqo. lokhu kugwema izindleko zokuqondisa nezinkinga zokuhluleka ngesikhathi kugcina iziqiniseko ezifanayo zokubalwa

## ama-courier

izicelo zokudluliswa zihambisa imali kuphela phakathi kwama-deposit ku-ledger elifanayo. ukuhambisa imali phakathi kwama-ledger, ama-wallet asebenzisa ama-courier — izinsizakalo ezibamba ama-deposit kuma-ledger amaningi futhi zithwale ukudluliswa phakathi kwawo. i-courier ikhangisa umthamo nezindleko zangakolunye ukolunye ku-ledger ngalinye ku-relay. lapho i-wallet ifuna ukuthumela ku-ledger A iye ku-ledger B, idala ukukhiya kokudluliswa ku-deposit ye-courier futhi icele ukuthi i-courier idale okukodwa kusuka ku-deposit yakhe ku-ledger lapho kufanele kufike khona kumamukeli. lapho kokubili ukukhiya sekumisiwe i-wallet yembula i-preimage kumamukeli, oqedela ukudluliswa kusuka ku-courier. uma isembuliwe, i-courier isebenzisa le-preimage efanayo ukuqedela ukudluliswa kusuka kumthumeli kuya ku-courier

leli yiphethini evamile ye-hash time-locked contract. silindele ukuthi isikhathi sokuvala se-courier esiphumayo sibe ngaphambi kwaleso esingenayo ngokuqinile, ukuqinisekisa ukuthi uma i-wallet ingembuli, kokubili ukukhiya kuphelelwa yisikhathi futhi akukho hlangothi olulahlekelwa yimali. akudingeki ukwethemba ngaphezu kwesiqiniseko sesikhathi esiphoqelwa ama-operator

ama-courier kufanele abeke izindleko ze-ledger ngalinye: fee_in ne-fee_out ku-ledger ngalinye abalinsizayo. i-wallet iqagela izindleko zomzila njenge-fee_out kumthombo kanye ne-fee_in endaweni ekuya kuyo. ama-courier angashintshashintsha izindleko nge-ledger ngokusekelwe ekutholakaleni kwemali, alinganise izikhundla zawo ngokwemvelo. ama-wallet athola ama-courier ngokukhangiswa kwabo ku-relay futhi akhethe ngezindleko, umthamo, noma ukumboza

## ukuxhumana

konke ukuxhumana phakathi kwama-wallet nama-operator, naphakathi kwama-operator, kusebenzisa ama-nostr relay. izibuyekezo zama-ledger zishicilelwa njengezenzakalo eziqinile ama-relay azigcinayo, okudala irekhodi eliqhubekayo elihlolekayo. izicelo nezimpendulo phakathi kwama-wallet nama-operator yizenzakalo zesikhashana ezine-TTL emfushane ku-relay. ama-operator akhangisa imibandela yawo njengezenzakalo ezingathathelwa indawo, okuvumela ama-wallet ukuthola nokuqhathanisa ama-operator ngaphandle kwenkomba ephakathi

le-architecture isho ukuthi ama-wallet awakudingi ukuxhumana okuhlala njalo -- angaphuma ku-inthanethi isikhathi esingenamkhawulo futhi alandele ngokudlala kabusha izenzakalo kunoma iyiphi i-relay enazo. ama-operator angatholakala nganoma iyiphi i-relay awaqaphayo, futhi ukukhetha i-relay yisinqumo sokumiswa, akusona isibopho seprothokholi

## izimali ezigciniwe ne-collateral

izimali ezigciniwe zigcinwa ku-UTXO enesilinganiso esilingana noma esingaphezu kwesamba sezibophezelo ze-ledger, esetshenziselwa iningi le-quorum, ebuya ku-operator emva kwesikhathi eside

i-collateral yimali ye-operator uqobo, efakwe futhi yakhiyelwa kuma-ledger amalunga e-quorum. ilunga ngalinye libamba i-deposit ye-collateral u-operator ayixhasa futhi ayikhiye isikhathi esicacisiwe. izibophezelo ze-ledger zilinganiselwa kabili kwe-collateral encane kunazo zonke yokukhi egcinwe yinoma yiliphi ilunga, futhi isikhathi se-quorum silinganiselwa esikhathini esifinqiwe sokukhiya. lokhu kuqinisekisa ukuthi inethiwekhi ye-collateral ihlala inesekelo elanele ukugquma ukudluliswa kokulondoloza. i-deposit ye-collateral efanayo ingasekela ama-ledger amaningi ukuze ithuthukise ukusebenza kahle kwemali, nakuba ama-wallet kufanele akhethe ama-operator anemithombo ye-collateral engahlanganisi

izibophezelo ziphoqelwa lapho kudala iziphakamiso zokuxhasa noma ama-invoice amasha. u-operator akakwazi ukudala iziphakamiso noma ama-invoice angadudula izibophezelo ze-ledger ngaphezu kwezimali ezigciniwe noma ngaphezu kabili kwe-collateral encane kunazo zonke, noma yikuphi okuncane

## quorum

ama-operator acela amanye ama-operator ukujoyina i-quorum yawo ngokufaka nokukhiya i-collateral ku-ledger lelunga. isicelo siqukethe isibophezelo se-collateral (inani nesikhathi sokukhiya) nemibandela yelunga: izisekelo ezincane zezindleko ama-deposit ku-ledger okumele azihlangabeze. ilunga ngalinye kumele lisebenzise i-ledger lalo futhi lingathatha i-collateral ye-operator uma u-operator ebonakala engahambisani. amalunga achibiyela imingcele yezindleko ngesikhathi sobulunga bawo be-quorum -- u-operator akakwazi ukuvula ama-deposit anezindleko ezingaphansi kwezincane kunazo zonke zelunga elingqongqo, ukuvikela amalunga ekuthwaleni izibophezelo ezingenanzuzo emva kokudluliswa kokulondoloza

lapho i-quorum isimisiwe, izimali ezigciniwe zishintshelwa ku-multisig UTXO entsha. amalunga asayina ngokubambisana izibuyekezo ezisemthethweni futhi ahlanganyele ekubuyisweni uma u-operator esayina ezingahambisani. ama-quorum amakhudlwana andisa umthwalo wokuxhumana kodwa anciphisa ubungozi be-operator, andisa ukutholakala, futhi enza ukubambisana ngokungekho emthethweni kube nzima futhi kubize kakhulu. ama-wallet kufanele akhethe ama-quorum amakhulu

## ukuvimbela ngezomnotho

iprothokholi ithathelwa indawo ukuphuma ngasohlangothini olulodwa ngokuvimbela ngezomnotho. amalunga e-quorum agqugquzelwa ngqo ukusebenza ngokuphambene nokungathembeki. ngesikhathi semisebenzi evamile athola izindleko ezincane ku-collateral, kodwa uma kunokuziphatha okungahambisani okufakazelekayo angathatha i-collateral ye-operator yonke ku-ledger lawo

lapho i-wallet isola ukuvinjelwa, ingandisa isicelo kumalunga e-quorum ngokuthunyelwa okuqinisekisiwe. ilunga lifaka i-hash yesicelo ku-ledger lalo ngendleko encane, okudala ubufakazi obuxhumeke ngesizathu. uma u-operator engawuphathi umsebenzi, ilunga linobufakazi nesizathu sezomnotho sokuqala impikiswano

ukukhwabanisa kwe-invoice ye-lightning kulandela iphethini efanayo yokuvimbela. u-operator uyazi ukuthi i-preimage yamukelwe yini, kodwa i-wallet ayikwazi. nokho noma yimuphi umkhokhi angahlinzeka nge-preimage ku-wallet. ukweba okukodwa okuqinisekisiwe kuqala impikiswano, ukuthathwa kwezimali ezigciniwe, nokuthathwa kwe-collateral. umvuzo wokweba ukukhokha okukodwa umncane, kodwa ubungozi bukhona kakhulu, okwenza ukweba nge-lightning kungabi nengqondo ngezomnotho nakuba kungenakunqatshwa ngokusemthethweni ngaphandle kokubambisana komuntu wesithathu

indlela yokuhluleka kokubini ukuvinjelwa nokuvimbela nge-lightning yikubambisana kwe-quorum yonke. iprothokholi ayikwazi ukuvikela uma i-quorum ibambisana ukweba, kodwa inethiwekhi ye-collateral iqinisekisa ukuthi ukubambisana kubiza ngaphezu kwalokho okuzuzwayo. ukusobala kwenethiwekhi kuvumela ama-wallet nezimakethe zokuthola ukubona izakhiwo ze-quorum ezisola ngaphambi kokufaka imali

## isikhathi

isikhathi esiphelele silinganiswa ngesendlalelo sesiseko. ukubekezelelwa akukwazi ukudlula inani elifanelekile leziqinisekiso ukuze kugcinwe ukuzinza ngesikhathi sokuhlelwa kabusha kwechungechunge

lapho ukubekezelelwa okungaphezulu kudingeka sithembela ekuhlelweni ngesizathu. i-ledger ye-cryptographic iwuchungechunge lwe-merkle. isibuyekezo ngasinye sifakazela ukuthi senziwa emva kwazo zonke izibuyekezo ezingaphambi kwaso, kodwa asinikezi iziqiniseko ngolwazi olungaphandle kwechungechunge. ukwakha ukuhlela okusakazekile, sidinga ukuthi ukusayina ngokubambisana kuhlanganise i-hash yesibuyekezo sakamuva ye-ledger yomsayini. leyo hash bese ifakwa ku-hash yesibuyekezo samanje, iba yingxenye yechungechunge kanye neyazo zonke ezinye izingxenye zechungechunge u-operator we-ledger azisayinela ngokubambisana, okudala inethiwekhi yezizathu. lokhu akukwazi ukufakazela isikhathi ngokusobala, kodwa kuyakwazi ukufakazela ukuthi izingxenye ezithile zolwazi zenziwe ngokulandelana okuthile

## ubufakazi bobugebengu

singafakazela izinhlobo ezihlukene zobugebengu ngokuveza ulwazi olwenziwe ngokulandelana okungalungile. lapho ulwazi lungafakiwe yimisebenzi evamile yenethiwekhi, lungafakwa ngokufihlekile ngokudala umsebenzi oqukethe i-hash yobufakazi. lapho isifakiwe esibuyekweni esisayinwe ngu-operator, ubufakazi buyembulwa njengobwenziwe endaweni engahambisani ekuhleleni:

- u-operator, esithembise ukukhredithi i-deposit ngemali ethunyelwe kwe-on-chain ekheli elithile, usayina isibuyekezo se-ledger esingaqukethi ikhredithi efanelekile, kodwa siqukethe uchungechunge oluveza i-hash yebhlokhi edlula inani leziqinisekiso ezivunyelwe ngaphambi kwekhredithi

- u-operator, esedale i-invoice ye-lightning egameni le-deposit, usayina isibuyekezo se-ledger esingakakhredithi i-deposit nakuba i-preimage yembuliwe echungechungeni

- ukusayina ngokubambisana okumemezela i-hash yamanje ye-ledger ukuthi iyileyo edlulwa yi-hash yabo yakamuva echungechungeni

- ilunga le-quorum le-ledger eliphikiswayo elalisekhona kodwa alizange lenze ngokuvumelana nobufakazi bobugebengu ngaphakathi kwenani lamablokhi

- ukusayina noma ukusayina ngokubambisana izibuyekezo ze-ledger ezingahambisani

ubufakazi bobugebengu buqukethe ubufakazi nochungechunge lwezizathu oluxhuma i-hash efakiwe ku-ledger ye-operator omangalelwayo. uchungechunge luwuchungechunge lwezibuyekezo ezisayinwe ngokubambisana, ngasinye siqukethe i-member_ledger_hash kusuka kwisixhumanisi sangaphambilini se-ledger. abaqinisekisi bahamba uchungechunge ngaphandle kokucinga, beqinisekisa isixhumanisi ngasinye ukuthi siyisibuyekezo esisayiniwe, nokuthi i-hash yobufakazi ihambisana nedatha efakiwe

## ukubuyisela

lapho i-ledger lingasatholakali noma lingahambisani, amalunga e-quorum angadala ukuqhubeka kwawo ku-ledger kusukela esibuyekweni sokugcina esihambisanayo. kumele amise i-quorum entsha futhi anikeze ubufakazi be-collateral. amalunga kumele ahlanganise ukuchitha izimali ezigciniwe zangaphambilini kuya kukhethwa kwamachungechunge angalandela. umnqobi walokhu kukhetha unezela isibuyekezo sokuthola echungechungeni lakhe, abanye bonezele isibuyekezo sokuguquka. ama-wallet aqhubeka ekhuluma ne-ledger elifanayo, amukela izimpendulo ezisayinwe ngokubambisana yi-quorum kuphela. ngezikhathi ezithile, nalapho izimpendulo zingasayinwanga ngokubambisana okulindelwe, i-wallet kufanele ibuze inethiwekhi futhi idlale kabusha izibuyekezo zama-ledger ukuze ibone izinguquko zokulondoloza

lapho ukungahambisani kubonakala kungokungaqondile (isib., i-ledger alitholakali inani elithile lamablokhi) ukuguqulwa kokulondoloza kumele kuhloniphe: kuphela inani lezimali ezigciniwe elidingekayo ukugquma izibophezelo ze-ledger lithunyelwa kukhethwa, noshintsho lubuyiselwa ku-pubkey ye-operator. ukulawula kwe-collateral akuthinteki

lapho ubufakazi bokungahambisani bukhona, inani elingaphezu kwezimali ezigciniwe ezidingekayo lehlukaniswa ngokulinganayo phakathi kwamalunga e-quorum, ne-collateral egcinwe kuma-ledger amalunga ivunyelwe ukuthathwa

## impilo yenethiwekhi

ukuhlasela okulula okukodwa wukwakha iziqhingi zama-operator abambisanayo. emva kokwakha izibophezelo ezinkulu kuma-ledger abo, ahlanganisa ukuphuma, eba imali edlula i-collateral elahlekile. inethiwekhi ingazivikela kulokhu, ngaphandle kwezindawo lapho inani langaphakathi lidlula i-collateral elixhuma inethiwekhi engabambisani. izilinganiso eziphezulu ze-collateral nama-quorum amakhudlwana ahlukahlukene zinciphisa amathuba okuthi lezizikhala zakheke, kodwa zingakheka ngamabomu futhi asinakukwazi ukulindela wonke ama-wallet ukuthi ahlole inethiwekhi yonke. esikhundleni salokho izimakethe zokuthola kufanele zishicilele amamethrikhi okuziphendulela kwe-operator ngokusekelwe ekuhlaziyeni kwamagraph njengama-algoritimu ze-prize-collecting

## isiphetho

siphakamisa inethiwekhi ye-collateral edinga ukubambisana ukweba, kodwa ukubambisana kwandisa i-collateral esengozini ngokushesha kunokukhulisa inani elingantshontshwa. sisebenzisa le nethiwekhi ukuvikelela ama-ledger e-cryptographic asekelwe yizimali ezigciniwe eziphelele. la ma-ledger asebenzela ama-akhawunti egameni lama-wallet angekho ku-inthanethi ngokushintshanisa ngezindleko ezixoxiswane ngaphambilini. izinto eziyisisekelo ze-ledger zisekela imibandela yokusetshenziswa ye-miniscript eyanele yezinkontileka ezilula ze-smart. inethiwekhi ikhula cishe ngokufanayo, okuvumela inethiwekhi enkulu ukuhlinzeka izigidigidi zama-wallet nomthamo wemisebenzi odlula izinethiwekhi zokukhokha ezivamile
