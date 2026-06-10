# Comparative Review Role Guidance

## `_role_guidance`

- Bron: `matcher/advies/comparative_review.py`
- Codebase: `matcher/advies`
- Type: `function`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `7ef476f2af8dea25b835592176dbb3af38ddb0f4bb4c4e6702db9a17b498b06e`
- Thesis-relevantie: Comparative review contract for main advice and related-document roles.
- Versies:
  - `COMPARATIVE_REVIEW_PROMPT_VERSION`: `advies_comparative_review_payload_20260517_v1`

```python
def _role_guidance() -> dict[str, str]:
    return {
        MAIN_ADVICE: "The target college's own final advice or adopted report.",
        DUPLICATE_OR_ALTERNATE_PUBLICATION: (
            "An equivalent publication of the same main advice, not a separate "
            "advice."
        ),
        INTERMEDIATE_REPORT: "A partial, interim or earlier advice report.",
        SUPPORTING_STUDY: "A study, appendix or background report supporting advice.",
        OFFERING_LETTER: "A letter offering or forwarding an advice/report.",
        CABINET_RESPONSE: "A cabinet or policy response to the advice/report.",
        STAKEHOLDER_RESPONSE: "A response from a stakeholder or third party.",
        PARLIAMENTARY_CONTEXT: "Parliamentary debate, context or progress material.",
        PROCEDURAL_CONTEXT: "Appointment, establishment, decision note or procedure.",
        TITLE_COLLISION_OR_UNRELATED: "A false positive or unrelated title collision.",
        UNCERTAIN: "Relevant enough to retain but not classifiable from evidence.",
        OTHER_RELEVANT: "Relevant relation that fits no narrower known role.",
        NEW_OR_UNMAPPED_ROLE: "A proposed stable role outside the known role list.",
    }
```
