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
import datetime
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

# Bir fiyat bandının kaç ay sonra "bayat" sayılacağı. Altı ay keyfi değil,
# docs/PLAN.md §3.8'in kendi ifadesinden geliyor: "Fiyatlar Türkiye enflasyonunda
# altı ayda anlamsızlaşıyor; tarihsiz fiyat yanıltıcıdır." 2026-08 ölçümünde tarihli
# 19 bandın eski tahminlerden medyan %8 yukarıda çıkması bunun ölçülmüş kanıtı.
PRICE_STALE_MONTHS = 6
# Bayatlama hesabının çapası. Bugünün tarihi yerine sabit bir gün kullanılıyor,
# çünkü denetimin çıktısı takvimin ilerlemesiyle kendiliğinden değişmemeli;
# yeni ölçüm alındığında bu tarih de elle ileri taşınır.
REFERENCE_DATE = datetime.date(2026, 8, 13)


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


def load() -> tuple[dict, list[tuple[pathlib.Path, dict]], dict, dict, dict]:
    criteria = json.loads((DATA / "criteria.json").read_text(encoding="utf-8"))
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))

    def dimension(name: str) -> dict:
        """Boyut kaydı dosyalarını okur; `_` ile başlayan açıklama anahtarlarını atar."""
        return {
            k: v
            for k, v in json.loads((DATA / name).read_text(encoding="utf-8")).items()
            if not k.startswith("_")
        }

    transmissions = dimension("transmissions.json")
    engines = dimension("engines.json")
    cars = [
        (p, json.loads(p.read_text(encoding="utf-8")))
        for p in sorted((DATA / "cars").glob("*.json"))
    ]
    return criteria, cars, sources, transmissions, engines


