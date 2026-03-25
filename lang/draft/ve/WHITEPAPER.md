# bitcoin deposits
## manweledzo

maitele a vhudziki ha vhathu vhavhili a tshelede ya elektroniki a nga konadzea uri mbadelo dzi rumelwe nga tshifhinga tshithihi u bva kha munwe muthu u ya kha munwe nga u tavhanya na hu si na u lugisela ho vhulahaho. lightning network i ita tshipida tsha thandululo, fhedzi vhubvo ha ndeme vhu a xelelwa arali hu tshi todea muthu wa vhuraru a fulufhedzeaho u langa vhuimo kha vhukati havho. ri dzinginya thandululo ya thaidzo iyi nga u shumisa ma ledger a khwathemedzeaho na webe ya collateral. operator vha hasela khwathisedzo dza ma ledger kha vhanwe vhashumisi, vha tshi khou sika rekhodo ya akhaunthu dzi kwathemedzeaho. wallet dzi hasela vhuphayela ha u sa fulufhedzea kha vhashumisi avho, vhane vha vhona uri ledger i langa operator wa vhulenda. u bva nga nthihi u fhatiselwa kha u fulufhedziswa ha uri tshelede i dzula i hone fhedzi arali netiweke i tshi kha di shuma. ri swika kha netiweke ine ya rumela mushumo wa u langa liquidity, ya iledza fees dza u thoma, ya kona u tanganya mbadelo musi i si kha inthanete, nahone ya gola nga ntle ha u elana na base layer

## mvulatswinga

bitcoin deposits i lavhelela u ita uri tshelede ine ya langwa nga khii i gidime nahone i gole, nga ntle ha u fulufhela, i si kha chain. mushumo wa on-chain u gola na tshivhalo tsha ma ledger na mbonelelo ya u shanduka ha reserves. throughput i gola nga ntha ha zwo linganaho na tshivhalo tsha ma ledger kha netiweke, izwo zwi ita uri milioni dza transekisheni nga sekhennde kha trillions dza wallet zwi konadzee

hu na u shandukana ho bulwaho:
- a hu na u bva nga nthihi: musi operator vha tshi kundelwa tshelede i dzula kha netiweke
- a hu na tshidzumbe: u khwathemedza zwi toda u bvisela khagala
- u vha hone ho katiho: deposit i vha hone sa operator. wallet dzi tea u phadalala tshelede u engedza u vha hone

ri lavhelela uri tshenzhemo ya wallet i do fana na base layer ya u gidima, i na ekonomi ya mbadelo i fanaho na lightning network

## ma ledger

ledger ndi chain ine ya sa shanduki ya khwathisedzo, ine ya vha na hash ya khwathisedzo ya phananda nahone ya sainwa nga operator wa ledger. mifuda yo fhambanaho ya khwathisedzo i na milayo yo fhambanaho i langaho uri i shumiswe lini na nga ndi. ma ledger a di talutshedza nga othe, khwathisedzo dzao dzi hone kha vhathu vhothe nahone dzi sa landulei, u konadzea munwe na munwe u sedza u tevhedza

ma ledger a na operator muthihi a re kha mushumo, fhedzi a langwa nga vhushaka ha mesh. operator munwe na munwe a nga sika nthihi, fhedzi arali a tshi nyalala kana a sa fulufhedzei operator muswa u do vhewa, na reserves. operator a re kha mushumo zwino u topiwa nga pubkey ye ya shumiswa u saina khwathisedzo ya tshifhinga tshi fhiraho ye ya sainwa nga vhuvhili

## deposits

deposit ndi akhaunthu yo khwathemelaho ine ya kona u rumela na u tanganya tshelede, i langwa nga miniscript. musi i tshi vulwa schedule ya fees i vhekanyiwa, na uri u tanganya tshelede zwi toda khumbelo ye ya sainwa nga wallet kana hai. operator u tea u tendela u fhirisana vhukati ha deposits kha ledger inthihi na u bva kha on-chain. vha tea u tendela deposits u badela lightning invoices

ndi kha operator u dzhia tsheo ya u sika dzinepho dza u badela on-chain kana lightning invoices kha vhukati ha deposit. arali vha tshi ita izwo, idzi dzi tea u sainwa nga murado wa quorum, nahone wallet i tea u khwathemedza signature iyi. dzinepho na invoices a dzi tshipida tsha ledger, ngauralo ndi vhudzifhinduleli ha wallet u khwathemedza signatures na u dzi vhulunga sa vhuphayela

