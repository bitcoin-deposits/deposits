# bitcoin deposits
## rezumat

o versiune ideală peer-to-peer a banilor electronici ar permite ca plățile online să fie trimise direct de la o parte la alta rapid și cu o pregătire minimă. lightning network oferă o parte din soluție, dar beneficiile esențiale se pierd dacă este necesară o terță parte de încredere pentru a gestiona starea în numele tău. propunem o soluție la această problemă folosind registre verificabile și o rețea de garanții. operatorii difuzează actualizări ale registrelor către colegii lor, creând un istoric auditabil al conturilor. portofelele difuzează dovezi de necinste către acei colegi, care se asigură că registrul menține un operator onest. ieșirea unilaterală este înlocuită de garanția că fondurile rămân disponibile atât timp cât rețeaua funcționează. ajungem la o rețea care deleagă întreținerea lichidității, evită taxele de configurare, este capabilă să primească plăți offline și se scalează independent de stratul de bază

## introducere

bitcoin deposits își propune să ofere fonduri rapide și scalabile controlate prin chei, fără încredere, off-chain. activitatea on-chain se scalează cu numărul de registre și frecvența rotației rezervelor. capacitatea de procesare se scalează ușor supra-liniar cu numărul de registre din rețea, făcând plauzibile milioane de tranzacții pe secundă pe trilioane de portofele

există compromisuri explicite:
- fără ieșire unilaterală: când operatorii eșuează, fondurile rămân în rețea
- fără confidențialitate: verificarea necesită transparență
- disponibilitate intermitentă: un depozit este disponibil doar cât este operatorul. portofelele ar trebui să distribuie fondurile pentru a crește disponibilitatea

ne așteptăm ca experiența portofelului să fie similară cu un strat de bază rapid, având o economie a plăților similară cu lightning network

## registre

un registru este un lanț imuabil de actualizări, conținând hash-ul actualizării anterioare și semnat de operatorul registrului. diferite tipuri de actualizări au reguli diferite care guvernează când și cum pot fi utilizate. registrele sunt auto-descriptive, actualizările lor sunt disponibile public și non-repudiabile, permițând oricui să evalueze conformitatea

registrele au un singur operator activ, dar sunt întreținute cooperativ de rețea. orice operator poate crea unul, dar dacă dispare sau devine necinstit, un alt operator va fi desemnat, împreună cu rezervele. operatorul activ curent este identificat prin cheia publică utilizată pentru a semna cea mai recentă actualizare co-semnată

## depozite

un depozit este un cont stabil care poate trimite și primi fonduri, controlat prin miniscript. la deschidere se stabilește un program de taxe, precum și dacă primirea fondurilor necesită o cerere semnată de portofel. un operator trebuie să permită transferuri între depozitele de pe același registru, precum și ieșiri on-chain. ar trebui să permită depozitelor să plătească facturi lightning

este la discreția operatorului să creeze oferte de finanțare on-chain sau facturi lightning în numele unui depozit. dacă o face, acestea ar trebui să fie co-semnate de un membru al cvorumului, iar portofelul ar trebui să verifice această semnătură. ofertele și facturile nu fac parte din registru, deci este responsabilitatea portofelului să verifice semnăturile și să le păstreze ca dovadă

## taxe

transferurile între depozite, on-chain și prin lightning au taxe plătite operatorului registrului. există de asemenea taxe aplicate periodic soldurilor cu o perioadă specificată. toate sunt negociate la deschiderea unui nou depozit. taxele pot fi modificate după un număr specificat de blocuri, cu un preaviz specificat în blocuri și în limita unui procent per-ajustare negociat la deschidere. cvorumul poate refuza să co-semneze actualizări care creează circumstanțe neprofitabile de care ar putea fi în cele din urmă responsabili

## transferuri

forma de bază a transferului este o operațiune în două faze între două depozite de pe același registru: un depozit emite o cerere de trimitere a fondurilor. dacă există suficiente fonduri disponibile, un blocaj asupra fondurilor cu o condiție de cheltuire este adăugat la registru. dacă condiția de cheltuire este îndeplinită înainte de expirare, fondurile se mută de la expeditor la destinatar minus taxa operatorului. dacă expirarea este atinsă, blocajul este eliberat, minus o taxă mai mică a operatorului. cu condiții de cheltuire miniscript, aceasta este suficientă pentru a permite oricărui depozit să ofere servicii de punte și lichiditate altor depozite de pe același registru

