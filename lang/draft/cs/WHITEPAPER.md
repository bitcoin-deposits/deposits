# bitcoin deposits
## abstrakt

ideální peer-to-peer verze elektronické hotovosti by umožňovala odesílat online platby přímo od jedné strany ke druhé rychle a s minimální přípravou. lightning network poskytuje část řešení, ale zásadní výhody se ztrácejí, pokud je k řízení stavu vaším jménem potřeba důvěryhodná třetí strana. navrhujeme řešení tohoto problému pomocí ověřitelných ledger a sítě collateral. operator vysílají aktualizace ledger svým protějškům a vytvářejí tak auditovatelný záznam účtů. wallet vysílají důkazy o nepoctivosti těmto protějškům, kteří zajišťují, že ledger udržuje poctivého operator. jednostranný odchod je nahrazen zárukou, že prostředky zůstanou dostupné, dokud síť existuje. dospíváme k síti, která deleguje správu likvidity, vyhýbá se vstupním poplatkům, dokáže přijímat platby offline a škáluje nezávisle na základní vrstvě

## úvod

bitcoin deposits si klade za cíl poskytnout rychlé a škálovatelné prostředky řízené klíči, bez nutnosti důvěry, mimo řetězec. aktivita na řetězci škáluje s počtem ledger a frekvencí rotace reserves. propustnost škáluje mírně nadlineárně s počtem ledger v síti, což činí miliony transakcí za sekundu přes biliony wallet reálnými

existují jasné kompromisy:
- žádný jednostranný odchod: když operator selžou, prostředky zůstávají v síti
- žádné soukromí: ověření vyžaduje transparentnost
- přerušovaná dostupnost: deposit je dostupný jen do té míry, do jaké je dostupný operator. wallet by měly rozložit prostředky pro zvýšení dostupnosti

očekáváme, že uživatelský zážitek wallet bude podobný rychlé základní vrstvě s ekonomikou plateb podobnou lightning network

## ledger

ledger je neměnný řetězec aktualizací obsahující hash předchozí aktualizace, podepsaný operator daného ledger. různé typy aktualizací mají různá pravidla určující, kdy a jak je lze použít. ledger jsou samopopisné, jejich aktualizace veřejně dostupné a nepopiratelné, takže kdokoliv může vyhodnotit soulad

ledger mají jednoho aktivního operator, ale kooperativně je udržuje celá síť. kterýkoliv operator může ledger vytvořit, ale pokud zmizí nebo se stane nepoctivým, je přiřazen jiný operator spolu s reserves. aktuálně aktivní operator je identifikován veřejným klíčem použitým k podpisu nejnovější spolupodepsané aktualizace

## deposit

deposit je stabilní účet schopný odesílat a přijímat prostředky, řízený pomocí miniscript. při otevření se stanoví sazebník poplatků a také to, zda přijímání prostředků vyžaduje žádost podepsanou wallet. operator musí umožnit převody mezi deposit na témže ledger i odchody na řetězec. měl by umožnit deposit platit lightning faktury

je na uvážení operator, zda vytvoří nabídky financování na řetězci nebo lightning faktury jménem deposit. pokud tak učiní, měly by být spolupodepsány členem quorum a wallet by měla podpis ověřit. nabídky a faktury nejsou součástí ledger, odpovědnost za ověření podpisů a jejich uchování jako důkazů tedy leží na wallet

## poplatky

převody mezi deposit, na řetězci a přes lightning nesou poplatky placené operator daného ledger. existují i poplatky periodicky účtované ze zůstatků se stanovenou periodou. vše se vyjednává při otevření nového deposit. poplatky lze změnit po stanoveném počtu bloků s daným předstihem v blocích a v rámci procentuálního limitu na úpravu vyjednaného při otevření. quorum může odmítnout spolupodepsat aktualizace vytvářející neziskové podmínky, za které by nakonec mohlo nést odpovědnost

## převody

