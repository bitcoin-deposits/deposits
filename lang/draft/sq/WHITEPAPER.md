# bitcoin deposits
## abstrakti

nje version ideal peer-to-peer i parase elektronike do te lejonte qe pagesat online te dergoheshin drejtperdrejt nga njera pale tek tjetra shpejt dhe me pergatitje minimale. lightning network ofron nje pjese te zgjidhjes, por perfitimet thelbesore humbasin nese kerkohet nje pale e trete e besuar per te menaxhuar gjendjen ne emrin tuaj. ne propozojme nje zgjidhje per kete problem duke perdorur ledger te verifikueshem dhe nje rrjet collateral. operator-et transmetojne perditesimet e ledger-it tek bashkepunetoret e tyre, duke krijuar nje regjistrim te auditueshsem te llogarive. wallet-at transmetojne prova te pandershmerise tek ata bashkepunetore, te cilet sigurojne qe ledger-i te ruaje nje operator te ndershem. dalja e njeanshme zevendesohet nga garancia qe fondet mbeten te disponueshme per sa kohe qe rrjeti ekziston. ne arrijme ne nje rrjet qe delegon mirembajtjen e likuiditetit, shmang tarifat e konfigurimit, eshte i afte te marre pagesa jashte linje, dhe shkallezohet ne menyre te pavarur nga shtresa baze

## hyrja

bitcoin deposits synojne te ofrojne fonde te shpejta dhe te shkallezueshme te kontrolluara me celesa, pa besim, jashte zinxhirit. aktiviteti ne zinxhir shkallezohet me numrin e ledger-ave dhe frekuencen e rotacionit te reserve-ave. kapaciteti shkallezohet pak me shume se linearisht me numrin e ledger-ave ne rrjet, duke e bere te mundshme miliona transaksione ne sekonde permes triliona wallet-ave

ka kompromise te qarta:
- asnje dalje e njeanshme: kur operator-et deshtojne fondet qendrojne ne rrjet
- asnje privatesi: verifikimi kerkon transparence
- disponueshmeri e nderprerje: nje deposit eshte e disponueshme vetem aq sa eshte operator-i. wallet-at duhet te shperndajne fondet per te rritur disponueshmerine

ne presim qe pervoja e wallet-es te jete e ngjashme me nje shtrese baze te shpejte, me ekonomi pagesash te ngjashme me lightning network

## ledger-at

nje ledger eshte nje zinxhir i pandryshueshsem perditesimesh, qe permban hash-in e perditesimit te meparshem dhe te firmosur nga operator-i i ledger-it. lloje te ndryshme perditesimesh kane rregulla te ndryshme qe percaktojne kur dhe si mund te perdoren. ledger-at jane vetepershkrues, perditesimet e tyre jane te disponueshme publikisht dhe te pamohueshme, duke i lejuar kujtdo te vleresoje konformitetin

ledger-at kane nje operator te vetem aktiv, por mirembahen ne menyre bashkepunuese nga mesh-i. cdo operator mund te krijoje nje te tille, por nese zhduket ose behet i pandershem, nje operator tjeter do te caktohet, se bashku me reserve-at. operator-i aktualisht aktiv identifikohet nga celesi publik qe u perdor per te firmosur perditesimin me te fundit te bashkefirmosur

## deposit-at

nje deposit eshte nje llogari e qendrueshme qe mund te dergoje dhe te marre fonde, e kontrolluar nga miniscript. ne hapje vendoset nje orar tarifash, si dhe nese marrja e fondeve kerkon nje kerkese te firmosur nga wallet-a. nje operator duhet te lejoje transfertat ndermjet deposit-ave ne te njejtin ledger si dhe daljet ne zinxhir. ata duhet te lejojne deposit-at te paguajne invoice-t lightning

eshte ne diskrecionin e operator-it te krijoje oferta financimi ne zinxhir ose invoice lightning ne emer te nje deposit-e. nese e bejne, ato duhet te bashkefirmosin nga nje anetar i quorum-it, dhe wallet-a duhet te verifikoje kete firme. ofertat dhe invoice-t nuk jane pjese e ledger-it, keshtu qe eshte pergjegjesia e wallet-es te verifikoje firmat dhe t'i ruaje ato si prove

