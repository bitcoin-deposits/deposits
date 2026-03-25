# bitcoin deposits
## incamake

uburyo bwiza bwo guhana amahera mu buryo bwa elegitoronike hagati y'abantu babiri butuma amahera arungikwa atarindira umwe ku wundi bidatevye kandi bidatowe gutegura vyinshi. igisata ca lightning gitanga igice c'umuti, ariko ivyiza nyamukuru birazimira iyo hari umuntu w'icitegererezo wundi akenewe kugira ngo agenzure ibikuranga. dushikiriza umuti w'iki kibazo dukoresheje ama ledger ashobora kugenzurwa n'urubuga rwa collateral. aba operator barungikira abo bakorana amakuru mashasha y'ama ledger, bakaba barema icandiko rishobora kugenzurwa ry'amakonti. ama wallet arungikira abandi aba operator ibimenyamenya vy'uburiganya, bakaba bakesha ko ledger igumana operator w'umutima-nyakuri. gusohoka ukwigeneye bisimburwa n'icemeza ko amahera agumana kuboneka igihe igisata kigikora. tushika ku gisata gisiganira ubutunzi bw'amazi, gikinza amafaranga yo kwinjira, gishobora kwakira amahera utari ku murongo, kandi gikura bidajanye n'urwego rw'ishingiro

## intangamarara

bitcoin deposits igamije gutanga amahera ajanwa n'urufunguzo mu buryo bwihuse kandi bushobora gukura, mu buryo butagendera ku kwizera, hanze y'umunyororo. ibikorwa kuri umunyororo bikura biganye n'igitigiri c'ama ledger n'incuro reserves zihindurwa. uburinganire bw'ibicuruzwa bukura burengeye gatoya uburinganire n'igitigiri c'ama ledger mu gisata, bigatuma imiliyoni y'ibicuruzwa ku musegonda mu mamiliyari y'ama wallet bishoboka

hariho ivyisubirwamwo bitomoye:
- nta gusohoka ukwigeneye: iyo aba operator basanze amahera aguma mu gisata
- nta bwihishe: kugenzura bisaba ubwazi
- kuboneka guhagarara: deposit iboneka gusa nk'uko operator aboneka. ama wallet akwiye gukwiragiza amahera kugira ngo yiyongere kuboneka

twizigiye ko uburambe bwa wallet buzomera nk'urwego rw'ishingiro rwihuse, bufise ubutunzi bw'amahera bumeze nka lightning

## ama ledger

ledger ni urunigi rudahinduka rw'amakuru mashasha, rurimo hash y'amakuru yabanje kandi rusinywe na operator wa ledger. ubwoko butandukanye bw'amakuru bufise amategeko atandukanye agenga igihe n'uburyo bishobora gukoreshwa. ama ledger aribwira, amakuru yavyo aboneka ku mugaragaro kandi adashobora kwihakana, bigatuma umuntu uwo ari we wese ashobora gusuzuma ubwitonzi

ama ledger afise operator umwe akora, ariko agenzurwa hamwe n'urubuga. operator uwo ari we wese ashobora gukora kimwe, ariko aramutse azimiye canke akaba umuhemu operator uwundi azoshirwaho, hamwe na reserves. operator akora ubu amenyekana n'urufunguzo rw'icese rwakoreshejwe gusinyira amakuru mashasha y'ubu yasinyweko hamwe

## ama deposit

deposit ni konti ihamye ishobora kohereza no kwakira amahera, igenwa na miniscript. mu kwugurura, amafaranga arategekanywa, kimwe n'uko kwakira amahera bisaba icifuzo gisinywe na wallet canke bitabisaba. operator akwiye kwemerera ihererekanya hagati y'ama deposit ku ledger kimwe hamwe no gusohora kuri umunyororo. bakwiye kwemerera ama deposit kwishura ama invoice ya lightning

biri mu bubasha bw'operator gukora ibisabwa vy'ifadanyo kuri umunyororo canke ama invoice ya lightning ku bw'ideposit. abikoze, ivyo bikwiye gusinywa hamwe n'umwe mu bagize quorum, kandi wallet ikwiye kugenzura iyo sinya. ibisabwa n'ama invoice si ibice vya ledger, ni inshingano ya wallet kugenzura amasinya no kubibika nk'icabona

