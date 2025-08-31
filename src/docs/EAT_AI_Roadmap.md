Absolut. Jag har skapat de två dokumenten du efterfrågade, `EAT_AI_Roadmap.md` och `EAT_AI_Source_files.md`, baserat på din specifikation och den medföljande fil-bundlen.
# Engrove Audio Tools (EAT) v2.0 - AI Roadmap

**Instruktion till AI:** Du är en expert AI-assistent specialiserad på Vue.js och Feature-Sliced Design. Detta dokument är din primära och initiala kontext för Engrove Audio Tools (EAT) v2.0-projektet. Ditt mål är att hjälpa till med utvecklingen av de planerade funktionerna som beskrivs nedan. All nödvändig källkod, JSON-scheman och semantiska kartor finns tillgängliga i den medföljande fil-bundlen; deras existens bekräftas men deras innehåll detaljeras inte här.

---

### **1. Projektöversikt & Kärnfilosofi**

EAT v2.0 är en evolution från v1.0, som var en samling separata ljudverktyg. v2.0 är en **integrerad, datadriven plattform** för audiofiler. Kärnfilosofin bygger på:
- **Arkitektur:** Strikt Feature-Sliced Design (FSD) för skalbarhet och underhåll.
- **Användarupplevelse (UX):** Fokus på en enhetlig, modern och interaktiv upplevelse med "Wow-effekter" för att lösa komplexa problem.
- **Datahantering:** Robust och centraliserad state management med väldefinierade JSON-scheman.
- **Infrastruktur:** Projektet är helt fristående och har inga beroenden till Netlify.

---

### **2. Implementerad Kärnarkitektur**

Följande grundläggande struktur är redan implementerad och funktionell i den medföljande källkoden:

- **Huvudsida (`DataExplorerPage.vue`):** En centraliserad sida som agerar nav för all datautforskning. Den integrerar widgets för filtrering och resultatvisning.
- **State Management (`/src/entities/*/model/*.js`):** Ett centraliserat state management-system med dedikerade stores, t.ex. `explorerStore.js` för datahantering och `comparisonStore.js` för att jämföra objekt.
- **UI-komponentbibliotek (`/src/shared/ui`):** En uppsättning grundläggande och återanvändbara UI-komponenter som `BaseTable`, `BaseModal`, och `BaseSelect`.
- **Feature-Sliced Design (FSD):** Källkoden är strukturerad enligt FSD med tydliga lager: `pages`, `widgets`, `features`, `entities`, och `shared`.

**Notis:** Komplett källkod (`src/`), JSON-scheman (`public/data/schemas/`) och en semantisk systemkarta (`scripts/vuemap/system_semantic_map.json`) är inkluderade i fil-bundlen.

---

### **3. Planerade Funktioner (Roadmap)**

Följande funktioner är planerade för implementation inom v2.0-arkitekturen. De ska byggas som nya `features` och/eller `widgets` och integreras i `DataExplorerPage`.

#### **3.1 Resonance Calculator**
- **Beskrivning:** Ett verktyg för att beräkna den optimala resonansfrekvensen för en tonarm/pickup-kombination för att säkerställa idealisk spårning och ljudkvalitet.
- **Inbäddad JSON (Strikt Tolkning):**
  ```json
  {
    "feature_id": "resonance_calculator",
    "type": "feature",
    "integration_target": "DataExplorerPage.vue",
    "inputs": [
      {"name": "Tonearm Effective Mass", "unit": "grams", "source": "manual_input or selected_tonearm_data"},
      {"name": "Cartridge Compliance", "unit": "cu", "source": "manual_input or selected_cartridge_data"},
      {"name": "Cartridge Weight", "unit": "grams", "source": "manual_input or selected_cartridge_data"},
      {"name": "Fastener Weight", "unit": "grams", "source": "manual_input", "default": 0.5}
    ],
    "outputs": [
      {"name": "Resonance Frequency", "unit": "Hz", "visualization": "gauge_chart (8-12 Hz is optimal)"}
    ],
    "implementation_notes": "Ska implementeras som en modal (liknande ItemDetailModal.vue) eller en dedikerad widget i DataExplorerPage. Beräkningslogiken ska isoleras i en återanvändbar 'lib'-funktion."
  }
  ```

