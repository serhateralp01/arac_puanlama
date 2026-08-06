/* ---------- dışarıya açılan uçların yapılandırması ---------- */
/* Sitenin dışarıyla konuştuğu iki nokta var: kaynak öneri formunun gönderim uç
   noktası ve iletişim ekranında yazan e-posta adresi. İkisi de tek bir yerde
   tanımlansın diye buraya alındı; böylece adres değiştiğinde arayüz kodunun
   içinde adres aramak gerekmiyor.

   Her iki değişken de boş bırakıldığı sürece sayfa çalışmaya devam eder ve
   kullanıcıya durumun neden böyle olduğu açıkça yazılır. Sessizce başarısız olan
   bir form, hiç olmayan bir formdan daha kötüdür; hiçbir yere ulaşmayan bir
   iletişim adresi de öyle.

   FORM_ENDPOINT — kaynak öneri formunun gönderileceği adres. Form, sunucusuz bir
   sayfadan e-posta göndermek için FormSubmit'i (formsubmit.co) kullanıyor; servis
   kayıt gerektirmiyor, ücretsiz ve sınırsız. İki biçim de çalışır:

     'https://formsubmit.co/ornek@ornek.com'     (ilk gönderimde onay postası gelir)
     'https://formsubmit.co/a1b2c3d4e5f6...'     (onay sonrası verilen gizli uç nokta)

   İkinci biçim tercih edilmeli: ham e-posta adresi HTML kaynağında görünmezse spam
   robotları adresi toplayamaz.

   CONTACT_EMAIL — iletişim ekranında görünecek adres. Burada gizlemek mümkün değil,
   çünkü kimsenin okuyamadığı bir iletişim adresi hiçbir işe yaramaz; adres HTML
   kaynağında görünecektir ve bu bilinçli olarak kabul ediliyor. Asıl gizlenmesi
   gereken, gönderimi taşıyan FORM_ENDPOINT değeridir.

   İkisinin aynı adres olması gerekmiyor ama pratikte aynı olması bekleniyor. */
const FORM_ENDPOINT = '';
const CONTACT_EMAIL = '';
