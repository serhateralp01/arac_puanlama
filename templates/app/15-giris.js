/* ---------- giriş (onboarding) adımları ---------- */
/* Giriş ekranının kendi içinde üç adımı var; bunlar ayrı rota değil, aynı
   #giris ekranının alt durumu. Adımlar arasında geçiş, ekranlar arasındaki
   geçişle aynı mantığı taşıyor: hiçbir şey yeniden yüklenmiyor. */
(function(){
 const panels=()=>Array.from(document.querySelectorAll('.opanel'));
 const dotsWrap=document.getElementById('odots');
 const N=document.querySelectorAll('.opanel').length;
 let step=1;

 for(let i=1;i<=N;i++){const d=document.createElement('span');d.className='d'+(i===1?' on':'');dotsWrap.appendChild(d);}

 function render(){
  panels().forEach(p=>p.classList.toggle('on',+p.dataset.step===step));
  dotsWrap.querySelectorAll('.d').forEach((d,i)=>d.classList.toggle('on',i+1===step));
  document.getElementById('oprev').style.visibility=step===1?'hidden':'visible';
  document.getElementById('onext').style.visibility=step===N?'hidden':'visible';
 }
 document.getElementById('onext').onclick=()=>{if(step<N){step++;render();}};
 document.getElementById('oprev').onclick=()=>{if(step>1){step--;render();}};
 /* Giriş bittiğinde artık doğrudan tabloya değil, ana ekrana gidiliyor
    (Y-07); DEFAULT_ROUTE de aynı hedefi gösteriyor, bu yüzden ikisi burada
    birbirinden kopmuyor. */
 document.getElementById('oskip').onclick=()=>{markOnboardingSeen();goTo('ana');};
 document.getElementById('oenter').onclick=()=>{markOnboardingSeen();goTo('ana');};
 render();
})();
