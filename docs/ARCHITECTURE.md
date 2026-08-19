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

> **DURUM UYARISI (2026-08-06, güncellendi 2026-08-07): Karar kısmen uygulandı.**
> Yazıldığı gün `specs.kerb_weight_kg`, `specs.torque_nm` ve
> `specs.fuel_consumption_l_100km` alanları 221 aracın 221'inde de boştu; `fun`,
> `comf`, `age` ve `cost` kriterlerinin hepsi tamamen elle veriliyordu.
>
> Bugün durum farklı: `age` MK-14 ile TÜV kusur eğrisine bağlandı
> (`scripts/compute_age.py`), `fun` MK-17 ile güç/ağırlık formülüne bağlandı
> (`scripts/compute_fun.py`) — ikisi de artık 0-100 arası deterministik, tekrarlanabilir
> bir hesaptan geçiyor. `comf` ve `cost` **hâlâ tamamen elle veriliyor**; ikisinin de
> formülü PLAN.md §3.5 ve §3.8'de taslak halinde duruyor ama girdi verisi (iç hacim,
> bagaj, resmi bakım tarifesi) henüz toplanmadı.
>
> Bu uyarı bilerek kaydın içine yazıldı: mimari karar kayıtlarının değeri, uygulanan
> ile uygulanmayanı ayırt edebilmelerine bağlıdır. Bir karar kaydı, gerçekte olmayan
> bir şeyi olmuş gibi anlatıyorsa belgenin tamamının güvenilirliğini düşürür.
> Ayrıntılı döküm `docs/PUANLAMA-TEMELI.md` §6'da (o bölüm de bu güncellemeyle
> tutarlı hale getirilmeli).

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

**2026-08-19 güncellemesi:** O eşiğe ulaşıldı (`index.html` 2 MB'a çıktı) ve burada
öngörülen çözüm birebir uygulandı — bkz. MK-24. Ekran yapısına gerçekten dokunulmadı;
değişen yalnızca `note`/`evidence` alanlarının nereden okunduğu.

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

---

## MK-10 · `brand_group` gerçek markadır, uydurma üst grup değildir

**Karar:** `specs.brand_group` (araç şemasında üst seviyede duran alan) artık her zaman
aracın gerçek üretici markasına eşit — "Volkswagen", "Toyota", "BMW" gibi. Önceki
"VAG", "Japon", "Egea/Fluence", "Diğer" gibi gevşek gruplamalar tamamen kaldırıldı;
160 araç kaydının 105'inin `brand_group` alanı 2026-08-06'da düzeltildi.

**Gerekçe.** Bu alan filtrede "Marka grubu" olarak görünüyor ve kullanıcı bir markayı
aradığında onu bulabilmesi gerekiyor. "Egea/Fluence" gibi bir etiket hem yanlış (iki
farklı üreticinin iki farklı modelini birleştiriyor, gerçek bir üst kategori değil) hem
kullanışsız (kullanıcı "Fiat" ya da "Renault" arıyor, "Egea/Fluence" aramıyor). "Japon"
etiketi de yanlıştı: Hyundai ve Kia Kore menşeli, aynı kovaya konmaları coğrafi bir
yanlışlıktan başka bir şey değildi. Eski tasarımın gerekçesi "filtre menüsü çok
uzamasın" idi, ama filtre menüsünün doğruluğu kullanışlılığından önce gelir; menü artık
11 yerine 29 gerçek marka gösteriyor ve bu, arayüzün amacına daha uygun.

**İstisna.** İki kayıt gerçekten iki farklı markanın rebadge edilmiş (aynı platformu
paylaşan, yalnızca farklı logoyla satılan) ikiz modelini temsil ediyor:
`citroen-c-elysee-peugeot-301-benzinli` ("Citroën / Peugeot") ve
`kia-rio-hyundai-i20-1-4` ("Kia / Hyundai"). Bu iki kayıtta iki gerçek marka adı
` / ` ile yan yana yazılıyor; üçüncü, uydurma bir isim (eskisi gibi) asla kullanılmıyor.
Bu istisna `data/schema/car.schema.json`'da açıkça belgelendi.

---

## MK-11 · LPG dönüşüm sıklığı filtresi denendi, geri alındı

**Karar:** `specs.lpg_common` alanı ve liste ekranındaki "LPG" filtre grubu
2026-08-06'da eklendi, aynı gün kullanıcı isteğiyle tamamen kaldırıldı. Alan hiçbir
araç kaydında kalmadı, filtre kodu (`templates/app/30-filtreler.js`), `build.py`
aktarımı ve şema tanımı geri alındı.

**Neden denenmişti.** Kullanıcı LPG dönüşümlü araçları filtreden eleyebilmek istedi.
Değer, motorun `data/engines.json`'daki `aspiration` alanından (atmosferik+port
enjeksiyon → yaygın; turbo/direkt enjeksiyonlu → nadir; dizel → uygulanmıyor) mekanik
olarak türetiliyordu — kaynaklı bir iddia değil, motorun doldurma biçiminden çıkarılan
bir çıkarımdı.

**Neden geri alındı.** Kullanıcı, ürünün bugünkü aşamasında bu filtreyi istemedi.
Karar geri alınabilir ve maliyeti düşüktü (tek bir alan, tek bir filtre grubu); bu
yüzden CLAUDE.md §2'deki "bitmemiş karmaşıklık için çalışan ürün riske atılmaz"
ilkesi gereği tartışmasız geri alındı, üzerinde ısrar edilmedi. Bu kayıt yalnızca
gelecekte aynı fikir tekrar gündeme gelirse "daha önce denendi ve neden kaldırıldığı"
sorusuna cevap vermek için tutuluyor.

---

## MK-12 · Yeni bileşen ailelerinde kaynak derinliği kullanıcı isteğiyle sınırlı tutuldu

**Karar:** 2026-08-06'daki motor/şanzıman çeşitlendirme turlarında (Y-01) yeni açılan
her motor/şanzıman ailesi **tam olarak bir** gerçek kaynağa dayanıyor (istisna: bazı
sıklıkla paylaşılan aileler iki kaynakla açıldı). Bu, önceki turlardaki (Y-02, Y-01
ilk turu) genelde 1-2 kaynaklı araştırma yoğunluğuyla aynı, ama bilinçli olarak daha
fazla derinleştirilmedi.

