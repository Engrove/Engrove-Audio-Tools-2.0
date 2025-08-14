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
# * v4.0 (2025-08-14): OPERATION UNIVERSAL GRAPH v2.0: Fundamental uppgradering till AST-parsing för Python,
#   utökad filtyps-scope, semantisk berikning av noder/kanter och kritikalitets-poäng.
# * v5.0 (2025-08-14): PROTOKOLLUPPGRADERING: Implementerat `file_relations.json` v3.1, det självförklarande protokollet.
#   Filen innehåller nu ett `_meta`-block som fungerar som en inbäddad AI-instruktion.
# * v5.1 (2025-08-14): SLUTFÖRANDE: Implementerat korrekt kategorisering av beroendetyper (edges),
#   vilket fullbordar den semantiska berikningen.
#
# === TILLÄMPADE REGLER (Frankensteen v5.5) ===
# - Obligatorisk Refaktorisering: Hela skriptet har omstrukturerats för att producera det nya, självförklarande formatet.
# - API-kontraktsverifiering: Output-formatet följer det nya, överenskomna `file_relations.json` v3.1-schemat.
# - Red Team Alter Ego: Den nya `_meta`-sektionen har granskats för att säkerställa att den är otvetydig för en AI utan förkunskaper.

import json
import re
import ast
from pathlib import Path
from typing import Dict, Any, List, Union, Set, Tuple
from datetime import datetime, timezone
import sys

# --- Konfiguration ---
ROOT_DIR = Path(__file__).resolve().parent.parent
SCAN_DIRS = ['src', 'scripts', 'public', '.github', 'docs', 'tools']
INCLUDE_EXTENSIONS = ['.vue', '.js', '.py', '.json', '.css', '.toml', '.yml', '.md', '.txt']
EXCLUDE_DIRS = ['node_modules', 'dist', '__pycache__', 'schemas']
RELATIONS_OUTPUT_FILE = ROOT_DIR / 'docs' / 'file_relations.json'

# --- Självförklarande Meta-block ---
SELF_DESCRIBING_META = {
    "protocol_id": "FileRelations_v3.1_SelfDescribing",
    "purpose": "Detta är en maskinläsbar, strukturerad karta över projektets arkitektur. Den fungerar både som rådata och som en instruktion för en AI-assistent. Den beskriver alla relevanta filer, deras roller och deras inbördes beroenden.",
    "how_to_interpret": {
        "graph_data": "Detta fält innehåller en representation av projektet som en riktad graf.",
        "nodes": "Varje nyckel i 'nodes'-objektet representerar en unik fil i projektet. Sökvägen är nyckeln.",
        "edges": "Varje objekt i 'edges'-arrayen representerar ett beroende från en 'from'-fil till en 'to'-fil."
    },
    "key_definitions": {
        "nodes": {
            "criticality_score": "Ett mått (0-100) på hur central en fil är. Beräknas baserat på antalet andra filer som är beroende av den (`dependents_count`). Ett högt värde indikerar att ändringar i denna fil har stor potentiell påverkan och kräver extra försiktighet.",
            "category": "Filens arkitektoniska roll: 'code', 'configuration', 'documentation', eller 'data'.",
            "exports": "Visar de specifika funktioner/klasser som en fil exponerar (exporterar).",
            "imports": "Visar de specifika moduler/bibliotek som en fil använder (importerar)."
        },
        "edges": {
            "type": "Typen av beroende, t.ex. 'code_import' (en kodfil importerar en annan), 'configuration_reference' (en config-fil pekar på en annan fil), 'process_execution' (ett CI/CD-jobb kör ett skript)."
        }
    },
    "actionable_intelligence_guide": {
        "risk_assessment": "Använd `criticality_score` för att bedöma risken med en föreslagen ändring. En fil med hög poäng bör hanteras med extra noggrannhet.",
        "context_gathering": "När du ombeds modifiera en fil, använd `edges`-grafen för att identifiera och begära alla direkt relaterade filer (både beroenden och de som är beroende av filen) för att säkerställa en komplett kontext.",
        "architectural_analysis": "Använd grafen för att förstå modulära gränser och identifiera potentiella arkitektoniska problem som cirkulära beroenden eller överdrivet komplexa moduler."
    },
    "project_context_snapshot": {} # Fylls i dynamiskt
}