## amafaranga

ihererekanya hagati y'ama deposit, kuri umunyororo, no mu nzira ya lightning birishurwa na operator wa ledger. hariho kandi amafaranga ashirwa ku miterere y'amahera mu kiringo kigenwe. vyose birahurweko iyo deposit nshasha iguruka. amafaranga arashobora guhindurwa inyuma y'igitigiri kigenwe c'ama block, hahawe itangazo ry'ama block kigenwe kandi mu rugero rw'igipimo c'ihindurwa kuri buri guhindurwa cyahurweko mu kugurura. quorum irashobora kwanka gusinyira hamwe amakuru mashasha atuma ibintu bidashobora gutanga inyungu kandi ayo bashobora kuba bariko bafatirwa

## ihererekanya

uburyo bworoshye bw'ihererekanya ni igikorwa c'intambwe zibiri hagati y'ama deposit abiri ku ledger kimwe: deposit itanga icifuzo co kohereza amahera. nimba hariho amahera ahagije, igifungo c'amahera gifise ibisabwa vyo gukoresha gishirwa ku ledger. nimba ibisabwa vyo gukoresha vyujujwe imbere y'igihe, amahera ava ku wohereje aja ku wakiriye hakurwaho amafaranga ya operator. nimba igihe cashitse, igifungo gisesurwa, hakurwaho amafaranga mato ya operator. hamwe n'ibisabwa vyo gukoresha vya miniscript, ibi bihagije kugira ngo deposit iryo ari ryo ryose ritange ubuserukizi bw'ibihuza n'ibikorwa vy'amazi ku ma deposit ayandi ku ledger kimwe

## lightning

aba operator bafise umuyoboro wa lightning barashobora kwemerera ama deposit kohereza no kwakira biciye kuri lightning. iyo deposit risavye invoice ya lightning, operator arikora biciye ku noodiyo yiwe ya lightning, agasaba abagize quorum kuyisinyira hamwe kugira ngo bemeze ko bazoshira ku konti ya deposit iyo amahera yishurwe. wallet ikwiye kubika iyi invoice isinywe hamwe nk'icabona. iyo deposit risavye kwishura invoice ya lightning, operator arishura akoresheje noodiyo yiwe ya lightning agakura amahera ku deposit amaze kuronka preimage

iyo uwishura n'uwakiriye bombi ari ama deposit ku operator umwe, operator arashobora guheza imbere ata nzira ya lightning, ashira no gukura ku ma deposit ajanye atarengutse. ibi bikinza amafaranga y'inzira n'ingorane mu gihe bibungabunga icemeza kimwe c'amakonti

## ama courier

ibisabwa vy'ihererekanya bimurira gusa amahera hagati y'ama deposit ku ledger kimwe. kugira ngo amahera ajabuke ama ledger, ama wallet akoresha ama courier — ibikorwa bifise ama deposit ku ma ledger vyinshi bikaba bijana ihererekanya hagati yavyo. courier imenyesha ubushobozi n'amafaranga ku buri ruhande kuri buri ledger kuri relay. iyo wallet ishaka kohereza kuva ku ledger A ija ku ledger B, ikora igifungo c'ihererekanya ku deposit ya courier igasaba courier gukora ikindi giturutse ku deposit ryayo ku ledger y'aho bigana gushika ku wakiriye. ibifungo vyombi bimaze gushirwaho, wallet ishikiriza preimage uwakiriye, akaba arangiza ihererekanya kuva ku courier. imaze gushirwa ahagaragara, courier ikoresha iyi preimage nyene kurangiza ihererekanya kuva ku wohereje ija ku courier

iki ni igishusho gisanzwe ca hash time-locked contract. twizigiye ko igihe co gusohoka ca courier kizoza imbere gukomeye y'ico kwinjira, bikaba vyerekana ko wallet idashikirije, ibifungo vyombi bishira kandi nta wuhomba. nta kwizera gusabwa atari icemeza c'igihe kigenwa na ba operator

