#!/usr/bin/env python3
"""sensitivity.py — puanlama modelinin duyarlılık ve tutarlılık analizi.

Bu betik bir doğrulama aracı değil, bir **ölçüm** aracı. `validate.py` verinin
kurallara uyup uymadığını sorar; bu betik modelin kendisinin sağlam olup olmadığını
sorar: ağırlıklar değişince sıralama ne kadar değişiyor, hangi kriter sonucu fiilen
belirliyor, iki kriter aynı şeyi mi ölçüyor.

Çıktısı `docs/PUANLAMA-TEMELI.md` içindeki sayıların kaynağıdır; belge güncellenirken
bu betik yeniden çalıştırılıp sayılar tazelenmelidir.

Kullanım:
    python3 scripts/analysis/sensitivity.py
    python3 scripts/analysis/sensitivity.py --json    # makine okunur çıktı
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"


def load():
    criteria = json.loads((DATA / "criteria.json").read_text(encoding="utf-8"))
    cars = [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((DATA / "cars").glob("*.json"))
    ]
    return criteria, cars


def price_scores(cars):
    """Fiyat puanı saklanmaz, listeye göre hesaplanır — arayüzdeki formülün aynısı."""
    mids = [(c["price_band_k_try"][0] + c["price_band_k_try"][1]) / 2 for c in cars]
    lo, hi = min(mids), max(mids)
    if hi == lo:
        return [50.0] * len(cars)
    return [100 * (hi - m) / (hi - lo) for m in mids]


def totals(cars, weights, order, price):
    """Ağırlıklı ortalama — arayüzdeki total() fonksiyonunun aynısı."""
    sw = sum(weights.get(k, 0) for k in order)
    if sw <= 0:
        return [0.0] * len(cars)
    out = []
    for i, c in enumerate(cars):
        s = 0.0
        for k in order:
            v = price[i] if k == "price" else c["scores"][k]
            s += v * weights.get(k, 0)
        out.append(s / sw)
    return out


def ranks(values):
    """Büyükten küçüğe sıra numaraları (1 = en yüksek). Eşitlikte ortalama sıra."""
    idx = sorted(range(len(values)), key=lambda i: -values[i])
    r = [0.0] * len(values)
    i = 0
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and values[idx[j + 1]] == values[idx[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[idx[k]] = avg
        i = j + 1
    return r


def spearman(a, b):
    """Sıra korelasyonu. 1.0 = sıralama birebir aynı, 0 = ilişkisiz."""
    ra, rb = ranks(a), ranks(b)
    n = len(ra)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    da = math.sqrt(sum((ra[i] - ma) ** 2 for i in range(n)))
    db = math.sqrt(sum((rb[i] - mb) ** 2 for i in range(n)))
    return num / (da * db) if da and db else 0.0


def pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    da = math.sqrt(sum((a[i] - ma) ** 2 for i in range(n)))
    db = math.sqrt(sum((b[i] - mb) ** 2 for i in range(n)))
    return num / (da * db) if da and db else 0.0


def top_n_overlap(a, b, n):
    """İki sıralamanın ilk n'inde kaç araç ortak."""
    sa = {i for i in sorted(range(len(a)), key=lambda i: -a[i])[:n]}
    sb = {i for i in sorted(range(len(b)), key=lambda i: -b[i])[:n]}
    return len(sa & sb)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="makine okunur çıktı")
    args = ap.parse_args()

    criteria, cars = load()
    order = criteria["full_order"]
    scored = criteria["scored_order"]
    presets = criteria["presets"]
    labels = criteria["preset_labels"]
    price = price_scores(cars)
    n = len(cars)

    report: dict = {"arac_sayisi": n}

    # ---------- 1) Hazır ayar setleri arasında sıralama ne kadar değişiyor ----------
    base = totals(cars, presets["custom"], order, price)
    preset_cmp = {}
    for name, w in presets.items():
        if name == "custom":
            continue
        t = totals(cars, w, order, price)
        preset_cmp[name] = {
            "etiket": labels.get(name, name),
            "spearman": round(spearman(base, t), 4),
            "ilk10_ortak": top_n_overlap(base, t, 10),
            "ilk20_ortak": top_n_overlap(base, t, 20),
        }
    report["hazir_ayar_karsilastirmasi"] = preset_cmp

    # ---------- 2) Tek kriterin ağırlığı sıfırlanınca ne oluyor ----------
    # "Bu kriter sonucu gerçekten belirliyor mu" sorusunun ölçümü.
    drop = {}
    for k in order:
        w = dict(presets["custom"])
        w[k] = 0
        t = totals(cars, w, order, price)
        drop[k] = {
            "spearman": round(spearman(base, t), 4),
            "ilk10_ortak": top_n_overlap(base, t, 10),
        }
    report["kriter_cikarma_etkisi"] = drop

    # ---------- 3) Kriterler birbirini tekrar ediyor mu ----------
    # Yüksek korelasyon = iki kriter aynı şeyi ölçüyor olabilir (bağımsızlık ihlali).
    cols = {k: [c["scores"][k] for c in cars] for k in scored}
    cols["price"] = price
    pairs = []
    for a, b in itertools.combinations(order, 2):
        r = pearson(cols[a], cols[b])
        pairs.append({"cift": f"{a}~{b}", "pearson": round(r, 3)})
    pairs.sort(key=lambda x: -abs(x["pearson"]))
    report["kriter_korelasyonlari"] = pairs

    # ---------- 4) Rastgele ağırlık bozulmasına dayanıklılık ----------
    # Her ağırlığa ±%25 gürültü ekleyip sıralamanın ne kadar korunduğuna bakıyoruz.
    rnd = random.Random(20260806)  # sabit tohum: sonuç tekrarlanabilir olsun
    sp, ov10 = [], []
    for _ in range(500):
        w = {k: max(0.0, presets["custom"][k] * (1 + rnd.uniform(-0.25, 0.25))) for k in order}
        t = totals(cars, w, order, price)
        sp.append(spearman(base, t))
        ov10.append(top_n_overlap(base, t, 10))
    sp.sort()
    report["agirlik_gurultusu_25"] = {
        "deneme": len(sp),
        "spearman_ortalama": round(sum(sp) / len(sp), 4),
        "spearman_en_dusuk": round(sp[0], 4),
        "spearman_5inci_yuzdelik": round(sp[int(len(sp) * 0.05)], 4),
        "ilk10_ortalama_ortak": round(sum(ov10) / len(ov10), 2),
    }

    # ---------- 5) Puanların yayılımı ----------
    # Dar yayılım = kriter ayırt edici değil.
    spread = {}
    for k in order:
        v = cols[k]
        mean = sum(v) / n
        sd = math.sqrt(sum((x - mean) ** 2 for x in v) / n)
        spread[k] = {
            "en_dusuk": round(min(v), 1),
            "en_yuksek": round(max(v), 1),
            "ortalama": round(mean, 1),
            "std_sapma": round(sd, 1),
        }
    report["puan_yayilimi"] = spread

    # ---------- 6) Ham toplamın yayılımı (normalize sütununun gerekçesi) ----------
    mean_t = sum(base) / n
    sd_t = math.sqrt(sum((x - mean_t) ** 2 for x in base) / n)
    report["ham_toplam"] = {
        "en_dusuk": round(min(base), 1),
        "en_yuksek": round(max(base), 1),
        "ortalama": round(mean_t, 1),
        "std_sapma": round(sd_t, 1),
        "aralik": round(max(base) - min(base), 1),
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    # ---------- insan okunur çıktı ----------
    print(f"=== Puanlama modeli duyarlılık analizi ({n} araç) ===\n")

    print("1) Hazır ayar setleri sıralamayı ne kadar değiştiriyor")
    print("   (Spearman 1.0 = sıralama aynı; ilk10 = dengeli setin ilk 10'uyla ortak araç)")
    for name, d in preset_cmp.items():
        print(f"   {d['etiket']:28s} spearman={d['spearman']:.3f}  ilk10={d['ilk10_ortak']}/10  ilk20={d['ilk20_ortak']}/20")

    print("\n2) Bir kriterin ağırlığı sıfırlanınca sıralama ne kadar bozuluyor")
    print("   (düşük spearman = o kriter sonucu fiilen belirliyor)")
    for k, d in sorted(drop.items(), key=lambda x: x[1]["spearman"]):
        print(f"   {k:6s} kaldırılınca spearman={d['spearman']:.3f}  ilk10={d['ilk10_ortak']}/10")

    print("\n3) Kriterler arası korelasyon (yüksek = aynı şeyi ölçüyor olabilir)")
    for p in pairs[:8]:
        print(f"   {p['cift']:16s} r={p['pearson']:+.3f}")

    g = report["agirlik_gurultusu_25"]
    print(f"\n4) Ağırlıklara ±%25 rastgele gürültü ({g['deneme']} deneme)")
    print(f"   spearman ortalama={g['spearman_ortalama']:.4f}  en düşük={g['spearman_en_dusuk']:.4f}  %5'lik dilim={g['spearman_5inci_yuzdelik']:.4f}")
    print(f"   ilk 10'da ortalama {g['ilk10_ortalama_ortak']}/10 araç korunuyor")

    print("\n5) Kriter puanlarının yayılımı (dar yayılım = az ayırt edici)")
    for k, d in sorted(spread.items(), key=lambda x: x[1]["std_sapma"]):
        print(f"   {k:6s} min={d['en_dusuk']:5.1f} max={d['en_yuksek']:5.1f} ort={d['ortalama']:5.1f} sd={d['std_sapma']:4.1f}")

    h = report["ham_toplam"]
    print(f"\n6) Ham toplam puan: {h['en_dusuk']} – {h['en_yuksek']} (aralık {h['aralik']}, sd {h['std_sapma']})")
    print("   Normalize sütunun varlık sebebi bu dar aralık.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
