# bitcoin deposits
## abstrak

versi peer-to-peer yang ideal dari uang elektronik akan memungkinkan pembayaran online dikirim langsung dari satu pihak ke pihak lain dengan cepat dan dengan persiapan minimal. lightning network menyediakan sebagian dari solusi, tetapi manfaat esensialnya hilang jika pihak ketiga yang dipercaya diperlukan untuk mengelola state atas nama Anda. kami mengusulkan solusi untuk masalah ini menggunakan buku besar yang dapat diverifikasi dan jaring jaminan. operator menyiarkan pembaruan buku besar kepada rekan-rekan mereka, menciptakan catatan akun yang dapat diaudit. dompet menyiarkan bukti ketidakjujuran kepada rekan-rekan tersebut, yang memastikan bahwa buku besar mempertahankan operator yang jujur. keluar sepihak digantikan oleh jaminan bahwa dana tetap tersedia selama jaringan masih ada. kami sampai pada sebuah jaringan yang mendelegasikan pemeliharaan likuiditas, menghindari biaya pengaturan, mampu menerima pembayaran secara offline, dan berskala secara independen dari lapisan dasar

## pendahuluan

bitcoin deposits bertujuan menyediakan dana terkendali kunci yang cepat dan skalabel, tanpa kepercayaan, di luar rantai. aktivitas on-chain berskala sesuai jumlah buku besar dan frekuensi rotasi cadangan. throughput berskala sedikit di atas linier sesuai jumlah buku besar dalam jaringan, menjadikan jutaan transaksi per detik di seluruh triliunan dompet masuk akal

ada tradeoff yang eksplisit:
- tidak ada keluar sepihak: ketika operator gagal, dana tetap di dalam jaringan
- tidak ada privasi: verifikasi membutuhkan transparansi
- ketersediaan intermiten: sebuah deposit hanya tersedia selama operatornya tersedia. dompet sebaiknya menyebarkan dana untuk meningkatkan ketersediaan

kami mengharapkan pengalaman dompet serupa dengan lapisan dasar yang cepat, memiliki ekonomi pembayaran yang mirip dengan lightning network

## buku besar

buku besar adalah rantai pembaruan yang tidak dapat diubah, berisi hash dari pembaruan sebelumnya dan ditandatangani oleh operator buku besar. jenis pembaruan yang berbeda memiliki aturan berbeda yang mengatur kapan dan bagaimana mereka dapat digunakan. buku besar bersifat deskriptif mandiri, pembaruannya tersedia secara publik dan tidak dapat disangkal, memungkinkan siapa pun untuk mengevaluasi kesesuaian

buku besar memiliki satu operator aktif, tetapi dipelihara secara kooperatif oleh mesh. operator mana pun dapat membuatnya, tetapi jika mereka menghilang atau menjadi tidak jujur, operator berbeda akan ditugaskan, beserta cadangannya. operator yang saat ini aktif diidentifikasi oleh pubkey yang digunakan untuk menandatangani pembaruan co-signed terbaru

## deposit

deposit adalah akun stabil yang dapat mengirim dan menerima dana, dikendalikan oleh miniscript. pada saat pembukaan, jadwal biaya ditetapkan, serta apakah penerimaan dana memerlukan permintaan yang ditandatangani dompet. operator harus mengizinkan transfer antar deposit pada buku besar yang sama serta keluar on-chain. mereka sebaiknya mengizinkan deposit untuk membayar invoice lightning

merupakan kebijaksanaan operator untuk membuat penawaran pendanaan on-chain atau invoice lightning atas nama deposit. jika mereka melakukannya, ini harus ditandatangani bersama oleh anggota kuorum, dan dompet harus memverifikasi tanda tangan ini. penawaran dan invoice bukan bagian dari buku besar, sehingga merupakan tanggung jawab dompet untuk memverifikasi tanda tangan dan menyimpannya sebagai bukti

## biaya

transfer antar deposit, on-chain, dan melalui lightning memiliki biaya yang dibayarkan kepada operator buku besar. ada juga biaya yang diterapkan secara berkala pada saldo dengan periode tertentu. semua dinegosiasikan saat deposit baru dibuka. biaya dapat diubah setelah jumlah blok tertentu, dengan pemberitahuan blok tertentu dan dalam batas persentase per-penyesuaian yang dinegosiasikan saat pembukaan. kuorum dapat menolak untuk menandatangani bersama pembaruan yang menciptakan keadaan tidak menguntungkan yang pada akhirnya bisa menjadi tanggung jawab mereka

## transfer

