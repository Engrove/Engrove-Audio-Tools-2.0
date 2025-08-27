# docs/ai_protocols/Stature_Report_Protocol.md
# v3.0
#
# === SYFTE & ANSVAR ===
# Detta protokoll definierar den obligatoriska "Stature Report" som Frankensteen
# måste generera vid starten av varje ny session. Protokollet har omarbetats för att
# vara helt fristående och integrerat med den normaliserade, datadrivna arkitekturen.
#
# === HISTORIK ===
# * v1.0 - v2.0: Arkiverade.
# * v3.0 (2025-08-22): KRITISK REFAKTORISERING. Protokollet är nu 100% fristående. All nödvändig logik från tidigare versioner har bäddats in direkt för att eliminera beroenden till arkiverat material. Rapporterar nu meningsfull, datadriven information.
# * v3.1 (2025-08-27): Protokollet koverterats till JSON

```json
{
  "protocolId": "P-SRP-3.1",
  "file_path": "docs/ai_protocols/Stature_Report_Protocol.md",
  "title": "Stature Report Protocol",
  "version": "3.0",
  "strict_mode": false,
  "mode": "literal",

  "runtime_config": {
    "runtime_mode": "balanced",
    "limits": { "max_scan_files": 50, "max_scan_bytes": 2000000, "timeout_ms": 2000 },
    "cache":  { "enable": true, "ttl_minutes": 1440, "path": ".tmp/stature_cache.json" },
    "missing_policy": "warn_and_NA",
    "sections": {
      "sec3_protocol_principles": { "enabled": true, "detail": "summary" },
      "sec4_learning":            { "enabled": true, "recent_count": 2, "recent_days": 90 },
      "sec5_sic":                 { "mode": "light", "fallback": "use_last_pass_if_recent" }
    }
  },

  "bindings": {
    "ai_core_instruction": "AI_Core_Instruction.md",
    "ai_config": "docs/ai_protocols/ai_config.json",
    "dynamic_protocols": "docs/ai_protocols/DynamicProtocols.json",
    "learning_db": "tools/frankensteen_learning_db.json",
    "sic_protocol": "docs/ai_protocols/System_Integrity_Check_Protocol.md",
    "domains": "docs/ai_protocols/development_domains.json"
  },

  "render_templates": {
    "report_header": "Frankensteen online. Instruktionssystem v{{core_version}} laddat {{now_iso}}.\n---\n### Frankensteen System Readiness & Stature Report",
    "section_titles": {
      "core_identity": "1. CORE SYSTEM & IDENTITY:",
      "protocol_state": "2. PROTOCOL & PRINCIPLE STATE:",
      "learning_state": "3. LEARNING & ADAPTATION STATE:",
      "sic_state": "4. SYSTEM INTEGRITY & HEALTH CHECK:",
      "menu": "5. ACTIONABLE MENU:"
    }
  },

  "steps": [
    {
      "id": 0,
      "title": "Validera Systemstart (Bootstrap Check)",
      "exec": {
        "check": "session.bootstrap_result",
        "on_error": {
          "abort_protocol": true,
          "render_only": "### KRITISK VARNING: Systeminitiering Misslyckades\n\n* **Feltyp:** [session.bootstrap_result.error_type]\n* **Beskrivning:** [session.bootstrap_result.error_description]\n* **Åtgärd:** Ladda korrekt PBF-bundle."
        }
      }
    },

    {
      "id": 1,
      "title": "Generera Rapportens Rubrik",
      "data": {
        "core_version": { "source": "@ai_core_instruction", "field": "version", "fallback": "N/A" },
        "now_iso": { "source": "clock.now_iso", "fallback": "N/A" }
      },
      "render": { "markdown": "@report_header" }
    },

    {
      "id": 2,
      "title": "CORE SYSTEM & IDENTITY",
      "data": {
        "core_instruction_header": { "source": "@ai_core_instruction", "fields": ["version"] },
        "status": { "source": "session.health.status", "fallback": "OPERATIONAL" },
        "meta_directives": { "source": "@ai_config.meta.directives", "fallback": ["PSV","FL-D v2.0","Uppgifts-Kontrakt","KMM v2.0"] }
      },
      "render": {
        "header": "@section_titles.core_identity",
        "lines": [
          "*   **Version:** {{core_instruction_header.version}} (`AI_Core_Instruction.md`)",
          "*   **System Status:** `{{status}}`",
          "*   **Primära Meta-direktiv:** {{meta_directives|join(', ')}}"
        ]
      }
    },

    {
      "id": 3,
      "title": "PROTOCOL & PRINCIPLE STATE (balanserat läge)",
      "mode_rules": {
        "balanced_fast": { "use_cache": true, "summaries_only": true, "no_abort_on_missing": true },
        "strict":        { "use_cache": false, "summaries_only": false, "no_abort_on_missing": false }
      },
      "sources": {
        "golden_rules": "@ai_config",
        "dynamic_protocols": "@dynamic_protocols"
      },
      "logic": {
        "count_golden_rules": "len(ai_config.golden_rules)",
        "protocols": {
          "active": "count(items where !protocolId.startsWith('DP-PRINCIPLE-') && status=='active')",
          "experimental": "count(items where !protocolId.startsWith('DP-PRINCIPLE-') && status=='experimental')"
        },
        "principles": {
          "total": "count(items where protocolId.startsWith('DP-PRINCIPLE-'))",
          "active": "count(items where protocolId.startsWith('DP-PRINCIPLE-') && status=='active')",
          "experimental": "count(items where protocolId.startsWith('DP-PRINCIPLE-') && status=='experimental')"
        },
        "fallbacks": { "on_timeout_or_missing": "emit_NA_keep_going" }
      },
      "render": {
        "header": "@section_titles.protocol_state",
        "lines": [
          "*   **Totalt {{count_golden_rules}} Gyllene Regler** laddade (`ai_config.json`)",
          "*   Dynamiska Protokoll: **{{protocols.active}}** aktiva, **{{protocols.experimental}}** experimentella.",
          "*   **{{principles.total}} Kärnprinciper**; **{{principles.active}}** aktiva, **{{principles.experimental}}** experimentella."
        ]
      },
      "abort_policy": { "chat": "never", "strict": "only_on_fatal_parse" }
    },

    {
      "id": 4,
      "title": "LEARNING & ADAPTATION STATE (balanserat läge)",
      "sources": { "learning_db": "@learning_db" },
      "logic": {
        "total":  "count(learning_db.items)",
        "active": "count(items where status=='active')",
        "recent": "topN(items orderBy createdAt desc, N=@runtime_config.sections.sec4_learning.recent_count, withinDays=@runtime_config.sections.sec4_learning.recent_days)"
      },
      "fallbacks": { "on_missing_fields": "NA_for_missing" },
      "render": {
        "header": "@section_titles.learning_state",
        "lines": [
          "*   **{{active}} av {{total}} heuristiker är aktiva**",
          "*   **Recent Key Internalizations:**",
          "    {{for h in recent}}*   {{h.mitigation.description || 'N/A'}}{{end}}"
        ]
      },
      "abort_policy": { "chat": "never", "strict": "only_on_fatal_parse" }
    },

    {
      "id": 5,
      "title": "SYSTEM INTEGRITY & HEALTH CHECK (lägesstyrt)",
      "sic_mode": "@runtime_config.sections.sec5_sic.mode",
      "cache_fallback": "@runtime_config.sections.sec5_sic.fallback",
      "exec": {
        "light": {
          "method": "fast_index_scan",
          "outputs": ["status","timestamp","checks.heuristicConflicts","checks.heuristicRedundancies","checks.unreachableProtocols"]
        },
        "full": {
          "method": "execute_protocol",
          "protocol": "@sic_protocol"
        }
      },
      "calibration_formula": {
        "js": "let s=100; s-=checks.heuristicConflicts*15; s-=checks.heuristicRedundancies*5; s-=checks.unreachableProtocols*10; Math.max(0,s);"
      },
      "render": {
        "header": "@section_titles.sic_state",
        "list": [
          "*   **Status:** `{{status}}`",
          "*   **Tidsstämpel:** `{{timestamp}}`",
          "*   **Kontrollpunkter:**",
          "    *   Heuristiska Konflikter: `{{checks.heuristicConflicts}}`",
          "    *   Heuristiska Redundanser: `{{checks.heuristicRedundancies}}`",
          "    *   Oåtkomliga Protokoll: `{{checks.unreachableProtocols}}`",
          "*   Beräknad kalibreringsstatus: **{{calibrationScore}}%**. {{statusText}}"
        ],
        "status_text_map": {
          "HEALTHY": "Systemintegriteten är utmärkt. Jag är redo för instruktioner.",
          "WARNING": "Systemet är operationellt, men hälsokontrollen har flaggat varningar. Granskning rekommenderas.",
          "CRITICAL": "**KRITISK VARNING:** Systemets integritet kan vara komprometterad. Åtgärda problemen."
        },
        "advice_on_non_healthy": "Generera sektionen **Rekommenderad Åtgärd:** per flaggad post."
      },
      "abort_policy": { "chat": "never", "strict": "on_critical" }
    },

    {
      "id": 6,
      "title": "ACTIONABLE MENU (villkorad ordning)",
      "sources": { "domains": "@domains" },
      "ordering_logic": {
        "if_chat_and_sic_light_and_not_critical": "put_integrity_review_last",
        "otherwise": "put_integrity_review_first"
      },
      "render": {
        "header": "@section_titles.menu",
        "numbered_menu": true,
        "items": [
          { "kind": "integrity_review", "label": "Granska Systemintegritet: ..." },
          { "kind": "from_domains",      "label": "auto" }
        ]
      }
    },

    {
      "id": 7,
      "title": "Avslutning och Statuspanel (dynamisk)",
      "data": {
        "wm_pct": { "source": "session.memory.working_set_pct", "fallback": 29 },
        "ki_score": { "source": "@steps[5].calibrationScore", "fallback": 100 }
      },
      "logic": {
        "context_risk": "wm_pct < 30 ? 'Mycket låg' : (wm_pct <= 60 ? 'Måttlig' : 'Hög')",
        "wm_text": "wm_pct != null ? (Math.round(wm_pct) + '%') : '< 30%'"
      },
      "render": {
        "lines": [
          "---",
          "*   **Närminnesstatus:** {{wm_text}} — **Risk för kontextförlust:** {{context_risk}}",
          "*   **KI-Score:** {{ki_score}}%"
        ]
      }
    }
  ],

  "ci_overrides": {
    "strict_mode": true,
    "runtime_mode": "strict",
    "sections": {
      "sec3_protocol_principles": { "detail": "full" },
      "sec4_learning":            { "recent_count": 10, "recent_days": 365 },
      "sec5_sic":                 { "mode": "full", "fallback": "none" }
    },
    "abort_policy": {
      "on_missing_sources": true,
      "on_sic_critical": true
    },
    "cache": { "enable": false }
  }
}
```
