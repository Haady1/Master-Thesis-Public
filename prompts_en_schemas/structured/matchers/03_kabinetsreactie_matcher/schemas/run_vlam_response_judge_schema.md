# Run Vlam Response Judge Schema

## `__classes__`

- Bron: `matcher/kabinetsreactie/run_vlam_response_judge.py`
- Codebase: `matcher/kabinetsreactie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `1fe5836833a94870d84c310d71461f4023a3830c6f0d340110fdbb115c9078c1`
- Thesis-relevantie: VLAM judgement prompt for deciding whether a document is a real cabinet response.
- Versies:
  - `PROMPT_VERSION`: `kabinetsreactie_vlam_response_judge_20260529_v4`

- Klasse `VlamResponseJudgeConfig` op regel `354`
  - Velden: provider: str, model: str | None, base_url: str | None, api_key_env: str | None, timeout_seconds: int
- Klasse `ReviewCase` op regel `363`
  - Velden: match: dict[str, Any], advice_text: str | None, advice_source_char_length: int | None, reaction_document: dict[str, Any] | None, hydration_error_status: str | None, hydration_error: str | None
- Klasse `VlamResponseJudge` op regel `372`
  - Docstring: Small OpenAI-compatible JSON client for response-match review.
