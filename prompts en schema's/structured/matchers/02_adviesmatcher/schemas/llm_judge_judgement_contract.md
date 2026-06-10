# Llm Judge Judgement Contract

## `JUDGEMENT_CONTRACT`

- Bron: `matcher/advies/llm_judge.py`
- Codebase: `matcher/advies`
- Type: `module_constant`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `3683f5a0d93793dbc5eb37b9057717108e116fe8b92ac9c77b6cffc7b6542ec5`
- Thesis-relevantie: LLM labelling prompt for deciding whether a candidate is a final advice document.
- Versies:
  - `LLM_PROMPT_VERSION`: `advies_discovery_llm_label_prompt_20260529_v6`

```python
JUDGEMENT_CONTRACT = {
    "final_advice_requires_target_own_report": (
        "Evidence must show the document is the target college's own advice, "
        "eindrapport, eindadvies or a report explicitly authored/adopted by "
        "the target college."
    ),
    "supporting_studies_are_not_main_advice": (
        "Commissioned studies, deelonderzoeken, technical annexes and reports "
        "written for a committee are relevant context, but not "
        "FINAL_ADVICE_OR_REPORT unless explicitly authored or adopted as the "
        "committee report."
    ),
    "stakeholder_and_response_documents_are_not_final_advice": (
        "Stakeholder responses, cabinet or policy responses, offering letters, "
        "roundtable reports, appointment letters and procedural documents are "
        "not the college's final advice."
    ),
    "duplicates_are_equivalent_not_independent": (
        "Alternate parliamentary publications of the same report should be "
        "identified as duplicate or equivalent publications, not as separate "
        "independent final advice documents."
    ),
    "broad_topic_matches_are_insufficient": (
        "A document that only shares a broad topic with the target, such as a "
        "technical report, progress report, parliamentary question, policy "
        "framework or regulatory note, is not FINAL_ADVICE_OR_REPORT without "
        "target-college authorship or adoption evidence."
    ),
}
```