**Gerekçe.** Kullanıcının açık talebi: "kaynak çok önemli değil, 1 kaynakları bile
olsa yeter, yeter ki sen devam et. Ben sahibinden'de gezerken gördüğüm ve merak
ettiğim her motor seçeneğini görüyor olayım platformumuzda." Kullanıcı burada bilinçli
bir değiş tokuş yapıyor: **kapsam genişliği, kanıt derinliğine göre önceliklendirildi.**
Bu, CLAUDE.md'nin "puan kanıta dayanır" ilkesini bozmuyor — her araç ve her bileşen
ailesi hâlâ en az bir gerçek, erişilebilir kaynağa dayanıyor, uydurma bir puan yok.
Değişen şey, kaynak *sayısının* (derinliğinin) Y-02'nin asıl hedefinden (ortalama 2.5
kaynak/araç) bilinçli olarak geride bırakılması.

**Sonuç.** `arac_basina_ortalama_kaynak` bu kararla birlikte üç turdur düşüyor (1.87 →
1.80 → 1.71 → 1.67); bu beklenen ve kabul edilen bir sonuç, gerileme sayılmıyor. Y-02
hâlâ geçerli bir hedef ama artık **ayrı bir tur** olarak ele alınmalı — liste
genişledikçe otomatik olarak kendini çözmüyor, çünkü her yeni araç paydaya "tek
kaynaklı" olarak giriyor. Bu ayrım `docs/ROADMAP.md` Y-01 ve Y-02 maddelerinde açıkça
yazılı duruyor ki ileride biri "neden ortalama düşüyor" diye sorduğunda cevap hazır
olsun.

---

## MK-13 · Elektrikli ve LPG araçlar kapsam dışı — kalıcı karar

**Karar:** Bu platform yalnızca geleneksel yakıtlı (Dizel/Benzin), otomatik vitesli
araçları kapsıyor. **Elektrikli araçlar (Togg, Tesla, MG'nin EV modelleri) ve LPG'li
araçlar hiçbir zaman listeye girmeyecek.** Bu, Y-01'in "önce şema kararı gerekiyor"
diye askıya aldığı D bölümünün geri alınmaz biçimde kapatılması: artık "karar
bekliyor" değil, "karar verildi ve kapsam dışı" durumu.

**Gerekçe.** Kullanıcının net talimatı: "elektrikli ve lpg araba olmayacak abi, net
bir karar o." Bu, `fuel` alanının (`Dizel`/`Benzin`) hiçbir zaman genişlemeyeceği
anlamına geliyor; MK-11'de zaten aynı yönde bir sinyal vardı (LPG dönüşüm filtresi
denenip geri alınmıştı). Hibrit araçlar (Lexus, Togg dışındaki bazı Toyota/Honda
modelleri) da aynı kapsam dışı kararın bir parçası sayılıyor, çünkü onlar da
`fuel` alanının bugünkü iki değerli (Dizel/Benzin) tasarımını bozacaktı.

**Sonuç.** `docs/ARCHITECTURE.md` ve `docs/Y01-HEDEF-LISTE.md`'deki "D) Şema kararı
bekleyenler" bölümü artık "kapsam dışı" olarak yeniden etiketlendi; Lexus, Togg, MG'nin
EV/PHEV modelleri ve benzeri hiçbir zaman araştırma turuna alınmayacak. Bu, projenin
kapsamını daraltıyor ama netleştiriyor: platform "otomatik vitesli, geleneksel yakıtlı
ikinci el araç" sorusuna cevap veriyor, "her türlü araç" sorusuna değil.

---

## MK-14 · `age` kriteri TÜV kusur eğrisine bağlandı, taslak doğrusal formül reddedildi

**Karar:** `age` (yaş, gövde ve elektrik riski) kriteri artık elle verilmiyor;
`scripts/compute_age.py` tarafından TÜV'ün gerçek muayene verisinden hesaplanıyor.
MK-06'nın "öznel kriterler formüle bağlanır" kararının fiilen uygulandığı ilk kriter
budur.

**Reddedilen taslak.** `docs/PLAN.md` §3.1 doğrusal bir formül öneriyordu
(`temel = 100 − 3.2 × yaş`). Bu formül uygulanmadan önce elimizdeki 228 aracın
araştırmayla verilmiş puanlarına karşı test edildi ve **tutmadığı görüldü**: ortalama
mutlak sapma 8 puan, en kötü durumda 31 puan (Audi A4 B5 için formül 8,8 verirken
kayıtlı puan 40'tı). Sebep, PLAN.md'nin kendi uyarısında zaten yazılıydı: yaş ile
arıza arasındaki ilişki doğrusal değil, yaşla birlikte hızlanan bir eğri. Doğrusal
formül uygulansaydı, tek tek araştırılmış puanların yerine onlardan daha kötü bir
tahmin konmuş olurdu. **Taslak formül bu yüzden reddedildi.**

**Kabul edilen kaynak.** Yerine TÜV Report 2025/2026 ve TÜV NORD 2026'nın yayınladığı
yaş bandı → ciddi kusur oranı (*erhebliche Mängel*) tablosu kullanıldı; yaklaşık
**9,5 milyon Hauptuntersuchung** sonucuna dayanıyor. Bu, metodolojimizin A seviyesi
(sayısal, kurumsal, örneklem tabanlı) tanımına giren ilk ve şu an tek kaynağımız.
Tabloya ikinci dereceden bir eğri uyduruldu (R² = 0,994) ve kusur oranı, TÜV'ün kendi
uç bantları çapa alınarak puana çevrildi (yüzde 6,45 kusur = 90 puan, yüzde 40,3
kusur = 20 puan).

**Ölçülen etki.** Yeni puanlarla eski puanlar arasındaki Spearman sıra korelasyonu
**0,95**: yani sıralama neredeyse aynı kaldı, eski elle verilen puanların *sırası*
doğruymuş. Değişen şey ölçek: ortalama 16,8 puanlık ve neredeyse tamamı aşağı yönlü
bir kayma var. Bunun anlamı, elle verilen puanların yaşlı araçlara Alman muayene
verisinin gösterdiğinden daha cömert davranmış olmasıdır. Bu bir kayıp değil, tam
olarak kurumsal veriden beklenen düzeltmedir.

**Yan karar — TÜV kaynağı araç kaynak listesine yazılmaz.** Kaynak yalnızca
`evidence.age` bloğunda anılıyor, `car["sources"]` listesine eklenmiyor. Gerekçe:
o liste "doğrulanmış" rozetini besleyen **araca özgü** bağımsız kaynakları sayıyor
(MK-04); TÜV eğrisi ise 228 aracın hepsine aynı şekilde uygulanan genel bir referans.
Listeye eklenseydi her aracın kaynak sayısı bir anda birer artar ve D-02'de kapatılan
iyimser etiketleme hatası geri gelirdi. Bu ayrım `scripts/validate.py`'ye de
öğretildi: `c-kaynakla-uc-puan` kuralı artık bir kriterin kendi `evidence` bloğundaki
kaynak seviyesine bakıyor, yetim kaynak sayımı da `evidence` referanslarını kullanım
sayıyor.

---

## MK-15 · Teknik özellik (ağırlık, tork, tüketim) verisi için dış veri seti kullanılır, ama kopyalanmaz

**Sorun.** MK-06'nın `fun`, `comf` ve `cost` için öngördüğü formüller boş ağırlık,
tork, iç hacim, bagaj hacmi ve yakıt tüketimi verisi istiyor. Bu alanlar
`data/schema/car.schema.json` içinde tanımlı ama **228 aracın 228'inde de boş**;
elle doldurmak araç başına ayrı araştırma demek.

**Değerlendirilen kaynaklar.** İki açık kaynak veri seti incelendi:

| Kaynak | Kapsam | Sonuç |
|---|---|---|
| `vbalagovic/cars-dataset` | 47.000 araç, 40+ alan | **Reddedildi.** GitHub deposu yalnızca 37 araçlık örnek içeriyor; tam veri seti ticari bir ürün (499-999 dolar) ve lisansı açıkça "proprietary". |
| `ilyasozkurt/automobile-models-and-specs` | 124 marka, 7.207 model, ~30.000 motor varyantı | **Referans olarak kabul edildi.** Ücretsiz ve tam veri deposunda; ağırlık, tork, tüketim, bagaj hacmi dahil ihtiyacımız olan bütün alanları taşıyor. |

**Karar:** İkinci veri seti **referans olarak** kullanılır, **kopyalanarak depoya
alınmaz.** Yani bir aracın ağırlığı oradan okunup kendi kaydımıza yazılır ve kaynağı
(autoevolution.com) künyeye işlenir; ham veri dosyaları `data/` içine aktarılmaz.

**Gerekçe.** Veri setinin bir LICENSE dosyası yok ve içeriği autoevolution.com'dan
izin belirtilmeden toplanmış. CLAUDE.md §4 bu projenin ticari hale gelebileceğini
söylüyor; lisansı belirsiz bir veri tabanını toplu olarak depoya almak, geri alınması
pahalı bir hukuki risk yaratır. Tek tek olguları (bir aracın ağırlığının kaç kilogram
olduğu) kaynak göstererek kullanmak ise zaten bütün projenin çalışma biçimi.

**Bilinen risk ve önlem.** ~30.000 motor varyantı arasından yanlış varyantı eşlemek,
MK-08'in uyardığı nesil karıştırma hatasının aynısını üretir (yanlış ağırlık, yanlış
tork). Bu yüzden eşleme toplu ve otomatik yapılmaz: marka, model, üretim yılı, motor
hacmi ve beygir birlikte doğrulanır, eşleşmeyen kayıt boş bırakılır. Boş bir alan,
yanlış bir alandan iyidir.

