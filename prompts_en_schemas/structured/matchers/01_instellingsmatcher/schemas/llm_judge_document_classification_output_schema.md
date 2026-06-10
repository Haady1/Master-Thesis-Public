# Llm Judge Document Classification Output Schema

## `DOCUMENT_CLASSIFICATION_OUTPUT_SCHEMA`

- Bron: `matcher/instellingsbesluit/llm_judge.py`
- Codebase: `matcher/instellingsbesluit`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `d3ec7592d7f2a263e305c3a958335e00b61a2c03af96ff14988c9d2054aa84af`
- Thesis-relevantie: Main legal-review prompts and JSON contracts for instellingsbesluit discovery and audits.
- Versies:
  - `CLASSIFIER_PROMPT_VERSION`: `instellingsbesluit_classifier_prompt_20260430_primary_text_carrier_v4`
  - `DISCOVERY_CLASSIFIER_PROMPT_VERSION`: `unknown_college_discovery_classifier_prompt_20260504_v1`
  - `KNOWN_COLLEGE_URL_VALIDATION_PROMPT_VERSION`: `known_college_url_validation_prompt_20260504_v1`
  - `VISIBLE_COLLEGE_METADATA_AUDIT_PROMPT_VERSION`: `visible_college_metadata_audit_prompt_20260506_v2`

```python
DOCUMENT_CLASSIFICATION_OUTPUT_SCHEMA: dict[str, Any] = {
    **EXPECTED_OUTPUT_SCHEMA,
    "extracted_metadata": {
        key: value
        for key, value in EXPECTED_OUTPUT_SCHEMA["extracted_metadata"].items()
        if key
        not in {
            "target_college_match",
            "target_match_reason",
            "matched_known_college_name",
            "matched_known_college_id",
        }
    },
}
```
