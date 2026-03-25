# bitcoin deposits
## resumen

una versión ideal de efectivo electrónico entre pares permitiría que los pagos en línea se envíen directamente de una parte a otra de forma rápida y con una preparación mínima. la red lightning proporciona parte de la solución, pero los beneficios esenciales se pierden si se requiere un tercero de confianza para administrar el estado en tu nombre. proponemos una solución a este problema utilizando libros contables verificables y una red de colateral. los operadores transmiten actualizaciones del libro contable a sus pares, creando un registro auditable de cuentas. las billeteras transmiten evidencia de deshonestidad a esos pares, quienes aseguran que el libro contable mantenga un operador honesto. la salida unilateral se reemplaza por la garantía de que los fondos permanecen disponibles mientras la red lo esté. llegamos a una red que delega el mantenimiento de liquidez, evita tarifas de configuración, es capaz de recibir pagos sin conexión y escala de forma independiente de la capa base

## introducción

bitcoin deposits busca proporcionar fondos rápidos y escalables controlados por claves, sin confianza, fuera de cadena. la actividad en cadena escala con la cantidad de libros contables y la frecuencia de rotación de reservas. el rendimiento escala ligeramente por encima de forma lineal con la cantidad de libros contables en la red, haciendo plausibles millones de transacciones por segundo a través de billones de billeteras

hay compensaciones explícitas:
- sin salida unilateral: cuando los operadores fallan, los fondos permanecen en la red
- sin privacidad: la verificación requiere transparencia
- disponibilidad intermitente: un depósito es tan disponible como el operador. las billeteras deben distribuir los fondos para aumentar la disponibilidad

esperamos que la experiencia de billetera sea similar a una capa base rápida, con una economía de pagos similar a la red lightning

## libros contables

un libro contable es una cadena inmutable de actualizaciones, que contiene el hash de la actualización anterior y está firmada por el operador del libro contable. diferentes tipos de actualizaciones tienen diferentes reglas que rigen cuándo y cómo pueden usarse. los libros contables son autodescriptivos, sus actualizaciones están disponibles públicamente y son irrepudiables, permitiendo que cualquiera evalúe la conformidad

los libros contables tienen un único operador activo, pero son mantenidos cooperativamente por la malla. cualquier operador puede crear uno, pero si desaparece o se vuelve deshonesto, se asignará un operador diferente junto con las reservas. el operador actualmente activo se identifica por la clave pública que se usó para firmar la actualización co-firmada más reciente

## depósitos

un depósito es una cuenta estable que puede enviar y recibir fondos, controlada por miniscript. al abrir se establece un esquema de tarifas, así como si recibir fondos requiere una solicitud firmada por la billetera. un operador debe permitir transferencias entre depósitos en el mismo libro contable, así como salidas en cadena. deben permitir que los depósitos paguen facturas lightning

queda a discreción del operador crear ofertas de financiamiento en cadena o facturas lightning en nombre de un depósito. si lo hacen, estas deben ser co-firmadas por un miembro del quórum, y la billetera debe verificar esta firma. las ofertas y facturas no son parte del libro contable, por lo que es responsabilidad de la billetera verificar las firmas y conservarlas como evidencia

## tarifas

las transferencias entre depósitos, en cadena y a través de lightning tienen tarifas pagadas al operador del libro contable. también hay tarifas aplicadas periódicamente a los saldos con un período especificado. todas se negocian cuando se abre un nuevo depósito. las tarifas pueden cambiarse después de un número especificado de bloques, dado un aviso de bloques especificado y dentro de un límite porcentual por ajuste negociado al momento de apertura. el quórum puede negarse a co-firmar actualizaciones que creen circunstancias no rentables de las cuales podrían ser responsables en última instancia

## transferencias

la forma básica de transferencia es una operación de dos fases entre dos depósitos en el mismo libro contable: un depósito emite una solicitud para enviar fondos. si hay fondos suficientes disponibles, se agrega al libro contable un bloqueo sobre los fondos con una condición de gasto. si la condición de gasto se cumple antes de un tiempo límite, los fondos se mueven del remitente al destinatario menos la tarifa del operador. si se alcanza el tiempo límite, el bloqueo se libera, menos una tarifa menor del operador. con condiciones de gasto miniscript, esto es suficiente para permitir que cualquier depósito proporcione puentes y servicios de liquidez a otros depósitos en el mismo libro contable

