# Schema Stage 05 Semantische Match Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_05_semantische_match.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `1612af1c8f762106b56f1a8e11ad4e156a1707531e9dcdb4a70d9368e230eaee`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `SemantischeMatch` op regel `36`
  - Bases: `BaseModel`
  - Velden: semantic_match_id: str, candidate_pair_id: str, advies_element_id: str, advies_element_type: AdviceElementType, advies_element_label: str, segment_id: str, segment_volgnummer: int, pagina_hint: str, semantische_match_basis: SemantischeMatchBasis, nli_relatie: NliRelatie, nli_toelichting: str, aanbeveling_componenten: dict[str, Any] | None, probleemdefinitie_componenten: dict[str, Any] | None, beleidslogica_componenten: dict[str, Any] | None, belangrijkste_overlap: list[str], belangrijkste_verschillen: list[str], contradictie_signalen: list[str], doorgaan_naar_positie_agent: bool, reden_doorzetten_of_stoppen: str, bron_citaten_kabinetsreactie: list[KabinetsreactieBronCitaat], zekerheid: Zekerheid, twijfelpunten: list[str]
- Klasse `GestoptCandidatePair` op regel `63`
  - Bases: `BaseModel`
  - Velden: candidate_pair_id: str, advies_element_id: str, segment_id: str, reden_stoppen: str, semantische_match_basis: SemantischeMatchBasis
- Klasse `SemantischeMatchResultaat` op regel `73`
  - Bases: `BaseModel`
  - Velden: schema_version: str, document_id: str, advies_id: str, samenvatting: dict[str, Any], semantische_matches: list[SemantischeMatch], gestopte_candidate_pairs: list[GestoptCandidatePair], audit_notities: list[str]
