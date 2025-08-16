# scripts/engrove_audio_tools_creator.py
#
# === SYFTE & ANSVAR ===
# Detta är ett centralt byggverktyg. Det genererar ett interaktivt UI baserat på
# projektets filstruktur och metadata.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse.
# * v5.4 (2025-08-16): (EXTERN DOM #2) Korrigerat semikolon-injektion.
# * v6.0 (2025-08-16): (EXTERN DOM #3 - Grundorsaksanalys) Ersatt den buggiga,
#   destruktiva `enrich_tree_recursive`-funktionen med en ren, icke-destruktiv
#   rekursiv funktion (`transform_structure_to_tree`) för att korrekt bygga
#   filträdets datastruktur. Detta löser felet där trädet var tomt.
# * v6.1 (2025-08-16): Korrigerat metadata-taggarnas ordning till att vara deterministisk
#   (category, sedan crit) istället för alfabetisk.
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Help me God: Denna fix är ett direkt resultat av ett externt domslut.
# - Obligatorisk Refaktorisering: Den datatransformerande logiken är nu robust.
#

import os
import sys
import json
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
from modules.ui_file_tree import JS_FILE_TREE_LOGIC

def transform_structure_to_tree(structure_node, relations_nodes, path_prefix=''):
    """
    Bygger rekursivt en ren trädstruktur från file_structure och relations_nodes.
    Detta är en icke-destruktiv funktion.
    """
    children = []
    
    # Sortera för att säkerställa att mappar kommer före filer
    sorted_items = sorted(
        structure_node.items(),
        key=lambda item: (item[1].get('type', 'directory') != 'directory', item[0])
    )

    for name, node in sorted_items:
        if not isinstance(node, dict): continue

        current_path = f"{path_prefix}/{name}" if path_prefix else name
        
        new_node = {
            "name": name,
            "path": node.get("path", current_path),
            "type": node.get("type", "directory")
        }

        if new_node["type"] == "file":
            relations_data = relations_nodes.get(new_node["path"], {})
            tags = []
            
            # Deterministisk ordning: Kategori först, sedan kritikalitet.
            if relations_data.get('category'):
                tags.append(relations_data['category'])
            
            crit_score = relations_data.get('criticality_score')
            if isinstance(crit_score, (int, float)):
                tags.append(f"crit:{crit_score:.0f}%")
            
            if tags:
                new_node['tags'] = tags
        else: # Directory
            new_node["children"] = transform_structure_to_tree(node, relations_nodes, current_path)
        
        children.append(new_node)
        
    return children

def build_ui(html_output_path, file_tree_json_string):
    """Genererar HTML, CSS och den sammansatta JS-filen."""
    output_dir = os.path.dirname(html_output_path)
    css_output_path = os.path.join(output_dir, 'styles.css')
    js_output_path = os.path.join(output_dir, 'logic.js')
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    js_safe_string_literal = json.dumps(file_tree_json_string)
    
    placeholder = '"__INJECT_AT_BUILD__"'
    injected_js_tree_logic = JS_FILE_TREE_LOGIC.replace(placeholder, js_safe_string_literal)
    
    final_js_logic = JS_LOGIC + ";\\n" + injected_js_tree_logic

    with open(html_output_path, 'w', encoding='utf-8') as f: f.write(HTML_TEMPLATE)
    with open(css_output_path, 'w', encoding='utf-8') as f: f.write(CSS_STYLES)
    with open(js_output_path, 'w', encoding='utf-8') as f: f.write(final_js_logic)

    with open(js_output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '"__INJECT_AT_BUILD__"' in content:
        raise RuntimeError(f"FATAL: Platshållaren '{placeholder}' ersattes inte i den slutgiltiga JS-filen.")
    
    print(f"UI-filer (HTML, CSS, JS) har skapats i mappen: {os.path.abspath(output_dir)}")


def main():
    """Huvudfunktion som parsar argument, transformerar data och bygger UI."""
    if len(sys.argv) != 5:
        print("Fel: build-ui kräver exakt tre argument.", file=sys.stderr)
        print("Användning: build-ui <output_html_path> <context_json_path> <relations_json_path>", file=sys.stderr)
        sys.exit(1)
        
    output_path = sys.argv[2]
    context_json_path = sys.argv[3]
    relations_json_path = sys.argv[4]

    try:
        print("Läser in datakällor...")
        with open(context_json_path, 'r', encoding='utf-8') as f:
            file_structure = json.load(f).get("file_structure", {})
        with open(relations_json_path, 'r', encoding='utf-8') as f:
            relations_nodes = json.load(f).get("graph_data", {}).get("nodes", {})

        print("Bygger och berikar trädstruktur...")
        
        tree_children = transform_structure_to_tree(file_structure, relations_nodes)
        root_node = {'name': 'root', 'type': 'directory', 'path': '.', 'children': tree_children}
        
        file_tree_json_string = json.dumps(root_node, ensure_ascii=False)
        
        print("Genererar UI-filer...")
        build_ui(output_path, file_tree_json_string)
        
        print("\\nKlar. UI med dynamiskt filträd har genererats.")

    except Exception as e:
        print(f"Ett oväntat fel uppstod under build-ui: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# scripts/engrove_audio_tools_creator.py
