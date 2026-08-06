# Motor/şanzıman çeşitlendirme — mevcut modellerin eksik varyantları

Bu belge Y-01'in yeni bir alt maddesi: **yeni model eklemek değil, listede zaten
bulunan model nesillerinin eksik motor/şanzıman varyantlarını kapatmak.** Kullanıcının
gözlemi doğru: liste yeni marka/model açısından genişledi ama aynı model içinde motor
çeşitliliği zayıf — bir BMW E39 altı varyantla temsil edilirken bir Mercedes W211 tek
varyantla duruyor, bir VW Golf 7 iki varyantla duruyor.

## Durum (2026-08-06 güncellemesi)

Kullanıcı "tüm markalar için çeşitlendirme istiyorum, hepsini uygula" dedi. Bu
belgedeki **bütün 🟢 satırlar (21 araç) aynı gün kaynaklandı ve `data/` içine
işlendi** — BMW (7: E39 520i/520d, E46 320d/320i, E60 520d, E87 120d, E36 325i),
Mercedes-Benz (4: W203 C200 Kompressor, W211 E200 Kompressor, W212 E200, W204 C220
CDI), VAG (5: Passat B7 1.8 TSI, Passat B8 1.4 TSI, Audi A4 B9 2.0 TFSI, Skoda Octavia
3 2.0 TDI, Skoda Superb 3 2.0 TDI), Renault (2: Talisman 1.6 dCi 160 EDC, Megane 4 1.3
TCe EDC), Toyota (1: Auris 1.8 Multidrive), Citroën (1: C4 1.6 THP), Kia (1: Ceed 1.6
GDi). Hiçbir yeni motor/şanzıman ailesi açılmadı; hepsi zaten kayıtlı ailelere
bağlandı. Ayrıntı `docs/ROADMAP.md` Y-01 maddesinde.

Aşağıdaki tablo hâlâ referans için duruyor (hangi aday neden seçildiği, hangi aile
kullanıldığı) ama artık güncel veri için asıl kaynak `data/cars/*.json`'dır. **🟡/🔴
etiketli satırlar (Golf 7 GTI, W211 E280, Megane 3 1.2 TCe, Clio 4 TCe, Laguna 1.9 dCi,
Peugeot 308 PureTech, Opel Insignia 2.0 Turbo, Opel Astra 1.7 CDTI) hâlâ işlenmedi** —
her biri yeni bir motor ailesi gerektiriyor, kullanıcı onayı bekliyor.

