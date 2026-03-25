# bitcoin deposito's
## abstrak

'n ideale eweknie-tot-eweknie weergawe van elektroniese kontant sou toelaat dat aanlyn betalings direk van een party na 'n ander gestuur word, vinnig en met minimale voorbereiding. die lightning-netwerk bied deel van die oplossing, maar die noodsaaklike voordele gaan verlore as 'n vertroude derde party vereis word om toestand namens jou te bestuur. ons stel 'n oplossing vir hierdie probleem voor deur gebruik te maak van verifieerbare grootboeke en 'n web van onderpand. operateurs saai grootboek-opdaterings na hul ewekniee uit, wat 'n ouditeerbare rekord van rekeninge skep. beursies saai bewyse van oneerlikheid na daardie ewekniee uit, wat verseker dat die grootboek 'n eerlike operateur handhaaf. eensydige uittrede word vervang deur die waarborg dat fondse beskikbaar bly solank die netwerk dit is. ons bereik 'n netwerk wat likiditeitsonderhoud delegeer, opstelgelde vermy, in staat is om betalings vanlyn te ontvang, en onafhanklik van die basislaag skaal

## inleiding

bitcoin deposito's het ten doel om vinnige en skaalbare sleutelbeheerde fondse te bied, vertrouensloos, buite-ketting. op-ketting aktiwiteit skaal met die aantal grootboeke en frekwensie van reserwerotasie. deurset skaal effens bo lineêr met die aantal grootboeke in die netwerk, wat miljoene transaksies per sekonde oor triljoene beursies aanneemlik maak

daar is uitdruklike afwegings:
- geen eensydige uittrede nie: wanneer operateurs faal, bly fondse in die netwerk
- geen privaatheid nie: verifikasie vereis deursigtigheid
- periodieke beskikbaarheid: 'n deposito is slegs so beskikbaar soos die operateur. beursies behoort fondse te versprei om beskikbaarheid te verhoog

ons verwag dat die beursie-ervaring soortgelyk sal wees aan 'n vinnige basislaag, met betalingsekonomie soortgelyk aan die lightning-netwerk

## grootboeke

'n grootboek is 'n onveranderlike ketting van opdaterings, wat die hash van die vorige opdatering bevat en deur die grootboek se operateur onderteken is. verskillende tipes opdaterings het verskillende reëls wat bepaal wanneer en hoe hulle gebruik kan word. grootboeke is selfbeskrywend, hul opdaterings is publiek beskikbaar en onweerlegbaar, wat enigiemand in staat stel om nakoming te evalueer

grootboeke het 'n enkele aktiewe operateur, maar word koöperatief deur die maas onderhou. enige operateur kan een skep, maar sou hulle verdwyn of oneerlik word, sal 'n ander operateur toegewys word, saam met reserwes. die huidige aktiewe operateur word geïdentifiseer deur die publieke sleutel wat gebruik is om die mees onlangse mede-ondertekende opdatering te onderteken

## deposito's

'n deposito is 'n stabiele rekening wat fondse kan stuur en ontvang, beheer deur miniscript. by opening word 'n geldskema vasgestel, sowel as of die ontvangs van fondse 'n beursie-ondertekende versoek vereis. 'n operateur moet oorplasings tussen deposito's op dieselfde grootboek sowel as op-ketting uittrede toelaat. hulle behoort deposito's toe te laat om lightning-fakture te betaal

dit is in die operateur se diskresie om op-ketting befondsingaanbiedinge of lightning-fakture namens 'n deposito te skep. indien hulle dit doen, behoort hierdie mede-onderteken te word deur 'n kworumlid, en die beursie behoort hierdie handtekening te verifieer. aanbiedinge en fakture is nie deel van die grootboek nie, dus is dit die beursie se verantwoordelikheid om handtekeninge te verifieer en as bewyse te behou

## gelde

oorplasings tussen deposito's, op-ketting, en deur lightning het gelde wat aan die grootboek se operateur betaal word. daar is ook gelde wat periodiek op saldo's toegepas word met 'n gespesifiseerde tydperk. almal word onderhandel wanneer 'n nuwe deposito geopen word. gelde kan verander word na 'n gespesifiseerde aantal blokke, gegewe 'n gespesifiseerde blok-kennisgewing en binne 'n per-aanpassing persentasielimiet wat by opening onderhandel is. die kworum mag weier om opdaterings mede te onderteken wat onwinsgewende omstandighede skep waarvoor hulle uiteindelik verantwoordelik kan wees

## oorplasings