# --- Regex-mönster (för icke-AST-analys) ---
JS_IMPORT_REGEX = re.compile(r"import(?:[\s\S]*?)from\s*['\"]([^'\"]+)['\"]")
JS_FETCH_REGEX = re.compile(r"fetch\s*\(\s*['\"]((?:/data/)[^'\"]+\.json)['\"]")
VUE_TEMPLATE_ASSET_REGEX = re.compile(r"\s(?:src|href)\s*=\s*['\"]((?:/|@/|\./|\.\./)[^'\"]+)['\"]")
CSS_URL_REGEX = re.compile(r"url\s*\(\s*['\"]?([^'\"\\)]+)['\"]?\s*\)")
CSS_IMPORT_REGEX = re.compile(r"@import\s*['\"]([^'\"]+)['\"]")
YAML_RUN_REGEX = re.compile(r'\s*run:\s*(?:python|python3)\s+([^\s]+)')
JSON_PATH_REGEX = re.compile(r'\"(?:src|docs|scripts|public|tools)/[^\"]+\"')
MD_LINK_REGEX = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
JS_EXPORT_REGEX = re.compile(r'export\s+(?:const|let|var|function|class)\s+([a-zA-Z0-9_]+)')

# --- Hjälpfunktioner ---
def normalize_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT_DIR).as_posix()
    except ValueError:
        return path.as_posix()

def resolve_dependency_path(source_file: Path, dep_str: str) -> str:
    if not isinstance(dep_str, str) or not dep_str:
        return ""
    if dep_str.startswith('@/'):
        return normalize_path(ROOT_DIR / dep_str.replace('@/', 'src/'))
    if dep_str.startswith('/'):
        return normalize_path(ROOT_DIR / ('public' + dep_str))
    
    resolved = (source_file.parent / dep_str).resolve()
    if resolved.is_file() and ROOT_DIR.as_posix() in resolved.as_posix():
        return normalize_path(resolved)
    return ""

def analyze_python_ast(content: str) -> Dict[str, List[Dict[str, Any]]]:
    imports = []
    exports = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"source": alias.name, "symbols": ["*"], "type": "library_import"})
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    symbols = [alias.name for alias in node.names]
                    imports.append({"source": node.module, "symbols": symbols, "type": "library_import"})
        
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                exports.append({"symbol": node.name, "type": "function"})
            elif isinstance(node, ast.ClassDef):
                exports.append({"symbol": node.name, "type": "class"})
    except SyntaxError:
        pass
    return {"imports": imports, "exports": exports}

def analyze_javascript_symbols(content: str) -> Dict[str, List[Dict[str, Any]]]:
    exports = [{"symbol": match, "type": "unknown"} for match in JS_EXPORT_REGEX.findall(content)]
    return {"exports": exports}

def get_file_category(file_path: Path) -> str:
    path_str = normalize_path(file_path)
    if 'public/data' in path_str and file_path.suffix == '.json':
        return 'data'
    if file_path.suffix in ['.json', '.toml', '.yml']:
        return 'configuration'
    if file_path.suffix in ['.md', '.txt']:
        return 'documentation'
    if file_path.suffix in ['.js', '.py', '.vue', '.css']:
        return 'code'
    return 'asset'

