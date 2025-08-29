# scripts/vuemap/system_semantic_map.py
# v1.0
# === SYFTE & ANSVAR ===
# Detta skript genererar en System Semantic Map (SSM) i JSON-format.
# Kartan representerar kodbasens artefakter (noder) och deras inbördes
# relationer (kanter), baserat på en statisk analys av källkoden.
# Det är designat för att köras i en CI/CD-miljö för att säkerställa
# att kartan alltid är synkroniserad med den faktiska koden.
#
# Beroenden: esprima-python

import os
import json
import hashlib
import argparse
import esprima
from datetime import datetime, timezone

# --- Kärnfunktioner för filhantering ---

def calculate_sha256(filepath):
    """Beräknar SHA-256-hash för en fil."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def is_binary(filepath):
    """Avgör om en fil är binär baserat på filändelse."""
    binary_extensions = ['.webp', '.jpg', '.jpeg', '.gif', '.png', '.pdf']
    return any(filepath.lower().endswith(ext) for ext in binary_extensions)

def extract_script_from_vue(content):
    """Extraherar innehållet från <script setup> eller <script> i en .vue-fil."""
    try:
        # Föredrar <script setup>
        script_content = content.split('<script setup>')[1].split('</script>')[0]
        return script_content
    except IndexError:
        try:
            # Fallback till <script>
            script_content = content.split('<script>')[1].split('</script>')[0]
            return script_content
        except IndexError:
            return "" # Ingen script-tagg hittades

# --- Bearbetningslogik för olika filtyper ---

def process_js_or_vue(filepath, root_dir):
    """Analyserar .js- eller .vue-filer med Esprima för att extrahera noder och kanter."""
    nodes, edges = [], []
    relative_path = os.path.relpath(filepath, root_dir)
    file_id = relative_path

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    code_to_parse = extract_script_from_vue(content) if filepath.endswith('.vue') else content

    if not code_to_parse.strip():
        return nodes, edges # Hoppa över filer utan script

    try:
        # Parsa koden till ett AST
        ast = esprima.parseModule(code_to_parse, {'range': True, 'loc': True})
        
        # Hitta importer
        for node in ast.body:
            if node.type == 'ImportDeclaration' and node.source and node.source.value:
                import_path = node.source.value
                # Skapa en IMPORT-kant
                # Not: En mer avancerad version skulle lösa relativa sökvägar
                edges.append({
                    "source": file_id,
                    "target": import_path,
                    "type": "IMPORTS"
                })

        # Ytterligare analys för funktioner, exporter, etc. kan läggas till här
        # Detta är en grundläggande implementation fokuserad på beroenden.

    except Exception as e:
        print(f"    - Varning: Kunde inte parsa {relative_path}: {e}")
        # Lägg till en kant som indikerar ett parsingfel för felsökning
        edges.append({
            "source": file_id,
            "target": "PARSING_ERROR",
            "type": "HAS_ERROR",
            "details": str(e)
        })

    return nodes, edges

def process_json_file(filepath, root_dir):
    """Bearbetar en JSON-fil, lägger bara till den som en nod."""
    # Framtida utökning: Parsa innehållet för att identifiera nyckelstrukturer.
    return [], []

def create_file_node(filepath, root_dir):
    """Skapar en grundläggande fil-nod för alla filtyper."""
    relative_path = os.path.relpath(filepath, root_dir)
    file_id = relative_path
    
    file_type = "VueComponent" if filepath.endswith('.vue') \
        else "PiniaStore" if 'store' in filepath.lower() and filepath.endswith('.js') \
        else "StaticData" if filepath.endswith('.json') \
        else "Utility" if filepath.endswith('.js') \
        else "Configuration" if filepath.endswith('.yml') \
        else "BinaryAsset" if is_binary(filepath) \
        else "Other"

    return {
        "id": file_id,
        "type": "File",
        "path": relative_path,
        "hash": calculate_sha256(filepath),
        "fileType": file_type,
        "purpose": f"Represents the file artifact at {relative_path}."
    }

# --- Huvudlogik ---

def main(root_dir, output_file):
    """Huvudfunktion för att generera SSM."""
    print("Startar generering av System Semantic Map (SSM)...")
    
    all_nodes = []
    all_edges = []
    
    target_dirs = [os.path.join(root_dir, 'src'), os.path.join(root_dir, 'public', 'data')]
    
    for directory in target_dirs:
        if not os.path.isdir(directory):
            print(f"Varning: Mappen {directory} hittades inte. Hoppar över.")
            continue
            
        print(f"  - Bearbetar mapp: {os.path.relpath(directory, root_dir)}")
        for subdir, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(subdir, filename)
                
                # 1. Skapa alltid en fil-nod
                file_node = create_file_node(filepath, root_dir)
                all_nodes.append(file_node)

                # 2. Utför djupare analys baserat på filtyp
                if filepath.endswith(('.js', '.vue')):
                    nodes, edges = process_js_or_vue(filepath, root_dir)
                    all_nodes.extend(nodes)
                    all_edges.extend(edges)
                elif filepath.endswith('.json'):
                    nodes, edges = process_json_file(filepath, root_dir)
                    all_nodes.extend(nodes)
                    all_edges.extend(edges)
                # Binära och andra filer behöver ingen ytterligare parsning
                
    # Skapa slutgiltig SSM-struktur
    ssm = {
        "$schema": "./system_semantic_map.schema.json",
        "version": "1.0.0",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "nodes": all_nodes,
        "edges": all_edges
    }
    
    # Skriv till output-fil
    output_path = os.path.join(root_dir, output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ssm, f, indent=2)
        
    print(f"\nSSM genererad framgångsrikt!")
    print(f"  - Noder: {len(all_nodes)}")
    print(f"  - Kanter: {len(all_edges)}")
    print(f"  - Output: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a System Semantic Map (SSM) for a Vue.js project.")
    parser.add_argument(
        "root_directory",
        help="The root directory of the project to scan."
    )
    parser.add_argument(
        "--output",
        default="scripts/vuemap/system_semantic_map.json",
        help="The relative path from the root directory to save the output JSON file."
    )
    
    args = parser.parse_args()
    main(args.root_directory, args.output)
