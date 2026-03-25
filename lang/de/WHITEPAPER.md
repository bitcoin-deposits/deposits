# bitcoin deposits
## Zusammenfassung

eine ideale Peer-to-Peer-Version von elektronischem Bargeld wuerde es ermoeglichen, Online-Zahlungen schnell und mit minimalem Aufwand direkt von einer Partei an eine andere zu senden. das lightning-Netzwerk bietet einen Teil der Loesung, aber die wesentlichen Vorteile gehen verloren, wenn ein vertrauenswuerdiger Dritter erforderlich ist, um den Zustand in Ihrem Auftrag zu verwalten. wir schlagen eine Loesung fuer dieses Problem vor, die verifizierbare Hauptbuecher und ein Netz von Sicherheiten verwendet. Betreiber uebermitteln Hauptbuch-Aktualisierungen an ihre Peers und schaffen so eine pruefbare Aufzeichnung von Konten. Wallets uebermitteln Beweise fuer Unehrlichkeit an diese Peers, die sicherstellen, dass das Hauptbuch einen ehrlichen Betreiber aufrechterhaelt. einseitiger Ausstieg wird ersetzt durch die Garantie, dass Mittel verfuegbar bleiben, solange das Netzwerk besteht. wir gelangen zu einem Netzwerk, das die Liquiditaetspflege delegiert, Einrichtungsgebuehren vermeidet, in der Lage ist, Zahlungen offline zu empfangen, und unabhaengig von der Basisschicht skaliert

## Einfuehrung

bitcoin deposits zielt darauf ab, schnelle und skalierbare schluesselkontrollierte Mittel bereitzustellen, vertrauenslos, off-chain. On-Chain-Aktivitaet skaliert mit der Anzahl der Hauptbuecher und der Haeufigkeit der Reservenrotation. der Durchsatz skaliert leicht ueberlinear mit der Anzahl der Hauptbuecher im Netzwerk, wodurch Millionen von Transaktionen pro Sekunde ueber Billionen von Wallets plausibel werden

es gibt explizite Kompromisse:
- kein einseitiger Ausstieg: wenn Betreiber ausfallen, bleiben die Mittel im Netzwerk
- keine Privatsphaere: Verifizierung erfordert Transparenz
- intermittierende Verfuegbarkeit: eine Einlage ist nur so verfuegbar wie der Betreiber. Wallets sollten Mittel verteilen, um die Verfuegbarkeit zu erhoehen

wir erwarten, dass die Wallet-Erfahrung aehnlich wie eine schnelle Basisschicht sein wird, mit Zahlungsoekonomie aehnlich dem lightning-Netzwerk

## Hauptbuecher

ein Hauptbuch ist eine unveraenderliche Kette von Aktualisierungen, die den hash der vorherigen Aktualisierung enthaelt und vom Betreiber des Hauptbuchs signiert ist. verschiedene Arten von Aktualisierungen haben unterschiedliche Regeln, die bestimmen, wann und wie sie verwendet werden koennen. Hauptbuecher sind selbstbeschreibend, ihre Aktualisierungen oeffentlich verfuegbar und nicht abstreitbar, sodass jeder die Konformitaet bewerten kann

Hauptbuecher haben einen einzigen aktiven Betreiber, werden aber kooperativ vom Netzwerk gepflegt. jeder Betreiber kann eines erstellen, aber sollte er verschwinden oder unehrlich werden, wird ein anderer Betreiber zugewiesen, zusammen mit Reserven. der derzeit aktive Betreiber wird durch den oeffentlichen Schluessel identifiziert, der zur Signierung der juengsten mitunterzeichneten Aktualisierung verwendet wurde

## Einlagen

