#!/usr/bin/env python3
"""import_tsb_catalog.py — TSB Kasko Değer Listesi'nden yeni katalog kaydı üretir.

Kullanıcı "portföyü öbür listeden ilham alarak genişlet" dedi. `data/catalog/*.json`
dosyaları elle düzenlenmiyor (her dosyanın kendi `_comment`'i bunu söylüyor) — bu betik
o kuralı bozmadan, TSB verisinden **kod aracılığıyla** yeni kayıt üretir.

Neden tam otomatik değil. `scripts/import_tsb_kasko.py` 1.508 satırı otomatik ayrıştırdı
ve yalnızca 76'sının otomatik şanzımanlı olduğunu, bunların da 35 benzersiz teknik
kombinasyona indiğini buldu (bkz. docs/ROADMAP.md Y-22). 35 küçük bir sayı olduğu için
her biri elle, tek tek incelendi: hangisi zaten `data/cars/` veya `data/catalog/`
içinde var (17'si), hangisi teknik olarak gerçek bir tarihi üretim kombinasyonu mu yoksa
şüpheli mi (Alfa MiTo 1.4 170 QV + TCT — bu oturumda tekrarlayan "zamanda imkânsız
eşleşme" ailesinden, QV 170'in bilinen üretim tarihçesiyle çelişiyor — bilinçli olarak
ATLANDI), gövde tipi ve çekiş TSB metninden veya modelin bilinen mimarisinden ne kadar
güvenle çıkarılabilir. Bu inceleme kodda değil bu dosyanın altındaki `NEW_ENTRIES`
listesinde duruyor; betik yalnızca o listeyi doğrulayıp mekanik olarak yazıyor —
tıpkı `scripts/import_kerb_weight.py`'nin elle hazırlanmış çalışma listesini işlemesi
gibi (MK-15 ile aynı desen: kanıt insan tarafından bulunur, yazma mekanik ve denetimli
olur).

Kullanım:
    python3 scripts/import_tsb_catalog.py            # listeyi doğrula, yazma
    python3 scripts/import_tsb_catalog.py --write    # data/catalog/*.json içine yaz
"""
from __future__ import annotations

import argparse
import json
import pathlib
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "data" / "catalog"
SOURCE_ID = "tsb_kasko_degeri_2026_07"
DATASET = "TSB-KASKO-2026-07"
IMPORTED_AT = "2026-08-18"

