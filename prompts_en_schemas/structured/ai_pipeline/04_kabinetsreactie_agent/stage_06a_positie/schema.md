# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_06a_positie.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `47b8edd57f3503c3630bed12686bbdf5383a600d37507de47cb4a957e64569c7`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `PositieItem06a` op regel `39`
  - Bases: `BaseModel`
  - Docstring: Single assessed match item from stage 06a (position assessment).
  - Velden: positie_opvolging_id: str, semantic_match_id: str, candidate_pair_id: str, advies_element_id: str, advies_element_type: str, advies_element_label: str, segment_id: str, segment_volgnummer: int, pagina_hint: str, semantische_match_basis: str, nli_relatie: str, kabinetspositie: KabinetspositieType, positie_toelichting: str, beleidsmatige_opvolging: BeleidsmatigeOpvolgingType, opvolging_toelichting: str, positie_signalen: list[PositieSignaalType], bron_citaten_kabinetsreactie: list[KabinetsreactieBronCitaat], zekerheid: ZekerheidType, audit_flags: list[str], twijfelpunten: list[str]
- Klasse `NietBeoordeeld06a` op regel `66`
  - Bases: `BaseModel`
  - Docstring: Semantic match that was not assessed in stage 06a.
  - Velden: semantic_match_id: str, candidate_pair_id: str, advies_element_id: str, segment_id: str, reden_niet_beoordeeld: str
- Klasse `PositieResultaat06a` op regel `78`
  - Bases: `BaseModel`
  - Docstring: Full result object from stage 06a.
  - Velden: schema_version: str, document_id: str, advies_id: str, samenvatting: dict, positie_items: list[PositieItem06a], niet_beoordeeld: list[NietBeoordeeld06a], audit_notities: list[str]
