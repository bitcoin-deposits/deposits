# bitcoin deposits
## abstract

una versione ideale peer-to-peer di denaro elettronico permetterebbe di inviare pagamenti online direttamente da una parte all'altra in modo rapido e con una preparazione minima. la lightning network fornisce parte della soluzione, ma i benefici essenziali vengono persi se una terza parte fidata e' richiesta per gestire lo stato per conto dell'utente. proponiamo una soluzione a questo problema utilizzando registri verificabili e una rete di garanzie collaterali. gli operatori trasmettono aggiornamenti del registro ai loro pari, creando un registro verificabile dei conti. i portafogli trasmettono prove di disonesta' a quei pari, che assicurano che il registro mantenga un operatore onesto. l'uscita unilaterale e' sostituita dalla garanzia che i fondi rimangano disponibili finche' la rete lo e'. arriviamo a una rete che delega la manutenzione della liquidita', evita le commissioni di configurazione, e' capace di ricevere pagamenti offline e scala indipendentemente dal livello base

## introduzione

bitcoin deposits mira a fornire fondi veloci e scalabili controllati da chiave, senza fiducia, off-chain. l'attivita' on-chain scala con il numero di registri e la frequenza di rotazione delle riserve. il throughput scala leggermente piu' che linearmente con il numero di registri nella rete, rendendo plausibili milioni di transazioni al secondo attraverso trilioni di portafogli

ci sono compromessi espliciti:
- nessuna uscita unilaterale: quando gli operatori falliscono i fondi rimangono nella rete
- nessuna privacy: la verifica richiede trasparenza
- disponibilita' intermittente: un deposito e' disponibile solo quanto lo e' l'operatore. i portafogli dovrebbero distribuire i fondi per aumentare la disponibilita'

ci aspettiamo che l'esperienza del portafoglio sia simile a un livello base veloce, con un'economia dei pagamenti simile alla lightning network

## registri

un registro e' una catena immutabile di aggiornamenti, contenente il hash dell'aggiornamento precedente e firmato dall'operatore del registro. diversi tipi di aggiornamento hanno regole diverse che governano quando e come possono essere utilizzati. i registri sono auto-descrittivi, i loro aggiornamenti sono pubblicamente disponibili e non ripudiabili, permettendo a chiunque di valutarne la conformita'

i registri hanno un singolo operatore attivo, ma sono mantenuti cooperativamente dalla mesh. qualsiasi operatore puo' crearne uno, ma se dovesse scomparire o diventare disonesto, un operatore diverso verra' assegnato, insieme alle riserve. l'operatore attualmente attivo e' identificato dalla chiave pubblica utilizzata per firmare l'aggiornamento co-firmato piu' recente

## depositi

un deposito e' un conto stabile che puo' inviare e ricevere fondi, controllato da miniscript. all'apertura viene stabilito un piano tariffario, cosi' come se la ricezione di fondi richieda una richiesta firmata dal portafoglio. un operatore deve consentire trasferimenti tra depositi sullo stesso registro cosi' come uscite on-chain. dovrebbero consentire ai depositi di pagare fatture lightning

e' a discrezione dell'operatore creare offerte di finanziamento on-chain o fatture lightning per conto di un deposito. se lo fanno, queste dovrebbero essere co-firmate da un membro del quorum, e il portafoglio dovrebbe verificare questa firma. offerte e fatture non fanno parte del registro, quindi e' responsabilita' del portafoglio verificare le firme e conservarle come prova

## commissioni

i trasferimenti tra depositi, on-chain e attraverso lightning hanno commissioni pagate all'operatore del registro. ci sono anche commissioni applicate periodicamente ai saldi con un periodo specificato. tutte sono negoziate quando un nuovo deposito viene aperto. le commissioni possono essere modificate dopo un numero specificato di blocchi, dato un preavviso specificato in blocchi e entro un limite percentuale per aggiustamento negoziato all'apertura. il quorum puo' rifiutare di co-firmare aggiornamenti che creano circostanze non redditizie di cui potrebbero in ultima analisi essere responsabili

## trasferimenti

