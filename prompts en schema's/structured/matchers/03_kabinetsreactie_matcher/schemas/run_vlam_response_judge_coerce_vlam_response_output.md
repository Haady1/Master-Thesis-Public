# Run Vlam Response Judge Coerce Vlam Response Output

## `coerce_vlam_response_output`

- Bron: `matcher/kabinetsreactie/run_vlam_response_judge.py`
- Codebase: `matcher/kabinetsreactie`
- Type: `function`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `8179f130bf8028669a9b1953a98a94634a938efab86bf61455d19fbeddff11f1`
- Thesis-relevantie: VLAM judgement prompt for deciding whether a document is a real cabinet response.
- Versies:
  - `PROMPT_VERSION`: `kabinetsreactie_vlam_response_judge_20260529_v4`

```python
def coerce_vlam_response_output(raw: Any) -> dict[str, Any]:
    """Validate the VLAM JSON contract without accepting unknown enum values."""

    errors: list[str] = []
    if not isinstance(raw, dict):
        return {
            "parse_status": "parse_failure",
            "parse_errors": ["VLAM output is not a JSON object."],
            "raw_output": raw,
            "vlam_output": None,
        }

    verdict = raw.get("verdict")
    if verdict not in ALLOWED_VERDICTS:
        errors.append(
            "Invalid verdict; expected one of: "
            + ", ".join(sorted(ALLOWED_VERDICTS))
        )

    raw_signals = raw.get("signals")
    uses_legacy_signal_schema = _uses_legacy_signal_schema(raw_signals)
    confidence = _coerce_confidence(raw.get("confidence"), errors)
    is_response_document = _coerce_bool(
        raw.get("is_response_document"),
        "is_response_document",
        errors,
    )
    is_response_to_advice = _coerce_bool(
        raw.get("is_response_to_advice"),
        "is_response_to_advice",
        errors,
    )
    has_substantive_advice_handling = _coerce_bool(
        raw.get("has_substantive_advice_handling"),
        "has_substantive_advice_handling",
        errors,
        default=(
            _default_has_substantive_for_legacy_verdict(verdict)
            if uses_legacy_signal_schema
            else None
        ),
    )
    target_type = _coerce_target_type(
        raw.get("target_type"),
        errors,
        default=(
            _default_target_type_for_verdict(verdict)
            if uses_legacy_signal_schema
            else None
        ),
    )
    reason = str(raw.get("reason") or "").strip()
    if not reason:
        errors.append("Missing non-empty reason.")

    normalized_signals: dict[str, list[str]] = {}
    if not isinstance(raw_signals, dict):
        errors.append("Missing signals object.")
    else:
        for group_name in REQUIRED_SIGNAL_GROUPS:
            values = _signal_group_values(raw_signals, group_name)
            if not isinstance(values, list):
                errors.append(f"Missing or invalid signals.{group_name} list.")
                continue
            normalized_signals[group_name] = [
                str(value).strip() for value in values if str(value).strip()
            ]

    evidence_quotes = _coerce_evidence_quotes(raw, verdict, errors)
    other_target = _coerce_other_target(raw, verdict, errors)
    _validate_verdict_consistency(
        verdict=verdict,
        is_response_document=is_response_document,
        is_response_to_advice=is_response_to_advice,
        has_substantive_advice_handling=has_substantive_advice_handling,
        target_type=target_type,
        other_target=other_target,
        signals=normalized_signals,
        errors=errors,
    )
    if errors:
        return {
            "parse_status": "parse_failure",
            "parse_errors": errors,
            "raw_output": raw,
            "vlam_output": None,
        }
    return {
        "parse_status": "parsed",
        "parse_errors": [],
        "raw_output": raw,
        "vlam_output": {
            "verdict": verdict,
            "confidence": confidence,
            "is_response_document": is_response_document,
            "is_response_to_advice": is_response_to_advice,
            "has_substantive_advice_handling": has_substantive_advice_handling,
            "target_type": target_type,
            "other_target": other_target,
            "reason": reason[:1000],
            "signals": normalized_signals,
            "evidence_quotes": evidence_quotes,
        },
    }
```
