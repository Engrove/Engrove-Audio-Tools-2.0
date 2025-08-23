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
#     med säker escapning av backslash och enkla citattecken.
#   - Fallback-replacer som hanterar tre varianter av platshållare i käll-JS:
#       '__TOKEN__', "__TOKEN__", __TOKEN__
#   - Validering: _verify_no_unresolved_placeholders() larmar om kvarvarande __INJECT__-tokens.
#   - Detta eliminerar SyntaxError: Unexpected identifier '_meta' och "[object Object] is not valid JSON"
#     när modulerna använder JSON.parse().
# * v10.4.1 (2025-08-23): (JS-litteralfix) Ändrar escapningsstrategi för att eliminera
#   "missing ) after argument list": rör inte backslashes från json.dumps, escapa ENDAST enkla citattecken.
#   Detta förhindrar över-escapning av \\ som kunde spräcka stränglitteralen i JS.
# * SHA256_LF: UNVERIFIED
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Korrigeringar efter rotorsaksanalys.
# - Help me God: Eliminering av platshållar-mismatch, 404 och ES-module-fel.
# - GR7 (Fullständig Historik): Historiken har uppdaterats korrekt.

import os
import sys
import json
import re
import hashlib
from datetime import datetime
from modules.ui_template import HTML_TEMPLATE
from modules.ui_styles import CSS_STYLES
from modules.ui_logic import JS_LOGIC
from modules.ui_file_tree import JS_FILE_TREE_LOGIC
from modules.ui_performance_dashboard import JS_PERFORMANCE_LOGIC
from modules.ui_einstein_search import JS_EINSTEIN_LOGIC

# Lägger till en kort hash av aktuell tidsstämpel i UI_VERSION
UI_VERSION = f"10.4.1-{hashlib.sha256(datetime.now().isoformat().encode()).hexdigest()[:6]}"

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
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def _to_js_single_quoted_string(json_text: str) -> str:
    """
    Gör om JSON-text (från json.dumps) till en säker JS-strängliteral.
    - Ändra inte backslashes: json.dumps har redan korrekta escape-sekvenser.
    - Escapa ENDAST enkla citattecken så att omslutande '...' inte spräcks.
    """
    safe_json = json_text.replace("'", "\\'")
    return f"'{safe_json}'"

def _inject_js_string_literal(js_source: str, placeholder: str, obj) -> str:
    """
    Ersätter alla förekomster av placeholdern (tre varianter) med en **strängliteral**:
      '__TOKEN__'  |  "__TOKEN__"  |  __TOKEN__
    där strängliteral = '...json...' (single quotes), avsedd för JSON.parse().
    """
    # Serialisera Python-objekt till JSON-text (med dubbla citattecken)
    json_text = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    js_literal = _to_js_single_quoted_string(json_text)

    # Bygg tre säkra regex-varianter
    # 1) 'PLACEHOLDER'
    pat1 = re.compile(re.escape("'" + placeholder + "'"))
    # 2) "PLACEHOLDER"
    pat2 = re.compile(re.escape('"' + placeholder + '"'))
    # 3) PLACEHOLDER (bar token)
    #    Matcha endast om token inte redan omges av bokstäver/siffror/underscore
    pat3 = re.compile(rf'(?<![\w]){re.escape(placeholder)}(?![\w])')

    js_source = pat1.sub(js_literal, js_source)
    js_source = pat2.sub(js_literal, js_source)
    js_source = pat3.sub(js_literal, js_source)
    return js_source

def _verify_no_unresolved_placeholders(*assets: str) -> None:
    """
    Skannar givna textassets och varnar om __INJECT__-platshållare finns kvar.
    Stoppar inte builden, men skriver tydlig varning till STDERR.
    """
    unresolved = []
    inject_re = re.compile(r'__INJECT_[A-Z0-9_]+__')
    for idx, text in enumerate(assets):
        hits = inject_re.findall(text or '')
        if hits:
            unresolved.append((idx, sorted(set(hits))))
    if unresolved:
        sys.stderr.write("VARNING: Oersatta __INJECT__-platshållare upptäckta:\n")
        for idx, tokens in unresolved:
            sys.stderr.write(f"  - Asset[{idx}]: {', '.join(tokens)}\n")

