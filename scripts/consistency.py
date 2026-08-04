#!/usr/bin/env python3
"""consistency.py — aynı donanımı paylaşan araçlar arasındaki puan tutarlılığı.

Bu betiğin varlık sebebi şudur: puanlar araç seviyesinde veriliyor, ama kanıtın çoğu
bileşen seviyesinde bulunuyor. Aynı şanzıman kutusu her araçta yeniden ve elden
değerlendirilince, aynı donanım farklı puanlar almaya başlıyor ve bu farkın gerekçesi
hiçbir yerde yazılı olmuyor.

Betik, aynı `transmission_id` değerini paylaşan araçların `trans` puanlarını
karşılaştırır ve yayılımı eşiği aşan kutuları raporlar. Motor kayıtları kurulduğunda
(`data/engines.json`) aynı denetim `motor` puanı için de çalıştırılacak.

Kullanım:
    python3 scripts/consistency.py
    python3 scripts/consistency.py --max-spread 10   # eşiği değiştir
    python3 scripts/consistency.py --json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Aynı kutuyu paylaşan araçlar arasında gerekçesiz kabul edilebilecek azami puan farkı.
# Sıfır seçilmedi, çünkü aynı kutunun farklı tork seviyelerinde çalışması gerçek bir
# fark yaratabiliyor. On beş puanın üstü ise açıklama gerektirir.
DEFAULT_MAX_SPREAD = 15


def load_cars() -> list[dict]:
    return [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((DATA / "cars").glob("*.json"))
    ]


def group_by_transmission(cars: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for car in cars:
        box_id = car["specs"].get("transmission_id")
        if box_id:
            groups.setdefault(box_id, []).append(car)
    return groups


def analyse(groups: dict[str, list[dict]], max_spread: int) -> tuple[list[dict], list[dict]]:
    findings, clean = [], []
    for box_id, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        scores = [c["scores"]["trans"] for c in members]
        spread = max(scores) - min(scores)
        entry = {
            "transmission_id": box_id,
            "car_count": len(members),
            "min": min(scores),
            "max": max(scores),
            "spread": spread,
            "median": statistics.median(scores),
            "cars": sorted(
                ({"name": c["name"], "trans": c["scores"]["trans"]} for c in members),
                key=lambda x: x["trans"],
            ),
        }
        (findings if spread > max_spread else clean).append(entry)
    findings.sort(key=lambda e: -e["spread"])
    return findings, clean


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-spread", type=int, default=DEFAULT_MAX_SPREAD)
    ap.add_argument("--json", action="store_true")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="tutarsızlık bulunursa çıkış kodunu düşür",
    )
    args = ap.parse_args()

    cars = load_cars()
    groups = group_by_transmission(cars)
    findings, clean = analyse(groups, args.max_spread)

    unlinked = [c["name"] for c in cars if not c["specs"].get("transmission_id")]

    if args.json:
        print(json.dumps(
            {"findings": findings, "clean": clean, "unlinked": unlinked},
            ensure_ascii=False, indent=2,
        ))
        return 1 if (args.strict and findings) else 0

    print("Şanzıman puanı tutarlılığı\n" + "=" * 60)
    print(
        f"{len(cars)} aracın {len(cars) - len(unlinked)} tanesi bir kutu kaydına bağlı. "
        f"Birden fazla araç paylaşan {len(findings) + len(clean)} kutu var.\n"
    )

    if findings:
        print(f"Yayılımı {args.max_spread} puanı aşan kutular:\n")
        for f in findings:
            print(f"  {f['transmission_id']}  —  {f['car_count']} araç, "
                  f"yayılım {f['spread']} puan ({f['min']}-{f['max']})")
            for c in f["cars"]:
                print(f"      {c['trans']:>3}  {c['name']}")
            print()
    else:
        print(f"Yayılımı {args.max_spread} puanı aşan kutu yok.\n")

    if clean:
        print(f"Eşiğin altında kalan {len(clean)} kutu:")
        for c in clean:
            print(f"  {c['transmission_id']:26} {c['car_count']} araç, yayılım {c['spread']}")
        print()

    if unlinked:
        print(f"Henüz bir kutu kaydına bağlanmamış {len(unlinked)} araç var; "
              "bunlar bu denetimin dışında kalıyor.")

    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