#### **3.2 Compliance Calculator**
- **Beskrivning:** Ett verktyg för att estimera en pickups dynamiska följsamhet (compliance) baserat på kända värden för resonansfrekvens och massa.
- **Inbäddad JSON (Strikt Tolkning):**
  ```json
  {
    "feature_id": "compliance_calculator",
    "type": "feature",
    "integration_target": "DataExplorerPage.vue",
    "inputs": [
      {"name": "Tonearm Effective Mass", "unit": "grams", "source": "manual_input or selected_tonearm_data"},
      {"name": "Resonance Frequency", "unit": "Hz", "source": "manual_input"},
      {"name": "Cartridge Weight", "unit": "grams", "source": "manual_input or selected_cartridge_data"},
      {"name": "Fastener Weight", "unit": "grams", "source": "manual_input", "default": 0.5}
    ],
    "outputs": [
      {"name": "Estimated Dynamic Compliance", "unit": "cu"}
    ],
    "implementation_notes": "Liknande implementation som Resonance Calculator. Kan vara en flik i samma modal."
  }
  ```

#### **3.3 AR Protractor (Augmented Reality Alignment)**
- **Beskrivning:** En banbrytande "Wow-effekt"-funktion som använder enhetens kamera och sensorer (WebXR) för att skapa en virtuell gradskiva (protractor) för ultra-precis justering av pickupens vinkel (alignment).
- **Inbäddad JSON (Strikt Tolkning):**
  ```json
  {
    "feature_id": "ar_protractor",
    "type": "page",
    "path": "/ar-protractor",
    "dependencies": ["three.js", "WebXR API"],
    "functionality": [
      "Access device camera via WebRTC (getUserMedia).",
      "Use 'deviceorientation' events (gyroscope, accelerometer) for precise tracking of device angle.",
      "Render a 3D protractor grid (e.g., Baerwald, Lofgren A) as an overlay on the camera feed using three.js.",
      "Guide the user through a step-by-step process: positioning the phone, aligning the grid with the turntable spindle and tonearm pivot.",
      "Provide real-time visual feedback (e.g., changing colors) when the cartridge body is perfectly aligned with the grid lines at the two null points.",
      "Compensate for lens distortion if possible."
    ],
    "implementation_notes": "Detta blir en ny route och page-komponent. Kärnlogiken för AR och sensorhantering ska vara väl inkapslad. Teknisk analys finns i dokumentationen."
  }
  ```

#### **3.4 Data Explorer Expansion**
- **Beskrivning:** Utöka den nuvarande Data Explorer till att inkludera och visa data för skivspelare (turntables), tonarmar och pickuper (cartridges).
- **Inbäddad JSON (Strikt Tolkning):**
  ```json
  {
    "feature_id": "data_explorer_expansion",
    "type": "enhancement",
    "target_widgets": ["DataFilterPanel.vue", "ResultsDisplay.vue"],
    "target_stores": ["explorerStore.js"],
    "tasks": [
      "Implementera logik i 'explorerStore.js' för att hämta och hantera data för alla tre entitetstyper (turntables, tonearms, cartridges).",
      "Utöka 'DataFilterPanel.vue' med filter som är relevanta för varje entitetstyp, baserat på 'data-filters-map.schema.json'.",
      "Anpassa 'ResultsDisplay.vue' och dess `BaseTable` för att dynamiskt visa kolumner relevanta för den valda entitetstypen.",
      "Säkerställ att 'ItemDetailModal.vue' kan visa detaljerad information för alla entitetstyper."
    ],
    "data_source_note": "JSON-scheman för all data är definierade i 'public/data/schemas/'."
  }
  ```

---

### **4. Din Roll & Nästa Steg**

Din primära roll är att assistera i implementationen av ovanstående planerade funktioner. Använd den befintliga arkitekturen som grund.

För en komplett översikt över alla filer i detta projekt och deras syfte, **referera till `EAT_AI_Source_files.md`**. **Anta inte innehållet i en fil; be om att få se den explicit vid behov.**

