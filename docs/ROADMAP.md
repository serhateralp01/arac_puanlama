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

## Durum özeti (son güncelleme: 2026-08-06)

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
| Kaynaksız araçlar (Y-02) | Kaynaksız araç yok; araç başına ortalama kaynak hâlâ hedefin (2.5) altında ve düşüyor, 1.71 |
| Araç listesi (Y-01) | Başlandı: 154 → 199 araç, 2016+ 5 → 27, SUV 1 → 18, 4 yeni marka (Dacia, Jeep, MINI, Cupra); üçüncü tur mevcut modellerin motor çeşitliliğini derinleştirdi |
| **Kaynak derinliği** | **Zayıf, ama iyileşiyor — kuyruk artık çalışır durumda** |
| **Araç kapsamı** | **Hâlâ dar ama genişliyor — 2016+ ve SUV hedeflerinin çoğu önümüzde** |
| Görsel dil / ürün hissi | Ham, iş odaklı |

Denetimin bugünkü çıktısı: **0 hata, 230 uyarı**. Uyarıların ezici çoğunluğu (191) tek
bir kalemden geliyor: araçların dört bağımsız kaynağa ulaşmamış olması. Kuyruk artık
kurulduğu için bu sayı, tek tek araç dosyası düzenlemek yerine kuyruğu tekrar tekrar
çalıştırarak düşürülebilir.

---

## Y-01 · Araç listesini genişlet ve kapsamı dengele — **başlandı**

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
`docs/Y01B-MOTOR-CESITLENDIRME.md`'deki 🟡/🔴 etiketli satırlar (Golf 7 GTI, W211 E280,
Megane 3 1.2 TCe, Clio 4 TCe, Laguna 1.9 dCi, Peugeot 308 PureTech, Opel Insignia 2.0
Turbo, Opel Astra 1.7 CDTI) hâlâ işlenmedi, her biri yeni bir motor ailesi gerektiriyor.

**Kalan iş — hedeflerin çoğu hâlâ karşılanmadı.** Bitmiş sayılma ölçütü (2016 sonrası
≥ 40, SUV ≥ 25, eksik markalardan en az 5 temsil) şu an marka kısmında neredeyse tam
(Dacia + Jeep + MINI + Cupra = 4, hedef 5 — bir marka daha eklenince bu madde de
biter). Sırada:

1. **Düşük riskli devam:** `docs/Y01-HEDEF-LISTE.md`'deki "Ertelenenler" bölümü
   (Kia Ceed SW hemen, sonra T-Roc/Polo/C-HR/CX-5/Focus4/MINI F56 için yeni bileşen
   araştırması) ve `docs/Y01B-MOTOR-CESITLENDIRME.md`'deki 🟡/🔴 satırlar. C5 Aircross
   ve 3008/Grandland X ailesi için depoda hâlâ 3 yetim kaynak (`araclo_c5aircross`,
   `erenservis_eat8`, `motor1_psa_suv_eat`) bekliyor.
2. **C bölümü (Subaru, MG)** — tamamen yeni bileşen ailesi zinciri gerektiriyor,
   kullanıcı onayı bekliyor.
