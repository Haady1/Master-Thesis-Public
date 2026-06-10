# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/aanbeveling_recall/schema.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `05c4832c88b939fbf55bd681633bf0fc0ef9d61f8a9ca6bb307a2c48da84ffc6`
- Thesis-relevantie: Pydantic output schemas paired with the advice-report extraction prompts.

- Klasse `RecallCandidateAudit` op regel `65`
  - Bases: `BaseModel`
  - Docstring: Audit trail for post-recall filtering and deduplicatie.
  - Velden: candidate_id: int, status: Literal['active', 'dropped_external_voice', 'dropped_duplicate'], duplicate_of: Optional[int], dedup_cluster_id: Optional[int], stem_verificatie: StemVerificatie, selection_reason: Optional[str], canonical: bool
- Klasse `AanbevelingCandidate` op regel `97`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Grounded kandidaat-aanbeveling voor recall.  Recall blijft bewust compact, maar gebruikt altijd grounded box_ids voor traceerbaarheid.
  - Velden: candidate_id: int, box_ids: List[Union[int, str]], short_actor_label: Optional[str], confidence: float, confidence_label: ConfidenceLabel, niveau: AanbevelingNiveau, bron_hint: Literal['adviescollege', 'externe_bron', 'consultatie_input', 'onbekend'], stem_verificatie: StemVerificatie, document_nummer: Optional[str], bronsectie_type: BronsectieType, section_heading: Optional[str], parent_candidate_id: Optional[int], parent_document_nummer: Optional[str]
  - Validators/normalizers: _coerce_confidence@204, _normalize_confidence_label@217, _normalize_stem_verificatie@234, _normalize_bronsectie_type@251, _sync_derived_fields@279
- Klasse `AanbevelingRecallResult` op regel `303`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Recall-output voor aanbevelingen.
  - Velden: analyse_denkstappen: str, candidates: List[AanbevelingCandidate], candidate_audit: List[RecallCandidateAudit], total_found: int
