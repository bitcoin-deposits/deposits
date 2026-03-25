# bitcoin deposits
## ensonga ennene

enkola ey'ekituufu ey'obupangisa ssente z'ekikompyuta wakati w'abantu babiri yandikkirizizza okusasula ku mutimbagano okutuumibwa butereevu okuva ku muntu omu okudda ku mulala mangu era nga tewali kuyimirizibwa. lightning network ewaayo ekitundu ky'okuddamu, naye ebirungi ebyetaagisa bibuulira singa ekitongole ekyekkirizibwa kyetaagisibwa okuddukanya embeera ku lw'oyo. tuteesa okuddamu ensonga eno nga tukozesa ledger ezikakasibwa n'omukutu gwa collateral. operator bagabanya eby'okulongoosa ledger eri bannabyabwe, nga batonda ebyawandiikibwa eby'akawunti ebyakebezebwa. wallet zibuulira obujulizi bw'obulimba eri bannabyabwe abo, abeekakasa nti ledger etereka operator omwesimbu. okufuluma ku bwokka kwo kwegyagulira kudda mu kukakasibwa nti ssente zisigala nga ziwebwayo emirundi gyonna omukutu lwe guliwo. tutuuka ku mukutu oguwaayo okuddukanya obukadde, gwewala ssente z'okutandika, guyinza okufuna okusasula nga oli offline, era gukula nga tegwesigamiziddwa ku mutimbagano gw'omusingi

## ennyanjula

bitcoin deposits egenderera okuwaayo ssente ezikola mangu era ezikula ezikolebwa ne bisumuluzo, awatali kweyama, ebweru w'olukuŋŋaana. emirimu ku mutimbagano gw'omusingi gikula n'omuwendo gwa ledger n'emirundi gy'okukyusa reserves. omutindo gukula waggulu watono okusingawo ku buyimivu n'omuwendo gwa ledger mu mukutu, nga biteeberezebwa nti obuwumbi bw'okutumirana buli sikonda mu tiriyoni za wallet bisoboka

waliwo enkyukakyuka ez'okwatibwako:
- tewali kufuluma ku bwokka kwo: operator bwe balemerwa ssente zisigala mu mukutu
- tewali kyama: okukebezebwa kwetaagisa okwoleka
- okuweebwa okutali kwa bulijjo: deposit yonna efaananira operator waayo mu kuweebwa. wallet zirina okusaasaanya ssente okusobola okwongera okuweebwa

tusuubira enneeyisa ya wallet okubeera ng'efaananira omutimbagano gw'omusingi ogw'amangu, nga erina ssente z'obupangisa ezifaananira lightning network

## ledger

ledger ye luyimu lw'eby'okulongoosa olutalika kukyusibwa, ekyerina hash y'ekyalongoosebwa ekyasooka era ekisayinidde operator wa ledger. ebika by'okulongoosa eby'enjawulo birina amateeka ag'enjawulo agafuga ddi era nga biyinza okukozesebwa bitya. ledger zyeenyonyola zyokka, eby'okulongoosa byabyo nga biri mu lwatu era tebisobola kuganibwa, nga bikikiriza omuntu yenna okukebera obutuukiridde

ledger zirina operator omu eyakola, naye zitunulirwa awamu n'omukutu. operator yenna ayinza okukitondawo, naye singa abulira oba afuuka omulimba operator omulala aliteerwa, awamu ne reserves. operator ow'ekiseera ekyo amanyibwa ne pubkey eyakozesebwa okusayina ekyalongoosebwa ekyasembyeyo ekyasayinidwa awamu

## deposit

deposit y'akawunti enkalu eyinza okusindika n'okufuna ssente, ekola ne miniscript. ku kutandika enteekateeka y'essente z'omusasula eteeberezebwa, awamu n'okuba nga okufuna ssente kyetaagisa okusaba okusayinidde wallet. operator alina okukkiriza okusindikagana wakati wa deposit ku ledger emu awamu n'okufuluma ku mutimbagano gw'omusingi. balina okukkiriza deposit okusasula lightning invoices

kiri mu buyinza bw'operator okutonda ebisuubizo by'okuteeka ssente ku mutimbagano gw'omusingi oba lightning invoices ku lwa deposit. bwe bakikola, bino birina okusayinidwa awamu ne membro wa quorum, era wallet erina okukebera omukono guno. ebisuubizo ne invoices tebiriko ku ledger, kale kiba kya wallet okukebera emikono n'okugitereka ng'obujulizi

