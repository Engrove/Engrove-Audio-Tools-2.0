# Multi_Sample_Protokoll v1.0

1. Generera n = 3 parallella svar.  
2. Beräkna Shannon‑entropi över tokens.  
3. Om entropi‑spridning > τ (standard 0.15) → flagga inkonsistens och starta RAG_Faktacheck.  
4. Returnera majoritets‑ eller median‑variant.
