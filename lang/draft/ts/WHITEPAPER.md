# bitcoin deposits
## xianakanyiso

muxaka lowunene wa mali ya xieleketironiki wa munhu-na-munhu wu ta pfumelela ku hakela ka inthanete ku rhumeriwa hi ku kongoma ku suka eka xiphemu xin'we ku ya eka xin'wana hi ku hatlisa na hi ku tilunghisela loku tsongo. lightning network yi nyika xiphemu xa nhlamulo, kambe mabuyelo ya nkoka ma lahleka loko xiphemu xa vunharhu lexi tshembekaka xi laveka ku lawula xiyimo eka vito ra wena. hi bumabumela nhlamulo ya xiphitiphiti lexi hi ku tirhisa ma ledger lama tiyisekisekaka na vunete bya collateral. operator va kandziyisa mimpfunyeto ya ma ledger eka vanghana va vona, va tumbuluxa rekhodho ya tiakhawunti leyi kambisekaka. wallet ti kandziyisa vumbhoni bya ku ka ku tshembeki eka vanghana volavo, lava tiyisekisaka leswaku ledger yi hlayisa operator wa ntiyiso. ku huma hi ku titsongahata ku siveriwa hi xitshembiso xa leswaku timali ti tshama ti kumeka loko nhlengeletano yi ha ri kona. hi fika eka nhlengeletano leyi nyikelaka ntirhelo wa ku hlayisa mali yo tenga, yi papalata tihakelelo to sungula, yi kota ku amukela tihakelelo loko munhu a nga ri eka inthanete, naswona yi kula hi ku tiyimela eka xiyenge xa le hansi

## nhlamuselo

bitcoin deposits yi kongomisa ku nyika timali leti lawulekaka hi xilotlelo leti hatlisaka na leti kulaka, hi ku tshembeka, handle ka tcheini. ntirho wa le tcheini wu kula na nhlayo ya ma ledger na ku hatlisa ka ku hundzuluxa reserves. ku famba ka swo tirhiwa swi kula hi ku tlula ku ya xitalo na nhlayo ya ma ledger eka nhlengeletano, ku endla leswaku timiliyone ta swo tirhiwa hi nkama swi koteka eka tiriliyoni ta wallet

ku ni ku cinca loku kombisiwaka:
- ku hava ku huma hi ku titsongahata: loko operator va tsandzeka timali ti tshama enhlengeletanweni
- ku hava xihundla: ku tiyisekisiwa ku lava ku vonakala
- ku va kona loku yimaka: deposit yi va kona ntsena ku fana na operator. wallet ti fanele ti hangalasa timali ku engetela ku va kona

hi languterile leswaku ntokoto wa wallet wu ta fana na xiyenge xa le hansi lexi hatlisaka, wu ri na ikhonomi ya ku hakela leyi fanaka na lightning network

## ma ledger

ledger i nhlovo leyi nga hundzuluxekiki ya mimpfunyeto, leyi nga na hash ya mpfunyeto wo hundza naswona yi sayiniwile hi operator wa ledger. tinxaka to hambana ta mpfunyeto ti ni milawu yo hambana leyi lawulaka loko na ndlela leyi ti nga tirhisiwaka ha yona. ma ledger ma tihlamusela hi toxona, mimpfunyeto ya tona yi kumeka eka vaaki naswona yi nga kanetseki, ku pfumelela munhu wihi na wihi ku kambisisa ku landzela milawu

ma ledger ma ni operator un'we loyi a tirhaka, kambe ma hlayiseka hi ku pfunanana hi mesh. operator wihi na wihi a nga tumbuluxa yin'we, kambe loko va nyamalala kumbe va ka va tshembeki operator wo hambana u ta averiwa, swin'we na reserves. operator loyi a tirhaka sweswi u tiveka hi pubkey leyi tirhisiweke ku sayina mpfunyeto wa vumbirhi lowu sayiniweke wa sweswilexikona

## deposits

deposit i akhawunti leyi tiyeke leyi nga rhumela na ku amukela timali, leyi lawulekaka hi miniscript. eku pfuriweni ka yona xedyulo ya tihakelelo yi vekiwa, hambi na leswaku ku amukela timali ku lava xikombelo lexi sayiniweke hi wallet kumbe ku ka ku lavi. operator u fanele a pfumelela ku hundziseriwa exikarhi ka deposits eka ledger leyi fanaka hambi na ku huma eka tcheini. va fanele va pfumelela deposits ku hakela lightning invoices