la forma base di trasferimento e' un'operazione in due fasi tra due depositi sullo stesso registro: un deposito emette una richiesta di invio fondi. se ci sono fondi sufficienti disponibili, un blocco sui fondi con una condizione di spesa viene aggiunto al registro. se la condizione di spesa viene soddisfatta prima di un timeout, i fondi si spostano dal mittente al destinatario meno la commissione dell'operatore. se il timeout viene raggiunto, il blocco viene rilasciato, meno una commissione dell'operatore piu' piccola. con condizioni di spesa miniscript, questo e' sufficiente per permettere a qualsiasi deposito di fornire ponti e servizi di liquidita' ad altri depositi sullo stesso registro

## lightning

gli operatori che hanno un canale lightning possono consentire ai depositi di inviare e ricevere attraverso la lightning network. quando un deposito richiede una fattura lightning, l'operatore ne crea una attraverso il proprio nodo lightning, chiede ai membri del quorum di co-firmarla per dimostrare che si impegnano ad accreditare il deposito al momento del pagamento. il portafoglio dovrebbe conservare questa fattura co-firmata come prova. quando un deposito richiede il pagamento di una fattura lightning, l'operatore paga utilizzando il proprio nodo lightning e addebita il deposito dopo aver ottenuto il preimage

quando il pagante e il beneficiario sono depositi sullo stesso operatore, l'operatore puo' regolare internamente senza instradare attraverso lightning, accreditando e addebitando i rispettivi depositi direttamente. questo evita le commissioni di instradamento e le modalita' di fallimento mantenendo le stesse garanzie contabili

## corrieri

le richieste di trasferimento spostano fondi solo tra depositi sullo stesso registro. per spostare fondi tra registri diversi, i portafogli utilizzano corrieri — servizi che detengono depositi su piu' registri e trasportano trasferimenti tra di essi. un corriere pubblicizza capacita' e commissioni direzionali per registro sul relay. quando un portafoglio vuole inviare dal registro A al registro B, crea un blocco di trasferimento al deposito del corriere e richiede che il corriere ne crei uno dal proprio deposito sul registro di destinazione al beneficiario. una volta che entrambi i blocchi sono stabiliti, il portafoglio rivela il preimage al beneficiario, che completa il trasferimento dal corriere. una volta rivelato, il corriere usa lo stesso preimage per completare il trasferimento dal mittente al corriere

questo e' un pattern standard di contratto hash time-locked. ci aspettiamo che il timeout in uscita del corriere sia rigorosamente anteriore a quello in entrata, assicurando che se il portafoglio non rivela mai, entrambi i blocchi scadono e nessuna delle parti perde fondi. non e' richiesta fiducia oltre alla garanzia di timeout applicata dagli operatori

i corrieri dovrebbero impostare commissioni per registro: fee_in e fee_out per ogni registro che servono. il portafoglio stima il costo del percorso come fee_out sulla sorgente piu' fee_in sulla destinazione. i corrieri possono variare le commissioni per registro in base alla liquidita' disponibile, riequilibrando naturalmente le proprie posizioni. i portafogli scoprono i corrieri attraverso i loro annunci sul relay e selezionano in base a commissione, capacita' o copertura

## comunicazione

tutta la comunicazione tra portafogli e operatori, e tra operatori, utilizza relay nostr. gli aggiornamenti del registro sono pubblicati come eventi durevoli che i relay conservano, creando un registro permanente verificabile. le richieste e le risposte tra portafogli e operatori sono eventi effimeri con un breve TTL sul relay. gli operatori pubblicizzano i propri termini come eventi sostituibili, permettendo ai portafogli di scoprire e confrontare operatori senza una directory centralizzata

questa architettura significa che i portafogli non necessitano di connessioni persistenti -- possono andare offline indefinitamente e recuperare riproducendo gli eventi da qualsiasi relay che li possieda. gli operatori possono essere raggiunti attraverso qualsiasi relay che monitorano, e la scelta del relay e' una decisione di deployment, non un vincolo del protocollo

## riserve e garanzie collaterali

le riserve sono detenute in un utxo con un importo maggiore o uguale alla somma delle obbligazioni di un registro, spendibile da una maggioranza del quorum, con fallback all'operatore dopo un periodo significativo

la garanzia collaterale e' il capitale proprio dell'operatore, depositato e bloccato sui registri dei membri del quorum. ogni membro detiene un deposito di garanzia collaterale che l'operatore finanzia e blocca per una durata specificata. le obbligazioni totali di un registro sono limitate al doppio del blocco di garanzia collaterale piu' piccolo detenuto da qualsiasi membro, e la durata del quorum e' limitata al tempo di blocco piu' breve. questo assicura che la rete di garanzie collaterali abbia sempre abbastanza copertura per gestire un trasferimento di custodia. lo stesso deposito di garanzia collaterale puo' garantire piu' registri per migliorare l'efficienza del capitale, anche se i portafogli dovrebbero preferire operatori con fonti di garanzia collaterale non sovrapposte

