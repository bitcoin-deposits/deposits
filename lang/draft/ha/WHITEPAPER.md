# bitcoin deposits
## taƙaitawa

ingantaccen tsarin kuɗin lantarki na takwara-zuwa-takwara zai ba da damar aika biyan kuɗi kai tsaye daga ɓangare ɗaya zuwa wani cikin sauri tare da ƙarancin shiri. lightning network ta samar da wani ɓangare na mafita, amma muhimman fa'idodi sun ɓace idan ana buƙatar amintaccen ɓangare na uku don sarrafa yanayi a madadinku. muna gabatar da mafita ga wannan matsala ta hanyar amfani da ledger masu tabbatarwa da yanar gizon collateral. operator suna watsa sabuntawar ledger zuwa takwarorinsu, suna ƙirƙirar bayanan asusu da za a iya bincika. wallet suna watsa shaidar rashin gaskiya zuwa waɗannan takwarorin, waɗanda ke tabbatar da cewa ledger yana kiyaye operator mai gaskiya. fita ta ɓangare ɗaya an maye gurbinsa da garantin cewa kuɗaɗe suna nan muddin hanyar sadarwar tana nan. mun isa ga hanyar sadarwa da ke ba da wakiltar kula da ruwa, guje wa kuɗin fara aiki, iya karɓar biyan kuɗi ba tare da haɗin yanar gizo ba, kuma tana girma ba tare da dogaro da matakin tushe ba

## gabatarwa

bitcoin deposits na nufin samar da kuɗaɗe masu sauri kuma masu girma waɗanda maɓalli ke sarrafa su, ba tare da amana ba, a wajen sarƙar. ayyukan kan sarƙar suna girma tare da yawan ledger da yawan juyawar reserves. ƙarfin aiki yana girma ɗan sama da layi tare da yawan ledger a cikin hanyar sadarwar, wanda ke sa miliyoyin ciniki a kowace daƙiƙa a cikin tiriliyan wallet ya zama mai yiwuwa

akwai musayar da aka bayyana a fili:
- babu fita ta ɓangare ɗaya: lokacin da operator suka gaza kuɗaɗe suna ci gaba a cikin hanyar sadarwar
- babu sirri: tabbatarwa tana buƙatar gaskiya
- samuwa na ɗan lokaci: deposit tana nan kamar yadda operator yake. wallet ya kamata su rarraba kuɗaɗe don ƙara samuwa

muna sa ran gogewar wallet ta yi kama da matakin tushe mai sauri, tare da tattalin arzikin biyan kuɗi mai kama da lightning network

## ledger

ledger sarƙar sabuntarwa ce da ba za a iya canzawa ba, wanda ke ɗauke da hash na sabuntawar da ta gabata kuma operator ya sa hannu a kansa. nau'o'in sabuntarwa daban-daban suna da ƙa'idoji daban-daban da ke jagorantar lokacin da yadda za a iya amfani da su. ledger suna bayyana kansu, sabuntawarsu suna samuwa ga jama'a kuma ba za a iya musantawa ba, wanda ke ba kowa damar kimanta daidaituwa

ledger suna da operator ɗaya mai aiki, amma haɗin gwiwa ne ke kula da su a cikin hanyar sadarwar. kowanne operator zai iya ƙirƙirar ɗaya, amma idan sun ɓace ko suka zama marasa gaskiya za a sanya wani operator daban, tare da reserves. operator mai aiki a halin yanzu ana gane shi ta maɓallin jama'a da aka yi amfani da shi wajen sa hannu a sabuntawar haɗin gwiwa ta ƙarshe

## deposit

deposit ita ce asusu mai ɗorewa wanda zai iya aika da karɓar kuɗaɗe, miniscript ke sarrafa shi. a lokacin buɗewa ana kafa jadawalin kuɗin sabis, da kuma ko karɓar kuɗaɗe yana buƙatar buƙatar da wallet ya sa hannu. dole ne operator ya ba da damar canja wuri tsakanin deposit a kan ledger ɗaya da kuma fita ta kan sarƙar. ya kamata su ba da damar deposit ta biya takardar kuɗin lightning

yana cikin ikon operator ya ƙirƙirar tayin tallafi a kan sarƙar ko takardar kuɗin lightning a madadin deposit. idan sun yi haka, ya kamata memba na quorum ya sa hannu a kansu tare, kuma wallet ya kamata ya tabbatar da wannan sa hannun. tayayyun da takardun kuɗi ba ɓangare ne na ledger ba, don haka alhakin wallet ne ya tabbatar da sa hannun kuma ya ajiye su a matsayin shaida