## fees

u fhirisana vhukati ha deposits, on-chain, na nga lightning zwi na fees dzi badelwaho operator wa ledger. hu dovha ha vha na fees dzi shuwaho kha balances nga tshifhinga tsho bulwaho. zwothe zwi khou negurishiwa musi deposit ntswa i tshi vulwa. fees dzi nga shandulwa nga murahu ha tshivhalo tsho bulwaho tsha blocks, hu pfi tshivhalo tsho bulwaho tsha block dza tsevho na kha tshikalo tsha phesente ya u shandula tsho negurishwaho musi i tshi vulwa. quorum i nga hana u saina khwathisedzo dzine dza sika nyimele ine ya sa vhuyise ine vha nga vha vho dzifhindulela khayo

## u fhirisana

mvelelo ya fhasi ya u fhirisana ndi mushumo wa masia mavhili vhukati ha deposits mbili kha ledger inthihi: deposit i rumela khumbelo ya u rumela tshelede. arali hu na tshelede yo linganaho, muloko kha tshelede u na phasilitheo ya u shumisa u engedzwa kha ledger. arali phasilitheo ya u shumisa i tshi khunyeledzwa phanḓa ha tshifhinga tshi fhela, tshelede i fhira u bva kha murumeli u ya kha mutanganyi hu tshi suswa fee ya operator. arali tshifhinga tshi tshi swika, muloko u vhofhololwa, hu tshi suswa fee thukhu ya operator. na miniscript spending conditions, izwi zwi lingana u tendela deposit inwe na inwe u netshedza bridging na liquidity services kha deposits dzinwe kha ledger inthihi

## lightning

operator vha re na channel ya lightning vha nga tendela deposits u rumela na u tanganya kha lightning network. musi deposit i tshi humbela lightning invoice, operator u i sika nga lightning node yavho, a humbela mirado ya quorum u i saina u sumbedza uri vho dziimisela u kreditha deposit musi hu tshi badelwa. wallet i tea u vhulunga invoice iyi ye ya sainwa sa vhuphayela. musi deposit i tshi humbela mbadelo ya lightning invoice, operator u badela a tshi shumisa lightning node yavho a debitha deposit nga murahu ha u wana preimage

musi mubadeli na mutanganyi vhe deposits kha operator muthihi, operator a nga khunyeledza nga ngomu hu si na u fhirisa nga lightning, a tshi kreditha na u debitha deposits dzo teaho nga tshivhangaphanḓa. izwi zwi iledza fees dza u fhirisa na mathaidzo a tshi dzula zwi vhulungile zwa akhaunthu

## courier

khumbelo dza u fhirisana dzi fhirisa tshelede fhedzi vhukati ha deposits kha ledger inthihi. u fhirisa tshelede vhukati ha ma ledger, wallet dzi shumisa courier — tshumelo dzine dza fara deposits kha ma ledger o fhambanaho nahone dza rwala u fhirisana vhukati hadzo. courier u hasela capacity na fees dza ndivho ya ledger kha relay. musi wallet i tshi toda u rumela u bva kha ledger A u ya kha ledger B, i sika muloko wa u fhirisana kha deposit ya courier nahone i humbela uri courier a sike nthihi u bva kha deposit yavho kha ledger ya hune zwa ya hone u ya kha muwanisi. musi miloko yothe mivhili yo vhekanyiwa wallet i bula preimage kha muwanisi, ane a khunyeledza u fhirisana u bva kha courier. musi yo buliwa, courier u shumisa preimage iyo inwe u khunyeledza u fhirisana u bva kha murumeli u ya kha courier

uyu ndi muanyo wa ntolovelo wa hash time-locked contract. ri lavhelela uri tshifhinga tsha u fhela tsha courier tsha u bva tshi vhe phanḓa nga maanda ha tsha u dzhena, u vhona uri arali wallet i sa buli, miloko yothe i fhela nahone a hu na ane a xelelwa. a hu todi u fulufhela ho fhiraho u fulufhedziswa ha tshifhinga tsha u fhela ho langwaho nga operator

courier vha tea u vhea fees dza ledger: fee_in na fee_out kha ledger inwe na inwe ine vha i shumela. wallet i linganya mutengo wa nḓila sa fee_out kha tshiko na fee_in kha hune zwa ya hone. courier vha nga shandula fees nga ledger zwo ḓitika kha liquidity ine ya vha hone, vha tshi dzudzanya vhuimo havho nga vhudo. wallet dzi wana courier nga dzihaseledzo dzavho kha relay nahone dzi nanga zwo ḓitika kha fee, capacity, kana coverage

