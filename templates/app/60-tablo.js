/* ---------- görünüm durumu (kart / tablo) ---------- */
/* Denetim, uygulamanın en ciddi kullanılabilirlik sorununu ortaya çıkardı: liste
   ekranı bir 15 sütunlu tablo olarak açılıyor, mobilde yatayda kayıyor ve 406
   aracın hepsi için ayrıntı satırı önceden inşa edildiği için tek bir render()
   çağrısı 55 binin üzerinde DOM düğümü üretiyordu (Y-25). Kart görünümü bunun
   yerine varsayılan oldu: her araç, toplam puanı ve yedi kriterin dağılımını tek
   bakışta gösteren bağımsız bir kart olarak listeleniyor. Tablo silinmedi —
   sütun bazlı karşılaştırma isteyen kullanıcı için ikinci bir sekme olarak
   duruyor — ama artık ilk açılışta görünen o değil. */
const VIEW_KEY='arac_puan_gorunum';
let viewMode='kart';
try{ const v=localStorage.getItem(VIEW_KEY); if(v==='kart'||v==='tablo') viewMode=v; }catch(e){}

function applyViewMode(){
 const screen=document.getElementById('listeScreen');
 if(screen){ screen.classList.remove('view-kart','view-tablo'); screen.classList.add('view-'+viewMode); }
 document.querySelectorAll('#viewToggle [data-view]').forEach(b=>{
  b.classList.toggle('on',b.dataset.view===viewMode);
 });
}
function setViewMode(v){
 if(v!==viewMode){ viewMode=v; try{localStorage.setItem(VIEW_KEY,v);}catch(e){} }
 applyViewMode();
 render();
}

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
  th.onclick=()=>{if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=(k==='name'||k==='tx')?1:-1;}syncSortSelect();render();};});}

/* ---------- kart görünümünün sıralama seçimi ---------- */
/* Tabloda sütun başlığına tıklamak sıralar; kartlarda sütun yok, bu yüzden
   aynı sortKey/sortDir durumunu okuyup yazan küçük bir açılır menü var.
   İki görünüm de aynı durumu paylaştığı için bir görünümde seçilen sıralama
   diğerine geçince kaybolmuyor. */
const SORT_OPTS=[{k:'tot',l:'Toplam puan',d:-1},{k:'name',l:'İsim',d:1},{k:'year',l:'Model yılı',d:-1},{k:'hp',l:'Beygir',d:-1},{k:'pband',l:'Tahmini fiyat',d:1}];
function syncSortSelect(){
 const sel=document.getElementById('sortSel');
 if(sel && sel.value!==sortKey) sel.value=sortKey;
 const dirBtn=document.getElementById('sortDirBtn');
 if(dirBtn) dirBtn.textContent=sortDir===1?'Artan ↑':'Azalan ↓';
}
(function initSortControls(){
 const sel=document.getElementById('sortSel');
 const dirBtn=document.getElementById('sortDirBtn');
 if(!sel||!dirBtn)return;
 sel.innerHTML=SORT_OPTS.map(o=>'<option value="'+o.k+'">'+o.l+'</option>').join('');
 sel.value=sortKey;
 sel.onchange=()=>{sortKey=sel.value;const o=SORT_OPTS.find(x=>x.k===sortKey);sortDir=o?o.d:-1;syncSortSelect();render();};
 dirBtn.onclick=()=>{sortDir*=-1;syncSortSelect();render();};
 syncSortSelect();
})();

/* ---------- "bu araç neden bu puanı aldı" dökümü (Y-06 ikinci katman) ---------- */
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
  evHtml+='<div class="evrow"><b>'+HEAD[k]+' &mdash; "'+e.band+'" bandı (güven: '+e.confidence+'):</b> '+e.reasoning+'</div>';
 });
 return '<div class="breakdown"><div class="bdhead">Bu araç neden bu puanı aldı</div>'
  +'<div class="bdscroll"><table class="bdtable"><thead><tr><th>Kriter</th><th>Puan</th><th>Ağırlık</th><th>Katkı</th></tr></thead><tbody>'+rows
  +'<tr class="bdtotal"><td class="rowlbl">Toplam</td><td colspan="3">'+total(c).toFixed(1)+' / 100</td></tr></tbody></table></div>'
  +(evHtml?'<div class="evwrap">'+evHtml+'</div>':'')+'</div>';
}

