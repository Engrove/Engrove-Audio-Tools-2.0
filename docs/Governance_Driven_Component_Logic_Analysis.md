# docs/Governance_Driven_Component_Logic_Analysis.md
#
# === SYFTE & ANSVAR ===
# Detta dokument utgör en djupgående teknisk analys av hur en
# "governance-driven" arkitektur, baserad på externa JSON-regelverk, kan
# komplettera de befintliga Frankensteen-protokollen för att styra
# komponentlogik och applikationsbeteende i Engrove Audio Toolkit v2.0.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initial skapelse av Frankensteen.
#
# === TILLÄMPADE REGLER (Frankensteen v4.0) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har genererats.
# - Red Team Alter Ego: En intern granskning har säkerställt att analysen
#   är balanserad och täcker både styrkor och svagheter.


Dokument: Analys av Governance-Driven Komponentlogik för Engrove Audio Toolkit v2.0

**1. Sammanfattning och Syfte**

Denna rapport analyserar den strategiska och tekniska potentialen i att införa en governance-driven arkitektur i Engrove Audio Toolkit. Konceptet bygger på att separera "policy" (affärsregler, funktionsflaggor, UI-konfiguration) från "implementation" (Vue-komponenternas kod). Policyn definieras i externa, maskinläsbara JSON-filer, vilka konsumeras av applikationen i realtid för att styra dess beteende.

Syftet är inte att ersätta de befintliga, processorienterade Frankensteen-protokollen – som styr *hur* kod produceras för att säkerställa kvalitet – utan att komplettera dem med ett datadrivet system som styr *vad* den producerade koden gör när den körs. Detta skapar en mer flexibel, underhållbar och transparent applikation.

**2. Kärnprincip: Separation av Policy och Implementation**

Grunden för denna arkitektur är en strikt tillämpning av "Separation of Concerns".

*   **Implementation (Vue-komponenter):** Komponenterna (`.vue`-filer) ansvarar för att *rendera* ett gränssnitt och *reagera* på användarinteraktioner. De innehåller ingen hårdkodad affärslogik eller konfiguration. De är motorn.
*   **Policy (governance.json):** En eller flera centrala JSON-filer agerar som en "regelbok". De definierar villkoren, tröskelvärdena och flaggorna som styr motorns beteende.

Fördelarna med denna separation är betydande:
1.  **Flexibilitet:** Affärsregler kan ändras utan att behöva skriva om, testa och driftsätta komponentkod. En ändring i en JSON-fil kan omedelbart förändra appens funktion.
2.  **Centralisering:** Regler som är spridda över flera komponenter kan samlas på en enda, auktoritativ plats, vilket förenklar underhåll och felsökning.
3.  **Transparens och Granskbarhet:** JSON-regelverket blir ett enkelt, mänskligt läsbart dokument som exakt beskriver appens beteende, vilket är ovärderligt för både utveckling och framtida dokumentation.

**3. Konkreta Användningsfall i Engrove Audio Toolkit**

Följande sektioner beskriver hur denna princip kan appliceras direkt på projektets befintliga moduler.

**3.1 Data Explorer (Primärt Användningsfall)**

`Data Explorer`-modulen är ett idealiskt pilotprojekt. Ett `governance.json` skulle kunna styra:

*   **Funktionsflaggor:** Aktivera eller inaktivera UI-element dynamiskt.
    *   *Fil:* `ResultsDisplay.vue`, `ComparisonTray.vue`
    *   *Regel:* En boolean `features.enableCsvExport` kan visa eller dölja "Download CSV"-knappen. `features.enableComparison` kan styra hela "Jämför Korg"-funktionen.
*   **Valideringsregler:** Centralisera applikationskonstanter.
    *   *Fil:* `comparisonStore.js`
    *   *Regel:* Värdet för `COMPARISON_LIMIT` (idag hårdkodat till 5) kan hämtas från `rules.comparisonLimit`.
*   **UI-Konfiguration:** Definiera standardbeteenden för gränssnittet.
    *   *Fil:* `ResultsDisplay.vue`, `BaseTable.vue`
    *   *Regel:* En lista `ui.tonearms.defaultVisibleColumns` kan specificera vilka kolumner som ska visas som standard för tonarmar, vilket frikopplar tabellkomponenten från datatypen.

**3.2 Kalkylatorerna (Compliance & Resonance)**

Verktygens logik och visualisering kan göras mer dynamisk.

*   **Visuella Tröskelvärden:** Färgkodningen för "ideal/varning/fara"-zoner i grafer (implementeras via `Chart.js`) kan definieras centralt.
    *   *Regel:* Ett objekt `resonance.zones.warningRange: { min: 8, max: 12 }` kan styra exakt var de gröna, gula och röda fälten ritas.
*   **Standardvärden:** De initiala värdena för sliders och inmatningsfält kan konfigureras.
    *   *Regel:* `complianceEstimator.defaults.trackingForce: 1.75` kan sätta startvärdet för Tracking Force-reglaget.

**3.3 Databehandlingskedjan (Backend-skript)**

Dina Python-skript kan göras mer robusta och konfigurerbara.

*   **Statistiska Parametrar:** Tröskelvärden och konstanter i `prepare_data.py` kan externaliseras.
    *   *Regel:* `dataProcessing.ransac.minSampleSize: 5` och `dataProcessing.ransac.rSquaredThreshold: 0.95` kan styra kvaliteten på de statistiska modellerna utan att kräva ändringar i Python-koden.