ama courier akwiye gushiraho amafaranga kuri buri ledger: fee_in na fee_out kuri buri ledger akorera. wallet igereranya igiciro c'inzira nka fee_out ku ledger y'ahatangurirwa hamwe na fee_in ku ledger y'aho bigana. ama courier arashobora guhindura amafaranga kuri buri ledger ashingiye ku butunzi buboneka, akagarukanisha ibibanza vyayo mu buryo busanzwe. ama wallet asanga ama courier biciye mu matangazo yazo kuri relay kandi ahitamwo ashingiye ku mafaranga, ubushobozi, canke urugero rwo gufuka

## ivugana

ivugana ryose hagati y'ama wallet na ba operator, no hagati y'aba operator, rikoresha nostr relay. amakuru mashasha y'ama ledger ashirwa ahagaragara nk'ibintu birama relay ibika, bigatuma haba icandiko rihoraho rishobora kugenzurwa. ibisabwa n'inyishu hagati y'ama wallet na ba operator ni ibintu vy'akanya gafise TTL ngufi kuri relay. aba operator batangaza ibisabwa vyabo nk'ibintu bisimburwa, bigatuma ama wallet asanga kandi agereranya aba operator ata nomero nkuru

iyi ngengabikorwa isobanura ko ama wallet adakeneye guhuza bihoraho — arashobora kwigumya hanze igihe ikintu cose agasubira bakasubirayo bavumviriza ibintu kuva kuri relay iyo ari yo yose ibifise. aba operator bashobora gushikwako biciye kuri relay iyo ari yo yose bakurikirana, kandi guhitamwo relay ni icemezo c'ishirwaho, si igengwa na amategeko ya protocol

## reserves na collateral

reserves zibikwa mu UTXO ifise igiciro kingana canke kirenze igisumba c'amasezerano ya ledger, ishobora gukoreshwa na benshi mu bagize quorum, igasubira ku operator inyuma y'ikiringo kinini

collateral ni umutungo bwite w'operator, wishizwe kandi wugawe ku ma ledger y'abagize quorum. buri mugize afise deposit ya collateral operator aduza kandi yuga mu kiringo kigenwe. amasezerano yose ya ledger agabanywa na kabiri ya collateral ntoya kuruta izindi zifatwa n'umugize uwo ari we wese, kandi ikiringo ca quorum kigabanywa n'igihe gigufi kuruta ibindi c'ugufunga. ibi vyerekana ko urubuga rwa collateral ruhoraho rufise ibihagije kugira ngo rutwikire ihinduka ry'ubuziganya. deposit rimwe rya collateral rirashobora gushigikira ama ledger vyinshi kugira ngo umutungo ukoreshwe neza, naho ama wallet akwiye guhitamwo aba operator bafise inkomoko za collateral zitasubiranya

amasezerano ashimikwa igihe ibisabwa bishasha vy'ifadanyo canke ama invoice bigirwa. operator ntashobora gukora ibisabwa canke ama invoice vyotuma amasezerano yose ya ledger arenze reserves canke arenze kabiri ya collateral ntoya kuruta izindi, ikintu ari co kitoya

## quorum

aba operator basaba abandi ba operator kujya mu quorum ryabo mu gutereka no gufunga collateral ku ledger y'umugize. icifuzo kirimo isezerano rya collateral (igiciro n'igihe c'ugufunga) n'ibisabwa vy'umugize: amafaranga mato ama deposit ku ledger akwiye kwuzuza. buri mugize akwiye gukoresha ledger yiwe kandi ashobora gufata collateral ya operator aramutse yemejwe ko adahuza. abagize barashiraho imbibe z'amafaranga mu gihe bari mu quorum — operator ntashobora gukora ama deposit afise amafaranga ari munsi y'ayo umugize akomeye kuruta abandi asaba, bikarinda abagize gusigara bafise amasezerano adatanga inyungu inyuma y'ihinduka ry'ubuziganya

quorum rimaze gushingwa, reserves zihindurwa zija mu UTXO nshasha ya multisig. abagize basinyira hamwe amakuru mashasha akwiye kandi bakagira uruhara mu kugarura iyo operator asinyiye amakuru adahuza. ama quorum manini yongera gusaba ivugana ariko agabanya ingorane z'operator, yongera kuboneka, kandi agatuma ubwumvikane bw'uburiganya bugorana kandi bukaguruka. ama wallet akwiye guhitamwo ama quorum manini

