# bitcoin deposits
## resum

una versió ideal peer-to-peer de diner electrònic permetria enviar pagaments en línia directament d'una part a una altra de manera ràpida i amb una preparació mínima. la xarxa lightning proporciona part de la solució, però els beneficis essencials es perden si es requereix un tercer de confiança per gestionar l'estat en nom teu. proposem una solució a aquest problema utilitzant llibres de comptes verificables i una xarxa de garanties. els operadors difonen actualitzacions del llibre de comptes als seus parells, creant un registre auditable de comptes. les carteres difonen evidència de deshonestedat a aquests parells, que asseguren que el llibre de comptes mantingui un operador honest. la sortida unilateral és substituïda per la garantia que els fons romanen disponibles mentre la xarxa ho estigui. arribem a una xarxa que delega el manteniment de la liquiditat, evita les comissions d'inici, és capaç de rebre pagaments fora de línia i escala independentment de la capa base

## introducció

bitcoin deposits té com a objectiu proporcionar fons ràpids i escalables controlats per clau, sense confiança, fora de cadena. l'activitat a la cadena escala amb el nombre de llibres de comptes i la freqüència de rotació de reserves. el rendiment escala lleugerament per sobre de linealment amb el nombre de llibres de comptes a la xarxa, fent plausibles milions de transaccions per segon a través de bilions de carteres

hi ha compromisos explícits:
- sense sortida unilateral: quan els operadors fallen, els fons es queden a la xarxa
- sense privadesa: la verificació requereix transparència
- disponibilitat intermitent: un dipòsit només és tan disponible com l'operador. les carteres haurien de repartir els fons per augmentar la disponibilitat

esperem que l'experiència de cartera sigui similar a una capa base ràpida, amb una economia de pagaments similar a la xarxa lightning

## llibres de comptes

un llibre de comptes és una cadena immutable d'actualitzacions, que conté el hash de l'actualització anterior i signada per l'operador del llibre. diferents tipus d'actualització tenen regles diferents que regeixen quan i com es poden utilitzar. els llibres de comptes són autodescriptius, les seves actualitzacions públicament disponibles i no repudiables, permetent a qualsevol avaluar-ne la conformitat

els llibres de comptes tenen un únic operador actiu, però són mantinguts cooperativament per la malla. qualsevol operador en pot crear un, però si desapareix o es torna deshonest, un operador diferent serà assignat, juntament amb les reserves. l'operador actualment actiu s'identifica per la clau pública que es va utilitzar per signar l'actualització co-signada més recent

## dipòsits

un dipòsit és un compte estable que pot enviar i rebre fons, controlat per miniscript. a l'obertura s'estableix un calendari de comissions, així com si rebre fons requereix una sol·licitud signada per la cartera. un operador ha de permetre transferències entre dipòsits al mateix llibre de comptes així com sortides a la cadena. haurien de permetre als dipòsits pagar factures lightning

queda a discreció de l'operador crear ofertes de finançament a la cadena o factures lightning en nom d'un dipòsit. si ho fa, aquestes haurien de ser co-signades per un membre del quòrum, i la cartera hauria de verificar aquesta signatura. les ofertes i factures no formen part del llibre de comptes, de manera que és responsabilitat de la cartera verificar les signatures i conservar-les com a evidència

## comissions

les transferències entre dipòsits, a la cadena i a través de lightning tenen comissions pagades a l'operador del llibre de comptes. també hi ha comissions aplicades periòdicament als saldos amb un període especificat. totes es negocien quan s'obre un nou dipòsit. les comissions es poden canviar després d'un nombre especificat de blocs, donat un avís de blocs especificat i dins d'un límit percentual per ajustament negociat a l'obertura. el quòrum pot negar-se a co-signar actualitzacions que creïn circumstàncies no rendibles de les quals en última instància podrien ser responsables

## transferències

