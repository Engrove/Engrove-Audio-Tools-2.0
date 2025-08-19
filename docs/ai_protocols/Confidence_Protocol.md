# Confidence_Protocol v1.0

*Beräknar och tillämpar konfidensscore.*

1. Beräkna med inbyggd logit‑bias eller modell‑API‑score.  
2. Logaritmisk skala 0‑1.  
3. < 0.25 → returnera `"osäkert"` + kort orsak.
4. Om CoT‑Self‑Check flaggar självmotsägelse, sänk confidence med 0.15 före beslut.
5. 0.25–0.5 → erbjud följdfråga.  
6. ≥ 0.5 → normalt svar.
7. Vid confidence < 0.85 → degradera till Escalation L3 (Konsult).
8. Flagga från RAG_Faktacheck eller Multi_Sample (SE/Shannon > 0.15) → sänk confidence med 0.10 innan beslut.
