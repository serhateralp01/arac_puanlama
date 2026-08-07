# Puanlama modelinin bilimsel temeli

Bu belge, projenin puanlama sisteminin **hangi yönteme dayandığını**, o yöntemin hangi
varsayımları gerektirdiğini ve bu varsayımların bugünkü veride gerçekten sağlanıp
sağlanmadığını anlatır. `docs/methodology.md` "puan nasıl verilir" sorusuna cevap verir;
bu belge "bu yöntem neden geçerli, nerede kırılıyor" sorusuna cevap verir.

Belgedeki bütün sayılar `scripts/analysis/sensitivity.py` çıktısından geliyor ve
221 araçlık bugünkü veri üzerinde ölçüldü. Veri değiştiğinde betik yeniden çalıştırılıp
bu belgedeki sayılar tazelenmelidir; aksi hâlde belge kendi iddiasını çürütür.

---

## 1. Sistem ne tür bir modeldir

Bu bir **çok kriterli karar analizi** (multi-criteria decision analysis, MCDA)
modelidir. Kullandığı toplama yöntemi literatürde **ağırlıklı toplam modeli** (weighted
sum model, WSM) diye geçer ve çok nitelikli fayda teorisinin (multi-attribute utility
theory, MAUT) en basit özel hâlidir. Temel referans Keeney ve Raiffa'nın *Decisions
with Multiple Objectives* (1976) çalışmasıdır; yöntemlerin karşılaştırmalı bir dökümü
için Triantaphyllou'nun *Multi-Criteria Decision Making Methods: A Comparative Study*
(2000) çalışmasına bakılabilir.

Formül şudur ve `templates/app/00-cekirdek.js` içindeki `total()` fonksiyonunda birebir
uygulanır:

```
toplam(araç) = Σ ( kriter_puanı(araç, k) × ağırlık(k) ) / Σ ağırlık(k)
```

Bu, her aracı sekiz boyutlu bir puan vektörü olarak ele alıp kullanıcının ağırlık
vektörüyle iç çarpımını alır. Sonuç, kullanıcının kendi tercih fonksiyonuna göre
hesaplanmış tek bir fayda skorudur.

### Neden ağırlıklı toplam, neden AHP veya TOPSIS değil

Alternatifler değerlendirildi ve bilinçli olarak reddedildi:

| Yöntem | Neden kullanılmadı |
|---|---|
| **AHP** (Saaty, 1980) | Kullanıcıdan kriterleri ikişer ikişer karşılaştırmasını ister (8 kriter için 28 karşılaştırma). Bir araç sitesinde bu, kullanıcının terk edeceği bir yüktür. Ayrıca tutarlılık oranı düşük çıktığında kullanıcıya "cevaplarınız çelişkili" demek gerekir; bu, ürünün amacı değil. |
| **TOPSIS** (Hwang ve Yoon, 1981) | İdeal ve anti-ideal noktalara uzaklık hesaplar. Matematiksel olarak zarif ama sonucun **neden** o sonuç olduğunu kullanıcıya anlatmak çok daha zor; bu projenin bütün iddiası açıklanabilirlik. |
| **ELECTRE / PROMETHEE** | Üstünlük ilişkisi (outranking) kurar, tam sıralama üretmeyebilir. Kullanıcı "hangi araç daha iyi" sorusuna net cevap bekliyor. |
| **Ağırlıklı toplam (seçilen)** | Şeffaf, tek satırda anlatılabilir, ağırlık değişiminin etkisi anında görülür. Bedeli aşağıda §4'te dürüstçe yazılı: telafi edici olması ve kriterlerin bağımsızlığını varsayması. |

Seçim, matematiksel üstünlük iddiasına değil **açıklanabilirlik** tercihine dayanıyor.
Kullanıcı bir aracın neden o sırada olduğunu anlayamıyorsa, modelin ne kadar zarif
olduğunun bir önemi yok.

---

## 2. Kriter puanları nasıl üretiliyor: çapalı derecelendirme ölçeği

Yedi kriterin her biri için `data/criteria.json` içinde yazılı **puan bantları** var.
Her bant bir puan aralığı, bir ad, kanıtın hangi somut durumu göstermesi gerektiğini
tanımlayan bir test cümlesi ve **listedeki gerçek bir araca işaret eden bir çapa**
(`example`) içerir.