---

## MK-16 · Araç kaynak listesi, bağlı olduğu motor/şanzıman ailesinin kaynaklarını otomatik miras alır

**Sorun.** `data/engines.json` ve `data/transmissions.json`'daki her aile kendi
`sources` alanını taşıyor (o motorun/kutunun bilinen zaafını belgeleyen kaynaklar).
Ama bir araç kaydı açıldığında bu kaynaklar araca özgü `sources` listesine elle
kopyalanmıyordu; araç kaydı çoğu zaman yalnızca kendi araştırması sırasında bulunan
1-2 kaynağı taşıyordu. Sonuç: `renault-megane-2-1-6.json` gibi bir kayıt, kendi
motorunun (K4M) özel olarak araştırılmış kaynağını (`bigskies_k4m`) hiç
listelemiyordu — kaynak zaten `data/engines.json`'da kayıtlı ve doğrulanmış olduğu
hâlde, o aracın "doğrulanmış" rozeti için sayılmıyordu. 232 araçta aynı boşluk vardı;
ortalama kaynak sayısı 2,2'de tıkanmıştı ve `dogrulanmis` sayısı yalnızca 9'du.

**Karar.** `scripts/build.py`'den önce çalışan bir düzeltme geçişiyle, her aracın
`specs.engine_id` ve `specs.transmission_id` üzerinden bağlı olduğu ailenin
`sources` listesi, aracın kendi `sources` listesine (küme birleşimi, yinelenen
eklenmez) katıldı; `verification` etiketi `derive_verification()` ile yeniden
hesaplandı. Bu, MK-14'teki TÜV kararının **tam tersi bir durum**, o yüzden aynı
kurala tabi değil: TÜV eğrisi 228 aracın hepsine aynı şekilde uygulanan genel bir
referanstı ve bir aracın kendi motoruyla/kutusuyla hiçbir doğrudan ilişkisi yoktu.
Buradaki kaynaklar ise tanım gereği **o aracın gerçekten taşıdığı motor/şanzıman
ailesiyle ilgili** — `engine_id`/`transmission_id` alanı zaten `scripts/validate.py`
tarafından hacim/tip uyuşmasıyla denetleniyor, yani bağ gerçek ve doğrulanmış.
Aracın kendi araştırmasında bulunmuş ayrı bir kaynağı hiç ummamış olması, o motorun
zaten bilinen kaynağının o araca uygulanamayacağı anlamına gelmiyor.

**Sonuç.** 249 aracın 232'sinde kaynak listesi genişledi; `dogrulanmis` 9'dan
177'ye, `arac_basina_ortalama_kaynak` 2,22'den 4,31'e çıktı, `kaynak-yetersiz`
uyarısı 240'tan 72'ye düştü. Hiçbir kaynağın `MAX_CARS_PER_SOURCE` (12) sınırını
aşan tek başına dayanak (`sole_reliance`) sayısı artmadı, çünkü bu değişiklik yalnızca
zaten 1'den fazla kaynağı olan araçlarda kaynak sayısını büyüttü. `validate.py`
0 hata ile tamamlandı.

---

## MK-17 · `fun` kriteri güç/ağırlık formülüne bağlandı; taslak eşit ağırlık dizel çarpıklığı yüzünden reddedildi

