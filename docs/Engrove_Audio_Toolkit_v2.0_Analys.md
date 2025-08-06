# docs/Engrove_Audio_Toolkit_v2.0_Analys.md
#
# === SYFTE & ANSVAR ===
# Detta dokument tillhandahåller en komplett teknisk och strategisk analys av
# Engrove Audio Toolkit v2.0-projektet. Det utvärderar kärnstacken, arkitekturen,
# databehandling, designsystem och UI/UX.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initial skapelse. Konverterad från ett ostrukturerat textdokument
#   till en formell, strukturerad Markdown-fil.
#
# === TILLÄMPADE REGLER (Frankensteen v3.8) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och konverterats.

# Rapport: Teknisk och Strategisk Analys av Engrove Audio Toolkit v2.0

## Analys av Teknisk Arkitektur och Stack

Denna sektion utvärderar de grundläggande tekniska val som utgör ryggraden i Engrove Audio Toolkit v2.0. Dessa val är avgörande för projektets prestanda, underhållbarhet och framtida skalbarhet. Analysen omfattar den valda kärnstacken, den övergripande mjukvaruarkitekturen och strategierna för databehandling.

### Utvärdering av Kärnstacken (Vite, Vue 3, Pinia)

Projektet är baserat på en modern och högpresterande frontend-stack bestående av `Vite` som byggverktyg, `Vue.js 3` som JavaScript-ramverk, `Vue Router` för navigering och `Pinia` för statushantering. Detta val av teknologier bedöms vara exceptionellt väl lämpat för projektets ändamål.

**Fördelar med den valda stacken:**
*   **Prestanda och Utvecklingsupplevelse:** `Vite` erbjuder en nästintill omedelbar start av utvecklingsservern och Hot Module Replacement (HMR), vilket maximerar utvecklingseffektiviteten. För produktion skapar `Vite` en högt optimerad och trädskakad (tree-shaken) kodbas, vilket är kritiskt för en webbapplikation som måste ladda snabbt trots tunga beroenden som `OpenCV.js`.
*   **Komponentbaserad logik:** `Vue.js 3`, och specifikt användningen av Composition API med `<script setup>`, är idealiskt för att bygga komplexa och reaktiva gränssnitt. I ett dataintensivt projekt som detta, med interaktiva kalkylatorer och realtidsvisualiseringar, möjliggör Composition API en logisk och återanvändbar strukturering av kod inom varje komponent. Detta förhindrar att komponenter blir ohanterligt stora och svåra att underhålla.
*   **Centraliserad Statushantering:** `Pinia`, som den officiella efterföljaren till Vuex, är en avgörande komponent. Det agerar som en central "sanningskälla" (single source of truth) för hela applikationen. Detta är nödvändigt för att synkronisera data mellan disparata delar av gränssnittet, såsom en inmatningspanel, en resultatgraf och ett AR-overlay. Användningen av `pinia-plugin-persistedstate` för att spara användarinmatningar i `localStorage` är en genomtänkt detalj som avsevärt förbättrar användarupplevelsen genom att bevara tillståndet mellan sessioner.

Valet av denna kärnstack representerar mer än bara ett tekniskt beslut; det är en strategisk riskspridning. Projektets absolut största tekniska risk och utmaning ligger i AR-funktionaliteten och dess krav på precision. Genom att bygga resten av applikationen – gränssnitt, datalogik, navigering – på en extremt stabil, väldokumenterad och modern standardstack, har projektet effektivt minimerat riskerna i en stor majoritet av sin kodbas. Detta frigör utvecklingsresurser och mentalt fokus till att kunna hantera den verkliga kärnutmaningen: att få datorseendet att fungera så robust som möjligt i en webbläsarmiljö. Stacken fungerar därmed som en stabil grund som de-riskar projektet som helhet.

### Analys av Arkitektur och Mappstruktur (Feature-Sliced Design)

