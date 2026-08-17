# Türkiye ikinci el araç fiyat verisinin programatik olarak elde edilmesi: kaynak araştırması

Bu belge, `arac_puanlama` projesinin fiyat bantlarını tarih damgalı ve savunulabilir bir
temele oturtabilmesi için hangi veri kaynaklarının gerçekten kullanılabilir olduğunu
araştırır. Projenin ihtiyacı somuttur: marka, model, motor ve şanzıman kırılımında,
ikinci el otomatik vitesli araçlar için P25, medyan ve P75 değerleri.

## Bu araştırmanın yöntemi ve sınırı

Araştırma, ağ çıkışının kısıtlı olduğu bir ortamda yapıldı. Bu ortamda `arabam.com`,
`sahibinden.com`, `kaggle.com`, `tsb.org.tr` ve hatta `wikipedia.org` gibi alan adlarına
doğrudan sayfa isteği atılamıyor; yalnızca arama motoru sonuç özetleri ve GitHub'ın kendi
arama API'si çalışıyor. Bunun doğrudan sonucu şudur: aşağıdaki bulguların bir kısmı arama
sonucu özetlerinden derlendi ve **sayfanın kendisi görülerek doğrulanmadı.** Hangi bilginin
doğrudan API'den geldiği, hangisinin arama özetinden derlendiği her başlıkta ayrıca
belirtildi. Kullanıcı bu adresleri kendi makinesinde açtığında sütun adları ve satır
sayıları gibi ayrıntıların doğrulanması gerekir.

Bu belge kod içermez ve bilerek içermiyor. Araştırmanın amacı, bir sitenin bot korumasını
aşmanın yolunu bulmak değil, **hukuken ve etik olarak temiz olan yolu bulmaktır.**

---

## 1. Hazır kamuya açık veri setleri

Türkiye ikinci el araç ilanlarından türetilmiş, indirilebilir veri setleri gerçekten
mevcuttur ve bunların çoğu Kaggle üzerinde toplanmıştır. Aşağıdaki tablo bulunan setleri
özetler; tablodan sonra her birinin projeye ne kadar uyduğu ayrıca değerlendirilmiştir.

| Veri seti | Adres | Dönem | Not |
|---|---|---|---|
| Turkey Car Market 2020 | `kaggle.com/datasets/alpertemel/turkey-car-market-2020` | 2020'nin ilk iki çeyreği | En çok atıf alan set. |
| Car Sale Dataset (2021) arabam.com | `kaggle.com/datasets/mertulas/car-sale-dataset-2021-arabamcom` | Şubat 2021 | Kaynağı açıkça arabam.com. |
| Used Car Prices Dataset (Turkey - arabam.com) | `kaggle.com/datasets/mehmettanriverdi/used-car-prices-dataset-turkey-arabam-com` | Belirsiz | Kaynağı açıkça arabam.com. |
| Turkey Used Car Prices - August 2025 | `kaggle.com/datasets/oguzarar/turkey-used-car-prices-august-2025` | Ağustos 2025 | Bulunan en güncel set. |
| Used Car Prices in Türkiye 2025 (EN/TR) | `kaggle.com/datasets/bahridgr/used-car-prices-in-trkiye-2025-entr` | 2025 | Sütun adları hem İngilizce hem Türkçe. |
| Car Sales | `kaggle.com/datasets/sametevik/car-sales` | Belirsiz | Arama özetine göre arabam.com'dan kazınmış. |

Bu setler arasında projenin ihtiyacına yapısal olarak en yakın olanı **Turkey Car Market
2020**'dir, çünkü arama sonuçlarından ve bu seti kullanan akademik çalışmalardan
anlaşıldığı kadarıyla bu set marka, model, model yılı, **vites tipi**, yakıt tipi, **motor
hacmi**, kilometre ve fiyat alanlarını ayrı sütunlar halinde taşır. Projenin istediği
marka artı model artı motor artı şanzıman kırılımı tam olarak bu alanlarla kurulabilir ve
ilan seviyesinde satırlar bulunduğu için P25, medyan ve P75 doğrudan hesaplanabilir.
Buna karşılık verinin 2020'nin ilk yarısına ait olması ciddi bir sorundur: aradan geçen
sürede Türk lirasının satın alma gücü ve ikinci el araç fiyatları o kadar değişti ki bu
seti mutlak fiyat kaynağı olarak kullanmak mümkün değildir.

