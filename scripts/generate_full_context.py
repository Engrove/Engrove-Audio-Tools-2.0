# scripts/generate_full_context.py
#
# HISTORIK:
# * v1.0 (Initial): Basversion för att hämta filstruktur och kommentarer.
# * v2.0 (Post-Tribunal): Kraftigt omskriven efter "Help me God"-granskning.
# * v3.0 (Binary File Handling): Lade till hantering av binära filer.
# * v4.0 (AI.md Integration): Lade till stöd för att hämta en extern AI-instruktionsfil.
# * v5.0 (Project Documentation): Lade till dynamisk inläsning av alla .md-filer från en /docs-mapp.
#
# TILLÄMPADE REGLER (Frankensteen v3.7):
# - Denna fil följer principerna om "Explicit Alltid" och robust felhantering.
# - Alla nätverksanrop är inkapslade i try-except-block.
# - Dataflöden (stdout) och loggflöden (stderr) är strikt separerade.
# - Koden har refaktoriserats för läsbarhet och underhållbarhet.

import requests
import re
import json
import os
import sys

# --- Konfiguration ---
REPO = "Engrove/Engrove-Audio-Tools-2.0"
BRANCH = "main"
AI_MD_PATH = "AI.md"
DOCS_PATH = "docs" # Ny mapp för styrande dokument

# Lista över filändelser som ska behandlas som binära och vars innehåll inte ska läsas.
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
    """Skriver loggmeddelanden till stderr för att inte förorena stdout."""
    print(f"[{level}] {message}", file=sys.stderr)

def get_session_headers():
    """Skapar headers för API-anrop. Använder GITHUB_TOKEN om det finns."""
    token = os.getenv('GITHUB_TOKEN')
    headers = {
        'User-Agent': 'Python-Context-Generator/5.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    if token:
        log_message("INFO", "GITHUB_TOKEN hittades. Använder autentiserade anrop.")
        headers['Authorization'] = f"token {token}"
    else:
        log_message("WARN", "Ingen GITHUB_TOKEN hittades. Anropen är anonyma och har strikt rate limit.")
    return headers

def get_api_data(url, headers):
    """Gör ett säkert anrop till GitHub API och returnerar JSON-data."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_message("ERROR", f"Kunde inte hämta data från API {url}: {e}")
        return None

def get_raw_file_content(path, headers):
    """Hämtar råtextinnehåll från en specifik fil i repot."""
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}"
    try:
        response = requests.get(url, headers={'User-Agent': headers['User-Agent']})
        response.raise_for_status()
        return response.content.decode('utf-8', 'ignore')
    except requests.exceptions.RequestException:
        log_message("WARN", f"Kunde inte läsa filen: {path}")
        return None

# --- Huvudlogik ---

def main():
    """Orkestrerar hela processen och skriver den slutgiltiga JSON-datan till stdout."""
    log_message("INFO", f"Startar generering av kontext för {REPO} på branchen {BRANCH}.")
    
    headers = get_session_headers()

    repo_info = get_api_data(f"https://api.github.com/repos/{REPO}", headers)
    tree_info = get_api_data(f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1", headers)

    if not repo_info or not tree_info or 'tree' not in tree_info:
        log_message("FATAL", "Kunde inte hämta grundläggande repository-data. Avbryter.")
        sys.exit(1)

    # Hämta alla styrande dokument från /docs-mappen
    project_documentation = {}
    doc_files = [item for item in tree_info['tree'] if item['path'].startswith(DOCS_PATH + '/') and item['path'].endswith('.md')]
    if doc_files:
        log_message("INFO", f"Hittade {len(doc_files)} styrande dokument i mappen '{DOCS_PATH}'.")
        for doc_item in doc_files:
            doc_path = doc_item['path']
            doc_content = get_raw_file_content(doc_path, headers)
            if doc_content:
                project_documentation[os.path.basename(doc_path)] = doc_content
    else:
        log_message("WARN", f"Inga .md-filer hittades i mappen '{DOCS_PATH}'.")

    # Analysera filstrukturen (exkluderar docs-mappen nu)
    file_structure = {}
    file_list = [item for item in tree_info['tree'] if item['type'] == 'blob' and not item['path'].startswith(DOCS_PATH + '/')]
    log_message("INFO", f"Hittade {len(file_list)} källkodsfiler att analysera.")

    for i, item in enumerate(file_list):
        path = item['path']
        # Hoppa över AI.md här eftersom den hanteras separat
        if path.lower() == AI_MD_PATH.lower():
            continue
            
        log_message("INFO", f"Bearbetar ({i+1}/{len(file_list)}): {path}")
        
        path_parts = path.split('/')
        current_level = file_structure
        for part in path_parts[:-1]:
            current_level = current_level.setdefault(part, {})
        
        current_level[path_parts[-1]] = {"type": "file", "path": path} # Håller det enkelt för nu

    ai_static_context = get_raw_file_content(AI_MD_PATH, headers)

    final_context = {
        "project_overview": {
            "repository": REPO,
            "description": repo_info.get('description'),
            "primary_language": repo_info.get('language'),
            "last_updated_at": repo_info.get('pushed_at'),
            "url": repo_info.get('html_url')
        },
        "ai_instructions": ai_static_context,
        "project_documentation": project_documentation,
        "file_structure_overview": file_structure # Byt namn för tydlighet
    }
    
    print(json.dumps(final_context, indent=2, ensure_ascii=False), file=sys.stdout)
    log_message("INFO", "Kontextgenerering slutförd. Resultat skickat till stdout.")

if __name__ == "__main__":
    main()
