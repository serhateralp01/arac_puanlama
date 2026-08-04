/*
 * smoke_test.js — üretilmiş HTML gerçekten çalışıyor mu?
 *
 * Şema doğrulaması (scripts/validate.py) verinin tutarlı olduğunu söyler ama
 * sayfanın açıldığını söylemez. Bu betik dosyayı gerçek bir tarayıcıda açıp
 * tablonun dolduğunu, konsola hata düşmediğini ve etkileşimin (filtre,
 * kıyaslama, ağırlık) çalıştığını doğrular.
 *
 * Kullanım: node scripts/smoke_test.js
 */
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = 'file://' + path.join(ROOT, 'arac-puanlama.html');

const checks = [];
function check(name, ok, detail = '') {
  checks.push({ name, ok, detail });
  console.log(`${ok ? 'OK  ' : 'HATA'} ${name}${detail ? ' — ' + detail : ''}`);
}

(async () => {
  // Yerelde önceden kurulu bir Chromium varsa onu kullan; yoksa Playwright'ın
  // kendi indirdiği tarayıcıya düş (CI böyle çalışıyor).
  const launchOpts = process.env.CHROMIUM_PATH
    ? { executablePath: process.env.CHROMIUM_PATH }
    : {};
  const browser = await chromium.launch(launchOpts);
  const page = await browser.newPage();
  const errors = [];
  // Google Fonts çevrimdışı ortamda yüklenemiyor; sayfa sistem fontuna düşüyor
  // ve bu beklenen davranış, JS hatası değil.
  const isNetworkNoise = (t) => /ERR_|Failed to load resource/.test(t);
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => {
    if (m.type() === 'error' && !isNetworkNoise(m.text())) errors.push(m.text());
  });

  await page.goto(FILE);
  await page.waitForSelector('#body tr.main');

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
  check('kıyaslama tepsisi açılıyor', await page.locator('#cmptray.show').isVisible());
  check('kıyaslama alanı doluyor', (await page.locator('#cmpArea .cmpcard').count()) === 1);

  // Ağırlık değişimi toplam puanı değiştirmeli.
  const before = await page.locator('#body tr.main td.tot').first().innerText();
  await page.fill('#rubric input[data-wk="fun"]', '55');
  await page.waitForTimeout(250);
  const after = await page.locator('#body tr.main td.tot').first().innerText();
  check('ağırlık değişimi puanı etkiliyor', before !== after, `${before} → ${after}`);

  // Zayıf halka işaretlemesi
  const weak = await page.locator('#body td.sc.weak').count();
  check('zayıf halka hücreleri işaretli', weak > 0, `${weak} hücre`);

  await browser.close();

  const failed = checks.filter((c) => !c.ok);
  console.log(`\n${checks.length - failed.length}/${checks.length} kontrol geçti.`);
  process.exit(failed.length ? 1 : 0);
})();
