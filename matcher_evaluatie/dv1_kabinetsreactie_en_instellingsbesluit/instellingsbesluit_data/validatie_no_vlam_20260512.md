# Validatieresultaten instellingsbesluit-matcher zonder VLAM

Deze run testte de matcher voor **bekende adviescollege-fasen**, niet de
discovery van onbekende colleges. De vraag was: als we voor elke bekende fase
zoeken naar het instellingsdocument, staat het gevalideerde juiste document dan
in de candidate pool, de top 25, of de shortlist die normaal naar VLAM gaat?

## Opzet

Datum run: 12 mei 2026

Matcher: `matcher/instellingsbesluit/run_discovery.py`

Configuratie: no-VLAM, tekstuele retrieval, heuristische reranking, geen
LLM-beoordeling.

Gold standard:

- Tabel: `matcher.instellingsbesluit_gevalideerde_links`
- Filter: alleen `link_type = 'canoniek'`
- Geaccepteerde labels: `human_geaccepteerd`, `ai_geaccepteerd`, `klopt`
- Omvang: 151 canonieke gold links over 145 adviescollege-fasen

## Berekening

Recall is berekend als:

```text
aantal gevonden gevalideerde links / totaal aantal gevalideerde links
```

Precision is berekend als:

```text
aantal correcte kandidaatparen / totaal aantal kandidaatparen
```

Accuracy is hier niet gebruikt als klassieke classificatie-accuracy, omdat dit
een retrievaltaak is zonder volledige negatieve set. Daarom is accuracy
gerapporteerd als **fase-level top-k hit rate**:

```text
aandeel adviescollege-fasen waarvoor minstens een correct canoniek document in de top-k of VLAM-shortlist zit
```

## Hoofdresultaten

| Metriek | Resultaat |
|---|---:|
| Candidate pool recall | 119/151 = 0.788 |
| Top-25 recall | 118/151 = 0.781 |
| VLAM-shortlist recall | 117/151 = 0.775 |
| Fase-level top-25 accuracy | 115/145 = 0.793 |
| Fase-level VLAM-shortlist accuracy | 115/145 = 0.793 |
| Precision alle kandidaten | 119/5532 = 0.0215 |
| Precision@25 | 118/3480 = 0.0339 |
| Precision VLAM-shortlist | 117/2063 = 0.0567 |

## Per categorie: recall in VLAM-shortlist

| Categorie | Recall |
|---|---:|
| Eenmalig | 84/96 = 0.875 |
| Tijdelijk | 11/15 = 0.733 |
| Permanent | 22/40 = 0.550 |
| Totaal | 117/151 = 0.775 |

## Interpretatie

De matcher functioneert in deze configuratie vooral als **high-recall
kandidaatgenerator**. Dat betekent dat hij veel mogelijke documenten ophaalt en
rangschikt, waarna VLAM of menselijke validatie de definitieve beslissing neemt.

De lage precision is daarom verwacht: de matcher haalt bewust veel kandidaten
op om de kans te vergroten dat het juiste document in de shortlist zit. Voor
een wetenschappelijke beschrijving is recall hier belangrijker dan raw
precision, omdat de matcher niet als autonome eindclassificator is gebruikt.

## Belangrijke kanttekeningen

1. De resultaten gelden voor bekende adviescollege-fasen, niet voor onbekende
   colleges.
2. De gold standard bestaat uit eerder gevalideerde canonieke links; fouten of
   lacunes daarin werken door in de evaluatie.
3. Permanente adviescolleges presteren duidelijk zwakker dan tijdelijke en
   eenmalige colleges. Waarschijnlijk komt dit doordat permanente colleges
   vaker via wetten, oudere Staatsblad-documenten of bredere wettelijke kaders
   zijn ingesteld.
4. De top-25 en VLAM-shortlist zijn retrieval-/rankingmaten. Ze zeggen niet dat
   het systeem zelfstandig het juiste document kiest, maar dat het juiste
   document beschikbaar is voor downstream beoordeling.
5. Klassieke accuracy is hier methodologisch minder geschikt, omdat er geen
   uitputtende set negatieve college-documentparen is vastgesteld.

## Mogelijke formulering voor paper

In a no-LLM validation run, the instellingsbesluit matcher retrieved candidate
establishment documents for known advisory body phases and was evaluated
against 151 manually validated canonical links. The correct canonical document
was present in the full candidate pool for 78.8% of gold links and in the VLAM
review shortlist for 77.5%. At the advisory-body-phase level, at least one
correct canonical document was present in the top-25 candidates for 79.3% of
validated phases. Precision was low, as expected for a high-recall retrieval
stage, with 5.7% of VLAM-shortlisted candidate pairs corresponding to validated
canonical links. The matcher should therefore be interpreted as a
recall-oriented candidate generation component rather than as an autonomous
final classifier.
