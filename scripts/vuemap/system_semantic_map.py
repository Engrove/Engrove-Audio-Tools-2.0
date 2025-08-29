# scripts/vuemap/system_semantic_map.py
# v1.1
# === SYFTE & ANSVAR ===
# Detta skript genererar en System Semantic Map (SSM) i JSON-format.
# Kartan representerar kodbasens artefakter (noder) och deras inbördes
# relationer (kanter), baserat på en statisk analys av källkoden.
# Det är designat för att köras i en CI/CD-miljö för att säkerställa
# att kartan alltid är synkroniserad med den faktiska koden.
#
# Beroenden: pyjsparser
#
# === HISTORIK ===
# v1.0: Initial version med esprima-python.
# v1.1: (Help me God - Domslut) Ersatt esprima-python med pyjsparser för att
#       korrekt hantera modern JavaScript-syntax (ES2020+), specifikt
#       optional chaining ('?.').

import os
import json
import hashlib
import argparse
import pyjsparser  # Byt ut esprima mot pyjsparser
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
        script_content = content.split('<script setup>')[1].split('</script>')[0]
        return script_content
    except IndexError:
        try:
            script_content = content.split('<script>')[1].split('</script>')[0]
            return script_content
        except IndexError:
            return ""

# --- Bearbetningslogik för olika filtyper ---

def process_js_or_vue(filepath, root_dir):
    """Analyserar .js- eller .vue-filer med PyJsParser för att extrahera noder och kanter."""
    nodes, edges = [], []
    relative_path = os.path.relpath(filepath, root_dir)
    file_id = relative_path

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    code_to_parse = extract_script_from_vue(content) if filepath.endswith('.vue') else content

    if not code_to_parse.strip():
        return nodes, edges

    try:
        # Parsa koden till ett AST med pyjsparser
        ast = pyjsparser.parse(code_to_parse)
        
        # Hitta importer
        for node in ast.get('body', []):
            if node.get('type') == 'ImportDeclaration' and node.get('source', {}).get('value'):
                import_path = node['source']['value']
                edges.append({
                    "source": file_id,
                    "target": import_path,
                    "type": "IMPORTS"
                })
    except Exception as e:
        print(f"    - Varning: Kunde inte parsa {relative_path}: {e}")
        edges.append({
            "source": file_id,
            "target": "PARSING_ERROR",
            "type": "HAS_ERROR",
            "details": str(e)
        })

    return nodes, edges

def process_json_file(filepath, root_dir):
    """Bearbetar en JSON-fil, lägger bara till den som en nod."""
    return [], []

def create_file_node(filepath, root_dir):
    """Skapar en grundläggande fil-nod för alla filtyper."""
    relative_path = os.path.relpath(filepath, root_dir)
    
    file_type = "VueComponent" if filepath.endswith('.vue') \
        else "PiniaStore" if 'store' in filepath.lower() and filepath.endswith('.js') \
        else "StaticData" if filepath.endswith('.json') \
        else "Utility" if filepath.endswith('.js') \
        else "Configuration" if filepath.endswith('.yml') \
        else "BinaryAsset" if is_binary(filepath) \
        else "Other"

    return {
        "id": relative_path,
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
                
                file_node = create_file_node(filepath, root_dir)
                all_nodes.append(file_node)

                if filepath.endswith(('.js', '.vue')):
                    nodes, edges = process_js_or_vue(filepath, root_dir)
                    all_nodes.extend(nodes)
                    all_edges.extend(edges)
                elif filepath.endswith('.json'):
                    nodes, edges = process_json_file(filepath, root_dir)
                    all_nodes.extend(nodes)
                    all_edges.extend(edges)
                
    ssm = {
        "$schema": "./system_semantic_map.schema.json",
        "version": "1.1.0",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "nodes": all_nodes,
        "edges": all_edges
    }
    
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
