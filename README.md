# Araç Puanlama

Türkiye ikinci el piyasasındaki otomatik vitesli araçları yedi kriter üzerinden
puanlayan ve kullanıcının kendi belirlediği ağırlıklara göre sıralayan bir
karşılaştırma platformu. Çıktı, hiçbir sunucuya veya bağımlılığa ihtiyaç duymadan
tarayıcıda açılan tek bir dosyadır: `arac-puanlama.html`.

Şu an listede **154 araç, motor ve şanzıman kombinasyonu** bulunuyor ve liste
genişletiliyor. Listeye girmek için tek şart aracın otomatik şanzımanla satılmış ve
Türkiye piyasasında bulunabilir olmasıdır; beygir, model yılı veya gövde tipi üzerinden
bir alt sınır yoktur. Daraltma işini kullanıcı filtrelerle yapar.

## Neden bu yapı

Proje daha önce tek bir büyük HTML dosyasıydı ve veri, tasarım ile mantık aynı yerde
duruyordu. Bu yapıda iki şey yapılamıyordu. Birincisi, bir puanın neden o puan olduğu
izlenemiyordu; ikincisi, yapılan araştırmalar kalıcı olarak saklanmıyordu, çünkü
kaynaklar yalnızca birer bağlantı olarak duruyordu.

Bu depo, veriyi koddan ayırarak her iki sorunu da çözmeyi hedefliyor:

```
data/cars/*.json        her araç kendi dosyasında
data/sources.json       kaynak künyeleri: hangi iddiayı, hangi yayıncı, hangi bağlantı
data/criteria.json      kriter tanımları, ağırlık setleri, eşikler
data/schema/*.json      JSON Schema; hem editör desteği hem veri sözleşmesi
templates/index.html    sayfanın iskeleti, veri yerine yer tutucu içerir
scripts/build.py        veri ile şablonu birleştirip HTML üretir
scripts/validate.py     veri bütünlüğünü ve kanıt politikasını denetler
scripts/smoke_test.js   üretilen sayfayı gerçek bir tarayıcıda çalıştırıp doğrular
legacy/                 göç öncesi tek dosyalık sürüm, referans olarak duruyor
docs/                   mimari kararlar, metodoloji, bilinen sorunlar, yol haritası
```

Bu ayrımın kazancı şudur: bir puan değiştiğinde `git diff` artık hem eski değeri, hem
yeni değeri, hem de commit mesajındaki gerekçeyi gösteriyor. Tek dosyalık sürümde bu iz
tamamen kayboluyordu.

## Kullanım

Harici bir bağımlılık yok; Python 3.9 veya üstü yeterli.

```bash
python3 scripts/build.py             # veriden HTML üret
python3 scripts/build.py --check     # üretilmiş dosya veriyle uyumlu mu, yazmadan söyle
python3 scripts/validate.py          # veriyi denetle
python3 scripts/validate.py --strict # uyarılar da başarısızlık sayılsın
```

Tarayıcı testi yalnızca geliştirme sırasında gerekir ve Playwright ister:

```bash
npm install playwright && node scripts/smoke_test.js
```

`arac-puanlama.html` üretilmiş bir dosyadır ve elle düzenlenmez. Bir şeyi değiştirmek
için `data/` veya `templates/` içinde düzenleme yapılır, ardından `build.py`
çalıştırılır.

## Veri modeli

Bir aracın kaydı şöyle görünür:

```json
{
  "id": "volvo-s60-2-0-d-d3-d4",
  "name": "Volvo S60 2.0 D (D3/D4)",
  "specs": { "hp": 163, "displacement_l": 2.0, "fuel": "Dizel",
             "drivetrain": "Önden", "transmission_type": "TK" },
  "price_band_k_try": [700, 1150],
  "verification": "partial",
  "scores": { "motor": 80, "trans": 90, "fun": 70, "comf": 82,
              "age": 70, "cost": 69, "liq": 50 },
  "sources": ["volvod", "volvops"],
  "note": "..."
}
```

Fiyat puanı dosyada tutulmaz. Listedeki en ucuz araca 100, en pahalı araca 0 verilerek
üretim sırasında hesaplanır, çünkü bu puan tek bir aracın değil listenin tamamının
fonksiyonudur.

