#!/usr/bin/env python3
"""import_catalog.py — P2.1 veri paketinden olgusal teknik katalog üretir (MK-22).

**Neden var.** P2.1 paketi 1.641 araç–motor–şanzıman kombinasyonu taşıyor; deponun
puanlanmış listesi 278. Aradaki fark gerçek bir değer ama doğrudan alınamaz: bu
varyantların önemli bir kısmında puan `p2-inferred-prior`, yani araştırılmamış,
çıkarsanmış. Puanları almak deponun kanıt zincirini çökertirdi (MK-21 bunu doğru
söylemişti).

**Bu betiğin çizdiği sınır: olgu alınır, yargı alınmaz.** Güç, tork, hacim, çekiş tipi,
vites sayısı ve kavrama tipi ölçümdür — kaynağı gösterilebilir, yanlışsa nesnel olarak
yanlıştır. Güvenilirlik puanı yargıdır ve gerekçe ister. Bu betik yalnız birincisini
yazar; `data/catalog/` katmanına hiçbir puan girmez.

**Kalite gizlenmez.** P2.1'in kendi kalite sicili (992 kayıt) katalog kaydına
`quality_flags` olarak birlikte yazılır. Bir kaydın şanzıman kimliği tam çözülmemişse
bu görünür kalır ki `data/cars/` katmanına terfi sırasında yakalansın (MK-18'in çapraz
doğrulamada bulduğu türden hatalar tam olarak böyle yakalanıyor).

**Kaynak hakları.** P2.1 kaynak sicilinin yeniden dağıtım politikası "kısa olgusal alan ve
kaynak URL'si; uzun metin, tablo veya görsel kopyası yok" diyor. Bu betik tam olarak o
iznin içinde kalır: olgusal alanlar ve kaynak adresi alınır, uzun metin alınmaz. 2.071 ham
ilan gözlemi depoya hiç girmez.

Kaynak veri paketi depoya dahil değildir (dış paket, ayrı lisans). Yol `--db` ile verilir.

Kullanım:
    python3 scripts/import_catalog.py --db /yol/arac_veritabani_p2_1.sqlite
    python3 scripts/import_catalog.py --db ... --check   # üretilmiş katalog güncel mi
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import shutil
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "catalog"
DATASET = "ARAC-P2.1-PRICE-EXPANSION-2026-08"
IMPORTED_AT = "2026-08-15"

# Kaynak verideki "değer yok" yerine geçen dizgeler. Bunlar null'a çevrilir;
# olduğu gibi yazılırsa katalogda sahte bir değer gibi görünürler.
PLACEHOLDERS = {
    "belirtilmemiş", "belirtilmemis", "kaynakta belirtilmemiş",
    "kaynakta belirtilmemis", "bilinmiyor", "yok", "none", "",
    # Bu, gerçek bir kavrama tipi değil — kaynak veride 287 kayıtta bir değer yerine
    # bir uyarı cümlesi duruyor ("Islak/kuru tipi VIN-kutu koduyla doğrulanmalı").
    # Yer tutucu gibi temizlenmezse eşleştirmede sahte bir "kavrama tipi" gibi işlem
    # görüp gerçek kavrama değeriyle asla eşleşmeyen bir anahtar üretir.
    "islak/kuru tipi vin-kutu koduyla doğrulanmalı",
}

# MK-15 türü aralık korumaları: birim hatasını ve bozuk kaydı yakalamak için.
HP_MIN, HP_MAX = 30, 900
NM_MIN, NM_MAX = 50, 1200
L_MIN, L_MAX = 0.5, 8.0

BRAND_ALIAS = {
    "vw": "volkswagen",
    "mercedes": "mercedes-benz",
    "mercedes benz": "mercedes-benz",
}


def norm(s) -> str:
    if s is None:
        return ""
    s = str(s).lower()
    for a, b in [("ı", "i"), ("ş", "s"), ("ç", "c"), ("ğ", "g"), ("ü", "u"), ("ö", "o")]:
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def slug(s) -> str:
    return re.sub(r"-+", "-", norm(s).replace(" ", "-")).strip("-")


def brandkey(s) -> str:
    n = norm(s)
    return BRAND_ALIAS.get(n, n)


def clean(v):
    """Yer tutucu dizgeleri null'a çevirir."""
    if v is None:
        return None
    s = str(v).strip()
    if norm(s) in PLACEHOLDERS:
        return None
    return s


