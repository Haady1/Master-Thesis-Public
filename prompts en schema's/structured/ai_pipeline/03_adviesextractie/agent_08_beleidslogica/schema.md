# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/beleidslogica_agent/schema.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `a73fdc8884dfff1fc625e18ddb3c42ab503f203e796fae141c92b595c2d1974c`
- Thesis-relevantie: Pydantic output schemas paired with the advice-report extraction prompts.

- Klasse `BeleidslogicaLink` op regel `41`
  - Bases: `BaseModel`
  - Docstring: One explicit policy-logic relation between existing extracted items.
  - Velden: advieslijn_id: str, canonical_label: str, probleemdefinitie_refs: List[str], aanbeveling_refs: List[str], relatie_type: RelatieType, link_confidence: LinkConfidence, link_basis: List[LinkBasis], toelichting: str, evidence_problem_box_ids: List[Union[int, str]], evidence_recommendation_box_ids: List[Union[int, str]]
  - Validators/normalizers: _coerce_refs@57, _normalize_link_basis_aliases@66, _flatten_evidence_box_ids@94
- Klasse `NietGekoppeldItem` op regel `108`
  - Bases: `BaseModel`
  - Docstring: Diagnostic item for a valid input item that was not linked.
  - Velden: item_id: str, reden: str
  - Validators/normalizers: _hydrate_legacy_ref_names@116
- Klasse `BeleidslogicaResult` op regel `130`
  - Bases: `BaseModel`
  - Docstring: Complete constrained beleidslogica output.
  - Velden: analyse_denkstappen: str, beleidslogica: List[BeleidslogicaLink], niet_gekoppelde_probleemdefinities: List[NietGekoppeldItem], niet_gekoppelde_aanbevelingen: List[NietGekoppeldItem]