swi le ka ku titsongahata ka operator ku tumbuluxa swinikelelo swa ku hakisa eka tcheini kumbe lightning invoices eka vito ra deposit. loko va endla tano, leswi swi fanele swi sayiniwana hi xirho xa quorum, naswona wallet yi fanele yi tiyisekisa sayino leyi. swinikelelo na invoices a swi ri xiphemu xa ledger, kutani i vutihlamuleri bya wallet ku tiyisekisa tisayino na ku ti hlayisa tanihi vumbhoni

## tihakelelo

ku hundzisiwa exikarhi ka deposits, eka tcheini, na hi lightning ku ni tihakelelo leti hakelwaka eka operator wa ledger. ku ni na tihakelelo leti tirhisiwaka nkarhi na nkarhi eka timalana na nkarhi lowu vuriweke. hinkwato ti bumabumeriwa loko deposit leyintshwa yi pfuriwa. tihakelelo ti nga hundzuluxiwa endzhaku ka nhlayo leyi vuriweke ya tibloko, hi ku nyikiwa xitiviso xa tibloko lexi vuriweke na le ka mpimo wa phesente ya ku cinca loku bumabumeriweke eku pfuriweni. quorum yi nga ala ku sayina swin'we mimpfunyeto leyi tumbuluxaka xiyimo lexi nga pfunikiki lexi va nga ta va na vutihlamuleri bya xona

## ku hundzisiwa

xivumbeko xa masungulo xa ku hundzisiwa i ntirho wa magoza mambirhi exikarhi ka deposits timbirhi eka ledger leyi fanaka: deposit yi humesa xikombelo xa ku rhumela timali. loko ku ri na timali leti ringaneke, xilotlelo xa timali na xiyimo xa ku tirhisa xi engeteriwile eka ledger. loko xiyimo xa ku tirhisa xi hetisekile ku nga se fika nkarhi, timali ti suka eka murhumeri ti ya eka muamukeri ku susiwa hakelelo ya operator. loko nkarhi wu fika, xilotlelo xi ntshunxiwa, ku susiwa hakelelo leyitsongo ya operator. hi tiyimo ta ku tirhisa ta miniscript, leswi swi ringanela ku pfumelela deposit yihi na yihi ku nyika vukorhokeri bya timbilichi na mali yo tenga eka deposits tin'wana eka ledger leyi fanaka

## lightning

operator lava nga na ndhawu ya lightning va nga pfumelela deposits ku rhumela na ku amukela hi lightning network. loko deposit yi kombela lightning invoice, operator u yi tumbuluxa hi ku tirhisa node ya yena ya lightning, a kombela swirho swa quorum ku yi sayina swin'we ku kombisa leswaku va tinyiketile ku xiyela deposit loko yi hakelwa. wallet yi fanele yi hlayisa invoice leyi sayiniweke swin'we tanihi vumbhoni. loko deposit yi kombela ku hakela lightning invoice, operator u hakela hi ku tirhisa node ya yena ya lightning naswona a debita deposit endzhaku ka ku kuma preimage

loko muhakeli na muhakelwi va ri deposits eka operator un'we, operator a nga hetisa ntirho wa le ndzeni handle ko tirhisa lightning, a xiyela na ku debita deposits leti faneleke hi ku kongoma. leswi swi papalata tihakelelo ta ku fambisa na tindlela ta ku tsandzeka kasi ku hlayisiwa swa ku hakisela swi ya emahlweni hi ku fana

## courier

