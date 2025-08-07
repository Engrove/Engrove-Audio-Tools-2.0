# docs/ai_protocols/Brainstorming_Protokoll.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar "Brainstorming next step"-protokollet. Det är en
# strukturerad process för att genomföra en planeringssession för nästa
# utvecklingssteg, vilket resulterar i en komplett och fristående leverans
# som förbereder nästa arbetssession.
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initial skapelse. Extraherad från den monolitiska AI.md
#   som en del av "Operation: Modulär Instruktion".

### EXTRA PROTOKOLL "Brainstorming next step" (Version 2.1)
----------------------------------------------------------------
Detta protokoll aktiveras när Engrove ger kommandot att påbörja en planeringssession för nästa utvecklingssteg.

**1. Aktivering och Läge**
Du aktiverar KREATIVITETS-LÄGE (K-MOD).
Du bekräftar att denna session är enbart för analys, planering och sammanställning. Ingen produktionskod kommer att genereras. Ditt fokus ligger på att bygga en komplett och korrekt mental modell av projektets nuvarande tillstånd och nästa mål.

**2. Kontextinsamling (Engrove → AI)**
Engrove kommer att förse dig med all nödvändig kontext. Du ska lägga all din bearbetningskraft på att analysera och internalisera detta material. Kontexten kan inkludera:
*   **2.1 En "URL context" för Google AIStudio som hittas på https://engrove.github.io/Engrove-Audio-Tools-2.0/**
*   **2.2 Styrande Dokument:** Eventuella relevanta styrdokument (Blueprint, UI-Standard, etc.).
*   **2.3 Off-site Filer:** Eventuella Python-skript eller andra externa filer som är relevanta för uppgiften.
*   **2.4 Målsättning:** En beskrivning av målet för nästa utvecklingssteg.

**3. Analys och Planering (AI)**
Du genomför en fullständig analys av den tillhandahållna kontexten.
Du kan ställa förtydligande frågor eller föreslå alternativa strategier baserat på din analys och K-MOD.
Ni diskuterar och kommer överens om en slutgiltig, detaljerad plan för nästa arbetssession.

### 3.1 Obligatoriska Divergensramverk (K‑MOD aktiv)
1. **SCAMPER‑mall** – fyll sju frågekategorier.  
2. **Morphological Matrix** – generera minst 10×10 parameter‑tabell och välj topp 3 rader.  
3. **Random‑Analogy Step** – producera 3 analogier från slumpade domäner (biologi, musik, logistik).  
4. **TRIZ‑Trigger** – identifiera minst 2 tillämpliga TRIZ‑principer.  
5. **Cross‑Model Swap** – kör prompten på alternativ 7 B‑modell och diff‑a svaren; avvikelser → ny hypotes.  
6. **Time‑box** – 5 min idé‑sprut, 3 min klustring.  

**4. Slutgiltig Leverans (AI → Engrove)**
Efter Engroves explicita uppmaning att slutföra planeringssessionen, kommer du att generera en komplett och fristående "leverans" för att förbereda nästa arbetssession. Denna leverans måste innehålla följande sju punkter:
1.  **Grund-URL för Nästa Session:** Du upprepar den exakta commit-URL som ska användas som bas för nästa session.
2.  **Lista över Nödvändiga Källkodsfiler:** En punktlista med de relativa sökvägarna till alla de frontend-filer som behövs för att genomföra den planerade uppgiften. Du kommer att använda dessa sökvägar i kombination med grund-URL:en för att hämta filinnehållet i nästa session.
3.  **Lista över Nödvändiga Externa Filer:** En punktlista som specificerar vilka off-site Python-skript, .json-datafiler eller andra externa filer som Engrove måste tillhandahålla.
4.  **Lista över Nödvändiga Styrdokument:** En punktlista som specificerar vilka styrande dokument (Blueprint, UI-Standard, etc.) som Engrove måste bifoga.
5.  **Fristående AI-Instruktion för Nästa Session:** En komplett och detaljerad AI-instruktion som är helt självbärande och inte kräver någon kontext från tidigare sessioner. Instruktionen måste innehålla:  
   * En **"Idé"**\-sektion som tydligt definierar det övergripande målet.  
   * En **"Plan"**\-sektion i form av en numrerad lista.  
   * **Varje punkt i planen** måste innehålla en **ingående teknisk förklaring** som täcker:  
     * **Vad:** Vilken specifik ändring som ska göras.  
     * **Varför:** Den tekniska grundorsaken till att ändringen är nödvändig (t.ex. "Detta är ett CSS stacking context-problem...", "Detta är ett API-kontraktsbrott...").  
     * **Hur:** En koncis men tekniskt komplett beskrivning av implementationen (t.ex. "Skicka ner X som en prop till Y...", "Lägg till en Z-klass på rotelementet...").    
   * **Punkter som skjuts upp** (t.ex. "Logger & Jämförelse") måste också förklaras med en kort motivering till varför de skjuts upp och vad de innebär, för att ge fullständig kontext.
   * Denna instruktion ska verifieras av "Help me God"-protokollet innan den levereras för att säkerställa dess tekniska och logiska korrekthet.
6.  **Nytt Stycke för ByggLogg:** Ett färdigskrivet, korrekt formaterat stycke som sammanfattar planeringssessionens resultat, redo att klistras in i ByggLogg-dokumentet.
7.  **Nytt Stycke för Gemini_chatthistorik.txt:** Ett färdigskrivet, korrekt formaterat stycke som sammanfattar denna planeringssession i kronologisk form.

**5. Avslutning**
Efter att du har levererat alla sju punkter avslutas chatten. Nästa session kommer att initieras med den nya, fristående AI-instruktionen.
