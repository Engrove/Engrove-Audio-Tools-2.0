# BEGIN FILE: scripts/engrove_audio_tools_creator.py
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
# * v8.0 (2025-08-17): (Help me God - Domslut) Refaktorerat datainjektionen. `JSON.parse` har tagits bort från `ui_file_tree.py`.
#   Detta skript injicerar nu ett direkt JS-objekt-literal, vilket löser `SyntaxError: "[object Object]" is not valid JSON`.
#   Lade även till hantering för versions-platshållaren i HTML-mallen.
# * v9.0 (2025-08-18): (Engrove Mandate) Modifierad för att importera och injicera den nya ui_einstein_search-modulen och dess datakälla (core_file_info.json).
# * v10.0 (2025-08-19): (Help me God - Domslut) Korrigerat ett NameError genom att korrekt definiera variabeln 'js_full_context_string' innan den används.
# * v10.1 (2025-08-19): (Help me God - Domslut) Återställt trunkerad logik och korrekt implementerat injicering av hela context.json.
# * SHA256_LF: 013731f125a9e948300225dc951451ca026b1dc08599ba3ed5c9ef46e129bb2d
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Denna fil har modifierats enligt en grundorsaksanalys.
# - Help me God: Felet var ett `NameError` som ledde till en katastrofal trunkering, vilket krävde en fullständig återställning och verifiering.

import os
import sys
import json
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
from modules.ui_file_tree import JS_FILE_TREE_LOGIC
from modules.ui_performance_dashboard import JS_PERFORMANCE_LOGIC
from modules.ui_einstein_search import JS_EINSTEIN_LOGIC

UI_VERSION = "10.1"

def calculate_node_size(node):
    if node['type'] == 'file':
        return node.get('size_bytes', 0)
    total_size = 0
    if 'children' in node:
        for child in node['children'].values():
            total_size += calculate_node_size(child)
    node['size_bytes'] = total_size
    return total_size

def transform_structure_to_tree(structure, relations_nodes, path_prefix=''):
    tree = []
    sorted_items = sorted(
        structure.items(),
        key=lambda item: (item[1].get('type', 'directory') != 'directory', item[0])
    )
    for name, node in sorted_items:
        current_path = os.path.join(path_prefix, name)
        tags = []
        if node['type'] == 'file':
            relations_data = relations_nodes.get(current_path, {})
            if relations_data.get('category'):
                tags.append(relations_data['category'])
        
        tree_node = {
            "name": name,
            "path": current_path,
            "type": node['type'],
            "tags": tags,
            "size_bytes": node.get('size_bytes', 0)
        }
        if node['type'] == 'directory':
            tree_node["children"] = transform_structure_to_tree(node.get('children', {}), relations_nodes, current_path)
        
        tree.append(tree_node)
    return tree

def build_ui(output_html_path, context_data, relations_data, overview_data, core_info_data):
    try:
        print("Bygger och berikar trädstruktur...")
        file_structure = context_data.get('file_structure', {})
        relations_nodes = relations_data.get("graph_data", {}).get("nodes", {})
        calculate_node_size(file_structure)
        file_tree_data = transform_structure_to_tree(file_structure, relations_nodes)

        print("Genererar UI-filer...")
        
        js_full_context_string = json.dumps(context_data)
        js_file_tree_string = json.dumps(file_tree_data)
        js_relations_string = json.dumps(relations_data)
        js_overview_string = json.dumps(overview_data)
        js_core_info_string = json.dumps(core_info_data)
        
        final_js_file_tree = JS_FILE_TREE_LOGIC.replace("`__INJECT_FILE_TREE_DATA__`", js_file_tree_string)
        
        final_js_logic = JS_LOGIC.replace("'__INJECT_CONTEXT_JSON_PAYLOAD__'", js_full_context_string)
        final_js_logic = final_js_logic.replace("'__INJECT_RELATIONS_JSON_PAYLOAD__'", js_relations_string)
        final_js_logic = final_js_logic.replace("'__INJECT_OVERVIEW_JSON_PAYLOAD__'", js_overview_string)

        final_einstein_logic = JS_EINSTEIN_LOGIC.replace("'__INJECT_CORE_FILE_INFO__'", js_core_info_string)

        version_tag = overview_data.get('repository', 'Engrove/Engrove-Audio-Tools-2.0').split('/')[-1]
        
        html_content = HTML_TEMPLATE
        html_content = html_content.replace("<!-- INJECT_STYLES -->", f"<style>{CSS_STYLES}</style>")
        html_content = html_content.replace("<!-- INJECT_LOGIC -->", f"<script type='module'>{final_js_logic}</script>")
        html_content = html_content.replace("<!-- INJECT_FILE_TREE_LOGIC -->", f"<script type='module'>{final_js_file_tree}</script>")
        html_content = html_content.replace("<!-- INJECT_PERFORMANCE_LOGIC -->", f"<script type='module'>{JS_PERFORMANCE_LOGIC}</script>")
        html_content = html_content.replace("<!-- INJECT_EINSTEIN_LOGIC -->", f"<script type='module'>{final_einstein_logic}</script>")
        html_content = html_content.replace("__VERSION_PLACEHOLDER__", f"{version_tag} - UI v{UI_VERSION}")

        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    except Exception as e:
        print(f"Ett oväntat fel uppstod under build-ui: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'build-ui':
        if len(sys.argv) != 7:
            print("Användning: python engrove_audio_tools_creator.py build-ui <output_html> <context_json> <relations_json> <overview_json> <core_info_json>", file=sys.stderr)
            sys.exit(1)
        
        try:
            print("Läser in datakällor...")
            with open(sys.argv[3], 'r', encoding='utf-8') as f: context_data = json.load(f)
            with open(sys.argv[4], 'r', encoding='utf-8') as f: relations_data = json.load(f)
            with open(sys.argv[5], 'r', encoding='utf-8') as f: overview_data = json.load(f)
            with open(sys.argv[6], 'r', encoding='utf-8') as f: core_info_data = json.load(f)
            
            build_ui(sys.argv[2], context_data, relations_data, overview_data, core_info_data)
            print("Klar. UI med dynamiskt filträd har genererats.")

        except FileNotFoundError as e:
            print(f"Fel: Kunde inte hitta en av indatafilerna: {e}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Fel: Kunde inte tolka en av JSON-filerna: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Ett oväntat fel uppstod: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Okänt kommando. Tillgängliga kommandon: 'build-ui'")
        sys.exit(1)

if __name__ == "__main__":
    main()

# END FILE: scripts/engrove_audio_tools_creator.py