swikombelo swa ku hundziseriwa swi fambisa timali ntsena exikarhi ka deposits eka ledger leyi fanaka. ku fambisa timali ku tsemakanya ma ledger, wallet ti tirhisa courier — vukorhokeri lebyi nga na deposits eka ma ledger yo tala naswona byi rhwala ku hundzisiwa exikarhi ka tona. courier u kandziyisa vuswikoti na tihakelelo ta ndzhawu nyin'wana na nyin'wana ta ledger eka relay. loko wallet yi lava ku rhumela ku suka eka ledger A ku ya eka ledger B, yi tumbuluxa xilotlelo xa ku hundzisiwa eka deposit ya courier naswona yi kombela leswaku courier a tumbuluxa xin'we ku suka eka deposit ya yena eka ledger ya le ku fikiweni ku ya eka muhakelwi. loko swilotlelo swombirhi swi vekiwile wallet yi paluxa preimage eka muhakelwi, loyi a hetisa ku hundzisiwa ku suka eka courier. loko yi paluxiwile, courier u tirhisa preimage leyi fanaka ku hetisa ku hundzisiwa ku suka eka murhumeri ku ya eka courier

loku i xivumbeko xa ntolovelo xa hash time-locked contract. hi languterile leswaku nkarhi wa courier wo huma wu ta va wu ri emahlweni hi ku tiya ku tlula wa ku nghenisa, ku tiyisekisa leswaku loko wallet yi nga paluxi, swilotlelo swombirhi swi hela naswona a ku na xiphemu lexi lahlekelwaka hi timali. a ku laveki ku tshemba ku tlula xitshembiso xa nkarhi lexi tirhisiwaka hi operator

courier va fanele va veka tihakelelo ta ledger nyin'wana na nyin'wana: fee_in na fee_out eka ledger yin'we na yin'we leyi va yi tirhelaka. wallet yi akanyela ndzhia ya ku durha tanihi fee_out eka xihlovo ku engeta fee_in eka ndzhawu yo fika. courier va nga hundzuluxa tihakelelo hi ku ya hi ledger hi ku ya hi mali yo tenga leyi kumekaka, va ringanyeta tipozixini ta vona hi ndlela ya ntumbuluko. wallet ti kuma courier hi ku tirhisa swikandziyiso swa vona eka relay naswona ti hlawula hi ku ya hi hakelelo, vuswikoti, kumbe ku khaveriwa

## vuhlanganisi

vuhlanganisi hinkwabyo exikarhi ka wallet na operator, na exikarhi ka operator, byi tirhisa nostr relay. mimpfunyeto ya ma ledger yi kandziyisiwa tanihi swiendlakalo leswi hlayisekaka leswi relay ti swi hlayisaka, ku tumbuluxa rekhodho leyi tshamaka leyi kambisekaka. swikombelo na tinhlamulo exikarhi ka wallet na operator i swiendlakalo swa nkarhi wo koma na TTL wo koma wa relay. operator va kandziyisa tindhawu ta vona tanihi swiendlakalo leswi siviwaka, ku pfumelela wallet ku kuma na ku pimanisa operator handle ka direktori ya le xikarhi

xivumbeko lexi xi vula leswaku wallet a ti lavi vuxokoxoko byo tshama -- ti nga ya handle ka inthanete nkarhi wo leha naswona ti vuya ti kuma hi ku tlangelisa swiendlakalo ku suka eka relay yihi na yihi leyi nga na swona. operator va nga fikeriwa hi ku tirhisa relay yihi na yihi leyi va yi langutaka, naswona ku hlawuriwa ka relay i xiboho xa ku tirhisiwa, ku nga ri xiboho xa layenisi

## reserves na collateral

reserves ti hlayisiwile eka UTXO leyi nga na xiyenge lexi ringanaka kumbe ku tlula ntsengo wa swikweleti swa ledger, leyi tirhisiwaka hi vuntsongo bya quorum, na ku tlhelela eka operator endzhaku ka nkarhi wo leha

collateral i mali ya operator hi yexe, leyi vekiweke na ku khiyiweke eka ma ledger ya swirho swa quorum. xirho xin'we na xin'we xi hlayisa deposit ya collateral leyi operator a yi hakelaka naswona a yi khiyela nkarhi lowu vuriweke. swikweleti hinkwaswo swa ledger swi pimisiwile eka kambirhi ka collateral lexitsongo xa xilotlelo lexi hlayisiweke hi xirho xihi na xihi, naswona nkarhi wa quorum wu pimisiwile eka nkarhi wo koma wo tiya wa xilotlelo. leswi swi tiyisekisa leswaku vunete bya collateral byi tshama byi ri na ku seketela loku ringaneke ku khanela ku hundzisiwa ka vuhlayisi. deposit ya collateral leyi fanaka yi nga seketela ma ledger yo tala ku antswisa ku tirhisiwa ka mali, hambi leswi wallet ti fanele ti rhandza operator lava nga na swihlovo swa collateral leswi nga fananeki

