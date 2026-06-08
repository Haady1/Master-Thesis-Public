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
from matcher.advies.evaluatie.text_fingerprint import fingerprint, normalize_tokens

DEFAULT_COLLEGE_IDS = [18, 21, 30, 15, 31]
DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "artifacts"

WEBSITE_REPORTS_SQL = r"""
    SELECT
        cd.id AS advies_id,
        cd.unique_id,
        cd.adviescollege_id,
        ac.officiele_naam AS college,
        coalesce(dm.document_titel, cd.official_name_raw, cd.original_filename) AS title,
        dm.document_datum_parsed AS date_published,
        cd.download_url,
        coalesce(t.text_clean, t.text, t.text_digital, t.text_ocr) AS body
    FROM corpus.adviesdocumenten cd
    JOIN public.adviescolleges ac ON cd.adviescollege_id = ac.id
    JOIN pipeline.v_canonical_document_classificatie dc ON cd.id = dc.document_id
    JOIN pipeline.v_canonical_document_metadata dm ON cd.id = dm.document_id
    LEFT JOIN corpus.adviesdocument_teksten t ON t.document_id = cd.id
    WHERE cd.adviescollege_id = ANY($1::int[])
      AND dc.final_sub_category = 'ADVIESRAPPORT'
      AND dc.detected_language = 'nl'
      AND dm.document_datum_parsed BETWEEN '2005-01-01' AND '2024-12-31'
      AND cd.download_url IS NOT NULL
      AND cd.download_url !~* '(officielebekendmakingen|overheid\.nl|open\.overheid|rijksoverheid|tweedekamer|eerstekamer)'
    ORDER BY cd.adviescollege_id, dm.document_datum_parsed
"""

def stratified_sample(rows: list[dict], per_college: int) -> list[dict]:
    by_college: dict[int, list[dict]] = {}
    for row in rows:
        by_college.setdefault(row["adviescollege_id"], []).append(row)
    sample: list[dict] = []
    for college_id, items in by_college.items():

        n = len(items)
        take = min(per_college, n)
        if take == 0:
            continue
        if take == n:
            chosen = items
        else:
            step = n / take
            indices = sorted({int(i * step) for i in range(take)})

            while len(indices) < take:
                for j in range(n):
                    if j not in indices:
                        indices.append(j)
                        break
            chosen = [items[i] for i in sorted(indices)[:take]]
        sample.extend(chosen)
    return sample

async def main() -> None:
    ap = argparse.ArgumentParser(description="Bouw grondwaarheid website-adviesrapporten")
    ap.add_argument("--college-id", type=int, action="append", default=None,
                    help="College-id (public.adviescolleges.id); herhaalbaar.")
    ap.add_argument("--per-college", type=int, default=10)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = ap.parse_args()

    college_ids = args.college_id or DEFAULT_COLLEGE_IDS
    args.out_dir.mkdir(parents=True, exist_ok=True)

    conn = await asyncpg.connect(db_config.asyncpg_dsn)
    try:
        rows = [dict(r) for r in await conn.fetch(WEBSITE_REPORTS_SQL, college_ids)]
    finally:
        await conn.close()


    rows = [r for r in rows if len(normalize_tokens(r.get("body"))) >= 50]
    print(f"Website-adviesrapporten met tekst: {len(rows)} over {len(college_ids)} colleges")

    full_fp_path = args.out_dir / "groundtruth_full_fp.jsonl"
    with full_fp_path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fp = sorted(fingerprint(r["body"]))
            fh.write(json.dumps({
                "advies_id": r["advies_id"],
                "adviescollege_id": r["adviescollege_id"],
                "shingles": fp,
            }) + "\n")
    print(f"[full]   {full_fp_path}  ({len(rows)} rapporten)")

    sample = stratified_sample(rows, args.per_college)
    print(f"Sample (recall-grondwaarheid): {len(sample)} rapporten")

    sample_csv = args.out_dir / "groundtruth_sample.csv"
    fields = ["advies_id", "unique_id", "adviescollege_id", "college", "title",
              "date_published", "download_url", "n_tokens"]
    with sample_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in sample:
            w.writerow({
                "advies_id": r["advies_id"],
                "unique_id": r["unique_id"],
                "adviescollege_id": r["adviescollege_id"],
                "college": r["college"],
                "title": (r["title"] or "")[:300],
                "date_published": r["date_published"],
                "download_url": r["download_url"],
                "n_tokens": len(normalize_tokens(r["body"])),
            })
    print(f"[sample] {sample_csv}")

    sample_fp = args.out_dir / "groundtruth_sample_fp.jsonl"
    with sample_fp.open("w", encoding="utf-8") as fh:
        for r in sample:
            fh.write(json.dumps({
                "advies_id": r["advies_id"],
                "adviescollege_id": r["adviescollege_id"],
                "shingles": sorted(fingerprint(r["body"])),
            }) + "\n")
    print(f"[sample-fp] {sample_fp}")


    per = {}
    for r in sample:
        per[r["college"]] = per.get(r["college"], 0) + 1
    print("Verdeling sample per college:")
    for k, v in per.items():
        print(f"  {v:>3}  {k}")

if __name__ == "__main__":
    asyncio.run(main())
