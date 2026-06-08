
from __future__ import annotations

import sys
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from pg_database.checks.advies_validatie.data_loading import _get_db_connection

SEED = 100
N_RESAMPLE = 100


KLASSE6 = {
    "overgenomen": "substantieel",
    "gedeeltelijk_overgenomen": "substantieel",
    "herformuleerd": "substantieel",
    "procedureel_doorgezet": "procedureel",
    "uitgesteld_voor_later_besluit": "procedureel",
    "gerelativeerd": "retorisch",
    "gekoppeld_aan_bestaand_beleid": "retorisch",
    "erkend_zonder_actie": "retorisch",
    "afgewezen": "afgewezen",
    "niet_herkenbaar_verwerkt": "niet_behandeld",
    "onduidelijk": "ambigu",
}
VANGNET = {"onduidelijk", "niet_herkenbaar_verwerkt"}


POSTFIX_RUN_DATUM = "2026-06-03"


SCOPE_CTE = """
    WITH scope_fasen AS (
        SELECT f.id FROM register.adviescollege_fasen f
        JOIN dashboard_public.colleges c ON c.id = f.id
        WHERE f.kaderwet IS TRUE
          AND c.instellingsbesluit_document_id IS NOT NULL
          AND f.tijd_adviescollege IN ('Permanent adviescollege',
                                        'Tijdelijk adviescollege',
                                        'Eenmalig',
                                        'Eenmalig adviescollege')
          AND f.officiele_naam NOT ILIKE '%Autoriteit Persoonsgegevens%'
          AND f.officiele_naam NOT ILIKE '%College Bescherming Persoonsgegevens%'
    )
"""


FILTER_SQL = f"""
    FROM pipeline.kabinetsreactie_aanbeveling_matches m
    JOIN pipeline.kabinetsreactie_analyse a
      ON a.document_id = m.document_id AND a.run_id = m.run_id
    JOIN pipeline.analyse_runs r ON r.run_id = a.run_id
    JOIN corpus.adviesdocumenten d ON d.id = a.advies_document_id
    JOIN scope_fasen sf ON sf.id = d.adviescollege_id
    LEFT JOIN register.adviescollege_fasen f ON f.id = d.adviescollege_id
    WHERE d.is_english IS NOT TRUE
      AND r.started_at >= '{POSTFIX_RUN_DATUM}'
"""

def _modal(lst):
    if not isinstance(lst, list) or not lst:
        return None
    vals = [str(x) for x in lst if x not in (None, "")]
    if not vals:
        return None
    return Counter(vals).most_common(1)[0][0]

def load_elementen() -> pd.DataFrame:
    conn = _get_db_connection()
    sql = f"""
        {SCOPE_CTE}
        SELECT
            m.document_id                              AS reactie_id,
            a.advies_document_id                       AS advies_id,
            m.advies_element_id,
            m.advies_element_type,
            m.verwerkingslabel,
            m.confidence,
            EXTRACT(YEAR FROM a.datum_reactie_parsed)::int AS jaar,
            COALESCE(f.officiele_naam, 'onbekend')     AS college,
            f.tijd_adviescollege                        AS collegetype_raw,
            (m.finale_verwerkingsitem #> '{{match_bewijs,kabinetsposities}}')        AS kpos_list,
            (m.finale_verwerkingsitem #> '{{match_bewijs,beleidsmatige_opvolging}}') AS opv_list
        {FILTER_SQL}
    """
    df = pd.read_sql(sql, conn)
    conn.close()

    def parse(v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except json.JSONDecodeError:
                return None
        return _modal(v)

    df["kabinetspositie"] = df["kpos_list"].apply(parse).fillna("onbekend")
    df["beleidsmatige_opvolging"] = df["opv_list"].apply(parse).fillna("onbekend")
    df = df.drop(columns=["kpos_list", "opv_list"])
    df["klasse6"] = df["verwerkingslabel"].map(KLASSE6).fillna("ambigu")


    collegetype_mapping = {
        'Permanent adviescollege': 'vast',
        'Tijdelijk adviescollege': 'tijdelijk',
        'Eenmalig': 'eenmalig',
        'Eenmalig adviescollege': 'eenmalig'
    }
    df["collegetype"] = df["collegetype_raw"].map(collegetype_mapping).fillna("onbekend")

    return df

def wilson_ci(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))) / denom
    return (max(0.0, center - half), min(1.0, center + half))

def verdeling(series: pd.Series) -> pd.DataFrame:
    n = len(series)
    vc = series.value_counts()
    rows = []
    for label, k in vc.items():
        lo, hi = wilson_ci(int(k), n)
        rows.append({
            "categorie": label, "n": int(k), "aandeel_pct": round(100 * k / n, 1),
            "ci95_laag_pct": round(100 * lo, 1), "ci95_hoog_pct": round(100 * hi, 1),
        })
    return pd.DataFrame(rows)

def cramers_v(x: pd.Series, y: pd.Series) -> dict:
    tab = pd.crosstab(x, y)
    chi2, p, _, _ = chi2_contingency(tab)
    n = tab.values.sum()
    r, k = tab.shape
    v = math.sqrt((chi2 / n) / max(1, (min(r, k) - 1)))
    return {"cramers_v": round(v, 4), "chi2": round(chi2, 1), "p_value": p, "n": int(n)}

