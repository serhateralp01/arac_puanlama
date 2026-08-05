# Faz 2 planı — tekrarlanabilirlik ve doğrulanabilirlik

Bu belge yapılacak işi tanımlar, yapılmış olanı değil. Faz 1'de veri koddan ayrıldı ve
denetim hattı kuruldu; bunun sonucunda neyin eksik olduğunu artık sayabiliyoruz. Faz 2,
sayılabilir hale gelen o eksikleri kapatma planıdır.

---

## 0. Başarı ölçütü

"Tekrarlanabilir" kelimesini ölçülebilir hale getirmeden bu iş bitmez. Hedef şu üç
testi geçmek:

1. **Kör yeniden puanlama testi.** Rastgele seçilen 10 araç, yalnızca kayıtlı kanıta
   ve yazılı bantlara bakılarak sıfırdan yeniden puanlanır. Kriter başına sapma
   **≤ 10 puan** olmalı. Bugün bu test yapılamıyor çünkü bant yok.
2. **Donanım tutarlılığı.** Aynı şanzıman kutusunu veya aynı motoru paylaşan araçlar
   arasındaki puan farkı, yazılı bir gerekçeye bağlı olmalıdır. Gerekçesi yazılmamış bir
   fark, tercih değil hata sayılır.
3. **Kanıt izlenebilirliği.** Her `verified` araçta, her kriterin puanı için "hangi
   kaynağın hangi cümlesi" sorusunun cevabı veride bulunmalı.

---

## 1. Teşhis

### 1.1 Denetimin söylediği

`scripts/validate.py` şu an 0 hata ve 401 uyarı veriyor. Araç başına ortalama kaynak
sayısı **1.09**, yani ortalama bir araç tek bir referansa dayanıyor.

| Bulgu | Adet |
|---|---:|
| Gövde tipi doldurulmamış araç | 154 (hepsi) |
| Dört kaynağa ulaşmadığı için doğrulanmış sayılamayan araç | 116 |
| Hiç güven seviyesi atanmamış kaynak | 68 (hepsi) |
| Hiçbir kaynağa bağlı olmayan araç | 37 |
| Yazılı puan bandı olmayan kriter | 7 (hepsi) |
| Tek kaynağın taşıdığı azami araç sayısı | 36 (`trbox`) |

Doğrulama etiketi politikası değiştikten sonra 154 araçtan yalnızca biri `verified`
kaldı. Bu, listenin bir gecede zayıflaması değil, önceki etiketlemenin fazla iyimser
olduğunun ölçülmesidir.

### 1.2 Asıl kanıt: aynı donanım, farklı puan

Denetim uyarılarından daha ağır bir bulgu var: aynı şanzıman kutusu farklı araçlarda
farklı puan alıyor ve bu farkın gerekçesi hiçbir yerde yazılı değil.

Bu bulgu ilk olarak araç notları üzerinde metin aramasıyla tahmin edilmişti. Kutu
kodları veriye alanlaştırıldıktan sonra (`data/transmissions.json` ve araç kayıtlarındaki
`specs.transmission_id`) artık tahmin değil ölçüm var. `scripts/consistency.py`, aynı
kutuyu paylaşan araçların `trans` puanları arasındaki yayılımı hesaplıyor.

**Ölçüm, tahminden daha ılımlı ve daha kesin bir tablo çıkardı.** Birden fazla araç
paylaşan 20 kutunun yalnızca üçünde 15 puanı aşan yayılım var:

| Kutu | Araç sayısı | Yayılım | Aralık |
|---|---:|---:|---|
| `nissan-xtronic` | 3 | **36** | Latitude 16 · Juke 45 · Fluence 52 |
| `getrag-6dct450` | 3 | **30** | Volvo S60 2.0 T 28 · Mondeo 50 · Focus 58 |
| `psa-al4` | 3 | **28** | C4 32 · Xsara 60 · 307 60 |

Kalan 17 kutu eşiğin altında ve çoğu oldukça tutarlı: `mb-5g-tronic` 12 araçta yalnızca
2 puan, `vag-dq200` 8 araçta 3 puan, `toyota-multidrive` 4 araçta 0 puan yayılıyor.

Bu, ilk teşhisin bir kısmını doğruluyor ama bir kısmını da düzeltiyor. Sorun sanıldığı
kadar yaygın değil; üç kutuda yoğunlaşmış durumda.

**Sorulması gereken bir sonraki soru şuydu: bu fark gerçek mi, yoksa hâlâ sezgisel bir
hata mı?** Aynı fiziksel kutu farklı motorlarla eşleştiğinde gerçekten farklı
davranabilir, çünkü şanzımanlar bir tork sınırına göre tasarlanır ve motorun torku bu
sınıra ne kadar yakınsa aşınma o kadar erken başlar. Bu, sezgi değil bilinen bir
mühendislik olgusu. Üç kutu tek tek araştırıldığında (bkz. `data/transmissions.json`
içindeki `torque_sensitivity` alanları):

