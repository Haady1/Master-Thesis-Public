# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/probleem_definitie_recall/schema.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `23598f30248d414a6cdd21de45fe35c48b547314b1d04253f10b176b4e69f5b8`
- Thesis-relevantie: Pydantic output schemas paired with the advice-report extraction prompts.

- Klasse `ProbleemRecallCandidateAudit` op regel `135`
  - Bases: `BaseModel`
  - Docstring: Audit trail for post-recall filtering and deduplicatie.
  - Velden: candidate_id: int, status: Literal['active', 'dropped_external_voice', 'dropped_duplicate'], duplicate_of: Optional[int], dedup_cluster_id: Optional[int], stem_verificatie: StemVerificatie, selection_reason: Optional[str], canonical: bool
- Klasse `EvidenceSpanSegment` op regel `167`
  - Bases: `BaseModel`
  - Docstring: Model-supplied or runtime-validated exact source segment.
  - Velden: page_number: Optional[int], box_id: Union[int, str], start_offset: Optional[int], end_offset: Optional[int], exact_text: str
- Klasse `ProbleemEvidenceOccurrence` op regel `177`
  - Bases: `BaseModel`
  - Docstring: Evidence-first recall occurrence supplied by the model or runtime.
  - Velden: occurrence_id: Optional[str], candidate_id: Optional[int], source_grounding_status: SourceGroundingStatus, span_segments: List[EvidenceSpanSegment], exact_quote: str, normalized_quote: Optional[str], source_fingerprint: Optional[str], page_range: Optional[str], section_title: Optional[str], source_section_role: SourceSectionRole, stem_verificatie: StemVerificatie, has_normatieve_claim_hint: bool, has_causaliteit_hint: bool, diagnostic_span_only: bool, local_reason: Optional[str], quality_flags: List[str]
- Klasse `ProbleemDefinitieCandidate` op regel `198`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Compacte kandidaat-probleemdefinitie.  Recall blijft bewust klein: box_ids, label, confidence en bron/stemsignalen.
  - Velden: candidate_id: int, candidate_uid: Optional[str], candidate_key: Optional[str], source_fingerprint: Optional[str], source_grounding_status: SourceGroundingStatus, primary_occurrence_id: Optional[str], evidence_occurrence_ids: List[str], source_fingerprints: List[str], canonical_candidate_uid: Optional[str], supporting_occurrence_ids: List[str], all_source_fingerprints: List[str], page_range: Optional[str], box_ids: List[Union[int, str]], short_label: Optional[str], confidence: float, confidence_label: ConfidenceLabel, niveau: ProbleemDefinitieNiveau, bron_hint: Literal['adviescollege', 'externe_bron', 'consultatie_input', 'onbekend'], stem_verificatie: StemVerificatie, source_section_role: SourceSectionRole, has_normatieve_claim_hint: bool, has_causaliteit_hint: bool
  - Validators/normalizers: _coerce_confidence@337, _normalize_confidence_label@350, _normalize_niveau@367, _normalize_stem_verificatie@372, _sync_derived_fields@388
- Klasse `ProbleemDefinitieCandidateLite` op regel `402`
  - Bases: `BaseModel`
  - Docstring: Compacte recall-candidate met box_ids.  Het model kiest alleen de bronboxen; runtime hydrateert die box_ids naar exacte boxtekst, box_level_span occurrences en source_fingerprints.
  - Velden: candidate_id: int, candidate_uid: Optional[str], candidate_key: Optional[str], source_fingerprint: Optional[str], source_grounding_status: SourceGroundingStatus, primary_occurrence_id: Optional[str], evidence_occurrence_ids: List[str], source_fingerprints: List[str], canonical_candidate_uid: Optional[str], supporting_occurrence_ids: List[str], all_source_fingerprints: List[str], short_label: str, page_range: str, box_ids: List[Union[int, str]], confidence: float, niveau: ProbleemDefinitieNiveau, bron_hint: Literal['adviescollege', 'externe_bron', 'consultatie_input', 'onbekend'], stem_verificatie: StemVerificatie, source_section_role: SourceSectionRole, has_normatieve_claim_hint: bool, has_causaliteit_hint: bool
  - Validators/normalizers: _normalize_niveau@450
- Klasse `ProbleemDefinitieRecallResult` op regel `454`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Legacy/full recall-output; live recall gebruikt ProbleemDefinitieRecallLiteResult.
  - Velden: analyse_denkstappen: str, candidates: List[ProbleemDefinitieCandidate], evidence_occurrences: List[ProbleemEvidenceOccurrence], canonical_candidates: List[dict], candidate_audit: List[ProbleemRecallCandidateAudit], total_occurrences: int, total_candidates: int, total_found: int
- Klasse `ProbleemDefinitieRecallLiteResult` op regel `544`
  - Bases: `BaseModel`
  - Docstring: Compact recall-resultaat met box_ids voor runtime grounding.  Het model vult alleen analyse_denkstappen, candidates en total_found. candidate_audit en schema_recovery zijn runtime-/schema-managed auditvelden.
  - Velden: analyse_denkstappen: str, candidates: List[ProbleemDefinitieCandidateLite], candidate_audit: List[ProbleemRecallCandidateAudit], total_found: int, schema_recovery: List[dict]
  - Validators/normalizers: _normalize_lite_result@687
