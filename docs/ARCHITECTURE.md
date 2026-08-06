# Mimari kararlar

Bu belge, geri alınması pahalı olan kararları ve gerekçelerini kaydeder. Bir karar
burada yazılıysa, değiştirilmeden önce buradaki gerekçenin neden geçersiz kaldığının
gösterilmesi gerekir.

---

## MK-01 · Veri dosyaları tek doğruluk kaynağıdır

**Karar:** `data/` klasöründeki JSON dosyaları projenin tek doğruluk kaynağıdır. Bunun
dışındaki her depolama biçimi — üretilen HTML, ileride gelebilecek bir veritabanı, bir
API yanıtı, bir arama dizini — türetilmiş çıktıdır ve her an sıfırdan yeniden
üretilebilir olmalıdır.

**Gerekçe:** Projenin çözmeye çalıştığı asıl sorun, bir puanın neden o puan olduğunun
izlenebilmesidir. Bu izlenebilirliği sağlayan şey git geçmişidir: bir puan değiştiğinde
`git diff` hem eski değeri, hem yeni değeri, hem de commit mesajındaki gerekçeyi
gösterir. Veri bir veritabanına taşınırsa bu iz kaybolur. Türetilmiş çıktılar
kaybolduğunda ise hiçbir şey kaybolmaz, çünkü yeniden üretilebilirler.

**Sonucu:** Normal çalışma akışındaki hiçbir betik `data/` dosyalarını değiştirmez;
yalnızca okur. `build.py` ve `validate.py` bu kurala tabidir ve veriye asla yazmaz.

**Tek istisna, göç betikleridir.** Yapısal bir değişiklik 154 dosyaya birden
uygulanacaksa, bu iş elle yapılamaz. Böyle durumlarda `scripts/migrations/` altına
tarihli ve tek seferlik bir betik yazılır, insan tarafından bilerek çalıştırılır ve
ürettiği fark `git diff` üzerinden gözden geçirilir. Betiğin kendisi de depoda kalır,
çünkü değişikliğin nasıl yapıldığı da değişikliğin kendisi kadar kayda değerdir.

İstisnanın sınırı nettir: göç betiği kendiliğinden, bir derleme veya denetim adımının
parçası olarak çalışmaz. Bir kez çalışır, sonucu incelenir ve commit edilir.

---

## MK-02 · Yıldız şema yerine boyut kayıtları ve JSON dosyaları

Proje sahibinin sorusu şuydu: veriyi yıldız şemalı (star schema) bir veritabanına mı
taşımalı, yoksa basit JSON dosyalarıyla mı devam etmeli?

**Karar:** Yıldız şemanın *modelleme disiplini* benimsenir, *veritabanı teknolojisi*
benimsenmez. Veri, dosya başına bir kayıt olacak şekilde JSON dosyalarında kalır.

**Gerekçe — neden yıldız şemanın fikri doğru:** Yıldız şemanın özü, tekrar eden
gerçekleri ayrı boyut tablolarına çıkarıp olgu satırının onlara referans vermesidir.
Bu projede tam olarak bu gerekiyor. Bugün aynı şanzıman kutusu dokuz ayrı araç
kaydında yeniden değerlendiriliyor ve farklı puanlar alıyor; aynı motor ailesi altı
ayrı yerde yeniden yorumlanıyor. Motor, şanzıman ve kaynak birer boyuttur; araç ise
bu boyutlara referans veren olgudur. Bu ayrım yapılmadığı sürece tutarsızlık
yapısaldır, dikkatle çözülemez.

**Gerekçe — neden veritabanı teknolojisi yanlış:** Yıldız şema, milyonlarca satır
üzerinde toplulaştırma sorguları çalıştırmak için tasarlanmış bir analitik desendir.
Buradaki veri kümesi en iyimser büyüme senaryosunda birkaç bin satır olacak ve
sorgular toplulaştırma değil, katalog okuma niteliğinde. Buna karşılık ilişkisel bir
veritabanına geçmenin bedeli ağır: veri artık insan tarafından okunamaz, `git diff`
ile incelenemez, pull request üzerinden gözden geçirilemez. Yani projenin varlık
sebebi olan izlenebilirlik, hiç ihtiyaç duyulmayan bir sorgu performansı uğruna feda
edilmiş olur.

**Uygulanacak yapı:**