def cramers_v_clustered(df: pd.DataFrame, label_col: str, x_col: str = "advies_element_type") -> dict:
    rng = np.random.default_rng(SEED)
    vs = []
    groups = df.groupby("reactie_id").indices
    idx_per_group = {g: np.array(ix) for g, ix in groups.items()}
    for _ in range(N_RESAMPLE):
        picks = [rng.choice(ix) for ix in idx_per_group.values()]
        sub = df.iloc[picks]
        vs.append(cramers_v(sub[x_col], sub[label_col])["cramers_v"])
    vs = np.array(vs)
    return {"mediaan": round(float(np.median(vs)), 4),
            "p05": round(float(np.percentile(vs, 5)), 4),
            "p95": round(float(np.percentile(vs, 95)), 4)}

def sensitivity_varianten(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    varianten = {
        "incl_alles": df,
        "excl_onduidelijk": df[df["verwerkingslabel"] != "onduidelijk"],
        "excl_beide_vangnet": df[~df["verwerkingslabel"].isin(VANGNET)],
    }
    for naam, d in varianten.items():
        for et in ["aanbeveling", "probleemdefinitie"]:
            sub = d[d["advies_element_type"] == et]
            n = len(sub)
            rows.append({
                "variant": naam, "elementtype": et, "n": n,
                "substantieel_pct": round(100 * (sub["klasse6"] == "substantieel").mean(), 1) if n else 0.0,
                "retorisch_pct": round(100 * (sub["klasse6"] == "retorisch").mean(), 1) if n else 0.0,
            })
    return pd.DataFrame(rows)

def collegetype_analyse(df: pd.DataFrame) -> dict:

    rows = []
    for ct in df["collegetype"].unique():
        sub = df[df["collegetype"] == ct]
        n_elem = len(sub)
        n_reacties = sub["reactie_id"].nunique()
        n_adviezen = sub["advies_id"].nunique()


        klasse_counts = sub["klasse6"].value_counts()
        klasse_totals = {
            "substantieel": 0, "retorisch": 0, "ambigu": 0,
            "niet_behandeld": 0, "procedureel": 0, "afgewezen": 0
        }
        for k in klasse_totals:
            klasse_totals[k] = klasse_counts.get(k, 0)

        row = {
            "collegetype": ct,
            "n_elementen": n_elem,
            "n_reacties": n_reacties,
            "n_adviezen": n_adviezen,
        }
        for k, count in klasse_totals.items():
            pct = round(100 * count / n_elem, 1) if n_elem > 0 else 0.0
            row[f"pct_{k}"] = pct
        rows.append(row)

    crosstab_6 = pd.DataFrame(rows).sort_values("n_elementen", ascending=False)


    cramers_6 = cramers_v(df["collegetype"], df["klasse6"])
    cramers_6_clustered = cramers_v_clustered(df, "klasse6", x_col="collegetype")
    cramers_11 = cramers_v(df["collegetype"], df["verwerkingslabel"])

    return {
        "crosstab_6": crosstab_6,
        "cramers_6": cramers_6,
        "cramers_6_clustered": cramers_6_clustered,
        "cramers_11": cramers_11,
    }

def meetkwaliteit_stratificatie(df: pd.DataFrame) -> pd.DataFrame:
    per_reactie = df.groupby("reactie_id")["verwerkingslabel"].apply(
        lambda s: (s == "onduidelijk").mean()
    )
    bins = pd.cut(per_reactie, [-0.01, 1 / 3, 2 / 3, 1.01],
                  labels=["laag_onduidelijk(<33%)", "midden(33-67%)", "hoog_onduidelijk(>=67%)"])
    df2 = df.merge(bins.rename("kwaliteit_proxy"), left_on="reactie_id", right_index=True)
    rows = []
    for kw, d in df2.groupby("kwaliteit_proxy", observed=True):
        n = len(d)
        rows.append({
            "kwaliteit_proxy": kw, "n_reacties": d["reactie_id"].nunique(), "n_elementen": n,
            "substantieel_pct": round(100 * (d["klasse6"] == "substantieel").mean(), 1),
            "retorisch_pct": round(100 * (d["klasse6"] == "retorisch").mean(), 1),
            "onduidelijk_pct": round(100 * (d["verwerkingslabel"] == "onduidelijk").mean(), 1),
        })
    return pd.DataFrame(rows)

def dekking() -> dict:
    conn = _get_db_connection()
    q = f"""
        {SCOPE_CTE}
        SELECT
            count(*) AS n_reacties,
            sum(CASE WHEN COALESCE((a.inhoudelijke_tellingen->>'advies_elementen_totaal')::int,0) > 0
                     THEN 1 ELSE 0 END) AS met_elementen,
            sum(CASE WHEN COALESCE((a.inhoudelijke_tellingen->>'advies_elementen_totaal')::int,0) = 0
                     THEN 1 ELSE 0 END) AS zonder_elementen
        FROM pipeline.kabinetsreactie_analyse a
        JOIN pipeline.analyse_runs r ON r.run_id = a.run_id
        JOIN corpus.adviesdocumenten d ON d.id = a.advies_document_id
        JOIN scope_fasen sf ON sf.id = d.adviescollege_id
        WHERE d.is_english IS NOT TRUE
          AND r.started_at >= '{POSTFIX_RUN_DATUM}'
    """
    df = pd.read_sql(q, conn)
    conn.close()
    return df.iloc[0].to_dict()

def run():
    df = load_elementen()
    res = {}
    res["n_elementen"] = len(df)
    res["n_reacties"] = df["reactie_id"].nunique()
    res["n_adviezen"] = df["advies_id"].nunique()
    res["per_type_n"] = df["advies_element_type"].value_counts().to_dict()
    res["dekking"] = dekking()

    res["verdeling_11"] = verdeling(df["verwerkingslabel"])
    res["verdeling_6"] = verdeling(df["klasse6"])
    res["verdeling_11_per_type"] = {
        et: verdeling(df[df["advies_element_type"] == et]["verwerkingslabel"])
        for et in ["aanbeveling", "probleemdefinitie"]
    }
    res["verdeling_6_per_type"] = {
        et: verdeling(df[df["advies_element_type"] == et]["klasse6"])
        for et in ["aanbeveling", "probleemdefinitie"]
    }


    res["dim_positie_per_type"] = {
        et: verdeling(df[df["advies_element_type"] == et]["kabinetspositie"])
        for et in ["aanbeveling", "probleemdefinitie"]
    }
    res["dim_opvolging_per_type"] = {
        et: verdeling(df[df["advies_element_type"] == et]["beleidsmatige_opvolging"])
        for et in ["aanbeveling", "probleemdefinitie"]
    }


    res["cramers_11"] = cramers_v(df["advies_element_type"], df["verwerkingslabel"])
    res["cramers_6"] = cramers_v(df["advies_element_type"], df["klasse6"])
    res["cramers_11_clustered"] = cramers_v_clustered(df, "verwerkingslabel")
    res["cramers_6_clustered"] = cramers_v_clustered(df, "klasse6")
    epd = df.groupby("reactie_id").size()
    res["elementen_per_reactie"] = {
        "mediaan": float(epd.median()), "q1": float(epd.quantile(.25)),
        "q3": float(epd.quantile(.75)), "min": int(epd.min()), "max": int(epd.max())}

    res["sensitivity"] = sensitivity_varianten(df)
    res["meetkwaliteit"] = meetkwaliteit_stratificatie(df)
    res["collegetype"] = collegetype_analyse(df)

    epa = df.groupby("advies_id").size()
    res["elementen_per_advies"] = {
        "mediaan": float(epa.median()), "q1": float(epa.quantile(.25)), "q3": float(epa.quantile(.75))}
    res["_df"] = df
    return res

def _print(res):
    print(f"\nNOEMER (DV2-gefilterd): {res['n_elementen']} elementen / "
          f"{res['n_reacties']} reacties / {res['n_adviezen']} adviezen")
    print(f"Per type: {res['per_type_n']}")
    print(f"Dekking: {res['dekking']}")
    print(f"Elementen per reactie: {res['elementen_per_reactie']}")
    print("\n--- 6-klasse verdeling (corpusbreed) ---")
    print(res["verdeling_6"].to_string(index=False))
    print("\n--- 11-label verdeling (corpusbreed) ---")
    print(res["verdeling_11"].to_string(index=False))
    for et in ["aanbeveling", "probleemdefinitie"]:
        print(f"\n--- 6-klasse | {et} ---")
        print(res["verdeling_6_per_type"][et].to_string(index=False))
    print("\n--- Kabinetspositie per type ---")
    for et in ["aanbeveling", "probleemdefinitie"]:
        print(f"[{et}]"); print(res["dim_positie_per_type"][et].to_string(index=False))
    print("\n--- Beleidsmatige opvolging per type ---")
    for et in ["aanbeveling", "probleemdefinitie"]:
        print(f"[{et}]"); print(res["dim_opvolging_per_type"][et].to_string(index=False))
    print("\n--- Cramer's V ---")
    print("11-label:", res["cramers_11"], "clustered:", res["cramers_11_clustered"])
    print("6-klasse:", res["cramers_6"], "clustered:", res["cramers_6_clustered"])
    print("\n--- Gevoeligheid (3 noemer-varianten) ---")
    print(res["sensitivity"].to_string(index=False))
    print("\n--- Meetkwaliteit-proxy stratificatie ---")
    print(res["meetkwaliteit"].to_string(index=False))
    print("\n--- Collegetype x 6-klasse (exploratief) ---")
    print(res["collegetype"]["crosstab_6"].to_string(index=False))
    print("Cramer's V 6-klasse:", res["collegetype"]["cramers_6"])
    print("Cramer's V 6-klasse clustered:", res["collegetype"]["cramers_6_clustered"])
    print("Cramer's V 11-label:", res["collegetype"]["cramers_11"])

if __name__ == "__main__":
    _print(run())