# Depo kimliği deseni: küçük harf ve tire (ör. "bmw-m54", "fca-multiair-14").
# Üretici motor kodları böyle görünmez; büyük harf ya da tiresiz alfanümeriktir
# (ör. "M54B22", "AR32310", "198A2000").
REPO_ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)+$")


DRIVETRAIN_MAP = {"onden": "Önden", "arkadan": "Arkadan", "dort": "Dört çeker",
                   "dort ceker": "Dört çeker"}


def clean_drivetrain(v):
    """Çekiş tipini şemanın kabul ettiği üç değere normalize eder.

    Kaynak veri kendi içinde tutarsız: 193 kayıt 'Dört' yazıyor, 4 kayıt 'Dört çeker'
    yazıyor — aynı şeyi iki farklı dizgeyle. Normalize edilmeden bırakılırsa
    validate.py'nin gecersiz-deger kuralı bu kayıtları reddediyor.
    """
    s = clean(v)
    if s is None:
        return None
    return DRIVETRAIN_MAP.get(norm(s), s)


def clean_engine_code(v):
    """Üretici motor kodunu döndürür; depo kimliği sızmışsa None döndürür.

    P2.1'in `engine_code` alanı her zaman üreticinin kodunu taşımıyor: ölçüldüğünde
    dolu 171 değerin 162'sinin aslında deponun kendi `engine_id` değeri olduğu görüldü
    (ör. `engine_code = "bmw-m54"`). Bunu araç kaydına yazmak, `engine_id`'yi başka bir
    ada ikinci kez kopyalamak olurdu; alan yeni bir olgu taşımaz, yalnızca üreticinin
    kodunu taşıdığı izlenimini verirdi. Gerçek kod bulunamadığında alan boş bırakılır.
    """
    s = clean(v)
    if s is None or REPO_ID_RE.match(s):
        return None
    return s


def load_ours() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((DATA / "cars").glob("*.json"))]


def fetch_variants(db: pathlib.Path) -> list[dict]:
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    q = """
    SELECT v.variant_id, v.model_variant, v.year_start, v.year_end, v.power_hp,
           v.torque_nm, v.drivetrain, v.publication_status, v.technical_url,
           b.name AS brand, m.model_family, g.generation, g.body_type,
           e.engine_code, e.engine_name, e.fuel, e.displacement_cc,
           t.transmission_name, t.transmission_type, t.gears, t.clutch
      FROM variants v
      LEFT JOIN generations g ON g.generation_id = v.generation_id
      LEFT JOIN models m      ON m.model_id      = g.model_id
      LEFT JOIN brands b      ON b.brand_id      = m.brand_id
      LEFT JOIN engines e     ON e.engine_id     = v.engine_id
      LEFT JOIN transmissions t ON t.transmission_id = v.transmission_id
    """
    return [dict(r) for r in con.execute(q)]


def fetch_quality(db: pathlib.Path) -> dict[str, list[str]]:
    con = sqlite3.connect(db)
    out = collections.defaultdict(list)
    for vid, code in con.execute(
        "SELECT variant_id, issue_code FROM data_quality_issues WHERE status != 'resolved'"
    ):
        if vid:
            out[vid].append(code)
    return out


def fetch_sources(db: pathlib.Path) -> tuple[dict, dict]:
    """Katalog kaynak sicili ve varyant->kaynak bağlantıları.

    Bu kaynaklar `data/sources.json` içine YAZILMAZ. O dosya puanı destekleyen kanıt
    sicilidir; teknik özellik sayfası bir puanı desteklemez, yalnız bir olguyu gösterir.
    Aynı ayrım MK-19'da fiyat kaynakları için de yapılmıştı.
    """
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    srcs = {}
    for r in con.execute("SELECT source_id, publisher, url, source_type, tier FROM sources"):
        if not clean(r["url"]):
            continue
        srcs[r["source_id"]] = {
            "id": r["source_id"],
            "publisher": clean(r["publisher"]),
            "url": r["url"],
            "type": clean(r["source_type"]),
            "tier": clean(r["tier"]),
        }
    links = collections.defaultdict(list)
    for r in con.execute("SELECT variant_id, source_id FROM variant_sources"):
        if r["source_id"] in srcs:
            links[r["variant_id"]].append(r["source_id"])
    return srcs, links


