/* ---------- ağırlık arayüzü ---------- */
/* Hazır ağırlık setleri iki ekranda birden duruyor: liste ekranında hızlı
   geçiş yapmak için, kriterler ekranında ise kriterlerin tanımıyla birlikte.
   İkisi de aynı W nesnesini düzenliyor, bu yüzden hangisinden değiştirilirse
   değiştirilsin diğeri de güncel kalıyor. */
const PRESET_BOXES=['presets','presetsFull'];
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
  if(boxId==='presets'){
   const link=document.createElement('a');link.href='#kriterler';link.className='btn ghost';
   link.style.textDecoration='none';link.textContent='Kriterleri ayrıntılı oku';
   pBox.appendChild(link);}
  /* "Kaydedildi" bildirimi yalnızca birinci kutuda; iki ayrı id olmaması için. */
  if(bi===0){const msg=document.createElement('span');msg.className='savemsg';msg.id='savemsg';msg.textContent='Kaydedildi';pBox.appendChild(msg);}
 });
}
function showSaved(){const m=document.getElementById('savemsg');if(!m)return;m.classList.add('show');setTimeout(()=>m.classList.remove('show'),1600);}

const rubric=document.getElementById('rubric');
CRIT.forEach(c=>{const el=document.createElement('div');el.className='card'+(c.AUTO?' auto':'');
 el.innerHTML=(c.AUTO?'<div class="nb">OTOMATİK HESAPLANIR</div>':'')+'<div class="t">'+c.t+'</div><div class="wbox"><input type="number" min="0" max="60" data-wk="'+c.k+'" value="'+W[c.k]+'"><small>puan ağırlığı</small></div><div class="def">'+c.d+'</div><div class="inc">'+c.inc+'</div><div class="exc">'+c.exc+'</div>';
 rubric.appendChild(el);});
rubric.addEventListener('input',e=>{const k=e.target.dataset.wk;if(!k)return;W[k]=Math.max(0,Math.min(60,+e.target.value||0));recalcAll();});
function syncWeights(){rubric.querySelectorAll('[data-wk]').forEach(i=>i.value=W[i.dataset.wk]);}
function updateSum(){const s=sumW(),b=document.getElementById('sumbox'),ok=(s===100);
 if(!b)return;
 b.className='sumbox '+(ok?'ok':'warn');
 b.innerHTML=ok?('Ağırlık toplamı = <b>'+s+'</b> / 100. Tam isabet.'):('Ağırlık toplamı = <b>'+s+'</b> / 100. '+(s>100?'Fazla':'Eksik')+', ama sonuç yine normalize ediliyor.');}
