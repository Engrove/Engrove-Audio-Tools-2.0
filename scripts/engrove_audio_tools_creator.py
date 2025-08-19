# BEGIN FILE: scripts/engrove_audio_tools_creator.py
# scripts/engrove_audio_tools_creator.py
# === SYFTE & ANSVAR ===
# Detta är ett centralt byggverktyg. Det genererar ett interaktivt UI baserat på
# projektets filstruktur och metadata.
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
# * v10.0 (2025-08-19): (Help me God - Domslut) Omarbetad för att ta bort statisk injicering av context.json. UI-logiken kommer nu att hämta denna fil asynkront.
# * SHA256_LF: UNVERIFIED
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Denna fil har modifierats enligt en grundorsaksanalys.
# - Help me God: Den bräckliga datainjektionsmetoden har ersatts med en robust, asynkron arkitektur.

import os
import sys
import json
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
from modules.ui_file_tree import JS_FILE_TREE_LOGIC
from modules.ui_performance_dashboard import JS_PERFORMANCE_LOGIC
from modules.ui_einstein_search import JS_EINSTEIN_LOGIC

def calculate_node_size(node):
    """Beräknar rekursivt storleken på en nod (fil eller mapp)."""
    if node['type'] == 'file':
        return node.get('size_bytes', 0)
    elif node['type'] == 'directory':
        total_size = 0
        for child in node.get('children', []):
            total_size += calculate_node_size(child)
        node['size_bytes'] = total_size
        return total_size
    return 0

def transform_structure_to_tree(structure, path_prefix=""):
    """Icke-destruktiv, rekursiv funktion för att omvandla den platta strukturen till ett träd."""
    tree = []
    for name, node_data in structure.items():
        current_path = os.path.join(path_prefix, name)
        if node_data['type'] == 'directory':
            children = transform_structure_to_tree(node_data.get('children', {}), current_path)
            tree.append({
                'name': name,
                'path': current_path,
                'type': 'directory',
                'children': children,
                'size_bytes': node_data.get('size_bytes', 0)
            })
        else:
            tree.append({
                'name': name,
                'path': current_path,
                'type': 'file',
                'size_bytes': node_data.get('size_bytes', 0),
                'category': node_data.get('category', 'unknown')
            })
    return tree

def build_ui(output_path, context_path, relations_path, overview_path, core_info_path):
    """Huvudfunktion för att bygga UI."""
    try:
        print("Läser in datakällor...")
        with open(context_path, 'r', encoding='utf-8') as f:
            context_data = json.load(f)
        with open(relations_path, 'r', encoding='utf-8') as f:
            file_relations_data = json.load(f)
        with open(overview_path, 'r', encoding='utf-8') as f:
            project_overview_data = json.load(f)
        with open(core_info_path, 'r', encoding='utf-8') as f:
            core_file_info_data = json.load(f)

        print("Bygger och berikar trädstruktur...")
        file_structure = context_data.get('file_structure', {})
        for name, node in file_structure.items():
            calculate_node_size(node)
        
        tree_data = transform_structure_to_tree(file_structure)
        js_tree_string = json.dumps(tree_data, ensure_ascii=False)
        
        print("Genererar UI-filer...")
        
        # Injektion av datakällor
        js_file_relations_string = json.dumps(file_relations_data)
        js_core_file_info_string = json.dumps(core_file_info_data)
        js_project_overview_string = json.dumps(project_overview_data)

        # Kombinera och ersätt platshållare i JS-moduler
        js_file_tree_content = JS_FILE_TREE_LOGIC.replace(
            "__FILE_TREE_DATA_PLACEHOLDER__", js_tree_string
        )
        
        js_einstein_content = JS_EINSTEIN_LOGIC.replace(
            "'__EINSTEIN_CORE_FILE_INFO_PLACEHOLDER__'", js_core_file_info_string
        )

        js_logic_content = JS_LOGIC.replace(
            "'__PROJECT_OVERVIEW_PLACEHOLDER__'", js_project_overview_string
        )

        # Skapa den slutgiltiga HTML-filen
        html_content = HTML_TEMPLATE.replace(
            "<!-- {{STYLES_PLACEHOLDER}} -->", f"<style>{CSS_STYLES}</style>"
        ).replace(
            "<!-- {{LOGIC_PLACEHOLDER}} -->", 
            f"<script type=\\\"module\\\">\\n{js_file_tree_content}\\n{js_logic_content}\\n{js_performance_dashboard_content}\\n{js_einstein_content}\\n</script>"
        ).replace(
            "{{VERSION_PLACEHOLDER}}", project_overview_data.get('last_updated_at', 'N/A')
        )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    except Exception as e:
        print(f"Ett oväntat fel uppstod under build-ui: {e}")
        sys.exit(1)

def main():
    """Hanterar kommandoradsargument."""
    if len(sys.argv) > 1 and sys.argv[1] == 'build-ui':
        if len(sys.argv) != 7:
            print("Användning: python engrove_audio_tools_creator.py build-ui <output_html> <context_json> <relations_json> <overview_json> <core_info_json>")
            sys.exit(1)
        build_ui(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    else:
        print("Okänt kommando. Använd 'build-ui'.")
        sys.exit(1)

if __name__ == '__main__':
    main()

# END FILE: scripts/engrove_audio_tools_creator.py
