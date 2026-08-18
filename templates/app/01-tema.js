/* ---------- koyu tema geçişi (Y-09) ----------
   İlk boyamadan önceki tema seçimi (varsa) templates/index.html'in <head>
   bölümündeki senkron betik tarafından uygulanıyor (yanıp sönme olmasın diye).
   Burası yalnızca: (1) düğmenin etiketini geçerli temayla eşitliyor, (2) tıklamada
   temayı değiştirip localStorage'a yazıyor, (3) kullanıcı hiç seçim yapmadıysa
   sistem tercihi değiştiğinde etiketi güncel tutuyor. Kullanıcı elle seçene kadar
   `data-theme` özniteliği hiç yazılmıyor; böylece sistem tercihi CSS'teki
   `prefers-color-scheme` kuralıyla canlı izlenmeye devam ediyor. */
const TEMA_KEY = 'arac_puan_tema';

function temaEfektif(){
  var s = null;
  try{ s = localStorage.getItem(TEMA_KEY); }catch(e){}
  if(s === 'light' || s === 'dark') return s;
  return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
}
function temaDugmesiniGuncelle(){
  var btn = document.getElementById('temaBtn');
  if(!btn) return;
  btn.textContent = temaEfektif() === 'dark' ? 'Açık tema' : 'Koyu tema';
}
function temaDegistir(){
  var next = temaEfektif() === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  try{ localStorage.setItem(TEMA_KEY, next); }catch(e){}
  temaDugmesiniGuncelle();
}
document.addEventListener('DOMContentLoaded', function(){
  temaDugmesiniGuncelle();
  var btn = document.getElementById('temaBtn');
  if(btn) btn.addEventListener('click', temaDegistir);
  if(window.matchMedia){
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    var onChange = function(){
      var secili = null;
      try{ secili = localStorage.getItem(TEMA_KEY); }catch(e){}
      if(secili !== 'light' && secili !== 'dark') temaDugmesiniGuncelle();
    };
    if(mq.addEventListener) mq.addEventListener('change', onChange);
  }
});
