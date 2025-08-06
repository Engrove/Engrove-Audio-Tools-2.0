# scripts/generate_full_context.py
#
# HISTORIK:
# * v1.0 (Initial): Basversion för att hämta filstruktur och kommentarer.
# * v2.0 (Post-Tribunal): Kraftigt omskriven med GITHUB_TOKEN, beroende-extrahering och robust felhantering.
# * v3.0 (Binary File Handling): Lade till hantering av binära filer för att undvika korrupt data.
# * v4.0 (AI.md Integration): Lade till stöd för att hämta en extern AI-instruktionsfil.
# * v5.0 (Project Documentation): Lade till dynamisk inläsning av alla .md-filer från en /docs-mapp.
# * v6.0 (Restoration & Synthesis): Återställde all förlorad funktionalitet och syntetiserade den.
# * v7.0 (Help me God Audit): Ändrat 'ignore' till 'replace' i decode för ökad robusthet.
# * v8.0 (Content Inclusion): Lade till nyckeln "content" för varje filobjekt.
# * v9.0 (JSON Size Fix): Behandlar .json-filer som "opak" data för att undvika att läsa in
#   stora (GB+) filer i minnet under byggprocessen. Innehållet hämtas istället on-demand i front-end.
# * v10.0 (Order Fix): Helt omskriven `extract_from_content`-funktion. Använder nu `re.finditer`
#   och sorterar matchningar baserat på deras startindex i filen. Detta korrigerar den
#   kritiska buggen där kommentarer och beroenden listades i fel (alfabetisk) ordning.
# * v11.0 (2025-08-06): Helt omskriven för att stödja den nya modulära
#   instruktionsstrukturen. Letar nu specifikt efter en kärninstruktion
#   (AI_Core_Instruction.md) och behandlar alla andra protokoll som vanlig
#   projektdokumentation. Avslutar med felkod om kärninstruktionen saknas.
#
# TILLÄMPADE REGLER (Frankensteen v4.0):
# - Följer den nya modulära arkitekturen.
# - API-kontraktsverifiering: Säkerställer att den genererade JSON-filen
#   har den förväntade strukturen med `ai_instructions` korrekt ifyllt.
# - Felresiliens: Implementerar en "fail-fast"-strategi med sys.exit(1) om
#   den kritiska kärninstruktionen inte kan hämtas eller är tom.

import requests
import re
import json
import os
import sys

# --- Konfiguration ---
REPO = "Engrove/Engrove-Audio-Tools-2.0"
BRANCH = "main"
AI_CORE_INSTRUCTION_PATH = "docs/ai_protocols/AI_Core_Instruction.md"
DOCS_PATH = "docs"

# Lista över filändelser som ska behandlas som binära.
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
    re.compile(r'require\([\'"]([^\'\"]+)[\'\"]\)', re.MULTILINE),
    re.compile(r'^\s*(?:from|import)\s+([a-zA-Z0-9_.]+)', re.MULTILINE),
]

# --- Hjälpfunktioner ---

def log_message(level, message):
    """Skriver loggmeddelanden till stderr för att inte förorena stdout."""
    print(f"[{level}] {message}", file=sys.stderr)

def sanitize_comment(comment_text):
    """Rensar bort inledande kommentarsyntax från en extraherad kommentar."""
    return re.sub(r'^[/*\->#;"\s]+|<!--|-->', '', comment_text).strip()

def extract_from_content(content, patterns):
    """
    En generell och ordningsbevarande funktion för att extrahera text.
    Använder re.finditer för att fånga positionen för varje matchning,
    sorterar dem och returnerar sedan texten i korrekt ordning.
    """
    all_matches = []
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            if pattern in DEP_PATTERNS:
                match_text = next((g for g in match.groups() if g is not None), None)
            else: # COMMENT_PATTERNS
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
    """Skapar headers för API-anrop. Använder GITHUB_TOKEN om det finns."""
    token = os.getenv('GITHUB_TOKEN')
    headers = {
        'User-Agent': 'Python-Context-Generator/11.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    if token:
        log_message("INFO", "GITHUB_TOKEN hittades. Använder autentiserade anrop.")
        headers['Authorization'] = f"token {token}"
    else:
        log_message("WARN", "Ingen GITHUB_TOKEN hittades. Anropen är anonyma.")
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
        return response.content.decode('utf-8', 'replace')
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

    ai_instructions = get_raw_file_content(AI_CORE_INSTRUCTION_PATH, headers)
    if not ai_instructions or not ai_instructions.strip():
        log_message("FATAL", f"Kunde inte hämta den obligatoriska kärninstruktionen från '{AI_CORE_INSTRUCTION_PATH}' eller så är filen tom. Avbryter.")
        sys.exit(1)
    log_message("INFO", f"Hämtade kärninstruktionen från '{AI_CORE_INSTRUCTION_PATH}'.")

    project_documentation = {}
    doc_files = [item for item in tree_info['tree'] if item['path'].startswith(DOCS_PATH + '/') and item['path'].endswith('.md') and item['path'] != AI_CORE_INSTRUCTION_PATH]
    if doc_files:
        log_message("INFO", f"Hittade {len(doc_files)} styrande dokument och protokoll.")
        for doc_item in doc_files:
            doc_path = doc_item['path']
            doc_content = get_raw_file_content(doc_path, headers)
            if doc_content:
                project_documentation[os.path.basename(doc_path)] = doc_content
    else:
        log_message("WARN", f"Inga ytterligare .md-filer hittades i mappen '{DOCS_PATH}'.")

    file_structure = {}
    file_list = [item for item in tree_info['tree'] if item['type'] == 'blob' and not item['path'].startswith(DOCS_PATH + '/')]
    log_message("INFO", f"Hittade {len(file_list)} källkodsfiler att analysera.")

    for i, item in enumerate(file_list):
        path = item['path']
        log_message("INFO", f"Bearbetar ({i+1}/{len(file_list)}): {path}")
        
        file_extension = path.split('.')[-1].lower() if '.' in path else ''
        is_binary = file_extension in BINARY_EXTENSIONS
        is_json = file_extension == 'json'

        path_parts = path.split('/')
        current_level = file_structure
        for part in path_parts[:-1]:
            current_level = current_level.setdefault(part, {})
        
        file_data = {
            "type": "file",
            "path": path,
            "size_bytes": item.get('size'),
            "file_extension": file_extension,
            "is_binary": is_binary or is_json,
            "comments": [],
            "dependencies": [],
            "content": None
        }

        if is_json:
            log_message("INFO", f"Hoppar över innehållsläsning för JSON-datafil: {path}")
        elif is_binary:
            log_message("INFO", f"Hoppar över innehållsläsning för binär fil: {path}")
        else:
            content = get_raw_file_content(path, headers)
            if content:
                file_data["comments"] = [sanitize_comment(c) for c in extract_from_content(content, COMMENT_PATTERNS)]
                file_data["dependencies"] = extract_from_content(content, DEP_PATTERNS)
                file_data["content"] = content

        current_level[path_parts[-1]] = file_data

    final_context = {
        "project_overview": {
            "repository": REPO,
            "description": repo_info.get('description'),
            "primary_language": repo_info.get('language'),
            "last_updated_at": repo_info.get('pushed_at'),
            "url": repo_info.get('html_url')
        },
        "ai_instructions": ai_instructions,
        "project_documentation": project_documentation,
        "file_structure": file_structure
    }
    
    print(json.dumps(final_context, indent=2, ensure_ascii=False), file=sys.stdout)
    log_message("INFO", "Kontextgenerering slutförd. Resultat skickat till stdout.")

if __name__ == "__main__":
    main()
