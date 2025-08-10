#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_full_context.py
v16.0 (2025-08-10)

Syfte:
- Generera context.json till AI Context Builder.
- Varje filnod innehåller:
  - is_content_full (bool)
  - git_sha1 (Git blob-id från GitHub API)
  - sha256_lf (SHA-256 över kanoniserad text: UTF-8, utan BOM, LF-rader)
- Toppnivå innehåller hash_index för snabb uppslagning: sha256_lf -> [paths], git_sha1 -> [paths].

Kör:
  python scripts/generate_full_context.py > context.json

Miljö:
  - Valfritt: GITHUB_TOKEN (höjer rate limit)
  - Kräver 'requests' paketet.
"""
import os
import sys
import re
import json
import hashlib
import codecs
import subprocess
from typing import Dict, Any, List, Optional
import requests

# --- Konfiguration ---
REPO = os.environ.get("ENGROVE_REPO", "Engrove/Engrove-Audio-Tools-2.0")
BRANCH = os.environ.get("ENGROVE_BRANCH", "main")

AI_CORE_INSTRUCTION_PATH = "docs/ai_protocols/AI_Core_Instruction.md"
AI_PROCESSOR_SCRIPT_PATH = "scripts/process_ai_instructions.py"
AI_METRICS_SCRIPT_PATH   = "scripts/process_ai_metrics.py"

# Maxstorlek (bytes) för textinnehåll som bäddas in direkt i context.json
MAX_EMBED_BYTES = int(os.environ.get("ENGROVE_MAX_EMBED_BYTES", "180000"))

# Filändelser som behandlas som binära/ej text
BINARY_EXT = {
    'png','jpg','jpeg','gif','webp','svg','ico','bmp','tiff',
    'woff','woff2','eot','ttf','otf',
    'zip','gz','tar','rar','7z',
    'pdf','doc','docx','xls','xlsx','ppt','pptx',
    'mp3','wav','ogg','mp4','mov','avi','mkv',
    'pyc','pyd','so','dll','exe','bin','dat'
}

# --- Regex för extraktion (låg ambitionsnivå, robust) ---
COMMENT_PATTERNS = [
    re.compile(r'//.*'),                     # JS/TS
    re.compile(r'/\*[\s\S]*?\*/'),           # JS/TS-block
    re.compile(r'<!--[\s\S]*?-->'),          # HTML
    re.compile(r'^\s*#.*', re.MULTILINE),    # Python/Shell
]
DEP_PATTERNS = [
    re.compile(r'^\s*import\s+([a-zA-Z0-9_./-]+)', re.MULTILINE),                 # py, js (simple)
    re.compile(r'^\s*from\s+([a-zA-Z0-9_.]+)\s+import\b', re.MULTILINE),          # python
    re.compile(r'require\([\'"]([^\'"]+)[\'"]\)', re.MULTILINE),                  # commonjs
    re.compile(r'^\s*import(?:.*?from)?\s*[\'"]([^\'"]+)[\'"]', re.MULTILINE),    # es modules
]

# --- Hjälp ---
def log(level: str, msg: str) -> None:
    print(f"[{level}] {msg}", file=sys.stderr)

def is_binary_path(path: str) -> bool:
    ext = (path.rsplit('.', 1)[-1] if '.' in path else '').lower()
    return ext in BINARY_EXT

def canon_text(s: str) -> str:
    # Ta bort UTF-8 BOM om sådan råkat hamna i strängen
    if s and s[0] == '\ufeff':
        s = s[1:]
    # CRLF/CR -> LF
    return s.replace('\r\n', '\n').replace('\r', '\n')

def sha256_lf_from_text(s: str) -> str:
    s = canon_text(s)
    b = s.encode('utf-8', 'strict')
    return hashlib.sha256(b).hexdigest()

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def headers() -> Dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN", "")
    h = {"User-Agent": "Engrove-Context-Builder/1.0"}
    if token:
        h["Authorization"] = f"token {token}"
    else:
        log("WARN", "No GITHUB_TOKEN; API rate limit kan bli låg.")
    return h

def api_get(url: str) -> Optional[Dict[str, Any]]:
    try:
        r = requests.get(url, headers=headers(), timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        log("ERROR", f"API GET fail {url}: {e}")
        return None

def get_repo_info() -> Dict[str, Any]:
    data = api_get(f"https://api.github.com/repos/{REPO}") or {}
    return data

def get_tree_recursive() -> List[Dict[str, Any]]:
    # Hämta SHA för gren
    ref = api_get(f"https://api.github.com/repos/{REPO}/git/refs/heads/{BRANCH}")
    if not ref or "object" not in ref:
        log("ERROR", f"Kunde inte läsa ref för {BRANCH}")
        return []
    sha = ref["object"]["sha"]
    tree = api_get(f"https://api.github.com/repos/{REPO}/git/trees/{sha}?recursive=1")
    if not tree or "tree" not in tree:
        log("ERROR", "Kunde inte läsa repo-träd.")
        return []
    return tree["tree"]

def raw_text(path: str) -> Optional[str]:
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}"
    try:
        r = requests.get(url, headers=headers(), timeout=30)
        r.raise_for_status()
        return r.content.decode("utf-8", "replace")
    except requests.exceptions.RequestException:
        log("WARN", f"Could not read raw text: {path}")
        return None

def raw_bytes(path: str) -> Optional[bytes]:
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}"
    try:
        r = requests.get(url, headers=headers(), timeout=30)
        r.raise_for_status()
        return r.content
    except requests.exceptions.RequestException:
        log("WARN", f"Could not read raw bytes: {path}")
        return None

def sanitize_comment(line: str) -> str:
    # Tar bort vanliga kommentars-prefix
    return re.sub(r'^[/*\\>#;"\s-]+|<!--|-->', '', line).strip()

def extract_patterns(content: str, pats: List[re.Pattern]) -> List[str]:
    out: List[str] = []
    for p in pats:
        for m in p.findall(content):
            if isinstance(m, tuple):
                m = m[0]
            s = sanitize_comment(str(m))
            if s and s not in out:
                out.append(s)
    return out

def run_subprocess_json(cmd: List[str]) -> Optional[Any]:
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8")
        txt = res.stdout.strip()
        if not txt:
            return None
        return json.loads(txt)
    except Exception as e:
        log("WARN", f"Subprocess misslyckades ({' '.join(cmd)}): {e}")
        return None

def get_processed_ai_config() -> Optional[Any]:
    if not os.path.exists(AI_PROCESSOR_SCRIPT_PATH):
        return None
    return run_subprocess_json([sys.executable, AI_PROCESSOR_SCRIPT_PATH])

def get_ai_performance_metrics() -> Optional[Any]:
    if not os.path.exists(AI_METRICS_SCRIPT_PATH):
        return None
    return run_subprocess_json([sys.executable, AI_METRICS_SCRIPT_PATH])

def build_file_structure(tree_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Bygger nästlad struktur av mappar och filer:
    - Mappar: { "<name>": { ... } }
    - Filer:  { "type":"file", "path":..., "size_bytes":..., "file_extension":..., "is_binary":..., "is_content_full":..., "comments":[], "dependencies":[], "content":?, "git_sha1":..., "sha256_lf":? }
    """
    file_structure: Dict[str, Any] = {}
    for it in tree_items:
        if it.get("type") != "blob":
            continue
        path = it.get("path")
        git_sha1 = it.get("sha")
        size = it.get("size", None)
        if not path:
            continue
        parts = path.split("/")
        cur = file_structure
        for d in parts[:-1]:
            cur = cur.setdefault(d, {})
        fname = parts[-1]
        file_extension = (fname.rsplit(".", 1)[-1] if "." in fname else "").lower()
        is_bin = is_binary_path(path)

        # Default filobjekt
        node: Dict[str, Any] = {
            "type": "file",
            "path": path,
            "size_bytes": size,
            "file_extension": file_extension,
            "is_binary": is_bin,
            "is_content_full": False,
            "comments": [],
            "dependencies": [],
            "content": None,
            "git_sha1": git_sha1,
            "sha256_lf": None
        }

        # Textinhämtning / hash
        if not is_bin:
            txt = raw_text(path)
            if txt is not None:
                txt_canon = canon_text(txt)
                b = txt_canon.encode("utf-8", "strict")
                node["is_content_full"] = (len(b) <= MAX_EMBED_BYTES)
                node["sha256_lf"] = sha256_bytes(b)
                if node["is_content_full"]:
                    node["content"] = txt_canon
                # Extra analys (lättvikt)
                try:
                    node["comments"] = extract_patterns(txt_canon, COMMENT_PATTERNS)[:50]
                    node["dependencies"] = extract_patterns(txt_canon, DEP_PATTERNS)[:50]
                except Exception as _:
                    pass
            else:
                # Kunde inte hämta text; försök bytes för hash
                rb = raw_bytes(path)
                if rb is not None:
                    try:
                        # Försök tolka text ändå (kanoniserad) för sha256_lf
                        txt = rb.decode("utf-8", "replace")
                        node["sha256_lf"] = sha256_lf_from_text(txt)
                    except Exception:
                        node["sha256_lf"] = None
        else:
            # Binär: läs bytes för full hash (ej _lf)
            rb = raw_bytes(path)
            if rb is not None:
                # Vi lämnar sha256_lf=None för binärer (inte patchbara i text)
                pass

        cur[fname] = node
    return file_structure

