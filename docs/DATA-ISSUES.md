# Bilinen veri sorunları

Göç sırasında ve ilk denetimde bulunanlar. Her madde ya düzeltilecek ya bilinçli
istisna olarak kapatılacak. `validate.py` çıktısı bu listenin canlı hali;
buradaki kayıtlar bağlam ve karar gerekçesi içindir.

---

## D-01 · İki araçta fazladan puan değeri (DÜZELTİLDİ — veri kaybıyla)

**Durum:** Kapatıldı, ama bir karar not edilmeli.

Eski HTML'de iki aracın `s` dizisi yedi yerine **dokuz** elemanlıydı:

| Araç | Dizi | Kullanılan | Sessizce atılan |
|---|---|---|---|
| Renault Megane 1.6 dCi 130 | `[70,44,54,80,68,74,86,84,72]` | ilk 7 | `84, 72` |
| Renault Clio 4 1.5 dCi | `[68,44,46,78,62,84,86,80,58]` | ilk 7 | `80, 58` |

Tarayıcı kodu `SCORED.forEach((k,j) => c.S[k] = c.s[j])` ile yalnızca ilk yediyi
okuduğu için fazlalıklar **zaten kullanılmıyordu** — yani sayfadaki puanlar yanlış
değildi, sadece dosyada ölü veri vardı. Göçte ilk yedi korundu.

Fazladan iki değerin ne olduğu bilinmiyor; muhtemelen dokuz kriterli eski sürümden
kalma ya da araştırma turunda eklenmiş taslak. **Bu tam olarak şema doğrulamasının
yakaladığı hata türü** ve tek dosyalık sürümde görünmez kalmıştı.

---

## D-02 · "Kaynaklı" etiketi tek kaynağa dayanıyor (AÇIK)

`verified` işaretli 70 aracın **38'i** tek bir kaynağa dayanıyor. Metodoloji
"en az iki bağımsız kaynak" diyor; etiketleme bu politika yazılmadan önce yapıldı.

Karar gerekiyor: ya bu 38 araç `partial`'a çekilecek, ya ikinci kaynak bulunacak.
Faz 2'nin ilk işi.

---

## D-03 · Tek kaynağa aşırı yoğunlaşma (AÇIK)

| Kaynak | Kaç aracı taşıyor |
|---|---:|
| `trbox` (araclo.com şanzıman rehberi) | **36** |
| `om61x` (Wikipedia / cars-expert) | **13** |

`trbox` tek bir blog yazısı ve listedeki araçların dörtte birinin şanzıman
değerlendirmesini tek başına taşıyor. Bu yazı yanlışsa ya da çürürse 36 araç birden
dayanaksız kalır. Tek noktadan bağımlılık; kırılması gerekiyor.

---

## D-04 · "Ön değerlendirme" etiketli ama kaynağı olan araçlar (AÇIK)

27 araç `preliminary` işaretli olmasına rağmen `sources` alanı dolu. İkisinden biri
yanlış: ya araç aslında araştırılmış ve etiket güncellenmemiş, ya kaynak gerçekten
o aracı desteklemiyor da genel bir referans olarak eklenmiş.

İkincisi daha muhtemel — `trbox` gibi genel şanzıman rehberleri birçok araca
"arka plan" olarak iliştirilmiş görünüyor. Kaynak-iddia ilişkisi kurulunca çözülecek.

---

## D-05 · Yetim kaynaklar (AÇIK — muhtemelen zararsız)

Hiçbir araca bağlı olmayan 13 kaynak var:

`andcetin_dct_tucson`, `andcetin_dq200`, `araclo_c5aircross`, `dhaber_qashqai13`,
`dhaber_sportage_dct`, `erenservis_eat8`, `hech_koleos`, `kronikyorum_qashqai`,
`mkt`, `motor1_psa_suv_eat`, `otomobilforum_sanziman`, `sikayetvar_qashqai`,
`sikayetvar_tucson_dct`

Çoğu SUV/MPV temizliğinden kalma (Tucson, Qashqai, Sportage, C5 Aircross, Grandland,
Koleos). Bunlar gerçek araştırma çıktısı ve **silinmemeli** — SUV kararı bir gün
gözden geçirilirse hazır duruyorlar. `build.py` bunları sayfaya basmıyor, yalnızca
arşivde tutuyor.

`mkt` (Türkiye ortalama ikinci el fiyatı) ve `otomobilforum_sanziman` (genel şanzıman
karşılaştırması) ise hâlâ geçerli ama hiçbir araca bağlanmamış genel referanslar.

---

## D-06 · Kapsam kuralı dışında kalan araçlar (AÇIK)

11 araç, listenin kendi koyduğu "en az 110 bg, 1998 sonrası" kuralının dışında:

- **110 bg'nin altı:** Renault Clio 4 1.5 dCi (90 bg), Hyundai Elantra XD (105 bg),
  Kia Cerato eski nesil (105 bg)
- **1998 öncesi:** BMW E36 (1995), Opel Vectra B (1995), Mercedes W202 (1993),
  Audi A4 B5 (1994), Skoda Octavia 1 (1996), Peugeot 406 (1995), Mazda 626 (1997),
  Saab 9-3/9-5 (1997)

Bazıları zaten `tag` alanında "sınır altı" diye işaretlenmiş, yani bilinçli. Ama kural
ya kapsayıcı olacak şekilde gevşetilmeli ya bu araçlar çıkarılmalı — şu anki hali
kuralı anlamsız kılıyor.

---

## D-07 · Kanıtsız zayıf halka (AÇIK)

4 araçta 35 altı (eleyici) puan var ama hiç kaynak yok. Bir aracı listeden fiilen
eleyen bir puanın kanıtsız verilmemesi gerekiyor. Bunlar önceliklendirilmiş
araştırma listesinin başına alınmalı.

---

## D-08 · Ağırlık seti belgeyle uyuşmazlığı (KAPATILDI)

Aktarım dokümanında varsayılan set `motor:18, trans:13, ...` (toplam 96) diye
yazılmıştı; çalışan HTML'de `motor:20, trans:15, ...` (toplam 100). Kodda olan
doğru kabul edildi ve `data/criteria.json` içine o yazıldı.