Daha güncel olan **Turkey Used Car Prices - August 2025** seti, tarih olarak projeye çok
daha yakındır. Ancak bu setin sütun yapısı ve satır sayısı bu ortamdan doğrulanamadı;
Kaggle sayfası açılamadığı için sütun listesi ve lisans bilgisi görülemedi. Kullanıcının
ilk yapması gereken işlerden biri bu sayfayı açıp setin şanzıman ve motor hacmi sütunları
taşıyıp taşımadığını kontrol etmektir, çünkü bu iki sütun yoksa set projenin kırılımını
besleyemez.

Hugging Face tarafında Türkiye ikinci el araç fiyatlarına ait bir veri seti bulunamadı.
Hugging Face üzerindeki Türkçe veri setleri metin ve duygu analizi ağırlıklıdır. Zenodo ve
Figshare aramaları da bu konuda bir sonuç vermedi. `data.gov.tr` benzeri kamu açık veri
portallarında araç fiyatı içeren bir veri seti bulunamadı; kamu tarafındaki veri, fiyat
değil tescil ve devir sayısı üzerinedir ve bu ayrım aşağıda üçüncü başlıkta ele alınıyor.

Akademik tarafta, DergiPark ve ResearchGate üzerinde Türkiye ikinci el araç fiyat tahmini
konusunda birden çok makale bulunmaktadır. Bunlar arasında Niğde Ömer Halisdemir
Üniversitesi Mühendislik Bilimleri Dergisi'nde yayımlanan karşılaştırmalı makine öğrenmesi
çalışması ve "Türkiye'de ikinci el araçların büyük veri ve makine öğrenme teknikleriyle
analizi ve fiyat tahmini" başlıklı çalışma dikkat çekicidir. Bu makalelerin çoğu veri
setini kendisi kazımıştır ve veriyi yayımlamamıştır; dolayısıyla makaleler metodoloji
açısından değerli, veri kaynağı olarak ise kullanılamaz durumdadır.

**Lisans konusunda önemli bir uyarı gereklidir.** Bu Kaggle setlerinin lisans bilgisi bu
ortamdan görülemedi, ancak lisans alanında ne yazarsa yazsın altta yatan gerçek şudur:
setlerin neredeyse tamamı `arabam.com` veya `sahibinden.com` içeriğinin izinsiz
kazınmasıyla üretilmiştir. Bir veri setini yükleyen kişinin ona "CC0" etiketi vermesi, o
verinin kaynak sitenin kullanım koşullarına aykırı biçimde toplandığı gerçeğini
değiştirmez. Bu yüzden bu setler aşağıdaki sıralamada birinci değil, ikinci gruba
yerleştirildi.

---

## 2. Mevcut açık kaynak kazıyıcılar

Bu başlıktaki bulgular GitHub'ın kendi arama API'si üzerinden alındığı için doğrudan ve
güvenilirdir; yıldız sayıları ve son güncelleme tarihleri gerçek değerlerdir.

`arabam.com` hedefleyen depolar sayıca azdır ve hiçbiri olgun bir proje değildir. En
dikkat çekici olanları şunlardır. `ridvansevik/arabam-com-scraper` Python, Selenium ve
BeautifulSoup kullanır, CSV üretir ve basit bir arayüzü vardır; son güncellemesi Temmuz
2026'dır ancak yalnızca bir yıldızı vardır. `vahitustaoglu/arabam.com-web-scraper`
sitedeki tüm otomobil ilanlarını yerel diske çekip veri seti oluşturmayı hedefler ve
Haziran 2026'da güncellenmiştir. `yasintsc99/ARABAM.COM-SCRAPER` Python ile yazılmıştır ve
iki yıldızı vardır. `hbaklan943/arabam.com-scraper` ise Node.js ile yazılmış olup araçları
fiyat, yıl ve kilometreye göre puanlayıp CSV kaydeder; bu depo 2023'ten beri
güncellenmemiştir ve bu projeye kavramsal olarak en yakın olanıdır.

`sahibinden.com` tarafında depo sayısı çok daha fazladır; arama kırk beş depo döndürdü.
En popüler olanı yirmi yedi yıldızlı `0Baris/sahibinden-scraper`'dır ve Python ile
Selenium kullanır. Ancak bu deponun açık sorunları vardır ve `sahibinden.com` tarafındaki
depoların büyük çoğunluğu emlak ilanlarına odaklanmıştır, araç ilanlarına değil.

