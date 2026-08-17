# Yol haritası — sıradaki işler

Bu belge, projenin **bundan sonra ne yapacağını** tanımlar. `docs/PLAN.md` Faz 2'nin
(tekrarlanabilirlik ve doğrulanabilirlik) planıydı ve büyük ölçüde tamamlandı; bu belge
Faz 3'ü tanımlıyor: **ürünleşme**.

Belgenin varlık sebebi pratik. Bir sohbetin bağlam penceresi dolduğunda iş yarıda
kalıyor ve yeni bir oturum neyin neden yapıldığını bilmeden devam etmeye çalışıyor.
Buradaki her madde, o maddeyi hiç konuşmamış birinin doğru şekilde devam
edebileceği kadar ayrıntılı yazıldı: sorun ne, kapsam ne, neyin bitmiş sayılacağı ne,
neye bağımlı.

**Bir maddeye başlarken yapılacaklar:** durumu `başlandı` olarak güncelle, işi bitirince
`bitti` yaz ve altına ne yapıldığını iki cümleyle özetle. Bu belge, kod kadar bakım
ister; güncellenmezse ilk işlevini kaybeder.

---

## Durum özeti (son güncelleme: 2026-08-17)

| Katman | Durum |
|---|---|
| Veri mimarisi (araç / motor / şanzıman / kaynak ayrımı) | Tamamlandı |
| Şanzıman kutusu kayıtları | 53 kutu (`data/transmissions.json`), hepsi temel puanlı, kaynaklı ve yapılandırılmış `known_issues` taşıyor |
| Motor ailesi kayıtları | 104 aile (`data/engines.json`), hepsi temel puanlı, kaynaklı ve yapılandırılmış `known_issues` taşıyor |
| Denetim hattı (`validate.py`, `consistency.py`, `smoke_test.js`) | Çalışıyor, 0 hata, 64/64 duman testi (statik sayfa, SEO ve katalog kontrolleri dahil) |
| `age` ve `fun` kriterleri (MK-06) | Formüle bağlandı: `age` → `scripts/compute_age.py` (MK-14), `fun` → `scripts/compute_fun.py` (MK-17, 233/378 araç; terfi eden 100 araçtan 71'i bu turda eklendi, 29'u ağırlık araştırması bekliyor — bkz. Y-19). `comf` ve `cost` hâlâ elle veriliyor. |
| `price` kriteri (MK-19) | **Tarihlendi.** 19 araç 2026-08-13 tarihli piyasa gözlemine bağlandı (`price_reference` bloğu: tarih, yöntem, örneklem, sınırlılık). Kalan 259 araç hâlâ tarihsiz tahmin ve denetimde `fiyat-tarihsiz` uyarısı üretiyor. |
| `liq` kriteri (MK-20) | **Ölçülemedi, gerekçesi yazıldı.** Elimizdeki 2.071 ilan gözlemi sorgu başına 50 ile sınırlı olduğu için sağdan sansürlü; en likit araçlar tavanda birbirine karışıyor. Doğru protokol, ilanları çekmek değil sorgu sonucundaki toplam ilan sayısını kaydetmek. |
| Çok ekranlı arayüz: ana ekran, giriş akışı, liste, metodoloji, kaynak öner, iletişim | Çalışıyor |
| GitHub Pages yayını | Çıktı `index.html` olarak üretiliyor, kök adres siteyi açıyor |
| Liste ekranı denetim çubuğu (Y-05) | Tamamlandı: ağırlık/arama/filtre tablonun üstünde, filtre paneli katlanabilir |
| Kaynak öneri formu (Y-04) | Arayüz tamamlandı; gönderim uç noktası ve iletişim adresi tanımlanmayı bekliyor |
| Ana ekran (Y-07) | Tamamlandı: veri kapsamı özeti, hazır giriş yolları, en riskli bileşenler |
| Araştırma kuyruğu (Y-03) | Tamamlandı: `data/queue/`, şema, iki aşamalı akış, bir tur uçtan uca çalıştırıldı |
| Kaynak derinliği (Y-02) | **Bitti (278 araçlık ilk parti için).** 357 araçtan 345'i "doğrulanmış" (4+ kaynak); Y-19 terfisiyle eklenen 79 aracın motor/trans puanı aile mirasıyla kanıtlı, ama comf/cost/liq/fun tahmini ve gerekçesiz — bkz. Y-19 |
| Araç listesi (Y-01) | 154 → 278 araç. Birinci dalgada **SUV 1 → 30 (hedefi aştı), marka 5/5 (hedefe ulaştı), 2016+ 5 → 42 (hedefi (40) aştı)**; ikinci dalga 300-900 bin TL bandında marka-model-motor-şanzıman çeşitliliğini artırıyor (228→278, 50 kombinasyon), odak artık sayısal hedeften ziyade popüler marka/modellerin motor çeşitliliği, sürüyor |
| Teknik katalog (MK-22) | **1.641 kayıt** (`data/catalog/`, marka başına bir dosya). Olgusal katmandır: güç, tork, çekiş, hacim, gövde, vites sayısı, kavrama tipi, motor kodu ve teknik kaynak adresi taşır; puan taşımaz. 281 kayıt puanlanmış bir araca bağlı, 1.345'i yalnız katalogda ve kendi statik sayfası var. |
| Kapsam sınırı | **Elektrikli, hibrit ve LPG'li araçlar kalıcı olarak kapsam dışı (MK-13)** |
| Puanlama şeffaflığı (Y-06) | **Bitti.** Bilimsel temel, kanıt zinciri, arayüz katmanı (kriter paneli artık liste ekranında, "neden bu puan" dökümü) tamamlandı |
| Veri doğruluğu (MK-18) | **Dış veri setiyle çapraz doğrulama yapıldı.** 220 araç bağımsız bir katalogla karşılaştırıldı; motor/şanzıman ailesinde 0 çelişki, beygir/torkta 10 çelişki bulundu ve doğrulanan 5 gerçek hata düzeltildi (en ağırı: bir 1.6 dizelde 400 Nm ve bir aracın tamamen yanlış motor ailesine bağlı olması). |
| Teknik özellik kapsamı | Tork 172 → **251/278**; boş ağırlık 163/278. `fun` formülünün önündeki tek engel artık boş ağırlık: 88 araçta tork var ama ağırlık yok. Çalışma listesi ve doğrulamalı içe aktarma betiği hazır (Y-16); veri toplama, spec sitelerine erişimi olan bir oturumu bekliyor. |
| Görsel dil / ürün hissi | Ham, iş odaklı |
| Arama motoru görünürlüğü (Y-11) | **Temel kuruldu.** `scripts/build_pages.py` 435 indekslenebilir sayfa üretiyor (araç/motor/şanzıman başına bir tane), her biri araca özgü başlık, açıklama, canonical ve JSON-LD ile; `sitemap.xml` ve `robots.txt` yayında. Search Console'a gönderim depo sahibini bekliyor. |
| Ticari strateji | `docs/URUN-STRATEJISI.md` — gelir modelleri, açık kaynak lisans katmanları, içerik/pazarlama hattı ve 90 günlük plan; her fikir uygulanabilirlik seviyesiyle birlikte |

Denetimin bugünkü çıktısı: **0 hata, 252 uyarı**. Uyarıların ezici çoğunluğu tek
bir kalemden geliyor: araçların **dört** bağımsız kaynağa ulaşmamış olması — bu, artık
kaynaksızlıktan değil "doğrulanmış" rozetinin katı eşiğinden kaynaklanıyor. Her aracın
en az iki kaynağı var (Y-02 derinlik turu, aşağıda).

---

## Y-01 · Araç listesini genişlet ve kapsamı dengele — **üç hedef de karşılandı**

**Öncelik: yüksek.** Ürünün değeri doğrudan buna bağlı; kimse aradığı aracı bulamadığı
bir listeyi ikinci kez açmaz.

**Sorun.** Liste 154 araç içeriyordu ama dağılımı çok dengesizdi:

| Boyut | Y-01 öncesi dağılım | Sorun |
|---|---|---|
| Model yılı | 1990'lar 20 · 2000'ler 73 · 2010'lar 61 | **2016 ve sonrası yalnızca 5 araç.** Liste pratikte 2015'te bitiyordu. |
| Gövde | Sedan 108 · Hatchback 37 · Coupe 3 · SUV 1 · SW 1 | SUV ve station wagon neredeyse yoktu, oysa Türkiye'de SUV payı çok yüksek. |
| Şanzıman | TK 103 · Kuru DCT 23 · Islak DCT 14 · CVT 12 · Robot 2 | Modern araçlarda yaygınlaşan ıslak DCT ve CVT az temsil ediliyordu. |

**Listede hiç bulunmayan markalar:** Dacia, Jeep, MINI, Lexus, Cupra, MG, Chery, BYD,
Togg, Subaru, Porsche, Infiniti, Tesla. Bunların bir kısmı bilinçli olarak kapsam dışı
sayılabilir (Porsche, Tesla, Infiniti gibi niş veya çok pahalı olanlar), ama **Dacia,
Jeep, MINI, Lexus, Cupra, MG ve Togg Türkiye ikinci el piyasasında otomatik vitesli
olarak gerçekten yaygın** ve yokluğu bir kapsam boşluğuydu.

**Bu turda ne yapıldı.** 2026-08-06'da altı araç eklendi, **hepsi mevcut, zaten temel
puanlı ve kaynaklı motor/şanzıman ailelerine bağlanarak** — bu turda hiçbir yeni
bileşen ailesi açılmadı, bu yüzden risk düşük tutuldu (madde 2'deki sıra kuralına
uyuldu):

- `dacia-duster-1-5-dci-edc` — **Dacia**, yeni marka. `renault-k9k` + `renault-edc-kuru`.
- `jeep-renegade-1-6-multijet-ddct` — **Jeep**, yeni marka. `fca-multijet-16` +
  `fiat-c635-ddct`.
- `vw-tiguan-1-4-tsi-dsg` — SUV, 2016+. `vag-ea211` + `vag-dq250`.
- `hyundai-tucson-1-6-crdi-7dct` — SUV, 2016+. `hyundai-u2-16` + `hyundai-7dct`.
- `nissan-qashqai-1-3-dig-t-cvt` — SUV, 2016+. `renault-h5ht` + `nissan-xtronic`.
- `renault-koleos-1-3-tce-edc` — SUV, 2020+. `renault-h5ht` + `getrag-7dct300`.

Her biri için gerçek kaynak arandı (WebSearch) ve araç kaydına bağlandı. Ayrıca depoda
önceden duran ama hiçbir araca bağlı olmayan (yetim) birkaç kaynak — `sikayetvar_tucson_dct`,
`dhaber_qashqai13`, `sikayetvar_qashqai`, `kronikyorum_qashqai`, `hech_koleos` — tam da
bu turda açılan araç kayıtlarına karşılık geldiği için doğrudan bağlandı; bu, önceki bir
oturumun Y-01'i önceden öngörüp araştırma yaptığının ama karşılık gelen aracı hiç
açmadığının kanıtı. `yetim-kaynak` uyarısı bu turda 11'den 6'ya düştü.

**Sonuç (birinci tur):** araç sayısı 154 → 160, 2016 sonrası araç sayısı 5 → 11, SUV
sayısı 1 → 7, iki yeni marka (Dacia, Jeep) eklendi. `validate.py` hâlâ 0 hata.

**İkinci tur — hedef liste önce sunuldu, sonra kullanıcı onayıyla işlendi.**
Kullanıcı "önce markaları geliştir, sonra modellerini, sonra yıl bazında motor/şanzıman
eşleştir; kaynaklı araştırmadan önce seçeneklerimi görmek istiyorum" dedi. Bunun için
önce `docs/Y01-HEDEF-LISTE.md` yazıldı: her aday satır 🟢 (mevcut bileşen), 🟡 (kısmi),
🔴 (yeni bileşen) veya ⛔ (şema kararı bekliyor) etiketiyle işaretlendi, hiçbiri henüz
kaynaklanmadı. Kullanıcı "A ve B'yi tamamla, C ve D'yi kaydet, ayarlarız" dedi.

A ve B bölümlerinin düşük riskli (🟢, mevcut bileşenli) satırları 2026-08-06'da
kaynaklandı ve işlendi — **18 araç, 1 yeni motor ailesi (`vag-ea888-evo4`), 2 yeni
marka (MINI, Cupra):**

- VAG: Skoda Kodiaq, Skoda Karoq, Audi Q3 (8U) quattro, Seat Ateca — dördü de mevcut
  EA211/EA288 + DQ200/DQ250 ailelerine bağlandı.
- PSA: Peugeot 2008 1.6 THP, Opel Grandland X 1.6 CDTI EAT6 — mevcut EP6/DV6 +
  AL4/EAT6 ailelerine bağlandı; Grandland X, depoda önceden duran yetim kaynakları
  (`motor1_psa_suv_eat`) kullandı.
- Renault: Captur, Kadjar, Megane 4, Clio 5 — dördü de mevcut K9K/H5Ht +
  EDC ailelerine bağlandı. Clio 5 aday listesinde "1.0 TCe" olarak duruyordu;
  araştırma sırasında gerçek şanzımanının 7 ileri **ıslak** EDC (`getrag-7dct300`)
  olduğu ve 1.3 TCe (`renault-h5ht`, zaten kayıtlı) seçeneğinin yeni motor
  gerektirmediği ortaya çıktı, aday buna göre düzeltildi.
- Japon grubu: Kia Sportage, Hyundai i30 (PD), Toyota Corolla (E210) — üçü de mevcut
  U2/ZR + 7DCT/Multidrive ailelerine bağlandı.
- Ford: Kuga 1.5 EcoBoost — aday listesinde "8F35" (yeni bileşen) olarak duruyordu;
  araştırma sırasında Mondeo 1.5 EcoBoost'ta zaten kayıtlı Aisin AWF21 kutusuyla aynı
  nesil eşleştiğinin daha güvenilir olduğu görüldü, 2. nesil (2017-2019) 6 ileri
  otomatik versiyon seçildi.
- **MINI** (yeni marka): R56 kuşağı Cooper ve Cooper S — motorları listede zaten
  kayıtlı "BMW/PSA Prince" ailesine (`psa-ep6-vti`/`psa-ep6-thp`) bağlandı, şanzıman
  Aisin `aisin-eat6` ile doğrulandı.
- **Cupra** (yeni marka): Formentor ve Leon, 2.0 TSI DSG — şanzıman mevcut
  `vag-s-tronic-islak` ailesine bağlandı; motor için **yeni** `vag-ea888-evo4` ailesi
  açıldı, çünkü listedeki eski `vag-ea888` kaydı farklı bir nesli (Golf Mk5/6 dönemi)
  temsil ediyordu ve MK-08 gereği doğrudan reddedilmesi gerekiyordu. İki gerçek kaynak
  (Cupra Forum, Araclo.com) evo3→evo4 arası yağ pompası tasarımının değişmediğini ve
  yağ tüketimi eğiliminin taşındığını doğruladı; base_score bu yüzden eskisinden çok
  farklı tutulmadı (46 → 50).

**Sonuç (ikinci tur):** araç sayısı 160 → 178, 2016 sonrası araç sayısı 11 → 25, SUV
sayısı 7 → 18, marka sayısı 29 → 31. `yetim-kaynak` uyarısı 6'dan 5'e düştü.
`validate.py` hâlâ 0 hata.

A/B'nin geri kalan (🟡/🔴 etiketli) satırları ve ertelenen adaylar
`docs/Y01-HEDEF-LISTE.md`'nin "Ertelenenler" bölümünde duruyor — en düşük riskli aday
(Kia Ceed SW, bileşenleri tamamen mevcut ama bu turda işlenmedi) bir sonraki round
için hazır bekliyor.

**Üçüncü tur — motor/şanzıman çeşitlendirme.** Kullanıcı farklı bir boşluk fark etti:
"aynı aracın farklı motor seçenekleri çok az cover'lanıyor" — bir BMW E39 altı
varyantla temsil edilirken bir Mercedes W211 tek varyantla duruyordu. Bu, yeni marka/
model eklemekten farklı bir sorun: **listede zaten bulunan model nesillerinin eksik
motor/şanzıman varyantlarını kapatmak.** Önce `docs/Y01B-MOTOR-CESITLENDIRME.md`
yazıldı (kaynaklanmamış seçenek listesi, marka bazında), kullanıcı "hepsini uygula,
tüm markalar" dedi. Bunun üzerine **21 araç** eklendi, hiçbiri yeni motor/şanzıman
ailesi gerektirmedi (hepsi listede zaten kayıtlı ailelere bağlandı):

- BMW (7): E39 520i/520d, E46 320d/320i, E60 520d, E87 120d, E36 325i.
- Mercedes-Benz (4): W203 C200 Kompressor, W211 E200 Kompressor, W212 E200, W204
  C220 CDI.
