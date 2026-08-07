/* ---------- dynamic (faceted) MULTI-SELECT filters ---------- */
/* Each filter category holds a Set of selected values. Empty set = no restriction ("Hepsi"). */
const F={tx:new Set(),fuel:new Set(),disp:new Set(),hp:new Set(),drv:new Set(),body:new Set(),budget:new Set(),brand:new Set()};
let searchTerm='';

/* ---------- sayısal aralık filtreleri (yıl, beygir, fiyat) ---------- */
/* Kova (bucket) filtreleri "110-130 beygir" gibi sabit dilimler sunuyordu; kullanıcı
   aralığı kendisi belirleyebilsin diye bunların yanına hem kutuya yazılabilen hem
   sürüklenebilen çift uçlu aralık denetimleri eklendi. RNG nesnesi seçili aralığı,
   RANGE_DEFS ise her aralığın veriden hesaplanan sınırlarını ve okuma işlevini
   tutuyor. null = sınır yok, yani kullanıcı o ucu hiç değiştirmemiş. */
const RNG={year:[null,null],hp:[null,null],price:[null,null]};
const RANGE_DEFS=[
 {k:'year',label:'Model yılı',unit:'',step:1,
  val:c=>parseInt(String(c.y).slice(0,4),10)},
 {k:'hp',label:'Beygir',unit:'bg',step:5,
  val:c=>c.hp},
 {k:'price',label:'Fiyat (bin TL)',unit:'bin',step:25,
  /* Aracın fiyat bandının alt ucu kıyaslanıyor: kullanıcı "en fazla 700 bin"
     dediğinde, 700'ün altından başlayan her araç makul biçimde adaydır. */
  val:c=>c.p[0]},
];
function rangeBounds(k){
 const d=RANGE_DEFS.find(x=>x.k===k);
 const vals=CARS.map(d.val).filter(v=>Number.isFinite(v));
 return [Math.min(...vals),Math.max(...vals)];
}
function rangePass(c,skip){
 for(const d of RANGE_DEFS){
  if(skip===d.k)continue;
  const [lo,hi]=RNG[d.k];
  if(lo===null&&hi===null)continue;
  const v=d.val(c);
  if(!Number.isFinite(v))continue;
  if(lo!==null&&v<lo)return false;
  if(hi!==null&&v>hi)return false;
 }
 return true;
}
function activeRangeCount(){
 return RANGE_DEFS.filter(d=>RNG[d.k][0]!==null||RNG[d.k][1]!==null).length;
}
function setRange(k,i,v){
 const [bLo,bHi]=rangeBounds(k);
 if(v===''||v===null||Number.isNaN(v)){RNG[k][i]=null;}
 else{
  let n=Math.max(bLo,Math.min(bHi,Math.round(v)));
  RNG[k][i]=n;
  /* İki uç birbirini geçerse diğerini iterek tutarlı tutuyoruz. */
  if(i===0&&RNG[k][1]!==null&&n>RNG[k][1])RNG[k][1]=n;
  if(i===1&&RNG[k][0]!==null&&n<RNG[k][0])RNG[k][0]=n;
 }
 renderFilters();render();
}
function clearRange(k){RNG[k]=[null,null];renderFilters();render();}
/* Gövde tipi dört karma model kaydında boş; o kayıtlar birleştirdikleri iki modelin
   gövdesi farklı olduğu için tek bir değere zorlanamıyor (bkz. docs/DATA-ISSUES.md
   D-10). Boş değer seçenek listesine girmiyor, dolayısıyla bir gövde seçildiğinde bu
   araçlar listeden düşüyor; "Hepsi" seçiliyken görünmeye devam ediyorlar. */
const FDEF=[
 {k:'tx',label:'Şanzıman',opts:()=>[...new Set(CARS.map(c=>c.tx))].sort(),val:c=>c.tx},
 {k:'body',label:'Gövde',opts:()=>[...new Set(CARS.map(c=>c.body).filter(Boolean))].sort(),val:c=>c.body},
 {k:'fuel',label:'Yakıt',opts:()=>[...new Set(CARS.map(c=>c.fuel))].sort(),val:c=>c.fuel},
 {k:'drv',label:'Çekiş',opts:()=>[...new Set(CARS.map(c=>c.drv))].sort(),val:c=>c.drv},
 {k:'brand',label:'Marka grubu',opts:()=>[...new Set(CARS.map(c=>c.g))].sort(),val:c=>c.g},
];
/* hp ve budget kovaları (110-130 gibi sabit dilimler) arayüzden kaldırıldı: yerlerini
   kullanıcının kendi sınırını yazabildiği/sürükleyebildiği aralık denetimleri aldı.
   Tanımlar geriye dönük uyumluluk için duruyor ama artık çizilmiyor. */