Bu depoların hepsi hakkında geçerli olan ve tek tek incelemeye gerek bırakmayan bir gözlem
vardır: **bunların neredeyse tamamı Selenium veya benzeri bir tarayıcı otomasyonu
kullanır.** Bu, sitenin basit HTTP istekleriyle veri vermediğinin, yani bir bot korumasının
devrede olduğunun doğrudan göstergesidir. Nitekim bir depo, açıklamasında "anti-bot
sistemlerini atlatabilen" ifadesini açıkça kullanmaktadır. Bu tür bir yazılımı çalıştırmak,
aşağıda beşinci başlıkta anlatılan kullanım koşulu ihlallerini doğrudan üstlenmek anlamına
gelir.

Ayrıca **kasko değer listesini işleyen tek bir açık kaynak depo bulunamadı.** GitHub'da
hem `kasko deger listesi` depo araması hem de `tsb.org.tr kasko` kod araması sıfır sonuç
verdi. Bu, aşağıda önerilen birinci seçeneğin hazır bir çözümünün olmadığını, yani
kullanıcının bu işi ilk yapan kişi olacağını gösterir. Bu bir dezavantaj gibi görünse de
aslında projenin lehinedir, çünkü ortada taklit edilecek ve hukuken şüpheli bir emsal
yoktur.

---

## 3. Resmî ve yarı resmî istatistik kaynakları

Bu başlık, araştırmanın en önemli bulgusunu içerir.

### 3.1. TSB Kasko Değer Listesi — en güçlü aday

Türkiye Sigorta, Reasürans ve Emeklilik Şirketleri Birliği, kısa adıyla TSB, **Kasko Değer
Listesi** adında bir belgeyi düzenli olarak yayımlar. Bu liste, sigorta şirketlerinin
sigortaladıkları motorlu taşıtların değerini belirlerken kullanmak zorunda oldukları resmî
referanstır ve piyasa fiyatları esas alınarak hazırlanır.

Bu listenin projeye uygunluğu birkaç açıdan dikkat çekicidir. Listenin satırları yalnızca
marka ve model yılı ile değil, **motor hacmi, yakıt tipi ve vites türü** ile birlikte
tanımlanır; her satır bir TSB marka kodu ve bir TSB tip kodu ile eşleştirilir. Yani
listenin kırılımı, projenin ihtiyaç duyduğu marka artı model artı motor artı şanzıman
kırılımıyla neredeyse birebir örtüşür. Liste ayda bir güncellenir ve piyasa koşulları
gerektirdiğinde ay içinde birden fazla kez güncellendiği belirtilmektedir. Liste, on beş
model yılına kadar geriye giden araçları kapsar ve binek otomobil, arazi taşıtı ile hafif
ticari araçları içerir.

TSB ayrıca **gün bazlı arşivi** erişime açmıştır. Bu, projenin "tarih damgası" ihtiyacı
açısından kritik bir imkândır: bir aracın belirli bir tarihteki resmî değeri geriye dönük
olarak sorgulanabilir ve kaynak gösterilebilir. İlgili adresler `tsb.org.tr/tr/kasko-deger-listesi`
ve `tsb.org.tr/tr/kasko-arsiv-listesi`'dir.

Bu kaynağın hukuki durumu temizdir. Liste kamuya açık olarak sunulur ve yalnızca sigorta
şirketleriyle sınırlı değildir; nitekim Allianz, Axa, Doğa Sigorta, Türkiye Sigorta, Quick
Sigorta ve HDI Sigorta gibi çok sayıda şirket ile Koalay, sigortam.net ve enuygunsigorta
gibi karşılaştırma siteleri bu listeyi kendi sayfalarında sorgulanabilir hale
getirmektedir. Bu kadar yaygın bir yeniden kullanım, verinin fiilen kamusal referans
niteliği taşıdığını gösterir.