**Karar.** `fun` (sürüş keyfi) kriteri artık elle verilmiyor; `scripts/compute_fun.py`
tarafından `docs/PLAN.md` §3.6'nın tanımladığı `temel + karakter_düzeltmesi`
formülünden hesaplanıyor. MK-06'nın "öznel kriterler formüle bağlanır" kararının
fiilen uygulandığı ikinci kriter budur (birincisi MK-14'teki `age`).

**Kapsam.** Formül yalnızca `specs.kerb_weight_kg` ve `specs.torque_nm` dolu olan
araçlara uygulanabiliyor; bu alanlar MK-15'in kademeli araştırmasına bağlı ve bugün
273 aracın 158'inde dolu. Diğer 115 araç dokunulmadan kaldı, eski elle verilmiş
puanlarını taşımaya devam ediyor — veri eksikken formül çalıştırılıp tahmini bir
sayı üretilmedi, "boş alan yanlış alandan iyidir" ilkesi (MK-15) burada da geçerli.

**Reddedilen taslak.** İlk deneme güç/ağırlık ve tork/ağırlığı eşit ağırlıklandırdı
(`0,5×güç + 0,5×tork`). Bu taslak 158 araca karşı test edildiğinde sayısal olarak
elle verilmiş puanlara karşı marjinal olarak biraz daha iyi korelasyon veriyordu
(Spearman 0,46), ama sıralaması **gözle görülür biçimde saçmaydı**: bir Renault
Megane 4 Estate dizel steyşın, VW Golf 7 GTI'den hemen sonra listenin 2. sırasına
çıktı; bir Peugeot 308 GT BlueHDi dizel ve bir Skoda Superb dizel de ilk 10'a
girdi. Sebep, dizel motorların aynı beygirde çok daha yüksek tork üretmesi — bu,
motorun daha keyifli sürüldüğü anlamına gelmiyor, yanma karakterinin bir yan
etkisi. Taslak formül bu yüzden reddedildi; ağırlık %75 güç / %25 tork'a çekildi.
Bu değişiklik korelasyonu ciddi bozmadan (0,46 → 0,43) sıralamayı ortak akla uygun
hale getirdi: ilk sıralarda artık GTI/hot-hatch/sportif modeller var, dizel
steyşınlar "nötr" banda düştü.

**Ölçülen etki ve dürüst sınır.** Formülün gerçekten araştırılmış (varsayılan 50
olmayan) 107 araca karşı Spearman korelasyonu 0,43, ortalama mutlak sapma ~18 puan
— MK-14'teki `age`'in 0,95 korelasyonunun çok altında. Bu, formülün yanlış olduğu
anlamına gelmiyor: `docs/PLAN.md` §3 kendi tablosunda `fun` için zaten "sezgi payı
sonrası ~%35" diyor, yani `age`'in aksine bu kriterin üçte biri formülün asla tam
yakalayamayacağı bir yargı bırakıyor. Elle verilmiş puanların da güvenilir bir
referans olmadığı ayrıca görüldü: 273 aracın 61'i (%22) birebir aynı değer olan 50
taşıyordu — araştırılmamış bir varsayılan, gerçek bir yargı değil (ör. VW Polo GTI
1.8 TSI DSG, aynı platformu paylaştığı Golf 7 GTI 86 puan alırken, hiç
araştırılmadan 50'de kalmıştı; formül bunu 76'ya çıkardı).

**Karakter düzeltmesinin kapsamı.** `± 15 puanla sınırlı, yazılı gerekçeli` kuralı
PLAN.md'nin beş kabul edilen ölçütünden yalnızca üçünü kullanabiliyor, çünkü
diğer ikisi için veri tabanında hiçbir alan yok:

| Ölçüt | Uygulandı mı | Kaynak alan |
|---|---|---|
| Arkadan itiş | Evet, +8 | `specs.drivetrain == "Arkadan"` |
| Sıralı altı silindir | Evet, +6 | `specs.engine_id`, BMW M52/M54/M57/N52 sabit listesi |
| Doğal emişli yüksek devir karakteri | Evet, +5 | `engines.json.aspiration == "Atmosferik"` + beygir/litre ≥ 75 |
| Sportif şasi kurulumu | **Hayır** | Şemada alan yok |
| Direksiyonun geri bildirimi | **Hayır** | Şemada alan yok |

Son iki ölçüt, veri tabanına yeni bir alan eklenmeden uygulanamaz; PLAN.md'nin
kendi kuralı ("hoşuma gidiyor" bir gerekçe sayılmaz, denetimsiz düzeltme hata
sayılır) burada kasıtlı olarak boş bırakmayı, kaynaksız bir sayı uydurmaya tercih
ettirdi. `evidence.fun.reasoning` bu boşluğu her araç kaydında açıkça yazıyor.

**Yan etki.** Formülün ürettiği bazı uç puanlar (0-34 veya 85-100 bandı) yalnızca
C seviyesi kaynaklara dayanıyor ve `validate.py`'nin `c-kaynakla-uc-puan` kuralını
tetikliyor (18 → 35 uyarı). Bu beklenen bir sonuç, hata değil: formül önceden
50'de donmuş, hiçbir kaynağa dayanmayan puanları gerçek uç değerlere taşıdı; kural
şimdi bu araçların gerçekten ikinci bir kaynağa ihtiyacı olduğunu doğru şekilde
işaretliyor. `validate.py` yine de 0 hata ile tamamlanıyor.

---

## MK-18 · Dış veri seti çapraz doğrulama için kullanılır; çelişki bulunduğunda depo düzeltilir

**Karar:** Depoya girmeyen bir dış veri seti bile, kendi verimizin **doğruluğunu ölçmek**
için kullanılabilir ve kullanılmalıdır. 2026-08-13'te elimize geçen P2.1 veri paketi
(1.641 araç–motor–şanzıman kombinasyonu) bu amaçla repoya karşı çalıştırıldı: iki veri
seti aynı aracın beygirini, torkunu, motor ve şanzıman ailesini bağımsız olarak
söylüyorsa, çelişen her satır bir taraftaki hatayı işaret ediyor demektir.

**Ölçüm.** 278 aracımızın 220'si P2.1'de de vardı. Sonuç:

| Karşılaştırılan alan | Çelişki | Yorum |
|---|---:|---|
| Motor ailesi (`engine_id`) | 0 | Bileşen sicili sağlam |
| Şanzıman ailesi (`transmission_id`) | 0 | Bileşen sicili sağlam |
| Beygir | 4 | İkisi varyant belirsizliği, ikisi gerçek hata |
| Tork | 6 | Üçü gerçek hata, üçü varyant/yuvarlama farkı |

**Bulunan gerçek hatalar ve düzeltmeleri.** Her biri bağımsız teknik kaynakla ayrıca
doğrulandıktan sonra düzeltildi:

- **`bmw-e46-320i` yanlış motor ailesine bağlıydı.** Kayıt, dört silindirli Valvetronic
  ailesine (`bmw-n4x`) bağlıydı ve o ailenin zincir kılavuzu zaafını taşıyordu. Oysa
  E46'da Valvetronic dört silindirliler 316i ve 318i'de kullanıldı; **320i bütün üretim
  boyunca sıralı altı silindirliydi.** 2001 sonrası 320i, M54B22 (2.171 cc, 170 bg,
  210 Nm) kullanıyor. Araç `bmw-m54` ailesine taşındı, beygir 150→170, hacim 2.0→2.2
  düzeltildi, tork alanı dolduruldu. Motor puanı 58→78 çıktı — eski puan yalnızca yanlış
  aile bağlantısının sonucuydu. Bu, MK-08'in uyardığı nesil karıştırma hatasının canlı
  bir örneğidir ve kendi denetimlerimizin (hacim/yakıt çelişki kuralları) neden yakalayamadığını
  da gösteriyor: 2.0 litre hem N4x hem M52 için geçerli bir hacimdi, yani kural sessiz kaldı.
- **`vw-passat-b7-1-6-tdi` 400 Nm taşıyordu.** 1,6 litrelik bir dizelin 400 Nm üretmesi
  mekanik olarak mümkün değil; gerçek değerler 105 bg ve 250 Nm. Bu hata `fun` puanını
  20 yerine 64 gösteriyordu, yani araç sürüş keyfi sıralamasında ilk ona giriyordu.
- **`vw-polo-gti-1-8-tsi-dsg` 320 Nm taşıyordu.** Bu, manuel şanzımanlı Polo GTI'nin
  değeri; DSG'li versiyonda tepe tork kutuyu korumak için fabrikada 250 Nm'ye
  sınırlandırılmış durumda ve bu kayıt DSG varyantını temsil ediyor.
- **`ford-focus-4-1-5-ecoblue` 270 Nm yerine 300 Nm**, **`honda-crv-3-2-0-ivtec-5at`
  190 yerine 192 Nm** olarak düzeltildi.

**Gerekçe.** Bu proje puanların gerekçesini saklıyor ama girdilerin doğruluğunu bugüne
kadar yalnızca kendi iç tutarlılık kurallarıyla denetliyordu. Passat örneği bu yaklaşımın
sınırını gösteriyor: 400 Nm hiçbir iç kuralı ihlal etmiyordu, çünkü tork alanı için üst
sınır tanımlı değildi. Bağımsız ikinci bir veri seti, iç kuralların göremediği hatayı tek
geçişte buldu. **Bu yüzden dış veri setiyle çapraz doğrulama artık bir defalık iş değil,
her yeni veri paketinde tekrarlanacak bir denetim adımıdır.**

**Yan karar — tork için üst sınır denetimi eklenmedi.** İlk refleks, `validate.py`'ye
"hacim başına tork şu değeri aşamaz" gibi bir kural eklemekti. Eklenmedi, çünkü böyle bir
sınır motor teknolojisine göre değişiyor (aynı 1,6 litre, atmosferik benzinlide 150 Nm,
modern turbo dizelde 320 Nm üretebiliyor) ve yanlış kalibre edilmiş bir sınır gerçek
verileri hata olarak işaretleyip denetime olan güveni düşürürdü. Bunun yerine çapraz
doğrulama yöntemi tercih edildi: iki bağımsız kaynağın aynı alanda anlaşması, tek taraflı
bir eşik kuralından daha güvenilir bir sinyal.

---

## MK-19 · Fiyat bandı tarihlenir ve yöntemi yazılır; ilan havuzu depoya alınmaz

**Karar:** `price_band_k_try` artık tarihsiz bir tahmin olmaktan çıkıyor. Ölçülmüş
bantlar, yanına `price_reference` bloğuyla birlikte saklanıyor: ölçüm tarihi (`as_of`),
yöntem, örneklem sayısı, gözlem penceresi, kaynak kimliği ve bilinen sınırlılıklar.
Bu, `docs/PLAN.md` §3.8'in istediği şeyin uygulanmasıdır.

**Ölçülen sorun.** 2026-08-13 tarihli piyasa gözlemleri, elimizdeki tahminlerle 19 araçta
karşılaştırılabildi. **Piyasa medyanı, tahminlerin medyan %8 üzerinde çıktı ve 19 aracın
15'inde tahmin piyasadan düşüktü.** Bazı sapmalar çok büyüktü: Skoda Octavia 1.6 TDI için
tahmin 700-1.000 bin TL derken gözlem 1.000-1.390 bin TL, Toyota Corolla E210 için tahmin
950-1.350 iken gözlem 1.415-1.665 bin TL. Bu, PLAN.md'nin "fiyatlar Türkiye enflasyonunda
altı ayda anlamsızlaşıyor" uyarısının ölçülmüş kanıtıdır: tahminler yanlış değil, **eskimişti.**

**Bandın yeni anlamı.** Ölçülmüş bir bant artık "tahmini fiyat aralığı" değil, o grupta
gözlenen istenen fiyatların **orta yarısıdır** (P25–P75). Bu tanım, uç ilanları — hasarlı
ucuzlar ve hayalci pahalılar — bandın dışında bırakıyor.

**Kabul edilen sınırlılıklar, açıkça yazılıyor.** Gözlemler tek bir pazar yerinin kamuya
açık arama sonuç kartlarından alındı ve **istenen fiyattır, gerçekleşen satış fiyatı
değildir.** Pazarlık payı ve satılamayıp ilanda birikenler yüzünden istenen fiyat
gerçekleşenin üzerindedir; aradaki fark bu veriyle ölçülemediği için bant düzeltilmeden
yazıldı. Sonuç kartında hasar bilgisi bulunmadığı için bantlar hasarlı ve hasarsız araçları
birlikte içeriyor. Bu üç sınırlılık her araç kaydında `price_reference.quality` ve
`price_semantics` alanlarında duruyor; gizlenmiyor.

**Depoya ne alındı, ne alınmadı.** `data/market/price-snapshots-2026-08.json` yalnızca
**grup düzeyinde istatistik** taşıyor: çeyreklikler, örneklem sayısı, pencere, aykırı değer
sayısı, satıcı türü dağılımı, medyan kilometre ve sorgu sayfasının adresi. **Tekil ilanlar,
ilan bağlantıları, satıcı iletişim bilgileri ve fotoğraflar bilinçli olarak alınmadı.**
Ayrım MK-15'in mantığının aynısı: bir platformun sürekli yeniden üretilebilen ilan havuzunu
kopyalamak ile o havuzdan türetilmiş bir istatistiği kaynak göstererek kullanmak aynı şey
değil. Bu proje yalnızca ikincisini yapıyor ve ticarileşme ihtimali (CLAUDE.md §4) bu ayrımı
bugünden korumayı gerektiriyor.

**Yan karar — piyasa kaynağı araç kaynak listesine yazılmaz.** Kaynak yalnızca
`price_reference.source` alanında anılıyor, `car["sources"]` listesine eklenmiyor. Gerekçe
MK-14'ün TÜV kararıyla birebir aynı: o liste "doğrulanmış" rozetini besleyen ve aracın
**güvenilirliğine** dair bağımsız kaynakları sayıyor. Bir ilan fiyatı gözlemi aracın motoru,
şanzımanı veya yaşı hakkında hiçbir şey söylemez; listeye eklenseydi fiyatı ölçülen her
aracın kaynak sayısı bir anda artar ve D-02'de kapatılan iyimser etiketleme hatası fiyat
üzerinden geri gelirdi. Bu ayrım `scripts/validate.py`'ye de öğretildi: yetim kaynak sayımı
artık `price_reference` referanslarını da kullanım sayıyor.

**Yeni denetim kuralları.** İki uyarı eklendi. `fiyat-tarihsiz`, `price_reference` bloğu
olmayan bantları işaretliyor — bugün 278 aracın 259'u bu durumda ve bu sayı, kapatılması
gereken boşluğun dürüst ölçüsüdür. `fiyat-bandi-bayat`, altı aydan eski ölçümleri
işaretliyor; altı ay eşiği PLAN.md'nin kendi ifadesinden geliyor.

---

## MK-20 · İlan sayısı likidite ölçüsü olarak reddedildi: örneklem tavana dayalı

**Karar:** `docs/PLAN.md` §3.7, `liq` (bulunabilirlik) kriterinin ilan sayımıyla
ölçülmesini öngörüyordu: "İlan sayısı kaydedilir → `liq` = log ölçekli ilan sayısının
listeye göre normalize hali." Elimize 2.071 tarihli ilan gözlemi geçtiğinde bu protokolün
nihayet uygulanabileceği düşünüldü. **Uygulanmadı ve veri bu amaçla reddedildi.**

**Gerekçe — sansürlenmiş örneklem.** Gözlemler 54 ayrı sorgu sayfasından toplandı ve
**her sorgu `take=50` parametresiyle, yani en fazla 50 ilan getirecek şekilde çalıştırıldı.**
Gruplardaki en yüksek gözlem sayısı tam olarak 50. Bu, istatistikte sağdan sansürlenmiş
(right-censored) örneklem demektir: 50 ilanı olan bir araç ile 4.000 ilanı olan bir araç
veride **birebir aynı** görünür.

Sorun yalnızca gürültü olsaydı katlanılabilirdi. Asıl sorun, sansürün **rastgele değil,
tam olarak ölçmek istediğimiz yönde** çalışması: en likit araçlar tavana dayanır ve
birbirinden ayırt edilemez hale gelir, seyrek araçlar ise gerçek sayılarıyla kalır. Bu
veriyle hesaplanacak bir `liq` puanı, en kolay bulunan araçları en likit rakiplerinden
ayıramaz ve sıralamayı sistematik olarak bozardı. **Yanlış bir ölçüm, ölçüm yokluğundan
kötüdür**, çünkü ölçülmüş görünür ve sorgulanmaz.

**Reddedilen ara çözümler.** İki çıkış yolu değerlendirilip elendi. (1) *Yalnızca 50'nin
altındaki grupları puanlamak:* bu, ölçümü tam olarak popüler araçların olmadığı bir alt
kümeye daraltır ve `liq`'in amacını ortadan kaldırır. (2) *Tavana dayananlara ortak bir
üst puan vermek:* bu, ölçüm gibi görünen bir tahmin üretir ve MK-14'te doğrusal `age`
formülünün reddedilme gerekçesiyle aynı hataya düşer.

**Ne yapıldı.** Sınırlılık, veri dosyasının kendi içine
(`known_limitations`) yazıldı ki bu veriyi sonradan açan hiç kimse aynı yanlışa düşmesin.
`liq` bugünkü haliyle elle verilmiş bir tahmin olarak kalıyor ve `docs/ROADMAP.md` bunu
açık bir eksik olarak taşımaya devam ediyor. Protokolün doğru uygulanması, sorgu başına
**toplam sonuç sayısını** (kaç ilan bulunduğunu) kaydetmeyi gerektiriyor; bu, listelenen
ilanları çekmekten farklı ve çok daha ucuz bir işlem.

---

## MK-21 · Dış katalog toplu olarak içe aktarılmaz; aday kuyruğundan tek tek geçer

**Karar:** P2.1 veri paketi 1.641 araç–motor–şanzıman kombinasyonu içeriyor; deponun
bugünkü listesi 278. Aradaki fark cazip görünüyor ama **toplu içe aktarma reddedildi.**
Adaylar `data/queue/car-candidates-p21.json` dosyasında bekliyor ve her biri deponun kendi
kanıt standardından (araca özgü kaynak, aile temel puanı, `evidence` bloğu) tek tek geçmek
zorunda.

**Ölçülen gerçek: asıl darboğaz araç sayısı değil, kimlik çözümleme.** 1.641 satır repo
standardına karşı süzüldüğünde yalnızca **6 tanesi** yeni bileşen ailesi açmadan
alınabiliyor. Kalan 1.415 satırın önündeki engel araştırma eksikliği değil: P2.1'in motor
kayıtlarının büyük kısmında motor kodu "Kaynakta belirtilmemiş" olarak duruyor, yani hangi
motor ailesi olduğu veri setinde çözülmemiş. Bir aracı kimliği çözülmemiş bir motor
ailesine bağlamak, MK-08'in uyardığı nesil karıştırma hatasını üretmenin en hızlı yolu
olurdu — ve MK-18 az önce bunun tam olarak nasıl göründüğünü gösterdi.

**Bulunan fırsat.** Marka, yakıt ve hacim üçlüsüyle bakıldığında bu çözülmemiş ailelerin
çoğunun repoda zaten karşılığı var. En çok araç açacak 30 aile için eşleme önerisi
üretildi ve kuyruk dosyasına yazıldı: **bu 30 ailenin doğrulanması 434 aracın önünü
açıyor.** Öneriler doğrulanmış değil, adaydır; her biri için motor kodunun üretim yılı ve
nesil aralığıyla birlikte teyit edilmesi gerekiyor. Y-02'de kaynak derinleştirmede işe
yarayan "en yüksek kaldıraçlı aileden başla" yöntemi burada da geçerli.

**Gerekçe.** CLAUDE.md §2 "bitmemiş karmaşıklık için çalışan ürün riske atılmaz" diyor.
1.641 satırı puanlarıyla birlikte içe almak, bugün 278 aracın hepsinde dolu olan kanıt
zincirini bir gecede seyreltirdi: ortalama kaynak sayısı çöker, "doğrulanmış" rozeti
anlamını yitirir ve deponun tek gerçek farklılaştırıcısı — her puanın arkasında yazılı bir
gerekçe olması — kaybolurdu. Katalog büyüklüğü rakiplerin de kolayca ulaşabileceği bir
metrik; kanıt derinliği değil.

---

## MK-22 · Katalog ile puanlanmış ürün iki ayrı katmandır; olgu toplu alınır, puan alınmaz

**Karar:** Depo bundan sonra iki veri katmanı taşıyor. `data/cars/` deponun **puanlanmış
ürünü**: her aracın kanıt bloğu, kaynak listesi ve yazılı gerekçesi var. `data/catalog/`
ise **olgusal teknik katalog**: P2.1 veri paketindeki araç–motor–şanzıman
kombinasyonlarının ölçülebilir alanları (güç, tork, çekiş, hacim, yakıt, gövde tipi, vites
sayısı, kavrama tipi, motor kodu, üretim yılı aralığı, teknik kaynak adresi). Katalog
katmanına **hiçbir puan yazılmaz.**

**MK-21 neyi doğru, neyi fazla geniş söylemişti.** MK-21 "dış katalog toplu olarak içe
aktarılmaz" diyordu ve gerekçesi doğruydu: 1.641 satırı **puanlarıyla birlikte** almak,
ortalama kaynak sayısını çökertir ve "doğrulanmış" rozetini anlamsızlaştırırdı. Bugün
ölçüldü, gerekçe sayıyla da doğrulandı: P2.1'in bizde karşılığı olmayan 1.101 varyantının
**451'i `p2-inferred-prior`**, yani puanı araştırılmamış, çıkarsanmış. Bunları puanlı
almak, projenin tek gerçek farklılaştırıcısını satmak olurdu.

MK-21'in fazla geniş davrandığı yer şu: **içe aktarmayı tek bir şey saydı.** Oysa bir güç
değeri ile bir güvenilirlik puanı aynı türden veri değil. Güç, tork, hacim, çekiş tipi ve
vites sayısı **ölçüm**dür; kaynağı gösterilebilir, tartışılmaz ve yanlışsa nesnel olarak
yanlıştır. Güvenilirlik puanı ise **yargı**dır; gerekçe ister. MK-21 ikisini birlikte
reddederek, alınmasında hiçbir sakınca olmayan 1.617 vites sayısını, 1.607 teknik kaynak
adresini ve 1.625 tork değerini de dışarıda bıraktı. Bu kayıp gereksizdi.

**Yeni sınır şu:** olgu toplu alınır, yargı tek tek kazanılır. Bir katalog kaydı, deponun
kanıt standardından geçtiğinde `data/cars/` katmanına terfi eder; terfi eden kayıt puan ve
`evidence` bloğu kazanır. Terfi etmemiş bir kayıt kataloğda kalır ve arayüzde **"katalogda
var, henüz puanlanmadı"** olarak görünür. Bir kullanıcının aradığı aracı bulup "bu araç
hakkında henüz puan vermedik ama teknik künyesi ve kaynağı burada" cevabını alması,
aracı hiç bulamamasından iyidir; sahte bir puan görmesinden ise kıyaslanamayacak kadar
iyidir.

**Kaynak hakları bu ayrımı zaten zorunlu kılıyordu.** P2.1'in kaynak sicilindeki yeniden
dağıtım politikası açık: 554 kayıt için "yalnız kaynak URL'si, eşleştirme metadatası ve
bağımsız türetilmiş alanlar", 500 ilan kaynağı için "toplu ham ilan kopyası yok; sayım,
zaman damgası ve sınırlı türetilmiş istatistik". Yani **kısa olgusal alan + kaynak adresi**
alınabilir, uzun metin ve ham tablo alınamaz. Katalog katmanının kapsamı tam olarak bu
iznin içinde kalıyor; 2.071 ham ilan gözlemi depoya hiç girmiyor, MK-19'daki gibi yalnız
toplulaştırılmış fiyat grupları giriyor.

**Kalite kapısı içeri taşındı.** P2.1 kendi kalite sicilini de taşıyor ve bu sicil dürüst:
798 kayıtta `generic_transmission_identity` (kutu ailesi tam çözülmemiş), 22 kayıt
`held_incomplete`, 13 kayıt `held_conflict`. Bu işaretler katalog kaydına birlikte
yazılıyor; gizlenmiyor. MK-18'in çapraz doğrulamada bulduğu türden hatalar (bir Alfa Romeo
159 kaydında Volvo şanzıman adının durması gibi) katalogda **görünür** kalıyor ki
terfi sırasında yakalansın.

