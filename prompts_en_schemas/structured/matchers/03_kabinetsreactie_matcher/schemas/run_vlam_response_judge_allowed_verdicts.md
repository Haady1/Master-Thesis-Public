# Run Vlam Response Judge Allowed Verdicts

## `ALLOWED_VERDICTS`

- Bron: `matcher/kabinetsreactie/run_vlam_response_judge.py`
- Codebase: `matcher/kabinetsreactie`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `770b59bc616f9f3f42c47bf67fc752a33d9ecc769aa8c494252c11b00c2dca97`
- Thesis-relevantie: VLAM judgement prompt for deciding whether a document is a real cabinet response.
- Versies:
  - `PROMPT_VERSION`: `kabinetsreactie_vlam_response_judge_20260529_v4`

```python
ALLOWED_VERDICTS = frozenset(
    {
        "valid_response_match",
        "likely_response_match",
        "not_response_document",
        "response_to_other_advice",
        "uncertain",
    }
)
```
