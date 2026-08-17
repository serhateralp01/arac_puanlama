#!/usr/bin/env python3
"""estimate_judgment_scores.py — comf/cost/liq için kardeş-araç kopyasını gerekçeli
bir tahminle değiştirir.

**Neden var.** `promote_catalog.py` (Y-19) katalogdan terfi eden araçlara `comf`,
`cost` ve `liq` puanını en yakın kardeş aracın değerinden **kopyalayarak** veriyordu.
Bu, aracın kendi özelliklerine (segment, gövde tipi, şanzıman yumuşaklığı) hiç
bakmıyordu — iki farklı hp sınıfındaki aynı markanın araçları aynı puanı alabiliyordu.
Kullanıcı bunu düzeltmemizi istedi.

**Yöntem: markanın kendi ortalamasından sapma.** Depodaki 278 orijinal (elle
değerlendirilmiş) aracın marka başına ortalama comf/cost/liq'u çıkarılıyor — bu,
"bu marka genelde nasıl değerlendiriliyor" sorusuna deponun kendi geçmiş kararlarından
gelen bir cevap, yeni bir varsayım değil. Sonra aracın kendi özellikleri (markanın
kendi ortalama beygirine göre üst/alt segment, gövde tipi, şanzıman tipi) bu
ortalamadan **sapma** olarak ekleniyor. "Mercedes markası genelde konfor puanı 72
alıyor, bu araç markanın ortalama gücünün üstünde olduğu ve TK şanzımanı olduğu için
+9" gibi bir gerekçe üretiyor — kardeş araç kopyalamaktan daha spesifik.

**Bu hâlâ kanıt değil, tahmin.** `comf`/`cost`/`liq` depoda hiçbir zaman kaynak
zinciriyle verilmiyor (`docs/ROADMAP.md`: "elle veriliyor"). Bu betik de elle veriyor,
ama artık kardeş araca değil, aracın kendi ölçülebilir özelliklerine dayanıyor ve
gerekçesi `note` alanında yazılı duruyor.

Kullanım:
    python3 scripts/estimate_judgment_scores.py            # rapor, dosya yazmaz
    python3 scripts/estimate_judgment_scores.py --write     # araç kayıtlarına işle
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARS = ROOT / "data" / "cars"

TRANS_COMF = {"TK": 3, "Islak DCT": 1, "Kuru DCT": -4, "Robot": -8, "CVT": -1}
TRANS_COST = {"TK": 2, "Islak DCT": -3, "Kuru DCT": -6, "Robot": -6, "CVT": -2}
TRANS_LIQ = {"TK": 0, "Islak DCT": 0, "Kuru DCT": -4, "Robot": -6, "CVT": 0}
TRANS_TR = {
    "TK": "tork konvertörü (yumuşak, olgun teknoloji)",
    "Islak DCT": "ıslak çift kavrama",
    "Kuru DCT": "kuru çift kavrama (bilinen düşük hız sarsıntısı riski)",
    "Robot": "robotlu yarı otomatik (en az yumuşak geçiş)",
    "CVT": "kademesiz (CVT)",
}
BODY_COMF = {"Station Wagon": 3, "Station": 3, "Sedan": 3, "SUV": 5, "SUV/MPV": 5,
             "MPV": 4, "Hatchback": 0, "Liftback": 1, "Sedan/Liftback": 2,
             "Coupe": -3, "Cabrio": -3, "Pick-up": 2}
BODY_LIQ = {"Sedan": 3, "Hatchback": 3, "SUV": 5, "SUV/MPV": 4, "MPV": 1,
            "Liftback": 2, "Sedan/Liftback": 3, "Station Wagon": -6, "Station": -6,
            "Coupe": -10, "Cabrio": -12, "Pick-up": -2}


def clip(v: float, lo: int = 15, hi: int = 95) -> int:
    return max(lo, min(hi, round(v)))


def load_cars() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CARS.glob("*.json"))]


def brand_baselines(original: list[dict]) -> dict[str, dict]:
    by_brand = collections.defaultdict(list)
    for c in original:
        by_brand[c["brand_group"]].append(c)
    out = {}
    for brand, cs in by_brand.items():
        n = len(cs)
        out[brand] = {
            "n": n,
            "comf": sum(c["scores"]["comf"] for c in cs) / n,
            "cost": sum(c["scores"]["cost"] for c in cs) / n,
            "liq": sum(c["scores"]["liq"] for c in cs) / n,
            "hp": sum(c["specs"]["hp"] for c in cs) / n,
        }
    return out


def segment_factor(hp: int, brand_avg_hp: float) -> tuple[float, str]:
    """Aracın markanın kendi ortalama gücüne göre üst/alt segmentte olup olmadığı."""
    ratio = hp / brand_avg_hp if brand_avg_hp else 1.0
    if ratio >= 1.5:
        return 1.5, "markanın ortalama gücünün belirgin üstünde (üst segment/performans eğilimi)"
    if ratio >= 1.15:
        return 1.0, "markanın ortalama gücünün üstünde"
    if ratio <= 0.65:
        return -1.0, "markanın ortalama gücünün belirgin altında (giriş segmenti)"
    if ratio <= 0.85:
        return -0.5, "markanın ortalama gücünün biraz altında"
    return 0.0, "markanın tipik güç aralığında"


def estimate(car: dict, baselines: dict) -> tuple[dict, str]:
    sp = car["specs"]
    brand = car["brand_group"]
    base = baselines.get(brand)
    if base is None:
        base = {"comf": 65, "cost": 65, "liq": 55, "hp": sp["hp"], "n": 0}

    seg_mult, seg_txt = segment_factor(sp["hp"], base["hp"])
    body = sp.get("body_type")
    tx = sp["transmission_type"]

    comf = base["comf"] + seg_mult * 6 + BODY_COMF.get(body, 0) + TRANS_COMF.get(tx, 0)
    cost = base["cost"] - seg_mult * 5 + TRANS_COST.get(tx, 0) + (3 if sp["fuel"] == "Dizel" else 0)
    liq_seg = -8 if seg_mult >= 1.5 else (-3 if seg_mult <= -1.0 else 0)
    liq = base["liq"] + BODY_LIQ.get(body, 0) + TRANS_LIQ.get(tx, 0) + liq_seg

    scores = {"comf": clip(comf), "cost": clip(cost), "liq": clip(liq, 15, 90)}

    parts = [
        f"{brand} markasının depodaki {base['n']} aracının ortalaması "
        f"(konfor {base['comf']:.0f}, maliyet {base['cost']:.0f}, likidite {base['liq']:.0f}) "
        f"çapa alındı." if base["n"] else f"{brand} için depoda başka araç olmadığından güvenli bir varsayılan kullanıldı."
    ]
    parts.append(f"Bu araç {seg_txt} ({sp['hp']} bg / marka ortalaması {base['hp']:.0f} bg).")
    if body:
        parts.append(f"Gövde tipi {body}.")
    parts.append(f"Şanzıman {TRANS_TR.get(tx, tx)}.")
    if sp["fuel"] == "Dizel":
        parts.append("Dizel motor, TR piyasasında genelde benzinliye göre işletme maliyetini hafif iyileştiriyor.")
    parts.append(
        "Bu üç kriter (konfor, maliyet, likidite) depoda hiçbir zaman kaynak zinciriyle "
        "verilmiyor; bu tahmin de öyle — ama artık kardeş araca değil, aracın kendi "
        "ölçülebilir özelliklerine (segment, gövde, şanzıman) dayanıyor."
    )
    reasoning = " ".join(parts)
    return scores, reasoning


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    all_cars = load_cars()
    original = [c for c in all_cars
                if "promote_catalog" not in c.get("provenance", {}).get("method", "")]
    promoted = [c for c in all_cars
                if "promote_catalog" in c.get("provenance", {}).get("method", "")]
    baselines = brand_baselines(original)

    print(f"orijinal araç: {len(original)} | terfi eden araç: {len(promoted)}")
    changed = 0
    for car in promoted:
        old = dict(car["scores"])
        scores, reasoning = estimate(car, baselines)
        car["scores"]["comf"] = scores["comf"]
        car["scores"]["cost"] = scores["cost"]
        car["scores"]["liq"] = scores["liq"]

        # note alanındaki "gerekçesizdir" uyarısını gerçek gerekçeyle değiştir.
        # promote_catalog.py'nin ürettiği not, MK-16 miras cümlesinden hemen sonra
        # "motor/şanzıman dışındaki kriterler ... araca özgü araştırılmadı" diyordu;
        # bu betik o cümleyi keser (miras cümlesi kalır) ve kendi gerekçesini ekler.
        note = car["note"]
        cut_marker = ", motor/şanzıman dışındaki kriterler"
        if cut_marker in note:
            head = note.split(cut_marker)[0].rstrip()
            if not head.endswith("."):
                head += "."
            car["note"] = (
                f"{head} Fiyat bandı hâlâ araca özgü araştırılmadı. {reasoning}"
            )
        changed += 1
        if args.write:
            path = CARS / f"{car['id']}.json"
            path.write_text(json.dumps(car, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"güncellenen: {changed}")
    if not args.write:
        print("(rapor kipi — dosya yazılmadı; işlemek için --write)")


if __name__ == "__main__":
    main()
