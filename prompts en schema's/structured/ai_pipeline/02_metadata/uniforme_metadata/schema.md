# Schema

## `__classes__`

- Bron: `AI agents/AI adviescollege documenten - classificatie and metadata/agents/metadata_agent/schemas/uniform_schema.py`
- Codebase: `AI adviescollege documenten - classificatie and metadata`
- Type: `class_summary`
- Categorie: `schema`
- Status: `active`
- SHA256: `bee38ddc44d2dfbd61c96851c6d566e687f9539f2750c36e25e83ad472442d2b`
- Thesis-relevantie: Uniform metadata schema used by metadata agents.

- Klasse `Ondertekenaar` op regel `41`
  - Bases: `BaseModel`
  - Docstring: Een mede-ondertekende organisatie bij gezamenlijk advies.
  - Velden: organisatie: str, box_ids: List[Union[int, str]]
- Klasse `UniformMetadataResult` op regel `57`
  - Bases: `BaseModel`
  - Docstring: Uniform metadata schema voor alle document types.  Alle agents moeten deze veldnamen gebruiken voor consistente output.
  - Velden: is_verkeerd_document: Optional[bool], verkeerd_document_reden: Optional[str], document_titel: Optional[str], document_titel_box_ids: List[Union[int, str]], document_titel_evidence: Optional[str], document_titel_zone: Optional[str], document_titel_confidence: Optional[float], document_subtitel: Optional[str], document_subtitel_box_ids: List[Union[int, str]], document_datum: Optional[str], document_datum_box_ids: List[Union[int, str]], document_datum_evidence: Optional[str], document_datum_zone: Optional[str], document_datum_confidence: Optional[float], document_kenmerk: Optional[str], document_kenmerk_box_ids: List[Union[int, str]], uw_kenmerk: Optional[str], uw_kenmerk_box_ids: List[Union[int, str]], afzender_organisatie: Optional[List[str]], afzender_organisatie_box_ids: List[Union[int, str]], afzender_organisatie_evidence: Optional[str], afzender_organisatie_zone: Optional[str], afzender_organisatie_confidence: Optional[float], afzender_functie: Optional[str], afzender_functie_box_ids: List[Union[int, str]], mede_ondertekenaars: Optional[List[Ondertekenaar]], ontvanger_organisatie: Optional[List[str]], ontvanger_organisatie_box_ids: List[Union[int, str]], ontvanger_functie: Optional[List[str]], ontvanger_functie_box_ids: List[Union[int, str]], wetsvoorstel_titel: Optional[str], wetsvoorstel_titel_box_ids: List[Union[int, str]], wetsvoorstel_afkorting: Optional[str], wetsvoorstel_afkorting_box_ids: List[Union[int, str]], dossier_nummer: Optional[str], dossier_nummer_box_ids: List[Union[int, str]], vergaderdatum: Optional[str], vergaderdatum_box_ids: List[Union[int, str]], opdrachtgever: Optional[str], opdrachtgever_box_ids: List[Union[int, str]] ... (+23 velden)
  - Validators/normalizers: normalize_recipient_list@400, validate_isbn_doi@422, normalize_datum@440
