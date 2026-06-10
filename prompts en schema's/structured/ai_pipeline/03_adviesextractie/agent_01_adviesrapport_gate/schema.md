# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/adviesrapport_gate/schema.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `689f35bd127fd2ab105bf69c8e525b9db582ebf9d87a994242e92fb6ddb3eda8`
- Thesis-relevantie: Pydantic output schemas paired with the advice-report extraction prompts.

- Klasse `AdviesrapportGateResult` op regel `51`
  - Bases: `_CompactBoxIdsMixin, BaseModel`
  - Docstring: Structured decision for the pre-extraction adviesrapport gate.
  - Velden: decision: GateDecision, confidence: int, suggested_doc_type: Optional[str], reasoning: str, positive_report_signals: list[str], blocking_form_signals: list[str], evidence_box_ids: list[Union[int, str]]
  - Validators/normalizers: _validate_decision_contract@103