const DISP_BUCKETS=[['s','1.6 ve altı',c=>c.disp<=1.6],['m','1.7 - 2.0',c=>c.disp>1.6&&c.disp<=2.0],['l','2.0 üstü',c=>c.disp>2.0]];
const HP_BUCKETS=[['a','110 - 130',c=>c.hp>=110&&c.hp<=130],['b','131 - 160',c=>c.hp>=131&&c.hp<=160],['c','161 - 200',c=>c.hp>=161&&c.hp<=200],['d','200 üstü',c=>c.hp>200]];
const BUDGET_BUCKETS=[['600','600 bin altına giren',c=>c.p[0]<=600],['700','700 bin altına giren',c=>c.p[0]<=700],['800','800 bin altına giren',c=>c.p[0]<=800],['1000','1 milyon altına giren',c=>c.p[0]<=1000]];
const BUCKET_DEFS={disp:DISP_BUCKETS,hp:HP_BUCKETS,budget:BUDGET_BUCKETS};

/* direct-equality categories: pass if set empty OR car's value is in the set (OR within category) */
function directPass(c,key,valFn,skip){
 if(skip===key)return true;
 const set=F[key];
 if(set.size===0)return true;
 return set.has(valFn(c));
}
/* bucket categories: pass if set empty OR car matches ANY selected bucket predicate (OR within category) */
function bucketPass(c,key,skip){
 if(skip===key)return true;
 const set=F[key];
 if(set.size===0)return true;
 const defs=BUCKET_DEFS[key];
 for(const bv of set){const d=defs.find(x=>x[0]===bv);if(d&&d[2](c))return true;}
 return false;
}
function matchesFilter(c,skip){
 if(!directPass(c,'tx',x=>x.tx,skip))return false;
 if(!directPass(c,'fuel',x=>x.fuel,skip))return false;
 if(!directPass(c,'drv',x=>x.drv,skip))return false;
 if(!directPass(c,'body',x=>x.body,skip))return false;
 if(!directPass(c,'brand',x=>x.g,skip))return false;
 if(!bucketPass(c,'disp',skip))return false;
 if(!bucketPass(c,'hp',skip))return false;
 if(!bucketPass(c,'budget',skip))return false;
 if(!rangePass(c,skip))return false;
 if(searchTerm){
   const hay=(c.n+' '+c.tag+' '+c.g+' '+c.fuel+' '+c.tx+' '+c.drv+' '+(c.body||'')+' '+c.y+' '+c.hp+' '+c.disp).toLowerCase();
   if(hay.indexOf(searchTerm)===-1)return false;
 }
 return true;
}
function pass(c){return matchesFilter(c,null);}
function toggleSetVal(key,v){
 const set=F[key];
 if(set.has(v))set.delete(v);else set.add(v);
 renderFilters();render();
}
function clearSet(key){F[key]=new Set();renderFilters();render();}

const fWrap=document.getElementById('filters');
function renderFilters(){
 fWrap.innerHTML='';
 FDEF.forEach(f=>{
  const avail=new Set(CARS.filter(c=>matchesFilter(c,f.k)).map(f.val));
  const g=document.createElement('div');g.className='fgroup';
  g.innerHTML='<span class="flabel">'+f.label+'</span>';
  const allBtn=document.createElement('button');allBtn.className='btn'+(F[f.k].size===0?' on':'');allBtn.textContent='Hepsi';
  allBtn.onclick=()=>clearSet(f.k);g.appendChild(allBtn);
  f.opts().forEach(v=>{
   const b=document.createElement('button');
   const active=avail.has(v);
   b.className='btn'+(F[f.k].has(v)?' on':'')+(active?'':' disabled');
   b.textContent=v;
   if(active)b.onclick=()=>toggleSetVal(f.k,v);
   g.appendChild(b);});
  fWrap.appendChild(g);
 });
 // disp bucket group
 const gd=document.createElement('div');gd.className='fgroup';gd.innerHTML='<span class="flabel">Motor hacmi</span>';
 const ad=document.createElement('button');ad.className='btn'+(F.disp.size===0?' on':'');ad.textContent='Hepsi';ad.onclick=()=>clearSet('disp');gd.appendChild(ad);
 DISP_BUCKETS.forEach(([v,t,fn])=>{const has=CARS.some(c=>matchesFilter(c,'disp')&&fn(c));
  const b=document.createElement('button');b.className='btn'+(F.disp.has(v)?' on':'')+(has?'':' disabled');b.textContent=t;
  if(has)b.onclick=()=>toggleSetVal('disp',v);gd.appendChild(b);});
 fWrap.appendChild(gd);
 /* sayısal aralıklar: hem yazılabilir kutu hem sürüklenebilir çift uç */
 RANGE_DEFS.forEach(d=>{
  const [bLo,bHi]=rangeBounds(d.k);
  const lo=RNG[d.k][0]===null?bLo:RNG[d.k][0];
  const hi=RNG[d.k][1]===null?bHi:RNG[d.k][1];
  const active=RNG[d.k][0]!==null||RNG[d.k][1]!==null;
  const g=document.createElement('div');g.className='fgroup rgroup';
  g.innerHTML='<span class="flabel">'+d.label+'</span>'
   +'<div class="rwrap">'
   +'<input type="number" class="rnum" data-rk="'+d.k+'" data-ri="0" value="'+lo+'" min="'+bLo+'" max="'+bHi+'" step="'+d.step+'" aria-label="'+d.label+' en az">'
   +'<span class="rdash">–</span>'
   +'<input type="number" class="rnum" data-rk="'+d.k+'" data-ri="1" value="'+hi+'" min="'+bLo+'" max="'+bHi+'" step="'+d.step+'" aria-label="'+d.label+' en çok">'
   +'<span class="runit">'+d.unit+'</span>'
   +'<div class="rslider">'
   +'<input type="range" data-rk="'+d.k+'" data-ri="0" value="'+lo+'" min="'+bLo+'" max="'+bHi+'" step="'+d.step+'" aria-label="'+d.label+' en az (kaydırıcı)">'
   +'<input type="range" data-rk="'+d.k+'" data-ri="1" value="'+hi+'" min="'+bLo+'" max="'+bHi+'" step="'+d.step+'" aria-label="'+d.label+' en çok (kaydırıcı)">'
   +'</div></div>';
  const rst=document.createElement('button');
  rst.className='btn'+(active?'':' on');rst.textContent='Hepsi';
  rst.onclick=()=>clearRange(d.k);
  g.insertBefore(rst,g.querySelector('.rwrap'));
  fWrap.appendChild(g);
 });
 updateFilterBadge();
}
/* Kutular ve kaydırıcılar aynı olayı paylaşıyor; kaydırıcı sürüklenirken anlık,
   sayı kutusu ise yazma bitince (change) uygulanıyor ki her tuşta tablo yeniden
   çizilip odak kaybolmasın. */
