# Y-01 hedef listesi — marka → model → yıl/motor/şanzıman

Bu belge, `docs/ROADMAP.md`'deki Y-01 maddesinin **kaynaklı araştırmadan önceki seçenek
listesi**. Kullanıcının istediği yöntem şu: önce markalar geliştirilir, sonra o
markaların modelleri, sonra o modellerin yıl bazında motor/şanzıman kombinasyonları
eşleştirilir — ve bütün bunlar kaynaklı araştırma (WebSearch, gerçek şikayet/forum
taraması, `data/queue/` akışı) başlamadan önce bir seçenek listesi olarak sunulur.

**Bu belgedeki hiçbir satır henüz kaynaklanmadı.** Motor/şanzıman eşleşmeleri genel
otomotiv bilgisine dayanıyor, model yılları ve güç rakamları yaklaşık. Kullanıcı
onayladıktan sonra her aday için gerçek kaynak aranacak, `data/queue/` üzerinden
işlenecek ve ancak öyle `data/` içine girecek — CLAUDE.md §1 ve MK-05 kuralı gereği.

Her aday üç etikattan biriyle işaretli:

- 🟢 **Mevcut bileşen** — motor ve şanzıman ailesi `data/engines.json` /
  `data/transmissions.json` içinde zaten var, zaten temel puanlı ve kaynaklı. Araç
  eklemek düşük riskli; yalnızca araca özgü kaynak aranması yeterli (Y-01'in ilk
  turundaki 6 araç gibi).
- 🟡 **Kısmi eşleşme** — motor veya şanzımandan biri mevcut ailelerden birine oturuyor
  ama diğeri yeni araştırma istiyor.