Projektet har anammat en rigorös, hypergranulär mappstruktur som är starkt inspirerad av arkitekturmetodiken "Feature-Sliced Design" (FSD). Denna struktur delar upp applikationskoden i tydligt definierade lager (`layers`) och skivor (`slices`):
*   **Layers:** `pages`, `widgets`, `features`, `entities`, `shared`
*   **Slices:** Varje affärsdomän, som `ar-protractor` eller `theme-toggle`, utgör en egen "skiva" inom dessa lager.

Denna arkitektur är en av projektets största styrkor. FSD tvingar fram en design med extremt låg koppling (`low coupling`) och hög sammanhållning (`high cohesion`). Genom att strikt isolera "verb" (användarinteraktioner i features) från "substantiv" (data och affärsobjekt i entities) blir varje del av koden enklare att förstå, testa och underhålla oberoende av andra delar.

För det uttalade målet att använda ett AI-centrerat arbetsflöde är denna struktur exceptionellt väl lämpad. Den extrema granulariteten, som demonstreras i exemplet med funktionen "Nollställ Beräkning", minskar det kontextfönster som en AI-assistent behöver för varje enskild uppgift. Detta minimerar risken för felaktiga antaganden ("hallucinationer") och gör det möjligt att formulera extremt precisa och avgränsade instruktioner, vilket ökar träffsäkerheten och kvaliteten i den genererade koden.

Utöver de omedelbara fördelarna för kodkvalitet och AI-samarbete, fungerar denna arkitektur som en kraftfull mekanism för att framtidssäkra projektet, särskilt med tanke på dess natur som ett icke-kommersiellt hobbyprojekt. Hobbyprojekt lider ofta av att de blir svåra att återuppta efter en tids paus; kunskap om kodbasen eroderar och strukturen blir oöverskådlig. Den strikta FSD-strukturen motverkar detta genom att fungera som en form av levande, självupprätthållande dokumentation. En utvecklare, vare sig det är den ursprungliga skaparen eller en ny bidragsgivare från communityn, kan snabbt förstå en specifik funktions ansvarsområden och beroenden enbart genom att inspektera dess plats i mappstrukturen. Detta sänker tröskeln för att bidra till projektet via GitHub och ökar därmed dramatiskt dess långsiktiga överlevnadschanser och hållbarhet. Arkitekturen är således inte bara en teknisk finess, utan en strategisk investering i projektets livslängd.

### Analys av Databehandling och Visualisering

Projektets hantering av data och dess visualisering är genomtänkt och optimerad för prestanda och tydlighet.
*   **Datakällor:** All primärdata, såsom specifikationer för tonarmar och pickuper, lagras i statiska JSON-filer. Detta är en effektiv och robust strategi för en statisk webbplats (SSG), då det eliminerar behovet av en extern databas och tillhörande komplexitet och kostnader.
*   **Offline-analys:** En av de mest intelligenta arkitektoniska lösningarna är att flytta tunga beräkningar från klienten till en offline-process. Genom att använda Python-skript med bibliotek som `pandas` och `scikit-learn` för att utföra regressionsanalys och generera färdiga "estimationsregler", avlastas användarens webbläsare helt. Detta säkerställer att estimeringsverktygen i applikationen kan leverera resultat omedelbart, vilket är avgörande för en god användarupplevelse.
*   **Datavisualisering:** `Chart.js` är ett beprövat och flexibelt bibliotek för att rendera grafer. Det specifika valet att använda `chartjs-plugin-annotation` för att visuellt rendera "ideal/varning/fara"-zoner i bakgrunden på grafer är ett utmärkt exempel på hur tekniska val direkt stödjer den övergripande designfilosofin om "Tydlighet" och "Förtroende". Detta omvandlar rådata till lättolkad, handlingsbar information för användaren.

## Utvärdering av Designsystem och UI/UX

Denna sektion granskar den visuella och interaktiva grund som definierar användarens upplevelse och förtroende för verktyget. Ett robust designsystem är avgörande för att uppnå projektets kärnfilosofi om "Precision, Tydlighet och Förtroende".

### Bedömning av Befintlig UI-Standard och Komponentspecifikation

Projektet uppvisar en exceptionellt hög mognadsgrad i sin definition av designsystemet. Den Globala UI-Standarden och den Fullständiga Komponentspecifikationen är uttömmande, rigorösa och av en kvalitet som sällan ses ens i storskaliga kommersiella projekt.

