# Promotion Policy Coerce Vlam Promotion Result

## `coerce_vlam_promotion_result`

- Bron: `matcher/advies/promotion_policy.py`
- Codebase: `matcher/advies`
- Type: `function`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `6f68c2bc9e7d10a0dcd45fbf925e1e11c80c4e94e3f653e3f8a71a6617aeccf8`
- Thesis-relevantie: VLAM promotion payload and expected output contract for advice discovery.
- Versies:
  - `PROMOTION_POLICY_VERSION`: `advies_vlam_promotion_20260507_v1`

```python
def coerce_vlam_promotion_result(
    raw: dict[str, Any],
    payload: dict[str, Any],
    *,
    provider: str | None = None,
    model: str | None = None,
    payload_stage: str = "top_candidates",
) -> VlamPromotionResult:
    candidate_ids = tuple(
        str(candidate.get("candidate_document_id"))
        for candidate in payload.get("candidates", [])
        if candidate.get("candidate_document_id")
    )
    status = str(raw.get("vlam_status") or raw.get("status") or "needs_review")
    if status not in {"approved_promote", "needs_review", "reject", "not_run"}:
        status = "needs_review"
    selected_id = raw.get("vlam_selected_document_id") or raw.get(
        "selected_document_id"
    )
    selected_id = str(selected_id) if selected_id else None
    if selected_id not in candidate_ids:
        selected_id = None
        if status == "approved_promote":
            status = "needs_review"
    confidence = _coerce_float(raw.get("vlam_confidence") or raw.get("confidence"))
    reason = str(raw.get("vlam_reason") or raw.get("reason") or "").strip()
    if not reason:
        reason = "Geen controleerbare VLAM-redenering ontvangen."
        confidence = min(confidence, 0.2)
        if status == "approved_promote":
            status = "needs_review"
    gate_failures: list[str] = []
    if status == "approved_promote":
        gate_failures = _approval_gate_failures(
            payload=payload,
            selected_document_id=selected_id,
            confidence=confidence,
        )
        if gate_failures:
            status = "needs_review"
            reason = (
                reason
                + " | approval_gate_blocked="
                + ",".join(gate_failures)
            )
    selected_url = _candidate_url(payload, selected_id)
    warnings = payload.get("warnings") or {}
    target = payload.get("target") or {}
    policy = payload.get("promotion_policy") or {}
    selected_candidate = payload.get("selected_candidate") or {}
    needs_review = bool(
        raw.get("vlam_needs_human_review")
        if "vlam_needs_human_review" in raw
        else status != "approved_promote"
    )
    if status != "approved_promote" or gate_failures:
        needs_review = True
    return VlamPromotionResult(
        college_id=int(target.get("college_id") or 0),
        officiele_naam=str(
            target.get("officiele_naam")
            or target.get("official_name")
            or ""
        ),
        deterministic_status=str(policy.get("deterministic_status") or ""),
        vlam_status=status,  # type: ignore[arg-type]
        vlam_selected_document_id=selected_id if status == "approved_promote" else None,
        vlam_selected_url=selected_url if status == "approved_promote" else None,
        vlam_confidence=confidence,
        vlam_reason=reason[:800],
        vlam_compared_candidate_ids=candidate_ids,
        vlam_needs_human_review=needs_review,
        selected_candidate_document_id=selected_candidate.get(
            "candidate_document_id"
        ),
        duplicate_document_warning=_warning_text(
            warnings.get("duplicate_document_warning")
        ),
        phase_warning=warnings.get("phase_warning"),
        provider=provider,
        model=model,
        payload_stage=payload_stage,
    )
```
