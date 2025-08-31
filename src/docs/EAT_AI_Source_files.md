# EAT AI Source File Manifest

Detta dokument är en komplett förteckning över alla filer som är inkluderade i denna file_bundle. Syftet är att ge dig en översikt över tillgängliga resurser. **Instruktion: Fråga efter en specifik fil via dess sökväg (t.ex. "Visa mig `src/pages/data-explorer/DataExplorerPage.vue`") när du behöver detaljerad information. Gör inga antaganden om filernas innehåll.**

---

### **`docs/` - Dokumentation**
*   `AR_Protractor_Förbättrad_Precision.md`: Detaljerad beskrivning av hur AR-funktionen använder enhetssensorer för att uppnå högre precision än analoga metoder.
*   `AR_Protractor_Teknisk_Analys.md`: Djupgående teknisk analys av AR Protractor, inklusive sensor-datafusion, precisionskrav och UX-utmaningar.
*   `AR_Protractor_Teknisk_Dokumentation.md`: Teknisk specifikation för AR Protractor-funktionen, avsedd som underlag för implementation.
*   `Engrove_Audio_Toolkit_v2.0_Analys.md`: En omfattande analys av hela v2.0-projektets arkitektur, designval och tekniska implementation.
*   `Global_UI-Standard_för_Engrove-plattformen.md`: Beskriver de övergripande UI/UX-principerna, design-tokens (färger, typografi) och den visuella identiteten.
*   `Global_UI-Standard_Komponentspecifikation.md`: Detaljerad specifikation för varje `Base` UI-komponent i `/src/shared/ui`.
*   `HomePage_Tekniska_Detaljer.md`: Teknisk beskrivning av hemsidans (`HomePage.vue`) interaktiva element.
*   `Product_Roadmap.md`: Den övergripande produktvisionen och roadmapen.
*   `Teknisk_Beskrivning_Engrove_Audio_Toolkit.md`: En högnivå teknisk översikt av projektet.
*   `Wow_Effekten_och_UX_Strategi.md`: Beskriver strategin för att skapa "Wow-effekter" (som AR Protractor) för att engagera användaren.

### **`public/` - Publika Resurser**
*   `_headers`, `_routes.json`: Konfigurationsfiler.
*   `data/schemas/*.schema.json`: **Kritiska filer.** Innehåller JSON Schema-definitioner för all data, inklusive `cartridges-data`, `tonearms-data`, `data-filters-map` och `data-translation-map`. Dessa styr datastruktur och filterlogik.
*   `images/*.webp`: Bildresurser för applikationen.

### **`scripts/vuemap/` - Skript & Analysverktyg**
*   `system_semantic_map.json`: En detaljerad semantisk karta över hela Vue-projektet. Definierar komponentrelationer, databeroenden och arkitektoniska regler. **Mycket viktig för att förstå kodbasen.**

### **`src/` - Källkod**

#### `src/app/` - Applikations-lager
*   `main.js`: Applikationens startpunkt (entrypoint). Initialiserar Vue, router, och globala stores.
*   `router.js`: Definierar applikationens routes (`/`, `/about`, `/explorer`, `/license`).
*   `styles/*.css`: Globala CSS-filer och design-tokens.

#### `src/pages/` - Sid-lager
*   `AboutPage.vue`: Sidan "Om oss".
*   `DataExplorerPage.vue`: **Huvudsida.** Integrerar alla kärnkomponenter för datautforskning (`DataFilterPanel`, `ResultsDisplay`, `ComparisonTray`).
*   `HomePage.vue`: Applikationens landningssida.
*   `LicensePage.vue`: Sida för att visa licensinformation.

#### `src/widgets/` - Widget-lager
*   `ComparisonTray/ComparisonTray.vue`: UI-widget som visar valda objekt för jämförelse. Använder `comparisonStore`.
*   `DataFilterPanel/DataFilterPanel.vue`: UI-widget som innehåller alla filter (`BaseSelect`, `RangeFilter`, etc.) för att manipulera data i `explorerStore`.
*   `GlobalFooter.vue`, `GlobalHeader.vue`, `MobileNavMenu.vue`: UI-widgets för global layout och navigation.
*   `ResultsDisplay/ResultsDisplay.vue`: UI-widget som visar filtrerad data i en `BaseTable`.

#### `src/features/` - Funktions-lager
*   `comparison-modal/ComparisonModal.vue`: Modal för att visa en detaljerad jämförelse av två objekt.
*   `item-details/ItemDetailModal.vue`: Modal för att visa all detaljerad information om ett enskilt dataobjekt.
*   `*-toggle/`: Funktioner för att växla teman, täthet i tabeller, och mobilmeny.

#### `src/entities/` - Entitets-lager
*   `comparison/model/comparisonStore.js`: State management för jämförelse-funktionen.
*   `data-explorer/api/fetchExplorerData.js`: Funktion för att hämta datan från JSON-filer.
*   `data-explorer/lib/*.js`: Hjälpfunktioner för filtrering och datatransformation.
*   `data-explorer/model/explorerStore.js`: **Kärn-store.** Hanterar all state relaterad till data, filter, sortering och paginering.
*   `logger/model/loggerStore.js`: State management för ett internt loggningssystem.
*   `settings/model/settingsStore.js`: State management för användarinställningar.
*   `theme/model/themeStore.js`: State management för applikationens tema (ljus/mörk).

#### `src/shared/ui/` - Delat UI-lager
*   `Base*.vue`: En samling av grundläggande, återanvändbara och "dumma" UI-komponenter som utgör grunden för applikationens gränssnitt (t.ex. `BaseButton.vue`, `BaseTable.vue`, `BaseModal.vue`).

