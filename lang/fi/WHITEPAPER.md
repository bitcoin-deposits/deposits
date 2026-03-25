# bitcoin deposits
## tiivistelma

ihanteellinen vertaisverkkoversio sahkoisesta rahasta mahdollistaisi verkkomaksujen lahettamisen suoraan osapuolelta toiselle nopeasti ja mahdollisimman vahalla valmistelulla. lightning-verkko tarjoaa osan ratkaisusta, mutta oleelliset hyodyt menetetaan, jos luotettu kolmas osapuoli vaaditaan hallitsemaan tilaa puolestasi. ehdotamme ratkaisua tahan ongelmaan kayttamalla todennettavia tilikirjoja ja vakuusverkkoa. operaattorit lahettavat tilikirjapaivityksia vertaisilleen luoden tarkastettavan kirjanpidon tileista. lompakot lahettavat todisteita eparehellisyydesta naille vertaisille, jotka varmistavat, etta tilikirja sailyttaa rehellisen operaattorin. yksipuolinen poistuminen korvataan takuulla, etta varat pysyvat saatavilla niin kauan kuin verkko toimii. paadymme verkkoon, joka delegoi likviditeetin yllapidon, valttaa perustamismaksut, kykenee vastaanottamaan maksuja offline-tilassa ja skaalautuu peruskerroksen ulkopuolella itsenaisesti

## johdanto

bitcoin deposits pyrkii tarjoamaan nopeita ja skaalautuvia avaimilla hallittuja varoja, luottamuksettomasti, ketjun ulkopuolella. ketjussa tapahtuva toiminta skaalautuu tilikirjojen maaran ja reservien kiertonopeuden mukaan. lapimenoteho skaalautuu hieman lineaarista nopeammin tilikirjojen maaran mukaan verkossa, tehden miljoonat tapahtumat sekunnissa biljoonien lompakoiden kesken mahdollisiksi

on selkeita kompromisseja:
- ei yksipuolista poistumista: kun operaattorit epaonnistuvat, varat jaavat verkkoon
- ei yksityisyytta: todentaminen vaatii lapinakyvyytta
- ajoittainen saatavuus: talletus on vain niin saatavilla kuin operaattori. lompakoiden tulisi hajauttaa varoja saatavuuden lisaamiseksi

odotamme lompakkokokemuksen olevan samankaltainen kuin nopea peruskerros, ja maksutaloustiede muistuttaa lightning-verkkoa

## tilikirjat

tilikirja on muuttumaton ketju paivityksia, joka sisaltaa edellisen paivityksen hash-arvon ja on tilikirjan operaattorin allekirjoittama. erityyppisilla paivityksilla on erilaiset saannot siita, milloin ja miten niita voidaan kayttaa. tilikirjat ovat itsekuvaavia, niiden paivitykset ovat julkisesti saatavilla ja kiistamattomia, mika mahdollistaa kenen tahansa arvioida saannonmukaisuutta

tilikirjoilla on yksi aktiivinen operaattori, mutta niita yllapidetaan yhteistoiminnallisesti verkon toimesta. mika tahansa operaattori voi luoda sellaisen, mutta mikali he katoavat tai muuttuvat eparehellisiksi, toinen operaattori maarataan yhdessa reservien kanssa. talla hetkella aktiivinen operaattori tunnistetaan julkisesta avaimesta, jota kaytettiin viimeisimman yhteisallekirjoitetun paivityksen allekirjoittamiseen

## talletukset

talletus on vakaa tili, joka voi lahettaa ja vastaanottaa varoja, ja jota hallitaan miniscript-kielella. avattaessa vahvistetaan maksuaikataulu seka se, vaatiiko varojen vastaanottaminen lompakon allekirjoittaman pyynnon. operaattorin on sallittava siirrot talletusten valilla samalla tilikirjalla seka ketjussa tapahtuvat poistumiset. haidan tulisi sallia talletusten maksaa lightning-laskuja

operaattorin harkinnassa on luoda ketjussa tapahtuvia rahoitustarjouksia tai lightning-laskuja talletuksen puolesta. mikali he tekevat niin, naiden tulisi olla koorumin jasenen yhteisallekirjoittamia, ja lompakon tulisi todentaa tama allekirjoitus. tarjoukset ja laskut eivat ole osa tilikirjaa, joten lompakon vastuulla on todentaa allekirjoitukset ja sailyttaa ne todisteina

