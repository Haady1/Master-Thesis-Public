# Thesis eindanalyse public export

Peildatum: 2026-06-05.

Deze map bevat de public-safe analysebestanden bij de eindversie van de thesis van
Haady Hassan over de zichtbare doorwerking van Kaderwet-adviescolleges. 

## Waarvoor Dit Is Gebruikt

- DV1: corpus, scope, koppelingen en dekking.
- DV2: validatie en betrouwbaarheid van de AI-documentanalyse.
- DV3: verwerking van advieselementen in kabinetsreacties.
- Verkennend binnen DV3: verschil tussen vaste, eenmalige en tijdelijke colleges.
- Matcherbijlage: retrievalprestatie van de instellingsbesluit-, advies- en
  kabinetsreactiematcher.

## Waarvoor Dit Kan Worden Gebruikt

- De tabellen uit de resultatensectie controleren.
- De gebruikte noemers en peildatum terugvinden.
- Public-safe CSV's online zetten.
- De analyse op hoofdlijnen reproduceren met notebooks en scripts.
- Controleren welke ruwe of oudere bestanden juist niet zijn gepubliceerd.

Let op: de scripts zijn bedoeld voor herkomstcontrole. Sommige scripts lezen live uit PostgreSQL of
verwachten lokale omgevingsconfiguratie. De bevroren CSV-bestanden in deze map zijn
leidend voor de gepubliceerde cijfers.

## Leidende Cijfers

- DV1: 171 collegefasen, 1.439 adviesrapporten, 1.374 extracties, 417 adviezen met
  kabinetsreactie en 507 reactiedocumenten.
- DV2: 419 kabinetsreactiedocumenten en 13.165 elementen in de validatiebasis.
- DV3: 15.368 elementen, 482 reacties en 400 adviezen.
- Parlementair spoor: canoniek 2.170 documenten en 3.332 advies-documentparen.

## Structuurboom

