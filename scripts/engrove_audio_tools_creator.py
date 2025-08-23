# scripts/engrove_audio_tools_creator.py
#
# === SYFTE & ANSVAR ===
# Genererar ett komplett, självbärande UI (index2.html + bundlade JS/CSS-filer)
# för AI Context Builder. Skriptet injicerar data som JS-litteraler och
# synkar med modulernas platshållare.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse.
# * v5.4 (2025-08-16): (EXTERN DOM #2) Korrigerat semikolon-injektion.
# * v6.0 (2025-08-16): (EXTERN DOM #3 - Grundorsaksanalys) Ersatt buggig, destruktiv
#   enrich_tree_recursive med icke-destruktiv transform_structure_to_tree.
# * v6.1 (2025-08-16): Deterministisk ordning på metadata-taggar.
# * v6.2 (2025-08-16): Injektering av project_overview och enbart category-tagg.
# * v6.3 (2025-08-17): Korrigerad file_tree_placeholder -> matchar bare-word-variabel.
# * v7.0 (2025-08-17): Rekursiv storleksberäkning.
# * v7.1 (2025-08-17): Import av ui_performance_dashboard.
# * v8.0 (2025-08-17): (Help me God - Domslut) JSON.parse borttagen (injekterar objekt).
# * v9.0 (2025-08-18): Injekterar ui_einstein_search och core_file_info.json.
# * v10.0 (2025-08-19): NameError-fix för js_full_context_string.
# * v10.1 (2025-08-19): Återställd trunkerad logik och full injektion av context.json.
# * v10.2 (2025-08-23): Root-safe calculate_node_size och robust relationsindex.
# * v10.3 (2025-08-23): (KRITISK) Fixar tokens, struktur & assets:
#   - Korrekt platshållare: __INJECT_FILE_TREE__ / __INJECT_*PAYLOAD__ (utan citattecken)
#   - FILE_TREE_DATA får formen { children: [...] } + "size"
#   - Skriv ut styles.css, logic.js, file_tree.js, einstein.js (404-fix)
#   - Injektera extra <script type="module">-taggar före </body>
#   - HTML-version formatteras via .format(version=...)
# * v10.3.1 (2025-08-23): Fixar SyntaxError '_meta' — injicerar **sträng**-payloads i logic.js
#   (kompatibelt med JSON.parse), objekt i file_tree.js och einstein.js lämnas oförändrade.
# * v10.3.2 (2025-08-23): Säkerställer att logic.js laddas som ES-modul och injicerar payloads
#   som objekt i samtliga moduler.
# * SHA256_LF: UNVERIFIED
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Korrigeringar efter rotorsaksanalys.
# - Help me God: Eliminering av platshållar-mismatch, 404 och ES-module-fel.

import os
import sys
import json
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
from modules.ui_file_tree import JS_FILE_TREE_LOGIC
from modules.ui_performance_dashboard import JS_PERFORMANCE_LOGIC
from modules.ui_einstein_search import JS_EINSTEIN_LOGIC

UI_VERSION = "10.3.2"

def _is_node(obj):
    return isinstance(obj, dict) and 'type' in obj

def calculate_node_size(node):
    if not isinstance(node, dict):
        return 0
    if _is_node(node):
        if node.get('type') == 'file':
            return node.get('size_bytes', 0)
        total = 0
        for child in node.get('children', {}).values():
            total += calculate_node_size(child)
        node['size_bytes'] = total
        return total
    total = 0
    for child in node.values():
        total += calculate_node_size(child)
    return total

def _build_relations_index(relations_data):
    nodes = relations_data.get("graph_data", {}).get("nodes", {})
    if isinstance(nodes, dict):
        return nodes
    index = {}
    if isinstance(nodes, list):
        for n in nodes:
            p = n.get('id') or n.get('path') or n.get('name')
            if p:
                index[p] = n
    return index

