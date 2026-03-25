# bitcoin deposits
## pfupiso

mhando yakakwana ye peer-to-peer yemari yepaindaneti inobvumira muripo wepamhepo kutumirwa kubva kune mumwe munhu kuenda kune mumwe nekukurumidza uye nokukanganisa kushoma. lightning network inopa chikamu chemhinduro, asi mibayiro yakakosha inorasika kana bato rechitatu rinovimbwa naro richidiwa kuti rirambe richitarisira mamiriro ezvinhu munzvimbo yako. tinopa mhinduro yedambudziko iri tichishandisa ma ledger anogona kusimbiswa uye mambure e collateral. ma operator anobudisa zvigadziriso zvitsva zvema ledger kuvashandirapamwe vavo, vachigadzira zvinyorwa zvingaongororwa zvemaakaunti. ma wallet anobudisa umboo hwekusatendeseka kuvashandirapamwe ivavo, avo vanochengetedza kuti ledger irambe iine operator akatendeseka. kubuda kwemunhu oga kunotsivwa nechokwadi chekuti mari inoramba iripo chero mambure achiripo. tinouya pamambure anopa kune vamwe basa rekuchengetedza kutenderera kwemari, anodzivirira mibhadharo yekuvhura, anokwanisa kugamuchira mubhadharo pasina kubatana, uye anokura zvakasiyana nezvigunwe zvepasi

## nhanganyaya

bitcoin deposits inokurudzira kupa mari inokurumidza uye inokura inotongwa nemakiyi, pasina kuvimba nevamwe, kunze kwecheni. basa recheni rinokura nehuwandu hwema ledger nekukurumidza kwekushandurwa kwereserve. huwandu hwebasa rinokura zvishoma pamusoro pemutsetse nehuwandu hwema ledger mumambure, zvichiita kuti mamiriyoni emabasa pachikamu chimwe nemabiriyone ema wallet zvigoneke

pane zvikumbiro zvakajeka:
- hapana kubuda kwemunhu oga: kana ma operator akakundikana mari inoramba iri mumambure
- hapana zvakavanzika: kusimbisa kunoda kujeka
- kuvapo kwenguva nenguva: deposit inongowanikwa sezvakawanda se operator. ma wallet anofanira kuparadzira mari kuti awedzere kuvapo

tinotarisira ruzivo rwema wallet ruchifanana nezvigunwe zvepasi zvinokurumidza, zvine mitengo yemubhadharo yakafanana ne lightning network

## ma ledger

ledger imhando isingashanduriki yemaapudeiti, ine hash yeapudeiti yakapfuura uye yakasainwa ne operator we ledger. mhando dzakasiyana dzemaapudeiti dzine mitemo yakasiyana inotonga nguva uye nzira dzekushandiswa kwadzo. ma ledger anozvitsanangura oga, maapudeiti awo aripo pachena uye asingagoni kurambwa, achibvumira munhu wese kuongorora kutevedzwa kwemitemo

ma ledger ane operator mumwe anoshanda, asi anochengetedzwa pamwe nemambure. operator upi neupi anogona kugadzira rimwe, asi kana akanyangadza kana akava asina kuvimbika operator akasiyana achagadzwa, pamwe nereserve. operator anoshanda panguva ino anozivikanwa nepubkey yakashandiswa kusaina apudeiti yekupedzisira yakasainwa pamwe

## ma deposit

deposit iakaundi yakatsiga inogona kutumira uye kugamuchira mari, inotongwa ne miniscript. pakuvhurwa mubhadharo wemafizi unorongwa, pamwe nekuti kugamuchira mari kunoda chikumbiro chakasainwa ne wallet here kana kwete. operator anofanira kubvumira kutambidzana pakati pema deposit pa ledger imwe chete pamwe nekubuda kwepacheni. vanofanira kubvumira ma deposit kubhadhara ma invoice e lightning

zviri musimba we operator kugadzira zvipo zvekufadhwa kwepacheni kana ma invoice e lightning panzvimbo ye deposit. kana vakaita, izvi zvinofanira kusainwa pamwe nenhengo ye quorum, uye wallet inofanira kusimbisa signature iyi. zvipo nema invoice hazvisi chikamu che ledger, saka ibasa re wallet kusimbisa ma signature nekuachengetedza seumboo

