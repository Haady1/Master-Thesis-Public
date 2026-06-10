# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_06b_context.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `5d7ed8e40e95e516f10126517fabcb2e7e2aa218548ac809c94f9b3a13604068`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `ContextItem06b` op regel `39`
  - Bases: `BaseModel`
  - Docstring: Single context item from stage 06b, keyed by positie_opvolging_id from 06a.
  - Velden: positie_opvolging_id: str, actie_type: list[ActieType], instrumenten: list[str], verantwoordelijke_actoren: list[str], uitvoerende_actoren: list[str], timing: TimingType, timing_toelichting: str, motiveringen: list[MotiveringType], transformaties: list[TransformatieType]
- Klasse `ContextResultaat06b` op regel `58`
  - Bases: `BaseModel`
  - Docstring: Full result object from stage 06b.
  - Velden: schema_version: str, document_id: str, advies_id: str, context_items: list[ContextItem06b], audit_notities: list[str]
