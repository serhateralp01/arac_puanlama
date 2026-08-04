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

**Sonucu:** Hiçbir betik `data/` dosyalarını okuyup değiştirmez; yalnızca okur. Veriyi
değiştiren tek şey insan eliyle yapılan ve gerekçesi commit mesajında bulunan
düzenlemedir.

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
