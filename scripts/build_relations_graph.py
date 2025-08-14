#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# scripts/build_relations_graph.py
#
# === SYFTE & ANSVAR ===
# Detta skript har ett dubbelt ansvar:
# 1. Relationsanalys: Analyserar källkoden (.vue, .js, .py) för att bygga en
#    detaljerad relationsgraf (docs/file_relations.json).
# 2. Schema-Inferens: Analyserar datafiler (.json) i public/data/ och
#    auto-genererar ett formellt JSON Schema för varje fil, vilket säkerställer
#    att AI-partnern har ett explicit datakontrakt att arbeta mot.
#
# === HISTORIK ===
# * v1.0 (2025-08-14): Initial skapelse av Frankensteen.
# * v2.0 (2025-08-14): Uppgraderad med schema-inferensfunktionalitet enligt direktiv.
# * v2.1 (2025-08-14): KRITISK FIX: Korrigerat ett logiskt fel i main-funktionen som
#   felaktigt hoppade över JSON-filer, vilket förhindrade schema-generering.

import json
import re
from pathlib import Path
from typing import Dict, Any, Set, List, Union

# --- Konfiguration ---
ROOT_DIR = Path(__file__).parent.parent
SCAN_DIRS = ['src', 'scripts', 'public/data']
INCLUDE_EXTENSIONS = ['.vue', '.js', '.py', '.json']
EXCLUDE_DIRS = ['node_modules', 'dist', '__pycache__', 'schemas']
RELATIONS_OUTPUT_FILE = ROOT_DIR / 'docs' / 'file_relations.json'
SCHEMA_OUTPUT_DIR = ROOT_DIR / 'public' / 'data' / 'schemas'

# --- Regex-mönster ---
JS_IMPORT_REGEX = re.compile(r"import(?:[\s\S]*?)from\s*['\"]([^'\"]+)['\"]")
PY_IMPORT_REGEX = re.compile(r"^\s*(?:import|from)\s+([\w.]+)", re.MULTILINE)
VUE_PROPS_REGEX = re.compile(r"defineProps\s*\(\s*({[\s\S]*?})\s*\)", re.MULTILINE)
VUE_EMITS_REGEX = re.compile(r"defineEmits\s*\(\s*(\[[\s\S]*?\])\s*\)", re.MULTILINE)
PINIA_STATE_REGEX = re.compile(r"state:\s*\(\)\s*=>\s*\(([\s\S]*?)\)", re.MULTILINE)
PINIA_GETTERS_REGEX = re.compile(r"getters:\s*{([\s\S]*?)}", re.MULTILINE)
PINIA_ACTIONS_REGEX = re.compile(r"actions:\s*{([\s\S]*?)}", re.MULTILINE)
OBJECT_KEY_REGEX = re.compile(r"(\w+)\s*:")
PY_FUNC_REGEX = re.compile(r"^\s*def\s+(\w+)\s*\(", re.MULTILINE)
PY_CLASS_REGEX = re.compile(r"^\s*class\s+(\w+)", re.MULTILINE)


def get_json_type(value: Any) -> str:
    """Returnerar JSON-datatypen för ett Python-värde."""
    if isinstance(value, str): return "string"
    if isinstance(value, bool): return "boolean"
    if isinstance(value, (int, float)): return "number"
    if isinstance(value, list): return "array"
    if isinstance(value, dict): return "object"
    return "null"

def infer_schema_from_data(data: Union[Dict, List]) -> Dict:
    """Härleder ett JSON Schema från en Python-datastruktur."""
    if isinstance(data, list):
        if not data:
            return {"type": "array"}
        # Analysera schemat baserat på det första objektet i listan
        item_schemas = [infer_schema_from_data(item) for item in data[:1]] # Analysera bara första för prestanda
        if not item_schemas:
            return {"type": "array"}
        return {"type": "array", "items": item_schemas[0]}

    if isinstance(data, dict):
        properties = {}
        required = []
        for key, value in data.items():
            properties[key] = {"type": get_json_type(value)}
            if get_json_type(value) == "object":
                properties[key] = infer_schema_from_data(value)
            elif get_json_type(value) == "array" and value:
                 properties[key] = infer_schema_from_data(value)
            required.append(key)
        
        return {
            "type": "object",
            "properties": properties,
            "required": sorted(required)
        }
    return {}


