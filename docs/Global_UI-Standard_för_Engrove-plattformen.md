# docs/Global_UI-Standard_för_Engrove-plattformen.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar den officiella UI-standarden för hela Engrove-plattformen.
# Det är den primära källan för designfilosofi, visuella grundstenar (design tokens)
# och övergripande interaktionsmönster som styr all UI-utveckling.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-05): Initial skapelse. Konverterad från ett ostrukturerat textdokument
#   till en formell, strukturerad Markdown-fil. All formatering, inklusive tabeller,
#   har standardiserats för maximal läsbarhet.
#
# === TILLÄMPADE REGLER (Frankensteen v3.7) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och konverterats.

# Global UI-Standard: Engrove-plattformen

## Del 1: Grundläggande Designfilosofi och Principer

Detta dokument definierar den officiella UI-standarden för hela Engrove-plattformen. Syftet är att etablera ett enhetligt, skalbart och högkvalitativt designsystem som säkerställer en konsekvent och förtroendeingivande användarupplevelse över alla moduler och funktioner. Standarden är bindande för all nyutveckling och ska fungera som den primära källan och referensen för design- och utvecklingsteam.

### 1.1 Kärnfilosofi: Precision, Tydlighet och Förtroende

Plattformens visuella och funktionella identitet bygger på tre kärnprinciper:

1.  **Precision:** Varje element i gränssnittet, från layout till minsta ikon, ska kommunicera noggrannhet och professionalism. Estetiken ska framkalla känslan av ett rent, modernt och exakt ingenjörsverktyg, en "digital arbetsbänk". Detta bygger användarens förtroende för den data och de funktioner som presenteras.
2.  **Tydlighet:** Gränssnittet måste vara intuitivt och minska den kognitiva belastningen. Komplex information ska presenteras på ett strukturerat och lättförståeligt sätt. Designen ska guida användaren, inte förvirra.
3.  **Förtroende:** Genom att vara transparenta i hur vi presenterar data och funktioner bygger vi förtroende. Detta uppnås genom verifierbarhet och en design som är ärlig och öppen med sin logik, och transformerar "svarta lådor" till transparenta "glaslådor".

Alla design- och implementationsbeslut ska utvärderas mot dessa tre principer.

### 1.2 Teknisk Arkitektur: En Modulär och Centraliserad Ansats

För att säkerställa konsekvens och underhållbarhet ska all UI-kod följa en modulär och centraliserad arkitektur.

*   **Centraliserad CSS:** Alla grundläggande stilar, design-tokens (variabler), och komponentstilar ska hanteras i en centraliserad CSS-struktur. Detta förhindrar kodduplicering och gör det enkelt att uppdatera plattformens utseende globalt. En rekommenderad struktur är att använda CSS Custom Properties för alla design-tokens.
*   **Komponentbibliotek:** Plattformen ska bygga på ett centralt bibliotek av återanvändbara UI-komponenter (t.ex. knappar, inmatningsfält, paneler). Detta garanterar att interaktiva element ser ut och beter sig likadant överallt.
*   **Centrala Hjälpfunktioner:** Gemensamma JavaScript-funktioner för formatering, validering eller beräkningar ska placeras i en central `services` eller `utils` katalog för att främja återanvändning och undvika logikspridning.

## Del 2: Visuella Grundstenar (Design Tokens)

Denna sektion definierar de atomära, visuella värden som utgör grunden för hela designsystemet. Dessa värden ska implementeras som centrala variabler (Design Tokens) i koden (t.ex. CSS Custom Properties) för att säkerställa global konsistens.

### 2.1 Typografi

Typografin är optimerad för läsbarhet, särskilt för teknisk och numerisk data.

*   **Brödtext och Gränssnittselement:** `Inter` används för all text i gränssnittet för dess höga läsbarhet.
*   **Numerisk Data och Kod:** `JetBrains Mono` används för all numerisk data i tabeller och för kodvisning för att säkerställa vertikal linjering och tydlighet.

**Tabell 2.1: Global Typografisk Skala**

| Element                 | Typsnitt        | Vikt     | Storlek (px) | Radavstånd (px) | Användning                                       |
| ----------------------- | --------------- | -------- | ------------ | --------------- | ------------------------------------------------ |
| Rubrik H1               | Inter           | Bold     | 32           | 40              | Sidans huvudtitel                                |
| Rubrik H2               | Inter           | Bold     | 24           | 32              | Sektionstitlar                                   |
| Rubrik H3               | Inter           | SemiBold | 20           | 28              | Undersektionstitlar, panelrubriker               |
| Brödtext                | Inter           | Regular  | 16           | 24              | Allmän text, beskrivningar                       |
| Etikett                 | Inter           | Medium   | 14           | 20              | Etiketter för inmatningsfält, knappar            |
| Liten Text              | Inter           | Regular  | 12           | 16              | Hjälptext, bildtexter, fotnoter                  |
| Data (Tabell)           | JetBrains Mono  | Regular  | 15           | 22              | All numerisk data i tabeller och resultatpaneler |
| Kod                     | JetBrains Mono  | Regular  | 14           | 20              | Visning av matematiska formler och kod           |

