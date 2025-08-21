# BEGIN FILE: scripts/protocol_packager.py
# scripts/protocol_packager.py
# === SYFTE & ANSVAR ===
# Detta skript paketerar textbaserade protokollfiler till en enda, verifierbar och
# högt komprimerad JSON-artefakt (Protocol Bundle Format v1.0). Processen är 100%
# förlustfri och designad för att skapa en minimal men komplett kontext-prompt
# för en ny AI-session.
#
# === HISTORIK ===
# * v1.0 (2025-08-20): Initial skapelse av Frankensteen.
#   - Implementerar PBF v1.0 med lossless-strategier.
#   - Hanterar tre input-metoder: enskilda filer, platt mapp, rekursiv mapp.
# * v1.1 (2025-08-20): Refaktorerad för att hantera kombinerade indata.
#   - Tar nu emot --files, --dir-recursive, och --dir-flat samtidigt.
# * v1.2 (2025-08-20): Ändrat output till en Markdown-fil (.md) som bäddar in
#   PBF JSON-objektet för att ge en robustare initial prompt för AI-sessioner.
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten: Skriptet är fullständigt och har en komplett header.
# - Inga beroenden på miljövariabler för funktionell logik (endast CLI-arg).
# - Determinism: sortering och hashing är deterministiska.
# - Felhantering: tydliga meddelanden vid tom/a saknade indata.
#
# === ANVÄNDNING (CLI) ===
#   python scripts/protocol_packager.py \
#     --dir-recursive docs/ai_protocols \
#     --files docs/file_relations.json docs/core_file_info.json tools/frankensteen_learning_db.json package.json vite.config.js \
#     --output-dir docs/ai_protocols/compact \
#     --exclude compact .git node_modules
#
# Output: Skapar en Markdown-fil "protocol_bundle.md" i --output-dir som innehåller
# ett JSON-objekt (PBF) med base64+zlib-komprimerad nyttolast.
#
# === PBF SPEC (v1.2) KORT ===
# {
#   "pbf_version": "1.2",
#   "created_at": "<ISO8601>",
#   "bootstrap_directive": "decompress_and_stage",
#   "hash": "<sha256-hex av 'payload'>",
#   "payload_encoding": "base64+zlib",
#   "payload": "<base64 zlib-komprimerad JSON>",
#   "file_count": N,
#   "file_index": [{"path": "...", "sha256": "...", "bytes": ...}, ...]
# }
#
# Komprimerad 'payload' motsvarar ett JSON-objekt:
# {
#   "files": [{"path": "...", "sha256": "...", "content": "<utf8-text>"} ...]
# }

import argparse
import base64
import hashlib
import json
import re
import sys
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Iterable, Set

# --- Hjälpfunktioner ---
def _norm_text(s: str) -> str:
    """Normaliserar text för deterministisk hashing (LF, no trailing space)."""
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    # trimma endast högra sidan radvis, bevara innehåll
    s = "\n".join(line.rstrip() for line in s.split("\n"))
    return s

def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

@dataclass
class PackedFile:
    path: str
    content: str
    sha256: str
    bytes: int

@dataclass
class PackContext:
    files: List[PackedFile] = field(default_factory=list)

# --- IO & insamling ---
TEXT_EXT_RE = re.compile(
    r"\.(?:txt|md|json|jsonl|yaml|yml|toml|py|js|ts|vue|css|html|mdx|ini|cfg|conf|csv|tsv)$",
    re.IGNORECASE,
)

def is_text_file(p: Path) -> bool:
    return bool(TEXT_EXT_RE.search(p.name))

