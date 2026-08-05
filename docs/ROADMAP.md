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

## Durum özeti (son güncelleme: 2026-08-05)

| Katman | Durum |
|---|---|
| Veri mimarisi (araç / motor / şanzıman / kaynak ayrımı) | Tamamlandı |
| Şanzıman kutusu kayıtları | 30 kutu, hepsi temel puanlı ve kaynaklı |
| Motor ailesi kayıtları | 79 aile, 78'i temel puanlı ve kaynaklı |
| Denetim hattı (`validate.py`, `consistency.py`, `smoke_test.js`) | Çalışıyor, 0 hata, 18/18 duman testi |
| Çok ekranlı arayüz + giriş akışı + metodoloji sayfası | Çalışıyor |
| **Kaynak derinliği** | **Zayıf — asıl açık burada** |
| **Araç kapsamı** | **Dar — modern kuşak ve gövde çeşitliliği eksik** |
| Görsel dil / ürün hissi | Ham, iş odaklı |

Denetimin bugünkü çıktısı: **0 hata, 183 uyarı**. Uyarıların ezici çoğunluğu (132) tek
bir kalemden geliyor: araçların dört bağımsız kaynağa ulaşmamış olması.

---

## Y-01 · Araç listesini genişlet ve kapsamı dengele

**Öncelik: yüksek.** Ürünün değeri doğrudan buna bağlı; kimse aradığı aracı bulamadığı
bir listeyi ikinci kez açmaz.

**Sorun.** Liste 154 araç içeriyor ama dağılımı çok dengesiz. Aşağıdaki tablo
`data/cars/` üzerinde yapılan sayımdan çıktı:

| Boyut | Bugünkü dağılım | Sorun |
|---|---|---|
| Model yılı | 1990'lar 20 · 2000'ler 73 · 2010'lar 61 | **2016 ve sonrası yalnızca 5 araç.** Liste pratikte 2015'te bitiyor. |
| Gövde | Sedan 108 · Hatchback 37 · Coupe 3 · SUV 1 · SW 1 | SUV ve station wagon neredeyse yok, oysa Türkiye'de SUV payı çok yüksek. |
| Şanzıman | TK 103 · Kuru DCT 23 · Islak DCT 14 · CVT 12 · Robot 2 | Modern araçlarda yaygınlaşan ıslak DCT ve CVT az temsil ediliyor. |
| Yakıt | Benzin 94 · Dizel 60 | Hibrit hiç yok; Türkiye'de Corolla/C-HR hibrit çok yaygın. |

**Listede hiç bulunmayan markalar:** Dacia, Jeep, MINI, Lexus, Cupra, MG, Chery, BYD,
Togg, Subaru, Porsche, Infiniti, Tesla. Bunların bir kısmı bilinçli olarak kapsam dışı
sayılabilir (Porsche, Tesla, Infiniti gibi niş veya çok pahalı olanlar), ama **Dacia,
Jeep, MINI, Lexus, Cupra, MG ve Togg Türkiye ikinci el piyasasında otomatik vitesli
olarak gerçekten yaygın** ve yokluğu bir kapsam boşluğudur.

**Kapsam.**

1. Eksik markaları ve modern kuşağı (2016-2024) kapsayan bir hedef liste çıkar. Her
   yeni araç için `data/cars/<id>.json` kaydı, doğru `engine_id` ve `transmission_id`
   bağlantısıyla birlikte açılır.
2. Yeni motor ailesi veya şanzıman kutusu gerekiyorsa `data/engines.json` /
   `data/transmissions.json` içine önce o kayıt kurulur, temel puanı ve kaynağı verilir;
   araç sonra bağlanır. **Ters sırada yapılırsa depo doğrulamadan geçmez.**
3. Hibrit araçlar için önce bir karar gerekiyor: `fuel` alanı bugün yalnızca
   `Dizel` / `Benzin` kabul ediyor. Hibrit eklenecekse şema genişletilmeli ve bunun
   `cost` ile `trans` kriterlerini nasıl etkilediği `docs/methodology.md` içinde
   tanımlanmalı. Bu, geri alınması pahalı bir karar olduğu için
   `docs/ARCHITECTURE.md`'ye MK kaydı olarak yazılmalı.

