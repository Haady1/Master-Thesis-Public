# Retrieval-laag pilot — kabinetsreactie-matcher

Onafhankelijke grondwaarheid: advies->reactie-paren waarvoor het adviescollege
zelf het Kamerstuk als reactie publiceerde; ware doelen bestaan in de zoekpool
(corpus.officiele_publicaties).

## Resultaten (N = 69 advies)

| Metriek | Waarde | 95%-CI (Wilson) |
|---|---|---|
| precision@1 | 0.565 | (0.4479, 0.6757) |
| recall@1 | 0.565 | (0.4479, 0.6757) |
| F1 (top-1) | 0.565 | — |
| recall@3 | 0.754 | (0.6404, 0.8401) |
| recall@10 | 0.870 | (0.7703, 0.9298) |
| recall@25 | 0.884 | (0.7875, 0.9401) |
| recall@50 | 0.884 | (0.7875, 0.9401) |
| MRR | 0.675 | — |

advies met >=1 kandidaat: 69 | advies zonder kandidaat: 0

## Beperkingen (verplicht vermelden)
- Dit meet de RETRIEVAL-laag, niet de hele matcher. De VLAM-judge (beslis-poort)
  wordt apart gemeten.
- Deterministische routes (semantische pgvector-route uitgeschakeld voor snelheid):
  de gerapporteerde recall is een ONDERGRENS; de semantische route zou recall
  verhogen.
- Grondwaarheid uit college-gepubliceerde Kamerstuk-reacties: mogelijke
  selectiebias richting "nette" gevallen.
- Kleine N -> brede betrouwbaarheidsintervallen; exploratieve pilot.
