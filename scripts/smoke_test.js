/*
 * smoke_test.js — üretilmiş HTML gerçekten çalışıyor mu?
 *
 * Şema doğrulaması (scripts/validate.py) verinin tutarlı olduğunu söyler ama
 * sayfanın açıldığını söylemez. Bu betik dosyayı gerçek bir tarayıcıda açıp
 * tablonun dolduğunu, konsola hata düşmediğini ve etkileşimin (filtre,
 * kıyaslama, ağırlık) çalıştığını doğrular.
 *
 * Bir kontrol başarısız olduğunda veya beklenmedik bir hata çıktığında, o anki
 * ekran görüntüsü ve konsolun TAMAMI (yalnızca hatalar değil) debug/ klasörüne
 * yazılır. Amaç, "bir şey bozuldu" ile yetinmeyip "hangi adımda, ekranda ne
 * görünürken, konsolda ne yazarken bozuldu" sorusuna hızlı cevap vermek.
 *
 * Kullanım:
 *   node scripts/smoke_test.js            # normal çalıştırma
 *   node scripts/smoke_test.js --debug     # her adımda ekran görüntüsü al
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = 'file://' + path.join(ROOT, 'index.html');
const DEBUG_DIR = path.join(ROOT, 'scripts', '.smoke-debug');
const ALWAYS_SCREENSHOT = process.argv.includes('--debug');

// Araç sayısı Y-01/Y-19 turlarında sık değişiyor; sabit bir sayı her turda bu
// dosyayı elle güncellemeyi gerektirirdi. data/cars/ dizinini sayıp aynı sonucu
// veriyoruz — test artık veriyle birlikte otomatik güncelleniyor.
const CAR_COUNT = fs.readdirSync(path.join(ROOT, 'data', 'cars')).filter((f) => f.endsWith('.json')).length;

const checks = [];
const consoleLog = []; // konsolun tamamı — hata filtrelemeden önce, debug için
let page; // dumpDebug() içinden erişilebilsin diye üstte tanımlı

function check(name, ok, detail = '') {
  checks.push({ name, ok, detail });
  console.log(`${ok ? 'OK  ' : 'HATA'} ${name}${detail ? ' — ' + detail : ''}`);
}

async function dumpDebug(label) {
  fs.mkdirSync(DEBUG_DIR, { recursive: true });
  const stamp = label.replace(/[^a-z0-9-]+/gi, '_').slice(0, 60);
  const shotPath = path.join(DEBUG_DIR, `${stamp}.png`);
  const logPath = path.join(DEBUG_DIR, `${stamp}.console.log`);
  try {
    if (page) await page.screenshot({ path: shotPath, fullPage: true });
    fs.writeFileSync(logPath, consoleLog.join('\n') + '\n', 'utf-8');
    console.log(`  debug: ${path.relative(ROOT, shotPath)}, ${path.relative(ROOT, logPath)}`);
  } catch (e) {
    console.log(`  debug dökümü de başarısız oldu: ${e}`);
  }
}

(async () => {
  // Yerelde önceden kurulu bir Chromium varsa onu kullan; yoksa Playwright'ın
  // kendi indirdiği tarayıcıya düş (CI böyle çalışıyor).
  const launchOpts = process.env.CHROMIUM_PATH
    ? { executablePath: process.env.CHROMIUM_PATH }
    : {};
  const browser = await chromium.launch(launchOpts);
  page = await browser.newPage();

  const errors = [];
  // Google Fonts çevrimdışı ortamda yüklenemiyor; sayfa sistem fontuna düşüyor
  // ve bu beklenen davranış, JS hatası değil. Yine de tam log'a yazılıyor,
  // sadece "hata" listesine girmiyor.
  const isNetworkNoise = (t) => /ERR_|Failed to load resource/.test(t);
  page.on('pageerror', (e) => {
    consoleLog.push(`[pageerror] ${e}`);
    errors.push(String(e));
  });
  page.on('console', (m) => {
    consoleLog.push(`[${m.type()}] ${m.text()}`);
    if (m.type() === 'error' && !isNetworkNoise(m.text())) errors.push(m.text());
  });

  try {
    // Tarayıcı bağlamı her çalıştırmada sıfırdan açıldığı için localStorage boş;
    // yani bu, siteye ilk gelen kullanıcının gördüğü durum. Giriş ekranının
    // otomatik açılması bekleniyor.
    await page.goto(FILE);
    await page.waitForSelector('.screen[data-screen="giris"].on');
    const girisOk = await page.locator('[data-screen="giris"]').isVisible();
    const listeGizli = !(await page.locator('[data-screen="liste"]').isVisible());
    check('ilk ziyarette giriş ekranı açılıyor', girisOk && listeGizli);
    if (!(girisOk && listeGizli)) await dumpDebug('giris-acilmadi');

    // Koyu tema (Y-09): düğme temayı değiştirmeli, `<html data-theme>` ve gövde
    // rengi buna göre değişmeli, seçim sayfa yenilense bile kalıcı olmalı ve
    // orijinal duruma dönünce hiçbir kalıntı bırakmamalı — sonraki bütün
    // kontroller varsayılan (açık) temayı görmeyi bekliyor.
    const bgBefore = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    const labelBefore = await page.locator('#temaBtn').innerText();
    await page.click('#temaBtn');
    await page.waitForTimeout(150);
    const themeAttr = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    const bgAfter = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    const labelAfter = await page.locator('#temaBtn').innerText();
    const themeToggled = themeAttr !== null && bgAfter !== bgBefore && labelAfter !== labelBefore;
    check('koyu tema düğmesi rengi ve etiketi değiştiriyor', themeToggled,
      `${labelBefore} → ${labelAfter}, data-theme=${themeAttr}`);
    if (!themeToggled) await dumpDebug('koyu-tema-degismedi');

    await page.reload();
    await page.waitForSelector('#temaBtn');
    const themeAttrAfterReload = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    const bgAfterReload = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    check('koyu tema seçimi sayfa yenilenince kalıcı', themeAttrAfterReload === themeAttr && bgAfterReload === bgAfter,
      `data-theme=${themeAttrAfterReload}`);

    // Orijinal (açık) temaya dön ki geri kalan kontroller varsayılan görünümü görsün.
    await page.click('#temaBtn');
    await page.waitForTimeout(150);
    const themeAttrReset = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    const bgReset = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    check('koyu temadan geri dönülüyor', bgReset === bgBefore, `data-theme=${themeAttrReset}`);
    // Bu noktadan sonra giriş ekranı hâlâ açık (tema değişimi ekranı değiştirmedi).
    await page.waitForSelector('.screen[data-screen="giris"].on');

    // Giriş akışı bitince ana ekrana gidilmeli (Y-07), doğrudan tabloya değil.
    await page.click('#oskip');
    await page.waitForTimeout(200);
    const onAnaAfterOnboard = await page.locator('[data-screen="ana"]').isVisible();
    check('giriş sonrası ana ekrana gidiliyor', onAnaAfterOnboard);
    if (!onAnaAfterOnboard) await dumpDebug('giris-sonrasi-ana-degil');

    // Ana ekranın içeriği veriden hesaplanıyor; elle yazılmadığı için beş
    // istatistik kutusu, üç hazır giriş yolu, beş üst sıra ve beş+beş riskli
    // bileşen bekleniyor.
    const anaStats = await page.locator('#anaStats .methstat').count();
    check('ana ekran istatistikleri doluyor', anaStats === 5, `${anaStats} kutu`);
    const anaPaths = await page.locator('.anapathbtn').count();
    check('ana ekran hazır giriş yolları doluyor', anaPaths === 3, `${anaPaths} yol`);
    const anaTop = await page.locator('#anaTop li').count();
    check('ana ekran en yüksek puanlı liste doluyor', anaTop === 5, `${anaTop} satır`);
    const anaRiskEngine = await page.locator('#anaRiskEngine li').count();
    const anaRiskTrans = await page.locator('#anaRiskTrans li').count();
    check(
      'ana ekran riskli bileşen listeleri doluyor',
      anaRiskEngine === 5 && anaRiskTrans === 5,
      `motor=${anaRiskEngine} şanzıman=${anaRiskTrans}`
    );
    const anaWidth = await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2);
    check('ana ekranda yatay taşma yok', anaWidth);

    // Ana ekrandaki üç liste artık kanıt sayfalarına bağlanıyor (Y-25 dördüncü
    // faz): en yüksek puanlı araçlar kendi arac/<cid>.html sayfasına, en riskli
    // motor/şanzıman aileleri kendi motor|sanziman/<id>.html sayfasına. Önceden
    // düz metindi; buradaki tek risk href'in var olmayan bir dosyaya işaret
    // etmesiydi, o yüzden gerçek dosya sistemi karşı kontrol ediliyor.
    const anaLinkHrefs = await page.$$eval(
      '#anaTop a.anlink, #anaRiskEngine a.anlink, #anaRiskTrans a.anlink',
      (els) => els.map((e) => e.getAttribute('href'))
    );
    const anaLinksResolve = anaLinkHrefs.length === 15
      && anaLinkHrefs.every((h) => fs.existsSync(path.join(ROOT, h)));
    check('ana ekran bağlantıları var olan kanıt sayfalarına gidiyor',
      anaLinksResolve, `${anaLinkHrefs.length} bağlantı`);

    // Hazır giriş yollarından biri: tıklanınca ilgili ağırlık seti uygulanıp
    // listeye götürmeli.
    await page.locator('.anapathbtn').first().click();
    await page.waitForTimeout(200);
    const onListeAfterPath = await page.locator('[data-screen="liste"]').isVisible();
    check('hazır giriş yolu listeye götürüyor', onListeAfterPath);

    // Bütçe girişi (Y-25 ikinci faz): eskiden yalnızca "en ucuzdan sırala"
    // yapıyordu, kullanıcının girdiği bir sınır yoktu. Şimdi gerçek bir üst
    // sınır alıp o sınırın altında kalan araçları toplam puana göre
    // sıralaması gerekiyor.
    await page.click('.nav a[data-route="ana"]');
    await page.waitForTimeout(150);
    await page.fill('#anaBudget', '600');
    await page.click('#anaBudgetGo');
    await page.waitForTimeout(250);
    const onListeAfterBudget = await page.locator('[data-screen="liste"]').isVisible();
    const budgetCardCount = await page.locator('#cardgrid .vcard').count();
    const budgetTotals = await page.$$eval('#cardgrid .vcard .vctot', (els) => els.map((e) => parseFloat(e.textContent)));
    const budgetSorted = budgetTotals.every((v, i) => i === 0 || budgetTotals[i - 1] >= v);
    check('bütçe girişi listeyi sınırın altına daraltıp puana göre sıralıyor',
      onListeAfterBudget && budgetCardCount > 0 && budgetCardCount < CAR_COUNT && budgetSorted,
      `${budgetCardCount} araç (406'dan), sıralı=${budgetSorted}`);

    // Onboarding artık görüldü sayıldığı için hash'siz bir sonraki ziyaret de
    // doğrudan ana ekrana düşmeli, tekrar giriş akışına değil.
    await page.goto(FILE);
    await page.waitForTimeout(200);
    const directToAna = await page.locator('[data-screen="ana"]').isVisible();
    check('tekrar ziyarette hash yokken doğrudan ana ekrana gidiliyor', directToAna);

    // Bundan sonrası liste ekranında geçiyor. Kart görünümü artık varsayılan
    // (Y-25); önce onu doğruluyoruz, sonra ikinci sekme olan tabloya geçip
    // geri kalan bütün kontrolleri (aşağıdaki gibi) orada sürdürüyoruz —
    // çünkü tablo, sütun bazlı doğrulamalar için daha uygun bir yüzey.
    await page.goto(FILE + '#liste');
    await page.waitForSelector('#cardgrid .vcard');
    if (ALWAYS_SCREENSHOT) await dumpDebug('01-yuklendi');

    // ---------- kart görünümü (Y-25) ----------
    const cardViewOnByDefault = (await page.locator('#listeScreen.view-kart').count()) === 1;
    check('liste ekranı kart görünümüyle açılıyor', cardViewOnByDefault);
    const cardRows = await page.locator('#cardgrid .vcard').count();
    check('bütün araçlar kart olarak listeleniyor', cardRows === CAR_COUNT, `${cardRows} kart (beklenen ${CAR_COUNT})`);
    const tableHiddenInCardView = !(await page.locator('#tablewrap').isVisible());
    check('kart görünümündeyken tablo gizli', tableHiddenInCardView);

    // Ayrıntı içeriği eskiden 406 aracın hepsi için önceden inşa ediliyordu
    // (55.007 DOM düğümü, 595ms). Şimdi bir kart ilk kez açılana kadar
    // .vcdetail boş kalmalı; bu, o performans düzeltmesinin kalıcı kanıtı.
    const firstCard = page.locator('#cardgrid .vcard').first();
    const detailEmptyBeforeOpen = (await firstCard.locator('.vcdetail').innerHTML()) === '';
    check('kart ayrıntısı açılana kadar boş (tembel oluşturma)', detailEmptyBeforeOpen);
    await firstCard.locator('.vctoggle').click();
    await page.waitForTimeout(150);
    const detailFilledAfterOpen = (await firstCard.locator('.vcdetail .bdtable').count()) === 1;
    check('kart ayrıntısı ilk tıklamada dolduruluyor', detailFilledAfterOpen);

    // Fiyat, puanların aksine arayüzden düzenlenebilen tek alan (CLAUDE.md §6);
    // bu istisna kart görünümünde de geçerli olmalı.
    const cardPriceEditable = (await firstCard.locator('.vcprice .pin').count()) === 2;
    check('kart üzerinde fiyat aralığı düzenlenebiliyor', cardPriceEditable);

    // Kartlarda sütun başlığı yok; aynı işi gören açılır sıralama menüsü var.
    const sortSelVisible = await page.locator('#sortWrap').isVisible();
    check('sıralama seçimi kart görünümünde görünür', sortSelVisible);
    await page.selectOption('#sortSel', 'name');
    await page.waitForTimeout(150);
    const namesAfterSort = await page.locator('#cardgrid .vcname').allInnerTexts();
    const namesSorted = namesAfterSort.slice(1).every((t, i) => namesAfterSort[i].localeCompare(t, 'tr') <= 0);
    check('isme göre sıralama kartları alfabetik diziyor', namesSorted);
    await page.selectOption('#sortSel', 'tot');
    await page.waitForTimeout(150);

    // Görünüm düğmesi tabloya geçirmeli ve tercih localStorage'da kalıcı olmalı.
    await page.click('#viewToggle [data-view="tablo"]');
    await page.waitForSelector('#body tr.main');
    const onTableViewNow = (await page.locator('#listeScreen.view-tablo').count()) === 1;
    check('görünüm düğmesi tabloya geçiriyor', onTableViewNow);
    await page.reload();
    await page.waitForTimeout(200);
    const tableViewPersisted = (await page.locator('#listeScreen.view-tablo').count()) === 1;
    check('görünüm tercihi sayfa yenilenince kalıcı', tableViewPersisted);

    // ---------- tablo görünümü (ikinci sekme, Y-25) ----------
    await page.goto(FILE + '#liste');
    await page.waitForSelector('#body tr.main');

    const rows = await page.locator('#body tr.main').count();
    check('bütün araçlar tabloda listeleniyor', rows === CAR_COUNT, `${rows} satır (beklenen ${CAR_COUNT})`);

    check('JS hatası yok', errors.length === 0, errors.slice(0, 3).join(' | '));

    const crit = await page.locator('#rubric .card').count();
    check('sekiz kriter kartı var', crit === 8, `${crit} kart`);

    const sumText = await page.locator('#sumbox').innerText();
    check('ağırlık toplamı 100', sumText.includes('100'), sumText.replace(/\n/g, ' '));

    // Y-06 ikinci katman: her kritere ağırlık gerekçesi, bantlı yedi kriterin
    // hepsine puan bandı açılır paneli ve ağırlık payı göstergesi eklendi.
    // Kriter kartları artık ayrı bir ekranda değil, liste ekranındaki katlanabilir
    // #kritpanel içinde (kullanıcı isteğiyle taşındı); paneli açmadan içindeki
    // öğeler tıklanabilir olmuyor, count() ise gizliyken de çalışıyor.
    const wrCount = await page.locator('#rubric .wr').count();
    check('ağırlık gerekçesi her kartta var', wrCount === 8, `${wrCount} kart`);
    const bandToggles = await page.locator('#rubric .banddet').count();
    check('puan bandı paneli bantlı yedi kriterde var', bandToggles === 7, `${bandToggles} panel`);
    const kritPanelClosed = !(await page.locator('#kritpanel').isVisible());
    check('kriter paneli ilk ziyarette kapalı', kritPanelClosed);
    await page.click('#krittoggle');
    await page.waitForTimeout(150);
    const kritPanelOpen = await page.locator('#kritpanel.open').isVisible();
    check('kriter düğmesi paneli açıyor', kritPanelOpen);
    await page.locator('#rubric .banddet summary').first().click();
    await page.waitForTimeout(150);
    const bandRows = await page.locator('#rubric .banddet[open] .bandrow').count();
    check('puan bantları açılınca beş satır görünüyor', bandRows === 5, `${bandRows} satır`);
    const contribTexts = await page.locator('#rubric .contrib').allInnerTexts();
    const contribOk = contribTexts.length === 8 && contribTexts.every((t) => /taşıyor|katkısı yok/.test(t));
    check('ağırlık payı göstergesi sekiz kartta da doluyor', contribOk, contribTexts.join(' | '));

    const refs = await page.locator('#refs li').count();
    check('kaynak listesi dolu', refs > 40, `${refs} kaynak`);

    // Metodoloji ekranı: canlı istatistikler DB'den hesaplanıyor, elle yazılmıyor.
    await page.click('.nav a[data-route="metodoloji"]');
    await page.waitForTimeout(200);
    const methStats = await page.locator('#methStats .methstat').count();
    check('metodoloji istatistikleri doluyor', methStats === 5, `${methStats} kutu`);
    const methWidth = await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2);
    check('metodoloji ekranında yatay taşma yok', methWidth);
    // Y-06 ikinci katman: fiyat kriterine ayrı bir bölüm eklendi (kart 7).
    const methCards = await page.locator('.methgrid .methcard').count();
    check('metodoloji ekranında yedi kart var', methCards === 7, `${methCards} kart`);
    // Kaynak öner ekranı: araç ve kriter listeleri veriden doluyor.
    await page.click('.nav a[data-route="katki"]');
    await page.waitForTimeout(200);
    const ktCars = await page.locator('#ktCar option').count();
    // araç sayısı + "seçin" + "listede yok" = CAR_COUNT + 2
    check('form araç listesi veriden doluyor', ktCars === CAR_COUNT + 2, `${ktCars} seçenek (beklenen ${CAR_COUNT + 2})`);
    const ktCrits = await page.locator('#ktCriterion option').count();
    check('form kriter listesi veriden doluyor', ktCrits > 5, `${ktCrits} seçenek`);
    // Uç nokta tanımlı değilken gönderim kapalı olmalı; sessizce başarısız
    // olan bir form, hiç olmayan bir formdan daha kötüdür.
    const ktDisabled = await page.locator('#ktSubmit').isDisabled();
    const ktNoticeShown = await page.locator('#ktNotice.warn').isVisible();
    check('uç nokta yokken gönderim kapalı ve sebebi yazıyor', ktDisabled && ktNoticeShown);
    const ktWidth = await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2);
    check('kaynak öner ekranında yatay taşma yok', ktWidth);

    // İletişim ekranı: adres tanımlı değilken sessizce boş kalmamalı.
    await page.click('.nav a[data-route="iletisim"]');
    await page.waitForTimeout(200);
    const ilWarn = await page.locator('#ilNotice.warn').isVisible();
    check('iletişim ekranı adres tanımsızken uyarı gösteriyor', ilWarn);
    const ilWidth = await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2);
    check('iletişim ekranında yatay taşma yok', ilWidth);

    // "Bu araca kaynak öner" düğmesi: liste ekranında bir satır açılıp düğmeye
    // basılınca kaynak öner formuna geçilmeli ve araç kutusu önceden seçili gelmeli.
    await page.click('.nav a[data-route="liste"]');
    await page.waitForTimeout(150);
    await page.locator('#body tr.main .name').first().click();
    await page.waitForTimeout(150);
    const firstCarName = await page.locator('#body tr.main .nm').first().innerText();

    // Y-06 ikinci katman: açılan satırda "bu araç neden bu puanı aldı" dökümü —
    // sekiz kriterin puan/ağırlık/katkı satırı artı toplam satırı olmalı.
    const bdRows = await page.locator('tr.detail.open .bdtable tbody tr').count();
    check('araç detayında puan dökümü sekiz kriter + toplam satırı gösteriyor', bdRows === 9, `${bdRows} satır`);
    const evRows = await page.locator('tr.detail.open .evrow').count();
    check('araç detayında motor/trans kanıt metni görünüyor', evRows > 0, `${evRows} kanıt satırı`);

    await page.locator('.sugbtn').first().click();
    await page.waitForTimeout(200);
    const onKatkiScreen = await page.locator('[data-screen="katki"]').isVisible();
    const ktCarValue = await page.locator('#ktCar').inputValue();
    check(
      'bu araca kaynak öner düğmesi formu doldurup açıyor',
      onKatkiScreen && !!ktCarValue && firstCarName.includes(ktCarValue.split(' (')[0]),
      `ekran=${onKatkiScreen} seçili="${ktCarValue}"`
    );

    await page.click('.nav a[data-route="liste"]');
    await page.waitForTimeout(150);

    // Sıralama: ilk satır en yüksek toplam puana sahip olmalı.
    const totals = await page.$$eval('#body tr.main td.tot', (tds) =>
      tds.map((td) => parseFloat(td.textContent))
    );
    const sorted = totals.every((v, i) => i === 0 || totals[i - 1] >= v);
    check('varsayılan sıralama toplam puana göre azalan', sorted);

    // Filtre paneli (Y-05): tercihi saklanıyor ama kayıt yokken kapalı başlıyor,
    // çünkü ilk gelen kullanıcının önce tabloyu görmesi gerekiyor.
    const panelClosed = !(await page.locator('#filterpanel').isVisible());
    check('filtre paneli ilk ziyarette kapalı', panelClosed);
    if (!panelClosed) await dumpDebug('filtre-paneli-kapali-degil');
    await page.click('#filttoggle');
    await page.waitForTimeout(150);
    const panelOpen = await page.locator('#filterpanel.open').isVisible();
    check('filtre düğmesi paneli açıyor', panelOpen);
    if (!panelOpen) await dumpDebug('filtre-paneli-acilmadi');

    // Filtre: "Robot" şanzıman seçilince liste daralmalı.
    await page.getByRole('button', { name: 'Robot', exact: true }).click();
    await page.waitForTimeout(150);
    const filtered = await page.locator('#body tr.main').count();
    check('şanzıman filtresi daraltıyor', filtered > 0 && filtered < rows, `${filtered} satır`);
    if (!(filtered > 0 && filtered < rows)) await dumpDebug('filtre-daraltmadi');

    // Panel kapalıyken hangi filtrelerin açık olduğu görünmez olmasın diye
    // düğmenin üstündeki rozet seçili filtre sayısını sayıyor.
    const badge = await page.locator('#filtbadge').innerText();
    check('filtre rozeti seçili filtre sayısını gösteriyor', badge.trim() === '1', `rozet "${badge.trim()}"`);

    // Sayısal aralık filtresi: model yılı üst sınırı düşürülünce liste daralmalı,
    // rozet de aralığı bir filtre olarak saymalı.
    const yearMax = page.locator('.rnum[data-rk="year"][data-ri="1"]');
    await yearMax.fill('2010');
    await yearMax.dispatchEvent('change');
    await page.waitForTimeout(200);
    const yearFiltered = await page.locator('#body tr.main').count();
    const yearOk = yearFiltered > 0 && yearFiltered < rows;
    check('model yılı aralık filtresi daraltıyor', yearOk, `2010 ve öncesi → ${yearFiltered} satır`);
    if (!yearOk) await dumpDebug('yil-araligi-daraltmadi');
    const rangeBadge = await page.locator('#filtbadge').innerText();
    check('aralık filtresi rozete sayılıyor', rangeBadge.trim() !== '', `rozet "${rangeBadge.trim()}"`);
    const sliderCount = await page.locator('.rslider input[type=range]').count();
    check('üç aralık için altı kaydırıcı var', sliderCount === 6, `${sliderCount} kaydırıcı`);

    // Kaydırıcı gerçekten SÜRÜKLENEBİLİYOR mu. Bu kontrol, 2026-08-17'de
    // bulunan gerileme yüzünden var: `setRange()` her `input` olayında filtre
    // panelini yeniden kuruyor ve kullanıcının o an tuttuğu elemanı siliyordu,
    // bu yüzden değer ilk adımdan sonra donuyordu. Elemanın varlığını saymak
    // bunu yakalamıyor; sürükleyip değerin fareyi takip ettiğini görmek gerek.
    await page.click('#filtclear');
    await page.waitForTimeout(150);
    const yearSlider = page.locator('.rslider input[type=range]').first();
    const beforeDrag = await yearSlider.inputValue();
    const sbox = await page.locator('.rslider').first().boundingBox();
    await page.mouse.move(sbox.x + 4, sbox.y + sbox.height / 2);
    await page.mouse.down();
    await page.mouse.move(sbox.x + sbox.width * 0.6, sbox.y + sbox.height / 2, { steps: 12 });
    await page.mouse.up();
    await page.waitForTimeout(250);
    const afterDrag = await yearSlider.inputValue();
    // Rayın %60'ı boyunca çekilen sürükleme, aralığın en az beşte birini
    // katetmeli. Bozuk sürümde bu fark 1 birimde kalıyordu.
    const sMin = Number(await yearSlider.getAttribute('min'));
    const sMax = Number(await yearSlider.getAttribute('max'));
    const moved = Number(afterDrag) - Number(beforeDrag);
    const dragOk = moved >= (sMax - sMin) * 0.2;
    check('kaydırıcı sürüklendiğinde fareyi takip ediyor', dragOk,
      `${beforeDrag} → ${afterDrag} (${moved} birim)`);
    if (!dragOk) await dumpDebug('kaydirici-suruklenmiyor');
    // Sürükleme bir aralık filtresi bırakıyor; bunu bilerek temizlemiyoruz,
    // çünkü hemen aşağıdaki "filtreleri temizle" kontrolünün sıfırlayacak bir
    // şey bulması gerekiyor (düğme, aktif filtre yokken devre dışı kalıyor).

    // "Filtreleri temizle" bütün kategorileri birden sıfırlamalı.
    await page.click('#filtclear');
    await page.waitForTimeout(150);
    const cleared = await page.locator('#body tr.main').count();
    check('filtreleri temizle düğmesi listeyi geri getiriyor', cleared === rows, `${cleared} satır`);
    if (cleared !== rows) await dumpDebug('filtre-temizlenmedi');

    // Gövde filtresi: "Sedan" seçilince liste daralmalı. Bu filtre yalnızca
    // specs.body_type dolu olduğunda çalışır, o yüzden verinin de kontrolü sayılır.
    const bodyGroup = page.locator('.fgroup').filter({ hasText: 'Gövde' });
    await bodyGroup.getByRole('button', { name: 'Sedan', exact: true }).click();
    await page.waitForTimeout(150);
    const bodyFiltered = await page.locator('#body tr.main').count();
    const bodyOk = bodyFiltered > 0 && bodyFiltered < rows;
    check('gövde filtresi daraltıyor', bodyOk, `Sedan → ${bodyFiltered} satır`);
    if (!bodyOk) await dumpDebug('govde-filtresi-daraltmadi');
    await bodyGroup.getByRole('button', { name: 'Hepsi' }).click();
    await page.waitForTimeout(150);

    // Arama
    await page.fill('#search', 'volvo');
    await page.waitForTimeout(200);
    const searched = await page.locator('#body tr.main').count();
    check('arama çalışıyor', searched > 0 && searched < rows, `"volvo" → ${searched} satır`);
    // Katalog bloğu (MK-22): aramada puanlanmamış araçlar da bulunmalı, ama
    // puan tablosunun içine karışmamalı.
    const catBlockVisible = await page.locator('#catwrap .catitem').count();
    check('arama katalog araçlarını da buluyor', catBlockVisible > 0,
      `${catBlockVisible} katalog kartı`);
    const catLink = await page.locator('#catwrap .catname').first().getAttribute('href');
    check('katalog kartı statik sayfaya bağlanıyor',
      /^katalog\/.+\.html$/.test(catLink || ''), catLink);
    const catRowsInTable = await page.locator('#body tr.main').count();
    check('katalog araçları puan tablosuna karışmıyor', catRowsInTable === searched,
      `tabloda ${catRowsInTable} satır`);

    await page.click('#searchclr');
    await page.waitForTimeout(150);
    const catAfterClear = await page.locator('#catwrap .catitem').count();
    check('arama temizlenince katalog bloğu kapanıyor', catAfterClear === 0);

    // Kıyaslama. İki görünüm de her render()'da inşa edildiği için gizli
    // kalan kart görünümünde de aynı sınıfta düğmeler var (Y-25); testin
    // görünürdeki (tablo) düğmeye tıkladığından emin olmak için #body ile
    // sınırlandırılıyor.
    await page.locator('#body .cmpbtn').first().click();
    await page.waitForTimeout(200);
    const trayOk = await page.locator('#cmptray.show').isVisible();
    check('kıyaslama tepsisi açılıyor', trayOk);
    const cmpCardOk = (await page.locator('#cmpArea .cmpcard').count()) === 1;
    check('kıyaslama alanı doluyor', cmpCardOk);
    if (!trayOk || !cmpCardOk) await dumpDebug('kiyaslama-bozuk');

    // Zayıf halka işaretlemesi (liste ekranındayken bakılıyor)
    const weak = await page.locator('#body td.sc.weak').count();
    check('zayıf halka hücreleri işaretli', weak > 0, `${weak} hücre`);

    // Tepsideki düğme kıyaslama ekranına götürmeli.
    await page.click('#trayGo');
    await page.waitForTimeout(250);
    const onCmpScreen = await page.locator('[data-screen="kiyaslama"]').isVisible();
    check('tepsi düğmesi kıyaslama ekranına götürüyor', onCmpScreen);
    if (!onCmpScreen) await dumpDebug('tepsi-yonlendirmedi');

    // MK-07'nin asıl sözü: ekran değiştirmek sepeti sıfırlamamalı. Listeye
    // dönüp ikinci bir araç ekleniyor, sonra kıyaslamaya geri dönülüyor;
    // ilk araç hâlâ orada olmalı.
    await page.click('.nav a[data-route="liste"]');
    await page.waitForTimeout(200);
    await page.locator('#body .cmpbtn').nth(1).click();
    await page.waitForTimeout(200);
    await page.click('.nav a[data-route="kiyaslama"]');
    await page.waitForTimeout(250);
    const kept = await page.locator('#cmpArea .cmpcard').count();
    check('sepet ekran değişince korunuyor', kept === 2, `${kept} araç`);
    if (kept !== 2) await dumpDebug('sepet-sifirlandi');

    // Ağırlık değişimi toplam puanı değiştirmeli; kriter paneli artık liste
    // ekranının kendi içinde olduğu için ekran değiştirmeye gerek yok.
    await page.click('.nav a[data-route="liste"]');
    await page.waitForTimeout(200);
    const before = await page.locator('#body tr.main td.tot').first().innerText();
    await page.fill('#rubric input[data-wk="fun"]', '55');
    await page.waitForTimeout(250);
    const after = await page.locator('#body tr.main td.tot').first().innerText();
    check('ağırlık değişimi puanı etkiliyor', before !== after, `${before} → ${after}`);

    // --- Y-11: statik sayfalar (scripts/build_pages.py çıktısı) ---
    // Bu sayfaların işi arama motorunda görünmek, yani başlık, açıklama ve canonical
    // etiketlerinin gerçekten dolu olması işlevin kendisi; boş bir açıklama sayfayı
    // çalışmaz hale getirmez ama işe yaramaz hale getirir. Bu yüzden denetleniyorlar.
    const carPage = 'file://' + path.join(ROOT, 'arac', 'vw-passat-b7-1-6-tdi.html');
    await page.goto(carPage);
    const spTitle = await page.title();
    check('araç sayfası araca özgü başlık taşıyor',
      spTitle.includes('Passat B7') && spTitle.includes('alınır mı'), spTitle);
    const spDesc = await page.locator('meta[name="description"]').getAttribute('content');
    check('araç sayfasında meta açıklama dolu', !!spDesc && spDesc.length > 60,
      `${(spDesc || '').length} karakter`);
    const spCanon = await page.locator('link[rel="canonical"]').getAttribute('href');
    check('araç sayfasında canonical adres var', !!spCanon && spCanon.endsWith('.html'), spCanon);
    const spH1 = await page.locator('h1').count();
    check('araç sayfasında tek h1 var', spH1 === 1, `${spH1} adet`);
    const spWide = await page.evaluate(
      () => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2);
    check('araç sayfasında yatay taşma yok', spWide);
    const spLd = await page.locator('script[type="application/ld+json"]').count();
    check('araç sayfasında yapılandırılmış veri var', spLd === 1, `${spLd} blok`);
    const spEv = await page.locator('.ev').count();
    check('araç sayfası puan gerekçelerini gösteriyor', spEv >= 2, `${spEv} gerekçe bloğu`);

    const engPage = 'file://' + path.join(ROOT, 'motor', 'vag-ea189.html');
    await page.goto(engPage);
    const engIssues = await page.locator('.issue').count();
    check('motor sayfası bilinen arızaları listeliyor', engIssues >= 1, `${engIssues} arıza`);

    // --- Katalog sayfaları (MK-22) ---
    // Bu sayfaların tek kritik şartı, puanı olmayan bir aracı puanı varmış gibi
    // göstermemeleri. Kontroller tam olarak onu bekliyor: puan tablosu olmayacak,
    // "henüz puanlanmadı" ifadesi görünecek.
    const catDir = path.join(ROOT, 'katalog');
    const catFiles = fs.existsSync(catDir)
      ? fs.readdirSync(catDir).filter((f) => f.endsWith('.html'))
      : [];
    check('katalog sayfaları üretildi', catFiles.length > 500, `${catFiles.length} sayfa`);

    const catPage = 'file://' + path.join(catDir, catFiles[0]);
    await page.goto(catPage);
    const catTitle = await page.title();
    check('katalog sayfası puanlanmadığını başlıkta söylüyor',
      /puanlanmad/i.test(catTitle), catTitle);
    const catH1 = await page.locator('h1').count();
    check('katalog sayfasında tek h1 var', catH1 === 1, `${catH1} adet`);
    const catScores = await page.locator('.scores, .score-row').count();
    check('katalog sayfasında puan tablosu YOK', catScores === 0, `${catScores} puan tablosu`);
    const catSpecs = await page.locator('table.kv tr').count();
    check('katalog sayfası teknik künyeyi listeliyor', catSpecs >= 5, `${catSpecs} satır`);
    const catLd = await page.locator('script[type="application/ld+json"]').count();
    check('katalog sayfasında yapılandırılmış veri var', catLd === 1, `${catLd} blok`);
    const catOverflow = await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth + 1);
    check('katalog sayfasında yatay taşma yok', catOverflow);

    // Dar ekranda menü artık bir açılır panele dönüşüyor (Y-25). Önceki
    // sürümde .nav tam genişlikte açık duruyordu, ekranın ~%32'sini kaplıyor
    // ve yarı saydam olduğu için altındaki içeriği okunaksız hale getiriyordu.
    // Bu kontrol, viewport'u geçici olarak daraltıp geri büyüterek çalışır;
    // sonraki hiçbir kontrolün göremeyeceği bir yan etki bırakmaz.
    await page.goto(FILE);
    await page.setViewportSize({ width: 390, height: 844 });
    await page.waitForTimeout(150);
    const toggleVisible = await page.locator('#navToggle').isVisible();
    const panelHiddenAtStart = !(await page.locator('#navPanel').evaluate((el) => el.classList.contains('open')));
    check('dar ekranda menü düğmesi görünür ve panel kapalı başlıyor',
      toggleVisible && panelHiddenAtStart);
    const navHeightBefore = await page.locator('.topbar').evaluate((el) => el.getBoundingClientRect().height);
    check('dar ekranda kapalı menü üstbaşlığı 70px altında kalıyor',
      navHeightBefore < 70, `${navHeightBefore.toFixed(0)}px`);
    await page.click('#navToggle');
    await page.waitForTimeout(200);
    const panelOpenNow = await page.locator('#navPanel').evaluate((el) => el.classList.contains('open'));
    check('menü düğmesi panele açıyor', panelOpenNow);
    await page.click('#navPanel a[data-route="liste"]');
    await page.waitForTimeout(250);
    const panelClosedAfterNav = !(await page.locator('#navPanel').evaluate((el) => el.classList.contains('open')));
    const routedToListe = (await page.evaluate(() => location.hash)) === '#liste';
    check('bir bağlantıya tıklayınca menü kapanıp doğru ekrana gidiyor',
      panelClosedAfterNav && routedToListe);

    // Kart görünümü denetimin asıl hedefiydi (Y-25): dar ekranda yatayda
    // kaymadan, tek sütun halinde okunabilir olmalı. Görünüm tercihi önceki
    // adımlarda 'tablo' olarak kalmıştı; burada kasıtlı olarak karta dönülüyor.
    // Adres zaten #liste'de duruyor; goto() aynı URL'ye gidince tarayıcı
    // bunu belge içi bir gezinme sayıp sayfayı yeniden yüklemeyebilir, bu
    // yüzden reload() kullanılıyor.
    await page.evaluate(() => localStorage.setItem('arac_puan_gorunum', 'kart'));
    await page.reload();
    await page.waitForSelector('#cardgrid .vcard');
    const listeOverflow = await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth + 1);
    check('dar ekranda kart görünümünde yatay taşma yok', listeOverflow);

    await page.setViewportSize({ width: 1280, height: 800 });
    await page.waitForTimeout(150);

    if (ALWAYS_SCREENSHOT) await dumpDebug('02-tum-kontroller-sonrasi');
  } catch (e) {
    // Beklenmedik bir hata (ör. bir seçici hiç bulunamadı) çıplak bir stack
    // trace bırakmasın; en azından o anın ekran görüntüsü ve konsolu elde kalsın.
    console.log(`\nBEKLENMEDİK HATA: ${e}`);
    await dumpDebug('beklenmedik-hata');
    await browser.close();
    process.exit(1);
  }

  const failed = checks.filter((c) => !c.ok);
  if (failed.length) {
    await dumpDebug('basarisiz-kontroller');
  }
  await browser.close();

  console.log(`\n${checks.length - failed.length}/${checks.length} kontrol geçti.`);
  if (failed.length) {
    console.log(`Konsolun tamamı (${consoleLog.length} kayıt) ve ekran görüntüsü ${path.relative(ROOT, DEBUG_DIR)}/ altında.`);
  }
  process.exit(failed.length ? 1 : 0);
})();