die basiese vorm van oorplasing is 'n tweefase-operasie tussen twee deposito's op dieselfde grootboek: 'n deposito reik 'n versoek uit om fondse te stuur. as daar voldoende fondse beskikbaar is, word 'n slot op die fondse met 'n bestedingsvoorwaarde by die grootboek gevoeg. as die bestedingsvoorwaarde voor 'n uitteltyd vervul word, beweeg fondse van die sender na die ontvanger minus die operateur se geld. as die uitteltyd bereik word, word die slot vrygestel, minus 'n kleiner operateurgeld. met miniscript-bestedingsvoorwaardes is dit voldoende om enige deposito in staat te stel om brûe en likiditeitsdienste aan ander deposito's op dieselfde grootboek te bied

## lightning

operateurs wat 'n lightning-kanaal het, mag deposito's toelaat om oor die lightning-netwerk te stuur en te ontvang. wanneer 'n deposito 'n lightning-faktuur versoek, skep die operateur een deur hul lightning-node, vra kworumlede om dit mede te onderteken om te bewys dat hulle verbind is om die deposito te krediteer by betaling. die beursie behoort hierdie mede-ondertekende faktuur as bewys te behou. wanneer 'n deposito betaling van 'n lightning-faktuur versoek, betaal die operateur deur hul lightning-node en debiteer die deposito nadat die preimage verkry is

wanneer die betaler en die begunstigde deposito's op dieselfde operateur is, mag die operateur intern vereffen sonder om deur lightning te roeteer, en die onderskeie deposito's direk krediteer en debiteer. dit vermy roeteringsgelde en falingsmodusse terwyl dieselfde rekeningkundige waarborge gehandhaaf word

## koeriers

oorplasingsversoeke beweeg slegs fondse tussen deposito's op dieselfde grootboek. om fondse oor grootboeke te beweeg, gebruik beursies koeriers — dienste wat deposito's op veelvuldige grootboeke hou en oorplasings tussen hulle dra. 'n koerier adverteer kapasiteit en per-grootboek rigtinggelde op die aflos. wanneer 'n beursie van grootboek A na grootboek B wil stuur, skep dit 'n oorplasingslot na die koerier se deposito en versoek dat die koerier een skep van hul deposito op die bestemmingsgrootboek na die begunstigde. sodra beide slotte gevestig is, onthul die beursie die preimage aan die begunstigde, wat die oorplasing van die koerier voltooi. sodra dit onthul is, gebruik die koerier dieselfde preimage om die oorplasing van die sender na die koerier te voltooi

dit is 'n standaard hash-tydgeslote kontrakpatroon. ons verwag dat die koerier se uitgaande uitteltyd streng vroeër as die inkomende sal wees, wat verseker dat as die beursie nooit onthul nie, beide slotte verval en geen party fondse verloor nie. geen vertroue is nodig bo die uitteltydwaarborg wat deur operateurs afgedwing word nie

koeriers behoort per-grootboek gelde te stel: fee_in en fee_out vir elke grootboek wat hulle bedien. die beursie skat roetekoste as fee_out op die bron plus fee_in op die bestemming. koeriers mag gelde per grootboek varieer op grond van beskikbare likiditeit, wat hul posisies natuurlik herbalanseer. beursies ontdek koeriers deur hul advertensies op die aflos en kies op grond van geld, kapasiteit, of dekking

## kommunikasie

alle kommunikasie tussen beursies en operateurs, en tussen operateurs, gebruik nostr-aflossers. grootboek-opdaterings word as duursame gebeure gepubliseer wat aflossers behou, wat 'n permanente ouditeerbare rekord skep. versoeke en antwoorde tussen beursies en operateurs is kortstondige gebeure met 'n kort aflos-TTL. operateurs adverteer hul voorwaardes as vervangbare gebeure, wat beursies in staat stel om operateurs te ontdek en te vergelyk sonder 'n gesentraliseerde gids

hierdie argitektuur beteken dat beursies geen volgehoue verbindings nodig het nie — hulle kan onbepaald vanlyn gaan en inhaal deur gebeure van enige aflos wat dit het, te herspeel. operateurs kan bereik word deur enige aflos wat hulle monitor, en die keuse van aflos is 'n ontplooiingsbesluit, nie 'n protokolbeperking nie

## reserwes en onderpand

reserwes word gehou in 'n utxo met 'n bedrag groter as of gelyk aan die som van 'n grootboek se verpligtinge, besteebaar deur 'n meerderheid van die kworum, met terugval na die operateur na 'n beduidende tydperk

onderpand is die operateur se eie kapitaal, gedeponeer en gesluit op kworumlid-grootboeke. elke lid hou 'n onderpanddeposito wat die operateur befonds en vir 'n gespesifiseerde tydsduur sluit. 'n grootboek se totale verpligtinge is beperk tot tweemaal die kleinste onderpandslot wat deur enige lid gehou word, en die kworum se tydsduur is beperk tot die kortste slottyd. dit verseker dat die onderpandweb altyd genoeg dekking het om 'n bewaarsoordrag te dek. dieselfde onderpanddeposito mag veelvuldige grootboeke rugsteun om kapitaaldoeltreffendheid te verbeter, alhoewel beursies operateurs met nie-oorvleuelende onderpandbronne behoort te verkies