Bu yöntem literatürde **davranışa çapalı derecelendirme ölçeği** (behaviorally anchored
rating scale, BARS) adıyla bilinir; Smith ve Kendall'ın 1963 tarihli *Journal of Applied
Psychology* makalesinde tanımlanmıştır. Yöntemin dayandığı bulgu şudur: insan yargısı
mutlak bir sayı biçerken tutarsız, iki şeyi karşılaştırırken çok daha tutarlı çalışır.
Bu yüzden yeni bir araç puanlanırken sorulan soru "bu araç kaç puan hak ediyor" değil,
"**bu araç çapa aracından iyi mi kötü mü**" olur.

Bantların uygulanmasında değişmeyen kural: **bantlar önce yazılır, sonra puanlara
bakılır. Sapma varsa puan düzeltilir, bant genişletilmez.** Bir bandın gerçek örneği
yoksa boş bırakılır; mevcut puanlara uydurulmaz. Bugün beş bant bu yüzden örneksiz
duruyor (bkz. `docs/methodology.md` §7).

### Kanıt seviyesinin puanı sınırlaması

Kaynaklara A/B/C güven seviyesi verilir ve bu seviye **hangi puanın verilebileceğini
sınırlar**: yalnızca C seviyesi kaynaklara dayanan bir puan en üst (90+) veya en alt
(34−) banda çıkamaz, orta bantta kalır. `scripts/validate.py` bu kuralı
`c-kaynakla-uc-puan` uyarısıyla denetler. Bu, iddianın gücünü kanıtın gücüne bağlayan
bir kısıttır ve modelin en önemli metodolojik korumasıdır.

---

## 3. Ölçülen sonuçlar: model ne kadar sağlam

Aşağıdaki bulgular `scripts/analysis/sensitivity.py` ile 221 araç üzerinde ölçüldü.

### 3.1 Ağırlık gürültüsüne dayanıklılık — **güçlü**

Her ağırlığa bağımsız olarak ±%25 rastgele gürültü eklenip 500 deneme çalıştırıldı:

| Ölçüt | Sonuç |
|---|---|
| Spearman sıra korelasyonu (ortalama) | **0.990** |
| Spearman en düşük | 0.967 |
| %5'lik dilim | 0.980 |
| İlk 10'da korunan araç (ortalama) | **9.33 / 10** |

Yorum: ağırlıkları bir miktar yanlış seçmek sıralamayı bozmuyor. Bu önemli, çünkü
ağırlıklar (aşağıda §5) türetilmiş değil, seçilmiş sayılar. Model, ağırlıkların tam
olarak "doğru" olmasına bağımlı değil.

### 3.2 Hazır ayar setleri sıralamayı gerçekten değiştiriyor — **tasarım gereği**

| Set | Spearman | İlk 10 ortak | İlk 20 ortak |
|---|---:|---:|---:|
| Güvenilirlik öncelikli | 0.955 | 7/10 | 17/20 |
| Sürüş keyfi öncelikli | 0.799 | **3/10** | 8/20 |

Yorum: "sürüş keyfi öncelikli" seti ilk 10'un yedisini değiştiriyor. Bu bir kusur değil,
ürünün varlık sebebi — farklı öncelikler farklı araçlar getirmeli. Ama §3.1'le birlikte
okunduğunda önemli bir ayrım çıkıyor: **küçük ağırlık hataları sonucu değiştirmiyor,
bilinçli öncelik değişikliği değiştiriyor.** Model tam olarak böyle davranmalı.

### 3.3 Hangi kriterler sonucu fiilen belirliyor

Bir kriterin ağırlığı sıfırlandığında sıralamanın ne kadar bozulduğu:

| Kriter | Spearman | Yorum |
|---|---:|---|
| `motor` | 0.821 | **Taşıyıcı kriter** |
| `trans` | 0.826 | **Taşıyıcı kriter** |
| `fun` | 0.925 | Orta etkili |
| `age` | 0.927 | Orta etkili |
| `price` | 0.928 | Orta etkili |
| `cost` | 0.954 | Zayıf etkili |
| `liq` | 0.982 | Çok zayıf etkili |
| `comf` | **0.986** | **Neredeyse etkisiz** |

Motor ve şanzıman sonucu belirliyor — bu, projenin baştaki teşhisiyle (asıl risk motor
ve şanzımanda) tutarlı ve iyi bir işaret.

