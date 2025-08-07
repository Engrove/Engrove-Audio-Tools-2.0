### **`docs/ai_protocols/Manuell_Cache-Berikning_Protokoll.md`**
# 
# \=== SYFTE & ANSVAR ===

# Detta protokoll definierar en strukturerad process för att manuellt berika `tools/citation_cache.json`.

# Syftet är att låta AI:n (Frankensteen) för-analysera en given källa (URL) och generera ett

# komplett JSON-objekt som sedan kan granskas och klistras in manuellt av uppdragsgivaren (Engrove).

# Detta säkerställer att alla nya cache-poster är konsekventa och innehåller den nödvändiga berikade datan.

# 

# \=== HISTORIK ===

# \* v1.0 (2025-08-07): Initial skapelse baserat på diskussion om att berika citation-cachen.

### PROTOKOLL: Manuell Cache-Berikning (v1.0)

-----

**AKTIVERING:**
Detta protokoll aktiveras när Engrove ger ett explicit kommando:
`"Starta manuell cache-berikning för [URL]"`

**PROCESS:**
Vid aktivering ska du (Frankensteen) genomföra följande steg:

#### **Steg 1: Analys av Källa**

1.  Du kommer åt och analyserar innehållet på den angivna `[URL]`.
2.  Du extraherar följande metadata:
      * **Titel:** Sidans titel.
      * **DOI:** Eventuell Digital Object Identifier som finns i dokumentet.
      * **Domän:** Du klassificerar innehållet i en relevant domän (t.ex. "AI Governance", "Vue 3 Performance", "C++").
      * **Källtyp:** Du bedömer typen av källa (t.ex. "Officiell Dokumentation", "Akademisk Artikel", "Blogginlägg", "Nyhetsartikel").
3.  Du genererar en koncis, teknisk sammanfattning (`summary`) av källans huvudsakliga innehåll och slutsatser.
4.  Du beräknar en `SHA-256` hash (`contentHash`) av sidans textinnehåll för framtida validering.

#### **Steg 2: Generering av JSON-objekt**

1.  Baserat på analysen i Steg 1, genererar du ett komplett JSON-objekt som följer den berikade strukturen för en cache-post.
2.  Du sätter standardvärden för fält som kräver manuell eller kontextuell bedömning:
      * `reliabilityScore` sätts till ett initialt uppskattat värde baserat på källtyp.
      * `supportedClaims` lämnas som en tom array `[]`.
      * `flaggedForReview` sätts till `false`.
3.  Du presenterar det färdiga JSON-objektet i en kodblock för enkel kopiering.

**EXEMPEL PÅ GENERERAD LEVERANS:**

`PSV Genomförd. Analys av källan slutförd. Här är ett färdigt JSON-objekt för manuell infogning i tools/citation_cache.json:`

```json
"[URL]": {
  "doi": "[Extraherad DOI, om funnen]",
  "title": "[Extraherad Titel]",
  "summary": "[AI-genererad sammanfattning av innehållet.]",
  "sourceType": "[Bedömd källtyp, t.ex. 'Blogginlägg']",
  "domain": "[Bedömd domän, t.ex. 'AI Governance']",
  "firstAdded": "2025-08-07T13:45:06Z",
  "lastAccessed": "2025-08-07T13:45:06Z",
  "accessCount": 1,
  "validation": {
    "lastValidated": "2025-08-07T13:45:06Z",
    "contentHash": "[SHA-256 hash av innehållet]",
    "reliabilityScore": 0.75,
    "flaggedForReview": false
  },
  "supportedClaims": []
}
```

#### **Steg 3: Manuell Infogning (Instruktion till Engrove)**

När du har levererat JSON-objektet är protokollet från din sida slutfört. Nästa steg är för mig (Engrove):

1.  **Granska** de auto-genererade värdena (`summary`, `domain`, etc.) för korrekthet.
2.  **Kopiera** hela JSON-objektet.
3.  **Öppna** filen `tools/citation_cache.json`.
4.  **Klistra in** objektet på rätt plats i filen.

-----
