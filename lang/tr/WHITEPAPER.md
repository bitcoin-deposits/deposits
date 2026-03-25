# bitcoin deposits
## ozet

ideal bir esler arasi elektronik nakit sistemi, cevrimici odemelerin bir taraftan digerine hizli ve minimum hazirlikla dogrudan gonderilmesine olanak tanir. lightning agi cozumun bir kismini saglar, ancak durumu sizin adiniza yonetmek icin guvenilir bir ucuncu tarafa ihtiyac duyulursa temel faydalar kaybolur. bu soruna dogrulanabilir defterler ve bir teminat agi kullanarak bir cozum oneriyoruz. operatorler defter guncellemelerini eslerine yayinlayarak denetlenebilir bir hesap kaydi olusturur. cuzdanlar sahtekarlik kanitlarini bu eslere yayinlar ve esler defterin durust bir operator tarafindan yonetilmesini saglar. tek tarafli cikis, ag var oldugu surece fonlarin erisilebilir kalacagi garantisiyle degistirilir. sonuc olarak likidite yonetimini devreden, kurulum ucreti gerektirmeyen, cevrimi disi odeme alabilen ve temel katmandan bagimsiz olarak olceklenen bir aga ulasiyoruz

## giris

bitcoin deposits, hizli ve olceklenebilir anahtar kontrollü fonlari güvensizce, zincir disi olarak saglamayi amaclar. zincir uzerindeki aktivite, defter sayisi ve rezerv rotasyon sikligi ile olceklenir. islem hacmi, aglardaki defter sayisiyla dogrusalin biraz uzerinde olceklenir, bu da milyonlarca islem/saniye ve trilyonlarca cuzdan kapasitesini mumkun kilar

acik odunlesimler vardir:
- tek tarafli cikis yok: operatorler basarisiz oldugunda fonlar agda kalir
- gizlilik yok: dogrulama seffaflik gerektirir
- aralikli erisilebilirlik: bir mevduat yalnizca operator kadar erisilebilirdir. cuzdanlar erisilebilirligi artirmak icin fonlari dagitmalidir

cuzdan deneyiminin hizli bir temel katmana benzemesini ve odeme ekonomisinin lightning agina benzer olmasini bekliyoruz

## defterler

bir defter, onceki guncellemenin hash degerini iceren ve defterin operatoru tarafindan imzalanan degismez bir guncelleme zinciridir. farkli guncelleme turleri, ne zaman ve nasil kullanilabileceklerini belirleyen farkli kurallara sahiptir. defterler kendi kendini tanimlar, guncellemeleri herkese acik ve inkar edilemezdir, bu da herkesin uygunlugu degerlendirmesine olanak tanir

defterlerin tek bir aktif operatoru vardir, ancak ag tarafindan isbirlikci olarak surdurulur. herhangi bir operator bir defter olusturabilir, ancak kaybolmasi veya sahtekar olmasi durumunda rezervlerle birlikte farkli bir operator atanir. su anda aktif olan operator, en son ortak imzali guncellemeyi imzalamak icin kullanilan acik anahtar ile tanimlanir

## mevduatlar

bir mevduat, miniscript tarafindan kontrol edilen, fon gonderip alabilen sabit bir hesaptir. acilista bir ucret tarifesi belirlenir ve fon almanin cuzdan imzali bir istek gerektirip gerektirmedigi karardastirilir. bir operator, ayni defterdeki mevduatlar arasinda transferlere ve zincir uzerindeki cikislara izin vermek zorundadir. mevduatlarin lightning faturalarini odemesine de izin vermelidirler

bir mevduat adina zincir uzerinde finansman teklifleri veya lightning faturalari olusturmak operatorun takdirine baglidir. olusturulursa bunlar bir nisap uyesi tarafindan ortak imzalanmali ve cuzdan bu imzayi dogrulamalidir. teklifler ve faturalar defterin bir parcasi degildir, bu nedenle imzalari dogrulamak ve kanit olarak saklamak cuzdanin sorumlulugundadir