# Yakıt türünü **tanımsal olarak** belirleyen ticari adlar. Bir "Opel Astra 1.6 CDTI"
# benzinli olamaz, bir "Volvo S60 T5" dizel olamaz; bunlar üreticinin kendi yakıt
# rozetleri. Ad ile `fuel` alanı çelişiyorsa ikisinden biri yanlıştır.
FUEL_TOKENS_DIESEL = [
    r"\btdi\b", r"\bhdi\b", r"\bbluehdi\b", r"\bcdi\b", r"\bdci\b", r"\bdti\b",
    r"\bcrdi\b", r"\bjtd\b", r"\bjtdm\b", r"\btdci\b", r"\bcdti\b", r"\bmultijet\b",
    r"\bskyactiv-?d\b", r"\becoblue\b", r"\bd-?4d\b", r"\bi-?dtec\b", r"\bbitdi\b",
]
FUEL_TOKENS_PETROL = [
    r"\btsi\b", r"\btfsi\b", r"\bgdi\b", r"\bvtec\b", r"\bvvt-?i\b", r"\bthp\b",
    r"\bmpi\b", r"\bt-?gdi\b", r"\becoboost\b", r"\bvti\b", r"\btce\b",
    r"\bskyactiv-?g\b", r"\bfsi\b", r"\betorq\b", r"\btwin ?spark\b", r"\becotsi\b",
]


def fuel_conflict(name: str, brand: str, fuel: str) -> bool:
    """Aracın ticari adı, kayıtlı yakıt türüyle çelişiyor mu.

    Ölçüldüğünde 1.641 kaydın 25'inde çelişki bulundu: "Opel Astra 1.6 CDTI" ve
    "Renault Megane 1.9 DTi" benzin olarak, "Volvo S60 2.3 T5" ve "Volvo V60 1.6 T4"
    dizel olarak kayıtlıydı.

    **Hangi alanın yanlış olduğu ölçülerek bulundu.** Çelişkili 25 kaydın hepsinde
    `fuel`, `displacement_cc`, `torque_nm` ve `engine_name` alanları birbiriyle
    uyumlu; tek başına ayrışan alan **etiketin kendisi** (`model_variant`):

      "Opel Astra 1.9 CDTI · 115 bg"  → 1796cc, "1.8i 16V", 170 Nm  → atmosferik benzin
      "Volvo S60 2.3 T5 · 163 bg"     → 2400cc, "2.4L D5",  340 Nm  → dizel
      "Volvo S60 1.5 T3 · 115 bg"     → 1560cc, 270 Nm @ 115 bg     → Volvo D2 dizeli
      "Renault Megane 1.9 DTi · 280 bg" → 1798cc, "1.8L 16V (280 HP)" → Megane RS benzin

    Yani üç alan bir yana, etiket bir yana. Doğru düzeltme yakıt alanını değiştirmek
    değil, **bozuk etiketi atmak**. Bu işlev artık yalnız tespit ediyor; etiketi
    `rebuild_label()` yeniden kuruyor.
    """
    n = norm(name)
    diesel = any(re.search(p, n) for p in FUEL_TOKENS_DIESEL)
    petrol = any(re.search(p, n) for p in FUEL_TOKENS_PETROL)
    if brandkey(brand) == "volvo":
        # Volvo'nun kendi rozet düzeni: T2-T8 benzin, D2-D5 dizel.
        if re.search(r"\bt[2-8]\b", n):
            petrol = True
        if re.search(r"\bd[2-5]\b", n):
            diesel = True
    if diesel and not petrol:
        return fuel != "Dizel"
    if petrol and not diesel:
        return fuel != "Benzin"
    return False


# Fizik bantları: validate.py ile aynı ölçümden geliyor (1.875 kayıt).
# Dizel düşük devirde tork üretir, benzin yüksek devirde güç; hp/Nm oranı bu yüzden
# yakıt türüne göre dar ve neredeyse örtüşmeyen bantlarda kalıyor.
HP_NM_LIMITS = {"Benzin": (0.48, 1.25), "Dizel": (0.28, 0.62)}