eine Einlage ist ein stabiles Konto, das Mittel senden und empfangen kann, gesteuert durch miniscript. bei der Eroeffnung wird ein Gebuehrenplan festgelegt, ebenso wie die Frage, ob der Empfang von Mitteln eine vom Wallet signierte Anfrage erfordert. ein Betreiber muss Ueberweisungen zwischen Einlagen auf demselben Hauptbuch sowie On-Chain-Ausstiege ermoeglichen. er sollte es Einlagen ermoeglichen, lightning-Rechnungen zu bezahlen

es liegt im Ermessen des Betreibers, On-Chain-Finanzierungsangebote oder lightning-Rechnungen im Auftrag einer Einlage zu erstellen. wenn er dies tut, sollten diese von einem Quorum-Mitglied mitunterzeichnet werden, und das Wallet sollte diese Signatur verifizieren. Angebote und Rechnungen sind nicht Teil des Hauptbuchs, daher liegt es in der Verantwortung des Wallets, Signaturen zu verifizieren und sie als Beweis aufzubewahren

## Gebuehren

Ueberweisungen zwischen Einlagen, On-Chain und ueber lightning haben Gebuehren, die an den Betreiber des Hauptbuchs gezahlt werden. es gibt auch Gebuehren, die periodisch auf Guthaben mit einem bestimmten Zeitraum angewendet werden. alle werden ausgehandelt, wenn eine neue Einlage eroeffnet wird. Gebuehren koennen nach einer bestimmten Anzahl von Bloecken geaendert werden, mit einer bestimmten Blockvorankuendigung und innerhalb eines bei der Eroeffnung ausgehandelten prozentualen Limits pro Anpassung. das Quorum kann sich weigern, Aktualisierungen mitzuunterzeichnen, die unrentable Umstaende schaffen, fuer die sie letztlich verantwortlich sein koennten

## Ueberweisungen

die grundlegende Form der Ueberweisung ist eine zweiphasige Operation zwischen zwei Einlagen auf demselben Hauptbuch: eine Einlage stellt eine Anfrage zum Senden von Mitteln. wenn genuegend Mittel verfuegbar sind, wird eine Sperre der Mittel mit einer Ausgabebedingung an das Hauptbuch angehaengt. wenn die Ausgabebedingung vor einem Timeout erfuellt wird, bewegen sich die Mittel vom Sender zum Empfaenger abzueglich der Betreibergebuehr. wenn das Timeout erreicht wird, wird die Sperre aufgehoben, abzueglich einer kleineren Betreibergebuehr. mit miniscript-Ausgabebedingungen reicht dies aus, um jeder Einlage die Bereitstellung von Bruecken- und Liquiditaetsdiensten fuer andere Einlagen auf demselben Hauptbuch zu ermoeglichen

## lightning

Betreiber, die einen lightning-Kanal haben, koennen es Einlagen ermoeglichen, ueber das lightning-Netzwerk zu senden und zu empfangen. wenn eine Einlage eine lightning-Rechnung anfordert, erstellt der Betreiber eine ueber seinen lightning-Knoten, bittet Quorum-Mitglieder, sie mitzuunterzeichnen, um zu beweisen, dass sie sich verpflichtet haben, die Einlage bei Zahlung gutzuschreiben. das Wallet sollte diese mitunterzeichnete Rechnung als Beweis aufbewahren. wenn eine Einlage die Zahlung einer lightning-Rechnung anfordert, bezahlt der Betreiber ueber seinen lightning-Knoten und belastet die Einlage nach Erhalt des preimage

wenn Zahler und Zahlungsempfaenger Einlagen beim selben Betreiber sind, kann der Betreiber intern abrechnen, ohne ueber lightning zu routen, und die jeweiligen Einlagen direkt gutschreiben und belasten. dies vermeidet Routing-Gebuehren und Fehlermodi bei Beibehaltung derselben Buchhaltungsgarantien

## Kuriere