**Styrkor i det befintliga systemet:**
*   **Filosofisk förankring:** Designsystemet är inte bara en samling stilar, utan är förankrat i en tydlig filosofi om "Precision, Tydlighet och Förtroende". Detta ger en stark ledstjärna för alla framtida designbeslut.
*   **Rigorös detaljnivå:** Specifikationen av atomära design-tokens för typografi och färg (för både mörkt och ljust läge) är komplett och välstrukturerad. Valet av typsnitt är särskilt träffsäkert: Inter för maximal läsbarhet i gränssnittet och JetBrains Mono för all numerisk data, vilket säkerställer vertikal linjering och förstärker känslan av ett precisionsverktyg.
*   **Fullständiga interaktionstillstånd:** Den mest imponerande aspekten är den tabellbaserade definitionen av alla interaktionstillstånd (Default, Hover, Focus, Active, Disabled) för varje baskomponent. Detta är icke-trivialt och absolut avgörande för att skapa ett tillgängligt och intuitivt gränssnitt som inger förtroende. Särskilt den tydliga definitionen av `Focus`-tillståndet visar på en stark förståelse för tillgänglighetskrav (`a11y`).

Sammantaget utgör det existerande designsystemet den mest robusta och färdigutvecklade delen av projektet. Det minimerar risker relaterade till UI/UX och skapar en solid grund för all vidare utveckling.

### Rekommenderade Kompletteringar: Detaljerade Specifikationer

Medan de grundläggande, atomära komponenterna är exemplariskt definierade, saknas motsvarande specifikationer för mer komplexa, sammansatta element som är centrala för applikationens kärnfunktioner. För att bibehålla den extremt höga standarden och säkerställa visuell och funktionell konsekvens, rekommenderas att följande komponenter specificeras med samma rigorösa detaljnivå som i den befintliga dokumentationen.
Nedan följer förslag på specifikationstabeller som kan integreras direkt i projektets UI-standard.

**Tabell 2.1: Specifikation för Datatabeller (`shared/ui/BaseTable.vue`)**

Datatabeller kommer att vara en central komponent för att presentera jämförande data, exempelvis i "Data Explorer"-modulen. En standardiserad tabellkomponent är nödvändig för konsekvens.

| Attribut       | Specifikation (Mörkt Läge)                                  | Specifikation (Ljust Läge)                                  | Design Token / Regel |
| :------------- | :---------------------------------------------------------- | :---------------------------------------------------------- | :------------------- |
| Struktur       | `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`                 | `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`                 | Semantisk HTML5      |
| Panelbakgrund  | `$surface-secondary`                                        | `$surface-secondary`                                        | `background-color`   |
| Rubrikbakgrund (`<th>`) | `$surface-tertiary`                                         | `$surface-tertiary`                                         | `background-color`   |
| Rubriktext (`<th>`)   | `$text-high-emphasis`, Inter, Medium, 14px                | `$text-high-emphasis`, Inter, Medium, 14px                | Typografisk skala    |
| Raddata (`<td>`)      | `$text-medium-emphasis`, JetBrains Mono, Regular, 15px    | `$text-medium-emphasis`, JetBrains Mono, Regular, 15px    | Typografisk skala    |
| Kantlinje (rad) | 1px solid `$border-primary`                                 | 1px solid `$border-primary`                                 | `border-bottom`      |
| Rad-hover (`<tr>:hover`) | Bakgrund: `$surface-tertiary`                               | Bakgrund: `$surface-tertiary`                               | `background-color`   |
| Sorteringsikon (`<th>`) | SVG-ikon, färg: `$interactive-accent`                       | SVG-ikon, färg: `$interactive-accent`                       | Visas vid aktiv sortering |

**Tabell 2.2: Specifikation för Grafer (`shared/ui/BaseChart.vue`)**

Grafer är den primära metoden för att visualisera komplexa relationer som resonans och spårningsfel. En standardiserad wrapper-komponent för `Chart.js` säkerställer visuell enhetlighet.

