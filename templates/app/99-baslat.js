/* ---------- başlatma ---------- */
/* Bütün ekranlar sayfada birden duruyor, bu yüzden hepsi bir kez burada
   doldurulur. Yönlendirici yalnızca hangisinin görüneceğine karar verir;
   ekran değiştirmek veriyi yeniden üretmez, dolayısıyla kıyaslama sepeti
   ve filtre seçimleri gezinirken korunur. */
buildPresetButtons();
renderFilters();
render();
updateContrib();
renderTray();
renderCompare();
renderAna();

const refUl=document.getElementById('refs');
Object.keys(R).forEach(k=>{const li=document.createElement('li');
 li.innerHTML=R[k][0]+'. Kaynak: <a href="'+R[k][2]+'" target="_blank" rel="noopener">'+R[k][1]+'</a>';refUl.appendChild(li);});
document.getElementById('foot').textContent=DB.build_stamp+' · Bu listede '+CARS.length+' otomatik vitesli araç bulunuyor. Puanlar mutlak bir ölçü değildir; yalnızca bu liste içindeki araçların birbirine göre durumunu gösterir. Bir kriterde 35 altında kalan puan zayıf halka sayılır ve tabloda kırmızı işaretlenir.';

startRouter();
startNavToggle();
