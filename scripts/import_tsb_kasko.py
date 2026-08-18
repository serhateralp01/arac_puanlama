#!/usr/bin/env python3
"""import_tsb_kasko.py — TSB Kasko Değer Listesi'ni araç fiyat bantlarına yazar.

`docs/FIYAT-KAYNAK-ARASTIRMASI.md` bu projenin en büyük eksiğinin tarihli, kanıta
dayalı bir fiyat kaynağı olduğunu, ve Türkiye Sigorta Birliği'nin (TSB) periyodik
Kasko Değer Listesi'nin bunun için en uygun aday olduğunu tespit etmişti. Bu ortamdan
tsb.org.tr'ye ağ erişimi engellendiği için kullanıcı listeyi elle depoya yapıştırdı;
ham veri `data/market/tsb-kasko-2026-07.tsv` içinde duruyor, bu betik onu işler.

TSB listesi marka+tip başına, 2012-2019 model yılları için TL cinsinden resmi kasko
değeri veriyor. Bu değer bir ilan fiyatı değil; `data/market/tsb-kasko-2026-07.json`
içindeki `known_limitations` bu farkı ve yöntemin sınırlarını açıklıyor.

Eşleştirme stratejisi kasıtlı olarak temkinli: `Tip Adı` serbest metin olduğu için
motor/şanzıman/yakıt bilgisini regex ile ayrıştırıp, YALNIZCA marka + hacim + beygir
+ yakıt + şanzıman-otomatik-mi birlikte örtüşen VE model ailesi adı (ör. "OCTAVIA")
satırda geçen kayıtlar eşleşme sayılıyor. Bu oturumda dört kez tekrarlayan "zamanda
imkânsız eşleşme" hatasından (bkz. docs/ROADMAP.md Y-19) ders alınarak, hacim ve
beygir tam sayısal uyuşma istiyor; yaklaşık eşleşme kabul edilmiyor.

Kullanım:
    python3 scripts/import_tsb_kasko.py            # eşleşmeleri raporla, yazma
    python3 scripts/import_tsb_kasko.py --write    # data/cars/*.json içine yaz
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TSV_PATH = DATA / "market" / "tsb-kasko-2026-07.tsv"
META_PATH = DATA / "market" / "tsb-kasko-2026-07.json"
YEAR_COLUMNS = ["2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012"]

# TSB marka adı -> bu projenin brand_group değeri. Bire bir eşleşmeyenler burada.
BRAND_ALIAS = {
    "MERCEDES": "Mercedes-Benz",
    "RENAULT (OYAK)": "Renault",
    "RENAULT": "Renault",
    "CITROEN": "Citroën",
    "VOLKSWAGEN": "Volkswagen",
    "VOLVO": "Volvo",
    "OPEL": "Opel",
    "SKODA": "Skoda",
    "SEAT": "Seat",
    "PEUGEOT": "Peugeot",
    "TOYOTA": "Toyota",
    "HONDA": "Honda",
    "HYUNDAI": "Hyundai",
    "KIA": "Kia",
    "MAZDA": "Mazda",
    "MITSUBISHI": "Mitsubishi",
    "NISSAN": "Nissan",
    "SUBARU": "Subaru",
    "FORD": "Ford",
    "FIAT": "Fiat",
    "AUDI": "Audi",
    "BMW": "BMW",
    "MINI": "MINI",
    "ALFA ROMEO": "Alfa Romeo",
}

# Marka adı yazılırken ayrıca aracın adında geçen "kısaltma" biçimleri de olabilir
# (ör. brand_group = Volkswagen ama isim "VW ..." ile başlıyor, ya da brand_group
# iki kelimeli ama isimde yalnızca ilk kelime kullanılıyor: "Alfa Romeo" -> "Alfa").
NAME_PREFIX_ALIAS = {
    "Volkswagen": ["Volkswagen", "VW"],
    "Mercedes-Benz": ["Mercedes-Benz", "Mercedes"],
    "Alfa Romeo": ["Alfa Romeo", "Alfa"],
    "Citroën": ["Citroën", "Citroen"],
    "Citroën / Peugeot": ["Citroën", "Citroen", "Peugeot"],
    "Kia / Hyundai": ["Kia", "Hyundai"],
}

DIESEL_TOKENS = (
    "DIZEL", "TDI", "TDCI", "CRDI", "CRDI", "DCI", "JTD", "JTDM", "HDI",
    "CDTI", "D2", "D3", "D4", "D5", "BLUEHDI", "MULTIJET", "DTI", "DDIS",
)
PETROL_HINT_TOKENS = (
    "TSI", "TFSI", "VTI", "PURETECH", "ECOBOOST", "SKY-G", "MZR", "THP",
    "VTEC", "TCE", "MPI", "GDI", "T-GDI", "TGDI",
)
AUTO_TOKEN_RE = re.compile(
    r"\b(\d?AT\d?|E?AT\d?|DSG\d?|TIPT\w*|POWERSHIFT|EDC|CVT|MCP|ETG\d?|AUTO\d?R?|"
    r"S[ -]?TRONIC|MULTITRONIC|XTRONIC|TCT)\b"
)
GEAR_RE = re.compile(r"(\d)\s?(?:AT|DSG|CVT)")

# TSB'nin serbest metin rozetini şanzıman AİLESİNE (kaba kategori) indirger. Bu
# ayrım olmadan "TIPTRONIC" (torque konvertörlü) ile "DSG" (çift kavrama) farklı
# fiziksel donanımlar olduğu halde aynı satırda karıştırılabiliyordu — Skoda Superb
# 1.8 TSI Tiptronic (TK) ile 1.8 TSI DSG (Kuru DCT) karışıklığı bu betik geliştirilirken
# canlı örnekte yakalandı, bu yüzden kategori kontrolü zorunlu tutuldu.
DCT_TOKENS = ("DSG", "TCT", "POWERSHIFT", "EDC")
S_TRONIC_RE = re.compile(r"\bS[ -]?TRONIC\b")
CVT_TOKENS = ("CVT", "XTRONIC", "MULTITRONIC")
ROBOT_TOKENS = ("MCP", "ETG")
TK_TOKENS = ("TIPT", "AUTO", "EAT")

CAR_TX_TO_CATEGORY = {
    "TK": "TK", "CVT": "CVT", "Kuru DCT": "DCT", "Islak DCT": "DCT", "Robot": "Robot",
}


def trans_category(upper: str) -> str | None:
    if any(t in upper for t in DCT_TOKENS) or S_TRONIC_RE.search(upper):
        return "DCT"
    if any(t in upper for t in CVT_TOKENS):
        return "CVT"
    if any(re.search(rf"\b{t}\d?\b", upper) for t in ROBOT_TOKENS):
        return "Robot"
    if any(t in upper for t in TK_TOKENS) or re.search(r"\bAT\d?\b", upper):
        return "TK"
    return None
DISPLACEMENT_RE = re.compile(r"\b([0-6]\.\d)\b")
HP_RE = re.compile(r"(?:\b([0-6]\.\d)\s+(\d{2,3})\b)|\((\d{2,3})\)")


def parse_row(row: dict) -> dict | None:
    text = row["tip_adi"]
    upper = text.upper()

    if not AUTO_TOKEN_RE.search(upper):
        return None  # manuel ya da tanınmayan şanzıman; bu proje otomatik dışını almıyor

    disp_m = DISPLACEMENT_RE.search(upper)
    if not disp_m:
        return None
    displacement_l = float(disp_m.group(1))

    hp = None
    hp_m = HP_RE.search(upper)
    if hp_m:
        hp = int(hp_m.group(2) or hp_m.group(3))
    if hp is None:
        return None

    is_diesel = any(re.search(rf"\b{t}\b", upper) for t in DIESEL_TOKENS)
    fuel = "Dizel" if is_diesel else "Benzin"

    gear_m = GEAR_RE.search(upper)
    gears = int(gear_m.group(1)) if gear_m else None

    category = trans_category(upper)
    if category is None:
        return None

    return {
        "displacement_l": displacement_l,
        "hp": hp,
        "fuel": fuel,
        "gears": gears,
        "category": category,
    }


def load_tsb_rows() -> list[dict]:
    lines = TSV_PATH.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        if not line.strip():
            continue
        cells = line.split("\t")
        row = dict(zip(header, cells))
        marka = row["Marka Adı"].strip()
        tip = row["Tip Adı"].strip()
        values = {y: int(row[y]) for y in YEAR_COLUMNS}
        rows.append({"marka": marka, "tip_adi": tip, "values": values})
    return rows


def family_token(car: dict) -> str:
    """Aracın adından marka önekini atıp kalan ilk kelimeyi model ailesi olarak alır."""
    name = car["name"]
    brand = car["brand_group"]
    prefixes = NAME_PREFIX_ALIAS.get(brand, [brand])
    for p in sorted(prefixes, key=len, reverse=True):
        if name.upper().startswith(p.upper() + " "):
            name = name[len(p):].strip()
            break
    m = re.match(r"[A-Za-zÇĞİıÖŞÜçğiöşü0-9\-]+", name)
    return m.group(0).upper() if m else ""


def load_cars() -> list[tuple[pathlib.Path, dict]]:
    out = []
    for f in sorted((DATA / "cars").glob("*.json")):
        out.append((f, json.loads(f.read_text(encoding="utf-8"))))
    return out


def year_range(car: dict) -> tuple[int, int]:
    lo, hi = car["years"].split("-")
    return int(lo), int(hi)


def match(car: dict, tsb_rows: list[dict]) -> list[dict]:
    brand_group = car["brand_group"]
    tok = family_token(car)
    if not tok:
        return []
    lo, hi = year_range(car)
    matches = []
    for row in tsb_rows:
        mapped_brand = BRAND_ALIAS.get(row["marka"], row["marka"].title())
        if mapped_brand != brand_group:
            continue
        if tok not in row["tip_adi"].upper():
            continue
        parsed = parse_row(row)
        if parsed is None:
            continue
        if parsed["displacement_l"] != car["specs"]["displacement_l"]:
            continue
        if abs(parsed["hp"] - car["specs"]["hp"]) > 3:
            continue
        if parsed["fuel"] != car["specs"]["fuel"]:
            continue
        car_category = CAR_TX_TO_CATEGORY.get(car["specs"]["transmission_type"])
        if car_category and parsed["category"] != car_category:
            continue
        car_gears = car["specs"].get("gears")
        if parsed["gears"] and car_gears and parsed["gears"] != car_gears:
            continue
        # bu tip için o aracın üretim yılları içine düşen model-yılı değerlerini al
        for y in YEAR_COLUMNS:
            yi = int(y)
            if not (lo <= yi <= hi):
                continue
            v = row["values"][y]
            if v > 0:
                matches.append({"tip_adi": row["tip_adi"], "year": yi, "value_try": v})
    return matches


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="hesabı araç dosyalarına yaz")
    args = ap.parse_args()

    tsb_rows = load_tsb_rows()
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    cars = load_cars()

    results = []
    for path, car in cars:
        m = match(car, tsb_rows)
        if not m:
            continue
        values = sorted(v["value_try"] for v in m)
        tip_adi_set = sorted({v["tip_adi"] for v in m})
        # Aynı motor+beygir+yakıt+şanzıman kategorisine birden fazla FARKLI TSB tipi
        # (ör. farklı kasa: hatchback/sedan/coupe) eşleşebilir; hepsi teknik olarak
        # aynı güç aktarma organına sahip olduğu için reddetmek yerine min-max'ı
        # bandın kendisi olarak alıyoruz. Bant çok genişlerse zaten validate.py'nin
        # 'fiyat-bandi' uyarısı (oran > 2.2) bunu görünür kılar.
        band = [round(values[0] / 1000), round(values[-1] / 1000)]
        if band[0] >= band[1]:
            band[1] = band[0] + max(1, round(band[0] * 0.05))
        results.append((path, car, band, m, tip_adi_set))

    print(f"TSB satırı: {len(tsb_rows)}, araç: {len(cars)}, eşleşen araç: {len(results)}")
    for path, car, band, m, tip_adi_set in sorted(results, key=lambda r: r[1]["id"]):
        old = car["price_band_k_try"]
        print(f"  {car['id']:38s} eski={str(old):>14s} yeni={str(band):>14s}  n={len(m):<2d}")
        for t in tip_adi_set:
            print(f"      <- {t}")

    if not args.write:
        print("\n(yazmadan çalıştırıldı; uygulamak için --write ver)")
        return 0

    for path, car, band, m, tip_adi_set in results:
        car["price_band_k_try"] = band
        car["price_reference"] = {
            "as_of": meta["as_of"],
            "method": meta["method"],
            "source": meta["source_id"],
            "marketplace": "TSB Kasko Değer Listesi",
            "price_semantics": meta["price_semantics"],
            "group_id": " | ".join(tip_adi_set),
            "observations": len(m),
            "median_try": round(sum(v["value_try"] for v in m) / len(m)),
            "km_median": None,
            "quality": "tsb_kasko_official_valuation_single_point_per_year",
        }
        path.write_text(json.dumps(car, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{len(results)} araç kaydına TSB kasko bandı yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
