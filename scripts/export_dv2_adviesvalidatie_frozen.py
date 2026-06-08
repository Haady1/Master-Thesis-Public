
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
    if val is None:
        return False
    return isinstance(val, (list, dict))

def _serialize_list_dict(val: Any) -> str | Any:
    if isinstance(val, (list, dict)):
        return json.dumps(val, ensure_ascii=False)
    return val

def _detect_json_columns(df: pd.DataFrame) -> set[str]:
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
    result = df.copy()
    json_cols = _detect_json_columns(result)
    for col in json_cols:
        result[col] = result[col].apply(_serialize_list_dict)
    return result

def save(df: pd.DataFrame, name: str) -> int:
    path = DATA_DIR / f"{name}.csv"
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"  -> {path.name} ({len(df):,} rijen)")
    return len(df)

def main() -> None:
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