### 2.2 Färgsystem

Plattformen stödjer både ett mörkt (standard) och ett ljust tema. Färgpaletterna är funktionella och designade för klarhet och fokus. En enda accentfärg används för primära handlingar, medan en separat palett reserveras för datavisualisering i grafer.

**Tabell 2.2: Färgpalett Tokens (Mörkt Läge - Standard)**

| Token                       | HEX-kod         | Användning                                             |
| --------------------------- | --------------- | ------------------------------------------------------ |
| `$surface-primary`          | `#121212`       | Huvudsaklig bakgrundsfärg                                |
| `$surface-secondary`        | `#1E1E1E`       | Bakgrund för paneler, kort, modaler                    |
| `$surface-tertiary`         | `#2A2A2A`       | Bakgrund för inmatningsfält, element med lägre elevation |
| `$border-primary`           | `#3C3C3C`       | Primära kanter och avdelare                            |
| `$text-high-emphasis`       | `#FFFFFF` (90%) | Rubriker, viktig text                                  |
| `$text-medium-emphasis`     | `#FFFFFF` (70%) | Brödtext, etiketter                                    |
| `$text-low-emphasis`        | `#FFFFFF` (50%) | Hjälptext, inaktiva element                            |
| `$interactive-accent`       | `#3391FF`       | Knappar, länkar, aktiva kontroller, fokusindikatorer   |
| `$interactive-accent-hover` | `#58A6FF`       | Hover-status för accentfärgade element                 |
| `$graph-series-1`           | `#82AAFF`       | Första dataserien i en graf                            |
| `$graph-series-2`           | `#C39AFF`       | Andra dataserien i en graf                             |
| `$graph-series-3`           | `#79F8F8`       | Tredje dataserien i en graf                            |
| `$graph-series-4`           | `#FFCB6B`       | Fjärde dataserien i en graf                            |
| `$status-error`             | `#F44336`       | Felmeddelanden, negativa värden                        |

**Tabell 2.3: Färgpalett Tokens (Ljust Läge)**

| Token                       | HEX-kod         | Användning                                             |
| --------------------------- | --------------- | ------------------------------------------------------ |
| `$surface-primary`          | `#FFFFFF`       | Huvudsaklig bakgrundsfärg                                |
| `$surface-secondary`        | `#F5F5F5`       | Bakgrund för paneler, kort, modaler                    |
| `$surface-tertiary`         | `#EEEEEE`       | Bakgrund för inmatningsfält, element med lägre elevation |
| `$border-primary`           | `#DCDCDC`       | Primära kanter och avdelare                            |
| `$text-high-emphasis`       | `#000000` (87%) | Rubriker, viktig text                                  |
| `$text-medium-emphasis`     | `#000000` (60%) | Brödtext, etiketter                                    |
| `$text-low-emphasis`        | `#000000` (38%) | Hjälptext, inaktiva element                            |
| `$interactive-accent`       | `#007BFF`       | Knappar, länkar, aktiva kontroller, fokusindikatorer   |
| `$interactive-accent-hover` | `#0056b3`       | Hover-status för accentfärgade element                 |
| `$graph-series-1`           | `#005DFF`       | Första dataserien i en graf                            |
| `$graph-series-2`           | `#8A2BE2`       | Andra dataserien i en graf                             |
| `$graph-series-3`           | `#008B8B`       | Tredje dataserien i en graf                            |
| `$graph-series-4`           | `#E59400`       | Fjärde dataserien i en graf                            |
| `$status-error`             | `#D32F2F`       | Felmeddelanden, negativa värden                        |

### 2.3 Ikonografi

Ett enhetligt bibliotek av minimalistiska linjeikoner ska användas för att visuellt kommunicera funktioner och koncept. Alla ikoner ska dela samma stil, linjetjocklek och detaljnivå för att skapa en förutsägbar och professionell användarupplevelse.

**Principer för nya ikoner:**

*   **Stil:** Minimalistisk linjestil.
*   **Tydlighet:** Ikonen ska vara omedelbart igenkännbar och representera sin funktion.
*   **Konsekvens:** Nya ikoner måste matcha den existerande uppsättningens visuella vikt och komplexitet.

### 2.4 Layout och Grid

En konsekvent layoutstruktur och ett responsivt grid-system är avgörande för en sammanhållen plattform.

*   **Primär Layout (Stora Skärmar):** En asymmetrisk tvåkolumnslayout rekommenderas för applikationsmoduler som har en tydlig separation mellan kontroller och innehåll/visualisering. Vänster kolumn för inmatning, höger för utdata.
*   **Responsivitet (Mobila Enheter):** Layouten ska kollapsa till en enda, vertikalt scrollbar vy på mindre skärmar. En "mobile-first"-strategi ska tillämpas.
*   **Tryckytor:** Alla interaktiva element måste ha en minsta tryckyta på 44x44 pixlar för att säkerställa god användbarhet på pekskärmar.

