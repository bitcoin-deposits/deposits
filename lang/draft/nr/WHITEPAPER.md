# bitcoin deposits
## isifinyezo

inguqulo epheleleko yemali ye-elekthronikhi ephakathi kwabantu ngqo ingavumela iimali ezikhokhwa ku-inthanethi ukuthi zithunyelwe ngqo komunye umuntu ziye komunye ngokurhaba nangokukulungiselelwa okuncani. i-lightning network iletha ingcenye yesisombhululo, kodwana iinzuzo eziqakathekileko zilahleka nange kutlhogeka umuntu wesithathu othembekileko bona aphathe ubujamo egameni lakho. siphakamisa isisombhululo sale nraro ngokusebenzisa ama-ledger aqinisekiswako nesisa se-collateral. ama-operator arhayila iimbuyekezo zama-ledger eenlenzini zabo, bakha irekhodi elilinganiswako lamaakhawunti. ama-wallet arhayila ubufakazi bokungathembeki eenlenzini lezo, eziqinisekisa bona i-ledger ihlala ine-operator othembekileko. ukuphuma kwedwa kuthathelwa yisiqinisekiso sokobana iimali ihlala itholakala ngaso soke isikhathi i-nethiwekhi ikhona. sifika ku-nethiwekhi edlulisela ukulondolozwa kokutheleleka kwemali, igegede iimali zokwakhiwa, ikghona ukwamukela iimali nayingekho ku-inthanethi, begodu ikhula ngokuzimela esigabeni sesisekelo

## isingeniso

i-bitcoin deposits ihlose ukuletha iimali ezirhabileko nezikhulako ezilawulwa ngamakhiye, ngaphandle kokuthemba, ngaphandle kwetjheyini. umsebenzi wetjheyini ukhula nenomboro yama-ledger kanye nokujikelelana kokutjhintjha kwama-reserve. ukudluliswa kukhula ngaphezudlwana kokuhambisana nenomboro yama-ledger ku-nethiwekhi, okwenza iingidi zeensetjenziswa ngomzuzwana hlangana neenkulungwane zama-wallet kube ngokunokwenzeka

kunokutjhintjhana okusobala:
- akukho ukuphuma kwedwa: nama-operator abhalelwa iimali zihlala ku-nethiwekhi
- akukho imfihlo: ukuqinisekiswa kutlhoga ukuba sobala
- ukutholakala okuphazanyiswako: i-deposit itholakala ngange-operator kuphela. ama-wallet kufanele asabalalise iimali ukwandisa ukutholakala

silindele bona isipiliyoni sama-wallet sizokufana nesigaba sesisekelo esirhabileko, sinomnotho wokukhokha ofana ne-lightning network

## ama-ledger

i-ledger sitjheyini esingaguqulekiko seembuyekezo, esiqukethe i-hash yembuyekezo yangaphambilini begodu sisakiwe ngu-operator we-ledger. iintlobo ezihlukahlukeneko zeembuyekezo zinemithetho ehlukahlukeneko elawula bona zingasetjenziswa nini nokobana njani. ama-ledger ayazichaza, iimbuyekezo zawo zitholakala tjhatjhalazi begodu azikghoni ukuphikiswa, okuvumela nanyana ngubani bona ahlole ukulandela

ama-ledger ane-operator munye osebenzako, kodwana alondolozwa ngokuhlanganyela yi-mesh. nanyana ngimuphi u-operator angakha eyodwa, kodwana nange anyamalala namkha angathembeki omunye u-operator uzokukhetha, kanye nama-reserve. u-operator osebenzako njengamanje ubonakala nge-pubkey ebesetjenziselwa ukusakha imbuyekezo yakamuva esakwe ngokuhlanganyela

## ama-deposit

i-deposit liakhawunti elizinzileko elingathunyelwa nelingamukelwa iimali, lilawulwa nge-miniscript. ngesikhathi lokuvulwa kubekwa isheduli yemali, kanye nokobana ukwamukela iimali kudinga isicelo esisakiwe yi-wallet na. u-operator kufanele avumele ukudluliselana phakathi kwama-deposit ku-ledger efanako kanye nokuphuma kwetjheyini. kufanele bavumele ama-deposit ukukhokha ama-invoice we-lightning

kusesikhethweni se-operator ukwakha iziphakamiso zokuxhasa kwetjheyini namkha ama-invoice we-lightning egameni le-deposit. nange bakwenza, kufanele kusakwe lilungu le-quorum, begodu i-wallet kufanele iqinisekise ukusakwa lokhu. iziphakamiso nama-invoice azisingcenye ye-ledger, ngalokho kusibopho se-wallet ukuqinisekisa amasakha nokuwalondoloza njengobufakazi

