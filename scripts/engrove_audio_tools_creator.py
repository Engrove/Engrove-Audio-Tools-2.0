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
# * v10.3.3 (2025-08-23): (Help me God - Domslut) Återinför JSON.parse() för injicerade strängar i JS-moduler
#   och lägger till dynamisk hash till UI_VERSION för spårbarhet.
# * v10.4 (2025-08-23): (KRITISK STABILITET) Tvingar **stränglitteral-injektion** för alla JSON-payloads.
#   - Ny funktion _inject_js_string_literal() som alltid producerar korrekt citerad JS-sträng (single quotes),
#     med säker escapning av enkla citattecken.
#   - Fallback-replacer som hanterar tre varianter av platshållare i käll-JS:
#       '__TOKEN__', "__TOKEN__", __TOKEN__
#   - Validering: _verify_no_unresolved_placeholders() larmar om kvarvarande __INJECT__-tokens.
#   - Eliminerar SyntaxError: Unexpected identifier '_meta' och "[object Object] is not valid JSON"
#     när modulerna använder JSON.parse().
# * v10.4.1 (2025-08-23): (JS-litteralfix) Rör inte backslashes från json.dumps, escapa ENDAST enkla citattecken.
#   Förhindrar "missing ) after argument list".
# * v10.4.1-fallback (2025-08-23): Robust modulimport (stöd både scripts/modules och modules).
# * v11.0 (2025-08-23): (ARKITEKTURÄNDRING) Ersatt den bräckliga stränginjektionen med en robust "Data Island"-metod.
#   - Datan serialiseras till JSON och bäddas in i <script type="application/json">-taggar i HTML:en.
#   - JavaScript-moduler läser nu sin data från DOM istället för från injicerade variabler.
#   - Detta eliminerar alla komplexa escaping-problem och löser grundorsaken till `SyntaxError`.
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Korrigeringar efter rotorsaksanalys.
# - Help me God: Eliminering av platshållar-mismatch, 404 och ES-module-fel.
# - GR7 (Fullständig Historik): Historiken uppdaterad.

import os
import sys
import json
import re
import hashlib
import html
from datetime import datetime

# --- robust modulimport (stöd både scripts/modules och modules) ---
try:
    # Vanlig layout i repo (körs från repo-rot): scripts/modules/...
    from modules.ui_template import HTML_TEMPLATE
    from modules.ui_styles import CSS_STYLES
    from modules.ui_logic import JS_LOGIC
    from modules.ui_file_tree import JS_FILE_TREE_LOGIC
    from modules.ui_performance_dashboard import JS_PERFORMANCE_LOGIC
    from modules.ui_einstein_search import JS_EINSTEIN_LOGIC
except ModuleNotFoundError:
    # Direktkörning bredvid filen: lägg till scripts/modules på sys.path och importera utan prefix
    _BASE = os.path.dirname(os.path.abspath(__file__))
    _MOD = os.path.join(_BASE, "modules")
    if _MOD not in sys.path:
        sys.path.insert(0, _MOD)
    from ui_template import HTML_TEMPLATE
    from ui_styles import CSS_STYLES
    from ui_logic import JS_LOGIC
    from ui_file_tree import JS_FILE_TREE_LOGIC
    from ui_performance_dashboard import JS_PERFORMANCE_LOGIC
    from ui_einstein_search import JS_EINSTEIN_LOGIC

# Lägger till en kort hash av aktuell tidsstämpel i UI_VERSION
UI_VERSION = f"11.0-{hashlib.sha256(datetime.now().isoformat().encode()).hexdigest()[:6]}"


def _is_node(obj):
    return isinstance(obj, dict) and 'type' in obj


def calculate_node_size(node):
    """
    Summerar storlek (size_bytes) rekursivt för katalognoder.
    Sätter 'size_bytes' på kataloger och returnerar bytes.
    """
    if not isinstance(node, dict):
        return 0
    if _is_node(node):
        if node.get('type') == 'file':
            return node.get('size_bytes', 0)
        total = 0
        for child in (node.get('children', {}) or {}).values():
            total += calculate_node_size(child)
        node['size_bytes'] = total
        return total
    total = 0
    for child in node.values():
        total += calculate_node_size(child)
    return total


