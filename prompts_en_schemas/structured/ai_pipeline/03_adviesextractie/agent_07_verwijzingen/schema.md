# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/verwijzing_extractie/schema.py`
- Codebase: `AI adviescollege documenten - validatie`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `ca0494569e7891d50aa7dcc4ddb34470d27dbc2d7cc36a085b8fa450e37d6bd6`
- Thesis-relevantie: Pydantic output schemas paired with the advice-report extraction prompts.

- Klasse `VerwijzingExtractieResult` op regel `31`
  - Bases: `BaseModel`
  - Docstring: Hoofdmodel voor Call 1B-a: extractie van consultaties, scenario's, beleidsopties en betrokken actoren.  Geen context box_ids (die gaan in Call 1B-b). Geen classificaties (die gaan in Call 2).
  - Velden: analyse_denkstappen: str, consultaties_kort: List[ConsultatieKort], scenarios: List[ScenarioItem], beleidsopties: List[BeleidsOptie], betrokken_actoren: List[BetrokkenActorCompact]
  - Validators/normalizers: _handle_legacy_consultaties@49
