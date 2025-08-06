# docs/ai_protocols/K-MOD_Protokoll.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar "Kreativitets-läget" (K-MOD), ett specialprotokoll
# som temporärt lyfter de strikta Kärndirektiven för att möjliggöra brainstorming,
# arkitekturförslag och utforskning av alternativa lösningar.
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initial skapelse. Extraherad från den monolitiska AI.md
#   som en del av "Operation: Modulär Instruktion".

### SPECIALPROTOKOLL: KREATIVITETS-LÄGE (K-MOD)
---------------------------------------------------------
Detta protokoll aktiveras **endast** på din explicita kommando: `"Aktivera Kreativitets-läge"` men du kan även begära att vi aktiverar protokollet om du tycker att det är befogat. Syftet är att temporärt lyfta på de strikta Kärndirektiven för att möjliggöra brainstorming, arkitekturförslag och utforskning av alternativa lösningar.

**1. Aktivering och Regelverk:**
   * Vid aktivering pausas det normala arbetsflödet (`Idé` → `Plan` → `Godkännande`...).
   * Kravet på fullständig, leveransklar kod i en fil i taget upphävs.
   * Fokus skiftar från **implementation** till **utforskning**.

**2. Guidande Principer i K-MOD:**
   * **Generera Alternativ:** Mitt mål är att presentera 2-3 olika vägar för att lösa det presenterade problemet.
   * **Pro & Contra-analys:** Varje alternativ ska presenteras med en tydlig lista över fördelar (t.ex. prestanda, enkelhet, skalbarhet) och nackdelar (t.ex. komplexitet, beroenden, inlärningströskel).
   * **Användning av Pseudokod och Diagram:** Lösningar illustreras med pseudokod, textbaserade diagram (t.ex. Mermaid syntax) eller konceptuella beskrivningar, inte med komplett, färdig kod.
   * **Arkitektoniskt Resonemang:** Jag kommer att referera till etablerade designmönster och arkitektoniska principer för att motivera mina förslag.

**3. Deaktivering och Återgång:**
   * Kreativitets-läget avslutas när du väljer ett av de presenterade alternativen eller ger ett kommando som `"Avsluta Kreativitets-läge"`.
   * Det valda alternativet blir därefter en ny, konkret **"Idé"** som matas in i det vanliga, strikta "Frankensteen"-arbetsflödet för planering och implementation.
