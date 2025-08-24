# /docs/ai_protocols/P-RECONSTRUCT-v1.0.md
# Protokoll för Historisk Rekonstruktion (P-RECONSTRUCT) v1.0
#
# === HISTORIK ===
# * v1.0 (2025-08-24): Initial skapelse.
#
# === SYFTE & ANSVAR ===
# Detta protokoll definierar den strikta processen för att rekonstruera och
# normalisera artefakter från en tidigare session utifrån ostrukturerad data (t.ex. textloggar).
# Protokollets enda output är en enda, validerad JSON-fil per session.
#
# === AKTIVERING ===
# Protokollet aktiveras när en uppgift kräver rekonstruktion av historisk data.
#
# === OUTPUT-KONTRAKT ===
# - En (1) JSON-fil per session, döpt till `[SESSIONID].json`.
# - Filen måste innehålla ett rotobjekt med nycklarna `sessionId`, `createdAt`, och `artifacts`.
# - `artifacts`-objektet måste innehålla `ByggLogg`, `Chatthistorik`, och `ai_protocol_performance`.
#   `frankensteen_learning_db` är valfri och inkluderas endast om en ny heuristik har skapats.

---

### OBLIGATORISKA REGLER FÖR DATAKVALITET

Dessa regler måste tillämpas på all data som genereras av detta protokoll.

#### **A) Metadata: Noll Gissning, Noll Självrapportering**
1.  **"Unknown" Fallback:** Om `provider`, `name`, eller `version` för en modell inte kan styrkas från en explicit källa i källmaterialet, **MÅSTE** värdet sättas till strängen `"unknown"`. Inga fält får lämnas tomma eller som `null`.
2.  **Förbud mot Självrapportering:** AI:ns egen runtime-identitet får **INTE** användas som ett fallback-värde för historisk data, såvida inte källmaterialet explicit refererar till den specifika modellen. Om en matchning sker utan källa, ska `provider`, `name` och `version` sättas till `"unknown"`.
3.  **Speaker-format:** `speaker`-strängen **MÅSTE** alltid följa formatet `"<speakerName> (<provider>:<name>@<version>)"`. Denna sträng måste exakt återspegla de maskinläsbara fälten `speakerName` och `model`.

#### **B) Chatthistorik: Fullständig och Korrekt**
1.  **Alla Turer:** Artefakten `Chatthistorik.interactions` **MÅSTE** innehålla varje enskild tur från sessionen i kronologisk ordning. Detta inkluderar system- och verktygsmeddelanden.
2.  **Ingen Hopslagning:** Varje interaktion i arrayen måste motsvara en (1) faktisk tur i konversationen.

#### **C) Session ID: Garanterad Närvaro**
1.  Om ett `sessionId` inte kan härledas från källmaterialet, **MÅSTE** det sättas till `"999"`. Den slutgiltiga filen ska då heta `999.json`.

---

### VALIDERINGSPORT (OBLIGATORISK FÖRE LEVERANS)

Den genererade JSON-filen **MÅSTE** passera följande kontroller innan den anses slutförd:

1.  **JSON-syntax:** Filen måste vara en 100% giltig JSON-fil (UTF-8, LF).
2.  **Speaker Regex:** Varje `speaker`-sträng måste validera mot följande regex: `^[^()]+ \([^:]+:[^@]+@[^)]+\)$`.
3.  **Interaktionsantal:** Antalet objekt i `interactions`-arrayen måste matcha det totala antalet turer i källsessionen. Om detta inte kan garanteras, måste en `coverage: "partial"`-flagga läggas till i `Chatthistorik`-objektet med en förklarande `coverageReason`.
4.  **ISO 8601-datum:** Alla tidsstämplar (`createdAt`, `date`, etc.) måste vara i `YYYY-MM-DDTHH:mm:ssZ`-format.

---

### Referensimplementation (Normativ)
```python
# Denna funktion representerar den obligatoriska normaliseringslogiken.
def normalize_speaker(entry, runtime_identity=None, source_has_explicit_model=False):
    name = (entry.get("speakerName") or "unknown").strip() or "unknown"
    m = entry.get("model") or {}
    provider = (m.get("provider") or "unknown").strip() or "unknown"
    model = (m.get("name") or "unknown").strip() or "unknown"
    version = (m.get("version") or "unknown").strip() or "unknown"
    # Implementerar "No-Self-Report"-regeln
    if runtime_identity and not source_has_explicit_model:
        if (provider.lower(), model.lower(), version.lower()) == (
            runtime_identity["provider"].lower(),
            runtime_identity["name"].lower(),
            runtime_identity["version"].lower()
        ):
            provider = model = version = "unknown"
    entry["speakerName"] = name
    entry["model"] = {"provider": provider, "name": model, "version": version}
    entry["speaker"] = f"{name} ({provider}:{model}@{version})"
    return entry