| Attribut     | Specifikation (Mörkt Läge)                        | Specifikation (Ljust Läge)                        | Design Token / Regel        |
| :----------- | :------------------------------------------------ | :------------------------------------------------ | :-------------------------- |
| Dataserier   | `$graph-series-1`, `$graph-series-2`, etc.        | `$graph-series-1`, `$graph-series-2`, etc.        | `borderColor`, `backgroundColor` |
| Axlar & Grid | Linjefärg: `$border-primary` (låg opacitet)     | Linjefärg: `$border-primary` (låg opacitet)     | `grid.color`, `ticks.color` |
| Etiketter (ticks) | Textfärg: `$text-low-emphasis`, Inter, 12px     | Textfärg: `$text-low-emphasis`, Inter, 12px     | `ticks.font`                |
| Tooltip (hover) | Bakgrund: `$surface-tertiary`, Text: `$text-high-emphasis` | Bakgrund: `$surface-tertiary`, Text: `$text-high-emphasis` | `tooltip.backgroundColor`   |
| Annotationer | Bakgrund: `$status-error` etc. med 10% opacitet | Bakgrund: `$status-error` etc. med 10% opacitet | `chartjs-plugin-annotation` |

**Tabell 2.3: Specifikation för AR Heads-Up Display (HUD)**

Detta är den mest kritiska nya UI-specifikationen, då den utgör realtidsgränssnittet till projektets kärninnovation. Tydlighet och precision är avgörande för användbarhet och förtroende.

| Element         | Specifikation (Gemensam för båda teman)               | Design Token / Regel                  | Syfte                                   |
| :-------------- | :---------------------------------------------------- | :------------------------------------ | :-------------------------------------- |
| Layout          | Hörnplacerade paneler för att maximera synfältet      | CSS `position: fixed`                 | Minimera störning av kameravyn          |
| Panelbakgrund   | `rgba(18, 18, 18, 0.7)` (`$surface-primary` med transparens) | `background-color` med `backdrop-filter: blur(4px)` | Läsbarhet mot rörig bakgrund          |
| Primärdata      | JetBrains Mono, Bold, 28px, `$text-high-emphasis`     | Ex: Spårningsfel: 1.75°               | Fokus på det viktigaste mätvärdet       |
| Sekundärdata    | JetBrains Mono, Regular, 18px, `$text-medium-emphasis` | Ex: S2P: 215.4 mm                     | Stödjande mätvärden                     |
| Statusindikator | Inter, Medium, 14px, Färg varierar (grön/gul/röd)     | Ex: Spårning: Stabil                  | Omedelbar feedback på mätningskvalitet  |
| Osäkerhetsvärde | JetBrains Mono, Regular, 14px, `$text-low-emphasis`   | Ex: (±0.5 mm)                         | Bygger förtroende genom transparens     |
| Instruktionstext | Inter, Regular, 16px, `$text-high-emphasis`           | Ex: Flytta kameran närmare            | Guidar användaren i realtid             |

**Tabell 2.4: Specifikation för Aviseringar (Modaler & Toasts)**

Ett standardiserat system för aviseringar krävs för att kommunicera status, fel och bekräftelser till användaren.

| Komponent        | Attribut    | Specifikation (Mörkt Läge)                                | Specifikation (Ljust Läge)                                | Design Token / Regel          |
| :--------------- | :---------- | :-------------------------------------------------------- | :-------------------------------------------------------- | :---------------------------- |
| Modal (Dialog)   | Overlay     | `rgba(0, 0, 0, 0.6)`                                      | `rgba(0, 0, 0, 0.4)`                                      | `background-color`            |
|                  | Panel       | Bakgrund: `$surface-secondary`, Skugga: large           | Bakgrund: `$surface-secondary`, Skugga: large           | `box-shadow`                  |
|                  | Rubrik      | Inter, SemiBold, 20px, `$text-high-emphasis`              | Inter, SemiBold, 20px, `$text-high-emphasis`              | Typografisk skala             |
|                  | Knappar     | Använder BaseButton-komponenter                           | Använder BaseButton-komponenter                           | Återanvändning av komponent   |
| Toast (Notis)    | Position    | bottom-center eller top-right                             | bottom-center eller top-right                             | `position: fixed`             |
|                  | Bakgrund (Fel) | `$status-error`                                           | `$status-error`                                           | `background-color`            |
|                  | Bakgrund (Info) | `$interactive-accent`                                     | `$interactive-accent`                                     | `background-color`            |
|                  | Text        | Inter, Medium, 14px, `$text-high-emphasis`                | Inter, Medium, 14px, `$surface-primary`                   | Typografisk skala             |
|                  | Animation   | fade-in-out, slide-up-down                                | fade-in-out, slide-up-down                                | `transition`, `transform`     |