*   **Datakvalitetsregler:** Hantera datanormalisering.
    *   *Regel:* En lista `dataProcessing.quality.manufacturerAliases` kan innehålla en mappning från vanliga felstavningar till korrekta tillverkarnamn.

**3.4 AR Protractor (Framtida Funktion)**

För en funktion där precision och säkerhet är avgörande är extern styrning ovärderlig.

*   **Kvalitetskrav:** Definiera minimikraven för en tillförlitlig mätning.
    *   *Regel:* `ar.calibration.requiredSamples: 20` säkerställer att kamerakalibreringen baseras på tillräckligt med data.
*   **Tröskelvärden för Gränssnittet:** Styr den realtidsfeedback användaren får.
    *   *Regel:* `ar.tracking.jitterThreshold: 0.5` kan definiera när spårningen anses "instabil" och en varning visas i HUD:en.

**4. Implementation: Steg-för-Steg Exempel (Styra CSV-Export)**

Detta visar hur man implementerar styrningen för `Data Explorer`-exportknappen.

**Steg 1: Skapa Governance-filen**
Placera denna fil i `public/data/governance.json`.
```json
{
  "version": "1.0",
  "data_explorer": {
    "features": {
      "enableCsvExport": true
    }
  }
}
```

**Steg 2: Definiera ett Schema (Rekommenderat)**
Använd ett valideringsbibliotek som `zod` för att säkerställa dataintegritet.
```javascript
// src/shared/governance/governance.schema.js
import { z } from 'zod';
export const GovernanceSchema = z.object({
  data_explorer: z.object({
    features: z.object({
      enableCsvExport: z.boolean(),
    }),
  }),
});
```

**Steg 3: Skapa en Pinia Store för Styrning**
Denna store blir den centrala bryggan mellan JSON-filen och applikationen.
```javascript
// src/entities/governance/model/governanceStore.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { GovernanceSchema } from '@/shared/governance/governance.schema';

export const useGovernanceStore = defineStore('governance', () => {
  const config = ref(null);

  async function loadGovernance() {
    try {
      const response = await fetch('/data/governance.json');
      const rawConfig = await response.json();
      const validation = GovernanceSchema.safeParse(rawConfig);
      if (validation.success) {
        config.value = validation.data;
      } else {
        console.error("Ogiltig governance.json", validation.error);
      }
    } catch (e) {
      console.error("Kunde inte ladda governance.json", e);
    }
  }

  const isCsvExportEnabled = computed(() => 
    config.value?.data_explorer?.features?.enableCsvExport ?? false
  );

  return { loadGovernance, isCsvExportEnabled };
});
```

**Steg 4: Använd i Komponent (`ResultsDisplay.vue`)**
Komponenten blir nu styrd av den externa konfigurationen.
```vue
// ... i ResultsDisplay.vue
<script setup>
import { useGovernanceStore } from '@/entities/governance/model/governanceStore';
const governanceStore = useGovernanceStore();

// Initiera storen i sidkomponenten (t.ex. onMounted i DataExplorerPage.vue)
// governanceStore.loadGovernance();
</script>

<template>
  <div class="results-header">
    <h3>...</h3>
    <BaseButton v-if="governanceStore.isCsvExportEnabled" @click="$emit('export-csv')">
      Download CSV
    </BaseButton>
  </div>
  ...
</template>
```

**5. Synergi med Frankensteen-protokollen**

Det är avgörande att förstå att dessa två system löser olika problem och därmed förstärker varandra.

| Dimension                | Governance via JSON                     | Utveckling via Frankensteen              |
|--------------------------|-----------------------------------------|------------------------------------------|
| **Fokus**                | Data-centrerad                          | Process-centrerad                        |
| **Syfte**                | Styra applikationens *runtime*-beteende | Säkerställa *utvecklings*-kvalitet        |
| **Typ av Regelverk**     | Deklarativt ("Vad ska gälla?")          | Imperativ & Proceduriell ("Hur ska det byggas?") |
| **Ändringscykel**        | Snabb (ändra JSON)                      | Metodisk (Idé -> Plan -> Kod)            |
| **Primär Granskning**    | Schema-validering (maskinell)           | "Alter Ego"-granskning (mänsklig logik)  |
| **Exempel**              | `enableCsvExport: true`                 | Regel: "API-kontraktsverifiering"        |


**6. Slutsats och Rekommendation**

Införandet av en governance-driven komponentlogik representerar nästa mognadssteg för Engrove Audio Toolkit. Det stärker applikationens flexibilitet och gör den mer robust och lättare att underhålla på lång sikt.

**Rekommenderad implementeringsplan:**
1.  **Pilotprojekt:** Börja med att implementera styrning för `Data Explorer`-modulen enligt stegen ovan. Detta är ett väl avgränsat och högst lämpligt startfall.
2.  **Expansion:** Applicera successivt konceptet på Kalkylatorerna och, när det blir aktuellt, på AR Protractor-modulen.
3.  **Formalisering:** Integrera hanteringen av `governance.json` i de befintliga styrdokumenten (`Mappstruktur_och_Arbetsflöde.md`, etc.).

Genom att kombinera den rigorösa kvaliteten från Frankensteen-processen med den dynamiska flexibiliteten hos ett externt regelverk kan projektet uppnå en exceptionellt hög nivå av både teknisk excellens och funktionell anpassningsbarhet.
```