**Gerekçe.** CLAUDE.md §4 mimari kararların üç yıl sonrası düşünülerek alınmasını istiyor.
Üç yıl sonra bu ürünün rakipleri katalog büyüklüğünde kolayca eşitlenir; eşitlenemeyeceği
yer kanıt derinliğidir. İki katmanlı yapı ikisini birden veriyor: katalog kapsamı arama
motoruna ve kullanıcının "benim arabam listede var mı" sorusuna cevap veriyor, puanlanmış
katman ise ürünün savunulabilir çekirdeği olarak saf kalıyor. Tek katmanda birleştirmek,
ya kapsamı ya da güvenilirliği feda etmek zorunda bırakırdı.

---

## MK-23 · Formülle hesaplanan puanlar, kaynak-seviyesi denetiminin dışındadır

**Karar:** Bir kriterin `evidence` bloğu `derivation: "formul"` taşıyorsa,
`validate.py`'nin "uç puan A veya B kanıt ister" kuralı (`c-kaynakla-uc-puan`) o
kritere uygulanmaz. Alan yoksa `kaynak` varsayılır, yani kural varsayılan olarak
uygulanmaya devam eder.

**Sorun neydi.** Kural (docs/PLAN.md M-2) doğru bir refleksten doğdu: bir motoru tek
bir forum mesajına dayanarak "felaket" ilan etmek, deponun bütün iddiasını çürütür.
Uç bir puan, iddialı bir puandır ve iddialı kanıt ister. Ama kural bütün kriterlere
aynı gözle bakıyordu, oysa depodaki puanlar iki farklı cinsten:

