# Faz 2 planı — tekrarlanabilirlik ve doğrulanabilirlik

Bu belge **ne yapılacağını** tanımlar, henüz yapılanı değil. Faz 1'de veri koddan
ayrıldı ve denetim hattı kuruldu; artık neyin eksik olduğunu sayabiliyoruz. Faz 2,
o eksikleri kapatma planı.

---

## 0. Başarı ölçütü

"Tekrarlanabilir" kelimesini ölçülebilir hale getirmeden bu iş bitmez. Hedef şu üç
testi geçmek:

1. **Kör yeniden puanlama testi.** Rastgele seçilen 10 araç, yalnızca kayıtlı kanıta
   ve yazılı bantlara bakılarak sıfırdan yeniden puanlanır. Kriter başına sapma
   **≤ 10 puan** olmalı. Bugün bu test yapılamıyor çünkü bant yok.
2. **Donanım tutarlılığı.** Aynı şanzıman kutusunu ve aynı motoru paylaşan araçlar
   arasındaki `trans` / `motor` farkı, yazılı bir gerekçeye bağlı olmalı. Gerekçesiz
   fark = hata.
3. **Kanıt izlenebilirliği.** Her `verified` araçta, her kriterin puanı için "hangi
   kaynağın hangi cümlesi" sorusunun cevabı veride bulunmalı.

---

## 1. Teşhis

### 1.1 Denetimin söylediği

`scripts/validate.py` · 0 hata, 170 uyarı. Araç başına ortalama kaynak: **1.09**.

| Bulgu | Adet |
|---|---:|
| Hiç güven seviyesi atanmamış kaynak | 68 (hepsi) |
| "Kaynaklı" ama tek kaynağa dayanan araç | 38 |
| "Ön değerlendirme" ama kaynağı olan araç | 27 |
| Yazılı puan bandı olmayan kriter | 7 (hepsi) |
| Tek kaynağın taşıdığı azami araç sayısı | 36 (`trbox`) |

### 1.2 Asıl kanıt: aynı donanım, farklı puan

Denetim uyarılarından daha ağır bir bulgu var. Veriye kutu ailesi bazında bakınca
**aynı şanzımanın farklı araçlarda farklı puan aldığı ve bu farkın hiçbir yerde
gerekçelendirilmediği** görülüyor:

| Kutu | Araç | `trans` |
|---|---|---:|
| Islak 6DCT450 (Ford/Volvo Powershift) | Volvo S60 2.0 T | **28** |
| Islak 6DCT450 (aynı kutu) | Ford Mondeo 2.0 TDCi | **50** |
| Islak 6DCT450 (aynı kutu) | Ford Focus 3 1.5 TDCi | **58** |
| Aisin TK | Volvo S60 2.0 D | **90** |
| Aisin AF40 (TK) | Opel Insignia 2.0 CDTI | **74** |
| Aisin AF40 (TK) | Peugeot 308 1.6 THP | **72** |
| Kuru DQ200 | VW Golf 1.4 TSI | **35** |
| Kuru DQ200 | VW Passat B7 1.6 TDI | **38** |
| Islak DQ250 | VW CC 1.8 TSI | **66** |
| Islak DQ250 | VW Passat B8 2.0 TDI | **72** |

Bunların bir kısmı savunulabilir (AF40'ın hidrolik beyin zaafı Volvo'nun Aisin
kutusunda yok; Volvo Powershift örneklerinin bakım geçmişi daha kötü olabilir).
Ama **hiçbiri veride yazmıyor.** 28 ile 58 arasındaki 30 puanlık fark, aynı donanım
için, gerekçesiz duruyor. Bu, sezgisel puanlamanın doğrudan izi.

> Not: yukarıdaki eşleştirme araç notlarındaki metin aramasıyla yapıldı, dolayısıyla
> tam bir envanter değil. Kutu kodları veriye alanlaştırılana kadar (bkz. 3.2) kesin
> ölçüm mümkün değil — ki bu da zaten yapılacaklardan biri.

### 1.3 Kök neden

Puanlar **araç seviyesinde** veriliyor ama kanıtın çoğu **bileşen seviyesinde**
(motor kodu, şanzıman kodu). Aynı bileşen her araçta yeniden, elle, hafızadan
değerlendirilince tutarsızlık kaçınılmaz oluyor.

---

## 2. Çapraz kesen mekanizmalar

Bunlar bütün kriterlere birden uygulanır.

### M-1 · Çapalı puan bantları (anchored rubrics)

Her kriter için "şu kanıt varsa şu aralık" tanımı. Ölçme literatüründe *behaviorally
anchored rating scale* denen yöntem: puan bir hisse değil, gözlemlenebilir bir
duruma bağlanır.

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

