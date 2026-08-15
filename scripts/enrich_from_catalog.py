#!/usr/bin/env python3
"""enrich_from_catalog.py — puanlanmış araçları katalog olgularıyla zenginleştirir.

**Neden var.** MK-22 ile gelen olgusal katalog (`data/catalog/`), `data/cars/` içindeki
araçlarda bulunmayan alanlar taşıyor: ileri vites sayısı, kavrama tipi, üreticinin motor
kodu, nesil adı ve teknik özellik sayfasının adresi. Bunlar ölçümdür, yargı değildir; bu
yüzden aktarılmalarında sakınca yok. Aktarılmamaları ise gerçek bir kayıp: kavrama tipi
kuru/ıslak ayrımını, motor kodu ise nesil doğrulamasını (MK-08) doğrudan okunur kılıyor.

**Yazma kuralı — çelişki varsa yazma.** Bir puanlanmış araca birden çok katalog kaydı
bağlanabiliyor (aynı araç farklı gövde veya nesil satırlarında geçtiği için). Bir alanın
değeri bu kayıtlar arasında çelişiyorsa alan **boş bırakılır** ve rapora yazılır. MK-15'in
kuralı burada da geçerli: boş bir alan, yanlış bir alandan iyidir. Mevcut bir değerin
üzerine de yazılmaz; depodaki değer, araştırmayla girilmiş olabilir.

**Puana dokunmaz.** Bu betik `scores`, `evidence`, `sources` veya `verification`
alanlarına hiç dokunmaz. Katalog kaynakları `car["sources"]` içine girmez — o liste puanı
destekleyen kanıt sicilidir (MK-19 ve MK-22 aynı ayrımı yapıyor).

Kullanım:
    python3 scripts/enrich_from_catalog.py            # rapor, dosya yazmaz
    python3 scripts/enrich_from_catalog.py --write    # araç kayıtlarına işle
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARS = ROOT / "data" / "cars"
CATALOG = ROOT / "data" / "catalog"
LINKED_AT = "2026-08-15"

# Katalogdan araç kaydına taşınabilecek olgusal alanlar.
SPEC_FIELDS = ["gears", "clutch", "engine_code", "torque_nm", "body_type"]


def load_catalog() -> list[dict]:
    out = []
    for path in sorted(CATALOG.glob("*.json")):
        if path.name == "_sources.json":
            continue
        out.extend(json.loads(path.read_text(encoding="utf-8")).get("entries", []))
    return out


def agree(values: list):
    """Çelişkisiz tek bir değer varsa onu, yoksa None döner."""
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    first = vals[0]
    return first if all(v == first for v in vals) else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    by_car = collections.defaultdict(list)
    for entry in load_catalog():
        if entry.get("scored_car_id"):
            by_car[entry["scored_car_id"]].append(entry)

    filled = collections.Counter()
    conflicts = collections.Counter()
    touched = 0

    for path in sorted(CARS.glob("*.json")):
        car = json.loads(path.read_text(encoding="utf-8"))
        entries = by_car.get(car["id"])
        if not entries:
            continue

        specs = car["specs"]
        changed = False

        for field in SPEC_FIELDS:
            if specs.get(field) is not None:
                continue  # mevcut değerin üzerine yazılmaz
            value = agree([e["specs"].get(field) for e in entries])
            if value is None:
                if any(e["specs"].get(field) is not None for e in entries):
                    conflicts[field] += 1
                continue
            specs[field] = value
            filled[field] += 1
            changed = True

        generation = agree([e.get("generation") for e in entries])
        technical_url = agree([e["provenance"].get("technical_url") for e in entries])
        ref = {
            "catalog_ids": sorted(e["id"] for e in entries),
            "generation": generation,
            "technical_url": technical_url,
            "dataset": entries[0]["provenance"]["dataset"],
            "linked_at": LINKED_AT,
        }
        if car.get("catalog_ref") != ref:
            car["catalog_ref"] = ref
            filled["catalog_ref"] += 1
            changed = True

        if changed:
            touched += 1
            if args.write:
                path.write_text(json.dumps(car, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")

    print(f"katalog kaydı bağlı araç : {len(by_car)}")
    print(f"değişen araç             : {touched}")
    print("doldurulan alanlar:")
    for k, n in filled.most_common():
        print(f"    {k:16} {n}")
    if conflicts:
        print("çelişki yüzünden BOŞ BIRAKILAN alanlar (MK-15):")
        for k, n in conflicts.most_common():
            print(f"    {k:16} {n}")
    if not args.write:
        print("\n(rapor kipi — dosya yazılmadı; işlemek için --write)")


if __name__ == "__main__":
    main()