## lightning

los operadores que tienen un canal lightning pueden permitir que los depósitos envíen y reciban a través de la red lightning. cuando un depósito solicita una factura lightning, el operador crea una a través de su nodo lightning, pide a los miembros del quórum que la co-firmen para demostrar que están comprometidos a acreditar el depósito tras el pago. la billetera debe conservar esta factura co-firmada como evidencia. cuando un depósito solicita el pago de una factura lightning, el operador paga usando su nodo lightning y debita el depósito después de obtener el preimage

cuando el pagador y el beneficiario son depósitos del mismo operador, el operador puede liquidar internamente sin enrutar a través de lightning, acreditando y debitando los depósitos respectivos directamente. esto evita tarifas de enrutamiento y modos de falla mientras mantiene las mismas garantías contables

## mensajeros

las solicitudes de transferencia solo mueven fondos entre depósitos en el mismo libro contable. para mover fondos entre libros contables, las billeteras usan mensajeros — servicios que mantienen depósitos en múltiples libros contables y transportan transferencias entre ellos. un mensajero anuncia capacidad y tarifas direccionales por libro contable en el relay. cuando una billetera quiere enviar del libro contable A al libro contable B, crea un bloqueo de transferencia al depósito del mensajero y solicita que el mensajero cree uno desde su depósito en el libro contable destino hacia el beneficiario. una vez que ambos bloqueos están establecidos, la billetera revela el preimage al beneficiario, quien completa la transferencia desde el mensajero. una vez revelado, el mensajero usa este mismo preimage para completar la transferencia del remitente al mensajero

este es un patrón estándar de contrato con bloqueo temporal por hash. esperamos que el tiempo límite de salida del mensajero sea estrictamente anterior al de entrada, asegurando que si la billetera nunca revela, ambos bloqueos expiren y ninguna parte pierda fondos. no se requiere confianza más allá de la garantía de tiempo límite aplicada por los operadores

los mensajeros deben establecer tarifas por libro contable: fee_in y fee_out para cada libro contable que atienden. la billetera estima el costo de la ruta como fee_out en el origen más fee_in en el destino. los mensajeros pueden variar las tarifas por libro contable según la liquidez disponible, rebalanceando naturalmente sus posiciones. las billeteras descubren mensajeros a través de sus anuncios en el relay y seleccionan según tarifa, capacidad o cobertura

## comunicación

toda la comunicación entre billeteras y operadores, y entre operadores, utiliza relays nostr. las actualizaciones del libro contable se publican como eventos durables que los relays retienen, creando un registro auditable permanente. las solicitudes y respuestas entre billeteras y operadores son eventos efímeros con un TTL corto en el relay. los operadores anuncian sus términos como eventos reemplazables, permitiendo que las billeteras descubran y comparen operadores sin un directorio centralizado

esta arquitectura significa que las billeteras no necesitan conexiones persistentes — pueden desconectarse indefinidamente y ponerse al día reproduciendo eventos desde cualquier relay que los tenga. los operadores pueden ser contactados a través de cualquier relay que monitoreen, y la elección del relay es una decisión de despliegue, no una restricción del protocolo

## reservas y colateral

las reservas se mantienen en un utxo con un monto mayor o igual a la suma de las obligaciones de un libro contable, gastable por una mayoría del quórum, con respaldo al operador después de un período significativo

el colateral es el capital propio del operador, depositado y bloqueado en los libros contables de los miembros del quórum. cada miembro mantiene un depósito de colateral que el operador financia y bloquea por una duración especificada. las obligaciones totales de un libro contable están limitadas al doble del bloqueo de colateral más pequeño mantenido por cualquier miembro, y la duración del quórum está limitada al tiempo de bloqueo más corto. esto asegura que la red de colateral siempre tenga suficiente respaldo para cubrir una transferencia de custodia. el mismo depósito de colateral puede respaldar múltiples libros contables para mejorar la eficiencia de capital, aunque las billeteras deben preferir operadores con fuentes de colateral no superpuestas