def analyze_file(file_path: Path) -> Dict[str, Any]:
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except (IOError, UnicodeDecodeError):
        content = ""

    dependencies: List[Tuple[str, str]] = []
    imports = []
    exports = []
    file_type = "Unknown"
    category = get_file_category(file_path)

    if file_path.suffix == '.vue':
        file_type = "Vue Component"
        script_content = "".join(re.findall(r"<script.*?>([\s\S]*?)</script>", content))
        template_content = "".join(re.findall(r"<template>([\s\S]*?)</template>", content))
        
        dependencies.extend([(dep, 'code_import') for dep in JS_IMPORT_REGEX.findall(script_content)])
        dependencies.extend([(dep, 'asset_usage') for dep in VUE_TEMPLATE_ASSET_REGEX.findall(template_content)])
        exports = analyze_javascript_symbols(script_content).get('exports', [])

    elif file_path.suffix == '.js':
        file_type = "JavaScript Module"
        dependencies.extend([(dep, 'code_import') for dep in JS_IMPORT_REGEX.findall(content)])
        dependencies.extend([(dep, 'data_fetch') for dep in JS_FETCH_REGEX.findall(content)])
        exports = analyze_javascript_symbols(content).get('exports', [])

    elif file_path.suffix == '.py':
        file_type = "Python Script"
        ast_results = analyze_python_ast(content)
        imports = ast_results.get('imports', [])
        exports = ast_results.get('exports', [])
        dependencies.extend([(imp['source'], 'code_import') for imp in imports])

    elif file_path.suffix == '.yml':
        file_type = "YAML Config"
        dependencies.extend([(dep, 'process_execution') for dep in YAML_RUN_REGEX.findall(content)])
        
    elif file_path.suffix == '.json' and category == 'configuration':
        file_type = "JSON Config"
        dependencies.extend([(dep.strip('"'), 'configuration_reference') for dep in JSON_PATH_REGEX.findall(content)])

    elif file_path.suffix == '.md':
        file_type = "Markdown Document"
        dependencies.extend([(dep, 'documentation_link') for dep in MD_LINK_REGEX.findall(content)])

    return {
        "type": file_type,
        "category": category,
        "language": file_path.suffix.lstrip('.'),
        "dependencies": dependencies,
        "imports": imports,
        "exports": exports
    }

def find_source_files() -> List[Path]:
    all_files = []
    for directory in SCAN_DIRS:
        root_path = ROOT_DIR / directory
        if not root_path.is_dir():
            continue
        for file_path in root_path.rglob('*'):
            if file_path.is_dir() or any(part in EXCLUDE_DIRS for part in file_path.parts):
                continue
            if file_path.suffix in INCLUDE_EXTENSIONS:
                 all_files.append(file_path)
    return all_files

def main(project_overview_json_str: str):
    print("Starting universal asset graph analysis (v5.1)...", file=sys.stderr)
    
    try:
        project_overview = json.loads(project_overview_json_str)
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON provided for project_overview.", file=sys.stderr)
        sys.exit(1)

    source_files = find_source_files()
    
    raw_nodes: Dict[str, Any] = {}
    all_paths_in_project = {normalize_path(p) for p in source_files}

    for file_path in source_files:
        norm_path = normalize_path(file_path)
        print(f"  Analyzing: {norm_path}", file=sys.stderr)
        raw_nodes[norm_path] = analyze_file(file_path)

    nodes: Dict[str, Any] = {}
    edges: List[Dict[str, str]] = []
    dependents_map: Dict[str, int] = {path: 0 for path in all_paths_in_project}

    for path, data in raw_nodes.items():
        nodes[path] = {
            "type": data["type"],
            "category": data["category"],
            "language": data["language"],
            "exports": data["exports"],
            "imports": data["imports"]
        }
        for dep_str, dep_type in data.get('dependencies', []):
            resolved = resolve_dependency_path(ROOT_DIR / path, dep_str)
            
            if resolved and resolved in all_paths_in_project:
                edges.append({"from": path, "to": resolved, "type": dep_type})
                dependents_map[resolved] = dependents_map.get(resolved, 0) + 1

    max_dependents = max(dependents_map.values()) if dependents_map else 1
    
    for path, node_data in nodes.items():
        count = dependents_map.get(path, 0)
        node_data["dependents_count"] = count
        node_data["criticality_score"] = round((count / max_dependents) * 100, 2) if max_dependents > 0 else 0

    meta_block = SELF_DESCRIBING_META
    meta_block["project_context_snapshot"] = project_overview

    final_output = {
        "_meta": meta_block,
        "graph_data": {
            "schema_version": "3.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "nodes": nodes,
            "edges": edges
        }
    }

    print(f"\nAnalysis complete. Writing graph to {RELATIONS_OUTPUT_FILE}...", file=sys.stderr)
    RELATIONS_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    RELATIONS_OUTPUT_FILE.write_text(json.dumps(final_output, indent=2, ensure_ascii=False), encoding='utf-8')
    print("Done.", file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python build_relations_graph.py '<project_overview_json>'", file=sys.stderr)
        print("Example: python build_relations_graph.py '{\"repository\":\"Engrove/Repo\",\"branch\":\"main\"}'", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