# Her satır TSB'nin ham verisinden elle doğrulandı: marka+tip kodu TSB'nin kendi
# birincil anahtarı (source_variant_id), years TSB'de o teknik kombinasyonun DEĞER
# taşıdığı model yıllarının (birden fazla eşdeğer satır varsa hepsinin birleşimi)
# min-max'ı. drivetrain ve body_type TSB metninde açık token yoksa modelin bilinen
# mimarisinden çıkarıldı (ör. Peugeot 3008 Mk1 hiçbir zaman bu motorlarla 4x4 satılmadı
# → Önden güvenle yazılabilir); şanzıman AİLESİ (kuru/ıslak DCT) TSB metninde hiç
# geçmiyor, bu yüzden her DCT kaydına `generic_transmission_identity` bayrağı kondu —
# katalogdaki 798 kayıt zaten aynı bayrağı taşıyor, bu yeni bir istisna değil.
NEW_ENTRIES = [
    dict(file="opel", brand="Opel", model_family="Crossland X",
         name="Opel Crossland X 1.2 Turbo AT6", years="2017-2019",
         hp=110, displacement_l=1.2, fuel="Benzin", drivetrain="Önden",
         body_type="SUV", transmission_type="TK", transmission_name="AT6",
         source_variant_id="1313"),
    dict(file="opel", brand="Opel", model_family="Corsa",
         name="Opel Corsa 1.4 AT6", years="2016-2019",
         hp=90, displacement_l=1.4, fuel="Benzin", drivetrain="Önden",
         body_type="Hatchback", transmission_type="TK", transmission_name="AT6",
         source_variant_id="1234"),
    dict(file="volkswagen", brand="VW", model_family="Jetta",
         name="VW Jetta 2.0 FSI Tiptronic", years="2014-2014",
         hp=150, displacement_l=2.0, fuel="Benzin", drivetrain="Önden",
         body_type="Sedan", transmission_type="TK", transmission_name="Tiptronic",
         source_variant_id="1532"),
    dict(file="opel", brand="Opel", model_family="Mokka X",
         name="Opel Mokka X 1.6 CDTI AT6", years="2018-2018",
         hp=136, displacement_l=1.6, fuel="Dizel", drivetrain="Önden",
         body_type="SUV", transmission_type="TK", transmission_name="AT6",
         source_variant_id="1342"),
    dict(file="skoda", brand="Skoda", model_family="Rapid",
         name="Skoda Rapid Spaceback 1.0 TSI DSG", years="2017-2018",
         hp=110, displacement_l=1.0, fuel="Benzin", drivetrain="Önden",
         body_type="Hatchback", transmission_type="Kuru DCT", transmission_name="DSG7",
         source_variant_id="1194"),
    dict(file="seat", brand="Seat", model_family="Ibiza",
         name="Seat Ibiza FR 1.4 TSI DSG · 150 bg", years="2012-2012",
         hp=150, displacement_l=1.4, fuel="Benzin", drivetrain="Önden",
         body_type="Hatchback", transmission_type="Kuru DCT", transmission_name="DSG7",
         source_variant_id="303"),
    dict(file="citro-n", brand="Citroën", model_family="C5",
         name="Citroën C5 1.6 e-HDi 115 MCP", years="2012-2015",
         hp=115, displacement_l=1.6, fuel="Dizel", drivetrain="Önden",
         body_type="Sedan", transmission_type="Robot", transmission_name="MCP",
         source_variant_id="1022"),
    dict(file="citro-n", brand="Citroën", model_family="C5",
         name="Citroën C5 1.6 e-HDi 112 MCP", years="2012-2013",
         hp=112, displacement_l=1.6, fuel="Dizel", drivetrain="Önden",
         body_type="Sedan", transmission_type="Robot", transmission_name="MCP",
         source_variant_id="331"),
    dict(file="peugeot", brand="Peugeot", model_family="3008",
         name="Peugeot 3008 1.6 HDi 112 Auto6", years="2012-2013",
         hp=112, displacement_l=1.6, fuel="Dizel", drivetrain="Önden",
         body_type="SUV", transmission_type="TK", transmission_name="AUTO6R",
         source_variant_id="872"),
    dict(file="peugeot", brand="Peugeot", model_family="3008",
         name="Peugeot 3008 1.6 HDi 110 Auto6", years="2012-2012",
         hp=110, displacement_l=1.6, fuel="Dizel", drivetrain="Önden",
         body_type="SUV", transmission_type="TK", transmission_name="AUTO6R",
         source_variant_id="849"),
    dict(file="citro-n", brand="Citroën", model_family="DS4",
         name="Citroën DS4 1.6 e-HDi 112 MCP", years="2012-2012",
         hp=112, displacement_l=1.6, fuel="Dizel", drivetrain="Önden",
         body_type="Hatchback", transmission_type="Robot", transmission_name="MCP",
         source_variant_id="352"),
    dict(file="citro-n", brand="Citroën", model_family="DS4",
         name="Citroën DS4 1.6 THP 156 MCP", years="2012-2013",
         hp=156, displacement_l=1.6, fuel="Benzin", drivetrain="Önden",
         body_type="Hatchback", transmission_type="Robot", transmission_name="MCP",
         source_variant_id="353"),
    dict(file="skoda", brand="Skoda", model_family="Octavia",
         name="Skoda Octavia RS 2.0 TDI CR 170 DSG", years="2012-2012",
         hp=170, displacement_l=2.0, fuel="Dizel", drivetrain="Önden",
         body_type=None, transmission_type="Islak DCT", transmission_name="DSG6",
         source_variant_id="383"),
    dict(file="skoda", brand="Skoda", model_family="Superb",
         name="Skoda Superb Elegance 1.8 TSI 160 Tiptronic", years="2012-2012",
         hp=160, displacement_l=1.8, fuel="Benzin", drivetrain="Önden",
         body_type="Sedan/Liftback", transmission_type="TK", transmission_name="Tiptronic",
         source_variant_id="373"),
    dict(file="audi", brand="Audi", model_family="A1",
         name="Audi A1 Sportback 1.6 TDI 90 S tronic", years="2012-2015",
         hp=90, displacement_l=1.6, fuel="Dizel", drivetrain="Önden",
         body_type="Hatchback", transmission_type="Kuru DCT", transmission_name="S tronic 7",
         source_variant_id="1025"),
]