## mafizi

kutambidzana pakati pema deposit, pacheni, uye kuburikidza ne lightning kune mafizi anobhadharwa ku operator we ledger. kunewo mafizi anoiswa panguva nenguva pamabaransi nenguva yakataurwa. ose anorangana kana deposit itsva ichivhurwa. mafizi anogona kushandurwa mushure memabhuroko akataurwa, nechiziviso chemabhuroko akataurwa uye mukati memiganhu yepesenti yekushandura imwe neimwe yakarangwa pakuvhura. quorum inogona kuramba kusaina pamwe maapudeiti anogadzira mamiriro asingaiti mari ayo vanogona kupedzisira vava nezvikwereti

## kutambidzana

nzira yakareruka yekutambidzana ibasa remadanho maviri pakati pema deposit mbiri pa ledger imwe chete: deposit inotumira chikumbiro chekutumira mari. kana paine mari yakakwana, kiyi yemari ine mamiriro ekushandiswa inowedzerwa ku ledger. kana mamiriro ekushandiswa azadziswa nguva isati yapera, mari inoenda kubva kumutumiri kumupiwa mari mafizi e operator abviswa. kana nguva yasvika, kiyi inosunungurwa, mafizi madiki e operator abviswa. nemamiriro ekushandiswa e miniscript, izvi zvakakwana kubvumira deposit ipi neipi kupa masevhisi emabhiriji nekutenderera kwemari kune dzimwe deposit pa ledger imwe chete

## lightning

ma operator ane chiteshi che lightning vanogona kubvumira ma deposit kutumira nekugamuchira kuburikidza ne lightning network. kana deposit ichikumbira invoice ye lightning, operator anoigadzira kuburikidza ne lightning node yavo, anokumbira nhengo dze quorum kuti dzisaine pamwe kuratidza kuti dzakazvipira kukreditisha deposit kana yabhadharwa. wallet inofanira kuchengetedza invoice iyi yakasainwa pamwe seumboo. kana deposit ichikumbira kubhadhara invoice ye lightning, operator anobhadhara achishandisa lightning node yavo uye anobvisa mari mu deposit mushure mekuwana preimage

kana mubhadhari neanopiwa mari vari ma deposit pa operator mumwe, operator anogona kurangana mukati pasina kuendesa kuburikidza ne lightning, achikreditisha nekubvisa muma deposit acho pachake. izvi zvinodzivirira mafizi ekuendesa nekukundikana asi vachichengetedza chokwadi chimwe chekuverengwa

## ma courier

zvikumbiro zvekutambidzana zvinotambidzira mari chete pakati pema deposit pa ledger imwe chete. kutambidzira mari nepakati pema ledger, ma wallet anoshandisa ma courier — masevhisi ane ma deposit pama ledger akawanda uye anotakura kutambidzana pakati pawo. courier anozivisa huwandu nemafizi erudivi rumwe nerumwe pa ledger imwe neimwe pa relay. kana wallet richida kutumira kubva pa ledger A kuenda pa ledger B, rinogadzira kiyi yekutambidzana ku deposit ye courier uye rinokumbira kuti courier agadzire imwe kubva pa deposit yavo pa ledger yekuenda kumugamuchiri. kana makiyi ose agadzirwa wallet rinoratidza preimage kumugamuchiri, anopedza kutambidzana kubva ku courier. kana yaratidzwa, courier anoshandisa preimage imwe iyi kupedza kutambidzana kubva kumutumiri kuenda ku courier

iyi imhando yakajairwa ye hash time-locked contract. tinotarisira kuti nguva yekupera ye courier yekubuda inofanira kuva nenguva pfupi zvakanyanya kupfuura yekupinda, kuchengetedza kuti kana wallet risingaratidze, makiyi ose anodhamba uye hapana munhu anorasikirwa nemari. hapana kuvimbana kunodikanwa kunze kwechokwadi chenguva chinochengetedzwa nema operator

