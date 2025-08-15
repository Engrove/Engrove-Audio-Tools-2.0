# scripts/engrove_audio_tools_creator.py
#
# === SYFTE & ANSVAR ===
# Detta är huvudskriptet för att bygga det nya Engrove Audio Tools-gränssnittet.
# Det orkestrerar anrop till olika moduler för att generera den slutgiltiga HTML-filen.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse. Importerar och skriver UI-mallen.
# * v1.1 (2025-08-15): KORRIGERING: Modifierad för att acceptera en output-sökväg som ett
#   kommandoradsargument. Detta är nödvändigt för CI/CD-integration.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - API-kontraktsverifiering: Importerar från en väldefinierad modul.
# - "Help me God": Grundorsaken till felet har identifierats via logganalys.

import os
import sys
from modules.ui_template import HTML_TEMPLATE

def main():
    """
    Huvudfunktion som genererar en HTML-fil från en mall.
    Accepterar output-sökväg som första kommandoradsargument.
    """
    # KORRIGERING: Läs output-sökväg från kommandoraden istället för att hårdkoda den.
    if len(sys.argv) < 2:
        print("Fel: En output-sökväg måste anges som argument.", file=sys.stderr)
        print("Användning: python engrove_audio_tools_creator.py <sökväg_till_output.html>", file=sys.stderr)
        sys.exit(1)
        
    output_path = sys.argv[1]
    
    try:
        # Säkerställ att målmappen existerar
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        print(f"Genererar UI till: {os.path.abspath(output_path)}")
        
        # Skriv mallen till fil
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(HTML_TEMPLATE)
            
        print(f"Klar. '{os.path.basename(output_path)}' har skapats.")
        
    except Exception as e:
        print(f"Ett fel uppstod: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# scripts/engrove_audio_tools_creator.py