**Ancak bu kaynağın iki gerçek sınırı vardır ve bunlar açıkça yazılmalıdır.** Birincisi,
kasko değeri bir *dağılım* değil *tek bir referans değerdir*; her tip kodu ve model yılı
için tek bir sayı verir. Dolayısıyla bu listeden doğrudan P25, medyan ve P75 üretilemez.
İkincisi, kasko değeri bir sigorta referans bedelidir ve piyasadaki ilan fiyatlarıyla
birebir aynı değildir; genellikle ilan fiyatlarının altında kalır, çünkü ilan fiyatı bir
satıcı talebi, kasko değeri ise bir tazminat tavanıdır. Bu iki sınırın pratikteki anlamı
şudur: kasko listesi, fiyat bandının **çapası** olarak kullanılmalı, bandın kendisi olarak
değil. Yani listeden gelen resmî değer merkez noktası kabul edilip, bandın genişliği
başka bir kaynaktan gelen dağılım bilgisiyle kalibre edilmelidir.

Bu listenin dosya formatı bu ortamdan doğrulanamadı. Arama sonuçları bir yerde PDF, bir
yerde Excel biçiminden söz etmektedir ve TSB sitesi açılamadığı için hangisinin doğru
olduğu belirlenemedi. Kullanıcının ilk kontrol etmesi gereken teknik nokta budur; sayfanın
bir sorgu arayüzü mü yoksa toplu indirilebilir bir dosya mı sunduğu, işin zorluğunu
tamamen belirler.

### 3.2. TÜİK

Türkiye İstatistik Kurumu, **Motorlu Kara Taşıtları** başlıklı aylık bülteni düzenli
olarak yayımlar ve bu bültenler `data.tuik.gov.tr` ile `veriportali.tuik.gov.tr`
üzerinden serbestçe erişilebilir. Ancak bu bültenler **fiyat değil adet verisi** içerir:
kaç aracın trafiğe kaydedildiğini ve kaç aracın el değiştirdiğini bildirir. Örneğin bir
ayda gerçekleşen 870.992 taşıt devri bilgisi bu bültenlerden gelir. Bu veri, pazarın
hacmini anlatmak için değerlidir ve projenin belgelerinde bağlam olarak kullanılabilir,
ancak model bazında fiyat üretmez. TÜİK'in ikinci el araç için model kırılımlı bir fiyat
endeksi yayımladığına dair bir kanıt bulunamadı.

### 3.3. ODMD ve OYDER

Otomotiv Distribütörleri ve Mobilite Derneği, `odmd.org.tr` üzerinden **İkinci El Online
Sektör Raporu** ve **İlanlar Sektör Raporu** başlıklı düzenli raporlar yayımlamaktadır.
Bu raporlar ücretsiz erişilebilir ve alıntılanabilir niteliktedir. Ancak içerikleri pazar
düzeyinde toplulaştırılmıştır; marka ve model bazında dağılım vermezler. Ayrıca bu
raporların bir kısmının INDICATA verisiyle hazırlandığı görülmektedir, ki bu da aşağıdaki
ticari kaynak başlığına bağlanır. OYDER de `oyder-tr.org` üzerinden TÜİK ve ODMD
verilerini derleyen raporlar yayımlar.

### 3.4. arabam.com'un kendi yayımladığı aylık endeks

Burada gözden kaçması kolay ama önemli bir ayrım vardır. `arabam.com` sitesini kazımak
kullanım koşullarına aykırıdır, ancak **arabam.com'un kendi isteğiyle basına dağıttığı
aylık fiyat endeksi tamamen kamusal ve alıntılanabilir bir kaynaktır.** Şirket her ay
"arabam.com Aylık Fiyat Endeksi" adı altında ortalama ilan fiyatını ve enflasyondan
arındırılmış reel değişimi açıklamakta, bu veriler Anadolu Ajansı ve diğer haber
kaynaklarınca yayımlanmaktadır. Örnek olarak, bu endekse göre ortalama ilan fiyatının
nisanda 912.045 lira, mayısta 913.190 lira, haziranda 914.918 lira ve temmuzda 917.614
lira olduğu açıklanmıştır.

Bu veri model kırılımı içermez, ancak projeye çok işe yarar bir hizmet sunar: **fiyat
bantlarının zaman içinde güncellenmesi için resmî ve ücretsiz bir düzeltme katsayısı.**
Bir kez model bazında bant kurulduktan sonra, bu endeksin aylık değişim oranı bantları
taşımak için kullanılabilir ve bunun için hiçbir siteyi kazımak gerekmez.

---

## 4. Ticari API'ler ve veri sağlayıcılar

Türkiye'de araç değerleme verisini ticari olarak satan aktörler mevcuttur ve bunlar
hukuken en temiz, ancak maliyeti en yüksek seçenektir.

