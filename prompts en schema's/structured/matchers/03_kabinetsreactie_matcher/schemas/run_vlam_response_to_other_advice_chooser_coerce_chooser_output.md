# Run Vlam Response To Other Advice Chooser Coerce Chooser Output

## `coerce_chooser_output`

- Bron: `matcher/kabinetsreactie/run_vlam_response_to_other_advice_chooser.py`
- Codebase: `matcher/kabinetsreactie`
- Type: `function`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `6b4f3728f4111043827887f30fb441922648ba36081106047b1cbbe496e86084`
- Thesis-relevantie: VLAM target chooser prompt for response-to-other-advice cases.
- Versies:
  - `PROMPT_VERSION`: `kabinetsreactie_vlam_target_chooser_20260526_v1`

```python
def coerce_chooser_output(
    raw: Mapping[str, Any],
    candidate_options: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    valid_ids = {
        _clean_text(option.get("advies_document_id"))
        for option in candidate_options
        if _clean_text(option.get("advies_document_id"))
    }
    choice = _clean_text(raw.get("choice"))
    if choice not in ALLOWED_CHOICES:
        errors.append(f"Invalid choice: {choice!r}.")
        choice = "none_of_the_above"

    selected = _clean_text(raw.get("selected_advies_document_id")) or None
    if choice == "best_match":
        if not selected:
            errors.append("best_match requires selected_advies_document_id.")
        elif selected not in valid_ids:
            errors.append(f"selected_advies_document_id is not in options: {selected}.")
    elif selected and selected not in valid_ids:
        errors.append(f"selected_advies_document_id is not in options: {selected}.")

    runner_ups = [
        value
        for value in (_clean_text(item) for item in _as_list(raw.get("runner_up_advies_document_ids")))
        if value and value in valid_ids and value != selected
    ][:5]
    confidence = max(0.0, min(_float_or_zero(raw.get("confidence")), 1.0))
    return (
        {
            "choice": choice,
            "selected_advies_document_id": selected,
            "runner_up_advies_document_ids": runner_ups,
            "confidence": confidence,
            "reason": _clean_text(raw.get("reason"))[:1200],
            "evidence_quotes": _coerce_string_list(raw.get("evidence_quotes"), limit=8),
            "mismatch_warnings": _coerce_string_list(raw.get("mismatch_warnings"), limit=8),
        },
        errors,
    )
```
