# Run Vlam Response To Other Advice Chooser Schema

## `__classes__`

- Bron: `matcher/kabinetsreactie/run_vlam_response_to_other_advice_chooser.py`
- Codebase: `matcher/kabinetsreactie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `8678355bc831018ae97db1de79d2e13dc78c58d4c95e97f78960059e912c5754`
- Thesis-relevantie: VLAM target chooser prompt for response-to-other-advice cases.
- Versies:
  - `PROMPT_VERSION`: `kabinetsreactie_vlam_target_chooser_20260526_v1`

- Klasse `VlamTargetChooserConfig` op regel `77`
  - Velden: provider: str, model: str | None, base_url: str | None, api_key_env: str | None, timeout_seconds: int
- Klasse `ChooserRunConfig` op regel `86`
  - Velden: source_matches_json: Path, run_id: str, output_dir: Path, confidence_threshold: float, workers: int, limit: int | None, dry_run: bool, match_status: str
- Klasse `VlamTargetChooser` op regel `97`
  - Docstring: Small OpenAI-compatible JSON client for target-choice review.
