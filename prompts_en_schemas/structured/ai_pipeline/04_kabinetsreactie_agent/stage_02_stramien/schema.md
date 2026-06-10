# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_02_stramien.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `e8cb89b2f2da9c66734165a29f8c39815c99e22926a601318421449ab9ff457a`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `SegmentStramienfunctie` op regel `67`
  - Bases: `BaseModel`
  - Velden: segment_id: str, primaire_stramienfunctie: Stramienfunctie, secundaire_stramienfuncties: list[Stramienfunctie], stramienfunctie_toelichting: str
- Klasse `StramienComponent` op regel `76`
  - Bases: `BaseModel`
  - Velden: component_type: StramienComponentType, segment_ids: list[str], toelichting: str, bron_citaten: list[KabinetsreactieBronCitaat], component_zekerheid: Zekerheid
- Klasse `StramienAnalyseResultaat` op regel `86`
  - Bases: `BaseModel`
  - Velden: schema_version: str, document_id: str, advies_id: str | None, samenvatting: dict[str, Any], segment_stramienfuncties: list[SegmentStramienfunctie], stramien_componenten: list[StramienComponent], documentpatroon: dict[str, Any], downstream_signalen: dict[str, Any], audit_notities: list[str]
