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
# * SHA256_LF: UNVERIFIED
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Korrigeringar efter rotorsaksanalys.
# - Help me God: Eliminering av platshållar-mismatch och 404 på statiska resurser.

import os
import sys
import json

from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
from modules.ui_file_tree import JS_FILE_TREE_LOGIC
from modules.ui_performance_dashboard import JS_PERFORMANCE_LOGIC
from modules.ui_einstein_search import JS_EINSTEIN_LOGIC

UI_VERSION = "10.3.1"


def _is_node(obj):
    """True om obj liknar en nod med 'type'."""
    return isinstance(obj, dict) and 'type' in obj


def _iter_children(node):
    """Iterator över barn oavsett representation."""
    if not isinstance(node, dict):
        return []
    if _is_node(node):
        return node.get('children', {}).values()
    # top-level mapping: namn -> nod
    return node.values()


def calculate_node_size(node):
    """
    Rot-säker storleksberäkning.
    - Om node är en mappnings-rot (utan 'type'): summera alla barn.
    - Om node är en nod med 'type': hantera fil/dir.
    - Annars: 0.
    """
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

    # Top-level mapping (rot utan 'type')
    total = 0
    for child in node.values():
        total += calculate_node_size(child)
    return total


def _build_relations_index(relations_data):
    """
    Normaliserar relationsnoder till en dict indexerad på sökväg.
    Stödjer både:
      - dict: { "<path>": {...} }
      - list: [ {"id"|"path"|"name": "<path>", ...}, ... ]
    """
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
    """
    Omvandlar context.file_structure (mapping) till en UI-trädstruktur.
    Returnerar en LISTA av barn (inte ett topp-objekt). Denna lista kommer
    senare kapslas i {"children": [...]} för att matcha UI-modulen.
    """
    tree = []
    # sortera mappar före filer, sedan alfabetiskt
    sorted_items = sorted(
        structure.items(),
        key=lambda item: (item[1].get('type', 'directory') != 'directory', item[0])
    )
    for name, node in sorted_items:
        current_path = os.path.join(path_prefix, name) if path_prefix else name

        # Taggar från relationsgrafen
        tags = []
        if node.get('type') == 'file':
            rel = relations_nodes.get(current_path, {}) or {}
            cat = rel.get('category')
            if cat:
                tags.append(cat)

        # Storlek
        size_bytes = node.get('size_bytes', 0)

        tree_node = {
            "name": name,
            "path": current_path,
            "type": node.get('type', 'directory'),
            "tags": tags,
            # UI:n förväntar sig 'size'
            "size": size_bytes
        }

        if node.get('type') == 'directory':
            children = node.get('children', {}) or {}
            tree_node["children"] = transform_structure_to_tree(children, relations_nodes, current_path)

        tree.append(tree_node)
    return tree


def _ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _write_text(path: str, content: str, encoding='utf-8'):
    _ensure_dir(path)
    with open(path, 'w', encoding=encoding) as f:
        f.write(content)


def _inject_scripts_into_html(html: str, extra_script_tags: str) -> str:
    """
    Infogar extra <script type="module" ...> precis före </body> om INJECT_* placeholders saknas.
    """
    insertion_point = html.rfind("</body>")
    if insertion_point == -1:
        return html + extra_script_tags
    return html[:insertion_point] + extra_script_tags + html[insertion_point:]


def build_ui(output_html_path, context_data, relations_data, overview_data, core_info_data):
    try:
        print("Bygger och berikar trädstruktur...")
        file_structure = context_data.get('file_structure', {}) or {}
        relations_index = _build_relations_index(relations_data)

        # Rot-säker storleksberäkning och transform
        calculate_node_size(file_structure)
        file_tree_list = transform_structure_to_tree(file_structure, relations_index)
        file_tree_payload = {"children": file_tree_list}  # matcha UI-modulen

        print("Genererar JS/CSS-innehåll...")
        # 1) Objekt-serialisering
        js_full_context_obj = json.dumps(context_data, ensure_ascii=False)
        js_relations_obj = json.dumps(relations_data, ensure_ascii=False)
        js_overview_obj = json.dumps(overview_data, ensure_ascii=False)
        js_core_info_obj = json.dumps(core_info_data, ensure_ascii=False)
        js_file_tree_obj = json.dumps(file_tree_payload, ensure_ascii=False)

        # 2) Dubbel-serialisera till JS-strängar för logic.js (använder JSON.parse(...))
        ctx_str = json.dumps(js_full_context_obj, ensure_ascii=False)
        rel_str = json.dumps(js_relations_obj, ensure_ascii=False)
        ovw_str = json.dumps(js_overview_obj, ensure_ascii=False)

        # 3) Token-replacement
        final_js_logic = (JS_LOGIC
                          .replace("__INJECT_CONTEXT_JSON_PAYLOAD__", ctx_str)
                          .replace("__INJECT_RELATIONS_JSON_PAYLOAD__", rel_str)
                          .replace("__INJECT_OVERVIEW_JSON_PAYLOAD__", ovw_str))

        final_js_file_tree = JS_FILE_TREE_LOGIC.replace("__INJECT_FILE_TREE__", js_file_tree_obj)
        final_js_einstein = JS_EINSTEIN_LOGIC.replace("__INJECT_CORE_FILE_INFO__", js_core_info_obj)

        print("Skriver statiska tillgångar...")
        out_dir = os.path.dirname(output_html_path) or "."
        _write_text(os.path.join(out_dir, "styles.css"), CSS_STYLES)
        _write_text(os.path.join(out_dir, "logic.js"), final_js_logic)
        _write_text(os.path.join(out_dir, "file_tree.js"), final_js_file_tree)
        _write_text(os.path.join(out_dir, "einstein.js"), final_js_einstein)

        print("Sammansätter HTML...")
        version_tag = f"{(overview_data.get('repository') or 'Engrove/Engrove-Audio-Tools-2.0').split('/')[-1]} - UI v{UI_VERSION}"
        html_content = HTML_TEMPLATE.format(version=version_tag)

        extra_tags = (
            "\n    <script type='module' src='file_tree.js'></script>"
            "\n    <script type='module' src='einstein.js'></script>\n"
        )
        html_content = _inject_scripts_into_html(html_content, extra_tags)

        _write_text(output_html_path, html_content)

        print("Klar. UI med dynamiskt filträd har genererats.")
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
            with open(sys.argv[3], 'r', encoding='utf-8') as f:
                context_data = json.load(f)
            with open(sys.argv[4], 'r', encoding='utf-8') as f:
                relations_data = json.load(f)
            with open(sys.argv[5], 'r', encoding='utf-8') as f:
                overview_data = json.load(f)
            with open(sys.argv[6], 'r', encoding='utf-8') as f:
                core_info_data = json.load(f)

            build_ui(sys.argv[2], context_data, relations_data, overview_data, core_info_data)
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
