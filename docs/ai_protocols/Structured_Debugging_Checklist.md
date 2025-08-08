# Structured Debugging Checklist (SDC)

**Steg 0 – Repro**
- Minimal repro (steg/URL/fil). Loggar insamlade.

**Steg 1 – Hypoteslista**
- Lista 3–7 möjliga orsaker (kod, kontrakt, konfig, data, cache, nät).

**Steg 2 – Verifiering per hypotes**
- Mätbar test: vad falsifierar/bekräftar?
- Källa: källkod, bygglogg, nätverkstrace.

**Steg 3 – Fix**
- Minsta ändring som eliminerar grundorsak.
- Diff-risk: påverkar inte andra flöden.

**Steg 4 – Verifiering efter fix**
- Repro testcase passerar.
- QG-A..E passerar (AI_Core_Instruction.md).
- Micro-Retro notis skapad.

**Anti-mönster att undvika**
- ”HTML i stället för JSON” utan att bevisa orsak.
- Konfig-gissning utan loggbevis.
- Tysta singular/plural-förvanskningar.