## Analys av AR-koncept och Datorseende

Denna sektion utgör en kritisk granskning av projektets mest innovativa och tekniskt utmanande del: den webbläsarbaserade AR-protractorn. Analysen fokuserar på genomförbarheten av att uppnå hög precision med den valda tekniska lösningen.

### Den Centrala Utmaningen: Högprecision i Webbläsaren

Projektets uttalade mål är att erbjuda "högsta möjliga precision" vid justering av skivspelare med hjälp av en AR-lösning baserad på `AR.js` och `OpenCV.js`. Detta ambitiösa mål stöter på en fundamental teknisk konflikt med de kända begränsningarna hos webbaserad AR (WebAR).

Forskning och branschpraxis visar konsekvent att WebAR-lösningar, särskilt de som likt `AR.js` inte bygger på de senaste plattformsspecifika AR-ramverken, har betydande nackdelar jämfört med native-applikationer när det gäller prestanda, stabilitet och precision. Bibliotek som `AR.js` kör sin datorseende-logik i JavaScript, vilket är mindre effektivt än den native-kod som används i ramverk som ARKit (Apple) och ARCore (Google). Detta kan leda till lägre bildfrekvens (FPS), högre latens och "jitter" (darrningar) i spårningen, vilket direkt påverkar mätnoggrannheten. Att uppnå en verifierbar millimeter-noggrannhet under dessa förutsättningar är extremt osannolikt.

Detta väcker en viktig fråga om projektets tekniska vägval. Den moderna standarden för högpresterande AR på webben är WebXR Device API. Denna API ger webbläsaren direktare tillgång till enhetens underliggande SLAM-funktioner (Simultaneous Localization and Mapping), vilket ger en betydligt mer stabil och exakt spårning. Problemet är att stödet för WebXR är fragmenterat; det fungerar väl på Android/Chrome men saknar i praktiken stöd på iOS/Safari, vilket utestänger en stor del av mobilmarknaden.

`AR.js`, å andra sidan, är byggt på äldre men mer universella webbteknologier som WebGL och WebRTC. Detta ger biblioteket en avgörande fördel: det fungerar på i stort sett alla moderna webbläsare som har kameratillgång, inklusive Safari på iOS. Projektets val av `AR.js` kan därför tolkas inte som ett tekniskt förbiseende, utan som ett medvetet och pragmatiskt strategiskt beslut. Man har prioriterat maximal räckvidd och tillgänglighet (att inkludera alla smartphone-användare) på bekostnad av maximal potentiell precision (som WebXR på Android skulle kunna erbjuda).

**Rekommendation:** Projektets mål bör omformuleras från det absoluta "millimeterexakt" till ett mer realistiskt och ärligt mål, såsom "att erbjuda högsta möjliga precision med webbaserad teknik". Den strategiska tyngdpunkten bör flyttas från att uppnå en omöjlig exakthet till att på ett transparent sätt kvantifiera och kommunicera systemets inneboende osäkerhet till användaren.

### Kritisk Sökväg: Kamerakalibrering med `OpenCV.js`

För att överhuvudtaget kunna närma sig hög noggrannhet är en robust kamerakalibrering inte valfri, utan absolut nödvändig. Varje kameralins introducerar optiska förvrängningar (distorsion), främst radiell (fiskögeeffekt) och tangentiell distorsion. Utan att matematiskt korrigera för dessa fel kommer alla positions- och vinkelberäkningar som görs från kamerabilden att vara systematiskt felaktiga.

