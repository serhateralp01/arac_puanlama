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

## Durum özeti (son güncelleme: 2026-08-07)

| Katman | Durum |
|---|---|
| Veri mimarisi (araç / motor / şanzıman / kaynak ayrımı) | Tamamlandı |
| Şanzıman kutusu kayıtları | 45 kutu (`data/transmissions.json`), çoğu temel puanlı ve kaynaklı |
| Motor ailesi kayıtları | 81 aile (`data/engines.json`), çoğu temel puanlı ve kaynaklı |
| Denetim hattı (`validate.py`, `consistency.py`, `smoke_test.js`) | Çalışıyor, 0 hata, 37/37 duman testi |
| Çok ekranlı arayüz: ana ekran, giriş akışı, liste, metodoloji, kaynak öner, iletişim | Çalışıyor |
| GitHub Pages yayını | Çıktı `index.html` olarak üretiliyor, kök adres siteyi açıyor |
| Liste ekranı denetim çubuğu (Y-05) | Tamamlandı: ağırlık/arama/filtre tablonun üstünde, filtre paneli katlanabilir |
| Kaynak öneri formu (Y-04) | Arayüz tamamlandı; gönderim uç noktası ve iletişim adresi tanımlanmayı bekliyor |
| Ana ekran (Y-07) | Tamamlandı: veri kapsamı özeti, hazır giriş yolları, en riskli bileşenler |
| Araştırma kuyruğu (Y-03) | Tamamlandı: `data/queue/`, şema, iki aşamalı akış, bir tur uçtan uca çalıştırıldı |
| Kaynak derinliği (Y-02) | **Kaynaksız araç yok, tek kaynaklı araç yok**; MK-16 mekanik miras turundan sonra 177/249 araç "doğrulanmış" (4+ kaynak), ortalama 4.31 |
| Araç listesi (Y-01) | 154 → 245 araç. Birinci dalgada **SUV 1 → 30 (hedefi aştı), marka 5/5 (hedefe ulaştı), 2016+ 5 → 42 (hedefi (40) aştı)**; ikinci dalga 300-900 bin TL bandında marka-model-motor-şanzıman çeşitliliğini artırıyor, 80-90 kombinasyon hedefinin bir kısmı karşılandı, sürüyor |
| Kapsam sınırı | **Elektrikli, hibrit ve LPG'li araçlar kalıcı olarak kapsam dışı (MK-13)** |
| Puanlama şeffaflığı (Y-06) | **Bitti.** Bilimsel temel, kanıt zinciri, arayüz katmanı (kriter paneli artık liste ekranında, "neden bu puan" dökümü) tamamlandı |
| Görsel dil / ürün hissi | Ham, iş odaklı |

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

**Sonuç (iki turun toplamı).** Araç sayısı 228 → 245 (17 yeni araç), motor ailesi
sayısı ve şanzıman kutusu sayısı arttı. `validate.py` her turdan sonra 0 hata ile
tamamlandı, `smoke_test.js` 49/49 kontrolü geçiyor.

**Kalan iş — hedeften uzak.** Kullanıcının koyduğu 80-90 kombinasyon hedefinin
yalnızca beşte biri kadarı karşılandı. Renault Symbol/Thalia (1.6L 16V 4AT, kutu
tedarikçisi doğrulanamadı) ve Renault Fluence (CVT, tedarikçi doğrulanamadı) hâlâ
araştırılmayı bekliyor; `/tmp` önbelleğindeki 550 satırlık aday listesinden (bkz.
oturum notları) daha fazla bütçe segmenti adayı (300-900 bin TL) taranmadan kaldı.
Sıradaki tur bu adaylardan devam etmeli.

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

**Kalan iş.** 72 araç hâlâ "kısmi kaynak" — bunların çoğu bağlı olduğu motor/şanzıman
ailesinin de az kaynaklı olduğu (1-2 kaynak) durumlar, yani mekanik mirasın tavan
yaptığı yerler. Buradan sonrası tekrar elle, araç veya bileşen bazlı gerçek araştırma
gerektiriyor.

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
5. **`evidence` bloğunu kalan beş kriter için genişletmek** (`fun`, `comf`, `age`,
   `cost`, `liq`, `price`) — bunların çoğu `docs/ARCHITECTURE.md` MK-06'nın hâlâ
   uygulanmamış `kerb_weight_kg`/`torque_nm`/`fuel_consumption_l_100km` formülüne
   bağlı olduğu için önce o veri işi gerekiyor.

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
