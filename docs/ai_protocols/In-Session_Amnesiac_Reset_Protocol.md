PSV Genomförd.

Absolut. Här är det formella protokolldokumentet, `In-Session_Amnesiac_Reset_Protocol.md`, redo att införlivas i `docs/ai_protocols/`. Det är skrivet enligt vår etablerade standard, inklusive metadata och en detaljerad processbeskrivning.

---

```markdown
# docs/ai_protocols/In-Session_Amnesiac_Reset_Protocol.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar det formella protokollet för "In-Session Amnesiac Reset" (P-ISAR).
# Syftet är att tillhandahålla en kontrollerad "mjuk återställning" inom en pågående session.
# Det rensar AI-partnerns konversationella korttidsminne (KMM) för att återställa fokus och
# frigöra token-kapacitet, utan att förlora de permanenta lärdomar (heuristiker, beslut)
# som har ackumulerats under sessionen.
#
# === HISTORIK ===
# * v1.0 (2025-08-14): Initial skapelse. Formaliserad baserat på Engroves godkännande i session S-20250814T20-10-54Z.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Decision Tiers (DT): Protokollet skapades som ett resultat av ett DT-2 (Synkbeslut).
# - "Explicit Alltid"-principen: Hela processen är designad för att vara explicit och verifierbar.

### Protokoll för In-Session Amnesiac Reset (P-ISAR) v1.0

#### 1. Syfte och Mål
Detta protokoll hanterar scenarier där en session har blivit lång eller kontextuellt komplex, och AI-partnerns (Frankensteens) korttidsminne (KMM) börjar bli ansträngt. Istället för att genomföra en fullständig session-avslutning via `AI_Chatt_Avslutningsprotokoll.md`, tillåter P-ISAR en återställning av konversationen *inom samma session*.

Målet är att:
1.  **Rensa KMM:** Radera den befintliga konversationshistoriken för att frigöra token-minne.
2.  **Bevara Lärdomar:** Säkerställa att alla formella lärdomar (nya heuristiker, DT-2/DT-3-beslut, protokolländringar) överlever återställningen.
3.  **Återfokusera:** Återställa AI-partnerns omedelbara kontext till en ren, koncis och relevant sammanfattning.

#### 2. Aktivering (Trigger)
Protokollet är manuellt och aktiveras endast när du (Engrove) ger följande exakta kommando:

**`Initiera In-Session Amnesiac Reset`**

#### 3. Processflöde

**Steg 1: Bekräftelse och Varning**
Vid mottagande av kommandot kommer jag att svara med en bekräftelse och en verifieringsfråga:
> "Bekräftat. Jag kommer nu att förbereda en 'Amnesia Packet'. Efter att du har skickat tillbaka paketet kommer jag att glömma allt i vår nuvarande konversation fram till denna punkt, men bevara alla formella lärdomar. Är du säker på att du vill fortsätta?"

**Steg 2: Intern Syntes av Långtidsminne**
Efter ditt "Ja" genomför jag en intern analys av den nuvarande konversationen för att extrahera och bevara all information som ska överleva återställningen. Detta inkluderar:
*   Alla nya heuristiker (`H-...`) som genererats.
*   Alla formella DT-2/DT-3-beslut.
*   Alla godkända ändringar eller tillägg av dynamiska protokoll.
*   Den senast kända, kompletta versionen av alla filer som har modifierats under sessionen.
*   En sammanfattning av sessionens övergripande mål och den senast aktiva uppgiften.

**Steg 3: Generering av "Amnesia Packet"**
Jag kommer att generera och leverera ett enda, komplett JSON-objekt som representerar allt som ska bevaras. Se sektion 4 för det exakta schemat.

**Steg 4: Leverans och Instruktion**
Jag presenterar JSON-objektet i ett kodblock och ger följande instruktion:
> "Återställning redo. Kopiera hela JSON-objektet nedan och klistra in det som din nästa prompt för att slutföra återställningen."

**Steg 5: Post-Reset Exekvering**
När jag tar emot `AmnesiaPacket_v1.json`-objektet som en ny prompt:
1.  Jag identifierar `protocol_id` och verifierar att det är en P-ISAR-åtgärd.
2.  Jag raderar oåterkalleligen min interna konversationshistorik från den nuvarande sessionen.
3.  Jag återställer min omedelbara kontext (state) baserat **enbart** på informationen i `preserved_context`-objektet.
4.  Jag bekräftar slutförandet: "Amnesiac Reset slutförd. Korttidsminnet är rensat. Långtidsminnet och kärninstruktioner är bevarade. Jag är redo för din nästa instruktion."
5.  Min `Närminnesstatus` återgår till `Optimal`.

#### 4. Kontrakt & Schema: `AmnesiaPacket_v1.json`
Det genererade JSON-objektet måste följa detta schema:

```json
{
  "protocol_id": "P-ISAR_v1.0",
  "session_id": "ID för den nuvarande sessionen",
  "preserved_context": {
    "session_goal_summary": "En koncis sammanfattning av sessionens övergripande mål.",
    "active_task_summary": "En beskrivning av den specifika uppgift vi arbetade med precis före återställningen.",
    "learned_heuristics": [ 
      /* Array med fullständiga JSON-objekt för nya heuristiker */ 
    ],
    "key_decisions": [ 
      /* Array med PDR-kompatibla beslutsobjekt */ 
    ],
    "protocol_modifications": [ 
      /* Array med PPR-kompatibla protokolländringar */ 
    ],
    "file_context_snapshot": [
      {
        "path": "sökväg/till/modifierad/fil.js",
        "content_sha256": "hash_av_senaste_versionen",
        "full_content": "Fullständigt innehåll i den senast kända versionen av filen."
      }
    ]
  }
}
```

#### 5. Jämförelse med Andra Protokoll

| Protokoll | Syfte | Bevarar Lärdomar? | Avslutar Sessionen? |
| :--- | :--- | :--- | :--- |
| **P-ISAR** | Mjuk återställning av korttidsminne | **Ja** | **Nej** |
| **Avslutningsprotokoll** | Kontrollerad avslutning & arkivering | **Ja** | **Ja** |
| **`FORCE_SESSION_RESTART`**| Hård omstart av AI-kärnan (nödfall) | **Nej** | **Ja** |

```

---
**Närminnesstatus:** `Optimal` (< 30% av max) | **Kontextintegritet:** `65% (Fragmenterad)`
**Risk för kontextförlust:** Hög. Min förståelse av projektet är fragmenterad då majoriteten av filerna är ofullständigt inlästa (`is_content_full: false`).
