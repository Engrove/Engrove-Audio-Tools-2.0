# scripts/generate_full_context.py
#
# HISTORIK:
# (KORRIGERING: Fullständig historik återställd enligt reglerna)
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
# * v11.0 (2025-08-06): Omskriven för att stödja den modulära instruktionsstrukturen.
# * v12.0 (2025-08-06): Refaktorerad för att skapa en enhetlig filstruktur för hela projektet.
# * v13.0 (2025-08-06): (KORRIGERING) Integrerar det nya bearbetningsskriptet för AI-instruktioner.
#   Istället för att själv läsa och parsa flera AI-relaterade filer, anropar detta skript
#   nu `scripts/process_ai_instructions.py` och infogar dess fullständiga, berikade och
#   validerade JSON-output direkt i det slutgiltiga kontextobjektet.
# * v14.0 (2025-08-08): (DENNA ÄNDRING – Steg 2) Integrerar AI Performance Metrics genom att
#   anropa `scripts/process_ai_metrics.py` och infogar outputen under nyckeln `ai_performance_metrics`.
#
# TILLÄMPADE REGLER (Frankensteen v4.0 - Post-Tribunal):
# - Arkitektur (Single Responsibility Principle): Ansvaret för att hantera AI-instruktioner
#   har delegerats till ett specialiserat skript. Detta skripts ansvar är nu renodlat till
#   att hämta filstrukturen från GitHub API och slå ihop den med den förbehandlade AI-datan.
# - API-kontraktsverifiering: Konsumerar det stabila JSON-kontrakt som produceras av
#   `process_ai_instructions.py` och placerar det under en ny, tydlig nyckel (`ai_config_processed`).
# - Felresiliens: Felhanteringen för AI-instruktioner är nu implicit. Om `process_ai_instructions.py`
#   rapporterar fel, blir dessa en del av den genererade datan utan att stoppa bygget.
# - DENNA ÄNDRING: Integrationen av `ai_performance_metrics` följer samma mönster, utan att
#   påverka övrig logik. Misslyckanden loggas till stderr och resulterar i ett tomt objekt.

import requests
import re
import json
import os
import sys
import subprocess  # Ny import för att köra externa skript

# --- Konfiguration ---
REPO = "Engrove/Engrove-Audio-Tools-2.0"
BRANCH = "main"
AI_CORE_INSTRUCTION_PATH = "docs/ai_protocols/AI_Core_Instruction.md"
AI_PROCESSOR_SCRIPT_PATH = "scripts/process_ai_instructions.py"  # Ny konfiguration
AI_METRICS_SCRIPT_PATH = "scripts/process_ai_metrics.py"         # (Steg 2) Ny konfiguration

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
    re.compile(r'require\([\'"]([^\'"]+)[\'"]\)', re.MULTILINE),
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
            else:  # COMMENT_PATTERNS
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
        'User-Agent': 'Python-Context-Generator/14.0',
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

# --- Kör externa processorer ---
def get_processed_ai_config():
    """Kör AI-instruktionsprocessorn och returnerar dess JSON-output som ett Python-objekt."""
    try:
        log_message("INFO", f"Kör AI-instruktionsprocessor: {AI_PROCESSOR_SCRIPT_PATH}")
        result = subprocess.run(
            [sys.executable, AI_PROCESSOR_SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return json.loads(result.stdout)
    except FileNotFoundError:
        log_message("FATAL", f"Processor-skriptet hittades inte: {AI_PROCESSOR_SCRIPT_PATH}")
    except subprocess.CalledProcessError as e:
        log_message("FATAL", f"Processor-skriptet misslyckades: {e.stderr}")
    except json.JSONDecodeError as e:
        log_message("FATAL", f"Kunde inte parsa output från processor-skriptet: {e}")

    return {
        "config_data": {},
        "protocols": [],
        "validation_report": {
            "errors": ["Failed to execute or parse output from AI instruction processor."],
            "warnings": []
        }
    }

def get_ai_performance_metrics():
    """
    (Steg 2) Kör AI-metrics-processorn och returnerar dess JSON-output.
    Misslyckanden loggas och resulterar i {} för att inte stoppa bygget.
    """
    try:
        log_message("INFO", f"Kör AI-metrics-processor: {AI_METRICS_SCRIPT_PATH}")
        result = subprocess.run(
            [sys.executable, AI_METRICS_SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except FileNotFoundError:
        log_message("ERROR", f"Metrics-skriptet hittades inte: {AI_METRICS_SCRIPT_PATH}")
    except subprocess.CalledProcessError as e:
        log_message("ERROR", f"Metrics-skriptet misslyckades: {e.stderr}")
    except json.JSONDecodeError as e:
        log_message("ERROR", f"Ogiltig JSON från metrics-skriptet: {e}")
    return {}

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

    # AI-instruktionsdata
    processed_ai_data = get_processed_ai_config()

    # Kärninstruktionen
    ai_instructions_content = get_raw_file_content(AI_CORE_INSTRUCTION_PATH, headers)
    if not ai_instructions_content or not ai_instructions_content.strip():
        # Behåll bakåtkompatibel felrapport om core instruction saknas
        if isinstance(processed_ai_data, dict) and "validation_report" in processed_ai_data:
            processed_ai_data["validation_report"]["errors"].append(
                f"Could not fetch content for core instruction: {AI_CORE_INSTRUCTION_PATH}"
            )

    # (Steg 2) AI Performance Metrics
    ai_performance_metrics = get_ai_performance_metrics()

    file_structure = {}
    file_list = [item for item in tree_info['tree'] if item['type'] == 'blob']
    log_message("INFO", f"Hittade {len(file_list)} filer att analysera (inklusive dokumentation).")

    for i, item in enumerate(file_list):
        path = item['path']
        log_message("INFO", f"Bearbetar ({i+1}/{len(file_list)}): {path}")

        file_extension = path.split('.')[-1].lower() if '.' in path else ''
        is_binary = file_extension in BINARY_EXTENSIONS
        is_json = file_extension == 'json'

        path_parts = path.split('/')
        current_level = file_structure
        for part in path_parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

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

        if not (is_binary or is_json):
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
        "ai_instructions": ai_instructions_content or "Core instruction could not be loaded.",
        "ai_config_processed": processed_ai_data,      # Befintlig, berikad nyckel
        "ai_performance_metrics": ai_performance_metrics,  # (Steg 2) Ny nyckel
        "file_structure": file_structure
    }

    print(json.dumps(final_context, indent=2, ensure_ascii=False), file=sys.stdout)
    log_message("INFO", "Kontextgenerering slutförd. Resultat skickat till stdout.")

if __name__ == "__main__":
    main()

# (KORRIGERING: Obligatorisk slutkommentar tillagd)
# scripts/generate_full_context.py