## gukingira ku butunzi

amategeko ya protocol asimbura gusohoka ukwigeneye n'ugukingira ku butunzi. abagize ba quorum bafise impamvu zuzuye zo gukora ku bw'ubuhemu. mu bikorwa bisanzwe baronka amafaranga mato ku collateral, ariko mu gihe c'ingeso zishobora kwemezwa zitahuza barashobora gufata collateral yose ya operator ku ledger yabo

iyo wallet ikeka ko hariho uguheza, irashobora gushira icifuzo ku bagize ba quorum biciye mu buryo bw'icese. umugize ashira hash y'icifuzo ku ledger yiwe ku giciro gito, bigatuma haba icabona gifise inkomoko. operator aramutse adakoze icifuzo, umugize afise icabona hamwe n'impamvu y'ubutunzi yo gutangura impari

uburiganya bw'ama invoice ya lightning bukurikira igishusho kimwe co gukingira. operator azi niba preimage yakiriwe, ariko wallet ntiizi. ariko uwishura uwo ari we wese arashobora gutanga preimage ku wallet. ubwiba bumwe bwemejwe butangura impari, gufata reserves, no gufata collateral. impembo yo kwiba ihererekanya imwe iragarukanijwe, ariko ingorane irahindura kubaho, bigatuma ubwiba bwa lightning butagira inyungu mu butunzi naho bidashobora kwemezwa mu buryo bwuzuye ata bufasha bw'uwundi

ingorane yo kubura ku guheza no ku gukingira kwa lightning ni ubwumvikane bwose bwa quorum. amategeko ya protocol ntashobora gukingira ku quorum ryumvikana kwiba, ariko urubuga rwa collateral rwerekana ko ubwumvikane ruguruka kuruta ivyo rwinjiza. ubwazi bw'igisata bugatuma ama wallet n'isoko ry'ugusanga bimenya ingengabikorwa z'ama quorum zitaringaniye mbere yo gutereka amahera

## igihe

igihe nyakuri ripimwa ku rwego rw'ishingiro. urugero ntirushobora kurenze igitigiri gikwiye c'amashimikiro kugira ngo bibanguke mu gihe c'ihinduka ry'umunyororo

aho urugero runini rusabwa dukoresha urutonde rw'imvo. ledger y'ubwandiko ni urunigi rwa merkle. buri hakuru mashasha yemeza ko yakozwe inyuma y'amakuru yose ayabanjirije, ariko ntitanga icemeza ku makuru ari hanze y'urunigi. kugira ngo dushinge urutonde rushwiranye, dusaba ko amasinya y'hamwe akuramo hash y'amakuru mashasha y'ubu kuva ku ledger y'uwusinye. iyo hash ikinjira mu hash y'amakuru y'ubu, ikaba igice c'urunigi hamwe n'igice c'izindi runigi zose operator wa ledger asinyira, bigatuma haba urubuga rw'imvo. ibi ntibishobora kwemeza igihe mu buryo bwuzuye, ariko birashobora kwemeza ko amakuru kanaka yakozwe mu rutonde runaka

## ibimenyamenya vy'uburiganya

turashobora kwemeza ubwoko butandukanye bw'uburiganya mu gushikiriza amakuru yakozwe mu rutonde rutari rwo. aho amakuru adashirwa mu bikorwa bisanzwe vy'igisata, arashobora gucishwa mu buryo bwo gukora ibikorwa birimo hash y'icabona. amaze gushirwa mu makuru mashasha asinywe na operator, icabona gishirwa ahagaragara ko cakozwe ahantu hatari ho mu rutonde:

- operator, amaze gusaba gushira amahera ku deposit yoherejwe kuri umunyororo ku cyerekezo kanaka, asinyira amakuru mashasha ya ledger adafise ifadanyo ikwiye, ariko afise urunigi rwerekana hash y'ama block irenze igitigiri c'amashimikiro yemerewe imbere y'ifadanyo

- operator, amaze gukora invoice ya lightning ku bw'ideposit, asinyira amakuru mashasha ya ledger ataraduza ku deposit naho preimage yashizwe ahagaragara mu runigi

- isinya ry'hamwe ryemeza ko hash ya ledger y'ubu ari imwe iza imbere y'iyo hash yabo y'inyuma mu runigi

