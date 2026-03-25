# bitcoin deposits
## abstrakt

idealna wersja elektronicznej gotówki peer-to-peer pozwalałaby na przesyłanie płatności online bezpośrednio między stronami, szybko i przy minimalnym przygotowaniu. lightning network zapewnia częściowe rozwiązanie, ale istotne korzyści zostają utracone, jeśli zaufana trzecia strona jest wymagana do zarządzania stanem w twoim imieniu. proponujemy rozwiązanie tego problemu z wykorzystaniem weryfikowalnych ksiąg i sieci zabezpieczeń. operatorzy rozsyłają aktualizacje ksiąg do swoich partnerów, tworząc audytowalny rejestr kont. portfele rozsyłają dowody nieuczciwości do tych partnerów, którzy zapewniają, że księga utrzymuje uczciwego operatora. jednostronne wyjście zastępowane jest gwarancją, że środki pozostają dostępne tak długo, jak długo istnieje sieć. w rezultacie otrzymujemy sieć, która deleguje zarządzanie płynnością, unika opłat konfiguracyjnych, jest zdolna do odbierania płatności offline i skaluje się niezależnie od warstwy bazowej

## wprowadzenie

bitcoin deposits ma na celu zapewnienie szybkich i skalowalnych środków kontrolowanych kluczem, bez zaufania, poza łańcuchem. aktywność on-chain skaluje się z liczbą ksiąg i częstotliwością rotacji rezerw. przepustowość skaluje się nieco ponad liniowo z liczbą ksiąg w sieci, co sprawia, że miliony transakcji na sekundę dla bilionów portfeli są realne

istnieją wyraźne kompromisy:
- brak jednostronnego wyjścia: gdy operatorzy zawodzą, środki pozostają w sieci
- brak prywatności: weryfikacja wymaga przejrzystości
- przerywana dostępność: depozyt jest tak dostępny, jak operator. portfele powinny rozdzielać środki, aby zwiększyć dostępność

oczekujemy, że doświadczenie portfela będzie podobne do szybkiej warstwy bazowej, z ekonomią płatności zbliżoną do lightning network

## księgi

księga jest niezmiennym łańcuchem aktualizacji, zawierającym hash poprzedniej aktualizacji i podpisanym przez operatora księgi. różne typy aktualizacji mają różne zasady określające, kiedy i jak mogą być używane. księgi są samoopisowe, ich aktualizacje publicznie dostępne i niezaprzeczalne, co pozwala każdemu ocenić zgodność

księgi mają jednego aktywnego operatora, ale są kooperatywnie utrzymywane przez sieć mesh. każdy operator może utworzyć księgę, ale jeśli zniknie lub stanie się nieuczciwy, zostanie przydzielony inny operator wraz z rezerwami. aktualnie aktywny operator jest identyfikowany przez klucz publiczny użyty do podpisania najnowszej współpodpisanej aktualizacji

## depozyty

depozyt to stabilne konto, które może wysyłać i odbierać środki, kontrolowane przez miniscript. przy otwarciu ustalany jest harmonogram opłat, a także to, czy odbieranie środków wymaga żądania podpisanego przez portfel. operator musi zezwalać na transfery między depozytami na tej samej księdze oraz na wyjścia on-chain. powinien umożliwiać depozytom opłacanie faktur lightning

to operator decyduje, czy tworzyć oferty finansowania on-chain lub faktury lightning w imieniu depozytu. jeśli to robi, powinny być one współpodpisane przez członka kworum, a portfel powinien zweryfikować ten podpis. oferty i faktury nie są częścią księgi, więc to portfel jest odpowiedzialny za weryfikację podpisów i ich przechowywanie jako dowodów

## opłaty

transfery między depozytami, on-chain i przez lightning mają opłaty płacone operatorowi księgi. istnieją również opłaty okresowo naliczane od sald z określonym okresem. wszystkie są negocjowane przy otwarciu nowego depozytu. opłaty mogą być zmieniane po określonej liczbie bloków, z określonym wyprzedzeniem blokowym i w ramach procentowego limitu na korektę, wynegocjowanego przy otwarciu. kworum może odmówić współpodpisania aktualizacji, które tworzą nieopłacalne okoliczności, za które mogłoby ostatecznie odpowiadać

## transfery

podstawową formą transferu jest operacja dwufazowa między dwoma depozytami na tej samej księdze: depozyt wysyła żądanie przesłania środków. jeśli dostępne są wystarczające środki, do księgi dodawana jest blokada środków z warunkiem wydania. jeśli warunek wydania zostanie spełniony przed upływem limitu czasu, środki przechodzą od nadawcy do odbiorcy minus opłata operatora. jeśli limit czasu zostanie osiągnięty, blokada jest zwalniana, minus mniejsza opłata operatora. dzięki warunkom wydania miniscript jest to wystarczające, aby każdy depozyt mógł świadczyć usługi mostów i płynności dla innych depozytów na tej samej księdze

