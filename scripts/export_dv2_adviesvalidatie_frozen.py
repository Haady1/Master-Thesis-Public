"""Exportscript DV2-adviesvalidatie: gevallen snapshot met peildatum.

Dit script vormt stap B van de DV2-analyse (advies-validatie-bevindingen voor de
scriptie). Het leest uitsluitend (alleen SELECT) via de data_loading-laag en schrijft
bevoren CSV-snapshots naar `thesis/Analyse/DV2_validatie_bronnen/01b_adviesvalidatie_171_frozen_YYYYMMDD/`.

Doel: fix de DV1-adviesvaliatie-data op een bepaalde peildatum, zodat alle latere
analyses (DV2, DV3) op dezelfde bevoren snapshot werken. Dit voorkomt datadrift en
maakt analyses reproduceerbaar.

Waarom CSV-tussenlaag: zoals DV1, mogen de CSV's + notebook publiek op GitHub.
De live database is groot en bevat gevoelige data. De CSV's zijn anoniem en compact.

Inputs:
  - .env in de projectroot (database-credentials)
  - PostgreSQL-tabel en views via pg_database/checks/advies_validatie/data_loading.py
    (read-only; scope="corpus_keuzes" = 171-Kaderwet colleges)

Outputs (in thesis/Analyse/DV2_validatie_bronnen/01b_adviesvalidatie_171_frozen_YYYYMMDD/):
  - df_docs.csv           : 1 rij per adviesrapport (1374 rijen verwacht)
  - df_aanbevelingen.csv  : 1 rij per aanbeveling (22286 rijen verwacht)
  - df_problemen.csv      : 1 rij per probleemdefinitie (17927 rijen verwacht)
  - _manifest.json        : peildatum, scope, beschrijving, rij-aantallen

Waarschuwing: kolommen met list/dict-waarden (consultaties_json, beleidsopties_json,
betrokken_actoren_json, box_ids, consultatie_vormen, consultatie_actoren, actor_rollen,
actor_namen, onderzoeksmethoden) worden JSON-geserialiseerd voordat ze naar CSV gaan,
zodat ze later herleesbaar zijn.

Draaien (vanuit projectroot of waar dan ook):
  python "thesis/Analyse/export_dv2_adviesvalidatie_frozen.py"
  of
  py "thesis/Analyse/export_dv2_adviesvalidatie_frozen.py"
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

                                                                                   
BASE_DIR = Path(__file__).resolve().parent                             
PROJECT_ROOT = BASE_DIR.parents[1]                                  
sys.path.insert(0, str(PROJECT_ROOT))

                         
from pg_database.checks.advies_validatie.data_loading import load_validation_data

                                                                                   
PEILDATUM = "2026-06-05"
SCOPE = "corpus_keuzes"
DATA_DIR = BASE_DIR / f"DV2_validatie_bronnen/01b_adviesvalidatie_171_frozen_{PEILDATUM.replace('-', '')}"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def _is_json_serializable(val: Any) -> bool:
    """Controleer of de waarde een list of dict is (moet JSON-geserialiseerd)."""
    if val is None:
        return False
    return isinstance(val, (list, dict))

def _serialize_list_dict(val: Any) -> str | Any:
    """Zet list/dict om naar JSON-string; andere waarden ongemoeid."""
    if isinstance(val, (list, dict)):
        return json.dumps(val, ensure_ascii=False)
    return val

def _detect_json_columns(df: pd.DataFrame) -> set[str]:
    """Detecteer kolommen met list/dict-waarden (eerste niet-NaN waarde genoeg)."""
    json_cols = set()
    for col in df.columns:
                                     
        for val in df[col]:
                                                                                            
            try:
                is_na = val is None or (isinstance(val, float) and pd.isna(val))
            except (ValueError, TypeError):
                                                   
                is_na = False

            if not is_na:
                if isinstance(val, (list, dict)):
                    json_cols.add(col)
                break
    return json_cols

def _serialize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Zet alle list/dict-kolommen om naar JSON-strings."""
    result = df.copy()
    json_cols = _detect_json_columns(result)
    for col in json_cols:
        result[col] = result[col].apply(_serialize_list_dict)
    return result

def save(df: pd.DataFrame, name: str) -> int:
    """Schrijf dataframe naar CSV, retourneer aantal rijen."""
    path = DATA_DIR / f"{name}.csv"
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"  -> {path.name} ({len(df):,} rijen)")
    return len(df)

def main() -> None:
    """Laad validatiedata en exporteer als bevoren snapshot."""
    print(f"DV2-adviesvalidatie snapshot-export naar {DATA_DIR}\n")

                                                                    
    print("Data laden uit PostgreSQL (scope=corpus_keuzes)...")
    try:
        validation_data = load_validation_data(
            scope="corpus_keuzes",
            include_english=False
        )
    except Exception as e:
        print(f"FOUT bij load_validation_data: {e}")
        raise

    df_docs = validation_data.df_docs
    df_aanbevelingen = validation_data.df_aanbevelingen
    df_problemen = validation_data.df_problemen

    print(f"  Geladen: {len(df_docs):,} adviesrapporten")
    print(f"           {len(df_aanbevelingen):,} aanbevelingen")
    print(f"           {len(df_problemen):,} probleemdefinities\n")

                                    
    print("List/dict-kolommen serialiseren...")
    df_docs = _serialize_dataframe(df_docs)
    df_aanbevelingen = _serialize_dataframe(df_aanbevelingen)
    df_problemen = _serialize_dataframe(df_problemen)
    print("  OK\n")

                   
    print("CSV's schrijven...")
    manifest: dict[str, object] = {
        "peildatum": PEILDATUM,
        "scope": SCOPE,
        "geexporteerd_op": datetime.now().isoformat(timespec="seconds"),
        "beschrijving": (
            "171 Kaderwet-colleges (permanent/tijdelijk/eenmalig) via "
            "pipeline.v_usable_advies_* + corpus.adviesdocumenten + "
            "register.adviescollege_fasen (CTE, Kaderwet=TRUE + instellingsbesluit + "
            "tijd_adviescollege filter), exclude ACOI/CBPD; Nederlands alleen."
        ),
        "rij_aantallen": {
            "df_docs": save(df_docs, "df_docs"),
            "df_aanbevelingen": save(df_aanbevelingen, "df_aanbevelingen"),
            "df_problemen": save(df_problemen, "df_problemen"),
        },
    }

                      
    (DATA_DIR / "_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"  -> _manifest.json\n")

                  
    print("Klaar.")
    print(f"  Snapshot opgeslagen in: {DATA_DIR}")
    print(f"  Peildatum: {PEILDATUM}")
    print(f"  Scope: {SCOPE}")
    print(f"  Documenten: {manifest['rij_aantallen']['df_docs']:,}")
    print(f"  Aanbevelingen: {manifest['rij_aantallen']['df_aanbevelingen']:,}")
    print(f"  Probleemdefinities: {manifest['rij_aantallen']['df_problemen']:,}")

if __name__ == "__main__":
    main()