**INDICATA**, Autorola grubuna bağlıdır ve `indicata.com.tr` üzerinden ürün paketleri
sunar. Türkiye'deki çevrim içi ikinci el pazarında kırk binden fazla kurumsal satıcının
hareketini gerçek zamanlı izlediğini, güncel değerleme ve gelecek değer tahmini sunduğunu
belirtmektedir. Bu, projenin ihtiyacına en yakın ticari üründür. **Autovista Group ve
Eurotax**, JD Power bünyesindedir ve Türkiye'de on bir yıldır faaliyet göstermektedir;
`AutovistaVALUATION` ürünü Eurotax, Glass's ve Schwacke verisini birleştirir. Her iki
sağlayıcı da fiyatlarını kamuya açık olarak yayımlamamaktadır ve kurumsal satış üzerinden
çalışırlar; bu da açık kaynaklı bir kişisel proje için pratikte erişilemez oldukları
anlamına gelir.

Bunların yanında `otoendeks.com`, `otodegeri.com`, `masscars.com.tr`, `tanoto2.com.tr` ve
`vava.cars` gibi tüketiciye dönük ücretsiz değerleme siteleri vardır. Bunlar tek tek araç
için değer üretir, toplu veri veya belgelenmiş bir API sunmazlar; dolayısıyla programatik
kullanım için uygun değildirler.

**Apify pazar yerindeki aktörler ayrı bir değerlendirmeyi hak eder.** `fatihtahta/arabam-com-scraper`
adlı aktör bin sonuç başına 6 dolar fiyatla satılmaktadır ve `seralifatih/turkish-automotive-intelligence-suite`
ile `stealth_mode/arabam-cars-search-scraper` gibi benzerleri vardır. Bunlar başlık, marka,
model, yıl, fiyat, kilometre, yakıt tipi, **vites**, şehir ve satıcı tipi alanlarını
döndürdüklerini iddia ederler; yani projenin istediği kırılımı verirler. Ancak bu
aktörlerin tanıtım metinlerinde açıkça "gelişmiş Cloudflare atlatma ve oturum çerezi
desteği" ifadesi geçmektedir. **Bir hizmetin para karşılığı satılıyor olması, o hizmetin
yaptığı işi meşrulaştırmaz.** Bu aktörler, `arabam.com`'un kullanım koşullarının açıkça
yasakladığı işi kullanıcı adına yapmaktadır ve satın alan taraf bu ihlalin sorumluluğundan
kurtulmaz. Bu yüzden bu seçenek aşağıda "uygun olmayan" grubuna yerleştirildi.

---

## 5. Uygulamacıların deneyimi ve hukuki çerçeve

Bu başlık, yukarıdaki seçeneklerin neden bu sıraya konduğunu açıklar.

### 5.1. Sitelerin kullanım koşulları

`sahibinden.com` kullanım koşulları konuyu tereddüde yer bırakmayacak biçimde
düzenlemiştir. Sözleşme metni, "otomatik program, robot, örümcek, tarayıcı, veri
madenciliği, veri taraması ve ekran kazıma yazılımları veya sistemleri, algoritma, yapay
zekâ uygulamaları, otomatik aletler ya da manuel süreçler" kullanılmasını yasaklamaktadır.
Metin ayrıca, sitenin açık ve yazılı izni olmadan portal içeriğinin **yapay zekâ
modellerini, büyük dil modelleri dahil, eğitmek, geliştirmek veya test etmek amacıyla**
kullanılamayacağını ayrıca hükme bağlamıştır. Site, ihlal tespiti halinde kullanıcıyı
yetkili makamlara bildirme hakkını saklı tutmaktadır.

`arabam.com` üyelik sözleşmesi de benzer bir yasak içerir ve otomatik programları,
robotları, tarayıcıları, veri madenciliğini, ekran kazıma yazılımlarını ve API protokollerini
kırma ya da API anahtar ve parametrelerine yetkisiz erişme girişimlerini açıkça
yasaklamaktadır.

Türk hukuku açısından bu yasakların dayanağı yalnızca sözleşme değildir. Konuyla ilgili
hukuk yazısında, veri tabanlarının kendine özgü korumadan yararlandığı ve web kazımanın
fikri mülkiyet ihlali doğurabileceği ele alınmaktadır. Yani "veri zaten herkese açık"
savunması Türk hukukunda da güvenilir bir savunma değildir.