## lightning

operatorzy posiadający kanał lightning mogą pozwalać depozytom na wysyłanie i odbieranie przez lightning network. gdy depozyt żąda faktury lightning, operator tworzy ją za pośrednictwem swojego węzła lightning, prosi członków kworum o jej współpodpisanie w celu udowodnienia, że zobowiązują się do uznania depozytu po dokonaniu płatności. portfel powinien zachować tę współpodpisaną fakturę jako dowód. gdy depozyt żąda opłacenia faktury lightning, operator płaci za pomocą swojego węzła lightning i obciąża depozyt po uzyskaniu preimage

gdy płatnik i odbiorca są depozytami u tego samego operatora, operator może rozliczyć wewnętrznie bez routingu przez lightning, bezpośrednio uznając i obciążając odpowiednie depozyty. pozwala to uniknąć opłat za routing i trybów awarii, zachowując te same gwarancje księgowe

## kurierzy

żądania transferu przenoszą środki tylko między depozytami na tej samej księdze. aby przenosić środki między księgami, portfele używają kurierów — usług posiadających depozyty na wielu księgach i przenoszących transfery między nimi. kurier ogłasza pojemność i kierunkowe opłaty per księga na przekaźniku. gdy portfel chce wysłać z księgi A na księgę B, tworzy blokadę transferu na depozyt kuriera i żąda, aby kurier utworzył blokadę ze swojego depozytu na księdze docelowej na rzecz odbiorcy. gdy obie blokady są ustanowione, portfel ujawnia preimage odbiorcy, który realizuje transfer od kuriera. po ujawnieniu kurier używa tego samego preimage, aby zrealizować transfer od nadawcy do kuriera

jest to standardowy wzorzec kontraktu hash time-locked. oczekujemy, że limit czasu wychodzący kuriera będzie ściśle wcześniejszy niż przychodzący, co zapewnia, że jeśli portfel nigdy nie ujawni, obie blokady wygasną i żadna strona nie straci środków. nie jest wymagane zaufanie poza gwarancją limitu czasu egzekwowaną przez operatorów

kurierzy powinni ustalać opłaty per księga: fee_in i fee_out dla każdej obsługiwanej księgi. portfel szacuje koszt trasy jako fee_out na źródle plus fee_in na celu. kurierzy mogą różnicować opłaty w zależności od księgi na podstawie dostępnej płynności, naturalnie równoważąc swoje pozycje. portfele odkrywają kurierów poprzez ich ogłoszenia na przekaźniku i wybierają na podstawie opłat, pojemności lub zasięgu

## komunikacja

cała komunikacja między portfelami i operatorami oraz między operatorami wykorzystuje przekaźniki nostr. aktualizacje ksiąg są publikowane jako trwałe zdarzenia, które przekaźniki przechowują, tworząc permanentny audytowalny rejestr. żądania i odpowiedzi między portfelami i operatorami są efemerycznymi zdarzeniami z krótkim TTL przekaźnika. operatorzy ogłaszają swoje warunki jako zdarzenia zastępowalne, umożliwiając portfelom odkrywanie i porównywanie operatorów bez scentralizowanego katalogu

ta architektura oznacza, że portfele nie potrzebują trwałych połączeń — mogą przejść w tryb offline na czas nieokreślony i nadrobić zaległości, odtwarzając zdarzenia z dowolnego przekaźnika, który je posiada. operatorzy mogą być osiągani przez dowolny przekaźnik, który monitorują, a wybór przekaźnika jest decyzją wdrożeniową, nie ograniczeniem protokołu

## rezerwy i zabezpieczenia

rezerwy są przechowywane w utxo o kwocie większej lub równej sumie zobowiązań księgi, wydawalne przez większość kworum, z awaryjnym przejściem do operatora po znacznym okresie

zabezpieczenie to własny kapitał operatora, zdeponowany i zablokowany na księgach członków kworum. każdy członek posiada depozyt zabezpieczający, który operator finansuje i blokuje na określony czas. łączne zobowiązania księgi są ograniczone do dwukrotności najmniejszej blokady zabezpieczenia posiadanej przez dowolnego członka, a czas trwania kworum jest ograniczony do najkrótszego czasu blokady. zapewnia to, że sieć zabezpieczeń zawsze ma wystarczające pokrycie na transfer powiernictwa. ten sam depozyt zabezpieczający może wspierać wiele ksiąg w celu poprawy efektywności kapitałowej, choć portfele powinny preferować operatorów z nienakładającymi się źródłami zabezpieczeń