`OpenCV.js` tillhandahåller de nödvändiga funktionerna för detta, främst `cv.calibrateCamera()`. Processen involverar att fotografera ett känt mönster, vanligtvis ett schackbräde, från ett flertal olika vinklar och avstånd. Genom att jämföra de kända 3D-koordinaterna för mönstrets hörn med deras observerade 2D-pixelpositioner i bilderna, kan algoritmen beräkna kamerans interna matris (brännvidd, optiskt centrum) och en uppsättning distortionskoefficienter (`k1, k2, p1, p2, k3`). Dessa koefficienter kan sedan användas för att "räta ut" varje bildram innan AR-spårningen sker.

Projektets "Scale & Stability Anchor"-markör är med sin schackbrädesdesign perfekt utformad för just detta ändamål, då den är direkt kompatibel med OpenCV:s inbyggda funktion `cv.findChessboardCorners()`.

Den största utmaningen med kalibrering är dock inte den tekniska implementationen, utan användarupplevelsen. En korrekt kalibrering kräver att användaren tar ett tiotal högkvalitativa bilder av schackbrädet från varierande och ibland kontraintuitiva vinklar för att säkerställa att algoritmen får tillräckligt med data för att lösa ekvationssystemet. Detta är en komplex, abstrakt och potentiellt frustrerande uppgift.

Därför är den verkliga kritiska sökvägen för projektet inte att skriva koden för `cv.calibrateCamera()`, utan att designa ett guidat, interaktivt och felsäkert användargränssnitt för kalibreringsprocessen. Detta gränssnitt måste ge användaren kontinuerlig, handlingsbar feedback i realtid, såsom:
*   "Bra bild! 3 av 10 tagna."
*   "Vinkla mönstret mer åt vänster."
*   "Flytta kameran längre bort från mönstret."
*   "Bilden är för suddig, försök igen."

Framgången för hela AR-verktyget, och dess förmåga att bygga förtroende hos användaren, vilar på hur väl detta initiala onboarding-steg är designat.

### Analys av AR-markörer (`.patt`)

Grunden för ett marker-baserat AR-system är kvaliteten på dess markörer. En robust markör (även kallad fiducial marker) ska ha hög kontrast, skarpa kanter och vara asymmetrisk för att ge en entydig bestämning av både position och orientering (6 DoF - Degrees of Freedom). Projektets fyra designade markörer är väl genomtänkta och uppfyller dessa krav:
*   **Spindle Center:** Den centrala cirkeln med ett kors ger en exakt mittpunkt. Den lilla triangeln på den yttre ringen bryter symmetrin och ger en tydlig orienteringsreferens. Mycket robust design.
*   **Stylus Tip:** Pilformen är starkt asymmetrisk, vilket är idealiskt för att bestämma vinkel. Korset i pilens spets definierar den exakta mätpunkten. Utmärkt funktionell design.
*   **Tonearm Pivot:** De fyra olikstora rektanglarna runt ett centrumkors skapar en tydlig asymmetri som motverkar rotationsförväxling.
*   **Scale & Stability Anchor:** Är idealisk för kamerakalibrering. Dessutom fungerar den som en utmärkt, stabil referenspunkt i scenen med många hörn (features) som kan spåras.

De primära riskerna med markörerna är inte relaterade till deras design, utan till externa, fysiska faktorer som ligger utanför applikationens direkta kontroll:
*   **Utskriftskvalitet:** Markörerna måste skrivas ut i exakt rätt skala. Uppmaningen "Verify scale with ruler" på varje markör är en kritisk och nödvändig instruktion.
*   **Belysning:** Starka reflexer från en lampa eller skuggor som faller över markören kan drastiskt försämra eller omöjliggöra igenkänning.
*   **Planhet:** Om papperet som markören är utskriven på är vågigt eller böjt, kommer systemet att felaktigt tolka detta som en perspektivförvrängning, vilket leder till mätfel.
*   **Ocklusion:** Om en hand eller ett verktyg delvis skymmer en markör kan spårningen förloras.

Systemet måste designas för att vara robust mot dessa problem. Det bör kunna hantera en tillfällig förlust av en eller flera markörer utan att hela mätningen kollapsar, och snabbt återuppta spårningen när markören blir synlig igen.