## kuɗin sabis

canja wuri tsakanin deposit, a kan sarƙar, da ta lightning suna da kuɗin sabis da ake biya wa operator na ledger. akwai kuma kuɗin sabis da ake cajin zaman kuɗi lokaci-lokaci tare da lokaci da aka ƙayyade. duk ana yin ciniki a kansu lokacin da aka buɗe sabuwar deposit. za a iya canza kuɗin sabis bayan adadin tubalan da aka ƙayyade, tare da sanarwar tubalan da aka ƙayyade kuma a cikin iyakar kashi na daidaitawa da aka yi ciniki a kansa lokacin buɗewa. quorum na iya ƙin sa hannu a kan sabuntarwa da ke haifar da yanayi mara riba wanda za su iya zama masu alhakinsa a ƙarshe

## canja wuri

tsarin asali na canja wuri shine aiki mai matakai biyu tsakanin deposit biyu a kan ledger ɗaya: deposit tana fitar da buƙatar aika kuɗaɗe. idan akwai isassun kuɗaɗe, kulle a kan kuɗaɗen tare da sharaɗin kashewa ana ƙara shi zuwa ledger. idan an cika sharaɗin kashewa kafin lokacin ƙarewa, kuɗaɗe suna tafiya daga mai aikawa zuwa mai karɓa ban da kuɗin sabis na operator. idan lokacin ƙarewa ya cika, ana sake sakin kullen, ban da ƙaramin kuɗin sabis na operator. tare da sharuɗɗan kashewa na miniscript, wannan ya isa ya ba kowanne deposit damar samar da gadoji da ayyukan ruwa ga sauran deposit a kan ledger ɗaya

## lightning

operator da ke da tashar lightning na iya ba da damar deposit ta aika da karɓa ta hanyar lightning network. lokacin da deposit ta buƙaci takardar kuɗin lightning, operator yana ƙirƙirar ta ta hanyar lightning node ɗinsu, yana roƙon membobin quorum su sa hannu tare don tabbatar da cewa sun jajirce wajen ƙara kuɗi ga deposit bayan biyan kuɗi. wallet ya kamata ya ajiye wannan takardar kuɗin da aka sa hannu tare a matsayin shaida. lokacin da deposit ta buƙaci biyan takardar kuɗin lightning, operator yana biya ta hanyar lightning node ɗinsu kuma yana rage kuɗi daga deposit bayan samun preimage

lokacin da mai biya da mai karɓa duka deposit ne a kan operator ɗaya, operator na iya daidaita cikin gida ba tare da wucewa ta lightning ba, yana ƙara da ragewa daga deposit kai tsaye. wannan yana guje wa kuɗin wucewa da matsalolin hanya yayin da yake kiyaye garantin lissafi iri ɗaya

## courier

buƙatun canja wuri suna motsa kuɗaɗe ne kawai tsakanin deposit a kan ledger ɗaya. don motsa kuɗaɗe a tsakanin ledger, wallet suna amfani da courier — ayyukan da ke riƙe da deposit a kan ledger da yawa kuma suna ɗaukar canja wuri a tsakaninsu. courier yana talla da ƙarfin iya da kuɗin sabis na kowanne ledger a kan relay. lokacin da wallet yana son aika daga ledger A zuwa ledger B, yana ƙirƙirar kulle canja wuri zuwa deposit na courier kuma yana buƙatar courier ya ƙirƙira ɗaya daga deposit ɗinsa a ledger da ake nufi zuwa ga mai karɓa. da zarar an kafa kullaye biyu, wallet yana bayyana preimage ga mai karɓa, wanda ke kammala canja wuri daga courier. da zarar an bayyana, courier yana amfani da wannan preimage ɗin don kammala canja wuri daga mai aikawa zuwa courier

wannan tsari ne na yau da kullun na hash time-locked contract. muna sa ran lokacin ƙarewa na fita na courier ya kasance da wuri fiye da na shigowa, don tabbatar da cewa idan wallet bai taɓa bayyanawa ba, kullaye biyu sun ƙare kuma babu ɓangaren da ya rasa kuɗaɗe. babu buƙatar amana bayan garantin lokacin ƙarewa da operator ke tilasta shi

