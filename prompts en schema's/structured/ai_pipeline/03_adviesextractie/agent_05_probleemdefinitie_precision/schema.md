# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/probleem_definitie_precision/schema.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `d7e0d32778c88e5baecad4a755f3c5a338293a6bae45f8ad5a5ef031b261786b`
- Thesis-relevantie: Pydantic output schemas paired with the advice-report extraction prompts.

- Klasse `ProbleemDefinitiePrecisionItem` op regel `396`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Uitgewerkte probleemdefinitie voor een eerder gevonden recall-kandidaat.  Deze fase vult de verbatim tekstvelden in en past de functionele drempel toe: een item is alleen geldig als zowel `normatieve_claim_tekst` als `causaliteit_tekst` daadwerkelijk uit de collegetekst zijn af te leiden. Items die de drempel niet halen worden in deze batch gemarkeerd met `is_valid=False` en krijgen een korte `drop_reason`.
  - Velden: candidate_id: int, candidate_uid: str, candidate_key: str, source_fingerprint: Optional[str], canonical_candidate_uid: Optional[str], primary_occurrence_id: Optional[str], source_grounding_status: Optional[str], precision_decision: Optional[PrecisionDecision], validity_confidence: Optional[float], invalid_code: Optional[InvalidCode], duplicate_of_candidate_uid: Optional[str], reconciliation_group_hint: Optional[str], causal_or_institutional_mechanism_type: CausalOrInstitutionalMechanismType, problem_definition_test: dict, quality_flags: List[str], original_recall_evidence: List[dict], precision_primary_evidence: Optional[dict], precision_supporting_evidence: List[dict], added_evidence_reason: Optional[str], is_valid: bool, normativiteit_status: NormativiteitStatus, stem_status: StemStatus, drop_reason: Optional[str], drop_code: Optional[Literal['DUPLICATE', 'EXTERNAL_VOICE', 'EVIDENCE_ONLY', 'CONTEXT_ONLY', 'SOLUTION_ONLY', 'MISSING_CAUSALITY', 'MISSING_NORMATIVITY', 'TRACEABILITY_FAILURE', 'RECOMMENDATION_CONTAMINATION', 'INVALID_IN_PRECISION', 'MISSING_ADVIES_ID', 'TOO_ABSTRACT_FOR_MATCHING', 'OTHER']], box_ids: List[Union[int, str]], primaire_box_id: Optional[Union[int, str]], niveau: ProbleemDefinitieNiveau, label_tekst: Optional[str], label_box_id: Optional[Union[int, str]], slachtoffers_tekst: Optional[str], slachtoffers_box_id: Optional[Union[int, str]], causaliteit_tekst: Optional[str], causaliteit_box_id: Optional[Union[int, str]], normatieve_claim_tekst: Optional[str], normatieve_claim_box_id: Optional[Union[int, str]], urgentie_tekst: Optional[str], urgentie_box_id: Optional[Union[int, str]]
  - Validators/normalizers: _normalize_niveau@625, _normalize_normativiteit_status@643, _normalize_mechanism_type@655, _normalize_stem_status@666, _normalize_drop_code@673, _include_referenced_box_ids@678, _validate_precision_contract@695
- Klasse `ProbleemDefinitiePrecisionBatchResult` op regel `750`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Batch-output van de probleemdefinitie precision-agent.
  - Velden: analyse_denkstappen: str, items: List[ProbleemDefinitiePrecisionItem]
  - Validators/normalizers: _reject_copied_prompt_example@846, _validate_unique_returned_candidates@854
