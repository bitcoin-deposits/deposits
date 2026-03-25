# bitcoin deposits
## sammendrag

en ideell likeperson-til-likeperson-versjon av elektroniske kontanter ville tillate nettbetalinger å bli sendt direkte fra en part til en annen, raskt og med minimal forberedelse. lightning-nettverket gir deler av løsningen, men de vesentlige fordelene går tapt dersom en betrodd tredjepart er nødvendig for å administrere tilstand på dine vegne. vi foreslår en løsning på dette problemet ved bruk av verifiserbare hovedbøker og et nett av sikkerhetsstillelse. operatører kringkaster hovedbokoppdateringer til sine likepersoner, og skaper et reviderbart register over kontoer. lommebøker kringkaster bevis på uærlighet til disse likepersonene, som sørger for at hovedboken opprettholdes av en ærlig operatør. ensidig utgang erstattes av garantien om at midler forblir tilgjengelige så lenge nettverket gjør det. vi ender opp med et nettverk som delegerer likviditetsforvaltning, unngår oppsettsgebyrer, er i stand til å motta betalinger frakoblet, og skalerer uavhengig av grunnlaget

## introduksjon

bitcoin deposits har som mål å tilby raske og skalerbare nøkkelkontrollerte midler, tillitsløst, utenfor kjeden. aktivitet på kjeden skalerer med antall hovedbøker og hyppigheten av reserverotasjon. gjennomstrømming skalerer litt over lineært med antall hovedbøker i nettverket, noe som gjør millioner av transaksjoner per sekund over billioner av lommebøker plausibelt

det er eksplisitte avveininger:
- ingen ensidig utgang: når operatører feiler, forblir midlene i nettverket
- ingen personvern: verifisering krever åpenhet
- periodisk tilgjengelighet: et innskudd er bare så tilgjengelig som operatøren. lommebøker bør spre midler for å øke tilgjengeligheten

vi forventer at lommebokopplevelsen vil ligne et raskt grunnlag, med betalingsøkonomi lik lightning-nettverket

## hovedbøker

en hovedbok er en uforanderlig kjede av oppdateringer, som inneholder hashen av den forrige oppdateringen og er signert av hovedbokens operatør. ulike typer oppdateringer har forskjellige regler som styrer når og hvordan de kan brukes. hovedbøker er selvbeskrivende, deres oppdateringer er offentlig tilgjengelige og ikke-benektbare, noe som lar hvem som helst evaluere samsvar

hovedbøker har én enkelt aktiv operatør, men vedlikeholdes i samarbeid av nettverket. enhver operatør kan opprette en, men skulle de forsvinne eller bli uærlige, vil en annen operatør bli tildelt, sammen med reserver. den nåværende aktive operatøren identifiseres av den offentlige nøkkelen som ble brukt til å signere den sist samsignerte oppdateringen

## innskudd

et innskudd er en stabil konto som kan sende og motta midler, kontrollert av miniscript. ved åpning etableres en gebyrplan, samt hvorvidt mottak av midler krever en lommebok-signert forespørsel. en operatør må tillate overføringer mellom innskudd på samme hovedbok samt utganger på kjeden. de bør tillate innskudd å betale lightning-fakturaer

det er opp til operatørens skjønn å opprette finansieringstilbud på kjeden eller lightning-fakturaer på vegne av et innskudd. hvis de gjør det, bør disse samsigneres av et kvorummedlem, og lommeboken bør verifisere denne signaturen. tilbud og fakturaer er ikke del av hovedboken, så det er lommebokens ansvar å verifisere signaturer og beholde dem som bevis

## gebyrer

overføringer mellom innskudd, på kjeden og gjennom lightning har gebyrer som betales til hovedbokens operatør. det er også gebyrer som periodisk pålegges saldoer med en spesifisert periode. alle forhandles når et nytt innskudd åpnes. gebyrer kan endres etter et spesifisert antall blokker, gitt et spesifisert blokkvarsel og innenfor en prosentvis grense per justering som forhandles ved åpning. kvorumet kan nekte å samsignere oppdateringer som skaper ulønnsomme omstendigheter som de til slutt kan bli ansvarlige for

## overføringer

den grunnleggende formen for overføring er en tofaset operasjon mellom to innskudd på samme hovedbok: et innskudd utsteder en forespørsel om å sende midler. hvis det er tilstrekkelige midler tilgjengelig, legges en lås på midlene med en bruksbetingelse til hovedboken. hvis bruksbetingelsen oppfylles før en tidsfrist, flyttes midlene fra avsender til mottaker minus operatørens gebyr. hvis tidsfristen nås, frigjøres låsen, minus et mindre operatørgebyr. med miniscript-bruksbetingelser er dette tilstrekkelig for å la ethvert innskudd tilby bro- og likviditetstjenester til andre innskudd på samme hovedbok

