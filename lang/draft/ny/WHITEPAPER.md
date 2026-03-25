# bitcoin deposits
## chidule

njira yabwino kwambiri yopereka ndalama zamagetsi pakati pa anthu awiri mwachindunji ikanatha kulola kuti malipiro a pa intaneti atumizidwe kuchokera kwa munthu wina kupita kwa wina mwachangu ndiponso popanda kukonzekera kwambiri. netiweki ya lightning imapereka gawo la yankho, koma phindu lake lalikulu limasowa ngati munthu wachitatu wodalirika akufunikira kusamalira zinthu m'malo mwanu. tikupereka yankho la vuto ili pogwiritsa ntchito ma ledger otsimikizika ndi ukonde wa collateral. ma operator amafalitsa zosintha za ledger kwa anzawo, kupanga mbiri yowunikidwa ya ma akaunti. ma wallet amafalitsa umboni wa chinyengo kwa anzawo amenewo, omwe amaonetsetsa kuti ledger isunga operator wowona mtima. kutuluka kwakumodzi kumalowidwa ndi chitsimikizo choti ndalama zimapezeka nthawi yonse pomwe netiweki ikugwira ntchito. timafika pa netiweki yomwe imapereka udindo wosamala thanzi la ndalama kwa ena, yopewa mtengo woyambira, yokwanitsa kulandira malipiro opanda kukhala pa intaneti, ndiponso yokulira mwayekha mosadalira gawo loyambira

## mawu oyamba

bitcoin deposits cholinga chake ndi kupereka ndalama zothamanga ndi zokuliranso zolawulidwa ndi makiyi, mosadalira wina, kunja kwa tcheini. ntchito za pa tcheini zimakula molingana ndi kuchuluka kwa ma ledger ndi kuchuluka kwa kusinthidwa kwa reserves. kuchuluka kwa ntchito kumakula pang'onopang'ono kuposa mowongoka molingana ndi kuchuluka kwa ma ledger mu netiweki, zomwe zimapangitsa kuti mamiliyoni a ntchito pa sekondi kudzera mu ma wallet a tiriliyoni zikhale zotheka

pali kusinthana momveka bwino:
- kulibe kutuluka kwakumodzi: pamene ma operator alephera ndalama zimakhala mu netiweki
- kulibe chinsinsi: kutsimikizira kumafuna kuwonekera
- kupezeka kwa nthawi zonse ayi: deposit imapezeka pokhapokha ngati operator amapezeka. ma wallet ayenera kufalitsa ndalama zawo kuti awonjezere kupezeka

tikuyembekeza kuti ntchito ya wallet idzakhale yofanana ndi gawo loyambira lothamanga, yokhala ndi chikhalidwe cha malipiro chofanana ndi netiweki ya lightning

## ma ledger

ledger ndi mndandanda wosasinthika wa zosintha, zomwe zili ndi hash ya zosintha zapitazo ndipo zasainidwa ndi operator wa ledger. mitundu yosiyana ya zosintha ili ndi malamulo osiyana olamulira nthawi ndi momwe angagwiritsidwe ntchito. ma ledger amadzifotokozera okha, zosintha zawo zikupezeka kwa aliyense ndipo sizitha kukanidwa, zomwe zimalola aliyense kuwunika kugwirizana ndi malamulo

ma ledger ali ndi operator mmodzi wogwira ntchito, koma amasamalidwa mogwirizana ndi ukonde wonse. operator aliyense akhoza kupanga imodzi, koma akachoka kapena kukhala wosakhulupirika operator wina adzapatsidwa, pamodzi ndi reserves. operator wogwira ntchito panopa amadziwika ndi pubkey yomwe inagwiritsidwa ntchito kusaina zosintha zomaliza zosainidwa pamodzi

## ma deposit

deposit ndi akaunti yokhazikika yomwe ingatumize ndi kulandira ndalama, yolawulidwa ndi miniscript. poyamba, mndandanda wa mitengo umakhazikitsidwa, komanso ngati kulandira ndalama kumafuna pempho losainidwa ndi wallet kapena ayi. operator ayenera kulola kusamutsa pakati pa ma deposit pa ledger imodzi komanso kutuluka pa tcheini. ayenera kulola ma deposit kulipira ma invoice a lightning

ndi chisankho cha operator kupanga zopereka za ndalama pa tcheini kapena ma invoice a lightning m'malo mwa deposit. akatero, izi ziyenera kusainidwa pamodzi ndi membala wa quorum, ndipo wallet iyenera kutsimikizira sainiya. zopereka ndi ma invoice si gawo la ledger, choncho ndi udindo wa wallet kutsimikizira masainiya ndi kuwasunga ngati umboni