las obligaciones se aplican al crear nuevas ofertas de financiamiento o facturas. el operador no puede crear ofertas o facturas que empujen las obligaciones totales del libro contable por encima de las reservas o por encima del doble del bloqueo de colateral más pequeño, lo que sea menor

## quórum

los operadores solicitan a otros operadores unirse a su quórum depositando y bloqueando colateral en el libro contable del miembro. la solicitud incluye el compromiso de colateral (monto y duración del bloqueo) y los términos del miembro: esquemas de tarifas mínimas que los depósitos en el libro contable deben cumplir. cada miembro debe operar su propio libro contable y puede confiscar el colateral del operador si se demuestra que el operador no cumple con las normas. los miembros especifican límites en los esquemas de tarifas durante su membresía en el quórum — el operador no puede abrir depósitos con tarifas por debajo de los mínimos del miembro más estricto, protegiendo a los miembros de heredar obligaciones no rentables después de una transferencia de custodia

una vez establecido el quórum, las reservas se rotan a un nuevo utxo multisig. los miembros co-firman actualizaciones válidas y participan en la recuperación si el operador firma actualizaciones no conformes. quórums más grandes aumentan la sobrecarga de comunicación pero reducen el riesgo del operador, aumentan la disponibilidad y hacen que la colusión sea más difícil y costosa. las billeteras deben preferir quórums más grandes

## disuasión económica

el protocolo reemplaza la salida unilateral con disuasión económica. los miembros del quórum están directamente incentivados a actuar contra la deshonestidad. durante operaciones normales ganan tarifas modestas sobre el colateral, pero en caso de comportamiento demostrablemente no conforme, pueden confiscar el depósito completo de colateral del operador en su libro contable

cuando una billetera sospecha censura, puede escalar la solicitud a los miembros del quórum mediante entrega certificada. el miembro incorpora el hash de la solicitud en su propio libro contable por una tarifa pequeña, creando evidencia causalmente anclada. si el operador no procesa la solicitud, el miembro tiene tanto la evidencia como el incentivo económico para iniciar una disputa

el fraude de facturas lightning sigue el mismo patrón de disuasión. el operador sabe si se recibió un preimage, pero la billetera no. sin embargo, cualquier pagador podría proporcionar el preimage a la billetera. un solo robo confirmado desencadena disputa, incautación de reservas y confiscación de colateral. la recompensa de robar un solo pago está acotada, pero el riesgo es existencial, haciendo que el robo por lightning sea económicamente irracional a pesar de ser formalmente indemostrable sin cooperación de terceros

el modo de falla tanto para la censura como para la disuasión lightning es la colusión unánime del quórum. el protocolo no puede proteger contra un quórum que coopera para robar, pero la red de colateral asegura que la colusión cueste más de lo que genera. la transparencia de la red permite que las billeteras y los mercados de descubrimiento identifiquen estructuras de quórum sospechosas antes de depositar fondos

## tiempo

el tiempo absoluto se mide contra la capa base. las tolerancias no pueden exceder un número razonable de confirmaciones para mantener la estabilidad durante reorganizaciones de cadena

donde se requieren tolerancias más altas, nos basamos en el ordenamiento causal. un libro contable criptográfico es una cadena merkle. cada actualización demuestra que fue creada después de todas las actualizaciones anteriores, pero no proporciona garantías sobre información fuera de la cadena. para construir un ordenamiento distribuido, requerimos que las co-firmas incluyan el hash de la última actualización del libro contable del co-firmante. ese hash se incorpora entonces al hash de la actualización actual, convirtiéndose en parte de la cadena así como de todas las demás cadenas para las que el operador del libro contable co-firma, creando una red de causalidad. esto no puede demostrar el tiempo explícitamente, pero puede demostrar que ciertas piezas de información fueron creadas en un orden específico

## pruebas de fraude

