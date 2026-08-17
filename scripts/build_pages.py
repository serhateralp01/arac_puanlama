#!/usr/bin/env python3
"""build_pages.py — data/ → araç, motor ve şanzıman başına statik sayfa.

**Neden var.** `scripts/build.py` tek bir `index.html` üretiyor ve ekranlar arası
geçiş `#liste` gibi çapa (hash) adlarıyla yapılıyor. Uygulama davranışı açısından bu
tasarım doğru ve MK-07'de bilinçli olarak seçildi. Ama arama motoru açısından sonucu
şudur: depodaki seksen bin kelimelik özgün, kaynaklı Türkçe analiz **tek bir sayfa**
olarak görünüyor. "Passat B7 kronik sorunları" arayan biri bu içeriği hiçbir zaman
bulamıyor.

Bu betik o boşluğu kapatıyor: her araç, her motor ailesi ve her şanzıman kutusu için
kendi adresi, kendi başlığı ve kendi açıklaması olan bir sayfa üretiyor. Sayfalar
depodaki gerçek gerekçe metinlerini taşıyor — arama motoru için üretilmiş içi boş
kapı sayfaları değil, zaten yazılmış olan analizin görünür hali.

**MK-01 bozulmuyor.** Üretilen sayfalar türetilmiş çıktıdır ve `data/` tek doğruluk
kaynağı olarak kalır; dosyalar her çalıştırmada sıfırdan yeniden üretilir. MK-02 bu
genişlemeyi zaten öngörüyordu: "derleme adımında yeni bir çıktı biçimi üretmek".

**Neden build.py'nin içinde değil.** Ayrı bir betik, çalışan `index.html` üretimini
hiç riske atmıyor. CLAUDE.md §2'nin kuralı bu: bitmemiş karmaşıklık için çalışan ürün
riske atılmaz. İki betik aynı veriyi okuyor, farklı çıktı biçimleri üretiyor.

Kullanım:
    python3 scripts/build_pages.py            # üret
    python3 scripts/build_pages.py --check    # üretilmiş sayfalar güncel mi
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Yayın adresi. GitHub Pages varsayılanı kullanılıyor; özel alan adı bağlanırsa
# yalnızca bu sabit değişir ve bütün canonical/sitemap adresleri onu izler.
BASE_URL = "https://serhateralp01.github.io/arac_puanlama"

CAR_DIR = ROOT / "arac"
ENGINE_DIR = ROOT / "motor"
TRANS_DIR = ROOT / "sanziman"
CATALOG_DIR = ROOT / "katalog"
SITEMAP = ROOT / "sitemap.xml"
ROBOTS = ROOT / "robots.txt"

# Kriter anahtarı → sayfada görünecek başlık. data/criteria.json'dan da okunabilirdi
# ama burada yalnızca kısa etiket gerekiyor ve bağımlılığı azaltmak sayfayı sadeleştiriyor.
CRIT_TITLES = {
    "motor": "Motor", "trans": "Şanzıman", "fun": "Sürüş keyfi", "comf": "Konfor",
    "age": "Yaş riski", "cost": "Sahip olma maliyeti", "liq": "Bulunabilirlik",
}

PAGE_CSS = """
:root{--pg:#F7F6F3;--sf:#fff;--ink:#1A1D1B;--ink2:#4C524E;--ink3:#787E7A;
--rule:#E2E1DA;--acc:#9A5B12;--ok:#1F5F5B;--bad:#9E4227}
@media(prefers-color-scheme:dark){:root{--pg:#13181A;--sf:#191F21;--ink:#E9EAE6;
--ink2:#A9AFAA;--ink3:#7C837E;--rule:#28312F;--acc:#DFA25C;--ok:#63B5AC;--bad:#E08267}}
*{box-sizing:border-box}
body{margin:0;background:var(--pg);color:var(--ink);line-height:1.6;
font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
.w{max-width:760px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--rule);background:var(--sf);padding:14px 0}
header a.home{color:var(--ink3);text-decoration:none;font-size:13px;letter-spacing:.02em}
header a.home:hover{color:var(--acc)}
h1{font-size:clamp(25px,4.6vw,36px);line-height:1.15;letter-spacing:-.02em;margin:26px 0 6px}
.sub{color:var(--ink2);font-size:16px;margin:0 0 20px}
h2{font-size:19px;margin:30px 0 10px;letter-spacing:-.01em;border-top:1px solid var(--rule);padding-top:20px}
p{margin:0 0 13px}
.badge{display:inline-block;font-size:11.5px;font-weight:650;letter-spacing:.06em;
text-transform:uppercase;padding:3px 8px;border-radius:3px;border:1px solid currentColor;margin-right:6px}
.b-ok{color:var(--ok)} .b-mid{color:var(--acc)} .b-low{color:var(--ink3)}
table{border-collapse:collapse;width:100%;font-size:14.5px;margin:0 0 14px}
th{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;
color:var(--ink3);padding:9px 10px;border-bottom:1px solid var(--rule)}
td{padding:9px 10px;border-bottom:1px solid var(--rule);color:var(--ink2);vertical-align:top}
td.k{color:var(--ink);font-weight:600;white-space:nowrap}
td.n{text-align:right;font-variant-numeric:tabular-nums;font-family:ui-monospace,Menlo,monospace;color:var(--ink)}
.tw{overflow-x:auto}
.ev{background:var(--sf);border:1px solid var(--rule);border-left:3px solid var(--acc);
padding:14px 16px;border-radius:0 4px 4px 0;margin:0 0 12px;font-size:14.5px;color:var(--ink2)}
.ev b{color:var(--ink);display:block;margin-bottom:5px;font-size:13px;letter-spacing:.02em}
.issue{background:var(--sf);border:1px solid var(--rule);padding:13px 15px;border-radius:4px;
margin:0 0 10px;font-size:14.5px}
.issue .m{color:var(--ink3);font-size:12.5px;margin-top:6px;font-family:ui-monospace,Menlo,monospace}
ul{padding-left:20px;margin:0 0 14px}li{margin-bottom:6px;color:var(--ink2);font-size:14.5px}
a{color:var(--ok)}
.rel{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}
.rel a{display:inline-block;padding:5px 11px;border:1px solid var(--rule);border-radius:3px;
background:var(--sf);text-decoration:none;font-size:13.5px;color:var(--ink2)}
.rel a:hover{border-color:var(--acc);color:var(--acc)}
footer{border-top:1px solid var(--rule);margin-top:36px;padding:22px 0 40px;
color:var(--ink3);font-size:13px}
.warn{color:var(--ink3);font-size:13px;font-style:italic}
code{font-family:ui-monospace,Menlo,monospace;font-size:.88em;background:var(--pg);padding:1px 4px;border-radius:3px}
"""


def e(text) -> str:
    """HTML kaçışı. None güvenli, çünkü şemada isteğe bağlı alanlar var."""
    return html.escape(str(text), quote=True) if text is not None else ""


def rich(text) -> str:
    """Kaçışlanmış metinde `**kalın**` ve `` `kod` `` işaretlerini biçime çevirir.

    Depodaki `note` ve `reasoning` alanları düz metin değil, hafif Markdown kullanıyor
    (ör. "**Düzeltme kaydı:**"). Bu işaretler ham yıldız olarak basılırsa sayfa özensiz
    görünüyor. Dönüşüm kaçışlamadan SONRA yapılıyor: önce bütün metin güvenli hale
    getiriliyor, sonra yalnızca bu iki kalıp etikete çevriliyor. Sıra tersine dönerse
    veri dosyasındaki bir metin sayfaya HTML enjekte edebilirdi.
    """
    if text is None:
        return ""
    out = e(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out, flags=re.S)
    out = re.sub(r"`([^`]+?)`", r"<code>\1</code>", out)
    return out


def load():
    criteria = json.loads((DATA / "criteria.json").read_text(encoding="utf-8"))
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    engines = {k: v for k, v in json.loads((DATA / "engines.json").read_text(encoding="utf-8")).items()
               if not k.startswith("_")}
    trans = {k: v for k, v in json.loads((DATA / "transmissions.json").read_text(encoding="utf-8")).items()
             if not k.startswith("_")}
    cars = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((DATA / "cars").glob("*.json"))]
    return criteria, cars, sources, engines, trans


def load_catalog() -> tuple[list[dict], dict]:
    """Olgusal katalog kayıtları ve katalog kaynak sicili (MK-22).

    Sayfa yalnızca **yalnız katalogda olan** kayıtlar için üretilir: puanlanmış bir
    araca bağlı olanların kendi sayfası zaten var, belirsiz eşleşenler ise bir
    puanlanmış aracın yakın kopyası olabilir. İkisini de basmak, arama motoruna aynı
    içeriği iki adresten sunmak olurdu.
    """
    cat_dir = DATA / "catalog"
    if not cat_dir.exists():
        return [], {}
    entries = []
    for path in sorted(cat_dir.glob("*.json")):
        if path.name == "_sources.json":
            continue
        entries.extend(json.loads(path.read_text(encoding="utf-8")).get("entries", []))
    entries = [x for x in entries
               if not x.get("scored_car_id") and not x.get("possible_scored_car_ids")]
    src_path = cat_dir / "_sources.json"
    srcs = json.loads(src_path.read_text(encoding="utf-8")).get("sources", {}) if src_path.exists() else {}
    return entries, srcs


def shell(*, title, description, canonical, body, jsonld=None) -> str:
    """Ortak sayfa iskeleti.

    Başlık ve açıklama her sayfada farklı; ikisi de aramada görünen metin olduğu
    için sayfaya özgü olmaları şart. Aynı başlığı taşıyan yüzlerce sayfa, arama
    motoru tarafından tek bir sayfanın kopyası gibi değerlendiriliyor.
    """
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:locale" content="tr_TR">
<meta name="twitter:card" content="summary">
<style>{PAGE_CSS}</style>
{ld}
</head>
<body>
<header><div class="w"><a class="home" href="{BASE_URL}/">← Araç Puanlama</a></div></header>
<main class="w">
{body}
</main>
<footer><div class="w">
<p>Bu sayfa <a href="{BASE_URL}/">Araç Puanlama</a> veri deposundan otomatik üretildi.
Puanlar resmî bir kalite ya da arıza istatistiği değildir; açıklanan kriterlerin, kaynak
kapsamının ve analist değerlendirmesinin birleşimidir. Yöntem
<a href="{BASE_URL}/#metodoloji">metodoloji sayfasında</a> açık yazılıdır.</p>
<p>Bu içerik ekspertiz, servis teşhisi veya piyasa değeri garantisi değildir. Araç almadan
önce şasi numarası, servis geçmişi ve bağımsız ekspertizle ayrıca doğrulama yapılmalıdır.</p>
</div></footer>
</body>
</html>
"""


def scores_table(car, criteria) -> str:
    rows = []
    for k in criteria["full_order"]:
        if k == "price":
            continue
        v = car["scores"].get(k)
        if v is None:
            continue
        rows.append(f'<tr><td class="k">{e(CRIT_TITLES.get(k, k))}</td><td class="n">{v}</td></tr>')
    return f'<div class="tw"><table><thead><tr><th>Kriter</th><th style="text-align:right">Puan</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def issues_html(component) -> str:
    out = []
    for iss in component.get("known_issues", []):
        meta = []
        if iss.get("onset_km"):
            meta.append(f"~{iss['onset_km']:,} km'den sonra".replace(",", "."))
        if iss.get("frequency"):
            meta.append(f"sıklık: {iss['frequency']}")
        if iss.get("severity"):
            meta.append(f"ağırlık: {iss['severity']}")
        m = f'<div class="m">{e(" · ".join(meta))}</div>' if meta else ""
        out.append(f'<div class="issue">{e(iss["issue"])}{m}</div>')
    return "".join(out)


def sources_html(ids, sources) -> str:
    items = []
    for sid in ids:
        src = sources.get(sid)
        if not src:
            continue
        items.append(f'<li><a href="{e(src["url"])}" rel="nofollow noopener" target="_blank">'
                     f'{e(src["publisher"])}</a> — {e(src["claim"])}</li>')
    return f"<ul>{''.join(items)}</ul>" if items else ""


def verification_badge(car) -> str:
    v = car["verification"]
    n = len(car["sources"])
    if v == "verified":
        return f'<span class="badge b-ok">doğrulanmış · {n} kaynak</span>'
    if v == "partial":
        return f'<span class="badge b-mid">kısmi kaynak · {n} kaynak</span>'
    return '<span class="badge b-low">ön değerlendirme</span>'


def car_page(car, criteria, sources, engines, trans) -> tuple[str, str]:
    s = car["specs"]
    eng = engines.get(s.get("engine_id"))
    box = trans.get(s.get("transmission_id"))
    name = car["name"]

    # Başlık, Türkiye'de gerçekten aranan kalıbı hedefliyor: "<model> alınır mı".
    title = f"{name} alınır mı? Kronik sorunları, puanı ve fiyatı"
    weak = [CRIT_TITLES[k] for k in ("motor", "trans")
            if car["scores"].get(k) is not None and car["scores"][k] < 50]
    weak_txt = f" En zayıf tarafı: {', '.join(weak).lower()}." if weak else ""
    desc = (f"{name} ({car['years']}, {s['hp']} bg, {s['transmission_type']}) için "
            f"kaynaklı güvenilirlik değerlendirmesi.{weak_txt} "
            f"{len(car['sources'])} bağımsız kaynağa dayanıyor.")

    parts = [f"<h1>{e(name)}</h1>",
             f'<p class="sub">{e(car["tag"])} · {e(car["years"])} · {verification_badge(car)}</p>']

    parts.append("<h2>Özet</h2>")
    spec_rows = [
        ("Motor gücü", f"{s['hp']} bg"),
        ("Motor hacmi", f"{s['displacement_l']} L"),
        ("Yakıt", s["fuel"]),
        ("Şanzıman", s["transmission_type"]),
        ("Çekiş", s["drivetrain"]),
    ]
    if s.get("torque_nm"):
        spec_rows.insert(1, ("Tork", f"{s['torque_nm']} Nm"))
    if s.get("kerb_weight_kg"):
        spec_rows.insert(2, ("Boş ağırlık", f"{s['kerb_weight_kg']} kg"))
    if s.get("fuel_consumption_l_100km"):
        spec_rows.append(("Tüketim", f"{s['fuel_consumption_l_100km']} L/100 km"))
    if s.get("body_type"):
        spec_rows.append(("Gövde", s["body_type"]))
    parts.append('<div class="tw"><table><tbody>' + "".join(
        f'<tr><td class="k">{e(k)}</td><td>{e(v)}</td></tr>' for k, v in spec_rows
    ) + "</tbody></table></div>")

    parts.append(f"<p>{rich(car['note'])}</p>")

    parts.append("<h2>Kriter puanları</h2>")
    parts.append(scores_table(car, criteria))

    # Asıl değer burada: her puanın neden o puan olduğunun yazılı gerekçesi.
    ev = car.get("evidence") or {}
    if ev:
        parts.append("<h2>Bu puanlar neden böyle</h2>")
        for k in criteria["full_order"]:
            block = ev.get(k)
            if not block or not block.get("reasoning"):
                continue
            parts.append(f'<div class="ev"><b>{e(CRIT_TITLES.get(k, k))} — {e(block.get("band", ""))}</b>'
                         f'{rich(block["reasoning"])}</div>')

    if eng and eng.get("known_issues"):
        parts.append(f"<h2>{e(eng['names'][0])} motorunda bilinen arızalar</h2>")
        parts.append(issues_html(eng))
        if eng.get("maintenance"):
            parts.append(f"<p><strong>Bakım notu:</strong> {e(eng['maintenance'])}</p>")
    if box and box.get("known_issues"):
        parts.append(f"<h2>{e(box['names'][0])} şanzımanında bilinen arızalar</h2>")
        parts.append(issues_html(box))
        if box.get("maintenance"):
            parts.append(f"<p><strong>Bakım notu:</strong> {e(box['maintenance'])}</p>")

    parts.append("<h2>Fiyat</h2>")
    lo, hi = car["price_band_k_try"]
    pref = car.get("price_reference")
    if pref:
        parts.append(f"<p>{e(lo)}–{e(hi)} bin TL. Bu bant, {e(pref['as_of'])} tarihinde "
                     f"{e(pref.get('marketplace', 'bir ilan platformunda'))} gözlenen "
                     f"{pref['observations']} ilanın orta yarısıdır (P25–P75).</p>")
        parts.append(f'<p class="warn">Bu değer <strong>istenen ilan fiyatıdır</strong>, '
                     f'gerçekleşmiş satış fiyatı değildir. {e(pref["method"])}</p>')
    else:
        parts.append(f'<p>{e(lo)}–{e(hi)} bin TL.</p>')
        parts.append('<p class="warn">Bu bant tarihlendirilmemiş bir tahmindir; hangi tarihte '
                     've hangi yöntemle ölçüldüğü kayıtlı değil. Türkiye enflasyonunda fiyatlar '
                     'hızla eskidiği için güncel ilanlarla ayrıca karşılaştırılmalıdır.</p>')

    rel = []
    if eng:
        rel.append(f'<a href="{BASE_URL}/motor/{e(s["engine_id"])}.html">{e(eng["names"][0])} motoru</a>')
    if box:
        rel.append(f'<a href="{BASE_URL}/sanziman/{e(s["transmission_id"])}.html">{e(box["names"][0])} şanzımanı</a>')
    if rel:
        parts.append("<h2>Bileşen kayıtları</h2>")
        parts.append(f'<div class="rel">{"".join(rel)}</div>')

    parts.append("<h2>Kaynaklar</h2>")
    parts.append(sources_html(car["sources"], sources))

    jsonld = {
        "@context": "https://schema.org", "@type": "Vehicle", "name": name,
        "vehicleTransmission": s["transmission_type"], "fuelType": s["fuel"],
        "vehicleEngine": {"@type": "EngineSpecification",
                          "enginePower": {"@type": "QuantitativeValue", "value": s["hp"], "unitCode": "BHP"},
                          "engineDisplacement": {"@type": "QuantitativeValue",
                                                 "value": s["displacement_l"], "unitCode": "LTR"}},
        "description": desc, "url": f"{BASE_URL}/arac/{car['id']}.html",
    }
    if s.get("torque_nm"):
        jsonld["vehicleEngine"]["torque"] = {"@type": "QuantitativeValue",
                                             "value": s["torque_nm"], "unitCode": "NU"}
    return f"{car['id']}.html", shell(
        title=title, description=desc,
        canonical=f"{BASE_URL}/arac/{car['id']}.html",
        body="\n".join(parts), jsonld=jsonld)


def component_page(cid, comp, kind, cars, sources) -> tuple[str, str]:
    """Motor ve şanzıman sayfaları aynı deseni izliyor, tek fark alan adları."""
    is_engine = kind == "motor"
    label = "motoru" if is_engine else "şanzımanı"
    name = comp["names"][0]
    users = [c for c in cars
             if c["specs"].get("engine_id" if is_engine else "transmission_id") == cid]

    title = f"{name} {label}: bilinen arızalar ve güvenilirlik"
    n_iss = len(comp.get("known_issues", []))
    desc = (f"{name} {label} için kaynaklı arıza kaydı"
            + (f" ({n_iss} bilinen arıza)" if n_iss else "")
            + f". Bu {'motoru' if is_engine else 'kutuyu'} kullanan {len(users)} araç listede.")

    parts = [f"<h1>{e(name)}</h1>"]
    alt = ", ".join(comp["names"][1:])
    sub = f"Diğer adları: {alt}. " if alt else ""
    parts.append(f'<p class="sub">{e(sub)}Tedarikçi: {e(comp.get("supplier", "—"))}.</p>')

    rows = []
    if is_engine:
        rows += [("Yakıt", comp["fuel"]),
                 ("Hacimler", ", ".join(f"{d} L" for d in comp["displacements_l"])),
                 ("Silindir", comp.get("cylinders")), ("Beslenme", comp.get("aspiration"))]
    else:
        rows += [("Tip", comp.get("type")), ("Vites sayısı", comp.get("gears")),
                 ("Kavrama", comp.get("clutch"))]
    if comp.get("base_score") is not None:
        rows.append(("Temel puan", f"{comp['base_score']} / 100"))
    parts.append('<div class="tw"><table><tbody>' + "".join(
        f'<tr><td class="k">{e(k)}</td><td>{e(v)}</td></tr>' for k, v in rows if v is not None
    ) + "</tbody></table></div>")

    if comp.get("note"):
        # Köşeli parantez içindeki puan gerekçesi iç not; sayfada ayrı gösteriliyor.
        note = comp["note"]
        main_note, _, rationale = note.partition("[base_score gerekçesi:")
        parts.append(f"<p>{rich(main_note.strip())}</p>")
        if rationale:
            parts.append(f'<div class="ev"><b>Temel puan neden bu</b>'
                         f'{e(rationale.rstrip("]").strip())}</div>')

    if comp.get("known_issues"):
        parts.append("<h2>Bilinen arızalar</h2>")
        parts.append(issues_html(comp))
    if comp.get("maintenance"):
        parts.append("<h2>Bakım notu</h2>")
        parts.append(f"<p>{e(comp['maintenance'])}</p>")
    if comp.get("revision_sensitivity"):
        parts.append("<h2>Üretim dönemine duyarlılık</h2>")
        parts.append(f"<p>{e(comp['revision_sensitivity'])}</p>")

    if users:
        parts.append(f"<h2>Bu {'motoru' if is_engine else 'kutuyu'} kullanan araçlar</h2>")
        parts.append('<div class="rel">' + "".join(
            f'<a href="{BASE_URL}/arac/{e(c["id"])}.html">{e(c["name"])}</a>' for c in users
        ) + "</div>")

    parts.append("<h2>Kaynaklar</h2>")
    parts.append(sources_html(comp.get("sources", []), sources))

    return f"{cid}.html", shell(
        title=title, description=desc,
        canonical=f"{BASE_URL}/{kind}/{cid}.html", body="\n".join(parts))


CATALOG_FLAG_TR = {
    "generic_transmission_identity":
        "Şanzıman kutusunun tam ailesi kaynak veride çözülmemiş; tip doğru ama kutu "
        "modeli kesinleşmemiş.",
    "missing_torque": "Tork değeri kaynak veride eksik.",
    "missing_displacement": "Motor hacmi kaynak veride eksik.",
    "missing_technical_url": "Teknik özellik sayfasının adresi kaynak veride eksik.",
    "label_corrected":
        "Kaynak verideki ticari ad, aracın yakıt/hacim/tork değerleriyle çelişiyordu "
        "ve atıldı; yukarıdaki ad doğrulanmış alanlardan yeniden kuruldu.",
    "spec_corrected":
        "Bu kayıtta güç, tork veya yakıt alanlarından biri kaynak veride yanlıştı; "
        "bağımsız teknik kaynaklarla doğrulanıp elle düzeltildi.",
    "spec_implausible":
        "Güç, tork ve motor hacmi birbiriyle fiziksel olarak tutarsız; bu üç alandan "
        "en az biri kaynak veride yanlış. Doğrulanmadan bu kayıt puanlanamaz.",
    "fuel_name_conflict":
        "Aracın ticari adı ile kayıtlı yakıt türü çelişiyor (ör. adı dizel rozeti "
        "taşıyan bir araç benzinli olarak kayıtlı). İkisinden biri yanlış; hangisi "
        "olduğu teknik özellik sayfasından doğrulanmadan bu kayıt puanlanamaz.",
}


def catalog_page(entry: dict, cat_sources: dict) -> tuple[str, str]:
    """Yalnız katalogda olan bir araç için sayfa.

    Bu sayfanın tek bir dürüstlük şartı var: **puan yokmuş gibi davranmamak ve puan
    varmış gibi de göstermemek.** Ziyaretçi aradığı aracı buluyor, teknik künyesini ve
    kaynağını görüyor, ama "bu araç henüz puanlanmadı" cümlesini de görüyor. Sahte bir
    puan göstermek, aracı hiç göstermemekten kötüdür (MK-22).
    """
    sp = entry["specs"]
    name = entry["name"]
    rows = [
        ("Üretim yılı", entry["years"]),
        ("Motor gücü", f"{sp['hp']} bg"),
        ("Tork", f"{sp['torque_nm']:.0f} Nm" if sp.get("torque_nm") else None),
        ("Motor hacmi", f"{sp['displacement_l']} L" if sp.get("displacement_l") else None),
        ("Yakıt", sp.get("fuel")),
        ("Çekiş", sp.get("drivetrain")),
        ("Gövde tipi", sp.get("body_type")),
        ("Şanzıman tipi", sp.get("transmission_type")),
        ("Vites sayısı", f"{sp['gears']} ileri" if sp.get("gears") else None),
        ("Kavrama", sp.get("clutch")),
        ("Motor kodu", sp.get("engine_code")),
        ("Nesil", entry.get("generation")),
    ]
    table = "".join(
        f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in rows if v)

    flags = ""
    if entry.get("quality_flags"):
        items = "".join(
            f"<li>{e(CATALOG_FLAG_TR.get(f, f))}</li>" for f in entry["quality_flags"])
        flags = (
            "<section><h2>Bu kaydın bilinen sınırlılıkları</h2>"
            "<p>Kaynak veri paketi bu kayıt için aşağıdaki eksikleri kendi kalite "
            "sicilinde işaretlemiş. Gizlenmiyorlar, çünkü bu araç ileride puanlanırken "
            "önce bunların çözülmesi gerekiyor.</p>"
            f"<ul>{items}</ul></section>")

    src_items = []
    tech = entry["provenance"].get("technical_url")
    if tech:
        src_items.append(f'<li><a href="{e(tech)}" rel="nofollow noopener">Teknik özellik sayfası</a></li>')
    for sid in entry.get("sources", [])[:6]:
        s = cat_sources.get(sid)
        if s and s.get("url"):
            label = s.get("publisher") or s["url"]
            src_items.append(f'<li><a href="{e(s["url"])}" rel="nofollow noopener">{e(label)}</a></li>')
    src_html = (f"<section><h2>Kaynaklar</h2><ul>{''.join(src_items)}</ul></section>"
                if src_items else "")

    desc = (f"{name} ({entry['years']}) teknik künyesi: {sp['hp']} bg"
            + (f", {sp['torque_nm']:.0f} Nm" if sp.get("torque_nm") else "")
            + f", {sp.get('transmission_type','otomatik')}. "
            "Bu araç veri tabanımızda kayıtlı ama henüz puanlanmadı.")

    body = f"""
<h1>{e(name)}</h1>
<p class="lede">Bu araç veri tabanımızda <strong>teknik künyesiyle kayıtlı</strong>, ama
<strong>henüz puanlanmadı</strong>. Aşağıdaki bilgiler ölçülebilir olgulardır ve kaynağı
gösterilmiştir; motor ve şanzıman güvenilirliğine dair bir değerlendirme içermezler.</p>
<section><h2>Teknik künye</h2><table class="kv">{table}</table></section>
{flags}
<section><h2>Neden puan yok?</h2>
<p>Bu depoda bir aracın puan alması için motor ve şanzıman ailesinin arıza sicilinin
araştırılmış, en az dört bağımsız kaynağa bağlanmış ve her puanın gerekçesinin yazılmış
olması gerekiyor. Bu araç o aşamadan henüz geçmedi. Elimizde puanı olmayan bir araç için
tahmini bir puan üretmek yerine, aracı olduğu gibi göstermeyi tercih ediyoruz:
uydurulmuş bir puan, hiç puan olmamasından daha yanıltıcıdır.</p>
<p><a href="{BASE_URL}/">Puanlanmış araç listesine göz atın</a> — aynı motor veya şanzıman
ailesini paylaşan bir araç zaten puanlanmış olabilir.</p></section>
{src_html}
"""
    jsonld = {
        "@context": "https://schema.org", "@type": "Vehicle", "name": name,
        "brand": {"@type": "Brand", "name": entry["brand"]},
        "fuelType": sp.get("fuel"),
        "vehicleTransmission": sp.get("transmission_type"),
    }
    if sp.get("hp"):
        jsonld["vehicleEngine"] = {"@type": "EngineSpecification",
                                   "enginePower": {"@type": "QuantitativeValue",
                                                   "value": sp["hp"], "unitCode": "BHP"}}
    return f"{entry['id']}.html", shell(
        title=f"{name} teknik özellikleri ({entry['years']}) — henüz puanlanmadı",
        description=desc[:158],
        canonical=f"{BASE_URL}/katalog/{entry['id']}.html",
        body=body, jsonld=jsonld,
    )


def build_all():
    criteria, cars, sources, engines, trans = load()
    catalog, cat_sources = load_catalog()
    pages: dict[pathlib.Path, str] = {}

    for car in cars:
        fname, content = car_page(car, criteria, sources, engines, trans)
        pages[CAR_DIR / fname] = content
    for cid, comp in engines.items():
        fname, content = component_page(cid, comp, "motor", cars, sources)
        pages[ENGINE_DIR / fname] = content
    for cid, comp in trans.items():
        fname, content = component_page(cid, comp, "sanziman", cars, sources)
        pages[TRANS_DIR / fname] = content
    for entry in catalog:
        fname, content = catalog_page(entry, cat_sources)
        pages[CATALOG_DIR / fname] = content

    urls = [f"{BASE_URL}/"] + [
        f"{BASE_URL}/{p.parent.name}/{p.name}" for p in sorted(pages, key=lambda x: str(x))
    ]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
               + "</urlset>\n")
    robots = (f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    return pages, sitemap, robots


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="yazma, güncel mi söyle")
    args = ap.parse_args()

    pages, sitemap, robots = build_all()

    if args.check:
        stale = [p for p, c in pages.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != c]
        if stale or not SITEMAP.exists() or SITEMAP.read_text(encoding="utf-8") != sitemap:
            print(f"statik sayfalar veriyle uyumsuz ({len(stale)} sayfa). "
                  "`python3 scripts/build_pages.py` çalıştırın.", file=sys.stderr)
            return 1
        print(f"{len(pages)} statik sayfa güncel.")
        return 0

    # Silinen bir araç kaydının sayfası ortada kalmasın diye klasörler sıfırlanıyor.
    for d in (CAR_DIR, ENGINE_DIR, TRANS_DIR, CATALOG_DIR):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    for path, content in pages.items():
        path.write_text(content, encoding="utf-8")
    SITEMAP.write_text(sitemap, encoding="utf-8")
    ROBOTS.write_text(robots, encoding="utf-8")

    total = sum(len(c) for c in pages.values())
    print(f"{len(pages)} statik sayfa yazıldı ({total:,} bayt).")
    print(f"  araç: {len(list(CAR_DIR.glob('*.html')))} · "
          f"motor: {len(list(ENGINE_DIR.glob('*.html')))} · "
          f"şanzıman: {len(list(TRANS_DIR.glob('*.html')))} · "
          f"katalog: {len(list(CATALOG_DIR.glob('*.html')))}")
    print(f"sitemap.xml ve robots.txt yazıldı ({len(pages) + 1} adres).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