## mitengo

kusamutsa pakati pa ma deposit, pa tcheini, ndi kudzera pa lightning kumakhala ndi mitengo yolipidwa kwa operator wa ledger. palinso mitengo yomwe imagwiritsidwa ntchito pa ndalama nthawi ndi nthawi pa nthawi yotchulidwa. zonse zimayankhulana pamene deposit yatsopano ikutsegulidwa. mitengo ingathe kusinthidwa pambuyo pa chiwerengero cha ma block chotchulidwa, popatsidwa chidziwitso cha ma block chotchulidwa ndiponso mkati mwa malire a peresenti pa kukonza kulikonse omwe anayankhulana poyamba. quorum ingathe kukana kusaina pamodzi zosintha zomwe zimapanga mikhalidwe yosapindulitsa yomwe ikhoza kudzakhala udindo wawo pomaliza

## kusamutsa

mtundu woyambira wa kusamutsa ndi ntchito ya magawo awiri pakati pa ma deposit awiri pa ledger imodzi: deposit imatumiza pempho lotumiza ndalama. ngati pali ndalama zokwanira, chotseka pa ndalama chokhala ndi chikhalidwe chogwiritsira ntchito chimaphatikizidwa ku ledger. ngati chikhalidwe chogwiritsira ntchito chakwaniritsidwa nthawi isanakwane, ndalama zimasamuka kuchoka kwa wotumiza kupita kwa wolandira kupatulapo mtengo wa operator. ngati nthawi yakwana, chotseka chimamasulidwa, kupatulapo mtengo wochepa wa operator. ndi mikhalidwe yogwiritsira ntchito ya miniscript, izi zimakwanira kulola deposit iliyonse kupereka mathandizo a mabwalo ndi ndalama kwa ma deposit ena pa ledger imodzi

## lightning

ma operator okhala ndi njira ya lightning angathe kulola ma deposit kutumiza ndi kulandira kudzera pa netiweki ya lightning. pamene deposit imapempha invoice ya lightning, operator amapanga imodzi kudzera pa node yawo ya lightning, amapempha mamembala a quorum kusaina pamodzi kuti atsimikizire kuti ali okonzeka kulemba ndalama ku deposit pakulipira. wallet iyenera kusunga invoice yosainidwa pamodzi ngati umboni. pamene deposit imapempha kulipira invoice ya lightning, operator amalipira pogwiritsa ntchito node yawo ya lightning ndipo amachotsa ndalama ku deposit atalandira preimage

pamene wolipira ndi wolandira onse ndi ma deposit pa operator yemweyo, operator angathe kumaliza mkati mosadutsa kudzera pa lightning, kulemba ndi kuchotsa ndalama ku ma deposit okhudzidwa mwachindunji. izi zimapewa mitengo yodutsa ndi mavuto ena pomwe zitsimikizo za akaunti zimasunga chimodzimodzi

## ma courier

mapempho okusamutsa amasamutsa ndalama pakati pa ma deposit pa ledger imodzi yokha. kusamutsa ndalama kudutsa ma ledger osiyanasiyana, ma wallet amagwiritsa ntchito ma courier — ntchito zomwe zimakhala ndi ma deposit pa ma ledger ambiri ndipo zimanyamula kusamutsa pakati pawo. courier amalengeza kuchuluka kwake ndi mitengo ya njira iliyonse pa ledger iliyonse pa relay. pamene wallet ikufuna kutumiza kuchokera pa ledger A kupita pa ledger B, imapanga chotseka chosamutsa ku deposit ya courier ndi kupempha kuti courier apange chimodzi kuchokera ku deposit yawo pa ledger yolandira kupita kwa wolandira. zotseka zonse zitakhazikitsidwa, wallet imaonetsera preimage kwa wolandira, amene amatsiriza kusamutsa kuchokera kwa courier. itaonetseredwa, courier amagwiritsa ntchito preimage yomweyo kutsiriza kusamutsa kuchokera kwa wotumiza kupita kwa courier

uwu ndi machitidwe wamba a hash time-locked contract. tikuyembekeza kuti nthawi ya kutuluka ya courier idzakhale yoyamba kwambiri kuposa ya kulowa, kuonetsetsa kuti ngati wallet siinaonetsera, zotseka zonse zitha ndipo palibe amene amataya ndalama. palibe kudalirana komwe kumafunikira kupatula chitsimikizo cha nthawi chomwe chimatsatiridwa ndi ma operator