## ssente z'omusasula

okusindikagana wakati wa deposit, ku mutimbagano gw'omusingi, ne mu lightning birina ssente z'omusasula ezisasulibwa operator wa ledger. waaliwo ne ssente z'omusasula ezisasulibwa ku balance buli kiseera ekyogerezebwako. zonna zikakasanyizibwa deposit empya bw'eggulwawo. ssente z'omusasula ziyinza okukyusibwa oluvannyuma lwa blocks ezigerezebwako, ng'ekirizibwa blocks ezigerezebwako ez'amannya era mu nkola y'okukebera ey'okutuusa eyakakasanyiziddwa ku kutandika. quorum eyinza okugaana okusayina awamu eby'okulongoosa ebitondawo embeera ezetegereza ssente eziyinza okuba nti basibire

## okusindikagana

enkola y'okusindikagana ey'omusingi kwe kukola okw'emitendera ebiri wakati wa deposit bbiri ku ledger emu: deposit esindika okusaba okusindika ssente. singa waliwo ssente ezimala, okugatta ku ssente awamu n'embeera ey'okusasula kuteekebwa ku ledger. embeera ey'okusasula bw'etuukirizibwa nga tekinnayitawo, ssente zisindikibwa okuva eri omusindika okudda eri afuna nga ssente z'omusasula za operator ziggyibwawo. ekiseera ky'okumaliriza bwe kituukibwa, okugatta kuggibwawo, nga ssente z'omusasula entono za operator ziggyibwawo. n'embeera z'okusasula za miniscript, kino kimala deposit yonna okusobola okuwaayo empita n'obuwumbi eri deposit ndala ku ledger emu

## lightning

operator abalina lightning channel bayinza okukkiriza deposit okusindika n'okufuna ku lightning network. deposit bw'esaba lightning invoice, operator akitonda mu lightning node yabwe, asaba ba membro ba quorum okugisayina awamu okukakasa nti beesuubiza okuteeka ssente ku deposit oluvannyuma lw'okusasula. wallet erina okukuuma invoice eno esayinidde awamu ng'obujulizi. deposit bw'esaba okusasula lightning invoice, operator asasula ng'akozesa lightning node yabwe era aggya ssente ku deposit oluvannyuma lw'okufuna preimage

omusasula n'afuna bwe baba ba deposit ku operator gwe gumu, operator ayinza okumaliriza munda awatali kuyita mu lightning, ng'agatako n'aggyako ku deposit ezeetaagisa butereevu. kino kiwewula ssente z'empita n'obutabaluwa nga kikuuma enkola y'akawunti ey'emu

## courier

okusaba okusindikagana kusisinkanira ssente wakati wa deposit ku ledger emu kyokka. okusindika ssente okuyita mu ledger ez'enjawulo, wallet zikozesa courier — empeereza ezikuuma deposit ku ledger ebitali bimu era ezitwalira okusindikagana wakati waabyo. courier eraga obuyinza n'essente z'omusasula ku buli ledger ku relay. wallet bw'eyagala okusindika okuva ku ledger A okudda ku B, etonda okugatta ku deposit ya courier era esaba courier okutonda ekigatta okuva ku deposit yaabwe ku ledger ey'ekigenderera okudda eri afuna. ebigatta byombi bwe biteekerateekerezebwa wallet eraga preimage eri afuna, amalawo okusindikagana okuva eri courier. preimage bw'eragibwa, courier akozesa preimage eno okumaliriza okusindikagana okuva eri omusindika okudda eri courier

eno ye nkola ya hash time-locked contract eya bulijjo. tusuubira nti ekiseera ky'okumaliriza eky'ebweru kya courier kiba ki kisooka okuyita ku ky'omunda, nga kikakasa nti wallet singa teragako, ebigatta byombi biggwawo era tewali ludda lufiirwa ssente. tewali kweyama kwetaagisibwa okujjako omukisa gw'ekiseera eky'okumaliriza ogufugibwa operator

courier zirina okuteeka ssente z'omusasula ku buli ledger: fee_in ne fee_out ku buli ledger kye baweereza. wallet ebalirira emirimu gy'empita nga fee_out ku nsibuko ne fee_in w'ekigenderera. courier bayinza okukyusa ssente z'omusasula ku buli ledger okusinziira ku buwumbi obuliwo, nga beequlibya mu ngeri ey'obulungi. wallet zizuula courier mu by'okulangirira ku relay era zironda okusinziira ku ssente z'omusasula, obuyinza, oba okubunyisa

