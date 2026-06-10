# Llm Judge Discovery Document Classification Output Schema

## `DISCOVERY_DOCUMENT_CLASSIFICATION_OUTPUT_SCHEMA`

- Bron: `matcher/instellingsbesluit/llm_judge.py`
- Codebase: `matcher/instellingsbesluit`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `467a2d89bd21b3beedff666bf9d4906fe2bdd6292b35867fc1a85a0df45fc550`
- Thesis-relevantie: Main legal-review prompts and JSON contracts for instellingsbesluit discovery and audits.
- Versies:
  - `CLASSIFIER_PROMPT_VERSION`: `instellingsbesluit_classifier_prompt_20260430_primary_text_carrier_v4`
  - `DISCOVERY_CLASSIFIER_PROMPT_VERSION`: `unknown_college_discovery_classifier_prompt_20260504_v1`
  - `KNOWN_COLLEGE_URL_VALIDATION_PROMPT_VERSION`: `known_college_url_validation_prompt_20260504_v1`
  - `VISIBLE_COLLEGE_METADATA_AUDIT_PROMPT_VERSION`: `visible_college_metadata_audit_prompt_20260506_v2`

```python
DISCOVERY_DOCUMENT_CLASSIFICATION_OUTPUT_SCHEMA: dict[str, Any] = {
    "label": (
        "ja_kaderwet_adviescollege|ja_permanent_wettelijk_adviescollege|"
        "waarschijnlijk_ja|verwant_maar_niet_primair|nee_buiten_scope|"
        "nee_geen_instelling|nee_geen_officiele_bron|twijfel"
    ),
    "dataset_acceptance": "accept_primary|keep_for_link_expansion|reject|manual_review",
    "confidence": "float between 0 and 1",
    "official_body_name": "official body name visible in the document or null",
    "body_name_variants": ["visible variants"],
    "document_title": "document title or null",
    "publication_source": "official source or null",
    "document_id": "document id or null",
    "source_url": "URL or null",
    "dates": {
        "publication_date": "date or null",
        "decision_date": "date or null",
        "entry_into_force_date": "date or null",
        "start_date": "date or null",
        "end_date": "date or null",
        "expiry_or_repeal_date": "date or null",
        "date_extraction_note": "short note or null",
    },
    "college_type": (
        "kaderwet_permanent_article_4|kaderwet_tijdelijk_article_5|"
        "kaderwet_eenmalig_article_6|permanent_wettelijk_article_79_or_statute|"
        "buiten_scope|onzeker"
    ),
    "phase_type": "permanent|tijdelijk|eenmalig|buiten_scope|onzeker",
    "legal_basis": {
        "legal_basis_law": "law/regulation or null",
        "legal_basis_article": "article 4|article 5|article 6|article 79|other|null",
        "legal_basis_article_exact": "exact citation or null",
        "legal_basis_text": "supporting text or null",
        "permanent_statutory_basis_text": "supporting text or null",
    },
    "articles": {
        "establishing_article": "article number or null",
        "establishing_article_text": "text or null",
        "duration_article": "article number or null",
        "duration_article_text": "text or null",
        "entry_into_force_article": "article number or null",
        "entry_into_force_article_text": "text or null",
        "remuneration_article": "article number or null",
        "remuneration_article_text": "text or null",
        "other_relevant_articles": ["article references"],
    },
    "canonical_status": "canonical_official_publication|primary_text_in_noncanonical_carrier|noncanonical_context_only|unknown",
    "carrier_type": "stb|stcrt|wetten_overheid|kamerstuk|bijlage|pdf_scan|other|unknown",
    "relationship_type": (
        "primaire_oprichting|latere_permanente_fase|tijdelijke_fase|"
        "eenmalige_fase|wijziging|verlenging|herinstelling|beeindiging|"
        "benoeming|vergoeding|adviesrapport|toelichting|concept|bijlage|"
        "kopie|ruis|onzeker"
    ),
    "institution_clause_found": "boolean",
    "institution_clause_text": "text or null",
    "kaderwet_trigger_found": "boolean",
    "permanent_statutory_trigger_found": "boolean",
    "remuneration_only_basis": "boolean",
    "negative_scope_family": ["scope family values"],
    "extracted_metadata": {
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
    "reasoning_summary": "short explanation or null",
}
```
