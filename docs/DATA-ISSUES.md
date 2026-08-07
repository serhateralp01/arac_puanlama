# Bilinen veri sorunları

Bu belge, göç sırasında ve ilk denetimlerde bulunan veri sorunlarını kaydeder. Her
madde ya düzeltilerek ya da bilinçli bir istisna olarak kabul edilerek kapatılır.
`scripts/validate.py` çıktısı bu listenin canlı halidir; buradaki kayıtlar ise o
çıktının arkasındaki bağlamı ve verilen kararların gerekçesini saklar.

---

## D-01 · İki araçta fazladan puan değeri (DÜZELTİLDİ — veri kaybıyla)

Bu madde kapatıldı, ancak alınan kararın kaydedilmesi gerekiyor.

Eski HTML dosyasında iki aracın puan dizisi yedi yerine dokuz elemanlıydı:

| Araç | Dizi | Kullanılan | Sessizce atılan |
|---|---|---|---|
| Renault Megane 1.6 dCi 130 | `[70,44,54,80,68,74,86,84,72]` | ilk 7 | `84, 72` |
| Renault Clio 4 1.5 dCi | `[68,44,46,78,62,84,86,80,58]` | ilk 7 | `80, 58` |

Tarayıcı kodu dizinin yalnızca ilk yedi elemanını okuduğu için fazlalıklar zaten
kullanılmıyordu. Yani sayfada görünen puanlar yanlış değildi, dosyada ölü veri vardı.
Göç sırasında ilk yedi değer korundu, fazlalıklar atıldı.

Fazladan gelen iki değerin ne olduğu bilinmiyor. Büyük ihtimalle ya dokuz kriterli eski
sürümden kalmışlar ya da bir araştırma turunda taslak olarak eklenip unutulmuşlar. Bu,
tam olarak şema doğrulamasının yakalamak için var olduğu hata türüdür ve tek dosyalık
sürümde yıllarca görünmeden kalmıştı.

---

## D-02 · "Kaynaklı" etiketi tek kaynağa dayanıyordu (KAPATILDI)

`verified` işaretli 70 aracın 38'i tek bir kaynağa dayanıyordu ve etiket elle
verildiği için bu tutarsızlık görünmüyordu.

Sorun, etiketi elle verilen bir değer olmaktan çıkarıp kaynak sayısından türetilen bir
değere dönüştürerek kapatıldı. Yeni kurala göre dört ve üzeri kaynağı olan araç
`verified`, bir ile üç arası kaynağı olan araç `partial`, hiç kaynağı olmayan araç
`preliminary` sayılıyor. Kural bütün veriye uygulandı ve `scripts/validate.py` artık
etiketin kaynak sayısıyla uyuşmadığı durumu hata olarak raporluyor.

Bunun sonucunda `verified` araç sayısı 70'ten **1**'e düştü. Bu düşüş bir kayıp değil,
önceki sayının gerçeği yansıtmadığının ölçülmesidir.

---

## D-03 · Tek kaynağa aşırı yoğunlaşma (KISMEN KAPATILDI — ölçüt de düzeltildi)

`trbox` (araclo.com şanzıman rehberi), listedeki 36 aracın notunda geçiyordu ve
bunların 32'si bu kaynağa **tek başına** dayanıyordu — yani kaynak yanlış çıksa
veya çürüse bu 32 araç bir anda dayanaksız kalacaktı.

İki şey yapıldı. Birincisi, denetimin ölçtüğü şey düzeltildi:
`scripts/validate.py`'deki `kaynak-yogunlasmasi` kuralı artık bir kaynağın toplam
kaç yerde geçtiğini değil, kaç aracın **başka hiçbir kaynağı olmadan** ona tek
başına dayandığını sayıyor. Bir kaynağın elli aracın notunda geçmesi zararsız
olabilir, eğer o elli aracın hepsinin ikinci bağımsız bir kaynağı da varsa; asıl
risk tek başınalıktır.

