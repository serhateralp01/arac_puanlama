# Araç Puanlama

Türkiye ikinci el piyasasındaki **otomatik vitesli 154 araç–motor–şanzıman kombinasyonunu**
yedi kriter üzerinden puanlayan, ağırlıkları kullanıcı tarafından ayarlanabilen bir
karşılaştırma aracı. Çıktı tek dosyalık, bağımlılıksız bir HTML: `arac-puanlama.html`.

Kapsam: 1998 ve sonrası, en az 110 beygir, otomatik şanzıman. SUV ve MPV'ler bilinçli
olarak dışarıda.

## Neden bu yapı

Proje daha önce tek bir dev HTML dosyasıydı: veri, tasarım ve mantık aynı yerdeydi.
İki şey yapılamıyordu — puanların **tekrarlanabilirliği** (aynı kanıt neden bu puanı
veriyor?) ve araştırmaların **kalıcı saklanması** (kaynaklar yalnızca link olarak
duruyordu). Bu depo o iki sorunu çözmek için veriyi koddan ayırır:

```
data/cars/*.json        her araç kendi dosyasında
data/sources.json       kaynak künyeleri (iddia, yayıncı, URL, tür, güven seviyesi)
data/criteria.json      kriter tanımları, ağırlık setleri, eşikler
data/schema/*.json      JSON Schema — editör desteği ve sözleşme
templates/index.html    sayfanın iskeleti (veri yerine yer tutucu)
scripts/build.py        veri + şablon → arac-puanlama.html
scripts/validate.py     veri bütünlüğü + kanıt politikası denetimi
scripts/smoke_test.js   üretilen sayfayı gerçek tarayıcıda çalıştırır
legacy/                 göç öncesi tek dosyalık sürüm (referans, dokunulmuyor)
docs/                   metodoloji, bilinen veri sorunları, yol haritası
```

Kazanç şu: bir puan değiştiğinde `git diff` artık **"puan 44'ten 38'e düştü, gerekçe:
şu kaynak"** diye okunabiliyor. Tek dosyalık sürümde bu iz tamamen kayıptı.

## Kullanım

Harici bağımlılık yok; Python 3.9+ yeterli.

```bash
python3 scripts/build.py            # veriden HTML üret
python3 scripts/build.py --check    # üretilmiş dosya veriyle uyumlu mu (CI için)
python3 scripts/validate.py         # veriyi denetle
python3 scripts/validate.py --strict # uyarılar da başarısızlık sayılsın
```

Tarayıcı testi için (yalnızca geliştirme sırasında, Playwright gerektirir):

```bash
npm install playwright && node scripts/smoke_test.js
```

**`arac-puanlama.html` elle düzenlenmez** — üretilmiş dosyadır. Değişiklik `data/`
veya `templates/` içinde yapılır, sonra `build.py` çalıştırılır.

## Veri modeli

Bir aracın kaydı (`data/cars/volvo-s60-2-0-d-d3-d4.json` gibi):

```json
{
  "id": "volvo-s60-2-0-d-d3-d4",
  "name": "Volvo S60 2.0 D (D3/D4)",
  "specs": { "hp": 163, "displacement_l": 2.0, "fuel": "Dizel",
             "drivetrain": "Önden", "transmission_type": "TK" },
  "price_band_k_try": [700, 1150],
  "verification": "verified",
  "scores": { "motor": 80, "trans": 90, "fun": 70, "comf": 82,
              "age": 70, "cost": 69, "liq": 50 },
  "sources": ["volvod", "volvops"],
  "note": "..."
}
```

Fiyat puanı dosyada tutulmaz; listedeki en ucuza 100, en pahalıya 0 verilerek üretim
sırasında hesaplanır. Şanzıman tipleri ve kriter tanımları için
[docs/methodology.md](docs/methodology.md).

## Denetimin bugünkü durumu

`validate.py` şu an **0 hata, 170 uyarı** veriyor. Uyarılar bilinçli olarak
başarısızlık sayılmıyor — bunlar Faz 2'nin iş listesi:

| Kural | Adet | Ne demek |
|---|---:|---|
| `guven-seviyesi-yok` | 68 | Hiçbir kaynağa A/B/C güven seviyesi atanmamış |
| `tek-kaynak` | 38 | "Kaynaklı" işaretli ama tek kaynağa dayanıyor |
| `etiket-uyumsuz` | 27 | "Ön değerlendirme" işaretli ama kaynağı var |
| `yetim-kaynak` | 13 | Hiçbir araca bağlı olmayan kaynak (SUV temizliğinden kalma) |
| `kapsam-kurali` | 11 | 110 bg / 1998 sınırının dışında kalan araçlar |
| `puan-bandi-yok` | 7 | Kriterlerin hiçbirinde yazılı puan bandı yok |
| `kanitsiz-zayif-halka` | 4 | 35 altı eleyici puan var ama kaynak yok |
| `kaynak-yogunlasmasi` | 2 | Tek kaynak 12'den fazla aracı taşıyor |

Araç başına ortalama kaynak sayısı **1.09**. Bu sayıyı yükseltmek Faz 2'nin ana hedefi.

## Yol haritası

[docs/PLAN.md](docs/PLAN.md) — puan bantları, güven seviyeleri, kaynak alıntılama,
kalan araçların araştırılması.

## Sorumluluk reddi

Puanlar mutlak değildir; yalnızca bu liste içindeki araçların birbirine göre durumunu
gösterir. Fiyatlar ikinci el piyasa ortalamalarına dayanan yaklaşık değerlerdir, tek tek
ilanlardan alınmamıştır. Satın almadan önce sahibinden.com ve arabam.com üzerinden
doğrulayın, ekspertize gösterin.
