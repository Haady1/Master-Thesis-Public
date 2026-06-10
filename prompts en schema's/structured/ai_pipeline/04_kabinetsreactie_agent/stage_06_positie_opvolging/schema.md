# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_06_positie_opvolging.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `92c02ab6414d8f27ec407b4a435d2c87dbcbd8164879dac0b4e7e3a9a4dcdb6f`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `PositieOpvolgingItem` op regel `45`
  - Bases: `BaseModel`
  - Velden: positie_opvolging_id: str, semantic_match_id: str, candidate_pair_id: str, advies_element_id: str, advies_element_type: AdviceElementType, advies_element_label: str, segment_id: str, segment_volgnummer: int, pagina_hint: str, semantische_match_basis: SemantischeMatchBasis, nli_relatie: NliRelatie, kabinetspositie: Kabinetspositie, positie_toelichting: str, beleidsmatige_opvolging: BeleidsmatigeOpvolging, opvolging_toelichting: str, actie_type: list[ActieType], instrumenten: list[str], verantwoordelijke_actoren: list[str], uitvoerende_actoren: list[str], timing: Timing, timing_toelichting: str, motiveringen: list[MotiveringType], transformaties: list[TransformatieType], positie_signalen: list[str], bron_citaten_kabinetsreactie: list[KabinetsreactieBronCitaat], zekerheid: Zekerheid, audit_flags: list[str], twijfelpunten: list[str]
  - Validators/normalizers: normalize_legacy_values@79
- Klasse `NietBeoordeeldeSemantischeMatch` op regel `94`
  - Bases: `BaseModel`
  - Velden: semantic_match_id: str, candidate_pair_id: str, advies_element_id: str, segment_id: str, reden_niet_beoordeeld: str
- Klasse `KabinetspositieEnOpvolgingResultaat` op regel `104`
  - Bases: `BaseModel`
  - Velden: schema_version: str, document_id: str, advies_id: str, samenvatting: dict[str, Any], positie_opvolging_items: list[PositieOpvolgingItem], niet_beoordeelde_semantische_matches: list[NietBeoordeeldeSemantischeMatch], audit_notities: list[str]