courier ya kamata su saita kuɗin sabis na kowanne ledger: fee_in da fee_out ga kowanne ledger da suke yi wa hidima. wallet yana ƙididdige farashin hanya a matsayin fee_out a kan tushe da fee_in a kan inda ake nufi. courier na iya bambanta kuɗin sabis ta ledger dangane da ruwan da ke samuwa, suna daidaita matsayinsu ta dabi'a. wallet suna gano courier ta hanyar tallarsu a kan relay kuma suna zaɓa bisa ga kuɗin sabis, ƙarfin iya, ko ɗaukar nauyi

## sadarwa

duk sadarwa tsakanin wallet da operator, da kuma tsakanin operator, suna amfani da nostr relay. sabuntawar ledger ana buga su a matsayin abubuwan da suka dore waɗanda relay ke riƙewa, suna ƙirƙirar bayanan da za a iya bincika na dindindin. buƙatoci da amsoshi tsakanin wallet da operator abubuwan ɗan gajeren lokaci ne tare da TTL ɗin relay mai gajarta. operator suna talla da sharuɗɗansu a matsayin abubuwan da za a iya maye gurbinsu, suna ba wa wallet damar gano da kwatanta operator ba tare da babban littafin rajista ba

wannan tsarin yana nufin wallet ba sa buƙatar haɗin dindindin -- za su iya kashe su na tsawon lokaci kuma su dawo ta hanyar sake kunna abubuwan daga kowanne relay da ke da su. za a iya isa ga operator ta kowanne relay da suke kula da shi, kuma zaɓin relay yanke shawara ne na amfani, ba takurawa na yarjejeniya ba

## reserves da collateral

reserves ana riƙe su a cikin UTXO tare da adadi mai girma ko daidai da jimlar wajibcin ledger, mafi yawan quorum ne ke iya kashewa, tare da madadin ga operator bayan wani muhimmin lokaci

collateral ita ce jarin operator da kansa, wanda aka ajiye kuma aka kulle a ledger na membobin quorum. kowanne memba yana riƙe da deposit na collateral da operator ke ba da kuɗi kuma ke kullewa na tsawon lokaci da aka ƙayyade. jimlar wajibcin ledger an iyakance ta zuwa ninki biyu na ƙaramin kulle collateral da kowanne memba ke riƙe, kuma tsawon lokacin quorum an iyakance shi zuwa mafi gajeren lokacin kulle. wannan yana tabbatar da cewa yanar gizon collateral koyaushe tana da isassun goyon baya don ɗaukar canja wurin kula. deposit na collateral ɗaya na iya tallafawa ledger da yawa don inganta amfani da jari, kodayake wallet ya kamata su fi son operator da tushen collateral marasa haɗuwa

ana tilasta wajibcin lokacin ƙirƙirar sababbin tayayyun tallafi ko takardun kuɗi. operator ba zai iya ƙirƙirar tayayyun ko takardun kuɗi da za su tura jimlar wajibcin ledger sama da reserves ko sama da ninki biyu na ƙaramin kulle collateral ba, wanne ne ya fi ƙanƙanta

## quorum

operator suna roƙon sauran operator su shiga quorum ɗinsu ta hanyar ajiye da kulle collateral a kan ledger na memba. buƙatar tana ƙunshi alkawarin collateral (adadi da tsawon lokacin kulle) da sharuɗɗan memba: mafi ƙarancin jadawalin kuɗin sabis da deposit a kan ledger dole ta cika. kowanne memba dole ne ya gudanar da ledger ɗinsa kuma yana iya kwace collateral na operator idan an tabbatar da cewa operator bai bi ƙa'ida ba. membobi suna ƙayyade iyakoki a kan jadawalin kuɗin sabis a lokacin zaman quorum ɗinsu -- operator ba zai iya buɗe deposit tare da kuɗin sabis ƙasa da mafi tsananin ƙarancin memba ba, don kare membobi daga gadon wajibcin da ba su da riba bayan canja wurin kula

da zarar an kafa quorum, ana juyar da reserves zuwa sabon multisig UTXO. membobi suna sa hannu tare a kan sabuntarwa masu inganci kuma suna shiga cikin farfaɗo idan operator ya sa hannu a kan waɗanda ba su bi ƙa'ida ba. manyan quorum suna ƙara nauyin sadarwa amma suna rage haɗarin operator, suna ƙara samuwa, kuma suna sa haɗin kai ya fi wuya da tsada. wallet ya kamata su fi son manyan quorum

## hanawa ta tattalin arziki