- **Yargı puanları** (`motor`, `trans`, `comf`, `cost`, `liq`): kaynaklar okunur,
  tartılır ve bir hükme varılır. Burada "hangi kaynağa dayanıyor" sorusu kurucu bir
  sorudur — kanıt zayıfsa hüküm de zayıftır.
- **Formül puanları** (`age`, `fun`): kaynak okunmaz. `age`, TÜV'ün yaş-kusur
  eğrisinden (MK-14); `fun`, güç/ağırlık ve tork/ağırlık oranlarından (MK-17)
  hesaplanır. İkisi de bütün araçlara aynı şekilde uygulanan, aynı girdiye her zaman
  aynı çıktıyı veren belirlenimci işlemler.

`compute_fun.py` tasarım gereği `evidence.fun.sources`'ı **boş** bırakır, çünkü o
puanı destekleyen araca özgü bir kaynak yoktur — kanıt, formülün kendisi ve yazılı
kalibrasyonudur. Kural boş listeyi görünce aracın genel kaynak listesine düşüyor ve
şu kategorik hatayı yapıyordu: **ölçülmüş bir oranı, o oranla hiç ilgisi olmayan
kaynakların seviyesine göre yargılamak.** "Bu araç 112 hp/ton üretiyor" cümlesi,
motorun şanzıman forumunda kaç kişinin şikâyet ettiğinden bağımsız olarak doğrudur.
Ölçülen bir sayıya forum kaynağı istemek, teraziye tanık istemeye benziyor.

