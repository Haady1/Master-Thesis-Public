# Llm Judge Known College Url Validation Output Schema

## `KNOWN_COLLEGE_URL_VALIDATION_OUTPUT_SCHEMA`

- Bron: `matcher/instellingsbesluit/llm_judge.py`
- Codebase: `matcher/instellingsbesluit`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `85166de36f71b8c1494fe7d2d3b09e0b6529c4a174481dc7bdd4826401485ae4`
- Thesis-relevantie: Main legal-review prompts and JSON contracts for instellingsbesluit discovery and audits.
- Versies:
  - `CLASSIFIER_PROMPT_VERSION`: `instellingsbesluit_classifier_prompt_20260430_primary_text_carrier_v4`
  - `DISCOVERY_CLASSIFIER_PROMPT_VERSION`: `unknown_college_discovery_classifier_prompt_20260504_v1`
  - `KNOWN_COLLEGE_URL_VALIDATION_PROMPT_VERSION`: `known_college_url_validation_prompt_20260504_v1`
  - `VISIBLE_COLLEGE_METADATA_AUDIT_PROMPT_VERSION`: `visible_college_metadata_audit_prompt_20260506_v2`

```python
KNOWN_COLLEGE_URL_VALIDATION_OUTPUT_SCHEMA: dict[str, Any] = {
    "target_body_name": "target body name",
    "target_category_or_phase": "target category or phase",
    "main_url": "main URL or null",
    "main_document_id": "main document id or null",
    "kandidaat_status": "echt_kaderwet|permanent_wettelijk_adviescollege|buiten_scope|onzeker",
    "hoofd_status": "correct|waarschijnlijk_correct|fout|onzeker",
    "beste_url": "better URL or null",
    "beste_document_id": "better document id or null",
    "official_body_name_in_document": "visible official body name or null",
    "name_variants_or_legal_predecessors": ["visible variants"],
    "document_title": "document title or null",
    "publication_source": "source or null",
    "source_url": "source URL or null",
    "dates": {
        "publication_date": "date or null",
        "decision_date": "date or null",
        "entry_into_force_date": "date or null",
        "start_date": "date or null",
        "end_date": "date or null",
        "expiry_or_repeal_date": "date or null",
        "date_extraction_note": "note or null",
    },
    "college_type": (
        "kaderwet_permanent_article_4|kaderwet_tijdelijk_article_5|"
        "kaderwet_eenmalig_article_6|permanent_wettelijk_article_79_or_statute|"
        "buiten_scope|onzeker"
    ),
    "phase_type": "permanent|tijdelijk|eenmalig|buiten_scope|onzeker",
    "legal_basis": {
        "legal_basis_law": "law or null",
        "legal_basis_article": "article 4|article 5|article 6|article 79|other|null",
        "legal_basis_article_exact": "exact citation or null",
        "legal_basis_text": "text or null",
        "permanent_statutory_basis_text": "text or null",
    },
    "articles": {
        "establishing_article": "article or null",
        "establishing_article_text": "text or null",
        "duration_article": "article or null",
        "duration_article_text": "text or null",
        "entry_into_force_article": "article or null",
        "entry_into_force_article_text": "text or null",
        "remuneration_article": "article or null",
        "remuneration_article_text": "text or null",
        "other_relevant_articles": ["references"],
    },
    "canonical_status": "canonical_official_publication|primary_text_in_noncanonical_carrier|noncanonical_context_only|unknown",
    "carrier_type": "stb|stcrt|wetten_overheid|kamerstuk|bijlage|pdf_scan|other|unknown",
    "relationship_type": (
        "primaire_oprichting|eerdere_fase|latere_permanente_fase|tijdelijke_fase|"
        "eenmalige_fase|wijziging|verlenging|herinstelling|beeindiging|"
        "naamwijziging|benoeming|vergoeding|adviesrapport|toelichting|concept|"
        "bijlage|kopie|ruis|onzeker"
    ),
    "institution_clause_found": "ja|nee|onzeker",
    "kaderwet_basis_found": "ja|nee|onzeker",
    "permanent_statutory_basis_found": "ja|nee|onzeker",
    "remuneration_only_basis": "ja|nee|onzeker",
    "related_links_reviewed": "ja|nee_geen_links_in_input|nee_niet_mogelijk",
    "relevant_related_links": ["related link review objects"],
    "timeline_correction_needed": "ja|nee|onzeker",
    "phase_change_found": "ja|nee|onzeker",
    "better_link_found": "ja|nee|onzeker",
    "negative_scope_family": ["scope family values"],
    "extracted_metadata": {
        "concerns_target_body": "boolean",
        "target_name_exactly_visible": "boolean",
        "target_name_variant_visible": "boolean",
        "creates_body": "boolean",
        "is_primary_operative_act": "boolean",
        "is_amendment": "boolean",
        "is_extension": "boolean",
        "is_reestablishment": "boolean",
        "is_conversion_to_permanent": "boolean",
        "is_repeal": "boolean",
        "is_appointment_or_nomination": "boolean",
        "is_remuneration_document": "boolean",
        "is_advisory_report": "boolean",
        "is_explanatory_or_parliamentary_context": "boolean",
        "contains_article_4_kaderwet": "boolean",
        "contains_article_5_kaderwet": "boolean",
        "contains_article_6_kaderwet": "boolean",
        "contains_article_79_grondwet": "boolean",
        "contains_kaderwet_zbo": "boolean",
        "contains_wet_vergoedingen": "boolean",
        "contains_besluit_vergoedingen": "boolean",
    },
    "evidence": [{"field": "field name", "short_quote": "quote or null", "explanation": "note or null"}],
    "confidence": "float between 0 and 1",
    "opmerking": "short note or null",
}
```