## iimali

ukudluliselana phakathi kwama-deposit, kwetjheyini, nange-lightning kunezimali ezikhokhwa ku-operator we-ledger. kukhona nezimali ezifakwa ngeenkhathi ezibekiweko eenbalansi. zoke zizanyelanwa ngesikhathi kuvulwa i-deposit elitjha. iimali zingabuye zitjhintjhwe ngemva kwenomboro yeenblokhi ebekiweko, ngesikhathi sokutshelwa ebekiweko nangehlelwana yokutjhintjha ezanyelanwe ngesikhathi sokuvulwa. i-quorum ingala ukusakha iimbuyekezo ezakha izimo ezingakhiphi inzuzo abangagcina baphendulelwa zona

## ukudluliselana

uhlobo oluyisisekelo lokudluliselana kusebenza ngezigaba ezimbili phakathi kwama-deposit amabili ku-ledger efanako: i-deposit likhipha isicelo sokuthumela iimali. nange kunezimali ezaneleko, ukuvaliwa kweemali ngombandela wokusebenzisa kwengezwa ku-ledger. nange umbandela wokusebenzisa ugcwaliswa ngaphambi kwesikhathi, iimali zisuka kumthumeli ziya kumamukeli ngaphandle kwemali ye-operator. nange isikhathi sifikiwe, ukuvaliwa kukhululwa ngaphandle kwemali encani ye-operator. ngemibandela yokusebenzisa ye-miniscript, lokhu kwanele ukuvumela nanyana nguliphi i-deposit ukunikela amabhriji neenkonzo zokutheleleka kwemali kwamanye ama-deposit ku-ledger efanako

## lightning

ama-operator anenxenye ye-lightning angavumela ama-deposit ukuthumela nokwamukela nge-lightning network. nange i-deposit licela i-invoice ye-lightning, u-operator uyayakha nge-node yakhe ye-lightning, acele amalungu e-quorum bona asakhe ukuze babonise bona bazibophelele ekulifakeni i-deposit ekukhokhweni. i-wallet kufanele igcine le-invoice esakiweko njengobufakazi. nange i-deposit licela ukukhokha i-invoice ye-lightning, u-operator ukhokha nge-node yakhe ye-lightning abuye athathele i-deposit ngemva kokuthola i-preimage

nange umkhokheli nomamukeli bangama-deposit ku-operator ofanako, u-operator angahlela ngaphakathi ngaphandle kokukhamba nge-lightning, afake abuye athathele ama-deposit ngqo. lokhu kugegeda iimali zokukhamba nobujamo bokubhalelwa kukulondoloza iimfanelo zokubalwa ezifanako

## ama-courier

izicelo zokudluliselana zidlulisa iimali phakathi kwama-deposit ku-ledger efanako kwaphela. ukudlulisa iimali hlangana nama-ledger, ama-wallet asebenzisa ama-courier — iinkonzo eziphethe ama-deposit eema-ledger ezinengi ezidlulisa ukudluliselana phakathi kwazo. i-courier ikhangisa umthamo neemali ngomkhombandlela nge-ledger ku-relay. nange i-wallet ifuna ukuthumela ukusuka ku-ledger A ukuya ku-ledger B, yakha ukuvaliwa kokudlulisela ku-deposit le-courier bese icela bona i-courier yakhe okukodwa esuka ku-deposit layo ku-ledger lapho kuyiwa khona kumamukeli. nange zombili izivaliwo zibekiwe, i-wallet yembula i-preimage kumamukeli, ogcwalisa ukudluliselana okuvela ku-courier. nase kwembuliwe, i-courier isebenzisa i-preimage efanako ukugcwalisa ukudluliselana okuvela kumthumeli okuyela ku-courier

lokhu kumhlobo ovamileko we-hash time-locked contract. silindele bona isikhathi sokuphela se-courier sokuthumela sibe ngaphambi kwesokwamukela, ukuqinisekisa bona nange i-wallet ingembuli, zombili izivaliwo ziphele begodu akakho olahlekelwako. akukho ukuthemba okutlhogekako ngaphandle kwesiqinisekiso sesikhathi esibekwe ngama-operator

