# DV2-aanpak resultatensectie

Peildatum: 2026-06-05
Scope: Nederlandstalige analysepijplijn (`include_english=False`)
Status: werkbestand voor het schrijven van de DV2-resultatensectie

## Doel van DV2

DV2 beantwoordt niet de vraag hoe groot het corpus is, maar hoe betrouwbaar de
AI-documentanalyse is. De deelvraag moet daarom worden uitgewerkt als
validatiefunnel: per AI-stap wordt vastgesteld welke output sterk genoeg is voor
corpusbrede conclusies, welke output alleen voorzichtig bruikbaar is, en welke
output niet als harde meetvariabele mag worden gebruikt.

Kernverschil met DV1:

- DV1 is een corpusfunnel: colleges, documenten, koppelingen en noemers.
- DV2 is een validatiefunnel: accuraatheid, stabiliteit, dekking,
  traceerbaarheid en verantwoord gebruik.

## Hoofdbronnen

Gebruik voor DV2 de bevroren bronnen die zijn uitgelijnd op de actuele
171-Kaderwet-scope:

- `thesis/Analyse/DV2_validatie_bronnen/README_DV2_bronnen.md`
- `thesis/Analyse/DV2_validatie_bronnen/01b_adviesvalidatie_171_frozen_20260605`
- `thesis/Analyse/DV2_validatie_bronnen/02b_kabinetsreactie_171_frozen_20260605`
- `thesis/Analyse/DV2_betrouwbaarheid_AI_documentanalyse_validatie.ipynb`
- `thesis/Analyse/DV2_meetmethoden_validatietekst.tex`

Leidende instellingen:

- `include_english=False`
- `USE_FROZEN_ADVIES=True`
- `USE_171_SCOPE_KABINET=True`
- peildatum: `2026-06-05`

## Hoofdnoemers

Gebruik deze noemers als uitgangspunt voor de DV2-tekst:

| Laag | Noemer | Betekenis |
| --- | ---: | --- |
| Adviesvalidatie | 1.374 adviesrapporten | Bevroren Nederlandstalige adviesvalidatie binnen de 171-Kaderwet-scope |
| Aanbevelingen | 22.286 elementen | Geextraheerde aanbevelingen uit de adviesrapporten |
| Probleemdefinities | 17.927 elementen | Geextraheerde probleemdefinities uit de adviesrapporten |
| Kabinetsreactievalidatie | 419 documenten | In-scope kabinetsreactiedocumenten in de DV2-bundel |
| Kabinetsreactie-elementen | 13.165 elementen | Advieselementen in de kabinetsreactievalidatie |
| Golden set kabinetsreactie | 87 elementen | In-scope golden/silver-set na afbakening |

## Voorgestelde tekstlengte

Schrijf de hoofdtekst compact: ongeveer 600 tot 700 woorden. De tekst moet
vooral het oordeel uitleggen, niet alle validatiedetails herhalen.

Voorgestelde volgorde:

1. Wat DV2 toetst: bruikbaarheid van AI-codering, niet perfectie.
2. Welke onderdelen sterk zijn: aanbevelingen, probleemdefinities en
   documentclassificatie.
3. Welke onderdelen voorzichtig gebruikt moeten worden: kabinetsreactielabels,
   vooral op elementniveau.
4. Welke onderdelen niet hard gebruikt mogen worden: consultatie-actoren,
   beleidslogica-koppelingen en theoretische labels.
5. Wat dit betekent voor DV3: AI gebruiken voor patronen op schaal, broncontrole
   voor losse casussen en gevoelige interpretaties.

## Hoofdtabellen

Gebruik maximaal twee of drie tabellen in de hoofdtekst.

### Tabel 1: Kernscores per AI-stap

Doel: in een oogopslag laten zien hoe goed de hoofdonderdelen presteren.

Kolommen:

- AI-stap
- noemer/testset
- kernscore
- oordeel
- betekenis voor gebruik

Opnemen:

- adviesextractie aanbevelingen;
- adviesextractie probleemdefinities;
- documentclassificatie;
- kabinetsreactie exact match;
- behandeld versus niet behandeld.

### Tabel 2: Gebruiksoordeel groen/oranje/rood

Doel: direct koppelen wat wel en niet verantwoord gebruikt mag worden.

Kolommen:

- onderdeel
- oordeel
- verantwoord gebruik
- beperking

Richtlijn:

- groen: aanbevelingen, probleemdefinities, documentclassificatie;
- oranje: brede kabinetsreactiepatronen en geaggregeerde labels;
- rood: consultatie-actoren, beleidslogica-koppelingen, Weiss/Hall-labels als
  harde kwantitatieve uitkomst.

### Tabel 3: Stabiliteit en dekking

Optioneel in de hoofdtekst. Alleen opnemen als er ruimte is.

Kolommen:

- controle
- uitkomst
- betekenis

Mogelijke rijen:

- adviesextractie hertest;
- kabinetsreactie hertest;
- missingness/dekking;
- traceerbaarheid naar bronpassages.

Als de tekst te lang wordt, gaat deze tabel naar de bijlage.

## Bijlage of CSV

Detailtabellen horen niet in de hoofdtekst. Zet ze in een CSV of bijlage.

Opnemen in bijlage/CSV:

- confusiematrix kabinetsreactielabels;
- per-label precision, recall en F1;
- hertest- en stabiliteitscijfers;
- traceerbaarheidscontrole;
- bron- en noemertabel;
- oude-versus-actuele cijferclaims.

## Kernzin voor het antwoord op DV2

AI-gedreven documentanalyse is betrouwbaar genoeg om op corpusschaal patronen in
probleemdefinities, aanbevelingen en brede verwerking in kabinetsreacties te
meten, maar niet om zonder broncontrole precieze elementlabels, zwakke subvelden
of theoretische impactlabels als harde uitkomsten te gebruiken.

## Aandachtspunten

### 0,912 versus 0,915

Er is nog een klein verschil rond de F1-score voor probleemdefinities. De thesis
gebruikt `0,912`, terwijl de notebook mogelijk `0,915` als puntwaarde geeft.
Veilige oplossing: kies expliciet een hoofdgetal en vermeld het interval
`0,912-0,919`, of gebruik `0,912` als conservatieve ondergrens.

### 4 juni versus 5 juni

De tekst moet niet blijven spreken over alleen een notebookrun van 4 juni 2026
als de leidende bevroren bronnen op 5 juni 2026 staan. Hoofdpeildatum voor DV2:
`2026-06-05`.

### 419/13.165 versus 417/507

Deze cijfers meten niet hetzelfde:

- `419` kabinetsreactiedocumenten en `13.165` elementen horen bij de
  DV2-validatiebasis.
- `417` adviesrapporten en `507` reactiedocumenten horen bij de DV1/DV3-context.

Niet gladstrijken naar een getal. In de tekst moet duidelijk staan welk
meetniveau wordt bedoeld.

### Golden set kabinetsreactie

De kabinetsreactie-golden-set is beter te noemen als golden/silver-set, omdat de
referentie niet volledig door meerdere menselijke codeurs is gemaakt. Dit beperkt
vooral claims over volledige reproduceerbaarheid.

## Werkafspraak

Gebruik DV2 in de thesis als kwaliteitsfilter voor DV3:

- harde claims alleen op groene onderdelen;
- geaggregeerde patronen op oranje onderdelen met nuance;
- rode onderdelen alleen als verkennende context of niet gebruiken;
- losse casusclaims altijd met broncontrole.
