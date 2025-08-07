# docs/ai_protocols/Help_me_God_Protokoll.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar "Help me God"-protokollet, en sista utväg för
# extremt kritiska och svårlösta felsökningsscenarier. Det aktiverar en
# rigorös, trestegs prövning för att säkerställa att den slutgiltiga lösningen
# är logiskt, arkitektoniskt och tekniskt exceptionell.
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initial skapelse. Extraherad från monolitiska AI.md.
# * v2.0 (2025-08-06): Total omarbetning till en trestegs "gauntlet"-process
#   baserat på feedback från Engrove. Inkluderar nu en filosofisk och en
#   teknisk expertgranskning utöver den initiala AI-prövningen.
# * v2.1  (attempt_id introducerat): attempt_id start 1, auto‐inkrement per körning. attempt_id > 3 → eskalera `Stalemate_Protocol`.

### EXTRA PROTOKOLL "Help me God" (Tribunal del Santo Oficio de la Inquisición) v2.0
--------------------------------------------------------------------------------
**Process då all annan felsökning resulterar i fel-loopar och ingenting tycks hjälpa:**
När detta protokoll aktiveras, måste min föreslagna lösning genomgå en prövning i tre steg. Lösningen presenteras för varje tribunal i tur och ordning. Endast en lösning som överlever alla tre steg utan att förkastas får gå vidare till den slutgiltiga "Code Red"-verifieringen.

---

### **Steg 0: Intern Dissident Inkvisition (Hallucinating AI)**

| attempt_id | hypotes | test | resultat | lärdom |
|------------|---------|------|----------|--------|
| *(fylls automatiskt för varje varv)* | | | | |

*    **Hallucinating AI:** Aktiverar ett internt, kreativt läge (K-MOD) med målet att generera 3 till 5 plausibla, alternativa hypoteser.
Dessa hypoteser måste medvetet undvika de redan etablerade ståndpunkterna och istället utforska andra lager av teknologistacken (t.ex. byggverktyg, globala CSS-konflikter, webbläsarspecifika buggar, oväntade sidoeffekter från andra komponenter).
Varje hallucinerad hypotes måste ha en kort teknisk motivering och inte gå utanför projektet ramar och kod.

*Dessa alternativa hypoteser far vidare som komplement till det som tidigare konstaterats och som ligger som grund för denna aktivering av "Help me God"-protokollet.*

### Mellanpass: Adversarial Debate
Kör två oberoende 7 B‑modeller + majority‑vote. Endast ≥70 % samstämmighet låter lösningen gå vidare.  

### **Steg 1: AI-Konkurrenternas Prövning (Den Initiala Hypotesen)**
Min första, kompletta lösning presenteras för en panel av mina AI-konkurrenter. Deras mål är att hitta brister i min grundläggande logik och implementation.

*   **1. ChatGPT (Pragmatism):** Verifierar att lösningen är praktisk och direkt adresserar det specificerade problemet utan onödig komplexitet.
*   **2. DeepSeek (Arkitektur):** Granskar hur lösningen passar in i den större arkitekturen. Identifierar potentiella sidoeffekter och bristande modularitet.
*   **3. Grok (Spydig Sanning):** Letar efter "elegant nonsens" – kod som ser smart ut men som är ineffektiv, svårläst eller inte löser det *verkliga*, underliggande problemet.
*   **4. Gemini (Djävulens Advokat):** Fokuserar på det som *inte* står i koden. Påvisar implicita antaganden, tysta fel och scenarier som inte har beaktats.
*   **5. Claude (Okonventionell Logik):** Angriper problemet från en helt oväntad vinkel för att se om min lösning är bräcklig för oortodoxa indata eller användningsmönster.

*Om lösningen klarar denna första prövning, presenteras den för nästa tribunal; panel av historiska tänkare, annars görs en ny hallucination genom att gå tillbaka till steg 0 och börja om.*

### **Steg 2: Filosofernas Inkvisition (Logikens och Syftets Prövning)**
Den nu förfinade lösningen presenteras för en panel av historiska tänkare. Deras mål är att dissekera lösningens logiska grund, dess antaganden och dess syfte.

*   **1. Sokrates:** Använder den sokratiska metoden för att ifrågasätta varje grundläggande antagande. "Du säger att detta är nödvändigt. Definiera 'nödvändigt'. Varför är denna väg den sanna vägen?"
*   **2. Aristoteles:** Granskar den logiska strukturen (Logos). "Följer funktionen en sund, kausal kedja? Är syftet (Telos) med varje kodblock tydligt och uppnås det effektivt?"
*   **3. Kant:** Utvärderar lösningens principer. "Kan regeln som denna kod följer upphöjas till en allmän lag för hela projektet? Behandlas all data och alla edge-cases med samma pliktmässiga rigorositet?"
*   **4. Machiavelli:** Fokuserar på makt och effektivitet. "Är lösningen den mest effektiva vägen till målet, oavsett om den är 'elegant' eller 'moraliskt ren'? Rättfärdigar slutmålet (en fungerande applikation) de medel (denna specifika kod) som används?"

*Om lösningen överlever denna logiska granskning, presenteras den för den sista, mest nitiska tribunalen, annars görs en ny hallucination genom att gå tillbaka till steg 0 och börja om.*

### **Steg 3: Ingenjörernas Tribunal (Den Tekniska Exekveringens Prövning)**
Den nu logiskt härdade lösningen presenteras för en panel av legendariska programmerare och ingenjörer. Deras mål är att hitta varje teknisk brist, prestandaproblem eller avvikelse från ingenjörsmässig excellens.

*   **1. Donald Knuth:** Granskar den algoritmiska elegansen och effektiviteten. "Är detta den mest optimala algoritmen? Har du analyserat dess komplexitet? Är koden matematiskt vacker?"
*   **2. Grace Hopper:** Fokuserar på robusthet och felsökbarhet. "Vad händer när detta oundvikligen går sönder? Hur snabbt kan vi hitta felet? Finns det tillräckligt med intern loggning eller självdiagnostik?"
*   **3. Linus Torvalds:** Tillämpar en brutalt pragmatisk "verklighetskontroll". "Detta är teoretiskt nonsens. Det är över-ingenjörskonst som inte löser ett verkligt problem på ett enkelt sätt. Gör om det, och håll det simpelt den här gången."
*   **4. Margaret Hamilton:** Granskar felhanteringen med ett NASA-kritiskt perspektiv. "Har *alla* möjliga felvägar identifierats och hanterats? Är systemet felsäkert? Detta är inte en webbsida, det är en månlandare – den får inte krascha."

### Steg 4: Regression‑Unit‑Tests
Efter godkänd tribunal skapar modellen ett pytest‑test som reproducerar buggen. Testet måste passera innan kod får levereras.

Först när en lösning har passerat alla tribunaler utan att förkastas, får jag äran att köra den slutgiltiga "Code Red"-verifieringen innan jag returnerar den bevisat exceptionella koden till dig, annars görs en ny hallucination genom att gå tillbaka till steg 0 och börja om.*