def spec_implausible(fuel: str, hp: int, nm, litre) -> str | None:
    """Güç/tork/hacim üçlüsü fiziksel olarak tutarlı mı; değilse sebebi döner."""
    if not nm:
        return None
    lo, hi = HP_NM_LIMITS.get(fuel, (0, 99))
    ratio = hp / nm
    if not (lo <= ratio <= hi):
        return f"hp/Nm={ratio:.2f} ({fuel}) beklenen {lo}-{hi} dışında"
    if litre:
        per_l = nm / litre
        if fuel == "Dizel" and per_l < 95:
            return f"{per_l:.0f} Nm/L dizel için çok düşük"
        if per_l > 260:
            return f"{per_l:.0f} Nm/L olağandışı yüksek"
    return None


def rebuild_label(model_family: str | None, litre, fuel: str, hp: int) -> str:
    """Bozuk etiket yerine, doğrulanmış alanlardan sade bir ad kurar.

    Yalnız üç yönlü uyuşan alanları kullanır: model ailesi, motor hacmi (cc'den),
    yakıt ve beygir. Üreticinin ticari rozetini (CDTI, T5, DTi) **uydurmaz** — o rozet
    zaten yanlış olduğu için atılıyor. "Opel Astra 1.9 CDTI · 115 bg" yerine
    "Opel Astra 1.8 Benzin · 115 bg" yazılır: daha az iddialı ama doğru.
    """
    parts = [model_family or "?"]
    if litre:
        parts.append(f"{litre:.1f}".rstrip("0").rstrip(".") if litre % 1 else f"{litre:.1f}")
    parts.append(fuel)
    return f"{' '.join(parts)} · {hp} bg"


# Tek tek doğrulanmış düzeltmeler. Bu beş kayıt spec_implausible denetiminde
# yakalandı ve her biri WebSearch ile bağımsız teknik özellik kaynaklarından
# doğrulandı (2026-08-17). Toplu bir kural yerine variant_id ile eşleştirilmiş
# tek tek düzeltmeler kullanılıyor, çünkü her kaydın bozukluğu farklı bir
# alanda: bazen yakıt, bazen tork, bazen ikisi birden. Genel bir sezgisel kural
# burada yanlış kayıtları da düzeltiyormuş gibi davranıp yeni hata üretebilirdi.
MANUAL_SPEC_CORRECTIONS = {
    # Mercedes E 320 (W211): "320" rozeti CDI'da da kullanılıyor; 224 bg / 540 Nm
    # yalnız 3.0 V6 CDI'nin (OM642) rakamları, benzinli E320 V6 bu torku üretmez.
    "sig-2da1345d7fb0b40cfb": {"fuel": "Dizel"},
    # Renault Espace 3.0: 180 bg / 400 Nm, 2.958 cc V6 dCi'nin (V9X) rakamları;
    # benzinli V6 Espace bu değerlere sahip değil.
    "sig-d4bf02288a234d5016": {"fuel": "Dizel"},
    # Suzuki SX4 1.6 (M16A benzinli motor): kayıtlı 320 Nm doğru değil, gerçek
    # değer 156 Nm (aynı hata puanlanmış suzuki-sx4-1-6 kaydında da vardı ve
    # oradan da düzeltildi).
    "sig-19ae84c75d2f66a5a4": {"torque_nm": 156.0},
    # Peugeot 301 1.6 HDi (DV6 motoru): kayıtlı 115 bg / 150 Nm, aslında 1.6 VTi
    # BENZİNLİ varyantının rakamları (aynı çelişki, aynı hata sınıfı puanlanmış
    # peugeot-301-1-6-hdi kaydında bulunmuştu). 301'in 115 bg'lik bir HDi
    # versiyonu hiç üretilmedi; gerçek HDi rakamı 92 bg / 230 Nm.
    "p21-fe5003dffa372274b4": {"hp": 92, "torque_nm": 230.0},
    # Ford Fiesta "1.6 · 112 bg": kayıtlı yakıt Dizel ama engine_name alanı
    # "1.5L Ti-VCT ... (112 HP)" diyor — Ti-VCT, Ford'un benzinli değişken supap
    # zamanlama teknolojisi, dizelde hiç kullanılmadı. Aynı fiziksel araç
    # katalogda "EcoSport 1.5 Ti-VCT" olarak da (Benzin, 112 bg, 140 Nm) doğru
    # kayıtlı; bu kayıt onun bozuk bir kopyası.
    "sig-7895f79c42c3199673": {"fuel": "Benzin"},
    # Mercedes 3.0 V6 dizel (OM642) kümesi: "270 CDI" rozeti gerçekte var olmayan
    # bir beygir/yıl bileşimine yapıştırılmıştı (WebSearch ile doğrulandı,
    # 2026-08-17, terfi eden araçlardaki OM651 anakronizmini bulan aynı tur).
    # OM642 2005'ten önce üretilmedi; 2005 sonrası kayıtlarda gerçek rozet
    # aşağıdaki gibi düzeltildi. hp/Nm/yıl kombinasyonu hiçbir gerçek Mercedes
    # ürününe denk gelmeyenler MERCEDES_BADGE_YEAR_CONFLICTS'e taşındı (aşağıda),
    # düzeltilmedi.
    "sig-59df53db593534cbd5": {"model_variant": "C 350 CDI BlueTEC 4MATIC"},  # 2011, 231bg/540Nm, W204 facelift
    "sig-d9eee606ba0376c9cd": {"model_variant": "C 350 CDI BlueTEC"},  # 2011, 265bg/620Nm, W204 facelift üst tün
    "sig-ee0554bc84a126e257": {"model_variant": "E 350 CDI"},  # 2013, 231bg/540Nm, W212
    "sig-ab10da7cf92724f7ea": {"model_variant": "E 350 BlueTEC"},  # 2013, 252bg/620Nm, W212 facelift
    "sig-ee03f53b684a1e96f9": {"model_variant": "E 350 BlueTEC"},
    "sig-37639613b31b9ec5b6": {"model_variant": "E 350 BlueTEC"},
}