## tarifat

transfertat ndermjet deposit-ave, ne zinxhir, dhe permes lightning kane tarifa qe i paguhen operator-it te ledger-it. ka gjithashtu tarifa qe aplikohen periodikisht ne bilance me nje periudhe te specifikuar. te gjitha negociohen kur hapet nje deposit e re. tarifat mund te ndryshohen pas nje numri te specifikuar blloqesh, me nje njoftim te specifikuar ne blloke dhe brenda nje kufiri perqindjeje per rregullim te negociuar ne hapje. quorum-i mund te refuzoje te bashkefirmose perditesime qe krijojne rrethana jofitimprurese per te cilat ata perfundimisht mund te jene pergjegjes

## transfertat

forma baze e transfertes eshte nje operacion dyfazor ndermjet dy deposit-ave ne te njejtin ledger: nje deposit leshon nje kerkese per te derguar fonde. nese ka fonde te mjaftueshme, nje bllokimi mbi fondet me nje kusht shpenzimi shtohet ne ledger. nese kushti i shpenzimit plotesohet para nje afati, fondet levizin nga derguesi tek marresi minus tarifen e operator-it. nese afati arrihet, bllokimi lirohet, minus nje tarife me te vogel te operator-it. me kushte shpenzimi miniscript, kjo mjafton per te lejuar cdo deposit te ofroje ura dhe sherbime likuiditeti per deposit-a te tjera ne te njejtin ledger

## lightning

operator-et qe kane nje kanal lightning mund te lejojne deposit-at te dergojne dhe te marrin permes lightning network. kur nje deposit kerkon nje invoice lightning, operator-i krijon nje permes nyjes se tij lightning, u kerkon anetareve te quorum-it ta bashkefirmosine per te provuar se jane te angazhuar te kreditojne deposit-en pas pageses. wallet-a duhet ta ruaje kete invoice te bashkefirmosur si prove. kur nje deposit kerkon pagesen e nje invoice lightning, operator-i paguan duke perdorur nyjen e tij lightning dhe debiton deposit-en pasi merr preimage-in

kur paguesi dhe marresi jane deposit-a tek i njejti operator, operator-i mund te shlyeje brendesisht pa e kaluar permes lightning, duke kredituar dhe debituar deposit-at perkatese drejtperdrejt. kjo shmang tarifat e percjelljes dhe menyrat e deshtimit duke ruajtur te njejtat garanci kontabel

## courier-at

kerkesat e transfertave levizin fonde vetem ndermjet deposit-ave ne te njejtin ledger. per te levizur fonde ndermjet ledger-ave, wallet-at perdorin courier-a -- sherbime qe mbajne deposit-a ne ledger-a te shumte dhe bartin transferta ndermjet tyre. nje courier reklamon kapacitetin dhe tarifat drejtuese per ledger ne relay. kur nje wallet deshiron te dergoje nga ledger A ne ledger B, krijon nje bllokimi transferte ne deposit-en e courier-it dhe kerkon qe courier-i te krijoje nje nga deposit-a e tyre ne ledger-in e destinacionit tek marresi. pasi te dy bllokimet vendosen, wallet-a zbulon preimage-in tek marresi, i cili perfundon transferten nga courier-i. pasi zbulohet, courier-i perdor te njejtin preimage per te perfunduar transferten nga derguesi tek courier-i

ky eshte nje model standard hash time-locked contract. ne presim qe afati i daljes se courier-it te jete rreptesisht me i hershem se ai i hyrjes, duke siguruar qe nese wallet-a nuk zbulon kurre, te dy bllokimet skadojne dhe asnjera pale nuk humb fonde. nuk kerkohet besim pertej garancise se afatit te zbatuar nga operator-et

courier-at duhet te vendosin tarifa per ledger: fee_in dhe fee_out per cdo ledger qe sherbejne. wallet-a vlereson koston e rruges si fee_out ne burimin plus fee_in ne destinacion. courier-at mund te ndryshojne tarifat sipas ledger-it bazuar ne likuiditetin e disponueshem, duke ribalancuar natyrshmerisht pozicionet e tyre. wallet-at zbulojne courier-at permes reklamave te tyre ne relay dhe zgjedhin bazuar ne tarife, kapacitet ose mbulim

