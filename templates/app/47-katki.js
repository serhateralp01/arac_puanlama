/* ---------- kaynak öner formu ---------- */
/* Form, sunucusuz bir sayfadan e-posta göndermek için FormSubmit'i kullanıyor
   (formsubmit.co). Kayıt gerektirmiyor, ücretsiz ve sınırsız.

   AKTİFLEŞTİRME — tek yapılması gereken:
   Aşağıdaki FORM_ENDPOINT değişkenine FormSubmit'in verdiği adresi yazın.
   İki biçim de çalışır:
     'https://formsubmit.co/ornek@ornek.com'          (ilk gönderimde onay postası gelir)
     'https://formsubmit.co/a1b2c3d4e5f6...'          (onay sonrası verilen gizli uç nokta)
   İkinci biçim tercih edilmeli: ham e-posta adresi HTML kaynağında görünmezse
   spam robotları adresi toplayamaz.

   Değişken boş bırakıldığı sürece form görünür ama gönderim kapalıdır ve
   kullanıcıya bunun neden böyle olduğu açıkça söylenir. Sessizce başarısız olan
   bir form, hiç olmayan bir formdan daha kötüdür. */
const FORM_ENDPOINT = '';

(function(){
 const form=document.getElementById('ktForm');
 if(!form)return;
 const carSel=document.getElementById('ktCar');
 const critSel=document.getElementById('ktCriterion');
 const notice=document.getElementById('ktNotice');
 const submit=document.getElementById('ktSubmit');
 const status=document.getElementById('ktStatus');

 /* Araç listesi veriden doldruluyor; elle yazılan bir liste veriyle
    hızla uyumsuz hale gelirdi. */
 const opts=['<option value="">— araç seçin —</option>'];
 [...CARS].sort((a,b)=>a.n.localeCompare(b.n,'tr')).forEach(c=>{
  opts.push('<option>'+c.n+' ('+c.y+')</option>');
 });
 opts.push('<option value="listede-yok">— aradığım araç listede yok —</option>');
 carSel.innerHTML=opts.join('');

 const crits=['<option value="">— kriter seçin —</option>','<option value="genel">Genel / emin değilim</option>'];
 CRIT.forEach(c=>{ if(!c.AUTO) crits.push('<option>'+c.t+'</option>'); });
 critSel.innerHTML=crits.join('');

 if(FORM_ENDPOINT){
  form.action=FORM_ENDPOINT;
  /* FormSubmit ayarları: konu başlığı, CAPTCHA kapalı, tablo biçimli e-posta. */
  [['_subject','Araç Puanlama — kaynak önerisi'],['_captcha','false'],['_template','table']]
   .forEach(([n,v])=>{const i=document.createElement('input');i.type='hidden';i.name=n;i.value=v;form.appendChild(i);});
  notice.style.display='none';
 }else{
  notice.className='ktnotice warn';
  notice.innerHTML='<b>Form henüz gönderime kapalı.</b> Önerileri toplayacak e-posta adresi hazırlanıyor; adres tanımlandığı anda bu form çalışmaya başlayacak. O zamana kadar aşağıdaki alanları görebilir ama gönderemezsiniz.';
  submit.disabled=true;
  submit.classList.add('disabled');
 }

 form.addEventListener('submit',e=>{
  if(!FORM_ENDPOINT){e.preventDefault();return;}
  if(document.getElementById('ktHoney').value){e.preventDefault();return;}
  if(!form.checkValidity()){
   e.preventDefault();
   status.textContent='Yıldızlı alanların doldurulması gerekiyor.';
   status.className='ktstatus err';
   form.reportValidity();
   return;
  }
  status.textContent='Gönderiliyor...';
  status.className='ktstatus';
 });
})();