## maksut

siirrot talletusten valilla, ketjussa ja lightning-verkon kautta sisaltavat maksuja, jotka maksetaan tilikirjan operaattorille. on myos maksuja, joita sovelletaan ajoittain saldoihin maaritellyin valein. kaikki neuvotellaan kun uusi talletus avataan. maksuja voidaan muuttaa maaritellyn lohkomaaran jalkeen, annetulla lohkoilmoituksella ja avattaessa neuvoteltujen prosentuaalisten saatorajojen puitteissa. koorumi voi kieltaytya yhteisallekirjoittamasta paivityksia, jotka luovat kannattamattomia olosuhteita, joista he voivat lopulta olla vastuussa

## siirrot

siirron perusmuoto on kaksivaiheinen operaatio kahden talletuksen valilla samalla tilikirjalla: talletus antaa pyynnon lahettaa varoja. mikali varoja on riittavasti saatavilla, varojen lukitus kayttoehdolla liitetaan tilikirjaan. mikali kayttoehto taytetaan ennen aikarajaa, varat siirtyvat lahettajalta vastaanottajalle vahennettyna operaattorin maksulla. mikali aikaraja saavutetaan, lukitus vapautetaan pienemmalla operaattorin maksulla. miniscript-kayttoehdoilla tama on riittavaa, jotta mika tahansa talletus voi tarjota silta- ja likviditeettipalveluita muille talletuksille samalla tilikirjalla

## lightning

operaattorit, joilla on lightning-kanava, voivat sallia talletusten lahettaa ja vastaanottaa lightning-verkon kautta. kun talletus pyytaa lightning-laskua, operaattori luo sellaisen lightning-solmunsa kautta, pyytaa koorumin jasenia yhteisallekirjoittamaan sen todistaakseen sitoutumisensa hyvittamaan talletuksen maksun yhteydessa. lompakon tulisi sailyttaa tama yhteisallekirjoitettu lasku todisteena. kun talletus pyytaa lightning-laskun maksamista, operaattori maksaa lightning-solmunsa kautta ja veloittaa talletusta saatuaan preimage-arvon

kun maksaja ja maksunsaaja ovat talletuksia samalla operaattorilla, operaattori voi selvittaa sisaisesti ilman lightning-verkon kautta reititysta, hyvittaen ja veloittaen kyseisia talletuksia suoraan. tama valttaa reititysmaksut ja vikatilanteet sailyttaen samat kirjanpitotakuut

## kuriirit

siirtopyynnot siirtavat varoja vain talletusten valilla samalla tilikirjalla. varojen siirtamiseksi tilikirjojen valilla lompakot kayttavat kuriireita — palveluita, joilla on talletuksia useilla tilikirjoilla ja jotka kuljettavat siirtoja niiden valilla. kuriiri ilmoittaa kapasiteettinsa ja tilikirjakohtaiset suuntakohtaiset maksunsa releessa. kun lompakko haluaa lahettaa tilikirjalta A tilikirjalle B, se luo siirtolukituksen kuriirien talletukseen ja pyytaa, etta kuriiri luo sellaisen talletuksestaan kohdetilikirjalla maksunsaajalle. kun molemmat lukitukset on perustettu, lompakko paljastaa preimage-arvon maksunsaajalle, joka suorittaa siirron kuriirilta. paljastamisen jalkeen kuriiri kayttaa samaa preimage-arvoa suorittaakseen siirron lahettajalta kuriirille

tama on vakiomuotoinen hash-aikalukittu sopimusmalli. odotamme kuriirien lahtevien aikarajojen olevan ehdottomasti aikaisempia kuin saapuvien, varmistaen etta mikali lompakko ei koskaan paljasta, molemmat lukitukset raukeavat eika kumpikaan osapuoli menetä varoja. luottamusta ei vaadita aikarajatakuun lisaksi, jonka operaattorit toimeenpanevat

kuriirit maarittelevat tilikirjakohtaiset maksut: fee_in ja fee_out kullekin palvelemalleen tilikirjalle. lompakko arvioi reittikustannuksen lahteen fee_out ja kohteen fee_in summana. kuriirit voivat vaihdella maksuja tilikirjittain saatavilla olevan likviditeetin perusteella, tasapainottaen luonnollisesti positioitaan. lompakot loytavat kuriirit naiden ilmoitusten kautta releessa ja valitsevat maksun, kapasiteetin tai kattavuuden perusteella

