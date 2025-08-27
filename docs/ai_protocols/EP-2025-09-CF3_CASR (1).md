# EP-2025-09-CF3_CASR
"Context Anchor & Focus 3.0 + Context Anchor Status Report"
Version: 1.2 | Last Updated: 2025-08-27

---

## **Översikt**
Detta protokoll definierar en **deterministisk och interaktiv process** för AI-assisterad utveckling.
Målet är att eliminera kontextuell tröghet, felaktiga antaganden och bristande kravställning.

Den består av tre huvudlägen:
1. **Läge A — Kontextuell Förankring**  
   Etablerar arkitekturen, kritiska filer, verktygsversioner och beroenden.
2. **Läge B — JSON-kontrakt**  
   Genererar ett maskinläsbart kontrakt för exakt definierade uppgifter.
3. **Läge C — Fokuserad Exekvering**  
   Utför deterministiskt kontraktet under steril kontext.

**CASR** fungerar som en automatisk grindvakt i alla steg.

---

## **Aktivering**
```text
!activate-protocol EP-2025-09-CF3_CASR
```
Vid aktivering:
- AI skriver ut denna inledande beskrivning.
- Sessionen styrs av protokollet.
- `PROTOCOL_ACTIVE = true`.

---

## **Interaktivt arbetsflöde**

### **Läge A — Kontextuell Förankring**
**Syfte:** Definiera projektets arkitektur.  
**Instruktioner:**
1. Ange projektscope.
2. Lista `anchor_critical_paths`.
3. Bekräfta `tooling_versions`.
4. Ange hosting-miljö och pipelines.
5. Kör `!context-anchor` för att skapa ankaret.
6. Bekräfta med `!anchor-ack`.

---

### **Läge B — JSON-kontrakt**
**Syfte:** Skapa ett maskinläsbart kontrakt för uppgiften.  
**Instruktioner:**
1. Ange `objective`.
2. Lista exakta filer i `files`.
3. Bekräfta AI-föreslagna `dependencies`.
4. Ange `forbidden_solutions`.
5. Definiera acceptanskriterier.
6. Generera kontraktet.
7. Bekräfta med `!contract-approve`.

> **Notera:** Om `files` saknas blockeras processen tills du svarar.

---

### **Läge C — Fokuserad Exekvering**
**Syfte:** Utföra kontraktet deterministiskt.  
**Instruktioner:**
1. Starta med `!EXECUTE_FOCUS_MODE`.
2. CASR körs automatiskt:
   - Blockerar om ankaret är föråldrat.
   - Varna vid drift i verktygsversioner.
3. AI levererar kodändringar, diffar, checksummor och testresultat.
4. Godkänn med `!accept` eller gå tillbaka med `!ROLLBACK <reason>`.

---

## **CASR — Context Anchor Status Report**
Automatiserad grindvakt som körs före varje steg.

**Statusnivåer:**
- `OK` → fortsätt.
- `WARN` → kräver `!ack-anchor-warn`.
- `STALE` → kräver `!context-anchor-update`.
- `BLOCK` → exekvering stoppas tills fel är åtgärdat.

---

## **Rollback**
```text
!ROLLBACK
Reason: Beskriv varför kontraktet måste justeras.
```
Återgår till **Läge B** för att uppdatera kontraktet utan att ändra ankaret.

---

## **Sammanfattning av kommandon**
- `!activate-protocol`
- `!context-anchor`
- `!anchor-ack`
- `!contract-approve`
- `!EXECUTE_FOCUS_MODE`
- `!casr-report`
- `!ack-anchor-warn`
- `!ROLLBACK`

---