## empuliziganya

empuliziganya yonna wakati wa wallet ne operator, ne wakati wa operator, ekozesa nostr relay. eby'okulongoosa ledger bifulumizibwa ng'ebintu eby'obuwangaazi relay bye bitereka, nga bitonda ebyawandiikibwa eby'olubeerera ebyakebezebwa. okusaba n'okuddamu wakati wa wallet ne operator biri ebintu eby'ekiseera ekitono awamu ne TTL ey'okumpi ku relay. operator balangirira embeera zaabwe ng'ebintu ebyennyisibwa, nga bakkiriza wallet okuzuula n'okugezaageranya operator awatali directory entuufu

enteekateeka eno etegeeza nti wallet tezeetaagisa nkwatagana ey'obutayima — ziyinza okuva ku mutimbagano okumala ekiseera kyonna era ne zidda nga zikkola eby'okulongoosa okuva ku relay yonna erinaabyo. operator bayinza okutuukibwako ku relay yonna gye batunuulira, n'okulonda relay kye kisalawo ky'okuteeka, si nkola ya protocol

## reserves ne collateral

reserves biterekebwa mu UTXO ey'omuwendo ogusingawo oba ogukwatagana n'omutwaalo gw'ebyetaago bya ledger, ekozesebwa bangi ba quorum, n'empita ey'okudda eri operator oluvannyuma lw'ekiseera eky'omuwendo

collateral bwe ssente za operator ze zennyini, eziterekedde era ezigattidde ku ledger za ba membro ba quorum. buli membro akuuma deposit ya collateral operator gy'ateekamu ssente era gye yagatta okumala ekiseera ekyogerezebwako. ebyetaago bya ledger byogerwa ku mirundi ebiri eya collateral eyasinga okuba entono ekuumibwa membro yenna, n'ekiseera kya quorum kikomekera ku nkola ey'ekiseera eky'okusobya okugatta. kino kikakasa nti omukutu gwa collateral gubeera n'ebisinziirwako ebimala okubikka obuddukanya bw'obukuumi. deposit ya collateral ey'emu eyinza okuwagira ledger ebitali bimu okwongera ku nkozesa nnungi ey'ebisumuluzo, wadde nga wallet zirina okwagala operator abalina nsibuko za collateral ezetali zimu

ebyetaago biteekebwa mu nkola mu kutonda ebisuubizo eby'okuteeka ssente empya oba invoices. operator tasobola kutonda ebisuubizo oba invoices ebiyinza okusindika ebyetaago bya ledger waggulu wa reserves oba waggulu w'emirundi ebiri eya collateral eyasinga okuba entono eyagattidde, ekisinga obuba kitono

## quorum

operator basaba operator abalala okwegatta mu quorum kyabwe nga bateeka n'okugatta collateral ku ledger ya membro. okusaba kulimu okwesuubiza kwa collateral (omuwendo n'ekiseera ky'okugatta) n'embeera za membro: enteekateeka y'obusinga eya ssente z'omusasula deposit ku ledger gye zirina okutuukiriza. buli membro alina okukola ledger ye era ayinza okukwata collateral ya operator singa operator akakasibwa okubeera atagoberera. ba membro bateeka emipimo ku nteekateeka y'essente z'omusasula mu kiseera kye bali mu quorum -- operator tasobola kuggula deposit n'essente z'omusasula wansi w'obusinga bwa membro, okukuuma ba membro obutaggya ebyetaago ebitalisasula oluvannyuma lw'okukyusa obuddukanya

quorum bwe kiteekerateekerezebwa, reserves bikyusibwa mu UTXO empya eya multisig. ba membro basayina awamu eby'okulongoosa ebigoberera era bayambibwa mu kuddamu singa operator asayina ebitali bigoberera. quorum ennene yongera empuliziganya naye eyimpisa okubi kw'operator, yongera okuweebwa, era efuula okukakirana okuzibu era okw'ebbeeyi. wallet zirina okwagala quorum ennene

## okuziyiza ky'enfuna

