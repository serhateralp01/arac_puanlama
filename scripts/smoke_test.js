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
const FILE = 'file://' + path.join(ROOT, 'arac-puanlama.html');
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
    await page.goto(FILE);
    await page.waitForSelector('#body tr.main');
    if (ALWAYS_SCREENSHOT) await dumpDebug('01-yuklendi');

    const rows = await page.locator('#body tr.main').count();
    check('bütün araçlar listeleniyor', rows === 154, `${rows} satır`);

    check('JS hatası yok', errors.length === 0, errors.slice(0, 3).join(' | '));

    const crit = await page.locator('#rubric .card').count();
    check('sekiz kriter kartı var', crit === 8, `${crit} kart`);

    const sumText = await page.locator('#sumbox').innerText();
    check('ağırlık toplamı 100', sumText.includes('100'), sumText.replace(/\n/g, ' '));

    const refs = await page.locator('#refs li').count();
    check('kaynak listesi dolu', refs > 40, `${refs} kaynak`);

    // Sıralama: ilk satır en yüksek toplam puana sahip olmalı.
    const totals = await page.$$eval('#body tr.main td.tot', (tds) =>
      tds.map((td) => parseFloat(td.textContent))
    );
    const sorted = totals.every((v, i) => i === 0 || totals[i - 1] >= v);
    check('varsayılan sıralama toplam puana göre azalan', sorted);

    // Filtre: "Robot" şanzıman seçilince liste daralmalı.
    await page.getByRole('button', { name: 'Robot', exact: true }).click();
    await page.waitForTimeout(150);
    const filtered = await page.locator('#body tr.main').count();
    check('şanzıman filtresi daraltıyor', filtered > 0 && filtered < rows, `${filtered} satır`);
    if (!(filtered > 0 && filtered < rows)) await dumpDebug('filtre-daraltmadi');
    await page.locator('.fgroup').first().getByRole('button', { name: 'Hepsi' }).click();
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

    // Ağırlık değişimi toplam puanı değiştirmeli.
    const before = await page.locator('#body tr.main td.tot').first().innerText();
    await page.fill('#rubric input[data-wk="fun"]', '55');
    await page.waitForTimeout(250);
    const after = await page.locator('#body tr.main td.tot').first().innerText();
    check('ağırlık değişimi puanı etkiliyor', before !== after, `${before} → ${after}`);

    // Zayıf halka işaretlemesi
    const weak = await page.locator('#body td.sc.weak').count();
    check('zayıf halka hücreleri işaretli', weak > 0, `${weak} hücre`);

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