### 5.2. Teknik engeller

Uygulamacıların anlattıkları, hukuki tablonun teknik karşılığını doğrular. `arabam.com`
Cloudflare koruması altındadır ve giriş duvarı uygulamaktadır. GitHub'daki depoların
istisnasız Selenium gibi tam tarayıcı otomasyonuna başvurmuş olması da bunun kanıtıdır;
basit bir HTTP isteği veri döndürseydi kimse tarayıcı sürmezdi. `sahibinden.com` benzer
biçimde korunmaktadır ve ayrıca oturum açma zorunluluğu getirmektedir, ki bu durumda
kazıma işlemi kullanıcının kendi hesabıyla yaptığı bir sözleşme ihlali haline gelir.

Bu engelleri aşmanın teknik yolları internette bolca anlatılmaktadır. **Bu belge bu
yolları ne aktarır ne de önerir.** Bir korumanın aşılabilir olması, aşılmasının meşru
olduğu anlamına gelmez ve bu proje açık kaynak bir ürün olarak konumlandığı için ilk
hukuki şikâyette savunulamayacak bir temele oturtulamaz.

---

## 6. Sıralı öneri: en gerçekçi üç seçenek

Aşağıdaki sıralama, hukuki temizlik ile pratik uygulanabilirliğin birlikte
değerlendirilmesiyle oluşturuldu.

### Birinci sıra: TSB Kasko Değer Listesini çapa olarak kullanmak

Bu seçenek, hukuken tartışmasız temiz olan ve projenin ihtiyaç duyduğu kırılımı gerçekten
taşıyan tek kaynaktır. Liste marka, tip, motor hacmi, yakıt ve vites ayrımını zaten
yapmaktadır, ayda bir güncellenmektedir ve gün bazlı arşivi sayesinde her değere bir
tarih damgası ve kalıcı bir kaynak referansı verilebilir. Projenin `docs/` katmanındaki
"kanıt puandan ayrı saklanır" ilkesiyle bu kaynak mükemmel uyumludur, çünkü her fiyat
bandının altına "TSB Kasko Değer Listesi, şu tarih, şu tip kodu" biçiminde bir alıntı
konulabilir.

Bu seçeneğin bedeli, listenin tek bir değer vermesi ve dolayısıyla P25 ile P75'in doğrudan
elde edilememesidir. Pratik çözüm, kasko değerini medyanın çapası kabul edip bant
genişliğini ayrı bir kalibrasyonla belirlemektir. Ayrıca hazır bir ayrıştırıcı bulunmadığı
için listeyi okuma işi sıfırdan yazılacaktır ve dosya formatının PDF mi Excel mi olduğu
önce doğrulanmalıdır.

### İkinci sıra: Mevcut Kaggle veri setinden bant *şeklini* öğrenip TSB ile ölçeklemek

Bu, birinci seçeneğin eksiğini kapatan tamamlayıcı adımdır. Kaggle setlerinden biri ilan
seviyesinde satırlar taşıdığı için, her marka, model, motor ve şanzıman grubu içinde
P25/medyan ve P75/medyan **oranları** hesaplanabilir. Bu oranlar, mutlak fiyatların aksine
zaman içinde çok daha kararlıdır; bir Egea otomatiğin fiyat dağılımının medyana göre ne
kadar geniş olduğu, liranın değerinden büyük ölçüde bağımsızdır. Bu oranlar TSB'den gelen
güncel çapa değerle çarpılarak güncel ve savunulabilir bir bant üretilebilir.

Bu seçeneğin bedeli hukuki gölgedir: bu setlerin kaynağı büyük olasılıkla izinsiz
kazımadır. Bu gölge, verinin **mutlak fiyat için değil yalnızca dağılım şekli için**
kullanılmasıyla ve kaynağının belgelerde açıkça belirtilmesiyle önemli ölçüde
hafifletilebilir, ancak tamamen ortadan kalkmaz. Projenin bu seti kullanmaya karar vermesi
halinde, kararın gerekçesi `docs/ARCHITECTURE.md` içine yazılmalıdır.

### Üçüncü sıra: arabam.com aylık fiyat endeksiyle bantları zaman içinde taşımak

