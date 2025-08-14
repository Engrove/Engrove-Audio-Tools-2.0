#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# scripts/build_relations_graph.py
#
# === SYFTE & ANSVAR ===
# Detta skript är en universell analysmotor med ett trefaldigt ansvar:
# 1. Relationsanalys (Kod): Analyserar källkoden (.vue, .js, .py) för 'import'-beroenden.
# 2. Relationsanalys (Tillgångar): Analyserar kod (.vue, .js, .css) för data-beroenden
#    (fetch) och statiska tillgångar (bilder, typsnitt).
# 3. Schema-Inferens: Analyserar datafiler (.json) i public/data/ och
#    auto-genererar ett formellt JSON Schema för varje fil.
#
# === HISTORIK ===
# * v1.0 (2025-08-14): Initial skapelse. Fokuserade på kod-importer.
# * v2.0 (2025-08-14): Uppgraderad med schema-inferensfunktionalitet.
# * v2.1-v2.2 (2025-08-14): Kritiska buggfixar relaterade till CI/CD-fel.
# * v3.0 (2025-08-14): ARKITEKTURUPPGRADERING: Implementerat "Plan 4.0" för universell tillgångsgraf.
# * v3.1 (2025-08-14): KRITISK FIX: Korrigerat ett SyntaxError i ett reguljärt uttryck (CSS_URL_REGEX).

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Union, Set
from datetime import datetime, timezone

# --- Konfiguration ---
ROOT_DIR = Path(__file__).parent.parent
SCAN_DIRS = ['src', 'scripts', 'public']
INCLUDE_EXTENSIONS = ['.vue', '.js', '.py', '.json', '.css']
EXCLUDE_DIRS = ['node_modules', 'dist', '__pycache__', 'schemas']
RELATIONS_OUTPUT_FILE = ROOT_DIR / 'docs' / 'file_relations.json'
SCHEMA_OUTPUT_DIR = ROOT_DIR / 'public' / 'data' / 'schemas'

# --- Regex-mönster ---
# JS/VUE <script>
JS_IMPORT_REGEX = re.compile(r"import(?:[\s\S]*?)from\s*['\"]([^'\"]+)['\"]")
JS_FETCH_REGEX = re.compile(r"fetch\s*\(\s*['\"]((?:\/data\/)[^'\"]+\.json)['\"]")
JS_WORKER_REGEX = re.compile(r"new\s+Worker\s*\(\s*['\"]([^'\"]+)['\"]")

# VUE <template>
VUE_TEMPLATE_ASSET_REGEX = re.compile(r"\s(?:src|href)\s*=\s*['\"]((?:\/|@\/|\.\/|\.\.\/)[^'\"]+)['\"]")

# CSS / VUE <style>
# KORRIGERING: Det felaktiga mönstret [^'\")] är nu korrekt som [^'\"\\)]+
CSS_URL_REGEX = re.compile(r"url\s*\(\s*['\"]?([^'\"\\)]+)['\"]?\s*\)")
CSS_IMPORT_REGEX = re.compile(r"@import\s*['\"]([^'\"]+)['\"]")


# PYTHON
PY_IMPORT_REGEX = re.compile(r"^\s*(?:import|from)\s+([\w.]+)", re.MULTILINE)

# (Resten av filen är oförändrad)

def normalize_path(path: Path) -> str:
    return path.relative_to(ROOT_DIR).as_posix()

def resolve_dependency_path(source_file: Path, dep_str: str) -> str:
    if dep_str.startswith('@/'):
        return normalize_path(ROOT_DIR / dep_str.replace('@/', 'src/'))
    if dep_str.startswith('/'):
        # Anta att rot-sökvägar i webben pekar på /public
        return normalize_path(ROOT_DIR / ('public' + dep_str))
    
    resolved = (source_file.parent / dep_str).resolve()
    if resolved.is_file() and ROOT_DIR in resolved.parents:
        return normalize_path(resolved)
    return ""

def get_json_type(value: Any) -> str:
    if isinstance(value, str): return "string"
    if isinstance(value, bool): return "boolean"
    if isinstance(value, (int, float)): return "number"
    if isinstance(value, list): return "array"
    if isinstance(value, dict): return "object"
    return "null"

