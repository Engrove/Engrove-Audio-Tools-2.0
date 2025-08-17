# BEGIN FILE: scripts/rag/build_vector_index.py
# scripts/rag/build_vector_index.py
#
# === SYFTE & ANSVAR ===
# Detta skript är kärnan i "Einstein" RAG-systemets indexeringsprocess.
# Dess ansvar är att rekursivt skanna en angiven källkatalog, extrahera textinnehåll
# från relevanta filer, dela upp texten i hanterbara "chunks", omvandla dessa
# chunks till vektorer (embeddings) och spara allt i en enda, portabel JSON-fil.
#
# === HISTORIK ===
# * v1.0 (2025-08-17): Initial skapelse. Implementerade indexering till ChromaDB.
# * v2.0 (2025-08-17): (Engrove Mandate - K-MOD & CI/CD Failure) Arkitektonisk omarbetning.
#   Tar bort ChromaDB-beroendet och producerar nu en fristående JSON-fil
#   för klient-sidig sökning i webbläsaren. Detta löser GitHubs filstorleksgräns.
# * SHA256_LF: a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# * Grundbulten v3.8: Filen är skapad enligt gällande protokoll.
# * K-MOD: Denna arkitektur är ett direkt resultat av en K-MOD-session.
# * Help me God: Denna ändring är en direkt konsekvens av en grundorsaksanalys av ett CI/CD-fel.

import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone

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

def get_file_paths(source_dir: Path) -> list[Path]:
    """Hittar alla relevanta filer rekursivt från en startkatalog."""
    logging.info(f"Skannar {source_dir} för relevanta filer...")
    all_files = []
    for path in source_dir.rglob('*'):
        if path.is_file() and path.suffix.lower() in INCLUDED_EXTENSIONS:
            if not any(excluded in path.parts for excluded in EXCLUDED_DIRS):
                all_files.append(path)
    logging.info(f"Hittade {len(all_files)} filer att indexera.")
    return all_files

def chunk_file_content(file_path: Path) -> list[str]:
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
        chunk = content[i:i + CHUNK_SIZE]
        chunks.append(chunk)
    return chunks

def main():
    """Huvudfunktion för att bygga och spara JSON-indexet."""
    if len(sys.argv) != 3:
        print("Användning: python build_vector_index.py <source_directory> <output_json_path>", file=sys.stderr)
        sys.exit(1)

    source_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not source_dir.is_dir():
        logging.error(f"Källkatalogen '{source_dir}' existerar inte.")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    files_to_index = get_file_paths(source_dir)

    all_chunks = []
    logging.info("Skapar text-chunks för varje fil...")
    for file_path in files_to_index:
        file_chunks = chunk_file_content(file_path)
        for chunk_content in file_chunks:
            all_chunks.append({
                'source': str(file_path),
                'content': chunk_content
            })
    
    if not all_chunks:
        logging.warning("Inga text-chunks kunde skapas. Skapar en tom indexfil.")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"model": EMBEDDING_MODEL, "createdAt": datetime.now(timezone.utc).isoformat(), "chunks": []}, f)
        sys.exit(0)

    logging.info(f"Laddar embedding-modellen: {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    documents_to_embed = [chunk['content'] for chunk in all_chunks]
    
    logging.info(f"Genererar embeddings för {len(documents_to_embed)} text-chunks...")
    embeddings = model.encode(documents_to_embed, show_progress_bar=True)

    for i, chunk in enumerate(all_chunks):
        chunk['vector'] = embeddings[i].tolist()

    final_index = {
        "model": EMBEDDING_MODEL,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "chunks": all_chunks
    }

    logging.info(f"Skriver index till {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_index, f)

    logging.info("="*50)
    logging.info("Einstein Vector Index-bygge slutfört!")
    logging.info(f"Totalt antal chunks i indexet: {len(all_chunks)}")
    logging.info("="*50)

if __name__ == "__main__":
    main()
# END FILE: scripts/rag/build_vector_index.py
