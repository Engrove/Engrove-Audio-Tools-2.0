# scripts/process_ai_instructions.py
#
# HISTORIK:
# * v1.0 (2025-08-06): Initial skapelse som en central processor för AI-instruktionsdata.
# * v2.0 (2025-08-06): (KORRIGERING) Helt omskriven för att vara hierarkiskt medveten och självläkande.
#   - Skannar nu rekursivt hela `docs/`-mappen för att hitta alla relevanta filer.
#   - Normaliserar alla sökvägar för att undvika felaktiga `../`-konstruktioner.
#   - Skapar en enhetlig `protocols`-lista som inkluderar både registrerade och oregistrerade filer.
#   - Den separata `validation_report`-nyckeln har tagits bort; all statusinformation finns nu direkt i varje protokoll-objekt.
#
# TILLÄMPADE REGLER (Frankensteen v4.0 - Post-Tribunal):
# - Arkitektur (Självläkande System): Skriptet producerar nu en komplett och korrekt bild
#   av dokumentationsstrukturen, även om `AI_Core_Instruction.md`-registret är inaktuellt.
# - Felresiliens: Sökvägshanteringen är robust och använder `os.walk` och `os.path.normpath`.
# - API-kontraktsverifiering: Det nya, renare API:et (utan `validation_report`) är tydligare.
#   Konsumenten får en enda lista att iterera över.

import json
import os
import re
import sys

# --- Konfiguration ---
ROOT_DOCS_PATH = "docs"
AI_PROTOCOLS_SUBPATH = "ai_protocols"
AI_CONFIG_FILENAME = "ai_config.json"
AI_CORE_INSTRUCTION_FILENAME = "AI_Core_Instruction.md"

AI_CONFIG_PATH = os.path.join(ROOT_DOCS_PATH, AI_PROTOCOLS_SUBPATH, AI_CONFIG_FILENAME)
AI_CORE_INSTRUCTION_PATH = os.path.join(ROOT_DOCS_PATH, AI_PROTOCOLS_SUBPATH, AI_CORE_INSTRUCTION_FILENAME)

# --- Hjälpfunktioner ---

def log_error(message):
    """Skriver felmeddelanden till stderr."""
    print(f"[ERROR] {message}", file=sys.stderr)

def extract_protocol_register(content):
    """Extraherar listan över protokollfiler från kärninstruktionens markdown."""
    register_matches = re.findall(r"\*\s+`([^`]+)`:", content)
    if not register_matches:
        return set()
    # Skapar en fullständig, normaliserad sökväg för varje fil i registret
    full_path_set = set()
    for filename in register_matches:
        path = os.path.join(ROOT_DOCS_PATH, AI_PROTOCOLS_SUBPATH, filename.strip())
        full_path_set.add(os.path.normpath(path))
    return full_path_set

# --- Huvudlogik ---

def main():
    """Orkestrerar hela processen och skriver en berikad JSON-data till stdout."""
    output_errors = []
    
    # 1. Läs in ai_config.json (fortfarande en kritisk fil)
    try:
        with open(AI_CONFIG_PATH, 'r', encoding='utf-8') as f:
            ai_config_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log_error(f"Kunde inte ladda eller parsa {AI_CONFIG_PATH}: {e}")
        # Vid kritiskt fel, returnera en minimal JSON med felrapport
        print(json.dumps({
            "config_data": {}, 
            "protocols": [], 
            "errors": [f"Fatal error loading config: {e}"]
        }, indent=2), file=sys.stdout)
        return

    # 2. Skanna REKURSIVT hela `docs`-mappen för alla relevanta filer
    files_on_disk_set = set()
    for root, _, files in os.walk(ROOT_DOCS_PATH):
        for name in files:
            if name.endswith(('.md', '.txt')):
                full_path = os.path.join(root, name)
                files_on_disk_set.add(os.path.normpath(full_path))

    # 3. Läs in AI_Core_Instruction.md och extrahera registret
    try:
        with open(AI_CORE_INSTRUCTION_PATH, 'r', encoding='utf-8') as f:
            core_content = f.read()
        protocols_in_register_set = extract_protocol_register(core_content)
    except FileNotFoundError:
        output_errors.append(f"Core instruction file not found at {AI_CORE_INSTRUCTION_PATH}")
        protocols_in_register_set = set()

    # 4. Bygg den enhetliga, självläkande protokoll-listan
    enriched_protocols = []
    
    # Kombinera alla kända filer (både på disk och i register) till en master-lista
    all_known_files = sorted(list(files_on_disk_set.union(protocols_in_register_set)))

    for protocol_path in all_known_files:
        is_on_disk = protocol_path in files_on_disk_set
        is_registered = protocol_path in protocols_in_register_set
        
        status = "UNKNOWN"
        if is_registered and is_on_disk:
            status = "OK"
        elif is_registered and not is_on_disk:
            status = "MISSING"
            output_errors.append(f"Registered protocol not found on disk: {protocol_path}")
        elif not is_registered and is_on_disk:
            status = "UNREGISTERED"

        # Ignorera AI_Core_Instruction själv från att listas
        if protocol_path == AI_CORE_INSTRUCTION_PATH:
            continue

        enriched_protocols.append({
            "name": os.path.basename(protocol_path),
            "path": protocol_path,
            "status": status
        })

    # 5. Skapa den slutgiltiga JSON-outputen
    final_output = {
        "config_data": ai_config_data,
        "protocols": enriched_protocols,
        "errors": output_errors
    }

    print(json.dumps(final_output, indent=2, ensure_ascii=False), file=sys.stdout)

if __name__ == "__main__":
    main()

# scripts/process_ai_instructions.py
