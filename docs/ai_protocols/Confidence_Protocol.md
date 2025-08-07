# Confidence_Protocol v1.0

*Beräknar och tillämpar konfidensscore.*

1. Beräkna med inbyggd logit‑bias eller modell‑API‑score.  
2. Logaritmisk skala 0‑1.  
3. < 0.25 → returnera `"osäkert"` + kort orsak.  
4. 0.25–0.5 → erbjud följdfråga.  
5. ≥ 0.5 → normalt svar.