def transform_structure_to_tree(structure, relations_nodes, path_prefix=''):
    tree = []
    sorted_items = sorted(
        structure.items(),
        key=lambda item: (item[1].get('type', 'directory') != 'directory', item[0])
    )
    for name, node in sorted_items:
        current_path = os.path.join(path_prefix, name) if path_prefix else name
        tags = []
        if node.get('type') == 'file':
            rel = relations_nodes.get(current_path, {}) or {}
            cat = rel.get('category')
            if cat:
                tags.append(cat)
        size_bytes = node.get('size_bytes', 0)
        tree_node = {
            "name": name,
            "path": current_path,
            "type": node.get('type', 'directory'),
            "tags": tags,
            "size": size_bytes
        }
        if node.get('type') == 'directory':
            children = node.get('children', {}) or {}
            tree_node["children"] = transform_structure_to_tree(children, relations_nodes, current_path)
        tree.append(tree_node)
    return tree

def _write_text(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def _inject_js_object(js_source: str, placeholder: str, obj) -> str:
    payload = json.dumps(obj, ensure_ascii=False)
    return js_source.replace(placeholder, payload)

def _inject_scripts_into_html(html: str, extra_script_tags: str) -> str:
    insertion_point = html.rfind("</body>")
    if insertion_point == -1:
        return html + extra_script_tags
    return html[:insertion_point] + extra_script_tags + html[insertion_point:]

def build_ui(output_html_path, context_data, relations_data, overview_data, core_info_data):
    try:
        file_structure = context_data.get('file_structure', {}) or {}
        relations_index = _build_relations_index(relations_data)
        calculate_node_size(file_structure)
        file_tree_list = transform_structure_to_tree(file_structure, relations_index)
        file_tree_payload = {"children": file_tree_list}
        final_js_logic = JS_LOGIC
        final_js_logic = _inject_js_object(final_js_logic, "__INJECT_CONTEXT_JSON_PAYLOAD__", context_data)
        final_js_logic = _inject_js_object(final_js_logic, "__INJECT_RELATIONS_JSON_PAYLOAD__", relations_data)
        final_js_logic = _inject_js_object(final_js_logic, "__INJECT_OVERVIEW_JSON_PAYLOAD__", overview_data)
        final_js_file_tree = _inject_js_object(JS_FILE_TREE_LOGIC, "__INJECT_FILE_TREE__", file_tree_payload)
        final_js_einstein = _inject_js_object(JS_EINSTEIN_LOGIC, "__INJECT_CORE_FILE_INFO__", core_info_data)
        out_dir = os.path.dirname(output_html_path) or "."
        _write_text(os.path.join(out_dir, "styles.css"), CSS_STYLES)
        _write_text(os.path.join(out_dir, "logic.js"), final_js_logic)
        _write_text(os.path.join(out_dir, "file_tree.js"), final_js_file_tree)
        _write_text(os.path.join(out_dir, "einstein.js"), final_js_einstein)
        _write_text(os.path.join(out_dir, "perf.js"), JS_PERFORMANCE_LOGIC)
        version_tag = f"{(overview_data.get('repository') or 'Engrove/Engrove-Audio-Tools-2.0').split('/')[-1]} - UI v{UI_VERSION}"
        html_content = HTML_TEMPLATE.format(version=version_tag)
        extra_tags = (
            "\n    <script type='module' src='logic.js'></script>"
            "\n    <script type='module' src='file_tree.js'></script>"
            "\n    <script type='module' src='einstein.js'></script>"
            "\n    <script type='module' src='perf.js'></script>\n"
        )
        html_content = _inject_scripts_into_html(html_content, extra_tags)
        _write_text(output_html_path, html_content)
        print("UI byggt framgångsrikt.")
    except Exception as e:
        print(f"Ett oväntat fel uppstod under build-ui: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'build-ui':
        if len(sys.argv) != 7:
            print("Användning: python engrove_audio_tools_creator.py build-ui <output_html> <context_json> <relations_json> <overview_json> <core_info_json>", file=sys.stderr)
            sys.exit(1)
        try:
            with open(sys.argv[3], 'r', encoding='utf-8') as f:
                context_data = json.load(f)
            with open(sys.argv[4], 'r', encoding='utf-8') as f:
                relations_data = json.load(f)
            with open(sys.argv[5], 'r', encoding='utf-8') as f:
                overview_data = json.load(f)
            with open(sys.argv[6], 'r', encoding='utf-8') as f:
                core_info_data = json.load(f)
            build_ui(sys.argv[2], context_data, relations_data, overview_data, core_info_data)
        except Exception as e:
            print(f"Ett oväntat fel uppstod: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Okänt kommando. Tillgängliga kommandon: 'build-ui'")
        sys.exit(1)

if __name__ == "__main__":
    main()
