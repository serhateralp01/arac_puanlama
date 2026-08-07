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

    // Hazır giriş yollarından biri: tıklanınca ilgili ağırlık seti uygulanıp
    // listeye götürmeli.
    await page.locator('.anapathbtn').first().click();
    await page.waitForTimeout(200);
    const onListeAfterPath = await page.locator('[data-screen="liste"]').isVisible();
    check('hazır giriş yolu listeye götürüyor', onListeAfterPath);

    // Onboarding artık görüldü sayıldığı için hash'siz bir sonraki ziyaret de
    // doğrudan ana ekrana düşmeli, tekrar giriş akışına değil.
    await page.goto(FILE);
    await page.waitForTimeout(200);
    const directToAna = await page.locator('[data-screen="ana"]').isVisible();
    check('tekrar ziyarette hash yokken doğrudan ana ekrana gidiliyor', directToAna);

    // Bundan sonrası liste ekranında geçiyor.
    await page.goto(FILE + '#liste');
    await page.waitForSelector('#body tr.main');
    if (ALWAYS_SCREENSHOT) await dumpDebug('01-yuklendi');

    const rows = await page.locator('#body tr.main').count();
    check('bütün araçlar listeleniyor', rows === 221, `${rows} satır`);

    check('JS hatası yok', errors.length === 0, errors.slice(0, 3).join(' | '));

    const crit = await page.locator('#rubric .card').count();
    check('sekiz kriter kartı var', crit === 8, `${crit} kart`);

    const sumText = await page.locator('#sumbox').innerText();
    check('ağırlık toplamı 100', sumText.includes('100'), sumText.replace(/\n/g, ' '));

    // Y-06 ikinci katman: her kritere ağırlık gerekçesi, bantlı yedi kriterin
    // hepsine puan bandı açılır paneli ve canlı katkı göstergesi eklendi.
    const wrCount = await page.locator('#rubric .wr').count();
    check('ağırlık gerekçesi her kartta var', wrCount === 8, `${wrCount} kart`);
    const bandToggles = await page.locator('#rubric .banddet').count();
    check('puan bandı paneli bantlı yedi kriterde var', bandToggles === 7, `${bandToggles} panel`);
    // Panel #liste'de gizli olduğu için tıklanabilir olması önce kriterler
    // ekranına geçmeyi gerektiriyor; count() gizliyken de çalışır ama click() çalışmaz.
    await page.click('.nav a[data-route="kriterler"]');
    await page.waitForTimeout(150);
    await page.locator('#rubric .banddet summary').first().click();
    await page.waitForTimeout(150);
    const bandRows = await page.locator('#rubric .banddet[open] .bandrow').count();
    check('puan bantları açılınca beş satır görünüyor', bandRows === 5, `${bandRows} satır`);
    const contribTexts = await page.locator('#rubric .contrib').allInnerTexts();
    const contribOk = contribTexts.length === 8 && contribTexts.every((t) => /fiili katkı|katkısı yok/.test(t));
    check('canlı katkı göstergesi sekiz kartta da doluyor', contribOk, contribTexts.join(' | '));

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
    // 221 araç + "seçin" + "listede yok" = 223
    check('form araç listesi veriden doluyor', ktCars === 223, `${ktCars} seçenek`);
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
    await page.click('#searchclr');
    await page.waitForTimeout(150);

    // Kıyaslama
    await page.locator('.cmpbtn').first().click();
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
    await page.locator('.cmpbtn').nth(1).click();
    await page.waitForTimeout(200);
    await page.click('.nav a[data-route="kiyaslama"]');
    await page.waitForTimeout(250);
    const kept = await page.locator('#cmpArea .cmpcard').count();
    check('sepet ekran değişince korunuyor', kept === 2, `${kept} araç`);
    if (kept !== 2) await dumpDebug('sepet-sifirlandi');

    // Ağırlık değişimi toplam puanı değiştirmeli (kriterler ekranında).
    await page.click('.nav a[data-route="liste"]');
    await page.waitForTimeout(200);
    const before = await page.locator('#body tr.main td.tot').first().innerText();
    await page.click('.nav a[data-route="kriterler"]');
    await page.waitForTimeout(200);
    await page.fill('#rubric input[data-wk="fun"]', '55');
    await page.waitForTimeout(250);
    await page.click('.nav a[data-route="liste"]');
    await page.waitForTimeout(200);
    const after = await page.locator('#body tr.main td.tot').first().innerText();
    check('ağırlık değişimi puanı etkiliyor', before !== after, `${before} → ${after}`);

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
