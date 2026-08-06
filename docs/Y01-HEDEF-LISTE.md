# Y-01 hedef listesi — marka → model → yıl/motor/şanzıman

Bu belge, `docs/ROADMAP.md`'deki Y-01 maddesinin **kaynaklı araştırmadan önceki seçenek
listesi**. Kullanıcının istediği yöntem şu: önce markalar geliştirilir, sonra o
markaların modelleri, sonra o modellerin yıl bazında motor/şanzıman kombinasyonları
eşleştirilir — ve bütün bunlar kaynaklı araştırma (WebSearch, gerçek şikayet/forum
taraması, `data/queue/` akışı) başlamadan önce bir seçenek listesi olarak sunulur.

## Durum (2026-08-06 güncellemesi)

Kullanıcı A ve B bölümlerinin tamamlanmasını onayladı, C ve D bölümleri sonraya
bırakıldı. **A ve B bölümleri artık kaynaklandı ve `data/` içine işlendi** — bu iki
bölümdeki satırlar aşağıda hâlâ referans için duruyor ama artık "aday" değil, ya
`data/cars/` içinde gerçek bir kayıt (✅) ya da bilinçli olarak sonraya ertelenmiş (⏸,
gerekçesiyle "Ertelenenler" bölümünde). Kullanılan gerçek kaynaklar, motor/şanzıman
eşleşmeleri ve puanlar `data/cars/*.json`, `data/sources.json` ve
`data/queue/candidates.json` içinde; buradaki tablo yalnızca hangi adayın
değerlendirildiğinin kaydı olarak kalıyor, yayındaki güncel veri için asıl kaynak her
zaman `data/` klasörüdür (CLAUDE.md §3).

Sonuç: araç sayısı 160 → 178, 2016 sonrası araç sayısı 11 → 25, SUV sayısı 7 → 18,
marka sayısı 29 → 31 (MINI ve Cupra eklendi). Ayrıntı `docs/ROADMAP.md` Y-01
maddesinde.