protocol ekyusa okufuluma ku bwokka kwo n'okuziyiza ky'enfuna. ba membro ba quorum balina ensonge butereevu okukolera ku bulimba. mu mirimu egya bulijjo bafuna ssente z'omusasula entono ku collateral, naye mu mbeera ey'enneeyisa etali ngoberera eyakakasibwa bayimirira okukwata collateral ya operator yonna ku ledger kyabwe

wallet bw'eteebereza okuziyizibwa, eyinza okusindika okusaba eri ba membro ba quorum mu mpita endagibwa. membro ateeka hash y'okusaba mu ledger ye ku ssente z'omusasula entono, nga atonda obujulizi obw'enkola. operator bw'aremwa okukola ku kusaba, membro alina obujulizi n'ensonge y'enfuna okutandika ensonga

obulimba ku lightning invoice bugoberera enkola y'emu ey'okuziyiza. operator amanyi oba preimage yafunibwa, naye wallet temanya. wabula omusasula yenna ayinza okuwaayo preimage eri wallet. okubba okukakasibwa okumu kutandika ensonga, okukwata reserves, n'okukwata collateral. empeera y'okubba okusasula okumu eba ya mpimo, naye akabi kaba ka bwonna, nga kufuula okubba ku lightning okutali kya magezi mu by'enfuna wadde nga tekiyinza kukakasibwa awatali buyambi bw'ebweru

embeera ey'obutakolera obulungi ku kuziyiza n'okuziyiza kwa lightning kwe kukakirana kwa quorum yonna. protocol tesobola kukuuma ssente singa quorum yonna ekakirana okubba, naye omukutu gwa collateral gukakasa nti okukakirana kusasula okusingawo ku kifunibwa. okwoleka kw'omukutu kukkiriza wallet n'akatale k'okuzuula okuteebereza enkolagana za quorum ez'okuteeberezebwa nga bateeka ssente

## ekiseera

ekiseera ekya ddala kibalirwa ku mutimbagano gw'omusingi. emipimo teyinza kusingawo omuwendo gwa confirmations ogukkirizibwa okukuuma obunywerevu mu kuddamu okuteekerateeka luyimu

emipimo ey'waggulu gye yeetaagisibwa tweyesigama ku nkola ey'ensonga. ledger ey'obukugu ye merkle chain. buli kulongoosa kukakasa nti kyatondebwa oluvannyuma lw'eby'okulongoosa byonna ebyasooka, naye tekiwa mukisa ku bimanyiiso ebweru w'oluyimu. okuzimba enteekateeka ey'okugabanya, twetaagisa nti emikono egy'awamu gikwateeko hash y'ekyalongoosebwa ekyasembyeyo okuva ku ledger ey'omusayinira. hash eyo etefula mu hash y'ekyalongoosebwa eky'ekiseera kino, nga kifuuka ekitundu ky'oluyimu awamu n'oluyimu lwonna olulala operator wa ledger ky'asayinira, nga kitonda omukutu gw'ensonga. kino tekiyinza kukakasa ekiseera mu ngeri ey'obulambulukufu, naye kiyinza okukakasa nti ebimanyiiso ebimu byatondebwa mu nkola ey'emu

## obujulizi bw'obulimba

tuyinza okukakasa ebika by'obulimba eby'enjawulo nga twoleka obumanyiiso obwatondebwa mu nkola embi. obumanyiiso bwe butali mu mirimu egya bulijjo egy'omukutu, buyinza okuyingizibwa nga mutonda emirimu egirina hash y'obujulizi. bwe buteekerateekerezebwa mu kulongoosa okusayinidde operator, obujulizi buragibwa ng'obwatondebwa mu kifo ekitali kigoberera mu nkola:

- operator, bwe yali asuubize okuteeka ssente ku deposit n'essente ezisindikidde ku mutimbagano gw'omusingi ku ndagiriro ey'emu, asayina ekyokulongoosa ledger ekitaliimu credit ensaanyufu, naye ekyerina oluyimu oluraga hash y'obulooke eyasingawo omuwendo gwa confirmations ezikkirizibwa nga credit tennateekedwa

- operator, bwe yali atondye lightning invoice ku lwa deposit, asayina ekyokulongoosa ledger ekitali kiteekayo ssente ku deposit wadde preimage eragiddwa mu luyimu

- omukono ogw'awamu ogwogera nti hash ya ledger eky'ekiseera kino ye emu eyasooka okusingawo hash yaabwe ey'oluvannyuma mu luyimu