ma courier ayenera kukhazikitsa mitengo ya ledger iliyonse: fee_in ndi fee_out pa ledger iliyonse yomwe amatumikira. wallet imayerekezera mtengo wa njira ngati fee_out pa gwero kuwonjezera fee_in pa kumene kukupita. ma courier angathe kusintha mitengo malinga ndi ledger molingana ndi ndalama zopezeka, kulinganiza malo awo mwachibadwa. ma wallet amapeza ma courier kudzera mu malengeza awo pa relay ndipo amasankha molingana ndi mtengo, kuchuluka, kapena kukwirira

## kulankhulana

kulankhulana konse pakati pa ma wallet ndi ma operator, ndi pakati pa ma operator okhaokha, kumagwiritsa ntchito ma nostr relay. zosintha za ledger zimafalitsidwa ngati zochitika zokhazikika zomwe ma relay amasunga, kupanga mbiri yosatha yowunikidwa. mapempho ndi mayankho pakati pa ma wallet ndi ma operator ndi zochitika zamkanthawi zokhala ndi TTL yochepa pa relay. ma operator amalengeza ndondomeko zawo ngati zochitika zosinthika, zomwe zimalola ma wallet kupeza ndi kuyerekezera ma operator popanda buku lapakati

kapangidwe aka kumatanthauza kuti ma wallet safunika kulumikizana kosalekeza — angathe kusiya kukhala pa intaneti kwa nthawi iliyonse ndi kubwerera powerenga zochitika kuchokera pa relay iliyonse yomwe ili nazo. ma operator angathe kupezedwa kudzera pa relay iliyonse yomwe amayang'anira, ndipo kusankha kwa relay ndi chisankho cha kukhazikitsa, osati choletsa cha protocol

## reserves ndi collateral

reserves zimakhala mu UTXO yokhala ndi ndalama zofanana kapena zoposa chiwerengero cha zomwe ledger iyenera kukwaniritsa, zotheka kugwiritsidwa ntchito ndi unyinji wa quorum, yokhala ndi njira yotsatira ya operator pambuyo pa nthawi yayikulu

collateral ndi chuma cha operator mwini, chomwe chaikidwa ndi chotsekeredwa pa ma ledger a mamembala a quorum. membala aliyense amakhala ndi deposit ya collateral yomwe operator amapereka ndalama ndipo amaitsekera kwa nthawi yotchulidwa. zomwe ledger iyenera kukwaniritsa zimapimidwa pa kawiri ka collateral yochepa kwambiri ya membala aliyense, ndipo nthawi ya quorum imapimidwa pa nthawi yochepa kwambiri yotsekeredwa. izi zimaonetsetsa kuti ukonde wa collateral umakhala ndi chithandizo chokwanira kuti kusamutsidwe ulamuliro. deposit ya collateral imodzi ikhoza kuthandiza ma ledger ambiri kuti ndalama zigwiritsidwe ntchito bwino, ngakhale ma wallet ayenera kusankha ma operator okhala ndi magwero a collateral osaphatikizana

zomwe ayenera kukwaniritsa zimatsatiridwa popanga zopereka zatsopano kapena ma invoice. operator sangathe kupanga zopereka kapena ma invoice zomwe zingakankhire zomwe ledger iyenera kukwaniritsa kupitirira reserves kapena kupitirira kawiri ka collateral yochepa kwambiri yotsekeredwa, chilichonse chochepa kwambiri

## quorum

ma operator amapempha ma operator ena kulowa mu quorum yawo poika ndi kutsekera collateral pa ledger ya membala. pempholo limaphatikiza pangano la collateral (kuchuluka ndi nthawi yotsekeredwa) ndi ndondomeko za membala: mitengo yochepa kwambiri yomwe ma deposit pa ledger ayenera kukwaniritsa. membala aliyense ayenera kuyendetsa ledger yake ndipo angathe kulanda collateral ya operator ngati operator atsimikizidwa kuti sakutsata malamulo. mamembala amatchula malire a mitengo pa nthawi ya umembala wawo wa quorum — operator sangathe kutsegula ma deposit okhala ndi mitengo yotsika kuposa yochepa kwambiri ya membala wolimba kwambiri, kuteteza mamembala ku kulandira ntchito zosapindulitsa pambuyo pa kusamutsidwa ulamuliro

quorum itakhazikitsidwa, reserves zimasinthidwa kupita ku UTXO yatsopano ya multisig. mamembala amasaina pamodzi zosintha zolondola ndipo amathandiza kubwezeretsa ngati operator asaina zomwe sizitsatira malamulo. ma quorum aakulu amaonjezera ntchito yolumikizana koma amachepetsa chiopsezo cha operator, kuonjezera kupezeka, ndi kupangitsa kuti kugwirizana kuchinyengo kukhale kovuta ndi kodula kwambiri. ma wallet ayenera kusankha ma quorum aakulu