## viestinta

kaikki viestinta lompakoiden ja operaattoreiden valilla seka operaattoreiden kesken kayttaa nostr-releita. tilikirjapaivitykset julkaistaan kestovina tapahtumina, jotka releet sailyttavat luoden pysyvan tarkastettavan kirjanpidon. pyynnot ja vastaukset lompakoiden ja operaattoreiden valilla ovat lyhytaikaisia tapahtumia lyhyella releen TTL-arvolla. operaattorit ilmoittavat ehtonsa korvattavina tapahtumina, mika mahdollistaa lompakoiden loydon ja operaattoreiden vertailun ilman keskitettya hakemistoa

tama arkkitehtuuri tarkoittaa, etta lompakot eivat tarvitse pysyvia yhteyksia — ne voivat olla offline-tilassa maarittelemattoman ajan ja pysya ajantasalla toistamalla tapahtumia milta tahansa releelta, jolla ne ovat. operaattoreihin voidaan ottaa yhteys minka tahansa niiden seuraamaan releen kautta, ja releen valinta on kayttoonottopäätös, ei protokollarajoite

## reservit ja vakuudet

reservit pidetaan utxo-tulosteessa, jonka maara on suurempi tai yhta suuri kuin tilikirjan velvoitteiden summa, ja joka on kaytettavissa koorumin enemmiston toimesta, varavaihtoehtona operaattorille merkittavan ajanjakson jalkeen

vakuus on operaattorin omaa paaomaa, talletettuna ja lukittuna koorumin jasenien tilikirjoihin. kukin jasen pitaa vakuustalletusta, jonka operaattori rahoittaa ja lukitsee maaritellyksi ajaksi. tilikirjan kokonaisvelvoitteet on rajoitettu kaksinkertaiseksi pienimman minkä tahansa jasenen hallussa olevan vakuuslukituksen maaraksi, ja koorumin kesto on rajoitettu lyhimpaan lukitusaikaan. tama varmistaa, etta vakuusverkolla on aina riittavasti katetta hallintasiirron kattamiseksi. sama vakuustalletus voi tukea useita tilikirjoja paaomakayton tehostamiseksi, vaikka lompakoiden tulisi suosia operaattoreita, joilla on paallekkaismattomat vakuuslahteen

velvoitteet pannaan taytantoon uusia rahoitustarjouksia tai laskuja luotaessa. operaattori ei voi luoda tarjouksia tai laskuja, jotka nostaisivat tilikirjan kokonaisvelvoitteet reservien ylapuolelle tai yli kaksinkertaiseksi pienimman vakuuslukituksen maaraksi, sen mukaan kumpi on pienempi

## koorumi

operaattorit pyytavat muita operaattoreita liittymaan koorumiinsa tallettamalla ja lukitsemalla vakuuden jasenen tilikirjaan. pyynto sisaltaa vakuussitoumuksen (maara ja lukitusaika) ja jasenen ehdot: vahimmaismaksuaikataulut, jotka tilikirjan talletusten on taytettava. kunkin jasenen on operoitava omaa tilikirjaansa ja he voivat takavarikoida operaattorin vakuuden, mikali operaattori todetaan saantojenvastaiskesi. jasenet maarittelevat maksuaikataulujen rajat koorumijasenyytensa aikana — operaattori ei voi avata talletuksia tiukimman jasenen vahimmaismaksuja alhaisemmilla maksuilla, suojaten jasenia kannattamattomien velvoitteiden perimiselta hallintasiirron jalkeen

kun koorumi on perustettu, reservit kierratetaan uuteen multisig utxo-tulosteeseen. jasenet yhteisallekirjoittavat validit paivitykset ja osallistuvat palautukseen, mikali operaattori allekirjoittaa saantojenvastaisia. suuremmat koorumit lisaavat viestintakuormaa, mutta vahentavat operaattoririskia, lisaavat saatavuutta ja tekevat yhteistoiminnasta vaikeampaa ja kalliimpaa. lompakoiden tulisi suosia suurempia koorumeja

## taloudellinen pelote