zobowiązania są egzekwowane przy tworzeniu nowych ofert finansowania lub faktur. operator nie może tworzyć ofert ani faktur, które pchnęłyby łączne zobowiązania księgi powyżej rezerw lub powyżej dwukrotności najmniejszej blokady zabezpieczenia, w zależności od tego, co jest niższe

## kworum

operatorzy proszą innych operatorów o dołączenie do ich kworum poprzez zdeponowanie i zablokowanie zabezpieczenia na księdze członka. żądanie zawiera zobowiązanie zabezpieczenia (kwotę i czas blokady) oraz warunki członka: minimalne harmonogramy opłat, które depozyty na księdze muszą spełniać. każdy członek musi prowadzić własną księgę i może skonfiskować zabezpieczenie operatora, jeśli operator okaże się niezgodny. członkowie określają limity harmonogramów opłat podczas ich członkostwa w kworum — operator nie może otwierać depozytów z opłatami poniżej najsurowszych minimów członka, chroniąc członków przed odziedziczeniem nieopłacalnych zobowiązań po transferze powiernictwa

po ustanowieniu kworum rezerwy są rotowane do nowego multisig utxo. członkowie współpodpisują prawidłowe aktualizacje i uczestniczą w odzyskiwaniu, jeśli operator podpisuje niezgodne. większe kwora zwiększają narzut komunikacyjny, ale zmniejszają ryzyko operatora, zwiększają dostępność i sprawiają, że zmowa jest trudniejsza i droższa. portfele powinny preferować większe kwora

## odstraszanie ekonomiczne

protokół zastępuje jednostronne wyjście odstraszaniem ekonomicznym. członkowie kworum są bezpośrednio zmotywowani do działania przeciwko nieuczciwości. podczas normalnych operacji zarabiają skromne opłaty od zabezpieczenia, ale w przypadku udowodnionego niezgodnego zachowania mogą skonfiskować pełny depozyt zabezpieczający operatora na swojej księdze

gdy portfel podejrzewa cenzurę, może eskalować żądanie do członków kworum za pośrednictwem poświadczonego dostarczenia. członek osadza hash żądania w swojej własnej księdze za niewielką opłatą, tworząc przyczynowo zakotwiczony dowód. jeśli operator nie przetworzy żądania, członek ma zarówno dowód, jak i ekonomiczną motywację do wszczęcia sporu

oszustwo faktur lightning podlega temu samemu wzorcowi odstraszania. operator wie, czy preimage został otrzymany, ale portfel nie wie. jednakże każdy płatnik może dostarczyć preimage do portfela. pojedyncza potwierdzona kradzież wyzwala spór, zajęcie rezerw i konfiskatę zabezpieczenia. nagroda za kradzież pojedynczej płatności jest ograniczona, ale ryzyko jest egzystencjalne, co sprawia, że kradzież lightning jest ekonomicznie irracjonalna, mimo że formalnie nieudowodniona bez współpracy strony trzeciej

tryb awarii zarówno dla cenzury, jak i odstraszania lightning to jednomyślna zmowa kworum. protokół nie może chronić przed kworum, które współpracuje w celu kradzieży, ale sieć zabezpieczeń zapewnia, że zmowa kosztuje więcej niż zyskuje. przejrzystość sieci pozwala portfelom i rynkom odkrywania identyfikować podejrzane struktury kworum przed zdeponowaniem środków

## czas

czas absolutny jest mierzony względem warstwy bazowej. tolerancje nie mogą przekraczać rozsądnej liczby potwierdzeń w celu utrzymania stabilności podczas reorganizacji łańcucha

tam, gdzie wymagane są wyższe tolerancje, polegamy na porządkowaniu przyczynowym. kryptograficzna księga jest łańcuchem merkle. każda aktualizacja dowodzi, że została utworzona po wszystkich aktualizacjach przed nią, ale nie daje gwarancji co do informacji spoza łańcucha. aby skonstruować rozproszone porządkowanie, wymagamy, aby współpodpisy zawierały najnowszy hash aktualizacji z księgi współpodpisującego. ten hash jest następnie włączany do hasha bieżącej aktualizacji, stając się częścią łańcucha, jak również częścią wszystkich innych łańcuchów, dla których operator księgi współpodpisuje, tworząc sieć przyczynowości. nie jest to w stanie udowodnić czasu wprost, ale jest w stanie udowodnić, że pewne informacje zostały utworzone w określonej kolejności

## dowody oszustwa