Ueberweisungsanfragen bewegen Mittel nur zwischen Einlagen auf demselben Hauptbuch. um Mittel ueber Hauptbuecher hinweg zu bewegen, verwenden Wallets Kuriere — Dienste, die Einlagen auf mehreren Hauptbuechern halten und Ueberweisungen zwischen ihnen transportieren. ein Kurier bewirbt Kapazitaet und richtungsabhaengige Gebuehren pro Hauptbuch auf dem Relay. wenn ein Wallet von Hauptbuch A zu Hauptbuch B senden moechte, erstellt es eine Ueberweisungssperre zur Einlage des Kuriers und fordert den Kurier auf, eine von seiner Einlage auf dem Ziel-Hauptbuch zum Zahlungsempfaenger zu erstellen. sobald beide Sperren eingerichtet sind, enthuellt das Wallet dem Zahlungsempfaenger das preimage, der die Ueberweisung vom Kurier abschliesst. nach der Enthuellung verwendet der Kurier dasselbe preimage, um die Ueberweisung vom Sender zum Kurier abzuschliessen

dies ist ein Standard-hash-zeitgesperrtes Vertragsmuster. wir erwarten, dass das ausgehende Timeout des Kuriers strikt frueher als das eingehende liegt, sodass bei Nichtenthuellen durch das Wallet beide Sperren ablaufen und keine Partei Mittel verliert. kein Vertrauen ist erforderlich ueber die von Betreibern durchgesetzte Timeout-Garantie hinaus

Kuriere sollten Gebuehren pro Hauptbuch festlegen: fee_in und fee_out fuer jedes Hauptbuch, das sie bedienen. das Wallet schaetzt die Routenkosten als fee_out auf der Quelle plus fee_in am Ziel. Kuriere koennen Gebuehren nach Hauptbuch basierend auf verfuegbarer Liquiditaet variieren und so ihre Positionen natuerlich ausgleichen. Wallets entdecken Kuriere durch deren Anzeigen auf dem Relay und waehlen basierend auf Gebuehr, Kapazitaet oder Abdeckung

## Kommunikation

alle Kommunikation zwischen Wallets und Betreibern sowie zwischen Betreibern nutzt nostr-Relays. Hauptbuch-Aktualisierungen werden als dauerhafte Ereignisse veroeffentlicht, die Relays aufbewahren, und schaffen so eine permanente pruefbare Aufzeichnung. Anfragen und Antworten zwischen Wallets und Betreibern sind ephemere Ereignisse mit einer kurzen Relay-TTL. Betreiber bewerben ihre Konditionen als ersetzbare Ereignisse, sodass Wallets Betreiber ohne ein zentralisiertes Verzeichnis entdecken und vergleichen koennen

diese Architektur bedeutet, dass Wallets keine persistenten Verbindungen benoetigen — sie koennen unbegrenzt offline gehen und durch Abspielen von Ereignissen von jedem Relay, das sie hat, aufholen. Betreiber koennen ueber jedes Relay erreicht werden, das sie ueberwachen, und die Wahl des Relays ist eine Bereitstellungsentscheidung, keine Protokollbeschraenkung

## Reserven und Sicherheiten

Reserven werden in einem utxo mit einem Betrag gehalten, der groesser oder gleich der Summe der Verpflichtungen eines Hauptbuchs ist, ausgabefaehig durch eine Mehrheit des Quorums, mit Rueckfall an den Betreiber nach einer erheblichen Zeitspanne

Sicherheiten sind das eigene Kapital des Betreibers, eingezahlt und gesperrt auf den Hauptbuechern der Quorum-Mitglieder. jedes Mitglied haelt eine Sicherheitseinlage, die der Betreiber finanziert und fuer eine bestimmte Dauer sperrt. die Gesamtverpflichtungen eines Hauptbuchs sind auf das Doppelte der kleinsten Sicherheitssperre begrenzt, die von einem Mitglied gehalten wird, und die Dauer des Quorums ist auf die kuerzeste Sperrzeit begrenzt. dies stellt sicher, dass das Sicherheitennetz immer genug Deckung hat, um eine Verwahrungsuebertragung abzudecken. dieselbe Sicherheitseinlage kann mehrere Hauptbuecher absichern, um die Kapitaleffizienz zu verbessern, obwohl Wallets Betreiber mit nicht-ueberlappenden Sicherheitenquellen bevorzugen sollten

