/* ---------- ana ekran (#ana, Y-07) ---------- */
/* Giriş akışı bittikten sonra kullanıcı doğrudan tüm satırları içeren tabloya
   düşmüyor; #liste ile #giris arasına giren bu ekran nereden başlayacağını
   gösteriyor. İçeriğin tamamı veriden hesaplanıyor, elle yazılmıyor — liste
   büyüdükçe ya da kaynak sayısı değiştikçe sayfa kendiliğinden güncel kalıyor.

   renderAna bir fonksiyon bildirimi olduğu için üst kapsama yükseltiliyor
   (hoisting); bu yüzden 99-baslat.js içinden, bütün parçalar yüklendikten
   sonra çağrılması yeterli, dosya sırası önemli değil. */
function renderAna(){
 const statBox=document.getElementById('anaStats');
 if(!statBox)return; // #ana ekranı derlenmediyse sessizce çık

 const totalCars=CARS.length;
 const sourceCount=Object.keys(R).length;
 const avgSources=(CARS.reduce((s,c)=>s+(c.r?c.r.length:0),0)/totalCars).toFixed(2);
 const stats=[
  [totalCars,'araç'],
  [DB.engine_count,'motor ailesi'],
  [DB.transmission_count,'şanzıman kutusu'],
  [sourceCount,'kaynak'],
  [avgSources,'araç başına ortalama kaynak'],
 ];
 statBox.innerHTML=stats.map(([v,l])=>'<div class="methstat"><b>'+v+'</b><span>'+l+'</span></div>').join('');

 /* Hazır giriş yolları: üçü de listeye götürür, farkları hangi ağırlık
    setinin uygulandığı ve listenin nasıl sıralandığı. "Bütçeye göre başla"
    ağırlıkları değiştirmiyor; yalnızca sıralamayı fiyata çeviriyor, çünkü
    bütçeyle başlamak isteyen kullanıcı önce en ucuzu görmek istiyor. */
 const pathsBox=document.getElementById('anaPaths');
 if(pathsBox){
  const pathDefs=[
   {t:'Güvenilirlik öncelikli ilk on',d:'Ağırlıklar "Güvenilirlik öncelikli" sete döner, liste toplam puana göre azalan sıralanır.',
    run:()=>{W={...PRESETS.family};syncWeights();sortKey='tot';sortDir=-1;}},
   {t:'Bütçeye göre başla',d:'Ağırlıklar değişmez, liste en ucuz araçtan başlayarak sıralanır.',
    run:()=>{sortKey='pband';sortDir=1;}},
   {t:'Sürüş keyfi öncelikli ilk on',d:'Ağırlıklar "Sürüş keyfi öncelikli" sete döner, liste toplam puana göre azalan sıralanır.',
    run:()=>{W={...PRESETS.enthusiast};syncWeights();sortKey='tot';sortDir=-1;}},
  ];
  pathsBox.innerHTML='';
  pathDefs.forEach(p=>{
   const b=document.createElement('button');b.type='button';b.className='btn anapathbtn';
   b.innerHTML='<span class="apt">'+p.t+'</span><span class="apd">'+p.d+'</span>';
   b.onclick=()=>{p.run();recalcAll();goTo('liste');};
   pathsBox.appendChild(b);
  });
 }

 /* En yüksek puanlı beş araç: şu anki ağırlık ayarına göre. Ayar
    değiştirildiğinde bu ekrana her dönüşte yeniden hesaplanıyor. */
 const topBox=document.getElementById('anaTop');
 if(topBox){
  const ranked=[...CARS].sort((a,b)=>total(b)-total(a)).slice(0,5);
  topBox.innerHTML=ranked.map(c=>'<li><span class="an">'+c.n+'</span><span class="av">'+total(c).toFixed(1)+'</span></li>').join('');
 }

 /* Kullanıcının asıl aradığı bilgi: hangi motor/şanzıman beni yakar. Bu
    liste build.py tarafından motor ve şanzıman ailelerinin base_score'undan
    türetilip DB'ye gömülüyor (bkz. scripts/build.py riskiest()); kaynağı
    bileşen kaydı, çünkü kanıtın aslı orada duruyor. */
 const riskEngineBox=document.getElementById('anaRiskEngine');
 const riskTransBox=document.getElementById('anaRiskTrans');
 const riskRow=e=>'<li><span class="an">'+e.name+'</span><span class="av risky">'+e.score+'</span></li>';
 if(riskEngineBox)riskEngineBox.innerHTML=DB.riskiest_engines.map(riskRow).join('');
 if(riskTransBox)riskTransBox.innerHTML=DB.riskiest_transmissions.map(riskRow).join('');
}
