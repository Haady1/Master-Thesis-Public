# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_08_audit.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `9d6faddd2fbf22915b282923cf40d8ab3645fbd2d411bf1dd9243246363a567d`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `BelangrijksteBewijsbasis` op regel `48`
  - Bases: `BaseModel`
  - Velden: candidate_pair_ids: list[str], semantic_match_ids: list[str], positie_opvolging_ids: list[str], segment_ids: list[str]
- Klasse `AuditItem` op regel `57`
  - Bases: `BaseModel`
  - Velden: audit_id: str, voorlopig_label_id: str, advies_element_id: str, advies_element_type: str, advies_element_label: str, voorlopig_verwerkingslabel: Verwerkingslabel, audit_oordeel: AuditOordeel, aanbevolen_verwerkingslabel: Verwerkingslabel, gebruik_in_analyse: GebruikInAnalyse, reden_audit_oordeel: str, belangrijkste_bewijsbasis: BelangrijksteBewijsbasis, consistentie_controles: dict[str, Any], audit_flags: list[str], stramien_flags: list[str], fouttype_flags: list[str], aanbevolen_correctie_toelichting: str, menselijke_review_nodig: bool, review_prioriteit: ReviewPrioriteit, twijfelpunten: list[str]
- Klasse `AuditEnReconciliatieResultaat` op regel `81`
  - Bases: `BaseModel`
  - Velden: schema_version: str, document_id: str, advies_id: str, samenvatting: dict[str, Any], audit_items: list[AuditItem], documentbrede_audit: dict[str, Any], audit_notities: list[str]
