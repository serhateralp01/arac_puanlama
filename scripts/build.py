#!/usr/bin/env python3
"""build.py — data/ + templates/ → index.html

Tek dosyalık aracı veriden üretir. Harici bağımlılık yok, standart kütüphane yeter.
Elle düzenlenen tek şey data/ ve templates/; kök dizindeki HTML çıktıdır.

Kullanım:
    python3 scripts/build.py            # üret
    python3 scripts/build.py --check    # üretilmiş dosya güncel mi, yaz(ma)dan söyle
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"
TEMPLATE = TEMPLATES / "index.html"
STYLES = TEMPLATES / "styles.css"
SCREENS = TEMPLATES / "screens"
APP = TEMPLATES / "app"
# GitHub Pages kök adreste index.html arar; başka bir ad verilirse depo özetini
# (README) gösterir. Çıktının adı bu yüzden index.html.
OUTPUT = ROOT / "index.html"
# Ayrıntı verisi (araç açıklaması + motor/şanzıman kanıt metni) index.html'in
# dışında, ayrı bir dosyada tutuluyor ve yalnız bir kart/satır ilk kez
# açıldığında fetch() ile çekiliyor; gerekçesi docs/ARCHITECTURE.md MK-24
# kaydında (ölçüm: bu tek alan çifti 406 araçta 2 MB'lık dosyanın %68'ini
# oluşturuyordu, oysa liste/kart görünümü hiçbirini okumuyor).
DETAIL_OUTPUT = ROOT / "detay.json"


def load_data() -> tuple[dict, list[dict], dict, dict, dict]:
    criteria = json.loads((DATA / "criteria.json").read_text(encoding="utf-8"))
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    engines = json.loads((DATA / "engines.json").read_text(encoding="utf-8"))
    transmissions = json.loads((DATA / "transmissions.json").read_text(encoding="utf-8"))
    cars = [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((DATA / "cars").glob("*.json"))
    ]
    # Tarayıcıdaki sıralama, göç öncesi listeyle aynı kalsın diye legacy_index'e
    # göre diziliyor; yeni araçlarda bu alan yoksa dosya adı sırası geçerli.
    cars.sort(key=lambda c: (c.get("legacy_index", 10**6), c["id"]))
    return criteria, cars, sources, engines, transmissions


def data_fingerprint(
    criteria: dict, cars: list[dict], sources: dict, engines: dict, transmissions: dict
) -> str:
    """Veri klasörünün içeriğine bağlı, oluşturma zamanından bağımsız damga.

    Zaman damgası kullanmıyoruz: aynı veriden her zaman aynı HTML çıksın ki
    `--check` gürültüsüz çalışsın ve git diff yalnızca gerçek değişimi göstersin.
    """
    blob = json.dumps(
        {
            "criteria": criteria,
            "cars": cars,
            "sources": sources,
            "engines": engines,
            "transmissions": transmissions,
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


def riskiest(components: dict, n: int = 5) -> list[dict]:
    """En düşük base_score'a sahip ilk n bileşeni döndürür.

    Ana ekranın "hangi motor/şanzıman beni yakar" bulgusu buradan besleniyor
    (Y-07). base_score'u henüz atanmamış bileşenler (araştırma yapılmamış)
    listeye girmiyor; boş bir alanı "en riskli" diye göstermek yanlış olurdu.
    """
    scored = [
        {"id": c["id"], "name": c["names"][0], "score": c["base_score"]}
        for key, c in components.items()
        if key != "_comment" and c.get("base_score") is not None
    ]
    scored.sort(key=lambda c: c["score"])
    return scored[:n]


def load_catalog_index() -> list[dict]:
    """Arayüzün arama kutusu için kırpılmış katalog dizini (MK-22).

    Yalnız **yalnız katalogda olan** kayıtlar alınır; puanlanmış bir araca bağlı
    olanlar zaten tabloda görünüyor ve iki kez listelenmeleri kullanıcıyı yanıltırdı.

    Alanlar bilinçli olarak azdır. Tam katalog kaydı (kaynaklar, kalite işaretleri,
    nesil, motor kodu) sayfa başına üretilen statik HTML'de zaten var; arayüze yalnız
    aramanın ve kısa künyenin ihtiyaç duyduğu alanlar taşınıyor. Tam kaydı gömmek
    index.html'i gereksiz yere birkaç yüz KB büyütürdü (Y-14'ün boyut kaygısı).
    """
    cat_dir = DATA / "catalog"
    if not cat_dir.exists():
        return []
    out = []
    for path in sorted(cat_dir.glob("*.json")):
        if path.name == "_sources.json":
            continue
        for e in json.loads(path.read_text(encoding="utf-8")).get("entries", []):
            if e.get("scored_car_id") or e.get("possible_scored_car_ids"):
                continue
            sp = e["specs"]
            out.append({
                "id": e["id"], "n": e["name"], "g": e["brand"], "y": e["years"],
                "hp": sp["hp"], "f": sp["fuel"], "tx": sp["transmission_type"],
                "b": sp.get("body_type"), "d": sp.get("displacement_l"),
            })
    out.sort(key=lambda x: (x["g"], x["n"]))
    return out


def to_runtime_db(
    criteria: dict, cars: list[dict], sources: dict, engines: dict, transmissions: dict
) -> tuple[dict, dict]:
    """Zengin JSON şemasını tarayıcı kodunun beklediği sade şekle indirger.

    Arayüz kodu göçten beri değişmedi; dönüşüm burada yapılıyor ki veri
    dosyaları okunabilir kalsın, UI kodu da yeniden yazılmak zorunda olmasın.

    İki sözlük döndürür: `db` (index.html'e gömülen, listeyi çizmek için
    yeterli özet veri) ve `detail` (detay.json'a yazılan, yalnız bir aracın
    ayrıntı paneli açıldığında okunan `note`+`evidence` metinleri, MK-24).
    """
    # Bant örnekleri (ör. "honda-civic-fd6-1-6") kimlikle veriliyor ki
    # data/criteria.json okunurken hangi aracın kastedildiği açık kalsın; arayüzde
    # gösterilecek olan ise kullanıcının bildiği araç adı. Çözümleme burada, derleme
    # sırasında yapılıyor ki JS tarafı id→ad eşlemesi taşımak zorunda kalmasın.
    cars_by_id = {car["id"]: car for car in cars}

    def band_runtime(b: dict) -> dict:
        ex = b.get("example")
        return {
            "range": b["range"],
            "name": b["name"],
            "test": b["test"],
            "example": cars_by_id[ex]["name"] if ex else None,
            "note": b.get("note"),
        }

    crit_runtime = []
    for c in criteria["criteria"]:
        entry = {
            "k": c["key"],
            "t": c["title"],
            "d": c["definition"],
            "inc": c["includes"],
            "exc": c["excludes"],
            "wr": c.get("weight_rationale"),
            "bands": [band_runtime(b) for b in c["bands"]] if c.get("bands") else None,
        }
        if c.get("auto"):
            entry["AUTO"] = 1
        crit_runtime.append(entry)

    verif_map = {"verified": True, "partial": "p", "preliminary": False}

    cars_runtime = []
    detail_runtime = {}
    for car in cars:
        s = car["specs"]
        cars_runtime.append(
            {
                # Arayüzde her araca kendi numaralı bir "id" atanıyor (00-cekirdek.js,
                # cmpSet ve satır/kart eşlemesi için); bu, build_pages.py'nin ürettiği
                # statik sayfanın dosya adıyla (data/cars/*.json'daki kalıcı id) aynı
                # değer değil. Ana ekranın "en yüksek puanlı beş araç" bulgusu bu
                # statik sayfaya bağlanabilsin diye kalıcı kimlik ayrı bir alanda
                # (cid) taşınıyor (Y-25 dördüncü faz); aynı cid, aracın ayrıntı
                # verisini detay.json'da bulmak için de kullanılıyor (MK-24).
                "cid": car["id"],
                "p": car["price_band_k_try"],
                "y": car["years"],
                "n": car["name"],
                "tag": car["tag"],
                "hp": s["hp"],
                "disp": s["displacement_l"],
                "tx": s["transmission_type"],
                "fuel": s["fuel"],
                "drv": s["drivetrain"],
                "body": s.get("body_type"),
                "g": car["brand_group"],
                "v": verif_map[car["verification"]],
                "r": car["sources"],
                "s": [car["scores"][k] for k in criteria["scored_order"]],
            }
        )
        # `note` (araç açıklaması) ve `evidence` (motor/şanzıman kanıt metni)
        # yalnız ayrıntı paneli açıldığında okunuyor, liste/kart görünümü hiç
        # dokunmuyor; ama 406 araçta ikisi birlikte dosyanın %68'ini oluşturuyor
        # (MK-24 ölçümü). Bu yüzden index.html'e değil detay.json'a yazılıyor.
        detail_runtime[car["id"]] = {
            "note": car["note"],
            "ev": car.get("evidence") or {},
        }

    # Sayfada yalnızca araçlara bağlanmış kaynaklar listeleniyor; artık hiçbir
    # araca bağlı olmayan kaynaklar arşivde kalır ama sayfaya basılmaz.
    used = {sid for car in cars for sid in car["sources"]}
    sources_runtime = {
        sid: [src["claim"], src["publisher"], src["url"]]
        for sid, src in sources.items()
        if sid in used
    }

    db = {
        "cars": cars_runtime,
        "catalog": load_catalog_index(),
        "sources": sources_runtime,
        "criteria": crit_runtime,
        "head_labels": {c["key"]: c["short"] for c in criteria["criteria"]},
        "scored_order": criteria["scored_order"],
        "full_order": criteria["full_order"],
        "weak_threshold": criteria["weak_threshold"],
        "presets": criteria["presets"],
        "preset_labels": criteria["preset_labels"],
        # Ana ekranın (#ana, Y-07) veri kapsamı özeti ve "hangi bileşen beni
        # yakar" bulgusu için: elle yazılmasın diye burada, veriden hesaplanıyor.
        "engine_count": len([k for k in engines if k != "_comment"]),
        "transmission_count": len([k for k in transmissions if k != "_comment"]),
        "riskiest_engines": riskiest(engines),
        "riskiest_transmissions": riskiest(transmissions),
        "build_stamp": "",  # render() dolduruyor
    }
    return db, detail_runtime


def concat_parts(folder: pathlib.Path, suffix: str) -> str:
    """Bir klasördeki parçaları dosya adına göre sırayla birleştirir.

    Dosya adlarının başındaki sayı yükleme sırasını belirler (00-, 10-, 20- ...).
    Sıra önemlidir: betikler ortak bir kapsamı paylaştığı için bir parça,
    kendinden önce tanımlanmış olana güvenebilir. Yeni bir ekran veya davranış
    eklemek, doğru numarayla yeni bir dosya açmaktan ibarettir; gerekçesi
    docs/ARCHITECTURE.md MK-07 kaydında.
    """
    parts = sorted(folder.glob(f"*{suffix}"))
    if not parts:
        raise SystemExit(f"{folder.relative_to(ROOT)} içinde {suffix} parçası yok.")
    chunks = []
    for p in parts:
        chunks.append(f"/* ==== {p.name} ==== */")
        chunks.append(p.read_text(encoding="utf-8").rstrip())
    return "\n".join(chunks)


def concat_screens() -> str:
    """Ekran parçalarını sırayla birleştirir; HTML olduğu için yorum biçimi ayrı."""
    parts = sorted(SCREENS.glob("*.html"))
    if not parts:
        raise SystemExit("templates/screens/ içinde ekran parçası yok.")
    chunks = []
    for p in parts:
        chunks.append(f"<!-- ==== {p.name} ==== -->")
        chunks.append(p.read_text(encoding="utf-8").rstrip())
    return "\n".join(chunks)


def render() -> tuple[str, str]:
    """index.html içeriğini ve ayrı detay.json içeriğini birlikte üretir (MK-24)."""
    criteria, cars, sources, engines, transmissions = load_data()
    stamp = f"veri damgası {data_fingerprint(criteria, cars, sources, engines, transmissions)}"

    db, detail = to_runtime_db(criteria, cars, sources, engines, transmissions)
    db["build_stamp"] = stamp

    template = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(db, ensure_ascii=False, separators=(",", ":"))
    # </script> dizisi JSON içinde geçerse betiği erkenden kapatır.
    payload = payload.replace("</", "<\\/")

    app_js = concat_parts(APP, ".js").replace("/*__DB__*/null", payload)

    html = template.replace("/*__STYLES__*/", STYLES.read_text(encoding="utf-8").rstrip())
    html = html.replace("<!--__SCREENS__-->", concat_screens())
    html = html.replace("/*__APP__*/", app_js)
    html = html.replace("__CAR_COUNT__", str(len(cars)))
    html = html.replace("__BUILD_STAMP__", stamp)

    detail_json = json.dumps(detail, ensure_ascii=False, separators=(",", ":"))
    return html, detail_json


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--check",
        action="store_true",
        help="dosyayı yazma, sadece güncel olup olmadığını bildir",
    )
    args = ap.parse_args()

    html, detail_json = render()
    if args.check:
        current_html = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        current_detail = DETAIL_OUTPUT.read_text(encoding="utf-8") if DETAIL_OUTPUT.exists() else ""
        stale = []
        if current_html != html:
            stale.append(str(OUTPUT.relative_to(ROOT)))
        if current_detail != detail_json:
            stale.append(str(DETAIL_OUTPUT.relative_to(ROOT)))
        if stale:
            print(
                f"{', '.join(stale)} veriyle uyumsuz. `python3 scripts/build.py` çalıştırın.",
                file=sys.stderr,
            )
            return 1
        print("index.html ve detay.json güncel.")
        return 0

    OUTPUT.write_text(html, encoding="utf-8")
    DETAIL_OUTPUT.write_text(detail_json, encoding="utf-8")
    print(f"{OUTPUT.relative_to(ROOT)} yazıldı ({len(html):,} bayt).")
    print(f"{DETAIL_OUTPUT.relative_to(ROOT)} yazıldı ({len(detail_json):,} bayt).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
