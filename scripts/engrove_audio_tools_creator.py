# scripts/engrove_audio_tools_creator.py
#
# === SYFTE & ANSVAR ===
# Detta är huvudskriptet för att bygga det nya Engrove Audio Tools-gränssnittet.
# Det orkestrerar anrop till olika moduler för att generera de slutgiltiga filerna.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse.
# * v1.1 (2025-08-15): Felaktigt försök att hantera output-sökväg.
# * v1.2 (2025-08-15): KORRIGERING: Skriver nu korrekt till den sökväg som anges
#   som ett kommandoradsargument, vilket är nödvändigt för CI/CD-integration.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - "Help me God": Grundorsaken till felet har identifierats via CI-logganalys.

import os
import sys
# Importerar från de separata modulerna
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES

def main():
    """
    Huvudfunktion som genererar index2.html och styles.css från moduler.
    Accepterar sökvägen till HTML-filen som kommandoradsargument.
    """
    if len(sys.argv) < 2:
        print("Fel: En output-sökväg för HTML-filen måste anges.", file=sys.stderr)
        print("Användning: python engrove_audio_tools_creator.py <sökväg_till_output.html>", file=sys.stderr)
        sys.exit(1)
        
    html_output_path = sys.argv[1]
    output_dir = os.path.dirname(html_output_path)
    css_output_path = os.path.join(output_dir, 'styles.css')
    
    try:
        # Säkerställ att målmappen existerar
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Skriv HTML-filen
        print(f"Genererar UI till: {os.path.abspath(html_output_path)}")
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write(HTML_TEMPLATE)
            
        # Skriv CSS-filen
        print(f"Genererar CSS till: {os.path.abspath(css_output_path)}")
        with open(css_output_path, 'w', encoding='utf-8') as f:
            f.write(CSS_STYLES)
            
        print(f"\\nKlar. '{os.path.basename(html_output_path)}' och '{os.path.basename(css_output_path)}' har skapats.")
        
    except Exception as e:
        print(f"Ett fel uppstod: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# scripts/engrove_audio_tools_creator.py