**Bitmiş sayılma ölçütü.** 2016 sonrası araç sayısı en az 40'a çıkmış, SUV sayısı en az
25 olmuş, listede hiç bulunmayan yaygın markalardan en az beşi temsil edilmiş ve
`validate.py` hâlâ 0 hata veriyor.

---

## Y-02 · Her aracın en az bir gerçek kaynağı olsun, ortalama dörde yaklaşsın

**Öncelik: yüksek.** Projenin bütün iddiası kanıta dayanmak; kanıtsız araç bu iddiayı
zayıflatıyor.

**Bugünkü tablo:**

| Kaynak sayısı | Araç | Durum |
|---:|---:|---|
| 0 | 14 | Hiçbir kanıta bağlı değil, puanlar tamamen değerlendirmeye dayanıyor |
| 1 | 43 | Tek kaynak çürürse dayanaksız kalır |
| 2-3 | 89 | Kısmi |
| 4+ | 8 | Doğrulanmış |

Araç başına ortalama **1.79** kaynak var; hedef 2.0'ın üstü, uzun vadede 4.

**Kaynaksız 14 araç** (öncelikli hedef): `alfa-romeo-mito-1-4`, `audi-a3-8p-2-0-tdi`,
`audi-a4-b5-1-8t-2-4`, `bmw-e87-116i-118i`, `bmw-e90-316i`, `chevrolet-cruze-1-6`,
`citroen-xsara-1-6`, `hyundai-accent-blue-1-6-benzinli`, `hyundai-i40-1-7-crdi`,
`kia-optima-1-7-crdi`, `peugeot-307-1-6`, `skoda-octavia-1-8-tsi`,
`vw-passat-b6-1-8-tsi`, `vw-passat-b7-2-0-tdi`.

**Önemli ayrım.** Motor ve şanzıman ailelerine verilen kaynaklar araç kaydına otomatik
yansımıyor; bunlar ayrı bağlantılar. Bir aracın kendi kaydında da o araca özgü kanıt
olmalı — kullanıcı yorumu, o modele özel arıza derlemesi, Türkiye'ye özgü bir şikayet
örüntüsü. Kullanıcının istediği "her araç için en az bir yorum kapsanmalı" şartı tam
olarak budur.

**Bitmiş sayılma ölçütü.** Kaynaksız araç sayısı sıfır, araç başına ortalama kaynak
2.5'in üstünde.

---

## Y-03 · İki aşamalı kaynak araştırma hattı kur

**Öncelik: yüksek — Y-01 ve Y-02'yi mümkün kılan altyapı budur.**

**Sorun.** Kaynak biriktirmek ile kaynağı puana çevirmek iki farklı iş ve farklı
yetenek istiyor. Birincisi geniş ama sığ bir tarama (çok sayıda aday kaynak bul),
ikincisi dar ama derin bir yargı (bu kaynak hangi iddiayı destekliyor, hangi banda
karşılık geliyor, güven seviyesi ne). İkisini aynı anda yapmak hem yavaş hem hatalı.

**Tasarım.**

1. **Toplama aşaması (hızlı model).** Bir araç veya bileşen listesi verilir; her biri
   için aday kaynaklar aranır ve ham halde bir kuyruk dosyasına yazılır. Bu aşamada
   puan verilmez, yorum yapılmaz. Çıktı biçimi: araç kimliği, bağlantı, yayıncı,
   bulunduğu arama sorgusu, kaynaktan alınan birebir alıntı.
2. **Kuyruk.** `data/queue/` altında, `data/` klasörünün geri kalanından **ayrı**
   tutulur. Kuyruktaki hiçbir kayıt `validate.py` tarafından gerçek veri sayılmaz ve
   sayfaya basılmaz. Bu ayrım kritik: doğrulanmamış bir kaynağın yanlışlıkla yayına
   girmesi, projenin bütün metodolojik temelini geçersiz kılar.
3. **İşleme aşaması (güçlü model).** Kuyruktaki her aday değerlendirilir: kaynak
   gerçekten iddiayı destekliyor mu, güven seviyesi (A/B/C) ne, hangi kritere ve hangi
   banda karşılık geliyor. Kabul edilenler `data/sources.json` ve ilgili araç kaydına
   işlenir; reddedilenler gerekçesiyle birlikte kuyrukta kalır (aynı kaynağın tekrar
   önerilmesini önlemek için).

