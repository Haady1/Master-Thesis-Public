"""DV3-verwerking bevriezen op de 171-Kaderwet-scope (peildatum 2026-06-05).

Wat dit script doet
-------------------
Roept `dv3_analyse.run()` aan (die op de 171/corpus_keuzes-scope draait, zie dv3_analyse.py)
en schrijft alle geaggregeerde uitkomsten read-only weg als een bevroren snapshot. Zo zijn
de DV3-cijfers in de thesis herleidbaar en reproduceerbaar, net als de DV2-bundels
(01b/02b/10). Het script muteert niets in de database; dv3_analyse doet alleen SELECT.

Input
-----
- thesis/Analyse/dv3_analyse.py :: run()  (live PostgreSQL, 171-scope, run-bewust)

Output
------
Bundel thesis/Analyse/DV2_validatie_bronnen/11_dv3_verwerking_171_frozen_20260605/
met _manifest.json + losse CSV's (verdelingen, dimensies, Cramer's V, gevoeligheid,
meetkwaliteit, noemer-metadata).

Plaats in de pijplijn
---------------------
Leeslaag bovenop de DV3-analyse. Vriest de cijfers in die anders alleen live bestonden.

"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from thesis.Analyse.dv3_analyse import run              

                                                                            
PEILDATUM = "2026-06-05"
SCOPE = "corpus_keuzes/171"
POSTFIX_RUN_DATUM = "2026-06-03"

OUTPUT_DIR = (
    PROJECT_ROOT / "thesis" / "Analyse" / "DV2_validatie_bronnen"
    / f"11_dv3_verwerking_171_frozen_{PEILDATUM.replace('-', '')}"
)

def _per_type_frame(res: dict, key: str) -> pd.DataFrame:
    """Voeg de twee elementtype-frames samen met een elementtype-kolom."""
    frames = []
    for et in ["aanbeveling", "probleemdefinitie"]:
        sub = res[key][et].copy()
        sub.insert(0, "elementtype", et)
        frames.append(sub)
    return pd.concat(frames, ignore_index=True)

def freeze_dv3() -> dict:
    """Voer de DV3-analyse uit op de 171-scope en exporteer de bevroren bundel."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[DV3-Freeze] Output: {OUTPUT_DIR}")
    print("[DV3-Freeze] dv3_analyse.run() aanroepen (171-scope)...")
    res = run()

                                
    res["verdeling_11"].to_csv(OUTPUT_DIR / "verdeling_11.csv", index=False)
    res["verdeling_6"].to_csv(OUTPUT_DIR / "verdeling_6.csv", index=False)

                                                                                
    _per_type_frame(res, "verdeling_6_per_type").to_csv(
        OUTPUT_DIR / "verdeling_per_type_6.csv", index=False)
    _per_type_frame(res, "verdeling_11_per_type").to_csv(
        OUTPUT_DIR / "verdeling_per_type_11.csv", index=False)

                                
    _per_type_frame(res, "dim_positie_per_type").to_csv(
        OUTPUT_DIR / "dimensie_positie.csv", index=False)
    _per_type_frame(res, "dim_opvolging_per_type").to_csv(
        OUTPUT_DIR / "dimensie_opvolging.csv", index=False)

                                                                     
    cramers = pd.DataFrame([
        {"niveau": "11-label", "cramers_v": res["cramers_11"]["cramers_v"],
         "chi2": res["cramers_11"]["chi2"], "n": res["cramers_11"]["n"],
         "clustered_mediaan": res["cramers_11_clustered"]["mediaan"],
         "clustered_p05": res["cramers_11_clustered"]["p05"],
         "clustered_p95": res["cramers_11_clustered"]["p95"]},
        {"niveau": "6-klasse", "cramers_v": res["cramers_6"]["cramers_v"],
         "chi2": res["cramers_6"]["chi2"], "n": res["cramers_6"]["n"],
         "clustered_mediaan": res["cramers_6_clustered"]["mediaan"],
         "clustered_p05": res["cramers_6_clustered"]["p05"],
         "clustered_p95": res["cramers_6_clustered"]["p95"]},
    ])
    cramers.to_csv(OUTPUT_DIR / "cramers_statistiek.csv", index=False)

                                     
    res["sensitivity"].to_csv(OUTPUT_DIR / "gevoeligheid.csv", index=False)
    res["meetkwaliteit"].to_csv(OUTPUT_DIR / "meetkwaliteit.csv", index=False)

                              
    res["collegetype"]["crosstab_6"].to_csv(OUTPUT_DIR / "collegetype_verdeling_6.csv", index=False)

                        
    pd.DataFrame([
        {"noemer": "elementen", "n": res["n_elementen"]},
        {"noemer": "reacties", "n": res["n_reacties"]},
        {"noemer": "adviezen", "n": res["n_adviezen"]},
        {"noemer": "aanbevelingen", "n": res["per_type_n"].get("aanbeveling")},
        {"noemer": "probleemdefinities", "n": res["per_type_n"].get("probleemdefinitie")},
    ]).to_csv(OUTPUT_DIR / "metadata_inscope.csv", index=False)

                 
    manifest = {
        "peildatum": PEILDATUM,
        "scope": SCOPE,
        "beschrijving": (
            "171 Kaderwet-fasen via de scope_fasen-CTE (Kaderwet=TRUE + instellingsbesluit "
            "+ tijd_adviescollege-type, excl. AP/CBP), Nederlands alleen, run-bewust op de "
            "post-fix verwerkingsronde. Identiek aan DV1/DV2 corpus_keuzes-scope. NB: de "
            "noemer is voller dan DV2's bevroren validatie-batch (419 docs / 13.165 "
            "elementen) omdat DV3 de actuele database leest, inclusief 171-scope-colleges "
            "die na die batch zijn geanalyseerd."
        ),
        "postfix_run_datum": POSTFIX_RUN_DATUM,
        "geexporteerd_op": datetime.now().isoformat(timespec="seconds"),
        "n_elementen": int(res["n_elementen"]),
        "n_reacties": int(res["n_reacties"]),
        "n_adviezen": int(res["n_adviezen"]),
        "per_type": {k: int(v) for k, v in res["per_type_n"].items()},
        "dekking": {k: (int(v) if v is not None else None)
                    for k, v in res["dekking"].items()},
        "elementen_per_reactie": res["elementen_per_reactie"],
        "elementen_per_advies": res["elementen_per_advies"],
        "cramers_v_11label": res["cramers_11"]["cramers_v"],
        "cramers_v_6klasse": res["cramers_6"]["cramers_v"],
        "cramers_v_11label_clustered": res["cramers_11_clustered"],
        "cramers_v_6klasse_clustered": res["cramers_6_clustered"],
        "collegetype_cramers_v_6klasse": res["collegetype"]["cramers_6"]["cramers_v"],
        "collegetype_cramers_v_6klasse_clustered": res["collegetype"]["cramers_6_clustered"],
        "collegetype_cramers_v_11label": res["collegetype"]["cramers_11"]["cramers_v"],
        "collegetype_tellingen": res["collegetype"]["crosstab_6"].to_dict(orient="records"),
        "bronnen": [
            "pipeline.kabinetsreactie_aanbeveling_matches",
            "pipeline.kabinetsreactie_analyse",
            "corpus.adviesdocumenten",
            "register.adviescollege_fasen (scope_fasen-CTE)",
        ],
    }
    (OUTPUT_DIR / "_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[DV3-Freeze] KLAAR -- {res['n_elementen']:,} elementen / "
          f"{res['n_reacties']} reacties / {res['n_adviezen']} adviezen")
    print(f"[DV3-Freeze] Cramer's V 11-label={res['cramers_11']['cramers_v']} | "
          f"6-klasse={res['cramers_6']['cramers_v']}")
    print("[DV3-Freeze] Bundel + manifest geschreven.")
    return manifest

if __name__ == "__main__":
    freeze_dv3()
