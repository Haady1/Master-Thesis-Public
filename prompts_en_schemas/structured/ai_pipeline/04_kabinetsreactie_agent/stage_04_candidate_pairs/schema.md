# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_04_candidate_pairs.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `110b51ff6ada3e11a704f2bac7c9874906f67f48d9e95028191cb0cd98b85fa1`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `ReverseRecallBasis` op regel `45`
  - Bases: `BaseModel`
  - Velden: aanwezig: bool, verwijzing_ids: list[str], link_statussen: list[str]
- Klasse `CandidatePair` op regel `53`
  - Bases: `BaseModel`
  - Velden: candidate_pair_id: str, advies_element_id: str, advies_element_type: AdviceElementType, advies_element_label: str, segment_id: str, segment_volgnummer: int, pagina_hint: str, candidate_type: CandidateType, candidate_strength: CandidateStrength, review_prioriteit: ReviewPrioriteit, retrieval_signals: list[str], reverse_recall_basis: ReverseRecallBasis, relatie_kort: str, waarom_opnemen: str, risico_op_false_positive: str, bron_citaten: list[KabinetsreactieBronCitaat], twijfelpunten: list[str]
  - Validators/normalizers: normalize_legacy_values@76
- Klasse `AdviesElementZonderKandidaat` op regel `93`
  - Bases: `BaseModel`
  - Velden: advies_element_id: str, advies_element_type: AdviceElementType, advies_element_label: str, reden_geen_kandidaat: str, review_prioriteit: ReviewPrioriteit
- Klasse `CandidatePairRetrievalResultaat` op regel `103`
  - Bases: `BaseModel`
  - Velden: schema_version: str, document_id: str, advies_id: str, samenvatting: dict[str, Any], candidate_pairs: list[CandidatePair], advies_elementen_zonder_kandidaten: list[AdviesElementZonderKandidaat], audit_notities: list[str]
