/* ---------- ağırlık arayüzü ---------- */
/* Hazır ağırlık seti düğmeleri tek bir yerde: liste ekranının denetim çubuğunda.
   Önceden ayrıca bir #kriterler ekranında da tekrarlanıyordu; kullanıcı isteğiyle
   ayrıntılı düzenleme paneli de listenin bulunduğu ekrana taşındığı için tekrar
   gerekmedi (bkz. #kritpanel, aşağıda). */
const PRESET_BOXES=['presets'];
function buildPresetButtons(){
 PRESET_BOXES.forEach((boxId,bi)=>{
  const pBox=document.getElementById(boxId);
  if(!pBox)return;
  pBox.innerHTML='';
  const lbl=document.createElement('span');lbl.className='flabel';lbl.textContent='Hazır ayar';
  pBox.appendChild(lbl);
  Object.entries(DB.preset_labels).forEach(([m,t])=>{
   const b=document.createElement('button');b.className='btn';b.dataset.m=m;b.textContent=t;
   b.onclick=()=>{W={...PRESETS[m]};syncWeights();recalcAll();};
   pBox.appendChild(b);});
  const rb=document.createElement('button');rb.className='btn ghost';rb.textContent='Sıfırla';
  rb.onclick=()=>{W={...PRESETS.custom};syncWeights();recalcAll();};pBox.appendChild(rb);
  const saveBtn=document.createElement('button');saveBtn.className='btn';saveBtn.textContent='Bu ayarı kaydet';
  saveBtn.onclick=()=>{try{localStorage.setItem('arac_puan_agirlik',JSON.stringify(W));showSaved();}catch(e){}};
  pBox.appendChild(saveBtn);
  const loadBtn=document.createElement('button');loadBtn.className='btn ghost';loadBtn.textContent='Kaydedilmiş ayarı yükle';
  loadBtn.onclick=()=>{try{const s=localStorage.getItem('arac_puan_agirlik');if(s){const o=JSON.parse(s);ORDER.forEach(k=>{if(o[k]!==undefined)W[k]=o[k];});syncWeights();recalcAll();}}catch(e){}};
  pBox.appendChild(loadBtn);
  /* "Kaydedildi" bildirimi yalnızca birinci kutuda; iki ayrı id olmaması için. */
  if(bi===0){const msg=document.createElement('span');msg.className='savemsg';msg.id='savemsg';msg.textContent='Kaydedildi';pBox.appendChild(msg);}
 });
}
function showSaved(){const m=document.getElementById('savemsg');if(!m)return;m.classList.add('show');setTimeout(()=>m.classList.remove('show'),1600);}

/* ---------- kriter paneli: aç/kapa (Y-05 desenini tekrar ediyor) ---------- */
/* Ayrıntılı kriter kartları (tanım, bant, ağırlık) önceden ayrı bir ekrandı;
   kullanıcı "araç listesinin olduğu yere gönder" dedi, bu yüzden filtre paneliyle
   birebir aynı katlanabilir/hatırlanan panel desenine taşındı. İlk ziyarette
   kapalı başlıyor ki kullanıcı önce tabloyu görsün. */
const KRIT_PANEL_KEY='arac_puan_kriter_paneli';
const kritPanel=document.getElementById('kritpanel');
const kritToggle=document.getElementById('krittoggle');
function setKritPanel(open){
 if(!kritPanel)return;
 kritPanel.classList.toggle('open',open);
 if(kritToggle)kritToggle.setAttribute('aria-expanded',open?'true':'false');
 try{localStorage.setItem(KRIT_PANEL_KEY,open?'1':'0');}catch(e){}
}
if(kritToggle)kritToggle.onclick=()=>setKritPanel(!kritPanel.classList.contains('open'));
(function(){
 let open=false;
 try{open=localStorage.getItem(KRIT_PANEL_KEY)==='1';}catch(e){open=false;}
 if(kritPanel)kritPanel.classList.toggle('open',open);
 if(kritToggle)kritToggle.setAttribute('aria-expanded',open?'true':'false');
})();