## vhudavhidzani

vhudavhidzani hothe vhukati ha wallet na operator, na vhukati ha operator, vhu shumisa nostr relay. khwathisedzo dza ma ledger dzi kandelwa sa zwithu zwi dzulaho zwine relay dzi zwi vhulunga, zwa sika rekhodo ya tshothe ine ya kona u kwathemedza. khumbelo na phindulo vhukati ha wallet na operator ndi zwithu zwa tshifhinga tshituku na TTL ya tshifhinga tshifhufhi kha relay. operator vha hasela mbekanyamushumo dzavho sa zwithu zwi fhatiwaho, u tendela wallet u wana na u vhambedza operator hu si na directory ya vhukati

tshanduko iyi i amba uri wallet a dzi todi khanekisheni dza tshothe -- dzi nga ya offline tshifhinga tsho fhelelaho nahone dza dovha dza gidima nga u bvela phanḓa na zwithu u bva kha relay inwe na inwe ine ya vha nazwo. operator vha nga swikelwa nga relay inwe na inwe ine vha i sedza, nahone u nanga relay ndi tsheo ya u vhea, a si tshilombo tsha protocol

## reserves na collateral

reserves dzi farwa kha UTXO ine ya vha na tshivhalo tshi linganaho kana tsho fhiraho summa ya zwo teaho zwa ledger, ine ya kona u shumiswa nga vhunzhi ha quorum, na fallback kha operator nga murahu ha tshifhinga tshilapfu

collateral ndi capital ya operator nga ene, yo vhewaho na u lokiwa kha ma ledger a mirado ya quorum. murado munwe na munwe u fara deposit ya collateral ine operator a i badela nahone a i lokha tshifhinga tsho bulwaho. zwo teaho zwothe zwa ledger zwi lomiwa kha tshivhili tsha collateral lock thukhu vhukuma ine ya farwa nga murado munwe na munwe, nahone tshifhinga tsha quorum tshi lomiwa kha tshifhinga tsha lokho tshifhufhi vhukuma. izwi zwi vhona uri webe ya collateral i na tsireledzo yo linganaho u gidisa u shandula custody. deposit inthihi ya collateral i nga tikedza ma ledger manwe u khwinisa u shumiswa ha capital, naho wallet dzi tea u takalela operator vha re na collateral sources dzi sa ovhalapiho

zwo teaho zwi langwa musi hu tshi sikwa dzinepho ntswa dza u badela kana invoices. operator a nga si sike dzinepho kana invoices dzine dza kakatela zwo teaho zwothe zwa ledger u fhira reserves kana u fhira tshivhili tsha collateral lock thukhu vhukuma, tshine tsha vha fhasi

## quorum

operator vha humbela operator vanwe u dzhenisa kha quorum yavho nga u vhea na u lokha collateral kha ledger ya murado. khumbelo i katela u dziimisela ha collateral (tshivhalo na tshifhinga tsha lokho) na mbekanyamushumo dza murado: schedule dza fees dza fhasi vhukuma dzine deposits kha ledger dzi tea u dzi swikelela. murado munwe na munwe u tea u shumisa ledger yavho nahone a nga dzhia collateral ya operator arali operator a tshi wanala a sa tevhedzi. mirado i bula milombo kha fee schedules tshifhingani tsha vhuima havho ha quorum -- operator a nga si vule deposits dzi na fees fhasi ha dza fhasi vhukuma dza murado, u tsireledza mirado kha u dzhia zwo teaho zwi sa vhuyisi nga murahu ha u shandula custody

musi quorum yo vhekanyiwa, reserves dzi shandulwa u ya kha UTXO ntswa ya multisig. mirado i saina khwathisedzo dza vhukona nahone i shela mulenzhe kha u vhuedzedza arali operator a tshi saina dzi sa tevhedzaho. quorum khulwane i engedza vhuleme ha vhudavhidzani fhedzi i fhungudza khombo ya operator, i engedza u vha hone, nahone i ita uri u kwamana zwi lemelele na u tura. wallet dzi tea u takalela quorum khulwane

## u thivhela nga ekonomi

