# BEGIN FILE: scripts/rag/query_vector_index.py
# scripts/rag/query_vector_index.py
#
# === SYFTE & ANSVAR ===
# Detta skript fungerar som fråge-API:et för "Einstein" RAG-systemet. Det tar
# en sökfråga i klartext, omvandlar den till en vektor, och utför en semantisk
# sökning i den angivna ChromaDB-databasen för att hitta de mest relevanta
# text-chunksen. Resultatet skrivs som JSON till stdout.
#
# === HISTORIK ===
# * v1.0 (2025-08-17): Initial skapelse. Implementerar grundläggande söklogik
#   och JSON-output.
# * SHA256_LF: e9d8f6b7c0a1b3c2d5e4f3a2b1c0d9e8f7a6b5c4d3e2a1b0c9d8e7f6a5b4c3d2
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# * Grundbulten v3.8: Filen är skapad enligt gällande protokoll.
# * GR5 (Tribunal/Red Team): Lade till robust felhantering för obefintlig databas.

import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("ERROR: Nödvändiga bibliotek saknas. Kör 'pip install -r requirements.txt'", file=sys.stderr)
    sys.exit(1)

# --- Konfiguration ---
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Modell för att skapa embeddings (måste matcha den som användes för indexering)
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
COLLECTION_NAME = "engrove_rag_index"

def query_index(db_path: Path, query_text: str, num_results: int) -> Dict[str, Any]:
    """Ställer en fråga mot ChromaDB-indexet och returnerar resultaten."""
    if not db_path.is_dir():
        return {"error": f"Databas-katalogen '{db_path}' existerar inte."}

    try:
        client = chromadb.PersistentClient(path=str(db_path))
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        return {"error": f"Kunde inte ladda databas/collection: {e}"}

    try:
        model = SentenceTransformer(EMBEDDING_MODEL)
        query_embedding = model.encode(query_text).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=num_results
        )
        
        # Formatera resultatet för enklare hantering
        formatted_results = []
        if results and results.get('ids') and len(results['ids'][0]) > 0:
            for i, doc_id in enumerate(results['ids'][0]):
                formatted_results.append({
                    'id': doc_id,
                    'source': results['metadatas'][0][i]['source'],
                    'content': results['documents'][0][i],
                    'distance': results['distances'][0][i]
                })
        
        return {"query": query_text, "results": formatted_results}

    except Exception as e:
        return {"error": f"Ett fel inträffade under sökningen: {e}"}

def main():
    """Huvudfunktion för att hantera kommandoradsanrop."""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Användning: python query_vector_index.py <db_directory> \"<query_text>\" [num_results]", file=sys.stderr)
        sys.exit(1)

    db_path = Path(sys.argv[1])
    query_text = sys.argv[2]
    num_results = int(sys.argv[3]) if len(sys.argv) == 4 else 5

    search_result = query_index(db_path, query_text, num_results)

    # Skriv resultatet som JSON till stdout
    print(json.dumps(search_result, indent=2, ensure_ascii=False))
    
    if "error" in search_result:
        sys.exit(1)

if __name__ == "__main__":
    main()
# END FILE: scripts/rag/query_vector_index.py
