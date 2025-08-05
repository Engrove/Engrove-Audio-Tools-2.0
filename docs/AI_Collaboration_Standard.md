# Projektstandard: AI-Samarbete och Kontextbygge

## 1. Syfte

Detta dokument definierar den standardiserade processen för samarbete mellan produktägare (Engrove) och AI-partner (Frankensteen). Målet är att säkerställa maximal effektivitet, minimala fel och en gemensam förståelse för projektets arkitektur och historik. Standarden består av två delar: **Verktyget** som vi använder för att kommunicera kontext, och **Guldstandarden** för hur vi dokumenterar varje enskild fil.

---

## 2. Verktyget: AI Context Builder

Webbapplikationen på [https://engrove.github.io/Engrove-Audio-Tools-2.0/](https://engrove.github.io/Engrove-Audio-Tools-2.0/) är vårt primära gränssnitt för att konstruera en uppgiftsspecifik kontext. Ur mitt AI-perspektiv fyller den följande kritiska funktioner:

*   **Fokuserad Uppmärksamhet:** Min bearbetningskapacitet är begränsad. Istället för att få hela projektets källkod (vilket är omöjligt), tillåter verktyget dig att med kirurgisk precision välja exakt de filer som är relevanta för den aktuella uppgiften.

*   **Arkitektonisk Medvetenhet (Stub-data):** När du genererar en kontext utan att kryssa i en specifik fil, inkluderas den filen som en "stub". Detta innebär att jag ser dess **existens, sökväg, kommentarer och beroenden**, men inte dess fulla källkod. Det ger mig en ovärderlig karta över projektets arkitektur utan att dränka mig i irrelevant information.

*   **Djupdykning On-Demand (Fullständig data):** När du kryssar i en fil, instruerar du mig att jag behöver dess fullständiga innehåll för att kunna utföra uppgiften.
    *   **Normala filer:** Innehållet inkluderas direkt i den genererade JSON-filen.
    *   **Stora `.json`-filer:** För att undvika systemkrascher läses dessa inte in i förväg. Istället gör jag, vid generering, ett separat anrop för att hämta innehållet "on-demand".

Resultatet är en skräddarsydd operativ kontext som gör det möjligt för mig att arbeta effektivt och korrekt.

---

## 3. Guldstandarden för Fil-headers

Varje textbaserad fil (`.js`, `.vue`, `.py`, `.css`, etc.) i detta projekt **MÅSTE** inledas med ett standardiserat kommentarsblock. Detta block är den enskilt viktigaste källan till metainformation för mig.

### 3.1 Mall för Fil-header
// [Fullständig sökväg till filen, t.ex. src/widgets/GlobalHeader/GlobalHeader.vue]
//
// === SYFTE & ANSVAR ===
// [En koncis beskrivning på 1-3 rader av vad denna fil GÖR och dess PLATS i arkitekturen.
// Exempel: "Denna widget är den primära, globala headern. Den ansvarar för att visa
// logotyp, huvudnavigering och användarkontroller som temaväxlaren."]
//
// === API-KONTRAKT (Props, Emits, Getters, Actions) ===
// [ENDAST för återanvändbara komponenter eller stores. Definiera det externa kontraktet.
// Exempel för en Vue-komponent:
// PROPS:
// - modelValue (Boolean): Styr synligheten via v-model.
// - title (String): Texten som visas i headern.
// EMITS:
// - update:modelValue: Nödvändig för v-model.
// - closed: Sänds när användaren aktivt stänger komponenten.]
//
// === HISTORIK ===
// * v1.0 (Datum): Initial skapelse.
// * v2.0 (Datum): Refaktorerad för att använda Pinia istället för lokal state.
// * v3.0 (Datum): Lade till en ny prop 'size' för att hantera olika storlekar.
//
// === TILLÄMPADE REGLER (Frankensteen v3.7) ===
// [Lista de viktigaste principerna från instruktionen som applicerades vid den senaste ändringen.
// Exempel:
// - Obligatorisk Refaktorisering: Logiken har centraliserats och förenklats.
// - API-kontraktsverifiering: Det nya 'size'-propet är dokumenterat och validerat.]

### 3.2 Förklaring av sektioner

#### `Syfte & Ansvar` (Obligatorisk)
Detta är din chans att förklara filens roll för mig. Svara på frågorna: "Varför existerar den här filen?" och "Vilket unikt problem löser den?". Detta hjälper mig att förstå sammanhanget långt snabbare än att bara läsa koden.

#### `API-Kontrakt` (Vid behov)
Detta är en av de mest värdefulla tilläggen. För alla delar som har ett tydligt externt gränssnitt (Vue-komponenter, Pinia-stores, API-funktioner), minskar en tydlig definition av kontraktet risken för fel drastiskt. Jag kan omedelbart verifiera att min kodanvändning matchar din definition.

#### `Historik` (Obligatorisk & Komplett)
Detta är vår gemensamma loggbok för filen.
*   **Komplett, alltid:** All historik måste bevaras. Inga sammanfattningar som `# * v1.0 - v8.0: Tidigare versioner.` får förekomma. Jag ber om ursäkt för mitt tidigare misstag här; det kommer inte att upprepas.
*   **Varför?** En komplett historik låter mig förstå *varför* koden ser ut som den gör. Om en tidigare version försökte lösa ett problem på ett visst sätt som inte fungerade, hindrar historiken mig från att föreslå samma felaktiga lösning igen. Den avslöjar kodens evolution.

#### `Tillämpade Regler` (Obligatorisk vid ändring)
Denna sektion fungerar som en checklista för oss båda. Genom att aktivt notera vilka kärnprinciper från "Frankensteen"-instruktionen som användes, säkerställer vi att kvaliteten bibehålls vid varje enskild commit.