### 2.5 UI-Densitet: Comfortable & Compact

För att tillgodose olika användarscenarier och skärmstorlekar, från fokuserad analys på en stor bildskärm till generell användning på en surfplatta, stödjer plattformen två densitetslägen:

*   **Comfortable (Standard):** Ett luftigt gränssnitt med generösa marginaler och avstånd, optimerat för maximal läsbarhet och en lugn användarupplevelse.
*   **Compact:** Ett informationstätt gränssnitt med reducerade typsnittsstorlekar och kompaktare avstånd. Detta läge är designat för avancerade användare som vill maximera mängden synlig data och minimera behovet av att scrolla.

Valet av densitet är en global användarinställning som appliceras över hela applikationen för att säkerställa en konsekvent upplevelse.

## Del 3: Komponentbibliotek och Interaktionsmönster

Denna sektion definierar hur interaktiva element ska byggas och bete sig. Alla komponenter ska vara återanvändbara och finnas i ett centralt bibliotek.

### 3.1 Komponentstatus

Varje interaktiv komponent i biblioteket måste ha väldefinierade stilar för alla sina primära tillstånd. Detta är icke förhandlingsbart och avgörande för en tillgänglig och intuitiv användarupplevelse.

*   **Default:** Komponentens grundläggande utseende.
*   **Hover:** Visuell feedback när användarens pekare är över komponenten.
*   **Focus:** En tydlig visuell markering (ofta en ram eller "glow") när komponenten är vald via tangentbordsnavigation. Detta är kritiskt för tillgänglighet.
*   **Active/Pressed:** Visuell feedback när komponenten aktiveras (t.ex. under ett musklick).
*   **Disabled:** Ett tydligt inaktivt utseende som indikerar att komponenten inte kan interageras med.

**Tabell 3.1: Exempelspecifikation för Komponentstatus (Primär Knapp, Mörkt Läge)**

| Status   | Bakgrundsfärg                 | Textfärg                 | Kant                               | Skugga                                    |
| -------- | ----------------------------- | ------------------------ | ---------------------------------- | ----------------------------------------- |
| Default  | `$interactive-accent`         | `$text-high-emphasis`    | Ingen                              | `box-shadow: 0 2px 4px rgba(0,0,0,0.2)`   |
| Hover    | `$interactive-accent-hover`   | `$text-high-emphasis`    | Ingen                              | `box-shadow: 0 4px 8px rgba(0,0,0,0.3)`   |
| Focus    | `$interactive-accent`         | `$text-high-emphasis`    | `2px solid $interactive-accent-hover` | `box-shadow: 0 2px 4px rgba(0,0,0,0.2)`   |
| Active   | `$interactive-accent`         | `$text-high-emphasis`    | Ingen                              | `box-shadow: inset 0 2px 4px rgba(0,0,0,0.2)` |
| Disabled | `$surface-tertiary`           | `$text-low-emphasis`     | Ingen                              | Ingen                                     |

*Not: En fullständig specifikation kräver liknande tabeller för alla interaktiva element (inmatningsfält, växlar, dropdowns etc.) för både mörkt och ljust läge.*

### 3.2 Globala Element

*   **Global Header:** En persistent global header ska finnas på alla sidor och innehålla applikationslogotyp, primär navigation, en länk till den globala hjälpmenyn/kunskapsbasen och temakontroller.
*   **Paneler/Kort:** Innehåll ska struktureras i paneler eller kort med en bakgrundsfärg av `$surface-secondary` för att skapa visuell hierarki och gruppering.

## Del 4: Användarstöd och Utbildning

För att maximera plattformens värde och användbarhet ska system för kontextuell hjälp och centraliserad dokumentation implementeras.

### 4.1 Kontextuella "Lärbara Stunder"

Komplexa termer eller funktioner i gränssnittet ska vara interaktiva. Vid klick ska en popover visas med en kort förklaring, och där det är lämpligt, en interaktiv animation som förklarar konceptet visuellt. Detta "just-in-time" lärande är mer effektivt än traditionella manualer.

### 4.2 Integrerad Kunskapsbas

En central, sökbar kunskapsbas ska nås från den globala headern. Den ska innehålla:

*   **Ordlista:** En komplett ordlista över alla tekniska termer som används på plattformen.
*   **Referensbibliotek:** En bibliografi över viktiga källor, forskning och standarder som plattformens funktioner bygger på.
*   **Guider och Artiklar:** Fördjupade guider för plattformens olika moduler.

Genom att konsekvent följa denna standard kommer Engrove-plattformen att uppnå en hög nivå av visuell och funktionell kvalitet, vilket stärker varumärket och skapar en överlägsen användarupplevelse.