def check_car_shape(
    rep: Report, path: pathlib.Path, car: dict, scored: list[str],
    transmissions: dict, engines: dict,
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

    # Motor ekseni, şanzıman ekseniyle birebir aynı deseni izliyor: araç aileye
    # kimlikle bağlanıyor, aile kaydı bir kez değerlendiriliyor. Yakıt ve hacim
    # çelişkisi, yanlış aileye bağlanmış bir aracı yakalamanın en pratik yolu.
    eng_id = s.get("engine_id")
    if eng_id is None:
        rep.warn(
            where, "motor-kaydi-yok",
            "engine_id boş; bu araç motor tutarlılık denetiminin dışında kalıyor",
        )
    elif eng_id not in engines:
        rep.error(
            where, "kayip-motor-kaydi",
            f"`{eng_id}` data/engines.json içinde yok",
        )
    else:
        eng = engines[eng_id]
        if eng["fuel"] != s["fuel"]:
            rep.error(
                where, "motor-yakit-celiski",
                f"araç `{s['fuel']}` diyor ama `{eng_id}` kaydı `{eng['fuel']}` diyor",
            )
        if s["displacement_l"] not in eng["displacements_l"]:
            rep.error(
                where, "motor-hacim-celiski",
                f"araç {s['displacement_l']} L diyor ama `{eng_id}` kaydı yalnızca "
                f"{eng['displacements_l']} hacimlerini tanıyor",
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
    # Kural kriter bazında bakıyor: bir kriterin kendi evidence bloğunda kaynak
    # varsa o kriterin seviyesi oradan okunuyor, yoksa aracın genel kaynak listesine
    # düşülüyor. Bu ayrım gerekliydi, çünkü bir kriter araç seviyesinde hiç kaynağı
    # olmayan bir referansa dayanabiliyor: `age` puanı TÜV'ün yaş-kusur eğrisinden
    # (A seviyesi) hesaplanıyor ama bu kaynak bilinçli olarak car["sources"]
    # listesine yazılmıyor, çünkü orası "doğrulanmış" rozetini besleyen araca özgü
    # kaynakları sayıyor (bkz. scripts/compute_age.py içindeki not ve MK-04).
    car_sources = car.get("sources", [])
    evidence = car.get("evidence") or {}

    def tiers_of(sids):
        return {sources[sid]["tier"] for sid in sids if sid in sources}

    extreme = []
    for k, v in car["scores"].items():
        bands = crit_by_key[k]["bands"]
        if not bands:
            continue
        if not (v >= bands[0]["range"][0] or v <= bands[-1]["range"][1]):
            continue
        crit_sources = (evidence.get(k) or {}).get("sources") or car_sources
        if not crit_sources:
            continue
        t = tiers_of(crit_sources)
        if t and t <= {"C", None}:
            extreme.append(k)
    if extreme:
        rep.warn(
            where, "c-kaynakla-uc-puan",
            f"{sorted(extreme)} kriterlerinde en üst veya en alt bant puanı var "
            "ama o kriteri destekleyen bütün kaynaklar C seviyesinde; uç puan A veya B kanıt ister",
        )

    # tag metni ile şanzıman tipinin çelişmesi — göç sırasında bulunan hata türü
    tag = car["tag"].lower()
    tx = car["specs"]["transmission_type"]
    if "kuru" in tag and tx not in ("Kuru DCT", "Robot"):
        rep.warn(where, "tag-tx-celiski", f"tag 'kuru' diyor ama transmission_type = {tx}")
    if "ıslak" in tag and tx != "Islak DCT":
        rep.warn(where, "tag-tx-celiski", f"tag 'ıslak' diyor ama transmission_type = {tx}")

    # docs/PLAN.md §3.8: fiyat bandı tarihsizse doğrulanamaz, eskiyen bant ise
    # yanıltıcıdır. Türkiye enflasyonunda bir fiyat altı ayda anlamını yitiriyor;
    # 2026-08 ölçümü tarihli 19 bandın eski tahminlerden medyan %8 yukarıda çıkması
    # bunun ölçülmüş kanıtı. Bu yüzden iki ayrı uyarı üretiliyor: bandın hiç tarihi
    # yoksa "tahmin" olduğu, tarihi varsa da eskidiği görünür olmalı.
    pref = car.get("price_reference") or {}
    as_of = pref.get("as_of")
    if not as_of:
        rep.warn(where, "fiyat-tarihsiz",
                 "price_band_k_try tarihsiz bir tahmin; price_reference bloğu boş, "
                 "bandın hangi tarihte ve hangi yöntemle ölçüldüğü doğrulanamıyor")
    else:
        try:
            months = (REFERENCE_DATE - datetime.date.fromisoformat(as_of)).days / 30.44
        except ValueError:
            rep.error(where, "fiyat-tarihi-bozuk", f"price_reference.as_of okunamadı: {as_of}")
            months = 0
        if months > PRICE_STALE_MONTHS:
            rep.warn(where, "fiyat-bandi-bayat",
                     f"fiyat bandı {as_of} tarihli, yaklaşık {months:.0f} aylık "
                     f"(sınır {PRICE_STALE_MONTHS} ay); yeniden ölçülmeli")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="uyarılar da başarısızlık sayılsın")
    ap.add_argument("--json", action="store_true", help="JSON çıktı ver")
    args = ap.parse_args()

    criteria, cars, sources, transmissions, engines = load()
    rep = Report()
    scored = criteria["scored_order"]

    # --- araç bazlı ---
    seen_ids: Counter[str] = Counter()
    seen_names: Counter[str] = Counter()
    for path, car in cars:
        check_car_shape(rep, path, car, scored, transmissions, engines)
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
        # Kriter bazlı kanıt bloğunda anılan kaynaklar da kullanımdır. Araç
        # seviyesinde listelenmeyen ama bir kriteri fiilen destekleyen bir kaynak
        # (ör. `age`'i besleyen TÜV eğrisi) bu sayılmazsa yetim görünürdü.
        for block in (car.get("evidence") or {}).values():
            usage.update((block or {}).get("sources") or [])
        # Fiyat bandının kaynağı da kullanımdır. Bu kaynak bilinçli olarak
        # car["sources"] listesine yazılmıyor (bkz. scripts/import_price_snapshot.py
        # içindeki not ve MK-19): o liste güvenilirlik kanıtı sayıyor, bir ilan
        # fiyatı gözlemi ise aracın motoru ya da şanzımanı hakkında hiçbir şey
        # söylemiyor. Burada sayılmazsa gerçek ve kullanılan bir kaynak yetim görünürdü.
        pref = car.get("price_reference") or {}
        if pref.get("source"):
            usage.update([pref["source"]])
    for box in transmissions.values():
        usage.update(box.get("sources", []))
        for issue in box.get("known_issues", []):
            usage.update(issue.get("sources", []))
    for eng in engines.values():
        usage.update(eng.get("sources", []))
        for issue in eng.get("known_issues", []):
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

    # Aynı gerekçe motor ekseni için de geçerli: motor puanı, bağlı olduğu ailenin
    # base_score'undan büyük ölçüde sapıyorsa bu sapmanın evidence.motor.reasoning
    # içinde yazılı bir gerekçesi olmalıdır. Motor ailelerine base_score atanana
    # kadar bu denetim sessizdir.
    for path, car in cars:
        eng_id = car.get("specs", {}).get("engine_id")
        if not eng_id or eng_id not in engines:
            continue
        base = engines[eng_id].get("base_score")
        if base is None:
            continue
        actual = car.get("scores", {}).get("motor")
        if actual is None:
            continue
        delta = actual - base
        has_reasoning = bool(car.get("evidence", {}).get("motor", {}).get("reasoning"))
        if abs(delta) > TRANS_DEVIATION_LIMIT and not has_reasoning:
            rep.warn(
                path.name, "motor-duzeltme-gerekcesiz",
                f"motor = {actual}, ama `{eng_id}` ailesinin base_score'u {base} "
                f"({delta:+d} fark); evidence.motor.reasoning boş, bu sapma "
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

    # --- motor kayıtları ---
    # Şanzıman kutularıyla aynı denetim seti. Tek fark: kaynaksızlık yalnızca
    # base_score atanmış motorlarda uyarı üretiyor. Henüz araştırılmamış bir
    # motorun hem puanı hem kaynağı yoktur; bunu iki ayrı uyarıyla bildirmek
    # aynı boşluğu iki kez saymak olurdu. Asıl kural şudur: puan verilmişse
    # arkasında kaynak olmak zorundadır.
    engine_usage: Counter[str] = Counter()
    for _, car in cars:
        eid = car.get("specs", {}).get("engine_id")
        if eid:
            engine_usage[eid] += 1

    for eid, eng in engines.items():
        if eng.get("base_score") is None:
            rep.warn(
                "engines.json", "motor-temel-puani-yok",
                f"`{eid}` için base_score atanmamış; puan hâlâ araç bazında veriliyor",
            )
        elif not eng.get("sources"):
            rep.warn(
                "engines.json", "motor-kaynaksiz",
                f"`{eid}` base_score taşıyor ama hiç kaynağa dayanmıyor",
            )
        for sid in eng.get("sources", []):
            if sid not in sources:
                rep.error(
                    "engines.json", "kayip-kaynak",
                    f"`{eid}` kaydındaki `{sid}` data/sources.json içinde yok",
                )
        if engine_usage[eid] == 0:
            rep.warn("engines.json", "yetim-motor", f"`{eid}` hiçbir araca bağlı değil")

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
        if not c.get("weight_rationale"):
            rep.warn(
                "criteria.json", "agirlik-gerekcesi-yok",
                f"`{c['key']}` için weight_rationale tanımlanmamış; arayüzde ağırlık "
                "kutusunun yanında gösterilecek gerekçe metni eksik kalır",
            )
        for b in c.get("bands") or []:
            ex = b.get("example")
            if ex and ex not in seen_ids:
                rep.error(
                    "criteria.json", "gecersiz-bant-ornegi",
                    f"`{c['key']}` bandındaki example `{ex}` data/cars içinde yok; "
                    "arayüz bu bandı gösterirken kırılır",
                )

    # --- fizik denetimi: beygir/tork/hacim birbirini tutuyor mu ---
    # Bir motorun gücü, torku ve hacmi bağımsız sayılar değil; aralarındaki oran
    # yakıt türüne göre dar bir bantta kalıyor. 1.875 kayıt ölçüldüğünde hp/Nm oranı
    # benzinde 0,54-0,89 (medyan 0,73), dizelde 0,38-0,52 (medyan 0,44) çıktı — iki
    # bant neredeyse hiç örtüşmüyor, çünkü dizel düşük devirde tork üretir.
    #
    # Bu denetim iki gerçek hatayı yakaladı: Peugeot 301 1.6 HDi'nin teknik değerleri
    # yanlışlıkla benzinli PureTech varyantından alınmıştı (115 bg / 150 Nm, hp/Nm
    # 0,77 — dizel için imkânsız), Suzuki SX4 1.6'nın torku 320 Nm yazılmıştı (hp/Nm
    # 0,38 — benzinli için imkânsız). İkisi de düzeltildi. Eşikler ölçülen p1/p99
    # sınırlarının dışına konuldu ki yalnız gerçek hatalar uyarı üretsin.
    HP_NM_LIMITS = {"Benzin": (0.48, 1.25), "Dizel": (0.28, 0.62)}
    for path, car in cars:
        sp = car.get("specs") or {}
        hp, nm, lit = sp.get("hp"), sp.get("torque_nm"), sp.get("displacement_l")
        fuel = sp.get("fuel")
        if not (hp and nm and fuel in HP_NM_LIMITS):
            continue
        lo, hi = HP_NM_LIMITS[fuel]
        ratio = hp / nm
        if not (lo <= ratio <= hi):
            rep.error(
                path.name, "fizik-disi-oran",
                f"{fuel.lower()} motorda hp/Nm = {ratio:.2f} ({hp} bg / {nm:.0f} Nm); "
                f"beklenen aralık {lo}-{hi}. Beygir, tork ya da yakıt alanından biri "
                "yanlış varyanttan gelmiş olabilir",
            )
        if lit:
            nm_per_l = nm / lit
            if fuel == "Dizel" and nm_per_l < 95:
                rep.warn(path.name, "fizik-dusuk-tork",
                         f"dizel motorda {nm_per_l:.0f} Nm/L çok düşük; tork ya da "
                         "hacim alanı şüpheli")
            elif nm_per_l > 260:
                rep.warn(path.name, "fizik-yuksek-tork",
                         f"{nm_per_l:.0f} Nm/L olağandışı yüksek; tork ya da hacim "
                         "alanı şüpheli")

    # --- katalog katmanı (MK-22) ---
    # Katalog olgusal bir katmandır ve puan taşımaz. Buradaki denetimin tek işi, o
    # sınırın korunduğunu ve kayıtların şekil olarak sağlam olduğunu doğrulamak.
    # Katalog kaydı `verification` üretmez, ortalama kaynak sayısına da karışmaz.
    catalog_dir = ROOT / "data" / "catalog"
    catalog_entries: list[dict] = []
    catalog_ids: set[str] = set()
    scored_ids = {car["id"] for _, car in cars if "id" in car}
    for path in sorted(catalog_dir.glob("*.json")):
        if path.name == "_sources.json":
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            rep.error(f"catalog/{path.name}", "bozuk-json", str(exc))
            continue
        for entry in payload.get("entries", []):
            catalog_entries.append(entry)
            where = f"catalog/{path.name}"
            eid = entry.get("id")
            if not eid:
                rep.error(where, "katalog-kimliksiz", "katalog kaydında id yok")
                continue
            if eid in catalog_ids:
                rep.error(where, "katalog-kimlik-cakismasi",
                          f"`{eid}` katalogda birden çok kez geçiyor")
            catalog_ids.add(eid)
            # Sınırın kendisi: katalog kaydı puan taşıyamaz.
            for forbidden in ("scores", "evidence", "verification"):
                if forbidden in entry:
                    rep.error(where, "katalogda-puan",
                              f"`{eid}` kaydında `{forbidden}` var; katalog katmanı "
                              "yargı değil olgu taşır (MK-22)")
            ref = entry.get("scored_car_id")
            if ref and ref not in scored_ids:
                rep.error(where, "katalog-kirik-bag",
                          f"`{eid}` -> scored_car_id `{ref}` data/cars içinde yok")
            for ref in entry.get("possible_scored_car_ids") or []:
                if ref not in scored_ids:
                    rep.error(where, "katalog-kirik-bag",
                              f"`{eid}` -> aday `{ref}` data/cars içinde yok")

    catalog_only = sum(
        1 for e in catalog_entries
        if not e.get("scored_car_id") and not e.get("possible_scored_car_ids")
    )

    # --- özet ---
    verif = Counter(car["verification"] for _, car in cars if "verification" in car)
    summary = {
        "arac": len(cars),
        "katalog_kaydi": len(catalog_entries),
        "yalniz_katalogda": catalog_only,
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
