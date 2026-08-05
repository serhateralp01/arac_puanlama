/* ---------- kıyaslama sepeti ---------- */
/* Sepet bellekte tutulan sıradan bir dizi. Ekranlar aynı JavaScript bağlamını
   paylaştığı için ekran değiştirmek sepeti sıfırlamıyor ve tarayıcı deposuna
   yazmaya gerek kalmıyor; gerekçesi docs/ARCHITECTURE.md MK-07 kaydında. */
let cmpSet=[];
function toggleCmp(id){
 const idx=cmpSet.indexOf(id);
 if(idx>-1){cmpSet.splice(idx,1);}
 else{ if(cmpSet.length>=4){alert('En fazla dört araç kıyaslayabilirsiniz.');return;} cmpSet.push(id); }
 renderTray();renderRows_softUpdate();renderCompare();
}
function renderTray(){
 const tray=document.getElementById('cmptray'),chips=document.getElementById('trayChips');
 const navCnt=document.getElementById('navCmpCount');
 if(navCnt)navCnt.textContent=cmpSet.length?'('+cmpSet.length+')':'';
 if(cmpSet.length===0){tray.classList.remove('show');return;}
 tray.classList.add('show');chips.innerHTML='';
 cmpSet.forEach(id=>{const c=CARS[id];const ch=document.createElement('span');ch.className='chip2';
  ch.innerHTML=c.n+' <span class="x" data-id="'+id+'">&times;</span>';
  ch.querySelector('.x').onclick=()=>toggleCmp(id);
  chips.appendChild(ch);});
}
document.getElementById('trayClear').onclick=()=>{cmpSet=[];renderTray();renderRows_softUpdate();renderCompare();};
document.getElementById('trayGo').onclick=()=>goTo('kiyaslama');
