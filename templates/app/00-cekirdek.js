const DB=/*__DB__*/null;
const R=DB.sources, CARS=DB.cars;

const ORDER=DB.full_order, SCORED=DB.scored_order;
const CRIT=DB.criteria;
const HEAD=DB.head_labels;
const WEAK_THR=DB.weak_threshold;
const PRESETS=DB.presets;
let W={...PRESETS.custom};
try{ const saved=localStorage.getItem('arac_puan_agirlik'); if(saved){ const o=JSON.parse(saved); ORDER.forEach(k=>{ if(o[k]!==undefined) W[k]=o[k]; }); } }catch(e){}

CARS.forEach((c,i)=>{c.id=i;c.S={};SCORED.forEach((k,j)=>c.S[k]=c.s[j]);});
function mid(c){return (c.p[0]+c.p[1])/2;}
function recalcPrice(){const ms=CARS.map(mid),lo=Math.min(...ms),hi=Math.max(...ms);
 CARS.forEach(c=>{c.S.price=hi===lo?50:Math.round(100*(hi-mid(c))/(hi-lo));});}
recalcPrice();
function sumW(){let t=0;ORDER.forEach(k=>t+=(+W[k]||0));return t;}
function total(c){const sw=sumW();if(sw<=0)return 0;let t=0;ORDER.forEach(k=>t+=c.S[k]*(+W[k]||0));return t/sw;}
function normOf(c){const ts=CARS.map(total),lo=Math.min(...ts),hi=Math.max(...ts);
 return hi===lo?100:100*(total(c)-lo)/(hi-lo);}
function colorFor(t){if(t>=72)return 'var(--sage)';if(t>=64)return '#c9a34e';if(t>=58)return 'var(--amber)';return 'var(--red)';}
function weakOnes(c){return SCORED.filter(k=>c.S[k]<WEAK_THR).map(k=>({k,v:c.S[k]}));}

/* ---------- weak-link reason generator ---------- */
function weakReason(c,k){
  const tx=c.tx, note=c.note;
  if(k==='trans'){
    if(tx.indexOf('Kuru')>-1) return 'Bu aracın otomatiği kuru kavramalı bir çift kavrama kutusu. Bu tip kutular Türkiye trafiğinde, özellikle yoğun şehir içi kullanımda, kavrama aşınması ve ısınma riski taşıyor.';
    if(tx==='CVT') return 'Bu aracın otomatiği CVT; markaya göre değişmekle birlikte bazı CVT kutuları yağ bakımı ihmal edildiğinde erken yıpranma gösteriyor ve tork konvertörlü kutular kadar dayanıklı kabul edilmiyor.';
    if(tx==='Robot') return 'Bu araçtaki kutu robotlu yarı otomatik; tek kavramalı bir mekanizmayı motor kontrol ünitesi yönetiyor. Vites geçişleri sarsıntılı ve aktüatör arızaları biliniyor.';
    return 'Bu aracın şanzımanı, listedeki tork konvertörlü kutulara göre daha fazla arıza riski taşıyor.';
  }
  if(k==='motor') return 'Bu motorda bilinen bir kronik arıza kalemi var; ayrıntısı için yukarıdaki açıklamayı okuyun.';
  if(k==='fun') return 'Bu araç güvenilirlik ve pratiklik önceliğiyle tasarlanmış; sürüş keyfi listenin gerisinde kalıyor.';
  if(k==='comf') return 'Bu araçta günlük kullanım konforu diğer kriterlere göre daha zayıf; sert süspansiyon, dar kabin veya zayıf ses yalıtımı gibi nedenler etkili olabiliyor.';
  if(k==='age') return 'Bu araç artık yaşlı bir model olduğu için pas, elektrik ve genel yıpranma riski yüksek.';
  if(k==='cost') return 'Bu aracın yakıt tüketimi, vergisi veya parça fiyatları listenin üzerinde; işletme maliyeti yüksek.';
  if(k==='liq') return 'Bu araç Türkiye ikinci el piyasasında az bulunuyor; alırken de satarken de daha fazla zaman gerekebilir.';
  return '';
}