```
data/cars/*.json          olgu — her araç bir dosya, boyutlara kimlikle referans verir
data/engines.json         boyut — motor ailesi kaydı
data/transmissions.json   boyut — şanzıman kutusu kaydı
data/sources.json         boyut — kaynak künyesi
data/criteria.json        boyut — kriter tanımları, bantlar, ağırlık setleri
```

Referans bütünlüğünü veritabanı değil `scripts/validate.py` sağlar. Bugün bu denetim
kaynak kimlikleri için zaten çalışıyor; motor ve şanzıman kayıtları eklendiğinde aynı
kural onlara da uygulanacak.

**Ölçek sınırı ve sonraki katman:** Bu düzen, araç sayısı birkaç bine çıkana kadar
sorunsuz çalışır. Tarayıcının tek seferde indirdiği veri kabul edilemez büyüklüğe
ulaştığında yapılacak şey veriyi taşımak değil, **derleme adımında yeni bir çıktı
biçimi üretmektir**: örneğin salt okunur bir SQLite dosyası veya sayfalanmış bir JSON
paketi. Kaynak yine `data/` olur, üretilen dosya yine türetilmiş çıktıdır ve MK-01
bozulmaz.

---

## MK-03 · Kapsam sınırları veriden değil filtreden gelir

**Karar:** Listeye girecek aracı belirleyen "en az 110 beygir", "1998 ve sonrası",
"SUV ve MPV hariç" gibi kurallar kaldırıldı. Veri kümesi olabildiğince geniş tutulur;
daraltma işini kullanıcı arayüzdeki filtrelerle yapar.

**Gerekçe:** Bu kurallar, proje tek bir kişinin kendi alım kararı için tuttuğu bir
araştırma dosyasıyken anlamlıydı. Proje bir platforma dönüştüğü anda anlamsızlaştı,
çünkü başka bir kullanıcının bütçesi, önceliği ve gövde tercihi farklıdır. Veriden
çıkarılan araç kimse için geri getirilemez; filtrelenen araç herkes için tek tıkla
geri gelir.

**Sonucu:** Veri kümesi genişleyecek. Bunun için gövde tipi (`body_type`) alanı şemaya
eklendi ve filtre listesine girecek. SUV ve MPV araştırmasından kalan kaynaklar
silinmedikleri için geri eklendiklerinde hazır bulunacaklar.

**Yeni sorumluluk:** Kapsam genişledikçe "bu araç neden listede" sorusunun yerini "bu
araç ne kadar iyi araştırılmış" sorusu alır. Doğrulama etiketleri (MK-04) bu yüzden
daha da kritik hale geldi.

---

## MK-04 · Doğrulama etiketi kaynak sayısından türetilir

**Karar:** Bir aracın doğrulama etiketi elle verilmez, sahip olduğu bağımsız kaynak
sayısından deterministik olarak hesaplanır:

| Kaynak sayısı | Etiket | Arayüzdeki karşılığı |
|---:|---|---|
| 4 ve üzeri | `verified` | doğrulanmış |
| 1 – 3 | `partial` | kısmi kaynak |
| 0 | `preliminary` | ön değerlendirme |

**Gerekçe:** Önceki düzende etiket elle veriliyordu ve bunun sonucunda 70 araç
"kaynaklı" görünüyorken bunların 38'i tek bir kaynağa dayanıyordu. Etiketin elle
verilmesi, etiketi bir izlenim yönetimi aracına dönüştürüyor. Sayıdan türetilmesi ise
etiketi ölçülebilir bir olguya bağlıyor ve iyimser işaretlemeyi imkânsız kılıyor.

Eşiğin dört seçilmesi bilinçli bir katılıktır. İki kaynak, ikisi de aynı forumdan veya
aynı iddiayı tekrarlayan ticari bloglardan geliyorsa gerçek bir doğrulama sağlamaz.
Dört kaynak, bağımsız olma ihtimalini anlamlı ölçüde yükseltir.

**Bugünkü sonucu, dürüstçe:** Bu kural uygulandığında 154 araçtan yalnızca biri
`verified` kalıyor. Liste birdenbire çok daha az doğrulanmış görünüyor. Bu bir gerileme
değil, önceki halin fazla iyimser olduğunun ölçülmesidir ve yol haritasının hedefini
netleştirir: her aracı dört kaynağa çıkarmak.

---

## MK-05 · Kullanıcı katkısı verinin içine doğrudan yazmaz