## kuletsa kwachuma

protocol imasinthira kutuluka kwakumodzi ndi kuletsa kwachuma. mamembala a quorum amalimbikitsidwa mwachindunji kuchita kanthu polimbana ndi chinyengo. pa ntchito zachibadwa amapeza mitengo yochepa pa collateral, koma pakakhala chikhalidwe chosatsatira malamulo chotsimikizika, amatha kulanda collateral yonse ya operator pa ledger yawo

pamene wallet ikusonyeza kutsekeredwa, ikhoza kukweza pempho kwa mamembala a quorum kudzera pa kutumiza kotsimikizidwa. membala amaika hash ya pempho mu ledger yawo pa mtengo wochepa, kupanga umboni wokhazikika pa chiyambi. ngati operator alephera kukonza pempholo, membala ali ndi umboni komanso chilimbikitso chachuma kuti ayambitse mkangano

chinyengo cha invoice ya lightning chimatsatira machitidwe omwewo a kuletsa. operator amadziwa ngati preimage yalandiridwa, koma wallet siikudziwa. komabe wolipira aliyense angathe kupereka preimage kwa wallet. kuberedwa kumodzi kotsimikizidwa kumayambitsa mkangano, kulanda reserves, ndi kulanda collateral. mphotho yakuba malipiro amodzi ndi yochepa, koma chiopsezo ndi chopha, zomwe zimapangitsa kuti kubera kwa lightning kukhale kopanda nzeru kwachuma ngakhale kuli kosatsimikizika mosavuta popanda kuthandizana ndi wachitatu

mkhalidwe wopasula wa kuletsa wa kutsekeredwa ndi wa lightning ndi kugwirizana kwa quorum yonse. protocol singathe kuteteza ku quorum yomwe imagwirizana kubera, koma ukonde wa collateral umaonetsetsa kuti kugwirizana kumadula kwambiri kuposa zomwe zimapezedwa. kuwonekera kwa netiweki kumalola ma wallet ndi misika yopeza kuzindikira mapangidwe a quorum okayikitsa asanayike ndalama

## nthawi

nthawi yeniyeni imayezedwa molingana ndi gawo loyambira. malire sangathe kupitirira chiwerengero choyenera cha zotsimikizira kuti zikhale zokhazikika pa nthawi ya kukonzanso kwa tcheini

pomwe malire aakulu akufunikira timagwiritsa ntchito kutsatizana kwa chiyambi. ledger ya cryptographic ndi tcheini ya merkle. zosintha zilizonse zimatsimikizira kuti zinapangidwa pambuyo pa zosintha zonse zapitazo, koma sizipereka chitsimikizo chilichonse pa zomwe zili kunja kwa tcheini. kuti tipange kutsatizana kofalitsidwa, timafuna kuti masainidwe opangidwa pamodzi aphatikize hash ya zosintha zaposachedwa za ledger ya wosainira. hash imeneyo imaphatikizidwa mu hash ya zosintha za panopo, kukhala gawo la tcheini imeneyo komanso gawo la matcheini ena onse omwe operator wa ledger amasainira, kupanga ukonde wa chiyambi. izi sizitha kutsimikizira nthawi momveka bwino, koma zimatha kutsimikizira kuti zidutswa zina za chidziwitso zinapangidwa mu dongosolo lotchulidwa

## umboni wachinyengo

tingathe kutsimikizira mitundu yosiyana ya chinyengo poonetsera chidziwitso chomwe chinapangidwa mu dongosolo lolakwika. pamene chidziwitso sichikuphatikizidwa ndi ntchito zachibadwa za netiweki, chikhoza kulowetsedwa mwamseri popanga ntchito yomwe imaphatikiza hash ya umboni. itaphatikizidwa mu zosintha zosainidwa ndi operator, umboni umadziwika kuti unapangidwa pa malo osatsatira malamulo mu dongosolo:

- operator, atapanga chopereka cholemba ndalama ku deposit pomwe ndalama zatumizidwa pa tcheini ku adiresi inayake, amasaina zosintha za ledger zomwe zilibe kulemba koyenera, koma zili ndi tcheini yoonetsera hash ya block yomwe yapitirira chiwerengero cha zotsimikizira zololedwa

- operator, atapanga invoice ya lightning m'malo mwa deposit, amasaina zosintha za ledger zomwe sizinalembe ndalama ku deposit ngakhale preimage itaonetseredwa mu tcheini

