"""Bereken recall@k (deterministisch) en precision/recall/F (VLAM) voor de advies-matcher.

Wat dit doet
------------
Leest de hit-tabellen van match_hits.py en rapporteert:
- Deterministische pipeline (Run A): candidate-recall @top-5/10/25 met 95%-Wilson-CI,
  rangverdeling, route-bijdrage en per-college-uitsplitsing. Meet of de RETRIEVAL het
  officiele-bekendmaking-rapport bovenaan krijgt.
- VLAM (Run B, indien aanwezig): precision, recall en F1 van het VLAM-oordeel
  "dit is een adviesrapport". Recall = van de in-de-pool gevonden grondwaarheid-rapporten,
  welk deel VLAM advies-positief labelt. Precision = van de VLAM advies-positieve
  kandidaten, welk deel echt een adviesrapport is (tekst-match met de full-set).

Hergebruik
----------
wilson_interval uit thesis/Analyse/dv1_matcher_recall/evaluate_kabinetsreactie_recall.py.

In-/uitvoer
-----------
Inputs: report_hits_<label>.jsonl en candidate_eval_<label>.jsonl (uit match_hits.py).
Outputs: stdout + report_<label>.json + report_<label>.md.

Plaats in de pijplijn
---------------------
Stap 4 van matcher/advies/evaluatie. Geen database-toegang.

"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DV1_DIR = PROJECT_ROOT / "thesis" / "Analyse" / "dv1_matcher_recall"
if str(DV1_DIR) not in sys.path:
    sys.path.insert(0, str(DV1_DIR))
from evaluate_kabinetsreactie_recall import wilson_interval              

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "artifacts"
TOPK = (5, 10, 25)

def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def rank_band(rows: list[dict]) -> dict:
    c = Counter()
    for r in rows:
        if not r.get("hit_text"):
            c["geen_hit"] += 1
            continue
        rk = r.get("best_rank")
        if rk is None:
            c["hit_geen_rang"] += 1
        elif rk <= 5:
            c["top_5"] += 1
        elif rk <= 10:
            c["top_10"] += 1
        elif rk <= 25:
            c["top_25"] += 1
        else:
            c["buiten_25"] += 1
    return dict(c)

def deterministic_metrics(reports: list[dict]) -> dict:
    n = len(reports)
    in_pool = sum(1 for r in reports if r.get("hit_text"))
    in_pool_or_title = sum(1 for r in reports if r.get("hit"))
    out = {"n": n, "gevonden_in_pool_tekst": in_pool, "gevonden_in_pool_of_titel": in_pool_or_title}
    for k in TOPK:
        hits = sum(1 for r in reports if r.get("hit_text") and (r.get("best_rank") or 10**9) <= k)
        p, lo, hi = wilson_interval(hits, n)
        out[f"recall_top_{k}"] = {"recall": round(p, 4), "wilson": [round(lo, 4), round(hi, 4)],
                                  "hits": hits, "n": n}
    p, lo, hi = wilson_interval(in_pool, n)
    out["recall_in_pool"] = {"recall": round(p, 4), "wilson": [round(lo, 4), round(hi, 4)],
                             "hits": in_pool, "n": n}
    out["rangverdeling"] = rank_band(reports)
    out["route_bijdrage"] = dict(Counter(r["best_route"] for r in reports if r.get("hit_text") and r.get("best_route")).most_common())
                  
    by_col = defaultdict(list)
    for r in reports:
        by_col[r.get("college", "?")].append(r)
    per = {}
    for col, sub in by_col.items():
        h25 = sum(1 for r in sub if r.get("hit_text") and (r.get("best_rank") or 10**9) <= 25)
        cp, clo, chi = wilson_interval(h25, len(sub))
        per[col] = {"n": len(sub), "recall_top_25": round(cp, 4),
                    "wilson": [round(clo, 4), round(chi, 4)],
                    "in_pool": sum(1 for r in sub if r.get("hit_text"))}
    out["per_college"] = per
    return out

def vlam_metrics(reports: list[dict], cands: list[dict]) -> dict | None:
    has_labels = any(c.get("llm_label") for c in cands)
    if not has_labels:
        return None
    in_pool = [r for r in reports if r.get("hit_text")]
                                                                                     
    recalled = sum(1 for r in in_pool if r.get("best_llm_label") in {"FINAL_ADVICE_OR_REPORT", "INDIVIDUAL_ADVICE"})
    recall = recalled / len(in_pool) if in_pool else 0.0
    recall_over_50 = recalled / len(reports) if reports else 0.0
                                                                                   
    pos = [c for c in cands if c.get("llm_positive")]
    tp = sum(1 for c in pos if c.get("is_real_advice"))
    precision = tp / len(pos) if pos else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    rp, rlo, rhi = wilson_interval(recalled, len(in_pool)) if in_pool else (0, 0, 0)
    pp, plo, phi = wilson_interval(tp, len(pos)) if pos else (0, 0, 0)
    return {
        "recall": round(recall, 4), "recall_wilson": [round(rlo, 4), round(rhi, 4)],
        "recall_teller_noemer": [recalled, len(in_pool)],
        "recall_over_alle_50": round(recall_over_50, 4),
        "precision": round(precision, 4), "precision_wilson": [round(plo, 4), round(phi, 4)],
        "precision_teller_noemer": [tp, len(pos)],
        "f1": round(f1, 4),
        "vlam_positieve_kandidaten": len(pos),
    }

def main() -> None:
    ap = argparse.ArgumentParser(description="Bereken recall@k en labeling precision/recall/F1")
    ap.add_argument("--label", required=True)
    ap.add_argument("--label-kind", default="labeling",
                    help="Naam van de labelstap voor het rapport (bijv. 'regelgebaseerd' of 'VLAM').")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = ap.parse_args()

    reports = load_jsonl(args.out_dir / f"report_hits_{args.label}.jsonl")
    cand_path = args.out_dir / f"candidate_eval_{args.label}.jsonl"
    cands = load_jsonl(cand_path) if cand_path.exists() else []

    det = deterministic_metrics(reports)
    vlam = vlam_metrics(reports, cands)
    result = {"label": args.label, "deterministisch": det, "vlam": vlam}

    (args.out_dir / f"report_{args.label}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [f"# Advies-matcher evaluatie: {args.label}", "",
             f"Grondwaarheid-rapporten (website): {det['n']}", ""]
    lines.append("## Deterministische pipeline (retrieval)")
    lines.append(f"- gevonden in pool (tekst-match): {det['gevonden_in_pool_tekst']}/{det['n']}")
    for k in TOPK:
        m = det[f"recall_top_{k}"]
        lines.append(f"- recall@{k}: {m['recall']:.1%}  [95% Wilson {m['wilson'][0]:.1%}-{m['wilson'][1]:.1%}]  ({m['hits']}/{m['n']})")
    lines.append(f"- rangverdeling: {det['rangverdeling']}")
    lines.append(f"- route-bijdrage: {det['route_bijdrage']}")
    lines.append("")
    lines.append("### Per college (recall@25)")
    for col, m in det["per_college"].items():
        lines.append(f"- {col}: {m['recall_top_25']:.1%} ({m['in_pool']}/{m['n']} in pool)")
    lines.append("")
    if vlam:
        lines.append(f"## Labeling ({args.label_kind}) precision / recall / F1")
        lines.append(f"- precision: {vlam['precision']:.1%}  ({vlam['precision_teller_noemer'][0]}/{vlam['precision_teller_noemer'][1]} advies-positieve kandidaten correct)")
        lines.append(f"- recall:    {vlam['recall']:.1%}  ({vlam['recall_teller_noemer'][0]}/{vlam['recall_teller_noemer'][1]} in-pool rapporten advies-gelabeld)")
        lines.append(f"- F1:        {vlam['f1']:.1%}")
        lines.append(f"- recall over alle 50: {vlam['recall_over_alle_50']:.1%}")
    else:
        lines.append("## VLAM\n- (geen LLM-labels in deze run)")
    md = "\n".join(lines)
    (args.out_dir / f"report_{args.label}.md").write_text(md, encoding="utf-8")
    print(md)

if __name__ == "__main__":
    main()
