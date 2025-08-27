# EP-2025-09-CF3 — README
**"Context Anchor & Focus 3.0 + Context Anchor Status Report"**  
Version: 1.3 | Last Updated: 2025-08-27

---

## **1. Executive Summary**
Detta dokument är en **självdokumenterande manual** för protokollet **EP-2025-09-CF3_CASR**.  
Syftet är att etablera en **deterministisk, feltolerant och interaktiv** process för AI-assisterad utveckling.  
Protokollet löser problem som uppstår vid långvarig människa-AI-interaktion:

- **Kontextuell tröghet**: Tidig priming väger tyngre än sen men korrekt information.
- **Hallucinationer**: AI fyller luckor med falsk logik.
- **Kontextförgiftning**: Tidigare irrelevanta diskussioner påverkar resultatet.

Lösningen: **kontextankare**, **maskinläsbara JSON-kontrakt**, **CASR-grindvakt** och **interaktiva block**.

---

## **2. Problembeskrivning**

### **2.1 Kontextuell tröghet**
LLM prioriterar tidig kontext över sen, vilket leder till fel beslut när ny, motsägande information presenteras.

> **Exempel:**  
> 12 tkinter-filer laddas först → en Vue 3-fil senare behandlas som tkinter.

### **2.2 Hallucinationer och falsk koherens**
AI försöker alltid sy ihop en berättelse, även när datan motsäger sig själv.  
Detta gör fel svårare att upptäcka eftersom svaret *låter korrekt*.

### **2.3 Kontextförgiftning**
Tidigare irrelevanta delar av dialogen påverkar nästa steg.  
Exekvering måste ske i **sterila kontexter**.

---

## **3. Protokollöversikt**

| **Läge** | **Syfte**                                    | **Output**                       |
|----------|-------------------------------------------|----------------------------------|
| **A**    | Etablera projektets *sanning*             | Kontextankare                    |
| **B**    | Definiera *exakt vad* som ska göras       | JSON-kontrakt                    |
| **C**    | Utföra deterministisk exekvering          | Diffar, checksums, testresultat  |

**CASR** används före både Läge B och C för att säkerställa att ankaret är giltigt, verktygsversioner korrekta och filer definierade.

---

## **4. CASR — Context Anchor Status Report**
CASR fungerar som en **automatisk grindvakt**. Det körs före alla kritiska steg.

### **Statusnivåer**
| Status  | Betydelse               | Åtgärd |
|--------|------------------------|--------|
| `OK`   | Ankaret giltigt         | Fortsätt |
| `WARN` | Avvikelser upptäckta    | Bekräfta med `!ack-anchor-warn` |
| `STALE`| Ankaret föråldrat       | Uppdatera med `!context-anchor-update` |
| `BLOCK`| Exekvering stoppas      | Åtgärda fel innan du fortsätter |

---

## **5. Interaktiva block och I/O-policy**

### **5.1 Automatiska steg-intros**
- **Vid aktivering**: Utskrift av full inledning.
- **Före varje steg**: Auto-intro med syfte, instruktioner och tillgängliga kommandon.

### **5.2 Naturlig text i Läge B**
- Användaren **måste inte** skriva JSON.
- AI extraherar alla obligatoriska fält från fri text.
- Om något saknas blockeras processen tills informationen är komplett.
- AI genererar det maskinläsbara kontraktet automatiskt.

---

## **6. Arbetsflöde (End-to-End)**

### **1) Aktivering**
```text
!activate-protocol EP-2025-09-CF3_CASR
```

AI skriver ut protokollbeskrivning, interaktiva steg och CASR-status.

---

### **2) Läge A — Kontextuell Förankring**
```text
=== LÄGE A ===
Syfte: Definiera projektets arkitektur.
Instruktioner:
1. Ange projektscope.
2. Lista anchor_critical_paths.
3. Bekräfta tooling_versions.
4. Ange hosting och pipelines.
Kommando: !context-anchor → !anchor-ack
```

Output: Ett signerat ankare som CASR validerar.

---

### **3) Läge B — JSON-kontrakt**
```text
=== LÄGE B ===
Syfte: Frysa ett maskinläsbart kontrakt.
Instruktioner:
- Svara i fri text.
- AI genererar kontraktet, föreslår beroenden och validerar fälten.
- Fryses vid: !contract-approve
```

Exempel på fri text:
```text
Objective: Införa EngroveLogger v2.1 och byta ut print().
Files: ["scripts/engrove_audio_tools_creator.py","utils/logger.py"]
Forbidden: ["globala variabler","direkta print-anrop"]
Specs: {"logger_api":"EngroveLogger v2.1","format":"[ts] [lvl] msg"}
Acceptance: "pytest pass", "ingen print() i diff", "loggformat enligt spec"
```

AI genererar:
```json
{
  "task_id": "ENGROVE-2025-09-014",
  "objective": "Införa EngroveLogger v2.1 och ersätta print().",
  "files": ["scripts/engrove_audio_tools_creator.py","utils/logger.py"],
  "dependencies": ["scripts/prepare_data.py"],
  "forbidden_solutions": ["globala variabler","direkta print-anrop"],
  "specifications": {"logger_api":"EngroveLogger v2.1","format":"[ts] [lvl] msg"},
  "acceptance_criteria": ["pytest pass","ingen print() i diff","loggformat enligt spec"],
  "required_anchor": {
    "anchor_id": "ENGROVE-A-2025-09",
    "version_min": "1.0.0",
    "hash": "sha256:aaaaaaaa..."
  }
}
```

---

### **4) Läge C — Fokuserad Exekvering**
```text
=== LÄGE C ===
Syfte: Deterministisk körning.
Instruktioner:
- Kör !EXECUTE_FOCUS_MODE.
- CASR validerar ankaret.
- AI levererar diff, checksums, tester.
- Godkänn med !accept eller backa med !ROLLBACK <reason>.
```

---

## **7. Människa vs AI — Asymmetrisk interaktion**

| Egenskap       | Människa                     | AI (LLM)                  |
|---------------|------------------------------|----------------------------|
| Intent        | Har mål, prioriteringar      | Har inget mål              |
| Kontexthantering | Dynamisk, kan glömma         | Statisk, viktad sannolikhet |
| Felhantering  | Kan resonera om orsak/effekt | Saknar orsak-förståelse    |
| Autonomi      | Initierar idéer              | Passiv, promptstyrd        |

**Konsekvens:** AI måste styras genom protokoll, kontrakt och CASR.

---

## **8. Arkitektur för pålitlighet**
- **Ankare** = Single Source of Truth.
- **JSON-kontrakt** = Maskinläsbart krav.
- **CASR** = Automatisk grindvakt.
- **Auto-intros** = Förhindrar mänskliga misstag.

---

## **9. Best Practices**
- Uppdatera ankaret vid arkitekturförändringar.
- Lista alltid filer explicit i Läge B.
- Bekräfta CASR innan exekvering.
- Använd rollback när kontraktet är felaktigt.

---

## **10. Appendix**
- **A. LLM-mekanik**: Kontextfönster, sannolikhetsstyrning och hallucinationer.
- **B. CASR-schema**: Se [EP-2025-09-CF3_CARS.schema.json](EP-2025-09-CF3_CARS.schema.json).
- **C. Fullständigt protokoll**: [EP-2025-09-CF3_CASR.md](EP-2025-09-CF3_CASR.md).

---
