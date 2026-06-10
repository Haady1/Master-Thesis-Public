# Llm Judge Expected Output Schema

## `EXPECTED_OUTPUT_SCHEMA`

- Bron: `matcher/instellingsbesluit/llm_judge.py`
- Codebase: `matcher/instellingsbesluit`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `ada307536fb1efc6770c2c7932a8dd4722aac874b4c54e3bd1c35815256a38bd`
- Thesis-relevantie: Main legal-review prompts and JSON contracts for instellingsbesluit discovery and audits.
- Versies:
  - `CLASSIFIER_PROMPT_VERSION`: `instellingsbesluit_classifier_prompt_20260430_primary_text_carrier_v4`
  - `DISCOVERY_CLASSIFIER_PROMPT_VERSION`: `unknown_college_discovery_classifier_prompt_20260504_v1`
  - `KNOWN_COLLEGE_URL_VALIDATION_PROMPT_VERSION`: `known_college_url_validation_prompt_20260504_v1`
  - `VISIBLE_COLLEGE_METADATA_AUDIT_PROMPT_VERSION`: `visible_college_metadata_audit_prompt_20260506_v2`

```python
EXPECTED_OUTPUT_SCHEMA: dict[str, Any] = {
    "label": "instellingsbesluit|verwant_document|ruis|onzeker",
    "confidence": "float between 0 and 1",
    "document_role": "short role label, e.g. canonical_regulation, appendix_copy, appointment, out_of_scope",
    "document_function": (
        "establishes_target_college|establishes_temporary_college|"
        "establishes_permanent_college|converts_temporary_to_permanent|"
        "establishes_appointment_committee|extends_existing|amends_existing|"
        "abolishes_existing|appointment_or_composition|compensation|"
        "explanatory_attachment|advice_report|parliamentary_context|noise|unknown"
    ),
    "phase_type": "permanent|tijdelijk|eenmalig|not_applicable|unknown",
    "canonical_status": "canonical_primary|primary_text_in_noncanonical_carrier|related_but_not_primary|false_positive|uncertain",
    "negative_reason": (
        "benoemingscommissie|bijlage|ontwerp|toelichting|ander_orgaan|"
        "verlenging|wijziging|opheffing|kopie|buiten_kaderwet|"
        "adviesrapport|onvoldoende_bewijs|null"
    ),
    "reason": "short Dutch explanation of the classification",
    "evidence_quote": "short decisive quote or null",
    "improvement_hint": "optional retrieval/rerank improvement hint or null",
    "extracted_metadata": {
        "official_name": "official council/body name or null",
        "target_entity_name": "body that this document actually creates/administers, or null",
        "is_primary_institution_document": "ja|nee|onzeker",
        "target_college_match": "ja|nee|onzeker",
        "target_match_reason": "short explanation of why this document does or does not match candidate.college",
        "matched_known_college_name": "known/extracted college name this document belongs to, or null",
        "matched_known_college_id": "known adviescolleges.id if explicitly known from deterministic post-processing, else null",
        "kaderwet_scope": "ja|nee|onzeker",
        "college_type": "permanent|tijdelijk|eenmalig|onzeker",
        "phase_type": "permanent|tijdelijk|eenmalig|not_applicable|unknown",
        "legal_basis_article": "article 4|article 5|article 6|article 79|other|null",
        "founding_date": "YYYY-MM-DD or natural-language date from text or null",
        "abolition_date": "YYYY-MM-DD, natural-language end condition, or null",
        "founding_reason": "why the body was created, or null",
        "function": "formal task/function of the body, or null",
        "issuing_authority": "minister(s), Crown, legislature or null",
        "canonical_document_id": "canonical document id if visible/inferable, else null",
        "canonical_reference": "canonical title/publication reference if visible/inferable, else null",
        "relationship_type": (
            "primary|benoeming|vergoeding|wijziging|verlenging|opheffing|"
            "administratief|adviesrapport|vervolgadvies|kabinetsreactie_candidate|"
            "kamerbrief|kamerstuk_context|parlementaire_doorwerking_candidate|"
            "bijlage_copy|concept|toelichting|temporary_to_permanent_conversion|"
            "appointment_committee|ruis|onzeker"
        ),
        "relation_group": (
            "institution|administration|advice|cabinet_response|"
            "parliamentary_context|noise|uncertain"
        ),
        "carrier_type": (
            "bijlage|kamerstuk|kamerbrief|staatscourant|staatsblad|beslisnota|"
            "concept|afschrift|scan|html|pdf|null"
        ),
        "canonical_status": "canonical_primary|primary_text_in_noncanonical_carrier|related_but_not_primary|false_positive|uncertain",
        "negative_reason": (
            "benoemingscommissie|bijlage|ontwerp|toelichting|ander_orgaan|"
            "verlenging|wijziging|opheffing|kopie|buiten_kaderwet|"
            "adviesrapport|onvoldoende_bewijs|null"
        ),
        "has_explicit_kaderwet_adviescolleges_art_4": "boolean",
        "has_explicit_kaderwet_adviescolleges_art_5": "boolean",
        "has_explicit_kaderwet_adviescolleges_art_6": "boolean",
        "has_article_79_grondwet": "boolean",
        "has_formal_statutory_institution": "boolean",
        "has_operational_institution_clause": "boolean",
        "has_task_to_advise_public_body": "boolean",
        "has_policy_or_legislation_advice_scope": "boolean",
        "has_individual_case_or_decision_advice_scope": "boolean",
        "has_implementation_or_coordination_scope": "boolean",
        "has_appointment_or_selection_scope": "boolean",
        "has_internal_or_interdepartmental_body": "boolean",
        "has_table_platform_or_consultation_body": "boolean",
        "has_research_supervision_scope": "boolean",
        "has_external_independent_membership": "boolean",
        "has_only_ambtelijke_membership": "boolean",
        "has_project_or_evaluation_or_monitoring_scope": "boolean",
        "has_wet_vergoedingen_reference": "boolean",
        "has_kaderwet_zbo_reference": "boolean",
        "is_wetsvoorstel_or_bijlage_or_rvs_advice": "boolean",
        "is_amendment_extension_repeal_or_appointment_only": "boolean",
        "says_aligns_with_kaderwet_but_not_under_it": "boolean",
        "negative_scope_family": (
            "individual_case_or_decision_advice|implementation_or_coordination|"
            "appointment_or_selection|internal_or_interdepartmental|"
            "table_platform_or_consultation|research_supervision|"
            "project_or_evaluation_or_monitoring|null"
        ),
        "notable_details": ["brief legally relevant details"],
    },
}
```
