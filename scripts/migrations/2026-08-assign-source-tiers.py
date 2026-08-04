#!/usr/bin/env python3
"""68 kaynağa güven seviyesi (A/B/C) atar.

Tek seferlik göç betiğidir; bir kez çalıştırıldı, tekrarlanabilirliği için depoda
duruyor. Tier tanımları docs/PLAN.md M-2'de yazılı:

  A — sayısal, kurumsal, örneklem tabanlı
  B — bağımsız teknik analiz veya çoklu bağımsız kullanıcı örüntüsü
  C — tekil anekdot, tek forum mesajı, ticari blog

Atama iki adımda yapılıyor. Önce her kaynağın import sırasında zaten hesaplanmış
`type` alanına göre bir varsayılan tier veriliyor (aşağıdaki DEFAULT_TIER_BY_TYPE).
Sonra, `type` tek başına yeterli ayrımı sağlamadığı durumlar için OVERRIDES ile elle
düzeltme yapılıyor — bunun tek örneği `complaint-aggregator` tipi: bir kaynağın
"çoklu konu başlığı" ifadesiyle birden fazla bağımsız şikayeti topladığı açıkça
belirtiliyorsa B, tek bir konu veya tek bir kullanıcı deneyimine dayanıyorsa C.

Bu betik nihai bir karar değil, ilk geçiş. Her tier atamasının doğruluğu, o kaynak
gerçekten kullanıldığında (bir puanın gerekçesi olarak) tekrar gözden geçirilecek.

Kullanım: python3 scripts/migrations/2026-08-assign-source-tiers.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
SOURCES_PATH = ROOT / "data" / "sources.json"

DEFAULT_TIER_BY_TYPE = {
    "official-inspection-data": "A",  # TÜV NORD gibi kurumsal, sayısal veri
    "owner-survey": "A",              # TrueDelta gibi örneklem tabanlı sahip anketi
    "spec-database": "A",             # auto-data.net gibi doğrulanmış teknik veri
    "independent-analyst": "B",       # And Çetin gibi bağımsız teknik analiz
    "encyclopedia": "B",              # Wikipedia/NamuWiki, kaynak gösteren derleme
    "trade-press": "B",               # profesyonel otomotiv yayıncılığı, tekil anekdot değil
    "complaint-aggregator": "B",      # varsayılan; tekil ise aşağıda C'ye çekiliyor
    "crowd-wiki": "C",                # kullanıcı katkılı, denetimsiz
    "forum": "C",                     # tek konu başlığı, tek topluluk deneyimi
    "trade-blog": "C",                # tek yazı, editoryal denetimi belirsiz
    "unknown": "C",                   # tip tespit edilemedi, temkinli varsayılan
}

# Yalnızca "type" alanının ayrım için yetersiz kaldığı kaynaklar. Kural: publisher
# alanında "çoklu konu başlığı" gibi açık bir çoğulluk işareti yoksa, bir
# complaint-aggregator kaydı tek kaynak sayılır ve C'ye çekilir.
OVERRIDES = {
    "audioil": "C",  # "Şikayetvar / vwturk" — çoklu başlık işareti yok, tekil referans
}


def main() -> None:
    sources = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))

    changed = 0
    for sid, src in sources.items():
        tier = OVERRIDES.get(sid) or DEFAULT_TIER_BY_TYPE.get(src["type"])
        if tier is None:
            raise SystemExit(f"`{sid}` için tip eşlemesi yok: {src['type']!r}")
        if src.get("tier") != tier:
            src["tier"] = tier
            changed += 1

    SOURCES_PATH.write_text(
        json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    from collections import Counter

    dist = Counter(s["tier"] for s in sources.values())
    print(f"{changed} kaynağa tier atandı.\n")
    for tier in ("A", "B", "C"):
        print(f"  {tier}: {dist[tier]} kaynak")


if __name__ == "__main__":
    main()