def infer_schema_from_data(data: Union[Dict, List]) -> Dict:
    if isinstance(data, list):
        if not data: return {"type": "array"}
        items_schema = infer_schema_from_data(data[0]) if isinstance(data[0], (dict, list)) else {"type": get_json_type(data[0])}
        return {"type": "array", "items": items_schema}
    if isinstance(data, dict):
        properties = {key: infer_schema_from_data(value) if isinstance(value, (dict, list)) else {"type": get_json_type(value)} for key, value in data.items()}
        return {"type": "object", "properties": properties, "required": sorted(list(data.keys()))}
    return {}

def analyze_file(file_path: Path) -> Dict[str, Any]:
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    dependencies = set()
    file_type = "Unknown"

    if file_path.suffix == '.json' and 'public/data' in normalize_path(file_path):
        file_type = "Data File"
        try:
            data = json.loads(content)
            if data:
                schema = infer_schema_from_data(data)
                schema_path = SCHEMA_OUTPUT_DIR / f"{file_path.stem}.schema.json"
                schema_path.parent.mkdir(parents=True, exist_ok=True)
                schema_path.write_text(json.dumps(schema, indent=2, ensure_ascii=False), encoding='utf-8')
        except json.JSONDecodeError:
            pass
        return {"type": file_type, "dependencies": list(dependencies)}

    if file_path.suffix == '.vue':
        file_type = "Vue Component"
        template_content = "".join(re.findall(r"<template>([\s\S]*?)<\/template>", content))
        script_content = "".join(re.findall(r"<script.*?>([\s\S]*?)<\/script>", content))
        style_content = "".join(re.findall(r"<style.*?>([\s\S]*?)<\/style>", content))
        dependencies.update(JS_IMPORT_REGEX.findall(script_content))
        dependencies.update(VUE_TEMPLATE_ASSET_REGEX.findall(template_content))
        dependencies.update(CSS_URL_REGEX.findall(style_content))
    elif file_path.suffix == '.js':
        file_type = "JavaScript Module"
        dependencies.update(JS_IMPORT_REGEX.findall(content))
        dependencies.update(JS_FETCH_REGEX.findall(content))
        dependencies.update(JS_WORKER_REGEX.findall(content))
    elif file_path.suffix == '.css':
        file_type = "Stylesheet"
        dependencies.update(CSS_IMPORT_REGEX.findall(content))
        dependencies.update(CSS_URL_REGEX.findall(content))
    elif file_path.suffix == '.py':
        file_type = "Python Script"
        dependencies.update(PY_IMPORT_REGEX.findall(content))

    return {"type": file_type, "dependencies": sorted(list(dependencies))}

def find_source_files() -> List[Path]:
    all_files = []
    for directory in SCAN_DIRS:
        root_path = ROOT_DIR / directory
        for file_path in root_path.rglob('*'):
            if (any(part in EXCLUDE_DIRS for part in file_path.parts) or
                    file_path.suffix not in INCLUDE_EXTENSIONS):
                continue
            all_files.append(file_path)
    return all_files

def main():
    print("Starting universal asset graph analysis...")
    source_files = find_source_files()
    
    raw_nodes: Dict[str, Any] = {}
    all_paths_in_project = {normalize_path(p) for p in source_files}

    for file_path in source_files:
        norm_path = normalize_path(file_path)
        print(f"  Analyzing: {norm_path}")
        raw_nodes[norm_path] = analyze_file(file_path)

    nodes: Dict[str, Any] = {}
    edges: List[Dict[str, str]] = []

    for path, data in raw_nodes.items():
        nodes[path] = {"type": data["type"], "dependents": []}
        for dep_str in data.get('dependencies', []):
            resolved = resolve_dependency_path(ROOT_DIR / path, dep_str)
            
            if resolved and resolved in all_paths_in_project:
                edge_type = "import"
                if ".json" in resolved: edge_type = "data_fetch"
                elif any(resolved.endswith(ext) for ext in ['.png', '.jpg', '.webp', '.svg']): edge_type = "asset_usage"
                
                edges.append({"from": path, "to": resolved, "type": edge_type})

    for edge in edges:
        if edge["to"] in nodes:
            nodes[edge["to"]]["dependents"].append(edge["from"])

    final_graph = {
        "schema_version": "2.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "nodes": nodes,
        "edges": edges
    }

    print(f"\nAnalysis complete. Writing graph to {RELATIONS_OUTPUT_FILE}...")
    RELATIONS_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    RELATIONS_OUTPUT_FILE.write_text(json.dumps(final_graph, indent=2, ensure_ascii=False), encoding='utf-8')
    print("Done.")

if __name__ == '__main__':
    main()

# scripts/build_relations_graph.py
