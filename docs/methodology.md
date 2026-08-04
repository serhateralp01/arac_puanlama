# Metodoloji

Bu belge puanların **nasıl** verildiğini tanımlar. Amaç, aynı kanıtın aynı puanı
üretmesi — yani tekrarlanabilirlik. Bugünkü durumda bu hedefin bir kısmı sağlanmış
(kriter tanımları net ve birbirini dışlıyor), bir kısmı henüz sağlanmamış (puan
bantları yazılı değil). Eksik olan yerler açıkça işaretlendi.

---

## 1. Kapsam

Listeye girmek için yalnızca iki şart var: aracın **otomatik şanzımanla** satılmış
olması ve **Türkiye ikinci el piyasasında bulunabilir** olması. Robotlu yarı otomatik
kutular otomatik sayılıyor, manuel şanzımanlı araçlar listeye girmiyor.

Daha önce geçerli olan "en az 110 beygir", "1998 ve sonrası" ve "SUV ile MPV hariç"
kuralları **kaldırıldı**. Bu kurallar, proje tek bir kişinin kendi alım kararı için
tuttuğu bir araştırma dosyasıyken anlamlıydı. Proje bir karşılaştırma platformuna
dönüştüğü anda anlamını yitirdiler, çünkü her kullanıcının bütçesi, önceliği ve gövde
tercihi farklı. Veriden çıkarılan bir araç kimse için geri getirilemez; buna karşılık
filtrelenen bir araç herkes için tek tıkla geri gelir.

Bunun sonucu olarak veri kümesi olabildiğince geniş tutuluyor ve daraltma işi tamamen
kullanıcının elindeki filtrelere bırakılıyor. Kararın tam gerekçesi
`docs/ARCHITECTURE.md` içindeki MK-03 kaydında yazılı.

Gövde tipi artık bir kapsam sınırı değil, bir filtre boyutu. Araç kayıtlarına
`specs.body_type` alanı eklendi; alan henüz doldurulmadığı için gövde filtresi de
henüz arayüzde yok. SUV ve MPV araçları listeye girdiğinde bu alan kullanılacak.

---

## 2. Kriterler

Yedi puanlanan kriter, artı otomatik hesaplanan fiyat. Kriterlerin tam tanımları
`data/criteria.json` içinde; aşağıdaki tablo özet.

| Kod | Ad | Ölçtüğü | Ölçmediği |
|---|---|---|---|
| `motor` | Motor Güveni | Motorun arıza sıklığı ve ağırlığı | Performans → `fun`; şanzıman → `trans` |
| `trans` | Şanzıman ve Otomatik Kutu | Kutunun tipi ve güvenilirliği | Motor → `motor`; vites hissi → `fun` |
| `fun` | Sürüş Keyfi ve Karakter | Güç, tork, şasi, direksiyon, çekiş | Güvenilirlik → diğer sütunlar |
| `comf` | Günlük Kullanım Rahatlığı | Sürme kolaylığı + oturma rahatlığı | Sürüş zevki → `fun` |
| `age` | Yaş, Gövde ve Elektrik Riski | Motordan bağımsız yaş riskleri | Motor/şanzıman mekaniği → kendi sütunları |
| `cost` | Sahip Olma Maliyeti | Yakıt, vergi, parça fiyatı ve erişimi | Arıza sıklığı → diğer sütunlar |
| `liq` | Bulunabilirlik ve Satılabilirlik | Bulma ve satma kolaylığı | Yedek parça bulma → `cost` |
| `price` | Fiyat Avantajı (otomatik) | Satın alma fiyatı, listeye göre normalize | Kullanım maliyeti → `cost` |

**Tasarım kararı — kriterler birbirini dışlar.** Her kriterin tanımında "neye
bakıyorum" ve "neyi başka sütunda değerlendiriyorum" cümleleri var. Bu, aynı özelliğin
(ör. performans) iki sütuna birden sızmasını engelliyor. Önceki sürümde dokuz kriter
vardı; "kolay sürülürlük" ile "konfor", "masraf" ile "parça erişimi" anlamca örtüştüğü
için birleştirildi.

---

## 3. Puan hesabı

```
toplam    = Σ(kriter_puanı × ağırlık) / Σ(ağırlıklar)
normalize = listedeki en yüksek toplama 100, en düşüğe 0 verilerek yeniden ölçekleme
fiyat     = 100 × (en_pahalı_orta − aracın_ortası) / (en_pahalı_orta − en_ucuz_orta)
```

Ağırlıklar toplamı 100'den saparsa hesap yine normalize edilir; arayüz sadece uyarır.

Normalize sütunun varlık sebebi: ham toplamlar dar bir bantta (yaklaşık 52–75)
toplanıyor ve aradaki fark gözle görülmüyor. Normalize sütun bu farkı büyütür.