protokolla korvaa yksipuolisen poistumisen taloudellisella pelotteella. koorumin jasenet ovat suoraan kannustettuja toimimaan eparehellisyytta vastaan. normaalin toiminnan aikana he ansaitsevat vaatimattomia maksuja vakuuksista, mutta todistettavasti saantojenvastaisen toiminnan tapauksessa he voivat takavarikoida operaattorin koko vakuustalletuksen tilikirjallaan

kun lompakko epailee sensuuria, se voi eskaloida pyynnon koorumin jasenille varmennetun toimituksen kautta. jasen upottaa pyyntohashin omaan tilikirjaansa pienella maksulla luoden kausaalisesti ankkuroidun todisteen. mikali operaattori epaonnistuu kasittelemaan pyyntoa, jasenella on seka todiste etta taloudellinen kannustin kiistan kaynnistamiseksi

lightning-laskupetos noudattaa samaa pelotemalli. operaattori tietaa, onko preimage vastaanotettu, mutta lompakko ei tieda. kuitenkin mika tahansa maksaja voi toimittaa preimage-arvon lompakolle. yksi vahvistettu varkaus kaynnistaa kiistan, reservien takavarikoinnin ja vakuuden menettamisen. yksittaisen maksun varastamisen palkkio on rajallinen, mutta riski on eksistentiaalinen, tehden lightning-varkaudesta taloudellisesti jarkevattoman, vaikka se on muodollisesti todistamaton ilman kolmannen osapuolen yhteistyota

sekä sensuurin etta lightning-pelotteen vikatilanne on yksimielinen koorumin yhteistoiminta. protokolla ei voi suojata koorumilta, joka tekee yhteistyota varastaakseen, mutta vakuusverkko varmistaa, etta yhteistoiminta maksaa enemman kuin se tuottaa. verkon lapinakyvyys mahdollistaa lompakoiden ja loytamarkkinoiden tunnistaa epailyttavat koorumirakenteet ennen varojen tallettamista

## aika

absoluuttista aikaa mitataan peruskerrosta vasten. toleranssit eivat voi ylittaa kohtuullista vahvistusmaaraa ketjun uudelleenjarjestelyiden aikaisen vakauden yllapitamiseksi

korkeampien toleranssien ollessa tarpeen turvaudumme kausaaliseen jarjestykseen. kryptografinen tilikirja on merkle-ketju. kukin paivitys todistaa, etta se luotiin kaikkien sita edeltavien paivitysten jalkeen, mutta ei anna takuita ketjun ulkopuolisesta tiedosta. hajautetun jarjestyksen rakentamiseksi vaadimme, etta yhteisallekirjoitukset sisaltavat viimeisimman paivityshashin yhteisallekirjoittajan tilikirjasta. tama hash sisallytetaan sitten nykyisen paivityksen hashiin, tullen osaksi ketjua seka osaksi kaikkia muita ketjuja, joille tilikirjan operaattori yhteisallekirjoittaa, luoden kausaalisuusverkon. tama ei kykene todistamaan aikaa nimenomaisesti, mutta kykenee todistamaan, etta tietyt tiedonpalat luotiin tietyssa jarjestyksessa

## petostodisteet

voimme todistaa erilaisia petostyyppeja paljastamalla tietoa, joka on luotu vaärässä jarjestyksessa. mikali tietoa ei sisallyteta normaalien verkkotoimintojen kautta, se voidaan salakuljettaa luomalla toimintaa, joka sisaltaa todisteen hashin. kun se on sisallytetty operaattorin allekirjoittamaan paivitykseen, todiste paljastetaan luoduksi saantojenvastaiseeen paikkaan jarjestyksessa:

- operaattori, joka on tarjoutunut hyvittamaan talletusta ketjussa tiettyyn osoitteeseen lahetetyilla varoilla, allekirjoittaa tilikirjapaivityksen, joka ei sisalla asianmukaista hyvitysta, mutta sisaltaa ketjun, joka paljastaa jonkin lohkohashin, joka ylittaa hyvitykselle sallitun vahvistusmaaran

- operaattori, joka on luonut lightning-laskun talletuksen puolesta, allekirjoittaa tilikirjapaivityksen, joka ei ole hyvittanyt talletusta huolimatta siita, etta preimage on paljastettu ketjussa

