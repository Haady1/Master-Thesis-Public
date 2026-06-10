# Export Kandidaten Chatgpt Prompt Header

## `PROMPT_HEADER`

- Bron: `matcher/advies/export_kandidaten_chatgpt.py`
- Codebase: `matcher/advies`
- Type: `module_constant`
- Categorie: `prompt`
- Status: `manual`
- SHA256: `97e5743382357ff3b7278c72b4f73110f2024c3a204657a0db20c47a0fe49d54`
- Thesis-relevantie: Manual ChatGPT batch prompt for online candidate checks.

```text
Je bent expert in Nederlandse Kaderwet-adviescolleges en overheidsdocumenten.
Hieronder staan kandidaat-documenten die een geautomatiseerde discovery-pipeline
heeft gevonden voor enkele tijdelijke adviescolleges die nu nog GEEN gekoppelde
adviezen hebben. We willen weten welke van deze kandidaten echte adviezen/rapporten
van dat college zijn, en welke iets anders (begeleidende brief, instellingsbesluit,
kamerstuk, bijlage, voortgangsrapport).

BELANGRIJK — zoek elk document eerst op. Vertrouw NIET blind op de titel of het
voorlopige label. Gebruik web-search (zoek op de exacte titel + het jaar, of open
de gegeven bron-URL) en bepaal aan de bron WAT voor document het is en WELK
adviescollege het feitelijk heeft uitgebracht.

Geef PER DOCUMENT je oordeel als:
  document_id | TYPE | hoort-bij-college (ja/nee/onzeker) | bron-URL | korte motivatie

waarbij TYPE een van: ADVIESRAPPORT, VOORTGANGS-/CONTEXTBRIEF, INSTELLINGSBESLUIT,
KAMERSTUK, BIJLAGE, ANDERS.

Let op:
- ADVIESRAPPORT = een inhoudelijk advies/eindrapport van het college zelf.
- Als je het document niet kunt terugvinden: zet TYPE=ANDERS en hoort-bij-college=onzeker.
- Noem bij twijfel expliciet waarom.
```