ma courier vanofanira kuisa mafizi pa ledger imwe neimwe: fee_in ne fee_out pa ledger imwe neimwe yavanoshanda. wallet rinoita tsananguro yemari yenzira se fee_out panzvimbo yekubva pamwe ne fee_in panzvimbo yekuenda. ma courier vanogona kushandura mafizi ne ledger zvichibva pakutenderera kwemari iripo, vachiringanisa mamiriro avo zvakasununguka. ma wallet anowana ma courier kuburikidza nemaziviso avo pa relay uye vanosarudza zvichibva pamafizi, huwandu, kana kukwanisa

## kutaurirana

kutaurirana kwose pakati pema wallet nema operator, uye pakati pema operator, kunoshandisa nostr relay. maapudeiti ema ledger anobudiswa sezviitiko zvichigara zvinochengetedzwa nema relay, zvichigadzira zvinyorwa zvekusingaperi zvinogona kuongororwa. zvikumbiro nemhinduro pakati pema wallet nema operator izviitiko zvenguva pfupi zvine TTL pfupi pa relay. ma operator vanozivisa mamiriro avo sezviitiko zvinogona kutsivwa, zvinobvumira ma wallet kuziva nekuenzanisa ma operator pasina bhuku guru

igadziriro iyi zvinoreva kuti ma wallet haadi kubatana kwenguva refu — vanogona kuenda padivi kwenguva refu uye vadzoke vachidzokorora zviitiko kubva ku relay ipi neipi inazvo. ma operator vanogona kuwanikwa kuburikidza ne relay ipi neipi yavanoona, uye kusarudza kwe relay ichokwadi chekuiswa kwete muganhu weprotocol

## reserve ne collateral

reserve inogara mu UTXO ine huwandu hukuru kana hunoenzana nezvimiro zvose zve ledger, inogona kushandiswa nevakawanda ve quorum, ine nzira yekudzoka ku operator mushure menguva yakareba

collateral imari ye operator pachake, yakaiswa uye yakakiywa pama ledger enhengo dze quorum. nhengo imwe neimwe ine deposit ye collateral inopiwa mari ne operator uye inokiywa kwenguva yakataurwa. zvimiro zvose zve ledger zvinogumira pakaviri ke collateral diki pane yose yakabatwa nenhengo ipi neipi, uye nguva ye quorum inogumira panguva pfupi yekukiya. izvi zvinochengetedza kuti mambure e collateral anogara aine mari yakakwana kutsigira kushandurwa kwecustody. deposit imwe ye collateral inogona kutsigira ma ledger akawanda kuti iwedzere kushanda kwemari, kunyange zvazvo ma wallet vanofanira kusarudza ma operator vane zvigadziko zve collateral zvisina kupindirana

zvimiro zvinochengetedzwa pakugadzira zvipo zvitsva zvekufadhwa kana ma invoice. operator haagoni kugadzira zvipo kana ma invoice zvingaita kuti zvimiro zvose zve ledger zvipfuure reserve kana zvipfuure kaviri ke collateral diki, chero chipi chiduku

## quorum

ma operator vanokumbira ma operator vamwe kuti vabatane ne quorum yavo nekuisa nekukiya collateral pa ledger yenhengo. chikumbiro chinosanganisira kuzvipira kwe collateral (huwandu nenguva yekukiya) nemamiriro enhengo: mafizi madiki anofanira kuzadziswa nema deposit pa ledger. nhengo imwe neimwe inofanira kushanda ledger yayo uye inogona kutora collateral ye operator kana operator akaonekwa kuti haatevere mitemo. nhengo dzinoisa miganhu yemafizi munguva yavo ye quorum — operator haagoni kuvhura ma deposit ane mafizi ari pasi peadiki yenhengo yakaoma kupfuura dzose, achidzivirira nhengo kubva pakugara nezvimiro zvisingaiti mari mushure mekushandurwa kwecustody

kana quorum yagadzirwa, reserve inoshandurwa kuenda ku multisig UTXO itsva. nhengo dzinosaina pamwe maapudeiti anotevera mitemo uye dzinobatsira mukudzosa kana operator akasaina zvisingatevere mitemo. quorum huru dzinowedzera mibhadharo yekutaurirana asi dzinoderedzera njodzi ye operator, dzinowedzera kuvapo, uye dzinoita kuti kubatana kuve kwakaoma uye kwakadhura. ma wallet vanofanira kusarudza quorum huru

## kudzivirira kwezveupfumi

