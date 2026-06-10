# Export Chatgpt Review Write Prompt File

## `_write_prompt_file`

- Bron: `matcher/advies/export_chatgpt_review.py`
- Codebase: `matcher/advies`
- Type: `function`
- Categorie: `schema_contract`
- Status: `manual`
- SHA256: `90ac6f7c7fbb4c58f21ed4c41ca10fb22b81f0c0b9a7b4c62b4c2b846093110b`
- Thesis-relevantie: Manual ChatGPT review prompt builder, only relevant for manually checked batches.

```python
def _write_prompt_file(output_dir: Path) -> None:
    prompt = """# ChatGPT-controle: welk document is het echte eindadvies?

Je bent een nauwkeurige onderzoeksassistent voor een politicologie-thesis over de
doorwerking van Nederlandse Kaderwet-adviescolleges (2005-2024). Voor een aantal
adviescolleges is automatisch een lijst kandidaat-documenten gevonden. Jouw taak
is om **per college te bepalen welk document (zo ja) het echte eindadvies /
eindrapport van dat college is**.

## Werkwijze (belangrijk: zoek elk document ONLINE op)
1. Neem het bestand van één college (de tabel met de top-10 kandidaten).
2. Voor elke kandidaat: **open de meegegeven online link** (kolom "Online link").
   Werkt de link niet of ontbreekt hij? **Zoek het document dan zelf op** via het
   document-ID en de titel op `officielebekendmakingen.nl`, `open.overheid.nl`,
   `zoek.officielebekendmakingen.nl` of de website van het college.
3. Bepaal voor elke kandidaat wat het document echt is:
   - **Eindadvies/eindrapport van het college zelf** (uitgebracht DOOR dit
     adviescollege), of
   - iets anders: een Kamerbrief/aanbiedingsbrief, een werkprogramma, een
     kabinetsreactie, een wet/wetsvoorstel, een begrotingsstuk, of niet
     gerelateerd.
4. Let op naamgeving: het moet echt om DIT college gaan, niet alleen een document
   dat het college toevallig noemt.

## Wat je per college teruggeeft
Geef per college een korte tabel terug met:
- de kandidaat-nummers,
- je oordeel per kandidaat (eindadvies van het college / anders – welk type),
- de bron-URL die je hebt bekeken,
- 1 zin onderbouwing.

Sluit af met een conclusie per college:
- **Hoofdadvies =** [document-ID + titel + URL], of
- **Geen geschikte kandidaat gevonden** (leg kort uit waarom).

Wees streng en eerlijk: als geen enkele kandidaat het echte eindadvies is, zeg dat
expliciet. Antwoord in het Nederlands.

## Hoe te gebruiken
Plak deze prompt in ChatGPT (met browsen/zoeken aan) en plak daarna de inhoud van
één college-bestand uit deze map. Herhaal per college, of geef ChatGPT de hele map
en laat het college voor college afwerken.
"""
    (output_dir / "_CHATGPT_PROMPT.md").write_text(prompt, encoding="utf-8")
```