## lightning

operatører som har en lightning-kanal kan tillate innskudd å sende og motta over lightning-nettverket. når et innskudd ber om en lightning-faktura, oppretter operatøren en gjennom sin lightning-node, ber kvorummedlemmer om å samsignere den for å bevise at de forplikter seg til å kreditere innskuddet ved betaling. lommeboken bør beholde denne samsignerte fakturaen som bevis. når et innskudd ber om betaling av en lightning-faktura, betaler operatøren via sin lightning-node og debiterer innskuddet etter å ha innhentet preimage

når betaler og mottaker er innskudd hos samme operatør, kan operatøren gjøre opp internt uten å rute gjennom lightning, og kreditere og debitere de respektive innskuddene direkte. dette unngår rutingsgebyrer og feilmoduser samtidig som de samme regnskapsgarantiene opprettholdes

## kurerer

overføringsforespørsler flytter kun midler mellom innskudd på samme hovedbok. for å flytte midler mellom hovedbøker bruker lommebøker kurerer — tjenester som holder innskudd på flere hovedbøker og bærer overføringer mellom dem. en kurer annonserer kapasitet og retningsbestemte gebyrer per hovedbok på reléet. når en lommebok ønsker å sende fra hovedbok A til hovedbok B, oppretter den en overføringslås til kurerens innskudd og ber kureren om å opprette en fra sitt innskudd på destinasjonshovedbo­ken til mottakeren. når begge låser er etablert, avslører lommeboken preimage til mottakeren, som fullfører overføringen fra kureren. når den er avslørt, bruker kureren samme preimage for å fullføre overføringen fra avsenderen til kureren

dette er et standard hash-tidslåst kontraktmønster. vi forventer at kurerens utgående tidsfrist er strengt tidligere enn den innkommende, slik at hvis lommeboken aldri avslører, utløper begge låsene og ingen av partene taper midler. ingen tillit er nødvendig utover tidsfristen som håndheves av operatører

kurerer bør sette gebyrer per hovedbok: fee_in og fee_out for hver hovedbok de betjener. lommeboken estimerer rutekostnad som fee_out på kilden pluss fee_in på destinasjonen. kurerer kan variere gebyrer per hovedbok basert på tilgjengelig likviditet, og rebalanserer naturlig sine posisjoner. lommebøker oppdager kurerer gjennom deres annonseringer på reléet og velger basert på gebyr, kapasitet eller dekning

## kommunikasjon

all kommunikasjon mellom lommebøker og operatører, og mellom operatører, bruker nostr-reléer. hovedbokoppdateringer publiseres som varige hendelser som reléer beholder, og skaper et permanent reviderbart register. forespørsler og svar mellom lommebøker og operatører er flyktige hendelser med kort relé-TTL. operatører annonserer sine vilkår som erstattbare hendelser, noe som lar lommebøker oppdage og sammenligne operatører uten en sentralisert katalog

denne arkitekturen betyr at lommebøker ikke trenger vedvarende tilkoblinger — de kan gå frakoblet på ubestemt tid og ta igjen ved å spille av hendelser fra et hvilket som helst relé som har dem. operatører kan nås gjennom et hvilket som helst relé de overvåker, og valg av relé er en distribusjonsbeslutning, ikke en protokollbegrensning

## reserver og sikkerhetsstillelse

reserver holdes i en utxo med et beløp større enn eller lik summen av en hovedboks forpliktelser, som kan brukes av et flertall av kvorumet, med tilbakefall til operatøren etter en betydelig periode

sikkerhetsstillelse er operatørens egen kapital, satt inn og låst på kvorummedlemmers hovedbøker. hvert medlem har et sikkerhetsinnskudd som operatøren finansierer og låser for en spesifisert varighet. en hovedboks totale forpliktelser er begrenset til det dobbelte av den minste sikkerhetslåsen holdt av et hvilket som helst medlem, og kvorumets varighet er begrenset til den korteste låsetiden. dette sikrer at sikkerhetsnettet alltid har tilstrekkelig dekning til å dekke en depotoverføring. samme sikkerhetsinnskudd kan dekke flere hovedbøker for å forbedre kapitaleffektiviteten, selv om lommebøker bør foretrekke operatører med ikke-overlappende sikkerhetskilder