**Neden kuyruk ayrı tutuluyor.** Bu, `docs/ARCHITECTURE.md` MK-05'teki "kullanıcı kaynak
önerir, puanı bakımcı verir" kuralının otomatik araştırmaya uyarlanmış hali. Kural
değişmiyor: **kaynağı kim getirirse getirsin, puanı metodoloji verir.**

**Bitmiş sayılma ölçütü.** `data/queue/` şeması tanımlı, kuyruğa yazan ve kuyruktan
işleyen iş akışı `docs/` içinde yazılı, en az bir tur uçtan uca çalıştırılmış.

---

## Y-04 · Kaynak öneri formu ve iletişim adresi

**Öncelik: orta. Bedava çözülmesi şart.**

**Amaç.** Kullanıcı bir araca kaynak önerebilsin, öneri bir e-posta adresine düşsün,
bakımcı inceleyip veriye işlesin. Öneri doğrudan veriye yazılmaz (MK-05).

**Bugün elde ne var.** `.github/ISSUE_TEMPLATE/kaynak-onerisi.yml` zaten çalışıyor ve
MK-05'teki üç katmanlı planın birinci katmanı bu. Ama GitHub hesabı olmayan bir
kullanıcı için engel yüksek; site içi form ikinci katman.

### Kullanıcının (yani projenin sahibinin) yapması gerekenler

Aşağıdaki adımların hepsi ücretsizdir ve sunucu gerektirmez.

1. **E-posta adresini aç.** Örneğin `kaynak@aracpuanlama.com` gibi bir adres ya da
   ücretsiz bir sağlayıcıda `aracpuanlama.kaynak@gmail.com` gibi bir hesap. Bu adres
   hem formun hedefi hem sitedeki iletişim adresi olacak.