**Ölçüsü.** Kural 40 uyarı üretiyordu; 33'ü `fun` ve `age` kaynaklıydı, yani
düzeltilemez cinstendi — bir kaynak bulunsa bile o kaynak puanı üretmiyor. Muafiyet
sonrası 7 uyarı kaldı ve hepsi gerçek yargı kriteri (`motor`, `trans`, `cost`,
`liq`). Yani kural gürültüyü bırakıp asıl işine döndü.

**Neden bir alan, neden kriter adına bakılmadı.** `if k in ("fun", "age"): continue`
yazmak daha kısaydı ama yanlış yere bağlanırdı: muafiyeti hak eden şey kriterin
**adı** değil, puanın **nasıl üretildiği**. Bugün `fun` formülle geliyor; yarın bir
kriter formülden yargıya (ya da tersine) geçerse, doğru davranış kendiliğinden gelmeli.
Alanı puanı üreten betiğin kendisi yazıyor, yani etiket ile gerçek arasında bir insan
adımı yok.

**Riski ve sınırı.** Şema `derivation: "formul"` değerini herhangi bir kritere yazmaya
izin veriyor; kötüye kullanılırsa bir yargı puanı denetimden kaçırılabilir. Bu bilinçli
olarak kabul edildi: alanı bugün yalnızca iki betik yazıyor, ikisi de
`data/cars/*.json`'a doğrudan yazan ve gerekçesi `reasoning` alanında açıkça duran
betikler. Elle `formul` yazılmış bir yargı puanı, kod incelemesinde `reasoning`
metninin betiğin imzasını taşımamasından anlaşılır.