## Doğrulama rozetleri

Her aracın adının yanında, o araç için ne kadar kanıt toplandığını gösteren bir rozet
bulunur. Rozet elle verilmez; aracın bağlı olduğu bağımsız kaynak sayısından
hesaplanır.

| Kaynak sayısı | Rozet | Bugünkü sayı |
|---:|---|---:|
| 4 ve üzeri | doğrulanmış | 1 |
| 1 – 3 | kısmi kaynak | 116 |
| 0 | ön değerlendirme | 37 |

Yalnızca bir aracın doğrulanmış sayılması, listenin zayıf olduğu anlamına gelmiyor;
önceki elle verilen etiketlerin fazla iyimser olduğu anlamına geliyor. Hedef, her aracı
dört bağımsız kaynağa çıkarmak. Gerekçesi `docs/ARCHITECTURE.md` içindeki MK-04
kaydında yazılı.

## Denetimin bugünkü durumu

`scripts/validate.py` şu an **0 hata, 401 uyarı** veriyor. Uyarılar bilinçli olarak
başarısızlık sayılmıyor; her biri yol haritasındaki bir maddeye karşılık geliyor.

| Kural | Adet | Ne anlama geliyor |
|---|---:|---|
| `govde-tipi-yok` | 154 | Gövde tipi alanı henüz doldurulmadı, gövde filtresi bu yüzden yok |
| `kaynak-yetersiz` | 116 | Araç bir ile üç arası kaynağa dayanıyor, dörde çıkması gerekiyor |
| `guven-seviyesi-yok` | 68 | Hiçbir kaynağa A, B veya C güven seviyesi atanmadı |
| `kaynaksiz` | 37 | Araç hiçbir kaynağa bağlı değil |
| `yetim-kaynak` | 13 | Kaynak hiçbir araca bağlı değil, çoğu SUV araştırmasından kalma |
| `puan-bandi-yok` | 7 | Hiçbir kriterin yazılı puan bandı yok |
| `kanitsiz-zayif-halka` | 4 | Aracı eleyen 35 altı puan var ama kaynak yok |
| `kaynak-yogunlasmasi` | 2 | Tek bir kaynak 12'den fazla aracı taşıyor |

Araç başına ortalama kaynak sayısı **1.09**. Bu sayıyı 2.0'ın üstüne çıkarmak yol
haritasının ana hedefi.

## Katkı

Bir aracın puanını destekleyen veya çürüten bir kaynağınız varsa
[kaynak önerisi formuyla](.github/ISSUE_TEMPLATE/kaynak-onerisi.yml) konu açabilirsiniz.
Öneriler doğrudan veriye yazılmaz; incelenir, kaynak künyesine dönüştürülür ve ilgili
aracın kanıt kaydına bağlanır. Puanı siz vermezsiniz, kaynağı siz getirirsiniz — puan
yazılı metodolojiye göre yeniden değerlendirilir. Bunun neden böyle çalıştığı
`docs/ARCHITECTURE.md` içindeki MK-05 kaydında anlatılıyor.

## Belgeler

- [CLAUDE.md](CLAUDE.md) — depoda çalışma kuralları: yazı dili, katmanlı inşa, modülerlik
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — geri alınması pahalı kararlar ve gerekçeleri
- [docs/methodology.md](docs/methodology.md) — kriterler, puan hesabı, şanzıman sınıflandırması
- [docs/PLAN.md](docs/PLAN.md) — yol haritası ve kriter bazlı teknikler
- [docs/DATA-ISSUES.md](docs/DATA-ISSUES.md) — bilinen veri sorunları ve verilen kararlar

## Sorumluluk reddi

Puanlar mutlak bir ölçü değildir; yalnızca bu liste içindeki araçların birbirine göre
durumunu gösterir. Fiyatlar ikinci el piyasa ortalamalarına dayanan yaklaşık
değerlerdir ve tek tek ilanlardan alınmamıştır. Bir araç satın almadan önce fiyatı
sahibinden.com ve arabam.com üzerinden doğrulayın, aracı da mutlaka ekspertize
gösterin.
