# Stage Registry

## `STAGE_DEFINITIONS`

- Bron: `AI agents/AI kabinetsreactie agent/pipeline/document_pipeline.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `508101b4da1fcb8f235e1cc9d0d94481d39969cac94511f0f8a38c64c0584180`
- Thesis-relevantie: V2 stage registry that links each kabinetsreactie prompt to its schema and schema version.

```python
STAGE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "01_segmentatie": {
        "schema": SegmentatieResultaat,
        "prompt": "agents/01_kabinetsreactie_segmentatie_agent_instruction.txt",
        "model_type": "fast",
        "schema_version": "kabinetsreactie_segmentatie_v1",
    },
    "02_stramien": {
        "schema": StramienAnalyseResultaat,
        "prompt": "agents/02_stramien_analyse_agent_instruction.txt.txt",
        "model_type": "fast",
        "schema_version": "stramien_analyse_v1",
    },
    "03_reverse_recall": {
        "schema": AdviesverwijzingReverseRecallResultaat,
        "prompt": "agents/03_adviesverwijzing_reverse_recall_agent_instruction.txt.txt",
        "model_type": "fast",
        "schema_version": "adviesverwijzing_reverse_recall_v1",
    },
    "04_candidate_pairs": {
        "schema": CandidatePairRetrievalResultaat,
        "prompt": "agents/04_candidate_pair_retrieval_agent_instruction.txt.txt",
        "model_type": "fast",
        "schema_version": "candidate_pair_retrieval_v1",
    },
    "05_semantische_match": {
        "schema": SemantischeMatchResultaat,
        "prompt": "agents/05_semantische_match_agent_instruction.txt.txt",
        "model_type": "fast",
        "schema_version": "semantische_match_v1",
    },
    "06a_positie": {
        "schema": PositieResultaat06a,
        "prompt": "agents/06a_kabinetspositie_agent_instruction.txt",
        "model_type": "fast",
        "schema_version": "positie_v1",
    },
    "06b_context": {
        "schema": ContextResultaat06b,
        "prompt": "agents/06b_opvolgingscontext_agent_instruction.txt",
        "model_type": "fast",
        "schema_version": "context_v1",
    },
    "08_audit": {
        "schema": AuditEnReconciliatieResultaat,
        "prompt": "agents/08_audit_en_reconciliatie_agent_instruction.txt.txt",
        "model_type": "fast",
        "schema_version": "audit_en_reconciliatie_v1",
    },
    "09_eindanalyse": {
        "schema": EindanalyseKabinetsreactieResultaat,
        "prompt": "agents/09_eindanalyse_agent_instruction.txt.txt",
        "model_type": "fast",
        "schema_version": "eindanalyse_kabinetsreactie_v1",
    },
}
```
