# bitcoin deposits
## resumen

una versión ideal de dinero electrónico entre pares permitiría que los pagos en línea se envíen directamente de una parte a otra de forma rápida y con una preparación mínima. la lightning network proporciona parte de la solución, pero los beneficios esenciales se pierden si se requiere un tercero de confianza para gestionar el estado en tu nombre. proponemos una solución a este problema utilizando libros de contabilidad verificables y una red de colateral. los operadores emiten actualizaciones del libro de contabilidad a sus pares, creando un registro auditable de cuentas. los monederos emiten evidencia de deshonestidad a esos pares, quienes se aseguran de que el libro de contabilidad mantenga un operador honesto. la salida unilateral se sustituye por la garantía de que los fondos permanecen disponibles mientras la red lo esté. llegamos a una red que delega el mantenimiento de liquidez, evita comisiones de configuración, es capaz de recibir pagos sin conexión y escala independientemente de la capa base

## introducción

bitcoin deposits pretende proporcionar fondos rápidos y escalables controlados por claves, sin confianza, fuera de la cadena. la actividad en la cadena escala con el número de libros de contabilidad y la frecuencia de rotación de reservas. el rendimiento escala ligeramente por encima de lo lineal con el número de libros de contabilidad en la red, haciendo plausibles millones de transacciones por segundo a través de billones de monederos

hay compensaciones explícitas:
- sin salida unilateral: cuando los operadores fallan, los fondos permanecen en la red
- sin privacidad: la verificación requiere transparencia
- disponibilidad intermitente: un depósito es tan disponible como el operador. los monederos deberían repartir los fondos para aumentar la disponibilidad

esperamos que la experiencia del monedero sea similar a una capa base rápida, con una economía de pagos similar a la de la lightning network

## libros de contabilidad

un libro de contabilidad es una cadena inmutable de actualizaciones, que contiene el hash de la actualización anterior y está firmado por el operador del libro. distintos tipos de actualización tienen diferentes reglas que rigen cuándo y cómo pueden utilizarse. los libros de contabilidad son autodescriptivos, sus actualizaciones están disponibles públicamente y son irrefutables, permitiendo a cualquiera evaluar la conformidad

los libros de contabilidad tienen un único operador activo, pero son mantenidos cooperativamente por la malla. cualquier operador puede crear uno, pero si desaparece o se vuelve deshonesto, se asignará un operador diferente junto con las reservas. el operador actualmente activo se identifica por la clave pública que se utilizó para firmar la actualización cofirmada más reciente

## depósitos

un depósito es una cuenta estable que puede enviar y recibir fondos, controlada por miniscript. al abrirse se establece un programa de comisiones, así como si la recepción de fondos requiere una solicitud firmada por el monedero. un operador debe permitir transferencias entre depósitos en el mismo libro de contabilidad así como salidas en la cadena. deberían permitir que los depósitos paguen facturas de lightning

queda a discreción del operador crear ofertas de financiación en la cadena o facturas de lightning en nombre de un depósito. si lo hace, estas deberían ser cofirmadas por un miembro del quórum, y el monedero debería verificar esta firma. las ofertas y facturas no forman parte del libro de contabilidad, por lo que es responsabilidad del monedero verificar las firmas y conservarlas como evidencia

## comisiones

las transferencias entre depósitos, en la cadena y a través de lightning tienen comisiones pagadas al operador del libro de contabilidad. también hay comisiones aplicadas periódicamente a los saldos con un período especificado. todas se negocian cuando se abre un nuevo depósito. las comisiones pueden modificarse después de un número especificado de bloques, con un preaviso de bloques especificado y dentro de un límite porcentual por ajuste negociado en la apertura. el quórum puede negarse a cofirmar actualizaciones que creen circunstancias no rentables de las que en última instancia podrían ser responsables

## transferencias

la forma básica de transferencia es una operación en dos fases entre dos depósitos en el mismo libro de contabilidad: un depósito emite una solicitud para enviar fondos. si hay fondos suficientes disponibles, se añade al libro de contabilidad un bloqueo de los fondos con una condición de gasto. si la condición de gasto se cumple antes de un tiempo límite, los fondos se mueven del remitente al destinatario menos la comisión del operador. si se alcanza el tiempo límite, el bloqueo se libera, menos una comisión del operador más reducida. con condiciones de gasto en miniscript, esto es suficiente para permitir que cualquier depósito proporcione puentes y servicios de liquidez a otros depósitos en el mismo libro de contabilidad

