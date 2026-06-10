# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_09_eindanalyse.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `cf079313dc04e72ec1a2f6921d113cba3481507cda22cab6f92d09c97cbd61c6`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `FinaleVerwerkingsitem` op regel `40`
  - Bases: `BaseModel`
  - Velden: advies_element_id: str, advies_element_type: AdviceElementType, advies_element_label: str, finale_verwerkingslabel: Verwerkingslabel, gebruik_in_analyse: GebruikInAnalyse, audit_oordeel: FinalAuditOordeel, review_nodig: bool, voorlopig_label_id: str | None, audit_id: str | None, candidate_pair_ids: list[str], semantic_match_ids: list[str], positie_opvolging_ids: list[str], segment_ids: list[str], bewijsbasis_kort: str, frame_mismatch: bool, herkomst: str, onduidelijk_herkomst: str
- Klasse `EindanalyseReviewpunt` op regel `71`
  - Bases: `BaseModel`
  - Velden: advies_element_id: str, advies_element_label: str, reden_review: str, prioriteit: ReviewPrioriteit
- Klasse `EindanalyseKabinetsreactieResultaat` op regel `80`
  - Bases: `BaseModel`
  - Velden: schema_version: str, document_id: str, advies_id: str, analyse_status: str, documentniveau_samenvatting: dict[str, Any], adviesstructuur_check: dict[str, Any], tellingen: dict[str, Any], finale_verwerkingsitems: list[FinaleVerwerkingsitem], analyse_probleemdefinities: dict[str, Any], analyse_aanbevelingen: dict[str, Any], analyse_beleidslogica: dict[str, Any], stramienanalyse: dict[str, Any], betrouwbaarheid_en_audit: dict[str, Any], reviewpunten: list[EindanalyseReviewpunt], scriptiepassage_kort: str, audit_notities: list[str]