- yhteisallekirjoitus, joka ilmoittaa nykyisen tilikirjahashin olevan sellainen, joka edeltaa haidan omaa myohempaa hashia ketjussa

- koorumin jasen kiistanalaisella tilikirjalla, joka oli aktiivinen mutta ei toiminut petostodisteen mukaisesti tietyn lohkomaaran kuluessa

- saantojenvastaisten tilikirjapaivitysten allekirjoittaminen tai yhteisallekirjoittaminen

petostodiste koostuu todisteesta ja kausaaliketjusta, joka yhdistaa upotetun hashin syytetyn operaattorin tilikirjaan. ketju on sarja yhteisallekirjoitettuja paivityksia, joista kukin sisaltaa member_ledger_hash-arvon edellisen lenkin tilikirjasta. todentajat kulkevat ketjun lapi etsimatta, vahvistaen kunkin lenkin olevan allekirjoitettu paivitys ja etta todistehash vastaa upotettua dataa

## palautus

kun tilikirja on muuttunut saavuttamattomaksi tai saantojenvastaisksi, koorumin jasenet voivat luoda oman jatkonsa tilikirjalle viimeisesta saantojenmukaisesta paivityksesta. haidan on perustettava uusi koorumi ja toimitettava vakuustodistukset. jasenien on sitten koordinoitava edellisen reservitulosteen kayttaminen arvontaan mahdollisista seuraavista ketjuista. arvonnan voittaja liittaa hankinpaivityksen ketjuunsa, ja muut liittaavat luovutuksen. lompakot jatkavat saman tilikirjan osoittamista hyväksyen vain koorumin yhteisallekirjoittamia vastauksia. ajoittain, ja kun vastauksilla ei ole odotettua yhteisallekirjoitusta, lompakon tulisi kysya verkkoa ja toistaa tilikirjapaivityksia tunnistaakseen hallintamuutokset

kun saantojenvastainen toiminta vaikuttaa tahattomalta (esim. tilikirja on ollut saavuttamattomissa tietyn lohkomaaran ajan), hallintamuutoksen on oltava kunnioittava: vain tilikirjan velvoitteiden kattamiseen tarvittava reservimaara lahetetaan arvontaan, ja vaihtorahat palautetaan operaattorin julkiseen avaimeen. vakuuksien hallintaa ei muuteta

kun todisteita saantojenvastaisuudesta on olemassa, tarvittavien reservien ylittava maara jaetaan tasan koorumin jasenien kesken, ja jasenien tilikirjoilla olevat vakuudet sallitaan takavarikoitaviksi

## verkon terveys

yksi suoraviivainen hyokkays on muodostaa saaria yhteistoimivista operaattoreista. rakennettuaan huomattavia velvoitteita tilikirjoilleen he koordinoivat poistumisen varastaen varoja, jotka ylittavat menetetyn vakuuden. verkko voi puolustautua tata vastaan, paitsi alueilla joissa sisainen arvo ylittaa sen eparehelliseen verkkoon yhdistavan vakuuden. korkeammat vakuussuhteet ja suuremmat, monimuotoisemmat koorumit vahentavat naiden taskujen muodostumisen todennakoisyytta, mutta ne voivat muodostua tarkoituksella emmeka voi odottaa jokaisen lompakon arvioivan koko verkkoa. sen sijaan loytamarkkinoiden tulisi julkaista operaattorin vastuullisuusmittareita graafeihin perustuvien analyysien, kuten palkintoa keraavien algoritmien, perusteella

## johtopäätös

ehdotamme vakuusverkkoa, joka vaatii yhteistoimintaa varastaakseen, mutta yhteistoiminta kasvattaa vaarassa olevaa vakuutta nopeammin kuin se kasvattaa varastettavaa arvoa. kaytamme tata verkkoa turvaamaan kryptografisia tilikirjoja, joilla on taydet reservit. nama tilikirjat palvelevat tileja offline-lompakoiden puolesta ennalta neuvotelluilla maksuilla. tilikirjan primitiivit tukevat miniscript-kayttoehtoja, jotka riittavat perusalykkaille sopimuksille. verkko skaalautuu lahes lineaarisesti, mahdollistaen suuren verkon tarjota miljardeja lompakoita ja tapahtumavolyymia, joka ylittaa perinteiset maksuverkot