def build_ui(output_html_path, context_data, relations_data, overview_data, core_info_data):
    try:
        # 1) Beräkna storlekar & bygg relationsindex
        file_structure = context_data.get('file_structure', {}) or {}
        relations_index = _build_relations_index(relations_data)
        calculate_node_size(file_structure)

        # 2) Transformera till UI-vänligt filträd
        file_tree_list = transform_structure_to_tree(file_structure, relations_index)
        file_tree_payload = {"children": file_tree_list}

        # 3) Injicera **stränglitteraler** (för JSON.parse) i samtliga JS-moduler
        final_js_logic = _inject_js_string_literal(JS_LOGIC, "__INJECT_CONTEXT_JSON_PAYLOAD__", context_data)
        final_js_logic = _inject_js_string_literal(final_js_logic, "__INJECT_RELATIONS_JSON_PAYLOAD__", relations_data)
        final_js_logic = _inject_js_string_literal(final_js_logic, "__INJECT_OVERVIEW_JSON_PAYLOAD__", overview_data)

        final_js_file_tree = _inject_js_string_literal(JS_FILE_TREE_LOGIC, "__INJECT_FILE_TREE__", file_tree_payload)
        final_js_einstein  = _inject_js_string_literal(JS_EINSTEIN_LOGIC, "__INJECT_CORE_FILE_INFO__", core_info_data)

        # 4) Skriv ut assets
        out_dir = os.path.dirname(output_html_path) or "."
        _write_text(os.path.join(out_dir, "styles.css"), CSS_STYLES)
        _write_text(os.path.join(out_dir, "logic.js"), final_js_logic)
        _write_text(os.path.join(out_dir, "file_tree.js"), final_js_file_tree)
        _write_text(os.path.join(out_dir, "einstein.js"), final_js_einstein)
        _write_text(os.path.join(out_dir, "perf.js"), JS_PERFORMANCE_LOGIC)

        # 5) Sammansätt HTML och injicera script-taggar (type=module)
        repo_name = (overview_data.get('repository') or 'Engrove/Engrove-Audio-Tools-2.0').split('/')[-1]
        version_tag = f"{repo_name} - UI v{UI_VERSION}"
        html_content = HTML_TEMPLATE.format(version=version_tag)

        extra_tags = (
            "\n    <script type='module' src='logic.js'></script>"
            "\n    <script type='module' src='file_tree.js'></script>"
            "\n    <script type='module' src='einstein.js'></script>"
            "\n    <script type='module' src='perf.js'></script>\n"
        )
        # För enkelhet: injicera extra taggar nära </body> om den inte redan finns
        insertion_point = html_content.rfind("</body>")
        if insertion_point == -1:
            html_content = html_content + extra_tags
        else:
            html_content = html_content[:insertion_point] + extra_tags + html_content[insertion_point:]

        _write_text(output_html_path, html_content)

        # 6) Validering av oersatta platshållare (icke-fatal)
        _verify_no_unresolved_placeholders(final_js_logic, final_js_file_tree, final_js_einstein, html_content)

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
'''
out_path = "/mnt/data/engrove_audio_tools_creator.py"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(updated_code)

import hashlib, pathlib, ast
content = pathlib.Path(out_path).read_text(encoding="utf-8")
sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
lines = content.count("\n") + (0 if content.endswith("\n") else 1)
tree = ast.parse(content)
funcs = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
classes = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])

print("Path:", out_path)
print("Lines:", lines)
print("Functions:", funcs)
print("Classes:", classes)
print("SHA-256:", sha256) ​:contentReference[oaicite:1]{index=1}​
