# Run Vlam Response Judge Allowed Target Types

## `ALLOWED_TARGET_TYPES`

- Bron: `matcher/kabinetsreactie/run_vlam_response_judge.py`
- Codebase: `matcher/kabinetsreactie`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `60e847e0d18be59a3e775b6d890f482602973579a4a0522d169c0e207b0307ec`
- Thesis-relevantie: VLAM judgement prompt for deciding whether a document is a real cabinet response.
- Versies:
  - `PROMPT_VERSION`: `kabinetsreactie_vlam_response_judge_20260529_v4`

```python
ALLOWED_TARGET_TYPES = frozenset(
    {
        "supplied_advice",
        "other_advice_or_report",
        "committee_request",
        "motion_or_question",
        "generic_policy",
        "unclear",
    }
)
```