`example` alanı kritik: her bant **listedeki gerçek bir araca çapalanır**. Yeni bir
araç puanlanırken "bu, X'ten iyi mi kötü mü" diye sorulur — mutlak yargı yerine
karşılaştırma. İnsan yargısı karşılaştırmada mutlak ölçmeden çok daha tutarlıdır.

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

Bugün kaynak = başlık + link. Link çürüyünce iddia dayanaksız kalıyor. Şema
`quotes[]` alanını tanımlıyor; doldurulacak:

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

Her kriter için üç çapa araç seçilir: yüksek, orta, düşük. Bunlar dondurulur ve
puanları yalnızca çok güçlü gerekçeyle değişir. Yeni her puan bu üçüne göre
konumlandırılır. Sürüklenmeye (drift) karşı en pratik önlem.

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

Projenin en çok emek verilen ama en tutarsız kriteri (§1.2).

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

Formüle çevrilemez; ampirik risk değerlendirmesi. `transmissions.json` ile aynı
mantıkta **`data/engines.json`** kurulur (N47, M57, EA888, 1.6 CDTI, OM611...) ve
araçlar motor koduna referans verir.

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

### 3.6 `fun` — Sürüş Keyfi · **formül + sınırlı düzeltme**

En öznel kriter, ama tamamen sezgiye bırakılması gerekmiyor:

```
temel = f(güç/ağırlık, tork/ağırlık, çekiş tipi, şanzıman tepkisi)
fun   = temel + karakter_düzeltmesi   (± 15 puanla sınırlı, yazılı gerekçeli)
```

`karakter_düzeltmesi` şu maddelerden birine dayanmak zorunda: arkadan itiş, sıralı
altı silindir, doğal emiş yüksek devir karakteri, spor şasi kurulumu, direksiyon
geri bildirimi. "Hoşuma gidiyor" gerekçe değil.

Ağırlık verisi (boş ağırlık) spec veritabanından gelir ve `specs.kerb_weight_kg`
olarak veriye eklenir — şu an yok, eklenmesi gerekiyor.

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

### Faz 2D — Kalan kanıt açığı
11. 38 tek-kaynaklı "kaynaklı" aracı ikinci kaynağa bağla veya `partial`'a çek.
12. `trbox` yoğunlaşmasını kır (36 → ≤12).
13. `liq` sayım protokolünü bir kez çalıştır.
14. 63 `preliminary` aracı 15-20'lik gruplar halinde derinleştir.

**Kabul ölçütü:** araç başına ortalama kaynak ≥ 2.0; kör yeniden puanlama testi
(§0.1) geçiyor.

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

## 7. Karar bekleyen sorular

Bunlar teknik değil, sahibinin kararı:

1. **Kapsam kuralı** (D-06): 110 bg / 1998 sınırının dışındaki 11 araç çıkarılsın mı,
   yoksa kural mı gevşetilsin? Şu anki hali kuralı anlamsız kılıyor.
2. **`fun` kriterinin ağırlığı:** Formüle çevrilince öznellik azalır ama kaybolmaz.
   Kişisel bir zevk kriteri, kanıta dayalı bir sistemde ne kadar yer tutmalı?
3. **Etiket mi politika mı:** 38 tek-kaynaklı araç `partial`'a mı çekilsin (dürüst
   ama liste birden zayıf görünür), yoksa ikinci kaynak bulunana kadar `verified`
   mı kalsın?
4. **SUV kararı:** 13 yetim kaynak SUV araştırmasından kalma. SUV'lar kalıcı olarak
   kapalı mı, yoksa ayrı bir liste olarak geri gelebilir mi?
5. **Faz 2 nereden başlasın:** Öneri 2A → 2B (yapı + formüller); en hızlı görünür
   kazanç orada. Alternatif, doğrudan 2D'ye geçip kalan 63 aracı araştırmak — ama o
   zaman araştırma eski, tutarsız yöntemle yapılmış olur.

---

## Kaynaklar

- [TÜV Report 2026 — TÜV-Verband](https://www.tuev-verband.de/pressemitteilungen/tuev-report-2026)
- [ADAC Pannenstatistik 2026 — ADAC Presse](https://presse.adac.de/meldungen/adac-ev/technik/adac-pannenstatistik-2026.html)
- [2026 MTV tarifesi](https://www.motorlutasitlarvergisi.org/2026-motorlu-ta%C5%9Fitlar-vergi%CC%87si%CC%87-mtv-yeni%CC%87-oranlar-g%C3%BCncel-hesaplama-tablosu)
- [arabam.com aylık ikinci el ilan verileri](https://www.aa.com.tr/tr/isdunyasi/otomotiv/arabamcom-haziran-ayi-ikinci-el-ilan-verilerini-paylasti/703387)