ama-courier kufanele abeke iimali nge-ledger: fee_in ne-fee_out nge-ledger ngayinye eziyikonzelako. i-wallet ilinganisa iindleko zendlela njenge-fee_out emsongweni ne-fee_in endaweni okuyiwa kiyo. ama-courier angahluka ngeemali nge-ledger ngokuya ngokutheleleka kwemali okutholakalako, alungise ngokwemvelo iindawo zazo. ama-wallet athola ama-courier ngokusebenzisa izikhangiso zazo ku-relay begodu akhethe ngemali, umthamo, namkha ukumboza

## ukukhulumisana

koke ukukhulumisana phakathi kwama-wallet nama-operator, naphakathi kwama-operator, kusebenzisa ama-relay we-nostr. iimbuyekezo zama-ledger zikhutsazwa njengezehlakalo ezihlala zikhona ama-relay azigcinako, zakhe irekhodi eliphumelelako elilinganiswako. izicelo neemphendulo phakathi kwama-wallet nama-operator zezehlakalo ezidlulako ezi-TTL emfitjhane ye-relay. ama-operator akhangisa imibandela yabo njengezehlakalo ezitjhintjhwako, avumela ama-wallet ukuthola nokulinganisa ama-operator ngaphandle kwedayirekthri ephakathi

ukwakhiwa lokhu kutjho bona ama-wallet awatlhogi ukuhlala ahlangene — angaphuma ku-inthanethi isikhathi eside bese abuya ngokuphinda adlale izehlakalo avela kunoma yiliphi i-relay eliyiphethe. ama-operator angafinyelelwa nganoma yiliphi i-relay awalibhekako, begodu ukukhetha kwe-relay sinqumo sokwakhiwa, akunasikhawu seprothokholi

## ama-reserve ne-collateral

ama-reserve agcinwa ku-UTXO enobukhulu obulingana namkha obudlula isamba sezibopho ze-ledger, okusebenziseka ngabanengi be-quorum, nokubuyelwa ku-operator ngemva kwesikhathi eside

i-collateral yimali ye-operator mathupha, efakiwe nevaliwe eema-ledger zamalungu e-quorum. ilungu ngalinye liphethe i-deposit le-collateral u-operator alixhasako nalivalelako isikhathi esibekiweko. izibopho ze-ledger zilinganiswa ngokuphindwe kabili kwe-collateral encani evaliwe ephethwe yilungu elinye, nesikhathi se-quorum silinganiswa ngesikhathi esimfitjhane sokuvaliwa. lokhu kuqinisekisa bona isisa se-collateral sihlala sinokwaneleko ukubhadelela ukudluliselwa kwe-custody. i-deposit le-collateral elifanako lingasekela ama-ledger amanengi ukwandisa ukusebenza kwemali, nanoma ama-wallet kufanele akhethe ama-operator ane-collateral engahlangani

izibopho zigcinwa ngesikhathi kukhiwa iziphakamiso zokuxhasa namkha ama-invoice amatjha. u-operator angeze akha iziphakamiso namkha ama-invoice azokudlulisa izibopho ze-ledger ngaphezulu kwama-reserve namkha ngaphezulu kwe-collateral encani ephindwe kabili, nanyana ngokuphi okuncani

## i-quorum

ama-operator acela amanye ama-operator ukujoyina i-quorum yawo ngokufaka nokuvala i-collateral ku-ledger yelungu. isicelo siqukethe isibopho se-collateral (isilinganiso nesikhathi sokuvaliwa) nemibandela yelungu: imisedlana emincani yeemali ama-deposit ku-ledger akufanele ayihlangabeze. ilungu ngalinye kufanele lisebenzise i-ledger yalo begodu lingathatha i-collateral ye-operator nange u-operator abonakala angalandeli. amalungu abeka imikhawulo yemisedlana yeemali ngesikhathi sobulunga be-quorum — u-operator angeze avule ama-deposit aneemali ngaphasi kweezinga eliqinileko zelungu, ukuvikela amalungu ekufumaneni izibopho ezingakhiphi inzuzo ngemva kokudluliselwa kwe-custody

nase i-quorum isungulwe, ama-reserve atjhintjhwa ku-UTXO etjha ye-multisig. amalungu asakha iimbuyekezo ezilungileko begodu ahlanganyele ekuvuseleni nange u-operator asakha ezingalungi. i-quorum ekulu yandisa ukukhulumisana kodwana inciphisa ubungozi be-operator, yandisa ukutholakala, yenze ukuhlanganyela kube budisi nobubiza. ama-wallet kufanele akhethe i-quorum ekulu

## ukuvimbela ngomnotho

