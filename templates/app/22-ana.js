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
    setinin uygulandığı ve listenin nasıl sıralandığı. */
 const pathsBox=document.getElementById('anaPaths');
 if(pathsBox){
  pathsBox.innerHTML='';
  const pathDefs=[
   {t:'Güvenilirlik öncelikli ilk on',d:'Ağırlıklar "Güvenilirlik öncelikli" sete döner, liste toplam puana göre azalan sıralanır.',
    run:()=>{W={...PRESETS.family};syncWeights();sortKey='tot';sortDir=-1;}},
   {t:'Sürüş keyfi öncelikli ilk on',d:'Ağırlıklar "Sürüş keyfi öncelikli" sete döner, liste toplam puana göre azalan sıralanır.',
    run:()=>{W={...PRESETS.enthusiast};syncWeights();sortKey='tot';sortDir=-1;}},
  ];
  pathDefs.forEach(p=>{
   const b=document.createElement('button');b.type='button';b.className='btn anapathbtn';
   b.innerHTML='<span class="apt">'+p.t+'</span><span class="apd">'+p.d+'</span>';
   b.onclick=()=>{p.run();if(typeof syncSortSelect==='function')syncSortSelect();recalcAll();goTo('liste');};
   pathsBox.appendChild(b);
  });

  /* Bütçeye göre en iyiler (Y-25 ikinci faz). Eskiden bu yol yalnızca
     listeyi en ucuzdan sıralıyordu ve kullanıcının girdiği bir sınır yoktu —
     "bütçeye göre" adını hak etmiyordu, çünkü 5 milyonluk bir araç da
     "en ucuz" sıralamada bir yerde görünüyordu. Şimdi kullanıcı gerçek bir
     üst sınır giriyor; ağırlıklar değişmiyor, yalnızca fiyat aralık filtresi
     (aynı RNG.price mekanizması, liste ekranındaki kaydırıcıyla paylaşılıyor)
     uygulanıp o sınırın altında kalanlar toplam puana göre sıralanıyor. */
  const budgetBox=document.createElement('div');
  budgetBox.className='anapathbtn anapath-budget';
  budgetBox.innerHTML='<span class="apt">Bütçeye göre en iyiler</span>'
   +'<span class="apd">Üst sınırınızı girin; o sınırın altında kalan araçlar toplam puana göre sıralanır.</span>'
   +'<div class="apinput"><input type="number" id="anaBudget" min="0" step="25" placeholder="ör. 700"><span class="runit">bin TL</span>'
   +'<button type="button" class="btn small" id="anaBudgetGo">Göster</button></div>';
  pathsBox.appendChild(budgetBox);
  const budgetInput=budgetBox.querySelector('#anaBudget');
  const budgetGo=()=>{
   const v=+budgetInput.value;
   if(!v||v<=0){budgetInput.focus();return;}
   setRange('price',1,v,false);
   sortKey='tot';sortDir=-1;
   if(typeof syncSortSelect==='function')syncSortSelect();
   recalcAll();
   goTo('liste');
  };
  budgetBox.querySelector('#anaBudgetGo').onclick=budgetGo;
  budgetInput.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();budgetGo();}});
  budgetInput.addEventListener('click',e=>e.stopPropagation());
 }

 /* En yüksek puanlı beş araç: şu anki ağırlık ayarına göre. Ayar
    değiştirildiğinde bu ekrana her dönüşte yeniden hesaplanıyor. Ad, aracın
    kendi statik sayfasına (arac/<cid>.html, build_pages.py'nin ürettiği kanıt
    sayfası) bağlanıyor — önceden düz metindi (Y-25 dördüncü faz). */
 const topBox=document.getElementById('anaTop');
 if(topBox){
  const ranked=[...CARS].sort((a,b)=>total(b)-total(a)).slice(0,5);
  topBox.innerHTML=ranked.map(c=>'<li><a class="an anlink" href="arac/'+c.cid+'.html">'+c.n+'</a><span class="av">'+total(c).toFixed(1)+'</span></li>').join('');
 }

 /* Kullanıcının asıl aradığı bilgi: hangi motor/şanzıman beni yakar. Bu
    liste build.py tarafından motor ve şanzıman ailelerinin base_score'undan
    türetilip DB'ye gömülüyor (bkz. scripts/build.py riskiest()); kaynağı
    bileşen kaydı, çünkü kanıtın aslı orada duruyor. Adlar artık build_pages.py
    tarafından üretilen kanıt sayfasına bağlanıyor (motor/<id>.html,
    sanziman/<id>.html) — önceden bu bulgu düz metindi, arkasındaki bilinen
    arıza kaydına ana ekrandan hiç erişilemiyordu (Y-25 dördüncü faz). */
 const riskEngineBox=document.getElementById('anaRiskEngine');
 const riskTransBox=document.getElementById('anaRiskTrans');
 const riskRow=dir=>e=>'<li><a class="an anlink" href="'+dir+'/'+e.id+'.html">'+e.name+'</a><span class="av risky">'+e.score+'</span></li>';
 if(riskEngineBox)riskEngineBox.innerHTML=DB.riskiest_engines.map(riskRow('motor')).join('');
 if(riskTransBox)riskTransBox.innerHTML=DB.riskiest_transmissions.map(riskRow('sanziman')).join('');
}
