/* ---------- table render ---------- */
let sortKey='tot',sortDir=-1;
const head=document.getElementById('head');
function renderHead(){head.innerHTML='';
 const cols=[{k:'rank',l:'#'},{k:'cmp',l:''},{k:'name',l:'Araç',lft:1},{k:'year',l:'Model Yılı'},{k:'hp',l:'Beygir'},{k:'disp',l:'Hacim'},{k:'tx',l:'Şanzıman Tipi'},{k:'pband',l:'Tahmini Fiyat'}];
 CRIT.forEach(c=>cols.push({k:c.k,l:HEAD[c.k]}));cols.push({k:'tot',l:'Toplam'});cols.push({k:'norm',l:'Normalize'});cols.push({k:'tg',l:''});
 cols.forEach(c=>{const th=document.createElement('th');if(c.lft)th.className='lft';th.dataset.k=c.k;
  const cc=CRIT.find(x=>x.k===c.k);
  th.innerHTML=c.k==='tot'?c.l+'<span class="ww">/100</span>':c.k==='norm'?c.l+'<span class="ww">en iyi 100</span>':c.k==='pband'?c.l+'<span class="ww">bin TL</span>':cc?c.l+' ?<span class="ww">ağırlık '+W[c.k]+'</span>':c.l;
  if(cc)th.title=cc.t+'\n\n'+cc.d+'\n\n'+cc.inc+'\n'+cc.exc;
  if(c.k!=='tg'&&c.k!=='rank'&&c.k!=='cmp')th.classList.toggle('sorted',c.k===sortKey);
  head.appendChild(th);});
 head.querySelectorAll('th').forEach(th=>{const k=th.dataset.k;if(k==='tg'||k==='rank'||k==='cmp')return;
  th.onclick=()=>{if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=(k==='name'||k==='tx')?1:-1;}render();};});}
/* ---------- "bu araç neden bu puanı aldı" dökümü (Y-06 ikinci katman) ---------- */
/* Katkı = puan × ağırlık / ağırlık toplamı; bu tam olarak total()'ın topladığı
   terim, yani buradaki sayılar toplam puanı gerçekten oluşturan sayılar — ayrı bir
   tahmin değil. Motor ve trans için evidence bloğu doluysa (bkz. data/cars/*.json
   evidence.motor/trans) hangi bandın hangi gerekçeyle verildiği de gösteriliyor;
   diğer beş kriter için evidence henüz boş olduğundan (docs/DATA-ISSUES.md D-12
   dışındaki kalan boşluklardan biri, bkz. docs/PUANLAMA-TEMELI.md §6) o kriterlerde
   yalnızca puan/ağırlık/katkı satırı görünür.
   Kaynak kısıtı: evidence yalnızca base_score'u olan bileşenlere bağlı araçlarda dolu.
   `ne=null` durumunu buradaki tablo değil, yukarıdaki "atlanan" mantığı (build.py)
   belirliyor; burası yalnızca var olanı gösteriyor. */
function scoreBreakdownHTML(c){
 const sw=sumW();
 const rows=ORDER.map(k=>{
  const v=c.S[k],w=Math.max(0,+W[k]||0),contrib=sw>0?(v*w/sw):0;
  const weak=(k!=='price'&&v<WEAK_THR);
  return '<tr><td class="rowlbl">'+HEAD[k]+'</td><td class="'+(weak?'weak':'')+'">'+v+'</td><td>'+w+'</td><td>'+contrib.toFixed(1)+'</td></tr>';
 }).join('');
 let evHtml='';
 ['motor','trans'].forEach(k=>{
  const e=c.ev&&c.ev[k];
  if(!e)return;
  evHtml+='<div class="evrow"><b>'+HEAD[k]+' &mdash; “'+e.band+'” bandı (güven: '+e.confidence+'):</b> '+e.reasoning+'</div>';
 });
 return '<div class="breakdown"><div class="bdhead">Bu araç neden bu puanı aldı</div>'
  +'<div class="bdscroll"><table class="bdtable"><thead><tr><th>Kriter</th><th>Puan</th><th>Ağırlık</th><th>Katkı</th></tr></thead><tbody>'+rows
  +'<tr class="bdtotal"><td class="rowlbl">Toplam</td><td colspan="3">'+total(c).toFixed(1)+' / 100</td></tr></tbody></table></div>'
  +(evHtml?'<div class="evwrap">'+evHtml+'</div>':'')+'</div>';
}