- **`nissan-xtronic`** — fark gerçek ve tork kaynaklı. Bu kutu ailesi düşük torklu
  benzinli motorlarla sorunsuz çalışıyor, ama yüksek torklu dizellerle eşleştiğinde
  zincir kayması nedeniyle 60-100 bin km aralığında titreme bildiriliyor
  ([go4trans.com](https://shop.go4trans.com/technical-transmission-general-articles/x-tronic-cvt-design-peculiarities-pros-and-cons-typical-repair-issues-and-useful-tips/)).
  Puanı en düşük olan araç (Renault Latitude, 16 puan) tam olarak listedeki en yüksek
  torklu üye. Fark artık gerekçeli.
- **`getrag-6dct450`** — fark tork kaynaklı değil. Kutu 450 Nm'ye kadar tasarlanmış
  ([Green Car Congress](https://www.greencarcongress.com/2012/02/volvo-20120201.html))
  ve listedeki üç aracın torku da (270-340 Nm) bu sınırın oldukça altında. Şikayetler
  markadan bağımsız ve genel (düşük hızda titreme, sert hızlanmada kavrama kayması),
  bu da farkın kutunun kendisinden çok üç yılda bir gereken bakımın araç bazında
  atlanmış olma ihtimaline işaret ediyor. Bu üç aracın bakım geçmişi ayrı ayrı
  araştırılmadan fark kapatılmamalı.
- **`psa-al4`** — fark ne torkla ne başka bir mühendislik sebebiyle açıklanabildi. Üç
  aracın beygiri de birbirine çok yakın (110-120 bg). Bu, muhtemelen gerçek bir donanım
  farkı değil, bizim puanlamamızdaki bir tutarsızlık; Citroen C4'ün 32 puanı ayrıca
  kaynakla doğrulanmalı ya da diğer ikisiyle aynı seviyeye çekilmeli.

Sonuç: donanım farkının **motora bağlı olarak gerçek olabileceği** doğrulandı, ama her
puan farkı otomatik olarak meşru sayılamaz. Bu yüzden §3.2'deki formül, tork yakınlığını
adı konmuş ve zorunlu kaynağa bağlı tek bir düzeltme türü olarak tanımlıyor —
"motora göre değişebilir" diye genel bir mazeret değil.

> Ölçüm henüz eksik: 154 aracın 97'si bir kutu kaydına bağlandı, 57'si bağlanmadan
> kaldı. Bağlanmayanların `tag` alanında kutu adı açıkça yazmıyor (örneğin yalnızca
> "4 ileri tork konvertörü" deniyor) ya da birden fazla ihtimal belirtiliyor (örneğin
> "ZF 5HP / GM 5L40E"). Bu araçların kutusu kaynağa dayalı araştırmayla belirlenecek.

### 1.3 Kök neden

Puanlar **araç seviyesinde** veriliyor ama kanıtın çoğu **bileşen seviyesinde**
(motor kodu, şanzıman kodu). Aynı bileşen her araçta yeniden, elle, hafızadan
değerlendirilince tutarsızlık kaçınılmaz oluyor.

---

## 2. Çapraz kesen mekanizmalar

Bunlar bütün kriterlere birden uygulanır.

### M-1 · Çapalı puan bantları (anchored rubrics)

Her kriter için "şu kanıt varsa puan şu aralıkta olur" biçiminde bir tanım yazılır.
Ölçme literatüründe bu yönteme *behaviorally anchored rating scale* deniyor ve özü
şudur: puan bir hisse değil, gözlemlenebilir bir duruma bağlanır.

Biçim (`data/criteria.json` → `bands`):

```json
"bands": [
  { "range": [90,100], "name": "temiz",
    "test": "İki bağımsız kaynakta kronik arıza kaydı yok VE kutu tipi tork konvertörü",
    "example": "volvo-s60-2-0-d-d3-d4" },
  { "range": [70,89], "name": "yönetilebilir bakım kalemi",
    "test": "Bilinen ama planlanabilir bir kalem var (ör. 60 bin km'de yağ değişimi şart)",
    "example": "peugeot-308-1-6-bluehdi" }
]
```

Buradaki `example` alanı belirleyicidir, çünkü her bandı listedeki gerçek bir araca
çapalar. Yeni bir araç puanlanırken sorulan soru "bu araç kaç puan hak ediyor" değil,
"bu araç çapa aracından iyi mi kötü mü" olur. İnsan yargısı karşılaştırma yaparken,
mutlak bir ölçü biçerken olduğundan çok daha tutarlı çalışır.

### M-2 · Kanıt seviyeleri (A/B/C)

Şema `tier` alanını tanımlıyor, 68 kaynağın hiçbirine atanmamış.

| Tier | Ne | Örnek |
|---|---|---|
| **A** | Sayısal, kurumsal, örneklem tabanlı | TÜV Report mängelquote, ADAC Pannenkennziffer, TrueDelta arıza sıklığı, resmi MTV tarifesi |
| **B** | Bağımsız teknik analiz veya çoklu bağımsız kullanıcı örüntüsü | And Çetin analizleri, üretici teknik dokümanı, Şikayetvar'da onlarca bağımsız aynı şikayet |
| **C** | Tekil anekdot, tek forum mesajı, ticari blog | "257 bin km sorunsuz gitti" tipi tek kullanıcı beyanı |

**Kural:** Bir puan yalnızca C kaynaklarına dayanıyorsa üst bantlara (90+) veya alt
bantlara (30−) çıkamaz; orta bantta kalır. Uç puan iddialıdır, iddialı puan A veya B
kanıt ister.

### M-3 · Alıntı yakalama ve link çürümesine karşı arşiv

Bugün bir kaynak yalnızca bir başlık ile bir bağlantıdan ibaret. Bağlantı çürüdüğünde
iddiayı taşıyan hiçbir şey elde kalmıyor. Şema bunun için `quotes[]` alanını tanımlıyor
ve bu alan doldurulacak:

```json
"quotes": [{
  "text": "3'ten 4'e geçişte tekrarlayan vuup sesi... bayi yetkilisi kronik olduğunu kabul etti",
  "supports": ["trans"],
  "context": "Şikayetvar, dört ayrı konu başlığı, 2023-2025"
}]
```

Ayrıca `retrieval.query` alanı: **kaynağın hangi aramayla bulunduğu**. Araştırmanın
tekrarlanabilirliği için gerekli — aynı sorgu tekrar çalıştırılabilmeli. Ek olarak
her kaynağa `archive_url` (web.archive.org) eklenmesi öneriliyor; şemaya alan
eklenecek.

### M-4 · Çapa araç seti (calibration set)

Her kriter için yüksek, orta ve düşük olmak üzere üç çapa araç seçilir. Bu araçların
puanları dondurulur ve yalnızca çok güçlü bir gerekçeyle değiştirilir; verilen her yeni
puan bu üçüne göre konumlandırılır. Zaman içindeki sürüklenmeye karşı elimizdeki en
pratik önlem budur.

### M-5 · Duyarlılık ve sürüklenme testleri

İki otomatik kontrol, `scripts/` altına yeni betikler:

- **`sensitivity.py`** — ağırlıklar ±%20 rastgele oynatıldığında ilk 10'un ne kadar
  değiştiğini ölçer. İlk 10 tamamen değişiyorsa sıralama ağırlık seçimine aşırı
  duyarlı demektir; bu, kullanıcıya söylenmesi gereken bir sınırlılıktır.
- **`consistency.py`** — aynı motor kodunu / şanzıman kodunu paylaşan araçlar
  arasındaki puan farkını ölçer, gerekçesiz farkları raporlar. §1.2'deki bulguyu
  otomatikleştirir. `validate.py` içine kural olarak da eklenebilir.

---

## 3. Kriter kriter teknikler

Her kriter aynı yöntemle güçlendirilemez, çünkü doğaları farklı. Ayrım şu:

| Kriter | Doğası | Ana teknik | Sezgi payı sonrası |
|---|---|---|---|
| `age` | Tamamen hesaplanabilir | Formül | ~%5 |
| `cost` | Tamamen hesaplanabilir | Formül + resmi tarife | ~%10 |
| `price` | Zaten hesaplanıyor | Tarihli piyasa anlık görüntüsü | %0 |
| `trans` | Yapısal | Kutu kaydına bağlama | ~%15 |
| `comf` | Ölçülebilir vekil | Boyut/ölçü verisi + formül | ~%30 |
| `fun` | Ölçülebilir vekil | Güç/ağırlık formülü + düzeltme | ~%35 |
| `liq` | Ölçülebilir | İlan sayım protokolü | ~%20 |
| `motor` | Ampirik-riskli | Bant + kanıt seviyesi | ~%40 |

Yani yedi kriterden üçü **formüle dönüşebilir** ve sezgiden tamamen çıkabilir. Bu,
"puanlar sezgisel" eleştirisinin büyük kısmını tek hamlede kapatır.

---

### 3.1 `age` — Yaş, Gövde ve Elektrik Riski · **formüle çevrilebilir**

Bugün elle veriliyor ama içeriğinin neredeyse tamamı hesaplanabilir.

**Önerilen formül:**

```
temel   = 100 − 3.2 × (2026 − model_yılı_ortası)        # yılda ~3.2 puan
düzeltme = pas_riski_cezası + elektronik_karmaşıklık_cezası + galvaniz_bonusu
age     = clamp(temel + düzeltme, 0, 100)
```

- `pas_riski_cezası`: gövde bazlı, kaynağa bağlı bayrak (W210 için −15 gibi).
  Kaynak: TÜV Report'un korozyon kalemi, marka forumları (B tier).
- `elektronik_karmaşıklık_cezası`: hava süspansiyonu, SBC fren, aktif kasa gibi
  bilinen elektronik yük kalemleri.
- Yıl başına katsayı keyfi olmasın: **TÜV Report'un yaş sınıfı başına mängelquote
  eğrisine kalibre edilir.** TÜV 2-3 yaştan 12-13 yaşa kadar yaş sınıfı bazında kusur
  oranı yayınlıyor; katsayı bu eğrinin eğiminden türetilir.

**Etki:** 154 aracın tamamında `age` deterministik olur. Denetim, formülden sapan
elle girilmiş değeri hata olarak yakalar.

---

### 3.2 `trans` — Şanzıman · **kutu kaydına bağlanır** (yapı kuruldu)

Bu kriter, proje boyunca en çok emek verilen ama aynı zamanda en tutarsız kalan
kriterdi; §1.2'deki tablo bunu gösteriyordu. `data/transmissions.json`,
`data/schema/transmission.schema.json` ve göç betiği (`scripts/migrations/`) artık
kurulu; 154 aracın 97'si bir kutu kaydına bağlı. Kalan iş, kutulara `base_score`
atamak.

Araç kaydı `specs.transmission_id: "getrag-6dct450"` der. `trans` puanı:

```
trans = kutu.base_score + düzeltme
```

Düzeltme yalnızca iki adı konmuş türden birine girerse uygulanabilir; ikisi de yazılı
gerekçe ister, boş bir "motora göre değişebilir" ifadesi gerekçe sayılmaz:

- **Tork yakınlığı düzeltmesi.** Kutunun `torque_rating_nm` alanı doluysa ve aracın
  motor torku bu sınıra yakınsa (kabaca sınırın %80'inden fazlaysa), düzeltme
  aşağı yönde uygulanabilir. Bu, §1.2'de `nissan-xtronic` için doğrulanan gerçek bir
  mühendislik etkisi — kutunun kendi `torque_sensitivity` alanında yazılı olmalı.
- **Bakım geçmişi düzeltmesi.** Kutunun kendisi sağlam ama belirli bir uygulamada
  bilinen bir bakım kalemi (ör. yağ değişiminin atlanma eğilimi) o araca özgü bir risk
  yaratıyorsa. Bu, §1.2'de `getrag-6dct450` için henüz kapatılmamış açık soru.

Bu ikisinin dışında kalan bir fark, düzeltme değil hata sayılır ve puan kutunun temel
puanına çekilir. `psa-al4` örneği tam olarak bu durumda: ne tork ne bakım farkı
bulunabildi, yani üç aracın puanı birbirine yakınsatılmalı.

**Etki:** Aynı kutu = aynı temel puan, yalnızca adı konmuş ve kaynaklı iki düzeltme
türüyle sapabilir. `scripts/consistency.py` bu sapmayı ölçüyor; kutu başına
`base_score` atandıkça sayı azalacak.

**Öncelik: en yüksek.** Kutu kodu bir kez araştırılır, aynı kutuyu paylaşan araçlarda
tekrar araştırılmaz.

---

### 3.3 `motor` — Motor Güveni · **bant + kanıt seviyesi**

Bu kriter formüle çevrilemez, çünkü ölçtüğü şey ampirik bir risk değerlendirmesidir.
Buna karşılık şanzımanda uygulanan yapısal çözümün aynısı burada da geçerli:
`data/engines.json` kurulur, motor aileleri (N47, M57, EA888, 1.6 CDTI, OM611 ve
diğerleri) bir kez değerlendirilir ve araçlar motor koduna referans verir.

**Arıza taksonomisi** — her bilinen arıza için üç boyut:

| Boyut | Değerler |
|---|---|
| Sıklık | yaygın / sık / seyrek / nadir |
| Ağırlık | motor ölür / büyük onarım / orta / bakım kalemi |
| Başlangıç km | <80k / 80-150k / >150k |

Puan bandı bu üç boyutun kombinasyonundan türer. Örnek: N47 zincir = yaygın ×
büyük onarım × 80-150k → 40-55 bandı. Bugünkü değeri 48 — bant içinde, ama bant
yazılı olmadığı için doğrulanamıyor.

**Kanıt kaynakları, tier sırasıyla:**

- **A** — [TÜV Report](https://www.tuev-verband.de/pressemitteilungen/tuev-report-2026)
  (yaklaşık 9,5 milyon muayene, 2-13 yaş, model bazında kusur oranı) ·
  [ADAC Pannenstatistik](https://presse.adac.de/meldungen/adac-ev/technik/adac-pannenstatistik-2026.html)
  (158 model, 27 marka, model-yılı bazında Pannenkennziffer) ·
  [TrueDelta](https://www.truedelta.com) (sahip anketi, kuşak bazlı arıza sıklığı)
- **B** — üretici teknik servis bültenleri, And Çetin gibi bağımsız analistler,
  Şikayetvar'da **sayılmış** şikayet örüntüleri (tek şikayet C, elli şikayet B)
- **C** — tekil forum anekdotları

**Sınırlılık, dürüstçe:** TÜV ve ADAC Alman pazarı ve çoğunlukla 13 yaşa kadar.
Listedeki 1998-2005 araçlar için kapsam yok; oralarda B/C kanıtla yetinmek ve
`confidence: "düşük"` işaretlemek gerekecek. Bu, gizlenecek değil kaydedilecek bir
şey.

---

### 3.4 `cost` — Sahip Olma Maliyeti · **formüle çevrilebilir**

Muhtemelen en yüksek kazanç/emek oranı olan kalem, çünkü girdilerin hepsi resmi
veya kamuya açık.

```
yıllık_maliyet = MTV + yakıt + sigorta + beklenen_bakım
cost_puanı     = listedeki en ucuza 100, en pahalıya 0 (fiyat puanı gibi normalize)
```

| Bileşen | Kaynak | Belirlenimcilik |
|---|---|---|
| **MTV** | Resmi tarife: silindir hacmi × araç yaşı (2018 öncesi araçlarda değer dilimi yok) | Tam |
| **Yakıt** | Araç varyantının l/100 km değeri (auto-data.net gibi spec veritabanı) × yıllık 15.000 km × güncel akaryakıt fiyatı | Tam |
| **Sigorta** | Kasko değeri üzerinden yaklaşık oran | Yaklaşık |
| **Bakım / parça** | Sabit bir "parça sepeti" (fren balatası + disk + yağ filtresi + triger seti + debriyaj) fiyatı | Ölçülebilir, emek ister |

MTV tarifesi `data/tax/mtv-2026.json` olarak veriye alınır ve tarihli tutulur; her
yıl güncellenir, eski yıllar arşivde kalır. Böylece "2026'da bu puan neydi" sorusu
cevaplanabilir.

**Kritik ayrım:** `cost` **arıza sıklığını içermez** (o `motor`/`trans`/`age`
işi), yalnızca **öngörülebilir** giderleri içerir. Bu ayrım metodolojide zaten var,
formüle geçerken korunmalı.

---

### 3.5 `comf` — Günlük Kullanım Rahatlığı · **vekil ölçüler**

Öznel ama vekil değişkenleri ölçülebilir:

```
comf = 0.30 × iç_hacim_skoru      (dingil mesafesi, arka diz mesafesi)
     + 0.20 × bagaj_skoru          (litre)
     + 0.20 × manevra_skoru        (uzunluk, dönüş çapı — ters yönde)
     + 0.15 × NVH_skoru            (ses yalıtımı; test sürüşü/inceleme kaynaklı)
     + 0.15 × şanzıman_yumuşaklığı (kutu tipinden türetilir: TK > CVT > ıslak DCT > kuru DCT > robot)
```

İlk üçü spec veritabanından çekilebilir ve tamamen belirlenimci. Son ikisi yargı
gerektirir ama ağırlığı %30'a iner. Bugünkü `comf` puanları bu formüle karşı test
edilip sapmalar gözden geçirilir.

---

### 3.6 `fun` — Sürüş Keyfi · **formüle bağlanır** (karar verildi)

Bu kriterin elle verilen bir puan olmaktan çıkarılıp formüle bağlanmasına karar
verildi; kararın gerekçesi `docs/ARCHITECTURE.md` içindeki MK-06 kaydında. Sürüş keyfi
öznel bir kavramdır, ancak öznel olması ölçülemez olduğu anlamına gelmez. Bir aracı
keyifli kılan şeylerin çoğu sayıdır: güç, tork, ağırlık, çekiş düzeni ve şanzımanın
tepki hızı.

```
temel = f(güç/ağırlık, tork/ağırlık, çekiş tipi, şanzıman tepkisi)
fun   = temel + karakter_düzeltmesi   (± 15 puanla sınırlı, yazılı gerekçeli)
```

`karakter_düzeltmesi` şu maddelerden en az birine dayanmak zorunda: arkadan itiş,
sıralı altı silindir, doğal emişli yüksek devir karakteri, sportif şasi kurulumu veya
direksiyonun geri bildirimi. "Hoşuma gidiyor" bir gerekçe sayılmaz ve denetim gerekçesi
yazılmamış düzeltmeyi hata olarak raporlar.

Formülün çalışabilmesi için araç kayıtlarına boş ağırlık ve tork alanlarının eklenmesi
gerekiyor. Bu alanlar (`specs.kerb_weight_kg`, `specs.torque_nm`) şemaya eklendi ve
doldurulmayı bekliyor.

---

### 3.7 `liq` — Bulunabilirlik ve Satılabilirlik · **sayım protokolü**

Ölçülebilir ama ölçüm bugün hiç yapılmamış; puanlar tamamen tahmin.

**Protokol (yazılı, tekrarlanabilir):**

1. Belirli bir tarihte, sahibinden.com ve arabam.com'da her araç için sabit bir
   arama tanımı (marka + model + şanzıman: otomatik + yıl aralığı) çalıştırılır.
2. İlan sayısı kaydedilir → `data/market/listings-YYYY-MM.json`.
3. `liq` = log ölçekli ilan sayısının listeye göre normalize hali.
4. Dış çapa: arabam.com'un
   [aylık ilan raporları](https://www.aa.com.tr/tr/isdunyasi/otomotiv/arabamcom-haziran-ayi-ikinci-el-ilan-verilerini-paylasti/703387)
   model bazında en çok ilan verilen listeyi yayınlıyor; sayım bununla çapraz
   kontrol edilir.

**Uyarı:** sahibinden.com otomatik erişime kapalı. Sayım elle yapılacak; 154 araç
için tek seferde ~3 saat. Ölçüm tarihi kaydedildiği için altı ayda bir
tekrarlanabilir ve eskime görünür olur.

---

### 3.8 `price` — Fiyat Avantajı · **anlık görüntüyü tarihlendir**

Formül zaten belirlenimci. Eksik olan, **girdinin** nereden geldiği: fiyat bantları
tarihsiz ve yöntemsiz.

Yapılacak: her fiyat bandına `as_of` tarihi ve `method` alanı (ör. "N=20 ilanın
medyanı ±%20") eklenir. Eskiyen bantlar denetimde uyarı üretir. Fiyatlar Türkiye
enflasyonunda altı ayda anlamsızlaşıyor; tarihsiz fiyat yanıltıcıdır.

---

## 4. Asset bazlı iş listesi

| Asset | Bugün | Yapılacak |
|---|---|---|
| `data/cars/*.json` | Puan var, gerekçe yok | `evidence` bloğu doldur; `kerb_weight_kg`, `fuel_consumption`, `engine_id`, `transmission_id` alanları ekle |
| `data/sources.json` | Başlık + link | `tier`, `quotes[]`, `retrieval.query`, `archive_url` doldur |
| `data/criteria.json` | `bands: null` | Yedi kriterin bantlarını yaz, çapa araçları ata |
| `data/engines.json` | 79 aile, 154 araç bağlı, 78'i base_score'lu | Kaynak sayısını 2.0'a çıkarmak için genel kaynak araştırması |
| `data/transmissions.json` | **yok** | Kutu kodu kaydı kur (~25 kutu) |
| `data/tax/mtv-YYYY.json` | **yok** | Resmi MTV tarifesini veriye al |
| `data/market/listings-YYYY-MM.json` | **yok** | İlan sayımı anlık görüntüsü |
| `scripts/validate.py` | 12 kural | Formül sapması, gerekçesiz düzeltme, kanıt-tier uyumu, fiyat eskimesi kuralları |
| `scripts/consistency.py` | **yok** | Aynı bileşen → aynı puan denetimi |
| `scripts/sensitivity.py` | **yok** | Ağırlık duyarlılığı analizi |
| `docs/methodology.md` | Bant bölümü boş | Bantlar yazılınca doldur |
| `.github/workflows/` | Denetim + duman testi | Link çürüme kontrolü (aylık cron) ekle |
| Arayüz | Puan gösteriyor | Puanın yanında güven rozeti ve "neden bu puan" paneli göster |

---

## 5. Sıralama

Sıra rastgele değil: **önce yapıyı kur, sonra veriyi doldur.** Ters sırada yapılırsa
doldurulan veri yapı değişince yeniden yazılır.

### Faz 2A — İskelet (veri girmeden)
1. `transmissions.json` kuruldu (30 kutu, 154 araç bağlı). `engines.json` kuruldu
   (79 aile, 154 araç bağlı, 78'i base_score'lu).
2. **Tamamlandı.** Yedi kriterin puan bantları yazıldı, her banda mümkün olan yerde
   kaynaklı bir çapa araç atandı; beş bant için (comf 35-49/0-34, age 85-100, cost 0-34)
   bugünkü veride gerçek örnek bulunmadığı için bilerek örneksiz bırakıldı
   (`docs/methodology.md` §7).
3. **Tamamlandı.** 68 kaynağa A/B/C tier atandı (3 A, 25 B, 40 C). C-kaynağa dayanan
   puanın uç bantlara çıkamaması kuralı denetime eklendi.
4. `consistency.py` yazıldı ve şanzıman kutularında çalıştırıldı; motor kayıtları
   kurulduğunda aynı denetim `motor` puanı için de eklenecek.

**Kabul ölçütü:** `validate.py --strict` yalnızca "veri henüz doldurulmadı" tipi
uyarı veriyor; yapısal uyarı kalmadı.

### Faz 2B — Yüksek kazançlı formüller
5. `age` formülünü uygula, 154 aracın tamamını yeniden hesapla, sapmaları incele.
6. MTV tarifesini veriye al, yakıt tüketimi verisini topla, `cost` formülünü uygula.
7. `price` bantlarına tarih ve yöntem ekle.

**Kabul ölçütü:** üç kriter formülden geliyor; elle girilen değer denetimde hata.

### Faz 2C — Kutu ve motor kayıtları
8. **Tamamlandı.** 29 kutunun tamamına `base_score` ve en az bir güvenilirlik
   kaynağı atandı. Daha önce yalnızca sınıflandırma sağlayan (hangi araç hangi
   kutuyu kullanıyor bilgisini veren ama güvenilirlik hakkında bir şey söylemeyen)
   kaynağa dayandığı için boş bırakılan beş kutuya (`aisin-geartronic`,
   `aisin-tf80`, `aisin-aw60t`, `mb-5g-tronic`, `alfa-tct`) ve hiç kaynağı olmayan
   altı kutuya (`zf-5hp`, `zf-6hp`, `gm-5l40e`, `mb-4g-tronic`, `mb-7g-tronic`,
   `vag-s-tronic-islak`) gerçek güvenilirlik araştırmasıyla kaynak ve puan
   verildi. Bu araştırma dört aracı `duzeltme-gerekcesiz` denetimine takıldı;
   üçü (`mercedes-c180-w204`, `mercedes-c250-cdi-w204`, `mercedes-e250-cdi-w212`)
   `mb-7g-tronic` kutusuna karşı ABD'de açılan toplu davanın ortaya çıkardığı
   gerçek bir mekatronik arıza kaydı yüzünden 80-82'den 44'e çekildi; biri
   (`alfa-romeo-159-1-9-jtdm`) `aisin-tf80`'in 2010 öncesi/sonrası üretim
   ayrımı nedeniyle 76'dan 58'e çekildi. `mercedes-c180-w204` bu düzeltmeyle
   birlikte dört kaynağa ulaşıp `verified` oldu.
9. **Tamamlandı.** `scripts/validate.py`'ye `duzeltme-gerekcesiz` kuralı eklendi: bir
   aracın `trans` puanı, bağlı olduğu kutunun `base_score`'undan 15 puandan fazla
   sapıyorsa ve `evidence.trans.reasoning` boşsa hata değil uyarı üretiyor. İlk
   çalıştırmada 9 araç yakalandı; yedisi kutunun kendi kanıtına göre düzeltildi (ör.
   dört Aisin AF40 aracı 74'ten 58'e çekildi), biri (Renault Latitude)
   `evidence.trans` bloğuyla gerekçelendirildi ve puanı korundu. Sonuncusu (Volvo S60
   2.0T) önce açık bırakıldı, ardından Volvo'ya özgü bir kanıt aranıp bulunamadığı
   teyit edildi ve puan kutunun temel puanına çekildi; bkz. `docs/DATA-ISSUES.md`
   D-09.
10. **Tamamlandı.** Kutu kaydına bağlı olmayan 57 araçtan 56'sı bağlandı. Bunun için
    15 yeni kutu kaydı kuruldu (`zf-4hp`, `gm-aisin-af17`, `gm-4t65e`,
    `honda-4at-5at`, `hyundai-a4af3`, `jatco-re4f0x`, `jatco-jf506e`, `ford-cd4e`,
    `ford-4f27e`, `aisin-awf21`, `mitsubishi-invecs-cvt`, `suzuki-4at`, `toyota-4at`,
    `alfa-q-system`, `aisin-aw55`) ve her biri kendi güvenilirlik araştırmasıyla
    birlikte geldi. Bağlanamayan tek araç `skoda-octavia-1-tour-1-6-1-8-2-0`: VAG'ın
    01N/01V kodlu 4 ileri Tiptronic kutusu için güvenilirlik hakkında bir şey söyleyen
    kaynak bulunamadı ve kaynaksız bir kutu kaydı açmak yerine bağlanmadan bırakıldı.
    Bu bağlama işi 22 araçta gerekçesiz puan sapması ortaya çıkardı ve hepsi kutunun
    temel puanına çekildi; ayrıntı ve gerekçe `docs/DATA-ISSUES.md` D-11'de.
    Yetim kutu kalmadı (`gm-5l40e` dört BMW'ye, `hyundai-6at` yedi Hyundai/Kia'ya
    bağlandı).
11. **İskeleti tamamlandı.** `data/engines.json` kuruldu: motor aileleri tanımlandı ve
    154 aracın tamamı `specs.engine_id` ile bir aileye bağlandı. `engine.schema.json`
    şanzıman şemasının desenini izliyor ve §3.3'teki arıza taksonomisini (sıklık,
    ağırlık, başlangıç kilometresi) `known_issues` altında taşıyor. `validate.py`'ye
    motor ekseninin denetimleri eklendi: `kayip-motor-kaydi`, `motor-yakit-celiski`,
    `motor-hacim-celiski` (hata); `motor-kaydi-yok`, `motor-temel-puani-yok`,
    `motor-kaynaksiz`, `yetim-motor`, `motor-duzeltme-gerekcesiz` (uyarı). Yakıt ve
    hacim çelişkisi denetimleri, yanlış aileye bağlanmış bir aracı yakalamak için
    kondu; 154 aracın hepsi bu denetimden hatasız geçti. `consistency.py` artık iki
    ekseni birden ölçüyor.

    **Tamamlandı.** 79 motor ailesinin 78'ine gerçek güvenilirlik araştırmasıyla
    `base_score`, `known_issues` ve en az bir kaynak verildi. Kalan tek istisna
    (`volvo-b4204s`) bilinçli olarak boş bırakıldı: motor kodu eşlemesi düşük güvenle
    yapıldığı için gerçek bir kaynak bulunana kadar puan üretilmedi; kaynaksız puan
    üretmek projenin kendi kuralına aykırı olurdu.

    Araştırma sırasında, ilk teşhiste görülen beş yüksek-yayılımlı motor ailesi çözüldü
    ve bu süreçte üç farklı düzeltme türü ortaya çıktı:

    1. **Aile bölündü** (fark doldurma yöntemi kadar temelse): `vag-ea111-tsi` →
       twincharger (36) + tekli turbo (56) sürümlerine; `psa-ep6` → `psa-ec5` (TU5
       türevi, EP6 ile ilgisi yoktu) + VTi (70) + THP (46) sürümlerine;
       `hyundai-gamma-16` → MPI (78) + GDI (46) sürümlerine — araştırma GDI alt ailesinin
       aynı dönemin toplu dava konusu Theta II/Nu motorlarıyla kök nedeni paylaştığını
       gösterdi.
    2. **`revision_sensitivity` alanı dolduruldu** (aynı aile, üretim yılına göre
       belgelenmiş bir revizyon var): BMW N47'de 2009 zincir tasarımı değişikliği,
       Mercedes OM651'de 2014 enjektör/zamanlama iyileştirmesi, PSA EP6-THP'de triger
       zinciri revizyonu, GM A20DTH'de 2013 dayanıklılık iyileştirmesi, Rover KV6'da 2001
       conta revizyonu, Saab B2x5'te 2006 PCV/VKG revizyon kiti.
    3. **Gerçek veri hatası düzeltildi** (revizyon değil, önceki araştırma eksikliği):
       `psa-dv6` — PSA'nın kendi markalı araçları 70-72, Volvo D2 45 puandı; araştırma
       aynı turbo yağ açlığı + EGR tıkanması paterninin PSA kaynaklarında da belgelendiğini
       gösterdi, üç Peugeot aracının puanı 44'e çekildi.

    Toplamda 11 araç puanı (motor veya trans), yeni bulunan kanıta göre gerekçeli olarak
    düzeltildi; her biri `evidence.motor.reasoning` veya doğrudan puan güncellemesiyle
    kayıt altına alındı ve `docs/sources.json`'a 60'tan fazla yeni kaynak eklendi.

    `psa-dv6` ile `vag-ea111-tsi` özellikle dikkat çekiyor: ikisinde de aynı fiziksel
    motor, farklı araçlarda 27 puan fark alıyor ve bu farkın hiçbir yerde yazılı bir
    gerekçesi yok. Bu, §1.3'teki kök nedenin motor tarafındaki birebir karşılığıdır.

**Kabul ölçütü — sağlandı.** §1.2 tablosundaki üç kutunun hepsi çözüldü:
`nissan-xtronic` gerekçeli (evidence.trans), `psa-al4` ve `getrag-6dct450` aileleri
tamamen kutuya yakınsadı (yayılımları sırasıyla 28→8 ve 30→8'e indi).
`scripts/consistency.py` artık yalnızca `nissan-xtronic`'i işaretliyor, o da
gerekçeli olduğu için beklenen bir durum.

### Faz 2D — Kapsamı genişletme
11. **Tamamlandı.** 154 aracın 150'sine `specs.body_type` atandı ve arayüze gövde
    filtresi eklendi. Dört karma model kaydı (Rio/i20, A/B Serisi, 2008/208,
    S40/V50) birleştirdikleri iki modelin gövdesi farklı olduğu için bilerek boş
    bırakıldı; gerekçesi `docs/DATA-ISSUES.md` D-10'da. Filtre diğer filtrelerle
    aynı çok seçimli mantığı kullanıyor (kategori içinde VEYA, kategoriler arasında
    VE) ve `scripts/smoke_test.js` artık bu filtreyi de gerçek tarayıcıda
    doğruluyor.
12. SUV ve MPV araçları listeye ekle. Bu araçlar için yapılmış araştırmadan kalan 13
    yetim kaynak (Tucson, Qashqai, Sportage, C5 Aircross, Grandland, Koleos) hazır
    bekliyor ve doğrudan bağlanacak.
13. Listeyi yeni segmentlere doğru genişlet. Genişleme sırasında her yeni araç, o
    tarihte yürürlükte olan bantlara ve kaynak politikasına göre puanlanır; eski
    araçlar için geriye dönük düzeltme ayrı bir iş kalemidir.

**Kabul ölçütü — kısmen sağlandı.** Gövde filtresi çalışıyor ve hiçbir araç kapsam
kuralı yüzünden listenin dışında değil. SUV ve MPV araçların listeye eklenmesi (madde
12) ile listenin yeni segmentlere genişletilmesi (madde 13) hâlâ açık.

### Faz 2F — Çok ekranlı arayüz ve giriş akışı (plan dışı, araya girdi)

Liste büyüdükçe tek uzun sayfa yetersiz kalmaya başladı. Bu, plandaki fazlardan
biri değildi ama proje ticari bir ürün olarak düşünülmeye başlandığı için öne
alındı. **Tamamlandı:**

- `templates/index.html` bir kabuğa, ortak bir stil dosyasına, ekran parçalarına
  (`templates/screens/*.html`) ve davranış parçalarına (`templates/app/*.js`) bölündü.
  Çıktı yine tek bir `arac-puanlama.html`; gerekçesi `docs/ARCHITECTURE.md` MK-07.
- Araç listesi, kıyaslama, kriterler ve kaynaklar ayrı ekranlara ayrıldı; aralarında
  `#liste`, `#kiyaslama` gibi yollarla, sayfa yeniden yüklenmeden geçiliyor. Kıyaslama
  sepeti ekran değiştikçe sıfırlanmıyor.
- Sade, ticari olmayan üç adımlık bir giriş akışı eklendi: bilgi asimetrisi sorunu,
  kanıta dayalı puanlama yaklaşımı, platformun ne olmadığı. İlk ziyarette otomatik
  açılıyor, sonrasında yalnızca üst menüden ("Bu nedir?") erişiliyor.
- `scripts/smoke_test.js`'ye giriş ekranının ilk ziyarette açıldığını, tepsi
  düğmesinin kıyaslama ekranına götürdüğünü ve sepetin ekran değişince korunduğunu
  doğrulayan kontroller eklendi (16/16 geçiyor).

Bu faz bilinçli olarak formüllerden ve bileşen kayıtlarından **sonraya** bırakıldı.
Liste, metodoloji oturmadan genişletilirse yeni araçlar da eski araçlarla aynı
tutarsızlıkla puanlanır ve sorun büyüyerek tekrarlanır.

### Faz 2E — Kalan kanıt açığı
14. 116 `partial` aracı dört kaynağa çıkar.
15. `trbox` yoğunlaşmasını kır; bu kaynağın taşıdığı araç sayısını 36'dan 12'nin
    altına indir.
16. `liq` sayım protokolünü bir kez çalıştır.
17. 37 `preliminary` aracı 15-20'lik gruplar halinde derinleştir.

**Kabul ölçütü:** araç başına ortalama kaynak sayısı 2.0'ın üstünde; kör yeniden
puanlama testi (§0, madde 1) geçiyor.

### Kullanıcı katkısı — fazlara paralel ilerler
Kaynak önerisi kabul eden GitHub konu şablonu kuruldu ve bugün çalışıyor. Bu, MK-05
kaydındaki üç katmanlı planın birinci katmanı. İkinci katman (site içi öneri formu) ve
üçüncü katman (katkı sahibi kaydı) yukarıdaki fazlardan bağımsız olarak, kendi
sıralarında ele alınacak. Katkı hacmi artmadan ikinci katmanı kurmak erken olur.

---

## 6. Riskler

| Risk | Etki | Karşılık |
|---|---|---|
| Bantlar mevcut puanlara *geriye dönük uydurulur* | Metodoloji tiyatroya döner | Bantlar önce yazılır, sonra puanlara bakılır; sapmalar **puan düzeltilerek** kapatılır, bant genişletilerek değil |
| TÜV/ADAC eski araçları kapsamıyor | Listenin yarısı A-tier kanıtsız kalır | `confidence: "düşük"` işaretlenip arayüzde gösterilir; gizlenmez |
| Formüller aracın gerçeğini kaçırır | Sayısal ama yanlış puan | Her formül önce 154 araçta çalıştırılıp mevcut puanla karşılaştırılır; büyük sapmalar formülü değil aracı sorgular |
| İlan sayımı elle ve eskiyor | `liq` çürür | Ölçüm tarihi kaydedilir, 6 aydan eski sayım denetimde uyarı üretir |
| Kapsam genişledikçe iş bitmez | Proje yarım kalır | Faz 2A ve 2B tek başına değerli; 2C/2D olmadan da araç kullanılabilir kalır |

---

## 7. Verilen kararlar

Bu bölümde daha önce karar bekleyen sorular listeleniyordu. Soruların hepsi
cevaplandı ve kararların tam gerekçeleri `docs/ARCHITECTURE.md` içine taşındı. Aşağıda
kararların özeti ve bu plana yansıması var.

**Kapsam sınırları kaldırıldı (MK-03).** "En az 110 beygir", "1998 ve sonrası" ve "SUV
ile MPV hariç" kurallarının üçü de kaldırıldı. Veri kümesi olabildiğince geniş
tutulacak, daraltma işi kullanıcının filtrelerine bırakılacak. Bu karar Faz 2D'yi
doğurdu.

**Doğrulama etiketi kaynak sayısından türetiliyor ve eşik dört (MK-04).** Tek kaynağa
dayanan araçlar `partial` oldu; `verified` rozeti için dört bağımsız kaynak gerekiyor.
Kural bütün veriye uygulandı ve `verified` araç sayısı 70'ten 1'e düştü.

**Sürüş keyfi formüle bağlanacak (MK-06).** Güç, tork, ağırlık, çekiş düzeni ve
şanzıman tepkisinden hesaplanan bir temel puan, gerekçesi yazılmak zorunda olan ve
±15 puanla sınırlı bir karakter düzeltmesiyle birleşecek. Ayrıntısı §3.6'da.

**Kullanıcı katkısı alınacak, ancak veriye doğrudan yazılmayacak (MK-05).** Kullanıcılar
kaynak önerir, puanı bakımcı verir. Birinci katman olan GitHub konu şablonu kuruldu.

**Veri yıldız şemalı bir veritabanına taşınmayacak (MK-02).** Yıldız şemanın modelleme
disiplini benimseniyor, yani motor, şanzıman ve kaynak birer boyut kaydı haline
geliyor; ancak depolama JSON dosyaları olarak kalıyor, çünkü `git diff` üzerinden
inceleme bu projenin varlık sebebi.

**Sıralama:** Faz 2A ve 2B önce yapılacak. Liste, metodoloji oturmadan
genişletilmeyecek.

---

## Kaynaklar

- [TÜV Report 2026 — TÜV-Verband](https://www.tuev-verband.de/pressemitteilungen/tuev-report-2026)
- [ADAC Pannenstatistik 2026 — ADAC Presse](https://presse.adac.de/meldungen/adac-ev/technik/adac-pannenstatistik-2026.html)
- [2026 MTV tarifesi](https://www.motorlutasitlarvergisi.org/2026-motorlu-ta%C5%9Fitlar-vergi%CC%87si%CC%87-mtv-yeni%CC%87-oranlar-g%C3%BCncel-hesaplama-tablosu)
- [arabam.com aylık ikinci el ilan verileri](https://www.aa.com.tr/tr/isdunyasi/otomotiv/arabamcom-haziran-ayi-ikinci-el-ilan-verilerini-paylasti/703387)