## komunikimi

i gjithe komunikimi ndermjet wallet-ave dhe operator-eve, dhe ndermjet operator-eve, perdor relay nostr. perditesimet e ledger-it publikohen si ngjarje te qendrueshme qe relay-t ruajne, duke krijuar nje regjistrim te perhershem te auditueshsem. kerkesat dhe pergjigjet ndermjet wallet-ave dhe operator-eve jane ngjarje kalimtare me nje TTL te shkurter relay-i. operator-et reklamojne kushtet e tyre si ngjarje te zevendesueshme, duke u lejuar wallet-ave te zbulojne dhe krahasojne operator-et pa nje direktori te centralizuar

kjo arkitekture do te thote qe wallet-at nuk kane nevoje per lidhje te vazhdueshme -- mund te shkojne jashte linje pa afat dhe te rikthehen duke riluajtur ngjarjet nga cdo relay qe i ka. operator-et mund te arrihen permes cdo relay-i qe monitorojne, dhe zgjedhja e relay-se eshte vendim vendosjeje, jo kufizim protokoli

## reserve-at dhe collateral

reserve-at mbahen ne nje UTXO me nje shume me te madhe ose te barabarte me shumen e detyrimeve te nje ledger-i, te shpenzueshme nga shumica e quorum-it, me rikthim tek operator-i pas nje periudhe te konsiderueshme

collateral eshte kapitali vetjak i operator-it, i depozituar dhe i bllokuar ne ledger-at e anetareve te quorum-it. cdo anetar mban nje deposit collateral qe operator-i financon dhe bllokon per nje kohezgjatje te specifikuar. detyrimet totale te nje ledger-i jane te kufizuara ne dyfishin e bllokimit me te vogel te collateral te mbajtur nga cdo anetar, dhe kohezgjatja e quorum-it eshte e kufizuar ne kohen me te shkurter te bllokimit. kjo siguron qe rrjeti i collateral ka gjithmone mbeshtetje te mjaftueshme per te mbuluar nje transferte custody. e njejta deposit collateral mund te mbeshtet ledger-a te shumte per te permiresuar efikasitetin e kapitalit, megjithese wallet-at duhet te preferojne operator-e me burime collateral qe nuk mbivendosen

detyrimet zbatohen kur krijohen oferta te reja financimi ose invoice. operator-i nuk mund te krijoje oferta ose invoice qe do te shtyenin detyrimet totale te ledger-it mbi reserve-at ose mbi dyfishin e bllokimit me te vogel te collateral, cilado qe eshte me e ulet

## quorum

operator-et kerkojne nga operator-e te tjere te bashkohen ne quorum-in e tyre duke depozituar dhe bllokuar collateral ne ledger-in e anetarit. kerkesa perfshine angazhimin e collateral (shumen dhe kohezgjatjen e bllokimit) dhe kushtet e anetarit: orar minimal tarifash qe deposit-at ne ledger duhet te plotesojne. cdo anetar duhet te operoje ledger-in e vet dhe mund te konfiskoje collateral e operator-it nese operator-i provohet jo-konform. anetaret specifikojne kufij ne oraret e tarifave gjate anetaresise se tyre ne quorum -- operator-i nuk mund te hape deposit-a me tarifa nen minimumin me te rrepte te anetareve, duke mbrojtur anetaret nga trashegimi i detyrimeve jofitimprurese pas nje transferte custody

pasi quorum-i vendoset, reserve-at rotohen ne nje UTXO te ri multisig. anetaret bashkefirmosine perditesimet e vlefshme dhe marrin pjese ne rikuperim nese operator-i firmos te pavlefshme. quorum-e me te medha rrisin ngarkesen e komunikimit por ulin rrezikun e operator-it, rrisin disponueshmerine, dhe e bejne bashkepunimin me te veshtire e me te kushtueshem. wallet-at duhet te preferojne quorum-e me te medha

## pengimi ekonomik

