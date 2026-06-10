# Promotion Policy Schema

## `__classes__`

- Bron: `matcher/advies/promotion_policy.py`
- Codebase: `matcher/advies`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `c1f5ffa3bc0b437c8cf0605cee2512a52f5388c8c60a10946836eaf8a44f04b4`
- Thesis-relevantie: VLAM promotion payload and expected output contract for advice discovery.
- Versies:
  - `PROMOTION_POLICY_VERSION`: `advies_vlam_promotion_20260507_v1`

- Klasse `DuplicateDocumentWarning` op regel `58`
  - Velden: document_id: str, college_ids: tuple[int, ...], college_names: tuple[str, ...]
- Klasse `VlamPromotionResult` op regel `75`
  - Velden: college_id: int, officiele_naam: str, deterministic_status: str, vlam_status: VlamPromotionStatus, vlam_selected_document_id: str | None, vlam_selected_url: str | None, vlam_confidence: float, vlam_reason: str, vlam_compared_candidate_ids: tuple[str, ...], vlam_needs_human_review: bool, selected_candidate_document_id: str | None, duplicate_document_warning: str | None, phase_warning: str | None, provider: str | None, model: str | None, payload_stage: str