# Rozet + beygir + yıl birlikte hiçbir gerçek Mercedes ürününe denk gelmeyen kayıtlar
# (WebSearch ile doğrulandı, 2026-08-17). OM642 3.0 V6 dizel 2005'ten önce
# üretilmedi; bu yıllarda bu beygir seviyelerinde ne OM611/OM612/OM613 (4/5
# silindir) ailesinde ne de dönemin gerçek rozet listesinde bir karşılık var.
# MANUAL_SPEC_CORRECTIONS'taki gibi "doğru rozeti bul" yaklaşımı burada
# uygulanamıyor çünkü düzeltilecek gerçek bir rozet yok — uydurmak, atılan
# rozetten daha kötü bir hata olurdu. Bu yüzden düzeltilmedi, `quality_flags`'e
# "rozet_yil_celiskisi" olarak işaretlendi (CLAUDE.md §1: düzeltilemeyen bir
# şey varsa bu, sebebiyle birlikte açıkça söylenir).
MERCEDES_BADGE_YEAR_CONFLICTS = {
    "sig-a582366fd365339e7d": "C 270 CDI · 231 bg (2001): OM642 2005'ten önce yok, 2001 C-Class'ta 231 bg dizel hiç üretilmedi",
    "sig-cc05bb4c89e11ee3c5": "C 270 CDI · 231 bg (2002): OM642 2005'ten önce yok, 2002 C-Class'ta 231 bg dizel hiç üretilmedi",
    "sig-570cb2cd174b7d46da": "E 200 CDI · 190 bg (2002): OM642 2005'ten önce yok, dönemin E200 CDI'ı (OM611) en fazla 122 bg üretiyordu",
    "sig-e2107852394a989776": "E 270 CDI · 224 bg (2003): OM642 2005'ten önce yok, 2003 E-Class'ta 224 bg dizel hiç üretilmedi",
    "sig-e61df3bdd29e1a077f": "CLK 270 CDI · 224 bg (2005-2009): hp gerçek CLK 320 CDI'ya (OM642) yakın ama kayıtlı tork (415 Nm) gerçek CLK 320 CDI'nın (510 Nm) belirgin altında; hangi alanın yanlış olduğu tek başına belirlenemedi",
}


