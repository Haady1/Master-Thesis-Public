"""Zuivere recall: van de aantoonbaar-aanwezige rapporten, hoeveel vindt de matcher?

Wat dit doet
------------
Combineert presence_full.csv (welke website-rapporten staan echt in de officiele
bekendmakingen, betrouwbaar bepaald via presence_scan.py) met candidate_eval_<label>.jsonl
(welke rapporten de matcher in zijn officiele kandidaten terugvond, met rang). Zo meten we
de ZUIVERE recall: noemer = alleen rapporten die aantoonbaar bestaan, dus elke miss is een
echte matcher-miss en geen corpus-gat.

Metrieken
---------
- clean recall = matcher-gevonden-en-aanwezig / aanwezig
- recall@5/10/25 over de aanwezige set (met 95%-Wilson-CI)
- per college
- labeling-precision (corpus-onafhankelijk): van advies-positief gelabelde kandidaten,
  welk deel is echt een adviesrapport (tekst-match).

In-/uitvoer
-----------
Inputs: presence_full.csv, candidate_eval_<label>.jsonl, groundtruth_sample.csv (collegenamen).
Outputs: stdout + report_clean_<label>.md / .json.

Geen database-toegang.

"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DV1_DIR = PROJECT_ROOT / "thesis" / "Analyse" / "dv1_matcher_recall"
if str(DV1_DIR) not in sys.path:
    sys.path.insert(0, str(DV1_DIR))
from evaluate_kabinetsreactie_recall import wilson_interval              

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "artifacts"
TOPK = (5, 10, 25)
COLLEGE_NAMES = {18: "AIV", 21: "RLI", 30: "Onderwijsraad", 15: "ROB", 31: "Raad voor Cultuur"}

def main() -> None:
    ap = argparse.ArgumentParser(description="Zuivere recall over aantoonbaar-aanwezige rapporten")
    ap.add_argument("--label", default="runA_det")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = ap.parse_args()

                                                   
    present = {}
    with (args.out_dir / "presence_full.csv").open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            present[int(r["advies_id"])] = {
                "college": int(r["adviescollege_id"]),
                "aanwezig": r["aanwezig_in_officiele"] in ("True", "true"),
            }
    present_ids = {aid for aid, v in present.items() if v["aanwezig"]}

                                                                               
    found: dict[int, dict] = {}
    pos_total = pos_real = 0
    with (args.out_dir / f"candidate_eval_{args.label}.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            c = json.loads(line)
            if c.get("llm_positive"):
                pos_total += 1
                pos_real += int(bool(c.get("is_real_advice")))
            if not c.get("is_real_advice"):
                continue
            aid = c.get("matched_full_advies_id")
            if aid is None:
                continue
            rank = c.get("rank")
            cur = found.get(aid)
            if cur is None or (c.get("best_full_jaccard", 0) > cur["jac"]):
                found[aid] = {"jac": c.get("best_full_jaccard", 0), "rank": rank,
                              "route": c.get("route"), "llm_positive": c.get("llm_positive")}

                                              
    n = len(present_ids)
    found_present = present_ids & set(found)
    p, lo, hi = wilson_interval(len(found_present), n)
    topk = {}
    for k in TOPK:
        hits = sum(1 for aid in found_present if (found[aid]["rank"] or 10**9) <= k)
        kp, klo, khi = wilson_interval(hits, n)
        topk[k] = {"recall": round(kp, 4), "wilson": [round(klo, 4), round(khi, 4)], "hits": hits}

                  
    per = {}
    pres_by_col = defaultdict(set)
    for aid in present_ids:
        pres_by_col[present[aid]["college"]].add(aid)
    for col, ids in pres_by_col.items():
        fp = ids & set(found)
        cp, clo, chi = wilson_interval(len(fp), len(ids))
        per[COLLEGE_NAMES.get(col, col)] = {"aanwezig": len(ids), "gevonden": len(fp),
                                            "recall": round(cp, 4), "wilson": [round(clo, 4), round(chi, 4)]}

    precision = round(pos_real / pos_total, 4) if pos_total else 0.0
    result = {
        "label": args.label,
        "aanwezig_in_officiele": n,
        "totaal_full_set": len(present),
        "matcher_gevonden_en_aanwezig": len(found_present),
        "clean_recall": round(p, 4), "clean_recall_wilson": [round(lo, 4), round(hi, 4)],
        "recall_topk": topk,
        "labeling_precision": precision, "labeling_precision_tn": [pos_real, pos_total],
        "per_college": per,
    }
    (args.out_dir / f"report_clean_{args.label}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    L = [f"# Zuivere recall (alleen aantoonbaar-aanwezige rapporten): {args.label}", "",
         f"Aanwezig in officiele bekendmakingen: {n} van {len(present)} (full-set)",
         f"Matcher vond daarvan terug: {len(found_present)}", "",
         f"## ZUIVERE RECALL: {p:.1%}  [95% Wilson {lo:.1%}-{hi:.1%}]  ({len(found_present)}/{n})"]
    for k in TOPK:
        m = topk[k]
        L.append(f"- recall@{k}: {m['recall']:.1%}  [{m['wilson'][0]:.1%}-{m['wilson'][1]:.1%}]  ({m['hits']}/{n})")
    L += ["", "## Per college (zuivere recall)"]
    for col, m in per.items():
        L.append(f"- {col}: {m['recall']:.1%} ({m['gevonden']}/{m['aanwezig']} aanwezig)")
    L += ["", "## Labeling-precision (corpus-onafhankelijk)",
          f"- precision: {precision:.1%} ({pos_real}/{pos_total} advies-positieve kandidaten echt advies)"]
    md = "\n".join(L)
    (args.out_dir / f"report_clean_{args.label}.md").write_text(md, encoding="utf-8")
    print(md)

if __name__ == "__main__":
    main()