forpliktelser håndheves ved opprettelse av nye finansieringstilbud eller fakturaer. operatøren kan ikke opprette tilbud eller fakturaer som ville presse hovedbokens totale forpliktelser over reservene eller over det dobbelte av den minste sikkerhetslåsen, avhengig av hva som er lavest

## kvorum

operatører ber andre operatører om å bli med i sitt kvorum ved å sette inn og låse sikkerhetsstillelse på medlemmets hovedbok. forespørselen inkluderer sikkerhetsforpliktelsen (beløp og låsevarighet) og medlemmets vilkår: minimumsgebyrplaner som innskudd på hovedboken må oppfylle. hvert medlem må drifte sin egen hovedbok og kan beslaglegge operatørens sikkerhetsstillelse hvis operatøren bevises å ikke være i samsvar. medlemmer spesifiserer grenser for gebyrplaner under sitt kvorummedlemskap — operatøren kan ikke åpne innskudd med gebyrer under det strengeste medlemmets minimumskrav, noe som beskytter medlemmer fra å arve ulønnsomme forpliktelser etter en depotoverføring

når kvorumet er etablert, roteres reserver inn i en ny multisig utxo. medlemmer samsignerer gyldige oppdateringer og deltar i gjenoppretting hvis operatøren signerer oppdateringer som ikke er i samsvar. større kvorumer øker kommunikasjonsoverhead, men reduserer operatørrisiko, øker tilgjengelighet og gjør sammensvergelse vanskeligere og dyrere. lommebøker bør foretrekke større kvorumer

## økonomisk avskrekning

protokollen erstatter ensidig utgang med økonomisk avskrekning. kvorummedlemmer er direkte incentiverte til å handle mot uærlighet. under normal drift tjener de beskjedne gebyrer på sikkerhetsstillelse, men i tilfelle av beviselig ikke-samsvarende atferd kan de beslaglegge operatørens fulle sikkerhetsinnskudd på sin hovedbok

når en lommebok mistenker sensur, kan den eskalere forespørselen til kvorummedlemmer via sertifisert levering. medlemmet legger inn forespørselens hash i sin egen hovedbok mot et lite gebyr, og skaper kausalt forankret bevis. hvis operatøren unnlater å behandle forespørselen, har medlemmet både beviset og det økonomiske incentivet til å innlede en tvist

lightning-fakturabedrageri følger samme avskrekkingsmønster. operatøren vet om en preimage ble mottatt, men lommeboken vet det ikke. imidlertid kan enhver betaler gi preimage til lommeboken. et enkelt bekreftet tyveri utløser tvist, beslaglegging av reserver og konfiskering av sikkerhetsstillelse. belønningen ved å stjele en enkelt betaling er begrenset, men risikoen er eksistensiell, noe som gjør lightning-tyveri økonomisk irrasjonelt til tross for at det formelt sett ikke kan bevises uten tredjepartssamarbeid

feilmodusen for både sensur- og lightning-avskrekning er enstemmig kvorumsammensvergelse. protokollen kan ikke beskytte mot et kvorum som samarbeider om å stjele, men sikkerhetsnettet sikrer at sammensvergelse koster mer enn det gir. nettverkets åpenhet lar lommebøker og oppdagelsesmarkeder identifisere mistenkelige kvorumstrukturer før de setter inn midler

## tid

absolutt tid måles mot grunnlaget. toleranser kan ikke overstige et rimelig antall bekreftelser for å opprettholde stabilitet under omorganiseringer av kjeden

der høyere toleranser kreves, stoler vi på kausal rekkefølge. en kryptografisk hovedbok er en merkle-kjede. hver oppdatering beviser at den ble opprettet etter alle oppdateringer før den, men gir ingen garantier om informasjon utenfor kjeden. for å konstruere en distribuert rekkefølge krever vi at samsignaturer inkluderer den siste oppdateringens hash fra samsignerens hovedbok. denne hashen inkorporeres deretter i den nåværende oppdateringens hash, og blir del av kjeden samt del av alle andre kjeder som hovedbokoperatøren samsignerer for, og skaper et nett av kausalitet. dette kan ikke bevise tid eksplisitt, men kan bevise at visse opplysninger ble opprettet i en bestemt rekkefølge

## svindelbevis

