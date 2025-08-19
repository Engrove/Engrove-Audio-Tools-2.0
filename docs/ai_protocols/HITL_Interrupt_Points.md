# HITL Interrupt Points v1.0

| Fas            | Trigger                | Vad AI måste göra                                  |
|----------------|------------------------|----------------------------------------------------|
| **Plan Review**| `plan.json` genererad  | Pausa, presentera plan, invänta **OK**.            |
| **Pre‑Commit** | `git_commit` föreslås  | Visa `git diff`, invänta godkännande.              |
| **Destruktivt**| `rm`, overwrite‑kommando| Lista kommando + parametrar, kräva **CONFIRM**.   |

**Escalation-mappning:** 
- Plan Review ↔ L4 (Samarbetspartner).
- Pre-Commit ↔ L3 vid confidence < 0.85.
- Destruktivt ↔ alltid HITL bekräftelse oavsett nivå.
