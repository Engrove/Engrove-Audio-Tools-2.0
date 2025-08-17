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
# * v6.2 (2025-08-16): Modifierat för att injicera project_overview och använda
#   endast `category` som tagg i filträdet.
# * v6.3 (2025-08-17): (Help me God - Grundorsaksanalys) Korrigerat `file_tree_placeholder`
#   för att matcha den bare-word-variabel som används i `ui_file_tree.py`,
#   vilket löser det kritiska `ReferenceError` vid körning.
# * v7.0 (2025-08-17): Lade till rekursiv storleksberäkning för filer och mappar.
# * v7.1 (2025-08-17): Importerar och inkluderar den nya (tomma) `ui_performance_dashboard.py`-modulen för att förbereda för framtida funktionalitet.
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Grundbulten v3.3: Denna ändring följer den uppgraderade processen för transparens.
# - GR7 (Fullständig Historik): Historiken har uppdaterats korrekt.
#
import os
import sys
import json
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
from modules.ui_file_tree import JS_FILE_TREE_LOGIC
from modules.ui_performance_dashboard import JS_PERFORMANCE_LOGIC

def calculate_node_size(structure_node):
    """
    Beräknar rekursivt den totala storleken för en nod (fil eller mapp).
    """
    if not isinstance(structure_node, dict):
        return 0
    if structure_node.get('type') == 'file':
        return structure_node.get('size_bytes', 0)
    
    total_size = 0
    for child_node in structure_node.values():
        total_size += calculate_node_size(child_node)
    return total_size

def transform_structure_to_tree(structure_node, relations_nodes, path_prefix=''):
    """
    Bygger rekursivt en ren trädstruktur från file_structure och relations_nodes,
    och berikar varje nod med dess storlek.
    """
    children = []
    
    sorted_items = sorted(
        structure_node.items(),
        key=lambda item: (item[1].get('type', 'directory') != 'directory', item[0])
    )

    for name, node in sorted_items:
        if not isinstance(node, dict): continue

        current_path = f"{path_prefix}/{name}" if path_prefix else name
        
        node_size = calculate_node_size(node)

        new_node = {
            "name": name,
            "path": node.get("path", current_path),
            "type": node.get("type", "directory"),
            "size": node_size
        }

        if new_node["type"] == "file":
            relations_data = relations_nodes.get(new_node["path"], {})
            tags = []
            
            if relations_data.get('category'):
                tags.append(relations_data['category'])
            
            if tags:
                new_node['tags'] = tags
        else: # Directory
            new_node["children"] = transform_structure_to_tree(node, relations_nodes, current_path)
        
        children.append(new_node)
        
    return children

def build_ui(html_output_path, file_tree_json_string, project_overview):
    """
    Genererar HTML, CSS och den sammansatta JS-filen.
    """
    output_dir = os.path.dirname(html_output_path)
    css_output_path = os.path.join(output_dir, 'styles.css')
    js_output_path = os.path.join(output_dir, 'logic.js')
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    js_safe_string_literal = json.dumps(file_tree_json_string)
    js_config_string = json.dumps(project_overview)
    
    file_tree_placeholder = '__INJECT_FILE_TREE__'
    injected_js_tree_logic = JS_FILE_TREE_LOGIC.replace(file_tree_placeholder, js_safe_string_literal)

    config_placeholder = '__INJECT_PROJECT_OVERVIEW__';
    injected_js_logic = JS_LOGIC.replace(config_placeholder, js_config_string)
    
    final_js_logic = injected_js_logic + " " + injected_js_tree_logic + " " + JS_PERFORMANCE_LOGIC

    with open(html_output_path, 'w', encoding='utf-8') as f: f.write(HTML_TEMPLATE)
    with open(css_output_path, 'w', encoding='utf-8') as f: f.write(CSS_STYLES)
    with open(js_output_path, 'w', encoding='utf-8') as f: f.write(final_js_logic)

    with open(js_output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if file_tree_placeholder in content:
        raise RuntimeError(f"FATAL: Platshållaren '{file_tree_placeholder}' ersattes inte i den slutgiltiga JS-filen.")
    if config_placeholder in content:
        raise RuntimeError(f"FATAL: Platshållaren '{config_placeholder}' ersattes inte i den slutgiltiga JS-filen.")
    
    print(f"UI-filer (HTML, CSS, JS) har skapats i mappen: {os.path.abspath(output_dir)}")


def main():
    """Huvudfunktion som parsar argument, transformerar data och bygger UI."""
    if len(sys.argv) != 6:
        print("Fel: build-ui kräver exakt fyra argument.", file=sys.stderr)
        print("Användning: build-ui <command> <output_html_path> <context_json_path> <relations_json_path> <project_overview_json_path>", file=sys.stderr)
        sys.exit(1)
        
    output_path = sys.argv[2]
    context_json_path = sys.argv[3]
    relations_json_path = sys.argv[4]
    project_overview_json_path = sys.argv[5]

    try:
        print("Läser in datakällor...")
        with open(context_json_path, 'r', encoding='utf-8') as f:
            file_structure = json.load(f).get("file_structure", {})
        with open(relations_json_path, 'r', encoding='utf-8') as f:
            relations_nodes = json.load(f).get("graph_data", {}).get("nodes", {})
        with open(project_overview_json_path, 'r', encoding='utf-8') as f:
            project_overview = json.load(f)

        print("Bygger och berikar trädstruktur...")
        
        tree_children = transform_structure_to_tree(file_structure, relations_nodes)
        root_node = {'name': 'root', 'type': 'directory', 'path': '.', 'children': tree_children}
        
        file_tree_json_string = json.dumps(root_node, ensure_ascii=False)
        
        print("Genererar UI-filer...")
        build_ui(output_path, file_tree_json_string, project_overview)
        
        print("Klar. UI med dynamiskt filträd har genererats.")

    except Exception as e:
        print(f"Ett oväntat fel uppstod under build-ui: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'build-ui':
        main()
    else:
        print("Användning: python scripts/engrove_audio_tools_creator.py build-ui <output_html_path> <context_json_path> <relations_json_path> <project_overview_json_path>")
        sys.exit(1)

# scripts/engrove_audio_tools_creator.py
