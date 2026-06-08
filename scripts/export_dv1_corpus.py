
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import URL

import os


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]
DATA_DIR = BASE_DIR / "data" / "dv1"
DATA_DIR.mkdir(parents=True, exist_ok=True)

START_YEAR = 1997
END_YEAR = 2025

load_dotenv(PROJECT_ROOT / ".env")


def env_value(*names: str, default: str | None = None) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default

def build_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    url = URL.create(
        "postgresql+psycopg2",
        username=env_value("PGUSER", "PG_USER", default="postgres"),
        password=env_value("PGPASSWORD", "PG_PASSWORD"),
        host=env_value("PGHOST", "PG_HOST", default="localhost"),
        port=int(env_value("PGPORT", "PG_PORT", default="5432")),
        database=env_value("PGDATABASE", "PG_DATABASE", default="antigravity_research"),
    )
    return url.render_as_string(hide_password=False)

engine = create_engine(build_database_url())
db_inspector = inspect(engine)

def require_read_only(sql: str) -> None:
    stripped = sql.strip().lower()
    if not (stripped.startswith("select") or stripped.startswith("with")):
        raise ValueError("Alleen SELECT/WITH queries zijn toegestaan in dit script.")
    blocked = ("insert", "update", "delete", "drop", "alter", "create", "truncate", "grant", "revoke")
    if re.search(r"\b(" + "|".join(blocked) + r")\b", stripped):
        raise ValueError("Query lijkt een schrijf- of schema-actie te bevatten.")

def read_sql(name: str, sql: str, params: dict | None = None) -> pd.DataFrame:
    require_read_only(sql)
    df = pd.read_sql_query(text(sql), engine, params=params or {})
    print(f"  {name}: {len(df):,} rijen")
    return df

def table_exists(schema: str, table: str) -> bool:
    return db_inspector.has_table(table, schema=schema)

def get_columns(schema: str, table: str) -> set[str]:
    if not table_exists(schema, table):
        return set()
    return {c["name"] for c in db_inspector.get_columns(table, schema=schema)}

def first_existing(columns: set[str], candidates: Iterable[str]) -> str | None:
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None

def sql_expr(alias: str, columns: set[str], candidates: Iterable[str], default: str = "NULL") -> str:
    column = first_existing(columns, candidates)
    return f"{alias}.{column}" if column else default

def clean_unknown(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.strip()
    return cleaned.replace({"": pd.NA, "None": pd.NA, "nan": pd.NA}).fillna("onbekend")

def parse_year_frame(df: pd.DataFrame, date_columns: list[str]) -> pd.DataFrame:
    result = df.copy()
    parsed = pd.Series(pd.NaT, index=result.index, dtype="datetime64[ns]")
    for column in date_columns:
        if column in result.columns:
            candidate = pd.to_datetime(result[column], errors="coerce", utc=True).dt.tz_convert(None)
            parsed = parsed.fillna(candidate)
    result["document_datum"] = parsed
    result["jaar"] = result["document_datum"].dt.year
    return result


def map_matcher(relation_group: str | None) -> str:
    g = (relation_group or "").lower()
    if g == "kabinetsreactie":
        return "3_kabinetsreactie_matcher"
    if g.startswith("instellingsbesluit") or g in {"legal_basis", "institution", "effective_date", "name_change"}:
        return "1_instellingsbesluit_matcher"
    if "parliament" in g:
        return "4_parlementair_matcher"
    if "advies" in g or "advice" in g or g == "adviesdocument" or g == "all_document_types_review":
        return "2_advies_matcher"
    return "overig"

PARLEMENTAIRE_GROEPEN = ("parliamentary_context",)


def save(df: pd.DataFrame, name: str) -> int:
    path = DATA_DIR / f"{name}.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  -> {path.name} ({len(df):,} rijen)")
    return len(df)

