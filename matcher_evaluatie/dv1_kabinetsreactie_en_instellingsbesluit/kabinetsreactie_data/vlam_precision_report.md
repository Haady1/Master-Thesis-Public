# VLAM-poort pilot — kabinetsreactie-matcher (Deel B)

De VLAM-judge is over de ECHTE opgehaalde top-10 shortlists van de retrieval-pilot
gedraaid (de afleiders zijn dus wat de matcher zelf voorstelde). Grondwaarheid:
advies->reactie-paren waarvoor het adviescollege zelf het Kamerstuk publiceerde.

## Resultaten (N = 69 advies; 505 kandidaten beoordeeld)

| Metriek | Waarde | 95%-CI |
|---|---|---|
| VLAM-precision (geaccepteerd correct) | 0.635 | (0.5357, 0.7248) (Wilson) |
| VLAM-recall (naald in shortlist) | 0.968 | (0.8914, 0.9913) (Wilson) |
| End-to-end matcher-recall | 0.812 | (0.7039, 0.8865) (Wilson) |
| F1 (precision x end-to-end recall) | 0.713 | [0.6329, 0.7938] (bootstrap) |

Geaccepteerd (primair): 96 | waarvan correct: 61
Advies met naald in shortlist (plafond end-to-end): 57 / 69

CI-methode: precision/recall via Wilson (enkele proportie); F1 via cluster-bootstrap
over advies (10000 herhalingen, seed 42),
omdat F1 geen enkele proportie is en uit twee verschillende noemers komt. Ter
vergelijking geeft dezelfde bootstrap voor precision [0.5431, 0.7416]
en voor end-to-end recall [0.7101, 0.8986].

### Strikte accept-variant (gevoeligheidscheck)
is_response_to_advice EN has_substantive_advice_handling:
precision = 0.635 (0.5357, 0.7248) ;
end-to-end recall = 0.812
(geaccepteerd 96, correct 61)

### Verdict-verdeling
{
  "valid_response_match": 96,
  "not_response_document": 167,
  "response_to_other_advice": 242
}

### Schijnbare false positives per verdict
{
  "valid_response_match": 35
}

## Beperkingen (verplicht vermelden)
- VLAM-precision is een ONDERGRENS: de grondwaarheid kent alleen de
  college-gepubliceerde reactie. Accepteert VLAM een andere, feitelijk juiste
  reactie, dan telt dat hier onterecht als false positive. Controleer de
  schijnbare false positives in per_kandidaat.csv handmatig.
- End-to-end recall is begrensd door de retrieval-laag (deterministische routes =
  ondergrens; semantische route stond uit). Plafond = advies met naald in shortlist.
- Eenmalige VLAM-run; labels zijn niet volledig reproduceerbaar (bekend
  pipeline-nondeterminisme) -> exploratief, kleine N, brede CI's.
- College-website-grondwaarheid = mogelijke selectiebias richting "nette" gevallen.