/* ---------- ayrıntı verisinin tembel yüklenmesi (MK-24) ---------- */
/* `note` (araç açıklaması) ve `evidence` (motor/şanzıman kanıt metni)
   index.html'e gömülmüyor; 406 araçta ikisi birlikte dosyanın %68'ini
   oluşturduğu ölçüldü, oysa liste/kart görünümü hiçbirini okumuyor. Bunun
   yerine build.py'nin ayrıca yazdığı detay.json'dan, yalnızca bir kart/satır
   İLK KEZ açıldığında, tek seferlik bir fetch() ile çekiliyor; sonucu bütün
   kartlar paylaşıyor (aynı Promise önbellekte tutuluyor, ikinci bir istek
   atılmıyor). `file://` olarak açılmış bir kopyada (bkz. docs/DATA-ISSUES.md'ye
   benzer şekilde katkı formunun da file://'da çalışmaması) tarayıcı bu isteği
   engeller; o durumda arayüz çökmek yerine hangi bilginin eksik olduğunu
   açıkça söyler, puan/kanıt sırası/kaynak bağlantıları gibi zaten yerel olan
   her şeyi eksiksiz göstermeye devam eder. */
let detailDataPromise=null;
function loadDetailData(){
 if(!detailDataPromise){
  detailDataPromise=fetch('detay.json').then(r=>{
   if(!r.ok)throw new Error('detay.json http '+r.status);
   return r.json();
  }).catch(()=>null);
 }
 return detailDataPromise;
}

/* ---------- ayrıntı panelinin ortak içeriği (tablo satırı + kart, ikisi de kullanır) ---------- */
/* Bu içerik eskiden 406 aracın hepsi için render() her çalıştığında önceden
   inşa ediliyordu — açılıp açılmayacağına bakılmaksızın. O tek karar 55.007
   DOM düğümü ve 595ms'lik bir render() süresine yol açıyordu (Y-25 denetimi).
   Şimdi bu işlev yalnızca bir araç ilk kez açıldığında bir kez çağrılıyor ve
   sonucu ilgili konteynerin dataset'inde önbelleğe alınıyor. */
function detailBodyHTML(c,detailUnavailable){
 const src=c.r&&c.r.length?'Kaynak: '+c.r.map(x=>'<a href="'+R[x][2]+'" target="_blank" rel="noopener">'+R[x][1]+'</a>').join(' &middot; '):'Bu puanlar kendi teknik değerlendirmeme dayanıyor.';
 const weaks=weakOnes(c);
 let weakHtml='';
 if(weaks.length){weakHtml='<div class="weaklist">';weaks.forEach(w=>{weakHtml+='<div class="weakitem"><b>'+HEAD[w.k]+' ('+w.v+'/100):</b> '+weakReason(c,w.k)+'</div>';});weakHtml+='</div>';}
 const leadHtml=c.note
  ?'<div class="lead">'+c.note+'</div>'
  :(detailUnavailable?'<div class="lead dim">Bu aracın yazılı açıklaması ve motor/şanzıman kanıt metni bu görünümde yüklenemedi — dosyayı doğrudan diskten açtıysanız bu beklenen bir durum. Puanlar, zayıf halka uyarıları ve kaynaklar aşağıda eksiksiz duruyor; tam açıklama için <a href="https://serhateralp01.github.io/arac_puanlama/#liste" target="_blank" rel="noopener">siteyi çevrimiçi ziyaret edin</a>.</div>':'');
 return '<div class="det-grid"><div>'+leadHtml+weakHtml+'<div class="src">'+src+'</div><button type="button" class="btn small ghost sugbtn" data-carid="'+c.id+'">Bu araca kaynak öner</button></div><div class="radarwrap">'+radarSVG([c])+'</div></div>'+scoreBreakdownHTML(c);
}
async function fillDetailOnce(container,c){
 if(container.dataset.built||container.dataset.building)return;
 container.dataset.building='1';
 container.innerHTML='<div class="detloading">Yükleniyor…</div>';
 if(c.note===undefined){
  const data=await loadDetailData();
  const d=data&&data[c.cid];
  if(d){c.note=d.note;c.ev=d.ev;}
 }
 container.innerHTML=detailBodyHTML(c,c.note===undefined);
 container.dataset.built='1';
 delete container.dataset.building;
 const btn=container.querySelector('.sugbtn');
 if(btn)btn.onclick=(e)=>{e.stopPropagation();suggestSourceFor(c);};
}

