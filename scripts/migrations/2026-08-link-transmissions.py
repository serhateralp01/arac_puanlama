#!/usr/bin/env python3
"""Araçları data/transmissions.json içindeki şanzıman kayıtlarına bağlar.

Bu, tek seferlik bir göç betiğidir. Bir kez çalıştırıldı ve tekrarlanabilirliği için
depoda duruyor; normal çalışma akışının parçası değildir.

Betik yeni bir iddia üretmiyor. Yalnızca araç kayıtlarının `tag` alanında zaten yazılı
olan kutu adlarını normalize edip `specs.transmission_id` alanına taşıyor. Kutu adı
`tag` içinde açıkça geçmiyorsa ya da birden fazla kutu ihtimali belirtilmişse (örneğin
"ZF 5HP / GM 5L40E" gibi) araç bilinçli olarak bağlanmadan bırakılıyor. Bu araçların
kutusu, kaynağa dayalı araştırmayla ayrı ayrı belirlenecek.

Kullanım: python3 scripts/migrations/2026-08-link-transmissions.py
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"

# Sıra önemlidir: en özgül kalıp önce denenir. Örneğin "ıslak DQ250 S tronic" ifadesi
# hem DQ250 hem S tronic içerdiği için önce DQ250 kalıbına yakalanmalıdır.
RULES: list[tuple[str, str]] = [
    (r"Getrag 7DCT300", "getrag-7dct300"),
    (r"6DCT450|ıslak Powershift", "getrag-6dct450"),
    (r"DPS6|KURU Powershift", "ford-dps6"),
    (r"DQ250", "vag-dq250"),
    (r"DQ200", "vag-dq200"),
    (r"S tronic", "vag-s-tronic-islak"),
    (r"Multitronic", "vag-multitronic"),
    (r"Multidrive", "toyota-multidrive"),
    (r"X-Tronic", "nissan-xtronic"),
    (r"\bETG\b", "psa-etg"),
    (r"\bAL4\b", "psa-al4"),
    (r"EAT6", "aisin-eat6"),
    (r"AF40", "aisin-af40"),
    (r"TF-80", "aisin-tf80"),
    (r"Aisin Geartronic", "aisin-geartronic"),
    (r"Aisin 6 TK", "aisin-aw60t"),
    (r"7G-DCT", "mb-7g-dct"),
    (r"7G-Tronic|7G/5G-Tronic", "mb-7g-tronic"),
    (r"5G-Tronic|· 5G ·", "mb-5g-tronic"),
    (r"4G-Tronic", "mb-4g-tronic"),
    (r"\bTCT\b", "alfa-tct"),
    (r"KURU EDC|EDC çift kavrama", "renault-edc-kuru"),
    (r"7DCT", "hyundai-7dct"),
]

# Birden fazla kutu ihtimali belirten kalıplar. Bu araçlar bağlanmadan bırakılır,
# çünkü hangi kutunun takılı olduğu ilan bazında değişiyor ve veriye tek bir kimlik
# yazmak yanlış bir kesinlik iddiası olurdu.
AMBIGUOUS = re.compile(r"ZF 5HP / GM 5L40E|ZF/GM|GM/ZF|ZF 4/5|Multitronic CVT veya Tiptronic")

# Yalnızca `tag` alanından çıkarılamayan, ancak veride zaten bulunan başka bir alanla
# kesinleşen eşleşmeler.
def special_case(car: dict) -> str | None:
    tag = car["tag"]
    tx = car["specs"]["transmission_type"]

    # Volvo'da "Powershift" iki ayrı kutuyu birden anlatıyor. Hangisi olduğu, veride
    # zaten bulunan şanzıman tipi alanından kesinleşiyor.
    if "Powershift" in tag and "Volvo" in car["name"]:
        return "getrag-6dct450" if tx == "Islak DCT" else "volvo-powershift-kuru"

    # Fiat Egea dizelde kutu adı yazılmamış ama üretici ve tip birlikte tek bir kutuya
    # işaret ediyor.
    if "Egea" in car["name"] and tx == "Kuru DCT":
        return "fiat-c635-ddct"

    if AMBIGUOUS.search(tag):
        return None

    # ZF kutuları vites sayısıyla ayrışıyor.
    if re.search(r"ZF 5HP|ZF 5 ileri", tag):
        return "zf-5hp"
    if re.search(r"ZF 6 ileri|ZF tiptronic", tag, re.IGNORECASE):
        return "zf-6hp"

    return None


def resolve(car: dict) -> str | None:
    tag = car["tag"]
    if AMBIGUOUS.search(tag):
        return None
    for pattern, box_id in RULES:
        if re.search(pattern, tag, re.IGNORECASE):
            return box_id
    return special_case(car)


def main() -> None:
    registry = json.loads((DATA / "transmissions.json").read_text(encoding="utf-8"))
    known = {k for k in registry if not k.startswith("_")}

    linked: dict[str, list[str]] = {}
    unlinked: list[str] = []

    for path in sorted((DATA / "cars").glob("*.json")):
        car = json.loads(path.read_text(encoding="utf-8"))
        box_id = special_case(car) or resolve(car)

        if box_id is None:
            unlinked.append(f"{car['name']}  ({car['tag']})")
            car["specs"].setdefault("transmission_id", None)
        else:
            assert box_id in known, f"kayıtta olmayan kutu: {box_id}"
            car["specs"]["transmission_id"] = box_id
            linked.setdefault(box_id, []).append(car["name"])

        path.write_text(
            json.dumps(car, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    total = sum(len(v) for v in linked.values())
    print(f"{total} araç bir kutu kaydına bağlandı, {len(unlinked)} araç bağlanmadan kaldı.\n")
    for box_id in sorted(linked, key=lambda k: -len(linked[k])):
        print(f"  {box_id:26} {len(linked[box_id])} araç")
    print("\nBağlanmayan araçlar (kutu adı tag alanında yazmıyor veya birden fazla ihtimal var):")
    for name in unlinked:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
