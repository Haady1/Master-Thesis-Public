# Llm Judge Visible College Metadata Audit Output Schema

## `VISIBLE_COLLEGE_METADATA_AUDIT_OUTPUT_SCHEMA`

- Bron: `matcher/instellingsbesluit/llm_judge.py`
- Codebase: `matcher/instellingsbesluit`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `7df488f947cd6e41a325db65db33ee949e32ac0090a777240d26c92a0a38eddb`
- Thesis-relevantie: Main legal-review prompts and JSON contracts for instellingsbesluit discovery and audits.
- Versies:
  - `CLASSIFIER_PROMPT_VERSION`: `instellingsbesluit_classifier_prompt_20260430_primary_text_carrier_v4`
  - `DISCOVERY_CLASSIFIER_PROMPT_VERSION`: `unknown_college_discovery_classifier_prompt_20260504_v1`
  - `KNOWN_COLLEGE_URL_VALIDATION_PROMPT_VERSION`: `known_college_url_validation_prompt_20260504_v1`
  - `VISIBLE_COLLEGE_METADATA_AUDIT_PROMPT_VERSION`: `visible_college_metadata_audit_prompt_20260506_v2`

```python
VISIBLE_COLLEGE_METADATA_AUDIT_OUTPUT_SCHEMA: dict[str, Any] = {
    "adviescollege_id": "integer or null",
    "huidige_naam": "current official name or null",
    "naam_correct": "ja|nee|onzeker",
    "juiste_naam": "correct official name, niet gevonden, onzeker or null",
    "naamcorrectie_toelichting": "short explanation",
    "naamvarianten_in_bron": ["visible name variants"],
    "huidige_startdatum": "current start date or null",
    "startdatum_correct": "ja|nee|onzeker",
    "juiste_startdatum": "correct start date, niet gevonden, onzeker or null",
    "startdatum_bronpassage": "source passage or null",
    "huidige_einddatum": "current end date or null",
    "einddatum_correct": "ja|nee|onzeker",
    "juiste_einddatum": "correct end date, source formulation, niet gevonden, onzeker or null",
    "einddatum_bronpassage": "source passage or null",
    "huidige_status": "current status or null",
    "status_correct_voor_zover_bron_aangeeft": "ja|nee|onzeker",
    "juiste_status_voor_zover_bron_aangeeft": (
        "lopend_voor_zover_bron_aangeeft|afgerond_voor_zover_bron_aangeeft|"
        "permanent|buiten_scope|onzeker"
    ),
    "status_toelichting": "short explanation",
    "huidige_document_url": "current document URL or null",
    "hoofd_status": "correct|waarschijnlijk_correct|fout|onzeker",
    "juiste_bron_url": "correct source URL, niet gevonden in input, onzeker or null",
    "broncorrectie_toelichting": "short explanation",
    "kandidaat_status_huidig": "current kandidaat_status or null",
    "kandidaat_status_correct": "ja|nee|onzeker",
    "juiste_kandidaat_status": "echt_kaderwet|permanent_wettelijk_adviescollege|buiten_scope|onzeker",
    "phase_type_huidig": "current phase_type or null",
    "phase_type_correct": "ja|nee|onzeker",
    "juiste_phase_type": "permanent|tijdelijk|eenmalig|buiten_scope|onzeker",
    "legal_basis_article": "article 4|article 5|article 6|article 79|other|null",
    "juridische_grondslag": "literal legal basis or null",
    "kaderwet_grondslag_gevonden": "ja|nee|onzeker",
    "alleen_vergoedingsgrondslag": "ja|nee|onzeker",
    "instellingsclausule_gevonden": "ja|nee|onzeker",
    "instellingsclausule": "source passage or null",
    "actuele_status_later_niet_controleerbaar": "ja|nee|onzeker",
    "typewisseling_gevonden_in_deze_bron": "ja|nee|onzeker",
    "naamwijziging_gevonden_in_deze_bron": "ja|nee|onzeker",
    "false_positive_reden": ["allowed false-positive reason values"],
    "correctie_nodig": "ja|nee|onzeker",
    "korte_toelichting": "short explanation",
    "samenvatting_bullets": ["maximum five short bullets"],
}
```
