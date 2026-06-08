"""College-effect op meetkwaliteit (groen-aandeel) — reproduceerbare herrekening + caveat.

Wat dit script doet
-------------------
Levert de cijfers voor de DV2-robuustheidsrij "College-effect" in de scriptie
(`master_thesis_conceptversie.tex`). Het berekent per adviescollege het aandeel
adviesrapporten met meetkwaliteit-label *groen* en maakt de bijbehorende
"mini-college-caveat" hard: hoeveel colleges hebben maar één gevalideerd rapport
(en dus per definitie 0% of 100% groen), en wat is de mediaan onder colleges met
n>=2 rapporten.

Herkomst van de data (bron-van-waarheid)
----------------------------------------
De per-document meetkwaliteit-labels (groen/oranje/rood) zijn een BEVROREN
validatie-artefact uit de adviesextractie-validatie. Het per-college groen-aandeel
wordt berekend in `thesis/Analyse/DV2_betrouwbaarheid_AI_documentanalyse_validatie.ipynb`,
cel "college_summary" (groupby college over advies_docs_labeled), en geexporteerd naar
`thesis/Analyse/data/college_effect_groen_oranje.csv`. Dit script leest die canonieke
CSV en leidt daar de scriptie-cijfers + caveat reproduceerbaar uit af. Omdat de labels
bevroren zijn, schalen ze niet mee met latere corpusgroei; daarom is dit een
expliciete peildatum-rapportage en geen live DB-query.

Inputs
------
  thesis/Analyse/data/college_effect_groen_oranje.csv
    (kolommen: college, n, pct_groen, pct_oranje, pct_rood, woorden_*, actoren_*)

Outputs (print naar stdout, geen schrijfacties)
-----------------------------------------------
  - pct_groen voor de vier in de scriptie genoemde colleges
  - caveat: aantal colleges met n==1 (0%/100%), mediaan pct_groen voor n>=2
  - mediaan over alle colleges

Plaats in de pijplijn
---------------------
Analyse-zijde van DV2 (robuustheid/meetkwaliteit). Wijzigt niets; levert alleen de
getallen voor de scriptietekst, peildatum gelijk aan de CSV-export.

"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "college_effect_groen_oranje.csv"

                                                                  
GENOEMDE_COLLEGES = [
    "Adviesraad voor wetenschap, technologie en innovatie",
    "Onderwijsraad",
    "Gezondheidsraad",
    "College voor de Rechten van de Mens",
]

def laad() -> pd.DataFrame:
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Canonieke CSV niet gevonden: {CSV_PATH}. "
            "Genereer hem opnieuw via de DV2-validatienotebook (cel college_summary)."
        )
    return pd.read_csv(CSV_PATH)

def genoemde_colleges(df: pd.DataFrame) -> pd.DataFrame:
    rijen = df[df["college"].isin(GENOEMDE_COLLEGES)][["college", "n", "pct_groen"]]
    return rijen.set_index("college").reindex(GENOEMDE_COLLEGES).reset_index()

def caveat(df: pd.DataFrame) -> dict[str, float]:
    n1 = df[df["n"] == 1]
    n2 = df[df["n"] >= 2]
    return {
        "n_colleges": int(len(df)),
        "n_documenten": int(df["n"].sum()),
        "colleges_n1": int(len(n1)),
        "colleges_n1_100pct": int((n1["pct_groen"] == 100).sum()),
        "colleges_n1_0pct": int((n1["pct_groen"] == 0).sum()),
        "colleges_n2plus": int(len(n2)),
        "mediaan_groen_n2plus": round(float(n2["pct_groen"].median()), 1),
        "mediaan_groen_alle": round(float(df["pct_groen"].median()), 1),
    }

def main() -> None:
    df = laad()
    print("=== College-effect op meetkwaliteit (groen-aandeel) ===")
    print(f"Bron: {CSV_PATH.name} (peildatum = exportdatum van de DV2-notebook)\n")

    print("Genoemde colleges:")
    for _, r in genoemde_colleges(df).iterrows():
        n = "-" if pd.isna(r["n"]) else int(r["n"])
        print(f"  {r['college']}: n={n}, groen={r['pct_groen']}%")

    c = caveat(df)
    print("\nMini-college-caveat:")
    print(f"  totaal colleges: {c['n_colleges']} (samen {c['n_documenten']} gevalideerde rapporten)")
    print(f"  colleges met n==1: {c['colleges_n1']} "
          f"(waarvan {c['colleges_n1_100pct']}x 100% en {c['colleges_n1_0pct']}x 0% groen)")
    print(f"  colleges met n>=2: {c['colleges_n2plus']}; "
          f"mediaan groen-aandeel = {c['mediaan_groen_n2plus']}%")
    print(f"  mediaan groen-aandeel over alle colleges: {c['mediaan_groen_alle']}%")

if __name__ == "__main__":
    main()