protocol inotsiva kubuda kwemunhu oga nekudzivirira kwezveupfumi. nhengo dze quorum dzinokurudzirwa zvakajeka kuti dziite zvinopesana nekusatendeseka. munguva yebasa rakanaka dzinowana mafizi mashoma pa collateral, asi kana pane maitiro asingatevere mitemo anogona kusimbiswa dzinogona kutora collateral yose ye operator pa ledger yadzo

kana wallet richifungidzira kuvharirwa, rinogona kukwidza chikumbiro kunhengo dze quorum kuburikidza nekutumirwa kwakasimbiswa. nhengo inoisa hash yechikumbiro mu ledger yayo nemafizi madiki, ichigadzira umboo hwakasimba hwechimwe chikonzero. kana operator akakundikana kuita chikumbiro, nhengo ine umboo uye chikurudziro chezveupfumi chekutanga nharo

unyengeri hwe invoice ye lightning hunotevera mhando imwe yekudzivirira. operator anoziva kuti preimage yakagamuchirwa here, asi wallet harizive. zvisinei mubhadhari upi neupi anogona kupa preimage ku wallet. kuba kumwe kwakasimbiswa kunotanga nharo, kutorwa kwe reserve, nekutorwa kwe collateral. mubayiro wekuba mubhadharo mumwe unokomberedzwa, asi njodzi inoparadza, zvichiita kuti kuba kwe lightning kusina musoro wezveupfumi kunyange zvisingagone kusimbiswa zvizere pasina kubatsirwa nebato rechitatu

mamiriro ekukundikana ekuvharirwa nekudzivirira kwe lightning kubatana kwe quorum yose. protocol haigoni kudzivirira quorum inobatana kuba, asi mambure e collateral anochengetedza kuti kubatana kunodhura kupfuura zvakunowana. kujeka kwemambure kunobvumira ma wallet nemamisika ekuwana kuziva magadzirirwo e quorum anotyisa vasati vaisa mari

## nguva

nguva yakajeka inoyerwa nezvigunwe zvepasi. miganhu haingapfuuri huwandu hwakaringana hwekusimbiswa kuti uchengetedze kutsiga munguva yekugadzirwa patsva kwecheni

kana miganhu mikuru ichidikanwa tinovimba nekurongwa kwechikonzero. ledger ye cryptographic i merkle chain. apudeiti imwe neimwe inosimbisa kuti yakagadzirwa mushure memaapudeiti ose akaitangira, asi haipa chokwadi pamusoro peruzivo kunze kwecheni. kuti tigadzire kurongwa kwakaparadzirwa, tinoda kuti kusaina pamwe kusanganisire hash yeapudeiti yazvino kubva ku ledger yeanosaina. hash iyi inobva yaiswa mu hash yeapudeiti yazvino, ichiva chikamu checheni pamwe nechikamu chezvimwe zvose zvinochengetedzwa ne operator we ledger anosainira, ichigadzira mambure echikonzero. izvi hazvinokwanise kusimbisa nguva zvakajeka, asi zvinokwanisa kusimbisa kuti zvimwe zveruzivo zvakagadzirwa mumarongerwo akatarwa

## umboo hweunyengeri

tinogona kusimbisa mhando dzakasiyana dzeunyengeri nekuratidza ruzivo rwakagadzirwa mumarongerwo asiri iwo. kana ruzivo rusina kusanganisirwa nemabasa ejairwa emambure, runogona kupinzwa nekugadzira basa rinosanganisira hash yeumboo. kana rwaiswa muapudeiti yakasainwa ne operator, umboo hunoratidizwa sehwakagadzirwa panzvimbo isingatevere mitemo mumarongerwo:

- operator, akavimbisa kukreditisha deposit nemari yakatumirwa pacheni kune kero yakatarwa, anosaina apudeiti ye ledger isina kukreditisha kwakakodzera, asi ine cheni inoratidza block hash inopfuura huwandu hwekusimbiswa hunobvumirwa nguva isati yasvika yekukreditisha

- operator, akagadzira invoice ye lightning panzvimbo ye deposit, anosaina apudeiti ye ledger isina kukreditisha deposit kunyange preimage yakaratidzwa mucheni

