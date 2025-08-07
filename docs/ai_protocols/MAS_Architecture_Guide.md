# MAS Architecture Guide v1.0
*Orchestrator–Worker‑mönster för Engrove Audio*

| Node | Kort beskrivning | I/O‑format |
|------|-----------------|------------|
| **Engrove Architect** | Dekomponerar uppgift till steg; skriver `plan.json`. | In: chatt‑uppdrag · Out: plan.json |
| **FRANKENSTEEN_DSP_Coder** | Implementerar DSP‑algoritmer. | In: kod‑spec · Out: *.cpp, *.hpp |
| **FRANKENSTEEN_UI_Dev** | Skapar Vue‑komponenter. | In: ui‑spec · Out: *.vue |
| **FRANKENSTEEN_Test_Engineer** | Skriver och kör tester. | In: src‑lista · Out: *.spec.js |
| **Reviewer_Agent** | Kör LLM‑Judge + diff‑analys. | In: patch‑set · Out: review‑report.md |

Arbetsflöden modelleras som:
*  plan --> code --> test --> review --> commit
*  review --|fail|--> code
*  test   --|fail|--> code

Branchlogik styrs av JSON‑fältet `status`.
