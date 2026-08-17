#!/usr/bin/env python3
"""fix_catalog_labels.py — katalog adı ile motor hacmi çelişkisini RAPORLAR.

**Bu betik veri yazmaz.** Adı, yazan bir düzeltme aracı olarak tasarlandı; yazma
yeteneği, aşağıda anlatılan yöntem hatası bulunduğu için bilinçli olarak kaldırıldı.
Ad, bulgunun kendisini taşısın diye korundu.

**Sorun.** Terfi kapısı yeniden kurulduğunda (Y-19) 119 katalog kaydının adı, kendi
`specs.displacement_l` alanıyla çelişiyordu: "Ford Focus 1.5 Ti-VCT · 125 bg"
kaydının hacmi 1.6 L, "Honda Civic 1.4 · 182 bg" kaydının hacmi 1.5 L yazıyordu. Bu
kayıtlar terfi edemiyor, çünkü yanlış adla doğru puan vermek kullanıcıyı yanıltır.

**Denenen çözüm ve neden çöktü.** Kaydın üçüncü bir alanı var gibi görünüyordu:
`specs.engine_name` (ör. "1.6L Ti-VCT 6AT FWD (125 HP)"). Bunu bağımsız bir hakem
sayıp MK-18'in çapraz doğrulama yöntemini uygulamak istedim: hakem kaydı tutuyorsa
ad yanlıştır, adı tutuyorsa kayıt yanlıştır. Yöntem 48 kayıt için "adı düzelt" dedi.

**Ama hakem bağımsız değil.** `import_catalog.py`'nin sorgusuna bakıldığında
`e.engine_name` ile `e.displacement_cc` **aynı `engines` satırından** geliyor
(`LEFT JOIN engines e ON e.engine_id = v.engine_id`). Yani "iki alan birbirini
doğruluyor" diye okuduğum şey, tek bir kaydın kendisini tekrar etmesiydi. Gerçek
karşılaştırma iki alan arasında değil, **iki tablo arasında**: `variants.model_variant`
(ad) bir yana, `engines` satırı (hacim + açıklama) öbür yana. Hangisinin doğru olduğu
bu veriyle belirlenemiyor.

**Somut karşı örnek.** Yöntem "Hyundai i40 1.7 CRDi Executive" ve "Kia Optima 1.7
CRDi" kayıtlarını 1.6'ya çevirmek istedi. İkisi de aynı gerçek motoru (Hyundai/Kia
U2 1.7 CRDi, 136 bg) taşıyor ve bu motorun 1.7 olduğu deponun kendi
`hyundai-u2-17` ailesinde zaten kayıtlı. Yani `engines` satırının sistematik olarak
yanıldığı, adın doğru olduğu bir durum — yöntemin tam tersini söylediği yer.

**Alınan karar.** Toplu yeniden adlandırma yapılmadı. 119 kayıt çelişkili kalıyor ve
terfiye kapalı; bu, yanlış adla puanlanmış araç üretmekten iyidir. Bu kayıtların
açılması, hangi tarafın doğru olduğunu söyleyen **gerçekten dışsal** bir kaynak
(teknik künye sayfası, üretici kataloğu) gerektiriyor — yani `MANUAL_SPEC_CORRECTIONS`
desenindeki gibi kayıt kayıt, alıntılı doğrulama.

Betik hangi kaydın hangi türde çeliştiğini listeleyerek o elle araştırmanın çalışma
listesini üretiyor.

Kullanım:
    python3 scripts/fix_catalog_labels.py            # çelişki raporu
    python3 scripts/fix_catalog_labels.py --liste     # tam liste (çalışma kuyruğu)
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "catalog"


def displacement_in(text: str, require_unit: bool = False) -> float | None:
    """Metindeki motor hacmini litre olarak döndürür."""
    if not text:
        return None
    pattern = r"(\d\.\d)\s*l\b" if require_unit else r"(\d\.\d)"
    m = re.search(pattern, text, re.I)
    return float(m.group(1)) if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--liste", action="store_true", help="çelişkili kayıtların tamamını yazdır")
    args = ap.parse_args()

    rows = []
    for path in sorted(CATALOG.glob("*.json")):
        if path.name == "_sources.json":
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        for e in doc.get("entries", []):
            if e.get("scored_car_id"):
                continue
            sp = e["specs"]
            rec = sp.get("displacement_l")
            if rec is None:
                continue
            name_d = displacement_in(e["name"])
            if name_d is None or abs(name_d - rec) <= 0.05:
                continue
            engine_name = sp.get("engine_name") or ""
            arb = displacement_in(engine_name, require_unit=True)
            hp_m = re.search(r"\((\d{2,3})\s*HP\)", engine_name, re.I)
            per_record = bool(hp_m) and int(hp_m.group(1)) == sp.get("hp")
            if arb is None:
                kind = "engines satırı hacim söylemiyor"
            elif not per_record:
                kind = "engines satırı bu kayda özgü değil (genel aile etiketi)"
            elif abs(arb - rec) <= 0.05:
                kind = "engines satırı kaydı tekrarlıyor (ad ile çelişiyor)"
            else:
                kind = "engines satırı hem addan hem kayıttan farklı"
            rows.append((e["id"], e["name"], rec, engine_name, kind))

    print(f"ad ile motor hacmi çelişen, terfiye kapalı katalog kaydı: {len(rows)}")
    print()
    by_kind: dict[str, int] = {}
    for *_, kind in rows:
        by_kind[kind] = by_kind.get(kind, 0) + 1
    for k, v in sorted(by_kind.items(), key=lambda x: -x[1]):
        print(f"  {v:5d}  {k}")
    print()
    print("Bu kayıtlar OTOMATİK düzeltilemez: adın kaynağı (variants tablosu) ile")
    print("hacmin kaynağı (engines tablosu) farklı ve hangisinin doğru olduğunu")
    print("söyleyecek üçüncü, gerçekten bağımsız bir alan yok. Betiğin başındaki")
    print("dokümantasyona bakınız; açılmaları dışsal teknik künye doğrulaması ister.")

    if args.liste:
        print()
        for cid, name, rec, en, kind in rows:
            print(f"  {cid:46s} {name[:38]:38s} kayıt={rec}L  engines='{en[:30]}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