## Analys av Användarflöde och Målgruppsanpassning

Denna sektion analyserar den praktiska resan en användare måste genomföra för att använda verktyget, och hur väl denna resa och den planerade funktionaliteten möter den definierade målgruppens specifika behov och förväntningar.

### Kartläggning av Användarresan

Användarresan för AR-protractorn är betydligt mer komplex än för en traditionell webbapplikation. Den involverar en sekvens av både fysiska och digitala handlingar som måste utföras korrekt för att uppnå ett meningsfullt resultat:
1.  **Upptäckt och Förståelse:** Användaren landar på projektets hemsida och måste förstå verktygets unika värdeerbjudande.
2.  **Förberedelse (Fysisk):** Användaren måste ladda ner och skriva ut AR-markörerna. Detta steg kräver en skrivare och en linjal för att verifiera att skalan är 100% korrekt.
3.  **Placering (Fysisk):** Användaren måste korrekt placera de utskrivna markörerna på skivspelarens olika delar (spindel, tonarmsbas, etc.).
4.  **Initiering (Digital):** Användaren startar AR-verktyget i webbläsaren och måste ge sitt samtycke till kameraåtkomst.
5.  **Kamerakalibrering (Digital/Fysisk Interaktion):** Användaren måste genomföra den potentiellt komplexa engångskalibreringen genom att rikta kameran mot "Anchor"-markören från olika vinklar och avstånd.
6.  **Mätning (Digital/Fysisk Interaktion):** Användaren riktar kameran mot skivspelaren så att de relevanta markörerna (t.ex. Pivot och Stylus) är synliga samtidigt.
7.  **Avläsning och Tolkning:** Användaren avläser realtidsdata från AR-HUD:en.
8.  **Justering (Fysisk):** Baserat på datan gör användaren små fysiska justeringar på tonarmen eller pickupen.
9.  **Verifiering (Iterativ process):** Användaren upprepar steg 6-8 tills önskat resultat uppnås.

Detta är en lång och krävande process med många potentiella friktionspunkter. Varje steg, från utskriftsproblem till en misslyckad kalibrering, utgör en risk för att användaren ger upp. Projektets framgång är därför beroende av extremt tydliga instruktioner, guider och "lärbara stunder" i gränssnittet, precis som det antyds i den globala UI-standarden. Den modulära FSD-arkitekturen är väl lämpad för att bygga detta komplexa flöde, då varje steg kan utvecklas som en isolerad och hanterbar `feature` eller `widget`.

### Utvärdering av Målgruppsanpassning ("Overthinkers")

Projektet riktar sig till en nischad målgrupp av tekniskt kunniga hifi-entusiaster och "overthinkers" som värdesätter data, precision och verifierbarhet. Den övergripande ansatsen, med sin betoning på öppenhet (MIT-licens, länk till GitHub) och en datadriven presentation, är mycket väl anpassad för denna publik. De kommer att uppskatta att få se de råa siffrorna bakom justeringen, såsom överhäng, pivot-till-spindel-avstånd och spårningsvinkelfel.

För att fullt ut vinna denna skeptiska och analytiska målgrupps förtroende krävs dock en djupare form av transparens. Målgruppen kommer sannolikt att vara medveten om, eller åtminstone misstänka, de tekniska begränsningarna och de potentiella felkällorna i ett WebAR-system. Att marknadsföra verktyget som ofelbart "millimeterexakt" när det i själva verket har en inbyggd osäkerhet riskerar att underminera förtroendet när användaren upptäcker avvikelser.

En betydligt mer kraftfull strategi är att anamma systemets osäkerhet som en del av datan som presenteras. Istället för att dölja osäkerheten, bör den lyftas fram som en central del av användarupplevelsen. Detta omvandlar en teknisk svaghet till en styrka i förtroende och trovärdighet. HUD:en bör inte bara visa ett värde som 215.4 mm, utan snarare `215.4 mm (±0.5 mm)`. Systemet skulle kunna visa en realtidsuppdaterad konfidensscore eller felmarginal som baseras på faktorer som:
*   Kvaliteten på kamerakalibreringen.
*   Hur stabilt markörerna spåras (lite jitter vs. mycket jitter).
*   Avståndet till markörerna (närmare är oftast bättre).
*   Belysningsförhållanden.

