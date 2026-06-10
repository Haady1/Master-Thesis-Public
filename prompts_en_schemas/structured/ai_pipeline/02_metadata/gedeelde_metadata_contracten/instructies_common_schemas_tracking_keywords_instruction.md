# Instructies Common Schemas Tracking Keywords Instruction

## `TRACKING_KEYWORDS_INSTRUCTION`

- Bron: `AI agents/AI adviescollege documenten - classificatie and metadata/agents/metadata_agent/schemas/common_schemas.py`
- Codebase: `AI adviescollege documenten - classificatie and metadata`
- Type: `module_constant`
- Categorie: `prompt`
- Status: `active`
- SHA256: `0c2df5f65c532180fa600fc9f248eb2e973a4f82400ba525f127df5485a35690`
- Thesis-relevantie: Shared metadata evidence and theme-code schema definitions.

```text
### tracking_keywords (CRUCIAAL VOOR S2-RETRIEVAL)
Genereer zoektermen om later het juiste inhoudelijke beleidsdossier terug te vinden in een database van Kamerstukken:
1. internal_fingerprint: Unieke, specifieke termen of projectnamen om dit traject te groeperen.
2. external_search_terms: De kern van de specifieke beleidskwestie (bijv. 'arbeidsparticipatie statushouders zorg').
- HARDE EIS 1: Gebruik ABSOLUUT GEEN algemene wetten, kaders of reglementen (zoals 'Kaderwet adviescolleges', 'Vreemdelingenwet 2000', 'Gemeentewet', 'Reglement van Orde') als zoekterm.
- HARDE EIS 2: Gebruik geen generieke politieke termen. Richt je uitsluitend op het unieke inhoudelijke probleem dat wordt geadviseerd.
- HARDE EIS 3: Vermijd losse containerwoorden zoals 'beleid', 'overheid', 'geschiedenis', 'racisme' of 'discriminatie' als zelfstandige zoekterm.
- FORMULEER als korte, dossier-specifieke nominale frase.
- GOEDE voorbeelden: 'arbeidsmarktdiscriminatie bij stagezoekende mbo studenten', 'doorwerking slavernijverleden in onderwijscanon', 'regionale uitvoeringscapaciteit jeugdzorg'.
- SLECHTE voorbeelden: 'beleid', 'overheid', 'discriminatie', 'geschiedenis', 'wetgeving'.
- Bij illustraties/schema's zonder inhoudelijk dossier zijn tracking_keywords
  alleen eventueel technische OCR/fingerprint-termen. Gebruik labels op
  puzzelstukken of schema-onderdelen NIET als inhoudelijke metadata of
  external_search_terms.
```
