/* ---------- compare section ---------- */
function renderCompare(){
 const area=document.getElementById('cmpArea'), empty=document.getElementById('cmpEmpty');
 if(cmpSet.length===0){area.classList.remove('show');empty.style.display='block';area.innerHTML='';return;}
 empty.style.display='none';area.classList.add('show');
 const cars=cmpSet.map(id=>CARS[id]);
 let html='<div class="cmpcards">';
 cars.forEach(c=>{html+='<div class="cmpcard"><div class="nm">'+c.n+'</div><div class="tag">'+c.tag+'</div><div class="spec">'+c.y+' &middot; '+c.hp+' bg &middot; '+c.disp.toFixed(1)+'L</div><div class="price">'+c.p[0]+'&ndash;'+c.p[1]+' bin TL</div><div style="margin-top:8px;font-family:var(--mono);font-weight:600;font-size:18px;color:'+colorFor(total(c))+'">'+total(c).toFixed(1)+' puan</div></div>';});
 html+='</div>';
 html+='<div class="radarwrap cmpradarbig">'+radarSVG(cars,420)+'</div>';
 // legend for radar colors
 const colors=['#5d8f6e','#5b83a8','#bd8a2c','#bb6a62'];
 html+='<div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-bottom:22px;font-family:var(--mono);font-size:12px;color:var(--dim)">';
 cars.forEach((c,i)=>{html+='<span><span style="display:inline-block;width:11px;height:11px;border-radius:3px;background:'+colors[i%4]+';margin-right:6px;vertical-align:middle"></span>'+c.n+'</span>';});
 html+='</div>';
 // table
 html+='<div class="tablewrap"><div class="scroll"><table class="cmptable"><thead><tr><th style="text-align:left;padding-left:14px">Kriter</th>';
 cars.forEach(c=>html+='<th>'+c.n+'</th>');
 html+='</tr></thead><tbody>';
 const rowsDef=[['Model Yılı',c=>c.y,null],['Beygir',c=>c.hp+' bg',c=>c.hp],['Motor Hacmi',c=>c.disp.toFixed(1)+'L',null],['Şanzıman Tipi',c=>c.tx,null],['Tahmini Fiyat',c=>c.p[0]+'-'+c.p[1]+' bin TL',c=>-c.p[0]]];
 rowsDef.forEach(([lbl,fmt,cmpfn])=>{
  html+='<tr><td class="rowlbl">'+lbl+'</td>';
  let best=null;
  if(cmpfn){const vals=cars.map(cmpfn);best=Math.max(...vals);}
  cars.forEach(c=>{const isBest=cmpfn&&cmpfn(c)===best;html+='<td'+(isBest?' class="best"':'')+'>'+fmt(c)+'</td>';});
  html+='</tr>';
 });
 CRIT.forEach(cr=>{
  html+='<tr><td class="rowlbl">'+cr.t+'</td>';
  const vals=cars.map(c=>c.S[cr.k]); const best=Math.max(...vals);
  cars.forEach(c=>{const v=c.S[cr.k];const isBest=v===best;const weak=cr.k!=='price'&&v<WEAK_THR;
   html+='<td class="'+(isBest?'best':(weak?'sc weak':''))+'">'+v+'</td>';});
  html+='</tr>';
 });
 html+='<tr><td class="rowlbl">Toplam Puan</td>';
 const tots=cars.map(total); const bestT=Math.max(...tots);
 cars.forEach(c=>{const t=total(c);html+='<td'+(t===bestT?' class="best"':'')+' style="font-weight:700">'+t.toFixed(1)+'</td>';});
 html+='</tr>';
 html+='</tbody></table></div></div>';
 area.innerHTML=html;
}