3. Hibrit/elektrikli araçlar (Lexus, Togg, MG'nin EV/PHEV modelleri) için önce bir
   şema kararı gerekiyor: `fuel` alanı bugün yalnızca `Dizel` / `Benzin` kabul ediyor.
   Bu, geri alınması pahalı bir karar olduğu için `docs/ARCHITECTURE.md`'ye MK kaydı
   olarak yazılmadan araç eklenmemeli.

**Bitmiş sayılma ölçütü (henüz karşılanmadı).** 2016 sonrası araç sayısı en az 40,
SUV sayısı en az 25, listede hiç bulunmayan yaygın markalardan en az beşi temsil
edilmiş (şu an 4/5) ve `validate.py` hâlâ 0 hata veriyor.

---

## Y-02 · Her aracın en az bir gerçek kaynağı olsun, ortalama dörde yaklaşsın — **kısmen bitti**

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

**Bugünkü tablo** (Y-01'in üçüncü turundan sonra, 199 araç üzerinden):

| Kaynak sayısı | Araç | Durum |
|---:|---:|---|
| 0 | 0 | — kalmadı |
| 1 | 97 | Tek kaynak çürürse dayanaksız kalır |
| 2-3 | 94 | Kısmi |
| 4+ | 8 | Doğrulanmış |

Ortalama kaynak 1.87 → 1.80 → 1.71 **gerilemeye devam ediyor** — bu bir gerileme
değil, aritmetik bir sonuç: Y-01'in ikinci ve üçüncü turlarında eklenen 39 aracın
(18 + 21) çoğu tek kaynakla açıldı, kaynaksız başlamamaları önceliklendirildi, bu da
paydayı büyütüp ortalamayı aşağı çekti. Bu artık kalıcı bir örüntü haline geldi;
Y-02'nin hedefine (2.5) ulaşmak için liste büyümesi bir noktada durup tek kaynaklı
araçlara (şimdi 97 tane) ikinci kaynak bulma turuna geçilmeli — aksi hâlde her yeni
araç turu ortalamayı yeniden düşürmeye devam edecek.

Araç başına ortalama kaynak **1.79 → 1.88**'e çıktı. Hedefin (2.5) altında; **kalan iş**
bu 14 aracı ve tek kaynaklı diğer 43 aracı ikinci, bağımsız bir kaynağa daha bağlamak.
Sıradaki oturum bunu doğrudan Y-03'teki kuyruğu tekrar çalıştırarak yapabilir.

**Önemli ayrım.** Motor ve şanzıman ailelerine verilen kaynaklar araç kaydına otomatik
yansımıyor; bunlar ayrı bağlantılar. Bir aracın kendi kaydında da o araca özgü kanıt
olmalı — kullanıcı yorumu, o modele özel arıza derlemesi, Türkiye'ye özgü bir şikayet
örüntüsü. Kullanıcının istediği "her araç için en az bir yorum kapsanmalı" şartı tam
olarak budur; bu turda eklenen 14 kaynağın hepsi bu türden.

**Bitmiş sayılma ölçütü (henüz karşılanmadı).** Araç başına ortalama kaynak 2.5'in
üstünde. Kaynaksız araç sayısı sıfıra indi, bu madde karşılandı.

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

## Y-06 · Puanlama şeffaflığı: her kriterin ağırlığı ne yapıyor, fiyat nasıl hesaplanıyor

**Öncelik: orta-yüksek.** Kullanıcının en net şikayeti buydu: "fiyat kısmı çok kafa
karıştırıcı, kriterin puanı nasıl etkilediğini bilmiyoruz."

**Bugünkü durum ve neden kafa karıştırıcı olduğu.** Fiyat, diğer yedi kriterden
yapısal olarak farklı çalışıyor ama arayüzde aynı görünüyor:

- Diğer kriterlerin puanı araç kaydında sabit durur ve kanıta dayanır.
- Fiyat puanı **hiçbir yerde saklanmaz**; listenin tamamına göre her yeniden çizimde
  hesaplanır: `100 × (en_pahalı_orta − aracın_ortası) / (en_pahalı_orta − en_ucuz_orta)`.
- Yani bir aracın fiyat puanı, **listedeki diğer araçlar değiştiğinde değişir**. Filtre
  uygulandığında ya da fiyat aralığı elle düzenlendiğinde bu puan kayar.

Bu davranış doğru ama görünmez, ve görünmediği için kafa karıştırıyor.

**Kapsam.**

1. `#metodoloji` ekranı kriter kriter genişletilir. Her kriter için: ne ölçüyor, ne
   ölçmüyor, puan bantları, hangi kanıt türünü istiyor, varsayılan ağırlığı ne ve o
   ağırlık neden o.
2. Fiyat kriterine ayrı ve açık bir bölüm: neden saklanmadığı, filtreye göre neden
   değiştiği, elle fiyat düzenlemenin toplam puanı nasıl etkilediği.
3. Ağırlık kutularının yanına, o kriterin toplam puandaki **fiili katkısını** gösteren
   canlı bir gösterge. Kullanıcı bir ağırlığı değiştirdiğinde etkisini tabloya bakmadan
   görebilmeli.
4. Araç detay panelinde "bu araç neden bu puanı aldı" dökümü: her kriterin puanı,
   ağırlığı ve toplama katkısı.

**Bitmiş sayılma ölçütü.** Bir kullanıcı, bir aracın toplam puanının hangi sayılardan
oluştuğunu arayüzden takip edebiliyor ve fiyat puanının neden değiştiğini
açıklayabiliyor.

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

Maddeler birbirine bağımlı; şu sıra hem riski hem tekrarı azaltır. **Y-03, Y-04, Y-05 ve
Y-07 bitti; Y-02 ve Y-01 kısmen bitti / başlandı** (aşağıda işaretli); geri kalanlar
için sıra hâlâ geçerli.

1. ~~**Y-03** (araştırma hattı)~~ — **bitti.**
2. **Y-02** (kaynaksız araçları kapat) — **kısmen bitti:** kaynaksız 14 araç kapandı,
   ortalama kaynak hâlâ hedefin altında. Sıradaki iş: kuyruğu (Y-03) tekrar çalıştırıp
   tek kaynaklı araçlara (şimdi ~59 tane, altısı bu turda eklenen yeni araçlar dahil)
   ikinci bir kaynak bulmak.
3. **Y-01** (listeyi genişlet) — **başlandı:** altı araç, ikisi yeni marka (Dacia,
   Jeep), dördü SUV/2016 sonrası; hepsi mevcut bileşen ailelerine bağlandı. Sıradaki
   iş: `data/queue/` içindeki 6 kalan yetim kaynağın işaret ettiği Citroën C5
   Aircross / Peugeot 3008 / Opel Grandland X için önce yeni motor/şanzıman ailesi
   açmak (1.5 BlueHDi, EAT8), sonra araçları bağlamak.
4. ~~**Y-05 + Y-06** (yerleşim ve şeffaflık)~~ — **Y-05 bitti.** Y-06 (puanlama
   şeffaflığı) hâlâ sırada, küçük ve bağımsız.
5. ~~**Y-04** (form)~~ — **arayüz kısmı bitti;** gönderim uç noktası ve iletişim
   adresi tanımlanmayı bekliyor, bu adım depo sahibine ait.
6. ~~**Y-07**~~ + **Y-09** (ana ekran ve tema) — **Y-07 bitti.** Y-09 (koyu tema) hâlâ
   sırada.
7. **Y-08** (hikayeler) — sürekli ve parça parça ilerleyebilecek, aceleye gelmeyen iş.

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
