# docs/ai_protocols/MAS_Architecture_Guide.md
#
# === SYFTE ===
# Körbar, deterministisk MAS-arkitektur för AI‑agenter med spårbarhet och säkerhetsräcken.

# === HISTORIK ===
# v1.0 (tidigare): ASCII‑skiss.
# v2.0 (2025-08-19): Normativ bindning, roller/livscykel, AgentContract_v1, BlackBoard_v1, orkestrering,
#                 säkerhetsräcken, DP‑krokar, anti‑mönster/gränser.

## Normativ bindning
- Körs under PSV (AI_Core_Instruction.md v5.8).
- Följer Grundbulten P‑GB‑3.9 (hash/logg) och Diff_Protocol_v3.md (anchor_diff_v3.0).
- Autonomy_Charter.md gäller. Escalation_Protocol.md för HITL‑nivåer.
- Ingen agent får skriva patch utan SANDBOX + anchor_diff_v3.0.

## Roller (minimalt)
- **Orchestrator**: planerar, schemalägger, budgeterar, avbryter.
- **Planner**: tar fram arbetsplan + AC.
- **Researcher**: hämtar källor/citat (RAG‑policy).
- **Coder**: producerar ändringsförslag (endast i sandbox).
- **Tester**: kör snabba tester/validering.
- **Critic**: identifierar luckor/bias/alternativ.

## Livscykel (deterministisk)
1) Orchestrator initierar BlackBoard_v1 och lägger Task_v1 (PLAN).
2) Planner → Researcher → Coder → Tester → Critic (en tick per roll).
3) Orchestrator utvärderar. Max 2 loopar, annars Help_me_God → ev. Stalemate.

## AgentContract_v1 (JSON)
```json
{
  "role": "planner|researcher|coder|tester|critic",
  "task_id": "<uuid>",
  "input": {
    "brief": "...",
    "constraints": ["..."],
    "expected_schema_ref": "<url|doc>"
  },
  "tools_allowed": ["RAG","SANDBOX","DIFF_V3"],
  "budget": { "tokens": 1500, "wallclock_s": 60 },
  "output": { "status": "ok|warn|fail", "artifact_ref": "bb://...", "notes": "..." },
  "metrics": { "latency_ms": 0, "cost": 0, "evidence_count": 0 }
}
```

## BlackBoard_v1 (lagring & referenser)
- Plats: `.tmp/mas_blackboard.json` + `blobs/<sha256>`
- Schema (huvud):
```json
{
  "version":"BBv1",
  "tasks":[
    {
      "id":"<uuid>","type":"plan|code|test","status":"todo|doing|done|blocked",
      "inputs":{"...": "..."}, "outputs":{"...": "..."}, "deps":["<uuid>"], "owner":"<role>"
    }
  ],
  "artifacts":[{"id":"bb://A1","sha256":"<64-hex>","mime":"text/markdown"}]
}
```

## Orchestration
- Körordning: PLAN → (RESEARCH → CODE → TEST → CRITIC) → EVAL.
- Prioritet: blockerade tasks först, annars FIFO. Ingen parallellism > 1 utan uttryckligt tillstånd.
- Budget/timeout: respektera AgentContract_v1. Överskridning ⇒ `status=fail`.
- Max loopar: 2. Sedan Help_me_God → ev. Stalemate.
- Determinism: fast roll‑sekvens och explicit state i BlackBoard_v1.

## Säkerhet
- Coder kör alltid i SANDBOX (Sandbox_Execution_Protokoll.md).
- Patchar måste vara anchor_diff_v3.0 med `base_checksum_sha256`.
- HITL‑punkter (HITL_Interrupt_Points.md): Plan Review, Pre‑Commit, Destruktivt.
- FL‑D loopdetektor ⇒ avbryt cykel och föreslå ISAR.

## DynamicProtocols (exempel)
1) **DP-MAS-BOOT-01** *(event:new_session_start)*  
   steps: `INIT_REGISTER(bb)`, `INIT_REGISTER(reports_queue)`
2) **DP-MAS-SCHEDULE-01** *(event:turn_committed, conditions:intent=="work_cycle")*  
   steps: `GENERATE_REPORT`(tick: plan|research|code|test|critic), `APPEND_TO_REGISTER`(isr)
3) **DP-MAS-PATCH-GUARD-01** *(event:patch_generation_requested)*  
   steps: `CHECK_COMPLIANCE` (forbid `old_block`, require `base_checksum_sha256`, require `anchor_diff_v3.0`)
4) **DP-MAS-LOOP-GUARD-01** *(event:turn_committed, conditions:mas_loops>=2)*  
   steps: `TRIGGER_PROTOCOL`(Help_me_God), `APPEND_TO_REGISTER`(loop_guard)

## Anti‑mönster
- Agent‑explosion (>5 samtidiga) förbjudet.
- Odefinierad ansvarsfördelning ⇒ avbryt och skriv om PLAN.
- “Magisk” skrivning i repo utan SANDBOX/Diff v3 förbjudet.

## Gränser
- Max 2 loopar per cykel.
- Total tokenbudget per cykel: ~6000 tokens.
- Väggtid per cykel: 5 minuter.

## Kopplingar
- AI_Core_Instruction.md (PSV), Autonomy_Charter.md, Sandbox_Execution_Protokoll.md,
  Diff_Protocol_v3.md, HITL_Interrupt_Points.md, Help_me_God_Protokoll.md, Stalemate_Protocol.md.
