# Canonical Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/schemas/canonical_schemas.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `58c7ddfa436a7a409233d009a8b59f550304d673937d21f92d9ffb92526834a2`
- Thesis-relevantie: Canonical recommendation, problem-definition, and policy-logic overlay schemas.

- Klasse `CanonicalEvidenceOccurrence` op regel `96`
  - Bases: `BaseModel`
  - Docstring: One traceable source occurrence supporting a canonical item.
  - Velden: bron_item_id: Optional[str], bron_box_ids: List[Union[int, str]], evidence_rol: Literal['primaire_tekst', 'samenvatting', 'context', 'beleidslogica', 'onduidelijk'], pagina_hint: Optional[Union[int, str]], korte_citaat_of_parafrase: Optional[str]
  - Validators/normalizers: _box_ids_must_not_be_empty@119
- Klasse `CanonicalAanbeveling` op regel `125`
  - Bases: `BaseModel`
  - Docstring: Canonical recommendation derived from one or more source recommendations.
  - Velden: canonical_aanbeveling_id: str, bron_aanbeveling_ids: List[str], beschrijving: str, granularity: CanonicalRecommendationGranularity, parent_canonical_id: Optional[str], granularity_status: CanonicalGranularityStatus, merge_redenering: str, bron_box_ids: List[Union[int, str]], evidence_occurrences: List[CanonicalEvidenceOccurrence], officiele_aanbeveling_cluster_id: Optional[str], officiele_aanbeveling_cluster_ids: List[str], officiele_aanbeveling_nummer: Optional[str], officiele_aanbeveling_parent_id: Optional[str], officiele_aanbeveling_confidence: OfficialRecommendationMappingConfidence, matchbaarheid: Literal['hoog', 'middel', 'laag', 'niet_matchbaar']
  - Validators/normalizers: _normalize_official_confidence@199, _evidence_fields_must_not_be_empty@208
- Klasse `OfficieleAanbevelingCluster` op regel `214`
  - Bases: `BaseModel`
  - Docstring: Post-canonical link between one official source group and canonical items.
  - Velden: official_group_id: str, canonical_aanbeveling_refs: List[str], bron_aanbeveling_ids: List[str], document_nummer: Optional[str], source_hoofd_aanbeveling_id: Optional[str], bron_box_ids: List[Union[int, str]], source_range: Optional[str], coverage_status: Literal['volledig', 'gedeeltelijk', 'geen', 'onduidelijk'], mapping_confidence: OfficialRecommendationMappingConfidence, mapping_basis: List[str], warnings: List[str]
- Klasse `CanonicalProbleemdefinitie` op regel `240`
  - Bases: `BaseModel`
  - Docstring: Canonical problem definition derived from source problem definitions.
  - Velden: canonical_probleemdefinitie_id: str, bron_probleemdefinitie_ids: List[str], beschrijving: str, canonical_label: str, kernprobleem_ref: Optional[str], probleem_type: str, mechanisme_domein: str, beleidsobject: str, matchbaarheid: Literal['hoog', 'middel', 'laag', 'niet_matchbaar'], bron_box_ids: List[Union[int, str]], evidence_occurrences: List[CanonicalEvidenceOccurrence]
  - Validators/normalizers: _evidence_fields_must_not_be_empty@278
- Klasse `CanonicalBeleidslogicaLink` op regel `284`
  - Bases: `BaseModel`
  - Docstring: Canonical relation between canonical problems and recommendations.
  - Velden: canonical_beleidslogica_id: str, canonical_label: str, canonical_probleemdefinitie_refs: List[str], canonical_aanbeveling_refs: List[str], bron_beleidslogica_ids: List[str], beleidslogica_kort: str, linksterkte: Literal['direct', 'indirect', 'randvoorwaardelijk', 'onduidelijk'], link_confidence: Literal['hoog', 'gemiddeld', 'laag', 'onduidelijk'], evidence_occurrences: List[CanonicalEvidenceOccurrence]
  - Validators/normalizers: _link_evidence_fields_must_not_be_empty@315
- Klasse `CanonicalizationAuditItem` op regel `321`
  - Bases: `BaseModel`
  - Docstring: Audit row explaining how a source item was canonicalized.
  - Velden: audit_id: str, item_type: Literal['aanbeveling', 'probleemdefinitie', 'beleidslogica'], source_id: str, source_ids: List[str], canonical_id: Optional[str], decision: CanonicalizationAuditDecision, reason: str, evidence_box_ids: List[Union[int, str]]
  - Validators/normalizers: _normalize_legacy_audit_fields@347, _required_text_fields_must_not_be_empty@373, _evidence_box_ids_must_not_be_empty@380
- Klasse `CanonicalizationQualityChecks` op regel `386`
  - Bases: `BaseModel`
  - Docstring: Non-blocking validation signals for the canonical overlay.
  - Velden: canonicalization_status: CanonicalizationStatus, duplicate_recommendation_risk: CanonicalRiskLabel, combined_item_risk: CanonicalRiskLabel, missing_problem_link_risk: CanonicalRiskLabel, evidence_coverage_risk: CanonicalRiskLabel, hierarchy_risk: CanonicalRiskLabel, summary_only_evidence_risk: CanonicalRiskLabel, notes: List[str]
- Klasse `CanonicalizationResult` op regel `399`
  - Bases: `BaseModel`
  - Docstring: Canonical overlay emitted by the advice canonicalizer agent.
  - Velden: analyse_denkstappen: str, canonicalization_status: CanonicalizationStatus, canonical_aanbevelingen: List[CanonicalAanbeveling], canonical_probleemdefinities: List[CanonicalProbleemdefinitie], canonical_beleidslogica: List[CanonicalBeleidslogicaLink], canonicalization_audit: List[CanonicalizationAuditItem], officiele_aanbeveling_clusters: List[OfficieleAanbevelingCluster], quality_checks: CanonicalizationQualityChecks
  - Validators/normalizers: _salvage_policy_links_with_empty_required_lists@574, _validate_canonical_references@645