- VAG (5): Passat B7 1.8 TSI, Passat B8 1.4 TSI, Audi A4 B9 2.0 TFSI, Skoda Octavia 3
  2.0 TDI, Skoda Superb 3 2.0 TDI (Superb'in listede ilk kez yer alan 3. nesli).
- Renault (2): Talisman 1.6 dCi 160 EDC, Megane 4 1.3 TCe EDC.
- Toyota (1): Auris 1.8 Multidrive. Citroën (1): C4 1.6 THP. Kia (1): Ceed 1.6 GDi.

**Sonuç (üçüncü tur):** araç sayısı 178 → 199. `arac_basina_ortalama_kaynak` 1.80'den
1.71'e **geriledi** — aynı Y-02'deki gerekçeyle: yeni eklenen 21 aracın çoğu tek
kaynakla açıldı, kaynaksız başlamamaları önceliklendirildi. `validate.py` hâlâ 0 hata.

**Dördüncü tur — sarı/kırmızı satırlar, kaynak derinliği bilinçli olarak sınırlandı.**
Kullanıcı devam etmemi istedi: "sarı ve kırmızılara devam, kaynak çok önemli değil,
1 kaynakları bile olsa yeter... sahibinden'de gezerken gördüğüm her motor seçeneğini
görüyor olayım." Bu, Y-01'in "önce bileşen, sonra araç" sıra kuralını değiştirmedi
(hâlâ her yeni araç için önce motor/şanzıman ailesi açılıyor, kaynağıyla), ama kaynak
*sayısını* bilinçli olarak sınırladı — gerekçesi `docs/ARCHITECTURE.md` MK-12
kaydında. Bu turda **6 yeni motor ailesi** (`psa-bluehdi-15`, `psa-puretech-12`,
`toyota-8nr-fts`, `ford-ecoblue-15`, `bmw-b38`, `mb-m112`) ve **2 yeni şanzıman
ailesi** (`psa-eat8`, `mazda-skyactiv-6at`) açıldı, **13 araç** eklendi: Peugeot 3008
1.6 BlueHDi, Citroën C5 Aircross 1.5 BlueHDi, Opel Crossland X 1.2 PureTech, Toyota
C-HR 1.2 Turbo, Mazda CX-5 2.0 Skyactiv-G, Ford Focus 4 1.5 EcoBlue, MINI Cooper
(F56) 1.5, MINI Countryman (F60) 1.5, Mercedes E280 (W211), VW Polo 6 1.0 TSI DSG,
VW T-Roc 1.5 TSI, VW Golf 7 GTI 2.0 TSI, Kia Ceed SW 1.6 CRDi. `vag-ea211` ailesi
1.0-1.5 litre aralığına genişletildi (gerçekte tek bir modüler aile olduğu için yeni
aile açmaya gerek kalmadı).

**Sonuç (dördüncü tur):** araç sayısı 199 → 212. `arac_basina_ortalama_kaynak` 1.71'den
1.67'ye geriledi (beklenen, kabul edilen sonuç — MK-12). `yetim-kaynak` uyarısı 5'ten
3'e düştü. `validate.py` hâlâ 0 hata. Kalan bilinen boşluklar (Megane 3 1.2 TCe,
Clio 4 TCe, Laguna 1.9 dCi, Opel Insignia 2.0 Turbo, Opel Astra 1.7 CDTI) her biri
ayrı bir yeni motor ailesi gerektiriyor, henüz işlenmedi.

**Beşinci tur — kalan sarı/kırmızılar + yeni marka (Subaru) + 2016 sonrası kapsamı.**
Kullanıcı "devam etsene, araç eklemeye de devam et" dedi. Bu turda **5 yeni motor
ailesi** (`renault-tce-12`, `renault-f9q`, `gm-a20net`, `gm-z17dt`, `subaru-fb20`) ve
**1 yeni şanzıman ailesi** (`subaru-lineartronic`) açıldı, **9 araç** eklendi:
Renault Megane 3 1.2 TCe, Renault Clio 4 1.2 TCe, Renault Laguna 1.9 dCi, Opel
Insignia 2.0 Turbo, Opel Astra 1.7 CDTI (bunlar `docs/Y01B-MOTOR-CESITLENDIRME.md`'nin
son kalan 🟡/🔴 satırlarıydı), **Subaru Forester 2.0i Lineartronic** ve **Subaru XV
2.0i Lineartronic** (listede ilk kez yer alan beşinci yeni marka), Hyundai Kona 1.6
CRDi 7DCT ve Seat Leon 1.5 TSI (2016 sonrası kapsamını büyüten, tamamen mevcut
bileşenli 🟢 ekler).

**Sonuç (beşinci tur):** araç sayısı 212 → 221. `validate.py` hâlâ 0 hata.

**Ara değerlendirme — üç şarttan ikisi karşılandı, üçüncüsü bir araç uzaklıkta.**
SUV sayısı hedefi aştı (28/25 ✅). **Marka şartı karşılandı (5/5 ✅: Dacia, Jeep,
MINI, Cupra, Subaru).** 2016 sonrası araç sayısı 39/40.

**Altıncı tur (2026-08-07) — kullanıcı "araç sayısını, araştırma sayısını, kaynak
sayısını artır" dedi.** `docs/Y01-HEDEF-LISTE.md`'nin A/B/C bölümleri artık tamamen
işlenmiş durumda olduğu için bu turda listede henüz hiç kapsanmayan, ama gerçekten
Türkiye piyasasında yaygın yeni model/nesil boşlukları arandı. **1 motor ailesi
hacim genişletmesi** (`vag-ea111-tsi-turbo`, 1.4'ten 1.2'ye — Skoda Fabia'nın 1.2
TSI'ı için, EA211'in 1.0/1.4/1.5 genişlemesiyle aynı mantık) ve **1 yeni şanzıman
ailesi** (`zf-8hp`, BMW F30 için) açıldı, **7 araç** eklendi:

- `peugeot-208-1-2-puretech-eat8`, `peugeot-2008-2-1-2-puretech-eat8`,
  `citroen-c3-aircross-1-2-puretech-eat6` — üçü de mevcut PSA ailelerine
  (`psa-puretech-12`, `psa-eat8`/`aisin-eat6`) bağlanan 🟢 ekler; ikisi listenin
  en yeni model yılına (2020-2023) sahip araçları, önceden boş olan `age` kriterinin
  85-100 bandına ilk kez gerçek bir örnek düştü.
- `skoda-fabia-1-2-tsi-dsg` — motor ailesi hacim genişletmesiyle 🟡.
- `bmw-f30-320d` — mevcut `bmw-n47` + yeni `zf-8hp`; listenin ilk F30 kaydı.
- `vw-touran-1-4-tsi-dsg` — listenin **ilk MPV gövde tipi** kaydı; mevcut
  `vag-ea111-tsi-tc` (twincharger, tekli turbolu `vag-ea111-tsi-turbo`'dan ayrı aile)
  ve `vag-dq200`'e bağlandı.
- `audi-a3-8v-1-4-tsi-stronic` — mevcut `vag-ea211` + `vag-dq200`; A3'ün 8V (üçüncü)
  neslini listeye ekliyor.

Araştırma sırasında iki gerçek düzeltme/dikkat noktası ortaya çıktı ve kayıt altına
alındı: Mercedes W205 (C-Serisi) için motor tarafında `mb-m270`'in yalnızca A/B
Serisi'nin enine motoru olduğu, C-Serisi'nin boyuna `M274` kullandığı fark edildi ve
bu araç bu yüzden bu turda **eklenmedi** (yeni motor ailesi araştırması gerektiriyor,
sonraya bırakıldı — yanlış aileye bağlamaktansa eklememek tercih edildi). Toyota
Yaris de benzer bir sebeple (hibrit/normal motor karışıklığı riski, 1NR-FE/2NR-FE
motor kodunun doğrulanamaması) bu turda eklenmedi. Dacia Sandero Stepway, Türkiye'de
"EDC" değil **Easy-R** (tek kavramalı robotlu, "Robot" tipi) şanzımanla satıldığı
araştırma sırasında ortaya çıktığı için mevcut `renault-edc-kuru` ailesine
bağlanamadı; ayrı bir "Robot" tipi bileşen ailesi gerektiriyor, sonraya bırakıldı.

**Sonuç (altıncı tur):** araç sayısı 221 → 228, marka sayısı değişmedi (32 — bu turda
eklenen 7 araç hepsi zaten listede olan markalardan), SUV 28 → 30, **2016 sonrası araç
sayısı 39 → 42 (hedefi (40) aştı)**. `validate.py` hâlâ 0 hata.

**Bitmiş sayılma ölçütü — üç şartın üçü de karşılandı.** SUV hedefi aştı (30/25 ✅).
Marka şartı karşılandı (5/5 ✅). **2016 sonrası hedefi de aştı (42/40 ✅).**

**Kalan iş, düşük öncelik.** `docs/Y01-HEDEF-LISTE.md`'nin D bölümü (Lexus, Togg,
MG'nin EV/PHEV modelleri) **kalıcı olarak kapsam dışı** (MK-13). MG'nin geleneksel
yakıtlı modelleri (varsa), Mercedes W205 (yeni `M274` motor ailesi gerekiyor), Toyota
Yaris (motor kodu doğrulanmalı) ve Dacia Sandero/Logan gibi Easy-R'li modeller
(yeni "Robot" tipi bileşen ailesi gerekiyor) araştırılmayı bekleyen somut adaylar.

Y-01'in üç hedefi karşılandığı için o tarihte tamamlandı sayıldı ve odak Y-02'ye
kaydı. Aşağıdaki "Y-01 · İkinci dalga" bölümü, Y-01'in daha sonra farklı bir sebeple
— kapsam genişliği değil kapsam **derinliği** — yeniden açıldığını anlatıyor.

---

## Y-01 · İkinci dalga: 300-900 bin TL bandında marka-model-motor-şanzıman çeşitliliği — **sürüyor**

**Neden yeniden açıldı.** Kullanıcı listeyi inceleyip şu tespiti yaptı: *"bu en
popüler arabaların nerdeyse hiçbir motor seçeneğini göremiyorum???? ... araç
modelleri hep yukarı fiyat yönlü genişletilmiş. 300-900 bin arası modeller en az
80-90 marka-model-motor-şanzıman kombinasyonu eklenmeli."* Birinci dalga (yukarıdaki
Y-01) SUV sayısı, marka sayısı ve 2016 sonrası araç sayısı gibi **genişlik**
hedeflerini karşılamıştı, ama aynı modelin farklı motor/şanzıman kombinasyonlarını
kapsayan **derinlik** boyutunu hedeflememişti. Bu ikinci dalga onu düzeltiyor.

Aynı istekte iki ek karar de netleşti: (1) `fun`/`comf`/`cost` kriterleri için
GitHub'da bulunan bir teknik özellik veri setinin (ağırlık, tork, yakıt tüketimi)
kullanılması — lisans durumu araştırılıp MK-15 olarak kayda geçti; (2) filtre
seçeneklerinin (yıl, beygir, fiyat) hem sayı girişiyle hem sürüklemeli aralık
kaydırıcılarıyla genişletilmesi.

**Yedinci tur — 12 araç, spec veri setiyle eşleştirme.** `ilyasozkurt/automobile-
models-and-specs` (autoevolution kaynaklı, LICENSE dosyası yok) referans olarak
kullanıldı; marka + beygir + hacim (±0.05L) + yıl aralığı örtüşmesi + model adı
eşleşmesiyle 134 araca `kerb_weight_kg`/`torque_nm`/`fuel_consumption_l_100km`
işlendi, eşleşmeyen 106 araç boş bırakıldı (tahmin yürütülmedi). Aynı turda 12 yeni
araç eklendi: Opel Corsa D, Opel Astra J CDTI, Ford Fiesta PowerShift, Peugeot 301,
Citroën C3 PureTech-EAT6, Citroën C-Elysée, Skoda Fabia 1.0 TSI DSG, Skoda Rapid TDI
DSG, Seat Ibiza 1.0 TSI DSG, VW Polo 5 1.4 DSG, Hyundai i20 1.4 Otomatik, Fiat Egea
1.4 Robotlu. `templates/app/30-filtreler.js` içine yıl/beygir/fiyat için çift
kaydırıcılı (dual-range) aralık filtreleri eklendi; eski beygir/bütçe "kova" (bucket)
filtreleri bunlarla örtüştüğü için kaldırıldı.

**Sekizinci tur (2026-08-07) — 5 araç, gerçekten yeni bileşen aileleri.** Yedinci
turun aday listesindeki bazı araçlar mevcut motor/şanzıman ailelerine zorla
bağlanamadığı için boş geçilmişti. Kullanıcı bunun üzerine *"tamam yeni motor
ailelerine açıl abi! ... sen güzelce eşleştire eşleştire git. hepsini otomatik
yaptığından emin ol"* dedi — yani reddedilen adaylar için doğru aileyi araştırıp
açmak, var olan bir aileye yanlış eşlemektense. Bu turda 4 yeni motor ailesi
(`toyota-1nr-fe`, `nissan-hr12de`, `honda-l13z`, `kia-kappa-12`) ve 2 yeni şanzıman
ailesi (`honda-cvt-earthdreams`, `hyundai-a4cf`) açıldı, 5 araç eklendi: Toyota Yaris
1.33 Multidrive, Nissan Micra 1.2 CVT, Honda Jazz 1.3 CVT, Kia Picanto 1.2 Otomatik,
Dacia Duster 1.5 dCi EDC (2. nesil). `nissan-hr12de` ailesi bilinçli olarak yalnızca
atmosferik "HR12DE" kodunu kapsıyor; kompresörlü "HR12DDT (DIG-S)" farklı bir arıza
profiline sahip olabileceği için aileye dahil edilmedi. Duster'ın motor ve şanzıman
kombinasyonu araştırılırken aynı kombinasyonun `renault-clio-4-1-2-tce.json`'da
zaten kayıtlı olduğu fark edilip mükerrer kayıt önlendi. Beş aracın da şanzımanı
gerçekten otomatik (üçü CVT, biri kuru DCT, biri tork konvertörlü klasik otomatik);
her biri için `evidence.motor`/`evidence.trans` bağlı ailenin temel puanından
mekanik olarak türetildi. Araç sayısı 240 → 245.

