<!-- BEGIN FILE: docs/ai_protocols/Grundbulten_Protokoll.md -->
SYFTE & ANSVAR:
"Grundbulten" (P-GB-4.1) är den vägledande processen för all filgenerering och modifiering. Den beskriver det övergripande arbetsflödet och de kvalitetskrav som gäller. De strikta, maskinläsbara reglerna och grindarna har normaliserats och finns nu definierade i `docs/ai_protocols/DynamicProtocols.json` under `protocolId: "DP-RULESET-PGB-01"`.

HISTORIK:
* v1.0 - v3.9: Se arkiverad version för detaljerad historik.
* v4.0 (2025-08-21): KRITISK NORMALISERING. Protokollet har refaktorerats. Alla tvingande, atomära regler (G-Grindar, Invarianter) har extraherats till `DynamicProtocols.json`. Denna fil fokuserar nu på process, syfte och arbetsflöde.
* v4.1 (2025-08-26): PRINCIP-SYNTES. Uppdaterat den obligatoriska `SHA256_LF`-platshållaren till en agerbar instruktion enligt heuristik H-20250826-01.
* SHA256_LF: [VERIFIERAS I CI/CD. Se context_bundle.json -> hash_index för slutgiltigt värde.]

TILLÄMPADE REGLER (Frankensteen v5.7+):
* Detta protokoll är nu en processguide. De tvingande reglerna hämtas och verifieras programmatiskt från `DP-RULESET-PGB-01`.
* Alla relevanta meta-protokoll (KIV, KMM, Uppgifts-Kontrakt, etc.) tillämpas.
END HEADER -->

# Protokoll: **Grundbulten** (P-GB-4.1) – Process för Universell Filhantering

```json
{
  "$schema": "docs/ai_protocols/schemas/DynamicProtocols.schema.json",
  "strict_mode": true,
  "mode": "literal",
  "protocol": {
    "id": "P-GB-4.1",
    "title": "Grundbulten – Process för Universell Filhantering",
    "strict_mode": true,
    "mode": "literal",
    "source_reference": "docs/ai_protocols/DynamicProtocols.json",
    "ruleset_id": "DP-RULESET-PGB-01",
    "philosophy": {
      "purpose": "Säkerställa spårbarhet, verifierbarhet och korrekthet vid alla filoperationer.",
      "guarantees": [
        "Inga felaktiga antaganden.",
        "Resultatet är robust, verifierat och hög kvalitet."
      ],
      "verification": "Pre-Svarsverifiering (PSV) mot DynamicProtocols.json"
    },
    "workflow": {
      "steps": [
        {
          "id": 1,
          "title": "Kontraktsfas",
          "reference": "Uppgifts-Kontrakt_Protokoll.md",
          "description": "Definiera mål och omfattning för uppgiften."
        },
        {
          "id": 2,
          "title": "Kontextverifiering",
          "includes": ["KIV", "G-Grindar"],
          "description": "Verifiera fullständig information och fil-hasher (G-1)."
        },
        {
          "id": 3,
          "title": "Planering och Intern Granskning",
          "reference": "Tribunal",
          "description": "Formulera plan och utför intern Red Team-granskning."
        },
        {
          "id": 4,
          "title": "Implementation",
          "description": "Generera ny fil eller ändring under strikt efterlevnad av invarianter (G5)."
        },
        {
          "id": 5,
          "title": "Kvalitetssäkring och Leverans",
          "outputs": [
            "VERIFICATION_LOG med diff och statiska kontroller.",
            "Uppdaterad HISTORIK med SHA256_LF-post.",
            "COMPLIANCE STATEMENT mot DP-RULESET-PGB-01.",
            "Leveransformat enligt Bilaga E."
          ]
        }
      ]
    },
    "principles": {
      "no_assumptions": "Avbryt vid mismatch eller ofullständig kontext.",
      "traceability": "Alla versioner dokumenteras med SHA256_LF-hashar.",
      "structural_stability": "Ändra aldrig publik API-yta utan REFRAKTOR-FLAG + DT-2-godkännande."
    },
    "delivery_matrix": {
      "reference": "Bilaga E",
      "decision_table": [
        {
          "task_type": "Ny fil",
          "delivery_format": "Fullständig Fil",
          "justification": "Enda sättet att garantera fullständighet."
        },
        {
          "task_type": "Liten, manuell ändring",
          "delivery_format": "Manuell Patch-Instruktion",
          "reference": "P-MP-1.0",
          "justification": "Otvetydighet och verifierbarhet för mänsklig operatör."
        },
        {
          "task_type": "Medelstor till stor ändring",
          "threshold": ">5 rader",
          "delivery_format": "Fullständig Fil",
          "justification": "Minimerar manuella fel."
        },
        {
          "task_type": "Programmatisk/Automatiserad Patchning",
          "delivery_format": "Strukturerad JSON-patch",
          "reference": "Diff_Protocol_v3.md",
          "justification": "Används vid verktygsstyrd patchning."
        }
      ]
    },
    "compliance": {
      "status": "Obligatorisk",
      "hash_placeholder": "SHA256_LF",
      "validation_source": "context_bundle.json -> hash_index"
    }
  }
}
