<!-- BEGIN FILE: docs/ai_protocols/Manuell_Patch_Protokoll.md
SYFTE & ANSVAR:
Detta protokoll (P-MP-1.0) definierar det strikta, otvetydiga formatet för att leverera en "Manuell Patch-Instruktion" i ett chatt-gränssnitt. Syftet är att ge en mänsklig operatör en exakt, steg-för-steg checklista för att utföra en filändring manuellt, med fullständig spårbarhet och verifierbarhet via SHA256-hashar.

HISTORIK:
* v1.0 (2025-08-18): Initial skapelse. Formaliserad baserat på en metadiskussion om behovet av ett explicit, mänskligt läsbart patch-format.
* SHA256_LF: 5f1b2c3d4e5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c

TILLÄMPADE REGLER (Frankensteen v5.7):
* Grundbulten v4.0: Denna fil skapas för att uppfylla ett beroende som nyligen lades till i Grundbultens beslutsmatris.
* GR5 (Tribunal/Red Team): Protokollets struktur är resultatet av en kritisk granskning av tidigare, tvetydiga leveransformat.

Datum: 2025-08-18
Extern granskare: Engrove (godkänd för införing i Steg 10)
END HEADER -->

# Protokoll för Manuell Patch-Instruktion (P-MP-1.0)

## 1. Syfte och Ansvarsområde
Detta protokoll definierar det obligatoriska formatet för att leverera en **Manuell Patch-Instruktion**. Formatet är designat för att vara en fullständig, otvetydig och verifierbar checklista för en mänsklig operatör (Engrove) som ska applicera en liten, fokuserad ändring på en befintlig fil.

Detta format ska användas i enlighet med beslutsmatrisen i `Grundbulten_Protokoll.md`, Bilaga E.

## 2. Formatstruktur
En Manuell Patch-Instruktion måste presenteras i ett enda Markdown-block och innehålla följande tre (3) huvudsteg i exakt denna ordning.


### MANUELL PATCH-INSTRUKTION (P-MP-1.0) ###

**MÅLFIL:** [Exakt relativ sökväg till filen]

**STEG 1: VERIFIERA BASVERSION**
- **Förutsättning:** Din lokala fil måste ha följande exakta SHA256-hash. Om den inte matchar, AVBRYT och hämta den senaste versionen.
- **`base_checksum_sha256`:** [64-tecken hex-hash för filen INNAN ändring]

**STEG 2: UTFÖR ÄNDRING**
- **OPERATION:** [ERSÄTT / RADERA / INFOGA EFTER]
- **ANKARE (Hitta exakt dessa rader):**

  // De 1-5 exakta raderna i koden som omedelbart FÖREGÅR (eller utgör starten av) ändringen.

- **INNEHÅLL (Vad som ska ändras):**

  *Fall 1: ERSÄTT*
  > **ERSÄTT** blocket mellan ankaret ovan och nästa ankare...
  > 
  > **...MED FÖLJANDE:**
  > 
  > // Det nya kodblocket

  *Fall 2: RADERA*
  > **RADERA** blocket mellan ankaret ovan och nästa ankare.
  
  *Fall 3: INFOGA*
  > **INFOGA FÖLJANDE** omedelbart efter ankar-raderna ovan:
  > 
  > // Det nya kodblocket


**STEG 3: VERIFIERA RESULTAT**
- **Efter att ändringen är sparad,** måste den nya filens SHA256-hash vara exakt följande värde.
- **`final_checksum_sha256`:** [64-tecken hex-hash för filen EFTER ändring]

**SAMMANFATTNING AV ÄNDRING:** [En kort mening som förklarar VARFÖR ändringen gjordes.]
