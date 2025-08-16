# scripts/engrove_audio_tools_creator.py
#
# === SYFTE & ANSVAR ===
# Detta är ett centralt byggverktyg. Det kan generera UI-filer eller
# konvertera datakällor baserat på kommandoradsargument.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse.
# * v4.0 (2025-08-16): (Help me God) Omstrukturerad för att vara både kommandodriven och bakåtkompatibel.
# * v5.0 (2025-08-16): ARKITEKTURUPPGRADERING: Implemented modular file tree logic.
# * v5.1 (2025-08-16): KRITISK FIX: Ändrat datainjektion till att använda en escapad JSON-sträng
#   och `JSON.parse()` i JS för att förhindra syntaxfel.
# * v5.2 (2025-08-16): (Help me God - Domslut) Implementerat dubbel JSON-serialisering för att skapa en
#   garanterat säker JavaScript-strängliteral. Lade till en självkontroll för att verifiera
#   att platshållaren har ersatts, vilket slutgiltigt löser `SyntaxError`.
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Help me God: Denna fix är ett direkt resultat av ett externt domslut efter flera misslyckanden.
# - Heuristik H-20250816-02: En ny självkontroll har lagts till för att verifiera att injektionen lyckats.

import os
import sys
import json
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
from modules.ui_file_tree import JS_FILE_TREE_LOGIC

def enrich_tree_recursive(current_node, name, relations_nodes):
    """
    Traverserar rekursivt den nästlade filstrukturen och lägger till metadata.
    """
    if not isinstance(current_node, dict):
        return

    current_node['name'] = name

    if current_node.get("type") == "file":
        path = current_node.get("path")
        if path and path in relations_nodes:
            node_meta = relations_nodes[path]
            tags = []
            if node_meta.get('category'):
                tags.append(node_meta['category'])
            crit_score = node_meta.get('criticality_score')
            if isinstance(crit_score, (int, float)):
                tags.append(f"crit:{crit_score:.0f}%")
            if tags:
                current_node['tags'] = sorted(tags)
    else: # Directory
        children_items = sorted(
            [(k, v) for k, v in current_node.items() if isinstance(v, dict)],
            key=lambda item: (item[1].get('type', 'directory') != 'directory', item[0])
        )
        
        current_node['children'] = [v for k, v in children_items]
        
        original_keys = [k for k, v in children_items]
        for key in original_keys:
            if key in current_node:
                del current_node[key]

        for i, child_node in enumerate(current_node['children']):
            child_name = children_items[i][0]
            enrich_tree_recursive(child_node, child_name, relations_nodes)


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
    final_js_logic = JS_LOGIC + "\\n\\n" + injected_js_tree_logic

    with open(html_output_path, 'w', encoding='utf-8') as f: f.write(HTML_TEMPLATE)
    with open(css_output_path, 'w', encoding='utf-8') as f: f.write(CSS_STYLES)
    with open(js_output_path, 'w', encoding='utf-8') as f: f.write(final_js_logic)

    # Verifieringssteg enligt Heuristik H-20250816-02
    with open(js_output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if placeholder in content:
        raise RuntimeError(f"FATAL: Platshållaren '{placeholder}' ersattes inte i den slutgiltiga JS-filen.")
    
    print(f"UI-filer (HTML, CSS, JS) har skapats i mappen: {os.path.abspath(output_dir)}")


def main():
    """Huvudfunktion som parsar argument, transformerar data och bygger UI."""
    if len(sys.argv) < 2:
        print("Fel: Ett kommando måste anges.", file=sys.stderr)
        print("Användning: python scripts/engrove_audio_tools_creator.py build-ui <output_html> <context_json> <relations_json>", file=sys.stderr)
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "build-ui":
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
            
            root_node = {'name': 'root', 'type': 'directory', 'path': '.', 'children_dict': file_structure}
            enrich_tree_recursive(root_node['children_dict'], 'root', relations_nodes)

            children_items = sorted(
                [(k, v) for k, v in root_node['children_dict'].items() if isinstance(v, dict)],
                key=lambda item: (item[1].get('type', 'directory') != 'directory', item[0])
            )
            root_node['children'] = [v for k,v in children_items]
            del root_node['children_dict']
            
            file_tree_json_string = json.dumps(root_node, ensure_ascii=False)
            
            print("Genererar UI-filer...")
            build_ui(output_path, file_tree_json_string)
            
            print("\\nKlar. UI med dynamiskt filträd har genererats.")

        except Exception as e:
            print(f"Ett oväntat fel uppstod under build-ui: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Okänt kommando: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

# scripts/engrove_audio_tools_creator.py
