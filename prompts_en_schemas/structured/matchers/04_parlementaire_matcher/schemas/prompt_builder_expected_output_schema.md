# Prompt Builder Expected Output Schema

## `EXPECTED_OUTPUT_SCHEMA`

- Bron: `matcher/parlementair_v2/ai_review/prompt_builder.py`
- Codebase: `matcher/parlementair_v2`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `e4af2e4fcc4ff105ee840e3b9ab1bd875d69d9a6cba3242d1d006f98cc32c4dc`
- Thesis-relevantie: LLM review prompt and expected output contract for parliamentary uptake candidates.
- Versies:
  - `PROMPT_VERSION`: `parlementair_v2_ai_document_review_prompt_20260517_v1`

```python
EXPECTED_OUTPUT_SCHEMA: dict[str, Any] = {
    "document_assessment": {
        "document_id": "string",
        "advice_id": "string",
        "document_connection": "ruis | context | procedureel_spoor | inhoudelijk_verbonden | expliciet_verbonden",
        "connection_reason": "string",
        "primary_parliamentary_function": (
            "aanbieden | agenderen | controleren | verantwoorden | financieren | "
            "institutionaliseren | wetgeven | bekritiseren | uitvoeren_voortgang_melden | "
            "adviesaanvraag_motivering | adviesproces_aankondiging | "
            "overig | geen_relevante_functie"
        ),
        "secondary_parliamentary_functions": [],
        "actors_using_advice_content": [],
        "explicit_reference_to_advice": False,
        "explicit_reference_to_advice_college": False,
        "explicit_reference_to_cabinet_response": False,
        "send_to_element_matching": False,
        "overall_evidence_strength": "sterk | middel | zwak | geen",
        "short_summary": "maximaal 3 zinnen",
    },
    "document_level_evidence": [
        {
            "quote": "kort parlementair fragment",
            "location": "pagina/alinea/fragment indien beschikbaar",
            "shows": "waarom dit fragment relevant is",
        }
    ],
    "element_matches": [
        {
            "element_id": "string",
            "element_type": "probleemdefinitie | aanbeveling",
            "element_summary": "string",
            "processing_function": (
                "referentieel_procedureel_gebruik | conceptueel_gebruik | "
                "instrumenteel_handelingsgericht_gebruik | legitimerend_substantierend_gebruik | "
                "strategisch_politiek_gebruik | controlerend_gebruik | conflictualiserend_gebruik | "
                "mobiliserend_agenderend_gebruik | representatief_gebruik | "
                "verantwoordingsafdwingend_gebruik | alternatief_beleidsvormend_gebruik | "
                "geen_inhoudelijke_verwerking"
            ),
            "match_type": (
                "overgenomen | gedeeltelijk_overgenomen | herformuleerd | afgewezen | "
                "gerelativeerd | gekoppeld_aan_bestaand_beleid | gebruikt_als_kritiek_op_kabinetsbeleid | "
                "gebruikt_als_steun_voor_alternatief_voorstel | gebruikt_om_uitvoering_af_te_dwingen | "
                "gebruikt_om_uitstel_of_gebrek_aan_reactie_te_bekritiseren | "
                "gebruikt_om_toezeggingen_te_controleren | procedureel_opgevolgd | "
                "financieel_institutioneel_opgevolgd | alleen_genoemd"
            ),
            "direction_of_use": (
                "steunend | kritisch | vragend_controlerend | alternatief | neutraliserend | "
                "legitimerend | mobiliserend | onduidelijk"
            ),
            "actor": (
                "kabinet_bewindspersoon | coalitiepartij | oppositiepartij | individuele_kamerleden | "
                "kamercommissie | eerste_kamer | tweede_kamer | indiener_motie_amendement | "
                "vragensteller | niet_toe_te_wijzen"
            ),
            "advice_quote": "kort adviesfragment",
            "parliamentary_quote": "kort parlementair fragment",
            "location_in_parliamentary_document": "string",
            "evidence_strength": "sterk | middel | zwak | geen",
            "count_as_processing": False,
            "interpretation": "korte uitleg",
        }
    ],
    "non_matches_or_noise": [
        {"issue": "string", "reason": "string", "quote_if_relevant": "string"}
    ],
    "final_judgement": {
        "usable_for_thesis_analysis": False,
        "use_as": "inhoudelijke verwerking | procedureel spoor | context | ruis | grensgeval",
        "reason": "string",
        "warnings": [],
    },
}
```
