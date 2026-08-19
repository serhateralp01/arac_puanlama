/* ---------- ekran yönlendiricisi ---------- */
/* Adres çubuğundaki "#liste" gibi bir yol adı hangi ekranın görüneceğini
   belirliyor. Ekranların hepsi sayfada duruyor ve yalnızca görünürlükleri
   değişiyor; bu yüzden ekran değiştirmek hiçbir durumu sıfırlamıyor. Yol
   adları bir gün gerçek sunucu adreslerine ("/liste") birebir çevrilebilsin
   diye seçildi; gerekçesi docs/ARCHITECTURE.md MK-07 kaydında. */
const ROUTES=['giris','ana','liste','kiyaslama','metodoloji','katki','kaynaklar','iletisim'];
const DEFAULT_ROUTE='ana';
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
 /* Ana ekranın "en yüksek puanlı beş araç" bulgusu şu anki ağırlık ayarına
    bağlı; ekrana her dönüşte yeniden hesaplanmazsa kullanıcı liste
    ekranındaki kriter panelinde ağırlığı değiştirip geri döndüğünde eski
    bir sonuç görür. */
 if(name==='ana')renderAna();
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

/* ---------- dar ekranda açılır menü (Y-25) ---------- */
function startNavToggle(){
 const btn=document.getElementById('navToggle');
 const panel=document.getElementById('navPanel');
 if(!btn||!panel)return;
 function setOpen(open){
  panel.classList.toggle('open',open);
  btn.setAttribute('aria-expanded',open?'true':'false');
  btn.setAttribute('aria-label',open?'Menüyü kapat':'Menüyü aç');
 }
 btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));
 /* Bir bağlantıya tıklayınca (rota değişse de değişmese de) panel kapanmalı;
    aksi halde kullanıcı her ekran değişiminde menüyü elle kapatmak zorunda kalır. */
 panel.querySelectorAll('a[data-route]').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
 document.addEventListener('click',(e)=>{
  if(panel.classList.contains('open')&&!panel.contains(e.target)&&e.target!==btn&&!btn.contains(e.target))setOpen(false);
 });
 document.addEventListener('keydown',(e)=>{if(e.key==='Escape')setOpen(false);});
}
