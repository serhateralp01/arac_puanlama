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
kadar yaygın değil; üç kutuda yoğunlaşmış durumda. Yine de bu üç kutudaki farkların
hiçbiri veride gerekçelendirilmemiş. `getrag-6dct450` örneğinde aynı donanım için 30
puanlık bir fark var ve Volvo'nun 28 puanı ile Ford'un 58 puanı arasındaki ayrımı
açıklayan tek bir cümle bile yok.

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

### 3.2 `trans` — Şanzıman · **kutu kaydına bağlanır**

Bu kriter, proje boyunca en çok emek verilen ama aynı zamanda en tutarsız kalan
kriterdir; §1.2'deki tablo bunu gösteriyor.

**Yapısal değişiklik — `data/transmissions.json`:**

```json
"6dct450": {
  "id": "6dct450",
  "names": ["Powershift (ıslak)", "Volvo Powershift", "Ford 6DCT450"],
  "type": "Islak DCT",
  "supplier": "Getrag",
  "base_score": 58,
  "known_issues": [
    { "issue": "mekatronik yağ sızıntısı", "onset_km": 120000,
      "severity": "orta", "sources": ["mondps"] }
  ],
  "maintenance": "3 yılda bir yağ değişimi şart",
  "sources": ["mondps", "volvops"]
}
```

Araç kaydı `specs.transmission_id: "6dct450"` der. `trans` puanı:

```
trans = kutu.base_score + araç_bazlı_düzeltme
```

`araç_bazlı_düzeltme` **yalnızca yazılı gerekçeyle** verilebilir (ör. "bu araçta
kutu daha yüksek tork altında çalışıyor: −5"). Gerekçesiz düzeltme = denetim hatası.

**Etki:** Aynı kutu = aynı temel puan garantisi. §1.2'deki 28/50/58 üçlüsü ya
gerekçelenir ya düzelir. Ayrıca kutu kodu bir kez araştırılır, 9 araçta tekrar
araştırılmaz — araştırma emeği ~%60 düşer.

**Öncelik: en yüksek.** Hem en büyük tutarsızlık burada, hem en kolay düzeltilebilir.

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
| `data/engines.json` | **yok** | Motor kodu kaydı kur (~35 motor ailesi) |
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
1. `transmissions.json` ve `engines.json` şemalarını ve boş kayıtlarını kur.
2. Yedi kriterin puan bantlarını yaz, her banda çapa araç ata.
3. Kaynak tier tanımlarını kesinleştir ve 68 kaynağa A/B/C ata.
4. `consistency.py` ve yeni denetim kurallarını yaz.

**Kabul ölçütü:** `validate.py --strict` yalnızca "veri henüz doldurulmadı" tipi
uyarı veriyor; yapısal uyarı kalmadı.

### Faz 2B — Yüksek kazançlı formüller
5. `age` formülünü uygula, 154 aracın tamamını yeniden hesapla, sapmaları incele.
6. MTV tarifesini veriye al, yakıt tüketimi verisini topla, `cost` formülünü uygula.
7. `price` bantlarına tarih ve yöntem ekle.

**Kabul ölçütü:** üç kriter formülden geliyor; elle girilen değer denetimde hata.

### Faz 2C — Kutu ve motor kayıtları
8. ~25 kutuyu araştır ve `base_score` ata (araç değil kutu araştırılıyor).
9. Araçları kutu kaydına bağla, farkları gerekçelendir veya düzelt.
10. Aynısını ~35 motor ailesi için yap.

**Kabul ölçütü:** §1.2 tablosundaki her fark ya yazılı gerekçeye bağlı ya kapanmış.

### Faz 2D — Kapsamı genişletme
11. Mevcut 154 aracın `specs.body_type` alanını doldur ve arayüze gövde filtresini ekle.
12. SUV ve MPV araçları listeye ekle. Bu araçlar için yapılmış araştırmadan kalan 13
    yetim kaynak (Tucson, Qashqai, Sportage, C5 Aircross, Grandland, Koleos) hazır
    bekliyor ve doğrudan bağlanacak.
13. Listeyi yeni segmentlere doğru genişlet. Genişleme sırasında her yeni araç, o
    tarihte yürürlükte olan bantlara ve kaynak politikasına göre puanlanır; eski
    araçlar için geriye dönük düzeltme ayrı bir iş kalemidir.

**Kabul ölçütü:** gövde filtresi çalışıyor ve hiçbir araç kapsam kuralı yüzünden
listenin dışında değil.

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
