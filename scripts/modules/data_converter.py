# scripts/modules/data_converter.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller den centrala logiken för att konvertera stora JSON-filer
# till det mer kompakta MessagePack-formatet.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse. Implementerar JSON till MessagePack-konvertering.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Obligatorisk Refaktorisering: Konverteringslogiken är isolerad i denna modul.

import json
import msgpack
import os

def convert_json_to_msgpack(input_path, output_path):
    """
    Läser en JSON-fil, konverterar den till MessagePack och sparar resultatet.
    """
    try:
        print(f"  > Läser in JSON-fil: {input_path}")
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Källfilen hittades inte: {input_path}")
            
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("  > Konverterar till MessagePack...")
        packed_data = msgpack.packb(data, use_bin_type=True)
        
        # Säkerställ att målmappen existerar
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        print(f"  > Skriver binär data till: {output_path}")
        with open(output_path, 'wb') as f:
            f.write(packed_data)
            
        original_size = os.path.getsize(input_path)
        packed_size = os.path.getsize(output_path)
        reduction = 100 - (packed_size / original_size * 100)
        
        print(f"  > KLAR. Storlek: {original_size / 1024:.0f} kB -> {packed_size / 1024:.0f} kB ({reduction:.1f}% minskning).")
        return True
        
    except Exception as e:
        print(f"  > FEL vid konvertering av {input_path}: {e}", file=os.sys.stderr)
        return False

# scripts/modules/data_converter.py