la forma bàsica de transferència és una operació en dues fases entre dos dipòsits al mateix llibre de comptes: un dipòsit emet una sol·licitud per enviar fons. si hi ha prou fons disponibles, un bloqueig sobre els fons amb una condició de despesa s'afegeix al llibre de comptes. si la condició de despesa es compleix abans d'un temps límit, els fons passen del remitent al destinatari menys la comissió de l'operador. si s'arriba al temps límit, el bloqueig s'allibera, menys una comissió d'operador més petita. amb condicions de despesa miniscript, això és suficient per permetre a qualsevol dipòsit proporcionar ponts i serveis de liquiditat a altres dipòsits al mateix llibre de comptes

## lightning

els operadors que tinguin un canal lightning poden permetre als dipòsits enviar i rebre a través de la xarxa lightning. quan un dipòsit sol·licita una factura lightning, l'operador en crea una a través del seu node lightning, demana als membres del quòrum que la co-signin per demostrar que estan compromesos a acreditar el dipòsit en rebre el pagament. la cartera hauria de conservar aquesta factura co-signada com a evidència. quan un dipòsit sol·licita el pagament d'una factura lightning, l'operador paga utilitzant el seu node lightning i debita el dipòsit després d'obtenir la preimatge

quan el pagador i el beneficiari són dipòsits del mateix operador, l'operador pot liquidar internament sense encaminar a través de lightning, acreditant i debitant els dipòsits respectius directament. això evita comissions d'encaminament i modes de fallada tot mantenint les mateixes garanties comptables

## missatgers

les sol·licituds de transferència només mouen fons entre dipòsits al mateix llibre de comptes. per moure fons entre llibres de comptes, les carteres utilitzen missatgers — serveis que mantenen dipòsits en múltiples llibres de comptes i transporten transferències entre ells. un missatger anuncia la capacitat i les comissions direccionals per llibre al relay. quan una cartera vol enviar del llibre A al llibre B, crea un bloqueig de transferència al dipòsit del missatger i sol·licita que el missatger en creï un des del seu dipòsit al llibre de destí cap al beneficiari. un cop establerts ambdós bloqueigs, la cartera revela la preimatge al beneficiari, que completa la transferència des del missatger. un cop revelada, el missatger utilitza aquesta mateixa preimatge per completar la transferència del remitent al missatger

aquest és un patró estàndard de contracte amb bloqueig temporal per hash. esperem que el temps límit de sortida del missatger sigui estrictament anterior al d'entrada, assegurant que si la cartera mai no revela, ambdós bloqueigs expirin i cap part perdi fons. no es requereix confiança més enllà de la garantia de temps límit aplicada pels operadors

els missatgers haurien d'establir comissions per llibre: fee_in i fee_out per cada llibre que serveixen. la cartera estima el cost de la ruta com fee_out a l'origen més fee_in al destí. els missatgers poden variar les comissions per llibre segons la liquiditat disponible, reequilibrant naturalment les seves posicions. les carteres descobreixen els missatgers a través dels seus anuncis al relay i seleccionen segons comissió, capacitat o cobertura

## comunicació

tota la comunicació entre carteres i operadors, i entre operadors, utilitza relays nostr. les actualitzacions del llibre es publiquen com a esdeveniments durables que els relays retenen, creant un registre auditable permanent. les sol·licituds i respostes entre carteres i operadors són esdeveniments efímers amb un TTL de relay curt. els operadors anuncien els seus termes com a esdeveniments reemplaçables, permetent a les carteres descobrir i comparar operadors sense un directori centralitzat

aquesta arquitectura significa que les carteres no necessiten connexions persistents — poden desconnectar-se indefinidament i posar-se al dia reproduint esdeveniments des de qualsevol relay que els tingui. els operadors es poden contactar a través de qualsevol relay que monitoritzin, i l'elecció del relay és una decisió de desplegament, no una restricció del protocol

## reserves i garanties

les reserves es mantenen en un utxo amb un import igual o superior a la suma de les obligacions d'un llibre de comptes, gastable per una majoria del quòrum, amb retorn a l'operador després d'un període significatiu

la garantia és el capital propi de l'operador, dipositat i bloquejat als llibres de comptes dels membres del quòrum. cada membre manté un dipòsit de garantia que l'operador finança i bloqueja durant un temps especificat. les obligacions totals d'un llibre es limiten al doble del bloqueig de garantia més petit mantingut per qualsevol membre, i la durada del quòrum es limita al temps de bloqueig més curt. això assegura que la xarxa de garanties sempre tingui prou suport per cobrir una transferència de custòdia. el mateix dipòsit de garantia pot recolzar múltiples llibres per millorar l'eficiència del capital, tot i que les carteres haurien de preferir operadors amb fonts de garantia no superposades