## lightning

los operadores que tengan un canal de lightning pueden permitir que los depósitos envíen y reciban a través de la lightning network. cuando un depósito solicita una factura de lightning, el operador crea una a través de su nodo de lightning, pide a los miembros del quórum que la cofirmen para demostrar que se comprometen a acreditar el depósito tras el pago. el monedero debería conservar esta factura cofirmada como evidencia. cuando un depósito solicita el pago de una factura de lightning, el operador paga utilizando su nodo de lightning y carga el depósito después de obtener el preimage

cuando el pagador y el beneficiario son depósitos en el mismo operador, el operador puede liquidar internamente sin enrutar a través de lightning, acreditando y cargando los depósitos respectivos directamente. esto evita comisiones de enrutamiento y modos de fallo manteniendo las mismas garantías contables

## mensajeros

las solicitudes de transferencia solo mueven fondos entre depósitos en el mismo libro de contabilidad. para mover fondos entre libros de contabilidad, los monederos utilizan mensajeros — servicios que mantienen depósitos en múltiples libros de contabilidad y transportan transferencias entre ellos. un mensajero anuncia su capacidad y comisiones direccionales por libro de contabilidad en el repetidor. cuando un monedero quiere enviar del libro de contabilidad A al libro de contabilidad B, crea un bloqueo de transferencia hacia el depósito del mensajero y solicita que el mensajero cree uno desde su depósito en el libro de contabilidad de destino hacia el beneficiario. una vez establecidos ambos bloqueos, el monedero revela el preimage al beneficiario, quien completa la transferencia desde el mensajero. una vez revelado, el mensajero utiliza este mismo preimage para completar la transferencia del remitente al mensajero

este es un patrón estándar de contrato con bloqueo temporal por hash. esperamos que el tiempo límite de salida del mensajero sea estrictamente anterior al de entrada, asegurando que si el monedero nunca revela, ambos bloqueos expiren y ninguna parte pierda fondos. no se requiere confianza más allá de la garantía de tiempo límite aplicada por los operadores

los mensajeros deberían establecer comisiones por libro de contabilidad: fee_in y fee_out para cada libro de contabilidad que atienden. el monedero estima el coste de la ruta como fee_out en el origen más fee_in en el destino. los mensajeros pueden variar las comisiones por libro de contabilidad según la liquidez disponible, reequilibrando naturalmente sus posiciones. los monederos descubren a los mensajeros a través de sus anuncios en el repetidor y seleccionan en función de la comisión, la capacidad o la cobertura

## comunicación

toda la comunicación entre monederos y operadores, y entre operadores, utiliza repetidores de nostr. las actualizaciones del libro de contabilidad se publican como eventos duraderos que los repetidores retienen, creando un registro auditable permanente. las solicitudes y respuestas entre monederos y operadores son eventos efímeros con un TTL corto en el repetidor. los operadores anuncian sus condiciones como eventos reemplazables, permitiendo a los monederos descubrir y comparar operadores sin un directorio centralizado

esta arquitectura significa que los monederos no necesitan conexiones persistentes — pueden desconectarse indefinidamente y ponerse al día reproduciendo eventos desde cualquier repetidor que los tenga. se puede contactar con los operadores a través de cualquier repetidor que monitoricen, y la elección del repetidor es una decisión de despliegue, no una restricción del protocolo

## reservas y colateral

las reservas se mantienen en un utxo con una cantidad mayor o igual a la suma de las obligaciones del libro de contabilidad, gastable por una mayoría del quórum, con alternativa al operador después de un período significativo

el colateral es el capital propio del operador, depositado y bloqueado en los libros de contabilidad de los miembros del quórum. cada miembro mantiene un depósito de colateral que el operador financia y bloquea durante un período especificado. las obligaciones totales de un libro de contabilidad están limitadas al doble del bloqueo de colateral más pequeño mantenido por cualquier miembro, y la duración del quórum está limitada al tiempo de bloqueo más corto. esto asegura que la red de colateral siempre tenga suficiente respaldo para cubrir una transferencia de custodia. el mismo depósito de colateral puede respaldar múltiples libros de contabilidad para mejorar la eficiencia del capital, aunque los monederos deberían preferir operadores con fuentes de colateral no superpuestas

