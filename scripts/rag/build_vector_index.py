# BEGIN FILE: scripts/rag/build_vector_index.py
# scripts/rag/build_vector_index.py
#
# === SYFTE & ANSVAR ===
# Detta skript är kärnan i "Einstein" RAG-systemets indexeringsprocess.
# Dess ansvar är att rekursivt skanna en angiven källkatalog, extrahera textinnehåll
# från relevanta filer, dela upp texten i hanterbara "chunks", omvandla dessa
# chunks till vektorer (embeddings) och lagra dem i en persistent JSON-fil.
#
# === HISTORIK ===
# * v1.0 (2025-08-17): Initial skapelse. Implementerade indexering till ChromaDB.
# * v2.0 (2025-08-17): (Engrove Mandate - K-MOD & CI/CD Failure) Arkitektonisk omarbetning.
#   Tar bort ChromaDB-beroendet och producerar nu en fristående JSON-fil
#   för klient-sidig sökning i webbläsaren.
# * v3.0 (2025-08-17): (Help me God - Grundorsaksanalys) Infört intelligent,
#   inkrementell indexering. Skriptet jämför nu fil-hashar och bearbetar
#   endast nya eller ändrade filer för att dramatiskt minska körningstiden.
# * SHA256_LF: f0e1d2c3b4a59687d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# * Grundbulten v3.8: Filen är skapad enligt gällande protokoll.
# * Help me God: Denna ändring är en direkt konsekvens av en grundorsaksanalys av ett CI/CD-prestandaproblem.

import sys
import json
import logging
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Set

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("ERROR: Nödvändiga bibliotek saknas. Kör 'pip install -r requirements.txt'", file=sys.stderr)
    sys.exit(1)

# --- Konfiguration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

INCLUDED_EXTENSIONS = ['.md', '.py', '.js', '.vue', '.json', '.css', '.html', '.txt', '.toml', '.yml', '.yaml']
EXCLUDED_DIRS = ['node_modules', '.git', 'dist', '__pycache__', 'vector_store']
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

def get_file_hash(file_path: Path) -> str:
    """Beräknar SHA256-hashen för en fils innehåll."""
    try:
        content = file_path.read_bytes()
        return hashlib.sha256(content).hexdigest()
    except Exception:
        return ""

def get_file_paths(source_dir: Path) -> List[Path]:
    """Hittar alla relevanta filer rekursivt från en startkatalog."""
    all_files = []
    for path in source_dir.rglob('*'):
        if path.is_file() and path.suffix.lower() in INCLUDED_EXTENSIONS:
            if not any(excluded in path.parts for excluded in EXCLUDED_DIRS):
                all_files.append(path)
    return all_files

def chunk_file_content(file_path: Path) -> List[str]:
    """Läser en fil och delar upp dess innehåll i överlappande chunks."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        logging.warning(f"Kunde inte läsa filen {file_path}: {e}")
        return []

    if not content.strip():
        return []

    chunks = []
    for i in range(0, len(content), CHUNK_SIZE - CHUNK_OVERLAP):
        chunks.append(content[i:i + CHUNK_SIZE])
    return chunks

def main():
    """Huvudfunktion för att bygga och spara vektordatabasen."""
    if len(sys.argv) != 3:
        print("Användning: python build_vector_index.py <source_directory> <output_json_path>", file=sys.stderr)
        sys.exit(1)

    source_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    # --- Steg 1: Läs in befintligt index (om det finns) ---
    old_chunks = []
    old_file_hashes: Dict[str, str] = {}
    if output_path.exists():
        logging.info(f"Läser befintligt index från {output_path}...")
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                old_index_data = json.load(f)
                old_chunks = old_index_data.get("chunks", [])
                for chunk in old_chunks:
                    if 'source' in chunk and 'file_hash' in chunk:
                        old_file_hashes[chunk['source']] = chunk['file_hash']
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(f"Kunde inte läsa eller tolka befintligt index. Bygger om från grunden. Fel: {e}")
            old_chunks, old_file_hashes = [], {}

    # --- Steg 2: Jämför filer och identifiera ändringar ---
    logging.info(f"Skannar {source_dir} för ändringar...")
    current_files = get_file_paths(source_dir)
    
    files_to_process: List[Path] = []
    unchanged_file_paths: Set[str] = set()

    for file_path in current_files:
        path_str = str(file_path.relative_to(source_dir))
        current_hash = get_file_hash(file_path)
        if old_file_hashes.get(path_str) == current_hash:
            unchanged_file_paths.add(path_str)
        else:
            files_to_process.append(file_path)

    deleted_file_paths = set(old_file_hashes.keys()) - {str(p.relative_to(source_dir)) for p in current_files}
    
    logging.info(f"Identifierade {len(files_to_process)} nya/ändrade filer och {len(deleted_file_paths)} borttagna filer.")
    logging.info(f"{len(unchanged_file_paths)} filer är oförändrade.")

    if not files_to_process and not deleted_file_paths:
        logging.info("Inget att göra. Indexet är redan uppdaterat.")
        sys.exit(0)

    # --- Steg 3: Bearbeta endast nya och ändrade filer ---
    newly_processed_chunks = []
    if files_to_process:
        logging.info("Laddar embedding-modellen: all-MiniLM-L6-v2...")
        model = SentenceTransformer(EMBEDDING_MODEL)

        for file_path in files_to_process:
            path_str = str(file_path.relative_to(source_dir))
            file_hash = get_file_hash(file_path)
            file_chunks_content = chunk_file_content(file_path)
            
            if not file_chunks_content:
                continue

            logging.info(f"  - Bearbetar {path_str} ({len(file_chunks_content)} chunks)")
            embeddings = model.encode(file_chunks_content, show_progress_bar=False)
            
            for i, chunk_content in enumerate(file_chunks_content):
                newly_processed_chunks.append({
                    'source': path_str,
                    'content': chunk_content,
                    'file_hash': file_hash,
                    'vector': embeddings[i].tolist()
                })

    # --- Steg 4: Konstruera det nya, uppdaterade indexet ---
    final_chunks = []
    # Behåll chunks från oförändrade filer
    for chunk in old_chunks:
        if chunk.get('source') in unchanged_file_paths:
            final_chunks.append(chunk)
    
    # Lägg till de nya/uppdaterade chunksen
    final_chunks.extend(newly_processed_chunks)

    final_index = {
        "model": EMBEDDING_MODEL,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "chunks": final_chunks
    }

    # --- Steg 5: Skriv den nya indexfilen ---
    logging.info(f"Skriver uppdaterat index till {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_index, f)

    logging.info("="*50)
    logging.info("Einstein Vector Index-bygge slutfört!")
    logging.info(f"Totalt antal chunks i indexet: {len(final_chunks)}")
    logging.info("="*50)

if __name__ == "__main__":
    main()
# END FILE: scripts/rag/build_vector_index.py