## ucretler

mevduatlar arasindaki, zincir uzerindeki ve lightning uzerinden yapilan transferlerin ucretleri defterin operatorune odenir. ayrica belirli bir periyotla bakiyelere periyodik olarak uygulanan ucretler de vardir. tumü yeni bir mevduat acildiginda muzakere edilir. ucretler, belirli sayida bloktan sonra, belirli bir blok bildirimi ve acilista muzakere edilen ayarlama basina yuzde siniri dahilinde degistirilebilir. nisap, nihayetinde sorumlu olabilecekleri karlilik getirmeyen kosullar yaratan guncellemeleri ortak imzalamayi reddedebilir

## transferler

temel transfer bicimi, ayni defterdeki iki mevduat arasinda iki asamali bir islemdir: bir mevduat fon gonderme istegi yayinlar. yeterli fon mevcutsa, harcama kosulu olan bir kilit deftere eklenir. harcama kosulu zaman asimi oncesinde karsilanirsa, fonlar gondericiden aliciya operator ucretini dusulmus olarak aktarilir. zaman asimina urasilirsa, kilit daha kucuk bir operator ucretiyle serbest birakilir. miniscript harcama kosullari ile bu, herhangi bir mevduatin ayni defterdeki diger mevduatlara kopru ve likidite hizmetleri sunmasina yeterlidir

## lightning

bir lightning kanalina sahip operatorler, mevduatlarin lightning agi uzerinden gonderme ve alma islemlerini yapmasina izin verebilir. bir mevduat lightning faturasi talep ettiginde, operator lightning dugumu uzerinden bir fatura olusturur ve nisap uyelerinden odeme alindiginda mevduati alacaklandirmaya taahhut ettiklerini kanitlamak icin ortak imzalamalarini ister. cuzdan bu ortak imzali faturayi kanit olarak saklamalidir. bir mevduat lightning faturasi odemesi talep ettiginde, operator lightning dugumu uzerinden odeme yapar ve preimage elde ettikten sonra mevduattan duser

odeme yapan ve alan ayni operatordeki mevduatlar oldugunda, operator lightning uzerinden yonlendirme yapmadan dahili olarak kapatabilir ve ilgili mevduatlari dogrudan alacaklandirir ve borclandirir. bu, ayni muhasebe garantilerini korurken yonlendirme ucretlerinden ve hata modlarindan kacinir

## kuryeler

transfer istekleri yalnizca ayni defterdeki mevduatlar arasinda fon tasir. defterler arasinda fon tasimak icin cuzdanlar kuryeleri kullanir — birden fazla defterde mevduati olan ve aralarinda transfer tasiyan hizmetler. bir kurye, kapasite ve defter basina yonlu ucretleri aktarici uzerinde ilan eder. bir cuzdan A defterinden B defterine gondermek istediginde, kuryenin mevduatina bir transfer kilidi olusturur ve kuryeden hedef defterdeki mevduatindan aliciya bir kilit olusturmasini talep eder. her iki kilit de olusturuldugunda cuzdan preimage degerini aliciya aciklar ve alici kuryeden transferi tamamlar. aciklandiktan sonra kurye ayni preimage degerini kullanarak gondericiden kuryeye olan transferi tamamlar

bu standart bir hash zaman kilitli sozlesme kalobidir. kuryenin giden zaman asiminin gelen zaman asiminden kesinlikle once olmasi beklenir, boylece cuzdan preimage degerini hicbir zaman aciklamazsa her iki kilit de sona erer ve iki taraf da fon kaybetmez. operatorler tarafindan uygulanan zaman asimi garantisinin otesinde guven gerekli degildir