**Karar:** İleride kullanıcılar kaynak ve bilgi önerebilecek, ancak bu öneriler
`data/` içine doğrudan yazılmayacak. Öneri bir kuyruğa girecek, incelenecek ve ancak
onaylandıktan sonra veri dosyasına dönüşecek.

**Gerekçe:** Projenin tek gerçek değeri, puanların arkasındaki kanıt zincirinin
güvenilir olmasıdır. Denetimsiz yazma hakkı verilirse ilk kötü niyetli veya sadece
dikkatsiz katkıda bu değer kaybolur ve geri kazanılması çok zordur. Buna karşılık
inceleme kuyruğu, katkının önünü kesmez, yalnızca yayına girişini geciktirir.

**Katmanlı uygulama planı:** Bu özellik tek hamlede değil, üç katmanda kurulur ve her
katman kendi başına faydalıdır.

1. **Birinci katman — GitHub konu şablonu.** Hiç altyapı gerektirmez ve bugün
   kurulabilir. Kullanıcı, hazır bir formla konu açar: hangi araç, hangi kriter, kaynak
   bağlantısı, kaynaktan alınan birebir alıntı. Bakımcı inceler ve veriye işler.
2. **İkinci katman — site içi form.** Arayüzde bir "kaynak öner" düğmesi bulunur; form,
   verilen bilgiyi bir öneri kuyruğuna yazar. Kuyruk ayrı bir depoda veya ayrı bir
   dosyada tutulur, `data/` klasörüne dokunmaz.
3. **Üçüncü katman — katkı sahibi kaydı ve itibar.** Önerileri kabul edilen kullanıcılar
   görünür hale gelir, tekrar tekrar kabul edilen katkıcıların önerileri öncelikli
   incelenir.

Hangi katmanda olunursa olunsun değişmeyen kural şudur: **kullanıcı kaynak önerir,
puanı bakımcı verir.** Kullanıcının doğrudan puan girmesi, sistemin bütün metodolojik
temelini geçersiz kılar.

---

## MK-06 · Öznel kriterler formüle bağlanır, tamamen elde bırakılmaz

**Karar:** `fun` (sürüş keyfi) kriteri elle verilen bir puan olmaktan çıkarılıp
ölçülebilir girdilerden hesaplanan bir formüle bağlanır. Aynı yaklaşım `comf`,
`age` ve `cost` için de geçerlidir.

**Gerekçe:** Sürüş keyfi öznel bir kavramdır, ama öznel olması ölçülemez olduğu anlamına
gelmez. Bir aracın ne kadar keyifli olduğunu belirleyen şeylerin çoğu sayıdır: güç,
tork, ağırlık, çekiş düzeni, şanzımanın tepki hızı. Bunlar formüle girdiğinde geriye
kalan öznel pay, gerekçe yazılması zorunlu ve büyüklüğü sınırlı bir düzeltmeye iner.

Formüle bağlamanın asıl kazancı tutarlılıktır. Elle verilen puanlar, aynı özellikteki
iki araca farklı değerler verebilir ve bugünkü veride bunun örnekleri var. Formül aynı
girdiye her zaman aynı çıktıyı verir.

**Formülün taslağı** `docs/PLAN.md` içindeki 3.6 numaralı bölümde. Uygulanabilmesi için
araç kayıtlarına boş ağırlık ve tork alanlarının eklenmesi gerekiyor; bu alanlar şemaya
eklendi ve doldurulmayı bekliyor.

---

## MK-07 · Çıktı tek dosya kalır, kaynak ekranlara bölünür

**Karar:** Uygulama tek bir uzun sayfa olmaktan çıkıp birden fazla ekrana ayrılır.
Buna karşılık üretilen çıktı **tek bir HTML dosyası olmaya devam eder**; ekranlar
adres çubuğundaki `#giris`, `#liste`, `#kiyaslama`, `#kaynaklar` gibi yol
adlarıyla ayrılır ve aralarında geçiş sayfayı yeniden yüklemeden yapılır.
Modülerlik çıktıda değil **kaynakta** kurulur: `templates/` klasörü ekran başına
bir parçaya bölünür ve `scripts/build.py` bunları birleştirir.

**Gerekçe:** Bu karar üç ölçüte göre alındı — sayfanın hafif kalması, modülerlik
ve gelecekteki eklemelerin kolay olması. Bu üç ölçüt, "çıktı" ile "kaynak"
ayrımı yapılmadığında birbiriyle çelişiyor gibi görünüyor; ayrım yapıldığında
çelişki ortadan kalkıyor.

