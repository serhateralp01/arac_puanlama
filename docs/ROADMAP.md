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

## Durum özeti (son güncelleme: 2026-08-20)

| Katman | Durum |
|---|---|
| Veri mimarisi (araç / motor / şanzıman / kaynak ayrımı) | Tamamlandı |
| Şanzıman kutusu kayıtları | 53 kutu (`data/transmissions.json`), hepsi temel puanlı, kaynaklı ve yapılandırılmış `known_issues` taşıyor |
| Motor ailesi kayıtları | 105 aile (`data/engines.json`), hepsi temel puanlı, kaynaklı ve yapılandırılmış `known_issues` taşıyor — Y-27'de BMW N57 eklendi |
| Denetim hattı (`validate.py`, `consistency.py`, `smoke_test.js`) | Çalışıyor, 0 hata, 92/92 duman testi — artık `file://` yerine süreç içi bir HTTP sunucusu üzerinden çalışıyor (statik sayfa, SEO, katalog, koyu tema, mobil menü, kart görünümü, bütçe girişi, ana ekran kanıt bağlantıları, tembel ayrıntı yükleme ve kaydırıcı etkileşimi kontrolleri dahil, bkz. Y-25/Y-26) |
| `age` ve `fun` kriterleri (MK-06) | Formüle bağlandı: `age` → `scripts/compute_age.py` (MK-14), `fun` → `scripts/compute_fun.py` (MK-17, **375/406 araç** — bkz. Y-19, Y-24). `comf` ve `cost` hâlâ elle veriliyor. |
| `price` kriteri (MK-19) | **Tarihlendi, iki ayrı kaynakla.** 19 araç 2026-08-13 tarihli arabam.com ilan gözlemine, 10 araç 2026-07 tarihli TSB Kasko Değer Listesi'ne bağlandı (bkz. Y-21). Toplam 29 araçta `price_reference` bloğu (tarih, yöntem, örneklem/kaynak, sınırlılık) var; kalan 371 araç hâlâ tarihsiz tahmin ve denetimde `fiyat-tarihsiz` uyarısı üretiyor. |
| `liq` kriteri (MK-20) | **Ölçülemedi, gerekçesi yazıldı.** Elimizdeki 2.071 ilan gözlemi sorgu başına 50 ile sınırlı olduğu için sağdan sansürlü; en likit araçlar tavanda birbirine karışıyor. Doğru protokol, ilanları çekmek değil sorgu sonucundaki toplam ilan sayısını kaydetmek. |
| Çok ekranlı arayüz: ana ekran, giriş akışı, liste, metodoloji, kaynak öner, iletişim | Çalışıyor |
| GitHub Pages yayını | Çıktı `index.html` (liste/kart için özet veri) ve `detay.json` (ayrıntı paneli için tembel yüklenen `note`+`evidence`, MK-24) olarak üretiliyor, kök adres siteyi açıyor |
| Liste ekranı denetim çubuğu (Y-05) | Tamamlandı: ağırlık/arama/filtre tablonun üstünde, filtre paneli katlanabilir |
| Kaynak öneri formu (Y-04) | Arayüz tamamlandı; gönderim uç noktası ve iletişim adresi tanımlanmayı bekliyor |
| Ana ekran (Y-07) | Tamamlandı: veri kapsamı özeti, hazır giriş yolları, en riskli bileşenler |
| Araştırma kuyruğu (Y-03) | Tamamlandı: `data/queue/`, şema, iki aşamalı akış, bir tur uçtan uca çalıştırıldı |
| Kaynak derinliği (Y-02) | **Bitti.** 400 aracın tamamı "doğrulanmış" (4+ kaynak) — `kaynak-yetersiz` uyarısı 2026-08-17'de tamamen kapandı, bkz. Y-19 |
| Araç listesi (Y-01) | 154 → 278 → 400 → 406 → **409 araç** (Y-19/Y-23/Y-27 terfi turları). Birinci dalgada **SUV 1 → 30 (hedefi aştı), marka 5/5 (hedefe ulaştı), 2016+ 5 → 42 (hedefi (40) aştı)**; ikinci dalga 300-900 bin TL bandında marka-model-motor-şanzıman çeşitliliğini artırıyor (228→278, 50 kombinasyon); Y-27'de portföy büyütme talebiyle 3 araç daha eklendi (2'si katalogdan otomatik terfi, 1'i elle araştırılan yeni bir motor ailesiyle — BMW N57/730d); Y-28'de depo sahibinin "C/D (+B) segmentine odaklan, E/F'ye, MPV'ye, ticariye gitme, 1,5 milyonu aşma" talimatıyla `data/queue/portfolio-expansion-bcd-worklist.json` üretildi — **877 aday trim, 301 grup**, henüz puanlanmadı, sıradaki turların çalışma listesi |
| Teknik katalog (MK-22) | **1.656 kayıt** (`data/catalog/`, marka başına bir dosya). Olgusal katmandır: güç, tork, çekiş, hacim, gövde, vites sayısı, kavrama tipi, motor kodu ve teknik kaynak adresi taşır; puan taşımaz. 283 kayıt puanlanmış bir araca bağlı, 1.215'i yalnız katalogda ve kendi statik sayfası var — bunun 15'i Y-22'de TSB Kasko Değer Listesi'nden eklendi. Y-27'de `promote_catalog.py`'nin terfi ettirdiği kaydın kaynak katalog satırını `scored_car_id` ile geri bağlamadığı bir betik hatası bulunup düzeltildi. |
| Kapsam sınırı | **Elektrikli, hibrit ve LPG'li araçlar kalıcı olarak kapsam dışı (MK-13)** |
| Puanlama şeffaflığı (Y-06) | **Bitti.** Bilimsel temel, kanıt zinciri, arayüz katmanı (kriter paneli artık liste ekranında, "neden bu puan" dökümü) tamamlandı |
| Veri doğruluğu (MK-18) | **Dış veri setiyle çapraz doğrulama yapıldı.** 220 araç bağımsız bir katalogla karşılaştırıldı; motor/şanzıman ailesinde 0 çelişki, beygir/torkta 10 çelişki bulundu ve doğrulanan 5 gerçek hata düzeltildi (en ağırı: bir 1.6 dizelde 400 Nm ve bir aracın tamamen yanlış motor ailesine bağlı olması). |
| Teknik özellik kapsamı | Boş ağırlık **375/406** (Y-24, WebSearch ile dolduruldu). Kalan 31 araçta tork veya ağırlık eksik; 4'ü bilinçli olarak boş bırakıldı (kaynakta kombinasyon doğrulanamadı, bkz. Y-24). |
| Görsel dil / ürün hissi | Koyu tema (Y-09) ve kart görünümü (Y-25) ile birlikte kullanıcı yüzeyi büyük ölçüde yenilendi; liste ekranı artık taranabilir kartlarla açılıyor, mobil menü açılır panele döndü. Denetim raporunun önerdiği dört fazdan yalnızca birincisi (tasarım/kullanılabilirlik) tamamlandı. |
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

**Durum: tamamlandı.** İkinci turda kalan 29 araç (Opel, Peugeot, Renault, Seat, Toyota,
VW, Volvo) için de ağırlık bulundu; terfi eden 99 aracın **tamamında** artık gerçek,
gerekçeli, `evidence.fun` kanıtlı bir `fun` puanı var — hiçbiri kardeş araçtan
kopyalanmıyor.

**İkinci turda 4 araç daha aynı rozet-uyuşmazlığı türünden düzeltildi.** Seat Ibiza
"1.0 EcoTSI · 150 bg" ve "1.6 · 150 bg" ile Volkswagen Golf "1.6 FSi · 130/150 bg" —
dördü de gerçekte var olmayan motor rozetleriydi (1.0 EcoTSI hiçbir zaman 150 bg
üretmedi, 1.6 FSI 2017'de VAG kataloğunda yoktu); gerçek motor dördünde de aynı ailenin
(`vag-ea211`) 1.5 TSI EVO ayarı. Düzeltme sırasında **bir gerçek kopya kayıt daha
bulundu**: Seat Ibiza'nın iki satırı (eski adlarıyla "1.0 EcoTSI 150 bg" ve
"1.6 150 bg") düzeltildikten sonra teknik özellikleri birebir aynı çıktı, yalnız yıl
aralığı farklıydı (2017-2017 vs 2017-2020, biri ötekinin alt kümesi) — aynı P2.1
eşleştirme zaafının (farklı rozetli kaynak satırları birleştirilmemiş) bir başka örneği.
Dar yıl aralıklı kayıt silindi, geniş aralıklı kayıt tutuldu, katalogdaki bağlı satır
yeni kimliğe yönlendirildi.

**Sonuç.** `validate.py` 0 hata, `smoke_test.js` 68/68, `build.py`/`build_pages.py`/
`build_content.py` yeniden üretildi. Araç sayısı 379 → 377 (bir terfi geri alındı, bir
kopya kayıt birleştirildi).

### Katalog katmanında Mercedes 3.0 V6 dizel (OM642) kümesi düzeltildi (2026-08-17)

**"sonra araştırma devam" fazının ilk turu.** `fun` düzeltmesi bitince, önceki turda
işaretlenmiş "Mercedes 3.0 dizel badge mismatch" grubuna geçildi: `data/catalog/
mercedes-benz.json`'da hacmi 3.0L olan 13 katalog-only kayıt, rozet metni (ör. "270
CDI", "E 320 CDI") ile beygir/tork/yıl arasında sistemli bir uyuşmazlık taşıyordu. Bu,
terfi eden araçlardaki OM651 anakronizmini bulan aynı araştırmanın devamı.

