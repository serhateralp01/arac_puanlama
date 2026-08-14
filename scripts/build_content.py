#!/usr/bin/env python3
"""build_content.py — known_issues kayıtlarından içerik taslağı üretir.

**Neden var.** `data/engines.json` ve `data/transmissions.json` içinde 300'ün üzerinde
yapılandırılmış bilinen arıza kaydı var; her biri hangi bileşen, hangi arıza, hangi
kilometrede, ne sıklıkta, hangi kaynakla bildirildiğini taşıyor. Bu, bir yıldan fazla
araştırmanın ham maddesi ama bugün yalnızca sayfa içinde küçük bir metin olarak
görünüyor. Sosyal medya içeriği, video senaryosu ve uzun biçim yazı için bu veriyi
elle yeniden yazmak hem yavaş hem de kaynağı metinden koparma riski taşıyor.

**Kapsam.** İçerik de türetilmiş bir çıktıdır: bu betik `data/`'dan hiçbir yeni olgu
üretmez, yalnızca zaten var olan `known_issues` kayıtlarını dört içerik biçimine
(kısa video senaryosu, kaydırmalı görsel metni, paylaşım dizisi, uzun biçim yazı
taslağı) döker. Her taslak, dayandığı kaynağın adını ve adresini taşır — kaynaksız
bir taslak üretilmez.

**Betik metin üretir, yayın yapmaz.** Hangi taslağın yayınlanacağına, nasıl
düzenleneceğine ve ne zaman paylaşılacağına insan karar verir. Bu betiğin işi, boş
sayfa karşısında başlamayı değil, kanıtla desteklenmiş bir ilk taslakla başlamayı
kolaylaştırmak.

**Neden build.py'nin içinde değil.** `scripts/build_pages.py` ile aynı gerekçe:
ayrı bir betik, çalışan `index.html` üretimini hiç riske atmıyor (CLAUDE.md §2).

Kullanım:
    python3 scripts/build_content.py            # icerik/ dizinini yeniden üret
    python3 scripts/build_content.py --check    # üretilmiş taslaklar güncel mi
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "icerik"


def load_json(name: str) -> dict:
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = (
        text.replace("ş", "s").replace("ç", "c").replace("ğ", "g")
        .replace("ü", "u").replace("ö", "o").replace("ı", "i")
    )
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:60]


def family_label(family_type: str, fam: dict) -> str:
    names = fam.get("names") or []
    primary = names[0] if names else fam.get("id", "?")
    if family_type == "motor":
        supplier = fam.get("supplier") or ""
        return f"{supplier} {primary}".strip()
    supplier = fam.get("supplier") or ""
    gears = fam.get("gears")
    gear_txt = f"{gears} ileri" if gears else ""
    return f"{supplier} {primary} ({gear_txt})".strip()


def onset_phrase(onset_km) -> str:
    if not onset_km:
        return "belirli bir kilometre sınırı bildirilmemiş"
    return f"genelde {onset_km:,} km civarında başlıyor".replace(",", ".")


def source_citation(issue: dict, sources: dict) -> tuple[str, str, str]:
    """İlk kaynağın (yayıncı, adres, iddia) üçlüsünü döndürür; kaynak yoksa boş döner."""
    src_ids = issue.get("sources") or []
    if not src_ids:
        return "", "", ""
    src = sources.get(src_ids[0])
    if not src:
        return "", "", ""
    return src.get("publisher", ""), src.get("url", ""), src.get("claim", "")


def render_video_script(label: str, issue: dict, publisher: str) -> str:
    onset = onset_phrase(issue.get("onset_km"))
    kaynak_satiri = f"Ekranda kaynak adı: {publisher}." if publisher else "Ekranda kaynak rozeti."
    return f"""**Kısa video senaryosu (30-40 sn)**