základní formou převodu je dvoufázová operace mezi dvěma deposit na témže ledger: deposit vydá žádost o odeslání prostředků. pokud je k dispozici dostatek prostředků, na ledger se připojí zámek s podmínkou utracení. je-li podmínka utracení splněna před vypršením časového limitu, prostředky se přesunou od odesílatele k příjemci po odečtení poplatku operator. pokud časový limit vyprší, zámek se uvolní po odečtení menšího poplatku operator. s podmínkami utracení v miniscript to stačí k tomu, aby jakýkoliv deposit mohl poskytovat mosty a likviditní služby ostatním deposit na témže ledger

## lightning

operator s lightning kanálem mohou umožnit deposit odesílat a přijímat přes lightning network. když deposit požádá o lightning fakturu, operator ji vytvoří přes svůj lightning uzel a požádá členy quorum o spolupodpis jako důkaz závazku připsat prostředky na deposit po zaplacení. wallet by si měla spolupodepsanou fakturu uchovat jako důkaz. když deposit požádá o zaplacení lightning faktury, operator zaplatí přes svůj lightning uzel a odečte prostředky z deposit po získání preimage

jsou-li plátce i příjemce deposit u téhož operator, operator může vyrovnat interně bez směrování přes lightning a přímo připisovat a odepisovat příslušné deposit. tím se vyhne směrovacím poplatkům a režimům selhání při zachování stejných účetních záruk

## courier

žádosti o převod přesouvají prostředky pouze mezi deposit na témže ledger. pro přesun prostředků mezi ledger používají wallet courier — služby držící deposit na více ledger a přenášející převody mezi nimi. courier inzeruje kapacitu a směrové poplatky na ledger na relay. když chce wallet odeslat z ledger A na ledger B, vytvoří zámek převodu na deposit courier a požádá courier o vytvoření zámku ze svého deposit na cílovém ledger pro příjemce. jakmile jsou oba zámky vytvořeny, wallet odhalí preimage příjemci, který dokončí převod od courier. po odhalení courier použije tentýž preimage k dokončení převodu od odesílatele ke courier

jde o standardní vzor hash time-locked kontraktu. očekáváme, že časový limit odchozího převodu courier bude striktně dřívější než příchozího, takže pokud wallet preimage nikdy neodhalí, oba zámky vyprší a žádná strana nepřijde o prostředky. důvěra není potřeba nad rámec záruky časového limitu vynucované operator

courier by měli nastavit poplatky na ledger: fee_in a fee_out pro každý ledger, který obsluhují. wallet odhaduje náklady trasy jako fee_out na zdroji plus fee_in na cíli. courier mohou poplatky měnit podle ledger na základě dostupné likvidity a přirozeně tak vyrovnávat své pozice. wallet nacházejí courier prostřednictvím jejich inzerátů na relay a vybírají podle poplatků, kapacity nebo pokrytí

## komunikace

veškerá komunikace mezi wallet a operator i mezi operator navzájem probíhá přes nostr relay. aktualizace ledger se publikují jako trvanlivé události, které relay uchovávají, a vytvářejí tak trvalý auditovatelný záznam. žádosti a odpovědi mezi wallet a operator jsou efemérní události s krátkým TTL na relay. operator inzerují své podmínky jako nahraditelné události, což wallet umožňuje objevovat a porovnávat operator bez centralizovaného adresáře

tato architektura znamená, že wallet nepotřebují trvalé připojení — mohou jít offline na libovolně dlouhou dobu a dohnat zameškané přehráním událostí z jakéhokoli relay, který je má. operator lze zastihnout přes jakýkoli relay, který sledují, a volba relay je rozhodnutím nasazení, nikoli omezením protokolu

## reserves a collateral

reserves se drží v UTXO s částkou větší nebo rovnou součtu závazků ledger, utratitelné většinou quorum, s návratem k operator po významném období

collateral je vlastní kapitál operator, uložený a uzamčený na ledger členů quorum. každý člen drží deposit collateral, který operator financuje a zamyká na stanovenou dobu. celkové závazky ledger jsou omezeny na dvojnásobek nejmenšího zámku collateral drženého jakýmkoli členem a trvání quorum je omezeno na nejkratší dobu zámku. tím je zajištěno, že síť collateral má vždy dostatečné krytí pro převod správy. tentýž deposit collateral může krýt více ledger pro zlepšení kapitálové efektivity, ačkoli wallet by měly preferovat operator s nepřekrývajícími se zdroji collateral