def _build_relations_index(relations_data):
    """
    Normaliserar relationsgrafens nodindex till en dict { path: node }.
    Accepterar både dict och list i relations_data['graph_data']['nodes'].
    """
    nodes = (relations_data.get("graph_data", {}) or {}).get("nodes", {})
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
    Omvandlar den hierarkiska file_structure till en lista av trädnoder för UI:t.
    Lägger till 'tags' (t.ex. category) och 'size' (bytes).
    """
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
    os.makedirs(os.path.dirname(path), exist_ok=True
                if os.path.dirname(path) else True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def _create_data_island_script_tag(dom_id: str, data_obj) -> str:
    """
    Serialiserar ett Python-objekt till en JSON-sträng och bäddar in det
    i en säker <script type="application/json">-tagg.
    Hanterar HTML-specifik escaping.
    """
    json_string = json.dumps(data_obj, ensure_ascii=False, separators=(',', ':'))
    
    # KRITISK SÄKERHETSÅTGÄRD: Förhindra att strängen "</script>" i datan
    # av misstag avslutar HTML-taggen. Ersätt med en säker variant.
    safe_json_string = json_string.replace('</script>', '<\\/script>')
    
    return f'<script type="application/json" id="{html.escape(dom_id)}">{safe_json_string}</script>'


def build_ui(output_html_path, context_data, relations_data, overview_data, core_info_data):
    try:
        # 1) Beräkna storlekar & bygg relationsindex
        file_structure = context_data.get('file_structure', {}) or {}
        relations_index = _build_relations_index(relations_data)
        calculate_node_size(file_structure)

        # 2) Transformera till UI-vänligt filträd
        file_tree_list = transform_structure_to_tree(file_structure, relations_index)
        file_tree_payload = {"children": file_tree_list}
        
        # 3) Skapa alla data island-taggar
        data_islands = [
            _create_data_island_script_tag('data-island-context', context_data),
            _create_data_island_script_tag('data-island-relations', relations_data),
            _create_data_island_script_tag('data-island-overview', overview_data),
            _create_data_island_script_tag('data-island-core-info', core_info_data),
            _create_data_island_script_tag('data-island-file-tree', file_tree_payload)
        ]
        data_islands_html = "\n    ".join(data_islands)

        # 4) Skriv ut de rena (icke-injicerade) JS- och CSS-filerna
        out_dir = os.path.dirname(output_html_path) or "."
        _write_text(os.path.join(out_dir, "styles.css"), CSS_STYLES)
        _write_text(os.path.join(out_dir, "logic.js"), JS_LOGIC)
        _write_text(os.path.join(out_dir, "file_tree.js"), JS_FILE_TREE_LOGIC)
        _write_text(os.path.join(out_dir, "einstein.js"), JS_EINSTEIN_LOGIC)
        _write_text(os.path.join(out_dir, "perf.js"), JS_PERFORMANCE_LOGIC)

        # 5) Sammansätt HTML, injicera data islands och script-taggar
        repo_name = (overview_data.get('repository') or 'Engrove/Engrove-Audio-Tools-2.0').split('/')[-1]
        version_tag = f"{repo_name} - UI v{UI_VERSION}"
        html_content = HTML_TEMPLATE.format(version=version_tag)
        
        # Injicera data islands
        html_content = html_content.replace(
            '<!-- __INJECT_DATA_ISLANDS__ -->', 
            data_islands_html
        )
        
        # Inkludera alla JS-moduler
        extra_tags = (
            "\n    <script type='module' src='file_tree.js'></script>"
            "\n    <script type='module' src='einstein.js'></script>"
            "\n    <script type='module' src='perf.js'></script>\n"
        )
        # Ersätt den gamla, enskilda logic.js-taggen med den nya listan
        html_content = html_content.replace(
            '<script type="module" src="logic.js"></script>',
            '<script type="module" src="logic.js"></script>' + extra_tags
        )

        _write_text(output_html_path, html_content)

        print("UI byggt framgångsrikt med robust 'Data Island'-metod.")
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