les obligacions s'apliquen en crear noves ofertes de finançament o factures. l'operador no pot crear ofertes o factures que empenyerien les obligacions totals del llibre per sobre de les reserves o per sobre del doble del bloqueig de garantia més petit, el que sigui més baix

## quòrum

els operadors sol·liciten a altres operadors que s'uneixin al seu quòrum dipositant i bloquejant garanties al llibre del membre. la sol·licitud inclou el compromís de garantia (import i durada del bloqueig) i els termes del membre: calendaris mínims de comissions que els dipòsits al llibre han de complir. cada membre ha d'operar el seu propi llibre i pot confiscar la garantia de l'operador si es demostra que l'operador no és conforme. els membres especifiquen límits en els calendaris de comissions durant la seva pertinença al quòrum — l'operador no pot obrir dipòsits amb comissions per sota dels mínims del membre més estricte, protegint els membres d'heretar obligacions no rendibles després d'una transferència de custòdia

un cop establert el quòrum, les reserves es roten cap a un nou utxo multisig. els membres co-signen actualitzacions vàlides i participen en la recuperació si l'operador en signa de no conformes. quòrums més grans augmenten la sobrecàrrega de comunicació però redueixen el risc de l'operador, augmenten la disponibilitat i fan que la col·lusió sigui més difícil i costosa. les carteres haurien de preferir quòrums més grans

## dissuasió econòmica

el protocol substitueix la sortida unilateral per la dissuasió econòmica. els membres del quòrum estan directament incentivats a actuar contra la deshonestedat. durant les operacions normals guanyen comissions modestes sobre la garantia, però en cas de comportament demostrablement no conforme poden confiscar el dipòsit complet de garantia de l'operador al seu llibre

quan una cartera sospita censura, pot escalar la sol·licitud als membres del quòrum mitjançant lliurament certificat. el membre incorpora el hash de la sol·licitud al seu propi llibre per una petita comissió, creant evidència causalment ancorada. si l'operador no processa la sol·licitud, el membre té tant l'evidència com l'incentiu econòmic per iniciar una disputa

el frau amb factures lightning segueix el mateix patró de dissuasió. l'operador sap si s'ha rebut una preimatge, però la cartera no. tanmateix, qualsevol pagador pot proporcionar la preimatge a la cartera. un únic robatori confirmat desencadena una disputa, confiscació de reserves i confiscació de garanties. la recompensa de robar un únic pagament és limitada, però el risc és existencial, fent que el robatori lightning sigui econòmicament irracional malgrat ser formalment indemostrable sense la cooperació d'un tercer

el mode de fallada tant per a la censura com per a la dissuasió lightning és la col·lusió unànime del quòrum. el protocol no pot protegir contra un quòrum que coopera per robar, però la xarxa de garanties assegura que la col·lusió costa més del que guanya. la transparència de la xarxa permet a les carteres i als mercats de descobriment identificar estructures de quòrum sospitoses abans de dipositar fons

## temps

el temps absolut es mesura contra la capa base. les toleràncies no poden excedir un nombre raonable de confirmacions per mantenir l'estabilitat durant reorganitzacions de la cadena

on es requereixen toleràncies més altes ens basem en l'ordenació causal. un llibre de comptes criptogràfic és una cadena de merkle. cada actualització demostra que va ser creada després de totes les actualitzacions anteriors, però no proporciona garanties sobre informació fora de la cadena. per construir una ordenació distribuïda, requerim que les co-signatures incloguin el hash de l'última actualització del llibre del co-signant. aquest hash s'incorpora llavors al hash de l'actualització actual, formant part de la cadena així com de totes les altres cadenes per a les quals l'operador del llibre co-signa, creant una xarxa de causalitat. això no pot demostrar el temps explícitament, però pot demostrar que certes peces d'informació van ser creades en un ordre específic

## proves de frau

