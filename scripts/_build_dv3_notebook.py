"""Bouwt en voert het DV3-notebook uit op basis van dv3_analyse.py (re-runbaar).

Draai: python thesis/Analyse/_build_dv3_notebook.py
Schrijft thesis/Analyse/DV3_verwerking_advieselementen.ipynb met gevulde outputcellen.
"""
from __future__ import annotations
from pathlib import Path
import nbformat as nbf
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from nbconvert.preprocessors import ExecutePreprocessor

HERE = Path(__file__).resolve().parent
NB_PATH = HERE / "DV3_verwerking_advieselementen.ipynb"

md = new_markdown_cell
co = new_code_cell

cells = [
    md(
        "# DV3 — Verwerking van advieselementen door kabinetsreacties\n\n"
        "**Run van 4 juni 2026.** Dit notebook beantwoordt deelvraag 3 (DV3): *hoe "
        "verhouden kabinetsreacties zich tot afzonderlijke probleemdefinities en "
        "aanbevelingen, en verschilt die verwerking tussen beide elementtypen?*\n\n"
        "Alle cijfers worden **live en re-runbaar** uit de PostgreSQL-database berekend "
        "via `dv3_analyse.py` (geen hardcoded aantallen; klopt ook als er later data "
        "bijkomt). De labels zijn op individueel elementniveau zwak gemeten (zie DV2, "
        "Krippendorff α ≈ 0,19); DV3 rapporteert daarom uitsluitend **geaggregeerde "
        "aandelen**, met meetkwaliteit als gevoeligheid.\n\n"
        "**Changelog**\n"
        "- 2026-06-04: Eerste versie. Noemer = match-rijen, DV2-gefilterd via het "
        "advies-document. Twee dimensies uit `finale_verwerkingsitem.match_bewijs`.\n\n"
        "**Input:** `pipeline.kabinetsreactie_aanbeveling_matches`, "
        "`pipeline.kabinetsreactie_analyse`, `corpus.adviesdocumenten`, "
        "`register.adviescollege_fasen`.  \n"
        "**Output:** tabellen voor de DV3-resultatensectie van de scriptie."
    ),
    md(
        "## Methode: noemer, filter en 11→6 klassenmapping\n\n"
        "De DV2-filter (`is_english IS NOT TRUE` + `dashboard_visible IS TRUE`) wordt "
        "toegepast **via het advies-document** (`a.advies_document_id`), niet via de "
        "reactie — reacties zijn Kamerstukken zonder college-link en zouden anders "
        "onterecht wegvallen. De 11 labels worden samengevat tot 6 grove klassen "
        "volgens de DV2-confusion-matrix."
    ),
    co(
        "import sys\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, str(Path.cwd()))\n"
        "import dv3_analyse as dv3\n\n"
        "print('DV2-consistente filter (via advies-document):')\n"
        "print(dv3.FILTER_SQL)\n"
        "print('11->6 klassenmapping:')\n"
        "for k, v in dv3.KLASSE6.items():\n"
        "    print(f'  {k:32s} -> {v}')"
    ),
    md(
        "## Stap 1 — Laden, noemer en dekking\n\n"
        "Eén rij per advies-element × reactie. De dekkingscontrole laat zien hoeveel "
        "reacties wél/geen elementen opleverden."
    ),
    co(
        "res = dv3.run()\n"
        "df = res['_df']\n"
        "print('NOEMER (DV2-gefilterd):', res['n_elementen'], 'elementen /',\n"
        "      res['n_reacties'], 'reacties /', res['n_adviezen'], 'adviezen')\n"
        "print('Per elementtype:', res['per_type_n'])\n"
        "print('Dekking (alle reacties):', res['dekking'])\n"
        "print('Elementen per reactie:', res['elementen_per_reactie'])\n"
        "print('\\nReconciliatie: de scriptie noemde 13.253/421 (oudere run);'\n"
        "      ' de actuele DB-stand is bovenstaande noemer.')"
    ),
    md(
        "## Stap 3 — Corpusbrede verdeling (11 labels + 6 klassen)\n\n"
        "Met 95%-Wilson-betrouwbaarheidsintervallen op de aandelen."
    ),
    co(
        "from IPython.display import display\n"
        "print('6 grove klassen:'); display(res['verdeling_6'])\n"
        "print('11 labels:'); display(res['verdeling_11'])"
    ),
    md(
        "## Stap 4 — Verdeling per elementtype\n\n"
        "De kern van DV3: verschilt de verwerking tussen aanbevelingen en "
        "probleemdefinities?"
    ),
    co(
        "for et in ['aanbeveling', 'probleemdefinitie']:\n"
        "    print(f'6-klasse | {et}'); display(res['verdeling_6_per_type'][et])\n"
        "for et in ['aanbeveling', 'probleemdefinitie']:\n"
        "    print(f'11-label | {et}'); display(res['verdeling_11_per_type'][et])"
    ),
    md(
        "## Stap 5 — Twee onderliggende dimensies per elementtype\n\n"
        "Het label volgt uit (kabinetspositie × beleidsmatige opvolging). Deze waarden "
        "komen uit `finale_verwerkingsitem.match_bewijs` (modale waarde per element). "
        "Bij `onduidelijk`/`niet_herkenbaar_verwerkt` is er geen positie → `onbekend`; "
        "dat verklaart het hoge `onbekend`-aandeel, vooral bij probleemdefinities."
    ),
    co(
        "print('Kabinetspositie:')\n"
        "for et in ['aanbeveling', 'probleemdefinitie']:\n"
        "    print(f'  [{et}]'); display(res['dim_positie_per_type'][et])\n"
        "print('Beleidsmatige opvolging:')\n"
        "for et in ['aanbeveling', 'probleemdefinitie']:\n"
        "    print(f'  [{et}]'); display(res['dim_opvolging_per_type'][et])"
    ),
    md(
        "## Stap 6 — Statistische vergelijking elementtype × verwerking\n\n"
        "Cramér's V als hoofdmaat (bij n≈11.000 is vrijwel alles 'significant'). "
        "**Clustering-voorbehoud:** elementen binnen één reactie zijn niet onafhankelijk, "
        "dus de chi²-p-waarde is te liberaal. De clustered-spreiding herberekent V op "
        "100 herbemonsteringen van 1 willekeurig element per reactie (seed=100)."
    ),
    co(
        "print('11-label  V =', res['cramers_11']['cramers_v'],\n"
        "      '| clustered mediaan/p05/p95 =', res['cramers_11_clustered'])\n"
        "print('6-klasse  V =', res['cramers_6']['cramers_v'],\n"
        "      '| clustered mediaan/p05/p95 =', res['cramers_6_clustered'])\n"
        "print('chi2 (11-label) =', res['cramers_11']['chi2'], 'p =', res['cramers_11']['p_value'])\n"
        "print('Elementen per reactie (clustering-context):', res['elementen_per_reactie'])"
    ),
    md(
        "## Stap 7 — Gevoeligheid 'onduidelijk' (3 noemer-varianten)\n\n"
        "(1) inclusief alles, (2) exclusief `onduidelijk`, (3) exclusief beide "
        "vangnetcategorieën. Toont hoe sterk de aandelen van die onzekere categorie "
        "afhangen."
    ),
    co("display(res['sensitivity'])"),
    md(
        "## Stap 8 — Meetkwaliteit-stratificatie (proxy)\n\n"
        "Transparante, grove proxy: reacties gegroepeerd naar hun aandeel `onduidelijk` "
        "(laag <33% / midden / hoog ≥67%). Dit is **geen** exacte heruitvoering van het "
        "DV2-usability-kader, maar maakt zichtbaar dat substantiële verwerking samenhangt "
        "met de meetkwaliteit van een reactie."
    ),
    co("display(res['meetkwaliteit'])"),
    md(
        "## Stap 9 — Context en conclusie\n\n"
        "Elementen per advies puur als context; **geen** vergelijking tussen colleges "
        "als zelfstandige bevinding (meetkwaliteit verschilt per college, zie DV2). "
        "DV3 is corpusbreed.\n\n"
        "**Kernbevinding:** aanbevelingen en probleemdefinities worden aantoonbaar "
        "verschillend behandeld (Cramér's V ≈ 0,44 op 11 labels; robuust onder "
        "clustering). Het verschil zit vooral in het hoge aandeel `onduidelijk`/"
        "`niet_herkenbaar_verwerkt` bij probleemdefinities — een meet- én "
        "verwerkingskenmerk dat binnen de DV2-betrouwbaarheidsgrenzen moet worden gelezen."
    ),
    co(
        "print('Elementen per advies:', res['elementen_advies'] if 'elementen_advies' in res\n"
        "      else res['elementen_per_advies'])\n"
        "print('Aantal colleges in scope:', df['college'].nunique())"
    ),
]

nb = new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}

ep = ExecutePreprocessor(timeout=1200, kernel_name="python3")
ep.preprocess(nb, {"metadata": {"path": str(HERE)}})
nbf.write(nb, NB_PATH)
print("Notebook geschreven en uitgevoerd:", NB_PATH)