- umugize wa quorum ya ledger y'impari yari akora ariko ntiyakoze mu buryo buhuza n'ibimenyamenya vy'uburiganya mu gitigiri c'ama block kigenwe

- gusinya canke gusinyira hamwe amakuru mashasha ya ledger adahuza

icabona c'uburiganya kigizwe n'ibimenyamenya n'urunigi rw'imvo ruhuza hash yashizwe na ledger y'uwagiriwe. urunigi ni urutinanwa rw'amakuru mashasha yasinyweko hamwe, buri kimwe kirimo member_ledger_hash kuva ku ledger y'uruhererekane rwabanje. abagenzuzi bakurikira urunigi ata gurondera, bemeza buri ruhererekane ko ari amakuru masinywe, kandi ko hash y'icabona ihuza amakuru yashizwe

## kugarura

ledger kimaze kubura canke kudahuza, abagize ba quorum barashobora gukora isubirayo rya ledger bafatiye ku makuru mashasha y'inyuma ahuza. bakwiye gushinga quorum nshasha no gutanga ibimenyamenya vya collateral. abagize bategerezwa gukorana kugira ngo bakoreshe reserves z'imbere baje ku tombola y'ama ledger bishasha bishoboka. uwatsinze iyi tombola ashira amakuru mashasha y'ukwakira ku runigi rwiwe, abandi bakashira amakuru mashasha y'ukwemera. ama wallet aguma atwerekeza ku ledger kimwe, akemera gusa inyishu zisinywe na quorum. rimwe na rimwe, kandi iyo inyishu zidafise isinya rya quorum ryitezwe, wallet ikwiye kubaza igisata no gusubiramo amakuru mashasha ya ledger kugira ngo imenye ihinduka mu buziganya

iyo ukudahuza kumeze nk'impanuka (nk'akarorero, ledger kitaboneka mu gitigiri kanaka c'ama block) ihinduka ry'ubuziganya rikwiye kuba ryubaha: gusa igiciro ca reserves gikenewe kugira ngo kitwikire amasezerano ya ledger gishirwa kuri tombola, n'isigaye isubizwa ku rufunguzo rw'icese rwa operator. ubutegetsi bwa collateral ntibuhinduwe

iyo icabona c'ukudahuza cihari, igiciro cirenze reserves zikenewe kigabanwa neza hagati y'abagize ba quorum, na collateral ku ma ledger y'abagize ishobora gufatwa

## ubuzima bw'igisata

igitero kimwe coroshe ni ugushinga ibirwa vy'aba operator b'ubwumvikane. inyuma yo gushinga amasezerano manini ku ma ledger vyabo, bakorana gusohoka, biba amahera arenze collateral bahomvye. igisata kirashobora kwikingira ibi, kiretse mu turere aho agaciro k'imbere karenze collateral zihuza n'igisata kitari mu bwumvikane. ingero ndende za collateral n'ama quorum manini kandi atandukanye bigabanya amahirwe y'ayo maboko gushingwa, ariko arashobora gushingwa namabomu kandi ntidushobora kwitega ko buri wallet isuzuma igisata cose. ahubwo isoko ry'ugusanga rikwiye gutangaza ibigereranyo vy'ukwemera kw'aba operator bishingiye ku busesanguzi bw'igishusho nk'ingengabikorwa zo gutorera ibihembo

## umwanzuro

dushikiriza igisata ca collateral gisaba ubwumvikane kugira ngo bibe, ariko ubwumvikane burushiriza kongereza collateral iri mu ngorane kuruta uko burushereza kongereza agaciro ko kwibwa. dukoresha iki gisata kugira ngo dutekanishe ama ledger y'ubwandiko bishigikiwe na reserves zuzuye. aya ma ledger akorera amakonti ku bwa wallet zitari ku murongo mu guhana amafaranga yahurweko mbere. ibintu vya ledger bishigikira ibisabwa vyo gukoresha vya miniscript bihagije ku bw'amasezerano yoroshe. igisata gikura hafi mu buryo bw'uburinganire, bigatuma igisata kinini gitanga imiliyari y'ama wallet n'ibicuruzwa birenze ibisata bisanzwe vy'amahera