```text
thesis_eindanalyse_public_20260607/
|-- README.md
|   Uitleg van deze public export.
|
|-- data/
|   |-- final_csv_export_20260605/
|   |   Public-safe CSV-export met de eindtabellen voor DV1, DV2 en DV3.
|   |
|   |   |-- 00_index/
|   |   |   |-- csv_index.csv
|   |   |   |   Index van alle publieke CSV's: bronpad, deelvraag, status en uitleg.
|   |   |   |-- export_summary.csv
|   |   |   |   Samenvatting van de export en public-safe status.
|   |   |   |-- excluded_files.csv
|   |   |   |   Lijst met bestanden die bewust niet zijn gepubliceerd, met reden.
|   |   |   |-- manifest_values.csv
|   |   |       Belangrijke manifestwaarden omgezet naar CSV.
|   |
|   |   |-- 01_dv1_corpus/
|   |   |   |-- DV1_resultatentabellen_20260605.csv
|   |   |       Canonieke DV1-eindtabel: corpusfunnel, analysebasis en parlementair spoor.
|   |
|   |   |-- 02_dv2_validatie/
|   |   |   |-- 01_scope_noemers/
|   |   |   |   CSV's met DV2-noemers: adviesrapporten, kabinetsreacties en uitval.
|   |   |   |-- 02_adviesextractie_public_sanitized/
|   |   |   |   Geschoonde aanbevelingen- en probleemdefinitiebestanden.
|   |   |   |-- 03_accuratesse_validatie/
|   |   |   |   F1-scores, classificatie-accuratesse en golden-set vergelijkingen.
|   |   |   |-- 04_stabiliteit_public/
|   |   |   |   Publieke stabiliteitstabellen zonder ruwe modelredenering.
|   |   |   |-- 05_traceerbaarheid/
|   |   |   |   Traceerbaarheid en waarschuwingen bij bronverwijzingen.
|   |   |   |-- 06_college_effect/
|   |   |       Meetkwaliteit per college.
|   |
|   |   |-- 03_dv3_verwerking/
|   |       |-- verdeling_11.csv
|   |       |   DV3-verdeling over de elf originele verwerkingslabels.
|   |       |-- verdeling_6.csv
|   |       |   DV3-verdeling over zes samengevoegde klassen.
|   |       |-- verdeling_per_type_11.csv
|   |       |   Elf labels uitgesplitst naar aanbeveling en probleemdefinitie.
|   |       |-- verdeling_per_type_6.csv
|   |       |   Zes klassen uitgesplitst naar aanbeveling en probleemdefinitie.
|   |       |-- dimensie_positie.csv
|   |       |   Onderliggende kabinetspositie per elementtype.
|   |       |-- dimensie_opvolging.csv
|   |       |   Onderliggende beleidsmatige opvolging per elementtype.
|   |       |-- cramers_statistiek.csv
|   |       |   Effectgroottes, waaronder Cramer's V.
|   |       |-- gevoeligheid.csv
|   |       |   Gevoeligheidsanalyse voor vangnetcategorieen.
|   |       |-- meetkwaliteit.csv
|   |       |   Meetkwaliteit-proxy op reactieniveau.
|   |       |-- metadata_inscope.csv
|   |       |   Metadata van de DV3-analysebasis.
|   |       |-- collegetype_verdeling_6.csv
|   |           Verkennende analyse naar vast, eenmalig en tijdelijk collegetype.
|   |
|   |-- dv3_manifest/
|       |-- _manifest.json
|           Herkomst, scope, peildatum en noemers van de bevroren DV3-bundel.
|
|-- matcher_evaluatie/
|   |-- dv1_adviesmatcher/
|   |   |-- README_DV1_advies_matcher.md
|   |   |   Uitleg bij de adviesmatcher-evaluatie.
|   |   |-- 00_grondwaarheid/
|   |   |   Onafhankelijke website-grondwaarheid voor adviesrapporten.
|   |   |-- 01_aanwezigheid/
|   |   |   Aanwezigheidsscan in officiele bekendmakingen.
|   |   |-- 02_runA_deterministisch/
|   |   |   Deterministische retrievalmeting.
|   |   |-- 03_runA2_alle_routes/
|   |   |   Robuustheidscheck met alle zoekroutes.
|   |   |-- 04_runB_vlam/
|   |   |   Samenvatting van de VLAM-labelpoort.
|   |   |-- 05_scripts/
|   |       Scripts waarmee de adviesmatcher-evaluatie is opgebouwd.
|   |
|   |-- dv1_kabinetsreactie_en_instellingsbesluit/
|       |-- README.md
|       |   Uitleg bij deze matcher-evaluaties.
|       |-- DV1_instellingsbesluit_matcher_evaluatie.tex
|       |   LaTeX-fragment met instellingsbesluitmatcher-cijfers.
|       |-- DV1_kabinetsreactie_matcher_evaluatie.tex
|       |   LaTeX-fragment met kabinetsreactiematcher-cijfers.
|       |-- instellingsbesluit_data/
|       |   Compacte metrics, ranks en recall-bestanden.
|       |-- kabinetsreactie_data/
|           Compacte retrieval- en VLAM-precisionrapporten.
|
|-- notebooks/
|   |-- DV2_betrouwbaarheid_AI_documentanalyse_validatie.ipynb
|   |   Notebook voor DV2-validatie, zonder outputs.
|   |-- DV3_verwerking_advieselementen.ipynb
|       Notebook voor DV3-verwerking, zonder outputs.
|
|-- scripts/
|   |-- README.md
|   |   Uitleg dat scripts provenance zijn.
|   |-- export_dv1_corpus.py
|   |   Oudere DV1-exportscript; niet leidend voor de finale DV1-cijfers.
|   |-- export_dv2_adviesvalidatie_frozen.py
|   |   Script voor bevroren DV2-adviesvalidatie-export.
|   |-- dv2_kabinetsreactie_171_herschaling.py
|   |   Script voor DV2-kabinetsreactie-herschaling naar 171-scope.
|   |-- college_effect_meetkwaliteit.py
|   |   Script voor college-effect / meetkwaliteit.
|   |-- dv3_analyse.py
|   |   Re-runbare DV3-analyse uit PostgreSQL.
|   |-- freeze_dv3.py
|   |   Script dat de DV3-resultaten bevriest naar CSV.
|   |-- _build_dv3_notebook.py
|       Helper om het DV3-notebook op te bouwen.
|
|-- docs/
    |-- README.md
    |   Uitleg bij de documentatiebestanden.
    |-- Analyse_README.md
    |   Oudere analyse-uitleg; eind-CSV's blijven leidend.
    |-- DV1_advies_matcher_evaluatie.tex
    |   LaTeX-fragment voor de adviesmatcher.
    |-- DV2_aanpak_resultatensectie.md
    |   Werkbestand voor de DV2-resultatensectie.
    |-- DV2_meetmethoden_validatietekst.tex
    |   Tekst over DV2-meetmethoden en validatie.
    |-- DV2_resultatentekst_20260605.tex
        Resultaattekst voor DV2 op peildatum 2026-06-05.
```

## Bewust Niet Opgenomen

- `thesis/Analyse/data/dv1/**` en oude `outputs/dv1/**`, omdat die oude noemers bevatten.
- `Tweede_kamer_data/dossier_pool_artifacts/**`, omdat die ruwe tekst, fragmenten en
  modelreview bevat.
- `matcher/parlementair_v2/analyse/*.csv`, omdat die oude 2.172/3.336-aantallen bevat.
- De volledige `DV2_validatie_bronnen/**`, omdat die ruwe JSON/tekst kan bevatten.
- `DV3_verwerking_resultaattekst.tex`, omdat die superseded is en oude DV3-cijfers bevat.

## Bekende Gaten

- De definitieve DV1-SQL stond tijdens de inventarisatie nog buiten de repo:
  `C:/tmp/dv1_corpus_totalen.py`.
- De definitieve corpuskeuzes stonden tijdens de inventarisatie nog buiten de repo:
  `C:/tmp/CORPUS_KEUZES.md`.
- `dv2_niveau2_freeze.py` wordt in documentatie genoemd, maar is niet gevonden.
- De oude parlementaire export gaf 2.172 documenten / 3.336 paren. Deze map gebruikt
  het canonieke eindcijfer 2.170 documenten / 3.332 paren.

## Controle Die Is Uitgevoerd

- Alle CSV's zijn met een CSV-parser geopend.
- De 31 CSV's in `data/final_csv_export_20260605/` zijn aanwezig.
- De notebooks zijn gestript: geen celoutputs en geen execution counts.
- Er zijn geen logs, locks, caches, `.pyc`-bestanden of ruwe reviewbestanden opgenomen.