## lightning

operatorii care au un canal lightning pot permite depozitelor să trimită și să primească prin lightning network. când un depozit solicită o factură lightning, operatorul creează una prin nodul său lightning, cere membrilor cvorumului să o co-semneze pentru a dovedi că se angajează să crediteze depozitul la plată. portofelul ar trebui să păstreze această factură co-semnată ca dovadă. când un depozit solicită plata unei facturi lightning, operatorul plătește folosind nodul său lightning și debitează depozitul după obținerea preimage-ului

când plătitorul și beneficiarul sunt depozite la același operator, operatorul poate efectua decontarea intern fără a ruta prin lightning, creditând și debitând depozitele respective direct. aceasta evită taxele de rutare și modurile de eșec, menținând în același timp aceleași garanții contabile

## curieri

cererile de transfer mută fonduri doar între depozite de pe același registru. pentru a muta fonduri între registre, portofelele folosesc curieri — servicii care dețin depozite pe mai multe registre și transportă transferuri între ele. un curier își face publică capacitatea și taxele direcționale per-registru pe releu. când un portofel dorește să trimită de pe registrul A pe registrul B, creează un blocaj de transfer către depozitul curierului și solicită curierului să creeze unul de la depozitul său de pe registrul destinație către beneficiar. odată ce ambele blocaje sunt stabilite, portofelul dezvăluie preimage-ul beneficiarului, care finalizează transferul de la curier. odată dezvăluit, curierul folosește același preimage pentru a finaliza transferul de la expeditor către curier

acesta este un model standard de contract hash time-locked. ne așteptăm ca expirarea de ieșire a curierului să fie strict anterioară celei de intrare, asigurând că dacă portofelul nu dezvăluie niciodată, ambele blocaje expiră și niciuna dintre părți nu pierde fonduri. nu este necesară încredere dincolo de garanția de expirare aplicată de operatori

curierii ar trebui să stabilească taxe per-registru: fee_in și fee_out pentru fiecare registru pe care îl deservesc. portofelul estimează costul rutei ca fee_out pe sursă plus fee_in pe destinație. curierii pot varia taxele per registru în funcție de lichiditatea disponibilă, reechilibrându-și natural pozițiile. portofelele descoperă curierii prin anunțurile lor pe releu și selectează pe baza taxei, capacității sau acoperirii

## comunicare

toată comunicarea între portofele și operatori, și între operatori, folosește relee nostr. actualizările registrelor sunt publicate ca evenimente durabile pe care releele le rețin, creând un istoric permanent auditabil. cererile și răspunsurile între portofele și operatori sunt evenimente efemere cu un TTL scurt pe releu. operatorii își fac publică oferta ca evenimente înlocuibile, permițând portofelelor să descopere și să compare operatorii fără un director centralizat

această arhitectură înseamnă că portofelele nu au nevoie de conexiuni persistente -- pot fi offline pe termen nedefinit și se pot sincroniza reluând evenimentele de pe orice releu care le deține. operatorii pot fi contactați prin orice releu pe care îl monitorizează, iar alegerea releului este o decizie de implementare, nu o constrângere de protocol

## rezerve și garanții

rezervele sunt deținute într-un utxo cu o sumă mai mare sau egală cu suma obligațiilor unui registru, cheltuibil de o majoritate a cvorumului, cu fallback către operator după o perioadă semnificativă

garanția este capitalul propriu al operatorului, depus și blocat pe registrele membrilor cvorumului. fiecare membru deține un depozit de garanție pe care operatorul îl finanțează și îl blochează pentru o durată specificată. obligațiile totale ale unui registru sunt limitate la de două ori cel mai mic blocaj de garanție deținut de orice membru, iar durata cvorumului este limitată la cel mai scurt timp de blocare. aceasta asigură că rețeaua de garanții are întotdeauna suficientă acoperire pentru a acoperi un transfer de custodie. același depozit de garanție poate susține mai multe registre pentru a îmbunătăți eficiența capitalului, deși portofelele ar trebui să prefere operatorii cu surse de garanție ne-suprapuse

