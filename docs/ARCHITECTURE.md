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

> **DURUM UYARISI (2026-08-06): Bu karar alındı ama hiç uygulanmadı.**
> `specs.kerb_weight_kg`, `specs.torque_nm` ve `specs.fuel_consumption_l_100km`
> alanları **221 aracın 221'inde de boş**. Yani `fun`, `comf`, `age` ve `cost`
> kriterleri hâlâ tamamen elle veriliyor; bu kayıttaki "formüle bağlanır" ifadesi
> bugün için bir niyet beyanıdır, yürürlükte olan bir kural değil.
>
> Bu uyarı bilerek kaydın içine yazıldı: mimari karar kayıtlarının değeri, uygulanan
> ile uygulanmayanı ayırt edebilmelerine bağlıdır. Bir karar kaydı, gerçekte olmayan
> bir şeyi olmuş gibi anlatıyorsa belgenin tamamının güvenilirliğini düşürür.
> Ayrıntılı döküm `docs/PUANLAMA-TEMELI.md` §6'da.

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
