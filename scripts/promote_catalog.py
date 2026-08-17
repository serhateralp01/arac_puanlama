#!/usr/bin/env python3
"""promote_catalog.py — katalog kaydını puanlanmış katmana terfi ettirir (Y-19/MK-22).

**Neden var.** `data/catalog/` (MK-22) 1.641 olgusal kayıt taşıyor; bunların bir kısmı
**zaten depoda kayıtlı bir motor/şanzıman ailesine** güvenle bağlanabiliyor. Böyle bir
kayıt için motor ve şanzıman puanı sıfırdan araştırılmıyor — MK-16'nın mekanik miras
deseniyle ailenin `base_score`'u ve kaynakları doğrudan devralınıyor.

**Eşleştirme neden dikkatli.** İlk deneme yalnızca (marka, yakıt, hacim) ile eşleştirdi
ve **yanlış** sonuçlar üretti: aynı hacim sınıfını paylaşan farklı nesil/marka motorları
birbirine karıştı (BMW M54'ün hiç üretmediği 306 bg'lik bir "535i"ye bağlanması gibi),
ve şanzıman eşleşmesi marka gözetmeden yalnız tip+vites sayısına baktığı için ZF 8HP ile
PSA/Aisin EAT8'i karıştırdı. Bu betik üç korumayla çalışıyor:

  1. Motor eşleşmesi **marka bazlı** ve **güç aralığı doğrulamalı**: (marka, yakıt,
     hacim) tek bir aileye düşmeli VE beygir, o ailenin depodaki araçlarında görülen
     aralığın (%75-%135) dışına çıkmamalı.
  2. Şanzıman eşleşmesi **marka bazlı**: (marka, tip, vites, kavrama) tek bir aileye
     düşmeli. Marka olmadan yapılan bir eşleşme kabul edilmiyor.
  3. Aynı katalog adı farklı satırlarda farklı aileye düşüyorsa (P2.1'in kendi içinde
     tutarsız olduğunu gösterir) o isim grubunun TAMAMI atlanıyor.

**Puanların kaynağı farklı ağırlıkta.** `motor` ve `trans` puanları aile `base_score`'una
eşitleniyor ve `evidence` bloğu aile kaynaklarına dayanıyor — bu, depodaki 278 aracın
tamamında kullanılan aynı standart. `comf`, `cost` ve `liq` ise depoda **hiçbir zaman**
kanıt zinciriyle verilmiyor (`docs/ROADMAP.md`: "elle veriliyor"); bu betik onları en
yakın kardeş aracın (aynı marka + yakın gövde tipi + yakın yıl) değerlerinden **tahmin
ediyor** ve bunu `note` alanında açıkça yazıyor. Bu, uydurma değil — deponun zaten
kullandığı yöntemin (yakın segment karşılaştırması) otomatikleştirilmiş hali, ve
dürüstçe işaretleniyor.

`fun` puanı `kerb_weight_kg` gerektiriyor; P2.1 kataloğunda bu alan hiç yok, bu yüzden
terfi eden araçların `evidence.fun` alanı **boş bırakılıyor** — depodaki 115/278 aracın
zaten içinde bulunduğu, kabul edilmiş bir durum.

Kullanım:
    python3 scripts/promote_catalog.py               # aday listesini yazdır
    python3 scripts/promote_catalog.py --write        # data/cars/ içine yaz
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TODAY = "2026-08-17"


def norm(s) -> str:
    if not s:
        return ""
    s = str(s).lower()
    for a, b in [("ı", "i"), ("ş", "s"), ("ç", "c"), ("ğ", "g"), ("ü", "u"), ("ö", "o")]:
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def load_cars() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted((DATA / "cars").glob("*.json"))]


def load_catalog() -> list[dict]:
    out = []
    for path in sorted((DATA / "catalog").glob("*.json")):
        if path.name == "_sources.json":
            continue
        out.extend(json.loads(path.read_text(encoding="utf-8")).get("entries", []))
    return [e for e in out if not e.get("scored_car_id") and not e.get("possible_scored_car_ids")]


def find_candidates(cars: list[dict], catalog: list[dict]) -> list[tuple[dict, str, str]]:
    """Katalog kaydını mevcut motor/şanzıman ailesine bağlar.

    Marka eşleşmesi varsayılan kural: bir motor ya da kutu, farklı üreticilerin aynı
    tip+ölçüdeki tamamen farklı ürünlerini birbirine karıştırmasın diye (ZF 8HP ile
    PSA/Aisin EAT8'in karışması gibi). Ama bu kural bazı ailelerde fazla katı: VAG
    grubu (VW/Audi/Skoda/Seat/Cupra), PSA/Stellantis (Peugeot/Citroën/Opel) ve
    Hyundai-Kia gibi ortak platform kullanan gruplarda **aynı fiziksel parça** birden
    çok markada satılıyor — ve bu, spekülasyon değil, depodaki kendi verimizde zaten
    kanıtlı: `vag-dq200` bugün Volkswagen/Audi/Skoda/Seat'te, `psa-eat8` Peugeot/
    Citroën/Opel'de kayıtlı. Bir aile depoda zaten 2+ farklı markada görülüyorsa, o
    aile için marka sınırı kaldırılıyor — bu, yeni bir varsayım eklemiyor, sadece
    deponun kendi araştırmasının (Y-01/Y-02) zaten doğruladığı paylaşımı kullanıyor.
    """
    eng_gt = collections.defaultdict(lambda: collections.defaultdict(list))
    tr_gt = collections.defaultdict(collections.Counter)
    tr_gt_noclutch = collections.defaultdict(collections.Counter)
    eng_brands = collections.defaultdict(set)
    tr_brands = collections.defaultdict(set)
    for c in cars:
        sp = c["specs"]
        b = norm(c.get("brand_group"))
        if sp.get("engine_id"):
            key_e = (b, sp["fuel"], round(sp["displacement_l"], 1))
            eng_gt[key_e][sp["engine_id"]].append(sp["hp"])
            eng_brands[sp["engine_id"]].add(b)
        if sp.get("transmission_id"):
            key_t = (b, sp["transmission_type"], sp.get("gears"), sp.get("clutch"))
            tr_gt[key_t][sp["transmission_id"]] += 1
            tr_gt_noclutch[(b, sp["transmission_type"], sp.get("gears"))][sp["transmission_id"]] += 1
            tr_brands[sp["transmission_id"]].add(b)

    # Marka sınırı gevşetilmiş arama tabloları — ama yalnız (fuel, hacim) ile değil,
    # (fuel, hacim) + "bu aile depoda zaten hangi markalarda görülüyor" ile. Yani bir
    # aday, ancak markası o AİLENİN kendi bilinen marka kümesindeyse eşleşebiliyor.
    # İlk sürüm bu kümeyi kontrol etmiyordu ve "Honda Accord"u Audi'nin EA888
    # motoruna, "BMW 528i"yi VW'nin EA211'ine bağladı — yalnızca ikisi de depoda
    # birden çok markada görülen bir aile olduğu için. Düzeltme: aday markası
    # `eng_brands[eid]` / `tr_brands[tid]` kümesinde olmalı.
    eng_gt_shared = collections.defaultdict(lambda: collections.defaultdict(list))
    for c in cars:
        sp = c["specs"]
        eid = sp.get("engine_id")
        if eid and len(eng_brands[eid]) >= 2:
            key = (sp["fuel"], round(sp["displacement_l"], 1))
            eng_gt_shared[key][eid].append(sp["hp"])
    tr_gt_shared = collections.defaultdict(collections.Counter)
    tr_gt_shared_noclutch = collections.defaultdict(collections.Counter)
    for c in cars:
        sp = c["specs"]
        tid = sp.get("transmission_id")
        if tid and len(tr_brands[tid]) >= 2:
            key = (sp["transmission_type"], sp.get("gears"), sp.get("clutch"))
            tr_gt_shared[key][tid] += 1
            key2 = (sp["transmission_type"], sp.get("gears"))
            tr_gt_shared_noclutch[key2][tid] += 1

    def brand_filtered(matches: dict, brand_sets: dict, b: str) -> dict:
        return {k: v for k, v in matches.items() if b in brand_sets[k]}

    raw = []
    for e in catalog:
        if e["quality_flags"]:
            continue
        sp = e["specs"]
        if not sp.get("displacement_l"):
            continue
        b = norm(e["brand"])
        key_e = (b, sp["fuel"], round(sp["displacement_l"], 1))
        eng_matches = eng_gt.get(key_e, {})
        if len(eng_matches) != 1:
            shared = eng_gt_shared.get((sp["fuel"], round(sp["displacement_l"], 1)), {})
            eng_matches = brand_filtered(shared, eng_brands, b)
            if len(eng_matches) != 1:
                continue
        eng_id, hp_list = list(eng_matches.items())[0]
        lo, hi = min(hp_list) * 0.75, max(hp_list) * 1.35
        if not (lo <= sp["hp"] <= hi):
            continue

        key_t = (b, sp["transmission_type"], sp.get("gears"), sp.get("clutch"))
        tr_matches = tr_gt.get(key_t, {})
        if len(tr_matches) == 1:
            tr_id = list(tr_matches)[0]
        else:
            key_t2 = (b, sp["transmission_type"], sp.get("gears"))
            tr_matches2 = tr_gt_noclutch.get(key_t2, {})
            if len(tr_matches2) == 1:
                tr_id = list(tr_matches2)[0]
            else:
                key_shared = (sp["transmission_type"], sp.get("gears"), sp.get("clutch"))
                shared3 = brand_filtered(tr_gt_shared.get(key_shared, {}), tr_brands, b)
                if len(shared3) == 1:
                    tr_id = list(shared3)[0]
                else:
                    key_shared2 = (sp["transmission_type"], sp.get("gears"))
                    shared4 = brand_filtered(tr_gt_shared_noclutch.get(key_shared2, {}), tr_brands, b)
                    if len(shared4) != 1:
                        continue
                    tr_id = list(shared4)[0]
        raw.append((e, eng_id, tr_id))

    # Marka-paylaşımlı eşleşme, aynı markanın FARKLI nesil/platformlarını da aynı
    # aileye düşürebiliyor — bu, marka bazında değil model bazında yanlış olabilir.
    # "Fiat Bravo 1.6 MultiJet Dualogic" (2007-2014, Fiat'ın kendi C635 tabanlı
    # Dualogic'i kullanıyor) yalnızca Fiat Egea'nın (2015+, farklı platform)
    # psa-etg'ye bağlı olduğu bilindiği için o aileye düştü — bu iki model aynı
    # tedarikçiyi paylaştığını gösteren bağımsız bir kanıt yok. Araştırılmadan
    # terfi edilmemesi için elle çıkarıldı.
    raw = [(e, eid, tid) for e, eid, tid in raw if e["id"] != "fiat-bravo-1-6-multijet-dualogic-120"]

    # Aynı ad farklı satırlarda farklı aileye düşüyorsa tüm grup atlanır.
    by_name = collections.defaultdict(set)
    for e, eid, tid in raw:
        by_name[e["name"]].add((eid, tid))
    inconsistent = {n for n, s in by_name.items() if len(s) > 1}
    clean_matches = [(e, eid, tid) for e, eid, tid in raw if e["name"] not in inconsistent]

    # Kaynak veride aynı fiziksel aracın birden çok satırı var: aynı ad, aynı
    # beygir/tork/motor/kutu, ama farklı model-yılı gözlemi olarak ayrı satıra
    # yazılmış (2012, 2013, 2013-2017 gibi). Bunları ayrı araç yazmak "Seat Leon 1.2
    # TSI · 110 bg" adında üç kopya üretiyordu. Grup yıl aralıklarının BİRLEŞİMİ
    # alınıyor (en erken başlangıç, en geç bitiş) ve body_type dolu olan satır
    # tercih ediliyor.
    # Tork bazen aynı fiziksel motor için 1-2 Nm farkla iki ayrı satırda duruyor
    # (249 vs 250 gibi) — yuvarlanmadan gruplanırsa bu tek yüzde birlik fark iki
    # ayrı "araç" üretiyordu.
    def rounded_nm(nm):
        return round(nm / 5) * 5 if nm else nm

    groups: dict[tuple, list] = collections.defaultdict(list)
    for item in clean_matches:
        e, eid, tid = item
        sp = e["specs"]
        sig = (norm(e["name"]), sp["hp"], rounded_nm(sp.get("torque_nm")), eid, tid)
        groups[sig].append(item)

    merged = []
    for members in groups.values():
        e, eid, tid = max(
            members, key=lambda m: bool(m[0]["specs"].get("body_type"))
        )
        years = [m[0]["years"] for m in members]
        y0 = min(int(y.split("-")[0]) for y in years)
        y1 = max(int(y.split("-")[1]) for y in years)
        e = dict(e)
        e["years"] = f"{y0}-{y1}"
        merged.append((e, eid, tid))
    return merged


BAND_MOTOR = [
    (85, 100, "neredeyse arızasız"),
    (65, 84, "sağlam, bilinen küçük bakım kalemi var"),
    (50, 64, "orta risk, izlenmesi gereken kalem var"),
    (35, 49, "yüksek risk, tanımlı bir tasarım hatası var"),
    (0, 34, "kumar"),
]
BAND_TRANS = [
    (85, 100, "temiz"),
    (65, 84, "yönetilebilir bakım kalemi"),
    (50, 64, "tekrarlayan ama yönetilebilir şikayet"),
    (35, 49, "bilinen risk, kavrama/mekatronik odaklı"),
    (0, 34, "düşük km'de felaket, çoklu kaynak"),
]


def band_for(score: int, bands) -> str:
    for lo, hi, name in bands:
        if lo <= score <= hi:
            return name
    return "sınıflandırılmamış"


def top_known_issue(comp: dict) -> str:
    issues = comp.get("known_issues") or []
    if not issues:
        return "belirgin bir zaaf kaydı yok"
    return issues[0]["issue"]


def nearest_sibling(cars: list[dict], brand: str, body_type: str | None, year_mid: float) -> dict | None:
    """comf/cost/liq tahmini için en yakın kardeş aracı bulur.

    Aynı markadan, mümkünse aynı gövde tipinden, yıl olarak en yakın aracı seçiyor.
    Bulunamazsa None döner ve çağıran taraf güvenli bir varsayılana düşer.
    """
    same_brand = [c for c in cars if norm(c.get("brand_group")) == norm(brand)]
    if not same_brand:
        return None
    pool = [c for c in same_brand if c["specs"].get("body_type") == body_type] or same_brand

    def year_mid_of(c):
        m = re.match(r"(\d{4})-(\d{4})", c.get("years", ""))
        return (int(m.group(1)) + int(m.group(2))) / 2 if m else 2015

    return min(pool, key=lambda c: abs(year_mid_of(c) - year_mid))


def build_car(e: dict, eng_id: str, tr_id: str, engines: dict, trans: dict,
              sources: dict, cars: list[dict], used_ids: set[str]) -> dict | None:
    sp = e["specs"]
    eng = engines[eng_id]
    tr = trans[tr_id]

    car_id = e["id"]
    if car_id in used_ids:
        return None
    used_ids.add(car_id)

    m_score = int(round(eng["base_score"])) if eng.get("base_score") is not None else None
    t_score = int(round(tr["base_score"])) if tr.get("base_score") is not None else None
    if m_score is None or t_score is None:
        return None  # motor ya da kutu ailesinin puanı henüz yok; terfi edilemez

    y0, y1 = (int(x) for x in e["years"].split("-"))
    year_mid = (y0 + y1) / 2
    sib = nearest_sibling(cars, e["brand"], sp.get("body_type"), year_mid)
    if sib:
        comf, cost, liq = sib["scores"]["comf"], sib["scores"]["cost"], sib["scores"]["liq"]
        fun = sib["scores"]["fun"]
        price = sib["price_band_k_try"]
        sib_note = f"kardeş araç: {sib['name']} ({sib['id']})"
    else:
        comf, cost, liq, fun = 60, 55, 45, 50
        price = [400, 700]
        sib_note = "kardeş araç bulunamadı, güvenli varsayılan kullanıldı"

    car_sources = sorted(set(eng.get("sources", [])) | set(tr.get("sources", [])))
    n_src = len(car_sources)
    verification = "verified" if n_src >= 4 else ("partial" if n_src >= 1 else "preliminary")

    trans_label = {
        "TK": f"{sp.get('gears') or '?'} ileri otomatik",
        "Islak DCT": f"{sp.get('gears') or '?'} ileri ıslak DCT",
        "Kuru DCT": f"{sp.get('gears') or '?'} ileri kuru DCT",
        "CVT": "CVT",
        "Robot": f"{sp.get('gears') or '?'} ileri robotlu yarı otomatik",
    }.get(sp["transmission_type"], sp["transmission_type"])
    tag = f"oto: {trans_label} · {sp['hp']}bg"

    # fun, compute_fun.py'nin gerektirdiği kerb_weight_kg P2.1 kataloğunda hiç
    # bulunmadığı için formülle hesaplanamıyor. Sabit bir sayı yerine (bu, hepsi
    # aynı "ortalama" görünen 79 araç üretirdi) kardeş aracın fun puanı kullanılıyor
    # — comf/cost/liq ile aynı tahmin yöntemi. evidence.fun bilinçli olarak
    # eklenmiyor; bu, depodaki 115/278 aracın zaten içinde bulunduğu, kabul edilmiş
    # bir durumla aynı (puan var, formül kanıtı yok).
    scores = {"motor": m_score, "trans": t_score, "fun": fun, "comf": comf,
              "age": 50, "cost": cost, "liq": liq}

    evidence = {
        "motor": {
            "band": band_for(m_score, BAND_MOTOR),
            "confidence": "orta" if n_src >= 2 else "düşük",
            "sources": eng.get("sources", [])[:3],
            "reasoning": (
                f"{eng['names'][0]} ({eng_id}) motor ailesinin temel puanı {m_score}. "
                f"Bu aracın motor puanı ({m_score}) temel puanla birebir aynı. Ailenin "
                f"bilinen zaafı: {top_known_issue(eng)}. Bu puan '{band_for(m_score, BAND_MOTOR)}' "
                "bandına giriyor."
            ),
            "assessed_at": TODAY,
        },
        "trans": {
            "band": band_for(t_score, BAND_TRANS),
            "confidence": "orta" if n_src >= 2 else "düşük",
            "sources": tr.get("sources", [])[:3],
            "reasoning": (
                f"{tr['names'][0]} ({tr_id}) şanzıman ailesinin temel puanı {t_score}. "
                f"Bu aracın trans puanı ({t_score}) temel puanla birebir aynı. Ailenin "
                f"bilinen zaafı: {top_known_issue(tr)}. Bu puan '{band_for(t_score, BAND_TRANS)}' "
                "bandına giriyor."
            ),
            "assessed_at": TODAY,
        },
    }

    note = (
        f"Bu araç {TODAY} tarihinde `data/catalog/`'dan (MK-22, P2.1 veri paketi) "
        f"terfi ettirildi (`scripts/promote_catalog.py`). Motor ve şanzıman puanı "
        f"aile kaydından miras alındı (MK-16 mekanik miras deseni), motor/şanzıman "
        f"dışındaki kriterler (sürüş keyfi, konfor, maliyet, likidite, fiyat bandı) araca özgü "
        f"araştırılmadı; {sib_note} temel alınarak tahmin edildi ve bu tahmin "
        f"gerekçesizdir — düzeltilmesi gerekiyorsa ilk yapılması gereken iş bu."
    )

    return {
        "id": car_id,
        "name": e["name"],
        "tag": tag,
        "brand_group": e["brand"],
        "years": e["years"],
        "specs": {
            "hp": sp["hp"],
            "displacement_l": sp["displacement_l"],
            "fuel": sp["fuel"],
            "drivetrain": sp.get("drivetrain") or "Önden",
            "transmission_type": sp["transmission_type"],
            "transmission_id": tr_id,
            "body_type": sp.get("body_type"),
            "engine_id": eng_id,
            "torque_nm": sp.get("torque_nm"),
            "gears": sp.get("gears"),
            "clutch": sp.get("clutch"),
            "engine_code": sp.get("engine_code"),
        },
        "price_band_k_try": price,
        "verification": verification,
        "scores": scores,
        "sources": car_sources,
        "note": note,
        "provenance": {
            "added_at": TODAY,
            "method": "scripts/promote_catalog.py — katalog terfi (Y-19/MK-22/MK-16)",
            "specs_source": f"data/catalog/, P2.1 kaynak varyant {e['provenance']['source_variant_id']}",
        },
        "evidence": evidence,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    cars = load_cars()
    catalog = load_catalog()
    engines = json.loads((DATA / "engines.json").read_text(encoding="utf-8"))
    trans = json.loads((DATA / "transmissions.json").read_text(encoding="utf-8"))
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))

    candidates = find_candidates(cars, catalog)
    used_ids = {c["id"] for c in cars}
    # Depoda zaten aynı adı taşıyan bir araç varsa (ör. "BMW E36 325i" önceki bir
    # turdan kayıtlıysa) yeni bir kopyasını yazmıyoruz; katalogdaki bu satırın
    # zaten karşılığı depoda var demektir, yalnızca eşleme kaçırılmış olabilir —
    # o, ayrı bir elle inceleme işi.
    existing_names = {norm(c["name"]) for c in cars}
    written = 0
    skipped_no_score = 0
    skipped_existing_name = 0
    for e, eng_id, tr_id in candidates:
        if args.limit and written >= args.limit:
            break
        if norm(e["name"]) in existing_names:
            skipped_existing_name += 1
            continue
        car = build_car(e, eng_id, tr_id, engines, trans, sources, cars, used_ids)
        if car is None:
            skipped_no_score += 1
            continue
        path = DATA / "cars" / f"{car['id']}.json"
        if args.write:
            path.write_text(json.dumps(car, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written += 1
        cars.append(car)  # sonraki nearest_sibling aramalarında da görünsün

    print(f"aday: {len(candidates)} | terfi edilen: {written} | "
          f"puanı olmadığı için atlanan: {skipped_no_score} | "
          f"depoda aynı adla zaten var: {skipped_existing_name}")
    if not args.write:
        print("(yazmadan çalıştırıldı; uygulamak için --write ver)")


if __name__ == "__main__":
    main()
