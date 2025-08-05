# Projektets Dokumentationsindex

Detta dokument fungerar som en central karta över all styrande och teknisk dokumentation för "Engrove Audio Tools 2.0". Syftet är att ge AI-assistenten (Frankensteen) en översikt för att kunna begära specifik, kontextuell information vid behov.

---

### Kategori 1: Styrande Dokument (Kärnan)

Dessa dokument definierar projektets icke förhandlingsbara regler och standarder.

- **`Global UI-Standard Komponentspecifikation.md`**
  - **Syfte:** Innehåller de exakta, tekniska specifikationerna (färger, kanter, skuggor) för alla `shared/ui`-komponenters olika tillstånd (hover, focus, etc.).
  - **När ska den begäras?** Vid all implementation eller ändring av en UI-komponent i `src/shared/ui/`.

- **`Global UI-Standard för Engrove-plattformen.md`**
  - **Syfte:** Definierar den övergripande designfilosofin, färgpaletter, typografi och globala UI-principer.
  - **När ska den begäras?** När nya UI-mönster diskuteras eller när den övergripande visuella identiteten är relevant.

- **`Mappstruktur & Arbetsflöde.md`**
  - **Syfte:** Definierar den strikta, FSD-inspirerade mappstrukturen och det AI-drivna arbetsflödet.
  - **När ska den begäras?** När nya filer eller moduler ska skapas, för att säkerställa att de placeras korrekt i arkitekturen.

- **`Teknisk Beskrivning: Engrove Audio Toolkit.md`**
  - **Syfte:** Ger en teknisk översikt av frontend-stacken (Vite, Vue, Pinia) och offline-databehandlingen.
  - **När ska den begäras?** För att få en övergripande förståelse av den tekniska arkitekturen eller vid frågor om kärnbiblioteken.

- **`Blueprint för Migrering: Engrove Audio Toolkit v1.0 -> v2.0.md`**
  - **Syfte:** Innehåller den detaljerade migreringsplanen, den nya namnstandarden för datafiler och den strategiska visionen för framtida "wow-funktioner".
  - **När ska den begäras?** Vid strategiska diskussioner om projektets roadmap eller vid frågor om hur v1.0-logik ska mappas till v2.0.

- **`Projektfil-Manifest: Engrove Audio Toolkit v2.0.md`**
  - **Syfte:** Den slutgiltiga sanningskällan för varje fils syfte i den nuvarande projektstrukturen.
  - **När ska den begäras?** Alltid. Denna fil bör ingå som en grundläggande del av kontexten i varje ny session för att ge en omedelbar arkitektonisk översikt.

---

### Kategori 2: Teknisk Underlag (Djupdykningar)

Dessa dokument ger djupgående teknisk information om specifika, komplexa moduler.

- **`Databehandlingskedja för Engrove Audio Toolkit.md` & relaterade filer**
  - **Syfte:** Beskriver i detalj den Python-baserade databehandlingskedjan (`runme.bat`, `ai_new_20.py`, `prepare_data.py`).
  - **När ska den begäras?** När uppgiften specifikt rör underhåll, felsökning eller utveckling av backend-skripten för datagenerering.

- **Dokumentation relaterad till `AR Protractor`**
  - **Syfte:** Innehåller all teknisk specifikation, utvärdering och kodbilagor för AR-funktionaliteten.
  - **När ska den begäras?** När uppgiften specifikt rör utveckling eller felsökning av AR-modulen.

---

### Kategori 3: Historik och Kontext

Dessa dokument är arkivmaterial som är värdefullt för att förstå projektets utveckling.

- **`ByggLogg.md`**
  - **Syfte:** En formell, steg-för-steg-logg över genomförda utvecklingssteg.
  - **När ska den begäras?** För att förstå historiska beslut, felsöka en regression eller för att skapa en ny loggpost.

- **`Gemini_chatthistorik.txt`**
  - **Syfte:** En detaljerad, kronologisk historik över AI-interaktioner.
  - **När ska den begäras?** Vid behov av att granska en specifik dialog eller ett tidigare resonemang i detalj.
