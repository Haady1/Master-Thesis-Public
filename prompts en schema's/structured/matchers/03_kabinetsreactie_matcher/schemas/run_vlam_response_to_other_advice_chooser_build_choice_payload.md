# Run Vlam Response To Other Advice Chooser Build Choice Payload

## `build_choice_payload`

- Bron: `matcher/kabinetsreactie/run_vlam_response_to_other_advice_chooser.py`
- Codebase: `matcher/kabinetsreactie`
- Type: `function`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `d39cb7aafbff72325306bae481d2a2ab4bcee586d1d8126f1e24435098a35624`
- Thesis-relevantie: VLAM target chooser prompt for response-to-other-advice cases.
- Versies:
  - `PROMPT_VERSION`: `kabinetsreactie_vlam_target_chooser_20260526_v1`

```python
def build_choice_payload(
    *,
    run_id: str,
    case_matches: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    if not case_matches:
        raise ValueError("Cannot build chooser payload without candidate matches.")
    first_match = case_matches[0]
    reaction_id = _clean_text(first_match.get("matched_reactie_document_id"))
    other_targets = _unique_other_targets(case_matches)
    options = [
        _candidate_option(index=index, match=match)
        for index, match in enumerate(case_matches, start=1)
    ]
    return {
        "prompt_version": PROMPT_VERSION,
        "task": {
            "review_scope": "choose_best_advice_from_relink_shortlist",
            "read_only": True,
            "no_database_writes": True,
            "no_external_knowledge": True,
            "date_fields_are_weak_tie_breakers": True,
        },
        "expected_output_schema": {
            "choice": sorted(ALLOWED_CHOICES),
            "selected_advies_document_id": "string or null",
            "runner_up_advies_document_ids": "list of strings",
            "confidence": "number between 0 and 1",
            "reason": "short Dutch evidence-based explanation",
            "evidence_quotes": "list of short strings",
            "mismatch_warnings": "list of short strings",
        },
        "metadata": {
            "source_run_id": run_id,
            "matched_reactie_document_id": reaction_id,
            "candidate_count": len(options),
            "candidate_title": first_match.get("candidate_title"),
            "candidate_document_type": first_match.get("candidate_document_type"),
            "candidate_date_published": first_match.get("candidate_date_published"),
            "candidate_link": first_match.get("candidate_link"),
        },
        "prior_vlam_other_targets": other_targets,
        "reaction_evidence": {
            "bewijs_citaten": _dedupe_texts(
                quote
                for match in case_matches
                for quote in _as_list(match.get("bewijs_citaten"))
            )[:8],
            "match_signalen": _dedupe_texts(
                signal
                for match in case_matches
                for signal in _as_list(match.get("match_signalen"))
            )[:20],
        },
        "candidate_options": options,
    }
```