závazky se vynucují při vytváření nových nabídek financování nebo faktur. operator nemůže vytvářet nabídky ani faktury, které by posunuly celkové závazky ledger nad reserves nebo nad dvojnásobek nejmenšího zámku collateral, podle toho, co je nižší

## quorum

operator žádají jiné operator o vstup do svého quorum uložením a uzamčením collateral na ledger člena. žádost zahrnuje závazek collateral (částka a doba zámku) a podmínky člena: minimální sazebníky poplatků, které deposit na ledger musí splňovat. každý člen musí provozovat vlastní ledger a může zabavit collateral operator, pokud je operator prokazatelně nevyhovující. členové stanovují limity sazebníků poplatků po dobu svého členství v quorum — operator nemůže otvírat deposit s poplatky pod minimem nejpřísnějšího člena, čímž chrání členy před zděděním neziskových závazků po převodu správy

jakmile je quorum ustaveno, reserves se rotují do nového multisig UTXO. členové spolupodepisují platné aktualizace a účastní se obnovy, pokud operator podepíše nevyhovující. větší quorum zvyšují komunikační režii, ale snižují riziko operator, zvyšují dostupnost a činí tajné dohody obtížnějšími a nákladnějšími. wallet by měly preferovat větší quorum

## ekonomické odrazení

protokol nahrazuje jednostranný odchod ekonomickým odrazením. členové quorum jsou přímo motivováni jednat proti nepoctivosti. za běžného provozu vydělávají mírné poplatky na collateral, ale v případě prokazatelně nevyhovujícího chování mohou zabavit plný deposit collateral operator na svém ledger

má-li wallet podezření na cenzuru, může žádost eskalovat k členům quorum přes certifikované doručení. člen vloží hash žádosti do svého ledger za malý poplatek a vytvoří tak kauzálně ukotvený důkaz. pokud operator žádost nezpracuje, člen má jak důkaz, tak ekonomickou motivaci zahájit spor

podvod s lightning fakturami podléhá stejnému vzorci odrazení. operator ví, zda preimage obdržel, ale wallet ne. nicméně jakýkoliv plátce může wallet preimage poskytnout. jediná potvrzená krádež spouští spor, zabavení reserves a konfiskaci collateral. odměna za krádež jedné platby je omezená, ale riziko je existenční, takže krádež přes lightning je ekonomicky iracionální, přestože je formálně nedokazatelná bez spolupráce třetí strany

režimem selhání jak cenzury, tak lightning odrazení je jednomyslná tajná dohoda quorum. protokol nedokáže chránit před quorum, které spolupracuje na krádeži, ale síť collateral zajišťuje, že tajné dohody stojí více, než přinášejí. transparentnost sítě umožňuje wallet a tržištím identifikovat podezřelé struktury quorum ještě před uložením prostředků

## čas

absolutní čas se měří vůči základní vrstvě. tolerance nesmí překročit rozumný počet potvrzení, aby zůstala zachována stabilita během reorganizací řetězce

kde jsou potřeba vyšší tolerance, spoléháme se na kauzální řazení. kryptografický ledger je merkle řetězec. každá aktualizace dokazuje, že byla vytvořena po všech předchozích, ale neposkytuje záruky o informacích mimo řetězec. pro konstrukci distribuovaného řazení vyžadujeme, aby spolupodpisy zahrnovaly nejnovější hash aktualizace z ledger spolupodepisujícího. tento hash se začlení do hash aktuální aktualizace a stane se součástí řetězce i všech ostatních řetězců, pro které operator ledger spolupodepisuje, čímž vzniká síť kauzality. tímto nelze explicitně dokázat čas, ale lze dokázat, že určité informace vznikly v konkrétním pořadí

## důkazy o podvodu

