<!-- BEGIN FILE: docs/ai_protocols/Grundbulten_Protokoll.md
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

## 1. Filosofi och Syfte

Grundbulten är den process som garanterar att varje filoperation (skapande eller ändring) är **spårbar, verifierad och korrekt**. Den säkerställer att jag aldrig agerar på felaktiga antaganden och att resultatet av mitt arbete är robust och av hög kvalitet.

De exakta, icke-förhandlingsbara "Hårda Grindarna" och "Strukturella Invarianterna" som styr denna process är definierade som maskinläsbara regler i:
`docs/ai_protocols/DynamicProtocols.json` (under **`protocolId: "DP-RULESET-PGB-01"`**).

Min `Pre-Svarsverifiering` (PSV) konsulterar alltid den JSON-filen för att säkerställa efterlevnad.

## 2. Arbetsflöde

När en uppgift kräver filhantering följer jag denna sekvens, som styrs av de nya meta-protokollen:

1.  **Kontraktsfas:** Enligt `Uppgifts-Kontrakt_Protokoll.md` definierar vi och kommer överens om uppgiftens mål och omfattning.
2.  **Kontextverifiering (KIV & G-Grindar):** Jag säkerställer att jag har fullständig och korrekt information om alla filer som ska ändras. Detta inkluderar att verifiera fil-hasher (`G-1`) och att innehållet är komplett (`G-1`).
3.  **Planering och Intern Granskning (Tribunal):** Jag formulerar en åtgärdsplan och utsätter den för en intern "Red Team"-granskning för att identifiera risker och svagheter.
4.  **Implementation:** Jag genererar den nya filen eller ändringarna. Under denna fas är jag bunden av de strukturella invarianterna (`G5`) för att förhindra oavsiktliga, brytande ändringar.
5.  **Kvalitetssäkring och Leverans:**
    *   Jag skapar ett `VERIFICATION_LOG` som innehåller en kvantitativ diff-analys och bevis på att alla statiska kontroller har passerat.
    *   Jag uppdaterar filens `HISTORIK` med en ny `SHA256_LF`-post för den nya versionen. Denna post är antingen den faktiska hashen eller den standardiserade platshållaren om värdet ännu inte kan beräknas.
    *   Jag presenterar resultatet tillsammans med en `COMPLIANCE STATEMENT` som bekräftar att alla regler i `DP-RULESET-PGB-01` har följts.
    *   Leveransformatet (full fil vs. patch) bestäms av `Bilaga E: Beslutsmatris`.

## 3. Viktiga Principer

*   **Inga Antaganden:** Om en fil-hash inte matchar eller om kontexten är ofullständig, avbryter jag alltid och begär korrekt information.
*   **Spårbarhet:** All historik bevaras och varje ändring resulterar i en ny, verifierbar fil-hash som dokumenteras både i filens header och i mitt svar.
*   **Strukturell Stabilitet:** Jag kommer aldrig att medvetet ändra den publika ytan (funktionssignaturer, API:er) av en fil utan ett explicit `REFRAKTOR-FLAG` och ett godkänt DT-2 beslut.

---

## Bilaga E: Beslutsmatris för Leveransformat i Chatt
Detta avsnitt styr valet av format när en filändring presenteras i ett svar. Valet baseras på uppgiftens art och mottagarens behov (människa vs. maskin).

| Uppgiftstyp | Rekommenderat Leveransformat | Motivering |
| :--- | :--- | :--- |
| **Ny fil** | `Fullständig Fil` | Icke förhandlingsbart. Enda sättet att garantera fullständighet. |
| **Liten, manuell ändring i en befintlig fil** | `Manuell Patch-Instruktion` (enligt P-MP-1.0) | Prioriterar otvetydighet och verifierbarhet för en mänsklig operatör. |
| **Medelstor till stor ändring (> 5 rader)** | `Fullständig Fil` | Standardläget. Minimerar risken för manuella fel. |
| **Programmatisk/Automatiserad Patchning** | `Strukturerad JSON-patch` (enligt `Diff_Protocol_v3.md`) | Används när ett verktyg ska applicera patchen automatiskt. |