def main() -> None:
    print(f"DV1-export naar {DATA_DIR}")
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("Databaseverbinding werkt.\n")

    manifest: dict[str, object] = {
        "geexporteerd_op": datetime.now().isoformat(timespec="seconds"),
        "database": env_value("PGDATABASE", "PG_DATABASE", default="antigravity_research"),
        "periode": [START_YEAR, END_YEAR],
        "rij_aantallen": {},
    }


    print("1. Documentbasis")
    doc_cols = get_columns("corpus", "adviesdocumenten")
    class_cols = get_columns("pipeline", "document_classificatie")
    meta_cols = get_columns("pipeline", "document_metadata")
    report_cols = get_columns("pipeline", "advies_rapport_analyse")
    phase_cols = get_columns("register", "adviescollege_fasen")

    document_unique_expr = sql_expr("d", doc_cols, ["unique_id", "document_unique_id", "uuid"], "d.id::text")
    adviescollege_id_expr = sql_expr("d", doc_cols, ["adviescollege_id", "college_id", "adviescollege_fase_id"], "NULL")
    doc_date_expr = sql_expr("d", doc_cols, ["publicatiedatum", "datum", "datum_publicatie", "created_at", "downloaded_at"], "NULL")
    main_category_expr = sql_expr("c", class_cols, ["final_main_category", "main_category", "hoofdcategorie"], "NULL")
    sub_category_expr = sql_expr("c", class_cols, ["final_sub_category", "sub_category", "subcategorie"], "NULL")
    document_type_expr = sql_expr("c", class_cols, ["document_type", "documenttype", "final_document_type"], "NULL")
    title_expr = sql_expr("m", meta_cols, ["titel", "title", "documenttitel", "document_titel"], "NULL")
    meta_date_expr = sql_expr("m", meta_cols, ["document_datum_parsed", "document_datum", "datum", "documentdatum", "datum_document", "publicatiedatum", "datum_publicatie", "rapport_publicatiedatum"], "NULL")
    gevraagd_expr = sql_expr("m", meta_cols, ["gevraagd_ongevraagd", "gevraagdheid", "advies_status"], "NULL")
    aanvrager_expr = sql_expr("m", meta_cols, ["advies_aanvrager", "aanvrager", "opdrachtgever", "verzoeker", "ministerie"], "NULL")
    ministerie_expr = sql_expr("m", meta_cols, ["ministerie", "departement", "beleidsdepartement"], "NULL")
    veldconsultatie_expr = sql_expr("ra", report_cols, ["veldconsultatie_niveau", "veldconsultatieniveau"], "NULL")
    beleidsveld_expr = sql_expr("ra", report_cols, ["beleidsveld", "beleidsdomein", "beleidsterrein"], "NULL")
    phase_name_expr = sql_expr("f", phase_cols, ["officiele_naam", "naam", "college_naam"], "NULL")
    phase_type_expr = sql_expr("f", phase_cols, ["type", "fase_type", "status", "college_type"], "NULL")
    phase_start_expr = sql_expr("f", phase_cols, ["startdatum", "start_datum", "datum_start"], "NULL")
    phase_end_expr = sql_expr("f", phase_cols, ["einddatum", "eind_datum", "datum_einde"], "NULL")

    document_sql = f"""
    SELECT
        d.id AS document_id,
        {document_unique_expr} AS document_unique_id,
        {adviescollege_id_expr} AS adviescollege_id,
        {doc_date_expr} AS datum_document_bron,
        {main_category_expr} AS hoofdcategorie,
        {sub_category_expr} AS subcategorie,
        {document_type_expr} AS documenttype,
        {title_expr} AS titel,
        {meta_date_expr} AS datum_metadata,
        {gevraagd_expr} AS gevraagd_ongevraagd,
        {aanvrager_expr} AS advies_aanvrager,
        {ministerie_expr} AS ministerie,
        {veldconsultatie_expr} AS veldconsultatie_niveau,
        {beleidsveld_expr} AS beleidsveld,
        {phase_name_expr} AS adviescollege_naam,
        {phase_type_expr} AS collegefase_type,
        {phase_start_expr} AS collegefase_start,
        {phase_end_expr} AS collegefase_einde
    FROM corpus.adviesdocumenten d
    LEFT JOIN pipeline.document_classificatie c ON c.document_id = d.id
    LEFT JOIN pipeline.document_metadata m ON m.document_id = d.id
    LEFT JOIN pipeline.advies_rapport_analyse ra ON ra.document_id = d.id
    LEFT JOIN register.adviescollege_fasen f ON f.id = {adviescollege_id_expr}
    """
    documents = read_sql("documents", document_sql)
    documents = parse_year_frame(documents, ["datum_metadata", "datum_document_bron"])
    for col in ["hoofdcategorie", "subcategorie", "documenttype", "gevraagd_ongevraagd",
                "advies_aanvrager", "adviescollege_naam", "collegefase_type"]:
        if col in documents.columns:
            documents[col] = clean_unknown(documents[col])
    documents["in_periode"] = documents["jaar"].between(START_YEAR, END_YEAR, inclusive="both")
    sub_norm = documents["subcategorie"].astype("string").str.lower()
    documents["is_adviesrapport"] = sub_norm.str.contains("adviesrapport", na=False)
    documents["is_kabinetsreactie"] = sub_norm.str.contains("kabinetsreactie|kabinets reactie|reactie", na=False)

    documents = documents.drop(columns=["datum_document_bron", "datum_metadata"], errors="ignore")
    manifest["rij_aantallen"]["documents_basis"] = save(documents, "documents_basis")


    print("2. Register-colleges")
    register = read_sql("register_colleges", """
        SELECT id, officiele_naam, type, type_adviescollege, tijd_adviescollege,
               startdatum, einddatum, kaderwet, dashboard_visible,
               relatie_ministerie, thematisch_type
        FROM register.adviescollege_fasen
    """)
    manifest["rij_aantallen"]["register_colleges"] = save(register, "register_colleges")


    print("3. Advies-elementen")
    def element_counts(schema: str, table: str, name: str) -> pd.DataFrame:
        cols = get_columns(schema, table)
        doc_col = first_existing(cols, ["document_id", "advies_document_id"])
        if doc_col is None:
            return pd.DataFrame(columns=["document_id", name])
        return read_sql(name, f"SELECT {doc_col} AS document_id, COUNT(*) AS {name} "
                              f"FROM {schema}.{table} GROUP BY {doc_col}")
    aanb = element_counts("pipeline", "advies_aanbevelingen", "n_aanbevelingen")
    prob = element_counts("pipeline", "advies_probleemdefinities", "n_probleemdefinities")
    elementen = aanb.merge(prob, on="document_id", how="outer")
    elementen[["n_aanbevelingen", "n_probleemdefinities"]] = (
        elementen[["n_aanbevelingen", "n_probleemdefinities"]].fillna(0).astype(int)
    )
    manifest["rij_aantallen"]["advies_elementen"] = save(elementen, "advies_elementen")


    print("4. Kabinetsreactie-paren")
    kr_cols = get_columns("pipeline", "kabinetsreactie_analyse")
    advies_doc_col = first_existing(kr_cols, ["advies_document_id", "advies_id", "source_document_id"])
    reactie_doc_col = first_existing(kr_cols, ["document_id", "kabinetsreactie_document_id", "reactie_document_id"])
    overname_col = first_existing(kr_cols, ["overname_percentage", "overname_pct"])
    telling_col = first_existing(kr_cols, ["inhoudelijke_tellingen", "tellingen_json", "label_tellingen"])
    parts = []
    if advies_doc_col:
        parts.append(f"{advies_doc_col} AS advies_document_id")
    if reactie_doc_col:
        parts.append(f"{reactie_doc_col} AS kabinetsreactie_document_id")
    if overname_col:
        parts.append(f"{overname_col} AS overname_percentage")
    if telling_col:
        parts.append(f"{telling_col} AS inhoudelijke_tellingen")
    kr_pairs = read_sql("kabinetsreactie_pairs",
                        f"SELECT {', '.join(parts)} FROM pipeline.kabinetsreactie_analyse")
    manifest["rij_aantallen"]["kabinetsreactie_pairs"] = save(kr_pairs, "kabinetsreactie_pairs")


    print("5. Matcher-relaties")
    relations = read_sql("relations", """
        SELECT relation_id, relation_group, relation_type, relation_method,
               validation_status, confidence,
               subject_adviescollege_fase_id, object_document_ref_id
        FROM matcher.relations
    """)
    relations["matcher"] = relations["relation_group"].map(map_matcher)
    manifest["rij_aantallen"]["matcher_relations"] = save(relations, "matcher_relations")


    print("6. Kandidaten-samenvatting")
    cand_summary = read_sql("match_candidates_summary", """
        SELECT relation_group, relation_type, COUNT(*) AS kandidaten
        FROM matcher.match_candidates
        GROUP BY relation_group, relation_type
    """)
    cand_summary["matcher"] = cand_summary["relation_group"].map(map_matcher)
    manifest["rij_aantallen"]["matcher_candidates_summary"] = save(cand_summary, "matcher_candidates_summary")


    print("7. Matcher-funnel")
    rel_summary = (relations.groupby(["matcher", "relation_group"], dropna=False)
                   .size().reset_index(name="gevalideerde_relaties"))
    cand_grp = (cand_summary.groupby(["matcher", "relation_group"], dropna=False)["kandidaten"]
                .sum().reset_index())
    funnel = cand_grp.merge(rel_summary, on=["matcher", "relation_group"], how="outer")
    funnel[["kandidaten", "gevalideerde_relaties"]] = (
        funnel[["kandidaten", "gevalideerde_relaties"]].fillna(0).astype(int)
    )
    funnel["verhouding_gevalideerd_op_kandidaten"] = (
        funnel["gevalideerde_relaties"] / funnel["kandidaten"].where(funnel["kandidaten"] > 0)
    )
    funnel = funnel.sort_values(["matcher", "relation_group"])
    manifest["rij_aantallen"]["matcher_funnel"] = save(funnel, "matcher_funnel")


    print("8. Parlementaire links")
    parl = relations[relations["relation_group"].str.lower().str.contains("parliament", na=False)].copy()
    manifest["rij_aantallen"]["parlementaire_links"] = save(parl, "parlementaire_links")


    print("9. College-niveau")
    ib_fasen = set(relations.loc[relations["relation_group"] == "instellingsbesluit_validated_link",
                                 "subject_adviescollege_fase_id"].dropna().astype(int))
    lb_fasen = set(relations.loc[relations["relation_group"] == "legal_basis",
                                 "subject_adviescollege_fase_id"].dropna().astype(int))
    advies_fasen = set(documents.loc[documents["is_adviesrapport"], "adviescollege_id"].dropna().astype(int))
    reactie_fasen = set(documents.loc[documents["is_kabinetsreactie"], "adviescollege_id"].dropna().astype(int))
    def kaderwet_categorie(value: str | None) -> str:
        v = (value or "").lower()
        if "permanent" in v:
            return "permanent"
        if "tijdelijk" in v:
            return "tijdelijk"
        if "eenmalig" in v:
            return "eenmalig"
        return "onbekend"

    college = register.copy()
    college["fase_id"] = college["id"].astype(int)
    college["kaderwet_categorie"] = college["tijd_adviescollege"].map(kaderwet_categorie)
    college["heeft_instellingsbesluit_link"] = college["fase_id"].isin(ib_fasen)
    college["heeft_legal_basis_link"] = college["fase_id"].isin(lb_fasen)
    college["heeft_oprichting_link"] = college["heeft_instellingsbesluit_link"] | college["heeft_legal_basis_link"]
    college["heeft_adviesrapport"] = college["fase_id"].isin(advies_fasen)
    college["heeft_kabinetsreactie"] = college["fase_id"].isin(reactie_fasen)
    manifest["rij_aantallen"]["college_niveau"] = save(college, "college_niveau")


    (DATA_DIR / "_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\n  -> _manifest.json")
    print("\nKlaar. Alle DV1-CSV's staan in", DATA_DIR)

if __name__ == "__main__":
    main()
