# Kaynak araştırma kuyruğu

Bu klasör `data/`'nın geri kalanından bilinçli olarak ayrı tutuluyor. Buradaki hiçbir
kayıt `scripts/validate.py` tarafından gerçek veri sayılmaz ve `scripts/build.py`
üretilen sayfaya hiçbir şey basmaz; şeması `data/schema/queue-candidate.schema.json`
içinde tanımlı. Ayrımın gerekçesi `docs/ARCHITECTURE.md` içindeki MK-09 kaydında: bir
kaynak yayına ancak açıkça kabul edildikten sonra girmeli, doğrulanmamış bir adayın
yanlışlıkla yayına karışması projenin bütün kanıt iddiasını zedeler.

## İki aşamalı akış

1. **Toplama.** Bir araç veya bileşen için aday kaynaklar aranır ve
   `candidates.json`'a `status: "pending"`, `resolution: null` olarak eklenir. Bu
   aşamada puan verilmez, yorum yapılmaz; yalnızca araç kimliği, hangi kriteri
   ilgilendirdiği, bağlantı, yayıncı ve kaynaktan çıkan iddianın kısa özeti kaydedilir.
2. **İşleme.** Her aday tek tek değerlendirilir: kaynak iddiayı gerçekten destekliyor
   mu, güven seviyesi (A/B/C) ne, hangi araca/kritere karşılık geliyor. Kabul edilen
   adaylar `status: "accepted"` olur, `resolution` alanı doldurulur ve aynı kimlikle
   `data/sources.json`'a taşınır; ilgili araç kaydının `sources` listesine eklenir ve
   `verification` alanı yeniden hesaplanır. Reddedilen adaylar `status: "rejected"`
   olarak, gerekçesiyle birlikte kuyrukta kalır — böylece aynı zayıf kaynak ikinci kez
   önerilmez.

## İlk tur

2026-08-06 tarihinde `data/cars/` içindeki kaynaksız 14 araç için bu akış uçtan uca
çalıştırıldı: her biri için gerçek bir kaynak arandı, değerlendirildi ve kabul edilenler
`data/sources.json` ile ilgili araç kayıtlarına işlendi. `candidates.json`'daki 14 kayıt
bu turun kaydı; hepsi `status: "accepted"`. Ayrıntı için `docs/ROADMAP.md` içindeki Y-02
ve Y-03 maddelerine bakın.