const body=document.getElementById('body');
let visible=[];
function render(){renderHead();
 let list=CARS.filter(pass);
 list.sort((a,b)=>{let av,bv;
  if(sortKey==='tot'||sortKey==='rank'){av=total(a);bv=total(b);}
  else if(sortKey==='norm'){av=normOf(a);bv=normOf(b);}
  else if(sortKey==='name'){return sortDir*a.n.localeCompare(b.n,'tr');}
  else if(sortKey==='tx'){return sortDir*a.tx.localeCompare(b.tx,'tr');}
  else if(sortKey==='pband'){av=a.p[0];bv=b.p[0];}
  else if(sortKey==='year'){av=parseInt(a.y);bv=parseInt(b.y);}
  else if(sortKey==='hp'){av=a.hp;bv=b.hp;}
  else if(sortKey==='disp'){av=a.disp;bv=b.disp;}
  else{av=a.S[sortKey];bv=b.S[sortKey];}
  return sortDir*(av-bv);});
 const ranked=[...CARS].sort((a,b)=>total(b)-total(a));
 visible=list;body.innerHTML='';
 document.getElementById('count').innerHTML='Filtrelere uyan <b>'+list.length+'</b> araç gösteriliyor. Listede toplam '+CARS.length+' araç var.';
 list.forEach(c=>{const gr=ranked.indexOf(c)+1,tt=total(c),nrm=normOf(c);
  const tr=document.createElement('tr');tr.className='main'+(cmpSet.includes(c.id)?' cmp':'');tr.dataset.id=c.id;
  const txc='tx-'+c.tx.split(' ')[0];
  let cells='<td class="rank">'+gr+'</td>';
  cells+='<td class="cmpcell"><button class="cmpbtn'+(cmpSet.includes(c.id)?' on':'')+'" data-cmp="'+c.id+'" '+(cmpSet.length>=4&&!cmpSet.includes(c.id)?'disabled':'')+'>'+(cmpSet.includes(c.id)?'✓':'+')+'</button></td>';
  cells+='<td class="name"><div class="nm">'+c.n+' <span class="chip '+(c.v===true?'v':c.v==='p'?'p':'a')+'">'+(c.v===true?'doğrulanmış':c.v==='p'?'kısmi kaynak':'ön değerlendirme')+'</span></div><div class="tag">'+c.tag+'</div></td>';
  cells+='<td class="spec">'+c.y+'</td><td class="spec">'+c.hp+' bg</td><td class="spec">'+c.disp.toFixed(1)+'</td>';
  cells+='<td><span class="txbadge '+txc+'">'+c.tx+'</span></td>';
  cells+='<td class="pr"><input type="number" class="pin" data-id="'+c.id+'" data-pi="0" value="'+c.p[0]+'"><span class="dash">-</span><input type="number" class="pin" data-id="'+c.id+'" data-pi="1" value="'+c.p[1]+'"></td>';
  ORDER.forEach(k=>{
   const v=c.S[k]; const weak=(k!=='price'&&v<WEAK_THR);
   cells+='<td class="sc'+(weak?' weak':(k==='price'?' psc':''))+'">'+v+'</td>';
  });
  cells+='<td class="tot" style="color:'+colorFor(tt)+'">'+tt.toFixed(1)+'</td>';
  cells+='<td class="norm">'+nrm.toFixed(0)+'</td>';
  cells+='<td class="toggle">+</td>';
  tr.innerHTML=cells;
  const det=document.createElement('tr');det.className='detail';
  const src=c.r&&c.r.length?'Kaynak: '+c.r.map(x=>'<a href="'+R[x][2]+'" target="_blank" rel="noopener">'+R[x][1]+'</a>').join(' &middot; '):'Bu puanlar kendi teknik değerlendirmeme dayanıyor.';
  const weaks=weakOnes(c);
  let weakHtml='';
  if(weaks.length){weakHtml='<div class="weaklist">';weaks.forEach(w=>{weakHtml+='<div class="weakitem"><b>'+HEAD[w.k]+' ('+w.v+'/100):</b> '+weakReason(c,w.k)+'</div>';});weakHtml+='</div>';}
  /* "Bu araca kaynak öner" (Y-04): kullanıcı zaten baktığı aracı ikinci kez
     aramak zorunda kalmasın diye kaynak öner formuna aracı önceden seçili
     götürüyor. */
  det.innerHTML='<td colspan="'+(ORDER.length+8)+'"><div class="det"><div class="det-grid"><div><div class="lead">'+c.note+'</div>'+weakHtml+'<div class="src">'+src+'</div><button type="button" class="btn small ghost sugbtn" data-carid="'+c.id+'">Bu araca kaynak öner</button></div><div class="radarwrap">'+radarSVG([c])+'</div></div>'+scoreBreakdownHTML(c)+'</div></td>';
  body.appendChild(tr);body.appendChild(det);
  const tg=()=>{const o=tr.classList.toggle('open');det.classList.toggle('open',o);tr.querySelector('.toggle').textContent=o?'−':'+';};
  tr.querySelector('.name').onclick=tg;tr.querySelector('.toggle').onclick=tg;
  tr.querySelector('[data-cmp]').onclick=(e)=>{e.stopPropagation();toggleCmp(c.id);};
  det.querySelector('.sugbtn').onclick=(e)=>{e.stopPropagation();suggestSourceFor(c);};
 });
 updateSum();
 renderCatalog();
}
function renderRows_softUpdate(){
 document.querySelectorAll('#body tr.main').forEach(tr=>{
  const id=+tr.dataset.id; const inCmp=cmpSet.includes(id);
  tr.classList.toggle('cmp',inCmp);
  const btn=tr.querySelector('[data-cmp]');
  if(btn){btn.classList.toggle('on',inCmp);btn.textContent=inCmp?'✓':'+';btn.disabled=(cmpSet.length>=4&&!inCmp);}
 });
}
/* Price inputs commit only on 'change' (blur) or Enter — not on every keystroke,
   so the table doesn't re-render (and steal focus) while the user is still typing. */
body.addEventListener('change',e=>{
 const pi=e.target.dataset.pi;
 if(pi===undefined)return;
 const id=+e.target.dataset.id;CARS[id].p[+pi]=Math.max(0,+e.target.value||0);recalcPrice();
 render();renderCompare();updateContrib();
});
body.addEventListener('keydown',e=>{
 if(e.key==='Enter'&&e.target.classList&&e.target.classList.contains('pin')){e.target.blur();}
});
function recalcAll(){renderHead();render();updateSum();renderCompare();updateContrib();}