swikweleti swi tirhisiwile loko ku tumbuluxiwa swinikelelo swa ku hakisa leswintshwa kumbe invoices. operator a nge tumbuluxi swinikelelo kumbe invoices leti nga ta susumeta swikweleti hinkwaswo swa ledger ku tlula reserves kumbe ku tlula kambirhi ka collateral lexitsongo xa xilotlelo, swifanele ku va swo hunguta

## quorum

operator va kombela operator van'wana ku joyina quorum ya vona hi ku veka na ku khiya collateral eka ledger ya xirho. xikombelo xi katsa ku tinyiketela ka collateral (xiyenge na nkarhi wa xilotlelo) na tindhawu ta xirho: mixedyulo ya le hansi ya tihakelelo leyi deposits eka ledger ti faneleke ku yi fikelela. xirho xin'we na xin'we xi fanele xi tirha ledger ya xona naswona xi nga teka collateral xa operator loko operator a kombisiwile ku ka a landzeli. swirho swi veka mpimo eka mixedyulo ya tihakelelo hi nkarhi wa vuswirho bya vona bya quorum — operator a nge pfuri deposits na tihakelelo leti nga le hansi ka mixedyulo ya le hansi ya xirho xa le ka mpimo wo tiya, ku sirhelela swirho ku suka eka ku amukelela swikweleti leswi nga pfunikiki endzhaku ka ku hundzisiwa ka vuhlayisi

loko quorum yi simekiwile, reserves ti hundzuluxeriwa eka UTXO leyintshwa ya multisig. swirho swi sayina swin'we mimpfunyeto leyi faneleke naswona swi nghenelela eka ku vuyeleriwa loko operator a sayina leswi nga landzeliki. quorum letikulu ti engetela ku tirhisana ka vuhlanganisi kambe ti hunguta xitshovo xa operator, ti engetela ku va kona, naswona ti endla leswaku ku pfumelelana ku va ku tika na ku durha. wallet ti fanele ti rhandza quorum letikulu

## ku sivela hi ikhonomi

layenisi yi sivela ku huma hi ku titsongahata hi ku sivela hi ikhonomi. swirho swa quorum swi khutaziwa hi ku kongoma ku lwisa ku ka ku tshembeki. hi nkarhi wa mintirho ya ntolovelo va kuma tihakelelo letitsongo eka collateral, kambe loko ku ri na mahanyelo lama nga landzeliki lama kombisekaka va nga teka collateral hinkwaxo xa operator eka ledger ya vona

loko wallet yi kanakana ku ka ku pfumeleriwa, yi nga ya emahlweni na xikombelo eka swirho swa quorum hi ku rhumeriwa loku tiyisekisiweke. xirho xi nghenisa hash ya xikombelo eka ledger ya xona hi hakelelo leyitsongo, ku tumbuluxa vumbhoni lebyi xiyeleke eka xivangelo. loko operator a tsandzeka ku tirhisa xikombelo, xirho xi ni vumbhoni na nxuvo wa ikhonomi ku sungula mphikizano

vukungundzwana bya lightning invoice byi landzela xivumbeko xin'we xa ku sivela. operator u tiva loko preimage yi amukeriwile, kambe wallet a yi tivi. hambiswiritano muhakeli wihi na wihi a nga nyika preimage eka wallet. ku tiyisekisiwa kun'we ka vukhamba ku sungula mphikizano, ku tekiwa ka reserves, na ku tekiwa ka collateral. mburho wa ku yiva ku hakela kun'we wu pimisiwile, kambe xitshovo xi kona ngopfu, ku endla leswaku vukhamba bya lightning byi ka byi ri na vutlhari bya ikhonomi hambi leswi byi nga kombisekiki hi ku hetiseka handle ka ku pfunana ka xiphemu xa vunharhu

