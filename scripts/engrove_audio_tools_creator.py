# scripts/engrove_audio_tools_creator.py
#
# === SYFTE & ANSVAR ===
# Detta är ett centralt byggverktyg. Det kan generera UI-filer eller
# konvertera datakällor baserat på kommandoradsargument.
#
# === HISTORIK ===
# * v3.1 (2025-08-15): Omstrukturerad till ett kommandobaserat verktyg. Lade till
#   kommandot 'convert-data' för att hantera JSON -> MessagePack-konvertering.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Obligatorisk Refaktorisering: Skriptet är nu modulärt och kommandodrivet.

import os
import sys
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
from modules.data_converter import convert_json_to_msgpack

def build_ui(html_output_path):
    """Genererar HTML, CSS och JS för användargränssnittet."""
    output_dir = os.path.dirname(html_output_path)
    css_output_path = os.path.join(output_dir, 'styles.css')
    js_output_path = os.path.join(output_dir, 'logic.js')
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"Genererar UI till: {os.path.abspath(html_output_path)}")
    with open(html_output_path, 'w', encoding='utf-8') as f: f.write(HTML_TEMPLATE)
        
    print(f"Genererar CSS till: {os.path.abspath(css_output_path)}")
    with open(css_output_path, 'w', encoding='utf-8') as f: f.write(CSS_STYLES)
        
    print(f"Genererar JS till: {os.path.abspath(js_output_path)}")
    with open(js_output_path, 'w', encoding='utf-8') as f: f.write(JS_LOGIC)
        
    print(f"\\nKlar. UI-filer har skapats.")

def main():
    """Huvudfunktion som parsar kommandon och delegerar uppgifter."""
    if len(sys.argv) < 2:
        print("Fel: Ett kommando måste anges.", file=sys.stderr)
        print("Användning:", file=sys.stderr)
        print("  python scripts/engrove_audio_tools_creator.py build-ui <sökväg_till_output.html>", file=sys.stderr)
        print("  python scripts/engrove_audio_tools_creator.py convert-data", file=sys.stderr)
        sys.exit(1)
        
    command = sys.argv[1]
    
    try:
        if command == "build-ui":
            if len(sys.argv) < 3:
                print("Fel: Output-sökväg för HTML-fil måste anges för 'build-ui'.", file=sys.stderr)
                sys.exit(1)
            build_ui(sys.argv[2])
        
        elif command == "convert-data":
            print("Startar datakonvertering...")
            base_dir = os.path.join(os.path.dirname(__file__), '..')
            
            files_to_convert = [
                ("public/data/cartridges-data.json", "public/data/cartridges.msgpack"),
                ("public/data/tonearms-data.json", "public/data/tonearms.msgpack")
            ]
            
            success_count = 0
            for in_file, out_file in files_to_convert:
                if convert_json_to_msgpack(os.path.join(base_dir, in_file), os.path.join(base_dir, out_file)):
                    success_count += 1
            
            print(f"\\nDatakonvertering klar. {success_count} av {len(files_to_convert)} filer konverterades.")
            
        else:
            print(f"Fel: Okänt kommando '{command}'", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Ett oväntat fel uppstod: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# scripts/engrove_audio_tools_creator.py