las obligaciones se aplican al crear nuevas ofertas de financiación o facturas. el operador no puede crear ofertas o facturas que lleven las obligaciones totales del libro de contabilidad por encima de las reservas o por encima del doble del bloqueo de colateral más pequeño, lo que sea menor

## quórum

los operadores solicitan a otros operadores que se unan a su quórum depositando y bloqueando colateral en el libro de contabilidad del miembro. la solicitud incluye el compromiso de colateral (cantidad y duración del bloqueo) y las condiciones del miembro: programas mínimos de comisiones que los depósitos en el libro de contabilidad deben cumplir. cada miembro debe operar su propio libro de contabilidad y puede confiscar el colateral del operador si se demuestra que el operador no es conforme. los miembros especifican límites en los programas de comisiones durante su participación en el quórum — el operador no puede abrir depósitos con comisiones por debajo de los mínimos del miembro más estricto, protegiendo a los miembros de heredar obligaciones no rentables tras una transferencia de custodia

una vez establecido el quórum, las reservas se rotan a un nuevo utxo multisig. los miembros cofirman actualizaciones válidas y participan en la recuperación si el operador firma actualizaciones no conformes. quórums más grandes aumentan la sobrecarga de comunicación pero reducen el riesgo del operador, aumentan la disponibilidad y hacen que la colusión sea más difícil y costosa. los monederos deberían preferir quórums más grandes

## disuasión económica

el protocolo sustituye la salida unilateral por la disuasión económica. los miembros del quórum están directamente incentivados a actuar contra la deshonestidad. durante las operaciones normales obtienen comisiones modestas sobre el colateral, pero en caso de comportamiento probadamente no conforme, pueden confiscar el depósito de colateral completo del operador en su libro de contabilidad

cuando un monedero sospecha de censura, puede escalar la solicitud a los miembros del quórum mediante entrega certificada. el miembro incorpora el hash de la solicitud en su propio libro de contabilidad por una pequeña comisión, creando evidencia causalmente anclada. si el operador no procesa la solicitud, el miembro tiene tanto la evidencia como el incentivo económico para iniciar una disputa

el fraude de facturas de lightning sigue el mismo patrón de disuasión. el operador sabe si se recibió un preimage, pero el monedero no. sin embargo, cualquier pagador podría proporcionar el preimage al monedero. un único robo confirmado desencadena una disputa, la incautación de reservas y la confiscación del colateral. la recompensa de robar un solo pago está acotada, pero el riesgo es existencial, haciendo que el robo mediante lightning sea económicamente irracional a pesar de ser formalmente indemostrable sin la cooperación de un tercero

el modo de fallo tanto para la censura como para la disuasión de lightning es la colusión unánime del quórum. el protocolo no puede proteger contra un quórum que coopera para robar, pero la red de colateral asegura que la colusión cuesta más de lo que se obtiene. la transparencia de la red permite a los monederos y a los mercados de descubrimiento identificar estructuras de quórum sospechosas antes de depositar fondos

## tiempo

el tiempo absoluto se mide contra la capa base. las tolerancias no pueden exceder un número razonable de confirmaciones para mantener la estabilidad durante reorganizaciones de la cadena

donde se requieren tolerancias mayores, nos apoyamos en el ordenamiento causal. un libro de contabilidad criptográfico es una cadena de merkle. cada actualización demuestra que fue creada después de todas las actualizaciones anteriores, pero no proporciona garantías sobre información fuera de la cadena. para construir un ordenamiento distribuido, requerimos que las cofirmas incluyan el hash de la última actualización del libro de contabilidad del cofirmante. ese hash se incorpora entonces al hash de la actualización actual, pasando a formar parte de la cadena así como de todas las demás cadenas para las que el operador del libro de contabilidad cofirma, creando una red de causalidad. esto no puede demostrar el tiempo explícitamente, pero sí puede demostrar que ciertas piezas de información fueron creadas en un orden específico

## pruebas de fraude

