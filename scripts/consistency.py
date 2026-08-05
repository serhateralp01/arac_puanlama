#!/usr/bin/env python3
"""consistency.py — aynı donanımı paylaşan araçlar arasındaki puan tutarlılığı.

Bu betiğin varlık sebebi şudur: puanlar araç seviyesinde veriliyor, ama kanıtın çoğu
bileşen seviyesinde bulunuyor. Aynı şanzıman kutusu veya aynı motor ailesi her araçta
yeniden ve elden değerlendirilince, aynı donanım farklı puanlar almaya başlıyor ve bu
farkın gerekçesi hiçbir yerde yazılı olmuyor.

Betik iki ekseni birden ölçer: aynı `transmission_id` değerini paylaşan araçların
`trans` puanlarını ve aynı `engine_id` değerini paylaşan araçların `motor` puanlarını.
Yayılımı eşiği aşan gruplar raporlanır.

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

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Aynı donanımı paylaşan araçlar arasında gerekçesiz kabul edilebilecek azami puan
# farkı. Sıfır seçilmedi, çünkü aynı kutunun farklı tork seviyelerinde çalışması ya da
# aynı motor ailesinin farklı güç seviyelerinde kullanılması gerçek bir fark
# yaratabiliyor. On beş puanın üstü ise açıklama gerektirir.
DEFAULT_MAX_SPREAD = 15

# İncelenen iki eksen. Her biri: araçtaki bağlantı alanı, puan anahtarı, başlık.
AXES = [
    ("transmission_id", "trans", "Şanzıman puanı tutarlılığı", "kutu"),
    ("engine_id", "motor", "Motor puanı tutarlılığı", "motor ailesi"),
]


def load_cars() -> list[dict]:
    return [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((DATA / "cars").glob("*.json"))
    ]


def group_by(cars: list[dict], link_field: str) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for car in cars:
        key = car["specs"].get(link_field)
        if key:
            groups.setdefault(key, []).append(car)
    return groups


def analyse(
    groups: dict[str, list[dict]], score_key: str, max_spread: int
) -> tuple[list[dict], list[dict]]:
    findings, clean = [], []
    for group_id, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        scores = [c["scores"][score_key] for c in members]
        spread = max(scores) - min(scores)
        entry = {
            "id": group_id,
            "car_count": len(members),
            "min": min(scores),
            "max": max(scores),
            "spread": spread,
            "median": statistics.median(scores),
            "cars": sorted(
                ({"name": c["name"], "score": c["scores"][score_key]} for c in members),
                key=lambda x: x["score"],
            ),
        }
        (findings if spread > max_spread else clean).append(entry)
    findings.sort(key=lambda e: -e["spread"])
    return findings, clean


def report_axis(
    cars: list[dict], link_field: str, score_key: str, title: str,
    unit: str, max_spread: int,
) -> list[dict]:
    groups = group_by(cars, link_field)
    findings, clean = analyse(groups, score_key, max_spread)
    unlinked = [c["name"] for c in cars if not c["specs"].get(link_field)]

    print(title + "\n" + "=" * 60)
    print(
        f"{len(cars)} aracın {len(cars) - len(unlinked)} tanesi bir {unit} kaydına "
        f"bağlı. Birden fazla araç paylaşan {len(findings) + len(clean)} {unit} var.\n"
    )

    if findings:
        print(f"Yayılımı {max_spread} puanı aşan {unit} kayıtları:\n")
        for f in findings:
            print(f"  {f['id']}  —  {f['car_count']} araç, "
                  f"yayılım {f['spread']} puan ({f['min']}-{f['max']})")
            for c in f["cars"]:
                print(f"      {c['score']:>3}  {c['name']}")
            print()
    else:
        print(f"Yayılımı {max_spread} puanı aşan {unit} yok.\n")

    if clean:
        print(f"Eşiğin altında kalan {len(clean)} {unit}:")
        for c in clean:
            print(f"  {c['id']:26} {c['car_count']} araç, yayılım {c['spread']}")
        print()

    if unlinked:
        print(f"Henüz bir {unit} kaydına bağlanmamış {len(unlinked)} araç var; "
              "bunlar bu denetimin dışında kalıyor.\n")

    return findings


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

    if args.json:
        payload = {}
        for link_field, score_key, _title, _unit in AXES:
            findings, clean = analyse(
                group_by(cars, link_field), score_key, args.max_spread
            )
            payload[score_key] = {
                "findings": findings,
                "clean": clean,
                "unlinked": [
                    c["name"] for c in cars if not c["specs"].get(link_field)
                ],
            }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        any_finding = any(payload[k]["findings"] for k in payload)
        return 1 if (args.strict and any_finding) else 0

    all_findings = []
    for i, (link_field, score_key, title, unit) in enumerate(AXES):
        if i:
            print()
        all_findings += report_axis(
            cars, link_field, score_key, title, unit, args.max_spread
        )

    return 1 if (args.strict and all_findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