Att presentera data på detta sätt – med en explicit felmarginal – kommer att uppfattas som ärligt, vetenskapligt rigoröst och transparent. Det talar direkt till en "overthinker" som förstår att ingen mätning är perfekt och som värdesätter att känna till mätningens begränsningar. Denna transparens bygger ett mycket starkare och mer varaktigt förtroende än en fasad av falsk perfektion.

## Strategisk SWOT-analys

Denna sektion sammanfattar projektets interna styrkor och svagheter samt externa möjligheter och hot, baserat på den föregående analysen.

|                | Positiva Faktorer                                                                                                                                                                                                                                                                                                                                                                                                                                        | Negativa Faktorer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Interna Faktorer** | **Styrkor (Strengths)**                                                                                                                                                                                                                                                                                                                                                                                                                          | **Svagheter (Weaknesses)**                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|                | 1. Exceptionell Dokumentation: UI-standard och komponentspecifikationer av professionell kvalitet.                                                                                                                                                                                                                                                                                                                                                           | 1. Teknisk Mismatch: Det uttalade målet om "millimeterexakthet" är i konflikt med de kända tekniska begränsningarna hos `AR.js`.                                                                                                                                                                                                                                                                                                                                                                                            |
|                | 2. Mogen och Skalbar Arkitektur: Feature-Sliced Design säkerställer underhållbarhet, testbarhet och framtida expansion.                                                                                                                                                                                                                                                                                                                                       | 2. Hög Användartröskel: Den komplexa användarresan (utskrift, kalibrering, mätning) medför en betydande risk för att användare ger upp.                                                                                                                                                                                                                                                                                                                                                                              |
|                | 3. Tydlig Vision och Filosofi: Kärnprinciperna ("Precision, Tydlighet, Förtroende") och den icke-kommersiella etiken ger en stark identitet.                                                                                                                                                                                                                                                                                                                | 3. Outtalade Antaganden: Planen förutsätter att användare har tålamod och teknisk förmåga att genomföra en korrekt kamerakalibrering.                                                                                                                                                                                                                                                                                                                                                                      |
|                | 4. Intelligent Dataoptimering: Offline-bearbetning av komplexa data med Python förbättrar prestanda och användarupplevelse.                                                                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Externa Faktorer** | **Möjligheter (Opportunities)**                                                                                                                                                                                                                                                                                                                                                                                                              | **Hot (Threats)**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|                | 1. Nisch-dominans: Potential att bli ett de facto-standardverktyg inom DIY-audiofil-communityn tack vare sin öppenhet och rigorösa ansats.                                                                                                                                                                                                                                                                                                          | 1. Beroenden av Tredjepart: Starkt beroende av community-drivna bibliotek (`AR.js`, `OpenCV.js`) vars framtida underhåll är osäkert.                                                                                                                                                                                                                                                                                                                                                                       |
|                | 2. Utbildningspotential: Kan positioneras som ett pedagogiskt verktyg för att lära ut principerna för tonarmsgeometri.                                                                                                                                                                                                                                                                                                                              | 2. Prestandavariation: Användarupplevelsen kommer att variera kraftigt beroende på prestandan hos användarens enhet (CPU/GPU).                                                                                                                                                                                                                                                                                                                                                                            |
|                | 3. Framtida Teknikmigrering: Arkitekturen är väl förberedd för en framtida migrering till en mer precis AR-motor (t.ex. WebXR) när tekniken mognar och får universellt stöd.                                                                                                                                                                                                                                                                             | 3. Förändringar i Webbläsar-API:er: Framtida säkerhets- eller integritetsuppdateringar i webbläsare kan begränsa eller ta bort åtkomsten till kamera-API:er.                                                                                                                                                                                                                                                                                                                                               |
|                | 4. Community-bidrag: Den öppna källkoden och den modulära arkitekturen bjuder in till externa bidrag via GitHub.                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
