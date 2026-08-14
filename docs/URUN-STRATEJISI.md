# Ürün, açık kaynak ve pazarlama stratejisi

**Sürüm:** S1 · **Tarih:** 13 Ağustos 2026 · **Kapsam:** GitHub entegrasyonu, gelir modelleri, içerik ve pazarlama, teknik büyüme yol haritası

Bu belge `docs/ROADMAP.md`'nin ticari eşdeğeridir. ROADMAP "sıradaki mühendislik işi ne"
sorusunu cevaplıyor; bu belge "bu iş kime, neden ve nasıl değerli" sorusunu cevaplıyor.
İkisi ayrı tutuldu çünkü karar süreçleri farklı: bir mühendislik maddesi doğrulanabilir,
bir pazarlama fikri ancak denenebilir.

Fikirler burada süzülmeden yazıldı, ama **süzgeç de yazıldı**. Her fikrin yanında
uygulanabilirlik seviyesi, beklenen getirisi ve bilinen riski duruyor. Bir fikrin bu
belgede olması yapılacağı anlamına gelmez; yapılıp yapılmayacağına karar verirken
gerekçenin elde olması anlamına gelir.

## Uygulanabilirlik ölçeği

| Seviye | Anlamı |
|---|---|
| **F1** | Bugün yapılabilir. Elimizdeki veri ve araçlar yeterli, iş birkaç saat ile birkaç gün arası. |
| **F2** | Kısa vade (2–6 hafta). Yeni kod veya yeni içerik gerekiyor ama dış bağımlılık yok. |
| **F3** | Orta vade (2–4 ay). Yeni veri toplama, yeni yetenek veya süreklilik gerektiren operasyon. |
| **F4** | Uzun vade veya belirsiz. Dış bağımlılık, hukuki kapı ya da doğrulanmamış varsayım içeriyor. |

---

## 1. Yönetici özeti — üç cümlelik tez

Bu projenin satılabilir asıl varlığı araç listesi değil, **motor ve şanzıman ailesi
düzeyinde yapılandırılmış, kaynaklı arıza sicilidir**; araç listesi rakiplerin de
kolayca kopyalayabileceği bir metrik, arıza sicili ise dört aylık araştırmanın birikimi.

Bugün bu birikimin neredeyse tamamı **görünmez** durumda: 83 bin kelimelik özgün Türkçe
analiz, arama motorlarının tek bir sayfa olarak gördüğü 1,2 MB'lık tek bir HTML dosyasının
içinde duruyor. Bu, stratejinin en büyük ve en ucuz kaldıracıdır.

Para kazanmanın en gerçekçi sırası ürün satmakla başlamıyor: **önce görünürlük (SEO ve
içerik), sonra güven (açık kaynak ve şeffaf yöntem), sonra dönüşüm (kişiye özel rapor),
en sonda ölçek (API ve kurumsal).** Bu sırayı bozmak — örneğin trafik yokken ödeme
altyapısı kurmak — en sık yapılan hata olur.

---

## 2. Elimizde gerçekte ne var?

Strateji, varlığın dürüst envanteriyle başlar. 13 Ağustos 2026 itibarıyla:

| Varlık | Miktar | Ticari anlamı |
|---|---:|---|
| Araç kaydı | 278 | Giriş bileti; tek başına farklılaştırıcı değil |
| Motor ailesi kaydı | 104 | **Asıl varlık.** Türkçede yapılandırılmış eşdeğeri yok |
| Şanzıman ailesi kaydı | 53 | **Asıl varlık.** Otomatik şanzıman odağı Türkiye'de nadir |
| Yapılandırılmış bilinen arıza kaydı | 166 | Her biri bir içerik parçası, bir uyarı, bir satır ürün |
| Kaynak künyesi | 314 | Kanıt zinciri; iddiaların denetlenebilirliği |
| Kanıt (`evidence`) bloğu | 972 | Puanın neden o puan olduğunun yazılı gerekçesi |
| Özgün Türkçe analiz metni | ~83.000 kelime | Bir kitap hacminde, tamamı özgün ve kaynaklı |
| "Doğrulanmış" araç (4+ kaynak) | 236 / 278 | Kalite iddiasının ölçülebilir kanıtı |
| Tarihli piyasa fiyatı | 19 araç | Yeni katman; büyütülmesi gereken |