**Hafiflik, çıktının tek dosya olmasını gerektiriyor.** Ayrı HTML dosyaları
üretmenin bedeli, veri yükünün her dosyada tekrarlanmasıdır. Bugün bu yük 154
araç için yaklaşık 160 KB; dört ekran için dört kopya demek. Asıl sorun bugünkü
sayı değil, MK-02'de kayıtlı olan büyüme beklentisidir: liste binlere çıkacak.
Kopyalanan bir veri yükü, liste büyüdükçe doğrusal olarak kötüleşir. Tek yük,
kaç ekran eklenirse eklensin sabit kalır.

**Modülerlik, kaynağın bölünmesini gerektiriyor.** Bugünkü `templates/index.html`
620 satır ve içinde yapı, biçim ve davranış iç içe duruyor. Yeni bir ekran
eklemek bu dosyayı büyütmek anlamına geliyor ve bu, CLAUDE.md'deki "bir dosyanın
başka bir katmanın işini yapmaya başlaması, bölünmesi gerektiğinin işaretidir"
kuralına takılıyor. Çözüm, çıktıyı bölmek değil kaynağı bölmektir: her ekran
kendi parçasında durur, adından ne olduğu anlaşılır, `build.py` birleştirir.
Yeni ekran eklemek artık yeni bir parça dosyası açıp yolu kaydetmek demektir.

**Kıyaslama sepetinin korunması bu kararla kendiliğinden çözülüyor.** Ekranlar
aynı JavaScript bağlamını paylaştığı için, kullanıcı listeye gidip geri
döndüğünde sepet yerinde durur; bunun için tarayıcı deposuna yazmak gerekmez.
Ayrı dosyalar seçilseydi sepetin `sessionStorage` üzerinden taşınması
gerekecekti ve bu, bellekte tutulan bir durumun diske yazılması demek olurdu —
hem daha kırılgan, hem de kullanıcının tarayıcı ayarlarına bağımlı.

**Uzun dönem karşılığı:** Bu karar bir sunucuya geçişi engellemiyor, tam tersine
ona hazırlıyor. `#liste` ve `#kiyaslama` gibi yol adları, bir gün gerçek sunucu
adreslerine (`/liste`, `/kiyaslama`) birebir çevrilebilecek biçimde seçildi.
O gün geldiğinde değişmesi gereken tek şey yönlendiricinin yol okuma biçimidir;
ekran parçaları, veri katmanı ve puanlama mantığı olduğu gibi kalır.

**Kabul edilen bedel:** Tek dosya olduğu için bir ekrana doğrudan bağlantı
verildiğinde tarayıcı yine bütün veriyi indirir. Bu, veri yükü birkaç megabayta
çıkana kadar katlanılabilir bir bedeldir; o eşiğe yaklaşıldığında doğru çözüm
dosyayı bölmek değil, veriyi ayrı bir dosyadan istek üzerine yüklemektir ve bu
değişiklik ekran yapısına dokunmadan yapılabilir.

---

## MK-08 · Bileşen revizyonu, motor/kutu ailesinin gizli bir boyutudur

**Karar:** `engine.schema.json` ve `transmission.schema.json`'a `revision_sensitivity`
alanı eklendi. Bu alan, aynı ailenin üretim yılları arasında geçirdiği ve
güvenilirliği gerçekten değiştiren bir revizyonu kaydetmek için var; `torque_sensitivity`
alanının zaman eksenindeki karşılığı.

**Gerekçe:** Aynı motor kodu veya aynı şanzıman adı, farklı üretim yıllarında farklı bir
mühendislik olabilir. Üretici aynı ismi korurken kaputun altındaki parçayı değiştirebilir
— bir turbo/kompresör kombinasyonundan tekli turboya geçebilir, bir triger zinciri
gergisini yeniden tasarlayabilir, bir yazılım güncellemesiyle vites geçiş mantığını
değiştirebilir. Bu, motor kayıtları kurulurken ilk günden karşılaşılan gerçek bir örnekle
doğrulandı: `vag-ea111-tsi` kaydı başlangıçta VW Golf'ün turbo+kompresör ("twincharger")
1.4 TSI motoruyla VW Jetta'nın daha sonraki, tekli turbolu 1.4 TSI motorunu tek bir
ailede birleştirmişti. Bunlar aynı aile değil; ikisi arasındaki 27 puanlık yayılım
donanım farkının kendisiydi, gerekçesiz bir tutarsızlık değil.

