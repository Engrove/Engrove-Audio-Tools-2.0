#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# scripts/build_document_manifest.py

import json
import re
import hashlib
from pathlib import Path

# --- Konfiguration ---
ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / 'docs'
OUTPUT_FILE = DOCS_DIR / 'document_manifest.json'

# Filer och mappar i docs/ som INTE är projektdokumentation och ska ignoreras
EXCLUDE_FILES = ['protocol_bundle.md']
EXCLUDE_DIRS = ['ai_protocols', 'ai', 'compact']

# Regex för att extrahera ett enkelt syfte från Markdown-filer
PURPOSE_REGEX = re.compile(r"^(?:#+)?\s*(?:SYFTE|SYFTE & ANSVAR|Purpose)[\s&ANSVAR]*:?\s*(.*)", re.IGNORECASE | re.MULTILINE)

def main():
    print("Building document manifest from top-level docs...")
    manifest = []

    for md_file in DOCS_DIR.glob('*.md'):
        # Hoppa över filer och mappar som är exkluderade
        if md_file.name in EXCLUDE_FILES or any(d in md_file.parts for d in EXCLUDE_DIRS):
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
            
            # 1. Extrahera syfte
            purpose_match = PURPOSE_REGEX.search(content)
            purpose = purpose_match.group(1).strip() if purpose_match else "No purpose statement found."

            # 2. Skapa nyckelord från filnamnet
            keywords = [kw.lower() for kw in md_file.stem.replace('_', ' ').split()]
            
            # 3. Beräkna checksumma
            sha256_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

            manifest.append({
                "file_path": f"docs/{md_file.name}",
                "purpose": purpose,
                "keywords": keywords,
                "sha256": sha256_hash
            })
            print(f"  + Indexed: {md_file.name}")

        except Exception as e:
            print(f"  - ERROR: Could not process {md_file.name}. Reason: {e}")

    # Sortera för konsekvent output
    manifest.sort(key=lambda x: x['file_path'])
    
    print(f"\nManifest built with {len(manifest)} entries. Writing to {OUTPUT_FILE}...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    print("Done.")

if __name__ == '__main__':
    main()
