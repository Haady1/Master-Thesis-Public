# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_01_segmentatie.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `91df649dcc79a31714e5d9f9cc94739119439a8bbb3724b4f557db1040bfbfb5`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `SegmentActor` op regel `107`
  - Bases: `BaseModel`
  - Velden: actor: str, actor_type: ActorType, rol_in_segment: str
- Klasse `KabinetsreactieSegment` op regel `115`
  - Bases: `BaseModel`
  - Velden: segment_id: str, volgnummer: int, pagina_hint: str, primaire_functie: PrimaireFunctie, secundaire_functies: list[PrimaireFunctie], beleidsthema: str, kernzin: str, tekst_kort: str, kabinetspositie: Kabinetspositie | None, actie_type: list[ActieType], actoren: list[SegmentActor], instrumenten: list[str], timing: Timing, timing_toelichting: str, motivering_kort: str, bron_citaten: list[KabinetsreactieBronCitaat], segmentatiezekerheid: Zekerheid, twijfelpunten: list[str]
  - Validators/normalizers: normalize_legacy_values@139
- Klasse `SegmentatieResultaat` op regel `174`
  - Bases: `BaseModel`
  - Velden: schema_version: str, document_id: str, segmentatie_samenvatting: dict[str, Any], segmenten: list[KabinetsreactieSegment], documentbrede_signalen: dict[str, Any], case_pair_sanity: dict[str, Any], audit_notities: list[str]