- **[0-3 sn — kanca]** Ekranda {label} görseli. Alt yazı: "{label} kullanılan bir araç mı alıyorsun?"
- **[3-18 sn — sorun]** Anlatıcı: "{issue.get('issue', '')}. Bu {issue.get('frequency', 'sıklığı bildirilmemiş')} bildirilen bir durum, {onset}. Ciddiyet seviyesi: {issue.get('severity', 'bildirilmemiş')}."
- **[18-28 sn — kanıt]** {kaynak_satiri} Anlatıcı: "Bu bilgiyi uydurmadık; kaynağımız {publisher or 'bağımsız bir yayın'}."
- **[28-38 sn — kapanış]** Anlatıcı: "{label}'in tam puan gerekçesi ve kaynak zinciri sitede — link biyoda."
"""


def render_carousel(label: str, issue: dict, publisher: str) -> str:
    onset = onset_phrase(issue.get("onset_km"))
    return f"""**Kaydırmalı görsel metni (5 slayt)**

1. "{label} alacaksan bunu bil 👇"
2. "{issue.get('issue', '')}"
3. "{onset.capitalize()} · Sıklık: {issue.get('frequency', 'sıklığı bildirilmemiş')} · Ciddiyet: {issue.get('severity', 'bildirilmemiş')}"
4. "Kaynak: {publisher or 'bağımsız kaynak, sitede künyesiyle birlikte'}"
5. "Tam gerekçe ve puan → sitede, link biyoda"
"""


def render_thread(label: str, issue: dict, publisher: str, url: str) -> str:
    onset = onset_phrase(issue.get("onset_km"))
    kaynak_satiri = f"Kaynak: {publisher}{' — ' + url if url else ''}" if publisher else "Kaynak sitede künyesiyle birlikte duruyor."
    return f"""**Paylaşım dizisi (X/Twitter thread, 5 gönderi)**

1/ {label} kullanan bir araç mı düşünüyorsun? Bilmen gereken bir şey var. 🧵
2/ {issue.get('issue', '')}
3/ {onset.capitalize()}. Sıklık: {issue.get('frequency', 'sıklığı bildirilmemiş')}. Ciddiyet: {issue.get('severity', 'bildirilmemiş')}.
4/ {kaynak_satiri}
5/ Bu, {label} için verdiğimiz puanın gerekçelerinden biri. Tam liste, kaynak zinciri ve diğer araçlarla kıyas sitede.
"""


def render_article(label: str, issue: dict, publisher: str, url: str, claim: str) -> str:
    onset = onset_phrase(issue.get("onset_km"))
    kaynak_cumlesi = (
        f"Bu bilgi {publisher} kaynaklı{' (' + url + ')' if url else ''}: {claim}"
        if publisher
        else "Bu bilgi sitedeki kaynak künyesinde tam olarak belgeli."
    )
    return f"""**Uzun biçim yazı taslağı**

{label} ailesinin bilinen zaaflarından biri: {issue.get('issue', '')}. {onset.capitalize()}, ve bu {issue.get('frequency', 'sıklığı bildirilmemiş')} bildirilen bir örüntü. Ciddiyet seviyesi "{issue.get('severity', 'bildirilmemiş')}" olarak sınıflandırılıyor — yani {"bu, bir bakım kalemi ötesine geçip büyük bir onarım gerektirebilir" if issue.get('severity', 'bildirilmemiş') in ("büyük onarım", "motor ölür") else "izlenmesi gereken ama genelde yönetilebilir bir kalem"}.

{kaynak_cumlesi}