podemos demostrar varios tipos de fraude exponiendo información que ha sido creada en el orden incorrecto. cuando la información no se incluye mediante operaciones normales de la red, puede introducirse clandestinamente creando actividad que incluya un hash de la evidencia. una vez incorporada en una actualización firmada por el operador, la evidencia se revela como habiendo sido creada en un lugar no conforme en el ordenamiento:

- un operador, habiendo ofrecido acreditar un depósito con fondos enviados en la cadena a una dirección específica, firma una actualización del libro de contabilidad que no contiene el crédito apropiado, pero sí contiene una cadena que revela algún hash de bloque que excede el número de confirmaciones permitidas antes del crédito

- un operador, habiendo creado una factura de lightning en nombre de un depósito, firma una actualización del libro de contabilidad que no ha acreditado el depósito a pesar de que el preimage ha sido revelado en la cadena

- una cofirma que declara que el hash actual del libro de contabilidad es uno que precede a su propio hash posterior en la cadena

- un miembro del quórum de un libro de contabilidad en disputa que estaba activo pero no actuó de acuerdo con la prueba de fraude dentro de un número de bloques

- firmar o cofirmar actualizaciones del libro de contabilidad no conformes

una prueba de fraude consiste en la evidencia y una cadena causal que conecta el hash incorporado con el libro de contabilidad del operador acusado. la cadena es una secuencia de actualizaciones cofirmadas, cada una incluyendo un member_ledger_hash del libro de contabilidad del enlace anterior. los verificadores recorren la cadena sin necesidad de buscar, confirmando que cada enlace es una actualización firmada, y que el hash de la prueba coincide con los datos incorporados

## recuperación

una vez que un libro de contabilidad se ha vuelto no disponible o no conforme, los miembros del quórum pueden crear su propia continuación del libro de contabilidad desde la última actualización conforme. deben establecer un nuevo quórum y proporcionar atestaciones de colateral. los miembros deben entonces coordinarse para gastar la salida de reservas anterior en una lotería de las posibles cadenas siguientes. el ganador de esta lotería añade una actualización de adquisición a su cadena, y los demás añaden una de cesión. los monederos continúan dirigiéndose al mismo libro de contabilidad, aceptando solo respuestas cofirmadas por el quórum. periódicamente, y cuando ninguna respuesta tiene la cofirma esperada, el monedero debería consultar la red y reproducir las actualizaciones del libro de contabilidad para identificar cambios en la custodia

cuando la no conformidad parece accidental (por ejemplo, un libro de contabilidad ha dejado de estar disponible durante un cierto número de bloques), el cambio de custodia debe ser respetuoso: solo la cantidad de reservas necesaria para cubrir las obligaciones del libro de contabilidad se envía a la lotería, y el cambio se devuelve a la clave pública del operador. el control del colateral no se ve afectado

cuando existe prueba de no conformidad, la cantidad que excede las reservas necesarias se reparte equitativamente entre los miembros del quórum, y se permite confiscar el colateral mantenido en los libros de contabilidad de los miembros

## salud de la red

un ataque directo es formar islas de operadores coludidos. después de acumular obligaciones sustanciales en sus libros de contabilidad, se coordinan para salir, robando fondos que exceden el colateral perdido. la red puede defenderse contra esto, excepto en regiones donde el valor interno excede el colateral que las conecta a la red no coludida. ratios de colateral más altos y quórums más grandes y diversos reducen la probabilidad de que se formen estos bolsillos, pero pueden formarse a propósito y no podemos esperar que cada monedero evalúe toda la red. en su lugar, los mercados de descubrimiento deberían publicar métricas de responsabilidad de los operadores basadas en análisis de grafos como algoritmos de recolección de premios

## conclusión

proponemos una red de colateral que requiere colusión para robar, pero la colusión aumenta el colateral en riesgo más rápido de lo que aumenta el valor a robar. utilizamos esta red para asegurar libros de contabilidad criptográficos respaldados por reservas completas. estos libros de contabilidad dan servicio a cuentas en nombre de monederos sin conexión a cambio de comisiones prenegociadas. las primitivas del libro de contabilidad soportan condiciones de gasto en miniscript suficientes para contratos inteligentes básicos. la red escala de forma casi lineal, permitiendo que una red grande proporcione miles de millones de monederos y un volumen de transacciones superior al de las redes de pago tradicionales