bentuk dasar transfer adalah operasi dua fase antara dua deposit pada buku besar yang sama: sebuah deposit mengajukan permintaan untuk mengirim dana. jika tersedia cukup dana, sebuah kunci pada dana dengan kondisi pembelanjaan ditambahkan ke buku besar. jika kondisi pembelanjaan terpenuhi sebelum batas waktu, dana berpindah dari pengirim ke penerima dikurangi biaya operator. jika batas waktu tercapai, kunci dilepaskan, dikurangi biaya operator yang lebih kecil. dengan kondisi pembelanjaan miniscript, ini cukup untuk memungkinkan deposit mana pun menyediakan jembatan dan layanan likuiditas kepada deposit lain pada buku besar yang sama

## lightning

operator yang memiliki channel lightning dapat mengizinkan deposit untuk mengirim dan menerima melalui lightning network. ketika deposit meminta invoice lightning, operator membuatnya melalui node lightning mereka, meminta anggota kuorum untuk menandatangani bersama sebagai bukti bahwa mereka berkomitmen untuk mengkreditkan deposit saat pembayaran diterima. dompet harus menyimpan invoice yang ditandatangani bersama ini sebagai bukti. ketika deposit meminta pembayaran invoice lightning, operator membayar menggunakan node lightning mereka dan mendebit deposit setelah memperoleh preimage

ketika pembayar dan penerima adalah deposit pada operator yang sama, operator dapat menyelesaikan secara internal tanpa merutekan melalui lightning, mengkreditkan dan mendebit deposit masing-masing secara langsung. ini menghindari biaya perutean dan mode kegagalan sambil mempertahankan jaminan akuntansi yang sama

## kurir

permintaan transfer hanya memindahkan dana antar deposit pada buku besar yang sama. untuk memindahkan dana antar buku besar, dompet menggunakan kurir — layanan yang memiliki deposit pada beberapa buku besar dan membawa transfer di antara mereka. kurir mengiklankan kapasitas dan biaya arah per-buku besar di relay. ketika dompet ingin mengirim dari buku besar A ke buku besar B, ia membuat kunci transfer ke deposit kurir dan meminta kurir membuat satu dari deposit mereka di buku besar tujuan ke penerima. setelah kedua kunci terbentuk, dompet mengungkapkan preimage kepada penerima, yang menyelesaikan transfer dari kurir. setelah terungkap, kurir menggunakan preimage yang sama untuk menyelesaikan transfer dari pengirim ke kurir

ini adalah pola hash time-locked contract standar. kami mengharapkan batas waktu keluar kurir secara ketat lebih awal dari batas waktu masuk, memastikan bahwa jika dompet tidak pernah mengungkapkan, kedua kunci kedaluwarsa dan tidak ada pihak yang kehilangan dana. tidak diperlukan kepercayaan di luar jaminan batas waktu yang ditegakkan oleh operator

kurir harus menetapkan biaya per-buku besar: fee_in dan fee_out untuk setiap buku besar yang mereka layani. dompet memperkirakan biaya rute sebagai fee_out pada sumber ditambah fee_in pada tujuan. kurir dapat memvariasikan biaya berdasarkan buku besar sesuai likuiditas yang tersedia, secara alami menyeimbangkan kembali posisi mereka. dompet menemukan kurir melalui iklan mereka di relay dan memilih berdasarkan biaya, kapasitas, atau cakupan

## komunikasi

semua komunikasi antara dompet dan operator, dan antar operator, menggunakan relay nostr. pembaruan buku besar diterbitkan sebagai event tahan lama yang disimpan relay, menciptakan catatan permanen yang dapat diaudit. permintaan dan respons antara dompet dan operator adalah event sementara dengan TTL relay yang pendek. operator mengiklankan ketentuan mereka sebagai event yang dapat diganti, memungkinkan dompet menemukan dan membandingkan operator tanpa direktori terpusat

arsitektur ini berarti dompet tidak memerlukan koneksi persisten -- mereka dapat offline tanpa batas waktu dan mengejar ketertinggalan dengan memutar ulang event dari relay mana pun yang memilikinya. operator dapat dijangkau melalui relay mana pun yang mereka pantau, dan pilihan relay adalah keputusan deployment, bukan batasan protokol

## cadangan dan jaminan

cadangan disimpan dalam utxo dengan jumlah lebih besar dari atau sama dengan jumlah kewajiban buku besar, dapat dibelanjakan oleh mayoritas kuorum, dengan fallback ke operator setelah periode yang signifikan

jaminan adalah modal milik operator sendiri, didepositkan dan dikunci pada buku besar anggota kuorum. setiap anggota memiliki deposit jaminan yang didanai dan dikunci operator untuk durasi tertentu. total kewajiban buku besar dibatasi hingga dua kali kunci jaminan terkecil yang dimiliki oleh anggota mana pun, dan durasi kuorum dibatasi oleh waktu kunci terpendek. ini memastikan bahwa jaring jaminan selalu memiliki cukup dukungan untuk menutupi transfer hak asuh. deposit jaminan yang sama dapat mendukung beberapa buku besar untuk meningkatkan efisiensi modal, meskipun dompet sebaiknya memilih operator dengan sumber jaminan yang tidak tumpang tindih