protocol i fhata u bva nga nthihi nga u thivhela nga ekonomi. mirado ya quorum i tutuwedzwa tshivhangaphanḓa u lwisa u sa fulufhedzea. tshifhingani tsha mushumo wo dowaho vha wana fees thukhu kha collateral, fhedzi musi hu na vhupfiwa vhu sa tevhedzaho ho sumbedzwaho vha nga dzhia collateral yothe ya operator kha ledger yavho

musi wallet i tshi vhona u hanelwa, i nga gonya khumbelo kha mirado ya quorum nga u rumela kwo khwathemedzeaho. murado u vhea hash ya khumbelo kha ledger yavho nga fee thukhu, a tshi sika vhuphayela vhu re na vhushaka ha mushumo. arali operator a tshi kundelwa u ita khumbelo, murado u na vhuphayela na tutuwedzo ya ekonomi ya u thoma phambano

vhufhura ha lightning invoice hu tevhedza muanyo wuthihi wa u thivhela. operator u divha uri preimage yo tanganyiwa, fhedzi wallet a i divhi. naho zwo ralo mubadeli munwe na munwe a nga nea preimage kha wallet. vhutshivhi vhuthihi vho khwathemedzeaho vhu thoma phambano, u dzhiwa ha reserves, na u dzhiwa ha collateral. muvhuya wa u tswa mbadelo inthihi u na mulombo, fhedzi khombo ndi ya u fhela, zwi tshi ita uri u tswa ha lightning zwi sa divhali zwa ekonomi naho zwi sa koni u sumbedzwa nga ntle ha u thuswa nga munwe wa vhuraru

nyimele ya u kundelwa ya censorship na u thivhela ha lightning ndi u kwamana hothe ha quorum. protocol a i koni u tsireledza kha quorum ine ya shuma vhathihi u tswa, fhedzi webe ya collateral i vhona uri u kwamana zwi tura u fhira zwo wanwaho. u bvisela khagala ha netiweke zwi tendela wallet na makete a u wana u topola quorum structures dzi sa fulufhedzeiho phanḓa ha u vhea tshelede

## tshifhinga

tshifhinga tsho fhelelaho tshi ganwa kha base layer. tolerances a dzi koni u fhira tshivhalo tsho pfeseseaho tsha confirmations u vhulunga u dzula zwi tshimbidzea tshifhingani tsha chain reorganizations

hune tolerances khulwane dzi todiwa ri ḓitika kha u tevhekana ha tshunifhalo. ledger ya cryptographic ndi merkle chain. khwathisedzo inwe na inwe i sumbedza uri yo sikwa nga murahu ha khwathisedzo dzothe dzo i rangaho phanḓa, fhedzi a i fulufhedzisi tshithu nga ha mafhungo a si kha chain. u itela u fhaṱa u tevhekana ho phadalaho, ri toda uri co-signatures dzi katele hash ya khwathisedzo ya zwino u bva kha ledger ya musaini-ngae. hash yeneyo i dzheniswa kha hash ya khwathisedzo ya zwino, ya vha tshipida tsha chain na tshipida tsha chain dzothe dzine operator wa ledger a dzi sainelaho, ya sika webe ya tshunifhalo. izwi a zwi koni u sumbedza tshifhinga nga vhuḓalo, fhedzi zwi kona u sumbedza uri zwipiḓa zwinwe zwa mafhungo zwo sikwa nga u tevhekana kwo bulwaho

## vhuphayela ha vhufhura

ri kona u sumbedza mifuda yo fhambanaho ya vhufhura nga u bula mafhungo o sikwaho nga u tevhekana ku si kwone. hune mafhungo a sa dzheniswi nga mushumo wo dowaho wa netiweke, a nga tshinyiwa nga u sika mushumo u katelaho hash ya vhuphayela. musi yo dzheniswa kha khwathisedzo yo sainwaho nga operator, vhuphayela vhu buliwa sa vho sikwaho fhethu hu sa tevhedzaho kha u tevhekana:

- operator, o nephalaho u kreditha deposit nga tshelede yo rumelwaho on-chain kha adiresi yo bulwaho, u saina khwathisedzo ya ledger ine ya sa vhe na credit yo teaho, fhedzi i na chain ine ya bula hash ya block i fhiraho tshivhalo tsha confirmations tsho tendelwaho phanḓa ha credit

- operator, o sikaho lightning invoice kha vhukati ha deposit, u saina khwathisedzo ya ledger ine ya sa kredithi deposit naho preimage yo buliwa kha chain

- co-signature ine ya amba uri hash ya ledger ya zwino ndi ine ya ranga phanḓa ha hash yavho ya murahu kha chain