**Bu belgedeki hiçbir satır henüz kaynaklanmadı** (kullanıcının talebi: "araştırmasını
sonra yaparız"). Aşağıdaki motor/şanzıman eşleşmeleri genel otomotiv bilgisine dayanıyor.
Her satır iki etiketten biriyle işaretli:

- 🟢 **Aile zaten var, yalnızca yeni hacim/güç eklenecek** — `data/engines.json` veya
  `data/transmissions.json`'daki aile zaten kayıtlı ve kaynaklı; yeni varyant o ailenin
  `displacements_l` listesine bir değer daha ekleyip (`validate.py`'nin bunu zorunlu
  kılması gerekiyor, CLAUDE.md §2) araç kaydı açmaktan ibaret. En düşük risk.
- 🟡/🔴 **Yeni aile gerekiyor** — motor kodu tamamen farklı, `data/engines.json`'da
  hiç karşılığı yok.

## Neden bu bir sorun

`scripts/validate.py`'nin bugünkü çıktısında `arac_basina_ortalama_kaynak` düşük olma
sebeplerinden biri de bu: aynı ailenin farklı güç/hacim varyantları ayrı araç kayıtları
olduğu için, bir model nesli ne kadar dar temsil edilirse kullanıcı o nesildeki gerçek
seçeneklerin ne kadarını gördüğünü bilemiyor. Bir kullanıcı "BMW E90" arayınca 6 satır
görüyor ama "Mercedes W211" arayınca 1 satır görüyor — oysa ikisi de gerçek hayatta
benzer sayıda otomatik vitesli varyantla satıldı. Bu, listenin **temsil dengesizliği**
sorunu; Y-01'in orijinal "marka/gövde/yıl dengesizliği" sorununun aynı ailesinden ama
farklı bir boyutu.

---

## BMW — en iyi kapsanan marka, ama hâlâ boşluklar var

Bugünkü kapsam: E39 6 varyant, E46 4 varyant, E90 6 varyant, E60 2 (birleşik) varyant,
E87 1 (birleşik) varyant, E36 1 varyant.

| Nesil | Listede olmayan gerçek varyant | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| E39 (1995-2003) | 520i, 528i zaten var ama **520d** yok — dönemin en çok satan dizeli | `bmw-m47` (mevcut, 2.0 zaten kayıtlı) | `zf-5hp` (mevcut) | 🟢 |
| E46 (1998-2005) | **320d**, **320i** — E46'nın en yaygın iki otomatik varyantı, hiç yok | `bmw-m47` / `bmw-m52` veya `bmw-n4x` (hepsi mevcut) | `zf-5hp` (mevcut) | 🟢 |
| E60 (2003-2010) | Birleşik kayıtlar (525d/530d, 525i/530i) ayrı satırlara bölünebilir; ayrıca **520d**, **535d** eksik | `bmw-m47`/`bmw-m57` (mevcut) | `zf-6hp` (mevcut) | 🟢 |
| E87 (2004-2011) | Birleşik "116i/118i" ayrı satırlara bölünebilir; **120d** eksik — bu gövdenin en yaygın dizeli | `bmw-n47` (mevcut) | `zf-6hp` (mevcut) | 🟢 |
| E36 (1990-2000) | Yalnızca 320i/323i birleşik; **325i**, **318i**, **325tds** dizel eksik | `bmw-m52`/`bmw-m43` (mevcut) | `zf-4hp` (mevcut) | 🟢 |
| F30 (2012-2019, hiç yok) | **320d**, **320i**, **318d** — E90'ın doğrudan devamı, listede bu nesil hiç yok | yeni (N13/N20/B47, listede yok) | `zf-8hp` (listede hiç yok, yeni) | 🔴 |

**Not:** BMW'de neredeyse bütün eksik varyantlar 🟢 — motor aileleri zaten kayıtlı ve
kaynaklı, yalnızca o hacmin/gücün araç kaydı açılmamış. Bu, en ucuz kazanılacak
alan.

---

## Mercedes-Benz — en zayıf kapsanan büyük marka

Bugünkü kapsam: neredeyse her şasi kodu (W202, W203, W204, W211, W212, CLK) yalnızca
1-3 varyantla temsil ediliyor; oysa Mercedes bu dönemde Türkiye'de en geniş motor
yelpazesini sunan markalardan biriydi.

| Nesil | Listede olmayan gerçek varyant | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| W203 (2000-2007) | **C220 CDI**, **C180 Komp.** — C200 CDI ve C270 CDI zaten var ama bu ikisi eksik | `mb-om611`/`mb-m271` (mevcut) | `mb-5g-tronic` (mevcut) | 🟢 |
| W204 (2007-2014) | **C220 CDI (W204)** — C180/C200 CDI/C250 CDI zaten var, bu güç basamağı eksik | `mb-om651` (mevcut) | `mb-5g-tronic` (mevcut) | 🟢 |
| W211 (2002-2009) | **E200 Komp.**, **E280**, **E320 CDI (W211 dönemi)** — yalnızca E220 CDI var | `mb-m271`/`mb-om642` (om642 listede yok, yeni) | `mb-5g-tronic` (mevcut) | 🟡 |
| W212 (2009-2016) | **E200**, **E220 CDI (W212)**, **E300** — yalnızca E250 CDI var | `mb-om651`/`mb-m270` (mevcut) | `mb-7g-tronic` (mevcut) | 🟢 |
| CLK (1997-2009) | **CLK220 CDI**, **CLK320** — 200/230 Komp. ve 270 CDI zaten var | `mb-om611`/`mb-m112` (m112 listede yok, yeni) | `mb-5g-tronic` (mevcut) | 🟡 |
| W176 A-Serisi (2012-2018, "A/B Serisi" birleşik) | Ayrı A180/A200/B180 satırlarına bölünebilir | `mb-m270` (mevcut) | `mb-7g-dct` (mevcut) | 🟢 |

**Not:** Mercedes'te de çoğu boşluk 🟢 — `mb-om611`, `mb-om651`, `mb-m271` gibi aileler
zaten kayıtlı, yalnızca o gövdedeki uygulaması eksik. En büyük yeni-aile ihtiyacı
`mb-om642` (V6 CDI, E-Class/S-Class'ta yaygın) ve `mb-m112` (V6 benzin, 2000'ler
E/CLK'de yaygın).

---

## VAG (Volkswagen/Audi/Skoda/Seat) — orta kapsam, nesil başına 1-3 varyant

| Nesil | Listede olmayan gerçek varyant | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Golf 7 (2013-2019) | **2.0 TDI**, **1.6 TDI** zaten var ama **GTI 2.0 TSI** yok | `vag-ea888` (mevcut, ama GTI genelde daha yeni evo — dikkat) | `vag-dq250` (mevcut) | 🟡 |
| Passat B7 (2011-2015) | 1.6/2.0 TDI zaten var, **1.8 TSI** eksik | `vag-ea888` (mevcut) | `vag-dq250` (mevcut) | 🟢 |
| Passat B8 (2014-2019) | Yalnızca 2.0 TDI var; **1.4 TSI**, **1.8 TSI** eksik | `vag-ea211`/`vag-ea888` (mevcut) | `vag-dq250` (mevcut) | 🟢 |
| Audi A4 B8 (2008-2015) | 3 varyant zaten iyi (1.8 TFSI, 2.0 TDI, 2.0 TFSI quattro); **2.0 TDI quattro** eksik | `vag-ea288`/`vag-ea113` (mevcut) | `vag-dq250` (mevcut) | 🟢 |
| Audi A4 B9 (2015-2019) | Yalnızca 2.0 TDI var; **2.0 TFSI**, **1.4 TFSI** eksik | `vag-ea888`/`vag-ea211` (mevcut) | `vag-dq250` (mevcut) | 🟢 |
| Skoda Octavia 3 (2013-2019) | 1.6 TDI/1.8 TSI zaten var; **2.0 TDI** eksik | `vag-ea288` (mevcut, 2.0 zaten aile içinde) | `vag-dq250` (mevcut) | 🟢 |
| Skoda Superb 3 (2015+, hiç yok) | Listede yalnızca Superb 2 (2009-2015) var; Superb 3 hiç yok | `vag-ea888`/`vag-ea288` (mevcut) | `vag-dq250` (mevcut) | 🟢 |

**Not:** VAG'da da neredeyse her boşluk 🟢 çünkü EA211/EA288/EA888 aileleri geniş bir
hacim/güç yelpazesini zaten kapsıyor ve listede kayıtlı.

---

## Renault — nesil başına genelde tek varyant

Renault'nun her nesli (Megane 2/3/4, Laguna, Talisman, Clio 4/5, Fluence) listede
yalnızca 1-2 varyantla var; oysa Renault Türkiye'de hem dCi (dizel) hem TCe (benzin
turbo) hem de güç basamağı çeşitliliğiyle satıldı.

| Nesil | Listede olmayan gerçek varyant | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Megane 3 (2012-2016) | Yalnızca 1.5 dCi var; **1.2 TCe**, **1.6 dCi 130** (bu ayrı bir satır olarak zaten var ama nesli belirsiz) eksik | `renault-k4m`/yeni (1.2 TCe listede yok) | `renault-edc-kuru` (mevcut) | 🟡 |
| Megane 4 (2016-2020) | Yalnızca 1.5 dCi EDC var (bu turda eklendi); **1.3 TCe** eksik | `renault-h5ht` (mevcut) | `getrag-7dct300` (mevcut) | 🟢 |
| Clio 4 (2012-2019) | Yalnızca 1.5 dCi var; **0.9 TCe**, **1.2 TCe** eksik | yeni (0.9/1.2 TCe küçük motorlar listede yok) | `renault-edc-kuru` (mevcut) | 🟡 |
| Talisman (2016-2020) | Yalnızca 1.5 dCi var; **1.6 dCi 160**, **1.3 TCe** eksik | `renault-h5ht`/yeni 1.6 dCi (r9m zaten mevcut, 1.6 var) | `getrag-7dct300` (mevcut) | 🟢 |
| Laguna 2 (2001-2007) | Yalnızca 1.6/2.0 birleşik; **1.9 dCi** eksik — dönemin en yaygın dizeli | `renault-m9r`/yeni eski nesil dCi (listede farklı kod olabilir) | `psa-al4` (mevcut) | 🟡 |

---

## Peugeot / Opel (PSA + eski GM) — nesil başına tek varyant

| Nesil | Listede olmayan gerçek varyant | Motor adayı | Şanzıman adayı | Etiket |
|---|---|---|---|---|
| Peugeot 308 (2014-2018) | Yalnızca 1.6 BlueHDi var; **1.2 PureTech** eksik | yeni (PureTech listede yok) | `aisin-eat6` (mevcut) | 🟡 |
| Peugeot 508 (2011-2018) | 1.6 THP ve 2.0 HDi zaten var — bu nesil iyi kapsanmış | — | — | ✅ zaten iyi |
| Opel Insignia (2009-2017) | 1.6 T ve 2.0 CDTI zaten var; **2.0 Turbo (benzin)** eksik | yeni (2.0 Turbo listede yok) | `aisin-awf21` (mevcut) | 🟡 |
| Opel Astra J (2010-2015) | Yalnızca 1.6 var; **1.7 CDTI** eksik | yeni (1.7 CDTI listede yok) | `aisin-af40` (mevcut) | 🟡 |

---

## Öncelik önerisi

BMW ve Mercedes'teki boşlukların büyük kısmı 🟢 (motor ailesi zaten kayıtlı ve
kaynaklı) — bu yüzden en verimli sıradaki adım bu ikisi. VAG da benzer şekilde ucuz.
Renault/PSA/Opel'de daha fazla 🟡 (yeni aile) var, o yüzden onlar ikinci sırada.

**Kullanıcıdan beklenen karar:** hangi marka(lar) ile devam edilsin — örneğin
"BMW ve Mercedes'in 🟢 satırlarını kaynakla" gibi. Onay verildikten sonra her aday için
gerçek kaynak aranacak (Y-03 kuyruğu üzerinden), sonra `data/` içine işlenecek.