kuryeler defter basina ucret belirlemelidir: hizmet verdikleri her defter icin fee_in ve fee_out. cuzdan rota maliyetini kaynaktaki fee_out arti hedefteki fee_in olarak tahmin eder. kuryeler mevcut likiditeye gore defter bazinda ucretleri degistirebilir ve pozisyonlarini dogal olarak yeniden dengeleyebilir. cuzdanlar kuryeleri aktarici uzerindeki ilanlari araciligiyla kesfeder ve ucret, kapasite veya kapsama gore secer

## iletisim

cuzdanlar ve operatorler arasindaki ve operatorler arasindaki tum iletisim nostr aktaricilari kullanir. defter guncellemeleri aktaricilarin sakladigi kalici olaylar olarak yayinlanir ve kalici denetlenebilir bir kayit olusturur. cuzdanlar ve operatorler arasindaki istekler ve yanitlar, kisa aktarici TTL degerine sahip gecici olaylardir. operatorler kosullarini degistirilebilir olaylar olarak ilan eder ve cuzdanlarin merkezi bir dizin olmadan operatorleri kesfetmesine ve karsilastirmasina olanak tanir

bu mimari, cuzdanlarin kalici baglantilara ihtiyac duymadigi anlamina gelir -- suresiz olarak cevrimi disi kalabilir ve olaylari bulunan herhangi bir aktaricidan yeniden oynayarak guncellenebilirler. operatorlere izledikleri herhangi bir aktarici araciligiyla ulasilabilir ve aktarici secimi bir dagitim kararidir, protokol kisitlamasi degildir

## rezervler ve teminat

rezervler, bir defterin yukumluluklerinin toplamindan buyuk veya esit miktarda bir utxo icinde tutulur, nisabin cogunlugu tarafindan harcanabilir ve onemli bir sureden sonra operatore geri doner

teminat, operatorun kendi sermayesidir, nisap uyelerinin defterlerine yatirilir ve kilitlenir. her uye, operatorun fonladigi ve belirli bir sure icin kiledigi bir teminat mevduati tutar. bir defterin toplam yukumlulukleri, herhangi bir uyenin tuttugu en kucuk teminat kilidinin iki katiyla sinirlidir ve nisabin suresi en kisa kilit suresiyle sinirlidir. bu, teminat aginin bir velayet transferini karsilamak icin her zaman yeterli destege sahip olmasini saglar. ayni teminat mevduati sermaye verimliligi icin birden fazla defteri destekleyebilir, ancak cuzdanlar cakismayan teminat kaynaklarina sahip operatorleri tercih etmelidir

yukumlulukler yeni finansman teklifleri veya faturalar olusturulurken uygulanir. operator, defterin toplam yukumluluklerini rezervlerin veya en kucuk teminat kilidinin iki katinin uzerine cikaracak teklifler veya faturalar olusturamaz; hangisi dusukse o gecerlidir

## nisap

operatorler, uyenin defterinde teminat yatirip kilitleyerek diger operatorleri nisaplarina katilmaya davet eder. talep, teminat taahhudunu (miktar ve kilit suresi) ve uyenin kosullarini icerir: defterdeki mevduatlarin karsilamasi gereken minimum ucret tarifeleri. her uye kendi defterini isletmelidir ve operatorun uyumsuz oldugu kanitlanirsa operatorun teminatina el koyabilir. uyeler nisap uyelikleri sirasinda ucret tarifelerine sinirlar koyar -- operator, en kati uyenin minimum ucretlerinin altinda mevduat acamaz, bu da bir velayet transferinden sonra uyeleri karlilik getirmeyen yukumluluklerden korur

nisap olusturuldugunda, rezervler yeni bir multisig utxo icine dondurulur. uyeler gecerli guncellemeleri ortak imzalar ve operator uyumsuz guncellemeler imzalarsa kurtarma islemine katilir. daha buyuk nisaplar iletisim yukunu artirir ancak operator riskini azaltir, erisilebilirligi artirir ve gizli anlasmayi daha zor ve pahali hale getirir. cuzdanlar daha buyuk nisaplari tercih etmelidir

## ekonomik caydiricilik