- murado wa quorum ya ledger yo phambaniswaho o vhaho a tshi shuma fhedzi a songo shuma u tevhedza vhuphayela ha vhufhura kha tshivhalo tsha blocks

- u saina kana u saina-ngae khwathisedzo dza ledger dzi sa tevhedzaho

vhuphayela ha vhufhura vhu na vhuphayela na chain ya tshunifhalo i kwamanaho hash yo dzheniswaho na ledger ya operator o salwaho mulandu. chain ndi mbuelano ya khwathisedzo dzo sainwaho nga vhuvhili, inwe na inwe i katelaho member_ledger_hash u bva kha ledger ya link ya phananda. vhakhwathemedzi vha tshimbila chain hu si na u toda, vha tshi khwathemedza uri link inwe na inwe ndi khwathisedzo yo sainwaho, na uri hash ya vhuphayela i fana na data yo dzheniswaho

## u vhuedzedza

musi ledger i si tsha wanala kana i sa tevhedzi, mirado ya quorum i nga sika u bvela phanḓa havho ha ledger u bva kha khwathisedzo ya u fhedzisela ye ya tevhedza. vha tea u vhea quorum ntswa na u nea collateral attestations. mirado i tea u shumisana u shumisa output ya reserves ya phanḓa kha lothari ya chain dza zwino dzine dza nga tevhela. muwini wa lothari iyi u engedza khwathisedzo ya u wana kha chain yavho, nahone vanwe vha engedza u nekedza. wallet dzi bvela phanḓa u amba na ledger inthihi, dzi tshi tanganya fhedzi phindulo dzo sainwaho nga quorum. nga tshifhinga tshothe, na musi phindulo dzi si na co-signature yo lavhelelwaho, wallet i tea u vhudzisa netiweke na u bvela phanḓa na khwathisedzo dza ledger u topola u shanduka ha custody

musi u sa tevhedza zwi tshi vhonala zwi tshinyadzo (eg, ledger i si tsha wanala tshivhalo tsho bulwaho tsha blocks) u shanduka ha custody zwi tea u vha na thonifho: fhedzi tshivhalo tsha reserves tsho teaho u badela zwo teaho zwa ledger tshi rumelwa kha lothari, nahone tshanduko i rumelwa kha pubkey ya operator. u langa collateral a zwi kwamei

musi vhuphayela ha u sa tevhedza vhu hone, tshivhalo tsho salaho kha reserves tsho teaho tshi kovhekanyiwa nga u lingana vhukati ha mirado ya quorum, nahone collateral ine ya farwa kha ma ledger a mirado i tendelwa u dzhiwa

## mutakalo wa netiweke

u lwa kwo leluwalaho ndi u fhaṱa zwilani zwa operator vha kwamananaho. nga murahu ha u fhaṱa zwo teaho zwihulwane kha ma ledger avho, vha shumisana u bva, vha tshi tswa tshelede i fhiraho collateral yo xelelwaho. netiweke i nga lwa na izwi, nga nnḓa ha hune ndeme ya nga ngomu i fhiraho collateral ine ya i kwamanya na netiweke i sa kwamaniho. collateral ratios dza ntha na quorum khulwane, dzo fhambanaho dzi fhungudza u konadzea ha mabaga aya u bvelela, fhedzi a nga itwa nga ndivho nahone a ri koni u lavhelela wallet inwe na inwe u sedza netiweke yothe. nthani hazwo makete a u wana a tea u bvisa metrics dza u dzifhindulela ha operator zwo ditika kha graph analyses sa prize-collecting algorithms

## magumo

ri dzinginya netiweke ya collateral ine ya toda u kwamana u tswa, fhedzi u kwamana zwi engedza collateral i re khomboni u gidima u fhira ndeme ine ya tea u tshwiwa. ri shumisa netiweke iyi u tsireledza ma ledger a cryptographic o tikedzwaho nga reserves dzo fhelelaho. ma ledger aya a shumela akhaunthu kha vhukati ha wallet dzi si kha inthanete hu tshi shandukiselwa fees dzo negurishwaho u ranga phanḓa. zwishumiswa zwa ledger zwi tikedza miniscript spending conditions dzo linganaho kha smart contracts dza fhasi. netiweke i gola tsini na u lingana, i tendela netiweke khulwane u nea billions dza wallet na tshivhalo tsha transekisheni tsho fhiraho netiweke dza mbadelo dza kale