ndlela ya ku tsandzeka eka ku siveriwa ka ku ka ku pfumeleriwa na ku siveriwa ka lightning i ku pfumelelana ka quorum hinkwayo. layenisi a yi nge sirheleli eka quorum leyi pfumelelanaka ku yiva, kambe vunete bya collateral byi tiyisekisa leswaku ku pfumelelana ku durha ku tlula leswi swi kumekaka. ku vonakala ka nhlengeletano ku pfumelela wallet na timarikete ta ku kuma ku tivisa swiakanyiwa swa quorum leswi kanakanyisaka ku nga se vekiwa timali

## nkarhi

nkarhi wa xiviri wu pimisiwa eka xiyenge xa le hansi. ku pfumeleriwaku a ku nge tluli nhlayo leyi twisisekaka ya tiyisekiso ku hlayisa ku tiya hi nkarhi wa ku hundzuluxiwa ka tcheini

laha ku pfumeleriwaku lokukulu ku lavekaka hi kona hi tshemba eka ku landzelelana ka xivangelo. ledger ya xikhiriphithografikhi i tcheini ya merkle. mpfunyeto wun'we na wun'we wu kombisa leswaku wu tumbuluxiwile endzhaku ka mimpfunyeto hinkwayo leyi nga ku sungula ka yona, kambe wu nga nyiki switshembiso hi vuxokoxoko byo huma handle ka tcheini. ku tumbuluxa ku landzelelana loku hangalasiweke, hi lava leswaku tisayino ta vumbirhi ti katsa hash ya mpfunyeto wa sweswilexikona ku suka eka ledger ya musayini wa vumbirhi. hash yoleyo yi nghenisiwile eka hash ya mpfunyeto wa sweswi, yi va xiphemu xa tcheini hambi na xa tintcheini tin'wana hinkwato leti operator wa ledger a ti sayinelaka, ku tumbuluxa vunete bya xivangelo. leswi a swi nge kombisi nkarhi hi ku hetiseka, kambe swi kota ku kombisa leswaku swiphemu swo karhi swa vuxokoxoko swi tumbuluxiwile hi ku landzelelana loku vuriweke

## vumbhoni bya vukungundzwana

hi nga kombisa tinxaka to hambana ta vukungundzwana hi ku paluxa vuxokoxoko lebyi tumbuluxiweke hi ku landzelelana loku hoxeke. laha vuxokoxoko byi nga katsiwi hi mintirho ya ntolovelo ya nhlengeletano, byi nga nghenisiwile hi ku tumbuluxana ntirho lowu katsaka hash ya vumbhoni. loko byi nghenisiwile eka mpfunyeto lowu sayiniweke hi operator, vumbhoni byi paluxiwa tanihi lebyi tumbuluxiweke eka ndhawu leyi nga landzeliki eka ku landzelelana:

- operator, a nyikelile ku xiyela deposit hi timali leti rhumiweke eka tcheini eka adirese leyi vuriweke, u sayina mpfunyeto wa ledger lowu nga katsiki ku xiyeriwa loku faneleke, kambe wu katsa tcheini leyi paluxaka hash ya bloko leyi tlulaka nhlayo ya tiyisekiso leti pfumeleriweke ku nga se xiyeriwa

- operator, a tumbuluxile lightning invoice eka vito ra deposit, u sayina mpfunyeto wa ledger lowu nga xiyelangiki deposit hambi loko preimage yi paluxiwile eka tcheini

- sayino ya vumbirhi leyi vulaka leswaku hash ya ledger ya sweswi yi va yin'we leyi nga le ku sunguleni ka hash ya vona ya le ndzhaku eka tcheini

- xirho xa quorum xa ledger leyi phikizaniweke lexi a xi tirha kambe xi nga tirhanga hi ku ya hi vumbhoni bya vukungundzwana le ka nhlayo ya tibloko

- ku sayina kumbe ku sayina swin'we mimpfunyeto ya ledger leyi nga landzeliki

vumbhoni bya vukungundzwana byi akiwa hi vumbhoni na tcheini ya xivangelo leyi hlanganisaka hash leyi nghenisiweke na ledger ya loyi a xanisiweke. tcheini i ku landzelelana ka mimpfunyeto leyi sayiniweke swin'we, wun'we na wun'we wu katsa member_ledger_hash ku suka eka ledger ya xihlanganisi xa le ku sunguleni. vatiyisekisi va famba hi tcheini handle ko lava, va tiyisekisa xihlanganisi xin'we na xin'we xi ri mpfunyeto lowu sayiniweke, na leswaku hash ya vumbhoni yi fana na data leyi nghenisiweke