yarjejeniyar tana maye gurbin fita ta ɓangare ɗaya da hanawa ta tattalin arziki. membobin quorum suna da kwarin gwiwa kai tsaye don yin aiki game da rashin gaskiya. a ayyukan yau da kullun suna samun ƙaramin kuɗin sabis a kan collateral, amma idan an tabbatar da halin da bai bi ƙa'ida ba suna da ikon kwace duk collateral na operator a kan ledger ɗinsu

lokacin da wallet ya zargi takurawa, yana iya ɗaga buƙatar zuwa membobin quorum ta hanyar isarwa tabbatacciya. memba yana shigar da hash na buƙatar a cikin ledger ɗinsa don ƙaramin kuɗin sabis, yana ƙirƙirar shaida mai tushen dalili. idan operator ya gaza aiwatar da buƙatar, memba yana da shaida da kuma kwarin gwiwa na tattalin arziki don fara takaddama

zamba ta takardar kuɗin lightning tana bin tsarin hanawa iri ɗaya. operator ya san ko an karɓi preimage, amma wallet ba ya sani. duk da haka kowanne mai biya na iya ba da preimage ga wallet. sata ɗaya da aka tabbatar tana haifar da takaddama, kwacewa na reserves, da kwace collateral. ladan satar biyan kuɗi ɗaya yana da iyaka, amma haɗarin yana da girma sosai, wanda ke sa satar lightning ta zama ba ta da hankali a tattalin arziki ko da ba za a iya tabbatar da ita ba a hukumance ba tare da haɗin gwiwar ɓangare na uku ba

yanayin gazawa na takurawa da hanawa ta lightning shine haɗin gwiwar quorum gaba ɗaya. yarjejeniyar ba za ta iya kare wa daga quorum da ta haɗa kai don sata ba, amma yanar gizon collateral tana tabbatar da cewa haɗin kai yana da tsada fiye da abin da ake samu. gaskiyar hanyar sadarwar tana ba wa wallet da kasuwannin gano damar gane tsarin quorum masu zargi kafin ajiye kuɗaɗe

## lokaci

lokaci na gaske ana aunawa a kan matakin tushe. iyakoki ba za su iya wuce adadi mai ma'ana na tabbatarwa ba don kiyaye kwanciyar hankali a lokacin sake tsara sarƙar

inda ake buƙatar manyan iyakoki muna dogaro da tsarin dalili. ledger na sirri sarƙar merkle ce. kowanne sabuntarwa yana tabbatar da cewa an ƙirƙira shi bayan duk sabuntarwar da suka gabace, amma ba ya ba da garantin bayanan da ke waje da sarƙar. don gina tsarin rarrabawa, muna buƙatar sa hannun haɗin kai su ƙunshi hash na sabuntarwa na ƙarshe daga ledger na mai sa hannu tare. wannan hash ana shigar da shi cikin hash na sabuntawar yanzu, yana zama ɓangare na sarƙar da kuma na duk sauran sarƙoƙin da operator na ledger ke sa hannu tare, yana ƙirƙirar yanar gizon dalili. wannan ba zai iya tabbatar da lokaci a fili ba, amma yana iya tabbatar da cewa wasu bayanai an ƙirƙira su a cikin tsari na musamman

## shaidar zamba

za mu iya tabbatar da nau'o'in zamba daban-daban ta hanyar bayyana bayanan da aka ƙirƙira a tsari mara kyau. inda ba a haɗa bayanai ta hanyar ayyukan hanyar sadarwa na yau da kullun ba, za a iya shigar da su ta hanyar ƙirƙirar ayyukan da ke ɗauke da hash na shaida. da zarar an shigar da su cikin sabuntarwar da operator ya sa hannu, ana bayyana shaida a matsayin wanda aka ƙirƙira a wuri mara bin ƙa'ida a cikin tsari:

- operator, bayan da ya yi tayin ƙara kuɗi ga deposit tare da kuɗaɗe da aka aika a kan sarƙar zuwa wani adireshi, ya sa hannu a sabuntawar ledger wanda ba ya ɗauke da ƙarin kuɗin da ya dace, amma yana ɗauke da sarƙar da ke bayyana hash na tubali da ya wuce adadin tabbatarwar da aka yarda kafin ƙara kuɗi

- operator, bayan ya ƙirƙiri takardar kuɗin lightning a madadin deposit, ya sa hannu a sabuntawar ledger wanda bai ƙara kuɗi ga deposit ba duk da cewa an bayyana preimage a cikin sarƙar