podemos demostrar varios tipos de fraude exponiendo información que ha sido creada en el orden incorrecto. donde la información no es incluida por las operaciones normales de la red, puede ser introducida creando actividad que incluya un hash de la evidencia. una vez incorporada en una actualización firmada por el operador, la evidencia se revela como habiendo sido creada en un lugar no conforme en el ordenamiento:

- un operador, habiendo ofrecido acreditar un depósito con fondos enviados en cadena a una dirección específica, firma una actualización del libro contable que no contiene el crédito apropiado, pero sí contiene una cadena que revela algún hash de bloque que excede el número de confirmaciones permitidas antes del crédito

- un operador, habiendo creado una factura lightning en nombre de un depósito, firma una actualización del libro contable que no ha acreditado el depósito a pesar de que el preimage fue revelado en la cadena

- una co-firma que declara que el hash actual del libro contable es uno que precede su propio hash posterior en la cadena

- un miembro del quórum de un libro contable en disputa que estaba activo pero no actuó de acuerdo con la prueba de fraude dentro de un número de bloques

- firmar o co-firmar actualizaciones del libro contable no conformes

una prueba de fraude consiste en la evidencia y una cadena causal que conecta el hash incorporado al libro contable del operador acusado. la cadena es una secuencia de actualizaciones co-firmadas, cada una incluyendo un member_ledger_hash del libro contable del enlace anterior. los verificadores recorren la cadena sin buscar, confirmando que cada enlace es una actualización firmada y que el hash de la prueba coincide con los datos incorporados

## recuperación

una vez que un libro contable se ha vuelto no disponible o no conforme, los miembros del quórum pueden crear su propia continuación del libro contable desde la última actualización conforme. deben establecer un nuevo quórum y proporcionar atestaciones de colateral. los miembros deben entonces coordinarse para gastar la salida de reservas anterior en una lotería de las posibles cadenas siguientes. el ganador de esta lotería agrega una actualización de adquisición a su cadena, y los demás agregan una de cesión. las billeteras continúan dirigiéndose al mismo libro contable, aceptando solo respuestas co-firmadas por el quórum. periódicamente, y cuando ninguna respuesta tiene la co-firma esperada, la billetera debe consultar la red y reproducir las actualizaciones del libro contable para identificar cambios en la custodia

cuando la no conformidad parece accidental (ej., un libro contable no ha estado disponible por cierto número de bloques) el cambio de custodia debe ser respetuoso: solo el monto de reservas requerido para cubrir las obligaciones del libro contable se envía a la lotería, y el cambio se devuelve a la clave pública del operador. el control del colateral no se ve afectado

cuando existe prueba de no conformidad, el monto en exceso de las reservas necesarias se divide equitativamente entre los miembros del quórum, y se permite confiscar el colateral mantenido en los libros contables de los miembros

## salud de la red

un ataque directo es formar islas de operadores en colusión. después de acumular obligaciones sustanciales en sus libros contables, se coordinan para salir, robando fondos que exceden el colateral perdido. la red puede defenderse contra esto, excepto en regiones donde el valor interno excede el colateral que la conecta a la red no coludida. ratios de colateral más altos y quórums más grandes y diversos reducen la probabilidad de que se formen estos bolsillos, pero pueden formarse a propósito y no podemos esperar que cada billetera evalúe toda la red. en su lugar, los mercados de descubrimiento deben publicar métricas de responsabilidad del operador basadas en análisis de grafos como algoritmos de recolección de premios

## conclusión

proponemos una red de colateral que requiere colusión para robar, pero la colusión aumenta el colateral en riesgo más rápido de lo que aumenta el valor a robar. usamos esta red para asegurar libros contables criptográficos respaldados por reservas completas. estos libros contables atienden cuentas en nombre de billeteras sin conexión a cambio de tarifas pre-negociadas. las primitivas del libro contable soportan condiciones de gasto miniscript suficientes para contratos inteligentes básicos. la red escala de forma casi lineal, permitiendo que una red grande proporcione miles de millones de billeteras y un volumen de transacciones que exceda el de las redes de pago tradicionales
