/*
 * import_legacy.js — tek seferlik göç betiği.
 *
 * legacy/arac-puanlama-v1.html içindeki gömülü `CARS` ve `R` yapılarını okuyup
 * data/ altındaki dosya-başına-araç JSON yapısına çevirir. Bir kez çalıştırıldı,
 * kaydı ve tekrarlanabilirliği için repoda duruyor.
 *
 * Kullanım: node scripts/import_legacy.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const LEGACY = path.join(ROOT, 'legacy', 'arac-puanlama-v1.html');
const DATA = path.join(ROOT, 'data');

const html = fs.readFileSync(LEGACY, 'utf8');

// Betiğin sadece veri kısmını (R + CARS) izole edip değerlendiriyoruz; DOM'a
// dokunan kod çalıştırılmıyor.
const script = html.match(/<script>([\s\S]*)<\/script>/)[1];
const dataPart = script.slice(0, script.indexOf('const ORDER='));
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(dataPart + '\nthis.R=R; this.CARS=CARS;', sandbox);
const { R, CARS } = sandbox;

const SCORED = ['motor', 'trans', 'fun', 'comf', 'age', 'cost', 'liq'];

const TR_MAP = { ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u', İ: 'i', I: 'i' };
function slug(s) {
  return s
    .replace(/[çğıöşüİI]/g, (ch) => TR_MAP[ch])
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

// Kaynak tipi, alan adından türetiliyor. Amaç kesin sınıflandırma değil,
// Faz 2'deki güven-seviyesi çalışmasına başlangıç noktası vermek.
const TYPE_BY_DOMAIN = [
  [/sikayetvar\.com/, 'complaint-aggregator'],
  [/kronikyorum|kroniksorunlar|otosorular/, 'complaint-aggregator'],
  [/wikipedia\.org|namu\.wiki/, 'encyclopedia'],
  [/eksisozluk\.com/, 'crowd-wiki'],
  [/truedelta\.com/, 'owner-survey'],
  [/tuev-nord-group\.com/, 'official-inspection-data'],
  [/auto-data\.net/, 'spec-database'],
  [/forum|forums|club|technopat|otopark|donanimhaber|bimmerfest|pistonheads|honda-tech|redriven/, 'forum'],
  [/andcetin\.com/, 'independent-analyst'],
  [/autoexpress|bmwblog|motor1|carchecker|clickmechanic|enginefinder|cars-expert|euroracingparts/, 'trade-press'],
  [/erenservis|hech\.com\.tr|goksenoto|araclo|insigniateam|apexxengines|orbimotors|autodoc|mtautoparts|stargaragemansfield|thecarlane|technicalparameters/, 'trade-blog'],
];
function sourceType(url) {
  for (const [re, t] of TYPE_BY_DOMAIN) if (re.test(url)) return t;
  return 'unknown';
}

const VERIF = { true: 'verified', p: 'partial', false: 'preliminary' };

// ---- sources.json ----
const sources = {};
for (const [key, [claim, publisher, url]] of Object.entries(R)) {
  sources[key] = {
    id: key,
    claim,
    publisher,
    url,
    type: sourceType(url),
    // Faz 2'de doldurulacak alanlar. null = "henüz değerlendirilmedi",
    // boş dizi = "henüz alıntı çıkarılmadı".
    tier: null,
    accessed: null,
    language: null,
    quotes: [],
  };
}

// ---- cars/*.json ----
const anomalies = [];
const usedIds = new Map();
const cars = CARS.map((c, i) => {
  let id = slug(c.n);
  if (usedIds.has(id)) {
    const n = usedIds.get(id) + 1;
    usedIds.set(id, n);
    id = `${id}-${n}`;
  } else usedIds.set(id, 1);

  if (c.s.length !== SCORED.length) {
    anomalies.push({
      car: c.n,
      issue: `s dizisi ${c.s.length} elemanlı, ${SCORED.length} olmalı`,
      dropped: c.s.slice(SCORED.length),
    });
  }
  if (!Array.isArray(c.r)) anomalies.push({ car: c.n, issue: 'r alanı dizi değil' });

  const scores = {};
  SCORED.forEach((k, j) => (scores[k] = c.s[j]));

  return {
    id,
    legacy_index: i,
    name: c.n,
    tag: c.tag,
    brand_group: c.g,
    years: c.y,
    specs: {
      hp: c.hp,
      displacement_l: c.disp,
      fuel: c.fuel,
      drivetrain: c.drv,
      transmission_type: c.tx,
    },
    price_band_k_try: c.p,
    verification: VERIF[String(c.v)],
    scores,
    sources: c.r || [],
    note: c.note,
    provenance: {
      imported_from: 'legacy/arac-puanlama-v1.html',
      imported_at: '2026-08-04',
      method: 'scripts/import_legacy.js',
    },
  };
});

fs.mkdirSync(path.join(DATA, 'cars'), { recursive: true });
for (const car of cars) {
  fs.writeFileSync(
    path.join(DATA, 'cars', `${car.id}.json`),
    JSON.stringify(car, null, 2) + '\n'
  );
}
fs.writeFileSync(
  path.join(DATA, 'sources.json'),
  JSON.stringify(sources, null, 2) + '\n'
);

console.log(`${cars.length} araç, ${Object.keys(sources).length} kaynak yazıldı.`);
if (anomalies.length) {
  console.log('\nVeri anomalileri (docs/DATA-ISSUES.md içine alın):');
  for (const a of anomalies) console.log(' -', a.car, '→', a.issue, a.dropped ? `(atılan: ${a.dropped})` : '');
}
