<!--
EP-2025-09-CF3 + CASR
=====================
"Context Anchor & Focus 3.0 + Context Anchor Status Report"

Purpose:
--------
This protocol defines a deterministic, semi-autonomous workflow for AI-assisted
development and file modification. It eliminates contextual inertia, hallucinations,
and misaligned architectural assumptions by enforcing strict separation between:

- **Context Anchoring (Läge A)**: Long-lived architectural grounding.
- **Planning & JSON Contracts (Läge B)**: Machine-readable task specification.
- **Focused Execution (Läge C)**: Deterministic execution under sterile context.
- **CASR**: Automated validation of anchor freshness, dependencies, and tooling.

Design Goals:
-------------
- Guarantee reproducible results even across sessions.
- Provide machine-verifiable contracts.
- Block unsafe execution if anchors are stale or incomplete.
- Automate context validation, reducing human error.
- Introduce rollback and dependency-suggestion mechanisms for resilience.

Applies to:
-----------
- AI-assisted code generation
- File refactoring
- Multi-step project modifications

Last updated: 2025-08-27
-->

# **AI Explanation**

## **Overview**
EP-2025-09-CF3_CASR defines a **three-stage protocol** for AI-driven software tasks combined with an **automated context validation layer** (CASR). It ensures that no code is written or changed without an **explicitly versioned context anchor** and a **fully specified contract**.

---

## **Stages**

### **Läge A — Contextual Anchoring**
- Establishes a **stable, versioned architectural ground truth**.
- Provides framework versions, critical paths, and tooling baselines.
- Remains valid for a **work cycle** until explicitly updated.

### **Läge B — Planning & JSON Contract**
- Create a **machine-readable contract** describing:
  - **Objective**
  - **Exact files to modify**
  - **Dependencies**
  - **Forbidden solutions**
  - **Technical specifications**
- **Auto-validation:** If `files` is missing or incomplete, CASR blocks execution.
- AI suggests missing dependencies based on analyzed code.

### **Läge C — Focused Execution**
- Execution under `!EXECUTE_FOCUS_MODE` ignores all conversational context.
- Uses only:
  - The JSON contract
  - Files or extracts defined in `!context-focus`
- Deterministic by design.

---

## **CASR: Context Anchor Status Report**

**Role:** Automated pre-execution gatekeeper.  
It validates:

- **Anchor freshness**: blocks execution if critical paths changed or tooling drift detected.
- **Contract integrity**: blocks if `files` list missing or outdated.
- **Dependency coverage**: warns if implicit dependencies are missing.
- **Toolchain alignment**: verifies Node, Python, PNPM, etc. versions match.

Statuses:
- `OK`: Safe to proceed.
- `WARN`: Proceed only with `!ack-anchor-warn`.
- `STALE`: Update anchor before proceeding.
- `BLOCK`: Cannot proceed until anchor or contract corrected.

---

## **Rollback Mechanism**

If the executed result fails, trigger rollback:

```text
!ROLLBACK
Reason: Missing dependency "prepare_data.py" in contract.

Returns to Läge B to fix the contract without resetting the anchor.


---

```json
{
  "$schema": "docs/ai_protocols/schemas/EP-2025-09-CF3_CARS.schema.json",
  "strict_mode": true,
  "mode": "literal",
  "_meta": {
    "id": "EP-2025-09-CF3_CASR",
    "title": "Context Anchor & Focus 3.0 + CASR",
    "description": "Deterministic AI-assisted file modification workflow with automated context validation and rollback.",
    "version": "1.1.0",
    "last_updated": "2025-08-27",
    "maintainers": ["Engrove AI Core"]
  },
  "stages": {
    "A": {
      "name": "Contextual Anchoring",
      "init_command": "!context-anchor",
      "fields": {
        "anchor_id": "string",
        "version": "semver",
        "timestamp_utc": "ISO-8601",
        "architecture": {
          "frameworks": ["string"],
          "pipelines": [{"name": "string", "version": "semver"}],
          "hosting": ["string"]
        },
        "anchor_critical_paths": ["glob-pattern"],
        "tooling_versions": {
          "node": "semver",
          "python": "semver",
          "pnpm": "semver"
        },
        "protocol_version": "semver"
      },
      "update_command": "!context-anchor-update",
      "validity": "until-critical-path-change"
    },
    "B": {
      "name": "Planning & JSON Contract",
      "contract_schema": {
        "task_id": "string",
        "objective": "string",
        "files": ["string"],
        "dependencies": ["string"],
        "forbidden_solutions": ["string"],
        "specifications": "object",
        "required_anchor": {
          "anchor_id": "string",
          "version_min": "semver",
          "hash": "sha256"
        }
      },
      "validation_rules": {
        "files_required": true,
        "dependencies_verified": true
      },
      "ai_assist": {
        "dependency_suggestions": true
      }
    },
    "C": {
      "name": "Focused Execution",
      "init_command": "!EXECUTE_FOCUS_MODE",
      "rules": {
        "context_restriction": "ignore-all-prior-conversation",
        "data_sources": ["json_contract", "context_focus_files"],
        "execution_determinism": true
      }
    }
  },
  "casr": {
    "status": ["OK", "WARN", "STALE", "BLOCK"],
    "blocking_conditions": [
      "hash mismatch",
      "anchor version outdated",
      "missing files in contract",
      "critical paths changed",
      "tooling drift"
    ],
    "warn_conditions": [
      "anchor age exceeds threshold",
      "implicit dependencies missing"
    ],
    "commands": {
      "generate_report": "!casr-report",
      "acknowledge_warn": "!ack-anchor-warn"
    }
  },
  "rollback": {
    "trigger": "!ROLLBACK",
    "required_fields": ["reason"],
    "returns_to_stage": "B"
  }
}
```