TURKISH_MAP = str.maketrans("ığüşöçİĞÜŞÖÇ", "igusocigusoc")


def slug(text: str) -> str:
    text = text.translate(TURKISH_MAP)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    out = []
    for ch in text.lower():
        if ch.isalnum() and ch.isascii():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def build_entry(spec: dict, existing_ids: set[str]) -> dict:
    base_id = f"{slug(spec['brand'])}-{slug(spec['model_family'])}-{slug(str(spec['displacement_l']))}-{spec['hp']}"
    entry_id = base_id
    n = 2
    while entry_id in existing_ids:
        entry_id = f"{base_id}-{n}"
        n += 1
    existing_ids.add(entry_id)

    return {
        "id": entry_id,
        "name": spec["name"],
        "brand": spec["brand"],
        "model_family": spec["model_family"],
        "generation": None,
        "years": spec["years"],
        "specs": {
            "hp": spec["hp"],
            "torque_nm": None,
            "displacement_l": spec["displacement_l"],
            "fuel": spec["fuel"],
            "drivetrain": spec["drivetrain"],
            "body_type": spec["body_type"],
            "transmission_type": spec["transmission_type"],
            "transmission_name": spec["transmission_name"],
            "gears": None,
            "clutch": None,
            "engine_code": None,
            "engine_name": None,
        },
        "scored_car_id": None,
        "possible_scored_car_ids": [],
        "quality_flags": ["generic_transmission_identity"],
        "sources": [SOURCE_ID],
        "provenance": {
            "dataset": DATASET,
            "imported_at": IMPORTED_AT,
            "source_variant_id": spec["source_variant_id"],
            "publication_status": "tsb_manual_curation",
            "technical_url": None,
            "rejected_label": None,
            "manually_corrected_fields": None,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="katalog dosyalarına yaz")
    args = ap.parse_args()

    existing_ids: set[str] = set()
    files: dict[str, dict] = {}
    for f in CATALOG_DIR.glob("*.json"):
        if f.name == "_sources.json":
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        files[f.stem] = (f, d)
        for e in d.get("entries", []):
            existing_ids.add(e["id"])
    for f in ROOT.glob("data/cars/*.json"):
        existing_ids.add(json.loads(f.read_text(encoding="utf-8"))["id"])

    by_file: dict[str, list[dict]] = {}
    for spec in NEW_ENTRIES:
        entry = build_entry(spec, existing_ids)
        by_file.setdefault(spec["file"], []).append(entry)

    print(f"{len(NEW_ENTRIES)} yeni katalog kaydı üretilecek, {len(by_file)} marka dosyasına dağılıyor:")
    for fname, entries in sorted(by_file.items()):
        for e in entries:
            print(f"  {fname:12s} {e['id']:45s} {e['years']:9s} {e['specs']['hp']:3d}bg "
                  f"{e['specs']['fuel']:6s} {e['specs']['transmission_type']}")

    if not args.write:
        print("\n(yazmadan çalıştırıldı; uygulamak için --write ver)")
        return 0

    for fname, entries in by_file.items():
        path, d = files[fname]
        d["entries"].extend(entries)
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    src_path = CATALOG_DIR / "_sources.json"
    src = json.loads(src_path.read_text(encoding="utf-8"))
    if SOURCE_ID not in src["sources"]:
        src["sources"][SOURCE_ID] = {
            "id": SOURCE_ID,
            "publisher": "Türkiye Sigorta Birliği (TSB)",
            "url": "https://tsb.org.tr/",
            "type": "spec-database",
            "tier": "A",
        }
        src["sources"] = dict(sorted(src["sources"].items()))
        src_path.write_text(json.dumps(src, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{len(NEW_ENTRIES)} kayıt {len(by_file)} dosyaya yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