İkincisi, `trbox`'a tek başına dayanan 32 araçtan 22'sine ikinci bir kaynak
eklendi. 18'i, zaten kutu kaydında (`data/transmissions.json`) doğrulanmış olan
ama araç kaydına hiç bağlanmamış kaynaklar araç düzeyine taşınarak (yeni araştırma
gerekmedi); 4'ü (Toyota Multidrive CVT ailesi) yeni bulunan bir kaynakla
(SlashGear'ın Toyota CVT güvenilirlik derlemesi) kazanıldı. `trbox`'a tek başına
dayanan araç sayısı 32'den **10**'a indi, sınırın (12) altına.

Kalan 10 araç bir süre daha tek başına `trbox`'a dayandı:
`audi-a4-b9-2-0-tdi`, `citroen-c-elysee-peugeot-301-benzinli`, `citroen-c4-1-6-vti`,
`ford-focus-3-1-6-ti-vct`, `mercedes-a-b-serisi`, `mitsubishi-lancer-1-6`,
`peugeot-2008-208-1-6-e-hdi`, `peugeot-301-1-6-hdi`, `peugeot-308-1-6-bluehdi`,
`toyota-corolla-e12-1-6-vvt-i`.

Bu kalıntı, kutu kayıtları tamamlanırken kendiliğinden büyük ölçüde çözüldü.
`psa-al4` kutusuna ikinci bağımsız bir kaynak (`go4trans_dp0`, DP0/AL4'ün valf
gövdesi ve aşırı ısınma sorunlarını anlatan teknik künye) bulunduğunda bu kaynak
hem kutuya hem de kutuya bağlı bütün araçlara eklendi; `mitsubishi-lancer-1-6` ve
`toyota-corolla-e12-1-6-vvt-i` ise kendi kutularının araştırmasından gelen
kaynaklarla ikinci referansına kavuştu. Denetimdeki `kaynak-yogunlasmasi` kuralı
artık hiçbir kaynağı işaretlemiyor.

Buradan çıkan genel ders şu: kaynak yoğunlaşması doğrudan saldırılması gereken
ayrı bir iş kalemi değil, bileşen kayıtları (kutu, motor) tamamlandıkça kendiliğinden
çözülen bir yan üründür. Bir kutu araştırıldığında bulunan kaynak, o kutuyu paylaşan
bütün araçlara aynı anda ikinci referans sağlıyor.

---

## D-04 · "Ön değerlendirme" etiketli ama kaynağı olan araçlar (KAPATILDI)

27 araç `preliminary` işaretli olmasına rağmen `sources` alanı doluydu. D-02 ile
birlikte gelen türetme kuralı bu çelişkiyi de ortadan kaldırdı; kaynağı olan araç
tanım gereği artık `preliminary` olamıyor ve bu 27 araç `partial` oldu.

Geriye asıl soru kaldı: bu kaynakların bir kısmı aracı gerçekten destekliyor mu, yoksa
genel bir arka plan referansı olarak mı iliştirilmiş? `trbox` gibi genel şanzıman
rehberleri için ikincisi daha muhtemel görünüyor. Bu soru, kaynak ile iddia arasındaki
bağ `evidence` bloğuyla kurulduğunda cevaplanacak.

---

## D-05 · Yetim kaynaklar (AÇIK — muhtemelen zararsız, sayı azalıyor)

Hiçbir araca veya şanzıman kutusu kaydına bağlı olmayan 11 kaynak var:

`araclo_c5aircross`, `dhaber_qashqai13`, `dhaber_sportage_dct`, `erenservis_eat8`,
`hech_koleos`, `kronikyorum_qashqai`, `mkt`, `motor1_psa_suv_eat`,
`otomobilforum_sanziman`, `sikayetvar_qashqai`, `sikayetvar_tucson_dct`

Sayı 13'ten 11'e düştü: `andcetin_dq200` ve `andcetin_dct_tucson`, şanzıman kutusu
kayıtları kurulurken `vag-dq200` ve `hyundai-7dct` kayıtlarına bağlandı. Bu, yetim
kaynak sayısının yalnızca SUV/MPV genişlemesiyle değil, kutu ve motor kayıtları
ilerledikçe de düşeceğini gösteriyor.

Çoğu SUV ve MPV temizliğinden kalma kaynaklar (Tucson, Qashqai, Sportage, C5 Aircross,
Grandland, Koleos). Bunlar gerçek araştırma çıktısı ve silinmediler. SUV ile MPV
araçların listeye geri alınması kararlaştırıldığı için de artık yetim olarak
kalmayacaklar; ilgili araçlar eklendiğinde doğrudan bağlanacaklar. `build.py` bir
kaynağı hiçbir araca bağlı olmadığı sürece sayfaya basmıyor, yalnızca arşivde
tutuyor.

`mkt` (Türkiye ortalama ikinci el fiyatı) ve `otomobilforum_sanziman` (genel şanzıman
karşılaştırması) ise hâlâ geçerli ama hiçbir araca bağlanmamış genel referanslar.

---

## D-06 · Kapsam kuralı dışında kalan araçlar (KAPATILDI — kural kaldırıldı)

Kapsam kuralının kendisi kaldırıldığı için bu madde konusuz kaldı. Aşağıdaki liste,
kararın hangi araçları ilgilendirdiğini göstermek için kayıt olarak duruyor. Bu
araçların hepsi listede kalıyor; kullanıcı isterse beygir ve model yılı filtreleriyle
kendi sınırını çiziyor. Gerekçe `docs/ARCHITECTURE.md` içindeki MK-03 kaydında.

<details>
<summary>Eski kuralın dışında kalan araçlar</summary>

11 araç, listenin kendi koyduğu "en az 110 bg, 1998 sonrası" kuralının dışında:

- **110 bg'nin altı:** Renault Clio 4 1.5 dCi (90 bg), Hyundai Elantra XD (105 bg),
  Kia Cerato eski nesil (105 bg)
- **1998 öncesi:** BMW E36 (1995), Opel Vectra B (1995), Mercedes W202 (1993),
  Audi A4 B5 (1994), Skoda Octavia 1 (1996), Peugeot 406 (1995), Mazda 626 (1997),
  Saab 9-3/9-5 (1997)

</details>

---

## D-07 · Kanıtsız zayıf halka (KAPATILDI)

Dört araçta en az bir kriterde 35'in altında puan bulunuyordu, ancak bu araçların
hiç kaynağı yoktu — Alfa Romeo 156 (`age`), Kia Rio / Hyundai i20 1.4 (`fun`),
Rover 75 (`age`, `liq`), Toyota Corolla 1.6 2007-13 (`fun`). 35 altındaki bir puan
aracı tabloda kırmızı işaretlediği ve pratikte listeden elediği için en iddialı
puan türüdür.

Dördü için de kaynak bulundu ve araç kaydına bağlandı: Alfa 156 için What Car?'ın
güvenilirlik derlemesi, Kia Rio/i20 için MotorBeam'in performans testi, Rover 75
için TechTurkey forumunun Türkiye'ye özel yedek parça tartışması, Corolla için
MotorBiscuit'in "sıkıcı ama güvenilir" derlemesi.

Bir not: Corolla'nın önceki metninde birebir bir forum alıntısı ("1960'ların
ToyoGlide tasarımının güncellenmiş hali...") vardı ama bu alıntının gerçek kaynağı
yeniden bulunamadı. Doğrulanamayan bir alıntıyı korumak yerine metinden çıkarıldı
ve doğrulanabilir bir kaynakla değiştirildi.

---

## D-08 · Ağırlık seti belgeyle uyuşmazlığı (KAPATILDI)

Aktarım dokümanında varsayılan ağırlık seti `motor:18, trans:13` diye başlıyor ve
toplamı 96 ediyordu; çalışan HTML dosyasında ise set `motor:20, trans:15` diye
başlıyor ve toplamı tam 100 ediyordu. Çalışan koddaki değerlerin doğru olduğu kabul
edildi ve `data/criteria.json` dosyasına o set yazıldı.

---

## D-09 · Volvo S60 2.0T'nin şanzıman puanı gerekçesiz kalıyordu (KAPATILDI)

`getrag-6dct450` kutusuna `base_score = 52` atandıktan sonra bu kutuyu paylaşan üç
araçtan ikisi (Ford Mondeo, Ford Focus) bu değere yakın kalırken, Volvo S60 2.0T'nin
puanı (28) kutunun temel puanından 24 puan düşükte duruyordu ve bu fark hiçbir
kaynakla açıklanamıyordu.

Torkla açıklanamadığı zaten biliniyordu (üç aracın torku da kutunun 450 Nm sınırının
altında). Geriye kalan ihtimal, Volvo'nun benzin turbo (T5 sınıfı) uygulamasının
dizel uygulamalardan daha ağır aşınması olabilirdi — bu ihtimal ayrıca araştırıldı.
AutoDoc'un Volvo S60 sorun derlemesi dahil hiçbir kaynak, Powershift şikayet
paternini (60-100 bin km'de sarsıntı, gecikmeli vites geçişi, kavrama aşınması)
motor tipine göre ayrıştırmıyor; hem Ford hem Volvo uygulamalarında aynı şekilde
tarif ediliyor.

Kanıt yokluğu teyit edildikten sonra puan kutunun temel puanına (52) çekildi. Bu,
tahmin değil, araştırmanın gerçekten yapılıp Volvo'ya özgü bir fark bulunamadığının
kaydı.

---

## D-10 · Gövde tipi doldurulurken dört karma model kaydı bilinçli boş bırakıldı (KAPATILDI)

154 aracın 150'sine `specs.body_type` atandı. Kalan dört kayıt, tek bir dosyada iki
farklı model birleştirdiği ve bu iki modelin gövde tipi birbirinden farklı olduğu için
`null` bırakıldı; tek bir değer zorlamak, filtrenin araçlardan birini yanlış
sınıflandırması anlamına gelirdi:

- **`kia-rio-hyundai-i20-1-4`** — Kia Rio Türkiye'de esas olarak sedan, Hyundai i20 ise
  yalnızca hatchback olarak satıldı.
- **`mercedes-a-b-serisi`** — A Serisi hatchback, B Serisi ise MPV (kompakt minivan)
  gövdeli.
- **`peugeot-2008-208-1-6-e-hdi`** — 2008 bir SUV/crossover, 208 ise hatchback.
- **`volvo-s40-v50-2-0`** — kaydın kendi notu da bunu "küçük sedan ve station wagon
  ikilisi" diye tanımlıyor; S40 sedan, V50 station wagon.

Diğer karma kayıtlarda (`nissan-almera-primera-1-6-2-0`, `saab-9-3-9-5-2-0t`,
`megane-clio-1-3-tce`, `opel-corsa-astra-1-4-turbo`) birleşen modellerin gövde tipi
aynı olduğu ya da kaydın kendi notu tek bir gövdeyi ("Japon sedan", "İsveç sedanı" gibi)
açıkça işaret ettiği için tek bir değer atanabildi.

---

## D-11 · "Tork konvertörü demek güvenli demek" varsayımı 22 araçta puan şişirmişti (KAPATILDI)

57 araç bir şanzıman kutusu kaydına bağlandığında ve o kutular tek tek araştırıldığında,
22 araçta puanın kutunun temel puanından 15'ten fazla saptığı ortaya çıktı. Sapmanın
yönü her seferinde aynıydı: araç puanı kutunun puanından **yüksekti**.

Sebep tek bir örtük varsayımdı. Bu araçların notları "otomatiği tork konvertörlü,
dertsiz" ya da "ZF otomatiği sağlam" gibi ifadeler taşıyordu; yani kutu tipi (tork
konvertörü) tek başına bir güvenilirlik kanıtı sayılmıştı. Kutu araştırması bu
varsayımı kısmen çürüttü — tork konvertörlü olmak çift kavramalı olmaya göre bir
avantaj, ama kutunun kendi arıza geçmişinin yerine geçmiyor:

| Kutu | Bulgu | Etkilenen araç |
|---|---|---:|
| `gm-5l40e` | Kilitleme solenoidi arızası tam güç kaybına yol açabiliyor | 4 |
| `psa-al4` | Selenoid valf arızası, aşırı ısınma, valf gövdesi hassasiyeti | 6 |
| `aisin-aw55` | 50.000 milin altında yaygınlaşan, yapısal kusur teşhisi konmuş arızalar | 4 |
| `ford-cd4e` | Sayılmış 545 şikayet kaydı, ana pompa tahriki sıyrılması | 2 |
| `zf-4hp` | BMW uygulamalarında bakıma rağmen erken arıza eğilimi | 2 |
| `jatco-jf506e` | Tüm vitelerde güç kaybına varabilen arızalar | 1 |
| `mitsubishi-invecs-cvt` | Üreticinin kendi geri çağırmasına konu olan CVT kusuru | 1 |
| `ford-4f27e` | Kutuya özgü kanıt olumluydu, sapma yine de kapatıldı | 2 |

Yirmi iki aracın hiçbirinde şanzımana özgü, kutunun bulgusunu geçersiz kılan bir kanıt
yoktu; tek istisna Ford Focus 2'nin Türkçe forum kaynağıydı ve o kaynak da kutunun
kendisi hakkında konuştuğu için araç düzeyinde bir istisna yazmak yerine kutunun temel
puanına taşındı (62'den 72'ye). Bu, `docs/PLAN.md` §6'daki kuralın uygulanmasıdır:
sapmalar puan düzeltilerek kapatılır, bant genişletilerek değil.

Değişimin büyüklüğü kayda değer — Volvo S60 birinci nesil 82'den 46'ya, Mondeo Mk3
72'den 42'ye indi. Bu bir kayıp değil, daha önce ölçülmemiş bir riskin ölçülmesidir.

---

## D-12 · Fiyat bantları gerçek piyasa verisiyle spot-kontrol edildi (KISMEN KAPATILDI — sınırlı erişimle)

Kullanıcının isteği üzerine 221 aracın `price_band_k_try` alanları gerçek 2026 Türkiye
ikinci el piyasasına karşı doğrulanmaya çalışıldı. Bu maddenin gerekçesi diğerlerinden
farklı: `README.md`'nin de yazdığı gibi fiyat aralığı `evidence` kuralının istisnası,
çünkü fiyat bir görüş değil piyasa verisi — dolayısıyla kanıt zincirinden değil,
doğrudan piyasadan doğrulanması gerekiyor.

**Karşılaşılan sınırlama.** Bu oturumun çalıştığı uzak ortamda `WebFetch` aracı hiçbir
dış sayfaya erişemiyor (`EGRESS_BLOCKED`) — yalnızca sahibinden.com/arabam.com değil,
kontrol amacıyla denenen en.wikipedia.org ve forum.donanimhaber.com/eksisozluk.com gibi
alakasız siteler de aynı hatayı verdi. Yani bu, ilan sitelerine özel bir engel değil,
ortamın ağ geçidi politikasının genel bir kısıtlaması; "forumlara bak" önerisi de aynı
sebeple WebFetch üzerinden uygulanamadı. Doğrulama bu yüzden tamamen `WebSearch`'ün
döndürdüğü arama sonucu özetlerine dayandı; bu özetler çoğunlukla genel ilan sayfası
bağlantıları veriyor, tek tek ilan fiyatı vermiyor.

Bulunan tek işe yarar kanal, sertifikalı ikinci el satıcılarının (esas olarak
**Borusan Next**) her ilanı ayrı bir URL'ye sahip olması ve bu URL'lerin arama
sonucu özetinde model yılı + km + TL fiyatıyla birlikte indekslenmesiyken; forum
(DonanımHaber, Ekşi Sözlük) ve genel "piyasa analizi" sonuçları hiçbir zaman tek
araç fiyatı vermedi, yalnızca trend yorumu içeriyordu. Bu kanal da yalnızca Borusan
Next'in stokladığı, göreli yeni (~10 yaşından küçük) araçlar için işliyor; 1990'lar-
2000'ler BMW/Mercedes gibi klasik-dönem kayıtlarımız için hiç veri bulunamadı, çünkü
bu satıcılar o yaştaki araçları zaten satmıyor. Bu yüzden derinlik hedeflenenden çok
daha dar kaldı: **221 araçtan 9'u** için gerçek fiyat rakamına ulaşıldı.

**Bulunanlar ve verilen kararlar.**

| Araç | Kayıtlı yıl aralığı | Bulunan gerçek veri | Karar |
|---|---|---|---|
| `hyundai-tucson-1-6-crdi-7dct` | 2016-2020 | Borusan Next, 2020 model 1.6 CRDi Elite otomatik dizel: 1.680.000-1.945.000 TL (sertifikalı satıcı fiyatı) | **Düzeltildi.** Bandın kayıtlı üst sınırı (1450) bulunan en düşük sertifikalı fiyatın (1680) bile altında kalıyordu; özel satıcı fiyatının sertifikalı satıcıdan genelde %10-20 daha düşük olduğu kabul edilse bile ([1000, 1450] → **[1050, 1700]**) bant gerçekçi aralığa çekildi. |
| `nissan-qashqai-1-3-dig-t-cvt` | 2017-2021 | Borusan Next, 2020 model 1.3 DIG-T Sky Pack otomatik: 1.775.000 TL (sertifikalı satıcı fiyatı, kayıtlı yıl aralığının tam içinde) | **Düzeltildi.** %15 özel-satıcı indirimiyle bile (~1.509.000) mevcut üst sınırın (1300) belirgin biçimde üzerinde kalıyordu; ([900, 1300] → **[950, 1600]**) bant yukarı çekildi. |
| `fiat-egea-1-6-multijet` | 2016-2023 | Borusan Next: 2019 model 830.000-915.000 TL, 2022 model 1.010.000 TL (2024 model 1.245.000 TL bulundu ama kaydın yıl aralığı dışında, karşılaştırmaya alınmadı) | **Değiştirilmedi.** Kayıtlı yıl aralığındaki en yüksek gerçek veri (2022, 1.010.000 TL) mevcut üst sınırın (1100) altında kalıyor; bant zaten gerçekçi. |
| `renault-clio-4-1-5-dci` | 2012-2019 | Borusan Next, 2018 model 1.5 dCi Touch otomatik dizel: 810.000 TL (sertifikalı satıcı fiyatı) | **Değiştirilmedi.** Sertifikalı fiyattan makul bir özel-satıcı indirimi (~%12-15) düşüldüğünde (~690-710 bin TL) mevcut üst sınırın (750) içine düşüyor; bant sınırda ama gerçekçi. |
| `toyota-corolla-1-6-2013` | 2013-2018 | Borusan Otomotiv, 2016 model 101.690 km otomatik: 848.000 TL (sertifikalı satıcı fiyatı) | **Değiştirilmedi, ama not düşüldü.** Bulunan rakam mevcut alt sınırın (900) biraz altında; tek veri noktası ve kaydın orta yılından (2016, yüksek km) geliyor, kaydın en eski yılı (2013) için beklenen fiyat muhtemelen daha da düşük. Bant tamamen yanlış değil ama alt sınır iyimser olabilir — üçüncü bir bağımsız veri noktası bulunursa yeniden değerlendirilmeli. |
| `kia-sportage-1-6-crdi-7dct` | 2016-2020 | Borusan Next, 2021 model (kayıtlı aralığın bir yıl dışında) Black Edition 38 bin km: 1.725.000 TL | **Değiştirilmedi.** Veri noktası kayıtlı yıl aralığının hemen dışında ve kayıtlı en yeni yıl (2020) için tahmini fiyat, model-yılı düşüşü ve satıcı indirimi birlikte düşünüldüğünde mevcut üst sınıra (1450) yakın çıkıyor. Tek başına ve aralık-dışı bir veri noktasıyla düzeltme yapmak riskli; değiştirilmedi. |
| `vw-troc-1-5-tsi` | 2018-2021 | Borusan Next, 2020-2021 model Highline otomatik: 1.530.000-1.670.000 TL (kayıtlı yıl aralığının tam içinde) | **Değiştirilmedi.** %15 indirimle (~1.300.000-1.420.000) mevcut bandın (1100-1550) içinde kalıyor. |
| BMW E46/E90 320i, W202/W203 C200 gibi klasik-dönem kayıtlar | — | Borusan Next'te hiç veri yok (bu satıcı ~10 yaşından eski araç satmıyor) | **Karşılaştırma yapılamadı.** Bu yaş grubundaki kayıtlar için bu oturumda kullanılan yöntemle hiç veri toplanamadı; ayrı bir kanal gerekiyor. |
| Opel Astra 1.6 CDTI | — | Arama özetinde "161.750-225.000 TL" rakamı çıktı | **Güvenilmez sayıldı, kullanılmadı.** Bu rakam bugünün TL'siyle tutarsız (aynı segmentteki her diğer araç 500 bin TL'nin üzerinde); muhtemelen eski bir sayfadan ya da alakasız bir bağlamdan (örn. ÖTV tablosu) geliyor. Kaynağı doğrulanamayan bir rakamı veriye yazmak, doğrulama işinin amacına aykırı olurdu. |

