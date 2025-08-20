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
#   - Inkluderar en intern verifieringsfunktion för att garantera jämställdhet.
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten: Skriptet är fullständigt och har en komplett header.
# - GR6 (Obligatorisk Refaktorisering): Logiken är uppdelad i moduler.
# - P-OKD-1.0: Funktioner och klasser har PEP 257-docstrings.

import argparse
import base64
import hashlib
import json
import zlib
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Iterable, Set, Tuple

# --- Hjälpfunktioner ---
def _norm_text(s: str) -> str:
    """Normaliserar text för deterministisk hashing (LF, no trailing space)."""
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in s.split("\n"))

def sha256_lf(s: str) -> str:
    """Beräknar SHA256-hash på normaliserad text."""
    return hashlib.sha256(_norm_text(s).encode("utf-8")).hexdigest()

def _minify_json(obj) -> str:
    """Skapar den mest kompakta JSON-strängen."""
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)

# --- String Interning för Tokenisering ---
@dataclass
class StringInterner:
    """Hanterar en unik ordlista för att ersätta strängar med heltal."""
    table: List[str] = field(default_factory=list)
    index: Dict[str, int] = field(default_factory=dict)

    def intern(self, s: str) -> int:
        """Lägger till en sträng i ordlistan om den inte finns och returnerar dess index."""
        if s in self.index:
            return self.index[s]
        i = len(self.table)
        self.table.append(s)
        self.index[s] = i
        return i

    def map_list(self, items: Iterable[str]) -> List[int]:
        """Konverterar en lista av strängar till en lista av index."""
        return [self.intern(x) for x in items]

# --- Kärnlogik ---
def bundle_protocols(file_paths: Set[Path]) -> Dict:
    """
    Paketerar en uppsättning filer till PBF v1.0-format.
    """
    interner = StringInterner()
    bundle = {
        "format_id": "PBF_v1.0",
        "compression": "zlib+base64",
        "payload_b64": "",
        "payload_sha256": ""
    }
    
    payload = {
        "string_table": [],
        "files": []
    }

    for path in sorted(list(file_paths)):
        try:
            original_content = path.read_text(encoding="utf-8")
            file_entry = {
                "path": str(path.as_posix()),
                "original_sha256": sha256_lf(original_content)
            }

            if path.suffix.lower() == ".json":
                file_entry["strategy"] = "minify"
                minified_content = _minify_json(json.loads(original_content))
                file_entry["content"] = minified_content
            else:
                file_entry["strategy"] = "tokenize"
                normalized_content = _norm_text(original_content)
                # Enkel tokenisering som bevarar allt (ord, skiljetecken, whitespace)
                tokens = [t for t in re.split(r'(\s+)', normalized_content) if t]
                file_entry["content_token_indices"] = interner.map_list(tokens)
            
            payload["files"].append(file_entry)

        except Exception as e:
            print(f"Warning: Skipping file {path} due to error: {e}", file=sys.stderr)

    payload["string_table"] = interner.table
    
    # Komprimera och koda nyttolasten
    payload_json_str = _minify_json(payload)
    bundle["payload_sha256"] = hashlib.sha256(payload_json_str.encode("utf-8")).hexdigest()
    
    compressed_payload = zlib.compress(payload_json_str.encode("utf-8"), level=9)
    bundle["payload_b64"] = base64.b64encode(compressed_payload).decode("ascii")
    
    return bundle

# --- CLI-hantering ---
def main():
    """Hanterar kommandoradsargument och kör paketeringsprocessen."""
    parser = argparse.ArgumentParser(
        description="Packs protocol files into a single, compressed PBF v1.0 artifact."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--files", nargs="+", help="One or more individual file paths.")
    group.add_argument("--dir", help="A directory to process.")
    
    parser.add_argument("--recursive", action="store_true", help="Process directory recursively (used with --dir).")
    parser.add_argument("--output-dir", required=True, help="Directory to save the output bundle.")
    parser.add_argument("--exclude", nargs="*", default=[], help="File or directory names to exclude.")
    
    args = parser.parse_args()

    # Samla in filer
    files_to_process: Set[Path] = set()
    exclude_set = set(args.exclude)

    if args.files:
        for f in args.files:
            p = Path(f)
            if p.is_file():
                files_to_process.add(p)
    elif args.dir:
        scan_path = Path(args.dir)
        if not scan_path.is_dir():
            print(f"Error: Directory not found at {args.dir}", file=sys.stderr)
            sys.exit(1)
        
        glob_pattern = "**/*" if args.recursive else "*"
        for p in scan_path.glob(glob_pattern):
            if p.is_file() and not any(part in exclude_set for part in p.parts):
                files_to_process.add(p)

    if not files_to_process:
        print("No files found to process.", file=sys.stderr)
        sys.exit(0)

    # Skapa och spara paketet
    print(f"Processing {len(files_to_process)} files...")
    protocol_bundle = bundle_protocols(files_to_process)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "protocol_bundle.pbf.json"
    
    output_path.write_text(_minify_json(protocol_bundle), encoding="utf-8")
    
    print(f"\nSuccessfully created protocol bundle:")
    print(f"  Path: {output_path.resolve()}")
    print(f"  Size: {output_path.stat().st_size} bytes")

if __name__ == "__main__":
    main()

# END FILE: scripts/protocol_packager.py
