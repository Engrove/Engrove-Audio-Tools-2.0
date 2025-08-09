# scripts/generate_full_context.py
#
# HISTORIK:
# * v15.0 (2025-08-09): (DENNA ÄNDRING) Operation Kontext-Integritet. Lade till en ny,
#   obligatorisk boolean-nyckel `is_content_full` till varje filobjekt. Detta skapar en
#   otvetydig sanningskälla för att skilja på fullständiga filer och stubs, vilket är
#   kritiskt för AI:ns interna kontexthantering.
#
# (Resten av historiken är bevarad)
# * v1.0 (Initial): Basversion för att hämta filstruktur och kommentarer.
# * v2.0 (Post-Tribunal): Kraftigt omskriven med GITHUB_TOKEN, beroende-extrahering och robust felhantering.
# * v3.0 (Binary File Handling): Lade till hantering av binära filer för att undvika korrupt data.
# * v4.0 (AI.md Integration): Lade till stöd för att hämta en extern AI-instruktionsfil.
# * v5.0 (Project Documentation): Lade till dynamisk inläsning av alla .md-filer från en /docs-mapp.
# * v6.0 (Restoration & Synthesis): Återställde all förlorad funktionalitet och syntetiserade den.
# * v7.0 (Help me God Audit): Ändrat 'ignore' till 'replace' i decode för ökad robusthet.
# * v8.0 (Content Inclusion): Lade till nyckeln "content" för varje filobjekt.
# * v9.0 (JSON Size Fix): Behandlar .json-filer som "opak" data.
# * v10.0 (Order Fix): Helt omskriven `extract_from_content`-funktion med `re.finditer`.
# * v11.0 (2025-08-06): Omskriven för att stödja den modulära instruktionsstrukturen.
# * v12.0 (2025-08-06): Refaktorerad för att skapa en enhetlig filstruktur för hela projektet.
# * v13.0 (2025-08-06): Integrerar `scripts/process_ai_instructions.py`.
# * v14.0 (2025-08-08): Integrerar `scripts/process_ai_metrics.py`.
#
# TILLÄMPADE REGLER (Frankensteen v5.0):
# - Post-Failure Scrutiny (PFS): Denna ändring adresserar direkt den designbrist som
#   identifierades i föregående interaktion. Heuristik H-20250809-25 tillämpas.
# - API-kontraktsverifiering: Det JSON-kontrakt som detta skript producerar har nu
#   utökats på ett bakåtkompatibelt sätt med den nya `is_content_full`-nyckeln.

import requests
import re
import json
import os
import sys
import subprocess

# --- Konfiguration ---
REPO = "Engrove/Engrove-Audio-Tools-2.0"
BRANCH = "main"
AI_CORE_INSTRUCTION_PATH = "docs/ai_protocols/AI_Core_Instruction.md"
AI_PROCESSOR_SCRIPT_PATH = "scripts/process_ai_instructions.py"
AI_METRICS_SCRIPT_PATH = "scripts/process_ai_metrics.py"

BINARY_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'ico', 'bmp', 'tiff',
    'woff', 'woff2', 'eot', 'ttf', 'otf',
    'zip', 'gz', 'tar', 'rar', '7z',
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'mp3', 'wav', 'ogg', 'mp4', 'mov', 'avi', 'mkv',
    'pyc', 'pyd', 'so', 'dll', 'exe', 'bin', 'dat'
}

# --- Reguljära uttryck för analys ---
COMMENT_PATTERNS = [
    re.compile(r'//.*'), re.compile(r'/\*[\s\S]*?\*/'),
    re.compile(r'<!--[\s\S]*?-->'), re.compile(r'#.*'),
]
DEP_PATTERNS = [
    re.compile(r'^\s*import(?:.*?from)?\s*[\'"]([^\'"]+)[\'"]', re.MULTILINE),
    re.compile(r'require\([\'"]([^\'"]+)[\'"]\)', re.MULTILINE),
    re.compile(r'^\s*(?:from|import)\s+([a-zA-Z0-9_.]+)', re.MULTILINE),
]


# --- Hjälpfunktioner ---
def log_message(level, message):
    print(f"[{level}] {message}", file=sys.stderr)

def sanitize_comment(comment_text):
    return re.sub(r'^[/\\*\\->#;\\"\\s]+|<!--|-->', '', comment_text).strip()