İkinci el alırken bu tek başına "bu araçtan kaç" anlamına gelmiyor — servis kaydında bu kaleme dair bir işlem olup olmadığını sormak, alım öncesi kontrolün bir parçası olmalı. Tam puan gerekçesi, bu ailenin diğer bilinen sorunları ve karşılaştırmalı puanlama sitede.
"""


def render_issue(i: int, issue: dict, sources: dict, label: str) -> str:
    publisher, url, claim = source_citation(issue, sources)
    parts = [
        f"## {i}. {issue.get('issue', '')}",
        "",
        render_video_script(label, issue, publisher),
        render_carousel(label, issue, publisher),
        render_thread(label, issue, publisher, url),
        render_article(label, issue, publisher, url, claim),
        "---",
    ]
    return "\n".join(parts)


def render_family(family_type: str, fid: str, fam: dict, sources: dict) -> str:
    label = family_label(family_type, fam)
    issues = fam.get("known_issues") or []
    lines = [
        f"# {label} — içerik taslakları",
        "",
        f"Bu dosya `data/{'engines.json' if family_type == 'motor' else 'transmissions.json'}`",
        f"içindeki `{fid}` kaydının `known_issues` alanından **otomatik üretildi**",
        "(`scripts/build_content.py`). Elle düzenlenmez; kaynak değişirse yeniden üretilir.",
        "",
    ]
    for idx, issue in enumerate(issues, 1):
        lines.append(render_issue(idx, issue, sources, label))
    return "\n".join(lines) + "\n"


def build() -> tuple[int, int]:
    engines = load_json("engines.json")
    transmissions = load_json("transmissions.json")
    sources = load_json("sources.json")

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "motor").mkdir(parents=True)
    (OUT / "sanziman").mkdir(parents=True)

    total_issues = 0
    index_rows = {"motor": [], "sanziman": []}

    for family_type, families, subdir in (
        ("motor", engines, "motor"),
        ("sanziman", transmissions, "sanziman"),
    ):
        for fid, fam in sorted(families.items()):
            if fid.startswith("_"):
                continue
            issues = fam.get("known_issues") or []
            if not issues:
                continue
            content = render_family(family_type, fid, fam, sources)
            (OUT / subdir / f"{fid}.md").write_text(content, encoding="utf-8")
            total_issues += len(issues)
            label = family_label(family_type, fam)
            index_rows[subdir].append((label, fid, len(issues)))

    index_lines = [
        "# İçerik taslakları — otomatik üretildi",
        "",
        "Bu dizin `scripts/build_content.py` tarafından `data/engines.json` ve",
        "`data/transmissions.json` içindeki `known_issues` kayıtlarından üretildi.",
        "Her taslak, dayandığı kaynağın adını ve adresini taşır. Betik yayın yapmaz —",
        "hangi taslağın kullanılacağına insan karar verir. Yeniden üretmek için:",
        "",
        "    python3 scripts/build_content.py",
        "",
        f"**Toplam: {total_issues} arıza kaydı için taslak, "
        f"{len(index_rows['motor']) + len(index_rows['sanziman'])} dosyada.**",
        "",
        "## Motor aileleri",
        "",
    ]
    for label, fid, n in index_rows["motor"]:
        index_lines.append(f"- [{label}](motor/{fid}.md) — {n} kayıt")
    index_lines += ["", "## Şanzıman kutuları", ""]
    for label, fid, n in index_rows["sanziman"]:
        index_lines.append(f"- [{label}](sanziman/{fid}.md) — {n} kayıt")

    (OUT / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return total_issues, len(index_rows["motor"]) + len(index_rows["sanziman"])


def check() -> bool:
    """Üretilmiş taslakların bugünkü veriyle uyumlu olup olmadığını denetler."""
    global OUT
    tmp_out = OUT.with_name("icerik.check-tmp")
    if tmp_out.exists():
        shutil.rmtree(tmp_out)

    real_out = OUT
    OUT = tmp_out
    try:
        build()
    finally:
        OUT = real_out

    if not real_out.exists():
        print("HATA: icerik/ dizini yok, önce `python3 scripts/build_content.py` çalıştırın.", file=sys.stderr)
        shutil.rmtree(tmp_out)
        return False

    ok = True
    for sub in ("motor", "sanziman", "."):
        real_dir = real_out if sub == "." else real_out / sub
        tmp_dir = tmp_out if sub == "." else tmp_out / sub
        real_files = {p.name for p in real_dir.glob("*.md")}
        tmp_files = {p.name for p in tmp_dir.glob("*.md")}
        if real_files != tmp_files:
            print(f"HATA: {sub} dizininde dosya listesi güncel değil.", file=sys.stderr)
            ok = False
            continue
        for name in tmp_files:
            if (real_dir / name).read_text(encoding="utf-8") != (tmp_dir / name).read_text(encoding="utf-8"):
                print(f"HATA: {sub}/{name} güncel değil, yeniden üretilmeli.", file=sys.stderr)
                ok = False

    shutil.rmtree(tmp_out)
    return ok


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        if check():
            print("icerik/ güncel.")
            sys.exit(0)
        sys.exit(1)

    total_issues, n_files = build()
    print(f"icerik/ yazıldı: {total_issues} arıza kaydı için taslak, {n_files} dosyada.")


if __name__ == "__main__":
    main()