**Bu envanterin okunuşu.** 278 araç, arabam.com'un yüz binlerce ilanı yanında hiçbir şey.
Ama arabam.com bir aracın DQ200 şanzımanının mekatronik basınç haznesinin neden çatladığını
söylemiyor, sahibinden.com bir motorun triger zincirinin arkada mı önde mi olduğunu
söylemiyor. **Onlar "ne satılıyor" sorusunu cevaplıyor; bu proje "hangisini alma ve neden"
sorusunu cevaplıyor.** İki ürün rakip değil, tamamlayıcı — ve ikincisinin Türkçede ciddi
bir karşılığı yok.

**Pazarın büyüklüğü.** 2025'te Türkiye'de ikinci el otomobil pazarı yüzde 6,6 artışla
7,5 milyon adedi aşarak rekor kırdı. Bu, yılda milyonlarca kez sorulan "bunu almalı mıyım"
sorusu demektir. Alıcıların çok küçük bir yüzdesine ulaşmak bile anlamlı bir iş kurar.

---

## 3. En büyük ve en ucuz kaldıraç: içeriği görünür yapmak

> **Durum güncellemesi (2026-08-13):** bu bölümün önerdiği iş **yapıldı**. `scripts/build_pages.py`
> 435 statik sayfa üretiyor, `sitemap.xml` ve `robots.txt` yayında, her sayfa araca özgü başlık,
> açıklama, canonical ve JSON-LD taşıyor. Aşağıdaki "bugünkü durum" dökümü, işin *öncesindeki*
> tabloyu anlatıyor ve gerekçenin kaydı olarak bırakıldı. Kalan tek adım, sayfaların Google
> Search Console'a gönderilmesi; o, depo sahibinin hesabıyla yapılacak bir iş.

### 3.1 Bugünkü durum, açıkça

`index.html` tek bir dosya ve ekranlar arası geçiş adres çubuğundaki `#liste`, `#kiyaslama`
gibi çapa (hash) adlarıyla yapılıyor. Bu tasarım MK-07'de bilinçli olarak seçildi ve
uygulama davranışı açısından hâlâ doğru. Ama arama motoru açısından sonucu şudur:

- Google'ın gördüğü sayfa sayısı: **1**
- İndekslenebilir araç sayfası: **0**
- `meta description`: **yok**
- `sitemap.xml` / `robots.txt`: **yok**
- Open Graph / Twitter kartı (paylaşım önizlemesi): **yok**
- Sayfa başlığı: "Araç Puanlama" — hiçbir arama sorgusuyla eşleşmiyor

Yani 83 bin kelime, hiç kimsenin bulamayacağı bir yerde duruyor.

### 3.2 Öneri: araç başına statik sayfa üretimi

**F1–F2 · Getiri: çok yüksek · Risk: düşük**

`scripts/build.py` bugün tek bir `index.html` üretiyor. Aynı betiğe ikinci bir çıktı
biçimi eklenir: her araç için `/arac/<id>.html`, her motor ailesi için `/motor/<id>.html`,
her şanzıman ailesi için `/sanziman/<id>.html`. Bu, MK-01'i bozmaz — üretilen dosya yine
türetilmiş çıktıdır ve `data/` tek doğruluk kaynağı olarak kalır. MK-02 zaten bu genişlemeyi
öngörüyor: "derleme adımında yeni bir çıktı biçimi üretmek".

Üretilecek sayfa sayısı bugünkü veriyle **435** (278 araç + 104 motor + 53 şanzıman) ve her
biri özgün, kaynaklı Türkçe metin taşıyor.

Hedeflenecek arama sorguları, Türkiye'de gerçekten aranan kalıplar:

| Sayfa türü | Hedef sorgu kalıbı | Örnek |
|---|---|---|
| Araç | `<model> alınır mı` | "Skoda Octavia 1.6 TDI alınır mı" |
| Araç | `<model> kronik sorunları` | "Passat B7 kronik sorunları" |
| Motor ailesi | `<motor kodu> sorunları` | "EA189 sorunları", "N47 triger zinciri" |
| Şanzıman | `<kutu> arıza` | "DQ200 mekatronik arızası", "AL4 şanzıman" |
| Karşılaştırma | `<A> mı <B> mi` | "Octavia mı Passat mı" |

Motor ve şanzıman sayfaları burada özellikle değerli: "N47 triger zinciri" arayan kişi
zaten sorunun farkında ve satın alma kararına çok yakın. Bu, dönüşümü en yüksek trafiktir.

