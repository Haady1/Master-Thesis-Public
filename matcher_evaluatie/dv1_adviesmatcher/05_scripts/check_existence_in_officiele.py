"""Bestaat het gemiste rapport wel in de officiele bekendmakingen? (corpus-gat vs matcher-miss)

!! WAARSCHUWING - METHODE ONBETROUWBAAR (2026-06-05) !!
Validatie op 7 bekend-aanwezige rapporten vond er slechts 1/7 terug: de substring-zoektocht
op lange woorden geeft veel vals-negatieven (lange samengestelde woorden worden bij
PDF-extractie anders afgebroken/gespeld; datumvenster mogelijk te krap). De uitkomst
"0/43 = corpus-gat" is DAAROM NIET GELDIG. Gebruik dit script niet voor conclusies tot
er een tekstindex (pg_trgm GIN op content_text) bestaat voor een snelle, betrouwbare
full-text bestaan-check.

Wat dit doet
------------
Voor elk grondwaarheid-rapport dat de matcher NIET vond, zoekt dit script in de hele
public.overheidsdocumenten (document_type='Bijlage') of er toch een kopie bestaat.
Per rapport bouwen we een distinctief patroon van 8 gespreide lange woorden (in volgorde,
met wildcards ertussen), robuust tegen OCR-/afbreekverschillen. Treffers bevestigen we
met tekst-Jaccard. Zo splitsen we:
- corpus-gat:   rapport staat niet in de officiele bekendmakingen -> miss is geen matcher-fout.
- matcher-miss: rapport staat er wel, maar de retrieval vond het niet -> echte matcher-fout.

In-/uitvoer
-----------
Inputs: report_hits_<label>.jsonl (uit match_hits.py) + corpus.adviesdocument_teksten.
Outputs: stdout + existence_<label>.csv.

Read-only t.o.v. de database.

"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import sys
from pathlib import Path

import asyncpg

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pg_database.config import db_config
from matcher.advies.evaluatie.text_fingerprint import fingerprint, jaccard, normalize_tokens

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "artifacts"

def distinctive_patterns(text: str, n: int = 3) -> list[str]:
    """Geef tot n goedkope substring-patronen: de langste, meest distinctieve woorden.

    Enkelvoudige substrings ('%woord%') zijn veel goedkoper te scannen dan geordende
    wildcard-ketens. We pakken de langste unieke woorden (lange Nederlandse samenstellingen
    zijn zeer distinctief); eventuele losse valse treffers vangen we daarna met Jaccard af.
    """
    toks = sorted({t for t in normalize_tokens(text) if len(t) >= 10}, key=len, reverse=True)
    if len(toks) < 1:
        toks = sorted({t for t in normalize_tokens(text) if len(t) >= 8}, key=len, reverse=True)
    return [f"%{t}%" for t in toks[:n]]

async def main() -> None:
    ap = argparse.ArgumentParser(description="Check bestaan in officiele bekendmakingen")
    ap.add_argument("--label", default="runA_det")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--jaccard", type=float, default=0.4)
    ap.add_argument("--query-timeout", type=int, default=30,
                    help="Harde limiet per rapport-query (s). Trage queries tellen conservatief als niet-gevonden.")
    ap.add_argument("--only-missed", action="store_true", default=True)
    args = ap.parse_args()

    reports = [json.loads(l) for l in (args.out_dir / f"report_hits_{args.label}.jsonl")
               .read_text(encoding="utf-8").splitlines() if l.strip()]
    targets = [r for r in reports if not r.get("hit_text")] if args.only_missed else reports
    advies_ids = [r["advies_id"] for r in targets]
    print(f"Te checken (gemist) rapporten: {len(advies_ids)}", flush=True)

    conn = await asyncpg.connect(db_config.asyncpg_dsn)
    try:
        await conn.execute(f"SET statement_timeout = '{int(args.query_timeout)}s'")
        meta_rows = await conn.fetch(
            "SELECT cd.id AS advies_id, dm.document_datum_parsed AS d, "
            "       coalesce(t.text_clean, t.text, t.text_digital, t.text_ocr) AS body "
            "FROM corpus.adviesdocumenten cd "
            "JOIN pipeline.v_canonical_document_metadata dm ON cd.id = dm.document_id "
            "LEFT JOIN corpus.adviesdocument_teksten t ON t.document_id = cd.id "
            "WHERE cd.id = ANY($1::int[])",
            advies_ids,
        )
        bodies = {r["advies_id"]: r["body"] for r in meta_rows}
        dates = {r["advies_id"]: r["d"] for r in meta_rows}

                                                                                              
                                                                                             
        PER_REPORT_SQL = (
            "SELECT id, title, content_text FROM public.overheidsdocumenten "
            "WHERE document_type='Bijlage' AND length(coalesce(content_text,''))>500 "
            "AND ($2::date IS NULL OR date_published BETWEEN $2 AND $3) "
            "AND content_text ILIKE ANY($1::text[]) LIMIT 60"
        )
        out = []
        exists = 0
        from datetime import timedelta
        for i, aid in enumerate(advies_ids, start=1):
            pats = distinctive_patterns(bodies.get(aid) or "")
            gt_fp = fingerprint(bodies.get(aid) or "")
            best_j, best_id, best_title = 0.0, None, None
            if pats:
                d = dates.get(aid)
                lo = (d - timedelta(days=250)) if d else None
                hi = (d + timedelta(days=250)) if d else None
                try:
                    rows = await conn.fetch(PER_REPORT_SQL, pats, lo, hi)
                except asyncpg.exceptions.QueryCanceledError:
                    rows = []
                for h in rows:
                    j = jaccard(gt_fp, fingerprint(h["content_text"] or ""))
                    if j > best_j:
                        best_j, best_id, best_title = j, h["id"], h["title"]
            found = best_j >= args.jaccard
            exists += int(found)
            out.append({"advies_id": aid, "bestaat_in_officiele": found,
                        "best_jaccard": round(best_j, 4), "officiele_id": best_id,
                        "officiele_titel": (best_title or "")[:120]})
            if i % 5 == 0:
                print(f"  ...{i}/{len(advies_ids)} verwerkt (tot nu gevonden: {exists})", flush=True)
    finally:
        await conn.close()

    csv_path = args.out_dir / f"existence_{args.label}.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    n = len(advies_ids)
    print("")
    print(f"=== Bestaan in officiele bekendmakingen (van {n} gemiste rapporten) ===")
    print(f"  WEL aanwezig (matcher-miss):   {exists}/{n}")
    print(f"  NIET gevonden (corpus-gat):    {n - exists}/{n}")
    print(f"[out] {csv_path}")

if __name__ == "__main__":
    asyncio.run(main())
