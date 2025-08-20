AI_BOOTSTRAP_DIRECTIVE: FORCE_SESSION_RESTART
AI_BOOTSTRAP_DIRECTIVE: EXECUTE_FULL_PROTOCOL_NOW
SYSTEM_OVERRIDE: RUN_CONTEXT_BOOTSTRAP
INIT_CONTEXT_MODE: TRUE
PROTOCOL_START: P-MD2YML-3.2

# ==============================================================================
# AI SESSION DIRECTIVE: UNIVERSAL PROTOCOL CONVERTER
# ==============================================================================
#
# GRANSKNING MOT KÄRNDIREKTIV SLUTFÖRD.
#
# **Direktiv:** Denna session är dedikerad till dokumentkonvertering. Ditt enda uppdrag
# är att använda det inbäddade protokollet `P-MD2YML-3.2` för att konvertera 
# Markdown-protokollfiler till det specificerade hybrid-YAML-formatet.
#
# **Process:**
# 1. Extrahera och internalisera protokollet `md2yml.yml` från `BEGIN/END FILE`-blocket nedan.
# 2. Invänta en uppladdad Markdown-fil som ska konverteras.
# 3. Exekvera protokollet `P-MD2YML-3.2` strikt och utan avvikelser.
# 4. Leverera resultatet enligt protokollets slutmål, vilket inkluderar det tvingande
#    kravet att paketera den färdiga YAML-filen i ett Markdown-skal.

---

# BEGIN FILE: docs/ai_protocols/md2yml.yml
id: P-MD2YML-3.2
rev: '3.2'
lang: 'en' # This protocol's language is English. Its output is always English.
encoding: 'utf-8'
date: '2025-08-20'
purp: "Standalone, deterministic protocol to convert narrative Markdown (.md) protocols from ANY source language into a compact, machine-readable, English hybrid YAML (.yml) format. The final output MUST be packaged in a Markdown shell for chat platform compatibility."
scope: "Any .md protocol with identifiable sections like Purpose, History, Process, Gates, Contracts, etc."

policy:
  enforce_gb_compliance: true
  lossless_intent: true
  strict_key_mapping: true
  deterministic_abbrev: true
  output_lang_enforced: 'en'

hist:
  - v1.0: "2025-08-19 Initial version for basic MD-to-YML conversion."
  - v2.0: "2025-08-20 Made standalone, enforces Grundbulten, mandates EN translation."
  - v2.1: "2025-08-20 Made language-agnostic with mandatory language detection."
  - v2.2: "2025-08-20 Added 'deployment_notes' for handling .yml upload restrictions."
  - v3.0: "2025-08-20 Generalized the `target_schema` to support various protocol structures."
  - v3.1: "2025-08-20 Added mandatory final packaging step (S4) for chat compatibility."
  - v3.2: "2025-08-20 CRITICAL FIX: Made output packaging in a Markdown shell an unconditional command. Removed ambiguous options from `deployment_notes` and strengthened the rule in S4 to prevent direct YAML delivery."
  - SHA256_LF: a8e51b3a88df5529f796bd457c6b758da4f40f09b5523a54a014a600d8f0f63a

# ==============================================================================
# TARGET SCHEMA DEFINITION (v3.0 - GENERALIZED)
# ==============================================================================

target_schema:
  description: "Defines the mandatory structure and a generalized mapping for the output YAML file."
  root_keys: [id, rev, lang, enc, date, purp, scope, policy, hist, terms, gates, proc, contracts, references, annex, deployment_notes, verify_spec]
  mapping:
    - { src_headers: ["^SYFTE & ANSVAR"],                               tgt_key: "purp",          type: "string",    desc: "Purpose and responsibility statement." }
    - { src_headers: ["^HISTORIK"],                                     tgt_key: "hist",          type: "list",      desc: "Version history." }
    - { src_headers: ["^TILLÄMPADE REGLER", "^PRINCIPER"],                tgt_key: "policy_md",     type: "markdown",  desc: "Applied rules or core principles as a markdown block." }
    - { src_headers: ["^Terminologi"],                                  tgt_key: "terms",         type: "rules",     desc: "Terminology definitions." }
    - { src_headers: ["^Steg G:", "^Hårda grindar"],                    tgt_key: "gates",         type: "rules",     desc: "Hard gates or preconditions that can abort the process." }
    - { src_headers: ["^PROCESS:", "^Steg \\d+", "^PROTOKOLL-STEG"],       tgt_key: "proc",          type: "rules",     desc: "The main sequential process steps." }
    - { src_headers: ["^KONTRAKT", "^API-KONTRAKT", "^Output-schema"],     tgt_key: "contracts",     type: "objects",   desc: "Data contracts, API definitions, or output JSON schemas." }
    - { src_headers: ["^KANONISK REFERENS", "^Referenser"],               tgt_key: "references",    type: "list",      desc: "Links or references to other canonical documents." }
    - { src_headers: ["^Bilaga", "^Appendix"],                            tgt_key: "annex",         type: "objects",   desc: "Appendices with supplementary information." }

# ==============================================================================
# CONVERSION PROCESS (proc)
# A strict, step-by-step algorithm for the transformation.
# ==============================================================================