**Somut iş kalemi:** `Y-11 · Statik sayfa üretimi ve SEO temeli` — **uygulandı.** Üretim
`build.py`'ye eklenmedi, ayrı bir `scripts/build_pages.py` dosyasına yazıldı ki çalışan
`index.html` üretimi riske girmesin. `Vehicle` JSON-LD eklendi; `FAQPage` şeması henüz
eklenmedi ve açık bir iş olarak duruyor. Nihai bitmiş sayılma ölçütü — Search Console'da
400+ sayfanın indekslenmiş görünmesi — hâlâ geçerli ve gönderim adımını bekliyor.

### 3.3 Yapılandırılmış veri (JSON-LD) ile zengin sonuç

**F2 · Getiri: orta-yüksek · Risk: düşük**

Her araç sayfasına `Vehicle` ve `FAQPage` şeması gömülürse arama sonucunda yıldız, soru-cevap
açılımı ve fiyat bandı görünebilir. Elimizdeki veri buna hazır: puanlar, fiyat bandı, üretim
yılları, motor hacmi ve gücü zaten yapılandırılmış. `FAQPage` içeriği de hazır — her
`evidence.reasoning` bloğu zaten "bu puan neden böyle" sorusunun cevabı.

### 3.4 Sayfa hızı ve "platformun hızlı tepki vermesi"

**F2 · Getiri: orta · Risk: düşük**

Bugün tek dosya 1,2 MB ve araç sayısı büyüdükçe doğrusal büyüyor. 1.000 araçta yaklaşık
4 MB olur; mobil bağlantıda kabul edilemez. Üç aşamalı çözüm, hepsi MK-01 ve MK-02 ile uyumlu:

1. **Veriyi kabuktan ayır (F2).** Uygulama kabuğu (HTML+CSS+JS) ayrı, veri ayrı bir
   `data.json` olarak yüklensin. Kabuk anında açılır, veri arkadan gelir.
2. **Liste için özet, detay için tam kayıt (F2).** Liste ekranı araç başına yalnızca 10-12
   alan istiyor; `evidence` metinleri (972 blok, veri hacminin büyük kısmı) yalnızca detay
   açıldığında yüklensin.
3. **Statik sayfalar zaten hızlıdır (F1).** §3.2'deki araç sayfaları tek başına küçük
   dosyalar olduğu için ilk açılış süresi sorunu doğal olarak çözülür.

**Ölçüm olmadan iyileştirme yapılmamalı.** Önce Lighthouse ve gerçek cihaz ölçümü alınır,
sonra hedef konur. Bugünkü duman testi (49 kontrol) sayfanın *çalıştığını* doğruluyor ama
*hızını* ölçmüyor; duman testine bir performans bütçesi kontrolü eklenmesi F2 işidir.

---

## 4. GitHub stratejisi: açık kaynak ne kadar açılmalı?

### 4.1 Temel gerilim

Depo bugün de GitHub'da ve herkese açık. Soru "açılsın mı" değil, **"neyin açık kalacağı
bilinçli mi"**. Açıklığın iki gerçek getirisi var: güvenilirlik (yöntemi gizleyen bir
puanlama sistemine kimse güvenmez) ve katkı (kullanıcılar hata bulur, kaynak önerir).
Bir gerçek riski var: kataloğun tamamı kopyalanıp aynı içerikle rakip bir site açılabilir.

### 4.2 Önerilen model: açık yöntem, açık çekirdek veri, ayrı ticari katman

**F1 (lisans kararı) + F2 (uygulama) · Getiri: yüksek · Risk: orta**

| Katman | Açıklık | Gerekçe |
|---|---|---|
| Yöntem, kod, şema, denetim (`scripts/`, `docs/`, `data/schema/`) | **Tam açık** (MIT veya Apache-2.0) | Güvenilirliğin kaynağı bu. Gizlenirse ürünün tek iddiası çöker. |
| Bileşen sicili ve araç kayıtları (`data/`) | **Açık ama paylaşımlı lisans** (CC BY-SA 4.0) | Kopyalayan, türev çalışmasını aynı lisansla açmak ve atıf vermek zorunda kalır. Sessiz ticari klonu caydırır. |
| Tarihli piyasa gözlemleri (`data/market/`) | **Açık, sınırlı** | Toplu istatistik açık kalır; ölçüm sıklığı ve tazeliği ticari katmanın avantajıdır. |
| Kişiye özel rapor üretimi, kurumsal panel, API | **Kapalı** | Gelirin geldiği yer burası; veri değil **hizmet** satılıyor. |

**Neden CC BY-SA?** Paylaşımlı (share-alike) lisans, veriyi alıp kapalı bir ürüne gömmeyi
hukuken zorlaştırır: türev çalışma da aynı lisansla açılmak zorundadır. Bu, akademik ve
gazetecilik kullanımını serbest bırakırken sessiz ticari klonu caydırır. Kod tarafında
paylaşımlı lisans gereksiz — orada asıl amaç benimsenme ve güven.