## MK-24 · Çıktı ikiye ayrıldı: liste için `index.html`, ayrıntı için ayrı bir `detay.json`

**Karar:** MK-07'nin "çıktı tek dosya kalır" kararı, artık **tam anlamıyla** geçerli
değil. `index.html` liste/kart görünümünü çizmeye yetecek özet veriyi taşımaya devam
ediyor, ama her aracın yazılı açıklaması (`note`) ve motor/şanzıman kanıt metni
(`evidence`) artık ayrı bir dosyada, `detay.json`'da duruyor ve yalnızca bir kart veya
satır ilk kez açıldığında, tek seferlik bir `fetch()` ile çekiliyor. Bu, Y-14'ün
("veri/kabuk ayrımı") uygulamaya geçmiş hali.

**Ön koşul karşılandı mı — evet, ölçümle.** Y-14 kaydı "ölçüm olmadan iyileştirme
yapılmaz" diyordu. 2026-08-19'da `index.html` 2 MB'a ulaşmıştı; ölçüldüğünde bunun
1,37 MB'ının (%68'i) yalnızca `note`+`evidence` metinlerinden geldiği, geri kalan
"liste için gerçekten gerekli" alanların (ad, yıl, beygir, puanlar, fiyat...) toplam
406 arabada yalnızca 178 KB tuttuğu görüldü. Yani dosyanın üçte ikisi, kullanıcıların
büyük çoğunluğunun (yalnızca gezinen, filtreleyen, karşılaştıran) hiç okumadığı bir
içerikti. Ayırma sonrası `index.html` 665 KB'a indi (%67 azalma); `detay.json` 1,31 MB
ve yalnızca bir kart açıldığında iniyor.

**Bu, MK-07'nin gerekçesini geçersiz kılmıyor, tamamlıyor.** MK-07'nin asıl amacı veri
yükünün ekran başına **tekrarlanmasını** önlemekti (dört ekran, dört kopya değil, tek
yük). O ilke hâlâ geçerli: `detay.json` da tek bir kopya, bütün kartlar onu paylaşıyor.
Değişen şey, "tek yük" ile "tek HTTP isteği"nin aynı şey olması gerektiği varsayımı —
o varsayım hiç yazılı değildi, zımniydi. Liste ekranı hiç dokunmadığı 1,37 MB'ı
indirmek zorunda kalmasın diye bu iki kavram ayrıldı.

**Bedeli: `file://` üzerinden doğrudan açılan bir kopyada ayrıntı paneli eksik kalır.**
Tarayıcılar `file://` kaynağından başka bir dosyaya (`detay.json` dahil) `fetch()`
isteğini varsayılan olarak engelliyor; GitHub Pages'te (gerçek dağıtım kanalı,
`https://serhateralp01.github.io/arac_puanlama/`) bu sorun yok. Bu, ilk defa
oluşturulmuş bir kısıt değil: katkı formu da `file://` üzerinden çalışmıyor
(`docs/ROADMAP.md`, Y-04 kaydı). Karar, bu kısıtı **çökme yerine dürüst bir mesajla**
sınırlamak: `note`/`evidence` yüklenemediğinde arayüz bunu açıkça söylüyor
("...dosyayı doğrudan diskten açtıysanız bu beklenen bir durum...") ve puanlar, zayıf
halka uyarıları, kaynak bağlantıları gibi zaten yerel olan hiçbir şeyi gizlemiyor —
`scripts/smoke_test.js` bunu ayrı ve kalıcı bir kontrolle doğruluyor.

**Kimlik köprüsü.** `detay.json` aracın numaralı arayüz kimliğiyle değil kalıcı
`id`'siyle (`cid`, Y-25 dördüncü fazda eklendi) anahtarlanıyor; bu iki dosya ayrı ayrı
üretilse bile (aynı `scripts/build.py render()` çağrısından çıktıkları için asla ayrı
üretilmezler, ama ilke olarak) doğru eşleşme kalıcı kimliğe dayanıyor, çalışma zamanı
sırasına değil.

**Test altyapısı da değişti.** `scripts/smoke_test.js` artık testlerin çoğu için
`file://` yerine süreç içi bir statik HTTP sunucusu (`http://127.0.0.1:<rastgele
port>`) kullanıyor, çünkü bu gerçek dağıtımı temsil ediyor ve `fetch()`'in gerçekten
çalıştığını doğruluyor. `file://` için ayrı, kasıtlı bir kontrol duruyor — o senaryonun
çökmeden geri düşmesi de doğrulanması gereken bir davranış.
