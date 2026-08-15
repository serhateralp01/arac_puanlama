/* ==== Katalogda bulunan ama henüz puanlanmamış araçlar (MK-22) ====

   Neden ayrı bir blok, neden tablonun içinde değil.
   Katalog araçlarının puanı yoktur. Puan tablosuna null puanlı satırlar koymak,
   sıralamayı, ağırlıklandırmayı, normalize puanı ve "zayıf halka" işaretlemesini
   bozardı; kullanıcı da puanlanmış bir araçla puanlanmamış birini yan yana görüp
   ikisinin aynı titizlikten geçtiğini sanırdı. Bu yüzden katalog sonuçları
   tablonun altında, kendi başlığı ve kendi uyarısıyla duruyor.

   Neden yalnızca arama yapılınca görünüyor.
   1.345 kaydı her açılışta listelemek, asıl ürünü (278 puanlanmış araç) görsel
   olarak boğardı. Blok yalnız kullanıcı bir şey aradığında ve o arama tabloda
   karşılık bulmadığında değerli: "benim arabam listede var mı" sorusuna
   "puanlamadık ama künyesi burada" cevabını veriyor. */

const CATALOG = (DB.catalog || []);
const CAT_LIMIT = 24; /* bir aramada gösterilecek azami kayıt */

/* Katalog metinleri dış bir veri paketinden geliyor. Bugün hepsi zararsız olsa da
   innerHTML'e ham konmamalı: kaynak paket yenilendiğinde içine < veya & giren bir
   model adı sayfayı bozabilir. */
function catEsc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function catalogMatches(term) {
  if (!term) return [];
  const out = [];
  for (let i = 0; i < CATALOG.length; i++) {
    const c = CATALOG[i];
    const hay = (c.n + ' ' + c.g + ' ' + c.f + ' ' + c.tx + ' ' +
                 (c.b || '') + ' ' + c.y + ' ' + c.hp).toLowerCase();
    if (hay.indexOf(term) !== -1) out.push(c);
  }
  return out;
}

function renderCatalog() {
  const wrap = document.getElementById('catwrap');
  if (!wrap) return;
  const term = (typeof searchTerm === 'string' ? searchTerm : '').trim();
  if (!term) { wrap.innerHTML = ''; wrap.style.display = 'none'; return; }

  const hits = catalogMatches(term);
  if (!hits.length) { wrap.innerHTML = ''; wrap.style.display = 'none'; return; }

  const shown = hits.slice(0, CAT_LIMIT);
  let rows = '';
  shown.forEach(c => {
    const spec = [c.y, c.hp + ' bg', c.d ? c.d.toFixed(1) + ' L' : null, c.f, c.tx, c.b]
      .filter(Boolean).join(' · ');
    rows += '<li class="catitem">'
      + '<a class="catname" href="katalog/' + c.id + '.html">' + catEsc(c.n) + '</a>'
      + '<span class="catspec">' + catEsc(spec) + '</span></li>';
  });

  const more = hits.length > shown.length
    ? '<p class="note">Aramaya uyan ' + hits.length + ' katalog kaydından ilk '
      + shown.length + ' tanesi gösteriliyor. Aramayı daraltarak listeyi küçültebilirsiniz.</p>'
    : '';

  wrap.style.display = '';
  wrap.innerHTML =
    '<h3 class="cattitle">Katalogda var, henüz puanlanmadı — ' + hits.length + ' araç</h3>'
    + '<p class="lede">Bu araçlar veri tabanında <b>teknik künyeleriyle</b> kayıtlı ama '
    + 'henüz puanlanmadı. Bir aracın puan alması için motor ve şanzıman ailesinin arıza '
    + 'sicilinin araştırılmış, en az dört bağımsız kaynağa bağlanmış ve her puanın '
    + 'gerekçesinin yazılmış olması gerekiyor. O aşamadan geçmemiş bir araca tahmini puan '
    + 'vermek yerine, künyesini olduğu gibi gösteriyoruz.</p>'
    + '<ul class="catlist">' + rows + '</ul>' + more;
}
