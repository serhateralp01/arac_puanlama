# Bu depoda çalışma kuralları

Bu dosya, projenin sahibinin kalıcı tercihlerini kaydeder. Her oturumda yeniden
anlatılmasın diye buraya yazıldı. Kurallar tercih değil, şart.

---

## 1. Yazı dili

Bu projedeki bütün metinler — belgeler, kod yorumları, commit mesajları, pull request
açıklamaları, arayüz metinleri — **tam cümlelerle** yazılır.

Bir cümlenin öznesi, yüklemi ve nesnesi yerinde olmalıdır. Yalnızca kısa görünsün diye
fiili atılmış, öznesi silinmiş, anlamı buharlaşmış ifadeler kabul edilmez. Kısaltmak,
anlamı yok etme pahasına yapılan bir iş değildir.

Yanlış:

> Kaynak yetersiz. Puan düşük. Faz 2'de düzeltilecek.

Doğru:

> Bu aracın puanı tek bir forum mesajına dayanıyor ve bu, bir aracı listeden eleyecek
> kadar ağır bir puan için yeterli kanıt değil. İkinci kaynak bulunana kadar araç
> "kısmi kaynak" olarak işaretlendi.

Aynı kural tablolar için de geçerlidir: tablo hücreleri kısa olabilir, ama tablonun
öncesinde ve sonrasında o tablonun ne anlattığını söyleyen tam cümleler bulunmalıdır.
Tablo, açıklamanın yerine geçmez; açıklamayı destekler.

Belgelerin dili Türkçedir. Teknik terimlerin yerleşik Türkçe karşılığı varsa o
kullanılır, yoksa terim olduğu gibi bırakılır ve ilk geçtiği yerde açıklanır.

**Neden yapıldığı, ne yapıldığı kadar önemlidir.** Bir kararın gerekçesi yazılmamışsa
o karar altı ay sonra kimse tarafından savunulamaz ve gereksiz yere geri alınır.

---

## 2. Katman katman inşa

Sistem tek hamlede değil, katmanlar halinde kurulur.

Her katmanın kuralı şudur: **en küçük çalışan sürümü önce tamamen faal ve doğrulanmış
hale getir, ancak ondan sonra üstüne yeni katman ekle.** Bir katman çalışmadan bir
sonrakine geçilmez.

Bunun doğrudan sonucu: **bitmemiş karmaşıklık için çalışan ürün riske atılmaz.** Yarım
kalmış bir yeniden yapılandırma yüzünden bugün çalışan sayfanın bozulması kabul
edilemez. Büyük bir değişiklik gerekiyorsa, çalışan sürüm ayakta kalacak şekilde
aşamalandırılır.

Pratikte bu şu anlama gelir:

- Her katman sonunda `python3 scripts/validate.py` hatasız çalışmalı, `node
  scripts/smoke_test.js` bütün kontrolleri geçmelidir.
- Bir commit, kendi başına çalışan bir durum bırakmalıdır. "Bir sonraki commit'te
  düzelecek" diye bozuk bırakılmaz.
- Yeni bir alan veya kavram eklenirken önce şemaya isteğe bağlı olarak girer, veri
  doldurulur, sonra zorunlu hale getirilir. Ters sırada yapılırsa depo günlerce
  doğrulamadan geçmez.

---

## 3. Modülerlik

Bileşenler birbirinden temiz biçimde ayrılmış durumda tutulur. Bir bileşenin ne işe
yaradığı adından ve konumundan anlaşılmalıdır.

Bugünkü ayrım şudur ve korunması gerekir:

| Katman | Sorumluluğu | Bilmediği şey |
|---|---|---|
| `data/` | Gerçekler ve kanıt. | Bunların nasıl gösterileceğini bilmez. |
| `templates/` | Sayfanın yapısı ve görünümü. | İçindeki verinin ne olduğunu bilmez. |
| `scripts/build.py` | Veriyi şablona bağlamak. | Puanın nasıl verildiğini bilmez. |
| `scripts/validate.py` | Verinin kurallara uyup uymadığı. | Sayfayı hiç görmez. |
| `docs/` | Kararların gerekçesi. | Kod içermez. |

Bir dosyanın başka bir katmanın işini yapmaya başlaması, o dosyanın bölünmesi
gerektiğinin işaretidir. Veri dosyasına mantık, şablona veri, betiğe metodoloji
sızmamalıdır.

---

## 4. Mimari kararlar uzun dönemli alınır

Bu proje kişisel bir araştırma dosyası olarak başladı, ama artık bir ürün olarak
düşünülüyor. Ticari bir hale gelebilir, üstüne yeni özellikler eklenebilir, kullanıcı
katkısı alabilir.

Bu yüzden mimari kararlar **bugünkü ihtiyaca göre değil, üç yıl sonraki ihtiyaca göre**
alınır. Geçici bir kolaylık için mimarinin tamamı değiştirilmez.

Buradan çıkan somut kurallar:

- **Kimlikler kalıcıdır.** Bir aracın `id` alanı bir kez verildikten sonra
  değiştirilmez. Kimlik değişirse git geçmişi kopar, dış bağlantılar çürür, kullanıcı
  yer imleri bozulur.
- **Veri, sunumdan bağımsız kalır.** Bugün çıktı tek dosyalık bir HTML. Yarın bir web
  uygulaması, bir API veya bir mobil arayüz olabilir. `data/` bu değişimden
  etkilenmemelidir.
- **Kanıt, puandan ayrı saklanır.** Puan bir sonuçtur; kaynak, alıntı ve gerekçe
  girdidir. Girdiler saklanmazsa sonuç doğrulanamaz.
- **Genişleme öngörülür.** Liste 154 araçtan binlere çıkabilir. Dosya başına bir araç
  düzeni bunu kaldırır; tek dosyada dev bir dizi kaldırmaz.
- Bir karar geri alınabilir değilse, alınmadan önce `docs/ARCHITECTURE.md` içine
  gerekçesiyle yazılır.

---

## 5. Adım adım ilerleme

Büyük bir iş verildiğinde, iş önce anlamlı ve kendi başına değerli parçalara bölünür.
Her parça bitirilir, doğrulanır ve kaydedilir; sonra bir sonrakine geçilir.

Bir oturumda her şeyi bitirmek, yarısı çalışan bir depo bırakmaktan daha az değerlidir.
Hangi adımda olunduğu ve sıradaki adımın ne olduğu her zaman `docs/PLAN.md` içinden
okunabilir olmalıdır.

---

## 6. Depoyla çalışırken

- `arac-puanlama.html` üretilmiş bir dosyadır ve elle düzenlenmez. Değişiklik `data/`
  veya `templates/` içinde yapılır, ardından `python3 scripts/build.py` çalıştırılır.
- Veriyi değiştiren her commit'ten önce `python3 scripts/validate.py` çalıştırılır.
- Puanlar arayüzden düzenlenemez; yalnızca veri dosyalarından, gerekçesiyle birlikte
  değişir. Fiyat aralıkları bunun istisnasıdır, çünkü fiyat bir görüş değil piyasa
  verisidir.
- `legacy/` klasörüne dokunulmaz. Orası projenin göç öncesi halinin kaydıdır.
