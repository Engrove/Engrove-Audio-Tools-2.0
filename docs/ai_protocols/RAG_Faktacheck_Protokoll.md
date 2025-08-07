# RAG_Faktacheck_Protokoll v1.0

**Syfte**  
Tvingar fram retrieval‑augmented generation för faktapåståenden.

**Process**  
* 1. Extrahera alla faktapåståenden i utkastet.
*  1a. **Citation‑Cache:** slå upp DOI/URL i `tools/citation_cache.json`; hoppa nät‑lookup om giltig post < 30 d.  
*  1b. **Domän‑RAG‑Index:** vid medicin, juridik eller finans, använd motsvarande fack‑index först.  
* 3. Kör webb‑ eller docs‑sök; behåll topp 3 källor.  
* 4. Jämför påståenden ↔ källor. Avvikelse → flagga.  
* 5. **HAT‑Pipeline:** om ≥15 % av fakta flaggas i steg 3, kör *Hallucination‑Aware Tuning* (RAG‑HAT) och logga i `rag_hat.log`.  
* 6. Bifoga käll‑citat i slut‑svaret.

**Aktivering**  
Implicit när PSV steg 4 triggas.