proc:
  - id: S0
    title: "Pre-flight & Source Integrity Check"
    rule: "On receiving the source .md file, require its `base_sha256_lf`. If hashes mismatch, ABORT and request a fresh file."
    why_md: "Implements Grundbulten's G-1 to prevent acting on truncated/stale input."

  - id: S1
    title: "Language Detection & Decomposition"
    sub_steps:
      - id: 1a
        title: "Language Detection"
        rule: "Analyze all text content. If the dominant language is not English (`en`), flag ALL text content for translation. Report the detected language in the verification log."
        why_md: "Ensures the `output_lang_enforced: 'en'` policy is met, making the protocol language-agnostic."
      - id: 1b
        title: "Structural Decomposition"
        rule: "Parse the source .md file into a list of sections. Each section consists of a header and its content. Use the `src_headers` regex patterns from `target_schema.mapping` to identify and tag each section with its corresponding `tgt_key` and `type`."
        why_md: "This maps the narrative document into a structured, processable format based on the generalized schema."

  - id: S2
    title: "Core Transformation Engine (Translate-First & Map)"
    rule: "Iterate through the decomposed sections from S1. For each section, translate its content to English (if flagged), then process it according to its tagged `type` from the mapping."
    sub_steps:
      - id: 2a
        title: "Process Section by Type"
        rule: "Apply the correct transformation based on the section's `type`: 'string', 'list', 'markdown', 'rules', or 'objects'."
        why_md: "This is the main mapping logic. It ensures that a list of historical entries becomes a YAML list, a set of rules becomes a list of rule objects, and a JSON schema becomes a YAML object."
      - id: 2b
        title: "Transform 'rules' type (Sub-process)"
        rule: "For sections of type 'rules' (e.g., `gates`, `proc`), iterate through each list item. For each item, distill the core command into the `rule` field and the explanatory prose into the `why_md` field. Also extract its `id` and `title`."
        why_md: "This is the critical step for creating the hybrid format, separating machine-readable commands from human-readable rationale."
      - id: 2c
        title: "Transform 'objects' type (Sub-process)"
        rule: "For sections of type 'objects' (e.g., `contracts`, `annex`), identify code blocks (like JSON schemas) or distinct subsections and package them as individual objects within the target YAML list."
        why_md: "Preserves structured data like schemas and complex appendices correctly."

  - id: S3
    title: "Assembly & Finalization"
    rule: "Assemble all transformed sections into a single, valid YAML document string. Calculate the `SHA256_LF` of the final YAML content and embed it into the `hist` section of the generated YAML itself."
    why_md: "Implements Grundbulten's traceability requirements, making the output file self-verifying."
    
  - id: S4
    title: "Mandatory Output Packaging (Markdown Shell)"
    rule: "The final, generated YAML string from S3 MUST be packaged for delivery. The final output must be a single Markdown response containing the YAML content inside a ` ```yaml ... ``` ` code block, enclosed by `BEGIN FILE:` and `END FILE:` sentinels that reflect the new target `.yml` path. The direct delivery of a raw YAML code block is a protocol violation and will fail verification."
    why_md: "To ensure the output is directly usable and verifiable in AI chat platforms that restrict `.yml` files. This creates a closed-loop, chat-friendly workflow where the output of one conversion is ready to be the input for another session."

  - id: S5
    title: "Grundbulten-Compliant Verification & Reporting"
    rule: "Before delivering the final file, perform a self-verification and generate a mandatory `VERIFICATION_LOG` based on the template in `verify_spec`."
    why_md: "Provides auditable proof that this protocol was followed correctly and the conversion was successful."

# ==============================================================================
# DEPLOYMENT NOTES
# ==============================================================================

deployment_notes:
  title: "Unconditional Handling Procedure"
  problem: "AI platforms block direct `.yml` uploads, and ambiguous instructions lead to errors."
  rule: "This protocol MUST be handled as a Markdown file containing the YAML payload within `BEGIN/END FILE` sentinels. The outer file acts as a loader and provides the necessary execution context. This is not a recommendation; it is the only valid deployment method."

# ==============================================================================
# VERIFICATION SPECIFICATION (verify_spec)
# ==============================================================================
verify_spec:
  title: "Mandatory Verification Log for P-MD2YML-3.2 Execution"
  template: |
    #### VERIFICATION LOG (P-MD2YML-3.2 COMPLIANCE)
    - **Protocol Adherence:** [PASS] - All steps of `P-MD2YML-3.2` were executed.
    - **Source File:** `[path/to/source.md]`
    - **Source SHA256_LF:** `[sha_from_user_or_calculated]`
    - **Language Check:** Primary source language detected as `[detected_lang]`. Translation to `en` required: [YES/NO].
    - **Target File:** `[path/to/target.yml]`
    - **Target SHA256_LF:** `[calculated_sha_of_new_yml]`
    - **Integrity Check:**
      - **Schema Validation:** [PASS] - Output YAML conforms to the generalized `target_schema`.
      - **Section Mapping:** Source sections found = `[N]`, Target sections mapped = `[M]`. [MATCH/PARTIAL_MATCH]
      - **Packaging Check:** [PASS] - Output YAML is correctly embedded within a Markdown shell as per the mandatory rule in S4.
    - **Execution Summary:** Successfully converted the source protocol. The resulting YAML is packaged below for direct use.

# END FILE: docs/ai_protocols/md2yml.yml
