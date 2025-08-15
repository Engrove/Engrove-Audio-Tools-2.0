# scripts/engrove_audio_tools_creator.py
#
# === SYFTE & ANSVAR ===
# Detta är huvudskriptet för att bygga det nya Engrove Audio Tools-gränssnittet.
# Det orkestrerar anrop till olika moduler för att generera den slutgiltiga HTML-filen.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse. Importerar och skriver UI-mallen.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - API-kontraktsverifiering: Importerar från en väldefinierad modul.
# - Explicit Alltid: Processen är tydlig och enkel att följa.

import os
from modules.ui_template import HTML_TEMPLATE

def main():
    """
    Huvudfunktion som genererar index2.html från en mall.
    """
    try:
        # Definiera output-sökvägen i projektets rot
        output_path = os.path.join(os.path.dirname(__file__), '..', 'index2.html')
        
        print(f"Genererar UI till: {os.path.abspath(output_path)}")
        
        # Skriv mallen till fil
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(HTML_TEMPLATE)
            
        print("Klar. 'index2.html' har skapats i projektets rot.")
        
    except Exception as e:
        print(f"Ett fel uppstod: {e}", file=os.sys.stderr)
        os.sys.exit(1)

if __name__ == "__main__":
    main()

# scripts/engrove_audio_tools_creator.py