Verpflichtungen werden bei der Erstellung neuer Finanzierungsangebote oder Rechnungen durchgesetzt. der Betreiber kann keine Angebote oder Rechnungen erstellen, die die Gesamtverpflichtungen des Hauptbuchs ueber die Reserven oder ueber das Doppelte der kleinsten Sicherheitssperre hinaus treiben wuerden, je nachdem, welcher Wert niedriger ist

## Quorum

Betreiber bitten andere Betreiber, ihrem Quorum beizutreten, indem sie Sicherheiten auf dem Hauptbuch des Mitglieds einzahlen und sperren. die Anfrage umfasst die Sicherheitsverpflichtung (Betrag und Sperrdauer) und die Bedingungen des Mitglieds: Mindestgebuehrenplaene, die Einlagen auf dem Hauptbuch erfuellen muessen. jedes Mitglied muss sein eigenes Hauptbuch betreiben und kann die Sicherheiten des Betreibers beschlagnahmen, wenn nachweislich nicht-konformes Verhalten vorliegt. Mitglieder legen Grenzen fuer Gebuehrenplaene waehrend ihrer Quorum-Mitgliedschaft fest — der Betreiber kann keine Einlagen mit Gebuehren unterhalb der strengsten Mindestanforderungen eines Mitglieds eroeffnen, was die Mitglieder davor schuetzt, nach einer Verwahrungsuebertragung unrentable Verpflichtungen zu erben

sobald das Quorum etabliert ist, werden die Reserven in ein neues multisig-utxo rotiert. Mitglieder unterzeichnen gueltige Aktualisierungen mit und beteiligen sich an der Wiederherstellung, wenn der Betreiber nicht-konforme signiert. groessere Quoren erhoehen den Kommunikationsaufwand, reduzieren aber das Betreiberrisiko, erhoehen die Verfuegbarkeit und machen Absprachen schwieriger und teurer. Wallets sollten groessere Quoren bevorzugen

## Oekonomische Abschreckung

das Protokoll ersetzt den einseitigen Ausstieg durch oekonomische Abschreckung. Quorum-Mitglieder sind direkt motiviert, gegen Unehrlichkeit vorzugehen. im Normalbetrieb verdienen sie bescheidene Gebuehren auf Sicherheiten, aber im Falle nachweislich nicht-konformen Verhaltens koennen sie die gesamte Sicherheitseinlage des Betreibers auf ihrem Hauptbuch beschlagnahmen

wenn ein Wallet Zensur vermutet, kann es die Anfrage ueber zertifizierte Zustellung an Quorum-Mitglieder eskalieren. das Mitglied bettet den Anfrage-hash in sein eigenes Hauptbuch fuer eine geringe Gebuehr ein und schafft so kausal verankerte Beweise. wenn der Betreiber die Anfrage nicht verarbeitet, hat das Mitglied sowohl die Beweise als auch den oekonomischen Anreiz, einen Streitfall einzuleiten

lightning-Rechnungsbetrug folgt demselben Abschreckungsmuster. der Betreiber weiss, ob ein preimage empfangen wurde, aber das Wallet nicht. allerdings koennte jeder Zahler dem Wallet das preimage liefern. ein einziger bestaetigter Diebstahl loest einen Streitfall aus, die Beschlagnahme von Reserven und die Konfiszierung von Sicherheiten. die Belohnung fuer den Diebstahl einer einzelnen Zahlung ist begrenzt, aber das Risiko ist existenziell, was lightning-Diebstahl oekonomisch irrational macht, obwohl er ohne Kooperation Dritter formal nicht beweisbar ist