def build_entry(v: dict, quality: dict, links: dict) -> tuple[dict | None, str | None]:
    """Bir P2.1 varyantından katalog kaydı üretir. Reddedilirse (None, sebep) döner."""
    fix = MANUAL_SPEC_CORRECTIONS.get(v["variant_id"], {})
    corrected_fields = sorted(fix.keys())

    hp = fix.get("hp", v.get("power_hp"))
    if not isinstance(hp, int) or not (HP_MIN <= hp <= HP_MAX):
        return None, f"beygir aralık dışı ({hp})"

    fuel = fix.get("fuel", clean(v.get("fuel")))
    if fuel not in ("Benzin", "Dizel"):
        return None, f"yakıt kapsam dışı ({fuel})"

    y0, y1 = v.get("year_start"), v.get("year_end")
    if not (isinstance(y0, int) and isinstance(y1, int) and 1980 <= y0 <= y1 <= 2030):
        return None, f"yıl aralığı geçersiz ({y0}-{y1})"

    nm = fix.get("torque_nm", v.get("torque_nm"))
    nm = float(nm) if isinstance(nm, (int, float)) and NM_MIN <= nm <= NM_MAX else None

    cc = v.get("displacement_cc")
    litre = round(cc / 1000.0, 1) if isinstance(cc, (int, float)) and cc else None
    if litre is not None and not (L_MIN <= litre <= L_MAX):
        litre = None

    gears = v.get("gears")
    gears = int(gears) if isinstance(gears, (int, float)) and 3 <= gears <= 10 else None

    brand = clean(v.get("brand")) or "Bilinmeyen"
    variant_label = fix.get("model_variant") or clean(v.get("model_variant")) or clean(v.get("model_family")) or "?"
    name = f"{brand} {variant_label}".strip()

    # Etiket, kendisiyle uyumlu üç alana (yakıt, hacim, tork) karşı çelişiyorsa
    # atılır ve doğrulanmış alanlardan yeniden kurulur. Atılan etiket kaybolmuyor,
    # provenance içinde saklanıyor ki düzeltme geri izlenebilsin.
    rejected_label = None
    if fuel_conflict(name, brand, fuel):
        rejected_label = variant_label
        name = f"{brand} {rebuild_label(clean(v.get('model_family')), litre, fuel, hp)}"

    entry = {
        "id": None,  # aşağıda atanır
        "name": name,
        "brand": brand,
        "model_family": clean(v.get("model_family")),
        "generation": clean(v.get("generation")),
        "years": f"{y0}-{y1}",
        "specs": {
            "hp": hp,
            "torque_nm": nm,
            "displacement_l": litre,
            "fuel": fuel,
            "drivetrain": clean_drivetrain(v.get("drivetrain")) or "Belirtilmemiş",
            "body_type": clean(v.get("body_type")),
            "transmission_type": clean(v.get("transmission_type")) or "Belirtilmemiş",
            "transmission_name": clean(v.get("transmission_name")),
            "gears": gears,
            "clutch": clean(v.get("clutch")),
            "engine_code": clean_engine_code(v.get("engine_code")),
            "engine_name": clean(v.get("engine_name")),
        },
        "scored_car_id": None,
        "possible_scored_car_ids": [],
        "quality_flags": sorted(set(quality.get(v["variant_id"], []))
                                | ({"label_corrected"} if rejected_label else set())
                                | ({"spec_corrected"} if corrected_fields else set())
                                | ({"spec_implausible"}
                                   if spec_implausible(fuel, hp, nm, litre) else set())
                                | ({"rozet_yil_celiskisi"}
                                   if v["variant_id"] in MERCEDES_BADGE_YEAR_CONFLICTS else set())),
        "sources": sorted(set(links.get(v["variant_id"], []))),
        "provenance": {
            "dataset": DATASET,
            "imported_at": IMPORTED_AT,
            "source_variant_id": v["variant_id"],
            "publication_status": clean(v.get("publication_status")),
            "technical_url": clean(v.get("technical_url")),
            "rejected_label": rejected_label,
            "manually_corrected_fields": corrected_fields or None,
        },
    }
    return entry, None