2. **Formu ileten servisi seç.** Site sunucusuz tek bir HTML dosyası olduğu için form
   gönderimini bir üçüncü tarafın taşıması gerekiyor. Ücretsiz ve kayıt gerektirmeyen
   seçenek **FormSubmit** (`formsubmit.co`): forma `action` olarak e-posta adresi
   yazılır, ilk gönderimde adrese bir onay postası gelir, o onaylandıktan sonra bütün
   gönderimler doğrudan gelen kutusuna düşer. Sınırsız ve ücretsizdir.
   - **Önemli:** ham e-posta adresi HTML kaynağında görünürse spam robotları toplar.
     FormSubmit onay sonrası bir *hashed* uç nokta veriyor; formda adres yerine o
     kullanılmalı.
   - Alternatifler: **Web3Forms** (aylık 250 gönderim, kayıt ister),
     **Google Forms** (sınırsız ama kullanıcıyı siteden çıkarır),
     **Netlify Forms** (yalnızca Netlify'da barındırılırsa, aylık 100).
3. **Siteyi barındır.** Form gönderimi `file://` üzerinden düzgün çalışmaz. **GitHub
   Pages** ücretsizdir ve bu depo zaten GitHub'da; ayarlardan açmak yeterli. Bu ayrıca
   projenin paylaşılabilir bir adrese kavuşması demek.
4. Adresi ve seçilen servisin uç noktasını bakımcıya (yani bu depoda çalışan kişiye)
   ilet; form ve iletişim bölümü ona göre yazılır.

### Depoda yapılacaklar (adres geldikten sonra)

- Araç detay panelinde "bu araca kaynak öner" bağlantısı; aracın kimliği forma gizli
  alan olarak taşınır ki hangi araç için önerildiği kaybolmasın.
- Formun topladığı alanlar: hangi araç, hangi kriter, kaynak bağlantısı, kaynaktan
  birebir alıntı, öneren kişinin adı (isteğe bağlı).
- Spam koruması: FormSubmit'in bal küpü (honeypot) alanı. CAPTCHA eklenmez, kullanıcıyı
  yorar ve bu hacimde gereksizdir.
- Yeni bir ekran: `#iletisim` — e-posta adresi, formun nasıl işlendiği ve öneri
  kabul kriterleri.

---

## Y-05 · Kriter panelini tablonun hemen üstüne al, yatay yerleşim

**Öncelik: orta. Küçük ama günlük kullanımı doğrudan etkileyen bir iş.**

**Sorun.** Liste ekranında hazır ayar düğmeleri, ağırlık toplamı kutusu, arama kutusu ve
sekiz satırlık filtre grubu üst üste diziliyor; tablo ekranın çok aşağısına kayıyor.
Kullanıcı asıl işi (tabloyu okumak) için her seferinde kaydırmak zorunda kalıyor.

**Kapsam.** Ağırlık ayarları ve filtreler tablonun hemen üstünde, yatayda ve mümkün
olduğunca tek satırda toplanmalı. Yer kazanmak için filtre grupları katlanabilir bir
panele alınabilir; ama **varsayılan olarak açık mı kapalı mı olacağı bir tercih
sorusudur ve kullanıcıya sorulmalıdır.** Ağırlık değişiminin tabloyu anında etkilemesi
korunmalı — bugün çalışan bu davranış bozulursa yerleşim kazancı anlamsızlaşır.

**Dikkat.** `templates/screens/30-liste.html` ve `templates/styles.css` değişecek.
`smoke_test.js` içindeki `#sumbox`, `#search`, `.fgroup` seçicileri bu düzenlemeden
etkilenir; testler birlikte güncellenmeli.

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

## Y-07 · Ana giriş ekranı (onboarding sonrası)

**Öncelik: orta.**

**Sorun.** Giriş akışı bittikten sonra kullanıcı doğrudan 154 satırlık tabloya
düşüyor. Tablo güçlü ama karşılama ekranı değil; nereden başlayacağını söylemiyor.

**Kapsam.** `#liste` ile `#giris` arasına bir ana ekran (`#ana`) girer ve varsayılan
rota o olur. İçeriği veriden hesaplanır, elle yazılmaz:

- Veri kapsamının durumu: kaç araç, kaç kaynak, kaç motor ailesi, kaç şanzıman kutusu,
  araç başına ortalama kaynak. (`#metodoloji` ekranındaki gösterge bloğu bunun ilk
  hali; genişletilerek taşınabilir.)
- Hazır giriş yolları: "güvenilirlik öncelikli ilk on", "bütçeye göre başla",
  "sürüş keyfi öncelikli ilk on". Her biri ilgili ağırlık setini uygulayıp listeye
  götürür.
- Öne çıkan bulgular: en yüksek puanlı araçlar ve — daha önemlisi — **en riskli
  bileşenler.** Kullanıcının asıl aradığı bilgi "hangi motor/şanzıman beni yakar"
  sorusunun cevabı; bu, temel puanı en düşük motor ve kutu kayıtlarından doğrudan
  üretilebilir.

**Dikkat.** Varsayılan rota değişince `templates/app/10-yonlendirici.js` içindeki
`DEFAULT_ROUTE` ve `smoke_test.js`'in ilk ziyaret kontrolü birlikte güncellenmeli.

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

Maddeler birbirine bağımlı; şu sıra hem riski hem tekrarı azaltır:

1. **Y-03** (araştırma hattı) — çünkü Y-01 ve Y-02'nin ikisi de buna dayanıyor.
2. **Y-02** (kaynaksız araçları kapat) — hattın ilk gerçek yükü, aynı zamanda testi.
3. **Y-01** (listeyi genişlet) — hat çalışır durumdayken yeni araç eklemek çok daha ucuz.
4. **Y-05 + Y-06** (yerleşim ve şeffaflık) — küçük, bağımsız, günlük kullanımı hemen
   iyileştiriyor.
5. **Y-04** (form) — kullanıcının e-posta adresini kurmasını bekliyor, o yüzden dışarıya
   bağımlı; hazır olunca araya girebilir.
6. **Y-07 + Y-09** (ana ekran ve tema) — birlikte yapılması gereken görsel iş.
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
- `arac-puanlama.html` üretilmiş dosyadır, elle düzenlenmez.
- Kimlikler kalıcıdır; bir araç, motor veya kutu kimliği verildikten sonra değişmez.
