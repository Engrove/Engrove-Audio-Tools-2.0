<!--
EP-2025-09-CF3_CASR v1.3
"Context Anchor & Focus 3.0 + Context Anchor Status Report"

Purpose
-------
Deterministisk, interaktiv process för AI-assisterad utveckling som minimerar
kontextuell tröghet och felaktiga antaganden via tre lägen (A/B/C) och en
automatiserad grindvakt (CASR). Protokollet skriver automatiskt ut inledning
vid aktivering och stegspecifika instruktioner före varje läge.

Key properties
--------------
- Aktivering via !activate-protocol.
- Inledande beskrivning och interaktiva block skrivs ut i chatten.
- Läge B accepterar naturlig text. AI extraherar och genererar JSON-kontrakt.
- CASR körs före planering och exekvering (gating).
- Rollback från C -> B utan att förlora ankare.
Last updated: 2025-08-27
-->

# EP-2025-09-CF3_CASR
"Context Anchor & Focus 3.0 + Context Anchor Status Report"  
Version: 1.3 | Last Updated: 2025-08-27

---

## **Aktivering**
```text
!activate-protocol EP-2025-09-CF3_CASR
```
Vid aktivering:
- Protokollets inledning och översikt skrivs ut.
- Interaktionsblocken för A/B/C registreras.
- `PROTOCOL_ACTIVE = true`.

---

## **Inledning (auto-utskrift)**
Detta protokoll definierar en **deterministisk och interaktiv** process.
Tre lägen:
1. **Läge A — Kontextuell Förankring**: definierar arkitektur, kritiska stigar, verktygsversioner, pipelines.
2. **Läge B — Planering & JSON-kontrakt**: skapar maskinläsbart kontrakt.
3. **Läge C — Fokuserad Exekvering**: steril körning baserat på kontrakt + focus-filer.

**CASR**: automatiserad validering som blockerar vid felaktig kontext.

---

## **Naturlig text i Läge B**
- Du kan svara i **fri text**. AI extraherar `objective`, `files`, `dependencies`,
  `forbidden_solutions`, `specifications`, `acceptance_criteria` och bygger
  **JSON-kontraktet**.
- Om något saknas avbryts processen och AI ber om komplettering.
- Kontraktet visas och fryses först vid `!contract-approve`.

---

## **Interaktivt arbetsflöde**

### **Läge A — Kontextuell Förankring (auto-intro före frågor)**
```
=== LÄGE A ===
Syfte: Etablera arkitekturens ground truth.
Instruktion:
1) Projektscope
2) anchor_critical_paths (globs)
3) tooling_versions (node, python, pnpm)
4) hosting, pipelines
Kommando: !context-anchor  →  Bekräfta: !anchor-ack
CASR körs efter ankar-skapande.
```

### **Läge B — Planering & JSON-kontrakt (auto-intro före frågor)**
```
=== LÄGE B ===
Syfte: Frysa ett komplett maskinläsbart kontrakt.
Instruktion:
- Svara i naturlig text eller struktur.
- Obligatoriskt: files, objective, specifications, acceptance_criteria.
- AI föreslår dependencies; du godkänner.
- Förbjudna lösningar listas.
Kommando för frysning: !contract-approve
CASR körs före frysning.
```

### **Läge C — Fokuserad Exekvering (auto-intro före körning)**
```
=== LÄGE C ===
Syfte: Deterministisk exekvering under steril kontext.
Instruktion:
- Endast JSON-kontrakt + !context-focus-filer.
- Ignorera tidigare chatt.
- CASR före start. WARN kräver !ack-anchor-warn.
- Efter körning: diff, checksums, tests.
- Godkänn: !accept  |  Återgå: !ROLLBACK <reason>
```

---

## **CASR — Context Anchor Status Report**
Status: `OK` | `WARN` | `STALE` | `BLOCK`  
Policy:
- `OK` → fortsätt.
- `WARN` → kräver `!ack-anchor-warn`.
- `STALE` → kräver `!context-anchor-update`.
- `BLOCK` → stoppa tills ankare/kontrakt korrigeras.

---

## **Rollback**
```text
!ROLLBACK
Reason: <orsak>
```
Återgår till Läge B för kontraktsjustering. Ankare kvarstår.

---

## **Kommandosamling**
- `!activate-protocol`
- `!context-anchor`, `!anchor-ack`, `!context-anchor-update`
- `!contract-approve`
- `!EXECUTE_FOCUS_MODE`, `!context-focus: <filer>`
- `!casr-report`, `!ack-anchor-warn`
- `!ROLLBACK`, `!accept`

---
