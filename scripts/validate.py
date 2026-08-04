#!/usr/bin/env python3
"""validate.py — veri bütünlüğü ve kanıt politikası denetimi.

İki tür bulgu üretir:

  HATA  — veri bozuk, sayfa üretilse bile yanlış olur. Çıkış kodu 1.
  UYARI — veri geçerli ama metodoloji açısından eksik. Örnek olarak, dört kaynağa
          ulaşmadığı için henüz doğrulanmış sayılamayan araçlar, hiçbir araca
          bağlı olmayan kaynaklar ve tek başına çok fazla aracı taşıyan kaynaklar
          bu gruba girer. Uyarılar varsayılanda çıkış kodunu düşürmez, --strict
          verildiğinde düşürür.

Bu ayrım bilinçli yapıldı. Bugünkü veri yüzlerce uyarı üretiyor ve bu uyarıların
her biri Faz 2'nin iş listesindeki bir maddeye karşılık geliyor. Hepsini hata
saymak, denetimi ilk günden işlevsiz hale getirirdi.

Kullanım:
    python3 scripts/validate.py
    python3 scripts/validate.py --strict     # uyarılar da başarısız sayılsın
    python3 scripts/validate.py --json       # makine okunur çıktı
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

FUEL = {"Dizel", "Benzin"}
DRIVETRAIN = {"Önden", "Arkadan", "Dört çeker"}
TRANSMISSION = {"TK", "Islak DCT", "Kuru DCT", "CVT", "Robot"}
VERIFICATION = {"verified", "partial", "preliminary"}

# Politika eşikleri. Bunlar keyfi sayılar değil, gerekçeleri docs/ARCHITECTURE.md
# içindeki MK-04 kaydında ve docs/methodology.md içinde yazılı.
MIN_SOURCES_FOR_VERIFIED = 4  # "doğrulanmış" demek için dört bağımsız kaynak gerekiyor
MIN_SOURCES_FOR_PARTIAL = 1   # en az bir kaynağı olan araç "kısmi kaynak" sayılır
MAX_CARS_PER_SOURCE = 12      # tek kaynağın taşıyabileceği azami araç sayısı


def derive_verification(source_count: int) -> str:
    """Doğrulama etiketi elle verilmez, kaynak sayısından hesaplanır.

    Etiketi sayıdan türetmek, iyimser işaretlemeyi imkânsız kılıyor. Önceki
    düzende etiket elle veriliyordu ve 70 araç "kaynaklı" görünürken bunların
    38'i tek bir kaynağa dayanıyordu.
    """
    if source_count >= MIN_SOURCES_FOR_VERIFIED:
        return "verified"
    if source_count >= MIN_SOURCES_FOR_PARTIAL:
        return "partial"
    return "preliminary"


class Report:
    def __init__(self) -> None:
        self.errors: list[dict] = []
        self.warnings: list[dict] = []

    def error(self, where: str, rule: str, msg: str) -> None:
        self.errors.append({"where": where, "rule": rule, "message": msg})

    def warn(self, where: str, rule: str, msg: str) -> None:
        self.warnings.append({"where": where, "rule": rule, "message": msg})


def load() -> tuple[dict, list[tuple[pathlib.Path, dict]], dict, dict]:
    criteria = json.loads((DATA / "criteria.json").read_text(encoding="utf-8"))
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    transmissions = {
        k: v
        for k, v in json.loads((DATA / "transmissions.json").read_text(encoding="utf-8")).items()
        if not k.startswith("_")
    }
    cars = [
        (p, json.loads(p.read_text(encoding="utf-8")))
        for p in sorted((DATA / "cars").glob("*.json"))
    ]
    return criteria, cars, sources, transmissions


def check_car_shape(
    rep: Report, path: pathlib.Path, car: dict, scored: list[str], transmissions: dict
) -> None:
    where = path.name
    required = [
        "id", "name", "tag", "brand_group", "years", "specs",
        "price_band_k_try", "verification", "scores", "sources", "note",
    ]
    for field in required:
        if field not in car:
            rep.error(where, "eksik-alan", f"`{field}` alanı yok")
    if any(f not in car for f in required):
        return

    if car["id"] != path.stem:
        rep.error(where, "id-dosya-adi", f"id `{car['id']}` dosya adıyla eşleşmiyor")

    s = car["specs"]
    for field, allowed in (("fuel", FUEL), ("drivetrain", DRIVETRAIN), ("transmission_type", TRANSMISSION)):
        if s.get(field) not in allowed:
            rep.error(where, "gecersiz-deger", f"specs.{field} = {s.get(field)!r}, izinli: {sorted(allowed)}")

    # Beygir ve model yılı için alt sınır denetimi bilinçli olarak kaldırıldı.
    # Kapsam sınırları artık veriden değil arayüzdeki filtrelerden geliyor;
    # gerekçesi docs/ARCHITECTURE.md içindeki MK-03 kaydında.
    if not isinstance(s.get("hp"), int) or s["hp"] <= 0:
        rep.error(where, "gecersiz-deger", f"specs.hp = {s.get('hp')!r}")

    if not isinstance(s.get("displacement_l"), (int, float)) or not (0.5 < s["displacement_l"] < 8):
        rep.error(where, "gecersiz-deger", f"specs.displacement_l = {s.get('displacement_l')!r}")

    if s.get("body_type") is None:
        rep.warn(where, "govde-tipi-yok", "body_type alanı boş; gövde filtresi bu araçta çalışmayacak")

    box_id = s.get("transmission_id")
    if box_id is None:
        rep.warn(
            where, "kutu-kaydi-yok",
            "transmission_id boş; bu araç şanzıman tutarlılık denetiminin dışında kalıyor",
        )
    elif box_id not in transmissions:
        rep.error(
            where, "kayip-kutu-kaydi",
            f"`{box_id}` data/transmissions.json içinde yok",
        )
    elif transmissions[box_id]["type"] != s["transmission_type"]:
        rep.error(
            where, "kutu-tipi-celiski",
            f"araç `{s['transmission_type']}` diyor ama `{box_id}` kaydı "
            f"`{transmissions[box_id]['type']}` diyor",
        )

    if not re.fullmatch(r"\d{4}-\d{4}", car["years"]):
        rep.error(where, "yil-formati", f"years = {car['years']!r}, `YYYY-YYYY` bekleniyor")
    else:
        lo, hi = (int(x) for x in car["years"].split("-"))
        if lo > hi:
            rep.error(where, "yil-araligi", f"years = {car['years']}, başlangıç bitişten büyük")

    p = car["price_band_k_try"]
    if not (isinstance(p, list) and len(p) == 2 and all(isinstance(x, (int, float)) for x in p)):
        rep.error(where, "fiyat-bandi", f"price_band_k_try = {p!r}, [alt, üst] bekleniyor")
    elif p[0] >= p[1]:
        rep.error(where, "fiyat-bandi", f"alt sınır {p[0]} üst sınır {p[1]}'den küçük olmalı")
    elif p[1] / p[0] > 2.2:
        rep.warn(where, "fiyat-bandi", f"band çok geniş ({p[0]}-{p[1]}), fiyat puanını anlamsızlaştırır")

    if car["verification"] not in VERIFICATION:
        rep.error(where, "gecersiz-deger", f"verification = {car['verification']!r}")

    scores = car["scores"]
    missing = set(scored) - set(scores)
    extra = set(scores) - set(scored)
    if missing:
        rep.error(where, "puan-eksik", f"puanı olmayan kriter: {sorted(missing)}")
    if extra:
        rep.error(where, "puan-fazla", f"tanımsız kriter puanı: {sorted(extra)}")
    for k, v in scores.items():
        if not isinstance(v, int) or not (0 <= v <= 100):
            rep.error(where, "puan-araligi", f"scores.{k} = {v!r}, 0-100 arası tam sayı olmalı")

    if not isinstance(car["note"], str) or len(car["note"]) < 40:
        rep.warn(where, "gerekce-kisa", "note alanı gerekçe olarak fazla kısa")


def check_evidence_policy(
    rep: Report, path: pathlib.Path, car: dict, criteria: dict, sources: dict
) -> None:
    """Puanın kanıtla ilişkisini denetler — projenin asıl derdi bu."""
    where = path.name
    n_src = len(car.get("sources", []))
    crit_by_key = {c["key"]: c for c in criteria["criteria"]}

    # Doğrulama etiketi türetilmiş bir değerdir; elle değiştirilmiş olması veri
    # hatasıdır, tercih değil.
    expected = derive_verification(n_src)
    if car["verification"] != expected:
        rep.error(
            where, "etiket-turetilmedi",
            f"verification = {car['verification']!r} ama {n_src} kaynak için "
            f"{expected!r} olmalı; etiket kaynak sayısından hesaplanır",
        )

    if car["verification"] == "partial":
        rep.warn(
            where, "kaynak-yetersiz",
            f"{n_src} kaynağa dayanıyor; 'doğrulanmış' olması için "
            f"{MIN_SOURCES_FOR_VERIFIED - n_src} kaynak daha gerekiyor",
        )
    elif car["verification"] == "preliminary":
        rep.warn(where, "kaynaksiz", "hiç kaynağa bağlı değil, puanlar ön değerlendirme")

    thr = criteria["weak_threshold"]
    weak = [k for k, v in car["scores"].items() if v < thr]
    if weak and n_src == 0:
        rep.warn(
            where, "kanitsiz-zayif-halka",
            f"{sorted(weak)} kriterlerinde {thr} altı puan var ama hiç kaynak yok; "
            "bir aracı eleyen puan kanıtsız verilmemeli",
        )

    # Bir puan yalnızca C seviyesindeki kaynaklara dayanıyorsa uç bantlara çıkamaz.
    # Gerekçesi docs/PLAN.md M-2: uç puan iddialıdır, iddialı puan A veya B kanıt
    # ister. Tier'i olmayan (henüz atanmamış) kaynak bu kural için C sayılır, yani
    # temkinli tarafta hata yapılır. "Uç bant" artık keyfi bir sayı değil, kriterin
    # kendi en üst ve en alt bandının sınırından okunuyor (bkz. §7 puan bantları).
    car_sources = car.get("sources", [])
    if car_sources:
        tiers = {sources[sid]["tier"] for sid in car_sources if sid in sources}
        only_c = tiers and tiers <= {"C", None}
        if only_c:
            extreme = []
            for k, v in car["scores"].items():
                bands = crit_by_key[k]["bands"]
                if bands and (v >= bands[0]["range"][0] or v <= bands[-1]["range"][1]):
                    extreme.append(k)
            if extreme:
                rep.warn(
                    where, "c-kaynakla-uc-puan",
                    f"{sorted(extreme)} kriterlerinde en üst veya en alt bant puanı var "
                    "ama bütün kaynaklar C seviyesinde; uç puan A veya B kanıt ister",
                )

    # tag metni ile şanzıman tipinin çelişmesi — göç sırasında bulunan hata türü
    tag = car["tag"].lower()
    tx = car["specs"]["transmission_type"]
    if "kuru" in tag and tx not in ("Kuru DCT", "Robot"):
        rep.warn(where, "tag-tx-celiski", f"tag 'kuru' diyor ama transmission_type = {tx}")
    if "ıslak" in tag and tx != "Islak DCT":
        rep.warn(where, "tag-tx-celiski", f"tag 'ıslak' diyor ama transmission_type = {tx}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="uyarılar da başarısızlık sayılsın")
    ap.add_argument("--json", action="store_true", help="JSON çıktı ver")
    args = ap.parse_args()

    criteria, cars, sources, transmissions = load()
    rep = Report()
    scored = criteria["scored_order"]

    # --- araç bazlı ---
    seen_ids: Counter[str] = Counter()
    seen_names: Counter[str] = Counter()
    for path, car in cars:
        check_car_shape(rep, path, car, scored, transmissions)
        if "id" in car:
            seen_ids[car["id"]] += 1
        if "name" in car:
            seen_names[car["name"]] += 1
        if all(f in car for f in ("scores", "sources", "verification", "tag", "specs")):
            check_evidence_policy(rep, path, car, criteria, sources)
        for sid in car.get("sources", []):
            if sid not in sources:
                rep.error(path.name, "kayip-kaynak", f"`{sid}` data/sources.json içinde yok")

    for cid, n in seen_ids.items():
        if n > 1:
            rep.error("data/cars", "yinelenen-id", f"`{cid}` {n} kez geçiyor")
    for name, n in seen_names.items():
        if n > 1:
            rep.warn("data/cars", "yinelenen-ad", f"`{name}` {n} araçta aynı; ayırt edilemez")

    # --- kaynak bazlı ---
    # Bir kaynak doğrudan bir araca değil, bir şanzıman kutusu kaydına da bağlı
    # olabilir (ör. kutunun tork sınırını gösteren bir üretici belgesi). İkisi de
    # geçerli bağlanma yollarıdır; yalnızca araç kullanımına bakmak gerçek referansı
    # yetim gibi raporlardı.
    usage: Counter[str] = Counter()
    for _, car in cars:
        usage.update(car.get("sources", []))
    for box in transmissions.values():
        usage.update(box.get("sources", []))
        for issue in box.get("known_issues", []):
            usage.update(issue.get("sources", []))

    # Yoğunlaşma riski, bir kaynağın toplam kaç yerde geçtiği değil, kaç aracın
    # BAŞKA HİÇBİR KAYNAĞI OLMADAN tek başına bu kaynağa dayandığıdır. Bir kaynak
    # elli aracın notunda geçebilir ve zararsız olabilir, eğer o elli aracın hepsinin
    # ikinci bağımsız bir kaynağı da varsa. Asıl risk şu: kaynak çürürse veya
    # yanlış çıkarsa, hangi araçlar tamamen dayanaksız kalır?
    sole_reliance: Counter[str] = Counter()
    for _, car in cars:
        car_sources = car.get("sources", [])
        if len(car_sources) == 1:
            sole_reliance[car_sources[0]] += 1

    for sid, src in sources.items():
        for field in ("claim", "publisher", "url"):
            if not src.get(field):
                rep.error("sources.json", "eksik-alan", f"`{sid}`.{field} boş")
        if not str(src.get("url", "")).startswith("http"):
            rep.error("sources.json", "gecersiz-url", f"`{sid}` URL'i http ile başlamıyor")
        if usage[sid] == 0:
            rep.warn("sources.json", "yetim-kaynak", f"`{sid}` hiçbir araca bağlı değil")
        elif sole_reliance[sid] > MAX_CARS_PER_SOURCE:
            rep.warn(
                "sources.json", "kaynak-yogunlasmasi",
                f"`{sid}` {sole_reliance[sid]} aracın TEK kaynağı "
                f"(sınır {MAX_CARS_PER_SOURCE}); bu kaynak çürürse o araçlar "
                "tamamen dayanaksız kalır",
            )
        if src.get("tier") is None:
            rep.warn("sources.json", "guven-seviyesi-yok", f"`{sid}` için tier atanmamış")

    # --- kutu.base_score + düzeltme formülünün fiilen uygulanması ---
    # docs/PLAN.md §3.2: trans = kutu.base_score + düzeltme, düzeltme yalnızca iki
    # adı konmuş türden (tork yakınlığı, bakım geçmişi) biriyse ve car.evidence.trans
    # içinde gerekçesi yazılıysa uygulanabilir. Kayıtlı bir gerekçe olmadan büyük bir
    # sapma, tam olarak projenin başlangıç teşhisindeki hatanın kendisidir.
    TRANS_DEVIATION_LIMIT = 15
    for path, car in cars:
        box_id = car.get("specs", {}).get("transmission_id")
        if not box_id or box_id not in transmissions:
            continue
        base = transmissions[box_id].get("base_score")
        if base is None:
            continue
        actual = car.get("scores", {}).get("trans")
        if actual is None:
            continue
        delta = actual - base
        has_reasoning = bool(
            car.get("evidence", {}).get("trans", {}).get("reasoning")
        )
        if abs(delta) > TRANS_DEVIATION_LIMIT and not has_reasoning:
            rep.warn(
                path.name, "duzeltme-gerekcesiz",
                f"trans = {actual}, ama `{box_id}` kutusunun base_score'u {base} "
                f"({delta:+d} fark); evidence.trans.reasoning boş, bu sapma "
                "kayıtlı bir gerekçeye bağlı değil",
            )

    # --- şanzıman kayıtları ---
    box_usage: Counter[str] = Counter()
    for _, car in cars:
        bid = car.get("specs", {}).get("transmission_id")
        if bid:
            box_usage[bid] += 1

    for bid, box in transmissions.items():
        if box.get("base_score") is None:
            rep.warn(
                "transmissions.json", "kutu-temel-puani-yok",
                f"`{bid}` için base_score atanmamış; puan hâlâ araç bazında veriliyor",
            )
        if not box.get("sources"):
            rep.warn("transmissions.json", "kutu-kaynaksiz", f"`{bid}` hiç kaynağa dayanmıyor")
        for sid in box.get("sources", []):
            if sid not in sources:
                rep.error(
                    "transmissions.json", "kayip-kaynak",
                    f"`{bid}` kaydındaki `{sid}` data/sources.json içinde yok",
                )
        if box_usage[bid] == 0:
            rep.warn("transmissions.json", "yetim-kutu", f"`{bid}` hiçbir araca bağlı değil")

    # --- ağırlık setleri ---
    for name, preset in criteria["presets"].items():
        missing = set(criteria["full_order"]) - set(preset)
        if missing:
            rep.error("criteria.json", "eksik-agirlik", f"`{name}` setinde {sorted(missing)} yok")
        total = sum(preset.values())
        if total != 100:
            rep.warn("criteria.json", "agirlik-toplami", f"`{name}` seti toplamı {total}, 100 değil")

    for c in criteria["criteria"]:
        if not c.get("auto") and c.get("bands") is None:
            rep.warn("criteria.json", "puan-bandi-yok", f"`{c['key']}` için puan bandı tanımlanmamış")

    # --- özet ---
    verif = Counter(car["verification"] for _, car in cars if "verification" in car)
    summary = {
        "arac": len(cars),
        "kaynak": len(sources),
        "dogrulanmis": verif["verified"],
        "kismi_kaynak": verif["partial"],
        "on_degerlendirme": verif["preliminary"],
        "arac_basina_ortalama_kaynak": round(
            sum(len(c.get("sources", [])) for _, c in cars) / max(len(cars), 1), 2
        ),
        "yetim_kaynak": sum(1 for sid in sources if usage[sid] == 0),
        "hata": len(rep.errors),
        "uyari": len(rep.warnings),
    }

    if args.json:
        print(json.dumps(
            {"summary": summary, "errors": rep.errors, "warnings": rep.warnings},
            ensure_ascii=False, indent=2,
        ))
    else:
        for e in rep.errors:
            print(f"HATA  [{e['rule']}] {e['where']}: {e['message']}")
        by_rule = Counter(w["rule"] for w in rep.warnings)
        for w in rep.warnings:
            print(f"UYARI [{w['rule']}] {w['where']}: {w['message']}")
        print("\n--- özet ---")
        for k, v in summary.items():
            print(f"{k:32} {v}")
        if by_rule:
            print("\nuyarılar kural bazında:")
            for rule, n in by_rule.most_common():
                print(f"  {rule:28} {n}")

    if rep.errors:
        return 1
    if args.strict and rep.warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