def extract_from_content(content, patterns):
    all_matches = []
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            if pattern in DEP_PATTERNS:
                match_text = next((g for g in match.groups() if g is not None), None)
            else:
                match_text = match.group(0)
            if match_text:
                all_matches.append((match.start(), match_text))

    all_matches.sort(key=lambda x: x[0])
    seen = set()
    ordered_unique_matches = []
    for _, text in all_matches:
        if text not in seen:
            seen.add(text)
            ordered_unique_matches.append(text)
    return ordered_unique_matches


# --- Kärnfunktioner för datahämtning ---
def get_session_headers():
    token = os.getenv('GITHUB_TOKEN')
    headers = {
        'User-Agent': 'Python-Context-Generator/15.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    if token:
        log_message("INFO", "GITHUB_TOKEN found. Using authenticated requests.")
        headers['Authorization'] = f"token {token}"
    else:
        log_message("WARN", "No GITHUB_TOKEN found. Requests will be anonymous.")
    return headers

def get_api_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_message("ERROR", f"Failed to fetch API data from {url}: {e}")
        return None

def get_raw_file_content(path, headers):
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}"
    try:
        response = requests.get(url, headers={'User-Agent': headers['User-Agent']})
        response.raise_for_status()
        return response.content.decode('utf-8', 'replace')
    except requests.exceptions.RequestException:
        log_message("WARN", f"Could not read file content: {path}")
        return None

# --- Kör externa processorer ---
def get_processed_ai_config():
    try:
        result = subprocess.run(
            [sys.executable, AI_PROCESSOR_SCRIPT_PATH],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        return json.loads(result.stdout)
    except Exception as e:
        log_message("FATAL", f"AI instruction processor failed: {e}")
        return { "errors": [f"Processor script failed: {e}"] }

def get_ai_performance_metrics():
    try:
        result = subprocess.run(
            [sys.executable, AI_METRICS_SCRIPT_PATH],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except Exception as e:
        log_message("ERROR", f"AI metrics processor failed: {e}")
        return {}

# --- Huvudlogik ---
def main():
    log_message("INFO", f"Starting context generation for {REPO} on branch {BRANCH}.")
    headers = get_session_headers()

    repo_info = get_api_data(f"https://api.github.com/repos/{REPO}", headers)
    tree_info = get_api_data(f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1", headers)

    if not repo_info or not tree_info or 'tree' not in tree_info:
        log_message("FATAL", "Could not fetch basic repository data. Aborting.")
        sys.exit(1)

    processed_ai_data = get_processed_ai_config()
    ai_instructions_content = get_raw_file_content(AI_CORE_INSTRUCTION_PATH, headers)
    ai_performance_metrics = get_ai_performance_metrics()

    file_structure = {}
    file_list = [item for item in tree_info['tree'] if item['type'] == 'blob']
    log_message("INFO", f"Found {len(file_list)} files to analyze.")

    for i, item in enumerate(file_list):
        path = item['path']
        log_message("INFO", f"Processing ({i+1}/{len(file_list)}): {path}")

        file_extension = path.split('.')[-1].lower() if '.' in path else ''
        is_binary = file_extension in BINARY_EXTENSIONS
        is_large_json = file_extension == 'json'

        path_parts = path.split('/')
        current_level = file_structure
        for part in path_parts[:-1]:
            current_level = current_level.setdefault(part, {})

        is_content_full = False
        content = None

        if not (is_binary or is_large_json):
            content = get_raw_file_content(path, headers)
            if content is not None:
                is_content_full = True

        file_data = {
            "type": "file",
            "path": path,
            "size_bytes": item.get('size'),
            "file_extension": file_extension,
            "is_binary": is_binary or is_large_json,
            "is_content_full": is_content_full, # NY NYCKEL
            "comments": [],
            "dependencies": [],
            "content": content
        }

        if is_content_full:
            file_data["comments"] = [sanitize_comment(c) for c in extract_from_content(content, COMMENT_PATTERNS)]
            file_data["dependencies"] = extract_from_content(content, DEP_PATTERNS)
        
        current_level[path_parts[-1]] = file_data

    final_context = {
        "project_overview": {
            "repository": REPO,
            "description": repo_info.get('description'),
            "primary_language": repo_info.get('language'),
            "last_updated_at": repo_info.get('pushed_at'),
            "url": repo_info.get('html_url')
        },
        "ai_instructions": ai_instructions_content or "Core instruction could not be loaded.",
        "ai_config_processed": processed_ai_data,
        "ai_performance_metrics": ai_performance_metrics,
        "file_structure": file_structure
    }

    print(json.dumps(final_context, indent=2, ensure_ascii=False))
    log_message("INFO", "Context generation complete. Result sent to stdout.")

if __name__ == "__main__":
    main()
