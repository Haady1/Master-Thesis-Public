"""Koppel matcher-kandidaten aan de grondwaarheid via tekst-overeenkomst.

Wat dit doet
------------
Leest de kandidaten van een discovery-run (run_discovery.py) en bepaalt per
grondwaarheid-rapport of de matcher de OFFICIELE-BEKENDMAKING-kopie heeft gevonden.
Een "hit" stellen we vast op tekst-Jaccard tussen de website-versie (grondwaarheid)
en de kandidaat-tekst uit public.overheidsdocumenten. Zo is de koppeling onafhankelijk
van document-id's (die verschillen tussen website en officiele bekendmaking).

Zuiverheid
----------
Kandidaten uit public.documenten (de website/legacy-advieslaag) tellen NIET mee als
hit: de matcher mag de website-kopie niet "terugvinden". Alleen kandidaten uit de
officiele bekendmakingen (document_type != 'public.documenten') zijn geldige hits.

In-/uitvoer
-----------
Inputs:
- --sample-fp      groundtruth_sample_fp.jsonl   (recall-grondwaarheid, ~50)
- --full-fp        groundtruth_full_fp.jsonl     (alle website-rapporten, voor precision)
- --groundtruth    groundtruth_sample.csv        (metadata voor leesbaarheid)
- --candidates     <run>.candidates.jsonl
- --jaccard        drempel (default 0.6)
- --label          naam van de run (bijv. runA_det / runB_vlam)

Outputs (in --out-dir):
- report_hits_<label>.csv / .jsonl   : per grondwaarheid-rapport hit/rang/route/llm_label
- candidate_eval_<label>.jsonl       : per officiele kandidaat match-info + llm_label
                                       (basis voor precision in evaluate_metrics.py)

Plaats in de pijplijn
---------------------
Stap 3 van matcher/advies/evaluatie. Read-only t.o.v. de database.

"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import asyncpg
from rapidfuzz import fuzz

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pg_database.config import db_config
from matcher.advies.evaluatie.text_fingerprint import fingerprint, jaccard
from matcher.advies.labeling import POSITIVE_ADVICE_LABELS

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "artifacts"

def load_fp_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                obj = json.loads(line)
                obj["shingles"] = set(obj["shingles"])
                rows.append(obj)
    return rows

def load_candidates(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def is_official(candidate: dict) -> bool:
    """True als de kandidaat uit de officiele bekendmakingen komt (niet website)."""
    return (candidate.get("document_type") or "") != "public.documenten"

def dedupe_official_by_id(candidates: list[dict]) -> dict[int, list[dict]]:
    """Per college: officiele kandidaten ontdubbeld op document-id (beste rerank-score)."""
    by_college: dict[int, dict[str, dict]] = defaultdict(dict)
    for c in candidates:
        if not is_official(c):
            continue
        cid = c.get("candidate_document_id")
        if not cid:
            continue
        college = c["college_id"]
        rerank = (c.get("scores") or {}).get("rerank_total", 0) or 0
        existing = by_college[college].get(cid)
        if existing is None:
            c = dict(c)
            c["_rerank"] = rerank
            by_college[college][cid] = c
        else:
                                                                              
            if rerank > existing["_rerank"]:
                existing["_rerank"] = rerank
                existing["scores"] = c.get("scores")
                existing["route"] = c.get("route")
            if c.get("llm_label") in POSITIVE_ADVICE_LABELS:
                existing["llm_label"] = c.get("llm_label")
    return {college: list(d.values()) for college, d in by_college.items()}

def assign_ranks(cands: list[dict]) -> None:
    """Geef rang 1..n op aflopende rerank-score (deterministisch, tie-break op id)."""
    ordered = sorted(cands, key=lambda c: (-(c.get("_rerank") or 0), str(c.get("candidate_document_id"))))
    for i, c in enumerate(ordered, start=1):
        c["_rank"] = i

def parse_date(value) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None

async def fetch_candidate_texts(ids: list[str]) -> dict[str, str]:
    if not ids:
        return {}
    conn = await asyncpg.connect(db_config.asyncpg_dsn)
    try:
        rows = await conn.fetch(
            "SELECT id, content_text FROM public.overheidsdocumenten WHERE id = ANY($1::text[])",
            ids,
        )
    finally:
        await conn.close()
    return {r["id"]: (r["content_text"] or "") for r in rows}

async def main() -> None:
    ap = argparse.ArgumentParser(description="Koppel kandidaten aan grondwaarheid (tekst-Jaccard)")
    ap.add_argument("--sample-fp", type=Path, default=DEFAULT_OUT_DIR / "groundtruth_sample_fp.jsonl")
    ap.add_argument("--full-fp", type=Path, default=DEFAULT_OUT_DIR / "groundtruth_full_fp.jsonl")
    ap.add_argument("--groundtruth", type=Path, default=DEFAULT_OUT_DIR / "groundtruth_sample.csv")
    ap.add_argument("--candidates", type=Path, required=True)
    ap.add_argument("--jaccard", type=float, default=0.6)
    ap.add_argument("--title-ratio", type=float, default=92.0)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = ap.parse_args()

    sample = load_fp_jsonl(args.sample_fp)
    full = load_fp_jsonl(args.full_fp)
    full_by_college: dict[int, list[dict]] = defaultdict(list)
    for r in full:
        full_by_college[r["adviescollege_id"]].append(r)

    meta: dict[int, dict] = {}
    with args.groundtruth.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            meta[int(row["advies_id"])] = row

    candidates = load_candidates(args.candidates)
    official_by_college = dedupe_official_by_id(candidates)
    for cands in official_by_college.values():
        assign_ranks(cands)

                                                                         
    all_ids = [c["candidate_document_id"] for cands in official_by_college.values() for c in cands]
    texts = await fetch_candidate_texts(sorted(set(all_ids)))
    cand_fp: dict[str, set] = {cid: fingerprint(txt) for cid, txt in texts.items()}

                                                                                          
    report_rows = []
    for s in sample:
        advies_id = s["advies_id"]
        college = s["adviescollege_id"]
        gt_fp = s["shingles"]
        m = meta.get(advies_id, {})
        gt_title = (m.get("title") or "")
        gt_date = parse_date(m.get("date_published"))
        cands = official_by_college.get(college, [])
        best = {"jac": 0.0, "cid": None, "rank": None, "route": None, "llm_label": None,
                "title_ratio": 0.0, "date_diff": None}
        for c in cands:
            cid = c["candidate_document_id"]
            jac = jaccard(gt_fp, cand_fp.get(cid, set()))
            if jac > best["jac"]:
                tr = fuzz.token_set_ratio(gt_title, c.get("candidate_title") or "")
                cdate = parse_date(c.get("date_published"))
                ddiff = abs((gt_date - cdate).days) if (gt_date and cdate) else None
                best = {"jac": jac, "cid": cid, "rank": c.get("_rank"),
                        "route": c.get("route"), "llm_label": c.get("llm_label"),
                        "title_ratio": tr, "date_diff": ddiff}
                                                           
        best_title = {"ratio": 0.0, "cid": None, "rank": None, "date_diff": None}
        for c in cands:
            tr = fuzz.token_set_ratio(gt_title, c.get("candidate_title") or "")
            if tr > best_title["ratio"]:
                cdate = parse_date(c.get("date_published"))
                ddiff = abs((gt_date - cdate).days) if (gt_date and cdate) else None
                best_title = {"ratio": tr, "cid": c["candidate_document_id"],
                              "rank": c.get("_rank"), "date_diff": ddiff}
        hit_text = best["jac"] >= args.jaccard
        hit_title = (best_title["ratio"] >= args.title_ratio and
                     best_title["date_diff"] is not None and best_title["date_diff"] <= 60)
        report_rows.append({
            "advies_id": advies_id,
            "adviescollege_id": college,
            "college": m.get("college", ""),
            "title": gt_title[:200],
            "date_published": m.get("date_published", ""),
            "n_official_candidates": len(cands),
            "best_jaccard": round(best["jac"], 4),
            "best_candidate_id": best["cid"],
            "best_rank": best["rank"],
            "best_route": best["route"],
            "best_llm_label": best["llm_label"],
            "hit_text": hit_text,
            "best_title_ratio": round(best_title["ratio"], 1),
            "title_fallback_candidate_id": best_title["cid"],
            "title_fallback_rank": best_title["rank"],
            "title_fallback_date_diff": best_title["date_diff"],
            "hit_title": hit_title,
            "hit": hit_text or hit_title,
        })

                                                                                             
    cand_rows = []
    for college, cands in official_by_college.items():
        full_reports = full_by_college.get(college, [])
        for c in cands:
            cid = c["candidate_document_id"]
            cfp = cand_fp.get(cid, set())
            best_jac, best_advies = 0.0, None
            for fr in full_reports:
                jac = jaccard(cfp, fr["shingles"])
                if jac > best_jac:
                    best_jac, best_advies = jac, fr["advies_id"]
            cand_rows.append({
                "college_id": college,
                "candidate_document_id": cid,
                "rank": c.get("_rank"),
                "rerank_score": c.get("_rerank"),
                "route": c.get("route"),
                "document_type": c.get("document_type"),
                "llm_label": c.get("llm_label"),
                "llm_positive": c.get("llm_label") in POSITIVE_ADVICE_LABELS,
                "best_full_jaccard": round(best_jac, 4),
                "matched_full_advies_id": best_advies,
                "is_real_advice": best_jac >= args.jaccard,
            })

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rep_csv = args.out_dir / f"report_hits_{args.label}.csv"
    with rep_csv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(report_rows[0].keys()))
        w.writeheader()
        w.writerows(report_rows)
    rep_jsonl = args.out_dir / f"report_hits_{args.label}.jsonl"
    with rep_jsonl.open("w", encoding="utf-8") as fh:
        for r in report_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    cand_jsonl = args.out_dir / f"candidate_eval_{args.label}.jsonl"
    with cand_jsonl.open("w", encoding="utf-8") as fh:
        for r in cand_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    hits = sum(1 for r in report_rows if r["hit"])
    text_hits = sum(1 for r in report_rows if r["hit_text"])
    print(f"[{args.label}] grondwaarheid-rapporten: {len(report_rows)}")
    print(f"  hit (tekst Jaccard>= {args.jaccard}): {text_hits}/{len(report_rows)}")
    print(f"  hit (tekst OF titel-fallback):        {hits}/{len(report_rows)}")
    print(f"  officiele kandidaten beoordeeld:      {len(cand_rows)}")
    print(f"[out] {rep_csv}")
    print(f"[out] {cand_jsonl}")

if __name__ == "__main__":
    asyncio.run(main())