Bu seçenek tek başına bant üretmez, ancak yukarıdaki ikisini tamamlar ve maliyeti sıfırdır.
Şirketin kendi basın bültenleriyle yayımladığı aylık endeks tamamen kamusaldır ve haber
ajanslarından alıntılanabilir. Bir kez kurulmuş bantlar, bu endeksin aylık değişimiyle
güncellenerek tarih damgası taze tutulabilir. Bu, projeye her ay yeniden veri toplama yükü
getirmeden bantların bayatlamasını önler.

---

## 7. Uygulanabilir olmayan seçenekler ve gerekçeleri

Aşağıdaki yollar araştırıldı ve bilinçli olarak elendi. Elenme gerekçelerinin yazılması,
bu kararların altı ay sonra gereksiz yere yeniden tartışılmasını önlemek içindir.

**Siteleri doğrudan kazımak uygulanabilir değildir.** Hem `sahibinden.com` hem
`arabam.com` kullanım koşulları otomatik veri toplamayı açıkça yasaklamaktadır ve
`sahibinden.com` ayrıca içeriğinin yapay zekâ modeli eğitiminde kullanılmasını da yasak
kapsamına almıştır. Bu, açık kaynak ve ileride ticarileşmesi düşünülen bir ürün için
kabul edilemez bir risktir; projenin kendi `CLAUDE.md` belgesindeki "mimari kararlar üç
yıl sonrası düşünülerek alınır" ilkesi de bunu dışlar.

**Apify aktörlerini satın almak uygulanabilir değildir.** Bu aktörler, tanıtımlarında
Cloudflare atlatmayı bir özellik olarak sayarak yukarıdaki yasağı ücret karşılığı
devretmektedir. Aracının parayla tutulmuş olması, işin kendisini meşru hale getirmez.

**GitHub'daki mevcut kazıyıcıları çalıştırmak uygulanabilir değildir.** Aynı hukuki gerekçe
geçerlidir. Bunun üstüne bu depoların hiçbiri bakımlı değildir; yıldız sayıları bir ile iki
arasındadır, çoğunun sorunları açıktır ve site arayüzü her değiştiğinde kırılmaya
mahkûmdurlar.

**TÜİK verisi doğrudan kullanılamaz.** Yayımlanan bültenler adet ve devir sayısı
içermektedir, model bazında fiyat içermemektedir. Bu veri projeye bağlam sağlar ama fiyat
bandı üretmez.

**INDICATA, Autovista ve Eurotax pratikte erişilemez.** Bunlar kurumsal satış üzerinden
çalışan, fiyatını kamuya açıklamayan sağlayıcılardır ve kişisel ölçekli bir açık kaynak
projesinin bütçesiyle uyumlu değildir. Proje ticarileşirse bu seçenek yeniden
değerlendirilmelidir; bugün için değil.

**Hugging Face, Zenodo ve kamu açık veri portalları bu konuda boştur.** Araştırma bu
kaynaklarda Türkiye ikinci el araç fiyatına ait kullanılabilir bir veri seti bulamamıştır.

---

## 8. Kullanıcının kendi makinesinde atması gereken ilk adımlar

Bu araştırma ağ kısıtı nedeniyle bazı noktaları doğrulayamadı. Aşağıdaki üç kontrol,
yukarıdaki önerinin uygulanabilir olup olmadığını kesinleştirecektir.

Birinci olarak `tsb.org.tr/tr/kasko-deger-listesi` adresi açılmalı ve listenin toplu
indirilebilir bir dosya olarak mı yoksa yalnızca tek tek sorgulanabilen bir arayüz olarak
mı sunulduğu görülmelidir. Bu, işin tamamının zorluğunu belirleyen tek soru budur.

İkinci olarak `kaggle.com/datasets/oguzarar/turkey-used-car-prices-august-2025` sayfası
açılmalı, sütun listesinde şanzıman ve motor hacmi alanlarının bulunup bulunmadığı ve
lisans etiketi kontrol edilmelidir. Bu iki sütun yoksa set ikinci sıradaki rolü
oynayamaz ve yerine `alpertemel/turkey-car-market-2020` seti geçmelidir.

Üçüncü olarak, TSB listesinin kullanım şartlarına dair sayfada bir ibare olup olmadığına
bakılmalıdır. Liste fiilen kamusal biçimde yeniden yayımlanıyor olsa da, projenin
belgelerinde kaynağın nasıl anıldığı bu ibareye göre şekillenmelidir.