le obbligazioni sono verificate quando si creano nuove offerte di finanziamento o fatture. l'operatore non puo' creare offerte o fatture che porterebbero le obbligazioni totali del registro al di sopra delle riserve o al di sopra del doppio del blocco di garanzia collaterale piu' piccolo, a seconda di quale sia inferiore

## quorum

gli operatori richiedono ad altri operatori di unirsi al loro quorum depositando e bloccando garanzia collaterale sul registro del membro. la richiesta include l'impegno di garanzia collaterale (importo e durata del blocco) e i termini del membro: piani tariffari minimi che i depositi sul registro devono rispettare. ogni membro deve gestire il proprio registro e puo' confiscare la garanzia collaterale dell'operatore se l'operatore risulta non conforme. i membri specificano limiti sui piani tariffari durante la loro appartenenza al quorum -- l'operatore non puo' aprire depositi con commissioni inferiori ai minimi del membro piu' severo, proteggendo i membri dall'ereditare obbligazioni non redditizie dopo un trasferimento di custodia

una volta che il quorum e' stabilito, le riserve vengono ruotate in un nuovo utxo multisig. i membri co-firmano aggiornamenti validi e partecipano al recupero se l'operatore firma aggiornamenti non conformi. quorum piu' grandi aumentano il sovraccarico di comunicazione ma riducono il rischio dell'operatore, aumentano la disponibilita' e rendono la collusione piu' difficile e costosa. i portafogli dovrebbero preferire quorum piu' grandi

## deterrenza economica

il protocollo sostituisce l'uscita unilaterale con la deterrenza economica. i membri del quorum sono direttamente incentivati ad agire contro la disonesta'. durante le operazioni normali guadagnano commissioni modeste sulla garanzia collaterale, ma in caso di comportamento dimostrabilmente non conforme possono confiscare l'intero deposito di garanzia collaterale dell'operatore sul loro registro

quando un portafoglio sospetta censura, puo' escalare la richiesta ai membri del quorum tramite consegna certificata. il membro incorpora il hash della richiesta nel proprio registro per una piccola commissione, creando prove ancorate causalmente. se l'operatore non riesce a elaborare la richiesta, il membro ha sia le prove che l'incentivo economico per avviare una disputa

la frode sulle fatture lightning segue lo stesso schema di deterrenza. l'operatore sa se un preimage e' stato ricevuto, ma il portafoglio no. tuttavia qualsiasi pagante potrebbe fornire il preimage al portafoglio. un singolo furto confermato innesca disputa, sequestro delle riserve e confisca della garanzia collaterale. la ricompensa del furto di un singolo pagamento e' limitata, ma il rischio e' esistenziale, rendendo il furto lightning economicamente irrazionale nonostante sia formalmente non dimostrabile senza cooperazione di terze parti

la modalita' di fallimento sia per la censura che per la deterrenza lightning e' la collusione unanime del quorum. il protocollo non puo' proteggere contro un quorum che coopera per rubare, ma la rete di garanzie collaterali assicura che la collusione costi piu' di quanto produca. la trasparenza della rete permette ai portafogli e ai mercati di scoperta di identificare strutture di quorum sospette prima di depositare fondi

## tempo

il tempo assoluto e' misurato rispetto al livello base. le tolleranze non possono superare un numero ragionevole di conferme per mantenere la stabilita' durante le riorganizzazioni della catena

dove sono richieste tolleranze maggiori ci affidiamo all'ordinamento causale. un registro crittografico e' una catena merkle. ogni aggiornamento prova di essere stato creato dopo tutti gli aggiornamenti precedenti, ma non fornisce garanzie sulle informazioni esterne alla catena. per costruire un ordinamento distribuito, richiediamo che le co-firme includano l'ultimo hash di aggiornamento dal registro del co-firmatario. quell'hash viene poi incorporato nell'hash dell'aggiornamento corrente, diventando parte della catena cosi' come parte di tutte le altre catene per cui l'operatore del registro co-firma, creando una rete di causalita'. questo non e' in grado di provare il tempo esplicitamente, ma e' in grado di provare che certi pezzi di informazione sono stati creati in un ordine specifico

