"""Betrouwbaar bepalen welke website-rapporten echt in de officiele bekendmakingen staan.

Wat dit doet
------------
Streamt alle Bijlage-documenten uit public.overheidsdocumenten (eerste 20.000 tekens) en
matcht ze met tekst-Jaccard tegen de full-set website-rapporten (groundtruth_full_fp-basis,
hier opnieuw berekend op dezelfde 20.000-teken-basis voor een eerlijke vergelijking).
Gebruikt een omgekeerde shingle-index zodat elke bijlage maar één keer hoeft te worden
verwerkt. Dit vervangt de onbetrouwbare substring-bestaan-check (die 1/7 haalde).

Waarom
------
Voor een ZUIVERE recall-test willen we alleen rapporten waarvan aantoonbaar een kopie in de
officiele bekendmakingen bestaat. Dan is elke gemiste = echte matcher-miss, geen corpus-gat.

In-/uitvoer
-----------
Inputs: corpus.adviesdocument_teksten (rapportteksten) + public.overheidsdocumenten (bijlagen).
Outputs: presence_full.csv (per rapport: aanwezig, beste officiele id, jaccard).
Validatie: print of de bekende-aanwezige hits (uit report_hits) ook als aanwezig uitkomen.

Read-only t.o.v. de database.

"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import asyncpg

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pg_database.config import db_config
from matcher.advies.evaluatie.text_fingerprint import fingerprint

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "artifacts"
PREFIX_CHARS = 20000

async def main() -> None:
    ap = argparse.ArgumentParser(description="Streaming presence-scan (Jaccard)")
    ap.add_argument("--college-id", type=int, action="append", default=[18, 21, 30, 15, 31])
    ap.add_argument("--jaccard", type=float, default=0.4)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = ap.parse_args()

    conn = await asyncpg.connect(db_config.asyncpg_dsn)
    try:
        await conn.execute("SET statement_timeout = '0'")
                                                                                          
        rep_rows = await conn.fetch(
            "SELECT cd.id AS advies_id, cd.adviescollege_id, "
            "       LEFT(coalesce(t.text_clean, t.text, t.text_digital, t.text_ocr), $2) AS body "
            "FROM corpus.adviesdocumenten cd "
            "JOIN pipeline.v_canonical_document_classificatie dc ON cd.id = dc.document_id "
            "JOIN pipeline.v_canonical_document_metadata dm ON cd.id = dm.document_id "
            "LEFT JOIN corpus.adviesdocument_teksten t ON t.document_id = cd.id "
            "WHERE cd.adviescollege_id = ANY($1::int[]) "
            "  AND dc.final_sub_category='ADVIESRAPPORT' AND dc.detected_language='nl' "
            "  AND dm.document_datum_parsed BETWEEN '2005-01-01' AND '2024-12-31' "
            "  AND cd.download_url IS NOT NULL "
            "  AND cd.download_url !~* '(officielebekendmakingen|overheid\\.nl|open\\.overheid|rijksoverheid|tweedekamer|eerstekamer)'",
            args.college_id, PREFIX_CHARS,
        )
        rep_fp: dict[int, set] = {}
        for r in rep_rows:
            fp = fingerprint(r["body"])
            if len(fp) >= 20:
                rep_fp[r["advies_id"]] = fp
        print(f"Rapporten (full-set) met bruikbare fingerprint: {len(rep_fp)}", flush=True)

                                                     
        inv: dict[int, list[int]] = defaultdict(list)
        for aid, fp in rep_fp.items():
            for sh in fp:
                inv[sh].append(aid)
        rep_size = {aid: len(fp) for aid, fp in rep_fp.items()}
        best: dict[int, tuple[float, str | None]] = {aid: (0.0, None) for aid in rep_fp}

                                                                        
        print("Streamen van bijlagen...", flush=True)
        processed = 0
        async with conn.transaction():
            cur = await conn.cursor(
                "SELECT id, LEFT(content_text, $1) AS ct FROM public.overheidsdocumenten "
                "WHERE document_type='Bijlage' AND length(coalesce(content_text,''))>500",
                PREFIX_CHARS,
            )
            while True:
                batch = await cur.fetch(500)
                if not batch:
                    break
                for row in batch:
                    bfp = fingerprint(row["ct"])
                    if len(bfp) < 20:
                        continue
                    counts: Counter = Counter()
                    for sh in bfp:
                        hit = inv.get(sh)
                        if hit:
                            for aid in hit:
                                counts[aid] += 1
                    blen = len(bfp)
                    for aid, inter in counts.items():
                        if inter < 20:
                            continue
                        jac = inter / (rep_size[aid] + blen - inter)
                        if jac > best[aid][0]:
                            best[aid] = (jac, row["id"])
                processed += len(batch)
                if processed % 10000 == 0:
                    present = sum(1 for v in best.values() if v[0] >= args.jaccard)
                    print(f"  ...{processed} bijlagen verwerkt (aanwezig tot nu: {present})", flush=True)
    finally:
        await conn.close()

    present_ids = {aid for aid, v in best.items() if v[0] >= args.jaccard}
    out = [{"advies_id": aid, "adviescollege_id": next(r["adviescollege_id"] for r in rep_rows if r["advies_id"] == aid),
            "aanwezig_in_officiele": aid in present_ids,
            "best_jaccard": round(best[aid][0], 4), "officiele_id": best[aid][1]} for aid in rep_fp]
    csv_path = args.out_dir / "presence_full.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    print("")
    print(f"=== Aanwezig in officiele bekendmakingen (full-set) ===")
    print(f"  aanwezig: {len(present_ids)} / {len(rep_fp)}")
                                
    rh = args.out_dir / "report_hits_runA_det.jsonl"
    if rh.exists():
        hits = [json.loads(l)["advies_id"] for l in rh.read_text(encoding="utf-8").splitlines()
                if l.strip() and json.loads(l)["hit_text"]]
        ok = sum(1 for h in hits if h in present_ids)
        print(f"  VALIDATIE: van {len(hits)} bekende-aanwezige hits ook hier aanwezig: {ok}/{len(hits)}")
    print(f"[out] {csv_path}")

if __name__ == "__main__":
    asyncio.run(main())
