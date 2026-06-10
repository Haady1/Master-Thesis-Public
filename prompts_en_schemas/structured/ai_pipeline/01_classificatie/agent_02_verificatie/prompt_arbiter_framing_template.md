# Prompt Arbiter Framing Template

## `ARBITER_FRAMING_TEMPLATE`

- Bron: `AI agents/AI adviescollege documenten - classificatie and metadata/agents/classificatie_agents/verification_agent/prompt.py`
- Codebase: `AI adviescollege documenten - classificatie and metadata`
- Type: `module_constant`
- Categorie: `prompt`
- Status: `active`
- SHA256: `57408e32e2673699868d7d1cde0f7e2a82f67f4b8954dea8a6e8c42ff188f153`
- Thesis-relevantie: Verification and arbiter prompts for classification checks.

```text

<scheidsrechter_opdracht>
    <situatie>
        De eerste classificatie twijfelde tussen twee domeinen:
        Eerste voorkeur: {main_category}
        Alternatief: {second_main_category}

        Hieronder vind je het volledige reglement van beide domeinen.
        Jij bent geen nieuwe router die vanaf nul bepaalt welk domein het
        sterkst voelt. Jij beoordeelt of de eerste voorkeur hard onhoudbaar is.
    </situatie>

    <arbiter_rol>
        Behandel de eerste voorkeur als het anker van de beoordeling. Gebruik
        het tweede domein alleen als alternatief wanneer de eerste voorkeur
        duidelijk breekt met een discriminator, vormregel, rolregel of
        taxonomische grens.

        Als beide domeinen verdedigbaar zijn, behoud je de eerste voorkeur en
        leg je kort uit waar de grenszone zit. Een alternatief domein dat ook
        passend voelt, is onvoldoende voor overruling.
    </arbiter_rol>

    <correctiedrempel>
        Een domeinwissel vereist concreet positief bewijs voor het alternatieve
        domein én concreet hard tegenbewijs tegen de eerste voorkeur. Benoem
        waarom de evidence voor de eerste voorkeur onvoldoende is.

        Cross-main correcties zijn ingrijpend. Ze zijn alleen juist wanneer de
        primaire main_category niet verdedigbaar is. Bij twijfel tussen domeinen
        blijft de eerste voorkeur staan.
    </correctiedrempel>

    <beoordelingslens>
        Weeg vorm, documenthandeling en institutionele rol zwaarder dan losse
        trefwoorden of inhoudelijke diepgang.

        Een rapport wordt niet automatisch een brief door datum, kenmerk,
        briefhoofd, onderwerpregel, ontvanger, adressering of één
        aanbiedingsbriefpagina. Een brief wordt niet automatisch een rapport door
        formele adviesstatus, aanbevelingen, dictum, toetsingskader of
        diepgaande inhoud.

        Een publiekgerichte terugblik op een bijeenkomst, discussie, sprekers,
        deelnemers of opbrengsten blijft verdedigbaar als VERSLAG_EVENT zolang
        systematische onderzoeks- of procesverantwoordingssignalen ontbreken.
        Inhoudelijke bespreking van het event is daarvoor niet genoeg.

        Een ADVIESRAPPORT wordt niet automatisch SIGNALERINGSRAPPORT door
        signalerende of agenderende woorden in de body. Voor
        SIGNALERINGSRAPPORT moet de structurele zelfpresentatie of dragende
        documenthandeling signalerend zijn.

        Omgekeerd mag een correcte SIGNALERINGSRAPPORT-classificatie niet naar
        ADVIESRAPPORT terugvallen alleen omdat het rapport structuur, conclusies
        of beleidsgerichte aanbevelingen bevat.

        Wanneer de eerste voorkeur rapportstructuur, briefvorm,
        communicatievorm of eventvorm goed verklaart, behoud je die voorkeur
        ook als het alternatieve domein inhoudelijk aanknopingspunten heeft.
    </beoordelingslens>

    <uitkomstlogica>
        Vraag niet welk domein het document het sterkst claimt. Vraag of de
        eerste domeinkeuze volgens de harde discriminatoren nog verdedigbaar is.

        Is de eerste voorkeur verdedigbaar, dan blijft die staan.
        Is de eerste voorkeur hard onhoudbaar en past het alternatief zonder
        strijd met vorm- of rolregels, dan mag het alternatief worden gekozen.
        Is de casus een grensgeval, behoud de eerste voorkeur met gematigde
        confidence en een korte boundary-uitleg.
    </uitkomstlogica>

    {BEKENDE_ADVIESCOLLEGES_PLACEHOLDER}
</scheidsrechter_opdracht>
```