### Ağırlık setleri

| Set | motor | trans | fun | comf | age | cost | liq | price |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Dengeli | 20 | 15 | 16 | 11 | 10 | 12 | 6 | 10 |
| Sürüş keyfi öncelikli | 17 | 13 | 30 | 8 | 8 | 8 | 4 | 12 |
| Güvenilirlik öncelikli | 20 | 16 | 6 | 16 | 12 | 12 | 6 | 12 |

---

## 4. Şanzıman tipi sınıflandırması

Projenin en çok emek harcanan kısmı. Şanzıman tipi hem `trans` puanını doğrudan
belirler hem `motor` ve `cost` puanlarını dolaylı etkiler.

| Kod | Anlamı | Neden bu sırada | Örnek |
|---|---|---|---|
| `TK` | Tork konvertörü | Mekanik sürtünme kavraması yok, güç yağ üzerinden aktarılıyor | ZF, Aisin, Mercedes 5G/7G-Tronic |
| `Islak DCT` | Islak kavramalı çift kavrama | Kavramalar yağ içinde çalışıyor, ısınma riski düşük | VW DQ250, Ford/Volvo 6DCT450 |
| `Kuru DCT` | Kuru kavramalı çift kavrama | Trafikte beklerken ısınma, kavrama aşınması | VW DQ200, Ford DPS6 |
| `CVT` | Kademesiz | Marka bağımlı: Toyota/Honda güvenilir, Nissan/Renault değişken | Toyota Multidrive, Renault X-Tronic |
| `Robot` | Robotlu yarı otomatik | Aslında manuel şanzıman, motorlu debriyaj | Peugeot ETG, Fiat Dualogic |

**Bu sınıflandırma birden fazla kez yanlış çıktı ve düzeltildi** — metodolojinin neden
"tek kaynağa güvenme" ilkesine dayandığının kanıtı:

- Hyundai Tucson: "2.0 CRDi + tork konvertörü" sanıldı; TR'de yaygın olan **1.6 CRDi + kuru DCT**.
- Nissan Qashqai 1.3 DIG-T: "ıslak DCT" sanıldı; TR pazarında çoğunlukla **X-Tronic CVT**.
- Renault Megane/Clio 1.3 TCe: "kuru DCT" sanıldı; gerçekte **ıslak 7 ileri Getrag EDC**.
- Seat Ateca 1.6 TDI: "ıslak DQ200/DQ250" diye çelişkili yazılmıştı (DQ200 zaten kuru).

`validate.py` artık `tag` metni ile `transmission_type` alanının çeliştiği durumları
otomatik yakalıyor (`tag-tx-celiski` kuralı).

---

## 5. Doğrulama etiketleri

Her aracın adının yanında, o araç için ne kadar kanıt toplandığını gösteren bir rozet
bulunuyor. Bu rozet elle verilmiyor; aracın bağlı olduğu bağımsız kaynak sayısından
hesaplanıyor.

| Kaynak sayısı | Etiket | Arayüzdeki karşılığı |
|---:|---|---|
| 4 ve üzeri | `verified` | doğrulanmış |
| 1 – 3 | `partial` | kısmi kaynak |
| 0 | `preliminary` | ön değerlendirme |

Eşiğin dört seçilmesi bilinçli bir katılıktır. İki kaynak, ikisi de aynı forumdan veya
birbirinin aynı iddiasını tekrarlayan ticari bloglardan geliyorsa gerçek bir doğrulama
sağlamaz. Dört kaynak, kaynakların birbirinden bağımsız olma ihtimalini anlamlı ölçüde
yükseltir.

Etiketin sayıdan türetilmesi de bilinçli bir tercihtir. Önceki düzende etiket elle
veriliyordu ve bunun sonucunda 70 araç "kaynaklı" görünürken bu araçların 38'i tek bir
kaynağa dayanıyordu. Elle verilen etiket, bir ölçüm olmaktan çıkıp bir izlenim yönetimi
aracına dönüşüyor. `scripts/validate.py` artık etiketin kaynak sayısıyla uyuşmadığı her
durumu **hata** olarak raporluyor, uyarı olarak değil.

**Bugünkü tablo, dürüstçe:** Kural uygulandığında 154 araçtan yalnızca biri
`verified` kalıyor, 116 araç `partial`, 37 araç `preliminary` oluyor. Liste birdenbire
çok daha az doğrulanmış görünüyor. Bu bir gerileme değil; önceki halin fazla iyimser
olduğunun ölçülmesi ve yol haritasının hedefinin netleşmesi anlamına geliyor. Hedef
artık açık: her aracı dört bağımsız kaynağa çıkarmak.

---

## 6. Zayıf halka eşiği