podem demostrar diversos tipus de frau exposant informació que ha estat creada en l'ordre incorrecte. quan la informació no és inclosa per les operacions normals de la xarxa, es pot introduir clandestinament creant activitat que inclogui un hash de l'evidència. un cop incorporada a una actualització signada per l'operador, l'evidència es revela com a creada en un lloc no conforme de l'ordenació:

- un operador, havent ofert acreditar un dipòsit amb fons enviats a la cadena a una adreça específica, signa una actualització del llibre que no conté el crèdit adequat, però conté una cadena que revela algun hash de bloc que excedeix el nombre de confirmacions permeses abans del crèdit

- un operador, havent creat una factura lightning en nom d'un dipòsit, signa una actualització del llibre que no ha acreditat el dipòsit malgrat que la preimatge ha estat revelada a la cadena

- una co-signatura que declara que el hash actual del llibre és un que precedeix el seu propi hash posterior a la cadena

- un membre del quòrum d'un llibre en disputa que era actiu però no va actuar d'acord amb la prova de frau dins d'un nombre de blocs

- signar o co-signar actualitzacions del llibre no conformes

una prova de frau consisteix en l'evidència i una cadena causal que connecta el hash incorporat al llibre de l'operador acusat. la cadena és una seqüència d'actualitzacions co-signades, cadascuna incloent un member_ledger_hash del llibre de l'enllaç anterior. els verificadors recorren la cadena sense cercar, confirmant que cada enllaç és una actualització signada i que el hash de la prova coincideix amb les dades incorporades

## recuperació

un cop un llibre de comptes ha esdevingut no disponible o no conforme, els membres del quòrum poden crear la seva pròpia continuació del llibre des de l'última actualització conforme. han d'establir un nou quòrum i proporcionar atestacions de garantia. els membres han de coordinar-se per gastar la sortida de reserves anterior cap a una loteria de les possibles cadenes següents. el guanyador d'aquesta loteria afegeix una actualització d'adquisició a la seva cadena, i els altres afegeixen una cessió. les carteres continuen adreçant-se al mateix llibre, acceptant només respostes co-signades pel quòrum. periòdicament, i quan cap resposta no té la co-signatura esperada, la cartera hauria de consultar la xarxa i reproduir les actualitzacions del llibre per identificar canvis en la custòdia

quan la no conformitat sembla accidental (p. ex., un llibre ha estat no disponible durant un cert nombre de blocs) el canvi de custòdia ha de ser respectuós: només l'import de reserves necessari per cobrir les obligacions del llibre s'envia a la loteria, i el canvi es retorna a la clau pública de l'operador. el control de la garantia no es veu afectat

quan existeix prova de no conformitat, l'import en excés de les reserves necessàries es divideix equitativament entre els membres del quòrum, i la garantia mantinguda als llibres dels membres es permet ser confiscada

## salut de la xarxa

un atac directe és formar illes d'operadors en col·lusió. després de construir obligacions substancials als seus llibres, es coordinen per sortir, robant fons que excedeixen la garantia perduda. la xarxa es pot defensar d'això, excepte en regions on el valor intern excedeix la garantia que la connecta a la xarxa no col·lusòria. ràtios de garantia més alts i quòrums més grans i diversos redueixen la probabilitat que es formin aquestes bosses, però es poden formar intencionadament i no podem esperar que cada cartera avaluï tota la xarxa. en canvi, els mercats de descobriment haurien de publicar mètriques de responsabilitat dels operadors basades en anàlisis de grafs com ara algorismes de recollida de premis

## conclusió

proposem una xarxa de garanties que requereix col·lusió per robar, però la col·lusió augmenta la garantia en risc més ràpidament del que augmenta el valor a ser robat. utilitzem aquesta xarxa per assegurar llibres de comptes criptogràfics recolzats per reserves completes. aquests llibres serveixen comptes en nom de carteres fora de línia a canvi de comissions prenegociades. les primitives del llibre admeten condicions de despesa miniscript suficients per a contractes intel·ligents bàsics. la xarxa escala gairebé linealment, permetent a una xarxa gran proporcionar milers de milions de carteres i un volum de transaccions superior al de les xarxes de pagament tradicionals
