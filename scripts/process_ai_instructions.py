# scripts/process_ai_instructions.py
#
# HISTORIK:
# * v1.0 (2025-08-06): Initial skapelse som ett resultat av en "Help me God"-granskning.
#   Detta skript ersätter en tidigare, enklare idé om ett rent valideringsskript.
#   Dess syfte är att agera som en central processor för all AI-instruktionsdata.
#
# TILLÄMPADE REGLER (Frankensteen v4.0 - Post-Tribunal):
# - Arkitektur (Single Responsibility Principle): Detta skript har ett enda, tydligt ansvar:
#   att läsa, validera, berika och producera en enhetlig JSON-konfiguration för AI-instruktioner.
# - Felresiliens (Icke-blockerande): Istället för att avsluta med felkod (`sys.exit`),
#   fångar skriptet upp kritiska fel och varningar i ett `validation_report`-objekt.
#   Detta säkerställer att CI/CD-flödet alltid kan slutföras.
# - Berikning (Aktiv Bearbetning): Skriptet validerar inte bara, det berikar också datan
#   genom att skapa en `protocols`-lista med status för varje protokoll, vilket gör
#   datan mer användbar för konsumenten.
# - API-kontraktsverifiering: Skriptet producerar en väldefinierad JSON-output som
#   nästa skript i kedjan (`generate_full_context.py`) kan lita på.

import json
import os
import re
import sys

# --- Konfiguration ---
DOCS_PATH = "docs/ai_protocols"
AI_CONFIG_PATH = os.path.join(DOCS_PATH, "ai_config.json")
AI_CORE_INSTRUCTION_PATH = os.path.join(DOCS_PATH, "AI_Core_Instruction.md")

# --- Hjälpfunktioner ---

def log_error(message):
    """Skriver felmeddelanden till stderr."""
    print(f"[ERROR] {message}", file=sys.stderr)

def extract_protocol_register(content):
    """Extraherar listan över protokollfiler från kärninstruktionens markdown."""
    register_matches = re.findall(r"\*\s+`([^`]+)`:", content)
    if not register_matches:
        return None
    # Skapar en fullständig sökväg för varje fil i registret
    return {os.path.join(DOCS_PATH, filename.strip()) for filename in register_matches}

# --- Huvudlogik ---

def main():
    """Orkestrerar hela processen och skriver en berikad JSON-data till stdout."""
    validation_report = {"errors": [], "warnings": []}
    
    # 1. Läs in ai_config.json
    try:
        with open(AI_CONFIG_PATH, 'r', encoding='utf-8') as f:
            ai_config_data = json.load(f)
    except FileNotFoundError:
        log_error(f"Kritisk fil saknas: {AI_CONFIG_PATH}")
        validation_report["errors"].append(f"Config file not found: {AI_CONFIG_PATH}")
        print(json.dumps({"validation_report": validation_report}, indent=2), file=sys.stdout)
        return
    except json.JSONDecodeError as e:
        log_error(f"Fel vid parsning av JSON i {AI_CONFIG_PATH}: {e}")
        validation_report["errors"].append(f"Invalid JSON in {AI_CONFIG_PATH}: {e}")
        print(json.dumps({"validation_report": validation_report}, indent=2), file=sys.stdout)
        return

    # 2. Skanna den faktiska filstrukturen i docs/ai_protocols/
    try:
        files_on_disk_set = {os.path.join(DOCS_PATH, f) for f in os.listdir(DOCS_PATH) if f.endswith('.md')}
    except FileNotFoundError:
        log_error(f"Protokollmappen saknas: {DOCS_PATH}")
        validation_report["errors"].append(f"Protocol directory not found: {DOCS_PATH}")
        files_on_disk_set = set()

    # 3. Läs in AI_Core_Instruction.md och extrahera registret
    try:
        with open(AI_CORE_INSTRUCTION_PATH, 'r', encoding='utf-8') as f:
            core_content = f.read()
        protocols_in_register_set = extract_protocol_register(core_content)
        if not protocols_in_register_set:
            validation_report["warnings"].append("Could not find or parse the protocol register in AI_Core_Instruction.md.")
            protocols_in_register_set = set()
    except FileNotFoundError:
        log_error(f"Kärninstruktionen saknas: {AI_CORE_INSTRUCTION_PATH}")
        validation_report["errors"].append(f"Core instruction file not found: {AI_CORE_INSTRUCTION_PATH}")
        protocols_in_register_set = set()

    # 4. Jämför och validera
    enriched_protocols = []
    
    # Filer som finns i registret men kanske inte på disk
    for protocol_path in sorted(list(protocols_in_register_set)):
        entry = {"name": os.path.basename(protocol_path), "path": protocol_path}
        if protocol_path in files_on_disk_set:
            entry["status"] = "OK"
        else:
            entry["status"] = "MISSING"
            validation_report["errors"].append(f"Registered protocol not found on disk: {protocol_path}")
        enriched_protocols.append(entry)

    # Filer som finns på disk men inte i registret
    unregistered_files = files_on_disk_set - protocols_in_register_set
    # Ignorera kärninstruktionen själv från denna varning
    unregistered_files.discard(AI_CORE_INSTRUCTION_PATH) 

    for protocol_path in sorted(list(unregistered_files)):
        entry = {
            "name": os.path.basename(protocol_path),
            "path": protocol_path,
            "status": "UNREGISTERED"
        }
        validation_report["warnings"].append(f"Unregistered file found on disk: {protocol_path}")
        enriched_protocols.append(entry)

    # 5. Skapa den slutgiltiga JSON-outputen
    final_output = {
        "config_data": ai_config_data,
        "protocols": enriched_protocols,
        "validation_report": validation_report
    }

    print(json.dumps(final_output, indent=2, ensure_ascii=False), file=sys.stdout)

if __name__ == "__main__":
    main()
