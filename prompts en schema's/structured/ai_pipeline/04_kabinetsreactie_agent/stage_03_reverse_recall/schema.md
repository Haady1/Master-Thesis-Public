# Schema

## `__classes__`

- Bron: `AI agents/AI kabinetsreactie agent/schemas/stage_03_reverse_recall.py`
- Codebase: `AI kabinetsreactie agent`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `f147d1c7f92a55a5f618476aa2802d031e8c3e23ee6dd77e89fd639b8ed68445`
- Thesis-relevantie: Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.

- Klasse `KandidaatLink` op regel `66`
  - Bases: `BaseModel`
  - Velden: advies_element_id: str, advies_element_type: AdviceElementType, canonical_label: str, match_plausibiliteit: str, relatie_tot_verwijzing: str, reden_kort: str
- Klasse `Adviesverwijzing` op regel `77`
  - Bases: `BaseModel`
  - Velden: verwijzing_id: str, segment_id: str, volgnummer: int, pagina_hint: str, segment_primaire_functie: str, verwijzingsterkte: str, verwijzingstype: VerwijzingsType, referentie_signaal: str, gerefereerde_adviesinhoud_kort: str, is_standpunt_of_alleen_weergave: str, link_status: LinkStatus, kandidaat_links: list[KandidaatLink], bron_citaten: list[KabinetsreactieBronCitaat], zekerheid: Zekerheid, audit_flags: list[AuditFlag], twijfelpunten: list[str]
- Klasse `MogelijkGemistAdviesItem` op regel `98`
  - Bases: `BaseModel`
  - Velden: missing_id: str, verwijzing_id: str, segment_id: str, waarschijnlijk_type: AdviceElementType | Literal['onduidelijk'], gerefereerde_adviesinhoud_kort: str, reden_waarom_mogelijk_gemist: str, bron_citaten: list[KabinetsreactieBronCitaat], review_prioriteit: ReviewPrioriteit
- Klasse `AdviesverwijzingReverseRecallResultaat` op regel `111`
  - Bases: `BaseModel`
  - Velden: schema_version: str, document_id: str, advies_id: str, samenvatting: dict[str, Any], verwijzingen: list[Adviesverwijzing], mogelijk_gemiste_advies_items: list[MogelijkGemistAdviesItem], audit_notities: list[str]
