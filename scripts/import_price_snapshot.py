#!/usr/bin/env python3
"""import_price_snapshot.py — tarihli piyasa gözlemlerini araç fiyat bantlarına yazar.

`docs/PLAN.md` §3.8 fiyat kriteri için tek bir eksik tanımlıyordu: formül zaten
belirlenimci, ama **girdinin nereden geldiği** yazılı değil. Bantlar tarihsiz ve
yöntemsizdi. Türkiye enflasyonunda altı ayda anlamsızlaşan bir sayı, hangi tarihte
ve hangi örneklemle ölçüldüğü kayıtlı değilse doğrulanamaz; bu yüzden PLAN.md o
bantlara `as_of` ve `method` alanı eklenmesini istiyordu. Bu betik o kararı uyguluyor.

Girdi `data/market/price-snapshots-YYYY-MM.json`: bir ilan platformundan belirli bir
tarihte alınan **toplu** fiyat istatistikleri. Dosyada tekil ilan yok — ilan
bağlantısı, satıcı bilgisi ve fotoğraf bilinçli olarak depoya alınmadı; yalnızca
grup düzeyinde çeyreklik, örneklem sayısı ve yöntem saklanıyor. Gerekçesi
`docs/ARCHITECTURE.md` MK-19'da: bir platformun sürekli yeniden üretilebilen ilan
havuzunu kopyalamak ile o havuzdan türetilmiş bir istatistiği kaynak göstererek
kullanmak aynı şey değil, ve bu proje yalnızca ikincisini yapıyor.

**Bandın anlamı.** `price_band_k_try` artık "tahmini fiyat aralığı" değil, o grupta
gözlenen istenen fiyatların **orta yarısı** (P25-P75), bin TL'ye yuvarlanmış hali.
Bu, uç ilanları (hasarlı ucuzlar, hayalci pahalılar) bandın dışında bırakıyor.

**İstenen fiyat, satış fiyatı değildir.** Pazarlık payı ve satılamayıp ilanda
birikenler yüzünden istenen fiyat gerçekleşen fiyatın üzerindedir. Aradaki fark bu
veriyle ölçülemediği için bant düzeltilmeden yazılıyor; sınırlılık her araç kaydında
`price_reference.price_semantics` alanında açıkça duruyor.

Kullanım:
    python3 scripts/import_price_snapshot.py            # sapmaları raporla, yazma
    python3 scripts/import_price_snapshot.py --write    # data/cars/*.json içine yaz
"""
from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MARKET_DIR = DATA / "market"

# Bir grubun araç bandına yazılabilmesi için gereken en az temiz gözlem sayısı.
# Beşin altındaki örneklemde çeyreklikler tek bir ilanın oynamasıyla savruluyor;
# o gruplar piyasa dosyasında kalır ama araç kaydına işlenmez.
MIN_OBSERVATIONS = 5

# Yalnız bu durumdaki gruplar araç bandına yazılır. `thin_sample` ve `insufficient`
# gruplar dosyada durur, çünkü ileride yeni gözlemle güçlenebilirler.
WRITABLE_STATUS = {"usable_single_market"}


def latest_snapshot() -> pathlib.Path:
    files = sorted(MARKET_DIR.glob("price-snapshots-*.json"))
    if not files:
        raise SystemExit("data/market/ içinde price-snapshots-*.json bulunamadı")
    return files[-1]


def to_k_try(value: float) -> int:
    """TL'yi bin TL'ye yuvarlar; arayüz ve fiyat kriteri bin TL ile çalışıyor."""
    return int(round(value / 1000))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="hesabı araç dosyalarına yaz")
    args = ap.parse_args()

    snap = json.loads(latest_snapshot().read_text(encoding="utf-8"))
    as_of = snap["as_of"]
    source_id = snap["source_id"]

    rows = []
    skipped_thin = 0
    for g in snap["groups"]:
        car_id = g.get("matched_car_id")
        if not car_id:
            continue
        if g["status"] not in WRITABLE_STATUS or g["observations_band"] < MIN_OBSERVATIONS:
            skipped_thin += 1
            continue
        path = DATA / "cars" / f"{car_id}.json"
        if not path.exists():
            continue
        car = json.loads(path.read_text(encoding="utf-8"))
        old = list(car["price_band_k_try"])
        new = [to_k_try(g["price_p25_try"]), to_k_try(g["price_p75_try"])]
        rows.append((path, car, old, new, g))

    print(f"{latest_snapshot().name}: {len(snap['groups'])} grup okundu.")
    print(f"{len(rows)} araç bandı güncellenecek, {skipped_thin} grup ince örneklem/durum nedeniyle atlandı.")

    if rows:
        drifts = [((n[0] + n[1]) / 2 - (o[0] + o[1]) / 2) / ((o[0] + o[1]) / 2) * 100
                  for _, _, o, n, _ in rows]
        drifts.sort()
        mid = drifts[len(drifts) // 2]
        print(f"eski tahmin ile piyasa arasındaki medyan sapma: {mid:+.1f}% "
              f"(piyasa yukarıda olan: {sum(1 for d in drifts if d > 0)}/{len(drifts)})")

    if not args.write:
        print("\n(yazmadan çalıştırıldı; uygulamak için --write ver)")
        for path, car, old, new, g in sorted(rows, key=lambda r: r[1]["id"]):
            print(f"  {car['id']:34s} {str(old):>14s} -> {str(new):>14s}  (n={g['observations_band']})")
        return 0

    for path, car, old, new, g in rows:
        car["price_band_k_try"] = new
        car["price_reference"] = {
            "as_of": as_of,
            "method": snap["method"],
            "source": source_id,
            "marketplace": snap["marketplace"],
            "price_semantics": snap["price_semantics"],
            "group_id": g["group_id"],
            "observations": g["observations_band"],
            "window_days": g["window_days"],
            "p25_try": g["price_p25_try"],
            "median_try": g["price_median_try"],
            "p75_try": g["price_p75_try"],
            "km_median": g.get("km_median"),
            "quality": g["quality"],
        }
        # Piyasa kaynağı bilinçli olarak car["sources"] listesine EKLENMİYOR; kaynak
        # yalnızca price_reference.source içinde anılıyor. Gerekçe MK-14'ün TÜV kararıyla
        # birebir aynı: o liste "doğrulanmış" rozetini besleyen, aracın GÜVENİLİRLİĞİNE
        # dair bağımsız kaynakları sayıyor (MK-04). Bir ilan fiyatı gözlemi aracın motoru,
        # şanzımanı veya yaşı hakkında hiçbir şey söylemez; listeye eklenseydi fiyatı
        # ölçülen her aracın kaynak sayısı bir anda artar ve D-02'de kapatılan iyimser
        # etiketleme hatası fiyat üzerinden geri gelirdi.
        car.pop("_price_source_placeholder", None)
        path.write_text(json.dumps(car, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{len(rows)} araç kaydına tarihli fiyat bandı yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