iprothokholi itjhintjha ukuphuma kwedwa ngokuvimbela ngomnotho. amalungu e-quorum akhuthazwa ngqo ukwenza ngokumelene nokungathembeki. emsebenzini ovamileko azuza iimali ezincani ku-collateral, kodwana ngesikhathi sokuziphatha okungalandeli okubonakalako angathatha yoke i-collateral ye-operator esigciniwe ku-ledger yabo

nange i-wallet isola ukuvinjelwa, ingadlulisa isicelo emalungwini e-quorum ngokuthunyelwa okuqinisekisiweko. ilungu lifaka i-hash yesicelo ku-ledger yalo ngemali encani, likhele ubufakazi obuhlala bukhona. nange u-operator abhalelwa ukusetjenza isicelo, ilungu linobufakazi nesizathu somnotho sokuqala ingxabano

inkohliso ye-invoice ye-lightning ilandela umhlobo ofanako wokuvimbela. u-operator uyazi bona i-preimage yamukelwe namkha awa, kodwana i-wallet ayazi. nanoma kunjalo nanyana ngimuphi umkhokheli angahlinzeka i-preimage ku-wallet. ukwebwa okukodwa okuqinisekisiweko kuqala ingxabano, ukuthathwa kwama-reserve, nokuthathwa kwe-collateral. umvuzo wokweba ukukhokha okukodwa ulinganisiwe, kodwana ubungozi buyingozi yokuphila, okwenza ukweba nge-lightning kungabi nomqondo ngomnotho nanoma kungabonakalisi ngaphandle kokusebenzisana komuntu wesithathu

indlela yokubhalelwa ngokuvinjelwa nange-lightning kukuhlanganyela kwe-quorum yoke. iprothokholi angeke ivikele i-quorum ehlanganyela ukweba, kodwana isisa se-collateral siqinisekisa bona ukuhlanganyela kubiza ngaphezu kwalokho okuzuzwayo. ukuba sobala kwe-nethiwekhi kuvumela ama-wallet nemimakethi yokufumanisa ukubona izindlela ze-quorum ezisolarisako ngaphambi kokufaka iimali

## isikhathi

isikhathi esingenayo silinganiselwa esigabeni sesisekelo. ukubekezelelwa akukghoni ukudlula inomboro efaneleko yokuqinisekiswa ukuze kuhlale kuzinzile ngesikhathi sokuhlela kutjha kwetjheyini

lapha ukubekezelelwa okuphezulu kutlhogekako sithembela ekuhlwayeni ngobangela. i-ledger ye-khripthogrifi itjheyini ye-merkle. imbuyekezo ngayinye ibonisa bona yakhiwe ngemva kwazo zoke iimbuyekezo ezangaphambi kwayo, kodwana ayinikezi iziqinisekiso ngolwazi ngaphandle kwetjheyini. ukwakha ukuhlwaya okusakazekako, sitlhoga bona ukusakwa okuhlanganyeleyo kuqukethe i-hash yembuyekezo yakamuva evela ku-ledger yomsakhi. leyo i-hash ifakwa ku-hash yembuyekezo yamanje, ibe yingcenye yetjheyini kanye nengcenye yazo zoke ezinye iintjheyini u-operator we-ledger asakha ngazo, kwakhiwe isisa sobangela. lokhu akukghoni ukubonisa isikhathi ngokusobala, kodwana kukghona ukubonisa bona iingcenye ezithile zelwazi zakhiwe ngehlelo ethile

## ubufakazi benkohliso

singabonisa iintlobo ezihlukahlukeneko zenkohliso ngokuveza ulwazi olwakhiwe ngehlelo engakalungi. lapha ulwazi lungafakwa misebenzi evamileko ye-nethiwekhi, lungafunjathiswa ngokwakha umsebenzi oqukethe i-hash yobufakazi. nase ufakwe embuyekisweni esakiwe ngu-operator, ubufakazi buvezwa njengobe bakhiwe endaweni engalandeli ehlwayeni:

- u-operator, ngemva kokuphakamisa ukufaka i-deposit ngeemali ezithunyelwe kwetjheyini ekheyini ethile, usakha imbuyekezo ye-ledger engaqukethi ukufakwa okufaneleko, kodwana equkethe itjheyini eveza i-hash yeblokhi edlula inomboro yokuqinisekiswa evunyelwe ngaphambi kokufakwa

- u-operator, ngemva kokwakha i-invoice ye-lightning egameni le-deposit, usakha imbuyekezo ye-ledger engakafaki i-deposit nanoma i-preimage ivezwe etjheyinini

- ukusakha okuhlanganyeleyo okutjho bona i-hash yamanje ye-ledger yilelo elingaphambi kwe-hash yabo yakamuva etjheyinini