- kusaina pamwe kunoti hash yazvino ye ledger ndeiyo inotangira hash yavo yezvino mucheni

- nhengo ye quorum ye ledger inonetsa yakanga ichishanda asi haina kuita zvinoenderana neumboo hweunyengeri mukati memabhuroko akatarwa

- kusaina kana kusaina pamwe maapudeiti e ledger asingatevere mitemo

umboo hweunyengeri hunosanganisira umboo necheni yechikonzero inobatanidza hash yakaiswa ku ledger ye operator anotongwa. cheni imhando yemaapudeiti akasainwa pamwe, rimwe nerimwe rinosanganisira member_ledger_hash kubva ku ledger yechikamu chakapfuura. vaongorori vanofamba necheni pasina kutsvaka, vachisimbisa kuti chikamu chimwe nechimwe chiapudeiti yakasainwa, uye kuti hash yeumboo inoenderana nedata yakaiswa

## kudzosa

kana ledger yava isina kuwanikwa kana isingatevere mitemo, nhengo dze quorum dzinogona kugadzira kupfuurira kwavo kwe ledger kubva paapudeiti yekupedzisira inotevera mitemo. vanofanira kugadzira quorum itsva nekupa umboo hwe collateral. nhengo dzinofanira kurangana kushandisa reserve yakapfuura kuenda kusarudzo yemhando yema ledger anogona kuva anotevera. akunda musarudzo iyi anowedzera apudeiti yekuwana kucheni yavo, uye vamwe vanowedzera kupa. ma wallet anoenderera mberi kutaura ku ledger imwe chete, achigamuchira chete mhinduro dzakasainwa pamwe ne quorum. panguva nenguva, uye kana mhinduro dzisina kusainwa pamwe ne quorum sezvakatarwa, wallet rinofanira kubvunza mambure nekudzokorora maapudeiti e ledger kuziva kushandurwa kwecustody

kana kusingatevere mitemo kuchiita sechinhu chisina kuitwa nemaune (semuenzaniso, ledger yava isina kuwanikwa kwemabhuroko akatarwa) kushandurwa kwecustody kunofanira kuremekedza: mari ye reserve inodikanwa chete kufukidza zvimiro zve ledger inotumirwa kusarudzo, uye chinja inotumirwa ku operator nepubkey yake. kutonga kwe collateral hakushandurwi

kana umboo hwekusingatevere mitemo huripo, mari inopfuura reserve inodikanwa inogovewa zvakaenzana pakati penhengo dze quorum, uye collateral iri pama ledger enhengo inobvumirwa kutorwa

## hutano hwemambure

kurwisa kumwe kwakareruka kugadzira zvitsuwa zvema operator vanobatana. mushure mekuvaka zvimiro zvakakura pama ledger avo, vanorangana kubuda, vachiba mari inopfuura collateral yakaraswa. mambure anogona kudzivirira izvi, kunze kwenzvimbo dzine mari yemukati inopfuura collateral inobatanidza kunharaunda isina kubatana. collateral yakawanda ne quorum huru dzakasiyana dzinoderedzera mukana wekuti matunhu aya agadzirwe, asi anogona kugadzirwa nemaune uye hatigoni kutarisira kuti wallet rimwe nerimwe riongorore mambure ose. panzvimbo pezvo mamisika ekuwana anofanira kuburitsa makiyi ekuverengeka kwe operator zvichibva paongororo dzemufananidzo sema algoritimu ekutsvaka mibayiro

## mhedziso

tinopa mambure e collateral anoda kubatana kuti akube, asi kubatana kunowedzera collateral iri pangozi nekukurumidza kupfuura kuita kuti mari inogona kubiwa iwedzere. tinoshandisa mambure aya kuchengetedza ma ledger e cryptographic akatsigirwa ne reserve yakazara. ma ledger aya anoshandira maakaunti panzvimbo yema wallet asiri pamhepo mukushandurana nemafizi akatarisirwa. zvigadziko zvema ledger zvinotsigira mamiriro ekushandiswa e miniscript akakwana kune zvibvumirano zvakareruka. mambure anokura zvakafanira nemutsetse, achibvumira mambure makuru kupa mabhiriyoni ema wallet nehuwandu hwekubhadharana hunopfuura mambure ekare ekubhadharana
