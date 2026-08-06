/* ---------- iletişim ekranı ---------- */
/* Adres templates/app/05-yapilandirma.js içindeki CONTACT_EMAIL değişkeninden
   geliyor. Değişken boş bırakıldığı sürece ekran hâlâ açılır ama adresin henüz
   tanımlanmadığı, kaynak öner formunun bu süreye kadar tek yol olduğu açıkça
   söylenir; sessizce boş bir sayfa göstermek yerine bunu tercih ediyoruz. */
(function(){
 const box=document.getElementById('ilNotice');
 if(!box)return;
 if(CONTACT_EMAIL){
  box.className='ktnotice';
  box.innerHTML='Öneri veya soru için <a href="mailto:'+CONTACT_EMAIL+'">'+CONTACT_EMAIL+'</a> adresine yazabilirsiniz.';
 }else{
  box.className='ktnotice warn';
  box.innerHTML='<b>İletişim adresi henüz tanımlanmadı.</b> Bu adres tanımlanana kadar en güvenilir yol <a href="#katki">kaynak öner formu</a>; adres tanımlandığı anda bu bölüm otomatik güncellenir.';
 }
})();