kewajiban ditegakkan saat membuat penawaran pendanaan atau invoice baru. operator tidak dapat membuat penawaran atau invoice yang akan mendorong total kewajiban buku besar di atas cadangan atau di atas dua kali kunci jaminan terkecil, mana pun yang lebih rendah

## kuorum

operator meminta operator lain untuk bergabung dengan kuorum mereka dengan mendepositkan dan mengunci jaminan pada buku besar anggota. permintaan tersebut mencakup komitmen jaminan (jumlah dan durasi kunci) dan ketentuan anggota: jadwal biaya minimum yang harus dipenuhi deposit pada buku besar. setiap anggota harus mengoperasikan buku besar mereka sendiri dan dapat menyita jaminan operator jika operator terbukti tidak sesuai. anggota menentukan batas pada jadwal biaya selama keanggotaan kuorum mereka -- operator tidak dapat membuka deposit dengan biaya di bawah minimum anggota yang paling ketat, melindungi anggota dari mewarisi kewajiban yang tidak menguntungkan setelah transfer hak asuh

setelah kuorum terbentuk, cadangan dirotasi ke utxo multisig baru. anggota menandatangani bersama pembaruan yang valid dan berpartisipasi dalam pemulihan jika operator menandatangani yang tidak sesuai. kuorum yang lebih besar meningkatkan overhead komunikasi tetapi mengurangi risiko operator, meningkatkan ketersediaan, dan membuat kolusi lebih sulit dan mahal. dompet sebaiknya memilih kuorum yang lebih besar

## pencegahan ekonomi

protokol menggantikan keluar sepihak dengan pencegahan ekonomi. anggota kuorum secara langsung diberi insentif untuk bertindak melawan ketidakjujuran. selama operasi normal mereka mendapatkan biaya modest atas jaminan, tetapi dalam hal perilaku yang terbukti tidak sesuai, mereka berpotensi menyita seluruh deposit jaminan operator pada buku besar mereka

ketika dompet mencurigai penyensoran, ia dapat mengeskalasi permintaan ke anggota kuorum melalui pengiriman bersertifikat. anggota menyematkan hash permintaan di buku besar mereka sendiri dengan biaya kecil, menciptakan bukti yang berlabuh secara kausal. jika operator gagal memproses permintaan, anggota memiliki bukti dan insentif ekonomi untuk memulai sengketa

penipuan invoice lightning mengikuti pola pencegahan yang sama. operator mengetahui apakah preimage diterima, tetapi dompet tidak. namun pembayar mana pun mungkin memberikan preimage kepada dompet. satu pencurian yang terkonfirmasi memicu sengketa, penyitaan cadangan, dan penyitaan jaminan. imbalan mencuri satu pembayaran terbatas, tetapi risikonya eksistensial, menjadikan pencurian lightning tidak rasional secara ekonomi meskipun secara formal tidak dapat dibuktikan tanpa kerja sama pihak ketiga

mode kegagalan untuk pencegahan penyensoran dan lightning adalah kolusi kuorum secara bulat. protokol tidak dapat melindungi terhadap kuorum yang bekerja sama untuk mencuri, tetapi jaring jaminan memastikan bahwa kolusi lebih mahal daripada keuntungannya. transparansi jaringan memungkinkan dompet dan pasar penemuan untuk mengidentifikasi struktur kuorum yang mencurigakan sebelum mendepositkan dana

## waktu

waktu absolut diukur terhadap lapisan dasar. toleransi tidak boleh melebihi jumlah konfirmasi yang wajar untuk menjaga stabilitas selama reorganisasi rantai

di mana toleransi yang lebih tinggi diperlukan, kita mengandalkan pengurutan kausal. buku besar kriptografi adalah rantai merkle. setiap pembaruan membuktikan bahwa ia dibuat setelah semua pembaruan sebelumnya, tetapi tidak memberikan jaminan tentang informasi di luar rantai. untuk membangun pengurutan terdistribusi, kita mengharuskan co-signature menyertakan hash pembaruan terbaru dari buku besar co-signer. hash tersebut kemudian dimasukkan ke dalam hash pembaruan saat ini, menjadi bagian dari rantai serta bagian dari semua rantai lain yang ditandatangani bersama oleh operator buku besar, menciptakan jaring kausalitas. ini tidak mampu membuktikan waktu secara eksplisit, tetapi mampu membuktikan bahwa potongan informasi tertentu dibuat dalam urutan tertentu

## bukti penipuan

kita dapat membuktikan berbagai jenis penipuan dengan mengungkap informasi yang telah dibuat dalam urutan yang salah. di mana informasi tidak disertakan oleh operasi jaringan normal, ia dapat diselundupkan dengan membuat aktivitas yang menyertakan hash dari bukti. setelah dimasukkan ke dalam pembaruan yang ditandatangani oleh operator, bukti terungkap sebagai telah dibuat di tempat yang tidak sesuai dalam pengurutan:

- operator, setelah menawarkan untuk mengkreditkan deposit dengan dana yang dikirim on-chain ke alamat tertentu, menandatangani pembaruan buku besar yang tidak berisi kredit yang sesuai, tetapi berisi rantai yang mengungkapkan beberapa hash blok yang melebihi jumlah konfirmasi yang diizinkan sebelum kredit

- operator, setelah membuat invoice lightning atas nama deposit, menandatangani pembaruan buku besar yang belum mengkreditkan deposit meskipun preimage telah terungkap dalam rantai

- co-signature yang mendeklarasikan hash buku besar saat ini sebagai yang mendahului hash mereka sendiri yang lebih kemudian dalam rantai

- anggota kuorum dari buku besar yang disengketakan yang aktif tetapi tidak bertindak sesuai dengan bukti penipuan dalam sejumlah blok

- menandatangani atau menandatangani bersama pembaruan buku besar yang tidak sesuai

bukti penipuan terdiri dari bukti dan rantai kausal yang menghubungkan hash yang disematkan ke buku besar operator yang dituduh. rantai tersebut adalah urutan pembaruan yang ditandatangani bersama, masing-masing menyertakan member_ledger_hash dari buku besar tautan sebelumnya. verifier menelusuri rantai tanpa pencarian, mengonfirmasi setiap tautan adalah pembaruan yang ditandatangani, dan bahwa hash bukti cocok dengan data yang disematkan

## pemulihan

setelah buku besar menjadi tidak tersedia atau tidak sesuai, anggota kuorum dapat membuat kelanjutan mereka sendiri dari buku besar dari pembaruan sesuai terakhir. mereka harus membentuk kuorum baru dan memberikan atestasi jaminan. anggota kemudian harus berkoordinasi untuk membelanjakan output cadangan sebelumnya ke lotere dari potensi rantai berikutnya. pemenang lotere ini menambahkan pembaruan akuisisi ke rantai mereka, dan yang lain menambahkan penyerahan. dompet terus menuju buku besar yang sama, hanya menerima balasan yang ditandatangani bersama oleh kuorum. secara berkala, dan ketika tidak ada balasan yang memiliki co-signature yang diharapkan, dompet harus meminta jaringan dan memutar ulang pembaruan buku besar untuk mengidentifikasi perubahan hak asuh

ketika ketidaksesuaian tampak tidak disengaja (mis., buku besar tidak tersedia selama sejumlah blok tertentu) perubahan hak asuh harus menghormati: hanya jumlah cadangan yang diperlukan untuk menutupi kewajiban buku besar yang dikirim ke lotere, dan kembalian dikirim kembali ke pubkey operator. kendali atas jaminan tidak terpengaruh

ketika bukti ketidaksesuaian ada, jumlah yang melebihi cadangan yang diperlukan dibagi rata di antara anggota kuorum, dan jaminan yang disimpan di buku besar anggota diizinkan untuk disita

## kesehatan jaringan

satu serangan yang mudah dipahami adalah membentuk pulau-pulau operator yang berkolusi. setelah membangun kewajiban substansial di seluruh buku besar mereka, mereka berkoordinasi untuk keluar, mencuri dana yang melebihi jaminan yang hilang. jaringan dapat bertahan melawan ini, kecuali di wilayah di mana nilai internal melebihi jaminan yang menghubungkannya ke jaringan yang tidak berkolusi. rasio jaminan yang lebih tinggi dan kuorum yang lebih besar dan lebih beragam mengurangi kemungkinan kantong-kantong ini terbentuk, tetapi mereka dapat terbentuk dengan sengaja dan kita tidak dapat mengharapkan setiap dompet untuk mengevaluasi seluruh jaringan. sebagai gantinya, pasar penemuan harus menerbitkan metrik akuntabilitas operator berdasarkan analisis graf seperti algoritma prize-collecting

## kesimpulan

kami mengusulkan jaringan jaminan yang memerlukan kolusi untuk mencuri, tetapi kolusi meningkatkan jaminan yang berisiko lebih cepat daripada meningkatkan nilai yang akan dicuri. kami menggunakan jaringan ini untuk mengamankan buku besar kriptografi yang didukung oleh cadangan penuh. buku besar ini melayani akun atas nama dompet offline sebagai imbalan atas biaya yang telah dinegosiasikan sebelumnya. primitif buku besar mendukung kondisi pembelanjaan miniscript yang cukup untuk kontrak pintar dasar. jaringan berskala mendekati linier, memungkinkan jaringan besar menyediakan miliaran dompet dan volume transaksi yang melebihi jaringan pembayaran tradisional