vi kan bevise ulike typer svindel ved å eksponere informasjon som har blitt opprettet i feil rekkefølge. der informasjon ikke inkluderes av normal nettverksdrift, kan den smugles inn ved å opprette aktivitet som inkluderer en hash av beviset. når det er inkorporert i en oppdatering signert av operatøren, avsløres beviset som opprettet på et ikke-samsvarende sted i rekkefølgen:

- en operatør som har tilbudt å kreditere et innskudd med midler sendt på kjeden til en spesifikk adresse, signerer en hovedbokoppdatering som ikke inneholder den riktige krediteringen, men som inneholder en kjede som avslører en blokkhash som overskrider antall bekreftelser tillatt før kreditering

- en operatør som har opprettet en lightning-faktura på et innskudds vegne, signerer en hovedbokoppdatering som ikke har kreditert innskuddet til tross for at preimage er avslørt i kjeden

- en samsignatur som erklærer at den nåværende hovedbokhashen er en som går forut for deres egen senere hash i kjeden

- et medlem av kvorumet til en omstridt hovedbok som var aktiv men ikke handlet i samsvar med svindelbevis innen et antall blokker

- signering eller samsignering av ikke-samsvarende hovedbokoppdateringer

et svindelbevis består av beviset og en kausal kjede som forbinder den innebygde hashen til den anklagede operatørens hovedbok. kjeden er en sekvens av samsignerte oppdateringer, der hver inkluderer en member_ledger_hash fra forrige lenkes hovedbok. verifiserere vandrer kjeden uten å søke, bekrefter at hver lenke er en signert oppdatering, og at bevishashen samsvarer med de innebygde dataene

## gjenoppretting

når en hovedbok har blitt utilgjengelig eller ikke-samsvarende, kan kvorummedlemmer opprette sin egen fortsettelse av hovedboken fra den siste samsvarende oppdateringen. de må etablere et nytt kvorum og gi sikkerhetsstillelsesattester. medlemmer må deretter koordinere for å bruke den forrige reserveutgangen til et lotteri av potensielle neste kjeder. vinneren av dette lotteriet legger til en oppkjøpsoppdatering på sin kjede, og de andre legger til en avståelse. lommebøker fortsetter å adressere samme hovedbok, og aksepterer kun svar samsignert av kvorumet. periodisk, og når ingen svar har den forventede samsignaturen, bør lommeboken spørre nettverket og spille av hovedbokoppdateringer for å identifisere endringer i depot

når manglende samsvar virker utilsiktet (f.eks. en hovedbok har blitt utilgjengelig i et visst antall blokker) må endringen i depot være respektfull: kun mengden reserver som kreves for å dekke hovedbokens forpliktelser sendes til lotteriet, og veksel sendes tilbake til operatørens offentlige nøkkel. kontroll over sikkerhetsstillelse påvirkes ikke

når bevis på manglende samsvar eksisterer, deles beløpet utover nødvendige reserver likt mellom medlemmene av kvorumet, og sikkerhetsstillelse holdt på medlemmers hovedbøker tillates beslaglagt

## nettverkshelse

et enkelt angrep er å danne øyer av sammensvorne operatører. etter å ha bygget opp betydelige forpliktelser på tvers av sine hovedbøker, koordinerer de for å forlate nettverket og stjeler midler som overstiger sikkerhetsstillelsen som går tapt. nettverket kan forsvare seg mot dette, bortsett fra i regioner der den interne verdien overstiger sikkerhetsstillelsen som kobler den til det ikke-sammensvorne nettverket. høyere sikkerhetsforhold og større, mer mangfoldige kvorumer reduserer sannsynligheten for at slike lommer dannes, men de kan dannes med vilje, og vi kan ikke forvente at hver lommebok evaluerer hele nettverket. i stedet bør oppdagelsesmarkeder publisere målinger av operatøransvarlighet basert på grafanalyser som prisinnsamlingsalgoritmer

## konklusjon

vi foreslår et sikkerhetsstillelsesnettverk som krever sammensvergelse for å stjele, men sammensvergelse øker sikkerhetsstillelsen i risiko raskere enn den øker verdien som kan stjeles. vi bruker dette nettverket til å sikre kryptografiske hovedbøker med fulle reserver. disse hovedbøkene betjener kontoer på vegne av frakoblede lommebøker i bytte mot forhåndsforhandlede gebyrer. hovedbokprimitiver støtter miniscript-bruksbetingelser tilstrekkelige for grunnleggende smarte kontrakter. nettverket skalerer nær lineært, noe som lar et stort nettverk tilby milliarder av lommebøker og transaksjonsvolum som overstiger tradisjonelle betalingsnettverk
