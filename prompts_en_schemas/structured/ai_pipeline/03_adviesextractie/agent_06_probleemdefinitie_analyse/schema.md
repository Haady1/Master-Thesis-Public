# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/probleem_definitie_analyse/schema.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `5fb318e8d7e47ed4767dc475935c0cb74f38d018cb2b14134b1a6edfbad6fa13`
- Thesis-relevantie: Pydantic output schemas paired with the advice-report extraction prompts.

- Klasse `ProbleemDedupCluster` op regel `41`
  - Bases: `BaseModel`
  - Docstring: Audit van semantische deduplicatie-clusters.
  - Velden: cluster_id: int, canonical_candidate_id: int, canonical_candidate_uid: Optional[str], canonical_candidate_key: Optional[str], member_candidate_ids: List[int], member_candidate_uids: List[str], member_candidate_keys: List[str], final_id: Optional[str], gedeelde_kern: str
  - Validators/normalizers: _validate_gedeelde_kern@71, _validate_cluster_contract@80
- Klasse `ProbleemAnalyseAudit` op regel `88`
  - Bases: `BaseModel`
  - Docstring: Audit per ingekomen precision-item: welk lot is het beschoren?
  - Velden: candidate_id: int, candidate_uid: Optional[str], candidate_key: Optional[str], status: Literal['accepted_kern', 'accepted_deel', 'merged_into_canonical', 'dropped_invalid_in_precision', 'dropped_in_analyse', 'candidate_reopen_requested'], final_id: Optional[str], drop_reason: Optional[str], drop_code: Optional[Literal['DUPLICATE', 'EXTERNAL_VOICE', 'EVIDENCE_ONLY', 'CONTEXT_ONLY', 'SOLUTION_ONLY', 'MISSING_CAUSALITY', 'MISSING_NORMATIVITY', 'TRACEABILITY_FAILURE', 'RECOMMENDATION_CONTAMINATION', 'INVALID_IN_PRECISION', 'MISSING_ADVIES_ID', 'OTHER']], audit_note: str
  - Validators/normalizers: _validate_audit_note@145, _normalize_drop_code@152, _validate_audit_contract@166
- Klasse `DominanteUrgentieProbleemRapport` op regel `188`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Dominant urgentietype van het centrale probleempakket.
  - Velden: urgentie_type: Literal['acuut', 'structureel', 'toekomstig', 'onbekend'], redenering_dominante_urgentie: str, dominante_urgentie_box_ids: List[Union[int, str]]
- Klasse `DominanteCausaliteitsframingRapport` op regel `208`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Dominante causaliteitsframing van het centrale probleempakket.
  - Velden: causaliteitstype: Literal['mechanisch', 'accidenteel', 'intentioneel', 'inadvertent', 'onbekend'], redenering_dominante_causaliteitsframing: str, dominante_causaliteitsframing_box_ids: List[Union[int, str]]
- Klasse `DominanteProbleemframingRapport` op regel `234`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Dominante probleemframing van het centrale probleempakket.
  - Velden: framing_type: Literal['instrumenteel', 'normatief', 'cognitief', 'onbekend'], redenering_dominante_probleemframing: str, dominante_probleemframing_box_ids: List[Union[int, str]]
- Klasse `ProbleemDefinitieAnalyseResult` op regel `254`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Finale output van de probleemdefinitie-pipeline.  Bevat primair canonical item-level probleemdefinities, plus secundaire rapportniveau-synthese en audittrails.
  - Velden: analyse_denkstappen: str, hoofdprobleem_synthese: Optional[HoofdProbleemSynthese], hoofdprobleem_box_ids: List[Union[int, str]], dominante_urgentie: Optional[DominanteUrgentieProbleemRapport], dominante_causaliteitsframing: Optional[DominanteCausaliteitsframingRapport], dominante_probleemframing: Optional[DominanteProbleemframingRapport], probleemdefinities: List[Probleemdefinitie], dedup_clusters: List[ProbleemDedupCluster], candidate_audit: List[ProbleemAnalyseAudit], candidate_lifecycle: List[dict], precision_batch_status: List[dict], pipeline_status: Literal['SUCCESS', 'SUCCESS_WITH_WARNINGS', 'PARTIAL_SUCCESS', 'FAILED', 'UNKNOWN'], traceability_warnings: List[str]
  - Validators/normalizers: _normalize_final_candidate_audit_entries@580, _accept_root_array@644
