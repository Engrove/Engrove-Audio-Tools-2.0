# Multi_Sample_Protokoll v1.0

1. Generera n = 3 parallella svar.  
2. **Semantic Entropy Probe (SEP):** beräkna semantisk entropi `SE` enligt Kossen et al. 2024. Om `SE > τ_SE (0.15)` markeras svar som hallucinationsrisk.
3. Sätt random.seed=42 per försök; logga SE, Shannon, seed i metrics.
4. Beräkna Shannon‑entropi över tokens.
5. Om entropi‑spridning > τ (0.15) **eller** SE‑värde > 0.15 → flagga inkonsistens och starta RAG_Faktacheck.
6. Om `entropy↑` (ökning > 10 % mellan attempt_id) under Help_me_God → paus, begär mer data innan nästa försök.
7. Om *antingen* SE eller Shannon‑spridning > τ → aktivera `RAG_Faktacheck`.
8. Logga `entropy` och `semantic_entropy` i interna metrics‑loggen.
9. **Entropy‑Watchdog:** om SE ökar mellan iteration `attempt_id n` och `n+1`, avbryt auto‑retry och begär ny data.  
10. Returnera majoritets‑ eller median‑variant.
11. Vid flagg (SE eller Shannon > 0.15): initiera RAG_Faktacheck och sänk confidence −0.10; överväg Escalation L3.