der Ausfallmodus sowohl fuer Zensur- als auch fuer lightning-Abschreckung ist einstimmige Quorum-Absprache. das Protokoll kann nicht vor einem Quorum schuetzen, das kooperiert, um zu stehlen, aber das Sicherheitennetz stellt sicher, dass Absprachen mehr kosten als sie einbringen. die Transparenz des Netzwerks ermoeglicht es Wallets und Entdeckungsmaerkten, verdaechtige Quorum-Strukturen vor der Einzahlung von Mitteln zu identifizieren

## Zeit

absolute Zeit wird an der Basisschicht gemessen. Toleranzen duerfen eine angemessene Anzahl von Bestaetigungen nicht ueberschreiten, um die Stabilitaet waehrend Kettenreorganisationen aufrechtzuerhalten

wo hoehere Toleranzen erforderlich sind, verlassen wir uns auf kausale Ordnung. ein kryptographisches Hauptbuch ist eine merkle-Kette. jede Aktualisierung beweist, dass sie nach allen vorherigen Aktualisierungen erstellt wurde, bietet aber keine Garantien ueber Informationen ausserhalb der Kette. um eine verteilte Ordnung zu konstruieren, verlangen wir, dass Mitunterzeichnungen den neuesten Aktualisierungs-hash vom Hauptbuch des Mitunterzeichners enthalten. dieser hash wird dann in den hash der aktuellen Aktualisierung integriert und wird Teil der Kette sowie Teil aller anderen Ketten, die der Hauptbuchbetreiber mitunterzeichnet, wodurch ein Netz der Kausalitaet entsteht. dies kann Zeit nicht explizit beweisen, kann aber beweisen, dass bestimmte Informationen in einer bestimmten Reihenfolge erstellt wurden

## Betrugsnachweise

wir koennen verschiedene Arten von Betrug beweisen, indem wir Informationen offenlegen, die in der falschen Reihenfolge erstellt wurden. wo Informationen nicht durch normale Netzwerkoperationen enthalten sind, koennen sie eingeschmuggelt werden, indem Aktivitaet erzeugt wird, die einen hash der Beweise enthaelt. sobald sie in eine vom Betreiber signierte Aktualisierung aufgenommen wurden, wird offenbart, dass die Beweise an einer nicht-konformen Stelle in der Ordnung erstellt wurden:

- ein Betreiber, der angeboten hat, eine Einlage mit On-Chain an eine bestimmte Adresse gesendeten Mitteln gutzuschreiben, signiert eine Hauptbuch-Aktualisierung, die die entsprechende Gutschrift nicht enthaelt, aber eine Kette enthaelt, die einen Block-hash offenbart, der die Anzahl der vor der Gutschrift zulaessigen Bestaetigungen ueberschreitet

- ein Betreiber, der eine lightning-Rechnung im Auftrag einer Einlage erstellt hat, signiert eine Hauptbuch-Aktualisierung, die die Einlage nicht gutgeschrieben hat, obwohl das preimage in der Kette offenbart wurde

- eine Mitunterzeichnung, die den aktuellen Hauptbuch-hash als einen deklariert, der ihrem eigenen spaeteren hash in der Kette vorausgeht

- ein Mitglied des Quorums eines umstrittenen Hauptbuchs, das aktiv war, aber nicht innerhalb einer bestimmten Anzahl von Bloecken gemaess dem Betrugsnachweis gehandelt hat

- das Signieren oder Mitunterzeichnen nicht-konformer Hauptbuch-Aktualisierungen

ein Betrugsnachweis besteht aus den Beweisen und einer kausalen Kette, die den eingebetteten hash mit dem Hauptbuch des beschuldigten Betreibers verbindet. die Kette ist eine Abfolge mitunterzeichneter Aktualisierungen, von denen jede einen member_ledger_hash vom Hauptbuch des vorherigen Glieds enthaelt. Verifizierer durchlaufen die Kette ohne zu suchen, bestaetigen, dass jedes Glied eine signierte Aktualisierung ist, und dass der Nachweis-hash mit den eingebetteten Daten uebereinstimmt