protokolli zevendeson daljen e njeanshme me pengim ekonomik. anetaret e quorum-it jane drejtperdrejt te motivuar te veprojne kunder pandershmerise. gjate operacioneve normale ata fitojne tarifa modeste mbi collateral, por ne rast te sjelljes jo-konforme te provueshme ata mund te konfiskojne deposit-en e plote te collateral te operator-it ne ledger-in e tyre

kur nje wallet dyshon censure, ajo mund ta pershkallezoje kerkesen tek anetaret e quorum-it permes dorezimit te certifikuar. anetari ngulit hash-in e kerkeses ne ledger-in e vet per nje tarife te vogel, duke krijuar prove te ankoruar shkakesisht. nese operator-i deshton te procesoje kerkesen, anetari ka si proven ashtu edhe motivimin ekonomik per te nisur nje mosmarreveshje

mashtrimi me invoice lightning ndjek te njejtin model pengimi. operator-i e di nese nje preimage u mor, por wallet-a nuk e di. megjithate cdo pagyes mund t'ia ofroje preimage-in wallet-es. nje vjedhje e vetme e konfirmuar shkakton mosmarreveshje, sekuestrim te reserve-ave dhe konfiskim te collateral. shperblimi i vjedhjes se nje pagese te vetme eshte i kufizuar, por rreziku eshte ekzistencial, duke e bere vjedhjen lightning ekonomikisht irracionale pavaresisht se formalisht eshte e provueshme vetem me bashkepunim palesh te treta

menyra e deshtimit per pengimin e censures dhe lightning eshte bashkepunimi unanim i quorum-it. protokolli nuk mund te mbroje kunder nje quorum-i qe bashkepunon per te vjedhur, por rrjeti i collateral siguron qe bashkepunimi kushton me shume sesa fitohet. transparenca e rrjetit u lejon wallet-ave dhe tregjeve te zbulimit te identifikojne struktura te dyshimta quorum-i para depozitimit te fondeve

## koha

koha absolute matet kunder shteses baze. tolerancat nuk mund te tejkalojne nje numer te arsyeshem konfirmimesh per te ruajtur qendrueshmerine gjate riorganizimeve te zinxhirit

aty ku kerkohen toleranca me te larta mbeshtemi ne renditjen shkakesore. nje ledger kriptografik eshte nje zinxhir merkle. cdo perditesim provon qe eshte krijuar pas te gjitha perditesimeve para tij, por nuk jep garanci per informacionin jashte zinxhirit. per te ndertuar nje renditje te shperndare, kerkojme qe bashkefirmat te perfshijne hash-in e perditesimit me te fundit nga ledger-i i bashkefirmosesit. ai hash pastaj integrohet ne hash-in e perditesimit aktual, duke u bere pjese e zinxhirit dhe pjese e te gjitha zinxhireve te tjere qe operator-i i ledger-it bashkefirmos, duke krijuar nje rrjet shkakesie. kjo nuk eshte e afte te provoje kohen ne menyre eksplicite, por eshte e afte te provoje qe pjese te caktuara informacioni u krijuan ne nje renditje specifike

## provat e mashtrimit

ne mund te provojme lloje te ndryshme mashtrimi duke ekspozuar informacion te krijuar ne renditjen e gabuar. aty ku informacioni nuk perfshihet nga operacionet normale te rrjetit, ai mund te kontrabohet duke krijuar aktivitet qe perfshin nje hash te proves. pasi integrohet ne nje perditesim te firmosur nga operator-i, prova zbulohet si e krijuar ne nje vend jo-konform ne renditje:

- nje operator, pasi ka oferuar te kreditoje nje deposit me fonde te derguara ne zinxhir ne nje adrese specifike, firmos nje perditesim ledger-i qe nuk permban kreditimin e duhur, por permban nje zinxhir qe zbulon hash-in e nje blloku qe tejkalon numrin e konfirmimeve te lejuara para kreditimit

- nje operator, pasi ka krijuar nje invoice lightning ne emer te nje deposit-e, firmos nje perditesim ledger-i qe nuk e ka kredituar deposit-en pavaresisht se preimage-i eshte zbuluar ne zinxhir

- nje bashkefirme qe deklaron hash-in aktuale te ledger-it si nje qe i paraprin hash-it te tyre me te vonshem ne zinxhir