**Kural şu şekilde işliyor:**

1. Revizyon farkı doldurma yöntemini değiştirecek kadar büyükse (turbo mu kompresör mü,
   ıslak mı kuru mü), çözüm bu alanı doldurmak değil, **aileyi ikiye bölmektir**. Kimlikler
   kalıcı olduğu için (CLAUDE.md §4) bu bölünme mümkün olduğunca erken yapılmalı; bir
   aile onlarca araca bağlandıktan sonra bölünmesi çok daha pahalıya mal olur.
2. Revizyon farkı bu kadar keskin değilse ama yine de belgelenmiş bir güvenilirlik
   etkisi varsa (ör. "2013 öncesi üretilen kutularda X sorunu vardı, sonra düzeltildi"),
   fark `revision_sensitivity` alanına kaynağıyla birlikte yazılır ve araç bazındaki
   sapma `evidence.motor.reasoning` veya `evidence.trans.reasoning` ile gerekçelenir.
3. Ne "motora göre değişebilir" ne de "yıllara göre değişebilir" tek başına bir gerekçe
   sayılır. İkisi de somut kaynağa bağlanmak zorunda; aksi hâlde `scripts/validate.py`
   içindeki `motor-duzeltme-gerekcesiz` / `duzeltme-gerekcesiz` kuralları bunu yakalar.

**Uygulama notu:** `data/engines.json` içinde büyük, gerekçesiz yayılım gösteren aileler
(`psa-ep6`, `psa-dv6`, `bmw-m52`, `vag-ea189`, eski `vag-ea111-tsi`) `base_score`
araştırması sırasında önce bu mercekten inceleniyor: fark gerçek bir revizyona mı
dayanıyor, yoksa güç/donanım seviyesine mi, yoksa hâlâ açıklanamayan bir tutarsızlığa mı?
Üçü de farklı bir düzeltme gerektiriyor ve hiçbiri otomatik olarak varsayılmıyor.

---

## MK-09 · Araştırma kuyruğu, toplama ile işlemeyi ayırıyor

**Karar:** `data/queue/` klasörü kuruldu (şeması `data/schema/queue-candidate.schema.json`).
Kaynak biriktirmek (toplama) ile kaynağı puana çevirmek (işleme) artık iki ayrı
aşama: adaylar önce `data/queue/candidates.json`'a `pending` olarak düşer, ancak
değerlendirildikten sonra `data/sources.json`'a ve ilgili araç kaydına taşınır.

**Gerekçe:** İki iş farklı yetenek istiyor. Toplama geniş ama sığ bir tarama —
mümkün olduğunca çok aday kaynak bulmak. İşleme dar ama derin bir yargı — bu kaynak
hangi iddiayı destekliyor, hangi banda karşılık geliyor, güven seviyesi ne. İkisini
aynı anda yapmaya çalışmak hem yavaş hem hatalı sonuç veriyor; bu proje ölçeğinde
onlarca aday aynı anda değerlendirilmeye çalışıldığında hangi kaynağın hangi iddiayı
gerçekten desteklediği gözden kaçıyor.

Bu karar, MK-05'teki "kullanıcı kaynak önerir, puanı bakımcı verir" kuralının otomatik
araştırmaya uyarlanmış hali. Kural değişmiyor: kaynağı kim getirirse getirsin —
kullanıcı, hızlı bir tarama modeli ya da bakımcının kendisi — puanı yalnızca yazılı
metodoloji ve işleme aşamasındaki karar verir.

**Uygulama notu.** `data/queue/` içindeki hiçbir kayıt `scripts/validate.py` tarafından
gerçek veri sayılmaz ve `scripts/build.py` tarafından sayfaya basılmaz; bu ayrım
bilinçli, çünkü doğrulanmamış bir adayın yanlışlıkla yayına karışması projenin bütün
kanıt iddiasını geçersiz kılar. 2026-08-06'da bu akış, o tarihte kaynaksız olan 14 araç
için uçtan uca çalıştırıldı (bkz. `data/queue/README.md`, `docs/ROADMAP.md` Y-02/Y-03):
her biri için gerçek bir kaynak arandı, tier'ı ve hangi kriteri desteklediği
belirlendi, kabul edilenler `data/sources.json`'a ve araç kayıtlarına işlendi. Bu ilk
tur, kuyruğun yalnızca kağıt üzerinde değil gerçek veri üzerinde çalıştığının kanıtı.