obligațiile sunt aplicate la crearea de noi oferte de finanțare sau facturi. operatorul nu poate crea oferte sau facturi care ar împinge obligațiile totale ale registrului peste rezerve sau peste de două ori cel mai mic blocaj de garanție, oricare este mai mic

## cvorum

operatorii solicită altor operatori să se alăture cvorumului lor prin depunerea și blocarea garanției pe registrul membrului. cererea include angajamentul de garanție (suma și durata blocării) și termenii membrului: programele minime de taxe pe care depozitele de pe registru trebuie să le îndeplinească. fiecare membru trebuie să opereze propriul registru și poate confisca garanția operatorului dacă operatorul este dovedit neconform. membrii specifică limite ale programelor de taxe pe durata apartenenței la cvorum -- operatorul nu poate deschide depozite cu taxe sub minimele celui mai strict membru, protejând membrii de a moșteni obligații neprofitabile după un transfer de custodie

odată ce cvorumul este stabilit, rezervele sunt rotite într-un nou utxo multisig. membrii co-semnează actualizările valide și participă la recuperare dacă operatorul semnează actualizări neconforme. cvorumurile mai mari cresc costul comunicării dar reduc riscul operatorului, cresc disponibilitatea și fac coluzia mai dificilă și mai costisitoare. portofelele ar trebui să prefere cvorumuri mai mari

## descurajare economică

protocolul înlocuiește ieșirea unilaterală cu descurajarea economică. membrii cvorumului sunt stimulați direct să acționeze împotriva necinstei. în timpul operațiunilor normale câștigă taxe modeste pe garanție, dar în cazul unui comportament demonstrabil neconform pot confisca întregul depozit de garanție al operatorului de pe registrul lor

când un portofel suspectează cenzură, poate escalada cererea către membrii cvorumului prin livrare certificată. membrul încorporează hash-ul cererii în propriul registru pentru o taxă mică, creând dovezi ancorate cauzal. dacă operatorul nu procesează cererea, membrul deține atât dovezile cât și stimulentul economic pentru a iniția o dispută

frauda cu facturi lightning urmează același model de descurajare. operatorul știe dacă un preimage a fost primit, dar portofelul nu știe. cu toate acestea, orice plătitor ar putea furniza preimage-ul portofelului. un singur furt confirmat declanșează disputa, confiscarea rezervelor și confiscarea garanției. recompensa furtului unei singure plăți este limitată, dar riscul este existențial, făcând furtul prin lightning irațional economic, deși formal nedemonstrabil fără cooperarea unei terțe părți

modul de eșec atât pentru cenzură cât și pentru descurajarea lightning este coluzia unanimă a cvorumului. protocolul nu poate proteja împotriva unui cvorum care cooperează pentru a fura, dar rețeaua de garanții asigură că coluzia costă mai mult decât câștigă. transparența rețelei permite portofelelor și piețelor de descoperire să identifice structuri suspecte de cvorum înainte de a depune fonduri

## timp

timpul absolut este măsurat în raport cu stratul de bază. toleranțele nu pot depăși un număr rezonabil de confirmări pentru a menține stabilitatea în timpul reorganizărilor lanțului

acolo unde sunt necesare toleranțe mai mari ne bazăm pe ordonarea cauzală. un registru criptografic este un lanț merkle. fiecare actualizare dovedește că a fost creată după toate actualizările anterioare, dar nu oferă garanții despre informații din afara lanțului. pentru a construi o ordonare distribuită, cerem ca co-semnăturile să includă cel mai recent hash de actualizare din registrul co-semnatarului. acel hash este apoi încorporat în hash-ul actualizării curente, devenind parte atât din lanț cât și din toate celelalte lanțuri pentru care operatorul registrului co-semnează, creând o rețea de cauzalitate. aceasta nu poate dovedi timpul explicit, dar poate dovedi că anumite informații au fost create într-o ordine specifică

## dovezi de fraudă