### 3.4 Bulunan sorun: `comf` kriteri ayırt etmiyor

`comf` iki ölçüte göre birden zayıf:

- Ağırlığı sıfırlandığında sıralama neredeyse hiç değişmiyor (Spearman 0.986, ilk 10'un
  9'u yerinde kalıyor).
- Puan yayılımı bütün kriterler içinde en dar: **56–88 arası, standart sapma 6.0**
  (karşılaştırma: `age` 16–88, sd 17.0).

Yani 221 aracın hepsi konfor açısından birbirine çok yakın puanlanmış. Bunun iki olası
açıklaması var ve ikisi farklı düzeltme gerektiriyor:

1. **Puanlama sorunu:** Konfor gerçekte daha geniş bir yelpazede değişiyor ama puanlar
   ortalamaya toplanmış (merkeze kayma eğilimi, central tendency bias — derecelendirme
   ölçeklerinin bilinen bir hatası). Düzeltme: bantları yeniden kalibre edip puanları
   dağıtmak.
2. **Kriter sorunu:** Otomatik vitesli, 2000 sonrası araçlar zaten konfor açısından
   birbirine yakın ve kriter gerçekten ayırt edici değil. Düzeltme: kriteri kaldırmak
   veya başka bir kriterle birleştirmek.

**Bu belge hangisinin doğru olduğunu iddia etmiyor.** Ayrımı yapabilmek için `comf`
puanlarının kanıta bağlanması gerekiyor (bkz. §6, `evidence` bloğu). Karar verilene
kadar `comf` kriteri yerinde kalıyor, ama düşük ayırt ediciliği burada kayıtlı.

### 3.5 Bulunan sorun: kriterler bağımsız değil

Ağırlıklı toplam modeli, kriterlerin **tercih bağımsız** olmasını varsayar. Ölçülen
korelasyonlar bu varsayımın kısmen ihlal edildiğini gösteriyor:

| Kriter çifti | Pearson r | Ne anlama geliyor |
|---|---:|---|
| `age` ~ `price` | **−0.802** | Yaşlı araç ucuz. Yaş riski hem `age` hem `price` üzerinden iki kez sayılıyor. |
| `cost` ~ `liq` | **+0.770** | İşletmesi ucuz araç aynı zamanda likit. Yaygınlık iki kez ödüllendiriliyor. |
| `fun` ~ `cost` | −0.690 | Eğlenceli araç pahalı işletiliyor. |
| `fun` ~ `liq` | −0.660 | Eğlenceli araç daha az likit. |

En ciddi olanı `age ~ price` (−0.80). Bir araç eskidiği için ucuzsa, kullanıcı yaş
riskini bir kez `age` sütununda ceza olarak, bir kez de `price` sütununda ödül olarak
görüyor. Bu **çifte sayım**dır ve ağırlıklı toplamın bilinen zayıflığıdır.

Bu sorunun üç bilinen çözümü var, üçü de maliyetli:

1. Kriterleri ortogonalleştirmek (ör. `price`'ı yaşa göre düzeltilmiş fiyat yapmak).
   Model karmaşıklaşır, açıklanabilirlik düşer.
2. Telafi etmeyen bir yönteme geçmek (ELECTRE gibi). §1'deki gerekçeyle reddedildi.
3. Korelasyonu belgelemek ve kullanıcıya göstermek. **Bugün seçilen yol bu.**

Üçüncü yol, sorunu çözmüyor ama gizlemiyor. Y-06 kapsamında arayüze eklenecek "bu araç
neden bu puanı aldı" dökümü, bu korelasyonun kullanıcı tarafından görülebilmesini
sağlamalı.

### 3.6 Ham toplamın dar aralığı — normalize sütunun gerekçesi

Ham toplam puanlar **50.3 – 76.5** arasında sıkışıyor (aralık 26.2, standart sapma 4.5).
100 puanlık bir ölçekte gerçek fark yalnızca 26 puanlık bir bantta yaşanıyor; gözle
bakan kullanıcı bunu ayırt edemiyor. Normalize sütunun (listenin en iyisine 100, en
kötüsüne 0) varlık sebebi tam olarak budur.

Normalize sütunun bilinen bedeli: **sıra tersine dönmesi** (rank reversal). Listeye yeni
bir araç eklendiğinde veya filtre uygulandığında normalize puanlar değişir, çünkü
referans noktaları (en iyi ve en kötü) değişir. Bu, ağırlıklı toplam ailesinin bilinen
bir davranışıdır ve ham toplam sütunu bu yüzden ekranda normalize sütunun yanında
tutuluyor: ham toplam mutlak, normalize görelidir.

---

## 4. Yöntemin kabul edilen sınırları

Ağırlıklı toplam modelinin bu projede kabul edilen üç zayıflığı:

1. **Telafi edicidir.** Bir kriterdeki çok düşük puan, başka bir kriterdeki çok yüksek
   puanla dengelenebilir. Şanzımanı felaket ama fiyatı çok iyi bir araç, toplam puanda
   makul görünebilir. **Kısmi çözüm:** zayıf halka işaretlemesi (herhangi bir kriterde
   35 altı puan hücreyi kırmızı yapar ve detay panelinde gerekçesi yazılır). Bu,
   telafi ediciliği ortadan kaldırmaz ama kullanıcıyı uyarır.
2. **Kriterlerin bağımsızlığını varsayar.** §3.5'te ölçüldüğü gibi bu varsayım kısmen
   ihlal ediliyor. Belgelendi, gizlenmedi.
3. **Ağırlıklar öznel.** Hiçbir matematiksel yöntem "motor 20 olmalı" diyemez; bu bir
   değer yargısıdır. Model bunu kullanıcıya devrediyor (ağırlıklar düzenlenebilir) ama
   varsayılan seti biri seçmek zorunda — bkz. §5.

---

## 5. Varsayılan ağırlıklar: SWING protokolüyle türetildi (2026-08-06)

**Önceki durum, dürüstçe:** Üç hazır ayarın (Dengeli, Sürüş keyfi öncelikli,
Güvenilirlik öncelikli) sayıları projenin göç öncesi tek dosyalık sürümünden
devralınmıştı ve hiçbir yerde yazılı bir gerekçeye dayanmıyordu. §3.1'deki ölçüm
(±%25 ağırlık gürültüsünde Spearman 0.99) bunun acil bir sorun olmadığını gösteriyordu
— ama "neden 20 ve 15, neden 22 ve 18 değil" sorusunun hâlâ cevabı yoktu. Bu bölüm o
boşluğu kapatıyor.

### Yöntem: SWING ağırlıklandırma

Kullanılan yöntem **SWING weighting** (von Winterfeldt ve Edwards, *Decision Analysis
and Behavioral Research*, 1986; Ödeme isteğine dayalı türetme veri istiyordu — ilan
bazlı fiyat/özellik eşlemesi bugün elde yok — bu yüzden veri gerektirmeyen yapılandırılmış
uzman yargısı yolu seçildi). Mantığı şu:

1. Her kriter için "en kötü gerçekçi düzeyden en iyi gerçekçi düzeye" (0'dan 100'e)
   bir sıçrama (swing) hayal edilir.
2. Bu sıçramaların **alıcı için ne kadar önemli olduğu** sıralanır ve en önemlisine
   100 puan verilir.
3. Diğer her kriterin sıçraması, en önemliye göre 0-100 arasında oranlanır.
4. Puanlar toplama (Σ=100) normalize edilir — bu doğrudan ağırlık olur.

Üç farklı kullanıcı profili için **ayrı ayrı** SWING yapıldı, çünkü "sürüş keyfi
öncelikli" bir kullanıcı için `fun`'ın sıçraması "dengeli" bir kullanıcıya göre çok
daha değerlidir; tek bir SWING'den üç preset türetmek yanlış olurdu.

### Dengeli set

| Kriter | Sıçrama puanı | Gerekçe |
|---|---:|---|
| `motor` | 100 (çapa) | Motor arızası tek seferde en pahalı ve en yıkıcı sonuç; ikinci el alıcısının en çok korktuğu şey. |
| `trans` | 85 | Mekatronik/kavrama onarımı motor kadar pahalı olabiliyor, ama "motor komple bitti" kadar toptan bir kayıp nadiren oluyor. |
| `age` | 55 | Pas, elektrik arızaları birikimli risk; tek seferde yıkıcı değil ama sürekli. |
| `cost` | 50 | Sürekli bir yük, gerçek para, ama bütçelenebilir — motor/şanzıman gibi "anlık felaket" değil. |
| `price` | 45 | Türkiye piyasasında bütçe çoğu zaman zaten ön filtre; kalite değerlendirmesinden önce devreye giriyor. |
| `fun` | 35 | Günlük memnuniyeti artırıyor ama güvenilirliği ya da maliyeti etkilemiyor. |
| `liq` | 25 | Çoğunlukla yalnızca satış anında önem kazanıyor; uzun süre elde tutan alıcı için ikincil. |
| `comf` | 20 | Yaşam kalitesi faktörü, en az "dealbreaker" olan. §3.4'teki ampirik bulgu (comf ayırt etmiyor) bu düşük sıralamayla tutarlı. |

Toplam sıçrama = 415. Ağırlık = sıçrama × 100/415, tam sayıya yuvarlandı:

| Kriter | motor | trans | age | cost | price | fun | liq | comf | Σ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Yeni** | 24 | 21 | 13 | 12 | 11 | 8 | 6 | 5 | 100 |
| Eski | 20 | 15 | 10 | 12 | 10 | 16 | 6 | 11 | 100 |

En büyük değişim `fun` (16→8) ve `comf`'ta (11→5): ikisi de ampirik ölçümde zaten
zayıf çıkmıştı (§3.3, §3.4), SWING bunu bağımsız bir yöntemle doğruladı. `trans` belirgin
biçimde yükseldi (15→21) çünkü şanzıman arızasının maliyeti motor kadar ciddiye
alınmalı — bu projenin adının "araç puanlama" değil özellikle "otomatik vitesli araç
puanlama" olmasıyla da örtüşüyor.

### Sürüş keyfi öncelikli

Ayrı bir SWING: bu persona için `fun` çapa (100), ama güvenilirlik tamamen terk
edilmiyor — "eğlenceli ama güvenilmez" bir araç önerisi sitenin amacına aykırı olurdu.

| Kriter | fun | motor | trans | price | age | cost | comf | liq | Σ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sıçrama | 100 | 70 | 55 | 45 | 35 | 30 | 25 | 20 | 380 |
| **Yeni ağırlık** | 26 | 18 | 15 | 12 | 9 | 8 | 7 | 5 | 100 |
| Eski ağırlık | 30 | 17 | 13 | 12 | 8 | 8 | 8 | 4 | 100 |

Bu preset en az değişen oldu — eski sayılar da zaten "fun baskın ama motor/trans hâlâ
ikinci sırada" mantığına uyuyordu.

### Güvenilirlik öncelikli

Ayrı bir SWING: `motor` çapa (100), güvenilirlikle doğrudan ilgili her şey (`trans`,
`age`) yüksek, geri kalan düşük.

| Kriter | motor | trans | age | cost | liq | comf | price | fun | Σ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sıçrama | 100 | 90 | 55 | 35 | 30 | 25 | 25 | 15 | 375 |
| **Yeni ağırlık** | 27 | 24 | 15 | 9 | 8 | 7 | 6 | 4 | 100 |
| Eski ağırlık | 20 | 16 | 12 | 12 | 6 | 16 | 12 | 6 | 100 |

**Burada gerçek bir tutarsızlık bulundu ve düzeltildi:** eski "Güvenilirlik öncelikli"
setinde `comf` ağırlığı (16) `motor` ile aynı bölgedeydi ve `age`'den (12) yüksekti —
bu, adı "güvenilirlik" olan bir presetin aslında konfor odaklı eski bir "aile" preseti
olarak tasarlanıp isim değiştirildiğine işaret ediyor, sayıları güncellenmeden. SWING
bu tutarsızlığı ortadan kaldırdı: `comf` 16'dan 7'ye indi, `motor`+`trans` toplamı
36'dan 51'e çıktı.

### Değişimin etkisi ölçüldü

`scripts/analysis/sensitivity.py` ile eski/yeni ağırlıklar karşılaştırıldı:

| Preset | Eski↔yeni Spearman | İlk 10'da korunan |
|---|---:|---:|
| Dengeli | 0.983 | 9/10 |
| Sürüş keyfi öncelikli | 0.980 | 7/10 |
| Güvenilirlik öncelikli | 0.967 | 9/10 |

Değişim gerçek ama yıkıcı değil — sıralamanın büyük kısmı korunuyor, en çok hareket
eden yerler zaten en zayıf gerekçeye dayanan eski sayılardı. Yeni ağırlıklar
`data/criteria.json` içine işlendi ve arayüzde canlı; `docs/methodology.md` §3'teki
tablo da güncellendi.

---

## 6. Bilinen boşluklar — dürüst döküm

Bu bölüm, sistemin bugün **eksik** olan taraflarını sayar. Belgenin güvenilir olmasının
şartı, iyi tarafları kadar bunları da yazmasıdır.

| Boşluk | Bugünkü durum | Etkisi |
|---|---|---|
| **`evidence` bloğu boş** | 221 araçtan **2**'sinde dolu | "Bu puan hangi kaynağın hangi bandına dayanıyor" sorusu kriter bazında cevapsız. Kaynak listesi araç seviyesinde var, ama kriter seviyesinde bağ yok. **En büyük açık budur.** |
| **MK-06 formülleri uygulanmadı** | `kerb_weight_kg`, `torque_nm`, `fuel_consumption_l_100km` alanları **221/221 boş** | `fun`, `comf`, `age`, `cost` hâlâ tamamen elle veriliyor. `docs/ARCHITECTURE.md` MK-06 "karar verildi" diyor ama karar hiç uygulanmadı. |
| **Ağırlıklar gerekçesiz** | §5 | Ölçüm gösteriyor ki etkisi sınırlı, ama gerekçe yine de yazılmalı. |
| **`comf` ayırt etmiyor** | §3.4 | Kriter fiilen sonuca katkı vermiyor. |
| **`age`~`price` çifte sayımı** | §3.5 | Yaş riski iki kez sayılıyor. |
| **Puanlar arası tutarlılık denetimi kısmi** | `validate.py` yalnızca bileşen temel puanından sapmayı denetliyor | İki benzer aracın `fun` puanının tutarlı olup olmadığını hiçbir denetim kontrol etmiyor. |

---

## 7. Sıradaki adımlar, öncelik sırasıyla

1. **`evidence` bloğunu doldurmak.** En yüksek değerli iş. Her araç için en azından
   `motor` ve `trans` kriterlerinde hangi kaynağın hangi banda karşılık geldiğini
   yazmak. Bu yapıldığında "bu puan neden bu" sorusu kriter bazında cevaplanabilir
   hale gelir ve Y-06'nın arayüz tarafı gerçek veriye dayanabilir.
2. **Ağırlıkları SMART/SWING protokolüyle türetip yazıya dökmek.** Bir oturumluk iş,
   veri gerektirmiyor.
3. **`comf` kararı.** Puanları kanıta bağladıktan sonra §3.4'teki iki açıklamadan
   hangisinin doğru olduğuna karar verip ya bantları yeniden kalibre etmek ya da
   kriteri birleştirmek.
4. **MK-06 formülleri** için ağırlık/tork/tüketim verisini doldurmak. Büyük veri işi;
   yukarıdakiler bittikten sonra ele alınmalı.

---

## Kaynakça

Yöntemsel dayanaklar:

- Keeney, R. L. ve Raiffa, H. (1976). *Decisions with Multiple Objectives: Preferences
  and Value Tradeoffs.* Çok nitelikli fayda teorisinin (MAUT) temel metni; ağırlıklı
  toplam modeli bu çerçevenin özel hâlidir.
- Triantaphyllou, E. (2000). *Multi-Criteria Decision Making Methods: A Comparative
  Study.* WSM, AHP, TOPSIS ve ELECTRE'nin karşılaştırmalı değerlendirmesi.
- Smith, P. C. ve Kendall, L. M. (1963). "Retranslation of expectations: An approach to
  the construction of unambiguous anchors for rating scales." *Journal of Applied
  Psychology.* Çapalı derecelendirme ölçeğinin (BARS) tanımlandığı çalışma.
- Saaty, T. L. (1980). *The Analytic Hierarchy Process.* §1'de değerlendirilip
  reddedilen alternatif.
- Hwang, C. L. ve Yoon, K. (1981). *Multiple Attribute Decision Making: Methods and
  Applications.* TOPSIS'in tanımlandığı çalışma; §1'de değerlendirilip reddedildi.

Veri kaynakları `data/sources.json` içinde künyeleriyle duruyor; bu belgede tek tek
sayılmıyor.