**Genel bulgu.** Aynı dönemde bulunan makro veri (Cumhuriyet, "İkinci el araçta 2026 ilk
yarı raporu"), Ocak-Haziran 2026 arasında ikinci el araç fiyat endeksinin yalnızca
%5 arttığını, buna karşın genel enflasyonun %17,7 olduğunu bildiriyor; 12 aylık
dönemde ikinci el artışı %15,4, enflasyon %32,1. Yani ikinci el fiyatları enflasyonun
belirgin biçimde gerisinde kalıyor. Buna rağmen dokuz örnekten ikisinde (Tucson,
Qashqai — ikisi de SUV) bant belirgin biçimde düşük çıktı; bu, SUV segmentinin diğer
gövde tiplerine göre nominal olarak daha hızlı değer kazandığına işaret ediyor
olabilir, ama iki örnekten genel bir kural çıkarmak için erken.

**Kapatılmama gerekçesi.** Bu madde "kısmen kapatıldı" işaretli, çünkü yapılan iş bir
doğrulama turu değil, bir **spot-kontrol** oldu — 221 aracın 9'u örneklendi, ikisi
düzeltildi. Kalan 212 araç hâlâ hiç piyasa verisiyle karşılaştırılmadı ve özellikle
1990'lar-2000'ler klasik-dönem kayıtları için bu oturumun yönteminin (sertifikalı
satıcı ilanları) hiçbir zaman veri üretemeyeceği görüldü — o segment için farklı bir
kaynak türü (örn. klasik araç forumları, ama bu ortamda WebFetch engelliyken
erişilemiyor) gerekiyor. Ağ erişimi bu ortamda kısıtlı olduğu sürece kapsamlı bir tur
pratik değil; kullanıcı sahibinden.com/arabam.com'a veya forumlara doğrudan erişimi
olan bir ortamda (yerel makine, farklı ağ politikası) daha geniş bir tur istiyorsa bu
madde yeniden açılıp genişletilebilir.
