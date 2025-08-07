```markdown
# HITL Interrupt Points v1.0

| Fas            | Trigger                | Vad AI måste göra                                  |
|----------------|------------------------|----------------------------------------------------|
| **Plan Review**| `plan.json` genererad  | Pausa, presentera plan, invänta **OK**.            |
| **Pre‑Commit** | `git_commit` föreslås  | Visa `git diff`, invänta godkännande.              |
| **Destruktivt**| `rm`, overwrite‑kommando| Lista kommando + parametrar, kräva **CONFIRM**.    |