- 🔴 **Yeni bileşen gerekiyor** — hem motor hem şanzıman için önce
  `data/engines.json` / `data/transmissions.json`'a yeni kayıt açılmalı, temel puanı
  ve kaynağı verilmeli. CLAUDE.md §2 ("ters sırada yapılırsa depo doğrulamadan
  geçmez") gereği araç bundan önce eklenemez.
- ⛔ **Şema kararı bekliyor** — hibrit/elektrikli araçlar. `fuel` alanı bugün yalnızca
  `Dizel`/`Benzin` kabul ediyor; bu markalar/modeller Y-01 madde 3'teki MK kaydı
  yazılmadan hiç ele alınmamalı.

---

## A) Mevcut markalarda model genişletmesi — çoğu 🟢

Bu markalar listede zaten var ama model çeşitliliği dar. Motor/şanzıman aileleri
büyük ölçüde zaten kayıtlı olduğu için en ucuz genişleme yolu burası.

### VAG (26 araç var) — SUV ve daha yeni kuşak eksik

| Model | Yıl (tahmini) | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Skoda Kodiaq 1.4 TSI | 2017-2021 | `vag-ea211` (mevcut) | `vag-dq250` (mevcut) | 🟢 |
| Skoda Karoq 1.6 TDI | 2018-2021 | `vag-ea288` (mevcut, 1.6 TDI) | `vag-dq200` (mevcut, kuru) | 🟢 |
| VW T-Roc 1.5 TSI | 2018-2021 | yeni (EA211 evo 1.5 TSI ACT, mevcut `vag-ea211` 1.4 TSI'dan farklı revizyon — MK-08 dikkatiyle değerlendirilmeli) | `vag-dq200` (mevcut) | 🟡 |
| Audi Q3 (F3) 2.0 TDI | 2018-2021 | `vag-ea288` (mevcut, 2.0 TDI) | `vag-dq250` (mevcut) | 🟢 |
| Seat Ateca 1.6 TDI | 2017-2021 | `vag-ea288` (mevcut) | `vag-dq200` (mevcut) | 🟢 |
| VW Polo 6 1.0 TSI DSG | 2018-2021 | yeni (EA211 1.0 TSI 3 silindir, listede yok) | `vag-dq200` (mevcut) | 🟡 |

### PSA (14 araç var) — SUV kuşağı hiç yok

| Model | Yıl (tahmini) | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Peugeot 2008 (1. nesil) 1.6 THP | 2016-2019 | `psa-ep6-thp` (mevcut) | `psa-al4` (mevcut) | 🟢 |
| Peugeot 3008 (2. nesil) 1.6 BlueHDi | 2017-2021 | `psa-dv6` (mevcut, ama 1.5 BlueHDi'den farklı, dikkat) | `aisin-eat6` (mevcut, "Grandland X EAT6" örneğiyle zaten kaynaklı) | 🟡 |
| Opel Grandland X 1.6 BlueHDi | 2018-2021 | `psa-dv6` (mevcut) | `aisin-eat6` (mevcut — depoda zaten yetim kaynak `motor1_psa_suv_eat` bunu doğruluyor) | 🟢 |
| Citroën C5 Aircross 1.5 BlueHDi | 2019-2022 | yeni (1.5 BlueHDi = DV5RC, mevcut `psa-dv6`'dan [1.6] farklı) | yeni (EAT8, depoda 3 yetim kaynak zaten var: `araclo_c5aircross`, `erenservis_eat8`, `motor1_psa_suv_eat`) | 🟡 (bileşenler için kanıt zaten kısmen elde) |
| Opel Crossland X 1.2 Turbo | 2017-2020 | yeni (PureTech 3 silindir, listede yok) | `psa-etg` veya manuel-ağırlıklı, dikkatli seçilmeli | 🔴 |

### Renault (9 araç var, Duster/Koleos yeni eklendi)

| Model | Yıl (tahmini) | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Renault Captur 1.5 dCi EDC | 2017-2020 | `renault-k9k` (mevcut) | `renault-edc-kuru` (mevcut) | 🟢 |
| Renault Kadjar 1.5 dCi EDC | 2016-2020 | `renault-k9k` (mevcut) | `renault-edc-kuru` (mevcut) | 🟢 |
| Renault Megane 4 1.5 dCi EDC | 2016-2020 | `renault-k9k` (mevcut) | `renault-edc-kuru` (mevcut) | 🟢 |
| Renault Clio 5 1.0 TCe EDC | 2019-2022 | yeni (H4Bt/H4D 1.0 TCe 3 silindir, listede yok) | `renault-edc-kuru` (mevcut) | 🟡 |

### Japon grubu (33 araç var) — SUV ve daha yeni kuşak eksik

| Model | Yıl (tahmini) | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Kia Sportage (QL) 1.6 CRDi 7DCT | 2016-2020 | `hyundai-u2-16` (mevcut) | `hyundai-7dct` (mevcut — depoda yetim kaynak `dhaber_sportage_dct` zaten var) | 🟢 |
| Kia Ceed SW 1.6 CRDi | 2016-2019 | `hyundai-u2-16` (mevcut) | `hyundai-7dct` (mevcut) | 🟢 |
| Hyundai i30 (PD) 1.6 CRDi 7DCT | 2017-2020 | `hyundai-u2-16` (mevcut) | `hyundai-7dct` (mevcut) | 🟢 |
| Toyota C-HR 1.2 Turbo | 2017-2020 | yeni (8NR-FTS 1.2 turbo, listede yok) | `toyota-multidrive` (mevcut CVT, ama C-HR gerçek CVT değil — doğrulanmalı) | 🟡 |
| Toyota Corolla (E210) 1.6 Benzin CVT | 2019-2022 | `toyota-zr` (mevcut, 1.6) | `toyota-multidrive` (mevcut) | 🟢 |
| Mazda CX-5 2.0 Skyactiv-G | 2017-2021 | `mazda-lf` (mevcut, 2.0) | yeni (Mazda'nın kendi 6 ileri otomatiği, listede yok) | 🟡 |
| Nissan Juke 1.6 CVT | 2016-2019 (liste zaten "Nissan Juke 1.6" adıyla var — bu satır olası kopya, kontrol edilmeli) | — | — | ⚠️ tekrar riski |

### Ford (7 araç var) — dar

| Model | Yıl (tahmini) | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Ford Kuga (3. nesil) 1.5 EcoBoost | 2019-2022 | `ford-ecoboost-15` (mevcut) | yeni (8F35 8 ileri otomatik, listede yok) | 🟡 |
| Ford Puma 1.0 EcoBoost Mild Hybrid | 2019-2022 | mild hibrit — ⛔ şema kararı gerekebilir | — | ⛔/🟡 sınırda |
| Ford Focus 4 1.5 EcoBlue | 2018-2021 | yeni (1.5 EcoBlue, listede yok) | `getrag-6dct450` (mevcut ıslak DCT) | 🟡 |

---

## B) Yeni markalar — düşük riskli adaylar (🟢/🟡)

### MINI (R56 kuşağı, 2006-2013) — 🟢 sürpriz eşleşme

MINI R56'nın (Cooper / Cooper S) motorları BMW-PSA ortak geliştirmesi "Prince" ailesi;
bu aile listede **zaten kayıtlı** (`psa-ep6-vti` atmosferik, `psa-ep6-thp` turbo —
tedarikçi alanı zaten "BMW / PSA" yazıyor). Otomatik şanzıman Aisin 6 ileri tork
konvertörü, listede `aisin-af40` veya `aisin-eat6` ailelerinden biriyle eşleşme
ihtimali yüksek (doğrulanmalı).

| Model | Yıl | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| MINI Cooper (R56) 1.6 | 2007-2013 | `psa-ep6-vti` (mevcut) | Aisin 6 ileri (mevcut ailelerden biri, doğrulanmalı) | 🟢 |
| MINI Cooper S (R56) 1.6 Turbo | 2007-2013 | `psa-ep6-thp` (mevcut) | Aisin 6 ileri (mevcut ailelerden biri, doğrulanmalı) | 🟢 |

### MINI (F56 kuşağı, 2014+) — 🔴 yeni bileşen

BMW'nin kendi B38/B48 motorlarına geçildi, listede yok. Şanzıman Aisin 6 ileri veya
Getrag 7 ileri ıslak DCT (bu ikincisi `getrag-7dct300`'e benziyor ama doğrulanmalı).

| Model | Yıl | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| MINI Cooper (F56) 1.5 | 2014-2021 | yeni (B38) | Aisin 6 ileri veya `getrag-7dct300` (doğrulanmalı) | 🔴/🟡 |
| MINI Countryman (F60) 1.5/2.0 | 2017-2021 | yeni (B38/B48) | Aisin 6 ileri veya ıslak DCT | 🔴 |

### Cupra — 🟡 kısmi

VAG platformu; şanzıman `vag-s-tronic-islak` (DQ381, mevcut) ile büyük ihtimalle
eşleşiyor. Motor EA888 evo4 (2.0 TSI), listedeki `vag-ea888` **eski revizyonu**
temsil ediyor (base_score 46, muhtemelen Golf Mk5/6 dönemi sorunları) — MK-08
gerekçesiyle doğrudan reddedilmeli, ayrı bir aile açılmalı.

| Model | Yıl | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Cupra Formentor 2.0 TSI DSG | 2020-2023 | yeni (EA888 evo4, mevcut `vag-ea888`'den ayrı) | `vag-s-tronic-islak` (mevcut) | 🟡 |
| Cupra Leon 2.0 TSI DSG | 2020-2023 | aynı | `vag-s-tronic-islak` (mevcut) | 🟡 |

---

## C) Yeni markalar — yüksek efor (🔴, tamamen yeni bileşen araştırması)

### Subaru

AWD standart olduğu için `drivetrain: Dört çeker` çeşitliliğine katkısı büyük, ama
boxer motor ve Lineartronic CVT listede hiç yok.

| Model | Yıl | Motor/şanzıman | Etiket |
|---|---|---|---|
| Subaru Forester 2.0i Lineartronic | 2016-2020 | boxer 2.0 + Subaru CVT, ikisi de yeni | 🔴 |
| Subaru XV 1.6i Lineartronic | 2017-2021 | boxer 1.6 + Subaru CVT, ikisi de yeni | 🔴 |

### MG

Türkiye'de yeni ve büyüyen bir marka; çoğu motor Çin pazarına özgü, listede
karşılığı yok. Bazı modeller PHEV/EV, ⛔ şema kararı gerekebilir.

| Model | Yıl | Motor/şanzıman | Etiket |
|---|---|---|---|
| MG ZS 1.5 (benzinli, hibrit olmayan) | 2021-2024 | yeni motor + yeni CVT/otomatik | 🔴 |
| MG5 (elektrikli) | — | ⛔ EV, şema kararı gerekiyor | ⛔ |
| MG HS PHEV | — | ⛔ plug-in hibrit, şema kararı gerekiyor | ⛔ |

---

## D) Şema kararı bekleyenler — ⛔ önce MK kaydı gerekiyor

Bunlar Y-01 madde 3'ün konusu: `fuel` alanı bugün yalnızca `Dizel`/`Benzin` kabul
ediyor. Bu markalar/gövdeler eklenmeden önce `docs/ARCHITECTURE.md`'ye hibrit/elektrikli
araçların `cost` ve `trans` kriterini nasıl etkilediğini tanımlayan bir MK kaydı
yazılmalı; bu, geri alınması pahalı bir karar olduğu için atlanmamalı.

- **Lexus** — Türkiye'de satılan hemen hemen bütün modeller (CT200h, IS300h, NX300h,
  ES300h) tam hibrit. Şema kararı olmadan hiç ele alınmamalı.
- **Togg T10X** — tam elektrikli, geleneksel şanzıman kavramı yok (`transmission_type`
  enum'una da uymuyor). Şema kararı hibritten de büyük bir karar.
- **Chery / BYD** — çoğunlukla EV veya PHEV; aynı blok.
- **Toyota/Honda hibrit varyantları** (Corolla Hybrid, C-HR Hybrid, CR-V Hybrid) —
  marka listede var ama hibrit gövdeler aynı bloğa giriyor.

---

## Öneri: hangi sırayla ilerlenmeli

Kullanıcının "önce marka, sonra model, sonra yıl/motor/şanzıman" yöntemine göre, risk
ve efor dengesi şöyle kurulabilir:

1. **A bölümü (mevcut marka genişletmesi, 🟢 satırlar)** — en ucuz, en hızlı. Tek
   başına 2016+ ve SUV sayısını hızla yükseltir; hiç yeni bileşen gerektirmiyor.
2. **B bölümü, MINI R56** — yeni bir marka kapatır, hâlâ 🟢/doğrulanabilir düşük risk.
3. **B bölümü, Cupra** — yeni marka, tek bir yeni motor ailesi (EA888 evo4) gerektirir,
   şanzıman zaten mevcut.
4. **A bölümü, 🟡 satırlar** (Peugeot 3008, Citroën C5 Aircross, Kuga vb.) — kısmi
   yeni bileşen, ama depoda zaten yetim kaynaklar hazır durumda.
5. **C bölümü (Subaru, MG)** — en yüksek efor, tamamen yeni bileşen ailesi zinciri
   gerektiriyor; MINI F56 de bu gruba yakın.
6. **D bölümü (Lexus, Togg, MG'nin EV/PHEV modelleri)** — önce `docs/ARCHITECTURE.md`
   MK kaydı yazılmadan hiç başlanmamalı.

**Kullanıcıdan beklenen karar:** yukarıdaki hangi satırların (ya da bölümlerin) bu
turda kaynaklı araştırmaya (`data/queue/` üzerinden) alınacağı. Onay verildikten sonra
her aday için WebSearch ile gerçek kaynak aranacak, sonra `data/` içine işlenecek.