/* ---------- ortak liste hesaplaması ---------- */
/* Filtreleme, sıralama ve sıralama numarası (#) hesabı her iki görünüm için de
   aynı; yalnızca bunun DOM'a nasıl çizileceği değişiyor. Sıra numarası eskiden
   her satır için `ranked.indexOf(c)` ile bulunuyordu — 406 araçlık listede bu
   406×406'ya kadar karşılaştırma anlamına geliyordu (O(n²)). Şimdi sıralı liste
   bir kez geziliyor ve her aracın sırası bir Map'e yazılıyor (O(n)). */
function computeList(){
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
 const rankMap=new Map();
 ranked.forEach((c,i)=>rankMap.set(c,i+1));
 return {list,rankMap};
}

const body=document.getElementById('body');
const cardgrid=document.getElementById('cardgrid');
let visible=[];

function render(){renderHead();
 const {list,rankMap}=computeList();
 visible=list;
 document.getElementById('count').innerHTML='Filtrelere uyan <b>'+list.length+'</b> araç gösteriliyor. Listede toplam '+CARS.length+' araç var.';
 /* İki görünüm de her render()'da inşa ediliyor, sadece CSS ile biri gizleniyor.
    Yalnız görüneni inşa etmek performans için baştan çekici görünse de, gizli
    kalan görünümde DOM güncellenmediği için orada eski, tıklanamaz kıyaslama
    düğmeleri kalıyordu — görünüm değiştirilince "hangi + düğmesi gerçek"
    belirsizleşiyordu. Ayrıntı içeriği zaten tembel (yalnız tıklanınca kuruluyor),
    o yüzden burada asıl maliyetli olan kısım hâlâ atlanıyor. */
 renderTableBody(list,rankMap);
 renderCardBody(list,rankMap);
 updateSum();
 renderCatalog();
}

function renderTableBody(list,rankMap){
 body.innerHTML='';
 list.forEach(c=>{const gr=rankMap.get(c),tt=total(c),nrm=normOf(c);
  const tr=document.createElement('tr');tr.className='main'+(cmpSet.includes(c.id)?' cmp':'');tr.dataset.id=c.id;
  const txc='tx-'+c.tx.split(' ')[0];
  let cells='<td class="rank">'+gr+'</td>';
  cells+='<td class="cmpcell"><button class="cmpbtn'+(cmpSet.includes(c.id)?' on':'')+'" data-cmp="'+c.id+'" title="'+(cmpSet.includes(c.id)?'Kıyaslamadan çıkar':'Kıyaslamaya ekle')+'" '+(cmpSet.length>=4&&!cmpSet.includes(c.id)?'disabled':'')+'>'+(cmpSet.includes(c.id)?'✓':'+')+'</button></td>';
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
  det.innerHTML='<td colspan="'+(ORDER.length+8)+'"><div class="det"></div></td>';
  body.appendChild(tr);body.appendChild(det);
  const detInner=det.querySelector('.det');
  const tg=()=>{const o=tr.classList.toggle('open');det.classList.toggle('open',o);tr.querySelector('.toggle').textContent=o?'−':'+';
   if(o)fillDetailOnce(detInner,c);};
  tr.querySelector('.name').onclick=tg;tr.querySelector('.toggle').onclick=tg;
  tr.querySelector('[data-cmp]').onclick=(e)=>{e.stopPropagation();toggleCmp(c.id);};
 });
}

/* ---------- kart görünümü ---------- */
/* Her kart: sıra + kıyaslama düğmesi + renkli toplam puan üstte; isim, etiket
   ve doğrulama rozeti; sekiz kriterin tamamı kompakt bir çubuk olarak (zayıf
   halka kırmızı vurgulanıyor); altta yıl/beygir/şanzıman/fiyat özeti. Ayrıntı
   içeriği (kaynak, kırılım tablosu, radar grafiği) tıklanana kadar hiç
   oluşturulmuyor. */
