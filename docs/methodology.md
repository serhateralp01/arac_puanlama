# Metodoloji

Bu belge puanların **nasıl** verildiğini tanımlar. Amaç, aynı kanıtın aynı puanı
üretmesi — yani tekrarlanabilirlik. Bugünkü durumda bu hedefin bir kısmı sağlanmış
(kriter tanımları net ve birbirini dışlıyor), bir kısmı henüz sağlanmamış (puan
bantları yazılı değil). Eksik olan yerler açıkça işaretlendi.

---

## 1. Kapsam kuralları

Listeye giren araç şu üç şartı sağlar:

- **1998 ve sonrası** model yılı,
- **en az 110 beygir**,
- **otomatik şanzıman** (robotlu yarı otomatik dahil, manuel hariç),
- Türkiye ikinci el piyasasında **bulunabilir** olması.

SUV ve MPV gövdeler bilinçli olarak dışarıda tutuluyor. Sedan, hatchback, station
wagon ve coupe listeleniyor.

Kapsam kuralı ihlalleri `validate.py` tarafından uyarı olarak raporlanıyor; şu an
11 araç sınırda veya dışında (ör. 90 bg Clio 4, 105 bg Elantra XD). Bunlar bilinçli
istisnalar mı yoksa temizlenecek mi — Faz 2'de karara bağlanacak.

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

| Etiket | Anlamı | Politika |
|---|---|---|
| `verified` | En az iki bağımsız kaynakla doğrulandı | `MIN_SOURCES_FOR_VERIFIED = 2` |
| `partial` | Kaynak var ama Türkiye pazarına özel değil | — |
| `preliminary` | Henüz araştırılmadı, ön puan | Kaynağı olmamalı |

**Bugünkü ihlal:** 38 araç `verified` işaretli olmasına rağmen tek kaynağa dayanıyor,
27 araç `preliminary` olmasına rağmen kaynağı var. Etiketleme, politika yazılmadan
önce yapıldığı için tutarsız. Faz 2'de ya etiketler ya politika düzeltilecek.

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

## 7. Eksik olan: puan bantları

**Bu bölüm henüz yazılmadı ve projenin en büyük metodolojik açığı.**

Şu an puanlar sezgisel veriliyor ("bu bana 70 gibi geliyor"). Yazılı, tekrar
uygulanabilir bir eşik seti yok; aynı kanıt farklı zamanlarda farklı puana yol
açabilir. `validate.py` bunu `puan-bandi-yok` kuralıyla yedi kriterin hepsi için
raporluyor.

Hedeflenen biçim — her kriter için "şu kanıt varsa şu aralık":

> **`trans` için taslak:**
> - **90–100** — İki bağımsız kaynakta kronik arıza kaydı yok, kutu tipi tork konvertörü.
> - **70–89** — Bilinen ama yönetilebilir bakım kalemi var (ör. 60 bin km'de yağ değişimi şart).
> - **50–69** — Tekrarlayan şikayet örüntüsü var ama felaket değil, tamiri makul maliyetli.
> - **30–49** — Düşük kilometrede ağır arıza vakaları, birden fazla kaynakta doğrulanmış.
> - **0–29** — Yapısal tasarım hatası, sınıfının en kötüsü, tamiri araç değerine yakın.

Bantlar `data/criteria.json` içindeki `bands` alanına yazılacak (şu an `null`) ve her
araç kaydındaki opsiyonel `evidence` bloğunda hangi bandın hangi kaynakla uygulandığı
tutulacak. Şema bu alanları şimdiden tanımlıyor.

Ayrıntılı plan: [PLAN.md](PLAN.md).
