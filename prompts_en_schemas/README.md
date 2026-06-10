# Thesis Prompt- En Schema-Export

Deze map bevat een reproduceerbare export van prompts en schema-contracten
voor de thesisbijlage.

Gebruik voor een GitHub-link in de thesis deze ingang:

```text
structured/README.md
```

`structured/INDEX.md` bevat daarna de volledige bestandslijst.

De hoofdstructuur is:

```text
structured/
  matchers/
    01_instellingsmatcher/
    02_adviesmatcher/
    03_kabinetsreactie_matcher/
    04_parlementaire_matcher/
  ai_pipeline/
    01_classificatie/
    02_metadata/
    03_adviesextractie/
    04_kabinetsreactie_agent/
```

De grote bestanden blijven bestaan voor volledigheid:

- `prompts_schemas_export.md`: volledige bijlage in een bestand.
- `prompts_schemas_export.json`: machineleesbare index.

Run opnieuw vanuit de projectroot:

```powershell
python thesis_export\prompts_schema_export_20260605\build_export.py
```

Het script leest alleen bronbestanden. Het gebruikt geen LLM, API, database,
`.env`, caches of bestaande outputmappen.
