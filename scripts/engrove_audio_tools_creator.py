# scripts/engrove_audio_tools_creator.py
#
# === SYFTE & ANSVAR ===
# Huvudskript för att bygga gränssnittet.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse.
# * v1.1 (2025-08-15): Korrigerad för att hantera kommandoradsargument.
# * v2.0 (2025-08-15): Uppdaterad för att generera både HTML och CSS.
# * v3.0 (2025-08-15): Uppdaterad för att även generera logic.js.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Obligatorisk Refaktorisering: Hanterar nu tre separata output-filer.

import os
import sys
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC

def main():
    """
    Huvudfunktion som genererar index2.html, styles.css och logic.js.
    """
    if len(sys.argv) < 2:
        print("Fel: En output-sökväg för HTML-filen måste anges.", file=sys.stderr)
        sys.exit(1)
        
    html_output_path = sys.argv[1]
    output_dir = os.path.dirname(html_output_path)
    css_output_path = os.path.join(output_dir, 'styles.css')
    js_output_path = os.path.join(output_dir, 'logic.js')
    
    try:
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        print(f"Genererar UI till: {os.path.abspath(html_output_path)}")
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write(HTML_TEMPLATE)
            
        print(f"Genererar CSS till: {os.path.abspath(css_output_path)}")
        with open(css_output_path, 'w', encoding='utf-8') as f:
            f.write(CSS_STYLES)
            
        print(f"Genererar JS till: {os.path.abspath(js_output_path)}")
        with open(js_output_path, 'w', encoding='utf-8') as f:
            f.write(JS_LOGIC)
            
        print(f"\\nKlar. '{os.path.basename(html_output_path)}', '{os.path.basename(css_output_path)}', och '{os.path.basename(js_output_path)}' har skapats.")
        
    except Exception as e:
        print(f"Ett fel uppstod: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# scripts/engrove_audio_tools_creator.py
