# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/aanbeveling_precision/schema.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `6cedb2b175fcfea93e9b27b6d317212200cfa3d78a512ba2cfb3c83eb0955655`
- Thesis-relevantie: Pydantic output schemas paired with the advice-report extraction prompts.

- Klasse `AanbevelingPrecisionItem` op regel `37`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Verificatie-uitkomst voor een eerder door recall gevonden kandidaat. Bevat alleen de keep/drop/reopen beslissing en de bijbehorende span. Verdere metadata voor behouden aanbevelingen komt uit recall/postprocessing, niet uit deze precision-output.
  - Velden: candidate_id: int, status: PrecisionStatus, status_reason: Optional[str], status_reason_code: Optional[PrecisionReasonCode], box_ids: List[Union[int, str]]
  - Validators/normalizers: _validate_consistency@77
- Klasse `AanbevelingPrecisionBatchResult` op regel `102`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Batch-output van de precision verificatie-agent.
  - Velden: analyse_denkstappen: str, aanbevelingen: List[AanbevelingPrecisionItem]
