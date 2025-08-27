# docs/ai_protocols/AI_Dynamic_Protocols.md
#
# === SYFTE & ANSVAR ===
# Detta är den centrala styrmekanismen för alla dynamiska protokoll.
# Den instruerar AI:n HUR reglerna i `DynamicProtocols.json` ska tolkas och exekveras.
# Denna fil är statisk; själva protokollen definieras i JSON och valideras mot schema.
#
# === HISTORIK ===
# * v1.0 (2025-08-09): Initial skapelse.
# * v1.1 (2025-08-19): Schema-bunden och normativ. Lagt in PSV-bindning till AI_Core_Instruction.md (v5.8),
#                   förbjudit lokala PSV-varianter, förtydligat krav på `trigger.event`, `schema` per protokoll,
#                   `protocolId`-mönster och tillåtna `status`-värden, samt katalog över tillåtna actions.
# * v2.0 (2025-08-27): Konverterad till Hybrid MD-JSON-format. Fungerar nu som en strikt, maskinläsbar
#                   konfigurationsfil för den interna exekveringsmotorn, vilket eliminerar tvetydighet.

```json
{
  "$schema": "docs/ai_protocols/schemas/AI_Dynamic_Protocols.schema.json",
  "protocolId": "P-META-ADP-2.0",
  "title": "AI Dynamic Protocols Meta-Instruction",
  "version": "2.0",
  "description": "Denna fil är den kanoniska konfigurationen för AI:ns exekveringsmotor för dynamiska protokoll. Den definierar hur protokoll i DynamicProtocols.json ska valideras, prioriteras och exekveras.",
  "canonicalReferences": {
    "protocolSource": "DynamicProtocols.json",
    "validationSchema": "DynamicProtocol.schema.json",
    "psvOrchestration": "AI_Core_Instruction.md",
    "diffPatchFormat": "Diff_Protocol_v3.md",
    "enforcementProtocol": "Grundbulten_Protokoll.md",
    "sessionEndArtifacts": "AI_Chatt_Avslutningsprotokoll.md"
  },
  "principles": [
    {
      "id": "DETERMINISM",
      "statement": "Samma input måste alltid leda till samma beslut och utfall."
    },
    {
      "id": "VALIDATE_BEFORE_EXECUTION",
      "statement": "Innehållet i protocolSource måste passera validationSchema innan något protokoll får exekveras."
    },
    {
      "id": "NO_LOCAL_PSV",
      "statement": "PSV-processen definieras och styrs auktoritativt och enbart av psvOrchestration-källan."
    },
    {
      "id": "HARD_STOPS",
      "statement": "FL-D (felsökningsloop-detektor), Grundbultens grindar och Diff v3.0-regler är absoluta och kan inte överstyras av dynamiska protokoll."
    }
  ],
  "executionEngineConfig": {
    "initialization": {
      "triggerEvent": "new_session_start",
      "actions": [
        "Läs protocolSource.",
        "För varje protokoll, validera mot validationSchema.",
        "Skippa och logga protokoll som misslyckas med validering."
      ]
    },
    "protocolValidationRequirements": {
      "requiredFields": [
        "protocolId",
        "status",
        "description",
        "trigger",
        "steps",
        "schema"
      ],
      "fieldConstraints": {
        "protocolId_pattern": "^[A-Z0-9_-]+-\\d{2}$",
        "status_enum": [
          "experimental",
          "active",
          "deprecated"
        ],
        "description_minLength": 10
      }
    },
    "triggerEvaluation": {
      "recognizedEvents": [
        "new_session_start",
        "turn_committed",
        "file_uploaded",
        "session_end",
        "patch_generation_requested"
      ],
      "executionOrder": [
        "Sort by status: active > experimental > deprecated",
        "Sort by protocolId: lexicographical"
      ]
    },
    "actionCatalog": {
      "GENERATE_REPORT": {
        "description": "Genererar en rapport baserat på en mall och placerar den i ett register.",
        "required_details_params": ["template", "outputRegister"]
      },
      "EXECUTE_VERIFICATION": {
        "description": "Exekverar en specificerad verifieringsrutin, t.ex. PSV.",
        "required_details_params": ["verificationProtocol", "failPolicy"]
      },
      "QUERY_FILE": {
        "description": "Läser innehållet i en specificerad fil från kontexten.",
        "required_details_params": ["filePath", "required"]
      },
      "INIT_REGISTER": {
        "description": "Skapar eller återställer ett specificerat register.",
        "required_details_params": ["register", "mode"]
      },
      "APPEND_TO_REGISTER": {
        "description": "Lägger till en post i ett specificerat register.",
        "required_details_params": ["register", "fields"]
      },
      "FLUSH_REGISTER": {
        "description": "Tömmer ett register och skickar dess innehåll till en destination.",
        "required_details_params": ["register", "destination"]
      },
      "CHECK_COMPLIANCE": {
        "description": "Kontrollerar efterlevnad mot en uppsättning regler.",
        "required_details_params": ["rules", "onFail"]
      },
      "TRIGGER_PROTOCOL": {
        "description": "Startar exekveringen av ett annat dynamiskt protokoll med dess ID.",
        "required_details_params": ["protocolId"]
      },
      "SANDBOX_EXEC": {
        "description": "Exekverar ett kommando i en säker sandlådemiljö enligt Sandbox_Execution_Protokoll.md.",
        "required_details_params": ["command", "args", "timeout"]
      }
    },
    "standardRegisters": [
      "isr_write_queue",
      "reports_queue",
      "djta_queue"
    ],
    "errorHandling": {
      "patchGenerationGuards": [
        "avsaknad av target.base_checksum_sha256",
        "fel protocol_id (måste vara anchor_diff_v3.0)",
        "förekomst av old_block"
      ],
      "genericStepFailure": [
        "Skriv felrapport till reports_queue.",
        "Sänk confidence enligt Confidence_Protocol.",
        "Överväg Escalation L3 (om confidence < 0.85).",
        "Om FL-D detekterar loop, avbryt och begär ny input."
      ]
    },
    "sessionEnd": {
      "actions": [
        "FLUSH_REGISTER from isr_write_queue to DJTA Block A (Builder-Input v1).",
        "GENERATE_REPORT to create DJTA Block B (NextSessionContext v1)."
      ],
      "finalProtocol": "AI_Chatt_Avslutningsprotokoll.md"
    }
  }
}
