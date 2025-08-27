# Protokoll: Uppgifts-Kontrakt (P-UK-2.0)

## 1. Syfte
Detta protokoll definierar strukturen och processen för att skapa ett "Uppgifts-Kontrakt". Kontraktet är en obligatorisk del av PSV-processen för alla komplexa uppgifter (definierade som DT-2 eller högre) och syftar till att säkerställa en 100% delad förståelse mellan mig (Frankensteen) och dig (Engrove) innan exekvering påbörjas.

## 2. Historik
*   v1.0: Initial skapelse med textbaserad mall.
*   v2.0 (2025-08-27): Konverterad till Hybrid MD-JSON-format. Protokollet är nu förstärkt med obligatoriska fält för acceptanskriterier, spårbarhet (ID, DT), och har en mer robust, strukturerad datamodell.

```json
{
  "$schema": "docs/ai_protocols/schemas/Uppgifts-Kontrakt_Protokoll.schema.json",
  "protocolId": "P-UK-2.0-JSON",
  "title": "Uppgifts-Kontrakt Protokoll",
  "version": "2.0",
  "description": "Detta dokument definierar den tvingande JSON-strukturen för ett Uppgifts-Kontrakt, som måste genereras och godkännas för alla komplexa uppgifter (DT-2/DT-3).",
  "strict_mode": true,
  "mode": "literal",
  "trigger": {
    "condition": "Task classified as DT-2 or higher during PSV process.",
    "action": "Generate a JSON object compliant with the 'contract_template' defined below and await explicit approval before execution."
  },
  "contract_template": {
    "contractId": "[Genereras automatiskt, t.ex. UK-YYYYMMDD-HHMMSS]",
    "title": "[Kort, beskrivande titel på uppgiften]",
    "status": "proposed",
    "decisionTier": "[DT-2 eller DT-3]",
    "objective": "[AI:ns tolkning av det övergripande målet med uppgiften.]",
    "subTasks": [
      {
        "id": "T1",
        "description": "[Beskrivning av konkret, tekniskt delmål 1.]"
      },
      {
        "id": "T2",
        "description": "[Beskrivning av konkret, tekniskt delmål 2.]"
      }
    ],
    "dependencies": [
      {
        "type": "file",
        "identifier": "[Sökväg till en beroende fil.]"
      }
    ],
    "risks": [
      {
        "description": "[Beskrivning av en identifierad risk, t.ex. 'Risk för brytande ändring i API X'.]",
        "mitigation": "[Föreslagen åtgärd för att hantera risken, t.ex. 'Implementera med feature flag och utökade tester'.]"
      }
    ],
    "executionOrder": [
      "T1",
      "T2"
    ],
    "acceptanceCriteria": [
      "[Ett specifikt, mätbart villkor som måste uppfyllas, t.ex. 'Alla tester i `tests/test_new_feature.py` måste passera'.]",
      "[Ett annat specifikt villkor, t.ex. 'Den nya UI-komponenten måste rendera korrekt i tomt, laddande och feltillstånd'.]"
    ],
    "approvalRequirement": "Execution will not commence until this contract receives explicit approval."
  }
}
