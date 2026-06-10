# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - classificatie and metadata/agents/classificatie_agents/schemas/classification_schemas.py`
- Codebase: `AI adviescollege documenten - classificatie and metadata`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `fd6d4e52d084bc66ae46604719a1dda64c6a08282837ef90f5a21d14d9036395`
- Thesis-relevantie: Pydantic classification and verification schemas.

- Klasse `DocTypeClassificationResult` op regel `94`
  - Bases: `BaseModel`
  - Docstring: Document type classification output.
  - Velden: analysis_trace: str, document_role: DocumentRole, formal_advice_status: FormalAdviceStatus, advice_product_form: AdviceProductForm, author_voice: AuthorVoice, trajectory_relation: TrajectoryRelation, adviesrapport_boundary: Optional[str], main_category: str, sub_category: str, second_choice_main_category: Optional[str], second_choice_sub_category: Optional[str], second_choice_reasoning: Optional[str], alternative_sub_category_same_main: Optional[str], alternative_same_main_reasoning: Optional[str], confidence: int, confidence_gap_analysis: str, detected_language: Optional[str]
  - Validators/normalizers: validate_classification_choices@195
- Klasse `SubAgentVerificationResult` op regel `282`
  - Bases: `BaseModel`
  - Docstring: Uniform output from category-specific verification sub-agents.
  - Velden: tegen_bewijs: str, redenatie: str, akkoord: bool, confidence: int, gecorrigeerde_categorie: str, formal_advice_status: FormalAdviceStatus, document_role: DocumentRole, advice_product_form: AdviceProductForm, author_voice: AuthorVoice, trajectory_relation: TrajectoryRelation, adviesrapport_boundary: Optional[str], checklist_antwoorden: Optional[List[str]]
  - Validators/normalizers: validate_verification_role_form_consistency@355
- Klasse `WaterfallVerificationResult` op regel `380`
  - Bases: `BaseModel`
  - Docstring: Complete result of the updated verification logic (Phase 2b).
  - Velden: first_choice_sub_category: str, first_choice_main_category: str, second_choice_sub_category: Optional[str], second_choice_main_category: Optional[str], verified: bool, verification_result: SubAgentVerificationResult, final_sub_category: str, final_main_category: str, status: Literal['FIRST_CHOICE_ACCEPTED', 'SECOND_CHOICE_ACCEPTED', 'VARIA', 'OTHER_CORRECTION']