- nje anetar i quorum-it te nje ledger-i te kontestuar qe ishte aktiv por nuk veproi ne perputhje me proven e mashtrimit brenda nje numri blloqesh

- firmosja ose bashkefirmosja e perditesimeve jo-konforme te ledger-it

nje prove mashtrimi perbehet nga prova dhe nje zinxhir shkakesor qe lidh hash-in e ngulur me ledger-in e operator-it te akuzuar. zinxhiri eshte nje sekuence perditesimesh te bashkefirmosuara, secila duke perfshire nje member_ledger_hash nga ledger-i i hallkes se meparshme. verifikuesit ndjekin zinxhirin pa kerkuar, duke konfirmuar qe cdo hallke eshte nje perditesim i firmosur, dhe qe hash-i i proves perputhet me te dhenat e ngulitura

## rikuperimi

pasi nje ledger behet i padisponueshem ose jo-konform, anetaret e quorum-it mund te krijojne vazhdimin e tyre te ledger-it nga perditesimi i fundit konform. ata duhet te vendosin nje quorum te ri dhe te ofrojne atestime collateral. anetaret duhet pastaj te koordinohen per te shpenzuar daljen e meparshme te reserve-ave ne nje llotari te zinxhireve te mundshme pasardhese. fituesi i kesaj llotarie shton nje perditesim blerje ne zinxhirin e tij, dhe te tjeret shtojne nje dorezim. wallet-at vazhdojne t'i drejtohen te njejtit ledger, duke pranuar vetem pergjigjet e bashkefirmosuara nga quorum-i. periodikisht, dhe kur asnje pergjigje nuk ka bashkefirmen e pritshme, wallet-a duhet te pyese rrjetin dhe te riluaje perditesimet e ledger-it per te identifikuar ndryshime ne custody

kur jo-konformiteti duket aksidental (p.sh., nje ledger behet i padisponueshem per nje numer te caktuar blloqesh) ndryshimi ne custody duhet te jete respektues: vetem shuma e reserve-ave e nevojshme per te mbuluar detyrimet e ledger-it dergohet ne llotari, dhe kusuri kthehet ne celesin publik te operator-it. kontrolli i collateral nuk preket

kur ekziston prove e jo-konformitetit, shuma ne teprice te reserve-ave te nevojshme ndahet ne menyre te barabarte ndermjet anetareve te quorum-it, dhe collateral i mbajtur ne ledger-at e anetareve lejohet te konfiskohet

## shendetsia e rrjetit

nje sulm i thjeshte eshte formimi i ishujve te operator-eve bashkepunues. pasi ndertojne detyrime te konsiderueshme neper ledger-at e tyre, ata koordinohen per te dalur, duke vjedhur fonde qe tejkalojne collateral e humbur. rrjeti mund te mbrohet kunder kesaj, pervecse ne rajone ku vlera e brendshme tejkalon collateral qe e lidh me rrjetin jo-bashkepunues. raportet me te larta te collateral dhe quorum-et me te medha e me te larmishme ulin mundesine e formimit te ketyre xhepave, por ato mund te formohen qellimisht dhe nuk mund te presim qe cdo wallet te vleresoje te gjithe rrjetin. ne vend te kesaj, tregjet e zbulimit duhet te publikojne metrika te pergjegjshmerise se operator-eve bazuar ne analiza grafike sic jane prize-collecting algorithm

## perfundimi

ne propozojme nje rrjet collateral qe kerkon bashkepunim per te vjedhur, por bashkepunimi e rrit collateral ne rrezik me shpejt sesa rrit vleren qe do te vidhet. ne e perdorim kete rrjet per te siguruar ledger-a kriptografike te mbeshtetur nga reserve te plota. keta ledger-a u sherbejne llogarive ne emer te wallet-ave jashte linje ne kembim te tarifave te paranegociuara. primitivat e ledger-it mbeshtesin kushte shpenzimi miniscript te mjaftueshme per kontrata te thjeshta inteligjente. rrjeti shkallezhohet pothuajse linearisht, duke i lejuar nje rrjeti te madh te ofroje miliarda wallet-a dhe volum transaksionesh qe tejkalon rrjetet tradicionale te pagesave