**Bu belgedeki C ve D bölümleri hâlâ kaynaklanmadı** ve hâlâ birer seçenek listesi;
kullanıcı onayı olmadan işlenmeyecek (CLAUDE.md §1 ve MK-05 kuralı gereği).

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
| Skoda Kodiaq 1.4 TSI | 2017-2021 | `vag-ea211` (mevcut) | `vag-dq250` (mevcut) | ✅ eklendi: `skoda-kodiaq-1-4-tsi-dsg` |
| Skoda Karoq 1.6 TDI | 2018-2021 | `vag-ea288` (mevcut, 1.6 TDI) | `vag-dq200` (mevcut, kuru) | ✅ eklendi: `skoda-karoq-1-6-tdi-dsg` |
| VW T-Roc 1.5 TSI | 2018-2021 | yeni (EA211 evo 1.5 TSI ACT, mevcut `vag-ea211` 1.4 TSI'dan farklı revizyon — MK-08 dikkatiyle değerlendirilmeli) | `vag-dq200` (mevcut) | ⏸ ertelendi (yeni motor ailesi gerektiriyor, bkz. Ertelenenler) |
| Audi Q3 (8U) 2.0 TDI quattro | 2015-2018 | `vag-ea288` (mevcut, 2.0 TDI) | `vag-dq250` (mevcut) | ✅ eklendi: `audi-q3-2-0-tdi-quattro` (dört çeker, quattro) |
| Seat Ateca 1.6 TDI | 2017-2021 | `vag-ea288` (mevcut) | `vag-dq200` (mevcut) | ✅ eklendi: `seat-ateca-1-6-tdi-dsg` |
| VW Polo 6 1.0 TSI DSG | 2018-2021 | yeni (EA211 1.0 TSI 3 silindir, listede yok) | `vag-dq200` (mevcut) | ⏸ ertelendi (yeni motor ailesi gerektiriyor, bkz. Ertelenenler) |

### PSA (14 araç var) — SUV kuşağı hiç yok

| Model | Yıl (tahmini) | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Peugeot 2008 (1. nesil) 1.6 THP | 2014-2017 | `psa-ep6-thp` (mevcut) | `psa-al4` (mevcut) | ✅ eklendi: `peugeot-2008-1-6-thp` |
| Peugeot 3008 (2. nesil) 1.6 BlueHDi | 2017-2021 | `psa-dv6` (mevcut, ama 1.5 BlueHDi'den farklı, dikkat) | `aisin-eat6` (mevcut, "Grandland X EAT6" örneğiyle zaten kaynaklı) | ⏸ ertelendi (motor tarafı 1.5 BlueHDi'ye özgü, bkz. Ertelenenler) |
| Opel Grandland X 1.6 CDTI | 2018-2021 | `psa-dv6` (mevcut) | `aisin-eat6` (mevcut — yetim kaynaklar `motor1_psa_suv_eat`, `dhaber_grandland_x` bağlandı) | ✅ eklendi: `opel-grandland-x-1-6-cdti-eat6` |
| Citroën C5 Aircross 1.5 BlueHDi | 2019-2022 | yeni (1.5 BlueHDi = DV5RC, mevcut `psa-dv6`'dan [1.6] farklı) | yeni (EAT8, depoda 3 yetim kaynak zaten var: `araclo_c5aircross`, `erenservis_eat8`, `motor1_psa_suv_eat`) | ⏸ ertelendi (yeni motor + yeni şanzıman ailesi, bkz. Ertelenenler) |
| Opel Crossland X 1.2 Turbo | 2017-2020 | yeni (PureTech 3 silindir, listede yok) | `psa-etg` veya manuel-ağırlıklı, dikkatli seçilmeli | ⏸ ertelendi (yeni motor ailesi gerektiriyor) |

### Renault (9 araç var, Duster/Koleos yeni eklendi)

| Model | Yıl (tahmini) | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Renault Captur 1.5 dCi EDC | 2017-2020 | `renault-k9k` (mevcut) | `renault-edc-kuru` (mevcut) | ✅ eklendi: `renault-captur-1-5-dci-edc` |
| Renault Kadjar 1.5 dCi EDC | 2016-2020 | `renault-k9k` (mevcut) | `renault-edc-kuru` (mevcut) | ✅ eklendi: `renault-kadjar-1-5-dci-edc` |
| Renault Megane 4 1.5 dCi EDC | 2016-2020 | `renault-k9k` (mevcut) | `renault-edc-kuru` (mevcut) | ✅ eklendi: `renault-megane-4-1-5-dci-edc` |
| ~~Renault Clio 5 1.0 TCe EDC~~ → **Renault Clio 5 1.3 TCe EDC** | 2019-2022 | `renault-h5ht` (mevcut — 1.0 TCe yerine 1.3 TCe seçildi, yeni motor araştırması gerekmiyor) | `getrag-7dct300` (mevcut — Clio 5 TCe EDC'nin gerçekte 7 ileri ıslak EDC olduğu araştırma sırasında ortaya çıktı, `renault-edc-kuru` değil) | ✅ eklendi: `renault-clio-5-1-3-tce-edc` (motor/şanzıman aday listesi araştırma sırasında düzeltildi) |

### Japon grubu (33 araç var) — SUV ve daha yeni kuşak eksik

| Model | Yıl (tahmini) | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Kia Sportage (QL) 1.6 CRDi 7DCT | 2016-2020 | `hyundai-u2-16` (mevcut) | `hyundai-7dct` (mevcut) | ✅ eklendi: `kia-sportage-1-6-crdi-7dct` (not: depodaki yetim kaynak `dhaber_sportage_dct` 2023 model — yani daha yeni bir nesil — hakkında olduğu için bu kayda bağlanmadı, hâlâ yetim; ayrı bir Sportage nesli eklenirse kullanılabilir) |
| Kia Ceed SW 1.6 CRDi | 2016-2019 | `hyundai-u2-16` (mevcut) | `hyundai-7dct` (mevcut) | ⏸ ertelendi (bu turda işlenmedi, düşük riskli aday olarak duruyor) |
| Hyundai i30 (PD) 1.6 CRDi 7DCT | 2017-2020 | `hyundai-u2-16` (mevcut) | `hyundai-7dct` (mevcut) | ✅ eklendi: `hyundai-i30-pd-1-6-crdi-7dct` |
| Toyota C-HR 1.2 Turbo | 2017-2020 | yeni (8NR-FTS 1.2 turbo, listede yok) | `toyota-multidrive` (mevcut CVT, ama C-HR gerçek CVT değil — doğrulanmalı) | ⏸ ertelendi (yeni motor ailesi + trans doğrulaması gerekiyor) |
| Toyota Corolla (E210) 1.6 Benzin CVT | 2019-2022 | `toyota-zr` (mevcut, 1.6) | `toyota-multidrive` (mevcut) | ✅ eklendi: `toyota-corolla-e210-1-6-cvt` |
| Mazda CX-5 2.0 Skyactiv-G | 2017-2021 | `mazda-lf` (mevcut, 2.0) | yeni (Mazda'nın kendi 6 ileri otomatiği, listede yok) | ⏸ ertelendi (yeni şanzıman ailesi gerekiyor, bkz. Ertelenenler) |
| Nissan Juke 1.6 CVT | 2016-2019 (liste zaten "Nissan Juke 1.6" adıyla var — bu satır olası kopya, kontrol edilmeli) | — | — | ⏸ ertelendi (tekrar riski, önce mevcut kayıtla karşılaştırılmalı) |

### Ford (7 araç var) — dar

| Model | Yıl (tahmini) | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Ford Kuga (2. nesil) 1.5 EcoBoost 6AT | 2017-2019 | `ford-ecoboost-15` (mevcut) | `aisin-awf21` (mevcut — Mondeo 1.5 EcoBoost'ta zaten kullanılan aynı kutu) | ✅ eklendi: `ford-kuga-1-5-ecoboost-6at` |
| Ford Puma 1.0 EcoBoost Mild Hybrid | 2019-2022 | mild hibrit — ⛔ şema kararı gerekebilir | — | ⏸ ertelendi (hibrit sınırında, bkz. Ertelenenler) |
| Ford Focus 4 1.5 EcoBlue | 2018-2021 | yeni (1.5 EcoBlue, listede yok) | `getrag-6dct450` (mevcut ıslak DCT) | ⏸ ertelendi (yeni motor ailesi gerektiriyor, bkz. Ertelenenler) |

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
| MINI Cooper (R56) 1.6 | 2007-2013 | `psa-ep6-vti` (mevcut) | `aisin-eat6` (doğrulandı) | ✅ eklendi: `mini-cooper-r56-1-6` |
| MINI Cooper S (R56) 1.6 Turbo | 2007-2013 | `psa-ep6-thp` (mevcut) | `aisin-eat6` (doğrulandı) | ✅ eklendi: `mini-cooper-s-r56-1-6-turbo` |

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
| Cupra Formentor 2.0 TSI DSG | 2020-2023 | yeni: `vag-ea888-evo4` açıldı | `vag-s-tronic-islak` (mevcut) | ✅ eklendi: `cupra-formentor-2-0-tsi-dsg` |
| Cupra Leon 2.0 TSI DSG | 2020-2023 | `vag-ea888-evo4` (aynı) | `vag-s-tronic-islak` (mevcut) | ✅ eklendi: `cupra-leon-2-0-tsi-dsg` |

---

## Ertelenenler — A/B içinde kaynaklanmayan satırlar

**Güncelleme (2026-08-06, aynı gün):** Kullanıcı "sarı/kırmızılara devam, kaynak
önemli değil" dedi; aşağıdaki satırların çoğu bu turda işlendi ve `data/` içine
girdi (bkz. `docs/Y01B-MOTOR-CESITLENDIRME.md` "ikinci tur"). Yalnızca **Nissan
Juke 1.6 CVT** (zaten mevcut kayıtla aynı olduğu doğrulandı, eklenmedi) ve **Ford
Puma 1.0 EcoBoost** (mild-hibrit, ⛔ şema kararı bekliyor) hâlâ bekliyor.

| Aday | Durum |
|---|---|
| VW T-Roc 1.5 TSI, VW Polo 1.0 TSI | ✅ eklendi — `vag-ea211` ailesi 1.0/1.5'e genişletildi, yeni motor açılmadı |
| Peugeot 3008 1.6 BlueHDi | ✅ eklendi — mevcut `psa-dv6`/`aisin-eat6` ile (1.6 trim seçildi, yeni motor gerekmedi) |
| Citroën C5 Aircross 1.5 BlueHDi | ✅ eklendi — yeni `psa-bluehdi-15` + yeni `psa-eat8` açıldı |
| Opel Crossland X 1.2 Turbo | ✅ eklendi (`opel-crossland-x-1-2-puretech`) — yeni `psa-puretech-12` açıldı |
| Kia Ceed SW 1.6 CRDi | ✅ eklendi — bileşenleri zaten mevcuttu |
| Toyota C-HR 1.2 Turbo | ✅ eklendi — yeni `toyota-8nr-fts` açıldı |
| Mazda CX-5 2.0 | ✅ eklendi — yeni `mazda-skyactiv-6at` açıldı |
| Nissan Juke 1.6 CVT | ⏸ eklenmedi — listede zaten "Nissan Juke 1.6" (`nissan-juke-1-6`) tam bu kombinasyonla kayıtlı, tekrar oluşturulmadı |
| Ford Puma 1.0 EcoBoost | ⏸ ertelendi — tamamen mild-hibrit satılıyor, ⛔ şema kararı sınırında |
| Ford Focus 4 1.5 EcoBlue | ✅ eklendi — yeni `ford-ecoblue-15` açıldı |
| MINI Cooper (F56) 1.5, MINI Countryman (F60) | ✅ eklendi — yeni `bmw-b38` açıldı |

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

## D) Kapsam dışı — kalıcı karar (2026-08-06)

**Bu bölüm artık "karar bekliyor" değil, "karar verildi" durumunda.** Kullanıcı net
konuştu: "elektrikli ve LPG araba olmayacak abi, net bir karar o." Gerekçesi
`docs/ARCHITECTURE.md` MK-13 kaydında. Aşağıdakiler **hiçbir zaman** araştırma
turuna alınmayacak, kaynaklı araştırma beklenmiyor:

- **Lexus** — Türkiye'de satılan hemen hemen bütün modeller (CT200h, IS300h, NX300h,
  ES300h) tam hibrit. Kapsam dışı.
- **Togg T10X** — tam elektrikli. Kapsam dışı.
- **Chery / BYD** — çoğunlukla EV veya PHEV. Kapsam dışı.
- **Toyota/Honda hibrit varyantları** (Corolla Hybrid, C-HR Hybrid, CR-V Hybrid) —
  marka listede var ama hibrit gövdeler kapsam dışı; aynı markanın geleneksel
  yakıtlı varyantları (ör. Toyota Corolla 1.6 CVT, Toyota C-HR 1.2 Turbo — ikisi de
  listede zaten var) kapsam içinde kalmaya devam ediyor.
- **LPG'li araçlar** — fabrika çıkışı ya da dönüşüm fark etmeksizin, hiçbir araç
  kaydı LPG'li olarak listelenmeyecek (bkz. MK-11, MK-13).

---

## Öneri: hangi sırayla ilerlenmeli

Kullanıcının "önce marka, sonra model, sonra yıl/motor/şanzıman" yöntemine göre risk
ve efor dengesi şöyle kurulmuştu; 1-3 artık **bitti**:

1. ~~**A bölümü (mevcut marka genişletmesi, 🟢 satırlar)**~~ — **bitti**, "Ertelenenler"
   bölümündeki birkaç satır hariç.
2. ~~**B bölümü, MINI R56**~~ — **bitti**, iki araç eklendi.
3. ~~**B bölümü, Cupra**~~ — **bitti**, yeni motor ailesi (`vag-ea888-evo4`) açıldı.
4. **"Ertelenenler" bölümü** — kısmi yeni bileşen gerektiren satırlar (Peugeot 3008,
   Citroën C5 Aircross, T-Roc, Polo, C-HR, CX-5, Focus 4, MINI F56 vb.); depoda zaten
   yetim kaynaklar hazır olanlar (3008/C5 Aircross/Grandland X ailesi) öncelikli.
5. **C bölümü (Subaru, MG)** — en yüksek efor, tamamen yeni bileşen ailesi zinciri
   gerektiriyor.
6. **D bölümü (Lexus, Togg, MG'nin EV/PHEV modelleri)** — önce `docs/ARCHITECTURE.md`
   MK kaydı yazılmadan hiç başlanmamalı.

**Kullanıcıdan beklenen karar:** "Ertelenenler", C ve D bölümlerinden hangisinin
sıradaki turda kaynaklı araştırmaya (`data/queue/` üzerinden) alınacağı.
