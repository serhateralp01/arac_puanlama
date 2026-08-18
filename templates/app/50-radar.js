/* ---------- radar chart (pure SVG) ---------- */
const RADAR_KEYS=['motor','trans','fun','comf','age','cost','liq'];
const RADAR_LABELS={motor:'Motor',trans:'Şanzıman',fun:'Keyif',comf:'Kullanım',age:'Yaş',cost:'Maliyet',liq:'Bulunur.'};
/* Renkler CSS değişkeninden okunuyor, sabit hex değil — böylece koyu temaya
   geçilince (Y-09) grafik de temayla birlikte değişiyor, ayrı bir JS anahtarı
   tutmaya gerek kalmıyor. */
function cssVar(name){return getComputedStyle(document.documentElement).getPropertyValue(name).trim();}
function radarSVG(carsToPlot,size){
 size=size||260;
 const cx=size/2, cy=size/2, R=size*0.34, n=RADAR_KEYS.length;
 const gridColor=cssVar('--line'), labelColor=cssVar('--dim');
 const colors=[cssVar('--sage'),cssVar('--blue'),cssVar('--amber'),cssVar('--red')];
 function pt(i,val){const ang=(Math.PI*2*i/n)-Math.PI/2;const r=R*(val/100);return [cx+r*Math.cos(ang),cy+r*Math.sin(ang)];}
 let svg='<svg viewBox="0 0 '+size+' '+size+'" width="100%" height="100%">';
 // grid rings
 [0.25,0.5,0.75,1].forEach(f=>{
  let pts=[];for(let i=0;i<n;i++){const [x,y]=pt(i,100*f);pts.push(x+','+y);}
  svg+='<polygon points="'+pts.join(' ')+'" fill="none" stroke="'+gridColor+'" stroke-width="1"/>';
 });
 // axes + labels
 for(let i=0;i<n;i++){const [x,y]=pt(i,100);
  svg+='<line x1="'+cx+'" y1="'+cy+'" x2="'+x+'" y2="'+y+'" stroke="'+gridColor+'" stroke-width="1"/>';
  const ang=(Math.PI*2*i/n)-Math.PI/2; const lx=cx+(R+18)*Math.cos(ang), ly=cy+(R+18)*Math.sin(ang);
  svg+='<text x="'+lx+'" y="'+ly+'" font-family="IBM Plex Mono, monospace" font-size="9.5" fill="'+labelColor+'" text-anchor="middle" dominant-baseline="middle">'+RADAR_LABELS[RADAR_KEYS[i]]+'</text>';
 }
 // data polygons
 carsToPlot.forEach((c,ci)=>{
  let pts=[];RADAR_KEYS.forEach((k,i)=>{const [x,y]=pt(i,c.S[k]);pts.push(x+','+y);});
  const col=colors[ci%colors.length];
  svg+='<polygon points="'+pts.join(' ')+'" fill="'+col+'" fill-opacity="0.14" stroke="'+col+'" stroke-width="2"/>';
  RADAR_KEYS.forEach((k,i)=>{const [x,y]=pt(i,c.S[k]);svg+='<circle cx="'+x+'" cy="'+y+'" r="2.6" fill="'+col+'"/>';});
 });
 svg+='</svg>';
 return svg;
}