**Dokuzuncu-on ikinci turlar — var olan ailelere eşleştirme + üç yeni aile.**
Dokuzuncu tur (4 araç, VAG grubu: Citroën Grand C4 Picasso/C4 Picasso, Seat Arona,
VW T-Cross) yeni aile açmadan var olan bileşenleri farklı marka-modellere
eşleştirdi. Onuncu tur (6 araç, yine VAG: Skoda Octavia/Superb'in eksik hacim
seçenekleri, Seat Ibiza/Leon'un eski nesli, VW Polo GTI) aynı yöntemi sürdürdü.
On birinci tur (4 araç, Honda/Hyundai/Kia) iki yeni motor ailesi açtı:
`honda-l15b7-turbo` (Civic FC'nin 1.5 turbo VTEC'i) ve `hyundai-nu-18` (Elantra
MD'nin 1.8'i; 2015'teki resmî geri çağırma ve grup davası nedeniyle düşük
puanlandı — MK-16 öncesi bir örnek: kaynak, aracın kendi araştırmasından değil
motor ailesinin kendi kaydından geliyor). On ikinci tur (1 araç, Ford) iki yeni
aile daha açtı: `ford-ecoboost-10` (soğutucu sızıntısı garanti uzatmasına konu
oldu, düşük puanlandı) ve `ford-selectshift-8at` (Focus Mk4'te sorunlu Powershift
DCT'nin yerine geçen Aisin kaynaklı 8 ileri tork konvertörlü kutu).

Bu turlarda gerçek bir hata yakalanıp düzeltildi: `data/criteria.json` motor ve
trans kriterleri için ayrı bant şemaları tanımlıyor (aynı puan aralığı iki
kriterde farklı bant adı taşıyor), ama evidence doldurma betiği ilk yazıldığında
tek bir ortak fonksiyon kullanıp motor'un bant adlarını trans'a da uyguluyordu.
Betik canlı şemadan okuyacak şekilde yeniden yazıldı (bkz. `.fill_evidence.py`
kalıbı, her turda yazılıp silinen dot-prefixli betik). Ayrıca `data/engines.json`,
`data/transmissions.json` ve üç eski araç kaydında CLAUDE.md §1'in yasakladığı
"X değil Y" kalıbında birkaç cümle bulunup düzeltildi.

**On üçüncü-on dördüncü turlar (7 araç) — PSA/GM/Renault/Nissan, var olan
ailelere eşleştirme.** Peugeot 308 GT 2.0 BlueHDi EAT8, Citroën C4 Cactus 1.2
PureTech EAT6, Citroën Grand C4 Picasso 2.0 BlueHDi EAT6 (aynı gövdenin 1.6
e-HDi'sinden farklı motor), Peugeot 308 3 Kapı 1.6 VTi 4AT, Opel Astra H 1.8
16V 4AT, Renault Mégane 4 Grandtour 1.6 dCi 165 EDC, Nissan Qashqai J10 1.6
CVT. Toyota Avensis T25 1.8 için araştırılan iki motor ailesi de (toyota-zz
sadece 1.6, toyota-zr farklı bir nesil/teknoloji) hacim veya nesil
uyuşmazlığı gösterdiği için zorla eşlenmedi, boş geçildi.

**On beşinci-on altıncı turlar (6 araç) — kullanıcı yönlendirmesiyle popüler
modellere odaklanma.** Kullanıcı *"popüler markaların ve modellerin motor
seçenekleri artsın... en popülerleri arttırmaya çalış"* dedi ve niş/düşük hacimli
adaylar yerine Türkiye'de gerçekten sık aranan modellere geçildi: VW Passat B8
1.6 TDI DSG, Dacia Duster (2. Nesil) 1.3 TCe EDC (dizelin gerilemesiyle öne
çıkan benzinli seçenek), Honda CR-V III 2.0 i-VTEC 5AT (yeni motor ailesi
`honda-r20a`; Türkiye'de yaygın ikinci el otomatik SUV), Peugeot 3008/5008'in
eksik motor/gövde seçenekleri, ve son olarak Mercedes W205 C-Class (listede
hiç yoktu; iki yeni aile açıldı: `mb-m274` ve `mb-9g-tronic`, Türkiye'de en çok
aranan ikinci el Mercedes nesillerinden biri).

**Sonuç (dokuzuncu-on altıncı turların toplamı).** Araç sayısı 245 → 273 (28
araç), toplam yeni açılan aile sayısı: 6 motor (`honda-l15b7-turbo`,
`hyundai-nu-18`, `ford-ecoboost-10`, `honda-r20a`, `mb-m274`) + 3 şanzıman
(`ford-selectshift-8at`, `mb-9g-tronic`, dolaylı olarak). `validate.py` her
turdan sonra 0 hata, `smoke_test.js` 49/49.

**MK-16 — kaynak mirası (bu turların arasında, ayrıca kayıtlı).** Y-01'in bu
ikinci dalgası sürerken kullanıcı kaynak derinliğini de artırmayı istedi;
`docs/ARCHITECTURE.md` MK-16'da yazılı mekanik geçiş, her aracın kendi bağlı
olduğu motor/şanzıman ailesinin zaten kayıtlı kaynaklarını miras almasını
sağladı — bu, "doğrulanmış" araç sayısını 9'dan 180'e çıkardı (bkz. Y-02
üçüncü tur, aşağıda).

**On yedinci tur (2026-08-07) — 3 araç, önceki turun notlarına dönüş.**
Önceki turda not edilen dört adaydan ikisi gerçek, sourced kanıtla kapatıldı:
BMW F30 320i (yeni motor ailesi `bmw-n20` — nesil belirsizliği, N20'nin
2011-erken 2015 pre-LCI üretimine, B48'in kapsam dışına bırakılmasına karar
verilerek çözüldü; kusur ABD'de Şubat 2021'de kesinleşen federal bir grup
davası ve BMW'nin resmi garanti uzatmasıyla doğrulanıyor — carcomplaints.com,
tier B) ve Hyundai Tucson/Kia Sportage 1.6 T-GDI 7DCT (yeni motor ailesi
`hyundai-gamma16-tgdi`, mevcut `hyundai-7dct` şanzıman ailesine bağlandı;
motor kusuru carchecker.pro'nun Tucson TL raporundan, tier C). Renault
Symbol/Thalia bu turda da atlandı: JATCO JF404E'nin bu araçta kullanıldığı
teyit edilebildi ama İngilizce/Türkçe hiçbir kaynakta bu kutuya özgü,
doğrulanabilir bir arıza örüntüsü bulunamadı — "boş alan yanlış alandan
iyidir" ilkesiyle zorla eklenmedi. Renault Fluence'ın ROADMAP'te "tedarikçi
doğrulanamadı" diye not edilen adayı zaten `data/cars/renault-fluence-1-6.json`
olarak dolu kayıtlıydı; not stale imiş, düzeltildi. `validate.py` 0 hata (95
kaynak-yetersiz, 33 c-kaynakla-uc-puan — ikisi de bu turdan önce de vardı),
`smoke_test.js`'in iki testinde sabit yazılı araç sayısı (273→276, 275→278)
güncellendi, 49/49.

**On sekizinci tur (2026-08-07) — 2 araç, mevcut ailelere düşük riskli eşleştirme.**
Yeni bileşen ailesi açmadan, tamamen listede zaten kayıtlı ve kaynaklı ailelere
eşleştirilen iki araç: Skoda Scala 1.0 TSI DSG (`vag-ea211` + `vag-dq200`,
Fabia/Ibiza/Polo'daki aynı kombinasyon; Rapid'in yerine geçen model listede
hiç yoktu) ve Renault Captur 1.2 TCe EDC (`renault-tce-12` + `renault-edc-kuru`,
listede zaten kayıtlı dizel Captur'un benzinli kardeşi). İkisi de "boş alan
riskli tahminden iyidir" ilkesinin tersi bir durumu gösteriyor: risk düşükken
(bileşenler zaten doğrulanmış) hızlı eklenebilecek gerçek boşluklar. `validate.py`
0 hata, `smoke_test.js`'in iki testinde sabit yazılı araç sayısı (276→278,
278→280) güncellendi, 49/49.

**Toplam durum (228 baseline'dan bu yana).** Araç sayısı 228 → 278 (50 yeni
kombinasyon), kullanıcının koyduğu 80-90 hedefinin yarısından fazlası
karşılandı. Bu iş doğası gereği kapanmayan, sürekli genişleyebilecek bir iş
kalemi. Renault Symbol/Thalia (1.6L 16V, otomatik kutu tedarikçisi JATCO
JF404E olarak teyit edildi ama arıza kanıtı yok — hâlâ araştırılmayı
bekliyor) ve `/tmp` önbelleğindeki 550 satırlık aday listesinden taranmamış
kalan adaylar sıradaki turlar için not. Sıradaki düşük riskli adaylar: Skoda
Kamiq (aynı VAG bileşenleri), Peugeot 2008/208'in eksik motor seçenekleri
(mevcut `psa-puretech-12`/`psa-eat8` ailelerine bağlanabilir).

---

## Y-10 · Dış veri paketi entegrasyonu (P2.1) — **birinci tur bitti**

**Ne geldi.** 2026-08-13'te 1.641 araç–motor–şanzıman kombinasyonu, 2.071 tarihli ilan
gözlemi ve 112 fiyat grubu içeren bir dış veri paketi (P2.1) elimize geçti. Paket depoyla
hizalıydı: motor ve şanzıman kimlikleri bizim bileşen sicilimizi kullanıyordu, 220 aracımız
pakette de vardı.

**Ne yapıldı, öncelik sırasıyla.** Cazip olan ilk hamle 1.641 satırı içe aktarmaktı; bu
bilinçli olarak yapılmadı (MK-21). Bunun yerine paketin **kanıt değeri** kullanıldı:

1. **Çapraz doğrulama (MK-18).** 220 ortak araç iki veri setinde karşılaştırıldı. Motor ve
   şanzıman ailelerinde sıfır çelişki çıktı — bileşen sicilimizin sağlam olduğunun bağımsız
   teyidi. Beygir ve torkta 10 çelişki bulundu; her biri ayrıca araştırıldı ve doğrulanan
   5 gerçek hata düzeltildi. En ağırı `bmw-e46-320i`: araç dört silindirli bir motor
   ailesine bağlıydı, oysa E46 320i her zaman sıralı altı silindirliydi. İkincisi
   `vw-passat-b7-1-6-tdi`: 1,6 litrelik bir dizelde 400 Nm kayıtlıydı ve bu, aracı sürüş
   keyfi sıralamasında haksız yere ilk ona taşıyordu.
2. **Fiyat katmanı tarihlendi (MK-19).** `docs/PLAN.md` §3.8'in istediği `as_of` ve
   `method` alanları `price_reference` bloğu olarak şemaya girdi; 19 araç gerçek, tarihli
   piyasa gözlemine bağlandı. Ölçüm, tahminlerimizin **medyan %8 düşük** kaldığını
   gösterdi (19 aracın 15'inde) — enflasyon aşınmasının ölçülmüş kanıtı.
3. **Tork geri dolduruldu.** 79 araca tork verisi işlendi (kapsam 172 → 251/278); beygir ve
   hacim birlikte doğrulanmadan hiçbir değer yazılmadı, uyuşmayan tek kayıt boş bırakıldı.
4. **`liq` reddedildi (MK-20).** İlan sayıları likidite ölçüsü olarak kullanılmadı, çünkü
   örneklem sorgu başına 50 ile sınırlı ve tam olarak ölçmek istediğimiz yönde sansürlü.
5. **Adaylar kuyruğa alındı (MK-21).** `data/queue/car-candidates-p21.json`.

**Bir sonraki tur için hazır iş.** Kuyruk dosyası iki somut liste taşıyor:

- **6 hazır aday** — motor ve şanzıman ailesi repoda zaten kayıtlı, yalnızca araca özgü
  kaynak araştırması ve `evidence` bloğu gerekiyor (BMW 118i F20 LCI, Audi A3 1.0 TFSI,
  Kia Ceed 1.6 CRDi 7DCT, Nissan Qashqai J11 1.3 DIG-T, Opel Corsa F 1.2 Turbo EAT8,
  Renault Captur II 1.3 TCe EDC).
- **30 motor ailesi eşleme önerisi** — doğrulanırsa **434 aracın** önünü açıyor. Bunlar
  yeni aile araştırması değil, kimlik çözümleme işi: P2.1'de motor kodu "belirtilmemiş"
  kalmış ailelerin, marka + yakıt + hacim üçlüsüyle repodaki karşılığına bağlanması. En
  yüksek kaldıraçlılar: BMW 2.0 dizel (36 araç), BMW 2.0 benzin (31), BMW 3.0 dizel (23),
  Mercedes 2.1 dizel (23), VAG 2.0 dizel (23).

**Kapanmayan boşluk — boş ağırlık.** P2.1'de boş ağırlık alanı hiç yok. Tork
doldurulduktan sonra `fun` formülünün önündeki **tek engel** bu alan kaldı: 88 araçta tork
var ama ağırlık yok. Bu 88 aracın ağırlığı doldurulursa `fun` kapsamı 163'ten 251'e çıkar,
yani tek bir veri kalemi kriterin kapsamını yarı yarıya büyütür. Sıradaki en yüksek getirili
veri işi budur.

---

## Y-02 · Her aracın en az bir gerçek kaynağı olsun, ortalama dörde yaklaşsın — **hedef karşılandı**

**Öncelik: yüksek.** Projenin bütün iddiası kanıta dayanmak; kanıtsız araç bu iddiayı
zayıflatıyor.

**Ne yapıldı.** Y-03'teki araştırma kuyruğu kurulduktan sonra ilk yükü olarak, o tarihte
kaynaksız olan 14 araca gerçek kaynak arandı (WebSearch ile): `alfa-romeo-mito-1-4`,
`audi-a3-8p-2-0-tdi`, `audi-a4-b5-1-8t-2-4`, `bmw-e87-116i-118i`, `bmw-e90-316i`,
`chevrolet-cruze-1-6`, `citroen-xsara-1-6`, `hyundai-accent-blue-1-6-benzinli`,
`hyundai-i40-1-7-crdi`, `kia-optima-1-7-crdi`, `peugeot-307-1-6`,
`skoda-octavia-1-8-tsi`, `vw-passat-b6-1-8-tsi`, `vw-passat-b7-2-0-tdi`. Her biri için
en az bir gerçek, erişilebilir kaynak bulundu, güven seviyesi (B veya C — hiçbiri A
değil, çünkü hepsi forum/şikayet toplamı niteliğinde) verildi ve `data/sources.json` ile
ilgili araç kaydına işlendi; `verification` alanları `preliminary`'den `partial`'a
geçti. Hiçbir puan bu turda değiştirilmedi — yalnızca kanıt eklendi; motor/şanzıman
temel puanları zaten paylaşılan bileşen kayıtlarından geliyor, araç kaydına eklenen
kaynak o aracın kendi kanıt zincirini tamamlıyor (bkz. "önemli ayrım" aşağıda).

**İkinci tur — derinlik: "her araca 1 motor + 1 şanzıman kaynağı".** Kullanıcı yeni ve
somut bir hedef koydu: *"kaynak derinliğiyle devam edebiliriz, tek kaynaklı araçlara
odaklanalım. Hedef her araca 1 motor + 1 şanzıman kaynağı."* Bu, Y-02'nin orijinal
"ortalama 2.5" hedefinden daha net bir kural: bir aracın kanıt zinciri, iki ana
bileşeninin (motor ve şanzıman) **ikisini birden** karşılamalı; yalnızca motor tarafını
anlatan bir kaynak aracın şanzıman puanını dayanaksız bırakıyor.

2026-08-06'da bu tur uçtan uca çalıştırıldı ve **tek kaynaklı 118 aracın tamamı
kapatıldı.** Yöntem: her araç, bileşen ailesine (motor veya şanzıman) göre gruplandı ve
eksik olan taraf için kaynak arandı. Bir kaynak aynı bileşen ailesini paylaşan bütün
araçlara bağlanabildiği için tur verimli ilerledi — örneğin ZF 5HP/6HP bakım rehberi 8
BMW'ye, VAG DSG (DQ200/DQ250) derlemesi 21 VAG aracına, Renault EDC forum başlığı 10
Renault'ya, Aisin 6 ileri derlemesi 12 farklı markadan araca bağlandı.

Bu turda **10 yeni kaynak** eklendi; hepsi bileşen seviyesinde (şanzıman ailesi bakım
rehberi, motor ailesi kronik arıza derlemesi) olduğu için tekil araç kaynaklarından daha
geniş kapsamlı. Ayrıca bir veri hatası düzeltildi: `bmw-e90-318d` kaydı M47 motorlu
olmasına rağmen N47 hakkında bir kaynağa bağlıydı, doğru kaynakla değiştirildi.

**Bugünkü tablo** (derinlik turundan sonra, 221 araç üzerinden):

| Kaynak sayısı | Araç | Durum |
|---:|---:|---|
| 0 | 0 | — kalmadı |
| **1** | **0** | **— kalmadı** |
| 2-3 | 213 | Kısmi |
| 4+ | 8 | Doğrulanmış |

Araç başına ortalama kaynak **1.65 → 2.18**'e çıktı. `c-kaynakla-uc-puan` uyarısı da
32'den 22'ye düştü: eklenen kaynakların bir kısmı B seviyesinde olduğu için, daha önce
"yalnızca C kaynağa dayanarak uç puan verilmiş" diye işaretlenen bazı araçlar artık bu
uyarıyı üretmiyor. Yani derinlik turu sadece sayıyı değil, **kanıt kalitesini de**
yükseltti.

**Önemli ayrım (o tarihte doğruydu, üçüncü turda değişti — aşağıya bakın).** Bu
turda motor ve şanzıman ailelerine verilen kaynaklar araç kaydına **elle, tek tek**
bağlandı; otomatik bir yansıma yoktu. Bir aracın kendi kaydında da o araca özgü kanıt
olmalı — kullanıcı yorumu, o modele özel arıza derlemesi, Türkiye'ye özgü bir şikayet
örüntüsü. Kullanıcının istediği "her araç için en az bir yorum kapsanmalı" şartı tam
olarak budur.

**Bitmiş sayılma ölçütü — karşılandı.** Kaynaksız araç yok (✅), tek kaynaklı araç yok
(✅), araç başına ortalama kaynak 2.5 hedefinin altında ama 2.18'e çıktı ve kullanıcının
koyduğu asıl hedef ("her araca 1 motor + 1 şanzıman kaynağı") sağlandı.

---

### Üçüncü tur — mekanik miras, MK-16 (2026-08-07)

Elle bağlama turu (yukarıda) her tek kaynaklı aracı kapattı, ama sistematik değildi:
bazı araçlar hâlâ, kendi bağlı olduğu motor/şanzıman ailesinin `data/engines.json` /
`data/transmissions.json` içinde zaten kayıtlı, zaten doğrulanmış kaynağını
listelemiyordu. Örnek: `renault-megane-2-1-6` kaydı K4M motoruna bağlıydı ama
`renault-k4m` ailesinin kendi kaynağı (`bigskies_k4m`) bu aracın `sources`
listesinde hiç yoktu — kaynak gerçek ve ilgiliydi, sadece unutulmuştu. Aynı boşluk
232 araçta tekrarlanıyordu.

Kullanıcının *"özellikle kaynakları ... arttır"* talimatı üzerine bu boşluk
mekanik bir geçişle kapatıldı: her aracın `specs.engine_id` ve
`specs.transmission_id` alanları üzerinden bağlı olduğu ailenin **bütün**
kaynakları, aracın kendi `sources` listesine (küme birleşimi, yineleme yok)
katıldı ve `verification` etiketi yeniden hesaplandı. Bu, MK-14'teki TÜV
kararının tersi bir durumdur ve gerekçesi MK-16'da yazılı: TÜV eğrisi bütün
araçlara aynı şekilde uygulanan genel bir referanstı, buradaki kaynaklar ise
tanım gereği o aracın **gerçekten taşıdığı** bileşenle ilgili (bağ zaten
`validate.py`'nin hacim/tip denetimiyle doğrulanmış durumda).

**Sonuç.** 249 aracın 232'sinde kaynak listesi genişledi. `dogrulanmis` **9 → 177**,
`arac_basina_ortalama_kaynak` **2,22 → 4,31**, `kaynak-yetersiz` uyarısı **240 → 72**.
`MAX_CARS_PER_SOURCE` sınırını aşan yeni bir tekil-dayanak riski oluşmadı (yalnızca
zaten 1'den fazla kaynağı olan araçlarda kaynak sayısı büyüdü). `validate.py` 0 hata.

**Kalan iş (o tarihte).** 72 araç hâlâ "kısmi kaynak" — bunların çoğu bağlı olduğu
motor/şanzıman ailesinin de az kaynaklı olduğu (1-2 kaynak) durumlar, yani mekanik
mirasın tavan yaptığı yerler. Buradan sonrası tekrar elle, araç veya bileşen bazlı
gerçek araştırma gerektiriyor. (Y-01'in sonraki turları bu sayıyı 95'e çıkardı, çünkü
her yeni araç kendi bileşen ailesiyle başlıyor — bkz. dördüncü tur.)

### Dördüncü tur — bileşen ailesi kaldıraçlı derinleştirme (2026-08-07)

Üçüncü turun notu doğruydu: kalan 95 kısmi-kaynaklı aracın çoğu, kendi bağlı olduğu
motor/şanzıman ailesinin zaten az kaynaklı olmasından geliyordu. Tek tek araç
araştırmak yerine, en çok aracı etkileyen az-kaynaklı aileler önce bulundu (`data/
cars/*.json`'ı `engine_id`/`transmission_id`'ye göre gruplayıp kısmi-kaynaklı araç
sayısına göre sıralayarak) ve o beş aile için WebSearch'le **gerçekten yeni** bir
kaynak arandı — bir ailenin kaynak sayısını 1 artırmak, o aileyi paylaşan bütün
araçları aynı anda etkiliyor.

Beş aile güncellendi, her biri için mevcut kaynaklardan **farklı** bir kaynak
bulunup `known_issues` (üçü daha önce boştu, yalnızca serbest metin `note` alanında
anlatılıyordu — artık yapılandırılmış ve kaynaklı) eklendi:

| Aile | Etkilenen araç | Yeni kaynak | Eklenen bulgu |
|---|---:|---|---|
| `vag-dq200` (7 ileri kuru DSG) | 15 | eco-torque.co.uk | Erken üretim kavrama paketi arızası, 0AM mekatronik basınç haznesi çatlağı |
| `psa-al4` (DPO) | 10 | teknikotomatiksanziman.com | Şanzıman beyni/solenoid valf arızası, yapılandırılmış known_issues |
| `aisin-eat6` | 10 | asrgearboxrepairs.co.uk | Mekanik arıza nadir, sert geçiş valf gövdesi tortusundan |
| `vag-ea211` (1.0/1.2/1.4/1.5 TSI) | 7 | enginecrux.com | Erken üretimde ölçülü yağ tüketimi (zincir sorunu EA111'den kalkmış) |
| `vag-ea288` (1.6/2.0 TDI) | 6 | enginefinders.co.uk | 170 PS varyantında triger zinciri uzaması, AdBlue enjektör/sensör arızası |

Yeni kaynaklar `data/sources.json`'a eklendikten sonra, MK-16'nın kurduğu mekanik
miras ilkesi tekrar uygulandı (bir kerelik betikle: `specs.engine_id`/
`specs.transmission_id`'si bu beş aileden birine bağlı her aracın `sources`
listesine ilgili yeni kaynak eklendi, `verification` yeniden hesaplandı) — MK-16'nın
kalıcı bir betik bırakmaması nedeniyle bu geçiş de aynı desende, tek seferlik bir
betikle yapıldı.

**Sonuç.** 64 araç etkilendi. `dogrulanmis` **181 → 213**, `kismi_kaynak`
**95 → 63**, `arac_basina_ortalama_kaynak` **4,18 → 4,48**, `kaynak-yetersiz`
uyarısı **95 → 63**. `validate.py` 0 hata, `smoke_test.js` 49/49.

**Kalan iş (o tarihte).** 63 araç hâlâ kısmi kaynak. Aynı kaldıraç yöntemi
tekrarlanabilir: sıradaki en yüksek kaldıraçlı adaylar `psa-puretech-12` (5
araç), `psa-dw10` (5 araç), `toyota-zr` (4 araç), `psa-dv6` (4 araç),
`psa-ep6-vti` (4 araç) — hepsi tek kaynaklı aileler.

### Beşinci tur — aynı kaldıraç yöntemi, ikinci raunt (2026-08-07)

Dördüncü turun notundaki adaylardan altısı işlendi: `aisin-af40` (7 araç,
1→2 kaynak), `psa-dw10` (5 araç, 1→2), `psa-eat8` (5 araç, 2→3),
`toyota-multidrive` (5 araç, 2→3), `psa-puretech-12` (4 araç, 1→2),
`toyota-zr` (4 araç, 1→2). Her biri için WebSearch'le gerçekten yeni bir
kaynak bulundu (ör. `psa-dw10`'a çift kütleli volan aşınması, `psa-puretech-12`'ye
yağ seyrelmesinin kayış aşınmasını hızlandırma mekanizması, `toyota-zr`'ye
2ZR-FE'nin oksijen sensörü/ateşleme bobini kalemleri eklendi) ve daha önce
boş olan `known_issues` alanları yapılandırıldı. Aynı mekanik miras geçişi
tekrarlandı: 28 araç etkilendi.

**Sonuç.** `dogrulanmis` **213 → 233** (bu turun kendisi, Y-01'in aynı günkü
on sekizinci turunda eklenen 2 doğrulanmış araçla birlikte toplam 235),
`kismi_kaynak` **63 → 43**, `arac_basina_ortalama_kaynak` **4,48 → 4,63**,
`kaynak-yetersiz` uyarısı **63 → 43**. `validate.py` 0 hata, `smoke_test.js`
49/49.

**Kalan iş.** 43 araç hâlâ kısmi kaynak, artık büyük ölçüde 1-2 araçlık
kuyruk (`hyundai-u2-16`, `psa-bluehdi-15`, `renault-h5ht`, `ford-sigma-tivct`,
`hyundai-6at`, `getrag-7dct300`, `psa-etg` gibi) — kaldıraç etkisi azalıyor,
bundan sonrası tek tek araç/aile araştırmasına daha yakın.

---

### Altıncı-onbirinci turlar — bileşen arıza sicilinin yapılandırılması (2026-08-13)

**Sorun.** Beşinci turdan sonra kaynak derinliği iyiydi ama bileşen kayıtlarının önemli bir
kısmında `known_issues` alanı **tamamen boştu**: arıza bilgisi yalnızca serbest metin
`note` alanında duruyordu. 157 aileden **49'u** bu durumdaydı. Yapılandırılmamış bilgi
üç yerde birden işe yaramıyor: statik sayfalarda listelenemiyor, içerik üretiminde
(Y-12) kullanılamıyor, ve "hangi kilometrede ne bekleyeyim" sorusuna cevap veremiyor.

**Yöntem.** Y-02'nin kaldıraç mantığı sürdürüldü: en çok aracı etkileyen boş aileden
başlandı. Her aile için WebSearch ile yeni bir kaynak arandı, arıza kayıtları
(`issue`, `onset_km`, `frequency`, `severity`, `sources`) yapılandırıldı ve MK-16 mekanik
mirasıyla araçlara işlendi.

**İşlenen aileler.** Şanzıman: `vag-dq250`, `mb-5g-tronic`, `renault-edc-kuru`, `zf-6hp`,
`zf-5hp`, `hyundai-7dct`, `hyundai-6at`, `gm-aisin-af17`, `honda-4at-5at`,
`getrag-7dct300`, `mb-7g-tronic`, `vag-multitronic`, `aisin-aw55`, `ford-dps6`,
`psa-etg`, `vag-s-tronic-islak`, `gm-5l40e`, `hyundai-a4af3`, `aisin-geartronic`,
`aisin-tf80`, `fiat-c635-ddct`, `alfa-tct`, `zf-4hp`, `aisin-awf21`, `ford-4f27e`,
`ford-cd4e`, `volvo-powershift-kuru`. Motor: `psa-ep6-vti`, `bmw-m47`, `fca-fire-14`,
`hyundai-beta-16`, `kia-kappa-12`, `toyota-1nr-fe`, `honda-r20a`, `volvo-b5254`.

**İki puan değişikliği, ikisi de kanıt ağırlaştığı için.**

- **`ford-dps6` 36 → 30.** Sorun artık forum şikayeti değil: Vargas v. Ford federal grup
  davasının 7 Nisan 2020'de yürürlüğe giren ve gruba en az 77,4 milyon dolar güvence altına
  alan uzlaşması, üç ayrı garanti uzatması (14M01, 14M02, 19N08) ve federal soruşturmalarla
  kayıtlı. Bu, B seviyesi kanıt ve 35-49 bandının "bilinen risk" ifadesinin taşıyamayacağı
  kadar ağır.
- **`volvo-powershift-kuru` 38 → 32.** Arızanın ortaya çıktığı kilometre ölçüldü:
  belirtiler 40.000-60.000 km'de başlıyor, birçok araçta 80.000-100.000 km'de komple
  kavrama değişimi gerekiyor. Bu, en alt bandın tarifi.

**Yan etki, dürüstçe.** Volvo temel puanı düşünce iki D2 aracının `trans` puanı 28'den
32'ye **yükseldi**. Bu bir gerileme değil: eski 28 puanı, kendi gerekçe metninin de
söylediği gibi "kayıtlı bir gerekçesi olmayan" bir sapmaydı. Artık iki araç da aile temel
puanında oturuyor ve gerekçe kaynaklı.

**Bulunan üç kayda değer şey.**

1. **Honda 4/5AT'nin tork konvertörü titremesi bir kutu arızası değil.** Üreticinin kendi
   servis bülteni (NHTSA'da yayımlı, B seviyesi) açıkça yazıyor: titremeyi bozulmuş
   şanzıman yağı üretiyor ve kutu zarar görmüyor. Bu, yaygın forum algısını düzelten bir
   kayıt ve alıcıya "bu araçtan kaç" değil "yağını değiştir" dedirtiyor.
2. **Aisin TF-80SC'nin sorunu bir üretim penceresine bağlı.** Sert geçiş ve kayma
   şikayetlerinin onda dokuzu valf gövdesi kaynaklı ve **06J ve sonrası seri numaralı
   kutular güncellenmiş valf gövdesiyle üretiliyor.** Yani bu, ikinci el alıcısının araç
   başında doğrudan kontrol edebileceği bir ayrım.
3. **Aynı kutunun üç markadaki kaydı farklı puanlar taşıyor.** Getrag 6DCT250 ailesi
   `renault-edc-kuru` (54), `volvo-powershift-kuru` (32) ve `ford-dps6` (30) olarak üç
   ayrı kayıtta duruyor. Bu gerçek bir kalibrasyon sorusu olabilir — markalar kutuyu farklı
   tork seviyelerinde ve farklı yazılımla kullanıyor, ama 22 puanlık fark bunun tek başına
   açıklayabileceğinden büyük görünüyor. Her kayıt şimdilik kendi kaynaklarının gösterdiği
   yerde bırakıldı; **açık bir iş kalemi olarak not edildi.**

**Sonuç.** Kaynak sayısı 314 → 345, `dogrulanmis` 236 → 259, `kismi_kaynak` 42 → 19,
araç başına ortalama kaynak 4,64 → 5,28. Yapılandırılmış arıza kaydı **166 → 253**,
`known_issues` boş aile **49 → 14**. `validate.py` 0 hata, `smoke_test.js` 57/57.

**Kalan iş.** 14 aile hâlâ boş ve hepsi 1-2 araçlık kuyrukta; kaldıraç etkisi bitti,
bundan sonrası tek tek araştırma. 19 araç hâlâ kısmi kaynak.

---

### Onikinci tur — kalan 1-2 araçlık kuyruk ve bir motor kodu belirsizliğinin çözümü (2026-08-14)

**Kapsam.** Kalan 14 boş `known_issues` ailesinden en yüksek kaldıraçlı yedisi işlendi:
şanzıman tarafında `toyota-4at`, `gm-4t65e`, `aisin-aw60t`; motor tarafında `volvo-b5254`,
`nissan-hr12de`, `mb-om613`, `honda-l13z`. Aynı turda `volvo-b4204s` de düzeltildi, ama bu
bir "boş `known_issues`" işi değildi — daha köklü bir sorun vardı.

**Kendi hatam, kayıt altında.** Bu turun ilk taslağında `volvo-b5254` ailesini "boş"
sanıp yeni bulguları eskisinin **üzerine yazdım**; ailenin zaten üç sourced arıza kaydı
vardı (triger kayışı, PCV, konta sızıntısı — hepsi `enginecrux_volvo_b5254`'e dayalı).
Hata `git diff` ile fark edildi ve commit edilmeden düzeltildi: eski üç kayıt geri
getirildi, yeni üç kayıt bunların **üstüne eklendi** (silinmedi), aile artık 6 kayıtlı.
Bu, gerçekten boş olan aileyi (`volvo-b4204s`) doğru hedeflemek yerine yanlış bir listeye
güvenmenin bedeliydi — bir daha karıştırmamak için: boşluk kontrolü her turun başında
`known_issues == []` üzerinden tazelenmeli, önceki turun zihindeki listesine güvenilmemeli.

**`volvo-b4204s` — boş değil, çözülememiş bir kod eşlemesiydi.** Bu ailenin `base_score`'u
daha önceki bir turda **bilinçli olarak `null` bırakılmıştı**: B4204S kodunun 1995-1999
ilk nesil S40/V40'a mı, yoksa listedeki 2004-2012 ikinci nesil S40/V50'ye mi ait olduğu
belirsizdi ve kaynaksız bir puan üretmek projenin temel kuralına aykırı olurdu. Bu turda
yapılan araştırma belirsizliği çözdü: B4204S3/B4204S4 kodlu motor, Volvo'nun Ford ile
ortak P1 platformunda Mazda LF kökenli 2.0 atmosferik aileyi paylaştığı motor — 145 bg /
185 Nm / 1999cc atmosferik özellikleri, `volvo-s40-v50-2-0` aracının kayıtlı rakamlarıyla
birebir örtüşüyor. Motor adları listesine B4204S3/B4204S4 eklendi, `base_score` 68 olarak
kaynaklandı (tek kaynak, C seviyesi — bu yüzden temkinli). Aracın kendisinde de bir eksik
vardı: `motor` puanı (74) hiçbir `evidence.motor` bloğuna bağlı değildi, muhtemelen eski
bir içe aktarma kalıntısıydı. Puan artık aile temel puanıyla hizalı (68) ve gerekçeli bir
`evidence.motor` bloğu eklendi.

**Sonuç.** Kaynak sayısı 345 → 357, `dogrulanmis` 259 → 261, `kismi_kaynak` 19 → 17,
araç başına ortalama kaynak 5,28 → 5,34. `validate.py` 0 hata, `smoke_test.js` 57/57.

**Kalan iş.** 7 aile hâlâ boş `known_issues` taşıyor (`suzuki-4at`, `mb-7g-dct`,
`mb-4g-tronic`, `jatco-re4f0x`, `jatco-jf506e`, `hyundai-a4cf`, `alfa-q-system`), hepsi
1 araçlık kuyrukta. 17 araç hâlâ kısmi kaynak.

---

### Onüçüncü tur — son yedi ailenin kuyruğu temizlendi (2026-08-14)

**Kapsam.** Onikinci turun sonunda kalan yedi tek-araçlık aile işlendi:
`suzuki-4at` (Suzuki SX4), `mb-7g-dct` (Mercedes A/B Serisi), `mb-4g-tronic` (Mercedes
W202), `jatco-re4f0x` (Nissan Almera/Primera), `jatco-jf506e` (Rover 75), `hyundai-a4cf`
(Kia Picanto), `alfa-q-system` (Alfa Romeo 156). Bu ailelerin hepsinde `base_score` zaten
kaynaklıydı; eksik olan yalnızca yapılandırılmış `known_issues` kaydıydı, bu yüzden hiçbir
puan değişikliği yapılmadı — sadece mevcut puanın arkasındaki kanıt somutlaştırıldı.

**Bulunan bir uyum notu.** Suzuki SX4 için bulunan kaynakların bir kısmı CVT'li geç dönem
modellerden bahsediyordu; bu araç 2007-2014 üretim ve döneminin SX4'ü klasik 4 ileri
tork konvertörlü otomatik kullanıyor. CVT'ye özgü iddialar (60.000 km'de aşınma başlangıcı,
150.000 km altı ömür) bilinçli olarak `known_issues`'a alınmadı; yalnızca şanzıman tipinden
bağımsız, genel "anormal ses / tereddüt" şikayetleri kullanıldı.

**Sonuç.** Kaynak sayısı 357 → 365, `dogrulanmis` 261 → 265, `kismi_kaynak` 17 → 13,
araç başına ortalama kaynak 5,34 → 5,37. `validate.py` 0 hata, `smoke_test.js` 57/57.
**`known_issues` boş bileşen ailesi kalmadı (49 → 0)** — Y-02'nin altıncı turunda başlayan
bileşen arıza sicili yapılandırma çalışması bu turla tamamlandı.

**Kalan iş.** 13 araç hâlâ kısmi kaynak (4'ten az kaynak); artık aile bazlı kaldıraç
tükendi, bundan sonrası araç başına araştırma. Bu, Y-02'nin bir sonraki doğal adımı.

---

### Ondördüncü-onbeşinci turlar — kalan 13 araç ve bir kanıt karışması hatası (2026-08-14)

**Kapsam.** Onüçüncü turdan sonra kalan 13 kısmi kaynaklı aracın hepsi tek tek ele alındı.
Bu araçların bazıları zaten doğru aileye bağlıydı ama ailenin kendisi tek kaynaklıydı
(`subaru-lineartronic`, `mb-9g-tronic`, `mb-m274`, `ford-selectshift-8at`, `aisin-af40`,
`mazda-skyactiv-6at`, `honda-cvt-earthdreams`, `vag-01m`, `getrag-7dct300`,
`hyundai-gamma16-gdi`, `hyundai-gamma-14`, `ford-sigma-tivct`); her birine yeni ve
bağımsız bir kaynak eklendi, MK-16 mekanik mirasıyla ilgili araçlara işlendi.

**Bulunan bir kanıt karışması hatası, düzeltildi.** `subaru-xv-2-0i-lineartronic` ve
`subaru-forester-2-0i-lineartronic` araçlarının kaynak listesinde ve `evidence.motor` /
`evidence.trans` gerekçe metninde `sikayetvar_corolla_genel` adlı bir kaynak duruyordu —
bu kaynak **Toyota Corolla'nın** şikayet derlemesi, Subaru'yla hiçbir ilgisi yok. Muhtemelen
erken bir turda kopyala-yapıştır ya da yanlış kaynak kimliği seçimiyle oluşmuş bir hata.
Kaynak her iki araçtan da çıkarıldı; yerine FB20 motoruna (yağ tüketimi) ve Lineartronic
CVT'ye (2014-2016 valf gövdesi arızaları, 2014-2015 model yılı riski) özgü, gerçekten
ilgili iki yeni kaynak eklendi. Bu, projenin kanıt bütünlüğü ilkesinin neden her turda
`git diff` ile kontrol edilmesi gerektiğinin bir başka örneği — bkz. onikinci turdaki
benzer kendi-kendine-düzeltme kaydı.

**Sonuç.** Kaynak sayısı 365 → 379, araç başına ortalama kaynak 5,37 → 5,48.
**`kismi_kaynak` 13 → 0 — projedeki her araç artık "doğrulanmış" (4+ bağımsız kaynak).**
`validate.py` 0 hata, `smoke_test.js` 57/57.

**Bu neyi kapatıyor.** Y-02'nin (kaynak derinliği) asıl hedefi buydu: "kaynaksız araç yok,
tek kaynaklı araç yok" beşinci turda söylenmişti, şimdi bir adım öteye geçildi — kısmi
kaynaklı araç da yok. Bileşen ailesi seviyesinde de `known_issues` boş kalmadı (onüçüncü
tur). Y-02 bu iki ölçütle **fiilen tamamlandı**; kalan iş yeni araç eklendikçe (Y-01) o
araçları da aynı standarda getirmek, ve mevcut kaynakların derinliğini (ortalama 5,48)
zamanla daha da artırmak.

---

## Y-19 · Dış veri paketinin tam kullanımı: olgusal katalog katmanı — **bitti (2026-08-15)**

**Sorun neydi.** P2.1 paketi 1.641 araç–motor–şanzıman kombinasyonu, 595 motor, 116
şanzıman ve 1.766 kaynak taşıyordu; depo bunun yalnızca fiyat katmanını (MK-19) ve altı
aday aracı kullanmıştı. Geri kalan veri kullanılmıyordu ve bu gerçek bir kayıptı: 1.617
vites sayısı, 1.607 teknik kaynak adresi, 1.625 tork değeri ve bizde hiç bulunmayan 18
marka (Jaguar, Land Rover, Lexus, Porsche ve diğerleri) dışarıda duruyordu.

**Neden daha önce alınmamıştı ve neyin değiştiği.** MK-21 "dış katalog toplu olarak içe
aktarılmaz" demişti. Gerekçesi doğruydu ve bugün sayıyla da doğrulandı: bizde karşılığı
olmayan 1.101 varyantın **451'i `p2-inferred-prior`**, yani puanı araştırılmamış. Bunları
puanlı almak deponun kanıt zincirini bir gecede seyreltirdi. MK-21'in fazla geniş
davrandığı yer, içe aktarmayı **tek bir şey** sayması: bir güç değeri ölçümdür, bir
güvenilirlik puanı yargıdır. MK-22 sınırı yeniden çizdi: **olgu toplu alınır, yargı tek
tek kazanılır.**

**Yapılan.** `data/catalog/` katmanı kuruldu (marka başına bir dosya, 48 dosya, 1.641
kayıt) ve `scripts/import_catalog.py` ile üretiliyor. `scripts/enrich_from_catalog.py`
puanlanmış 182 araca olgusal alanları taşıdı: vites sayısı (152), kavrama tipi (63),
üretici motor kodu (12), eksik tork (5). `build_pages.py` katalog kayıtları için de sayfa
üretiyor: **435 → 1.780 statik sayfa.**

**İki gerçek kusur bulundu ve düzeltildi.**

- **Eşleştirme modeli hiç karşılaştırmıyordu.** İlk sürüm marka+beygir+hacim üçlüsüne
  bakıyordu ve farklı modelleri bağlıyordu: bir Opel Vectra kaydı Astra satırına, bir Seat
  Arona kaydı Ibiza ve Leon satırlarına eşleşti. Ayrıca yıl ve şanzıman tipi kontrolleri
  yalnızca bir kayda birden çok araç düştüğünde çalışıyordu; oysa pratikte tersi oluyor ve
  bir CR-V III kaydı 2002-2006 nesline de bağlanmıştı. Model adı, yıl örtüşmesi ve
  şanzıman tipi artık her bağ için zorunlu. Bağ sayısı 451'den 281'e indi — azalma kayıp
  değil, yanlış bağın temizlenmesi.
- **`engine_code` alanının çoğu sahteydi.** P2.1'de dolu 171 değerin 162'si aslında
  deponun kendi `engine_id` değeriydi (ör. `engine_code = "bmw-m54"`). Yazılsalardı
  `engine_id` başka bir ada kopyalanmış olurdu. Süzüldü; geriye 12 gerçek üretici kodu
  kaldı (M54B25, N43B20, CJBA, 1ZR-FAE gibi).

**Kalite gizlenmedi.** 836 katalog kaydı `quality_flags` taşıyor (798'i
`generic_transmission_identity`). Bunlar katalog sayfasında da görünüyor, çünkü bir kayıt
puanlanmış katmana terfi ederken önce bu eksiklerin çözülmesi gerekiyor.

**Kaynak hakları gözetildi.** P2.1 sicilinin yeniden dağıtım politikası "kısa olgusal alan
ve kaynak URL'si; uzun metin, tablo veya görsel kopyası yok" diyor; ilan kaynakları için
"toplu ham ilan kopyası yok". Katalog tam olarak bu iznin içinde kalıyor ve 2.071 ham ilan
gözlemi depoya hiç girmiyor.

**Sonuç.** `validate.py` 0 hata (katalog için üç yeni koruma eklendi ve bozuk veriyle test
edildi: katalogda puan alanı, kırık bağ, kimlik çakışması), `smoke_test.js` 57/57 → 64/64.

**Arayüz bağlantısı (aynı gün tamamlandı).** Katalog araçları artık liste ekranında da
bulunuyor: arama kutusuna yazıldığında tablonun altında "Katalogda var, henüz
puanlanmadı" bloğu açılıyor ve her kart kendi statik sayfasına bağlanıyor. Blok
**tablonun içine karıştırılmadı**, çünkü katalog araçlarının puanı yok; null puanlı
satırlar sıralamayı, ağırlıklandırmayı ve "zayıf halka" işaretlemesini bozardı, üstelik
kullanıcı puanlanmış bir araçla puanlanmamış birini yan yana görüp ikisinin aynı
titizlikten geçtiğini sanırdı. Blok yalnız arama yapıldığında görünüyor: 1.345 kaydı her
açılışta listelemek asıl ürünü görsel olarak boğardı. Arayüze taşınan alanlar bilinçli
olarak az (kimlik, ad, marka, yıl, beygir, hacim, yakıt, şanzıman tipi, gövde);
`index.html` 1,20 MB'tan 1,42 MB'a çıktı (+%17,5). Tam kayıt zaten statik sayfada var.

**Bir veri hatası daha bulundu: ad ile yakıt türü çelişkisi.** Arayüz ilk kez ekranda
görüldüğünde "Volvo S60 2.3 T5 · Dizel" ve "Volvo S60 1.5 T3 · Dizel" satırları göze
çarptı; Volvo'nun rozet düzeninde T2-T8 benzin, D2-D5 dizeldir. Tarama yapıldığında
1.641 kaydın **25'inde** aynı türden çelişki bulundu: "Opel Astra 1.6 CDTI" ve "Renault
Megane 1.9 DTi" benzin olarak, "Volvo V60 1.6 T4" ve "Volvo V70 2.4 D5" ters yönde
kayıtlı. Bunlar tanımsal rozetler; ikisinden biri kesinlikle yanlış. **Çelişki
düzeltilmedi, işaretlendi** (`fuel_name_conflict`): hangi alanın yanlış olduğunu
söylemek teknik özellik sayfasına bakmayı gerektiriyor ve o siteler bu ortamda ağ
geçidince engelli. MK-18'in dersi burada bağlayıcı — çapraz doğrulamada bulunan her
çelişki taraf tutulmadan önce elle doğrulanır. İşaret katalog sayfasında Türkçe
açıklamasıyla görünüyor ve kaydı terfiye kapatıyor.

### 25 yakıt çelişkisi ve 5 fizik-dışı kayıt düzeltildi, beygir-tork denetimi kalıcılaştı (2026-08-17)

**Yakıt çelişkisi "işaretlenmedi, düzeltildi.**" Ölçüldüğünde çelişkili 25 kaydın
hepsinde `fuel`, `displacement_cc`, `torque_nm` ve `engine_name` alanları birbiriyle
uyumluydu; ayrışan tek alan **etiketin kendisiydi** ("Opel Astra 1.9 CDTI · 115 bg" →
1796cc, "1.8i 16V", 170 Nm → aslında atmosferik benzin). Bozuk etiket atılıp doğrulanmış
alanlardan yeniden kuruldu; atılan etiket `provenance.rejected_label`'da saklı.

**Kalıcı bir fizik denetimi eklendi.** 1.875 ölçülebilir kayıt (katalog + araç)
tarandığında hp/Nm oranının benzinde 0,54-0,89, dizelde 0,38-0,52 bandında kaldığı ve iki
bandın neredeyse hiç örtüşmediği görüldü. Bu oran `validate.py`'ye kalıcı bir kural
olarak eklendi ve **iki gerçek hatayı yakaladı, ikisi de puanlanmış araçlardaydı**:
Peugeot 301 1.6 HDi'nin teknik değerleri yanlışlıkla benzinli PureTech varyantından
alınmıştı (92 bg/230 Nm olarak düzeltildi), Suzuki SX4 1.6'nın torku 320 Nm yazılmıştı
(156 Nm olarak düzeltildi). Katalogda aynı denetim 5 kaydı daha yakaladı, hepsi
`WebSearch` ile doğrulanıp `scripts/import_catalog.py` içinde tek tek düzeltildi.

### 79 katalog kaydı puanlanmış katmana terfi etti — 278 → 357 araç (2026-08-17)

**`scripts/promote_catalog.py` yazıldı.** Zaten depoda var olan motor/şanzıman
ailelerine güvenle bağlanabilen katalog kayıtlarını `data/cars/`'a terfi ettiriyor.
`motor`/`trans` puanı MK-16 mekanik miras deseniyle aile `base_score`'undan geliyor;
`comf`/`cost`/`liq`/`fun` depoda hiçbir zaman kanıt zinciriyle verilmediği için ("elle
veriliyor") en yakın kardeş aracın değerinden tahmin ediliyor ve bu, her aracın `note`
alanında **açıkça gerekçesiz olarak işaretleniyor** — düzeltilmesi gereken ilk şey diye.

**Eşleştirme üç turda sıkılaştırıldı, her turda gerçek bir hata bulundu.** İlk deneme
yalnız (marka, yakıt, hacim) kullandı ve BMW M54'ün hiç üretmediği 306 bg'lik bir
"535i"ye, ZF 8HP'yi PSA/Aisin EAT8'e bağladı — motor eşleşmesine güç aralığı doğrulaması
(ailenin bilinen aralığının %75-135'i), şanzıman eşleşmesine marka zorunluluğu eklendi.
Sonra kaynak veride birebir yinelenen satırlar bulundu (aynı araç farklı model-yılı
gözlemi olarak ayrı satıra yazılmış, "Honda Accord 2.4 · 200 bg" üç kopya üretiyordu) —
aynı ad+güç+tork+aile grubu tek araca birleştirildi. Son olarak iki aday, depoda ÖNCEDEN
VAR olan araçlarla (`bmw-e36-325i`, `honda-accord-2-0-cu2`) aynı ada sahipti — id
çakışması yoktu ama isim çakışması vardı; mevcut adlara karşı da kontrol eklendi.

**Sonuç.** 82 aday → 79 terfi (3'ü mevcut isimle çakıştığı için atlandı). Araç sayısı
278 → 357, doğrulanmış araç 345. `validate.py` 0 hata, `smoke_test.js` 68/68 (araç sayısı
sabitleri güncellendi).

### İkinci ve üçüncü tur: paylaşımlı aileler ve motor kodu ayrımı (357 -> 379)

**Marka sınırı, kanıtlanmış paylaşıma göre gevşetildi.** VAG grubu (VW/Audi/Skoda/
Seat/Cupra) aynı DQ200/EA211/EA888/multitronic'i, PSA grubu (Peugeot/Citroën/Opel) aynı
EAT8/AL4/ETG'yi paylaşıyor — bu spekülasyon değil, deponun kendi verisinde zaten kanıtlı.
Bir aile 2+ markada görülüyorsa marka sınırı o aile için kaldırıldı.

**Kendi hatam, commit edilmeden yakalandı.** İlk sürüm bunu güvensiz uyguladı: marka
kontrolünü tamamen kaldırıp yalnız (yakıt, hacim) eşleştirdi ve "Honda Accord 2.0"u
Audi'nin EA888 motoruna, "BMW 528i"yi VW'nin EA211'ine bağladı. Düzeltme: aday markası,
o ailenin depodaki BİLİNEN marka kümesinde olmalı — genel bir varsayım değil, yalnız
zaten kanıtlı paylaşımı kullanan bir kısıtlama.

Bir aday da elle çıkarıldı: "Fiat Bravo 1.6 MultiJet Dualogic", Fiat Egea'nın psa-etg'ye
bağlı olması yüzünden markanın bilinen kümesine düştü, ama Bravo farklı bir nesil/
platform ve bu genelleme araştırılmadan yapılamaz.

**Üçüncü turda motor kodu öneki denendi**, üreticinin kendi kodunun (ör. "K24Z3",
"M54B25") aynı kovaya düşen birden çok aileyi (BMW 2.0 benzin gibi) ayırmak için
kullanılması. Getirisi düşük çıktı — çoğu belirsiz kovada `engine_code` alanı ya boş ya
da bulaşmış veriyle kirli. Bir kayıt açtı (VW Scirocco 1.4 TSI, "CAVD" kodu EA211'in
bilinen "CAV" önekiyle eşleşti).

**Sonuç.** 357 → 378 → 379 araç. `validate.py` 0 hata, `smoke_test.js` 68/68.
`smoke_test.js` artık araç sayısını `data/cars/`'dan okuyor, sabit sayı taşımıyor.

**Kalan iş.** 1.202 katalog kaydı hâlâ yalnız katalogda. Kaldıraç belirgin biçimde
azaldı: kalan büyük gruplar (BMW 2.0 benzin, Mercedes 3.0 dizel, Honda 2.0 benzin) ya
gerçekten birden çok aileye bölünüyor ya da kaynak veri kirli (aynı ada birden çok motor
adı bulaşmış — MK-18 türü bir sorun, tek tek araştırma gerektiriyor). Bundan sonrası
Y-02'nin "en yüksek kaldıraçlı aileden başla" yöntemiyle tek tek.

### comf/cost/liq: kardeş-araç kopyalaması yerine gerekçeli tahmin (2026-08-17)

**Sorun neydi.** Terfi eden 101 aracın `comf`/`cost`/`liq` puanı en yakın kardeş
aracın değerinden birebir kopyalanıyordu — aracın kendi segmentine, gövde tipine ya da
şanzıman tipine hiç bakmıyordu. Kullanıcı bunun düzeltilmesini istedi.

**Yapılan.** `scripts/estimate_judgment_scores.py` yazıldı. Depodaki 278 elle
değerlendirilmiş (terfi ETMEMİŞ) aracın marka başına ortalama comf/cost/liq'u çıkarılıyor
— bu, deponun kendi geçmiş kararlarından gelen bir çapa, yeni bir varsayım değil. Sonra
aracın kendi özellikleri bu ortalamadan **sapma** olarak ekleniyor: markanın kendi
ortalama beygirine göre üst/alt segment, gövde tipi (Station Wagon/SUV daha konforlu,
Coupe/Cabrio daha az likit), şanzıman tipi (kuru DCT ve robotlu yarı otomatik daha az
yumuşak/daha yüksek bakım riski). Her aracın `note` alanına gerçek gerekçe yazıldı: "X
markasının depodaki N aracının ortalaması Y çapa alındı, bu araç markanın ortalama
gücünün üstünde/altında, gövde tipi Z, şanzıman W" gibi.

**Kalıcı hale getirildi.** `promote_catalog.py` da bu yöntemi kullanacak şekilde
güncellendi; bundan sonraki terfi turları artık kardeş-araç kopyalaması değil bu
gerekçeli tahmini üretecek. Çapa yalnız hiç terfi etmemiş araçlardan hesaplanıyor ki
hata turdan tura birikmesin.

**Sonuç.** comf/cost/liq artık gerçek çeşitlilik taşıyor (önceden birkaç kopya kümesi,
şimdi 19-27 benzersiz değer). `validate.py` 0 hata, `smoke_test.js` 68/68. `fun` puanı bu
turun kapsamı dışında bırakıldı (kullanıcı özellikle comf/cost/liq istedi); hâlâ kardeş
araçtan geliyor ve `evidence.fun` yok — depodaki 115/278 aracın zaten içinde bulunduğu,
kabul edilmiş bir durum.

### fun: kardeş-araç kopyasından gerçek formüle (71/100 araç, sürüyor — 2026-08-17)

**Sorun neydi.** `fun` de tıpkı düzeltilmeden önceki comf/cost/liq gibi kardeş araçtan
kopyalanıyordu. Ama `fun`'ın zaten kanıta dayalı bir formülü vardı (`scripts/
compute_fun.py`, MK-06/MK-17): güç/ağırlık ve tork/ağırlık oranından hesaplıyor. Formül
yalnızca `specs.kerb_weight_kg` dolu olan araçlara çalışıyor ve terfi eden 101 aracın
hiçbirinde bu alan yoktu — katalogda boş ağırlık hiç bulunmuyordu. Yani buradaki eksik
başka bir tahmin katmanı eklemek değil, formülün zaten ihtiyaç duyduğu tek eksik veriyi
(gerçek boş ağırlık) bulmaktı.

**Yöntem: tahmin değil, araştırma.** Her araç için WebSearch ile gerçek boş ağırlık
(kerb weight) arandı — marka, model, motor hacmi, beygir ve yıl birlikte eşleştirilerek,
mümkün olduğunda otomatik şanzımanlı versiyonun rakamı tercih edilerek. Bulunan değer
600-3000 kg makul aralığına karşı denetlendi, sonra `scripts/compute_fun.py --write`
çalıştırıldı — puan elle verilmedi, formül gerçek girdiyle hesapladı.

**Araştırma sırasında gerçek bir eşleştirme hatası bulundu ve düzeltildi.** 7 Mercedes
dizel aracı, model yılında henüz üretilmeye başlanmamış OM651 motor ailesine (2008+)
`promote_catalog.py`'nin hp bazlı eşleştirmesiyle bağlanmıştı — ör. 2000 model bir "C200
CDI" 2008 sonrası motoru taşıyor görünüyordu. Bu, MK-08'in uyardığı "farklı nesiller
karıştırılmasın" riskinin tam örneği, hp eşleşmesi doğru olsa da yıl kontrolü eksikti.
6 kayıt gerçek dönem motoruna (OM611/OM646, ikisi de depoda zaten kanıtlı) yeniden
bağlandı, motor puanı ve kanıt metni o ailenin gerçek `base_score`'undan yeniden
hesaplandı. 1 kayıt (CLK 270 CDI · 150 bg) hiçbir gerçek CLK varyantıyla eşleşmiyordu
(gerçek CLK 270 CDI 2.7L 5 silindirli OM647 taşır, depoda bu ailenin kanıtı yok) —
terfisi geri alındı, katalog-only durumuna döndürüldü (`revert`, veri
`data/catalog/mercedes-benz.json`'da `scored_car_id: null` ve
`provenance.manually_corrected_fields` ile işaretli).

Ayrıca 6 kayıtta motor ailesi doğruydu ama P2.1 kaynağındaki rozet metni yanlıştı (aynı
"yakıt çelişkisi" türünden bir sorun, bu kez beygir-rozet uyuşmazlığı):
B180 CDI·136bg → gerçeği B200 CDI, B180 CDI·177bg → B220 CDI, E200 CDI·204bg → E320 CDI
(motoru OM613 3.2L, gerçekten 204bg üretiyor), E320 CDI·204bg(2013) → E250 CDI (OM651
2.1L 204bg, W212), C270 CDI·204bg → C250 CDI (aynı desen), Skoda Octavia "1.6 FSI"·130bg
→ 1.5 TSI (2019'da 1.6 FSI diye bir motor Skoda'nın kataloğunda yoktu). Her düzeltme
`name` alanında görünüyor ve `provenance.manually_corrected_fields`'da eski/yeni değer +
gerekçeyle kayıtlı.

**assessed_at'teki eskimişlik giderildi.** `compute_fun.py` daha önce her `--write`
çalıştırmasında `evidence.fun.assessed_at`'i sabit "2026-08-07" yazıyordu — bugün
çalıştırılınca bile. Artık tarih dinamik (`datetime.date.today()`) ama yalnızca gerçekten
yeni bir değerlendirme olduğunda ilerliyor (araçta daha önce `evidence.fun` yoktu ya da
hesaplanan puan değişti); aksi halde zaten var olan tarih korunuyor — aynı girdiyle
yeniden çalıştırmak, dokunulmamış araçların değerlendirme tarihini yanlışlıkla "bugün"
gibi göstermesin diye.

**Durum: 100 terfi edilmiş araçtan 71'i tamamlandı.** Kalan 29'u (Opel, Peugeot, Renault,
Seat, Toyota, VW, Volvo) için ağırlık araştırması sürüyor; formül yalnızca ağırlığı
bulunan araca yazıldı, kalanlar dokunulmadan (eski, gerekçesiz kardeş-kopya `fun`
puanıyla) bırakıldı — yarım kalan araştırma için sahte bir sayı üretmek yerine.

**Sonuç.** `validate.py` 0 hata, `smoke_test.js` 68/68, `build.py`/`build_pages.py`/
`build_content.py` yeniden üretildi. Araç sayısı 379 → 378 (bir terfi geri alındığı için).

---

## Y-03 · İki aşamalı kaynak araştırma hattı kur — **bitti**

**Sorun neydi.** Kaynak biriktirmek ile kaynağı puana çevirmek iki farklı iş ve farklı
yetenek istiyor. Birincisi geniş ama sığ bir tarama (çok sayıda aday kaynak bul),
ikincisi dar ama derin bir yargı (bu kaynak hangi iddiayı destekliyor, hangi banda
karşılık geliyor, güven seviyesi ne). İkisini aynı anda yapmak hem yavaş hem hatalı.

**Ne yapıldı.**

1. **Şema.** `data/schema/queue-candidate.schema.json` kuruldu: bir adayın araç
   kimliği, hangi kriteri ilgilendirdiği, arama sorgusu, bağlantı, yayıncı, iddia,
   varsa birebir alıntı ve durumu (`pending`/`accepted`/`rejected`) alanlarını
   tanımlıyor.
2. **Kuyruk.** `data/queue/` klasörü, `data/`'nın geri kalanından ayrı tutuluyor.
   `scripts/validate.py` bu klasörü hiç okumuyor ve `scripts/build.py` içeriğini
   sayfaya basmıyor; bu ayrımın gerekçesi `docs/ARCHITECTURE.md` MK-09 kaydında.
3. **İşleme.** Kabul edilen bir adayın kimliği değişmeden `data/sources.json`'a
   taşınıyor ve ilgili araç kaydının `sources` listesine ekleniyor; reddedilenler
   gerekçesiyle birlikte kuyrukta kalıyor ki aynı zayıf kaynak ikinci kez
   önerilmesin.
4. **Uçtan uca ilk tur.** 2026-08-06'da bu akış, o tarihte kaynaksız olan 14 araç için
   gerçek kaynak taramasıyla çalıştırıldı: `data/queue/candidates.json` içindeki 14
   kayıt bu turun dökümü, hepsi `accepted`. Ayrıntı Y-02'de ve `data/queue/README.md`
   içinde.

**Neden kuyruk ayrı tutuluyor.** Bu, `docs/ARCHITECTURE.md` MK-05'teki "kullanıcı kaynak
önerir, puanı bakımcı verir" kuralının otomatik araştırmaya uyarlanmış hali. Kural
değişmiyor: **kaynağı kim getirirse getirsin, puanı metodoloji verir.**

---

## Y-04 · Kaynak öneri formu — **kısmen bitti, e-posta adresi bekliyor**

**Amaç.** Kullanıcı bir araca kaynak önerebilsin, öneri bir e-posta adresine düşsün,
bakımcı inceleyip veriye işlesin. Öneri doğrudan veriye yazılmaz (MK-05).

### Bitti

`#katki` ekranı kuruldu ve üst menüde "Kaynak öner" olarak duruyor. Ekranda gerçek bir
form var; GitHub'a yönlendirme yapılmıyor, öneri site içinden alınıyor.

- Araç ve kriter listeleri **veriden dolduruluyor**, elle yazılmıyor; liste büyüdükçe
  form kendiliğinden güncel kalıyor. Aracı listede bulunmayan kullanıcı için ayrı bir
  seçenek var.
- Zorunlu alanlar: hangi araç, hangi kriter, kaynağın bağlantısı, kaynaktan birebir
  alıntı. Alıntının zorunlu olması bilinçli: bağlantı çürüdüğünde iddiayı ayakta tutan
  tek şey o.
- Robotlara karşı bal küpü (honeypot) alanı var; CAPTCHA yok, bu hacimde kullanıcıyı
  yormaya değmez.
- Uç nokta tanımlı olmadığı sürece gönderim **kapalı** ve kullanıcıya sebebi açıkça
  yazılıyor. Sessizce başarısız olan bir form, hiç olmayan bir formdan daha kötüdür.
- `smoke_test.js` üç yeni kontrol kazandı: araç listesi doluyor mu, kriter listesi
  doluyor mu, uç nokta yokken gönderim gerçekten kapalı mı.

### Kalan tek iş: e-posta adresi ve uç nokta

Bu adımlar depo sahibine ait ve hepsi ücretsizdir.

1. **E-posta adresini aç.** Örneğin `aracpuanlama.kaynak@gmail.com`. Bu adres hem formun
   hedefi hem sitedeki iletişim adresi olacak.
2. **FormSubmit'i etkinleştir** (`formsubmit.co`, kayıt gerektirmez, sınırsız, ücretsiz).
   Formdan ilk gönderim yapıldığında adrese bir onay postası gelir; o onaylanınca bütün
   gönderimler doğrudan gelen kutusuna düşer.
3. **Gizli uç noktayı al.** FormSubmit onay sonrası e-posta yerine kullanılabilecek
   karma (hashed) bir adres veriyor. Ham e-posta adresi HTML kaynağında görünürse spam
   robotları toplar; bu yüzden karma adres tercih edilmeli.
4. **Depoda tek satır değiştir.** `templates/app/47-katki.js` dosyasının başındaki
   `FORM_ENDPOINT` değişkenine bu adres yazılır, `python3 scripts/build.py` çalıştırılır.
   Form o anda açılır, uyarı kutusu kendiliğinden kaybolur. Başka hiçbir değişiklik
   gerekmez.
5. **Siteyi barındır.** Form gönderimi `file://` üzerinden çalışmaz. GitHub Pages
   ücretsizdir ve çıktı artık `index.html` olduğu için ayarlardan açmak yeterli.

### Ayrıca bitti (bu turda)

- Araç detay panelinde **"Bu araca kaynak öner"** düğmesi eklendi
  (`templates/app/60-tablo.js`). Tıklandığında `#katki` ekranına geçiliyor ve araç
  kutusu o araca önceden seçili geliyor (`suggestSourceFor`, `templates/app/47-katki.js`);
  kullanıcı listede zaten baktığı aracı formda ikinci kez aramak zorunda kalmıyor.
- **`#iletisim` ekranı** kuruldu (`templates/screens/49-iletisim.html`): e-posta
  adresi ve dört maddelik öneri kabul kriterleri. Adres, formun uç noktasıyla aynı
  mantıkla tek bir yerde tutuluyor: `templates/app/05-yapilandirma.js` içindeki
  `CONTACT_EMAIL`. Adres tanımlı değilken ekran sessizce boş kalmıyor, kaynak öner
  formunun bu süreye kadar tek yol olduğu açıkça yazıyor.
- `FORM_ENDPOINT` ve `CONTACT_EMAIL`, tek bir yapılandırma dosyasına
  (`templates/app/05-yapilandirma.js`) taşındı; adres tanımlandığında tek satır
  değiştirmek hem formu hem iletişim ekranını birden açıyor.
- `smoke_test.js` üç yeni kontrol kazandı: iletişim ekranı adres tanımlı değilken
  uyarısını gösteriyor mu, "bu araca kaynak öner" düğmesi forma götürüp aracı
  önceden seçiyor mu, iletişim ekranında yatay taşma var mı.

### Sonraya kalan

- Gelen önerileri Y-03'teki kuyruğa (`data/queue/`) taşıyan akış. Bu, Y-03 kurulmadan
  anlamlı biçimde yapılamaz.

---

## Y-05 · Kriter panelini tablonun hemen üstüne al, yatay yerleşim — **bitti**

**Sorun neydi.** Liste ekranında hazır ayar düğmeleri, ağırlık toplamı kutusu, arama
kutusu ve sekiz satırlık filtre grubu üst üste diziliyordu; tablo ekranın çok aşağısına
kayıyor ve kullanıcı asıl işi (tabloyu okumak) için her seferinde kaydırmak zorunda
kalıyordu.

**Ne yapıldı.** Hazır ayarlar, ağırlık toplamı kutusu, arama kutusu, filtre düğmesi ve
"kaç araç gösteriliyor" sayacı tablonun hemen üstünde tek bir denetim çubuğunda
(`.ctrlbar`) yatay olarak toplandı; sekiz filtre grubu ise katlanabilir bir panele
(`#filterpanel`) alındı. Ağırlık değişiminin tabloyu anında etkilemesi korundu, çünkü
hazır ayar düğmeleri eskisi gibi aynı `W` nesnesini düzenleyip `recalcAll` çağırıyor.

**Panelin varsayılanı sorulmuştu, cevap şu oldu:** panel **ilk ziyarette kapalı**
geliyor, ama kullanıcının açık/kapalı tercihi `localStorage` içinde
(`arac_puan_filtre_paneli`) saklanıyor ve sonraki ziyarette bıraktığı gibi açılıyor. İlk
ziyaretin kapalı olması bilinçli: siteye ilk gelen kullanıcının önce tabloyu görmesi
gerekiyor, filtreyi ancak listeyi gördükten sonra arıyor.

Panel kapalıyken hangi filtrelerin açık olduğunun görünmez kalması yeni bir sorun
yaratırdı; bunu önlemek için düğmenin üstüne seçili filtre sayısını gösteren bir rozet
ve yanına panel kapalıyken de erişilebilen bir "Filtreleri temizle" düğmesi kondu.

`smoke_test.js` dört yeni kontrol kazandı: panel ilk ziyarette kapalı mı, düğme paneli
açıyor mu, rozet seçili filtre sayısını doğru sayıyor mu, "temizle" bütün kategorileri
birden sıfırlıyor mu.

---

## Y-06 · Puanlama şeffaflığı — **bitti (üç katmanın tamamı)**

**Öncelik: yüksek.** Kullanıcının en net iki şikayeti buradan geliyor: "fiyat kısmı çok
kafa karıştırıcı, kriterin puanı nasıl etkilediğini bilmiyoruz" ve daha sonra
"kriterlerin bilimsel olarak belirlenmesi konusunu netleştirmemişiz, formüller falan
yazmıyor hiçbir yerde."

### Birinci katman — bilimsel temel (2026-08-06, bitti)

İkinci şikayet haklıydı ama tam olarak sanıldığı gibi değil. Denetim yapıldığında
görüldü ki toplama formülü `docs/methodology.md` §3'te zaten yazılıydı ve
`00-cekirdek.js`'te birebir uygulanıyordu; yedi kriterin hepsinin çapalı puan bantları
da `criteria.json` içinde tanımlıydı. **Gerçekten eksik olanlar başkaydı:**

- Sistemin hangi akademik yönteme dayandığı hiçbir yerde yazmıyordu (aslında bir MCDA /
  ağırlıklı toplam modeli).
- Varsayılan ağırlıkların (20/15/16/11/10/12/6/10) hiçbir gerekçesi yoktu.
- Modelin kendisi hiç ölçülmemişti: ağırlık değişince sıralama ne oluyor, hangi kriter
  sonucu belirliyor, kriterler birbirini tekrar ediyor mu — bilinmiyordu.
- `docs/ARCHITECTURE.md` MK-06 "fun/comf/age/cost formüle bağlanır, karar verildi"
  diyordu ama formülün girdileri **221/221 boştu**; karar hiç uygulanmamıştı.

Bu katmanda yapılanlar:

1. **`scripts/analysis/sensitivity.py`** yazıldı — modelin duyarlılık ve tutarlılık
   ölçümü. `validate.py` verinin kurallara uyup uymadığını sorar; bu betik modelin
   kendisinin sağlam olup olmadığını sorar. Sabit rastgelelik tohumu kullanıyor, yani
   sonuçlar tekrarlanabilir.
2. **`docs/PUANLAMA-TEMELI.md`** yazıldı — yöntemin akademik dayanağı (MAUT/WSM, BARS),
   alternatiflerin (AHP, TOPSIS, ELECTRE) neden reddedildiği, ölçüm sonuçları ve
   bilinen boşlukların dürüst dökümü.
3. **MK-06'ya durum uyarısı** eklendi: karar alındı ama uygulanmadı, açıkça yazıldı.

**Ölçümün bulduğu üç şey** (ayrıntısı `PUANLAMA-TEMELI.md` §3'te):

- **İyi haber:** Model ağırlık hatasına dayanıklı. ±%25 gürültüde Spearman 0.99, ilk
  10'un 9.33'ü korunuyor. Yani ağırlıkların gerekçesiz olması sanıldığı kadar ciddi bir
  sorun değil.
- **Sorun 1:** `comf` kriteri neredeyse hiç ayırt etmiyor — ağırlığı sıfırlanınca
  Spearman 0.986, puan yayılımı en dar (56–88, sd 6.0). Ya puanlama merkeze kaymış ya
  da kriter gerçekten gereksiz; ayrım için `evidence` bloğu gerekiyor.
- **Sorun 2:** `age` ile `price` arasında −0.80 korelasyon var. Yaş riski bir kez ceza
  (`age`), bir kez ödül (`price`) olarak iki kez sayılıyor. Ağırlıklı toplamın bilinen
  zayıflığı; belgelendi, gizlenmedi.

### Üçüncü katman — kanıt zinciri (2026-08-06, bitti)

`PUANLAMA-TEMELI.md` §6'nın en büyük açığı şuydu: `evidence` bloğu 221 araçtan
yalnızca 2'sinde doluydu. Yani "bu puan hangi kaynağın hangi bandına dayanıyor"
sorusu kriter bazında cevapsızdı; kaynak listesi araç seviyesinde vardı ama kriter
seviyesinde bağ yoktu.

Bu katmanda `evidence.motor` ve `evidence.trans` blokları 221 araçtan **220'sinde**
dolduruldu (`volvo-s40-v50-2-0` istisna kaldı, çünkü bağlı olduğu `volvo-b4204s`
motor ailesinin henüz `base_score`'u yok — `motor-temel-puani-yok` uyarısı bunu zaten
işaretliyor). Doldurma elle yazılmadı; zaten var olan üç bilgi mekanik biçimde
birleştirildi:

1. Aracın bağlı olduğu motor/şanzıman ailesinin kaynaklı `base_score`'u.
2. Aracın kendi fiili puanı ve bu puanın hangi BARS bandına düştüğü.
3. Aracın kendi kaynaklarının seviyesi (`confidence`: A varsa yüksek, B varsa orta,
   yalnızca C varsa düşük).

Bu üç bilgiden otomatik üretilen `reasoning` metni, aile adını, temel puanı, sapmayı
(varsa yönü ve büyüklüğü) ve ailenin bilinen ilk zaafını tam cümlelerle anlatıyor.
Hiçbir yeni iddia üretilmedi; var olan bağ yapılandırılmış hâle getirildi. Doğrulama
döngüsü (`build.py`, `validate.py`, `smoke_test.js`) 0 hata ve 37/37 kontrolle
tamamlandı.

Aynı oturumda `PUANLAMA-TEMELI.md` §5'teki ağırlık türetme işi de (SWING protokolü)
tamamlandı: üç kullanıcı profili (aile, meraklı, özel) için kriter kriter swing puanı
verildi, normalize edildi ve `data/criteria.json`'daki üç hazır ağırlık seti bu
sayılarla güncellendi. Eski ile yeni ağırlıklar arasındaki Spearman korelasyonu
0.967–0.983 çıktı — sıralama devrilmiyor ama anlamlı ölçüde düzeltiliyor. Süreçte
eski "Güvenilirlik öncelikli" (aile) setinin `comf` ağırlığının `motor` kadar yüksek
olduğu, muhtemelen yeniden adlandırılmamış bir "aile/konfor" mirası olduğu da ortaya
çıktı; yeni sette düzeltildi.

### İkinci katman — arayüz (2026-08-07, bitti)

**Önceki durum ve neden kafa karıştırıcı olduğu.** Fiyat, diğer yedi kriterden yapısal
olarak farklı çalışıyor ama arayüzde aynı görünüyordu:

- Diğer kriterlerin puanı araç kaydında sabit durur ve kanıta dayanır.
- Fiyat puanı **hiçbir yerde saklanmaz**; listenin tamamına göre her yeniden çizimde
  hesaplanır: `100 × (en_pahalı_orta − aracın_ortası) / (en_pahalı_orta − en_ucuz_orta)`.
- Yani bir aracın fiyat puanı, **listedeki diğer araçlar değiştiğinde değişir**. Filtre
  uygulandığında ya da fiyat aralığı elle düzenlendiğinde bu puan kayar.

Bu davranış doğruydu ama görünmezdi, ve görünmediği için kafa karıştırıyordu. Dört
maddenin tamamı yapıldı:

1. **`#kriterler` ekranı kriter kriter genişletildi.** Her kartta artık tanımın
   (ne ölçüyor/ölçmüyor) yanında `data/criteria.json`'a yeni eklenen
   `weight_rationale` alanından gelen bir gerekçe metni ("bu ağırlık neden bu") ve
   bantlı yedi kriterin hepsinde `<details>` ile açılıp kapanan bir "puan bantlarını
   göster" paneli var — beş bandın aralığı, adı, test cümlesi ve varsa listedeki
   gerçek örnek aracı. Bant örnekleri `data/criteria.json` içinde araç kimliğiyle
   tutuluyor; `build.py` bunları derleme sırasında araç adına çeviriyor, JS tarafı
   id→ad eşlemesi taşımak zorunda kalmıyor. `validate.py`'ye bu örneklerin gerçek bir
   araca karşılık geldiğini doğrulayan yeni bir kural eklendi
   (`gecersiz-bant-ornegi`), aksi hâlde ileride bir araç kimliği değişirse arayüz
   sessizce kırılabilirdi.
2. **Fiyat kriterine ayrı bir bölüm.** `#metodoloji` ekranına yedinci kart eklendi:
   fiyat puanının neden hiçbir dosyada saklanmadığı, filtre uygulandığında neden
   anında değiştiği ve tablodaki fiyat kutucuklarını elle düzenlemenin listenin
   tamamının fiyat puanını nasıl yeniden hesaplattığı somut bir örnekle anlatılıyor.
3. **Canlı katkı göstergesi.** Her ağırlık kutusunun altında o kriterin toplam
   puandaki **fiili katkı payını** gösteren bir yüzde var. Bu, ham ağırlık yüzdesi
   değil; ağırlık × kriterin listedeki ortalama puanı üzerinden hesaplanıyor, çünkü
   ağırlığı yüksek ama listede herkesin birbirine yakın puan aldığı bir kriter fiilen
   daha az ayırt edici olabilir. Ağırlık değiştikçe, hazır ayar seçildikçe veya bir
   aracın fiyatı elle düzenlendikçe (listenin ortalama fiyat puanı kaydığı için)
   anında güncelleniyor.
4. **Araç detay panelinde "bu araç neden bu puanı aldı" dökümü.** Liste ekranında bir
   satır açıldığında artık sekiz kriterin tamamı için puan/ağırlık/katkı satırlarını
   ve toplam satırını gösteren bir tablo var; buradaki katkı sayıları `total()`
   fonksiyonunun fiilen topladığı terimlerin ta kendisi, ayrı bir tahmin değil. Motor
   ve şanzıman için `evidence` bloğu doluysa (üçüncü katmanın ürettiği 220/221 araç)
   hangi bandın hangi gerekçeyle verildiği de aynı panelde metin olarak görünüyor;
   diğer beş kriterde evidence henüz boş olduğu için yalnızca puan satırı var.

`smoke_test.js` yedi yeni kontrol kazandı: ağırlık gerekçesi sekiz kartta da var mı,
bant paneli yedi kriterde var mı, panel açılınca beş satır görünüyor mu, canlı katkı
göstergesi sekiz kartta da doluyor mu, metodoloji ekranında yedi kart var mı, araç
detayında dökümün dokuz satırı (sekiz kriter + toplam) ve en az bir kanıt metni var
mı. Toplam kontrol sayısı 37'den **44**'e çıktı, hepsi geçiyor.

**Bitmiş sayılma ölçütü — karşılandı.** Bir kullanıcı artık bir aracın toplam
puanının hangi sayılardan oluştuğunu arayüzden takip edebiliyor, fiyat puanının neden
değiştiğini açıklayabiliyor ve her ağırlığın neden o değerde olduğunu okuyabiliyor.

**Düzeltme (2026-08-07, aynı gün) — kullanıcı geri bildirimiyle iki değişiklik.**
Yukarıdaki madde 1 ve 3 kullanıma girer girmez iki sorun bildirildi:

1. **Kriter paneli yanlış yerdeydi.** Ayrıntılı kriter kartları (`#rubric`) ayrı bir
   `#kriterler` ekranındaydı; kullanıcı ağırlığı değiştirmek için sekme değiştirmek
   zorunda kalmak istemedi ve "araç listesinin olduğu yere gönder" dedi. `#kriterler`
   ekranı tamamen kaldırıldı; kartlar liste ekranına, filtre paneliyle birebir aynı
   katlanabilir desende yeni bir "Kriterleri düzenle" panelinde taşındı
   (`#kritpanel`, `templates/screens/30-liste.html`). Nav menüsünden "Kriterler"
   sekmesi kalktı; ana ekran ve metodoloji ekranındaki `#kriterler` bağlantıları
   `#liste`'ye güncellendi.
2. **"Fiili katkı" göstergesi anlaşılmıyordu.** Kullanıcının tepkisi birebir şuydu:
   "fiili katkı ne amk lan? benim belirlediğim kriterler kadar etkilesin." Gösterge
   ağırlık × listenin ortalama puanını çarpan bir sayı gösteriyordu; kullanıcının
   yazdığı sayıdan görünür biçimde farklı çıkıyor ve neden farklı olduğu hiçbir yerde
   açıklanmıyordu. Hesap basitleştirildi: artık yalnızca kullanıcının kendi girdiği
   ağırlığın, ağırlık toplamı içindeki payını gösteriyor (`ağırlık / toplam × 100`) —
   başka hiçbir sayıyla karışmadan, doğrudan girilen değere orantılı. Metin de tam
   cümleye çevrildi ("Bu kriter, girdiğiniz ağırlıkların toplamının %X'ini
   taşıyor."), çünkü kısaltılmış "fiili katkı ≈ %X" ifadesi CLAUDE.md §1'in "tam
   cümle" kuralını ihlal ediyordu.

`scripts/smoke_test.js` buna göre güncellendi (kriterler ekranına gitmek yerine yeni
`#kritpanel`'i açıyor); toplam kontrol sayısı 44'ten **46**'ya çıktı.

---

## Y-07 · Ana giriş ekranı (onboarding sonrası) — **bitti**

**Sorun neydi.** Giriş akışı bittikten sonra kullanıcı doğrudan 154 satırlık tabloya
düşüyordu. Tablo güçlü ama karşılama ekranı değil; nereden başlayacağını söylemiyordu.

**Ne yapıldı.** `#liste` ile `#giris` arasına bir ana ekran (`#ana`,
`templates/screens/25-ana.html`) girdi ve varsayılan rota o oldu
(`templates/app/10-yonlendirici.js` içindeki `DEFAULT_ROUTE`). Giriş akışındaki
"Geç" ve "Araç listesine geç" düğmeleri de artık doğrudan tabloya değil ana ekrana
götürüyor (`templates/app/15-giris.js`); ikisinin aynı hedefi göstermesi bilinçli,
aksi hâlde giriş akışı kendi varsayılanından kopardı.

İçeriğin tamamı veriden hesaplanıyor, elle yazılmıyor (`templates/app/22-ana.js`,
`renderAna`), ve ekrana her dönüşte yeniden hesaplanıyor ki kriterler ekranında
ağırlık değiştirilip geri dönüldüğünde eski bir sonuç görünmesin:

- **Veri kapsamı özeti:** kaç araç, kaç motor ailesi, kaç şanzıman kutusu, kaç kaynak,
  araç başına ortalama kaynak. Motor ailesi ve şanzıman kutusu sayıları yeni:
  `scripts/build.py` artık `data/engines.json` ve `data/transmissions.json`'ı da
  okuyup üretilen veri tabanına (`DB`) gömüyor; önceden yalnızca `#metodoloji`
  ekranındaki beş göstergeye sahiptik, ana ekran bu ikisini ekleyerek yediye çıkardı.
- **Hazır giriş yolları:** "güvenilirlik öncelikli ilk on" ilgili ağırlık setini
  uygulayıp listeyi toplam puana göre azalan sıralar; "bütçeye göre başla" ağırlıkları
  değiştirmeden listeyi en ucuzdan başlatır; "sürüş keyfi öncelikli ilk on" ilgili
  ağırlık setini uygular. Üçü de listeye götürür.
- **Öne çıkan bulgular:** en yüksek puanlı beş araç (şu anki ağırlığa göre) ve — daha
  önemlisi — **en riskli beş motor ailesi ile en riskli beş şanzıman kutusu.**
  Kullanıcının asıl aradığı bilgi "hangi motor/şanzıman beni yakar" sorusunun cevabı;
  bu liste araç kaydından değil, temel puanı en düşük motor ve kutu kayıtlarından
  doğrudan üretiliyor (`scripts/build.py` içindeki `riskiest()`). Henüz temel puanı
  atanmamış bileşenler bu listeye girmiyor; boş bir alanı "en riskli" diye göstermek
  yanlış olurdu.

`smoke_test.js` dokuz yeni kontrol kazandı: onboarding sonrası ana ekrana gidiliyor
mu, beş istatistik kutusu doluyor mu, üç hazır giriş yolu doluyor mu, en yüksek
puanlı beş satır doluyor mu, riskli motor/şanzıman listeleri beşer satır doluyor mu,
ana ekranda yatay taşma var mı, hazır giriş yolu listeye götürüyor mu, ikinci
ziyarette hash olmadan doğrudan ana ekrana düşülüyor mu.

---

## Y-08 · Araç hikayeleri

**Öncelik: düşük-orta. Ürünü sevilir kılan kısım burası.**

**Amaç.** Her araç için kısa bir firma ve tasarım hikayesi, bir iki niş bilgi. Referans
ton: Gran Turismo'nun araç açıklamaları — kısa, bilgili, övmeyen, meraklıya hitap eden.

**Kapsam.**

1. `data/schema/car.schema.json` içine isteğe bağlı bir `story` alanı eklenir. Şema
   kuralı gereği önce isteğe bağlı girer, veri dolar, sonra gerekirse zorunlu olur.
2. Alan **puanı etkilemez.** Bu ayrım korunmalı: hikaye anlatı, puan kanıt. Karışırsa
   metodoloji zedelenir.
3. Araç detay panelinde ayrı ve görsel olarak ayrışan bir bölümde gösterilir.
4. Hikayeler de kaynağa bağlanabilmeli; uydurma bir tarih veya rakam, projenin bütün
   güvenilirlik iddiasına zarar verir.

**Bitmiş sayılma ölçütü.** En az 40 aracın hikayesi yazılmış ve arayüzde görünüyor.

---

## Y-09 · Görsel dil: koyu tema ve yumuşak yüzeyler

**Öncelik: düşük-orta. Y-05 ve Y-07 ile birlikte yapılırsa verimli olur.**

**Kapsam.** Sert ve büyük kenarlar yumuşatılır, koyu bir tema kurulur, otomobil
kültürüne yakın ama ciddiyetini koruyan bir görsel dil oturtulur.

**Kesin sınırlar (kullanıcının açık talebi):** Süslü veya "eğlenceli" yazı tipi
kullanılmaz. Dekoratif görsel kullanılmaz. **Emoji kullanılmaz.** Mevcut yazı tipi
üçlüsü (Archivo, IBM Plex Mono, Newsreader) zaten teknik ve ciddi bir ton veriyor;
değiştirilmesi için güçlü bir gerekçe gerekir.

**Öneri.** Koyu tema, mevcut açık temanın yerine geçmek yerine onun yanına kurulmalı ve
kullanıcı seçebilmeli. `templates/styles.css` zaten CSS değişkenleriyle yazıldığı için
bu, renk değişkenlerinin ikinci bir kümesini tanımlamak kadar basit; yapıyı değiştirmek
gerekmiyor.

---

## Sıralama önerisi

**Veri tarafı büyük ölçüde tamamlandı; sıradaki iş arayüz ve içerik.**

Biten maddeler: ~~Y-01~~ (liste genişletme — SUV, marka ve 2016+ hedeflerinin üçü de
karşılandı/aşıldı), ~~Y-02~~ (kaynak derinliği — kaynaksız ve tek kaynaklı araç
kalmadı), ~~Y-03~~ (araştırma hattı), ~~Y-04~~ (form arayüzü; yalnızca uç nokta adresi
depo sahibini bekliyor), ~~Y-05~~ (yerleşim), ~~Y-06~~ (puanlama şeffaflığı, üç
katmanın tamamı), ~~Y-07~~ (ana ekran).

Sıradaki iş, öncelik sırasıyla:

1. **Y-09 · Koyu tema** — bağımsız, görsel, riski düşük.
2. **Y-08 · Araç hikayeleri** — sürekli ve parça parça ilerleyebilecek, aceleye gelmeyen
   iş; 228 araç için yazılacak çok içerik var.
3. **Y-01'in ötesi (düşük öncelik)** — MG'nin geleneksel yakıtlı modelleri (varsa),
   Dacia Sandero/Logan gibi robotlu (AMT) şanzımanlı modeller (ayrı bir "Robot" tipi
   bileşen ailesi araştırması gerektiriyor, bu turda ertelendi). Elektrikli/hibrit/LPG
   kalıcı olarak kapsam dışı (MK-13).
4. **Y-02'nin uzun vadeli hedefi** — ortalamayı 4'e çıkarmak, yani her araca üçüncü ve
   dördüncü bağımsız kaynak. Bileşen bazlı toplu bağlama yöntemi burada işe yaramıyor;
   araç bazında tekil araştırma gerekiyor, bu yüzden yavaş ve pahalı bir iş.
5. **`evidence` bloğunu kalan üç kriter için genişletmek** (`comf`, `cost`, `liq`) —
   `age` (MK-14), `fun` (MK-17) ve `price` (MK-19) artık betiklerden geliyor. `comf`/`cost`
   hâlâ MK-06'nın uygulanmamış kalan formüllerine bağlı (iç hacim/bagaj hacmi, resmi bakım
   tarifesi); `liq` sayım protokolü MK-20'de reddedildi ve doğru biçimiyle yeniden kurulmayı
   bekliyor.

---

## Faz 4 · Ürünleşme ve görünürlük (Y-11 … Y-18)

Buraya kadarki maddeler ürünün **doğru** olmasıyla ilgiliydi. Aşağıdaki maddeler ürünün
**bulunabilir ve sürdürülebilir** olmasıyla ilgili. Ticari gerekçeleri, gelir modelleri ve
pazarlama tarafı ayrı bir belgede duruyor: `docs/URUN-STRATEJISI.md`. Burada yalnızca
mühendislik kapsamı ve bitmiş sayılma ölçütü var.

Sıralamanın mantığı şu: en ucuz kaldıraç önce. Y-11 ve Y-13 bugünkü veriyle yapılabiliyor,
biri trafiği diğeri topluluk katkısını açıyor; ödeme altyapısı (Y-17) bilinçli olarak sona
bırakıldı, çünkü trafik olmadan kurulan bir ödeme akışı boş bir dükkândır.

### Y-11 · Statik sayfa üretimi ve SEO temeli — **bitti (2026-08-13)**

**Sorun.** Depoda 83 bin kelimelik özgün, kaynaklı Türkçe analiz var ve bu içeriğin
tamamı arama motorlarına **görünmez**. Çıktı tek bir 1,2 MB'lık `index.html` ve ekranlar
arası geçiş `#liste` gibi çapa adlarıyla yapılıyor; Google'ın gördüğü sayfa sayısı bir.
`meta description`, `sitemap.xml`, `robots.txt`, `canonical` ve paylaşım önizleme etiketleri
hiç yok, sayfa başlığı da hiçbir arama sorgusuyla eşleşmeyen "Araç Puanlama".

**Kapsam.** `scripts/build.py`'ye ikinci bir çıktı biçimi eklenir: araç başına
`/arac/<id>.html`, motor ailesi başına `/motor/<id>.html`, şanzıman başına
`/sanziman/<id>.html`. Bugünkü veriyle **435 indekslenebilir sayfa** demek. Her sayfaya
araca özgü `title`, `meta description`, `canonical` ve Open Graph etiketleri; `sitemap.xml`
ve `robots.txt` üretimi; `Vehicle` ve `FAQPage` JSON-LD bloğu (`evidence.reasoning`
metinleri zaten soru-cevap biçiminde hazır).

**MK-01 bozulmuyor:** üretilen sayfalar türetilmiş çıktıdır, `data/` tek doğruluk kaynağı
olarak kalır. MK-02 bu genişlemeyi zaten öngörüyordu ("derleme adımında yeni bir çıktı
biçimi üretmek").

**Bitmiş sayılma ölçütü — karşılandı.** `scripts/build_pages.py` yazıldı ve **435 statik
sayfa** üretiyor (278 araç + 104 motor + 53 şanzıman); `sitemap.xml` 436 adres taşıyor,
`robots.txt` sitemap'i işaret ediyor. Her sayfa araca özgü başlık (ör. "VW Passat B7 1.6 TDI
alınır mı? Kronik sorunları, puanı ve fiyatı"), 150 karakterlik özgün açıklama, canonical
adres, Open Graph etiketleri ve `Vehicle` JSON-LD bloğu taşıyor. Duman testine yedi yeni
kontrol eklendi (49 → 57) ve `--check` kipi derlenmiş sayfaların veriyle uyumunu denetliyor.

**Uygulamada verilen kararlar.** Betik `build.py`'nin içine değil **ayrı bir dosyaya**
yazıldı: çalışan `index.html` üretimi hiç riske atılmasın diye (CLAUDE.md §2). Sayfalar
arama motoru için üretilmiş içi boş kapı sayfaları değil — depodaki gerçek `evidence`
gerekçelerini, bileşen ailelerinin `known_issues` kayıtlarını ve kaynak listesini taşıyorlar,
yani zaten yazılmış olan analizin görünür hali. Tarihsiz fiyat bandı taşıyan araçlarda sayfa
bunu açıkça yazıyor ("tarihlendirilmemiş bir tahmindir"), tarihli olanlarda ise ölçüm tarihi,
örneklem ve "istenen fiyat, satış fiyatı değildir" uyarısı görünüyor. Ana `index.html` de
başlık, açıklama, canonical ve Open Graph etiketleriyle donatıldı.

**Kalan iş.** Sayfalar üretiliyor ama henüz Google Search Console'a gönderilmedi; bu, depo
sahibinin hesabıyla yapılacak bir adım. `BASE_URL` sabiti GitHub Pages varsayılanına
ayarlı — özel alan adı bağlanırsa yalnızca o sabit değişmeli.

### Y-12 · İçerik üretim betiği (`build_content.py`) — **bitti (2026-08-14)**

**Sorun neydi.** `data/engines.json` ve `data/transmissions.json` içinde (Y-02'nin
onbeşinci turu sonunda) **305 yapılandırılmış bilinen arıza kaydı** birikmişti; her biri
hangi bileşen, hangi arıza, hangi kilometrede, ne sıklıkta, hangi kaynakla bildirildiğini
taşıyor. Bu, bir yıldan fazla araştırmanın ham maddesiydi ama yalnızca sayfa içinde küçük
bir metin olarak görünüyordu.

**Yapılan.** `scripts/build_content.py` yazıldı. `data/`'dan hiçbir yeni olgu üretmiyor,
yalnızca zaten var olan `known_issues` kayıtlarını dört içerik biçimine döküyor: kısa
video senaryosu (30-40 sn, sahne sahne), kaydırmalı görsel metni (5 slayt), paylaşım
dizisi (X/Twitter thread, 5 gönderi) ve uzun biçim yazı taslağı. Her taslak, dayandığı
kaynağın yayıncı adını ve adresini taşıyor — kaynaksız bir taslak üretilmiyor. Çıktı
`icerik/motor/<aile-id>.md` ve `icerik/sanziman/<aile-id>.md` altında, bir de her şeyi
listeleyen `icerik/INDEX.md` var. `--check` kipi CI'ye eklendi (`build_pages.py --check`
ile aynı desen): `known_issues` güncellenip taslak yeniden üretilmezse denetim kırmızı
yanar, eski/yanlış bir taslak sessizce kalmaz.

**Bitmiş sayılma ölçütü — aşıldı.** Hedef "en az 20 taslak" idi; **305 arıza kaydının
hepsi için** taslak üretiliyor (157 dosyada, 104 motor ailesi + 53 şanzıman kutusu).
Betik metin üretiyor, yayın yapmıyor — hangi taslağın kullanılacağına, nasıl
düzenleneceğine ve ne zaman paylaşılacağına insan karar veriyor; bu bilinçli bir sınır.

### Y-13 · GitHub katkı kapısı ve sürekli denetim — **büyük ölçüde bitti (2026-08-13)**

**Düzeltme kaydı.** Bu maddenin ilk yazımında "MK-05'in birinci katmanı hâlâ kurulmadı"
ve "GitHub Actions denetimi yok" deniyordu. **İkisi de yanlıştı.** Kaynak öneri şablonu
(`.github/ISSUE_TEMPLATE/kaynak-onerisi.yml`) `b8e6caf` commit'inde zaten kurulmuştu ve
`validate.py` + `build.py --check` + `smoke_test.js` çalıştıran CI iş akışı
(`.github/workflows/ci.yml`) da mevcuttu. Yanlış iddia, dosyalar kontrol edilmeden
yazıldığı için oluştu; bu kayıt, aynı işin ikinci kez yapılmasını önlemek için burada
bırakıldı.

**Gerçekten eksik olanlar ve yapılanlar.**

- **İki yeni konu şablonu** eklendi: `hata-bildir.yml` (yanlış sayı/kimlik/sınıflandırma
  bildirimi) ve `arac-oner.yml` (listeye araç önerisi). Bir de `config.yml` ile metodoloji
  ve mimari belgelerine yönlendiren bağlantılar eklendi. Kaynak öneri şablonu olduğu gibi
  korundu — çalışıyor, değiştirmek için sebep yoktu.
- **`CONTRIBUTING.md`** yazıldı: katkının nasıl işlediği, kaynak güven seviyeleri (A/B/C),
  üretilmiş dosyaların elle düzenlenmeyeceği kuralı ve derleme/denetim komutları.
- **`CITATION.cff`** eklendi; akademik veya gazetecilik kullanımında atıf künyesi hazır.
- **CI genişletildi:** `build_pages.py --check` (statik sayfalar veriyle uyumlu mu) ve
  `consistency.py` (bileşen bazlı puan tutarlılığı) adımları eklendi.

**Kalan iş.** README hâlâ bir iç belge gibi okunuyor; rozet satırı (araç sayısı,
doğrulanmış oran, son güncelleme) `validate.py --json` çıktısından otomatik üretilebilir
ama üretilmiyor. Ayrıca haftalık zamanlanmış bir iş, `fiyat-bandi-bayat` uyarısı üreten
araçları listeleyip otomatik konu açabilir — kurulmadı.

### Y-14 · Veri/kabuk ayrımı ve tembel yükleme

**Sorun.** Tek dosya bugün 1,2 MB ve araç sayısıyla doğrusal büyüyor; 1.000 araçta yaklaşık
4 MB olur ve mobil bağlantıda kabul edilemez hale gelir. Veri hacminin büyük kısmını 972
`evidence` bloğunun metinleri oluşturuyor ve bunlar yalnızca detay panelinde okunuyor.

**Kapsam.** Uygulama kabuğu ile veri ayrılır; liste ekranı için özet veri, detay için tam
kayıt tembel yüklenir. Duman testine bir performans bütçesi kontrolü eklenir — bugünkü 49
kontrol sayfanın çalıştığını doğruluyor ama hızını hiç ölçmüyor.

**Ön koşul:** Ölçüm olmadan iyileştirme yapılmaz. Önce gerçek cihazda ölçüm alınır, hedef
sayı yazılır, sonra iş başlar.

### Y-15 · Fiyat ölçümünün tekrarlanabilir hale gelmesi

**Sorun.** MK-19 ile 19 araç tarihli piyasa gözlemine bağlandı, ama 259 araç hâlâ tarihsiz
tahmin taşıyor ve denetim bunu `fiyat-tarihsiz` uyarısıyla işaretliyor. Ölçüm bir kez
yapıldı; tekrarlanabilir bir hat değil.

**Kapsam.** Ölçümün belgelenmiş, tekrarlanabilir bir protokole dönüşmesi ve kapsamın
büyütülmesi. Tazelik, kopyalanamayan tek rekabet avantajı olduğu için bu madde ticari
olarak da en kritik olanlardan biri (`docs/URUN-STRATEJISI.md` §4.2).

**Bitmiş sayılma ölçütü.** Ölçüm ikinci kez, aynı yöntemle ve elle müdahale olmadan
çalıştırılabiliyor; tarihli fiyat taşıyan araç sayısı belirgin biçimde artıyor.

### Y-16 · Boş ağırlık verisinin doldurulması — **hazırlandı, veri toplama bekliyor**

**Sorun.** P2.1 entegrasyonundan sonra tork kapsamı 251/278'e çıktı ama `fun` kapsamı
163'te kaldı. Sebep tek bir alan: **88 araçta tork var, boş ağırlık yok** ve formül ikisini
birden istiyor. P2.1 veri paketinde boş ağırlık alanı hiç bulunmuyor — hem SQLite hem
Excel çıktısı ayrı ayrı kontrol edildi.

**Neden öncelikli.** Tek bir veri kalemi, bir kriterin kapsamını 163'ten 251'e çıkarıyor —
yani neredeyse yarı yarıya büyütüyor. Depodaki hiçbir iş kaleminin getiri/çaba oranı buna
yakın değil.

**2026-08-13'te ne yapıldı.** Veri toplanamadı ama iş **mekanik hale getirildi**:

- `data/queue/kerb-weight-worklist.json` — doldurulacak 88 aracın listesi; her satırda
  kimlik, ad, üretim yılı, beygir, hacim, şanzıman tipi ve boş bırakılmış
  `kerb_weight_kg` / `source_url` alanları. Yoğunluk BMW (22), Mercedes (18) ve Audi (9).
- `scripts/import_kerb_weight.py` — doldurulmuş listeyi araç kayıtlarına işleyen betik.
  MK-15 korumaları kod düzeyinde zorunlu: **kaynak adresi olmayan satır reddedilir**,
  listedeki beygir veya hacim araç kaydıyla uyuşmazsa reddedilir, 600 kg altı / 3.000 kg
  üstü değerler reddedilir (bu eşik varyant elemek için değil, libre-kilogram birim
  hatasını yakalamak için). Üç koruma da sahte veriyle test edildi ve çalışıyor.

**Neden bu oturumda doldurulamadı — dürüst kayıt.** Teknik özellik siteleri
(autoevolution.com, auto-data.net, ultimatespecs.com, carfolio.com) ve Wikipedia,
çalışma ortamının ağ geçidi tarafından engelli. Arama sonucu parçacıkları varyant bazında
**otomatik/manuel ayrımı vermiyor**; aynı modelin otomatik versiyonu manuelden 25-40 kg
ağır olabiliyor ve buradaki araçların hepsi otomatik. Manuel değeri yazmak güç/ağırlık
formülünü doğrudan yanıltırdı. CLAUDE.md'nin ve MK-15'in kuralı burada belirleyici oldu:
**boş bir alan, yanlış bir alandan iyidir.**

**Bitmiş sayılma ölçütü.** Çalışma listesi kaynak adresleriyle doldurulup
`python3 scripts/import_kerb_weight.py --write` ve ardından
`python3 scripts/compute_fun.py --write` çalıştırıldığında `fun` kapsamı 251/278'e
çıkıyor. Ağ erişimi olan bir oturum ya da doğrudan depo sahibi bunu tek geçişte bitirebilir.

### Y-17 · Kişiye özel rapor üretimi

**Sorun.** Puanlama motoru kullanıcının ağırlıklarıyla sıralama yapabiliyor ama bu yetenek
yalnızca arayüzde yaşıyor; teslim edilebilir bir çıktıya dönüşmüyor.

**Kapsam.** Kullanıcının bütçe, kullanım biçimi ve önceliklerinden bir kısa liste, her aday
için kaynaklı risk notu ve araç görmeye giderken kullanılacak kontrol listesi üreten bir
rapor çıktısı. İlk sürümde ödeme altyapısı **kurulmaz**; raporlar elle karşılanır, çünkü
amaç gelir değil öğrenmedir.

**Ön koşul.** Ödeme alınacaksa mesafeli sözleşme, ön bilgilendirme, cayma/iade akışı ve
KVKK aydınlatması önce kurulmalıdır (`docs/URUN-STRATEJISI.md` §8).

### Y-18 · `liq` için doğru sayım protokolü

**Sorun.** MK-20, elimizdeki 2.071 ilan gözlemini `liq` için reddetti: örneklem sorgu
başına 50 ile sınırlıydı, yani sağdan sansürlüydü ve sansür tam olarak ölçmek istediğimiz
yönde çalışıyordu.

**Kapsam.** Doğru ölçüm, ilanları çekmek değil **sorgu sonucundaki toplam ilan sayısını**
kaydetmektir; bu hem çok daha ucuz hem sansürsüz. `docs/PLAN.md` §3.7'deki protokol bu
düzeltmeyle güncellenmeli ve ölçüm tarihiyle birlikte `data/market/` altına yazılmalı.

---

## Değişmeyen kurallar

Bu maddelerin hiçbiri aşağıdakileri esnetmez. Hepsinin gerekçesi `CLAUDE.md` ve
`docs/ARCHITECTURE.md` içinde yazılı.

- Puan kanıta dayanır; kaynağı olmayan puan üretilmez. Bir bileşenin temel puanı yoksa
  alan boş bırakılır, uydurulmaz.
- Kullanıcı kaynak önerir, puanı metodoloji verir (MK-05).
- Katman katman ilerlenir: her katman kendi başına çalışır durumda bırakılır. Yarım
  kalmış bir yenileme yüzünden bugün çalışan sayfa bozulmaz.
- Her commit sonrası `python3 scripts/validate.py` hatasız, `node scripts/smoke_test.js`
  tam geçmelidir.
- `index.html` üretilmiş dosyadır, elle düzenlenmez.
- Kimlikler kalıcıdır; bir araç, motor veya kutu kimliği verildikten sonra değişmez.
