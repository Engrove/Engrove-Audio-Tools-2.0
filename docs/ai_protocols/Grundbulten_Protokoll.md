<!-- BEGIN FILE: docs/ai_protocols/Grundbulten_Protokoll.md
SYFTE & ANSVAR:
Detta är "Grundbulten" (P-GB-2.1), ett universellt och tvingande protokoll för all generering och modifiering av filer (kod, dokumentation, konfiguration, etc.). Det säkerställer att varje leverans är komplett, konsekvent dokumenterad, verifierad, testad och spårbar.

HISTORIK:
* v1.0 (2025-08-16): Initialt förslag, fokuserat enbart på kod.
* v2.0 (2025-08-16): Omarbetad till ett universellt protokoll, men med otillräcklig teknisk detaljnivå.
* v2.1 (2025-08-16): (Help me God - StigBritt Tribunal) Slutgiltig syntes. Kombinerar den universella strukturen från v2.0 med den tekniska rigorösiteten från ”idiotsäkert”-direktivet.
 
 TILLÄMPADE REGLER (Frankensteen v5.4):
* GR4 – Strikt interaktionskontrakt: Självgranskning + extern domslut-loop; definierad outputordning och ansvar (§9).
* GR5 – Tribunal/Red Team-grind: KajBjörn-validering av SPEC och StigBritt-granskning av åtgärdsplan är obligatoriska (§3).
* GR6 – Processrefaktorering: Ad-hoc ersatt av reproducerbar pipeline med tydliga grindar och verktygssteg (§0, §5–§11).
* GR7 – Historik & spårbarhet: Full historik i header och BEGIN/END med filsökväg; inga platshållare (§1a–§1b).

Övriga tillämpade policies:
* Help me God – Eskalering efter två misslyckade försök (§11).
* Red Team Alter Ego – StigBritt formaliserad som oberoende granskare (§3).

Datum: 2025-08-16
Extern granskare: Engrove (godkänd för införing i Steg 10)

END HEADER -->

# Protokoll: **Grundbulten** (P-GB-2.1) – Universell filhantering

## Steg 0: Mål och omfattning
- **Omfattning:** Gäller **alla** filer som skapas eller modifieras.
- **Mål:** Producera en fil som är 100% komplett, korrekt, spårbar och i enlighet med gällande projektstandarder.

## Steg 1: Dokumentation & metadata (obligatoriskt första steg)
- **1a. Fil-header:** Konstruera fullständig header (se toppkommentar). Måste innehålla:
  - `SYFTE & ANSVAR`
  - `HISTORIK` (full, utan platshållare)
  - `TILLÄMPADE REGLER` (**lämnas tom**; fylls i steg 10 av extern granskare)
- **1b. Fil-sökvägar & kommentarspolicy:** Inkludera start- **och** slutkommentarer med exakt filsökväg.
  - Använd endast **giltig** kommentar-syntax för filtypen (t.ex. Markdown: `<!-- -->`; JSON: **inga kommentarer**).

## Steg 2: Specifikation & hypotes
- Presentera **SPEC/ANTAGANDEN**: kontrakt, IO, invarianter, felhantering, typer, tråd/async, prestanda, miljö/beroenden.
- Märk antaganden *[Härledd]* vs *[Explicit]*. Testerna i steg 6 måste binda dessa.

## Steg 3: Tribunalgranskning (obligatorisk grind)
- **KajBjörn-validering:** Säkerställ att *SPEC/ANTAGANDEN* bygger uteslutande på given info.
- **StigBritt-granskning:** Granska *ÅTGÄRDSPLAN* för logiska brister **innan** implementation.

## Steg 4: Fel- och riskkategorier (checklista)
- **Grundläggande:** syntax, namn, typer, null/None, index/avgränsning, edge-fall.
- **Avancerat:** tillstånd, race, init-ordning, resurser/läckor, I/O (encoding, tidszon), kontraktsbrott.
- **Säkerhet & prestanda:** injektion, path traversal, osäker deserialisering, Big-O-regressioner.
- **Beroenden:** versioner, brytande ändringar, cirkulära imports.

## Steg 5: Åtgärdsplan
- Prioritering: **korrigera → säkra → stabilisera → dokumentera → städa**.
- Motivera minsta nödvändiga ändringar; omdesign endast vid behov och motiverad.

## Steg 6: Testdesign
- **Kod:** Enhets- och egenskapstester som täcker SPEC/ANTAGANDEN, felvägar och gränsvärden. Använd determinism (`seed=42`).
- **Icke-kod:** Verifiera formatering/syntax/innehåll mot styrande standard (t.ex. JSON Schema, stil/CI-linters).

## Steg 7: Körning & bevis
- **Kod:** redovisa **FAKTISK KÖRLOGG** eller tydligt märkt **SIMULERAD KÖRLOGG** (kommandon + resultat).
- **Icke-kod:** redovisa valideringskommandon och utfall (linters, schema-validering).

## Steg 8: Filleverans
- Leverera den fullständiga, färdiga filen i en **KOD/INNEHÅLL**-sektion.
- **Obs:** `TILLÄMPADE REGLER` i headern lämnas tom här (fylls i steg 10).

## Steg 9: Självgranskning & extern dom
- **9a. Självgranskning (Frankensteen):** Leverera `self_review_artifact.json` som listar följda regler med kort bevisning.
- **9b. Extern granskning (Engrove):** Extern part ger **(A) korrigering** *eller* **(B) godkännande** genom att tillhandahålla slutlig `TILLÄMPADE REGLER`.

## Steg 10: Arkivering
- Författaren inför den externa `TILLÄMPADE REGLER`-texten i headern och arkiverar/committar.

## Steg 11: Eskalering
- Efter två misslyckade försök att passera kvalitetsgrindar: aktivera `Help_me_God_Protokoll.md`.

<!-- END FILE: docs/ai_protocols/Grundbulten_Protokoll.md -->