## Wiederherstellung

sobald ein Hauptbuch nicht mehr verfuegbar oder nicht-konform geworden ist, koennen Quorum-Mitglieder ihre eigene Fortfuehrung des Hauptbuchs ab der letzten konformen Aktualisierung erstellen. sie muessen ein neues Quorum gruenden und Sicherheitenbescheinigungen vorlegen. die Mitglieder muessen dann koordinieren, um den vorherigen Reserven-Output in eine Lotterie der potenziellen naechsten Ketten auszugeben. der Gewinner dieser Lotterie haengt eine Uebernahme-Aktualisierung an seine Kette an, und die anderen haengen eine Abtretung an. Wallets adressieren weiterhin dasselbe Hauptbuch und akzeptieren nur Antworten, die vom Quorum mitunterzeichnet sind. periodisch und wenn keine Antworten die erwartete Mitunterzeichnung haben, sollte das Wallet das Netzwerk abfragen und Hauptbuch-Aktualisierungen abspielen, um Aenderungen in der Verwahrung zu identifizieren

wenn Nicht-Konformitaet versehentlich erscheint (z.B. ein Hauptbuch ist fuer eine bestimmte Anzahl von Bloecken nicht verfuegbar geworden), muss der Verwahrungswechsel respektvoll sein: nur der Betrag an Reserven, der zur Deckung der Verpflichtungen des Hauptbuchs erforderlich ist, wird in die Lotterie gesendet, und Wechselgeld wird an den oeffentlichen Schluessel des Betreibers zurueckgesendet. die Kontrolle ueber Sicherheiten wird nicht beeinflusst

wenn Beweise fuer Nicht-Konformitaet vorliegen, wird der ueber die notwendigen Reserven hinausgehende Betrag gleichmaessig unter den Mitgliedern des Quorums aufgeteilt, und die auf Mitglieder-Hauptbuechern gehaltenen Sicherheiten duerfen beschlagnahmt werden

## Netzwerkgesundheit

ein einfacher Angriff besteht darin, Inseln kooperierender Betreiber zu bilden. nachdem sie erhebliche Verpflichtungen ueber ihre Hauptbuecher aufgebaut haben, koordinieren sie den Ausstieg und stehlen Mittel, die die verlorenen Sicherheiten uebersteigen. das Netzwerk kann sich dagegen verteidigen, ausser in Regionen, in denen der interne Wert die Sicherheiten uebersteigt, die es mit dem nicht-abgesprochenen Netzwerk verbinden. hoehere Sicherheitenquoten und groessere, vielfaeltigere Quoren verringern die Wahrscheinlichkeit, dass sich diese Taschen bilden, aber sie koennen absichtlich gebildet werden und wir koennen nicht erwarten, dass jedes Wallet das gesamte Netzwerk bewertet. stattdessen sollten Entdeckungsmaerkte Metriken der Betreiberverantwortlichkeit basierend auf Graphanalysen wie Prize-Collecting-Algorithmen veroeffentlichen

## Schlussfolgerung

wir schlagen ein Sicherheitennetzwerk vor, das Absprachen zum Stehlen erfordert, aber Absprachen erhoehen die gefaehrdeten Sicherheiten schneller als den zu stehlenden Wert. wir verwenden dieses Netzwerk, um kryptographische Hauptbuecher abzusichern, die durch vollstaendige Reserven gedeckt sind. diese Hauptbuecher bedienen Konten im Auftrag von Offline-Wallets im Austausch fuer vorverhandelte Gebuehren. Hauptbuch-Primitive unterstuetzen miniscript-Ausgabebedingungen, die fuer grundlegende Smart Contracts ausreichen. das Netzwerk skaliert nahezu linear, sodass ein grosses Netzwerk Milliarden von Wallets und Transaktionsvolumen bereitstellen kann, das ueber das traditioneller Zahlungsnetzwerke hinausgeht
