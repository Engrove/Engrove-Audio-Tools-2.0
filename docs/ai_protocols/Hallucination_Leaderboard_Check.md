# Hallucination_Leaderboard_Check v1.0
**Trigger:** före Confidence-beslut. 
**Utdata:** { "label":"ok|risk", "reason":"…" }. Vid "risk": sänk confidence −0.05 och kör Multi_Sample.
1. Kör veckovis HTTP‑GET mot Vectara‑/OpenAI‑hallucination‑leaderboard API.  
2. Om vår modell sjunker > 2 placeringar → flagga i ByggLogg och planera retraining. <!-- Leaderboard﻿:contentReference[oaicite:7]{index=7} -->
3. Cacha DOI/URL för varje faktakälla i `hallucination_cache.json` för RAG‑lagrets återanvändning.