## ku vuyeleriwa

loko ledger yi ka yi ha kumeki kumbe yi ka yi ha landzeli, swirho swa quorum swi nga tumbuluxa ku ya emahlweni ka vona ka ledger ku suka eka mpfunyeto wo hetelela lowu landzelaka. va fanele va simeka quorum leyintshwa na ku nyika vumbhoni bya collateral. swirho swi fanele ku pfunanana ku tirhisa output ya reserves ya le ku sunguleni ku yi yisa eka lothari ya tintcheini leti nga landzelaka. muhluri wa lothari leyi u engetela mpfunyeto wa ku teka eka tcheini ya yena, naswona van'wana va engetela ku nyiketa. wallet ti ya emahlweni ti kongomisa eka ledger leyi fanaka, ti amukela ntsena tinhlamulo leti sayiniweke swin'we hi quorum. nkarhi na nkarhi, na loko tinhlamulo ti nga ri na sayino ya vumbirhi leyi langutiweke, wallet yi fanele yi vutisa nhlengeletano na ku tlangelisa mimpfunyeto ya ledger ku tiva ku hundzuluxiwa ka vuhlayisi

loko ku ka ku landzeli ku vonaka ku ri ka xihoxo (xik., ledger yi ka yi ha kumeki hi nhlayo ya tibloko leyi vuriweke) ku hundzuluxiwa ka vuhlayisi ku fanele ku va ka ku xixima: ntsena xiyenge xa reserves lexi lavekaka ku khanela swikweleti swa ledger xi rhumeriwa eka lothari, naswona ku hundzuluxiwa ku tlherisiwa eka pubkey ya operator. ku lawula ka collateral a ku khumbekiwi

loko vumbhoni bya ku ka ku landzeli byi ri kona, xiyenge lexi tlulaka reserves leti lavekaka xi avisanisiwa hi ku ringana exikarhi ka swirho swa quorum, naswona collateral lexi hlayisiweke eka ma ledger ya swirho xi pfumeleriwile ku tekiwa

## rihanyo ra nhlengeletano

nhlaselo yin'we leyi olovelekaka i ku vumba tihlaru ta operator lava pfumelelanaka. endzhaku ko aka swikweleti leswikulu ku tsemakanya ma ledger ya vona, va pfunanana ku huma, va yiva timali leti tlulaka collateral lexi lahliweke. nhlengeletano yi nga tivikanya eka leswi, handle ka le tindhawini laha nkoka wa le ndzeni wu tlula collateral lexi hlanganisaka na nhlengeletano leyi nga pfumelelanangiki. swipimo swo tlakuka swa collateral na quorum letikulu leti hambanyeke ti hunguta ku koteka ka tixangu leti, kambe ti nga vumbiwa hi xikongorelo naswona a hi nge languterili leswaku wallet yin'we na yin'we yi kambisisa nhlengeletano hinkwayo. ematshan'weni timarikete ta ku kuma ti fanele ti kandziyisa swipimo swa vutihlamuleri bya operator hi ku ya hi swinanunananiso swa girafe swo fana na tialgorithimi ta prize-collecting

## mahetelelo

hi bumabumela nhlengeletano ya collateral leyi lavaka ku pfumelelana ku yiva, kambe ku pfumelelana ku engetela collateral lexi nga exikarhi ka xitshovo hi ku hatlisa ku tlula leswi swi engeteraka nkoka lowu nga yiviwaka. hi tirhisa nhlengeletano leyi ku sirhelela ma ledger ya xikhiriphithografikhi lama seketeriweke hi reserves hinkwato. ma ledger lama ma tirha tiakhawunti eka vito ra wallet leti nga handle ka inthanete hi ku hundzuluxeriwa tihakelelo leti bumabumeriweke. swivumbeko swa ledger swi seketela tiyimo ta ku tirhisa ta miniscript leti ringanelaka tikhontiraka ta masungulo ta smart. nhlengeletano yi kula hi ku tshinela ku ya xitalo, ku pfumelela nhlengeletano leyikulu ku nyika tibiliyoni ta wallet na nhlayo ya swo tirhiwa leyi tlulaka tinhlengeletano ta ku hakela ta ntolovelo
