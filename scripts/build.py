#!/usr/bin/env python3
"""build.py — data/ + templates/ → arac-puanlama.html

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
OUTPUT = ROOT / "arac-puanlama.html"


def load_data() -> tuple[dict, list[dict], dict]:
    criteria = json.loads((DATA / "criteria.json").read_text(encoding="utf-8"))
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    cars = [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((DATA / "cars").glob("*.json"))
    ]
    # Tarayıcıdaki sıralama, göç öncesi listeyle aynı kalsın diye legacy_index'e
    # göre diziliyor; yeni araçlarda bu alan yoksa dosya adı sırası geçerli.
    cars.sort(key=lambda c: (c.get("legacy_index", 10**6), c["id"]))
    return criteria, cars, sources


def data_fingerprint(criteria: dict, cars: list[dict], sources: dict) -> str:
    """Veri klasörünün içeriğine bağlı, oluşturma zamanından bağımsız damga.

    Zaman damgası kullanmıyoruz: aynı veriden her zaman aynı HTML çıksın ki
    `--check` gürültüsüz çalışsın ve git diff yalnızca gerçek değişimi göstersin.
    """
    blob = json.dumps(
        {"criteria": criteria, "cars": cars, "sources": sources},
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


def to_runtime_db(criteria: dict, cars: list[dict], sources: dict) -> dict:
    """Zengin JSON şemasını tarayıcı kodunun beklediği sade şekle indirger.

    Arayüz kodu göçten beri değişmedi; dönüşüm burada yapılıyor ki veri
    dosyaları okunabilir kalsın, UI kodu da yeniden yazılmak zorunda olmasın.
    """
    crit_runtime = []
    for c in criteria["criteria"]:
        entry = {
            "k": c["key"],
            "t": c["title"],
            "d": c["definition"],
            "inc": c["includes"],
            "exc": c["excludes"],
        }
        if c.get("auto"):
            entry["AUTO"] = 1
        crit_runtime.append(entry)

    verif_map = {"verified": True, "partial": "p", "preliminary": False}

    cars_runtime = []
    for car in cars:
        s = car["specs"]
        cars_runtime.append(
            {
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
                "note": car["note"],
            }
        )

    # Sayfada yalnızca araçlara bağlanmış kaynaklar listeleniyor; artık hiçbir
    # araca bağlı olmayan kaynaklar arşivde kalır ama sayfaya basılmaz.
    used = {sid for car in cars for sid in car["sources"]}
    sources_runtime = {
        sid: [src["claim"], src["publisher"], src["url"]]
        for sid, src in sources.items()
        if sid in used
    }

    return {
        "cars": cars_runtime,
        "sources": sources_runtime,
        "criteria": crit_runtime,
        "head_labels": {c["key"]: c["short"] for c in criteria["criteria"]},
        "scored_order": criteria["scored_order"],
        "full_order": criteria["full_order"],
        "weak_threshold": criteria["weak_threshold"],
        "presets": criteria["presets"],
        "preset_labels": criteria["preset_labels"],
        "build_stamp": "",  # render() dolduruyor
    }


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


def render() -> str:
    criteria, cars, sources = load_data()
    stamp = f"veri damgası {data_fingerprint(criteria, cars, sources)}"

    db = to_runtime_db(criteria, cars, sources)
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
    return html


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--check",
        action="store_true",
        help="dosyayı yazma, sadece güncel olup olmadığını bildir",
    )
    args = ap.parse_args()

    html = render()
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != html:
            print(
                "arac-puanlama.html veriyle uyumsuz. `python3 scripts/build.py` çalıştırın.",
                file=sys.stderr,
            )
            return 1
        print("arac-puanlama.html güncel.")
        return 0

    OUTPUT.write_text(html, encoding="utf-8")
    print(f"{OUTPUT.relative_to(ROOT)} yazıldı ({len(html):,} bayt).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