**Uyarı, dürüstçe:** Lisans caydırır, engellemez. Türkiye'de veri tabanı hakkı ve lisans
ihlali takibi pratikte zordur. Asıl koruma hukuki değil operasyoneldir: **tazelik**.
Kopyalanan katalog kopyalandığı günün fotoğrafıdır; haftalık güncellenen bir kaynak altı
ayda kopyayı işe yaramaz hale getirir. Bu yüzden güncelleme sıklığı bir pazarlama
özelliğidir, sadece bir bakım işi değil.

### 4.3 Depoyu bir ürün vitrinine çevirmek

**F1 · Getiri: orta · Risk: yok**

Bugünkü `README.md` bir iç belge gibi. GitHub deposu aslında ilk temas noktasıdır ve şunlar
eksik:

- **Rozet satırı** — araç sayısı, doğrulanmış oran, son güncelleme, denetim durumu. Bunlar
  `validate.py --json` çıktısından otomatik üretilebilir (F1).
- **Ekran görüntüsü ve canlı bağlantı** — deposu açan kişi ürünü 5 saniyede görmeli.
- **"Neden var" paragrafı** — bugün README teknik başlıyor; önce sorun anlatılmalı.
- **Katkı rehberi (`CONTRIBUTING.md`)** — 2026-08-13'te yazıldı. Katkının nasıl işlediğini,
  kaynak güven seviyelerini ve üretilmiş dosyalara dokunulmama kuralını anlatıyor.
- **Konu şablonları (`.github/ISSUE_TEMPLATE/`)** — kaynak öneri şablonu **zaten kuruluydu**
  (bu belgenin ilk sürümünde yanlışlıkla "kurulmadı" yazılmıştı); üstüne "hata bildir" ve
  "araç öner" şablonları eklendi. Arayüzdeki "kaynak öner" formunun (Y-04) gönderim uç
  noktası hâlâ tanımlı değil ve **GitHub Issues bu uç nokta olabilir** — sıfır altyapı
  gerektiren, hâlâ açık bir F1 işi.
- **`CITATION.cff`** — akademik atıf dosyası. Bir tez veya makale bu veriyi kullandığında
  atıf verir; bu hem geri bağlantı hem güvenilirlik getirir.

### 4.4 GitHub Actions ile sürekli denetim

**F1 · Getiri: orta · Risk: yok · durum: büyük ölçüde kurulu**

Bu belgenin ilk sürümünde "bugün elle çalıştırılıyor" deniyordu; **yanlıştı** — CI iş akışı
zaten `validate.py`, `build.py --check` ve `smoke_test.js` çalıştırıyordu. 2026-08-13'te
buna `build_pages.py --check` ve `consistency.py` adımları eklendi. Ek olarak haftalık bir zamanlanmış iş,
`fiyat-bandi-bayat` uyarısı üreten araçları listeleyip otomatik bir konu (issue) açabilir —
yani veri tazeliği kendi kendini hatırlatır.

### 4.5 Açık veriyi bir dağıtım kanalı olarak kullanmak

**F2–F3 · Getiri: orta · Risk: düşük**

Veri yalnızca depoda durmak zorunda değil. Aynı veriden türetilebilecek dağıtım biçimleri:

- **Hugging Face Datasets / Kaggle'da yayın (F2).** Veri bilimi topluluğu Türkçe otomotiv
  veri seti arıyor ve neredeyse hiç bulamıyor. Buradan gelen görünürlük, geri bağlantı ve
  "bu veriyi kim üretti" merakı doğrudan siteye trafik getirir.
- **Salt okunur SQLite yayını (F2).** MK-02 bunu zaten ölçek çözümü olarak öngörüyor;
  aynı dosya aynı zamanda geliştiricilere ve analistlere hitap eden bir dağıtım biçimidir.
- **Wikipedia/Vikipedi katkısı (F3, dikkatli).** Motor ailesi maddelerine kaynaklı bilgi
  eklemek meşru bir katkıdır, ama kendi sitesini kaynak göstermek reddedilir ve itibar
  kaybettirir. Yalnızca birincil kaynaklara atıfla, tanıtım amacı gütmeden yapılmalı.

---

## 5. Gelir modelleri — fikir balonları ve süzgeç

Aşağıdaki fikirler ham haliyle listelendi, sonra süzüldü. Sıralama beklenen getiri/çaba
oranına göre.

