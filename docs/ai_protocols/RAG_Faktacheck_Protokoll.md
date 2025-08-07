# RAG_Faktacheck_Protokoll v1.0

**Syfte**  
Tvingar fram retrieval‑augmented generation för faktapåståenden.

**Process**  
1. Extrahera alla faktapåståenden i utkastet.  
2. Kör webb‑ eller docs‑sök; behåll topp 3 källor.  
3. Jämför påståenden ↔ källor. Avvikelse → flagga.  
4. Bifoga käll‑citat i slut‑svaret.

**Aktivering**  
Implicit när PSV steg 4 triggas.