- kusainidwa pamodzi komwe kumatchula hash ya ledger yapanopo kukhala imodzi yomwe imatsogolera hash yawo yambuyo mu tcheini

- membala wa quorum wa ledger yokangana yomwe anali wogwira ntchito koma sanachite molingana ndi umboni wachinyengo mkati mwa chiwerengero chotchulidwa cha ma block

- kusaina kapena kusaina pamodzi zosintha za ledger zosatsatira malamulo

umboni wachinyengo umapangidwa ndi umboni weniweni ndi tcheini ya chiyambi yolumikiza hash yoyikidwa ku ledger ya operator woimbidwa mlandu. tcheiniyo ndi mndandanda wa zosintha zosainidwa pamodzi, chilichonse chophatikiza member_ledger_hash kuchokera pa ledger ya chunganizo chapitazo. owunika amayenda pa tcheini mosafunafuna, kutsimikizira kuti chunganizo chilichonse ndi zosintha zosainidwa, ndi kuti hash ya umboni ikugwirizana ndi deta yoyikidwa

## kubwezeretsa

ledger itakhala yosapezeka kapena yosatsatira malamulo, mamembala a quorum angathe kupanga kupitiriza kwawo kwa ledger kuchokera pa zosintha zomaliza zotsatira malamulo. ayenera kukhazikitsa quorum yatsopano ndi kupereka umboni wa collateral. mamembala ayenera kugwirizana kugwiritsa ntchito ndalama za reserves zapitazo kupita ku maere a matcheini omwe angathe kutsatira. wopambana wa maere amaphatikiza zosintha zolandira ku tcheini yawo, ndipo ena amaphatikiza zopereka. ma wallet amapitiriza kutumiza ku ledger yomweyo, kulandira mayankho okha omwe asainidwa pamodzi ndi quorum. nthawi ndi nthawi, ndiponso pamene mayankho alibe kusainidwa pamodzi koyembekezereka, wallet iyenera kufunsa netiweki ndi kuwerenga zosintha za ledger kuti idziwe kusintha kwa ulamuliro

pamene kusatsatira malamulo kumaoneka kwangozi (mwachitsanzo, ledger yakhala yosapezeka kwa chiwerengero chinazake cha ma block) kusintha kwa ulamuliro kuyenera kukhala kwa ulemu: ndalama za reserves zokwanira pokha kuphatikiza zomwe ledger iyenera kukwaniritsa zimatumizidwa ku maere, ndipo zotsala zimabwezeredwa ku pubkey ya operator. ulamuliro wa collateral suukhudzidwa

pamene umboni wosatsatira malamulo ulipo, ndalama zopitirira reserves zofunikira zimagawidwa mofanana pakati pa mamembala a quorum, ndipo collateral yomwe ili pa ma ledger a mamembala imalolezedwa kulandidwa

## thanzi la netiweki

nkhondo imodzi yosavuta ndi kupanga zilumba za ma operator ogwirizana. atamanga zomwe ayenera kukwaniritsa zambiri pa ma ledger awo, amagwirizana kutuluka, kubera ndalama zopitirira collateral yotayidwa. netiweki ingathe kudziteteza ku izi, kupatula m'malo omwe mtengo wamkati umapitirira collateral yolumikiza ku netiweki yosagwirizana. collateral yaikulu ndi ma quorum aakulu osiyanasiyana amachepetsa kuthekera kwake, koma zingathe kupangidwa dala ndipo sitiyenera kuyembekeza kuti wallet iliyonse iwunike netiweki yonse. m'malo mwake, misika yopeza iyenera kufalitsa miyezo ya kudzipereka kwa ma operator kutengera kusanthula kwa ma graph monga ma algorithm a prize-collecting

## mathero

tikupereka ukonde wa collateral womwe umafuna kugwirizana kuti kuberedwe, koma kugwirizana kumaonjezera collateral yoopsezedwa mofulumira kuposa momwe kumaonjezera mtengo woberedwa. timagwiritsa ntchito ukonde uwu kuteteza ma ledger a cryptographic othandizidwa ndi reserves zonse. ma ledger awa amatumikira ma akaunti m'malo mwa ma wallet osakhala pa intaneti posinthanitsa mitengo oyankhulana kale. zinthu zoyambira za ledger zimathandiza mikhalidwe yogwiritsira ntchito ya miniscript yokwanira kwa ma contract aung'ono. netiweki imakula pafupifupi mowongoka, zomwe zimalola netiweki yaikulu kupereka ma wallet abiliyoni ndi kuchuluka kwa malipiro kopitirira netiweki zachikhalidwe za malipiro
