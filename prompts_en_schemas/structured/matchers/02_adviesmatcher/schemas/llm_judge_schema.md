# Llm Judge Schema

## `__classes__`

- Bron: `matcher/advies/llm_judge.py`
- Codebase: `matcher/advies`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `e666832d8ba5c391c3fa5b311f38f559b9e40611912cf8471062eec833db66e8`
- Thesis-relevantie: LLM labelling prompt for deciding whether a candidate is a final advice document.
- Versies:
  - `LLM_PROMPT_VERSION`: `advies_discovery_llm_label_prompt_20260529_v6`

- Klasse `LlmLabelerConfig` op regel `260`
  - Velden: provider: str, model: str | None, base_url: str | None, api_key_env: str | None, timeout_seconds: int, max_candidates_per_college: int, workers: int, unattended_output_root: Path | None, unattended_enabled: bool, unattended_warmup_workers: str, unattended_circuit_sleep_seconds: int
- Klasse `LlmAdviceLabeler` op regel `274`
