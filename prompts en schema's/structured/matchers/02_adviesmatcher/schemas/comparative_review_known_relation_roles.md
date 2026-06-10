# Comparative Review Known Relation Roles

## `KNOWN_RELATION_ROLES`

- Bron: `matcher/advies/comparative_review.py`
- Codebase: `matcher/advies`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `8500aefde0c80b8f0df673b1644dd083ce0c6a85c045e863347e8ef91744d3c1`
- Thesis-relevantie: Comparative review contract for main advice and related-document roles.
- Versies:
  - `COMPARATIVE_REVIEW_PROMPT_VERSION`: `advies_comparative_review_payload_20260517_v1`

```python
KNOWN_RELATION_ROLES = (
    MAIN_ADVICE,
    DUPLICATE_OR_ALTERNATE_PUBLICATION,
    INTERMEDIATE_REPORT,
    SUPPORTING_STUDY,
    OFFERING_LETTER,
    CABINET_RESPONSE,
    STAKEHOLDER_RESPONSE,
    PARLIAMENTARY_CONTEXT,
    PROCEDURAL_CONTEXT,
    TITLE_COLLISION_OR_UNRELATED,
    UNCERTAIN,
    OTHER_RELEVANT,
    NEW_OR_UNMAPPED_ROLE,
)
```
