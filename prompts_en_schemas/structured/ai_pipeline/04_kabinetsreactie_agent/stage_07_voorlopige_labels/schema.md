# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_07_voorlopige_labels.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `3b24fc40d0e47e17bb9f4f71b35e48a95ae402d2843e4de927122071b0c51cc3`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `VoorlopigVerwerkingsitem` op regel `44`
  - Bases: `BaseModel`
  - Velden: voorlopig_label_id: str, advies_element_id: str, advies_element_type: str, advies_element_label: str, candidate_pair_ids: list[str], semantic_match_ids: list[str], positie_opvolging_ids: list[str], segment_ids: list[str], voorlopig_verwerkingslabel: Verwerkingslabel, inhoudelijke_match_score: float | None, score_uitleg: str, regelpad: list[str], bewijsbasis_kort: str, review_prioriteit: ReviewPrioriteit
- Klasse `VoorlopigeLabelsResultaat` op regel `63`
  - Bases: `BaseModel`
  - Velden: schema_version: str, document_id: str, advies_id: str, voorlopige_verwerkingsitems: list[VoorlopigVerwerkingsitem], audit_notities: list[str]