- sa hannun haɗin kai da ke bayyana hash na ledger na yanzu ya zama wanda ya riga hash ɗinsu na baya a cikin sarƙar

- memba na quorum na ledger mai takaddama wanda yake a aiki amma bai yi aiki bisa ga shaidar zamba a cikin adadin tubali ba

- sa hannu ko sa hannun haɗin kai a sabuntawar ledger marasa bin ƙa'ida

shaidar zamba ta ƙunshi shaida da sarƙar dalili da ke haɗa hash da aka shigar zuwa ledger na operator da ake zargi. sarƙar jerin sabuntarwa ne da aka sa hannu tare, kowanne ya ƙunshi member_ledger_hash daga ledger na da ya gabata. masu tabbatarwa suna bi ta sarƙar ba tare da bincike ba, suna tabbatar da kowanne haɗi sabuntarwa ce da aka sa hannu, kuma hash na shaida ya dace da bayanan da aka shigar

## farfaɗo

da zarar ledger ya zama ba a samu ko mara bin ƙa'ida, membobin quorum na iya ƙirƙirar ci gabansu na ledger daga sabuntawar ƙarshe mai bin ƙa'ida. dole ne su kafa sabon quorum kuma su samar da shaidar collateral. membobi dole ne su haɗa kai don kashe fitowar reserves da ta gabata zuwa caca na sarƙoƙin da za su iya biyo baya. wanda ya ci nasarar wannan cacar yana ƙara sabuntawar saye zuwa sarƙarsu, sauran kuma suna ƙara mika wuya. wallet suna ci gaba da tuntuɓar ledger ɗaya, suna karɓar amsoshi ne kawai da quorum ta sa hannu tare. lokaci-lokaci, musamman lokacin da amsoshi ba su da sa hannun haɗin kai da ake tsammani, wallet ya kamata ya binciki hanyar sadarwar kuma ya sake kunna sabuntawar ledger don gano canje-canjen kula

lokacin da rashin bin ƙa'ida ya bayyana kamar ba da gangan ba ne (misali, ledger ya ɓace na adadin tubali) canjin kula dole ne ya kasance mai ladabi: adadin reserves da ake buƙata kawai don ɗaukar wajibcin ledger ne ake aika zuwa cacar, kuma sauran ana mayar da su zuwa maɓallin jama'a na operator. iko a kan collateral ba a shafa ba

lokacin da shaidar rashin bin ƙa'ida ta wanzu, adadin da ya wuce reserves da ake buƙata ana raba shi daidai wa daida tsakanin membobin quorum, kuma collateral da ake riƙewa a ledger na membobi ana ba da izinin kwace ta

## lafiyar hanyar sadarwa

harin kai tsaye ɗaya shine samar da tsibiran operator masu haɗin kai. bayan gina wajibci mai yawa a cikin ledger ɗinsu, suna haɗa kai don fita, suna sace kuɗaɗe da suka wuce collateral da aka rasa. hanyar sadarwar na iya kare wa daga wannan, sai dai a yankunan da darajar da ke ciki ta wuce collateral da ke haɗa ta zuwa hanyar sadarwar da ba ta haɗin kai. manyan ƙimar collateral da manyan quorum masu bambanci suna rage yiwuwar waɗannan wurare su samu, amma za a iya samar da su da gangan kuma ba za mu iya sa ran kowanne wallet ya binciki dukkan hanyar sadarwar ba. a maimakon haka kasuwannin gano ya kamata su buga ma'aunin lissafin operator dangane da binciken jadawali kamar prize-collecting algorithms

## ƙarshe

muna gabatar da hanyar sadarwar collateral da ke buƙatar haɗin kai don sata, amma haɗin kai yana ƙara collateral da ke cikin haɗari da sauri fiye da yadda yake ƙara darajar da za a sace. muna amfani da wannan hanyar sadarwar don tabbatar da ledger na ƙa'ida da cikakken reserves ke tallafawa. waɗannan ledger suna yi wa asusu hidima a madadin wallet da ba su da haɗin yanar gizo a musayar kuɗin sabis da aka yi ciniki a kansu tun farko. abubuwan asali na ledger suna tallafawa sharuɗɗan kashewa na miniscript waɗanda suka isa don ƙananan kwangilolin wayo. hanyar sadarwar tana girma kusan daidai da layi, wanda ke ba babbar hanyar sadarwa damar samar da biliyoyin wallet da ƙarfin ciniki da ya wuce hanyoyin biyan kuɗi na gargajiya
