# Katkı rehberi

Bu depoya katkı vermenin en değerli yolu kod yazmak değil, **kanıt getirmek**. Projenin
tek gerçek farklılaştırıcısı her puanın arkasında yazılı bir gerekçe ve erişilebilir bir
kaynak olması; katkı süreci de bunu korumak üzere kurulmuş durumda.

## En hızlı yol: konu açın

Hiçbir şey kurmanıza gerek yok. Depodaki
[konu şablonlarından](https://github.com/serhateralp01/arac_puanlama/issues/new/choose)
birini seçin:

| Şablon | Ne zaman kullanılır |
|---|---|
| **Kaynak önerisi** | Bir aracın ya da bileşenin puanını destekleyen (veya çürüten) bir kaynak biliyorsanız |
| **Veri hatası bildir** | Bir sayı, kimlik veya sınıflandırma yanlış görünüyorsa |
| **Araç öner** | Listede olması gerektiğini düşündüğünüz bir araç varsa |

Veri hatası bildirimleri özellikle değerli. 2026-08-13'te dış bir veri setiyle yapılan
çapraz doğrulama beş gerçek hata buldu; bunlardan biri 1,6 litrelik bir dizelde kayıtlı
400 Nm'lik imkânsız bir tork değeriydi ve o aracı sürüş keyfi sıralamasında haksız yere
ilk ona taşıyordu. Gözünüze tuhaf gelen her sayı bildirilmeye değer.

## Önerilen kaynak doğrudan veriye yazılmaz

Bu bilinçli bir yavaşlık. Gerekçesi `docs/ARCHITECTURE.md` içindeki MK-05 kaydında:
denetimsiz yazma hakkı verilirse, ilk kötü niyetli veya sadece dikkatsiz katkıda kanıt
zincirinin güvenilirliği kaybolur ve geri kazanılması çok zordur. Öneriniz önce
`data/queue/candidates.json` içindeki araştırma kuyruğuna girer, incelenir, güven
seviyesi (A/B/C) atanır ve ancak ondan sonra ilgili kayda işlenir.

Kaynak seviyeleri şöyle ayrılıyor:

- **A** — sayısal, kurumsal, örneklem tabanlı. Bugün depoda yalnızca beş tane var
  (ör. TÜV'ün yaklaşık 9,5 milyon muayeneye dayanan yaş-kusur tablosu).
- **B** — resmî geri çağırma duyurusu, teknik servis bülteni, mahkeme kaydı, ciddi
  ticari basın.
- **C** — forum başlığı, şikayet toplayıcı, ticari blog. Depodaki kaynakların çoğu
  burada ve bu açıkça yazılı; tek başına C seviyesi kaynağa dayanan uç puanlar
  denetimde uyarı üretiyor.

## Kod veya veri değişikliği gönderecekseniz

Üç kural var ve üçü de otomatik denetleniyor:

```bash
python3 scripts/validate.py        # veri bütünlüğü ve kanıt politikası — 0 hata vermeli
python3 scripts/build.py           # index.html'i yeniden üret
python3 scripts/build_pages.py     # statik sayfaları yeniden üret
node scripts/smoke_test.js         # tarayıcı duman testi — hepsi geçmeli
```

1. **`index.html`, `arac/`, `motor/`, `sanziman/`, `sitemap.xml` elle düzenlenmez.**
   Bunlar üretilmiş dosyalardır. Değişiklik `data/` veya `templates/` içinde yapılır,
   sonra derleme betikleri çalıştırılır. Gerekçesi MK-01'de.
2. **Puan değişikliği gerekçesiz gönderilmez.** Bir puanı değiştiriyorsanız, o aracın
   `evidence` bloğundaki `reasoning` alanı da neden değiştiğini anlatmalı.
3. **Her commit kendi başına çalışan bir durum bırakır.** "Bir sonraki commit'te
   düzelecek" diye bozuk bırakılmaz.

## Yazı dili

Bu depodaki bütün metinler — belgeler, kod yorumları, commit mesajları, arayüz metinleri —
**tam cümlelerle** yazılır ve dili Türkçedir. Kısaltmak, anlamı yok etme pahasına yapılan
bir iş değildir; bir kararın gerekçesi yazılmamışsa o karar altı ay sonra kimse tarafından
savunulamaz. Ayrıntısı `CLAUDE.md` §1'de.

## Neyin kapsam dışı olduğu

Elektrikli, hibrit ve LPG'li araçlar **kalıcı olarak** kapsam dışıdır (MK-13). Bu, projeyi
daraltan ama netleştiren bir karar: platform "otomatik vitesli, geleneksel yakıtlı ikinci el
araç" sorusuna cevap veriyor, "her türlü araç" sorusuna değil.

## Nereden başlamalı

`docs/ROADMAP.md` sıradaki işleri, `docs/ARCHITECTURE.md` geri alınması pahalı kararları
ve gerekçelerini tutuyor. Yeni bir katkıya başlamadan önce ikisine de göz atmak, aynı
tartışmayı ikinci kez yapmaktan kurtarır.
