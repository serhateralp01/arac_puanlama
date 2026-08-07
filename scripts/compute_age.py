#!/usr/bin/env python3
"""compute_age.py — `age` kriterini TÜV kusur oranı eğrisinden hesaplar.

`docs/ARCHITECTURE.md` MK-06 kaydı "age formüle bağlanır" diyordu ve
`docs/PLAN.md` §3.1 taslak olarak doğrusal bir formül öneriyordu
(`100 − 3.2 × yaş`). Bu betik o kararı fiilen uyguluyor, ama taslak formülü
değil: doğrusal form 228 araca karşı test edildiğinde ortalama 8, en kötü
durumda 31 puan sapma verdi, çünkü gerçek yaş-kusur ilişkisi doğrusal değil,
yaşla birlikte hızlanan bir eğri.

Eğri artık TÜV'ün gerçek muayene verisine dayanıyor (yaklaşık 9,5 milyon
Hauptuntersuchung, "erhebliche Mängel" yani aracı muayeneden ilk seferde
geçirmeyen ciddi kusur oranı). Bu, metodolojimizin A seviyesi (sayısal,
kurumsal, örneklem tabanlı) kanıt tanımına giren tek kaynak türü.

Kullanım:
    python3 scripts/compute_age.py            # sapmaları raporla, dosyaya yazma
    python3 scripts/compute_age.py --write    # data/cars/*.json içine yaz
"""
from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REFERENCE_YEAR = 2026

# TÜV Report 2025 / 2026 ve TÜV NORD 2026'nın yayınladığı yaş bandı → ciddi
# kusur oranı tablosu. (yaş bandının ortası, kusur yüzdesi)
TUV_POINTS = [
    (2.5, 6.45),
    (4.5, 9.10),
    (6.5, 13.60),
    (8.5, 17.90),
    (10.5, 22.95),
    (12.5, 28.05),
    (20.5, 40.30),
]

# Yukarıdaki noktalara ikinci dereceden en küçük kareler uydurması (R² = 0.994).
# Katsayılar burada sabit yazılı, çünkü betiğin numpy gibi bir bağımlılığa
# ihtiyaç duymaması gerekiyor; türetme yöntemi ve ham noktalar yukarıda duruyor,
# yani sayılar istendiğinde yeniden üretilebilir.
QUAD_A, QUAD_B, QUAD_C = -0.02186, 2.46488, -0.71484

# Eğri 22 yaş civarında tepe yapıp aşağı dönüyor; bu matematiksel bir yan etki,
# gerçek bir bulgu değil (25 yaşındaki bir araç 22 yaşındakinden daha az kusurlu
# değildir). Bu yüzden yaş girdisi 22'de sabitleniyor.
AGE_CAP = 22.0

# Kusur oranını puana çeviren doğrusal eşleme. Çapalar doğrudan TÜV'ün kendi
# uç bantlarından alındı: en genç band (%6,45 kusur) 90 puan, en yaşlı band
# (%40,3 kusur) 20 puan. Taban 10, çünkü sıfır puan "bu araç hurdadır" demek
# olurdu ve TÜV verisi bunu söylemiyor.
ANCHOR_LOW_DEFECT, ANCHOR_LOW_SCORE = 6.45, 90.0
ANCHOR_HIGH_DEFECT, ANCHOR_HIGH_SCORE = 40.30, 20.0
SCORE_FLOOR = 10


def defect_rate(age_years: float) -> float:
    """Bir yaş değerinin TÜV eğrisine göre beklenen ciddi kusur oranı (%)."""
    a = min(age_years, AGE_CAP)
    return QUAD_A * a * a + QUAD_B * a + QUAD_C


def age_score(mid_year: float, reference_year: int = REFERENCE_YEAR) -> int:
    """Model yılı ortasından `age` puanı üretir."""
    d = defect_rate(reference_year - mid_year)
    slope = (ANCHOR_HIGH_SCORE - ANCHOR_LOW_SCORE) / (ANCHOR_HIGH_DEFECT - ANCHOR_LOW_DEFECT)
    raw = ANCHOR_LOW_SCORE + slope * (d - ANCHOR_LOW_DEFECT)
    return max(SCORE_FLOOR, min(100, round(raw)))


def mid_year_of(car: dict) -> float:
    start, end = car["years"].split("-")
    return (int(start) + int(end)) / 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="hesabı araç dosyalarına yaz")
    args = ap.parse_args()

    paths = sorted((DATA / "cars").glob("*.json"))
    rows = []
    for path in paths:
        car = json.loads(path.read_text(encoding="utf-8"))
        mid = mid_year_of(car)
        new = age_score(mid)
        rows.append((path, car, car["scores"]["age"], new))

    deltas = [new - old for _, _, old, new in rows]
    mean_abs = sum(abs(d) for d in deltas) / len(deltas)
    print(f"{len(rows)} araç değerlendirildi.")
    print(f"ortalama mutlak sapma: {mean_abs:.1f} puan")
    print(f"en büyük aşağı/yukarı sapma: {min(deltas)} / {max(deltas)}")

    if not args.write:
        print("\n(yazmadan çalıştırıldı; uygulamak için --write ver)")
        print("en büyük 10 sapma:")
        for path, car, old, new in sorted(rows, key=lambda r: -abs(r[3] - r[2]))[:10]:
            print(f"  {car['id']:44s} {old:3d} → {new:3d} ({new - old:+d})")
        return 0

    for path, car, old, new in rows:
        car["scores"]["age"] = new
        evidence = car.get("evidence") or {}
        evidence["age"] = {
            "band": "TÜV yaş-kusur eğrisinden hesaplandı",
            "confidence": "yüksek",
            "sources": ["tuv_report_yas_kusur_egrisi"],
            "reasoning": (
                f"Bu aracın model yılı ortalaması {mid_year_of(car):.1f}, yani "
                f"{REFERENCE_YEAR} itibarıyla yaşı yaklaşık "
                f"{REFERENCE_YEAR - mid_year_of(car):.1f} yıl. TÜV'ün yaklaşık 9,5 milyon "
                f"muayeneye dayanan yaş-kusur eğrisine göre bu yaştaki bir araçta ciddi "
                f"kusur bulunma olasılığı yüzde {defect_rate(REFERENCE_YEAR - mid_year_of(car)):.1f}. "
                f"Bu oran, TÜV'ün kendi uç bantları çapa alınarak (yüzde 6,45 kusur = 90 puan, "
                f"yüzde 40,3 kusur = 20 puan) {new} puana çevrildi. Puan elle verilmedi; "
                f"scripts/compute_age.py tarafından hesaplandı ve aynı girdi her zaman aynı "
                f"çıktıyı üretir."
            ),
            "assessed_at": "2026-08-07",
        }
        car["evidence"] = evidence
        # TÜV kaynağı bilinçli olarak car["sources"] listesine EKLENMİYOR. O liste,
        # "doğrulanmış" rozetini besleyen bağımsız araç kaynaklarını sayıyor (MK-04);
        # TÜV eğrisi ise bütün araçlara aynı şekilde uygulanan genel bir referans,
        # araca özgü bir kanıt değil. Listeye eklenseydi 228 aracın tamamının kaynak
        # sayısı bir anda birer artar ve rozet, D-02'de tam olarak kapatılan iyimser
        # etiketleme hatasını tekrar üretirdi. Kaynak yalnızca evidence.age içinde
        # anılıyor; oradan da sayfada görünüyor.
        path.write_text(json.dumps(car, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{len(rows)} araç kaydına yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