- membro wa quorum eya ledger ey'ensonga eyali akola naye atakola ng'obujulizi bw'obulimba bwe bwetaagisa mu miwendo gya blocks

- okusayina oba okusayina awamu eby'okulongoosa ledger ebitali bigoberera

obujulizi bw'obulimba bukubwa obujulizi n'oluyimu lw'ensonga olugatta hash eyateekerateekerezebwa ne ledger eya operator avunaanibwa. oluyimu lwe lulundagaana lw'eby'okulongoosa ebyasayinidwa awamu, buli kimu nga kirina member_ledger_hash okuva ku ledger ey'enkolagana eyasooka. abakebezi batambula ku luyimu nga tebanonya, nga bakakasa buli nkolagana nti ye kulongoosa okusayinidde, era nti hash y'obujulizi yenkanankana n'ebimanyiiso ebyateekerateekerezebwa

## okuddamu

ledger bw'ebuulira oba butali bugoberera, ba membro ba quorum bayinza okutonda okusigala kwa ledger okuva ku kulongoosa okugoberera okusembyeyo. balina okuzimba quorum empya n'okuwaayo obukakasa bwa collateral. ba membro balina okukola awamu okusasula reserves eby'emabega okutuuka ku mpiirira y'oluyimu olw'okuddiriira. omuwanguzi w'empiirira eno ateekako ekyokulongoosa eky'okufuna ku luyimu lwabwe, n'abalala ne bateekako eky'okuvaayo. wallet zisigala okuwandiikira ledger emu, nga zikkiriza okuddamu okusayinidde awamu quorum kyokka. buli kiseera, era okuddumuza bwe kutaba na mukono gwa quorum ogusuubirwa, wallet erina okubuuza omukutu n'okukola eby'okulongoosa ledger okumanya enkyukakyuka mu buddukanya

obutali bugoberera bwe bufaananira okuba kw'ekikozesebwa (eky'okulabirako, ledger ebulidde okumala blocks ezimu) okukyusa obuddukanya kulina okuba okw'ekisa: omuwendo gwa reserves ogwetaagisibwa okubikka ebyetaago bya ledger gwokka gwe gutumibwa ku mpiirira, n'ekyakyuka kisindikibwa eddayo ku pubkey ya operator. obuddukanya bwa collateral tebukyusibwa

obujulizi bw'obutali bugoberera bwe buliwo, omuwendo ogusingawo reserves ebyetaagisibwa gugabibwa kwe kumu mu ba membro ba quorum, era collateral ekuumibwe ku ledger za ba membro ekkirizibwa okukwatibwa

## obulamu bw'omukutu

olumbe olumu olw'obulungi kwe kutonda ebizinga bya operator abakakirana. oluvannyuma lw'okuzimba ebyetaago ebinene ku ledger zaabwe, bakola awamu okufuluma, nga babba ssente ezisingawo collateral efiiriddwa. omukutu guyinza okwekuuma okuva ku kino, wabula mu bitundu ebyomunda ebisinga collateral egatta ku mukutu ogutali gukakirana. emipimo gya waggulu egya collateral n'ebibinja ebinene ebyenjawulo biyimpisa okukolerwa okutondebwa kw'ebibuntu bino, naye biyinza okutondebwa mu ngeri era tetusobola kusuubira wallet yonna okukebera omukutu gwonna. mu kifo ky'ekyo akatale k'okuzuula galina okufulumya ebipimo by'obwanirizi bwa operator okusinziira ku nsengeka z'engeri ng'entoledde ez'okukuŋŋaanya empeera

## enkomerero

tuteesa omukutu gwa collateral ogwetaagisa okukakirana okubba, naye okukakirana kwongera collateral ebeera mu kabi mangu okusinga omuwendo oguyinza okubibwa. tukozesa omukutu guno okukuuma ledger ez'obukugu eziwagirwa reserves entuufu. ledger zino ziweereza akawunti ku lwa wallet ez'offline nga biggyawo ssente z'omusasula ezikakasanyiziddwa. ebikozesebwa bya ledger biwagira embeera z'okusasula za miniscript ezimala ku nkola entono ez'amagezi. omukutu gukula kumpi mu buyimivu, nga gukkiriza omukutu omunene okuwaayo obuwumbi bwa wallet n'omutindo gw'okutumirana ogusingawo emikutu gya bulijjo egy'okusasula