## prove di frode

possiamo provare vari tipi di frode esponendo informazioni che sono state create nell'ordine sbagliato. dove le informazioni non sono incluse dalle normali operazioni di rete, possono essere introdotte creando attivita' che include un hash delle prove. una volta incorporate in un aggiornamento firmato dall'operatore, le prove vengono rivelate come create in un punto non conforme nell'ordinamento:

- un operatore, avendo offerto di accreditare un deposito con fondi inviati on-chain a un indirizzo specifico, firma un aggiornamento del registro che non contiene l'accredito appropriato, ma contiene una catena che rivela un hash di blocco che eccede il numero di conferme consentite prima dell'accredito

- un operatore, avendo creato una fattura lightning per conto di un deposito, firma un aggiornamento del registro che non ha accreditato il deposito nonostante il preimage sia stato rivelato nella catena

- una co-firma che dichiara che l'hash corrente del registro sia uno che precede il proprio hash successivo nella catena

- un membro del quorum di un registro contestato che era attivo ma non ha agito in conformita' con la prova di frode entro un certo numero di blocchi

- firmare o co-firmare aggiornamenti del registro non conformi

una prova di frode consiste nelle prove e in una catena causale che collega il hash incorporato al registro dell'operatore accusato. la catena e' una sequenza di aggiornamenti co-firmati, ognuno dei quali include un member_ledger_hash dal registro del collegamento precedente. i verificatori percorrono la catena senza cercare, confermando che ogni collegamento e' un aggiornamento firmato e che il hash della prova corrisponde ai dati incorporati

## recupero

una volta che un registro e' diventato non disponibile o non conforme, i membri del quorum possono creare la propria continuazione del registro dall'ultimo aggiornamento conforme. devono stabilire un nuovo quorum e fornire attestazioni di garanzia collaterale. i membri devono poi coordinarsi per spendere l'output delle riserve precedenti in una lotteria delle potenziali catene successive. il vincitore di questa lotteria aggiunge un aggiornamento di acquisizione alla propria catena, e gli altri aggiungono una cessione. i portafogli continuano ad indirizzare lo stesso registro, accettando solo risposte co-firmate dal quorum. periodicamente, e quando nessuna risposta ha la co-firma attesa, il portafoglio dovrebbe interrogare la rete e riprodurre gli aggiornamenti del registro per identificare cambiamenti nella custodia

quando la non conformita' appare accidentale (ad esempio, un registro e' diventato non disponibile per un certo numero di blocchi) il cambio di custodia deve essere rispettoso: solo l'importo delle riserve necessario a coprire le obbligazioni del registro viene inviato alla lotteria, e il resto viene restituito alla chiave pubblica dell'operatore. il controllo della garanzia collaterale non e' influenzato

quando esiste prova di non conformita', l'importo in eccesso rispetto alle riserve necessarie viene diviso equamente tra i membri del quorum, e la garanzia collaterale detenuta sui registri dei membri puo' essere confiscata

## salute della rete

un attacco diretto e' formare isole di operatori collusi. dopo aver accumulato obbligazioni sostanziali attraverso i propri registri, si coordinano per uscire, rubando fondi che eccedono la garanzia collaterale persa. la rete puo' difendersi da questo, tranne nelle regioni dove il valore interno eccede la garanzia collaterale che la collega alla rete non collusa. rapporti di garanzia collaterale piu' alti e quorum piu' grandi e diversificati riducono la probabilita' che queste sacche si formino, ma possono formarsi intenzionalmente e non possiamo aspettarci che ogni portafoglio valuti l'intera rete. invece i mercati di scoperta dovrebbero pubblicare metriche di responsabilita' degli operatori basate su analisi del grafo come algoritmi di raccolta premi

## conclusione

proponiamo una rete di garanzie collaterali che richiede collusione per rubare, ma la collusione aumenta la garanzia collaterale a rischio piu' velocemente di quanto aumenti il valore da rubare. utilizziamo questa rete per proteggere registri crittografici supportati da riserve complete. questi registri servono conti per conto di portafogli offline in cambio di commissioni pre-negoziate. le primitive del registro supportano condizioni di spesa miniscript sufficienti per contratti intelligenti di base. la rete scala quasi linearmente, permettendo a una grande rete di fornire miliardi di portafogli e un volume di transazioni superiore a quello delle reti di pagamento tradizionali
