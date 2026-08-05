/* ---------- dynamic (faceted) MULTI-SELECT filters ---------- */
/* Each filter category holds a Set of selected values. Empty set = no restriction ("Hepsi"). */
const F={tx:new Set(),fuel:new Set(),disp:new Set(),hp:new Set(),drv:new Set(),body:new Set(),budget:new Set(),brand:new Set()};
let searchTerm='';
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
 // hp bucket group
 const gh=document.createElement('div');gh.className='fgroup';gh.innerHTML='<span class="flabel">Beygir</span>';
 const ah=document.createElement('button');ah.className='btn'+(F.hp.size===0?' on':'');ah.textContent='Hepsi';ah.onclick=()=>clearSet('hp');gh.appendChild(ah);
 HP_BUCKETS.forEach(([v,t,fn])=>{const has=CARS.some(c=>matchesFilter(c,'hp')&&fn(c));
  const b=document.createElement('button');b.className='btn'+(F.hp.has(v)?' on':'')+(has?'':' disabled');b.textContent=t;
  if(has)b.onclick=()=>toggleSetVal('hp',v);gh.appendChild(b);});
 fWrap.appendChild(gh);
 // budget bucket group
 const gb=document.createElement('div');gb.className='fgroup';gb.innerHTML='<span class="flabel">Bütçe</span>';
 const ab=document.createElement('button');ab.className='btn'+(F.budget.size===0?' on':'');ab.textContent='Hepsi';ab.onclick=()=>clearSet('budget');gb.appendChild(ab);
 BUDGET_BUCKETS.forEach(([v,t,fn])=>{const has=CARS.some(c=>matchesFilter(c,'budget')&&fn(c));
  const b=document.createElement('button');b.className='btn'+(F.budget.has(v)?' on':'')+(has?'':' disabled');b.textContent=t;
  if(has)b.onclick=()=>toggleSetVal('budget',v);gb.appendChild(b);});
 fWrap.appendChild(gb);
}

/* search */
const searchInp=document.getElementById('search'), searchClr=document.getElementById('searchclr');
searchInp.addEventListener('input',()=>{searchTerm=searchInp.value.trim().toLowerCase();searchClr.style.display=searchTerm?'block':'none';renderFilters();render();});
searchClr.onclick=()=>{searchInp.value='';searchTerm='';searchClr.style.display='none';renderFilters();render();};