def build_hash_index(file_structure: Dict[str, Any]) -> Dict[str, Dict[str, List[str]]]:
    idx_sha256: Dict[str, List[str]] = {}
    idx_gitsha1: Dict[str, List[str]] = {}

    def walk(node: Any):
        if isinstance(node, dict) and node.get("type") == "file":
            p = node.get("path")
            s256 = node.get("sha256_lf")
            gsha = node.get("git_sha1")
            if s256:
                idx_sha256.setdefault(s256, []).append(p)
            if gsha:
                idx_gitsha1.setdefault(gsha, []).append(p)
        elif isinstance(node, dict):
            for v in node.values():
                walk(v)

    walk(file_structure)
    return {"sha256_lf": idx_sha256, "git_sha1": idx_gitsha1}

def main() -> None:
    repo_info = get_repo_info()
    tree = get_tree_recursive()

    # AI-core-instruktion (valfritt, text)
    core_instruction = None
    txt = raw_text(AI_CORE_INSTRUCTION_PATH)
    if txt is not None:
        core_instruction = txt

    processed_ai = get_processed_ai_config()
    perf_metrics = get_ai_performance_metrics()

    fs = build_file_structure(tree)
    hash_index = build_hash_index(fs)

    final = {
        "project_overview": {
            "repository": REPO,
            "branch": BRANCH,
            "description": repo_info.get("description"),
            "primary_language": repo_info.get("language"),
            "last_updated_at": repo_info.get("pushed_at"),
            "url": repo_info.get("html_url")
        },
        "ai_instructions": core_instruction or "Core instruction could not be loaded.",
        "ai_config_processed": processed_ai,
        "ai_performance_metrics": perf_metrics,
        "file_structure": fs,
        "hash_index": hash_index
    }

    print(json.dumps(final, ensure_ascii=False, indent=2))
    log("INFO", "Context generation complete.")

if __name__ == "__main__":
    main()