### 5.1 Kişiye özel analist raporu — **birincil öneri**

**F2 · Getiri: yüksek · Risk: düşük**

Kullanıcı bütçesini, kullanım biçimini (şehir içi / uzun yol), önceliklerini ve varsa
aday listesini veriyor; karşılığında kaynaklı, ağırlıkları görünür bir kısa liste ve her
aday için risk notu alıyor. Bu, `veri_urun_stratejisi.md`'nin de önerdiği ürün ve mevcut
puanlama motorunun doğal çıktısı.

**Fiyatlandırma çapası, gerçek piyasadan:** Türkiye'de oto ekspertiz hizmeti 2026 itibarıyla
4.000–10.000 TL bandında. Ekspertiz **tek bir aracı** fiziksel olarak inceliyor; bizim
raporumuz **hangi araca gidileceğini** belirliyor ve ekspertize gitmeden önceki adımı
çözüyor. Bu konumlandırmayla 750–2.000 TL bandı savunulabilir: ekspertizin belirgin altında,
ama ciddi bir araştırma emeğinin karşılığı. Yanlış araca yapılan tek bir ekspertiz ücreti
bile raporun bedelini karşılıyor — satış argümanı budur.

**Neden bu ürün önce gelmeli:** ödeme altyapısı dışında yeni teknoloji gerektirmiyor,
marjı yüksek, ve her rapor bir sonraki rapor için veri üretiyor (hangi araçlar soruluyor,
hangi bütçe bandı yoğun).

### 5.2 "Bu ilanı değerlendir" — tek ilan risk raporu

**F3 · Getiri: yüksek · Risk: orta**

Kullanıcı bir ilan bağlantısı veya ilan bilgilerini yapıştırıyor; sistem aracı bileşen
siciline eşleyip "bu motorda şu yaşta şu arıza bekleniyor, sor şunu, kontrol ettir şunu"
diyen bir kontrol listesi üretiyor. Fiyatı da tarihli piyasa bandıyla karşılaştırıyor.

**Risk ve sınır:** İlan sayfasını otomatik okumak (kazıma) hem teknik hem hukuki olarak
sorunlu; `veri_urun_stratejisi.md` bunu açıkça uyarıyor ve arabam.com'un robots dosyası
arama yollarını otomatik erişime kapatıyor. **Çözüm: bağlantıyı okumak yerine kullanıcının
kendi girdiği bilgiyi kullanmak** (marka, model, yıl, kilometre, motor, fiyat). Bu, hukuki
kapıyı tamamen aşar ve ürünün özünü hiç bozmaz.

### 5.3 İçerik ve topluluk gelirleri (YouTube, Reels, ortaklık)

**F2 · Getiri: orta, gecikmeli · Risk: düşük**

Ayrıntısı §6'da. Kısa vadede doğrudan gelir değil, **trafik ve güven** üretir; asıl işi
5.1'deki ürüne kullanıcı taşımaktır.

### 5.4 Galeri ve kurumsal (B2B) katman

**F3–F4 · Getiri: yüksek ama belirsiz · Risk: orta**

Galeriler ve filo alıcıları için toplu değerlendirme, stok risk analizi ve fiyat konumlama
paneli. Cazip, çünkü ödeme gücü yüksek ve tekrarlayan gelir. Ama iki gerçek engel var:
(1) galerinin asıl derdi "hangi araç iyi" değil "hangi araç hızlı döner" — bu farklı bir
veri seti (devir hızı) gerektiriyor ve elimizde yok; (2) kurumsal satış, ürün satışından
farklı bir operasyon ve tek kişilik bir ekibi hızla tüketir. **Öneri: bu katmanı bilinçli
olarak ertelemek** ve ancak bireysel ürün oturduktan sonra açmak.

### 5.5 Lisanslı veri / API

**F4 · Getiri: orta · Risk: yüksek (hukuki kapı)**

`veri_urun_stratejisi.md` bunu zaten ayrı bir hak kapısının arkasına koymuş ve haklı: ham
veri satmak, kaynakların satır bazında kullanım hakkının incelenmesini gerektirir. Bugünkü
314 kaynağın büyük kısmı forum ve ticari blog; bunlardan türetilmiş **kendi sentezimizi**
satmak ile kaynakların içeriğini yeniden dağıtmak arasındaki çizgi teknik değil hukuki bir
konudur. **Öneri: bu kapı, bir uygulayıcıyla görüşülene kadar kapalı kalsın.** Bu arada
"veri" değil "analiz" satmak aynı geliri hukuki riske girmeden üretebilir.

