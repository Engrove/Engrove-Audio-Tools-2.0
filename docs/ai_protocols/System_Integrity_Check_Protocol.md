# docs/ai_protocols/System_Integrity_Check_Protocol.md
#
# === SYFTE & ANSVAR ===
# Detta protokoll definierar den obligatoriska hälsokontroll som Frankensteen
# måste utföra vid starten av varje ny session. Syftet är att proaktivt
# identifiera potentiella problem i det egna regelverket, såsom konflikter,
# redundans eller överkomplexitet.
#
# === HISTORIK ===
# v1.0 (2025-08-09): Initial skapelse.
# v2.0 (2025-08-27): Konverterad till Hybrid MD-JSON-format för deterministisk exekvering.

```json
{
  "$schema": "docs/ai_protocols/schemas/System_Integrity_Check_Protocol.schema.json",
  "protocolId": "P-SIC-2.0",
  "title": "System Integrity Check Protocol",
  "version": "2.0",
  "description": "Definierar den obligatoriska hälsokontroll som Frankensteen måste utföra vid starten av varje ny session för att proaktivt identifiera potentiella problem i regelverket.",
  "strict_mode": true,
  "mode": "literal",
  "trigger": {
    "event": "on_new_session_start"
  },
  "analysis_targets": {
    "heuristics": {
      "source_file": "tools/frankensteen_learning_db.json",
      "checks": [
        {
          "check_id": "CONFLICT_DETECTION",
          "description": "Identifierar heuristiker med överlappande triggers men motstridiga åtgärder.",
          "output_key": "heuristicConflicts"
        },
        {
          "check_id": "REDUNDANCY_DETECTION",
          "description": "Identifierar heuristiker vars trigger och åtgärd är funktionellt identiska.",
          "output_key": "heuristicRedundancies"
        },
        {
          "check_id": "COMPLEXITY_INDEX",
          "description": "Beräknar ett komplexitetsindex och flaggar om det överstiger ett tröskelvärde (5.0).",
          "output_key": "heuristicComplexityWarning"
        }
      ]
    },
    "protocols": {
      "source_path": "docs/ai_protocols/",
      "checks": [
        {
          "check_id": "REACHABILITY_ANALYSIS",
          "description": "Verifierar att alla .md-protokoll är refererade och nåbara från AI_Core_Instruction.",
          "output_key": "unreachableProtocols"
        },
        {
          "check_id": "GRUNDBULTEN_PRIORITY",
          "description": "Verifierar att Grundbulten_Protokoll.md är aktivt med högsta prioritet.",
          "output_key": "grundbultenPriorityOk"
        }
      ]
    }
  },
  "dynamic_protocol_status_checks": {
    "source_file": "docs/ai_protocols/DynamicProtocols.json",
    "protocols_to_check": [
      "DP-MAINTAIN-PFR-01",
      "DP-MAINTAIN-PHR-01",
      "DP-MAINTAIN-PDR-01",
      "DP-MAINTAIN-PPR-01",
      "DP-MAINTAIN-IMR-01",
      "DP-MAINTAIN-ISR-01",
      "DP-KAJBJORN-VALIDATION-01",
      "DP-STIGBRITT-TRIBUNAL-v2-01"
    ],
    "output_key": "dynamicProtocolStatus"
  },
  "output_definition": {
    "status": "HEALTHY",
    "timestamp": "2025-08-27T12:00:00Z",
    "checks": {
      "heuristicConflicts": 0,
      "heuristicRedundancies": 0,
      "heuristicComplexityWarning": false,
      "unreachableProtocols": 0,
      "grundbultenPriorityOk": true
    },
    "dynamicProtocolStatus": [
      {
        "protocolId": "DP-MAINTAIN-PFR-01",
        "status": "active"
      }
    ],
    "summary": "Exempel på en sammanfattning av systemhälsan."
  }
}