putem dovedi diverse tipuri de fraudă prin expunerea informațiilor care au fost create în ordinea greșită. acolo unde informația nu este inclusă prin operațiunile normale ale rețelei, poate fi introdusă prin crearea de activitate care include un hash al dovezii. odată încorporată într-o actualizare semnată de operator, dovada este dezvăluită ca fiind creată într-un loc neconform în ordonare:

- un operator, având oferit să crediteze un depozit cu fonduri trimise on-chain la o adresă specifică, semnează o actualizare a registrului care nu conține creditul corespunzător, dar conține un lanț care dezvăluie un hash de bloc ce depășește numărul de confirmări permise înainte de creditare

- un operator, având creat o factură lightning în numele unui depozit, semnează o actualizare a registrului care nu a creditat depozitul în ciuda preimage-ului dezvăluit în lanț

- o co-semnătură care declară hash-ul curent al registrului ca fiind unul care precede propriul hash ulterior din lanț

- un membru al cvorumului unui registru contestat care era activ dar nu a acționat în conformitate cu dovada de fraudă în cadrul unui număr de blocuri

- semnarea sau co-semnarea actualizărilor neconforme ale registrului

o dovadă de fraudă constă din dovezi și un lanț cauzal care conectează hash-ul încorporat la registrul operatorului acuzat. lanțul este o secvență de actualizări co-semnate, fiecare incluzând un member_ledger_hash din registrul verigii anterioare. verificatorii parcurg lanțul fără căutare, confirmând că fiecare verigă este o actualizare semnată și că hash-ul dovezii corespunde datelor încorporate

## recuperare

odată ce un registru a devenit indisponibil sau neconform, membrii cvorumului pot crea propria lor continuare a registrului de la ultima actualizare conformă. trebuie să stabilească un nou cvorum și să furnizeze atestări de garanție. membrii trebuie apoi să se coordoneze pentru a cheltui ieșirea anterioară de rezerve către o loterie a potențialelor lanțuri următoare. câștigătorul acestei loterii adaugă o actualizare de achiziție la lanțul său, iar ceilalți adaugă o cedare. portofelele continuă să se adreseze aceluiași registru, acceptând doar răspunsuri co-semnate de cvorum. periodic, și când niciun răspuns nu are co-semnătura așteptată, portofelul ar trebui să interogheze rețeaua și să relueze actualizările registrului pentru a identifica schimbările de custodie

când neconformitatea pare accidentală (de ex., un registru a devenit indisponibil pentru un anumit număr de blocuri) schimbarea custodiei trebuie să fie respectuoasă: doar suma de rezerve necesară pentru a acoperi obligațiile registrului este trimisă la loterie, iar restul este trimis înapoi la cheia publică a operatorului. controlul garanției nu este afectat

când există dovada de neconformitate, suma în exces față de rezervele necesare este împărțită în mod egal între membrii cvorumului, iar garanția deținută pe registrele membrilor poate fi confiscată

## sănătatea rețelei

un atac simplu este formarea de insule de operatori complici. după acumularea unor obligații substanțiale pe registrele lor, se coordonează pentru a ieși, furând fonduri care depășesc garanția pierdută. rețeaua se poate apăra împotriva acestui lucru, cu excepția regiunilor în care valoarea internă depășește garanția care o conectează la rețeaua ne-complice. raporturi de garanție mai mari și cvorumuri mai mari și mai diverse reduc probabilitatea formării acestor buzunare, dar se pot forma intenționat și nu ne putem aștepta ca fiecare portofel să evalueze întreaga rețea. în schimb, piețele de descoperire ar trebui să publice metrici de responsabilitate a operatorilor bazate pe analize de graf, cum ar fi algoritmii prize-collecting

## concluzie

propunem o rețea de garanții care necesită coluzie pentru a fura, dar coluzia crește garanția în pericol mai repede decât crește valoarea de furat. folosim această rețea pentru a securiza registre criptografice susținute de rezerve integrale. aceste registre deservesc conturi în numele portofelelor offline în schimbul unor taxe pre-negociate. primitivele registrelor suportă condiții de cheltuire miniscript suficiente pentru contracte inteligente de bază. rețeaua se scalează aproape liniar, permițând unei rețele mari să ofere miliarde de portofele și un volum de tranzacții care depășește rețelele de plăți tradiționale