możemy udowodnić różne rodzaje oszustwa, ujawniając informacje, które zostały utworzone w niewłaściwej kolejności. tam, gdzie informacje nie są włączane w ramach normalnych operacji sieciowych, mogą być przemycone przez tworzenie aktywności, która zawiera hash dowodów. po włączeniu do aktualizacji podpisanej przez operatora, dowód zostaje ujawniony jako utworzony w niezgodnym miejscu porządku:

- operator, który zaoferował uznanie depozytu środkami wysłanymi on-chain na konkretny adres, podpisuje aktualizację księgi, która nie zawiera odpowiedniego uznania, ale zawiera łańcuch ujawniający hash bloku przekraczający liczbę potwierdzeń dozwolonych przed uznaniem

- operator, który utworzył fakturę lightning w imieniu depozytu, podpisuje aktualizację księgi, która nie uznała depozytu pomimo ujawnienia preimage w łańcuchu

- współpodpis, który deklaruje, że bieżący hash księgi jest tym, który poprzedza ich własny późniejszy hash w łańcuchu

- członek kworum kwestionowanej księgi, który był aktywny, ale nie działał zgodnie z dowodem oszustwa w ciągu określonej liczby bloków

- podpisywanie lub współpodpisywanie niezgodnych aktualizacji księgi

dowód oszustwa składa się z dowodów i łańcucha przyczynowego łączącego osadzony hash z księgą oskarżonego operatora. łańcuch jest sekwencją współpodpisanych aktualizacji, z których każda zawiera member_ledger_hash z księgi poprzedniego ogniwa. weryfikatorzy przechodzą łańcuch bez wyszukiwania, potwierdzając, że każde ogniwo jest podpisaną aktualizacją i że hash dowodu odpowiada osadzonym danym

## odzyskiwanie

gdy księga stanie się niedostępna lub niezgodna, członkowie kworum mogą utworzyć własną kontynuację księgi od ostatniej zgodnej aktualizacji. muszą ustanowić nowe kworum i dostarczyć poświadczenia zabezpieczenia. członkowie muszą następnie skoordynować wydanie poprzedniego wyjścia rezerw do loterii potencjalnych kolejnych łańcuchów. zwycięzca tej loterii dołącza aktualizację przejęcia do swojego łańcucha, a pozostali dołączają ustąpienie. portfele nadal adresują tę samą księgę, akceptując tylko odpowiedzi współpodpisane przez kworum. okresowo, oraz gdy żadne odpowiedzi nie mają oczekiwanego współpodpisu, portfel powinien odpytać sieć i odtworzyć aktualizacje księgi, aby zidentyfikować zmiany w powiernictwie

gdy niezgodność wydaje się przypadkowa (np. księga stała się niedostępna na pewną liczbę bloków), zmiana powiernictwa musi być szanująca: tylko kwota rezerw wymagana do pokrycia zobowiązań księgi jest wysyłana do loterii, a reszta zwracana na klucz publiczny operatora. kontrola nad zabezpieczeniem pozostaje nienaruszona

gdy istnieje dowód niezgodności, kwota przekraczająca niezbędne rezerwy jest dzielona równo między członków kworum, a zabezpieczenie utrzymywane na księgach członków może zostać skonfiskowane

## zdrowie sieci

jednym prostym atakiem jest tworzenie wysp zmówionych operatorów. po zbudowaniu znacznych zobowiązań na swoich księgach koordynują wyjście, kradnąc środki przekraczające utracone zabezpieczenie. sieć może się przed tym bronić, z wyjątkiem regionów, w których wewnętrzna wartość przekracza zabezpieczenie łączące go z niezmówiną siecią. wyższe wskaźniki zabezpieczenia i większe, bardziej zróżnicowane kwora zmniejszają prawdopodobieństwo tworzenia się tych enklaw, ale mogą one powstawać celowo i nie możemy oczekiwać, że każdy portfel oceni całą sieć. zamiast tego rynki odkrywania powinny publikować metryki odpowiedzialności operatorów na podstawie analiz grafowych, takich jak algorytmy prize-collecting

## podsumowanie

proponujemy sieć zabezpieczeń, która wymaga zmowy do kradzieży, ale zmowa zwiększa zabezpieczenie narażone na ryzyko szybciej niż zwiększa wartość do kradzieży. używamy tej sieci do zabezpieczenia kryptograficznych ksiąg wspieranych pełnymi rezerwami. te księgi obsługują konta w imieniu portfeli offline w zamian za wcześniej wynegocjowane opłaty. prymitywy księgi wspierają warunki wydania miniscript wystarczające do podstawowych inteligentnych kontraktów. sieć skaluje się blisko liniowo, pozwalając dużej sieci obsługiwać miliardy portfeli i wolumen transakcji przekraczający tradycyjne sieci płatnicze
