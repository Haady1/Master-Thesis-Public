# Diagnostic Judge Expected Diagnostic Schema

## `EXPECTED_DIAGNOSTIC_SCHEMA`

- Bron: `matcher/instellingsbesluit/diagnostic_judge.py`
- Codebase: `matcher/instellingsbesluit`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `technical`
- SHA256: `b1d76b5bed136b6df6b3287c5be1aac6cdb8e32acf2652347f0318572c80ce7d`
- Thesis-relevantie: Technical diagnostic prompt/schema for explaining pipeline failures.

```python
EXPECTED_DIAGNOSTIC_SCHEMA: dict[str, Any] = {
    "case_id": "string or null",
    "legal_truth": {
        "correct_label": "instellingsbesluit|verwant_document|ruis|onzeker",
        "correct_relationship_type": (
            "primary|bijlage|concept|benoeming|wijziging|verlenging|opheffing|"
            "toelichting|ruis|onzeker|null"
        ),
        "canonical_document_id": "string or null",
        "short_explanation": "Dutch explanation of what the document actually is",
    },
    "why_pipeline_was_misled": {
        "primary_failure_type": (
            "retrieval_miss|retrieval_noise|merge_dedup_gap|canonical_link_gap|"
            "rerank_false_positive|rerank_false_negative|judge_prompt_gap|"
            "metadata_extraction_gap|data_quality_gap|expected_hard_case"
        ),
        "secondary_failure_types": ["same enum values if relevant"],
        "evidence": [
            {
                "signal": "exact field/phrase/score/reason",
                "interpretation": "why this signal matters",
            }
        ],
    },
    "codex_improvement_brief": {
        "priority": "high|medium|low",
        "likely_targets": [
            {
                "pipeline_area": (
                    "retrieval text patterns|semantic query templates|merge/dedup stage|"
                    "rerank scoring rules|Jina candidate text/query construction|"
                    "LLM judge prompt/schema|canonical document linking|review/export schema|"
                    "regression tests"
                ),
                "change_hypothesis": "specific change Codex should investigate",
                "why_this_target": "evidence-based reason",
                "risk": "what could go wrong if changed too broadly",
            }
        ],
        "suggested_regression_test": {
            "test_name": "descriptive snake_case name",
            "fixture_summary": "minimal document/candidate setup",
            "expected_assertion": "what must be true after the fix",
        },
    },
    "confidence": "float between 0 and 1",
}
```