/* ---------- puan bantları (Y-06 ikinci katman) ---------- */
/* Her kriterin çapalı bant tanımı data/criteria.json'dan geliyor (build.py bant
   örneklerini araç kimliğinden araç adına çeviriyor); burada yalnızca gösteriliyor,
   üretilmiyor. Varsayılan kapalı: sekiz kart yan yanayken beş bandın tamamını açık
   göstermek grid'i düzensizleştirir, bu yüzden <details> ile isteğe bağlı. */
function bandsHTML(c){
 if(!c.bands)return '';
 const rows=c.bands.map(b=>{
  const ex=b.example?'<div class="bex">Örnek: <b>'+b.example+'</b></div>':'';
  const nt=b.note?'<div class="bnote">'+b.note+'</div>':'';
  return '<div class="bandrow"><div class="brange">'+b.range[0]+'-'+b.range[1]+'</div><div class="bmid"><b>'+b.name+'</b><span>'+b.test+'</span>'+ex+nt+'</div></div>';
 }).join('');
 return '<details class="banddet"><summary>Puan bantlarını göster</summary><div class="bandlist">'+rows+'</div></details>';
}

/* ---------- ağırlık payı göstergesi ---------- */
/* Önceki sürümde burada "fiili katkı" diye ağırlığı listenin ortalama puanıyla
   çarpan bir sayı gösteriliyordu; kullanıcı bunun ne anlama geldiğinin belli
   olmadığını, kendi belirlediği ağırlığın payının doğrudan görünmesi gerektiğini
   söyledi. Gösterge bu yüzden basitleştirildi: sadece kullanıcının kendi yazdığı
   ağırlığın, ağırlık toplamı içindeki payı — başka hiçbir sayıyla karışmıyor. */
function weightShares(){
 const sw=sumW();
 const out={};
 ORDER.forEach(k=>{out[k]=sw>0?100*Math.max(0,+W[k]||0)/sw:0;});
 return out;
}
function updateContrib(){
 const shares=weightShares();
 document.querySelectorAll('[data-contrib]').forEach(el=>{
  const k=el.dataset.contrib,w=Math.max(0,+W[k]||0);
  el.textContent=w<=0
   ?'Bu kriterin ağırlığı sıfır, toplam puana katkısı yok.'
   :('Bu kriter, girdiğiniz ağırlıkların toplamının %'+shares[k].toFixed(0)+'\'ini taşıyor.');
 });
}

const rubric=document.getElementById('rubric');
CRIT.forEach(c=>{const el=document.createElement('div');el.className='card'+(c.AUTO?' auto':'');
 el.innerHTML=(c.AUTO?'<div class="nb">OTOMATİK HESAPLANIR</div>':'')
  +'<div class="t">'+c.t+'</div>'
  +'<div class="wbox"><input type="number" min="0" max="60" data-wk="'+c.k+'" value="'+W[c.k]+'"><small>puan ağırlığı</small></div>'
  +'<div class="contrib" data-contrib="'+c.k+'"></div>'
  +'<div class="def">'+c.d+'</div><div class="inc">'+c.inc+'</div><div class="exc">'+c.exc+'</div>'
  +(c.wr?'<div class="wr">'+c.wr+'</div>':'')
  +bandsHTML(c);
 rubric.appendChild(el);});
rubric.addEventListener('input',e=>{const k=e.target.dataset.wk;if(!k)return;W[k]=Math.max(0,Math.min(60,+e.target.value||0));recalcAll();});
function syncWeights(){rubric.querySelectorAll('[data-wk]').forEach(i=>i.value=W[i.dataset.wk]);}
function updateSum(){const s=sumW(),b=document.getElementById('sumbox'),ok=(s===100);
 if(!b)return;
 b.className='sumbox '+(ok?'ok':'warn');
 b.innerHTML=ok?('Ağırlık toplamı = <b>'+s+'</b> / 100. Tam isabet.'):('Ağırlık toplamı = <b>'+s+'</b> / 100. '+(s>100?'Fazla':'Eksik')+', ama sonuç yine normalize ediliyor.');}