### 5.6 Reddedilen veya ertelenen fikirler, gerekçeleriyle

Bir stratejinin değeri neyi yapmayacağını da söylemesindedir.

| Fikir | Karar | Gerekçe |
|---|---|---|
| İlan platformu kurmak | **Reddedildi** | Ağ etkisi gerektiriyor, sermaye yoğun, mevcut oyuncular yerleşik. Bizim avantajımız orada değil. |
| Ekspertiz hizmeti vermek | **Reddedildi** | Fiziksel operasyon, şehir şehir kadro, tamamen farklı bir iş. Ortaklık olarak düşünülebilir, sahiplik olarak hayır. |
| Araç değerleme (fiyat tahmini) motoru | **Ertelendi (F4)** | Gerçekleşen satış fiyatı verisi olmadan güvenilir değerleme yapılamaz; elimizde yalnızca istenen fiyat var ve bu ikisi aynı şey değil. |
| Kullanıcı yorumu / puanlama toplama | **Ertelendi (F3)** | Denetimsiz katkı, kanıt zincirinin güvenilirliğini bozar (MK-05). Önce moderasyon akışı gerekiyor. |
| Mobil uygulama | **Ertelendi (F4)** | Web zaten mobil çalışıyor; uygulama mağazası bakım yükü getirir ve şu an çözdüğü bir sorun yok. |
| LPG/elektrikli kapsama genişleme | **Reddedildi** | MK-13 kalıcı kapsam kararı. Kapsamı daraltmak konumlandırmayı netleştiriyor. |

---

## 6. Pazarlama ve içerik: veriyi içeriğe çeviren makine

### 6.1 Merkezî fikir: içerik bir derleme çıktısıdır

**F2 · Getiri: yüksek · Risk: düşük**

Bu, belgedeki en özgün öneri. Elimizde **166 yapılandırılmış bilinen arıza kaydı** var ve
her biri şu alanları taşıyor: hangi bileşen, hangi arıza, hangi kilometrede başlıyor, ne
sıklıkta, ne kadar ağır, hangi kaynak. Bu, bir içerik takviminin ham maddesidir.

Öneri: `scripts/build_content.py` yazılır ve `data/`'dan içerik taslakları üretir — tıpkı
`build.py`'nin sayfa üretmesi gibi. MK-01 bozulmaz, içerik de türetilmiş çıktıdır.

Üretilecek biçimler:

- **Kısa video senaryosu (Reels/Shorts/TikTok):** 30–45 saniyelik sabit kurgu — "Bu aracı
  almadan önce şunu bil" → arıza → hangi kilometrede → nasıl kontrol edilir → kaynak.
- **Kaydırmalı görsel (carousel):** motor ailesi kartı; bilinen arızalar, bakım kalemi,
  puan ve gerekçesi.
- **Tweet dizisi:** bir şanzıman ailesinin hikâyesi; neden bu kutu bu kadar şikayet alıyor.
- **Blog/SEO yazısı:** §3.2'deki statik sayfaların uzun biçimi.

**Neden bu güçlü:** İçerik üretiminin en pahalı kısmı araştırmadır ve o araştırma zaten
yapılmış, kaynaklanmış ve yapılandırılmış durumda. 166 kayıt, haftada üç paylaşımla bir
yıldan fazla içerik demektir — ve her paylaşımın altında gerçek bir kaynak var, bu da
Türkiye otomotiv içeriğinde nadir bir konumlandırma sağlar.

### 6.2 Kanal kanal strateji

**YouTube Shorts ve Instagram Reels (F2 · getiri yüksek).** Türkiye otomotiv YouTube
ekosistemi büyük ve yerleşik: Doğan Kabak 1,5 milyon, Otopark.com 431 bin, Otomobil Dünyam
268 bin abone. Bu kanallarla **test sürüşü ve inceleme alanında rekabet edilemez** — kadro,
ekipman ve araç erişimi gerekiyor. Ama hiçbiri "veri tabanından gelen, kaynaklı, sayısal
arıza uyarısı" yapmıyor. Boşluk burada: yüz yok, araç yok, sadece veri ve grafik. Üretim
maliyeti düşük, ölçeklenebilir ve doğrudan siteye yönlendirir.

**X/Twitter (F1 · getiri orta).** Otomotiv Türkiye topluluğu burada tartışıyor. En işe
yarayacak biçim: "bugünün arıza kaydı" formatında günlük tek paylaşım ve tartışmalı
sorulara veriyle cevap vermek. Twitter'ın asıl getirisi trafik değil **otorite**: bir
tartışmada kaynaklı cevap veren hesap, zamanla başvurulan hesap olur.

