# Final Result Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/schemas/final_result.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `bd707ad8de9db1cf69547a0a4a2e5f15c5c2dc522b623f16d97ea391aa768c03`
- Thesis-relevantie: Final advice-report extraction result schema used downstream in the thesis pipeline.

- Klasse `ExtractieReliability` op regel `92`
  - Bases: `BaseModel`
  - Docstring: Top-level reliability contract for downstream measurement decisions.
  - Velden: is_fully_reliable: bool, blocking_subpipelines: List[str], partial_subpipelines: List[str], warning_count: int, warning_flags: List[str], diagnostics: dict
- Klasse `RapportProbleemAnalyse` op regel `124`
  - Bases: `BaseModel`
  - Docstring: Compacte rapport-niveau probleemanalyse voor downstream validatie.
  - Velden: hoofdprobleem_synthese: Optional[HoofdProbleemSynthese], hoofdprobleem_box_ids: List[Union[int, str]], dominante_urgentie: Optional[dict], dominante_causaliteitsframing: Optional[dict], dominante_probleemframing: Optional[dict], probleemdefinities_aantal: int, candidate_audit: List[dict], dedup_clusters: List[dict], candidate_lifecycle: List[dict], precision_batch_status: List[dict], pipeline_status: ProbleemDefinitiePipelineStatus, traceability_warnings: List[str]
- Klasse `RapportAanbevelingAnalyse` op regel `174`
  - Bases: `BaseModel`
  - Docstring: Compacte rapport-niveau aggregatie van aanbevelingspatronen.
  - Velden: operationaliteit_rapport: Optional[OperationaliteitRapport], orde_van_verandering: Optional[OrdeVanVerandering], aanbevelingenpakket_samenvatting: Optional[str], bewijs_box_ids: List[Union[int, str]], aanbevelingen_aantal: int, aanbevelingen_extractie_status: AanbevelingenExtractieStatus, extraction_warnings: List[str], aanbevelingen_aantal_input_candidates: int, aanbevelingen_aantal_unresolved: int, aanbevelingen_aantal_dropped: int, aanbevelingen_aantal_failed: int, reliability_label: ReliabilityLabel
- Klasse `BeleidslogicaItem` op regel `233`
  - Bases: `BaseModel`
  - Docstring: Expliciete link tussen probleemdefinitie(s) en aanbeveling(en).
  - Velden: advieslijn_id: str, canonical_label: str, probleemdefinitie_refs: List[str], aanbeveling_refs: List[str], beleidslogica_kort: str, link_tekst: str, linksterkte: Literal['direct', 'indirect', 'randvoorwaardelijk', 'onduidelijk'], link_confidence: Literal['hoog', 'gemiddeld', 'laag', 'onduidelijk'], link_basis: List[str], evidence_problem_box_ids: List[Union[int, str]], evidence_recommendation_box_ids: List[Union[int, str]], generated_by: Literal['beleidslogica_agent', 'deterministic_fallback', 'unknown']
- Klasse `AdviesRapportExtractieResult` op regel `277`
  - Bases: `_SoftTruncateMixin, _CompactBoxIdsMixin, BaseModel, SelfCheckMixin`
  - Docstring: Hoofdmodel voor de diepte-extractie van een Adviesrapport (box-mode).  Bronnen:   Universiteit van Tilburg & Berenschot (2004), Spelen met doorwerking.   Ministerie van BZK (2011), Derde staat van advies.   Craft, J., & Howlett, M. (2012), Policy formulation, governance shifts     and policy influence.   Schlaufer (2019) in Routledge Handbook of Policy Advisory Systems (2025).   Boswell, C. (2009), The Political Uses of Expert Knowledge.   Hall, P.A. (1993), Policy Paradigms, Social Learning, and the State,     Comparative Politics, 25(3), p. 275-296.
  - Velden: analyse_denkstappen: str, is_co_advies: bool, redenering_co_advies: str, beleidsreikwijdte: Beleidsreikwijdte, operationaliteit_rapport: OperationaliteitRapport, onderzoeksmethodologie: Onderzoeksmethodologie, scenarios_en_opties: ScenariosEnOpties, scenarios: List[ScenarioItem], orde_van_verandering: OrdeVanVerandering, hoofdprobleem_synthese: Optional[HoofdProbleemSynthese], rapport_aanbeveling_analyse: Optional[RapportAanbevelingAnalyse], rapport_probleem_analyse: Optional[RapportProbleemAnalyse], aanbevelingen: List[Aanbeveling], hoofd_aanbevelingen: List[Aanbeveling], overige_aanbevelingen: List[Aanbeveling], probleemdefinities: List[Probleemdefinitie], beleidslogica: List[BeleidslogicaItem], beleidslogica_diagnostics: Optional[dict], canonical_aanbevelingen: List[CanonicalAanbeveling], canonical_probleemdefinities: List[CanonicalProbleemdefinitie], canonical_beleidslogica: List[CanonicalBeleidslogicaLink], canonicalization_audit: List[CanonicalizationAuditItem], officiele_aanbeveling_clusters: List[OfficieleAanbevelingCluster], quality_checks: CanonicalizationQualityChecks, canonicalization_status: CanonicalizationStatus, consultaties_kort: List[ConsultatieKort], interactie_aanwezig: Literal['ja', 'nee', 'onduidelijk'], beleidsopties: List[BeleidsOptie], betrokken_actoren: List[BetrokkenActorCompact], advies_vraag: Optional[dict], advies_vraag_box_ids: List[Union[int, str]], recall_candidate_audit: List[RecallCandidateAudit], recall_postprocessing_stats: Optional[dict], consolidatie_stats: Optional[dict], aanbevelingen_extractie_status: AanbevelingenExtractieStatus, extraction_warnings: List[str], precision_batch_status: List[dict], precision_candidate_status: List[dict], aanbevelingen_aantal_input_candidates: int, aanbevelingen_aantal_unresolved: int ... (+4 velden)
  - Validators/normalizers: _handle_legacy_consultaties@567