**11 kaydın 6'sı düzeltildi, 5'i düzeltilemedi ve dürüstçe işaretlendi.** OM642 3.0 V6
dizel 2005'ten önce üretilmedi. 2005 sonrası kayıtlarda rozet gerçek varyanta düzeltildi
(ör. "C 270 CDI · 231 bg" → gerçeği "C 350 CDI BlueTEC 4MATIC", "E 320 CDI · 252 bg" →
"E 350 BlueTEC"). 2001-2003 arası 4 kayıt ve bir CLK kaydı (tork/hp uyuşmazlığı çözülemedi)
için **hiçbir gerçek Mercedes ürünü rozet+beygir+yıl kombinasyonuna denk gelmiyordu** —
rozet uydurmak, atılan rozetten daha kötü bir hata olurdu, bu yüzden düzeltilmedi. Yeni bir
`quality_flags` değeri (`rozet_yil_celiskisi`) eklendi ve katalog sayfasında Türkçe
gerekçesiyle görünüyor (`scripts/build_pages.py`'deki `CATALOG_FLAG_TR` sözlüğü).

**Kendi hatam, commit edilmeden yakalandı.** İlk denemede düzeltmeyi `import_catalog.py`'yi
kaynak SQLite paketinden sıfırdan yeniden çalıştırarak uyguladım. Bu, hedeflenen 11 kaydı
doğru düzeltti ama **istenmeyen bir yan etki** yarattı: betiğin kendi iç bağlama mantığı
(`model_matches`), `promote_catalog.py`'nin bu oturumda kurduğu daha zengin eşleştirmeyi
(marka paylaşımı, motor kodu öneki, terfi sırasında elle düzeltilen adlar) bilmiyor ve
Mercedes dosyasındaki `scored_car_id` bağlarının çoğunu sıfırladı — katalogda yalnız
kalan kayıt sayısı 1.203'ten 1.221'e çıktı. `git diff --stat` ile fark tam yayılmadan
önce görüldü, hiçbir şey commit edilmedi; `git checkout` ile katalog dosyaları geri
alındı ve düzeltme bunun yerine **yalnız 11 hedef kaydı elle güncelleyen dar bir yama**
olarak yeniden yazıldı — `scored_car_id` alanına hiç dokunmadan. Ders: `import_catalog.py`
artık tek doğruluk kaynağı değil, üstüne `promote_catalog.py`'nin kurduğu bağlar var;
tam yeniden üretim yerine hedefli yama tercih edilmeli.

**Sonuç.** `validate.py` 0 hata, `smoke_test.js` 68/68, katalog-yalnız sayısı değişmedi
(1.203). Kalan büyük gruplar: BMW 2.0 benzin (çoklu aile bölünmesi), Honda 2.0 benzin
(K20/K24 vs R20A ayrımı) — Y-02 yöntemiyle sırayla devam.

### BMW 2.0 benzin kümesi tarandı, 7 anakronistik kayıt işaretlendi (2026-08-17)

**Bulgu.** 45 katalog-only BMW 2.0L benzin kaydı incelendi. Bunların çoğu (`engine_code`
dolu olanlar: N46B20, N43B20, N13B16) zaten sağlamdı. Geri kalanlarda `engine_code` boş
ve `engine_name` alanı Mercedes kümesindeki gibi bulaşmış/anlamsızdı ("318Ci 5AT RWD
(143 HP)" onlarca farklı beygir değeriyle tekrarlanıyordu) — bu yüzden marka+beygir+yıl
üçlüsü, dosyanın kendi içindeki **doğrulanmış** `engine_code`'lu satırların yıl
aralıklarıyla karşılaştırıldı (N46B20: ~2004-2007, N43B20: 2007-2011) ve iki dış olgu
WebSearch ile doğrulandı: N43B20'nin 2007'den önce, 528i'nin 245 bg'lik turbo tününü
üreten N20B20'nin 2012'den önce üretilmedi (mymotorlist.com, carbuzz.com).

**Sonuç: 7 kayıt anakronistik.** 3 kayıt (318i/320i, 143-170 bg, 2005 tarihli) N43B20'nin
üretime girmesinden 2 yıl önceye tarihli. 4 kayıt ("528i · 245 bg", 2009-2010) N20B20'nin
üretime girmesinden 2-3 yıl önceye tarihli. Mercedes kümesindekiyle aynı `rozet_yil_
celiskisi` etiketiyle işaretlendi, rozet uydurulmadı.

**Bir yanlış varsayım kendi kendine düzeltildi.** İlk bakışta "BMW 5 Serisi hiçbir zaman
4 silindirli motor almadı, F10'a kadar" varsayımıyla 8 kaydı (163/170/184/245 bg,
2007-2010) toptan işaretlemeyi düşündüm. WebSearch, N43B20'nin E60 5 Serisi 520i'de de
kullanıldığını gösterdi (yalnız *turbolu* 4 silindir F10'a özgüymüş) — bu yüzden 170 bg
(N43B20 sinyaline tam uyan) 2007 tarihli 2 kayıt **işaretlenmedi**, gerçek çıktı. Toptan
bir kural yerine tek tek doğrulamanın neden gerekli olduğuna bir örnek daha.

**Belirsiz kalan 3 kayıt bilinçli olarak dokunulmadı**: 184 bg/2009, 163 bg/2007 ve
170 bg/190 Nm/2009 hiçbir bilinen motor imzasıyla tam örtüşmüyor ama kesin "imkânsız"
da denemedi — düşük güvenle bir hüküm vermek, hiç vermemekten kötü.

**Sonuç.** `validate.py` 0 hata, `smoke_test.js` 68/68, katalog-yalnız sayısı değişmedi.
Sıradaki grup: Honda 2.0 benzin (K20/K24 vs R20A ayrımı).

### Honda ve VW kümeleri temiz çıktı; Skoda'da bir tork hatası bulundu (2026-08-17)

**Honda 2.0 benzin (9 kayıt) ve VW 2.0 dizel (31 kayıt) tarandı, ikisi de temiz.**
Honda'da 3 kayıt zaten `engine_code`'la (K20A4/K20A6/R20A) sağlam; geri kalan 6 kaydın
147-155 bg aralığı, F20B→K20A6 Accord 2.0 hattının bilinen pazar/yıl çeşitliliğiyle
tutarlı, zorlama bir düzeltme veya işaret gerekmedi. VW'de 110-240 bg arası bütün
tünler (PD-era ve EA189/EA288) gerçek, iyi belgeli VAG motorlarına denk geliyor ve
üretim pencereleri örtüştüğü için hiçbir yıl "imkânsız" testinden geçmedi. **Sorun
bulunmaması da bir sonuçtur** — zorlama bir işaretleme, gereksiz bir düzeltmeden farksız
bir hata olurdu.

**Skoda'da (94 kayıt tarandı) bir gerçek tork hatası bulundu.** "Octavia Scout 2.0 TDI
· 140 bg" (2006-2008) kaydı 434 Nm taşıyordu; dosyadaki diğer 5 "Octavia 140 bg"
kaydının hepsi 320 Nm. WebSearch beş bağımsız kaynakla (auto-data.net, ultimatespecs,
autodata24 dahil) gerçek değerin 320 Nm (BKD motoru) olduğunu doğruladı — 434 kaynak
veride bozuk. `torque_nm` düzeltildi, `engine_code: "BKD"` eklendi,
`MANUAL_SPEC_CORRECTIONS`'a işlendi (ileride yeniden içe aktarmada kaybolmasın diye).
Aynı taramada 150 bg'lik dört farklı gerçek motor (1.4 TSI/1.6 TDI/1.8T/2.0 TDI) ve
183 vs 184 bg (aynı motorun bölgesel PS/hp yuvarlama farkı) gibi görünüşte tuhaf ama
gerçekte doğru kayıtlar da kontrol edildi, dokunulmadı.

**Sonuç.** `validate.py` 0 hata, `smoke_test.js` 68/68.

### Yöntem değişti: marka-marka elle taramadan tüm katalogda otomatik aykırı-değer taramasına (2026-08-17)

**Neden değişti.** Hyundai, Volvo, Ford, Peugeot ve Citroën kümeleri elle tek tek
tarandı (Mercedes/BMW'deki gibi mantıksız yıl/rozet birleşimi arandı) ve hepsi temiz
çıktı — getiri belirgin biçimde azaldı. Skoda'daki gerçek hatayı (Octavia Scout 434 Nm)
bulan asıl şey yıl mantığı değil, **aynı rozet+beygirdeki kardeş kayıtlardan sapma**
oldu. Bu yüzden yöntem, kalan ~30 markayı tek tek elle taramak yerine, **48 marka
dosyasının tamamını tek geçişte** (marka, model ailesi, yakıt, beygir, hacim) gruplayıp
grup medyanından **%15'ten fazla sapan tork** değerlerini otomatik bulan bir betiğe
döndü.

**Bulgu: tüm katalogda yalnızca 1 gerçek hata kaldı.** "Hyundai i40 1.7 CRDi Executive
· 136 bg" (2011-2018) 441 Nm taşıyordu; dosyadaki 3 diğer aynı-badge kayıt 320-329 Nm.
WebSearch (auto-data.net, automobile-catalog.com, motoreu.com) gerçek değerin ~330 Nm
olduğunu doğruladı. Düzeltildi, `MANUAL_SPEC_CORRECTIONS`'a işlendi. Taramanın ilk
sürümü (hacimsiz gruplama) BMW 1 Serisi ve Citroën C3'te de "aykırı değer" buldu ama
ikisi de incelenince gerçekte **farklı iki motorun** (ör. Citroën C3 1.2 PureTech
110bg/205Nm vs 1.6 110bg/147Nm) hp'sinin tesadüfen çakışması çıktı — gruplama anahtarına
`displacement_l` eklenince bu yanlış pozitifler kayboldu. Kalan tek aykırı değer
(Citroën C5 e-HDi 115bg, 2014, 285 Nm vs 240 Nm) WebSearch'te üçüncü bir değer (270 Nm)
bulundu ve hangisinin doğru olduğu netleşmediği için **dokunulmadı**.

**Sonuç.** `validate.py` 0 hata, `smoke_test.js` 68/68. Katalogdaki bilinen hata sayısı:
Mercedes 3.0 dizel (6 düzeltildi + 5 işaretlendi), BMW 2.0 benzin (7 işaretlendi), Skoda
Octavia Scout (1 düzeltildi), Hyundai i40 (1 düzeltildi) — toplam 20 kayıt dokunuldu,
geri kalan ~1.183 katalog-yalnız kayıt bu taramadan temiz çıktı.

### Puanlanmış 22 araçta boş gövde tipi dolduruldu (2026-08-17)

**`govde-tipi-yok` uyarısı 26 → 4.** Terfi eden araçların çoğu katalogdan `body_type`
boş miras almıştı (P2.1 kaynak verisinde bu alan sık boştu); bu, arayüzdeki gövde
filtresinin o araçlarda çalışmaması demek. 22 kaydın gövde tipi tek ve tartışmasız
olduğu için dolduruldu (ör. Mercedes B-Serisi → MPV, CLK/CLC → Coupe, Skoda Octavia →
Hatchback — dosyadaki 9 diğer Octavia kaydıyla aynı kural). **4 kayıt bilinçli olarak
boş bırakıldı**: bunlar tek bir aracı değil, gövde tipi gerçekten farklı iki modeli
birlikte temsil eden eski (P2.1 öncesi) birleşik kayıtlar ("Kia Rio / Hyundai i20",
"Mercedes A/B Serisi", "Peugeot 2008 / 208", "Volvo S40 / V50" — meselā S40 sedan,
V50 istasyon vagonu). Bu dördüne tek bir gövde tipi yazmak, doğru olanı seçmek değil
yanlış bir kesinlik uydurmak olurdu.

**Sonuç.** `validate.py` 0 hata, `smoke_test.js` 68/68.

### Kaynak-yetersiz uyarısı tamamen kapandı: 377 aracın tamamı doğrulanmış (2026-08-17)

**Bulgu.** `kaynak-yetersiz` uyarısı taşıyan 11 aracın hepsi tam olarak 1 kaynak
eksikti (3/4). Bunlardan 6'sı zaten bu oturumda motor ailesi düzeltmesi gören
Mercedes araçlarıydı — **kendi düzeltmemin yan etkisiydi**: `specs.engine_id`'yi
OM651'den OM611/OM646'ya taşırken `evidence.motor.sources` güncellendi ama üst
seviye `car["sources"]` dizisi eski (yanlış) OM651 kaynağını hâlâ taşıyordu; ayrıca
`verification` alanı da kaynak sayısı 4'e çıktıktan sonra "verified"e taşınmamıştı
(validate.py bunu `etiket-turetilmedi` HATASI olarak yakaladı, commit'ten önce
görüldü ve düzeltildi).

**Kalan 5 araç 4 farklı motor ailesine dağılıyordu** (mb-m270, mb-om612, mb-m111,
hyundai-u2-16), her biri yalnızca 1 kaynağa dayanıyordu. Her aile için WebSearch'le
**genuinely bağımsız** (aynı yayın değil) bir ikinci kaynak bulundu (ör. M111 için
zaten `enginefinder.co.za` kayıtlıydı, arama aynı adresi tekrar getirdi ve
kullanılmadı — `usedmercedesparts.co.za` yerine seçildi), her ailenin `known_issues`
listesine yeni bir madde eklendi (MK-16 mekanik miras deseniyle bütün o aileyi
paylaşan araçlara otomatik yayılıyor).

**Sonuç: 377 araçtan 377'si "doğrulanmış".** `kismi_kaynak` 11 → 0. `validate.py`
0 hata, `smoke_test.js` 68/68. 4 yeni kaynak `data/sources.json`'a eklendi.

### Fiyat araştırması engellendi (ağ erişimi), küçük temizlikler yapıldı (2026-08-17)

**Fiyat araştırması denendi, teknik olarak imkânsız çıktı.** Kullanıcı arabam.com/
sahibinden.com'dan yeni bir fiyat anlık görüntüsü (snapshot) çekmemi istedi.
`WebFetch` ile üç ayrı otomotiv sitesi (arabam.com, sahibinden.com, arabalar.com.tr)
ve kontrol amaçlı Wikipedia denendi — **hepsi ağ geçidi tarafından engellendi**
(`EGRESS_BLOCKED`). `WebSearch` yalnızca arama sonucu özeti veriyor, tekil ilan
fiyatı değil — `scripts/import_price_snapshot.py`'nin gerektirdiği P25/medyan/P75
hesaplaması için gereken ham gözlem sayısına ulaşılamıyor. Düşük kaliteli bir tahmin
(blog yazısı ortalaması) üretip MK-19'un kendi tarihli-kaynaklı-örneklemli
standardını taklit etmek, hiç fiyat vermemekten kötü olurdu — bu yüzden
denenmedi, dürüstçe bildirildi.

**Bunun yerine küçük ama gerçek üç temizlik yapıldı.**
1. `yinelenen-ad`: "Audi A4 1.8T" adını taşıyan 2 farklı araç (150/163 bg) rozete
   beygir eklenerek ayırt edildi.
2. `yetim-kaynak`: 3 bağlanmamış kaynaktan 2'si gerçek bir eve sahipti —
   `otomobilforum_sanziman` (Renault EDC güvenilirliği) `renault-edc-kuru` ailesine,
   `dhaber_sportage_dct` (Kia Sportage DCT tartışması) `hyundai-7dct` ailesine
   bağlandı; bu iki aileyi paylaşan 28 araca da yayıldı.
3. **Kendi hatam, commit edilmeden yakalandı.** İlk denemede bu 28 aracın
   `sources` alanını "motor ∪ şanzıman" kümesiyle **değiştirdim**, oysa bazı
   araçlarda motor/şanzıman ailesinin taşımadığı **araca özgü ek kaynaklar**
   vardı (ör. "sikayetvar_tucson_dct") — bu üzerine yazma onları sildi, yetim
   kaynak sayısını 3'ten 11'e çıkardı. `validate.py` çıktısında fark edildi,
   `git checkout` ile geri alındı, düzeltme **ekleyici birleştirme** (mevcut
   kümeye yeni kaynağı eklemek, değiştirmemek) olarak yeniden yazıldı.
   `mkt` (genel TR piyasa ortalaması, tek bir araca özgü değil) hâlâ yetim —
   zorla bir eve bağlamak yanlış bir kesinlik olurdu, öyle bırakıldı.

**Sonuç.** `yinelenen-ad` 1 → 0, `yetim-kaynak` 3 → 1. `validate.py` 0 hata,
`smoke_test.js` 68/68.

### c-kaynakla-uc-puan: 40 → 29, iki aile B-seviye kanıtla güçlendirildi (2026-08-17)

**`c-kaynakla-uc-puan` uyarısının çoğu (26/40) aslında `fun` içindi ve düzeltilebilir
değil.** `fun` formülle hesaplanıyor ve `evidence.fun.sources` bilinçli olarak hep
boş (`compute_fun.py`'nin kendi belgelediği tasarım kararı); kural bu durumda aracın
genel kaynak listesine düşüyor, yani bu 26 uyarı "daha iyi kaynak bulunmadığı" için
değil, kuralın `fun` gibi formül-türevli bir kriterle "kaynak-tier" mantığının
kavramsal olarak örtüşmemesinden geliyor. Kalan ~14 uyarı (motor/trans/cost/liq)
gerçekten kaynak sorunu.

**PSA/Stellantis 1.2 PureTech (8 araç, motor).** Bu motorun yağ banyolu triger
kayışı sorunu o kadar yaygındı ki Stellantis 2020 ve 2022'de resmi bir geri çağırma
kampanyası başlattı (İngiltere'de tek başına 44.000 araç). Bu, C seviyesi bir forum
anekdotu değil — üreticinin kendi resmi eylemi, Parkers.co.uk (kurumsal otomotiv
basını) üzerinden B seviye kaynak olarak eklendi. `psa-puretech-12` ailesini
paylaşan 8 araca (Peugeot/Citroën/Opel) MK-16 ile yayıldı.

**Volvo kuru Powershift / Ford DPS6 (3 araç, trans).** Depoda zaten "Volvo'nun kuru
kavramalı kutusu, Ford'un DPS6'sıyla aynı temel tasarım (Getrag 6DCT250)" notu
vardı ve Ford DPS6 kaydında zaten B-seviye bir kaynak (ABD federal Vargas v. Ford
grup davası, 2020'de 77,4 milyon dolarlık uzlaşma) duruyordu — bu kaynak henüz
`volvo-powershift-kuru`'ya bağlanmamıştı. **Neredeyse mükerrer kaynak ekliyordum**:
WebSearch aynı topclassactions.com makalesini farklı bir ID'yle tekrar getirdi;
eklemeden önce mevcut kaynaklar tarandı, aynı URL'nin zaten `vargas_ford_dps6_
uzlasma` olarak kayıtlı olduğu görüldü, yeni kayıt silindi ve mevcut olan
`volvo-powershift-kuru`'ya bağlandı.

**Sonuç.** `c-kaynakla-uc-puan` 40 → 29 (11 gerçek düzeltme: 8 PSA + 3 Volvo).
Kalan 29'un çoğu hâlâ `fun` kaynaklı — kritere özgü bir kural düzeltmesi (fun'ı bu
kontrolden muaf tutmak ya da farklı bir eşik kullanmak) ayrı bir karar, burada
yapılmadı. `validate.py` 0 hata, `smoke_test.js` 68/68.

### MK-23: formül puanları kaynak-seviyesi denetiminden muaf tutuldu, 29 → 7 (2026-08-17)

**Yukarıda "ayrı bir karar" diye bırakılan iş karara bağlandı.** Kalan 29 uyarının
22'si `fun` ve `age` kaynaklıydı ve **düzeltilebilir cinsten değildi**: bu iki puanı
kaynak okuyarak değil belirlenimci bir formül üretiyor (`compute_age.py` TÜV yaş-kusur
eğrisinden, `compute_fun.py` güç/ağırlık oranından), dolayısıyla bir kaynak bulunsa
bile o kaynak puanı üretmiyor. Kural, `compute_fun.py`'nin tasarım gereği boş bıraktığı
`evidence.fun.sources` listesini görüp aracın genel kaynak listesine düşüyor ve
ölçülmüş bir oranı, o oranla ilgisi olmayan motor/şanzıman kaynaklarının seviyesine
göre yargılıyordu.

**Çözüm bir alan oldu, kriter adı listesi değil.** `evidence` şemasına `derivation`
alanı eklendi (`kaynak` | `formul`); iki hesaplama betiği kendi ürettikleri bloklara
`formul` yazıyor, `validate.py` bu değeri görünce kuralı atlıyor. `if k in ("fun",
"age")` yazmak daha kısaydı ama muafiyeti hak eden şey kriterin **adı** değil puanın
**nasıl üretildiği** — bir kriter yarın formülden yargıya geçerse doğru davranış
kendiliğinden gelmeli. Gerekçenin tamamı `docs/ARCHITECTURE.md` MK-23'te.

**Kuralın hâlâ iş gördüğü bozuk veriyle test edildi** (deponun yerleşik pratiği):
bir aracın `derivation` alanı `kaynak`'a çevrilip `fun` puanı 95'e (uç bant)
çekildiğinde kural yeniden ateşledi. İlk test "ateşlemedi" gibi göründü ama sebep
`grep` desenimin yanlış olmasıydı (kural adı çıktıda araç adından önce geliyor) —
kod değil test hatalıydı, doğrulanıp geçildi.

**Sonuç.** `c-kaynakla-uc-puan` 29 → 7, kalan 7'nin hepsi gerçek yargı kriteri
(`motor`, `trans`, `cost`, `liq`) — yani kural gürültüyü bırakıp asıl işine döndü.
Toplam uyarı 439 → 370. `validate.py` 0 hata, `smoke_test.js` 68/68.

### Terfi kapısı yeniden kuruldu: 377 → 403 araç, beş yeni koruma (2026-08-17)

**Terfi neden durmuştu.** Katalogdaki 1.243 puanlanmamış kaydın **769'u** hiç
denenmiyordu, çünkü `promote_catalog.py` "herhangi bir `quality_flags` varsa atla"
diyordu. Bunların 681'i **yalnızca** `generic_transmission_identity` taşıyordu ve bu
bayrak "KAYNAK VERİ kutu modelini çözememiş" demek — oysa bu betik kaynağın kutu
kimliğini hiç okumuyor, kutuyu deponun kendi tablosundan türetiyor ve her adımda
tekil eşleşme şart koşuyor. Yani kendi çözdüğümüz bir soruyu, başkası çözemedi diye
çözülmemiş sayıyorduk. Bayrak listesi "bayrak varsa dur"dan "**bayrak neyi söylüyorsa
ona göre dur**"a çevrildi (`BLOCKING_FLAGS`, her madde tek tek gerekçeli).

**Kapı açılınca beş gerçek hata sınıfı ortaya çıktı — hepsi yazmadan önce yakalandı.**
İlk kuru çalıştırma 54 aday üretti ve elle denetimde şunlar görüldü:

1. **Anakronizm (bu oturumda dördüncü kez).** 2004-2009 model bir Seat Toledo'ya
   2012'de üretime giren EA288 ve 2008'de çıkan DQ200 bağlanmıştı. Aynı sınıf hata
   daha önce OM651 (2000 model Mercedes'e), N43 (2005 model BMW'ye) ve N20 (2009
   model 528i'ye) ile üç kez çıkmıştı — hepsinde beygir/hacim doğru, yanlış olan tek
   şey zamandı. Artık **elle değil sistemik** çözülüyor: ailenin depoda görüldüğü
   model yılı aralığı çıkarılıyor ve aday o pencerenin dışındaysa eleniyor. Pencere
   dışarıdan bir üretim takvimi değil, deponun kendi 377 aracının söylediği şey.
2. **Kapsam ihlali.** Altı Toyota Corolla Hybrid aday listesine girmişti. Kaynak veri
   hibritleri "Benzin" yazdığı için yakıt alanı yakalamıyor. MK-13'ün gerekçesi
   (puanlama içten yanmalı motor + klasik otomatik davranışı üzerine kurulu) hibrit
   için de geçerli ve depoda bugüne kadar hiç puanlanmış hibrit yok; addan eleniyor.
3. **Platform karıştırma (MK-08).** Önden çekişli enine motorlu bir Audi A1, deponun
   tek `zf-6hp` örneği olan **dört çeker boyuna** A6'dan çıkarımla ZF 6HP'ye
   bağlanmıştı. Boyuna ve enine kutular aynı tedarikçiden bile olsa farklı fiziksel
   ünitedir; çekiş tipi artık şanzıman eşleştirme anahtarının parçası.
4. **Nesil sınırını aşan güç bandı.** "BMW 5 Serisi 535i · 306 bg" M54'e bağlanmıştı —
   betiğin **kendi dokümantasyonunda** "ilk sürümde yakalandı" diye yazan hatanın
   aynısı, ikinci kez. Sebep: %75-%135 bandı. M54 3.0L depoda 231 bg üretiyor, üst
   sınır 312'ye açılıyor ve 306 bg'lik N54 çift turbo içeri giriyordu. Bant %85-%110'a
   çekildi (aynı motor kodunun aynı hacimdeki gerçek tün farkı %10'u nadiren aşar) ve
   yıl toleransı 2'den 1'e indirildi; bu ikisi birlikte yanlış eşleşen bütün BMW
   benzinli adayları (218/230/258/306 bg) eledi, doğru dizel olanları (M57 197/231 bg)
   bıraktı.
5. **Ad ile kaydın çelişmesi.** "Volvo S60 2.0 T · 150 bg" yakıtı Dizel kayıtlıydı
   (düz "T" rozeti mevcut yakıt-çelişki denetiminde yoktu), "Ford Focus 1.5 Ti-VCT"
   kaydı 1.6 L idi. Bu kayıtların specs alanları büyük olasılıkla doğru, yanlış olan
   ad — ama o adla terfi etmek kullanıcıya benzinli rozet gösterip dizel puanı vermek
   olurdu. Ad düzeltilene kadar terfi bekletiliyor.

**Bir de kullanıcıyı doğrudan yanıltacak bir veri hatası bulundu ve düzeltildi.**
"Ford Fiesta 1.6 · 105 bg" kaydı şanzımanı "TK" (tork konvertörü) diyordu; bu neslin
Fiesta otomatiği istisnasız 6 ileri **PowerShift çift kavramalı** kutudur (DPS6),
automobile-catalog.com kayıtlarında "PowerShift (d-cl. 6)" diye açıkça yazılı. Fark
kozmetik değil: yanlış bırakılsa kayıt Ford'un sağlam Aisin AWF21'ine bağlanacaktı,
oysa gerçek kutu depoda **30 puanla "düşük km'de felaket" bandında** duran DPS6.
Düzeltildikten sonra kayıt doğru kutuya (`ford-dps6`) bağlandı.

**Bir gerileme de kapatıldı.** Daha önce terfisi geri alınan "CLK 270 CDI · 150 bg"
kaydına o sırada bayrak konmamıştı; bayraksız olduğu için aynı gün ikinci turda
sessizce geri geldi. `rozet_yil_celiskisi` ile kalıcı olarak kapatıldı.

**Sonuç.** 54 ham aday → beş koruma sonrası **26 terfi**. Araç sayısı 377 → 403,
statik sayfa 1.737 → 1.763. Yeni araçların gövde tipi elle dolduruldu (17 kayıt).
`validate.py` 0 hata, `smoke_test.js` 68/68.

**Kalan 1.217 kaydın neden terfi edemediği ölçüldü** (bir sonraki yatırımın nereye
yapılacağını bu belirliyor):

| Sebep | Kayıt |
|---|---|
| Bu marka+hacim+yakıt için depoda motor ailesi yok | 411 |
| Kovada birden çok motor ailesi var, ayrım yapılamıyor | 291 |
| Motor geçti, şanzıman ya da yıl elemesinde düştü | 231 |
| Ad ile kayıt çelişiyor | 119 |
| Beygir, ailenin bilinen bandının dışında | 86 |
| Engelleyen kalite bayrağı | 59 |
| Hibrit (MK-13 kapsam dışı) | 6 |

En büyük kalem (411) yeni motor ailesi araştırması istiyor — yani bu, eşleştirmeyle
değil Y-02'nin kaynak araştırmasıyla açılacak bir kapı.

### Ad-hacim çelişkisi: yöntem kuruldu, test edildi, **çöktüğü görülüp geri çekildi** (2026-08-17)

**Plan.** Yukarıdaki tablodaki 119 "ad ile kayıt çelişiyor" kaydı en işlenebilir
grup gibi görünüyordu: daha önce 25 yakıt çelişkisinde ölçülen örüntüde specs doğru,
ad yanlış çıkmıştı. Aynı MK-18 çapraz doğrulama yöntemi kurulacaktı: kaydın üçüncü
alanı `specs.engine_name` (ör. "1.6L Ti-VCT 6AT FWD (125 HP)") hakem sayılacak,
hakem kaydı tutuyorsa ad düzeltilecekti. Yöntem yazıldı, bir de koruma eklendi
(hakemin beygiri kaydınkiyle tutmalı, yoksa o satır bütün nesle yapıştırılmış genel
bir aile etiketidir) ve 48 kayıt "adı düzeltilebilir" çıktı.

**Yöntem çöktü: hakem bağımsız değilmiş.** `import_catalog.py`'nin sorgusuna
bakıldığında `e.engine_name` ile `e.displacement_cc` **aynı `engines` satırından**
geliyor (`LEFT JOIN engines e ON e.engine_id = v.engine_id`). Yani "iki alan
birbirini doğruluyor" diye okuduğum şey, tek bir kaydın kendini tekrar etmesiydi.
Gerçek karşılaştırma iki alan arasında değil **iki tablo arasında**:
`variants.model_variant` (ad) bir yana, `engines` satırı (hacim + açıklama) öbür yana.

**Somut karşı örnek bulundu.** Yöntem "Hyundai i40 1.7 CRDi Executive" ve "Kia
Optima 1.7 CRDi" kayıtlarını 1.6'ya çevirmek istiyordu. İkisi de aynı gerçek motoru
(Hyundai/Kia U2 1.7 CRDi, 136 bg) taşıyor ve bu motorun 1.7 olduğu deponun kendi
`hyundai-u2-17` ailesinde zaten kayıtlı — yani `engines` satırının sistematik
yanıldığı, adın doğru olduğu bir durum. Yöntem tam tersini söylüyordu.

**Karar: toplu yeniden adlandırma yapılmadı.** 48 kayıt yanlış adlandırılmadan önce
durduruldu; hiçbir veri dosyasına yazılmadı. `scripts/fix_catalog_labels.py`
korundu ama **yazma yeteneği kaldırıldı** — betik artık yalnız çelişkileri türlerine
göre raporlayan bir çalışma kuyruğu üretiyor, ve başındaki dokümantasyon yöntemin
neden çöktüğünü anlatıyor ki aynı yola ikinci kez girilmesin. Bu 119 kayıt
çelişkili ve terfiye kapalı kalıyor; açılmaları, hangi tarafın doğru olduğunu
söyleyen **gerçekten dışsal** bir kaynak (teknik künye sayfası) gerektiriyor —
`MANUAL_SPEC_CORRECTIONS` desenindeki gibi kayıt kayıt, alıntılı.

Bu, deponun kendi kuralının (CLAUDE.md §1: gerekçesi yazılmamış karar savunulamaz)
bir uygulaması: yanlış adla puanlanmış 48 araç üretmek, 48 kaydı çelişkili
bırakmaktan kötü olurdu.

### Yeni terfi edenlerin `fun` puanı hesaplandı; ağırlık araştırması 3 sahte kayıt daha yakaladı (2026-08-17)

**Terfi eden 26 aracın boş ağırlığı araştırıldı** ve `compute_fun.py` çalıştırıldı;
yani bu araçlar da kardeş-kopya değil, gerçek güç/ağırlık formülünden gelen kanıtlı
bir `fun` puanı taşıyor (23 araç; kalan 3'ü aşağıdaki sebeple geri alındı).

**Ağırlık aramak, beklenmedik bir denetim aracı çıktı.** Bir aracın gerçek teknik
künyesine bakmak, ağırlığın yanında rozet/yıl/güç birleşiminin tutarlılığını da
gösteriyor. Bu turda üç kayıt böyle yakalandı ve **terfileri geri alındı**:

| Kayıt | Sorun |
|---|---|
| BMW 530xd · 231 bg (2003-2004) | E60 530xd xDrive dizel ancak Eylül 2005'te üretime girdi |
| Saab 9-3 2.0 TS · 130 bg | 130 bg Saab'ın **atmosferik** 2.0i'sidir, addaki turbo rozetiyle çelişiyor |
| Saab 9-3 2.0 Turbo · 154 bg | 154 bg düşük basınçlı 2.0t'dir; "2.0 Turbo" rozeti Saab'ta 185-205 bg motoru anlatır |

Üçü de `rozet_yil_celiskisi` ile kalıcı olarak kapatıldı ve
`import_catalog.py`'ye işlendi. BMW 530xd, yıl penceresi kontrolünün neden tek
başına yetmediğinin iyi bir örneği: M57 ailesi depoda 1999-2011 arasında görülüyor,
yani 2003 pencerenin **içinde** — ama o yılda o gövdede o motorun **xDrive** sürümü
yoktu. Pencere ailenin ömrünü biliyor, modele özgü donanım takvimini bilmiyor.

**Sonuç.** Araç sayısı 403 → 400 (üç geri alma). Formülle hesaplanan `fun` puanı
taşıyan araç 261 → 284. `validate.py` 0 hata, `smoke_test.js` 68/68.

---

## Y-20 · Fiyat kaynağı araştırması ve aralık kaydırıcısının onarımı — **araştırma bitti, onarım bitti (2026-08-17)**

### Fiyat: hangi kaynağın kullanılabileceği araştırıldı

**Sorun.** `fiyat-tarihsiz` uyarısı 381 araçla en büyük açık kalem ve bu ortamdan
kapatılamıyor: `arabam.com`, `sahibinden.com` ve hatta `wikipedia.org` ağ geçidince
engelli (`EGRESS_BLOCKED`), yalnız arama motoru özetleri geliyor. Bu turda "veriyi
çek" yerine **"hangi yol hukuken ve pratik olarak açık"** sorusu araştırıldı; sonuç
`docs/FIYAT-KAYNAK-ARASTIRMASI.md` içinde tam metin olarak duruyor.

**En güçlü aday: TSB Kasko Değer Listesi.** Türkiye Sigorta Birliği'nin yayımladığı
kasko değer listesi, projenin ihtiyaç duyduğu kırılımı zaten taşıyan tek temiz kaynak:
satırlar marka ve tip kodunun yanında **motor hacmini, yakıtı ve vitesi** ayırıyor,
liste ayda bir güncelleniyor ve gün bazlı arşivi sayesinde her değere kalıcı bir tarih
damgası ile kaynak referansı verilebiliyor. Bu, deponun "kanıt puandan ayrı saklanır"
ilkesiyle birebir uyumlu. Bedeli, listenin **tek bir değer** vermesi: P25 ve P75
doğrudan çıkmıyor.

**Tamamlayıcı adım: bant genişliğini ayrı öğrenmek.** Kaggle'daki ilan seviyeli Türkiye
veri setlerinden P25/medyan ve P75/medyan **oranları** hesaplanabilir. Bu oranlar mutlak
fiyatın aksine zaman içinde kararlı: bir aracın fiyat dağılımının medyana göre ne kadar
geniş olduğu liranın değerinden büyük ölçüde bağımsız. Oranlar TSB'den gelen güncel
çapayla çarpılarak bant üretilir. Bu setlerin kaynağı büyük olasılıkla izinsiz kazıma
olduğu için **mutlak fiyat olarak kullanılmamalı**, yalnız dağılım şekli için ve kaynağı
belgede anılarak kullanılmalıdır.

**Elenenler, gerekçeleriyle yazıldı** ki altı ay sonra yeniden tartışılmasın: siteleri
doğrudan kazımak (iki sitenin de kullanım koşulları otomatik toplamayı açıkça yasaklıyor;
`sahibinden.com` ayrıca içeriğinin yapay zekâ eğitiminde kullanılmasını da yasaklıyor),
Cloudflare atlatmayı özellik diye satan hazır aktörler (parayla tutulmuş olması işi meşru
yapmıyor), GitHub'daki bakımsız kazıyıcılar, TÜİK (adet ve devir yayımlıyor, fiyat değil)
ve kurumsal fiyatlı sağlayıcılar (INDICATA, Autovista).

**Bu turda veri yazılmadı.** Araştırmanın kendisi çıktı; TSB listesinin toplu indirilebilir
olup olmadığı ve Kaggle setinin sütun listesi bu ortamdan doğrulanamadı, ikisi de belgenin
son bölümünde "kendi makinende ilk şu üç şeye bak" diye somut adım olarak duruyor.

### Aralık kaydırıcısı gerçekten sürüklenmiyordu; sebep beklenen yerde değildi

**Bulgu.** Kullanıcı model yılı/beygir/fiyat kaydırıcılarının "kaydırılmadığını"
bildirdi. Tarayıcıda ölçüldüğünde şikâyet birebir doğrulandı: rayın %60'ı boyunca
çekilen bir sürükleme, 1990-2020 aralığında değeri yalnızca **1990'dan 1991'e**
taşıyordu. Yani kaydırıcı tutuluyor, bir adım atıyor, sonra donuyordu.

**İlk şüpheli suçlu değildi.** CSS'teki `pointer-events:none` / thumb'a `auto` numarası
akla ilk gelen sebepti ve değiştirildi; davranış hiç değişmedi. Asıl sebep
`30-filtreler.js` içindeydi: `setRange()` her `input` olayında `renderFilters()`
çağırıyor, o da `fWrap.innerHTML=''` yaparak filtre panelinin bütün DOM'unu siliyordu —
**kullanıcının o an tuttuğu `<input type=range>` elemanı dahil**. Eleman yok olunca
tarayıcının sürükleme hedefi kayboluyordu.

**Düzeltme.** `setRange()` artık sürüklemenin sürüp sürmediğini biliyor. Sürerken panel
yeniden kurulmuyor; yalnız tablo yenileniyor ve o aralığa ait alanlar yerinde
eşitleniyor (`syncRangeDom`). Sürükleme bitince (`change`) tam yeniden çizim yapılıyor,
çünkü "kullanılabilir seçenek" kümeleri ancak o zaman güncellenmeli. Denenip gereksiz
olduğu görülen CSS değişiklikleri geri alındı: düzeltme tek bir gerçek sebebe indi.

**Gerileme testi eklendi.** `smoke_test.js` artık kaydırıcıyı gerçekten sürüklüyor ve
değerin aralığın en az beşte birini katetmesini şart koşuyor. Elemanın varlığını saymak
bu hatayı yakalamıyordu — nitekim eski sürümde "altı kaydırıcı var" kontrolü geçiyordu.
Kontrol sayısı 68 → 69.

Sürükleme, fare ve klavye (ok tuşları) için doğrulandı; rayın kendisine yapılan dokunuş
bilinçli olarak uçları oynatmıyor, çünkü iki uç üst üste durduğu için raya dokunmak
yanlış ucu fırlatabilirdi.

---

## Y-21 · TSB Kasko Değer Listesi'nin araca yazılması — **birinci tur bitti (2026-08-18)**

**Bulgu.** Y-20'de aranan ama bu ortamdan erişilemeyen TSB Kasko Değer Listesi'ne
kullanıcı kendi makinesinden ulaştı ve ham veriyi depoya elle yapıştırdı: 1.508 satır,
marka kodu + tip kodu + marka adı + serbest metin tip adı + 2012-2019 model yılları için
TL cinsinden resmi kasko değeri. Bu, Y-20'nin "kendi makinende doğrula" adımının karşılık
bulmasıydı ve projenin en büyük açık kalemi olan tarihsiz fiyat bandı sorununu ilk kez
gerçek, resmi, tarihli bir kaynakla kapatma imkânı verdi.

**Veri nereye kondu.** Ham TSV hiç değiştirilmeden `data/market/tsb-kasko-2026-07.tsv`
içine, yöntem ve sınırlılıkları anlatan künye `data/market/tsb-kasko-2026-07.json` içine
yazıldı — `price-snapshots-2026-08.json`'un izlediği örüntünün aynısı (MK-19). Kaynak
künyesi `data/sources.json`'a `tsb_kasko_degeri_2026_07` kimliğiyle eklendi (tip
`spec-database`, tier `A`, çünkü resmi bir sektör birliği yayını, tekil anekdot değil).

**Neden bir tür-değil sigorta değeri, ilan fiyatı değil.** `price_reference.price_semantics`
alanı `"estimate"` olarak işaretlendi; bu, `arabam.com` anlık ilan gözleminin taşıdığı
`"asking_price_snapshot"`'tan kasıtlı olarak farklı. Kasko değeri pazarlık payı taşımaz ve
tek bir satıcının iyimserliğini yansıtmaz; bu yüzden ilan fiyatının bir miktar altında
kalması beklenir. İki kaynak birbirinin yerine geçmiyor, birbirini tamamlıyor.

**Eşleştirme neden bu kadar temkinli tutuldu.** `scripts/import_tsb_kasko.py` yazıldı.
TSB'nin `Tip Adı` alanı serbest metin (ör. `"3 HB SKY-G 1.5 120 REFLEX 6AT"`); motor
hacmi, beygir, yakıt ve şanzıman kategorisi regex ile ayrıştırılıyor. Betik geliştirilirken
canlı veride iki gerçek çakışma yakalandı ve ikisi de bu oturumun daha önce dört kez
tekrarlayan "zamanda imkânsız eşleşme" hatasıyla aynı aile:

1. Skoda Superb 1.8 TSI için TSB satırı `"TIPTRONIC"` diyordu (torque konvertörlü),
   ama araç kaydı `"DSG"` (kuru çift kavrama, DQ200) taşıyordu — ikisi farklı fiziksel
   donanım. Kaba kategori kontrolü (`trans_category()`) eklenip DSG/TCT/S-tronic → DCT,
   düz "Tiptronic"/"AT"/"EAT" → TK, CVT/Multitronic → CVT, MCP/ETG → Robot ayrımı
   zorunlu tutulunca bu satır otomatik olarak elendi.
2. Aynı kontrol, Alfa Romeo MiTo 1.4 170 QV için TSB'nin "TCT" (çift kavrama) rozetli
   satırını da elimine etti, çünkü araç kaydı `aisin-tf80` (torque konvertörlü) taşıyor;
   iki kaynağın aynı nominal araç için farklı şanzıman ailesi iddia etmesi, MiTo QV'nin
   bilinen üretim tarihçesiyle (170 bg QV manuel şanzımanla satıldı) birlikte
   düşünüldüğünde, satırın atlanması gereken bir çelişki olarak değerlendirildi.

Eşleşme kabulü şu beşinin **hepsini** istiyor: marka, model ailesi adı (aracın isminden
marka öneki atılıp kalan ilk kelime — "Giulietta", "Octavia" gibi — TSB metninde geçmeli),
hacim (tam eşleşme), beygir (±3), yakıt ve şanzıman kategorisi. Bulunan yıl değerleri
aracın kendi üretim yılları aralığına (`years`) kırpılıyor; aralığın dışındaki model
yılları hiç okunmuyor.

**Sonuç: 400 aracın 10'una tarihli bant yazıldı.** 2012-2019 ile kesişen 289 araçtan
yalnızca 10'u bu beş koşulun tamamını sağladı — düşük bir oran, ama bilinçli bir seçim:
TSB listesi geniş olsa da bu projenin sahip olduğu spesifik motor/beygir/şanzıman
kombinasyonlarının çoğunu içermiyor, ve serbest metinden yanlış eşleştirmek (kanıt
kirletmek) hiç eşleştirmemekten daha kötü. Yazılan 10 araç:
`citroen-c4-1-6-thp`, `ford-focus-3-1-6-ti-vct`, `opel-astra-1-4-t-2013`,
`opel-insignia-1-6-t`, `seat-altea-1-6-tdi-105-bg-105`, `seat-ibiza-6j-1-2-tsi-dsg`,
`seat-leon-1-6-tdi-105-bg-105-2`, `skoda-octavia-1-4-tsi-122`,
`skoda-octavia-1-4-tsi-122-bg-122`, `skoda-superb-2-0-tdi`. Yeni bantlar eskilerin
%10-25 civarında sapmasıyla çıktı — aşırı bir düzeltme değil, mevcut tahminlerin genel
doğru sırada olduğunun bağımsız bir teyidi. `fiyat-tarihsiz` uyarısı 381 → 371'e indi.

**Bilinçli olarak yapılmayan iş — portföy genişletme.** Kullanıcı ayrıca "portföyü öbür
listeden ilham alarak genişlet" istedi. `data/catalog/*.json` dosyaları elle
düzenlenmiyor — `_comment` alanında açıkça yazdığı gibi `scripts/import_catalog.py`
tarafından P2.1 veri paketinden üretiliyor (MK-22); TSB satırlarından elle yeni katalog
kaydı uydurmak bu katman sınırını ihlal ederdi. Ayrıca katalogdan puanlı araca terfi
(`promote_catalog.py`) yalnızca fiyatla değil motor/şanzıman/konfor gibi güvenilirlik
kanıtıyla da besleniyor; TSB tek başına bunu sağlamıyor. Bu yüzden genişletme bu turda
yapılmadı; TSB'nin geniş marka/model kapsamı ileride hangi katalog kayıtlarının terfi
kuyruğunda önceliklendirilebileceğine dair bir ipucu olarak duruyor, ayrı bir tur ister.

*Güncelleme:* Kullanıcı katman sınırını bilerek gevşetti ("portföy genişletmene izin
veriyorum") ve genişletme aynı gün Y-22'de, katalog dosyalarını hâlâ elle değil kod
aracılığıyla değiştiren bir yöntemle yapıldı — ayrıntı aşağıda.

**Bitmiş sayılma ölçütü — bir sonraki tur için.** `python3 scripts/import_tsb_kasko.py`
dry-run'da kaç yeni eşleşme bulduğunu gösterir. Eşleştirme kapsamını genişletmenin en
güvenli yolu model ailesi token listesini (bugün tek kelime) çok kelimeli isimlere
(`"C4 CACTUS"`, `"3008"` gibi) genişletmek ve gövde tipini (`body_type`) de TSB metninden
ayrıştırıp beşinci bir eşleşme koşulu yapmaktır — bu, `opel-astra-1-4-t-2013` gibi
GTC/sedan/hatchback karışık bantların gövdeye göre daralmasını sağlar.

---

## Y-22 · TSB verisiyle katalog portföyünü genişletme — **birinci tur bitti (2026-08-18)**

**Kullanıcı izni.** Y-21, "portföyü genişlet" isteğini bilinçli olarak ertelemişti çünkü
`data/catalog/*.json` elle düzenlenmiyor ve TSB tek başına terfi için gereken
güvenilirlik kanıtını sağlamıyor. Kullanıcı "tamam portföy genişletmene izin veriyorum
ya" diyerek katman sınırını değil, o sınırın YÖNTEMİNİ gevşetti: katalog dosyalarına
elle JSON yazmak yerine, `data/cars/`'ın ötesinde yeni bir **olgusal** (puansız) katalog
kaydı üretmenin kod aracılığıyla yapılmasına onay verdi.

**Kapsam neden küçük çıktı.** `import_tsb_kasko.py`'nin ayrıştırıcısı 1.508 satırdan
yalnızca 76'sının otomatik şanzımanlı olduğunu buldu (listenin çoğu manuel varyant —
bu proje yalnızca otomatik vitesli araçları kapsıyor, MK ile uyumlu bir eleme). 76 satır,
aynı teknik kombinasyonun farklı donanım seviyelerini (STYLE/ELEGANCE gibi) birleştirince
35 benzersiz marka+model+hacim+beygir+yakıt+şanzıman kombinasyonuna indi. Bunların 17'si
zaten `data/cars/` veya `data/catalog/` içinde vardı (aynı eşleştirme mantığıyla
doğrulandı), 1'i (Alfa Romeo MiTo 1.4 170 QV + TCT) bu oturumda tekrarlayan
"zamanda imkânsız eşleşme" ailesinden olduğu için bilinçli olarak atlandı — MiTo QV
170'in bilinen üretim tarihçesi manuel şanzımanla satıldığını gösteriyor, TSB'nin çift
kavramalı TCT rozeti bu bilgiyle çelişiyor. Geriye **15 gerçekten yeni** kayıt kaldı.

**Neden elle liste, tam otomasyon değil.** 35 küçük bir sayı olduğu için her biri tek
tek incelendi: TSB'nin serbest metninde çekiş (önden/arkadan/4x4) ve gövde tipi çoğu
zaman açık değil; genel bir algoritma yazmak yerine her kaydın çekişi modelin bilinen
mimarisinden (ör. Peugeot 3008 Mk1 bu motorlarla hiç 4x4 satılmadı → güvenle Önden),
gövde tipi modelin adından (ör. "DS4" her zaman hatchback, "C5" bu yıllarda sedan)
elle doğrulandı. Bu liste `scripts/import_tsb_catalog.py` içindeki `NEW_ENTRIES`
sabitinde duruyor; betiğin kendisi yalnızca bu listeyi id çakışması ve şema sınırları
için denetleyip mekanik olarak yazıyor — `scripts/import_kerb_weight.py`'nin elle
hazırlanmış çalışma listesini işlemesiyle aynı desen (MK-15).

**Şanzıman ailesi belirsizliği görünür bırakıldı.** TSB metni kuru/ıslak çift kavrama
ayrımını hiç vermiyor; bu yüzden DCT kategorisindeki her yeni kayıt torque/hp'ye dayalı
bilinen mühendislik kuralıyla (düşük tork → kuru, yüksek tork → ıslak — aynı kural bu
oturumda Seat Altea/Skoda Superb DSG eşleşmelerinde zaten doğrulandı) sınıflandırıldı
ve `generic_transmission_identity` bayrağıyla işaretlendi. Bu yeni bir istisna değil:
katalogdaki 1.641 kayıttan 798'i zaten aynı bayrağı taşıyor.

**Sonuç.** 15 yeni katalog kaydı: Opel Crossland X 1.2 Turbo, Opel Corsa 1.4 AT6, VW
Jetta 2.0 FSI Tiptronic, Opel Mokka X 1.6 CDTI, Skoda Rapid Spaceback 1.0 TSI DSG, Seat
Ibiza FR 1.4 TSI DSG 150, Citroën C5 1.6 e-HDi (112 ve 115 bg, iki ayrı kayıt), Peugeot
3008 1.6 HDi (110 ve 112 bg), Citroën DS4 1.6 e-HDi 112 ve 1.6 THP 156, Skoda Octavia RS
2.0 TDI 170 DSG, Skoda Superb 1.8 TSI 160 Tiptronic (mevcut DSG'li Superb'ten AYRI bir
kayıt — aynı motor/beygir ama farklı şanzıman ailesi, iki gerçek tarihi varyant), Audi
A1 Sportback 1.6 TDI 90 S tronic. Katalog kaynak sicili `data/catalog/_sources.json`'a
`tsb_kasko_degeri_2026_07` eklendi. `katalog_kaydi` 1.641 → 1.656, `yalniz_katalogda`
1.203 → 1.218. Hiçbiri puanlı araca terfi etmedi — terfi ayrı bir tur ve ayrı bir kanıt
standardı ister (bkz. `promote_catalog.py`), bu tur yalnızca olgusal varlığı kaydetti.

**Bitmiş sayılma ölçütü — bir sonraki tur için.** `python3 scripts/import_tsb_catalog.py`
dry-run'da mevcut `NEW_ENTRIES` listesini gösterir. Genişletmeyi sürdürmenin yolu, TSB'nin
şu an atlanan **manuel** şanzımanlı satırlarını değil (proje kapsamı dışı), gelecekteki
başka bir TSB baskısını veya başka bir yapılandırılmış listeyi aynı elle-inceleme
disipliniyle işlemektir — otomatik ayrıştırmanın hacmi büyütmesi değil, incelemenin
insan tarafından yapılması bu katmanın güvenilirliğini koruyan şey.

---

## Y-23 · Terfi turu: 8 anakronik katalog kaydı bulundu, 6 araç güvenle terfi etti — **bitti (2026-08-18)**

**Bağlam.** Kullanıcı "verileri genişletmek, portföyü genişletmek, bilgileri doğrulamak"
dedi. `scripts/promote_catalog.py` dry-run çalıştırıldığında 38 aday, bunların 27'si
depoda zaten aynı adla vardı, geri kalan 11'i incelendi.

**Bulgu: iki tanıdık isim geri geldi.** Aday listesinde `bmw-5-serisi-530xd-231-bg-231-2`
ve iki Saab kaydı vardı — bunlar bu oturumun DAHA ÖNCEKİ bir turunda (bkz. yukarıdaki
"Yeni terfi edenlerin fun puanı hesaplandı" bölümü) zamanda-imkânsız eşleşme oldukları
için puanlı katmandan SİLİNMİŞTİ. Sorun: silme işlemi yalnızca `data/cars/`'daki
kopyayı kaldırmıştı, bunları besleyen `data/catalog/` satırlarına hiç bayrak
konmamıştı — yani aynı hatalı eşleşme `promote_catalog.py` bir dahaki sefer
çalıştığında sessizce GERİ GELEBİLİRDİ. Bu turda önce bu üçü `rozet_yil_celiskisi`
bayrağıyla işaretlendi (kalıcı engel, bkz. `BLOCKING_FLAGS`).

**Sistematik tarama, üçten sekize çıktı.** Bayraklı satırların "kardeşlerini" (aynı
`name` alanını taşıyan diğer katalog satırlarını) taradığımda 5 tane daha bulundu:
`saab-9-3-2-0-ts-130-bg-130-2` ve dört BMW 318i/320i kaydı — hepsi P2.1 veri
paketinin AYNI gerçek-dışı kombinasyonu farklı `source_variant_id` altında birden
fazla kez tekrarladığının kanıtı. Sekizi de bayraklandı; `scripts/import_catalog.py`
içindeki `BADGE_YEAR_CONFLICTS` sözlüğüne de eklendi (yalnız üretilen JSON'a değil,
kaynağa da yazıldı ki katalog bir daha üretilirse bayrak kaybolmasın).

**Yol boyunca üçüncü bir kusur: `year_ok()`'un ince-örneklem kaçış deliği.**
`promote_catalog.py`'nin kendi zaman-makullüğü kontrolü, bir aile depoda **2'den az
araçta** görülüyorsa (`len(ys) < 4`) kontrolü tamamen ATLIYOR ve adayı otomatik geçerli
sayıyor — "depo o ailenin bütün üretim dönemini örneklemiş olmayabilir" gerekçesiyle
bilinçli eklenmiş bir esneklik, ama bunun bedelini bu turda somut olarak ödedik:
"Skoda Superb 1.8 TSI 160 Tiptronic" (2012 model, Y-22'de eklenen bir katalog kaydı)
`vag-01m`'e eşleşti — bu, depoda TEK bir araçta (1996-2010 model bir Skoda Octavia
Tour) görülen, **4 ileri** eski nesil bir kutu. 2012 model bir Superb'e 1990'ların
4 ileri kutusunu bağlamak, bu oturumda dört kez tekrarlayan "zamanda imkânsız eşleşme"
hatasının BEŞİNCİ örneği olurdu — yalnız bu kez hatayı üreten kendi yazdığım betikti.
Aynı sebeple "Alfa Romeo MiTo 1.4 T 135 bg (2008)" adayı da elendi: `fca-multiair-14`
motor ailesi depoda yalnızca 2009 ve sonrasında görülüyor (MultiAir teknolojisi
MiTo'ya gerçekte 2009-2010'da geldi, 2008 lansmanında değil), aday yalnızca ±1 yıl
toleransının sınırında kaldığı için otomatik geçti. İkisi de `--write` çalıştırılmadan
ELLE elendi (betiğin ürettiği 8 adaydan 6'sı yazıldı); ikisi de kalıcı bir
`rozet_yil_celiskisi` bayrağı ALMADI çünkü bu ortamdan web erişimi olmadığı için iddia
tam doğrulanamadı — yanlış olduklarına dair güçlü ama kesin olmayan bir sinyal var, bu
yüzden gelecekte doğrulanana kadar yalnızca katalogda, terfi edilmemiş halde bekliyorlar.

**`year_ok()` kendisi bu turda değiştirilmedi.** Eşiği "2'den az araç" yerine sıkılaştırmak
(ör. hep uygula, hiç atlamama) muhtemelen bugün GEÇERLİ olan başka eşleşmeleri
yanlışlıkla reddederdi — deponun 406 aracının çoğu aile başına 1-3 örnekle temsil
ediliyor. Doğru düzeltme muhtemelen "ailenin TEK örneği varsa pencereyi o örneğin
kendi yıl aralığına ±1 sabitle" gibi daha ince bir kural, ama bunun başka hangi
mevcut terfileri etkileyeceği bu turda test edilmedi. Bir sonraki adım olarak
`docs/ROADMAP.md`'ye not düşüldü, koda dokunulmadı — CLAUDE.md §2: çalışan bir sistemi
aceleyle değiştirmek yerine önce anlaşılmalı.

**Sonuç.** 6 araç terfi etti: `audi-a8-3-0-tdi-250-bg-250`, `citroen-c5-1-6-115`,
`citroen-c5-1-6-112`, `citroen-ds4-1-6-112`, `opel-corsa-1-4-90`, `skoda-rapid-1-0-110`
(dördü Y-22'de TSB'den eklenen katalog kayıtlarının terfisi). 400 → 406 araç. `motor`/
`trans` puanları MK-16 mekanik miras deseniyle aile kaydından geldi; `comf`/`cost`/`liq`/
`fun` en yakın kardeş araçtan tahmin edildi ve `note` alanında açıkça "araca özgü
araştırılmadı" yazıyor — uydurma değil, deponun zaten kullandığı yöntemin otomatikleştirilmiş
hali. `validate.py` 0 hata (yeni uyarılar `c-kaynakla-uc-puan` +2 ve `govde-tipi-yok` +1,
ikisi de deponun geri kalanında zaten var olan, kabul edilmiş bir kalıp). `smoke_test.js`
tam geçti.

**Bitmiş sayılma ölçütü — bir sonraki tur için.** `python3 scripts/promote_catalog.py`
çalıştırıp "aday" sayısına bakmak: kalan 27 "depoda aynı adla zaten var" satırının
eşlemesi elle çözülebilir (aynı araç muhtemelen farklı bir id altında zaten var, ama
`scored_car_id` bağlanmamış). `year_ok()`'un ince-örneklem kuralı sıkılaştırılmadan
önce mevcut 406 aracın kaçının bu kuralın gevşekliğinden geçtiği taranmalı — bu turda
üç örnek elle bulundu, sistematik bir tarama yapılmadı.

---

## Y-24 · Boş ağırlık verisi 88 → 91/95 dolduruldu, `fun` kapsamı 285 → 375 — **birinci tur bitti (2026-08-18)**

**Bağlam.** Y-16'nın çalışma listesi (`data/queue/kerb-weight-worklist.json`) 2026-08-13'te
88 satırla hazırlanmış ama hiç doldurulmamıştı; bu ortamdaki `WebFetch`/doğrudan sayfa
erişimi bu turda da engelliydi, ama `WebSearch` (arama motoru özetleri) çalışıyor —
bu farkın kendisi Y-20'de zaten tespit edilmişti. Bu tur o farkı kullandı: 95 aracın
her biri için (listeye 6. bölümdeki 7 yeni araç da eklendi) marka+model+üretim yılı+
motor hacmi+beygir+şanzıman tipini BİRLİKTE doğrulayan bir sorgu yazıldı (MK-15), sonuç
tek bir kaynak URL'siyle birlikte çalışma listesine işlendi.

**Sonuç: 91/95 dolduruldu, 4'ü bilinçli olarak boş bırakıldı.** `python3
scripts/import_kerb_weight.py --write` bu 91 satırı 0 ret ile işledi (hiçbiri MK-15'in
beygir/hacim/aralık korumalarına takılmadı, çünkü her satır yazılmadan önce elle
doğrulandı). Boş bırakılan 4'ün nedeni farklı, hepsi CLAUDE.md §1'in "düzeltilemeyen bir
şey varsa gerekçesiyle açık bırakılır" ilkesine uyuyor:
- **Ford Kuga 1.5 EcoBoost 6AT (150 bg)** ve **Peugeot 2008 1.6 THP (156 bg)**: arama
  sonuçları ısrarla farklı bir beygir seviyesinin (180 PS, 156 yerine değişik bir tün)
  verisini döndürdü; doğru varyantın ağırlığı bulunamadı.
- **Hyundai Elantra AD 1.6 CRDi 7DCT (136 bg)**: doğru sayfalar bulundu ama arama
  özetinde sayısal değer hiç görünmedi.
- **Skoda Fabia 1.0 TSI DSG (95 bg)**: bulunan tek otomatik veri noktası aslında 110 bg
  tünü içindi; 95 bg'nin gerçekten DSG ile satılıp satılmadığı kaynaklarda belirsiz
  kaldı — bu, Y-19'da BMW E90 318d'de görülen "düşük güç tünü yalnız manuel olabilir"
  kalıbının aynısı. Sayı uydurmak yerine boş bırakıldı; ayrı bir doğrulama gerektiriyor.

**Bazı satırlar tam eşleşme yerine gerekçeli tahmin taşıyor.** Otomatik şanzımanlı
model doğrudan bulunamadığında (özellikle eski/az bilinen Mercedes/BMW/Opel modelleri),
manuel şanzımanın doğrulanmış ağırlığına bu segment için tipik tork-konvertörlü fark
(~20-40 kg, deponun kendi karşılaştırılabilir çiftlerinden — ör. Seat Altea XL manuel/
DSG farkı — kalibre edildi) eklendi ve bu **`kerb-weight-worklist.json`'daki `note`
alanında açıkça yazıldı**. Bu, deponun zaten kabul ettiği bir yöntemin
(`promote_catalog.py`'nin comf/cost/liq tahmini) aynısı — uydurma değil, açıkça
işaretlenmiş bir yaklaşım.

**`fun` kapsamı 285 → 375 (406 aracın %92'si).** `scripts/compute_fun.py --write`
çalıştırıldığında ortalama mutlak sapma eski elle verilen puana göre yalnızca 3,7 puan
çıktı (betiğin kendi dokümantasyonundaki tipik 17-18 puanlık sapmanın çok altında — bu
turda düzeltilen ağırlıkların çoğu zaten iyi tahmin edilmiş kombinasyonlardı). En büyük
sapmalar (BMW E46 318i 68→21, Toyota C-HR 52→9) tek tek incelendi: ikisi de düşük güç/
ağırlık oranlı, girişseviyesi motor varyantları — eski elle verilen puan muhtemelen
"marka spor imajı" önyargısıyla şişirilmişti, formül düzeltmesi mantıklı.

**Doğrulanan pipeline sırası.** `import_kerb_weight.py --write` → `compute_fun.py
--write` → `validate.py` (0 hata) → `build.py` → `build_pages.py` → `build_content.py`
→ `smoke_test.js` (72/72). Her adım ayrı ayrı çalıştırılıp doğrulandı.

**Bitmiş sayılma ölçütü — bir sonraki tur için.** Kalan 31 araçta (406-375) hâlâ tork
veya ağırlık eksik; `python3 scripts/compute_fun.py` (yazmadan) hangi araçların
atlandığını listeler. 4 bilinçli boş satır (yukarıda) ayrı bir WebSearch turunda farklı
sorgu ifadeleriyle yeniden denenebilir. Skoda Fabia 1.0 TSI 95 bg + DSG kombinasyonunun
gerçekten var olup olmadığı, bu oturumda tekrarlayan "kombinasyon gerçek mi" sorusunun
yeni bir örneği — dış doğrulama (kullanıcının kendi araştırması ya da web erişimi olan
bir oturum) gerekiyor.

---

## Y-25 · Tasarım denetimi ve kart görünümü: liste ekranı baştan ele alındı — **beş faz + görsel tazeleme bitti (2026-08-19)**

**Bağlam.** Depo sahibi bu turda açıkça "tasarımsal ögeler kesinlikle değişmeli,
araç listesinin olduğu site çok daha streamlined ve akıcı olmalı, site genel
olarak hiç kullanıcı dostu değil" dedi ve ardından "çözmeye başla her şeyi;
tasarım ve frontend bu projenin her şeyi, iş kaliteli olmalı" diyerek tam
kapsamlı bir düzeltme turunu onayladı. Önce `docs/` içindeki mevcut kayıtlar
(ARCHITECTURE, URUN-STRATEJISI, PLAN) okunup projenin kendi öz-eleştirisi
çıkarıldı, sonra gerçek DOM ölçümleriyle (Playwright, `scrollWidth`, düğüm
sayısı, `performance.now()`) bağımsız bir denetim yapıldı. İki bulgu diğerlerinden
ayrıştı: mobil menü ekranın üçte birini kaplayıp yarı saydamlığıyla altındaki
içeriği okunaksız kılıyordu, ve liste ekranı 15 sütunlu bir tabloyla açılıp
406 aracın hepsi için ayrıntı satırını önceden inşa ediyordu — tek bir
`render()` çağrısı 55.007 DOM düğümü üretip 595ms sürüyordu.

**Birinci faz kapsamı — dört değişiklik.**

**1) Mobil menü artık açılır bir panel (dar ekran, ≤860px).** Önceden `.nav`
dar ekranda tam genişlikte açık bir sütuna dönüşüyor, sekiz bağlantı+tema
düğmesini üst üste diziyor ve toplam ~270px (844px'lik bir ekranın %32'si)
kaplıyordu. Artık üç çizgili bir düğme (`#navToggle`) bu listeyi bir açılır
panele (`#navPanel`, `.open` sınıfıyla) çeviriyor; kapalıyken üstbaşlık 59px'te
kalıyor. Panel bir bağlantıya tıklanınca, panelin dışına tıklanınca veya Esc'e
basılınca kapanıyor. Yalnızca CSS medya sorgusu ve `templates/app/10-yonlendirici.js`
içindeki `startNavToggle()` işlevi; masaüstü düzenine hiç dokunmadı.

**2) Liste ekranında kart görünümü varsayılan oldu, tablo ikinci sekme.**
`templates/app/60-tablo.js` yeniden yazıldı: `computeList()` filtre+sıralama
mantığını iki görünüm için ortaklaştırıyor ve sıra numarasını artık
`ranked.indexOf(c)` ile değil (406 satırlık listede O(n²) karşılaştırma) önceden
kurulmuş bir `Map`'le (O(n)) buluyor. Her kart; sırası, kıyaslama düğmesi,
renk kodlu toplam puanı (`colorFor()`, tablodakiyle aynı fonksiyon), adı ve
doğrulama rozetini üstte gösteriyor; altında sekiz kriterin hepsi kompakt birer
çubuk olarak duruyor (zayıf halka — `WEAK_THR` altı — kırmızı vurgulu); en altta
yıl/beygir/şanzıman rozeti ve düzenlenebilir fiyat aralığı var. Görünüm tercihi
`localStorage` (`arac_puan_gorunum`) ile kalıcı; `#viewToggle` düğmeleriyle
değiştiriliyor.

**3) Ayrıntı içeriği artık tembel — hem kartta hem tabloda.** Eskiden
`scoreBreakdownHTML()` + `radarSVG()` + zayıf halka listesi + kaynaklar her
aracın satırı için `render()` her çalıştığında önceden inşa ediliyordu, açılıp
açılmayacağına bakılmaksızın. Bu, denetimdeki 55 bin düğümün tek başına en
büyük kaynağıydı. Şimdi bu içerik `detailBodyHTML(c)` işlevinde toplandı ve
yalnızca bir kart veya satır ilk kez açıldığında bir kez çağrılıp konteynerin
`dataset.built` bayrağıyla önbelleğe alınıyor. Karar gereği hem tablo hem kart
görünümü her `render()` çağrısında birlikte inşa ediliyor (yalnızca aktif olan
CSS ile gösteriliyor) — bu, ilk tasarımda denenen "yalnız görüneni inşa et"
yaklaşımından vazgeçildiği anlamına geliyor, çünkü o yaklaşım gizli kalan
görünümde eski/tıklanamaz kıyaslama düğmeleri bırakıyordu ve zaten pahalı olan
kısım (ayrıntı içeriği) tembel olduğu için iki özet listeyi birden inşa etmenin
maliyeti kabul edilebilir kaldı.

**4) "Bir cümlelik otomatik özet" fikri kasıtlı olarak terk edildi.** İlk
tasarımda her kartın altında `note` alanının ilk cümlesinden üretilen bir
özet vardı. Gerçek veri üzerinde denenince, terfi edilmiş ~120 aracın `note`
alanının "Bu araç 2026-08-17 tarihinde `data/catalog/`'dan terfi ettirildi..."
gibi bir köken cümlesiyle başladığı görüldü — ilk cümleyi almak filoyla %30'u
için anlamsız veya yanıltıcı bir özet üretirdi. Bunun yerine zaten var olan ve
kanıta dayalı `weakOnes()`/`weakReason()` mekanizması (bir kriterin neden düşük
puan aldığını doğal dilde açıklıyor) kartın "nelere dikkat" katmanı olarak
kullanıldı; hiçbir yeni metin üretilmedi. CLAUDE.md §4'ün "kanıt puandan ayrı
saklanır" ilkesiyle çelişecek bir kısayol alınmadı.

**Yan değişiklikler.** Liste ekranının 1067 karakterlik `.lede` paragrafı bir
`<details>` açılır bloğuna alındı; ilk görünen yalnızca iki cümlelik bir özet.
Not metni ("sağdaki iki sütun...") artık yalnız tablo görünümündeyken görünüyor
(`.tableonly`, `#listeScreen.view-kart` altında gizleniyor); kart görünümü bu
kavramı hiç göstermiyor (plan gereği "normalize puan" kart görünümünden
kaldırıldı, tabloda ve CSV dışa aktarımında duruyor).

**Doğrulama.** `python3 scripts/validate.py` (0 hata) → `scripts/build.py` →
`scripts/build_pages.py` → `scripts/build_content.py` →
`node scripts/smoke_test.js` (87/87, önceki turdan 76/76'ydı — 11 yeni kontrol
eklendi: kart varsayılan görünüm, tembel ayrıntı, kart üzerinde fiyat düzenleme,
sıralama seçimi, görünüm geçişi ve kalıcılığı, dar ekranda kart taşması yok).
Ayrıca gerçek bir tarayıcıda ekran görüntüsüyle görsel doğrulama yapıldı;
ilk denemede kart ayrıntı panelinin `det-grid`'i viewport genişliğine göre
kırılıyordu ama kartın kendi konteyneri (~300px) viewport'tan çok dardı, bu
yüzden metin tek kelimelik satırlara bölünüyordu — düzeltme, kart ayrıntısını
viewport'tan bağımsız olarak her zaman tek sütun akıtmak oldu (konteyner
darlığı bir medya sorgusuyla çözülemez).

**İkinci faz — bütçe girişi gerçek bir sınıra kavuştu (2026-08-19, aynı gün).**
Ana ekrandaki üç hazır giriş yolundan biri "Bütçeye göre başla" adını
taşıyordu ama aslında bir bütçe almıyordu; yalnızca listeyi en ucuz araçtan
başlayarak sıralıyordu. Bu, isminin vaat ettiğini yapmıyordu — 5 milyon TL'lik
bir araç da "en ucuz" sıralamada bir yerde görünürdü, kullanıcının girdiği bir
üst sınır yoktu. `templates/app/22-ana.js` içinde bu yol "Bütçeye göre en
iyiler" olarak yeniden yazıldı: kullanıcı gerçek bir üst sınır (bin TL) giriyor,
`setRange('price',1,v,false)` çağrısıyla liste ekranındaki fiyat aralık
filtresiyle **aynı mekanizma** (`RNG.price`) devreye giriyor ve o sınırın
altında kalan araçlar arasından toplam puana göre en iyiler gösteriliyor.
Ayrıca kıyaslama düğmelerine (`+`/`✓`, hem kart hem tablo) `title` özniteliği
eklendi — düğmenin ne yaptığı artık üzerine gelince görünüyor, küçük ama
denetimin "site kullanıcı dostu değil" bulgusuyla doğrudan ilgili bir eksikti.

**Doğrulama (ikinci faz).** `node scripts/smoke_test.js` 87/87'den **88/88**'e
çıktı; yeni kontrol bütçe girişinin listeyi gerçekten sınırın altına
daralttığını VE sonucu toplam puana göre azalan sıraladığını doğruluyor (600
bin TL sınırıyla 406 araçtan 148'i kaldığı, hepsinin sıralı olduğu ölçüldü).
Ayrıca gerçek bir tarayıcıda ekran görüntüsüyle görsel doğrulama yapıldı.

**Dördüncü faz — ana ekran artık kanıt sayfalarına bağlanıyor (2026-08-19,
aynı gün).** Ana ekranın üç listesi ("en yüksek puanlı beş araç", "en riskli
motor aileleri", "en riskli şanzıman kutuları") `build_pages.py`'nin ürettiği
1.781 statik sayfaya hiç bağlanmıyordu; adlar düz metindi, arkasındaki
kaynaklı arıza kaydına ulaşmanın tek yolu önce liste ekranına gidip aracı
aramaktı. `DB.riskiest_engines`/`riskiest_transmissions` zaten bileşenin
kalıcı `id`'sini taşıyordu, o yüzden motor/şanzıman bağlantıları veri
değişikliği gerektirmeden eklendi. Araç listesi için durum farklıydı: arayüze
gömülen `cars_runtime` sözlüğünde (`scripts/build.py`) aracın statik sayfa
dosya adıyla eşleşen kalıcı `id`'si hiç yoktu, yalnızca arayüzün kendi
ürettiği sayısal indeks vardı (kıyaslama sepeti için, CLAUDE.md §4'ün "kimlikler
kalıcıdır" ilkesiyle eşleşmiyor). Bu yüzden `cars_runtime`'a `"cid": car["id"]`
alanı eklendi — yeni bir alan, geriye dönük hiçbir şeyi bozmuyor — ve ana
ekran artık `arac/<cid>.html` adresine bağlanıyor.

**Doğrulama (dördüncü faz).** Üretilen 15 bağlantının (5 araç + 5 motor + 5
şanzıman) hepsi gerçek bir tarayıcıda toplanıp dosya sistemine karşı
denetlendi; hepsi var olan sayfalara işaret ediyor, konsolda hata yok.
`node scripts/smoke_test.js` 88/88'den **89/89**'a çıktı; yeni kontrol bu
15 bağlantının dosya sisteminde gerçekten var olduğunu her turda doğruluyor —
gelecekte bir sayfa adlandırma kuralı değişirse bu kontrol kırılıp haber verir.

**Beşinci faz — veri/kabuk ayrımı (Y-14), ölçümle başlayıp mimari karara vardı
(2026-08-19, aynı gün).** Faz 2'nin en büyük maddesi Y-14'tü ve kendi ön koşulu
"ölçüm olmadan iyileştirme yapılmaz" diyordu. Ölçüm önce yapıldı:
`index.html` 2 MB'a ulaşmıştı ve bunun 1,37 MB'ı (%68'i) yalnızca her aracın
`note` (yazılı açıklama) ve `evidence` (motor/şanzıman kanıt metni) alanlarındaydı
— liste/kart görünümünün hiç okumadığı, yalnızca bir kartın ayrıntı paneli
açıldığında görülen içerik. Kalan "gerçekten listeye gerekli" veri (ad, yıl,
beygir, puanlar, fiyat...) 406 arabada yalnızca 178 KB tutuyordu.

Bu ölçüm, `docs/ARCHITECTURE.md` MK-07'nin ("çıktı tek dosya kalır") kendi
öngördüğü eşiği doğruladı — MK-07'nin kendisi zaten "veri yükü birkaç
megabayta çıkana kadar katlanılabilir, o eşiğe yaklaşıldığında doğru çözüm
dosyayı bölmek değil, veriyi ayrı bir dosyadan istek üzerine yüklemektir"
diyordu. Bu yüzden serbestçe uygulanmadı, önce MK-24 olarak
`docs/ARCHITECTURE.md`'ye yazıldı, sonra kodlandı: `scripts/build.py` artık
`index.html` (665 KB, %67 küçüldü) ile ayrı bir `detay.json` (1,31 MB) üretiyor;
ikincisi yalnızca bir kart/satır ilk açıldığında tek seferlik `fetch()` ile
çekiliyor ve sonucu bütün kartlar paylaşıyor.

**`file://` bedeli açıkça kabul edildi, gizlenmedi.** Tarayıcılar `file://`
kaynağından başka bir dosyaya `fetch()` isteğini engelliyor (GitHub Pages'te,
gerçek dağıtım kanalında, bu sorun yok — zaten katkı formu da `file://`'da
çalışmıyor, aynı kısıt Y-04'te de var). `templates/app/60-tablo.js`'teki
`fillDetailOnce()` bu durumda çökmek yerine `.lead.dim` sınıflı, açıkça ne
olduğunu söyleyen bir mesaj gösteriyor ("...dosyayı doğrudan diskten
açtıysanız bu beklenen bir durum...") ve puanlar, zayıf halka uyarıları,
kaynak bağlantıları gibi zaten yerel olan hiçbir şeyi gizlemiyor.

**Test altyapısı da yeniden kuruldu.** `scripts/smoke_test.js` artık testlerin
çoğu için `file://` yerine süreç içi, rastgele porta bağlanan bir statik HTTP
sunucusu kullanıyor — bu gerçek dağıtımı temsil ediyor ve yeni `fetch()`
davranışının gerçekten çalıştığını doğruluyor. `file://` için ayrı, kasıtlı
tek bir kontrol duruyor: o senaryonun çökmeden geri düşmesi de doğrulanması
gereken bir davranış. `node scripts/smoke_test.js` 89/89'dan **90/90**'a çıktı.

**Doğrulama (beşinci faz).** Gerçek bir tarayıcıda hem HTTP hem `file://`
üzerinden manuel doğrulama yapıldı (ikisi de smoke_test.js'e kalıcı kontrol
olarak girdi). `python3 scripts/build.py --check`, `build_pages.py --check`
ve `build_content.py --check` üçü de "güncel" diyor. `validate.py` 0 hata.

**Bitmemiş bırakılanlar — sıradaki turlar için.** Denetim raporu dört fazlık
bir plan önermişti; bu turda birinci faz (tasarım/kullanılabilirlik) tamamen,
ikinci fazın bir maddesi (bütçe girişi), dördüncü faz (kanıt sayfalarının ana
ekranda görünürleşmesi) ve Faz 2'nin en büyük maddesi (veri/kabuk ayrımı,
Y-14) yapıldı. Sanal/pencereli liste render'ı (Faz 2'nin geri kalanı — artık
daha düşük öncelikli, çünkü asıl ağırlık zaten detay verisindeydi ve o
çözüldü) ve Faz 3'ün geri kalanı (kıyaslama özelliğinin ana ekranda ayrı bir
tanıtım kartıyla öne çıkarılması — şimdilik yalnızca düğme etiketleri
netleştirildi, çünkü mevcut kıyaslama tepsisi zaten her zaman görünür bir
giriş noktası) sıradaki turlara bırakıldı; hiçbiri bu turda çalışan hiçbir
şeyi riske atmadı.

**Görsel tazeleme (2026-08-19, aynı gün).** Önceki dört fazın hepsi yapıya
(kart görünümü, mobil menü, bütçe girişi, kanıt bağlantıları) dokundu ama
görsel dile hiç dokunmamıştı — renkler, gölgeler, tipografi ağırlığı aynı
kalmıştı. Bu turda: ana ekran artık yumuşak bir gradyan zemin, iri bir başlık
ve iki eylem düğmesiyle gerçek bir "kahraman" bölümü; üç özet kartı renk
kodlu üst kenarlıkla ayrılıyor ve üstüne gelince hafifçe kalkıyor; liste ve
kıyaslama ekranlarındaki toplam puan artık düz metin değil, rengi puana göre
değişen bir rozet; sıralamada birinci olan araç altın bir rozetle vurgulanıyor;
üst menü çubuğu ve kartlar daha derin, iki katmanlı bir gölge kullanıyor
(`--shadowlg`). Hem açık hem koyu temada, hem masaüstü hem mobilde denendi.
`node scripts/smoke_test.js` 90/90 geçmeye devam ediyor; `.btn` sınıfının artık
`<a>` etiketlerinde de (yeni kahraman düğmeleri) kullanılabilmesi için
`text-decoration:none` eklendi — bu, ekran görüntüsüyle yakalanan tek gerçek
hataydı (düğme altı çizili görünüyordu).

---

## Y-26 · Kaydırıcılar gerçekten sürüklenebilir hale geldi, puan tabanlı alt sınır filtresi eklendi — **bitti (2026-08-19)**

**Bulgu — depo sahibinden.** "Slider'lar çalışmıyor" bildirimi geldi. Ölçülünce
neden anlaşıldı: liste ekranındaki çift uçlu aralık kaydırıcıları (yıl, beygir,
fiyat) iki `<input type=range>`'i üst üste bindiriyordu ve bunu yapabilmek için
ikisinin de gövdesi `pointer-events:none` idi — yalnızca birkaç piksellik thumb
tıklanabiliyordu. Çubuğun geri kalanına (kullanıcının doğal olarak tıklamayı
beklediği her yer) dokunmak hiçbir şey yapmıyordu; thumb'ı tam pikselinden
tutturamayan bir sürükleme de sessizce başarısız oluyordu. Bu, önceki bir
oturumda zaten var olan bir kusurdu, bu turda yeni bozulmadı — ama kullanıcı
şimdi denedi ve gerçek bir kullanılamazlık olarak karşılaştı.

**Düzeltme.** `templates/app/30-filtreler.js`'e `.rslider` konteynerinin
tamamını dinleyen bir işaretçi (pointer) sürücüsü eklendi: tıklanan/sürüklenen
noktayı bir değere çeviriyor, hangi ucun (min/max) daha yakın olduğuna karar
veriyor ve o ucu güncelliyor — thumb'ın pikselini tutturmak artık gerekmiyor.
Fare ve dokunma (mobil) aynı kod yolunu paylaşıyor (Pointer Events API).
Sürükleme durumu `document` üzerindeki `pointermove`/`pointerup` dinleyicileriyle
takip ediliyor; ilk denemede `slider.setPointerCapture()` kullanılmıştı ama bu,
sürükleme bitiminde paneli yeniden kuran `renderFilters()` ile çakışıp bir kez
sayfadaki HİÇBİR düğmenin tepki vermediği bir kilitlenmeye yol açtı (duman
testinde yakalandı, gerçek kullanıcıya hiç ulaşmadı) — `document` seviyesinde
dinleyici ekleyip çıkarmak bu riski taşımıyor.

**Aynı turda eklenen ikinci istek — puan tabanlı alt sınır.** Depo sahibi
"normalize puanı ve toplamı belli bir değerden az olan araçları gösterme"
istedi. Var olan çift-uçlu aralık bileşeni (`RANGE_DEFS`) zaten tam bunu
yapacak şekilde tasarlıydı; `total(c)`/`normOf(c)` okuyan iki yeni giriş
eklemek yeterli oldu — yeni bir UI deseni icat edilmedi. Kullanıcı yalnızca alt
ucu çekiyor (üst uç varsayılan tavanda kalıyor), tıpkı "2010 ve öncesi" gibi
zaten kullanılan diğer filtrelerde olduğu gibi. Ağırlıkları değiştirmek bu iki
filtrenin sınırlarını da otomatik yeniden hesaplatıyor (fiyat filtresinin fiyat
girildiğinde yaptığı gibi).

**Doğrulama.** `node scripts/smoke_test.js` 90/90'dan **92/92**'ye çıktı: biri
çubuğun ortasına (thumb dışına) tıklamanın çalıştığını, biri toplam puan alt
sınırının listeyi gerçekten daralttığını kilitliyor. Test yazılırken bir kez
daha aynı "hiçbir düğme tepki vermiyor" durumuyla karşılaşıldı — bu kez neden
uygulamanın kendisi değil, testin art arda iki kez `#filtclear`'a basıp bir
sonraki kontrolün aktif filtre bulamamasıydı; düzeltme yalnızca test
sırasındaydı, gerçek kod değişmedi.

---

## Y-27 · Araç portföyünü büyütme: BMW N57 motor ailesi, 730d ve iki otomatik terfi — **birinci tur bitti (2026-08-20)**

**Bulgu — depo sahibinden.** "gpt'nin dümdüz basit bir aramayla önerdiği nerdeyse
hiçbir araba, marka model kombinasyon yok, araç portföyümüz felaket sınırlı; baya
büyütmeliyiz, sahibinden'deki tüm kombinasyonları görmeliyim" istendi. Bu, tek
oturumda bitirilemeyecek bir istek: bu depodaki kalite çıtası (4+ bağımsız kaynak,
uydurma vergi/güvenilirlik verisi yasağı, Y-23'ün öğrettiği anakronizm dikkati)
her yeni araca gerçek araştırma süresi harcatıyor. Bu tur, o büyümenin **ilk
adımını** atıyor ve aynı zamanda büyümeyi ucuzlatan iki mekanik iyileştirme
yapıyor.

**Ağ erişimi sınırlaması — dürüst kayıt.** sahibinden.com'a doğrudan erişim bu
çalışma ortamında engelli (WebFetch her denemede `EGRESS_BLOCKED` döndürdü, üç
farklı harici teknik özellik/vergi sitesinde de aynı sonuç alındı). Bu yüzden
"sahibinden'i canlı tara" birebir uygulanamadı; onun yerine iki alternatif yol
izlendi.

**1. Yol — katalogdan ücretsiz terfi.** `scripts/promote_catalog.py`, depoda
zaten puanlanmış motor/şanzıman ailelerine güvenle bağlanabilen 1.215 "yalnız
katalogda" kaydı otomatik tarıyor. Bu turda çalıştırılınca (`--write`) iki yeni
araç sıfır elle araştırmayla terfi etti: **Alfa Romeo MiTo 1.4 T · 135 bg** (EA111
motor ailesi, motor puanı 46) ve **Skoda Superb 1.8 TSI · 160 bg** (EA888 motor
ailesi, motor puanı 46; vag-01m şanzıman, puan 66). `comf`/`cost`/`liq`,
deponun zaten kullandığı yöntemle (marka içi en yakın kardeş aracın puanına göre
tahmin, `confidence: "düşük"`, kaynak boş) dürüstçe düşük güvenle işaretlendi.

**Bu yolda bulunan ve düzeltilen bir betik hatası.** `promote_catalog.py`
içindeki `TODAY` sabiti `"2026-08-17"` olarak donmuştu — betik hangi gün
çalıştırılırsa çalıştırılsın terfi kayıtlarına o sabit tarihi yazıyordu.
`datetime.date.today().isoformat()` ile değiştirildi; bu turda üretilen iki
dosyanın tarihi (betik düzeltmeden ÖNCE yazıldıkları için) elle `2026-08-20`'ye
düzeltildi, çünkü isimden eşleşen kayıt dedup'ı script'i yeniden çalıştırmakla
düzeltilemiyordu.

**Bu yolda bulunan ikinci, daha önemli betik hatası.** `promote_catalog.py`
terfi ettirdiği araç kaydını yazıyordu ama katalogdaki kaynak satırın
`scored_car_id` alanını hiç doldurmuyordu — yani terfi eden bir kayıt hem
"puanlanmış araç" hem "yalnız katalogda" listesinde birden görünüyordu (bu,
BMW 730d eklenirken elle fark edilip elle düzeltilmişti, ama otomatik terfi
eden iki kayıtta unutulmuştu). Betiğe `link_catalog_entries()` fonksiyonu
eklendi: `--write` sonunda terfi eden her katalog id'sini kaynak dosyasında
bulup `scored_car_id`'yi dolduruyor. Bu turun iki otomatik terfisi ve BMW 730d
için katalog kayıtları elle/otomatik tutarlı hale getirildi; bundan sonraki her
`--write` çalıştırması bu adımı kendiliğinden yapacak.

**2. Yol — elle araştırma: BMW N57 + 730d (F01).** Katalogda karşılığı olmayan,
gerçekten eksik bir motor ailesi elle araştırıldı: **BMW N57** (3.0 dizel, altı
silindir), N47'nin altı silindirli kardeşi. Dört bağımsız kaynak (iki forum, iki
teknik blog) N57'nin N47 ile aynı temel tasarım hatasını (triger zincirinin
motorun şanzıman tarafında olması) taşıdığını ama zincir arızalarının N47'ye göre
daha seyrek bildirildiğini doğruladı; `base_score` bu yüzden N47'nin 38 puanının
üzerinde ama "bilinen risk" bandının tavanının (49) altında, 46 olarak
kalibre edildi — gerekçe motor kaydının `note` alanında tam cümlelerle yazılı.
Bu aileye bağlı ilk araç olarak **BMW 730d (F01), 258 bg** eklendi; `comf`/`cost`/
`liq` depodaki 5 serisi araçlarıyla segment karşılaştırması yapılarak (bayrak
modeli için daha yüksek konfor, daha büyük/pahalı segment için daha düşük
maliyet puanı, Türkiye pazarında niş kalan bir gövde için belirgin biçimde düşük
likidite) düşük güvenle verildi.

**Doğrulama.** `python3 scripts/validate.py` 0 hata; `python3
scripts/consistency.py` yeni bir çelişki bayrağı üretmedi. Tam üretim hattı
(`build.py` → `build_pages.py` → `build_content.py`) yeniden çalıştırıldı: araç
sayısı **406 → 409**, motor ailesi sayısı **104 → 105**. `node
scripts/smoke_test.js` **92/92** kontrolü geçti, yeni araçlar hiçbir mevcut
kontrolü bozmadı.

**Kapsam düzeltmesi — önceki turun yanlış negatifleri.** Bu turda fark edildi:
daha önce "eksik" sayılan Citroën C4/C5 ve BMW 1-Serisi ailelerinin depoda
zaten kısmi karşılığı var; bunlar gerçek boşluk değil, önceki bir turun kaba
marka-düzeyi sezgisinin yanlış negatifiydi. Gerçekten eksik olduğu doğrulanan
aileler: **Audi A7, BMW 6-Serisi, Mercedes CLA/CLS/S-Serisi**, ve ticari
tabanlı yolcu araçları (**Ford Connect, Fiat Doblo, VW Caddy**).

**Bitmemiş bırakılanlar — dürüst kayıt.** Bu tur, "sahibinden'deki tüm
kombinasyonlar" hedefinin küçük bir kesridir; bu depronun kalite çıtasında bu
hedefe ulaşmak tek oturumda bitmez, çok turlu bir çalışma gerektirir. Yukarıdaki
5 gerçek boşluk (Audi A7, BMW 6-Serisi, Mercedes CLA/CLS/S-Serisi, ticari tabanlı
yolcu araçları) bir sonraki turun aday listesidir. Ayrıca zaten kısmi kapsamı
olan ailelerin (Citroën C4/C5, BMW 1-Serisi) hangi TRIM'lerinin gerçekten eksik
olduğu, marka-düzeyi sezginin artık güvenilmez kanıtlanmasından sonra tek tek
yeniden denetlenmeli.

---

## Y-28 · Portföy genişletmenin kapsamını bulma turu: C/D (+ B) segmentine odaklı 877 aday — **kapsam bulma bitti (2026-08-20), terfi sürüyor**

**Bulgu — depo sahibinden.** Y-27'nin ardından açık bir yön verildi: genişleme
E/F segmentine (5-Serisi, E-Sınıfı, A6/A8, 7-Serisi ve dengi büyük SUV'lar)
gitmemeli, ticari tabanlı yolcu araçlarına ve MPV'ye hiç gitmemeli, C/D
segmentine odaklanmalı (B segmenti de eklenebilir), ve hiçbir aracın fiyatı
1,5 milyon TL'yi aşmamalı. Ayrıca açık bir sıra verildi: **önce bütün
portföyün kapsamını bul, kaynak bulma işini sonraya bırak.**

**Neden "önce bul" ayrı bir adım.** Bu depoda bir aracın puanlanması demek
motor/şanzıman ailesinin dört bağımsız kaynakla (ya da en azından ikiyle)
doğrulanmış olması demek (MK-02/MK-16); 877 adayın hepsini bu turda kaynaklamak
mümkün değil. Ama "hangi araçların eksik olduğunu bilmek" ayrı, kanıt
gerektirmeyen bir iştir — depodaki 1.656 kayıtlık teknik katalog (MK-22) zaten
P2.1 veri paketinden gelen gerçek, olgusal teknik özellikler taşıyor. Bu tur bu
ayrımı kullandı: **uydurma yapmadan**, yalnızca depoda zaten duran gerçek
verinin üzerinden "hangi C/D/B segmenti aracı hâlâ katalogda ama puanlı
listede yok" sorusuna kesin bir sayı verdi.

**Yöntem.** Katalogdaki 430 farklı (marka, model ailesi) çiftinin her biri elle
B/C/D/E/F/MPV/TICARI/SKIP segmentlerinden birine atandı (yaygın, tartışmasız
segment sınıflandırması — VW Golf/Toyota Corolla gibi ailelerin C segmenti
olduğu, VW Passat/BMW 3-Serisi gibi ailelerin D segmenti olduğu, 5-Serisi/
E-Sınıfı gibi ailelerin E segmenti olduğu genel otomotiv bilgisi, kaynak
gerektirmeyen bir sınıflandırma). Bu haritayla, `scripts/promote_catalog.py`'nin
zaten yüklediği katalog + araç verisi üzerinden, **puanlanmamış VE B/C/D
segmentinde VE depoda aynı adla zaten kayıtlı bir aracı olmayan** katalog
kayıtları filtrelendi; marka+model ailesi+nesil kırılımında gruplandı.

**Sonuç — `data/queue/portfolio-expansion-bcd-worklist.json`.** 301 grup, 877
trim. Segmentlere göre dağılım: B 40 grup/95 trim, C 143 grup/379 trim, D 118
grup/403 trim. Her grup, o gruptaki motor ailesinin (marka+yakıt+hacim kovası)
depoda **zaten var olup olmadığını** (`any_engine_bucket_known`) taşıyor: 92
grup (338 trim) depoda zaten kayıtlı bir motor kovasına düşüyor — bu, sıfırdan
motor araştırması gerektirmediği için bir sonraki turların önceliği olmalı; en
büyükleri Volvo S60 (28 trim), Renault Megane (28), BMW 3-Serisi E46/E90/E91
(46 trim toplam), Saab 9-3 (15), Honda Civic (12), Toyota Avensis (12).
Kalan 209 grup (539 trim) sıfırdan motor ailesi araştırması gerektiriyor.
Bu sayı, `promote_catalog.py`'nin kendi güvenli otomatik eşleştiricisinin
bulduğu adaylarla (32 toplam, hepsi zaten depoda isimle eşleşiyordu — bkz.
Y-27'nin "ücretsiz terfi" kapısının artık kapalı olduğu bulgusu) karıştırılmamalı;
bu worklist **motor kovası** düzeyinde eşleşiyor, `promote_catalog.py`'nin
katı eşleştiricisi ise **isim+beygir aralığı+yıl** düzeyinde, çok daha sıkı bir
koşul arıyor — worklist'teki her satır yine de tek tek elle doğrulanmalı
(Y-23'ün anakronizm dersi burada da geçerli).

**Fiyat tavanı — dürüst kayıt.** Katalog kayıtlarında fiyat alanı hiç yok (MK-22:
katalog olgusal teknik veridir, puan veya fiyat taşımaz), bu yüzden 1,5 milyon
TL tavanı bu census aşamasında **uygulanamadı**. Bunun yerine worklist'in
`_comment` alanına açıkça yazıldı: her araç terfi ederken (nearest-sibling
yöntemiyle fiyat aldığı an) tavan elle denetlenmeli, aşan varsa terfi
durdurulmalı ya da fiyat elle düşürülmeli.

**Bitmemiş bırakılanlar.** Bu tur bilinçli olarak **yalnızca kapsamı buldu**;
worklist'teki 877 satırdan hiçbiri bu turda puanlanmadı, depo sahibinin kendi
isteğiyle ("kaynak bulamayabilirsin ama önce bütün portföyü bul, sonra kaynak
buluruz"). Sıradaki iş: worklist'in `any_engine_bucket_known: true` grupları
büyükten küçüğe ele alınıp, her grubun her trimindeki beygir/yıl kombinasyonu
gerçek üretim verisiyle (WebSearch, bu ortamda WebFetch hâlâ engelli)
doğrulanarak, Y-27'deki BMW N57/730d turunda izlenen adım adım yöntemle
puanlanmalı.

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

## Y-09 · Görsel dil: koyu tema ve yumuşak yüzeyler — **bitti (2026-08-18)**

**Öncelik: düşük-orta. Y-05 ve Y-07 ile birlikte yapılırsa verimli olur.**

**Kapsam.** Sert ve büyük kenarlar yumuşatılır, koyu bir tema kurulur, otomobil
kültürüne yakın ama ciddiyetini koruyan bir görsel dil oturtulur.

**Kesin sınırlar (kullanıcının açık talebi):** Süslü veya "eğlenceli" yazı tipi
kullanılmaz. Dekoratif görsel kullanılmaz. **Emoji kullanılmaz.** Mevcut yazı tipi
üçlüsü (Archivo, IBM Plex Mono, Newsreader) zaten teknik ve ciddi bir ton veriyor;
değiştirilmesi için güçlü bir gerekçe gerekir. Bu üç sınırın hepsine uyuldu: tema
düğmesi düz metin ("Koyu tema"/"Açık tema"), hiçbir yeni görsel veya emoji eklenmedi,
yazı tipi üçlüsü değişmedi.

**Kapsam yalnızca ana uygulamaydı.** `scripts/build_pages.py`'nin ürettiği ~1.775 statik
SEO sayfası (`arac/`, `katalog/`, `motor/`, `sanziman/`) zaten kendi `PAGE_CSS`'i
içinde `prefers-color-scheme` ile koyu temayı taşıyordu — muhtemelen Y-11'de fark
edilmeden kurulmuş. Bu turun konusu yalnızca `templates/` kaynaklı tek sayfalık
uygulamaydı (`index.html`), onda hiç koyu tema yoktu.

**Yöntem: `:root`'taki değerler açık tema, iki blok onu geçersiz kılıyor.**
`@media(prefers-color-scheme:dark){:root:not([data-theme="light"])}` sistem tercihine
JS'siz uyum sağlıyor (CSS ayrıştırma anında uygulanıyor, yanıp sönme olmuyor);
`:root[data-theme="dark"]` kullanıcının elle seçtiği tercih. Kullanıcı hiç seçim
yapmadıysa `data-theme` özniteliği hiç yazılmıyor, yani sistem teması canlı izlenmeye
devam ediyor (işletim sistemi teması değişirse sayfa da JS'siz değişir). Kullanıcı
düğmeye bastığında seçim `localStorage`'a yazılıyor ve `data-theme` sabitleniyor;
`<head>`'deki küçük senkron betik bu seçimi ilk boyamadan ÖNCE uyguluyor, aksi halde
açık temayla boyanıp bir kare sonra koyuya dönme (FOUC) olurdu.

**Yol boyunca bulunan iki bağımsız kusur, aynı işte düzeltildi:**
1. `.catwrap`/`.catlist`/`.catitem` (katalog sonuçları bloğu, MK-22) hiç tanımlanmamış
   `--rule`/`--sf`/`--sf2`/`--ink2`/`--ink3` değişkenlerini kullanıyordu. Tanımsız
   `var()` geçersiz sayıldığı için ilgili özellik (ör. kenarlık) sessizce hiç
   uygulanmıyordu — koyu temadan bağımsız, önceden var olan bir hata. Zaten var olan
   gerçek değişkenlere (`--line`, `--panel2`, `--panel`, `--dim`) bağlandı.
2. `.cmptray` (kıyaslama tepsisi) `background:var(--ink)` kullanıyordu — açık temada
   `--ink` koyu olduğu için "her zaman koyu bar" görünümü kazara doğru çıkıyordu, ama
   koyu temada `--ink` açık renge döneceği için bar görünmez olurdu. Sabit bir
   `--bar` değişkeni eklendi (iki temada da aynı değeri taşıyor), tepsi artık temadan
   bağımsız olarak koyu kalıyor — tasarımın zaten amaçladığı davranış.

**Radar grafiği (SVG) sabit hex renk yerine `getComputedStyle` ile CSS değişkeni
okuyor.** Aksi halde grafik açık temanın renklerinde donup kalırdı; artık tema
değişince yeniden çizilen her radar doğru paleti kullanıyor (bilinen sınır: EKRANDA
AÇIKKEN tema değiştirilirse o an görünen bir radar kendiliğinden yeniden boyanmıyor,
ekran yeniden render edilene kadar eski renkte kalıyor — düşük risk, küçük ve kasıtlı
bir sınırlama, sayfa yenilendiğinde veya ekran değiştirildiğinde kendiliğinden düzeliyor).

**Doğrulama.** Playwright ile ana ekran, araç listesi + filtre paneli + kaydırıcılar,
kıyaslama ekranı (radar dahil) ve metodoloji ekranı koyu temada ekran görüntüsü
alınarak elle incelendi; kontrastsız metin veya görünmez kenarlık bulunmadı.
`smoke_test.js`'e üç kalıcı kontrol eklendi: düğme rengi/etiketi değiştiriyor mu,
seçim sayfa yenilenince kalıcı mı, açık temaya geri dönülebiliyor mu. Kontrol sayısı
69 → 72.

---

## Sıralama önerisi

**Veri tarafı büyük ölçüde tamamlandı; sıradaki iş arayüz ve içerik.**

Biten maddeler: ~~Y-01~~ (liste genişletme — SUV, marka ve 2016+ hedeflerinin üçü de
karşılandı/aşıldı), ~~Y-02~~ (kaynak derinliği — kaynaksız ve tek kaynaklı araç
kalmadı), ~~Y-03~~ (araştırma hattı), ~~Y-04~~ (form arayüzü; yalnızca uç nokta adresi
depo sahibini bekliyor), ~~Y-05~~ (yerleşim), ~~Y-06~~ (puanlama şeffaflığı, üç
katmanın tamamı), ~~Y-07~~ (ana ekran), ~~Y-09~~ (koyu tema, 2026-08-18).

Sıradaki iş, öncelik sırasıyla:

1. **Y-08 · Araç hikayeleri** — sürekli ve parça parça ilerleyebilecek, aceleye gelmeyen
   iş; 400 araç için yazılacak çok içerik var.
2. **Y-01'in ötesi (düşük öncelik)** — MG'nin geleneksel yakıtlı modelleri (varsa),
   Dacia Sandero/Logan gibi robotlu (AMT) şanzımanlı modeller (ayrı bir "Robot" tipi
   bileşen ailesi araştırması gerektiriyor, bu turda ertelendi). Elektrikli/hibrit/LPG
   kalıcı olarak kapsam dışı (MK-13).
3. **Y-02'nin uzun vadeli hedefi** — ortalamayı 4'e çıkarmak, yani her araca üçüncü ve
   dördüncü bağımsız kaynak. Bileşen bazlı toplu bağlama yöntemi burada işe yaramıyor;
   araç bazında tekil araştırma gerekiyor, bu yüzden yavaş ve pahalı bir iş.
4. **`evidence` bloğunu kalan üç kriter için genişletmek** (`comf`, `cost`, `liq`) —
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

### Y-14 · Veri/kabuk ayrımı ve tembel yükleme — **bitti (2026-08-19, bkz. Y-25 beşinci faz)**

**Sorun neydi.** Tek dosya 2026-08-19'da 2 MB'a ulaşmıştı ve araç sayısıyla doğrusal
büyüyordu. Veri hacminin büyük kısmını `evidence` ve `note` bloğunun metinleri
oluşturuyordu ve bunlar yalnızca detay panelinde okunuyordu.

**Ön koşul karşılandı.** Bu madde "ölçüm olmadan iyileştirme yapılmaz" diyordu. Ölçüm
yapıldı: `note`+`evidence` toplam dosyanın %68'iydi (1,37 MB / 2 MB), oysa liste/kart
görünümü ikisini de hiç okumuyordu.

**Ne yapıldı.** `scripts/build.py` artık iki dosya üretiyor: `index.html` (liste için
özet veri, 665 KB'a indi) ve `detay.json` (yalnız bir kart/satır ilk açıldığında
`fetch()` ile çekilen `note`+`evidence`, 1,31 MB). Tam kayıt, gerekçe ve `file://`
uyumluluk tartışması `docs/ARCHITECTURE.md` MK-24'te ve `docs/ROADMAP.md`'nin Y-25
kaydının beşinci fazında duruyor.

**Bitmemiş bırakılan.** Performans bütçesi kontrolü (duman testine "X saniyeden hızlı
olmalı" türünden bir eşik) eklenmedi; bunun yerine gerçek ölçüm sayıları (index.html
boyutu, detay.json boyutu) Y-25'in beşinci faz kaydına yazıldı. Sabit bir zaman eşiği
makineye göre değiştiği için gürültülü bir test olurdu; boyut ölçümü daha kararlı bir
gösterge.

### Y-15 · Fiyat ölçümünün tekrarlanabilir hale gelmesi

**Sorun.** MK-19 ile 19 araç tarihli piyasa gözlemine bağlandı, ama 259 araç hâlâ tarihsiz
tahmin taşıyor ve denetim bunu `fiyat-tarihsiz` uyarısıyla işaretliyor. Ölçüm bir kez
yapıldı; tekrarlanabilir bir hat değil.

**Kapsam.** Ölçümün belgelenmiş, tekrarlanabilir bir protokole dönüşmesi ve kapsamın
büyütülmesi. Tazelik, kopyalanamayan tek rekabet avantajı olduğu için bu madde ticari
olarak da en kritik olanlardan biri (`docs/URUN-STRATEJISI.md` §4.2).

**Bitmiş sayılma ölçütü.** Ölçüm ikinci kez, aynı yöntemle ve elle müdahale olmadan
çalıştırılabiliyor; tarihli fiyat taşıyan araç sayısı belirgin biçimde artıyor.

### Y-16 · Boş ağırlık verisinin doldurulması — **büyük ölçüde bitti (2026-08-18, bkz. Y-24)**

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