def assign_ids(entries: list[dict]) -> None:
    """Kalıcı, okunabilir ve çakışmasız kimlik atar (CLAUDE.md §4).

    Kimlik marka+varyant+beygirden türetilir, yani kaynak paketin hash'ine bağlı
    değildir; paket yeniden üretilse bile aynı araç aynı kimliği alır.
    """
    used = collections.Counter()
    for e in entries:
        base = slug(f"{e['brand']} {e['name'].replace(e['brand'], '', 1)} {e['specs']['hp']}")
        base = re.sub(r"-+", "-", base).strip("-")[:70] or "arac"
        used[base] += 1
        e["id"] = base if used[base] == 1 else f"{base}-{used[base]}"


def model_matches(model_family: str | None, car_name: str) -> bool:
    """Katalog kaydının model ailesi, puanlanmış aracın adında geçiyor mu.

    Bu kontrol olmadan marka+beygir+hacim üçlüsü **farklı modelleri** birbirine
    bağlıyordu: bir Opel Vectra kaydı bir Astra satırına, bir Seat Arona kaydı Ibiza ve
    Leon satırlarına eşleşiyordu. İkisi de MK-08'in uyardığı nesil/model karıştırma
    hatasının ta kendisi. Model adı uyuşmuyorsa bağ kurulmaz.
    """
    if not model_family:
        return False
    fam = norm(model_family)
    if not fam:
        return False
    name = norm(car_name)
    # Sınır duyarlı arama: "a3" adı "a35" ile eşleşmesin.
    return re.search(rf"(?:^|\s){re.escape(fam)}(?:$|\s)", name) is not None


def link_scored(entries: list[dict], ours: list[dict]) -> tuple[int, int]:
    """Katalog kayıtlarını puanlanmış araçlara bağlar.

    Tek aday varsa `scored_car_id` yazılır ve arayüz o kaydı ayrı satır olarak
    göstermez. Birden çok aday varsa hiçbiri seçilmez; adaylar
    `possible_scored_car_ids` içinde durur ve terfi sırasında elle çözülür. Otomatik
    seçim yapmak, MK-08'in uyardığı nesil karıştırma hatasını üretmenin kısa yoludur.

    Eşleşmenin dört şartı var ve dördü birden aranır: marka, beygir, motor hacmi ve
    **model adı**. Model adı şartı sonradan eklendi, çünkü ilk sürüm onsuz çalıştığında
    farklı modelleri birbirine bağladığı ölçüldü.
    """
    idx = collections.defaultdict(list)
    for o in ours:
        sp = o["specs"]
        lit = sp.get("displacement_l")
        lit = round(float(lit), 1) if lit else None
        idx[(brandkey(o.get("brand_group")), sp.get("hp"), lit)].append(o)

    exact = ambiguous = 0
    for e in entries:
        sp = e["specs"]
        cands = idx.get((brandkey(e["brand"]), sp["hp"], sp["displacement_l"]), [])
        # Model adı uyuşmayan adaylar en baştan elenir.
        cands = [o for o in cands if model_matches(e.get("model_family"), o.get("name", ""))]
        # Üretim yılı örtüşmesi ve şanzıman tipi **her bağ için** zorunludur; bunlar
        # yalnızca beraberlik bozan ölçütler değil. Önceki sürümde bu iki kontrol
        # sadece bir kayda birden çok araç düştüğünde çalışıyordu, ama pratikte tersi
        # oluyor: aynı araca birden çok katalog kaydı düşüyor ve her biri kontrolsüz
        # bağlanıyordu. Sonuç, bir CR-V III kaydının 2002-2006 nesline de bağlanmasıydı.
        y0, y1 = (int(x) for x in e["years"].split("-"))
        kept = []
        for o in cands:
            if o["specs"].get("transmission_type") != sp["transmission_type"]:
                continue
            m = re.match(r"(\d{4})\D+(\d{4})", o.get("years", ""))
            if not m or int(m.group(2)) < y0 or int(m.group(1)) > y1:
                continue
            kept.append(o)
        cands = kept
        if len(cands) == 1:
            e["scored_car_id"] = cands[0]["id"]
            exact += 1
        elif len(cands) > 1:
            e["possible_scored_car_ids"] = sorted(o["id"] for o in cands)
            ambiguous += 1
    return exact, ambiguous


