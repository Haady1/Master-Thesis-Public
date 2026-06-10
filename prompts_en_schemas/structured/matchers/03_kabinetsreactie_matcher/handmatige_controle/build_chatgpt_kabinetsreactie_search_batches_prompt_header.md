# Build Chatgpt Kabinetsreactie Search Batches Prompt Header

## `PROMPT_HEADER`

- Bron: `matcher/kabinetsreactie/build_chatgpt_kabinetsreactie_search_batches.py`
- Codebase: `matcher/kabinetsreactie`
- Type: `module_constant`
- Categorie: `prompt`
- Status: `manual`
- SHA256: `63e36f73ade2b068dc6670f06e2e0d3a76d6a0aef35475cb59ac8d22485d4bd1`
- Thesis-relevantie: Manual ChatGPT/web-search batch prompt, only relevant when manual validation was used.

````text
# ChatGPT-zoekopdracht: bestaat er een kabinetsreactie op deze adviezen?

## Wat je moet doen
Je bent een onderzoeksassistent. Voor ELK advies hieronder ga je ACTIEF OP HET INTERNET ZOEKEN
(gebruik je web-/browsing-tool; doe meerdere zoekopdrachten per advies). Vertrouw NIET op je
geheugen — open en lees daadwerkelijk bronnen. Zoek vooral op:
- zoek.officielebekendmakingen.nl en officielebekendmakingen.nl
- open.overheid.nl
- tweedekamer.nl (Kamerstukken / brieven regering)
- rijksoverheid.nl

Je zoekt of er een **kabinetsreactie** bestaat: een brief of Kamerstuk van de regering, een
minister of staatssecretaris waarin op DIT specifieke advies INHOUDELIJK wordt gereageerd
(appreciatie van het advies, overname of afwijzing van aanbevelingen).

Zoektips: combineer de naam van het adviescollege + het onderwerp/titel + woorden als
"kabinetsreactie", "reactie op het advies", "appreciatie", "brief regering", plus het jaartal.

## Wat NIET telt als kabinetsreactie
Een aanbiedingsbrief, instellingsbesluit, benoemings-/ontslagbesluit, vacature, of het advies
zelf telt NIET. Het moet een inhoudelijke regeringsreactie zijn. Wees streng; bij twijfel
"onzeker" met uitleg.

## Verplicht uitvoerformaat (machine-leesbaar)
Je mag eerst kort je redenering per advies geven. MAAR sluit je antwoord ALTIJD af met EEN
enkel JSON-codeblok (```json ... ```) met een array van objecten, EXACT 1 object per advies,
en gebruik de `advies_document_id` precies zoals hieronder vermeld. Gebruik dit schema:

```json
[
  {
    "advies_document_id": "blg-XXXXXX",
    "kabinetsreactie_gevonden": "ja",
    "reactie_titel": "officiele titel van de reactie, of null",
    "reactie_publicatie_id": "bv. kst-32175-17 of stcrt-2019-... , of null",
    "reactie_url": "directe URL naar de reactie, of null",
    "reactie_datum": "YYYY-MM-DD of null",
    "bewijs_citaat": "korte letterlijke zin uit de reactie die aantoont dat het op DIT advies reageert, of null",
    "toelichting": "1-2 zinnen waarom dit wel/niet een kabinetsreactie is",
    "zekerheid": 0.0
  }
]
```

Regels voor het JSON-blok:
- `kabinetsreactie_gevonden`: gebruik exact "ja", "nee" of "onzeker".
- `zekerheid`: getal tussen 0.0 en 1.0 (jouw zekerheid dat dit een echte kabinetsreactie is).
- Bij "nee": zet reactie_* en bewijs_citaat op null, maar vul wel `toelichting`.
- Verzin NOOIT een URL of publicatienummer; als je het niet zeker via een bron hebt, gebruik null.
- Lever geldige JSON: dubbele aanhalingstekens, geen trailing komma's.

---
````