**Ekşi Sözlük / Donanım Haber / Technopat (F1 · getiri orta, dikkat gerektirir).** Bu
mecralar zaten kaynaklarımızın bir kısmının geldiği yer ve buradaki kullanıcılar tam
hedef kitle. **Ama açık reklam burada geri teper.** Tek meşru yol: gerçekten cevap veren,
kaynak gösteren, ürünü ancak sorulduğunda anan katılım. Sabırlı ve yavaş bir kanal.

**Reddit r/Turkey, r/otomobil (F1 · getiri düşük-orta).** Küçük ama nitelikli. Açık veri
setinin yayınlanması burada iyi karşılanır.

**E-posta listesi (F2 · getiri orta, uzun vadede yüksek).** Sosyal medya erişimi ödünç
alınmış bir varlıktır; e-posta listesi sahip olunan tek kanaldır. "Aylık fiyat güncellemesi
ve yeni arıza kayıtları" bülteni, hem tazeliği hem ürünü tanıtır.

### 6.3 Reklam şeffaflığı — ihmal edilemez kural

Ticaret Bakanlığı'nın sosyal medya etkileyicileri kılavuzu, ücretli iş birliği, sponsorluk,
hediye veya yönlendirme geliri içeren içeriğin ticari niteliğinin açıkça belirtilmesini
zorunlu kılıyor. Bu proje ilerde ortaklık geliri (ör. ekspertiz yönlendirmesi) alırsa,
her içerikte bu açıkça yazılmalıdır. Bu bir tercih değil, yükümlülük — ve zaten bu
projenin şeffaflık iddiasıyla birebir uyumlu.

### 6.4 Ölçüm: neyin işe yaradığını nasıl bileceğiz

Pazarlama, ölçülmezse harcamadır. Baştan kurulacak asgari ölçüm:

| Metrik | Neden | Araç |
|---|---|---|
| İndekslenen sayfa sayısı | SEO temelinin çalışıp çalışmadığı | Google Search Console (ücretsiz) |
| Sorgu bazlı tıklama | Hangi araç/motor sayfası çekiyor | Search Console |
| Sayfa → rapor talebi dönüşümü | İçeriğin ürüne bağlanıp bağlanmadığı | Basit olay sayacı |
| Depo yıldızı ve çatallama | Teknik güvenilirlik sinyali | GitHub |
| Bülten kayıt oranı | Sahip olunan kanalın büyümesi | E-posta aracı |

**Gizlilik notu:** KVKK kapsamında çerez ve izleme için aydınlatma gerekiyor. En basit ve
en savunulabilir yol, kişisel veri toplamayan, çerezsiz bir sayaç kullanmak.

---

## 7. Teknik yol haritası — ürünü taşıyacak altyapı

Bu bölüm ROADMAP'e girecek maddelerin ticari gerekçesini taşıyor.

| # | İş | Seviye | Neden ticari olarak önemli |
|---|---|---|---|
| Y-11 | Statik sayfa üretimi + SEO temeli | F1–F2 | Görünmez içeriği görünür yapar. Tek başına en yüksek getirili iş. |
| Y-12 | İçerik üretim betiği (`build_content.py`) | F2 | 166 arıza kaydını içerik takvimine çevirir. |
| Y-13 | GitHub Actions denetim + katkı şablonları | F1 | Katkı kapısını açar (MK-05 birinci katman), güven rozeti üretir. |
| Y-14 | Veri/kabuk ayrımı ve tembel yükleme | F2 | Ölçek büyüdükçe hızın çökmesini engeller. |
| Y-15 | Fiyat ölçümünün tekrarlanabilir hale gelmesi | F2–F3 | Tazelik, kopyalanamayan tek avantaj. Bugün 19/278 araç tarihli. |
| Y-16 | Boş ağırlık verisinin doldurulması (88 araç) | F2 | `fun` kapsamını 163'ten 251'e çıkarır; tek veri kalemi, çift kapsam. |
| Y-17 | Kişiye özel rapor üretimi + ödeme | F3 | İlk gerçek gelir kalemi. |
| Y-18 | `liq` için doğru sayım protokolü | F3 | MK-20'de reddedilen ölçümün doğru biçimde kurulması. |

**Sıralamanın mantığı:** Y-11 ve Y-13 önce, çünkü ikisi de bugünkü veriyle yapılabiliyor ve
biri trafiği, diğeri katkıyı açıyor. Y-17 (ödeme) bilinçli olarak sonda: trafik olmadan
kurulan ödeme altyapısı boş bir dükkândır.