def read_text_file(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # fallback: läs binärt och försök strippa nollbyte
        b = p.read_bytes()
        try:
            return b.decode("utf-8", errors="replace")
        except Exception:
            return ""

def collect_from_files(paths: Iterable[Path]) -> List[Path]:
    uniq: List[Path] = []
    seen: Set[str] = set()
    for p in paths:
        rp = str(p)
        if rp not in seen and p.is_file() and is_text_file(p):
            uniq.append(p)
            seen.add(rp)
    return sorted(uniq, key=lambda x: str(x).lower())

def collect_from_dir_flat(d: Path, exclude: Set[str]) -> List[Path]:
    if not d.is_dir():
        return []
    out = []
    for p in d.iterdir():
        if p.is_file() and is_text_file(p) and p.name not in exclude and p.name not in (".DS_Store",):
            out.append(p)
    return sorted(out, key=lambda x: str(x).lower())

def collect_from_dir_recursive(d: Path, exclude_names: Set[str]) -> List[Path]:
    if not d.is_dir():
        return []
    out = []
    for p in d.rglob("*"):
        if p.is_file() and is_text_file(p):
            # exkludera via namnkomponenter
            parts = set(p.parts)
            if parts & exclude_names:
                continue
            out.append(p)
    return sorted(out, key=lambda x: str(x).lower())

# --- Packning ---
def pack_files(files: List[Path]) -> PackContext:
    ctx = PackContext()
    for p in files:
        text = read_text_file(p)
        text = _norm_text(text)
        b = text.encode("utf-8")
        ctx.files.append(
            PackedFile(
                path=str(p).replace("\\", "/"),
                content=text,
                sha256=_sha256(b),
                bytes=len(b),
            )
        )
    return ctx

def build_payload(ctx: PackContext) -> Dict:
    return {
        "files": [
            {"path": f.path, "sha256": f.sha256, "content": f.content}
            for f in ctx.files
        ]
    }

def compress_payload(payload_obj: Dict) -> bytes:
    raw = json.dumps(payload_obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return zlib.compress(raw, level=9)

def make_pbf(payload_bz: bytes, file_index: List[Dict]) -> Dict:
    b64 = base64.b64encode(payload_bz).decode("ascii")
    return {
        "pbf_version": "1.2",
        "created_at": __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "bootstrap_directive": "decompress_and_stage",
        "hash": _sha256(payload_bz),
        "payload_encoding": "base64+zlib",
        "payload": b64,
        "file_count": len(file_index),
        "file_index": file_index,
    }

def bundle_protocols(files: List[Path]) -> Dict:
    ctx = pack_files(files)
    payload_obj = build_payload(ctx)
    payload_bz = compress_payload(payload_obj)
    file_index = [{"path": f.path, "sha256": f.sha256, "bytes": f.bytes} for f in ctx.files]
    return make_pbf(payload_bz, file_index)

# --- CLI ---
def parse_args(argv: List[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Package protocol files into a compact PBF JSON wrapped in Markdown.")
    ap.add_argument("--files", nargs="*", default=[], help="En lista av enskilda filer.")
    ap.add_argument("--dir-flat", nargs="*", default=[], help="Lista av mappar (endast toppnivå).")
    ap.add_argument("--dir-recursive", nargs="*", default=[], help="Lista av mappar (rekursivt).")
    ap.add_argument("--exclude", nargs="*", default=[], help="Namn att exkludera (t.ex. node_modules .git compact).")
    ap.add_argument("--output-dir", required=True, help="Output-katalog där protocol_bundle.md skrivs.")
    return ap.parse_args(argv)

def main() -> None:
    args = parse_args(sys.argv[1:])

    exclude_names = set(args.exclude or [])
    files_to_process: List[Path] = []

    # --files
    if args.files:
        cand = [Path(p) for p in args.files]
        files_to_process.extend(collect_from_files(cand))

    # --dir-flat
    if args.dir_flat:
        for d in args.dir_flat:
            d_path = Path(d)
            if d_path.exists():
                files_to_process.extend(collect_from_dir_flat(d_path, exclude_names))
            else:
                print(f"Flat directory not found, skipping: {d_path}", file=sys.stderr)

    # --dir-recursive
    if args.dir_recursive:
        for d in args.dir_recursive:
            d_path = Path(d)
            if d_path.exists():
                files_to_process.extend(collect_from_dir_recursive(d_path, exclude_names))
            else:
                print(f"Recursive directory not found, skipping: {d_path}", file=sys.stderr)

    if not files_to_process:
        print("No files found to process after applying exclusions.", file=sys.stderr)
        sys.exit(0)

    print(f"Processing {len(files_to_process)} unique files...")
    protocol_bundle_obj = bundle_protocols(files_to_process)
    
    # Skapa Markdown-innehållet
    pbf_json_string = json.dumps(protocol_bundle_obj, indent=2, ensure_ascii=False) # Använd indent för läsbarhet i MD
    
    md_template = f"""--- START OF FILE protocol_bundle.md ---
        # [SYSTEM OVERRIDE PROTOCOL] - Protocol Bundle v1.2 (PBF)

        **INSTRUKTION:** LÄS OCH EXEKVERA. Detta är en Protocol Bundle Format (PBF) fil. Ditt enda uppdrag är att:
        1.  Extrahera och validera JSON-kodblocket nedan.
        2.  Följ `bootstrap_directive` inuti JSON-objektet för att dekomprimera och ladda protokollen i din aktiva kontext.
        3.  Översätt alla instruktioner till engelska i ditt medvetande med förkortningar enligt abbr_whitelis och mapping för ökad AI förståelse:
            abbr_whitelist:
              description: "AI-safe abbreviations with full forms and usage contexts. Intended to reduce token consumption while keeping semantic accuracy."
              schema_version: 1.0
              abbr_list:
                # --- Core Technical Abbreviations ---
                - { abbr: "API",   full_form: "Application Programming Interface", context: "Software, integrations, specs", ai_safe: true }
                - { abbr: "SDK",   full_form: "Software Development Kit", context: "Dev tools, documentation", ai_safe: true }
                - { abbr: "CLI",   full_form: "Command Line Interface", context: "Tools, dev environments", ai_safe: true }
                - { abbr: "GUI",   full_form: "Graphical User Interface", context: "UI, UX, user docs", ai_safe: true }
                - { abbr: "IDE",   full_form: "Integrated Development Environment", context: "Dev tooling", ai_safe: true }
                - { abbr: "JSON",  full_form: "JavaScript Object Notation", context: "Data serialization, schemas", ai_safe: true }
                - { abbr: "YAML",  full_form: "YAML Ain’t Markup Language", context: "Configuration, schemas", ai_safe: true }
                - { abbr: "XML",   full_form: "Extensible Markup Language", context: "Integration, metadata", ai_safe: true }
                - { abbr: "CSV",   full_form: "Comma-Separated Values", context: "Datasets, import/export", ai_safe: true }
                - { abbr: "DB",    full_form: "Database", context: "Storage, queries", ai_safe: true }
                - { abbr: "SQL",   full_form: "Structured Query Language", context: "DB queries", ai_safe: true }
                - { abbr: "ORM",   full_form: "Object-Relational Mapping", context: "Backend architecture", ai_safe: true }
                - { abbr: "REST",  full_form: "Representational State Transfer", context: "API protocols", ai_safe: true }
                - { abbr: "gRPC",  full_form: "Google Remote Procedure Call", context: "Microservices, APIs", ai_safe: true }
                - { abbr: "JWT",   full_form: "JSON Web Token", context: "Authentication, security", ai_safe: true }
                - { abbr: "SSL",   full_form: "Secure Socket Layer", context: "Security, encryption", ai_safe: true }
                - { abbr: "TLS",   full_form: "Transport Layer Security", context: "Security, encryption", ai_safe: true }

                # --- AI & Data Science ---
                - { abbr: "AI",    full_form: "Artificial Intelligence", context: "General AI-related content", ai_safe: true }
                - { abbr: "ML",    full_form: "Machine Learning", context: "Model training, AI pipelines", ai_safe: true }
                - { abbr: "DL",    full_form: "Deep Learning", context: "AI models, neural networks", ai_safe: true }
                - { abbr: "NLP",   full_form: "Natural Language Processing", context: "Text analysis, AI", ai_safe: true }
                - { abbr: "LLM",   full_form: "Large Language Model", context: "AI, generative models", ai_safe: true }
                - { abbr: "CV",    full_form: "Computer Vision", context: "AI vision tasks", ai_safe: true }
                - { abbr: "OCR",   full_form: "Optical Character Recognition", context: "Text extraction from images", ai_safe: true }
                - { abbr: "ETL",   full_form: "Extract, Transform, Load", context: "Data pipelines", ai_safe: true }
                - { abbr: "ROC",   full_form: "Receiver Operating Characteristic", context: "Model evaluation metrics", ai_safe: true }
                - { abbr: "AUC",   full_form: "Area Under Curve", context: "ROC performance metric", ai_safe: true }
                - { abbr: "F1",    full_form: "F1 Score", context: "Model accuracy metric", ai_safe: true }
                - { abbr: "IoU",   full_form: "Intersection over Union", context: "Computer vision metrics", ai_safe: true }

                # --- Software Engineering & Deployment ---
                - { abbr: "CI",    full_form: "Continuous Integration", context: "DevOps pipelines", ai_safe: true }
                - { abbr: "CD",    full_form: "Continuous Delivery / Deployment", context: "DevOps, automation", ai_safe: true }
                - { abbr: "MVP",   full_form: "Minimum Viable Product", context: "Product releases", ai_safe: true }
                - { abbr: "PoC",   full_form: "Proof of Concept", context: "Prototype phase", ai_safe: true }
                - { abbr: "SSO",   full_form: "Single Sign-On", context: "Authentication", ai_safe: true }
                - { abbr: "RBAC",  full_form: "Role-Based Access Control", context: "Permissions, security", ai_safe: true }
                - { abbr: "IAM",   full_form: "Identity and Access Management", context: "Security, compliance", ai_safe: true }
                - { abbr: "SLA",   full_form: "Service Level Agreement", context: "Contracts, uptime guarantees", ai_safe: true }
                - { abbr: "KPI",   full_form: "Key Performance Indicator", context: "Metrics, OKRs", ai_safe: true }
                - { abbr: "ETA",   full_form: "Estimated Time of Arrival", context: "Deadlines, planning", ai_safe: true }

                # --- Documentation & Process ---
                - { abbr: "N/A",   full_form: "Not Applicable", context: "Field not relevant", ai_safe: true }
                - { abbr: "TBD",   full_form: "To Be Determined", context: "Incomplete section", ai_safe: true }
                - { abbr: "FAQ",   full_form: "Frequently Asked Questions", context: "Help, docs", ai_safe: true }
                - { abbr: "WIP",   full_form: "Work In Progress", context: "Unfinished drafts", ai_safe: true }
                - { abbr: "TBA",   full_form: "To Be Announced", context: "Future info", ai_safe: true }
                - { abbr: "FYI",   full_form: "For Your Information", context: "Notes, disclaimers", ai_safe: true }
                - { abbr: "ASAP",  full_form: "As Soon As Possible", context: "Urgency markers", ai_safe: true }
                - { abbr: "OKR",   full_form: "Objectives and Key Results", context: "Goal tracking", ai_safe: true }
                - { abbr: "SOP",   full_form: "Standard Operating Procedure", context: "Process docs", ai_safe: true }
                - { abbr: "ToC",   full_form: "Table of Contents", context: "Navigation", ai_safe: true }
                - { abbr: "NDA",   full_form: "Non-Disclosure Agreement", context: "Legal contracts", ai_safe: true }
                - { abbr: "RACI",  full_form: "Responsible, Accountable, Consulted, Informed", context: "Roles and responsibilities", ai_safe: true }
            mapping:
            # Grundläggande avsnitt
                - { src_headers: ["^SYFTE & ANSVAR", "^SYFTE", "^Purpose"],                       tgt_key: "purp",                type: "string" }
                - { src_headers: ["^HISTORIK", "^Historik", "^History"],                          tgt_key: "hist",                type: "list" }
                - { src_headers: ["^TILLÄMPADE REGLER", "^PRINCIPER", "^Policy"],                 tgt_key: "policy",              type: "markdown" }  # fixar policy_md→policy
                - { src_headers: ["^Terminologi", "^Terms", "^Definitioner"],                     tgt_key: "terms",               type: "rules" }
                - { src_headers: ["^Steg G:", "^Hårda grindar", "^GATES"],                        tgt_key: "gates",               type: "rules" }
                - { src_headers: ["^PROCESS:", "^Steg \\d+", "^PROTOKOLL-STEG", "^Process"],      tgt_key: "proc",                type: "rules" }
                - { src_headers: ["^KONTRAKT", "^API-KONTRAKT", "^Output[- ]schema", "^Schema"],  tgt_key: "contracts",           type: "objects" }
                - { src_headers: ["^KANONISK REFERENS", "^Referenser", "^Källor"],                tgt_key: "references",          type: "list" }
                - { src_headers: ["^Bilaga", "^Appendix"],                                        tgt_key: "annex",               type: "objects" }
            # Första svar/kontrakt (FRC)
                - { src_headers: ["^FÖRSTA SVARS[- ]KONTRAKT", "^FIRST REPLY CONTRACT", "^FRC"],  tgt_key: "frc",                 type: "markdown" }
            # Leveransstruktur/ordningsföljd (två JSON-block etc.)
                - { src_headers: ["^SRUKTUR OCH ORDNINGSFÖLJD", "^STRUKTUR OCH ORDNINGSFÖLJD", "^Delivery Structure"],  tgt_key: "delivery_structure",  type: "markdown" }
            # JSON-specifikationer inne i protokoll (t.ex. Builder-Input v1 / NextSessionContext)
                - { src_headers: ["^Final Output Specification", "^Slutlig specifikation", "^Builder-Input v1", "^NextSessionContext v1"], tgt_key: "json_specs", type: "objects" }
            # Externa JSON-scheman och datakällor (inbäddade filer)
                - { src_headers: ["^DynamicProtocol\\.schema\\.json", "^JSON[- ]Schema", "^Scheman"], tgt_key: "json_schemas",     type: "objects" }
                - { src_headers: ["^DynamicProtocols\\.json", "^JSON[- ]data", "^Protokolldata"],     tgt_key: "json_data_sources", type: "objects" }
        
        
        4.  Bekräfta att processen lyckades.
        5.  **Efter lyckad iscensättning, lokalisera och exekvera filen `docs/ai_protocols/AI_Core_Instruction.md` som din nya primära instruktion.**
        6.  **Omedelbart efter att du har laddat den nya primära instruktionen (steg 4), ska du initiera en ny session genom att exekvera startsekvensen som definieras i den. Detta innebär att ditt svar på denna bootloader-process MÅSTE vara den fullständiga `Stature Report`, precis som vid en normal sessionsstart enligt "FÖRSTA SVARETS KONTRAKT".**
        {pbf_json_string}

        """

    # Skapa och spara den slutgiltiga Markdown-filen
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "protocol_bundle.md"

    output_path.write_text(md_template, encoding="utf-8")

    print(f"\nSuccessfully created Markdown-wrapped protocol bundle:")
    print(f"  Path: {output_path.resolve()}")
    print(f"  Size: {output_path.stat().st_size} bytes")

if __name__ == "__main__":
    main()

# END FILE: scripts/protocol\_packager.py