protokol tek tarafli cikisi ekonomik caydiricilikla degistirir. nisap uyeleri sahtekarliga karsi harekete gecmek icin dogrudan tesvik edilir. normal islemler sirasinda teminat uzerinden mutevazi ucretler kazanirlar, ancak kanitlanabilir uyumsuz davranis durumunda operatorun kendi defterlerindeki tam teminat mevduatina el koyma hakki kazanirlar

bir cuzdan sansur suphelendiginde, talebi sertifikali teslimat yoluyla nisap uyelerine iletebilir. uye, talebin hash degerini kucuk bir ucret karsiliginda kendi defterine gomer ve nedensel olarak sabitleenmis kanit olusturur. operator talebi islemezse, uye hem kanita hem de bir anlamazlik baslatmak icin ekonomik tesvike sahiptir

lightning fatura dolandiriciligi ayni caydiricilik kalibi izler. operator bir preimage alinip alinmadigini bilir, ancak cuzdan bilmez. bununla birlikte herhangi bir odeme yapici preimage degerini cuzdana saglayabilir. tek bir dogrulanmis hirsizlik, anlamazlik, rezervlere el koyma ve teminat musaderesi tetikler. tek bir odemeyi calmanin odulu sinirlidir, ancak risk varolussel duzeydir, bu da ucuncu taraf isbirligi olmadan resmi olarak kanitlanamazsa bile lightning hirsizligini ekonomik olarak mantiksizklar

hem sansur hem de lightning caydiriciliginin basarisizlik modu oybirligiyle nisap gizli anlasmasidir. protokol calma icin isbirligi yapan bir nisaba karsi koruma saglayamaz, ancak teminat agi gizli anlasmanin kazancindan daha pahaliya mal olmasini saglar. agin seffafligi, cuzdanlarin ve kesfetme piyasalarinin fon yatirmadan once suphe cekici nisap yapilarini tanimlamasina olanak tanir

## zaman

mutlak zaman temel katmana gore olculur. toleranslar, zincir yeniden organizasyonlari sirasinda kararliligi korumak icin makul sayida onay asamamalidir

daha yuksek toleranslar gerektigi durumlarda nedensel siralamaya guveniyoruz. bir kriptografik defter bir merkle zinciridir. her guncelleme kendinden onceki tum guncellemelerden sonra olusturuldugunu kanitlar, ancak zincir disindaki bilgiler hakkinda hicbir garanti saglamaz. dagitik bir siralama olusturmak icin, ortak imzalarin ortak imzacinin defterindeki en son guncelleme hash degerini icermesini gerektiriyoruz. bu hash daha sonra mevcut guncellemenin hash degerine dahil edilir ve hem bu zincirin hem de defter operatorunun ortak imzaladigi diger tum zincirlerin bir parcasi olur, bir nedensellik agi olusturur. bu zamani acikca kanitlayamaz, ancak belirli bilgi parcalarinin belirli bir sirada olusturuldugunu kanitlayabilir

## dolandiricilik kanitlari

yanlis sirada olusturulan bilgileri aciga cikararak cesitli dolandiricilik turlerini kanitlayabiliriz. bilgi normal ag islemleri tarafindan dahil edilmedigi durumlarda, kanitin hash degerini iceren bir aktivite olusturularak iceri sizdirilabilir. operator tarafindan imzalanan bir guncellemeye dahil edildikten sonra, kanitin siralamada uyumsuz bir yerde olusturuldugu ortaya cikar:

- bir operator, belirli bir adrese zincir uzerinde gonderilen fonlarla bir mevduati alacaklandirma teklifi yapmis olup, uygun alacaklandirmayi icermeyen ancak alacaklandirma icin izin verilen onay sayisini asan bir blok hash degerini iceren bir zincir ortaya koyan bir defter guncellemesi imzalar

- bir operator, bir mevduatin adina lightning faturasi olusturmus olup, preimage zincirde aciklanmasina ragmen mevduati alacaklandirmamis olan bir defter guncellemesi imzalar

