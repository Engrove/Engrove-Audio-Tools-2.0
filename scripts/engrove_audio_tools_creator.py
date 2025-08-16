# scripts/engrove_audio_tools_creator.py
#
# === SYFTE & ANSVAR ===
# Detta är ett centralt byggverktyg. Det kan generera UI-filer eller
# konvertera datakällor baserat på kommandoradsargument.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse.
# * v1.1 (2025-08-15): Korrigerad för att hantera kommandoradsargument.
# * v2.0 (2025-08-15): Uppdaterad för att generera både HTML och CSS.
# * v3.0 (2025-08-15): Uppdaterad för att även generera logic.js.
# * v4.0 (2025-08-16): (Help me God - Rotorsaksanalys) Omstrukturerad för att vara
#   både kommandodriven och bakåtkompatibel. Lade till 'convert-data'-kommando
#   och hanterar nu det äldre anropssättet (med enbart sökväg) som ett
#   implicit 'build-ui'-kommando för att säkerställa att CI/CD inte misslyckas.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Fullständig Historik: Korrigerat misstag och återställt komplett historik.
# - Felresiliens: Skriptet är nu robust mot olika anropssätt.

import os
import sys
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
# Importera den nya modulen endast om den finns, för att undvika fel
try:
    from modules.data_converter import convert_json_to_msgpack
    DATA_CONVERTER_AVAILABLE = True
except ImportError:
    DATA_CONVERTER_AVAILABLE = False

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
        print("Fel: Ett kommando eller en sökväg måste anges.", file=sys.stderr)
        sys.exit(1)
        
    command_or_path = sys.argv[1]
    
    try:
        # Bakåtkompatibilitet: Om argumentet inte är ett känt kommando, anta att det är en sökväg för 'build-ui'
        if command_or_path == "build-ui" or not command_or_path in ["convert-data"]:
            path = sys.argv[2] if command_or_path == "build-ui" else command_or_path
            build_ui(path)
        
        elif command_or_path == "convert-data":
            if not DATA_CONVERTER_AVAILABLE:
                print("Fel: data_converter-modulen kunde inte importeras. Har du skapat den?", file=sys.stderr)
                sys.exit(1)
            
            print("Startar datakonvertering...")
            base_dir = os.path.dirname(os.path.dirname(__file__)) # Gå upp en nivå från /scripts
            
            files_to_convert = [
                ("public/data/cartridges-data.json", "public/data/cartridges.msgpack"),
                ("public/data/tonearms-data.json", "public/data/tonearms.msgpack")
            ]
            
            success_count = 0
            for in_file, out_file in files_to_convert:
                if convert_json_to_msgpack(os.path.join(base_dir, in_file), os.path.join(base_dir, out_file)):
                    success_count += 1
            
            print(f"\\nDatakonvertering klar. {success_count} av {len(files_to_convert)} filer konverterades.")
            
    except Exception as e:
        print(f"Ett oväntat fel uppstod: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# scripts/engrove_audio_tools_creator.py