function cardBarsHTML(c){
 return ORDER.map(k=>{
  const v=c.S[k];
  const weak=(k!=='price'&&v<WEAK_THR);
  const lbl=k==='price'?'Fiyat':HEAD[k];
  const col=colorFor(v);
  return '<div class="vcbar'+(weak?' weak':'')+'" title="'+lbl+': '+v+'/100">'
   +'<span class="vcbarlbl">'+lbl+'</span>'
   +'<span class="vcbartrack"><span class="vcbarfill" style="width:'+Math.max(2,v)+'%;background:'+col+'"></span></span>'
   +'<span class="vcbarval">'+v+'</span></div>';
 }).join('');
}
function renderCardBody(list,rankMap){
 cardgrid.innerHTML='';
 const frag=document.createDocumentFragment();
 list.forEach(c=>{const gr=rankMap.get(c),tt=total(c);
  const inCmp=cmpSet.includes(c.id);
  const txc='tx-'+c.tx.split(' ')[0];
  const el=document.createElement('div');
  el.className='vcard'+(inCmp?' cmp':'');
  el.dataset.id=c.id;
  el.innerHTML=
   '<div class="vctop">'
    +'<span class="vcrank'+(gr===1?' top1':'')+'">#'+gr+'</span>'
    +'<button class="cmpbtn'+(inCmp?' on':'')+'" data-cmp="'+c.id+'" title="'+(inCmp?'Kıyaslamadan çıkar':'Kıyaslamaya ekle')+'" '+(cmpSet.length>=4&&!inCmp?'disabled':'')+'>'+(inCmp?'✓':'+')+'</button>'
    +'<span class="vctot" style="color:'+colorFor(tt)+'">'+tt.toFixed(1)+'</span>'
   +'</div>'
   +'<div class="vcname">'+c.n+' <span class="chip '+(c.v===true?'v':c.v==='p'?'p':'a')+'">'+(c.v===true?'doğrulanmış':c.v==='p'?'kısmi kaynak':'ön değerlendirme')+'</span></div>'
   +'<div class="vctag">'+c.tag+'</div>'
   +'<div class="vcbars">'+cardBarsHTML(c)+'</div>'
   +'<div class="vcfoot">'
    +'<span class="spec">'+c.y+'</span>'
    +'<span class="spec">'+c.hp+' bg</span>'
    +'<span class="txbadge '+txc+'">'+c.tx+'</span>'
    +'<span class="vcprice"><input type="number" class="pin" data-id="'+c.id+'" data-pi="0" value="'+c.p[0]+'"><span class="dash">-</span><input type="number" class="pin" data-id="'+c.id+'" data-pi="1" value="'+c.p[1]+'"><span class="runit">bin TL</span></span>'
   +'</div>'
   +'<button type="button" class="vctoggle">Ayrıntıları göster</button>'
   +'<div class="vcdetail"></div>';
  const vcdetail=el.querySelector('.vcdetail');
  const toggleBtn=el.querySelector('.vctoggle');
  const tg=()=>{const o=vcdetail.classList.toggle('open');
   toggleBtn.textContent=o?'Ayrıntıları gizle':'Ayrıntıları göster';
   if(o)fillDetailOnce(vcdetail,c);};
  toggleBtn.onclick=tg;
  el.querySelector('[data-cmp]').onclick=(e)=>{e.stopPropagation();toggleCmp(c.id);};
  frag.appendChild(el);
 });
 cardgrid.appendChild(frag);
}

function renderRows_softUpdate(){
 document.querySelectorAll('#body tr.main, #cardgrid .vcard').forEach(el=>{
  const id=+el.dataset.id; const inCmp=cmpSet.includes(id);
  el.classList.toggle('cmp',inCmp);
  const btn=el.querySelector('[data-cmp]');
  if(btn){btn.classList.toggle('on',inCmp);btn.textContent=inCmp?'✓':'+';btn.disabled=(cmpSet.length>=4&&!inCmp);}
 });
}
function onPriceChange(e){
 const pi=e.target.dataset.pi;
 if(pi===undefined)return;
 const id=+e.target.dataset.id;CARS[id].p[+pi]=Math.max(0,+e.target.value||0);recalcPrice();
 render();renderCompare();updateContrib();
}
function onPinEnter(e){
 if(e.key==='Enter'&&e.target.classList&&e.target.classList.contains('pin')){e.target.blur();}
}
body.addEventListener('change',onPriceChange);
body.addEventListener('keydown',onPinEnter);
cardgrid.addEventListener('change',onPriceChange);
cardgrid.addEventListener('keydown',onPinEnter);
function recalcAll(){renderHead();render();updateSum();renderCompare();updateContrib();}

/* ---------- görünüm geçiş düğmeleri ---------- */
document.querySelectorAll('#viewToggle [data-view]').forEach(b=>{
 b.onclick=()=>setViewMode(b.dataset.view);
});
applyViewMode();
