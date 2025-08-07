# scripts/process_ai_metrics.py
#
# === SYFTE & ANSVAR ===
# Detta skript fungerar som en "backend"-processor för AI Performance Dashboard.
# Dess enda ansvar är att på ett robust sätt läsa in de JSON-baserade loggfilerna
# (ByggLogg.json, frankensteen_learning_db.json) och aggregera dem till ett
# enda, rent JSON-objekt som är optimerat för frontend-konsumtion.
# Det skrivs ut till standard output för att kunna fångas upp av andra skript.
#
# === HISTORIK ===
# * v1.0 (2025-08-07): Initial skapelse som en del av "Operation: Metakognition, Fas 5".
#
# === TILLÄMPADE REGLER (Frankensteen v4.0) ===
# - Arkitektur (Single Responsibility Principle): Skriptet gör en sak: läser och aggregerar data.
# - Felresiliens: Hanterar fall där loggfilerna inte finns eller är korrupta
#   genom att returnera tomma listor istället för att krascha.
# - API-kontraktsverifiering: Outputen följer ett strikt och förutsägbart JSON-schema.

import json
import os
import sys

# Definiera de relativa sökvägarna till datakällorna
BYGGLOGG_PATH = 'docs/ByggLogg.json'
LEARNING_DB_PATH = 'tools/frankensteen_learning_db.json'

def read_json_file(path, default_value):
    """
    Läser en JSON-fil på ett säkert sätt. Returnerar ett standardvärde (t.ex. en tom lista)
    om filen inte finns eller inte kan parsas.
    """
    if not os.path.exists(path):
        # Det är inte ett fel om filen inte finns än, särskilt i början.
        return default_value
    try:
        with open(path, 'r', encoding='utf-8') as f:
            # Hantera specialfallet med en helt tom fil
            content = f.read()
            if not content.strip():
                return default_value
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        # Skriv en varning till stderr så att det syns i byggloggar
        # utan att förorena JSON-outputen.
        print(f"Warning: Could not read or parse {path}. Returning default. Reason: {e}", file=sys.stderr)
        return default_value

def main():
    """
    Huvudfunktion som orkestrerar läsning, aggregering och utskrift.
    """
    # Läs in data från källfilerna med robust felhantering
    bygglogg_data = read_json_file(BYGGLOGG_PATH, [])
    learning_db_data = read_json_file(LEARNING_DB_PATH, [])

    # Strukturera den slutgiltiga outputen enligt det definierade kontraktet
    final_metrics = {
        "performanceLog": bygglogg_data,
        "learningDatabase": learning_db_data
    }

    # Skriv ut det kombinerade JSON-objektet till standard output
    print(json.dumps(final_metrics, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
