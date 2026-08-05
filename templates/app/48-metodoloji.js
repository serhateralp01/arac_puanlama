/* ---------- metodoloji ekranı: canlı istatistikler ---------- */
/* Metodoloji sayfasındaki sayılar veriden hesaplanıyor, elle yazılmıyor;
   böylece veri değiştikçe sayfa da otomatik güncel kalıyor. */
(function(){
 const box=document.getElementById('methStats');
 if(!box)return;
 const total=CARS.length;
 const verified=CARS.filter(c=>c.v===true).length;
 const partial=CARS.filter(c=>c.v==='p').length;
 const avgSources=(CARS.reduce((sum,c)=>sum+(c.r?c.r.length:0),0)/total).toFixed(2);
 const sourceCount=Object.keys(R).length;
 const stats=[
  [total, 'araç'],
  [sourceCount, 'kaynak'],
  [verified, 'doğrulanmış araç'],
  [partial, 'kısmi kaynaklı araç'],
  [avgSources, 'araç başına ortalama kaynak'],
 ];
 box.innerHTML=stats.map(([v,l])=>'<div class="methstat"><b>'+v+'</b><span>'+l+'</span></div>').join('');
})();