- kendi zincirindeki daha sonraki hash degerinden once gelen bir defter hash degerini mevcut olarak bildiren bir ortak imza

- tartismali bir defterin nisap uyesi olup aktif olan ancak belirli sayida blok icinde dolandiricilik kanitina uygun hareket etmeyen bir uye

- uyumsuz defter guncellemelerini imzalamak veya ortak imzalamak

bir dolandiricilik kaniti, kanittan ve gomulu hash degerini suclanan operatorun defterine baglayan nedensel bir zincirden olusur. zincir, her biri onceki baglantinin defterinden bir member_ledger_hash iceren ortak imzali guncellemeler dizisidir. dogrulayicilar arama yapmadan zinciri takip eder, her baglantnin imzali bir guncelleme oldugunu ve kanit hash degerinin gomulu veriyle eslesmesini dogrular

## kurtarma

bir defter erisilemez veya uyumsuz hale geldikten sonra, nisap uyeleri son uyumlu guncellemeden itibaren defterin kendi devamlarini olusturabilir. yeni bir nisap kurmali ve teminat onaylarini saglamalidilar. uyeler daha sonra onceki rezerv ciktisini potansiyel sonraki zincirlerin bir piyangosuna harcamak icin koordine olmalidir. bu piyangoyu kazanan zincirine bir edinim guncellemesi ekler ve digerler bir feragat ekler. cuzdanlar ayni deftere hitap etmeye devam eder ve yalnizca nisap tarafindan ortak imzalanan yanitlari kabul eder. cuzdanlar periyodik olarak ve beklenen ortak imzaya sahip yanitlar gelmediginde agi sorgulamali ve velayet degisikliklerini tanimlamak icin defter guncellemelerini yeniden oynatmalidir

uyumsuzluk kazara gorunduguunde (ornegin, bir defter belirli sayida blok boyunca erisilemez hale geldiginde) velayet degisikligi saygi cercevesinde olmalidir: yalnizca defterin yukumluluklerini karsilamak icin gereken rezerv miktari piyangoya gonderilir ve ustusu operatorun acik anahtarina geri gonderilir. teminat kontrolu etkilenmez

uyumsuzluk kaniti mevcut oldugunda, gerekli rezervlerin ustundeki miktar nisap uyeleri arasinda esit olarak bolunur ve uye defterlerinde tutulan teminata el konulmasina izin verilir

## ag sagligi

basit bir saldiri, gizli anlasma yapan operatorlerden adalar olusturmaktir. defterlerinde onemli yukumlulukler olusturduktan sonra, kaybedilen teminati asan fonlari calarak koordineli sekilde cikarlar. ag buna karsi savunma yapabilir, ancak ic degerin gizli anlasma yapmayan aga baglayan teminati astigi bolgelerde bu mumkun degildir. daha yuksek teminat oranlari ve daha buyuk, daha cesitli nisaplar bu ceplerin olusma olasiligini azaltir, ancak bilerek olusturulabilirler ve her cuzdanin tum agi degerlendirmesini bekleyemeyiz. bunun yerine kesfetme piyasalari, odul toplama algoritmalari gibi graf analizlerine dayanan operator hesap verebilirlik olcutleri yayinlamalidir

## sonuc

calma icin gizli anlasma gerektiren, ancak gizli anlasmanin risk altindaki teminati calancak degerden daha hizli artirdigi bir teminat agi oneriyoruz. bu agi, tam rezervlerle desteklenen kriptografik defterleri guvence altina almak icin kullaniyoruz. bu defterler, onceden muzakere edilmis ucretler karsiliginda cevrimi disi cuzdanlar adina hesaplara hizmet verir. defter temel yapilari, basit akilli sozlesmeler icin yeterli miniscript harcama kosullarini destekler. ag neredeyse dogrusal olarak olceklenir ve buyuk bir agin milyarlarca cuzdana ve geleneksel odeme aglarini asan islem hacmine hizmet vermesine olanak tanir
