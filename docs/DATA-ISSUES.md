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

## D-03 · Tek kaynağa aşırı yoğunlaşma (AÇIK)

| Kaynak | Kaç aracı taşıyor |
|---|---:|
| `trbox` (araclo.com şanzıman rehberi) | **36** |
| `om61x` (Wikipedia / cars-expert) | **13** |

`trbox`, araclo.com üzerindeki tek bir blog yazısıdır ve listedeki araçların yaklaşık
dörtte birinin şanzıman değerlendirmesini tek başına taşımaktadır. Bu yazıdaki bir
hata ortaya çıkarsa ya da bağlantı çürürse 36 araç aynı anda dayanaksız kalır. Tek
noktadan bağımlılık, kanıt zincirindeki en kırılgan noktadır ve bu bağımlılığın
kırılması gerekiyor.

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

## D-07 · Kanıtsız zayıf halka (AÇIK)

Dört araçta en az bir kriterde 35'in altında puan bulunuyor, ancak bu araçların hiç
kaynağı yok. 35 altındaki bir puan, aracı tabloda kırmızı işaretlediği ve pratikte
listeden elediği için en iddialı puan türüdür. Bir aracı eleyen puanın kanıtsız
verilmesi kabul edilemez, bu yüzden bu dört araç araştırma sırasının başına alınacak.

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