def analyze_file(file_path: Path) -> Dict[str, Any]:
    """Analyserar en enskild fil för antingen relationer eller schema."""
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    
    if file_path.suffix == '.json':
        try:
            data = json.loads(content)
            schema = infer_schema_from_data(data)
            schema_path = SCHEMA_OUTPUT_DIR / f"{file_path.name.replace('.json', '')}.schema.json"
            schema_path.parent.mkdir(parents=True, exist_ok=True)
            schema_path.write_text(json.dumps(schema, indent=2), encoding='utf-8')
            print(f"  Schema inferred and saved to: {normalize_path(schema_path)}")
        except json.JSONDecodeError:
            print(f"  [WARNING] Could not parse JSON, skipping schema generation for: {normalize_path(file_path)}")
        return {"type": "Data File", "api": {}, "dependencies": []}

    file_type = "Unknown"
    api = {}
    dependencies = set()

    if file_path.suffix in ['.js', '.vue']:
        file_type = "Vue Component" if file_path.suffix == '.vue' else "JavaScript Module"
        imports = JS_IMPORT_REGEX.findall(content)
        for imp in imports:
            if imp.startswith('@/'): imp = 'src/' + imp[2:]
            try:
                resolved_path = (file_path.parent / imp).resolve()
                if resolved_path.exists(): dependencies.add(normalize_path(resolved_path))
            except Exception: pass
        if 'store' in file_path.name.lower(): file_type = "Pinia Store"

    elif file_path.suffix == '.py':
        file_type = "Python Script"
        dependencies.update(PY_IMPORT_REGEX.findall(content))
        api['functions'] = PY_FUNC_REGEX.findall(content)
        api['classes'] = PY_CLASS_REGEX.findall(content)

    return {
        "type": file_type,
        "api": api,
        "dependencies": sorted(list(dependencies))
    }

def find_source_files() -> List[Path]:
    """Hittar alla relevanta källkodsfiler i projektet."""
    all_files = []
    for directory in SCAN_DIRS:
        root_path = ROOT_DIR / directory
        for file_path in root_path.rglob('*'):
            if (any(part in EXCLUDE_DIRS for part in file_path.parts) or
                    file_path.suffix not in INCLUDE_EXTENSIONS):
                continue
            all_files.append(file_path)
    return all_files

def normalize_path(path: Path) -> str:
    """Normaliserar en sökväg till ett relativt, plattformsoberoende format."""
    return path.relative_to(ROOT_DIR).as_posix()

def main():
    """Huvudfunktion som kör hela processen."""
    print("Starting analysis of project file relations and data schemas...")
    source_files = find_source_files()
    
    nodes: Dict[str, Any] = {}
    
    for file_path in source_files:
        norm_path = normalize_path(file_path)
        print(f"  Analyzing: {norm_path}")
        
        # KORRIGERING: Anropa analyze_file för ALLA filer.
        # Funktionen själv avgör om den ska generera schema eller analysera beroenden.
        analysis_result = analyze_file(file_path)

        if file_path.suffix != '.json':
            nodes[norm_path] = analysis_result

    edges: List[Dict[str, str]] = []
    for path in nodes:
        nodes[path]['dependents'] = []

    for path, data in nodes.items():
        for dep_path in data.get('dependencies', []):
            potential_paths = [dep_path]
            if not Path(dep_path).suffix:
                 potential_paths.extend([f"{dep_path}.js", f"{dep_path}.vue"])
            
            found_dep = None
            for p_path in potential_paths:
                if p_path in nodes:
                    found_dep = p_path
                    break
            
            if found_dep:
                edges.append({"from": path, "to": found_dep, "type": "import"})
                if found_dep in nodes:
                    nodes[found_dep]['dependents'].append(path)

    for path in nodes:
        del nodes[path]['dependencies']
        
    final_graph = {
        "schema_version": "1.0",
        "generated_at": json.dumps(
            Path(__file__).stat().st_mtime, 
            default=str
        ).strip('\"'),
        "nodes": nodes,
        "edges": edges
    }

    print(f"\nAnalysis complete. Writing relations graph to {RELATIONS_OUTPUT_FILE}...")
    RELATIONS_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    RELATIONS_OUTPUT_FILE.write_text(json.dumps(final_graph, indent=2, ensure_ascii=False), encoding='utf-8')
    print("Done.")

if __name__ == '__main__':
    main()

# scripts/build_relations_graph.py
