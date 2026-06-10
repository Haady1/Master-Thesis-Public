# Comparative Review Expected Output Contract

## `_expected_output_contract`

- Bron: `matcher/advies/comparative_review.py`
- Codebase: `matcher/advies`
- Type: `function`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `d2cdf007395ab80a4c58ab766d27f23720dc2df13de3738649eeb8cedbab1f76`
- Thesis-relevantie: Comparative review contract for main advice and related-document roles.
- Versies:
  - `COMPARATIVE_REVIEW_PROMPT_VERSION`: `advies_comparative_review_payload_20260517_v1`

```python
def _expected_output_contract() -> dict[str, Any]:
    list_of_document_ids = "list of candidate_document_id values"
    return {
        "main_advice_document_id": "candidate_document_id or null",
        "multiple_main_advices": "boolean",
        "main_advice_document_ids": list_of_document_ids,
        "relation_roles_by_document_id": {
            "candidate_document_id": list(KNOWN_RELATION_ROLES),
        },
        "duplicate_or_alternate_publication_ids": list_of_document_ids,
        "intermediate_report_ids": list_of_document_ids,
        "supporting_study_ids": list_of_document_ids,
        "offering_letter_ids": list_of_document_ids,
        "cabinet_response_ids": list_of_document_ids,
        "stakeholder_response_ids": list_of_document_ids,
        "parliamentary_context_ids": list_of_document_ids,
        "procedural_context_ids": list_of_document_ids,
        "uncertain_ids": list_of_document_ids,
        "other_relevant": [
            {
                "document_id": "candidate_document_id",
                "role": OTHER_RELEVANT,
                "reason": "short evidence-based reason",
            }
        ],
        "new_or_unmapped_roles": [
            {
                "document_id": "candidate_document_id",
                "role": NEW_OR_UNMAPPED_ROLE,
                "proposed_role": "short stable role name",
                "reason": "why known roles are insufficient",
            }
        ],
        "needs_deep_context_ids": list_of_document_ids,
        "needs_human_review": "boolean",
        "reason": "concise evidence-based reason",
    }
```
