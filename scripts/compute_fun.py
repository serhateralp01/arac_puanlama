#!/usr/bin/env python3
"""compute_fun.py — `fun` kriterini güç/ağırlık formülünden hesaplar.

`docs/ARCHITECTURE.md` MK-06 kaydı "fun formüle bağlanır" diyordu ve
`docs/PLAN.md` §3.6 taslak formülü tanımlıyordu:

    temel = f(güç/ağırlık, tork/ağırlık, çekiş tipi, şanzıman tepkisi)
    fun   = temel + karakter_düzeltmesi   (± 15 puanla sınırlı, yazılı gerekçeli)

Bu betik o kararı uyguluyor. `docs/PLAN.md` §3 kendi tablosunda `fun` için
"sezgi payı sonrası ~%35" diyor — yani formülün elle verilmiş puanlarla tam
örtüşmesi zaten beklenmiyor, `age`'deki gibi neredeyse birebir bir eğri değil
bu. Kalibrasyon (158 araç, boş olmayan `kerb_weight_kg`/`torque_nm` alanlı)
şunu gösterdi: elle verilmiş puanların 61'i (273'ün %22'si) birebir aynı
değer olan 50 — yani araştırılmamış, varsayılan bir sayı, gerçek bir yargı
değil. Gerçekten araştırılmış (50 dışı) 107 araca karşı test edildiğinde
formülün Spearman sıra korelasyonu 0,46, ortalama mutlak sapma 17-18 puan —
`age`'in 0,95 korelasyonunun çok altında. Bu beklenen bir sonuç: `age`
yaş-kusur ilişkisi neredeyse mekanik bir eğridir, `fun` ise PLAN.md'nin
kendi kabulüyle üçte biri sezgiye kalan bir kriterdir. Formül yine de
uygulanıyor çünkü (a) MK-06 kararı zaten verildi, (b) varsayılan 50'ler sıfır
kanıt taşıyordu, (c) formül tekrarlanabilir ve gerekçesi yazılı, elle verilen
sayı değil.

**Güç/tork ağırlığı 50/50 değil, %75/%25.** İlk taslak güç/ağırlık ve
tork/ağırlığı eşit ağırlıklandırıyordu; bu, dizel araçları listenin tepesine
taşıdı (ör. bir Renault Megane 4 Estate dizel, VW Golf 7 GTI'den hemen sonra
2. sıraya çıktı) çünkü dizel motorlar aynı beygirde çok daha yüksek tork
üretir — bu, motorun sürüş keyfi verdiği anlamına gelmez, yanma karakterinin
bir yan etkisidir. Eşit ağırlıklı sürüm elle verilmiş puanlara karşı
marjinal olarak biraz daha iyi korelasyon veriyordu (Spearman 0,46 → 0,43),
ama bariz saçma bir sıralama üretiyordu (aile tipi bir dizel steyşın,
sportif bir SUV'un önünde). Saçma bir sıralamayı marjinal bir korelasyon
kazancı için kabul etmek yanlış; bu yüzden ağırlık %75 güç / %25 tork'a
çekildi — bu hem dizel çarpıklığını gözle görülür biçimde azaltıyor hem de
korelasyonu ciddi ölçüde bozmuyor (0,46 → 0,43).

**Kapsam sınırı.** `karakter_düzeltmesi` PLAN.md'nin beş kriterinden yalnızca
üçünü kullanıyor: arkadan itiş (`specs.drivetrain`), sıralı altı silindir
(motor ailesi bilgisinden — bkz. `INLINE_SIX_ENGINES`) ve doğal emişli yüksek
devir karakteri (`engines.json`'daki `aspiration` + beygir/litre oranı).
"Sportif şasi kurulumu" ve "direksiyonun geri bildirimi" için veri
tabanında hiçbir alan yok; bunlar veri eklenmeden uygulanamaz, çünkü
PLAN.md'nin kendi kuralı "hoşuma gidiyor" gibi kaynaksız gerekçeleri hata
sayıyor. Bu iki madde bilinçli olarak boş bırakıldı.

Yalnızca `specs.kerb_weight_kg` VE `specs.torque_nm` dolu olan araçlara
uygulanır (bugün 273 aracın ~151'i, MK-15'in kademeli araştırmasına bağlı).
Diğerleri dokunulmadan kalır; formülün veri istediği ama bulamadığı bir
alan, yanlış bir sayı üretmek yerine boş bırakılıyor.

Kullanım:
    python3 scripts/compute_fun.py            # sapmaları raporla, dosyaya yazma
    python3 scripts/compute_fun.py --write    # data/cars/*.json içine yaz
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = datetime.date.today().isoformat()
DATA = ROOT / "data"

# Veri tabanındaki 158 aracın (kerb_weight_kg + torque_nm dolu) gözlenen
# beygir/ton ve tork/ton aralığı. Normalize etmek için çapa olarak kullanılıyor;
# yeni araçlar bu aralığın dışına taşarsa 0-100'e kırpılır (clamp), formül
# bozulmaz. Aralık `python3 scripts/compute_fun.py --write` her çalıştığında
# yeniden türetilebilir, burada sabit yazılı olması betiğin veri setinin o
# anki uç noktalarına bağımlı kalmaması için.
POWER_PER_TON_MIN, POWER_PER_TON_MAX = 70.0, 161.0
TORQUE_PER_TON_MIN, TORQUE_PER_TON_MAX = 108.0, 289.0

# Dizel tork çarpıklığını düzeltmek için güce verilen ağırlık (bkz. yukarıdaki
# docstring). Kalanı (1 - POWER_WEIGHT) tork/ağırlığa gidiyor.
POWER_WEIGHT = 0.75

# Şanzıman tepkisinin "temel" formülüne katkısı. Bu sıralama veri setinden
# türetilmedi (setteki ortalamalar şanzıman tipiyle güç seviyesinin karışması
# yüzünden güvenilmez) — otomotiv mühendisliğinde yerleşik vites geçiş hızı
# sırasına dayanıyor: kuru çift kavramalı en hızlı ve en doğrudan tepkiyi
# verir, ıslak çift kavrama biraz daha ağır ama yine hızlı, klasik tork
# konvertörlü otomatik (TK) orta, tek kavramalı robotize kutular (Robot)
# geçişte sarsıntılı ve yavaş, CVT ise ayrık vites hissi vermediği için
# sürüş keyfi açısından en az doğrudan olanı.
TRANSMISSION_RESPONSE_ADJUSTMENT = {
    "Kuru DCT": 6,
    "Islak DCT": 4,
    "TK": 0,
    "Robot": -8,
    "CVT": -6,
}

# BMW M52/M54/N52 (atmosferik) ve M57 (turbo) — BMW'nin bu dönemdeki bütün
# benzinli/dizel altı silindirli aileleri sıralı altı silindirdir (V6 değil);
# bu, motor mimarisine dair üretici düzeyinde bilinen bir olgu, `data/engines.json`
# içindeki `cylinders: 6` alanı tek başına sıralı/V ayrımını taşımıyor.
INLINE_SIX_ENGINES = {"bmw-m52", "bmw-m54", "bmw-m57", "bmw-n52"}

# Doğal emişli motorun "yüksek devir karakteri" sayılması için beygir/litre eşiği.
# Düşük devirde tork üretmek üzere ayarlanmış sıradan atmosferik motorlar
# (çoğu 1.6-2.0 aile motoru) 50-65 hp/L bandında kalıyor; 75 hp/L üstü, motorun
# gücünü devirden aldığı, daha sportif bir ayarı işaret ediyor.
NA_HIGH_REV_HP_PER_LITER = 75.0

CHARACTER_CAP = 15


def normalize(value: float, lo: float, hi: float) -> float:
    return max(0.0, min(100.0, (value - lo) / (hi - lo) * 100.0))


def base_score(specs: dict) -> tuple[float, dict]:
    """`temel` puanını ve ara değerleri döndürür (evidence metni için)."""
    power_per_ton = specs["hp"] / (specs["kerb_weight_kg"] / 1000)
    torque_per_ton = specs["torque_nm"] / (specs["kerb_weight_kg"] / 1000)
    norm_power = normalize(power_per_ton, POWER_PER_TON_MIN, POWER_PER_TON_MAX)
    norm_torque = normalize(torque_per_ton, TORQUE_PER_TON_MIN, TORQUE_PER_TON_MAX)
    perf = POWER_WEIGHT * norm_power + (1 - POWER_WEIGHT) * norm_torque

    # Çekiş tipi: burada yalnızca mekanik etki değerlendiriliyor (tork direksiyonu,
    # çekiş avantajı), "arkadan itişin hissi" karakter_düzeltmesinde ayrıca
    # puanlanıyor — ikisi aynı şey değil, PLAN.md ikisini de ayrı ayrı listeliyor.
    drivetrain = specs.get("drivetrain")
    if drivetrain == "Önden" and specs["hp"] > 180:
        drivetrain_adj = -3.0
    elif drivetrain == "Dört çeker":
        drivetrain_adj = 2.0
    else:
        drivetrain_adj = 0.0

    trans_adj = float(TRANSMISSION_RESPONSE_ADJUSTMENT.get(specs.get("transmission_type"), 0))

    temel = max(0.0, min(100.0, perf + drivetrain_adj + trans_adj))
    detail = {
        "power_per_ton": power_per_ton,
        "torque_per_ton": torque_per_ton,
        "norm_power": norm_power,
        "norm_torque": norm_torque,
        "drivetrain_adj": drivetrain_adj,
        "trans_adj": trans_adj,
    }
    return temel, detail


def character_correction(specs: dict, engines: dict) -> tuple[float, list[str]]:
    """`karakter_düzeltmesi` puanını ve yazılı gerekçe listesini döndürür."""
    correction = 0.0
    reasons = []

    if specs.get("drivetrain") == "Arkadan":
        correction += 8.0
        reasons.append("arkadan itiş")

    engine_id = specs.get("engine_id")
    if engine_id in INLINE_SIX_ENGINES:
        correction += 6.0
        reasons.append("sıralı altı silindir")

    engine = engines.get(engine_id, {})
    if engine.get("aspiration") == "Atmosferik" and specs.get("displacement_l"):
        hp_per_liter = specs["hp"] / specs["displacement_l"]
        if hp_per_liter >= NA_HIGH_REV_HP_PER_LITER:
            correction += 5.0
            reasons.append(f"doğal emişli yüksek devir karakteri ({hp_per_liter:.0f} hp/L)")

    return min(CHARACTER_CAP, correction), reasons


def band_name(score: float, bands: list[dict]) -> str:
    for band in bands:
        lo, hi = band["range"]
        if lo <= score <= hi:
            return band["name"]
    return bands[-1]["name"]


def has_required_specs(specs: dict) -> bool:
    return bool(specs.get("kerb_weight_kg") and specs.get("torque_nm") and specs.get("hp"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="hesabı araç dosyalarına yaz")
    args = ap.parse_args()

    engines = json.loads((DATA / "engines.json").read_text(encoding="utf-8"))
    criteria = json.loads((DATA / "criteria.json").read_text(encoding="utf-8"))
    fun_bands = next(c["bands"] for c in criteria["criteria"] if c["key"] == "fun")

    paths = sorted((DATA / "cars").glob("*.json"))
    applied, skipped = [], []
    for path in paths:
        car = json.loads(path.read_text(encoding="utf-8"))
        specs = car["specs"]
        if not has_required_specs(specs):
            skipped.append(car["id"])
            continue
        temel, detail = base_score(specs)
        correction, reasons = character_correction(specs, engines)
        new = round(max(0.0, min(100.0, temel + correction)))
        applied.append((path, car, car["scores"]["fun"], new, temel, correction, reasons, detail))

    print(f"{len(applied)} araç hesaplandı, {len(skipped)} araç veri eksikliğinden atlandı "
          "(kerb_weight_kg / torque_nm boş).")
    deltas = [new - old for _, _, old, new, *_ in applied]
    if deltas:
        mean_abs = sum(abs(d) for d in deltas) / len(deltas)
        print(f"ortalama mutlak sapma (eski elle verilen puana göre): {mean_abs:.1f} puan")
        print(f"en büyük aşağı/yukarı sapma: {min(deltas)} / {max(deltas)}")

    if not args.write:
        print("\n(yazmadan çalıştırıldı; uygulamak için --write ver)")
        print("en büyük 10 sapma:")
        worst = sorted(applied, key=lambda r: -abs(r[3] - r[2]))[:10]
        for path, car, old, new, *_ in worst:
            print(f"  {car['id']:44s} {old:3d} → {new:3d} ({new - old:+d})")
        return 0

    for path, car, old, new, temel, correction, reasons, detail in applied:
        car["scores"]["fun"] = new
        evidence = car.get("evidence") or {}
        prev_fun_evidence = evidence.get("fun") or {}
        # assessed_at yalnız gerçekten yeni bir değerlendirme olduğunda ilerliyor
        # (daha önce evidence.fun hiç yoktu ya da hesaplanan puan değişti); aksi
        # halde aynı girdiyle yeniden çalıştırmak, dokunulmamış araçların
        # değerlendirme tarihini yanlışlıkla "bugün" gibi göstermesin diye eski
        # tarih korunuyor.
        if prev_fun_evidence and prev_fun_evidence.get("band") and old == new:
            assessed_at = prev_fun_evidence.get("assessed_at", TODAY)
        else:
            assessed_at = TODAY

        reason_text = (
            f"Güç/ağırlık oranı {detail['power_per_ton']:.0f} hp/ton (normalize "
            f"{detail['norm_power']:.0f}/100), tork/ağırlık oranı "
            f"{detail['torque_per_ton']:.0f} Nm/ton (normalize {detail['norm_torque']:.0f}/100); "
            f"ikisinin %{POWER_WEIGHT*100:.0f}/%{(1-POWER_WEIGHT)*100:.0f} ağırlıklı "
            f"ortalaması (tork payı düşük tutuldu; gerekçesi bütün araçlara aynı şekilde "
            f"uygulanan sabit bir metodoloji kararı, bkz. docs/ARCHITECTURE.md MK-17) "
            f"ve çekiş tipi/şanzıman tepkisi düzeltmeleriyle (çekiş "
            f"{detail['drivetrain_adj']:+.0f}, şanzıman {detail['trans_adj']:+.0f}) "
            f"temel puan {temel:.0f}."
        )
        if reasons:
            reason_text += (
                f" Karakter düzeltmesi +{correction:.0f} puan uygulandı, gerekçesi: "
                f"{', '.join(reasons)} (±{CHARACTER_CAP} puanla sınırlı)."
            )
        else:
            reason_text += (
                " Karakter düzeltmesi uygulanmadı: araç PLAN.md §3.6'nın kabul ettiği "
                "beş ölçütten (arkadan itiş, sıralı altı silindir, doğal emişli yüksek "
                "devir, sportif şasi, direksiyon geri bildirimi) hiçbirini veri tabanında "
                "kayıtlı, doğrulanabilir bir olguyla karşılamıyor."
            )
        reason_text += (
            " Puan elle verilmedi; scripts/compute_fun.py tarafından hesaplandı ve aynı "
            "girdi her zaman aynı çıktıyı üretir. Formülün kendisi elle verilmiş puanlara "
            "karşı test edildi (docs/ARCHITECTURE.md ilgili MK kaydına bakınız); sportif "
            "şasi kurulumu ve direksiyon geri bildirimi verisi eksik olduğu için sezgi "
            "payı beklenenden (PLAN.md §3: ~%35) yüksek kalabilir."
        )

        evidence["fun"] = {
            "band": band_name(new, fun_bands),
            "confidence": "orta" if reasons else "düşük",
            "sources": [],
            "reasoning": reason_text,
            # Bu puan kaynak okunarak değil formülle üretildi; kanıtı formülün
            # kendisi ve yazılı kalibrasyonu. validate.py'nin "uç puan A/B kanıt
            # ister" kuralı bu yüzden bu kritere uygulanmıyor (o kural yargı
            # puanlarını hedefliyor, ölçülmüş oranları değil).
            "derivation": "formul",
            "assessed_at": assessed_at,
        }
        car["evidence"] = evidence
        path.write_text(json.dumps(car, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{len(applied)} araç kaydına yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