- ilungu le-quorum le-ledger ephikiswako ebelisebenza kodwana alizange lenze ngokuya nobufakazi benkohliso phakathi kwenomboro yeenblokhi

- ukusakha namkha ukuhlanganyela ukusakha iimbuyekezo zama-ledger ezingalandeli

ubufakazi benkohliso buqukethe ubufakazi netjheyini yobangela ehlanganisa i-hash efakiweko ku-ledger yomsolwa. itjheyini ngumlandelano weembuyekezo ezasakwa ngokuhlanganyela, ngayinye iqukethe member_ledger_hash evela ku-ledger yesihlanganiso sangaphambilini. abahloli bakhamba etjheyinini ngaphandle kokusesela, baqinisekise isihlanganiso ngasinye simbuyekezo esakiweko, nokobana i-hash yobufakazi ihlangana nolwazi olufakiweko

## ukuvuselela

nase i-ledger ingasatholakali namkha ingasalandeli, amalungu e-quorum angakha ukuragela phambili kwe-ledger ukusuka embuyekisweni yokugcina elandelako. kufanele asungule i-quorum etjha anikele ubufakazi be-collateral. amalungu kufanele asebenzisane ukusebenzisa okukhiphwe ngaphambilini kwama-reserve ukuya kulothari yeentjheyini ezingaba ngezalandelako. owina le lothari ufaka imbuyekezo yokuthola etjheyinini yabo, nabanye bafake ukudedela. ama-wallet aragela phambili akhuluma ne-ledger efanako, amukele iimphendulo ezisakiwe yi-quorum kwaphela. ngezikhathi, nanange iimphendulo zingenaso isiqinisekiso esilindelweko, i-wallet kufanele ibuze i-nethiwekhi iphinde idlale iimbuyekezo ze-ledger ukubona izinguquko ku-custody

nange ukungalandeli kubonakala kwenzeka ngephutha (isib., i-ledger ingasatholakali iinblokhi ezithile) ukutjhintjha ku-custody kufanele kuhloniphe: yisilinganiso sama-reserve esitlhogekako ukumboza izibopho ze-ledger kuphela esithunyelwa elotharini, nokutjhintjha okubuyiselwa ku-pubkey ye-operator. ukulawula kwe-collateral akuthinteki

nange ubufakazi bokungalandeli bukhona, isilinganiso esingaphezulu kwama-reserve etlhogekako sabiwa ngokulinganako phakathi kwamalungu e-quorum, ne-collateral esiphethwe eema-ledger zamalungu sivunyelwe ukuthathwa

## ipilo ye-nethiwekhi

ukuhlasela okulula kukwakha iinhlangothi zama-operator ahlanganyela. ngemva kokwakha izibopho ezinkulu hlangana nama-ledger abo, bahlela ukuphuma, bebe iimali ezidlula i-collateral esilahlekileko. i-nethiwekhi ingavikela lokhu, ngaphandle kwezindawo lapha ilinani langaphakathi lidlula i-collateral ehlanganisa ne-nethiwekhi engahlanganyeli. ama-ratio we-collateral aphezulu nama-quorum amakhulu ahlukahlukeneko anciphisa amathuba wokobana lezi zindawo zakheke, kodwana zingakhiwa ngamabomu begodu asingalindeli bona yoke i-wallet ihlole yoke i-nethiwekhi. esikhundleni salokho imimakethi yokufumanisa kufanele ikhutsaze iimetrikhi zokuphendulelwa kwama-operator ngokohlaziywa kwegrafu njenge-algorithmu yokubhidliza

## isiphetho

siphakamisa i-nethiwekhi ye-collateral etlhoga ukuhlanganyela ukweba, kodwana ukuhlanganyela kwandisa i-collateral ebungozini ngokurhaba kunokulinani okuzokwebwa. sisebenzisa le nethiwekhi ukuvikela ama-ledger e-khripthogrifi anama-reserve agcweleko. lawa ama-ledger akonzela amaakhawunti egameni lama-wallet angekho ku-inthanethi ngokukhokha iimali ezizanyelanwe ngaphambilini. izinto eziyisisekelo zama-ledger zisekela imibandela yokusebenzisa ye-miniscript eyaneleko yamakontraga avamileko. i-nethiwekhi ikhula ngokulingana, ivumela i-nethiwekhi ekulu ukunikela iimbiliyoni zama-wallet nomthamo weensetjenziswa odlula iinthiwekhi zokukhokha ezijayelekileko
