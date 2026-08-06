/* ---------- ekran yönlendiricisi ---------- */
/* Adres çubuğundaki "#liste" gibi bir yol adı hangi ekranın görüneceğini
   belirliyor. Ekranların hepsi sayfada duruyor ve yalnızca görünürlükleri
   değişiyor; bu yüzden ekran değiştirmek hiçbir durumu sıfırlamıyor. Yol
   adları bir gün gerçek sunucu adreslerine ("/liste") birebir çevrilebilsin
   diye seçildi; gerekçesi docs/ARCHITECTURE.md MK-07 kaydında. */
const ROUTES=['giris','kriterler','liste','kiyaslama','metodoloji','katki','kaynaklar','iletisim'];
const DEFAULT_ROUTE='liste';
const ONBOARD_KEY='arac_puan_giris_gorundu';

function currentRoute(){
 const r=(location.hash||'').replace(/^#/,'');
 return ROUTES.includes(r)?r:DEFAULT_ROUTE;
}

function showScreen(name){
 document.querySelectorAll('.screen').forEach(s=>{
  s.classList.toggle('on',s.dataset.screen===name);
 });
 document.querySelectorAll('.nav a[data-route]').forEach(a=>{
  a.classList.toggle('on',a.dataset.route===name);
 });
 /* Ekran değişince sayfanın ortasında kalmamak için başa dönülüyor; ama
    kullanıcı zaten en üstteyse gereksiz bir sıçrama yaratılmıyor. */
 if(window.scrollY>0)window.scrollTo({top:0,behavior:'instant'});
 if(name==='kiyaslama')renderCompare();
}

function goTo(name){
 if(location.hash.replace(/^#/,'')===name){showScreen(name);return;}
 location.hash=name;
}

function startRouter(){
 window.addEventListener('hashchange',()=>showScreen(currentRoute()));
 /* Giriş ekranı yalnızca ilk ziyarette otomatik açılıyor. Sonraki
    ziyaretlerde kullanıcı doğrudan listeye düşüyor, giriş menüde duruyor. */
 let seen=false;
 try{seen=localStorage.getItem(ONBOARD_KEY)==='1';}catch(e){seen=false;}
 if(!location.hash&&!seen){
  location.hash='giris';
 }
 showScreen(currentRoute());
}

function markOnboardingSeen(){
 try{localStorage.setItem(ONBOARD_KEY,'1');}catch(e){}
}