fWrap.addEventListener('input',e=>{
 const t=e.target;
 if(t.type!=='range'||!t.dataset.rk)return;
 setRange(t.dataset.rk,+t.dataset.ri,+t.value);
});
fWrap.addEventListener('change',e=>{
 const t=e.target;
 if(!t.classList.contains('rnum'))return;
 setRange(t.dataset.rk,+t.dataset.ri,t.value===''?null:+t.value);
});

/* search */
const searchInp=document.getElementById('search'), searchClr=document.getElementById('searchclr');
searchInp.addEventListener('input',()=>{searchTerm=searchInp.value.trim().toLowerCase();searchClr.style.display=searchTerm?'block':'none';renderFilters();render();});
searchClr.onclick=()=>{searchInp.value='';searchTerm='';searchClr.style.display='none';renderFilters();render();};

/* ---------- katlanabilir filtre paneli (Y-05) ---------- */
/* Sekiz filtre grubu alt alta dizildiğinde tabloyu ekranın çok aşağısına
   itiyordu. Gruplar artık katlanabilir bir panelde duruyor ve panelin açık mı
   kapalı mı olduğu tarayıcıda saklanıyor: kullanıcı paneli bir kez açtıysa
   sonraki ziyaretinde açık bulur, kapattıysa kapalı. İlk ziyarette kapalı
   başlar, çünkü ilk gelen kullanıcının önce tabloyu görmesi gerekiyor.

   Panel kapalıyken hangi filtrelerin aktif olduğu görünmez olmasın diye düğmenin
   üstünde seçili filtre sayısını gösteren bir rozet duruyor; "temizle" düğmesi de
   panel kapalıyken erişilebilir kalıyor. */
const FILTER_PANEL_KEY='arac_puan_filtre_paneli';
const filtPanel=document.getElementById('filterpanel');
const filtToggle=document.getElementById('filttoggle');
const filtBadge=document.getElementById('filtbadge');
const filtClear=document.getElementById('filtclear');

function activeFilterCount(){let n=0;Object.keys(F).forEach(k=>n+=F[k].size);return n+activeRangeCount();}
function updateFilterBadge(){
 const n=activeFilterCount();
 if(filtBadge)filtBadge.textContent=n?String(n):'';
 if(filtToggle)filtToggle.classList.toggle('on',n>0);
 if(filtClear)filtClear.classList.toggle('disabled',n===0);
}
function setFilterPanel(open){
 if(!filtPanel)return;
 filtPanel.classList.toggle('open',open);
 if(filtToggle)filtToggle.setAttribute('aria-expanded',open?'true':'false');
 try{localStorage.setItem(FILTER_PANEL_KEY,open?'1':'0');}catch(e){}
}
function clearAllFilters(){
 Object.keys(F).forEach(k=>{F[k]=new Set();});
 RANGE_DEFS.forEach(d=>{RNG[d.k]=[null,null];});
 renderFilters();render();
}
if(filtToggle)filtToggle.onclick=()=>setFilterPanel(!filtPanel.classList.contains('open'));
if(filtClear)filtClear.onclick=()=>clearAllFilters();
(function(){
 let open=false;
 try{open=localStorage.getItem(FILTER_PANEL_KEY)==='1';}catch(e){open=false;}
 if(filtPanel)filtPanel.classList.toggle('open',open);
 if(filtToggle)filtToggle.setAttribute('aria-expanded',open?'true':'false');
})();