verpligtinge word afgedwing wanneer nuwe befondsingaanbiedinge of fakture geskep word. die operateur kan nie aanbiedinge of fakture skep wat die grootboek se totale verpligtinge bo die reserwes of bo tweemaal die kleinste onderpandslot sal stoot nie, watter een ook al laer is

## kworum

operateurs versoek ander operateurs om by hul kworum aan te sluit deur onderpand op die lid se grootboek te deponeer en te sluit. die versoek sluit die onderpandverbintenis in (bedrag en slotduur) en die lid se voorwaardes: minimum geldskemas waaraan deposito's op die grootboek moet voldoen. elke lid moet hul eie grootboek bedryf en mag die operateur se onderpand konfiskeer as die operateur bewys word as nie-nakomend. lede spesifiseer limiete op geldskemas tydens hul kworumlidmaatskap — die operateur kan nie deposito's open met gelde onder die strengste lid se minimums nie, wat lede beskerm teen die oorerwing van onwinsgewende verpligtinge na 'n bewaarsoordrag

sodra die kworum gevestig is, word reserwes in 'n nuwe multisig utxo geroteer. lede mede-onderteken geldige opdaterings en neem deel aan herstel as die operateur nie-nakomende onderteken. groter kworums verhoog kommunikasie-oorhoofse koste, maar verminder operateursrisiko, verhoog beskikbaarheid, en maak sameswering moeiliker en duurder. beursies behoort groter kworums te verkies

## ekonomiese afskrikking

die protokol vervang eensydige uittrede met ekonomiese afskrikking. kworumlede word direk aangespoor om teen oneerlikheid op te tree. tydens normale bedrywighede verdien hulle beskeie gelde op onderpand, maar in die geval van bewysbaar nie-nakomende gedrag staan hulle om die operateur se volle onderpanddeposito op hul grootboek te konfiskeer

wanneer 'n beursie sensuur vermoed, kan dit die versoek na kworumlede eskaleer via gesertifiseerde aflewering. die lid bed die versoek-hash in hul eie grootboek in vir 'n klein geld, wat oorsaaklik verankerde bewyse skep. as die operateur versuim om die versoek te verwerk, het die lid beide die bewyse en die ekonomiese aansporing om 'n dispuut te inisieer

lightning-faktuur bedrog volg dieselfde afskrikkingspatroon. die operateur weet of 'n preimage ontvang is, maar die beursie weet nie. enige betaler kan egter die preimage aan die beursie verskaf. 'n enkele bevestigde diefstal veroorsaak 'n dispuut, beslaglegging op reserwes, en onderpandkonfiskasie. die beloning van die steel van 'n enkele betaling is begrens, maar die risiko is eksistensieel, wat lightning-diefstal ekonomies irrasioneel maak ten spyte daarvan dat dit formeel onbewysbaar is sonder derdeparty-samewerking

die falingsmodus vir beide sensuur en lightning-afskrikking is eenparige kworumsameswering. die protokol kan nie beskerm teen 'n kworum wat saamwerk om te steel nie, maar die web van onderpand verseker dat sameswering meer kos as wat dit oplewer. die netwerk se deursigtigheid laat beursies en ontdekkingsmarkte toe om verdagte kworumstrukture te identifiseer voor fondse gedeponeer word

## tyd

absolute tyd word gemeet teen die basislaag. toleransies kan nie 'n redelike aantal bevestigings oorskry nie om stabiliteit tydens kettingherskikkings te handhaaf

waar hoër toleransies vereis word, maak ons staat op oorsaaklike ordening. 'n kriptografiese grootboek is 'n merkle-ketting. elke opdatering bewys dat dit na alle opdaterings voor dit geskep is, maar bied geen waarborge oor inligting buite die ketting nie. om 'n verspreide ordening te konstrueer, vereis ons dat mede-handtekeninge die nuutste opdatering-hash van die mede-ondertekenaar se grootboek insluit. daardie hash word dan in die huidige opdatering se hash opgeneem, wat deel word van die ketting sowel as van alle ander kettings waarvoor die grootboek-operateur mede-onderteken, wat 'n web van oorsaaklikheid skep. dit is nie in staat om tyd eksplisiet te bewys nie, maar is in staat om te bewys dat sekere stukke inligting in 'n spesifieke volgorde geskep is

## bedrogbewyse

ons kan verskeie tipes bedrog bewys deur inligting bloot te stel wat in die verkeerde volgorde geskep is. waar inligting nie deur normale netwerkbedrywighede ingesluit word nie, kan dit ingesmokkel word deur aktiwiteit te skep wat 'n hash van die bewyse insluit. sodra dit in 'n opdatering opgeneem is wat deur die operateur onderteken is, word die bewyse onthul as geskep op 'n nie-nakomende plek in die ordening:

- 'n operateur, wat aangebied het om 'n deposito te krediteer met fondse wat op-ketting na 'n spesifieke adres gestuur is, onderteken 'n grootboek-opdatering wat nie die toepaslike krediet bevat nie, maar wel 'n ketting bevat wat 'n blok-hash onthul wat die aantal bevestigings oorskry wat voor krediet toegelaat word

- 'n operateur, wat 'n lightning-faktuur namens 'n deposito geskep het, onderteken 'n grootboek-opdatering wat nie die deposito gekrediteer het nie ten spyte daarvan dat die preimage in die ketting onthul is

- 'n mede-handtekening wat verklaar dat die huidige grootboek-hash een is wat hul eie latere hash in die ketting voorafgaan

- 'n lid van die kworum van 'n betwiste grootboek wat aktief was maar nie opgetree het in ooreenstemming met bewys van bedrog binne 'n aantal blokke nie

- ondertekening of mede-ondertekening van nie-nakomende grootboek-opdaterings

'n bedrogbewys bestaan uit die bewyse en 'n oorsaaklike ketting wat die ingebedde hash aan die beskuldigde operateur se grootboek verbind. die ketting is 'n reeks mede-ondertekende opdaterings, wat elk 'n member_ledger_hash van die vorige skakel se grootboek insluit. verifieerders loop die ketting sonder om te soek, bevestig elke skakel is 'n ondertekende opdatering, en dat die bewys-hash met die ingebedde data ooreenstem

## herstel

sodra 'n grootboek onbeskikbaar of nie-nakomend geword het, mag kworumlede hul eie voortsetting van die grootboek skep vanaf die laaste nakomende opdatering. hulle moet 'n nuwe kworum vestig en onderpandattestasies verskaf. lede moet dan koördineer om die vorige reserwes-uitset na 'n lotery van die potensiële volgende kettings te bestee. die wenner van hierdie lotery voeg 'n verkrygingsopdatering by hul ketting, en die ander voeg 'n afstand by. beursies rig steeds na dieselfde grootboek, en aanvaar slegs antwoorde wat deur die kworum mede-onderteken is. periodiek, en wanneer geen antwoorde die verwagte mede-handtekening het nie, behoort die beursie die netwerk te ondervra en grootboek-opdaterings te herspeel om veranderinge in bewaring te identifiseer

wanneer nie-nakoming toevallig lyk (bv. 'n grootboek het vir 'n sekere aantal blokke onbeskikbaar geword) moet die verandering in bewaring respekvol wees: slegs die bedrag reserwes wat nodig is om die grootboek se verpligtinge te dek word na die lotery gestuur, en wisselgeld word teruggestuur na die operateur se publieke sleutel. beheer van onderpand word nie geraak nie

wanneer bewys van nie-nakoming bestaan, word die bedrag bo die nodige reserwes gelykop verdeel onder lede van die kworum, en onderpand wat op lidgrootboeke gehou word, word toegelaat om gekonfiskeer te word

## netwerkgesondheid

een eenvoudige aanval is om eilande van sameswerende operateurs te vorm. nadat hulle aansienlike verpligtinge oor hul grootboeke opgebou het, koördineer hulle om uit te tree en fondse te steel wat die onderpand wat verloor is oorskry. die netwerk kan hierteen verdedig, behalwe in streke waar die interne waarde die onderpand wat dit aan die nie-sameswerende netwerk verbind, oorskry. hoër onderpandverhoudings en groter, meer diverse kworums verminder die waarskynlikheid dat hierdie sakke vorm, maar hulle kan doelbewus vorm en ons kan nie verwag dat elke beursie die hele netwerk evalueer nie. in plaas daarvan behoort ontdekkingsmarkte maatstawwe van operateuraanspreeklikheid te publiseer gebaseer op grafiekontledings soos prysversamelingsalgoritmes

## gevolgtrekking

ons stel 'n onderpandnetwerk voor wat sameswering vereis om te steel, maar sameswering verhoog die onderpand in gevaar vinniger as wat dit die waarde wat gesteel kan word verhoog. ons gebruik hierdie netwerk om kriptografiese grootboeke te beveilig wat deur volle reserwes gerugsteun word. hierdie grootboeke bedien rekeninge namens vanlyn beursies in ruil vir vooraf-onderhandelde gelde. grootboekprimitiewe ondersteun miniscript-bestedingsvoorwaardes wat voldoende is vir basiese slim kontrakte. die netwerk skaal naby lineêr, wat 'n groot netwerk in staat stel om miljarde beursies en transaksie-volume bo dié van tradisionele betalingsnetwerke te voorsien