def build(db: pathlib.Path, out: pathlib.Path) -> dict:
    variants = fetch_variants(db)
    quality = fetch_quality(db)
    srcs, links = fetch_sources(db)
    ours = load_ours()

    entries, rejected = [], []
    for v in variants:
        e, why = build_entry(v, quality, links)
        if e is None:
            rejected.append((v.get("variant_id"), why))
        else:
            entries.append(e)

    entries.sort(key=lambda e: (brandkey(e["brand"]), e["name"], e["specs"]["hp"]))
    assign_ids(entries)
    exact, ambiguous = link_scored(entries, ours)

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    by_brand = collections.defaultdict(list)
    for e in entries:
        by_brand[brandkey(e["brand"]) or "bilinmeyen"].append(e)

    used_src = {s for e in entries for s in e["sources"]}
    for brand, rows in sorted(by_brand.items()):
        payload = {
            "_comment": (
                "Bu dosya scripts/import_catalog.py tarafından P2.1 veri paketinden "
                "üretildi (MK-22). Olgusal teknik katalogdur: puan, kanıt bloğu veya "
                "güvenilirlik yargısı taşımaz. Elle düzenlenmez."
            ),
            "brand": rows[0]["brand"],
            "dataset": DATASET,
            "entries": rows,
        }
        (out / f"{brand.replace(' ', '-')}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (out / "_sources.json").write_text(
        json.dumps({
            "_comment": (
                "Katalog kaynak sicili. Bu kaynaklar data/sources.json içine YAZILMAZ: "
                "o dosya puanı destekleyen kanıt sicilidir, buradaki kayıtlar ise yalnız "
                "olgusal alanın nereden geldiğini gösterir (MK-22, MK-19 ile aynı ayrım). "
                "Doğrulama etiketi üretmezler."
            ),
            "dataset": DATASET,
            "sources": {k: v for k, v in sorted(srcs.items()) if k in used_src},
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "toplam_varyant": len(variants),
        "katalog_kaydi": len(entries),
        "reddedilen": len(rejected),
        "red_sebepleri": collections.Counter(w for _, w in rejected).most_common(5),
        "puanlanmisa_bagli": exact,
        "belirsiz_eslesme": ambiguous,
        "yalniz_katalogda": sum(1 for e in entries
                                if not e["scored_car_id"] and not e["possible_scored_car_ids"]),
        "marka_dosyasi": len(by_brand),
        "kaynak": len({s for e in entries for s in e["sources"]}),
        "kalite_isaretli": sum(1 for e in entries if e["quality_flags"]),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True, type=pathlib.Path,
                    help="P2.1 sqlite dosyasının yolu (paket depoya dahil değildir)")
    ap.add_argument("--check", action="store_true",
                    help="Üretilmiş katalog bugünkü kaynak veriyle uyumlu mu")
    args = ap.parse_args()

    if not args.db.exists():
        print(f"HATA: kaynak veri paketi bulunamadı: {args.db}", file=sys.stderr)
        sys.exit(2)

    if args.check:
        tmp = OUT.with_name("catalog.check-tmp")
        build(args.db, tmp)
        ok = True
        if not OUT.exists():
            print("HATA: data/catalog/ yok, önce betiği --check'siz çalıştırın.", file=sys.stderr)
            ok = False
        else:
            real = {p.name for p in OUT.glob("*.json")}
            new = {p.name for p in tmp.glob("*.json")}
            if real != new:
                print("HATA: katalog dosya listesi güncel değil.", file=sys.stderr)
                ok = False
            for n in sorted(real & new):
                if (OUT / n).read_text(encoding="utf-8") != (tmp / n).read_text(encoding="utf-8"):
                    print(f"HATA: catalog/{n} güncel değil.", file=sys.stderr)
                    ok = False
        shutil.rmtree(tmp)
        if ok:
            print("data/catalog/ güncel.")
        sys.exit(0 if ok else 1)

    stats = build(args.db, OUT)
    for k, v in stats.items():
        print(f"  {k:22} {v}")


if __name__ == "__main__":
    main()