různé typy podvodu lze dokázat odhalením informací vytvořených v nesprávném pořadí. pokud informace nejsou zachyceny běžným provozem sítě, mohou se propašovat vytvořením aktivity obsahující hash důkazu. jakmile je začleněna do aktualizace podepsané operator, důkaz se odhalí jako vytvořený na nevyhovujícím místě v řazení:

- operator, který nabídl připsání prostředků na deposit po zaslání na řetězci na konkrétní adresu, podepíše aktualizaci ledger neobsahující příslušný kredit, ale obsahující řetězec odhalující hash bloku přesahující povolený počet potvrzení před připsáním

- operator, který vytvořil lightning fakturu jménem deposit, podepíše aktualizaci ledger, která nepřipsala prostředky na deposit, přestože preimage byl odhalen v řetězci

- spolupodpis deklarující aktuální hash ledger jako takový, který předchází vlastnímu pozdějšímu hash spolupodepisujícího v řetězci

- člen quorum sporného ledger, který byl aktivní, ale nejednal v souladu s důkazem podvodu v rámci stanoveného počtu bloků

- podpis nebo spolupodpis nevyhovujících aktualizací ledger

důkaz o podvodu sestává z důkazů a kauzálního řetězce spojujícího vložený hash s ledger obviněného operator. řetězec je sekvence spolupodepsaných aktualizací, z nichž každá obsahuje member_ledger_hash z ledger předchozího článku. ověřovatelé procházejí řetězcem bez vyhledávání, potvrzují, že každý článek je podepsaná aktualizace a že hash důkazu odpovídá vloženým datům

## obnova

jakmile se ledger stane nedostupným nebo nevyhovujícím, členové quorum mohou vytvořit vlastní pokračování ledger od poslední vyhovující aktualizace. musí ustavit nové quorum a poskytnout atestace collateral. členové pak koordinují utracení předchozího výstupu reserves do loterie potenciálních nástupnických řetězců. vítěz loterie připojí aktualizaci o nabytí ke svému řetězci a ostatní připojí aktualizaci o postoupení. wallet pokračují v adresování téhož ledger a přijímají pouze odpovědi spolupodepsané quorum. pravidelně — a kdykoli odpovědi postrádají očekávaný spolupodpis — by wallet měla dotázat síť a přehrát aktualizace ledger k identifikaci změn ve správě

když nevyhovující chování působí jako nahodilé (např. ledger se stal nedostupným po určitý počet bloků), změna ve správě musí být ohleduplná: do loterie se odešle pouze částka reserves potřebná k pokrytí závazků ledger a zbytek se vrátí na veřejný klíč operator. kontrola nad collateral zůstává nedotčena

pokud existuje důkaz o nevyhovujícím chování, částka přesahující nutné reserves se rozdělí rovným dílem mezi členy quorum a collateral držený na ledger členů může být zabaven

## zdraví sítě

jedním přímočarým útokem je tvorba ostrovů tajně se dohodujících operator. po vybudování značných závazků na svých ledger koordinují odchod a kradou prostředky přesahující ztracenou collateral. síť se může bránit, s výjimkou oblastí, kde vnitřní hodnota přesahuje collateral spojující ji s nepodvádějící sítí. vyšší poměry collateral a větší, rozmanitější quorum snižují pravděpodobnost vzniku těchto kapes, ale mohou vzniknout úmyslně a nemůžeme čekat, že každá wallet vyhodnotí celou síť. místo toho by tržiště měla publikovat metriky odpovědnosti operator na základě grafových analýz, jako jsou algoritmy prize-collecting

## závěr

navrhujeme síť collateral, která k ukradení prostředků vyžaduje tajnou dohodu, ale tajná dohoda zvyšuje ohrožený collateral rychleji, než roste hodnota k ukradení. tuto síť používáme k zabezpečení kryptografických ledger krytých plnými reserves. tyto ledger obsluhují účty jménem offline wallet výměnou za předem vyjednané poplatky. primitivy ledger podporují podmínky utracení v miniscript dostatečné pro základní chytré kontrakty. síť škáluje téměř lineárně, což velké síti umožňuje obsluhovat miliardy wallet s objemem transakcí přesahujícím tradiční platební sítě