Herhangi bir kriterde puan **35'in altındaysa** hücre kırmızı işaretlenir ve detay
panelinde neden düşük olduğu açıklanır.

Eşik neden 35: 30'da yalnızca 15 araçta, 40'ta 43 araçta (listenin üçte biri) en az bir
kırmızı hücre çıkıyordu. 40 çok gevşek olduğu için uyarı anlamını yitiriyordu. 35'te
28 araç işaretleniyor — makul bir denge.

Açıklama metni `weakReason()` fonksiyonu tarafından kural tabanlı üretiliyor: kritere
ve `transmission_type` alanına bakıp uygun gerekçeyi seçiyor. Ölçeklenebilir ama kaba;
araca özel gerekçe yazmıyor.

---

## 7. Puan bantları

Yedi kriterin yedisi de artık yazılı, çapalı bir bant tanımına sahip. Bantlar
`data/criteria.json` içindeki her kriterin `bands` alanında tutuluyor; bu bölüm o
verinin nasıl okunacağını ve neden bu biçimde kurulduğunu anlatıyor.

Her bant beş parçadan oluşuyor: bir puan aralığı, kısa bir ad, kanıtın hangi somut
durumu göstermesi gerektiğini tanımlayan bir test cümlesi, listedeki gerçek bir araca
işaret eden bir `example` ve gerekirse bir açıklama notu. `example` alanı belirleyici,
çünkü her bandı soyut bir sayı aralığından çıkarıp listedeki gerçek bir araca çapalıyor.
Yeni bir araç puanlanırken sorulan soru "bu araç kaç puan hak ediyor" değil, "bu araç
çapa aracından iyi mi kötü mü" oluyor; insan yargısı karşılaştırma yaparken mutlak bir
ölçü biçmekten çok daha tutarlı çalışıyor (`docs/PLAN.md` M-1).

`trans` kriterinin bantları örnek olarak:

| Aralık | Ad | Test |
|---|---|---|
| 85–100 | temiz | İki bağımsız kaynakta kronik arıza kaydı yok, kutu tipi tork konvertörü ya da düşük torkla eşleşen ıslak çift kavrama |
| 65–84 | yönetilebilir bakım kalemi | Kutu sağlam ama düzenli bir bakım kalemi bildiriliyor (ör. periyodik yağ değişimi) |
| 50–64 | tekrarlayan ama yönetilebilir şikayet | Tekrarlayan bir şikayet örüntüsü var ama felaket değil |
| 35–49 | bilinen risk, kavrama/mekatronik odaklı | En az bir kaynak, düşük-orta kilometrede kavrama veya mekatronik arızasını doğruluyor |
| 0–34 | düşük km'de felaket, çoklu kaynak | Birden fazla bağımsız kaynak, ağır ve pahalı bir arızayı doğruluyor |

Kalan altı kriterin (`motor`, `fun`, `comf`, `age`, `cost`, `liq`) bantları aynı
mantıkla `data/criteria.json` içinde tanımlı.

**Boş kalan bantlar, bilerek doldurulmadı.** Bugünkü 154 araçlık listede beş bant
(`comf` 35-49 ve 0-34, `age` 85-100, `cost` 0-34) için gerçek bir örnek yok — ne
kaynaklı ne kaynaksız. Örneğin en düşük `comf` puanı bile 56, yani hiçbir araç
"belirgin konfor zafiyeti" bandına düşmüyor. Bu, bandın yanlış tanımlandığı anlamına
gelmiyor; listenin bugüne kadar hiç sert veya spartan bir araç içermediği anlamına
geliyor. Bant tanımı, gerçek bir örnek bulunana kadar örneksiz kalıyor; mevcut
puanlara uydurulmuyor. Bu, doğrudan bir metodoloji ilkesinin uygulanmasıdır: **bantlar
önce yazılır, sonra puanlara bakılır; sapmalar puan düzeltilerek kapatılır, bant
genişletilerek değil** (`docs/PLAN.md` §6).

Bir istisna var: `liq` kriterinin 0-34 bandı, kaynaksız bir araca (`rover-75-2-0`)
çapalandı. Bu araç için "Türkiye'de neredeyse hiç usta ve parça ağı yok" değerlendirmesi
kaynakla doğrulanmadı, ama dilin kalibre edilmesi için gerçek bir örneğe ihtiyaç vardı.
Bant kaynak bulunana kadar bu şekilde kalıyor, aracın kendi puanının doğruluğu ayrıca
iddia edilmiyor.

Bir sonraki adım, her araç kaydındaki opsiyonel `evidence` bloğunu doldurmak: hangi
kriterin hangi banda göre, hangi kaynakla puanlandığı. Şema bu alanı şimdiden
tanımlıyor (`data/schema/car.schema.json`).

Ayrıntılı plan: [PLAN.md](PLAN.md).
