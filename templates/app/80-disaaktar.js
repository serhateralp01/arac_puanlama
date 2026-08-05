/* ---------- export CSV ---------- */
document.getElementById('exportBtn').onclick=()=>{
 const cols=['Araç','Model Yılı','Beygir','Hacim','Şanzıman','Yakıt','Çekiş','Fiyat Alt','Fiyat Üst',...CRIT.map(c=>c.t),'Toplam Puan','Normalize Puan'];
 let csv=cols.join(';')+'\n';
 visible.forEach(c=>{
  const row=[c.n,c.y,c.hp,c.disp,c.tx,c.fuel,c.drv,c.p[0],c.p[1],...ORDER.map(k=>c.S[k]),total(c).toFixed(1),normOf(c).toFixed(0)];
  csv+=row.map(x=>('"'+String(x).replace(/"/g,'""')+'"')).join(';')+'\n';
 });
 const blob=new Blob(['﻿'+csv],{type:'text/csv;charset=utf-8;'});
 const url=URL.createObjectURL(blob);
 const a=document.createElement('a');a.href=url;a.download='arac-puanlama-listesi.csv';a.click();
 URL.revokeObjectURL(url);
};
