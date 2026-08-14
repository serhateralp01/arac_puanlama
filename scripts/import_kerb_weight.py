#!/usr/bin/env python3
"""import_kerb_weight.py — doldurulmuş çalışma listesinden boş ağırlık verisini işler.

**Neden ayrı bir betik.** `scripts/compute_fun.py` bir aracın sürüş keyfi puanını
hesaplamak için hem torka hem boş ağırlığa ihtiyaç duyuyor. 2026-08-13'te tork verisi
251/278 araca çıktı, ama ağırlık 163'te kaldı; yani **88 araçta tek eksik bu alan** ve
o alan dolduğunda `fun` kapsamı 163'ten 251'e çıkıyor. Deponun hiçbir iş kaleminin
getiri/çaba oranı buna yakın değil.

Veri elle toplanıyor çünkü tek bir toplu kaynağı yok: P2.1 veri paketinde boş ağırlık
alanı hiç bulunmuyor. `data/queue/kerb-weight-worklist.json` doldurulacak listeyi
tutuyor; bu betik onu okuyup araç kayıtlarına işliyor.

**MK-15 koruması burada zorunlu tutuluyor.** Betik hiçbir değeri körü körüne yazmıyor:

- Kaynak adresi olmayan satır reddedilir. Kaynaksız bir sayı, kaynaksız bir puandan
  daha tehlikelidir çünkü olgu gibi görünür.
- Listedeki beygir ve hacim, araç kaydındakiyle eşleşmezse satır reddedilir. Bu, aynı
  modelin farklı varyantını yanlışlıkla eşlemeye karşı MK-08'in istediği koruma.
- Sınır dışı bir ağırlık (600 kg altı, 3.000 kg üstü) reddedilir. Bu eşik, bir varyantı
  elemek için değil, birim hatasını (libre/kilogram karışması) yakalamak için var.

Kullanım:
    python3 scripts/import_kerb_weight.py            # ne yazılacağını raporla
    python3 scripts/import_kerb_weight.py --write    # data/cars/*.json içine yaz
"""
from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
WORKLIST = DATA / "queue" / "kerb-weight-worklist.json"

# Birim hatası yakalama aralığı. Bir binek otomobil bu sınırların dışına çıkmaz;
# 1.500 kg'lık bir aracın libre değeri (3.300) üst sınırı aşar ve yakalanır.
MIN_KG, MAX_KG = 600, 3000


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="araç dosyalarına yaz")
    args = ap.parse_args()

    if not WORKLIST.exists():
        raise SystemExit(f"{WORKLIST.relative_to(ROOT)} bulunamadı.")
    doc = json.loads(WORKLIST.read_text(encoding="utf-8"))

    ready, rejected, empty = [], [], 0
    for row in doc["vehicles"]:
        kg = row.get("kerb_weight_kg")
        if kg in (None, ""):
            empty += 1
            continue
        path = DATA / "cars" / f"{row['car_id']}.json"
        if not path.exists():
            rejected.append((row["car_id"], "araç kaydı yok"))
            continue
        car = json.loads(path.read_text(encoding="utf-8"))
        s = car["specs"]
        if not row.get("source_url"):
            rejected.append((row["car_id"], "kaynak adresi boş"))
            continue
        if not isinstance(kg, (int, float)) or not (MIN_KG <= kg <= MAX_KG):
            rejected.append((row["car_id"], f"ağırlık {kg} makul aralıkta değil"))
            continue
        if int(row.get("hp", -1)) != int(s["hp"]):
            rejected.append((row["car_id"], f"beygir uyuşmuyor ({row.get('hp')} ≠ {s['hp']})"))
            continue
        if abs(float(row.get("displacement_l", -1)) - float(s["displacement_l"])) > 0.06:
            rejected.append((row["car_id"],
                             f"hacim uyuşmuyor ({row.get('displacement_l')} ≠ {s['displacement_l']})"))
            continue
        if s.get("kerb_weight_kg"):
            rejected.append((row["car_id"], "kayıtta zaten ağırlık var"))
            continue
        ready.append((path, car, int(round(kg)), row))

    print(f"{WORKLIST.name}: {len(doc['vehicles'])} satır okundu.")
    print(f"  yazmaya hazır : {len(ready)}")
    print(f"  henüz boş     : {empty}")
    print(f"  reddedilen    : {len(rejected)}")
    for cid, why in rejected:
        print(f"      {cid:36s} {why}")

    if not args.write:
        if ready:
            print("\n(yazmadan çalıştırıldı; uygulamak için --write ver)")
            for _, car, kg, _ in ready[:20]:
                print(f"      {car['id']:36s} {kg} kg")
        return 0

    for path, car, kg, row in ready:
        car["specs"]["kerb_weight_kg"] = kg
        prov = car.setdefault("provenance", {})
        existing = prov.get("specs_source", "")
        prov["specs_source"] = (existing + " " if existing else "") + (
            f"Boş ağırlık ({kg} kg) {row['source_url']} adresinden alındı; eşleme MK-15 kuralına "
            f"göre beygir ({car['specs']['hp']} bg) ve motor hacmi "
            f"({car['specs']['displacement_l']} L) birlikte doğrulanarak yapıldı."
        ).strip()
        path.write_text(json.dumps(car, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{len(ready)} araç kaydına boş ağırlık yazıldı.")
    if ready:
        print("Sırada: `python3 scripts/compute_fun.py --write` ile fun puanlarını yenileyin.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
