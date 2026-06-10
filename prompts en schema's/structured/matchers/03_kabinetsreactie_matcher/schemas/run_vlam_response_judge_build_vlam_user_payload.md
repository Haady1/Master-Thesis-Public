# Run Vlam Response Judge Build Vlam User Payload

## `build_vlam_user_payload`

- Bron: `matcher/kabinetsreactie/run_vlam_response_judge.py`
- Codebase: `matcher/kabinetsreactie`
- Type: `function`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `8fa345f430e4f04a0d5556548854673bd2e18d026342827c87aef63ab0978117`
- Thesis-relevantie: VLAM judgement prompt for deciding whether a document is a real cabinet response.
- Versies:
  - `PROMPT_VERSION`: `kabinetsreactie_vlam_response_judge_20260529_v4`

```python
def build_vlam_user_payload(
    *,
    run_id: str,
    match: dict[str, Any],
    advice_text: str,
    reaction_document: dict[str, Any],
    advice_source_char_length: int | None,
    advice_char_limit: int,
) -> dict[str, Any]:
    """Build the ordered JSON payload sent as the user message."""

    advice_body = str(advice_text or "")[: max(0, int(advice_char_limit))]
    reaction_text = str(reaction_document.get("content_text") or "")
    input_text_lengths = {
        "advice_body_chars": len(advice_body),
        "advice_source_chars": (
            int(advice_source_char_length)
            if advice_source_char_length is not None
            else len(str(advice_text or ""))
        ),
        "reaction_text_chars": len(reaction_text),
    }
    return {
        "prompt_version": PROMPT_VERSION,
        "task": {
            "review_scope": "single_deterministic_strong_match",
            "read_only": True,
            "no_database_writes": True,
            "no_external_knowledge": True,
        },
        "expected_output_schema": {
            "verdict": sorted(ALLOWED_VERDICTS),
            "confidence": "number between 0 and 1",
            "is_response_document": "boolean",
            "is_response_to_advice": "boolean",
            "has_substantive_advice_handling": "boolean",
            "target_type": sorted(ALLOWED_TARGET_TYPES),
            "other_target": {
                "title": "string or null",
                "identifier": "string or null",
                "organisation": "string or null",
                "date": "string or null",
                "evidence_quote": "string or null",
            },
            "reason": "short Dutch evidence-based explanation",
            "signals": {name: "list of strings" for name in REQUIRED_SIGNAL_GROUPS},
            "evidence_quotes": [{"quote": "string", "shows": "string"}],
        },
        "metadata": {
            "source_run_id": run_id,
            "advies_document_id": match.get("advies_document_id"),
            "matched_reactie_document_id": match.get("matched_reactie_document_id"),
            "reaction_document": {
                "id": reaction_document.get("id"),
                "title": reaction_document.get("title"),
                "document_type": reaction_document.get("document_type"),
                "type_group": reaction_document.get("type_group"),
                "date_published": reaction_document.get("date_published"),
                "preferred_url": reaction_document.get("preferred_url"),
            },
            "input_text_lengths": input_text_lengths,
        },
        "deterministic_signals": {
            "match_status": match.get("match_status"),
            "bronlaag": match.get("bronlaag"),
            "confidence_score": match.get("confidence_score"),
            "review_nodig": match.get("review_nodig"),
            "match_signalen": match.get("match_signalen") or [],
            "tegen_signalen": match.get("tegen_signalen") or [],
        },
        "candidate_evidence": {
            "bewijs_citaten": match.get("bewijs_citaten") or [],
            "source_refs": match.get("source_refs") or [],
            "korte_toelichting": match.get("korte_toelichting"),
        },
        "document_texts": {
            "adviesbody_first_chars": advice_body,
            "reactietekst_full": reaction_text,
        },
    }
```