---

## 8. Riskler ve dürüst sınırlar

| Risk | Olasılık | Etki | Azaltma |
|---|---|---|---|
| Kaynak hakları satır bazında incelenmemiş | Yüksek | Yüksek (ham veri satışını engeller) | Analiz satmak, veri satmamak; API kapısını kapalı tutmak |
| Tek kişilik ekip, kapasite sınırı | Kesin | Yüksek | Otomasyon (içerik ve denetim betikleri), B2B'yi ertelemek |
| Fiyat verisinin bayatlaması | Yüksek | Orta | `fiyat-bandi-bayat` uyarısı kuruldu; ölçümün tekrarı Y-15 |
| Katalog kopyalanması | Orta | Orta | Paylaşımlı lisans + tazelik avantajı |
| Puanların "kesin doğru" sanılması | Orta | Yüksek (itibar) | Yöntem sayfası, güven seviyeleri ve uyarı metinleri zaten var; korunmalı |
| Mesafeli satış / KVKK / ETBİS yükümlülükleri | Kesin (satış başlarsa) | Yüksek | Ödeme almadan önce sözleşme ve ön bilgilendirme akışı kurulmalı |
| İstenen fiyatın satış fiyatı sanılması | Orta | Orta | `price_semantics` alanı bunu veri düzeyinde işaretliyor; arayüzde de yazılmalı |

**Belgenin kendi sınırı:** Bu bir hukuki görüş değildir. Canlı satış öncesinde mesafeli
sözleşme, cayma/iade, KVKK, vergi ve kaynak kullanım modeli bir Türkiye e-ticaret/telif
uygulayıcısıyla kontrol edilmelidir.

---

## 9. Doksan günlük somut plan

Her hafta bir çıktı bırakacak şekilde, en ucuz kaldıraçtan başlayarak.

**1.–2. hafta — görünürlük temeli.** Y-11'in ilk yarısı: `build.py` araç başına statik
sayfa üretsin, `sitemap.xml` ve `robots.txt` eklensin, her sayfaya başlık ve açıklama
girsin. Search Console'a kayıt. *Bitmiş sayılma: 400+ sayfa gönderildi.*

**3.–4. hafta — depo vitrini ve katkı kapısı.** Y-13: README yeniden yazılır, rozetler
eklenir, üç konu şablonu ve `CONTRIBUTING.md` kurulur, GitHub Actions denetimi açılır.
*Bitmiş sayılma: dışarıdan biri kaynak önerisini beş dakikada gönderebiliyor.*

**5.–7. hafta — içerik makinesi.** Y-12: `build_content.py` ilk sürümü, 166 arıza
kaydından ilk 20 içerik taslağı, iki kanalda (Shorts + X) haftada üç paylaşımla yayın
başlangıcı. *Bitmiş sayılma: dört hafta ileriye dolu içerik takvimi.*

**8.–10. hafta — veri tazeliği ve kapsam.** Y-16 (88 araca boş ağırlık) ve Y-15'in ilk
turu (fiyat ölçümünün tekrarlanabilir hale getirilmesi). *Bitmiş sayılma: `fun` kapsamı
251/278, tarihli fiyat 19'dan belirgin biçimde yukarıda.*

**11.–13. hafta — ilk ürün denemesi.** Y-17'nin en yalın hali: ödeme altyapısı kurmadan,
elle karşılanan 10 adet kişiye özel rapor. Amaç gelir değil **öğrenme**: insanlar ne
soruyor, hangi bütçe bandında, raporun hangi kısmını okuyor. *Bitmiş sayılma: 10 rapor
teslim edildi ve geri bildirim yazıya döküldü.*

**Doksan gün sonunda beklenen durum:** ölçülebilir organik trafik, çalışan bir içerik
hattı, açık bir katkı kapısı ve gerçek kullanıcılardan gelmiş ürün geri bildirimi.
Bunların hiçbiri büyük bir yatırım gerektirmiyor; hepsi bugün elimizde olan veriden
türüyor.

---

## 10. Bir cümlelik hatırlatma

Bu projenin rekabet avantajı ne araç sayısı ne de arayüzdür; **her puanın arkasında yazılı
bir gerekçe ve erişilebilir bir kaynak olmasıdır.** Büyüme kararlarının hiçbiri bu özelliği
zayıflatmamalı — çünkü zayıfladığı gün ürün, kolayca kopyalanabilir bir listeye dönüşür.
