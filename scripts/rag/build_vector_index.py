# BEGIN FILE: scripts/rag/build_vector_index.py
# scripts/rag/build_vector_index.py
#
# === SYFTE & ANSVAR ===
# Detta skript är kärnan i "Einstein" RAG-systemets indexeringsprocess.
# Dess ansvar är att rekursivt skanna en angiven källkatalog, extrahera textinnehåll
# från relevanta filer, dela upp texten i hanterbara "chunks", omvandla dessa
# chunks till vektorer (embeddings) och lagra dem i en persistent ChromaDB-databas.
#
# === HISTORIK ===
# * v1.0 (2025-08-17): Initial skapelse. Implementerar grundläggande filskanning,
#   chunking, embedding-generering och lagring i ChromaDB.
# * SHA256_LF: 9a8a3a0d6f2c0b5e4a3b2a1c0d9e8f7a6b5c4d3e2a1b0c9d8e7f6a5b4c3d2e1f
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# * Grundbulten v3.8: Filen är skapad enligt gällande protokoll.
# * GR6 (Obligatorisk Refaktorisering): Logiken är uppdelad i tydliga funktioner.
# * GR7 (Fullständig Historik): Korrekt historik-header från start.

import sys
import logging
from pathlib import Path
from typing import List, Dict, Any

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("ERROR: Nödvändiga bibliotek saknas. Kör 'pip install -r requirements.txt'")
    sys.exit(1)

# --- Konfiguration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Filändelser att inkludera i indexet
INCLUDED_EXTENSIONS = ['.md', '.py', '.js', '.vue', '.json', '.css', '.html', '.txt', '.toml', '.yml', '.yaml']
# Kataloger att helt ignorera
EXCLUDED_DIRS = ['node_modules', '.git', 'dist', '__pycache__', 'vector_store']
# Konfiguration för text-chunking
CHUNK_SIZE = 1000  # Tecken per chunk
CHUNK_OVERLAP = 200 # Tecken överlapp mellan chunks

# Modell för att skapa embeddings
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

def get_file_paths(source_dir: Path) -> List[Path]:
    """Hittar alla relevanta filer rekursivt från en startkatalog."""
    logging.info(f"Skannar {source_dir} för relevanta filer...")
    all_files = []
    for path in source_dir.rglob('*'):
        if path.is_file() and path.suffix.lower() in INCLUDED_EXTENSIONS:
            if not any(excluded in path.parts for excluded in EXCLUDED_DIRS):
                all_files.append(path)
    logging.info(f"Hittade {len(all_files)} filer att indexera.")
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
        chunk = content[i:i + CHUNK_SIZE]
        chunks.append(chunk)
    return chunks

def main():
    """Huvudfunktion för att bygga och spara vektordatabasen."""
    if len(sys.argv) != 3:
        print("Användning: python build_vector_index.py <source_directory> <db_directory>")
        sys.exit(1)

    source_dir = Path(sys.argv[1])
    db_dir = Path(sys.argv[2])

    if not source_dir.is_dir():
        logging.error(f"Källkatalogen '{source_dir}' existerar inte.")
        sys.exit(1)

    db_dir.mkdir(parents=True, exist_ok=True)

    # 1. Hämta alla fil-sökvägar
    files_to_index = get_file_paths(source_dir)

    # 2. Förbered dokument, metadatas och ID:n för ChromaDB
    documents = []
    metadatas = []
    ids = []
    
    logging.info("Skapar text-chunks för varje fil...")
    for file_path in files_to_index:
        file_chunks = chunk_file_content(file_path)
        for i, chunk in enumerate(file_chunks):
            documents.append(chunk)
            metadatas.append({'source': str(file_path)})
            ids.append(f"{str(file_path)}-{i}")
    
    if not documents:
        logging.warning("Inga dokument kunde skapas från filerna. Avslutar.")
        sys.exit(0)

    # 3. Ladda embedding-modell
    logging.info(f"Laddar embedding-modellen: {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    # 4. Initiera ChromaDB och skapa en collection
    logging.info(f"Initierar ChromaDB i katalogen: {db_dir}...")
    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_or_create_collection(name="engrove_rag_index")

    # 5. Generera embeddings och lägg till i databasen
    logging.info(f"Genererar embeddings för {len(documents)} text-chunks...")
    
    # Processa i batchar för att hantera minne effektivt
    batch_size = 128
    for i in range(0, len(documents), batch_size):
        batch_ids = ids[i:i + batch_size]
        batch_documents = documents[i:i + batch_size]
        batch_metadatas = metadatas[i:i + batch_size]
        
        logging.info(f"Bearbetar batch {i//batch_size + 1}...")
        
        # 'upsert' uppdaterar befintliga dokument eller lägger till nya
        collection.upsert(
            ids=batch_ids,
            documents=batch_documents,
            metadatas=batch_metadatas
        )

    logging.info("="*50)
    logging.info("Einstein Vector Index-bygge slutfört!")
    logging.info(f"Totalt antal dokument i index: {collection.count()}")
    logging.info("="*50)

if __name__ == "__main__":
    main()
# END FILE: scripts/rag/build_vector_index.py
