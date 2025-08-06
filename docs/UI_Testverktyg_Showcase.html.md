# docs/UI_Testverktyg_Showcase.html.md
#
# === SYFTE & ANSVAR ===
# Detta dokument beskriver syftet och den tekniska implementeringen av
# `showcase.html`, den fristående utvecklingsmiljön för UI-komponenter.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initial skapelse. Konverterad från ett ostrukturerat textdokument
#   till en formell, strukturerad Markdown-fil.
#
# === TILLÄMPADE REGLER (Frankensteen v3.8) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och konverterats.

# Del 1: Syfte och Filosofi

`showcase.html` är hjärtat i ert UI-utvecklingsflöde och den pragmatiska "KISS"-ersättningen för komplexa verktyg som Storybook. Det är en enda, fristående HTML-fil som fungerar som en levande, interaktiv verkstad för alla era grundläggande UI-komponenter. Dess syfte är fyrfaldigt:

1.  **Isolerad Utveckling:** Tillåter dig och din AI att bygga och styla komponenter som knappar och inmatningsfält helt isolerat från resten av applikationens logik och komplexitet.
2.  **Visuell Verifiering:** Fungerar som en visuell checklista där ni kan se varje komponent i alla dess specificerade tillstånd (Default, Hover, Focus, Active, Disabled) sida vid sida, för både mörkt och ljust tema. Detta omvandlar era statiska designdokument till ett levande, verifierbart system.
3.  **Central Sanningskälla:** Filen blir den enda, obestridliga källan till sanning för hur en baskomponent ska se ut och bete sig. Om en komponent ser korrekt ut i `showcase.html`, är den korrekt.
4.  **Perfekt AI-Kontext:** Genom att vara en enda, avgränsad fil är den idealisk att ge som kontext till din AI. Du kan ge hela filens innehåll till AI:n och be den att lägga till eller ändra en sektion, vilket drastiskt minskar risken för missförstånd.

## Del 2: Teknisk Implementation

För att `showcase.html` ska kunna rendera era Vue-komponenter behöver den fungera som en egen liten, fristående Vue-applikation.

### 2.1 Filplacering

Filen ska placeras i mappen `/public/` i ert projekt:
*   `/public/showcase.html`

Detta gör att den enkelt kan nås i webbläsaren under utveckling och deployas direkt till Cloudflare Pages för granskning.

### 2.2 Grundläggande Struktur

`showcase.html` kommer att bestå av tre delar:
1.  HTML-stommen: En standard HTML5-struktur som innehåller sektioner för varje komponent.
2.  CSS-länkar: Länkar till era globala stilmallar, särskilt den som innehåller era design-tokens (färger, typsnitt etc.).
3.  JavaScript-motor: Ett litet skript som startar en Vue-instans och monterar den på HTML-stommen, vilket gör det möjligt att använda era `.vue`-komponenter.

### 2.3 Den Levande Verkstaden: `showcase.html`

Detta är den fullständiga koden för er `showcase.html`. Den är designad för att vara en startmall som du ger till din AI.

```html
<!DOCTYPE html>
<html lang="sv">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Engrove UI Component Showcase</title>
   <link rel="stylesheet" href="/src/app/styles/_tokens.css">
   <link rel="stylesheet" href="/src/app/styles/_global.css">
   <style>
       /* Interna stilar endast för denna showcase-sida */
       body { font-family: 'Inter', sans-serif; padding: 2rem; transition: background-color 0.3s, color 0.3s; }
      .showcase-section { margin-bottom: 4rem; border-bottom: 1px solid var(--color-border-primary); padding-bottom: 2rem; }
      .showcase-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 2rem; align-items: center; }
      .component-state { display: flex; flex-direction: column; gap: 0.5rem; }
      .component-state-label { font-size: 12px; color: var(--color-text-medium-emphasis); }
       h1, h2, h3 { color: var(--color-text-high-emphasis); }
       
       /* Klasser för att simulera interaktiva tillstånd */
      .pseudo-hover { /* Stilar för att efterlikna :hover */ }
      .pseudo-focus { /* Stilar för att efterlikna :focus */ }
      .pseudo-active { /* Stilar för att efterlikna :active */ }

       /* Temahantering */
      .dark-theme { background-color: var(--color-surface-primary); }
      .light-theme { background-color: var(--color-surface-primary); }
   </style>
</head>
<body>

   <div id="showcase-app">
       <h1>Engrove UI Component Showcase</h1>
       <p>Detta är en levande dokumentation av alla baskomponenter i `shared/ui`.</p>
       
       <base-button @click="toggleTheme">Växla till {{ otherTheme }} tema</base-button>

       <div class="showcase-section" :class="themeClass">
           <h2>Knappar (Buttons)</h2>
           <p>Baseras på specifikation 1.1 och 1.2 i Appendix.</p>
           
           <h3>Primär Knapp</h3>
           <div class="showcase-grid">
               <div class="component-state">
                   <span class="component-state-label">Default</span>
                   <base-button variant="primary">Klicka här</base-button>
               </div>
               <div class="component-state">
                   <span class="component-state-label">Hover</span>
                   <base-button variant="primary" class="pseudo-hover">Klicka här</base-button>
               </div>
               <div class="component-state">
                   <span class="component-state-label">Focus</span>
                   <base-button variant="primary" class="pseudo-focus">Klicka här</base-button>
               </div>
               <div class="component-state">
                   <span class="component-state-label">Active</span>
                   <base-button variant="primary" class="pseudo-active">Klicka här</base-button>
               </div>
               <div class="component-state">
                   <span class="component-state-label">Disabled</span>
                   <base-button variant="primary" :disabled="true">Klicka här</base-button>
               </div>
           </div>

           <h3>Sekundär Knapp</h3>
           <div class="showcase-grid">
               </div>
       </div>

       <div class="showcase-section" :class="themeClass">
           <h2>Inmatningsfält (Input Fields)</h2>
           </div>

       </div>

   <script type="importmap">
   {
       "imports": {
           "vue": "https://unpkg.com/vue@3/dist/vue.esm-browser.js"
       }
   }
   </script>
   <script type="module" src="/public/showcase.js"></script>

</body>
</html>
```
### 2.4 JavaScript-motorn: showcase.js

Skapa en ny fil i /public/ som heter showcase.js. Denna fil kommer att importera Vue och alla era baskomponenter och göra dem tillgängliga i showcase.html.

Instruktion till AI: "Skapa filen /public/showcase.js. Den ska importera createApp och ref från Vue. Den ska sedan importera alla komponenter från /src/shared/ui/ (t.ex. BaseButton.vue, BaseInput.vue). Skapa en ny Vue-app som hanterar temaväxling och registrera alla baskomponenter globalt så att de kan användas direkt i showcase.html."
```javascript
import { createApp, ref, computed } from 'vue';

// Importera alla era baskomponenter
import BaseButton from '../src/shared/ui/BaseButton.vue';
import BaseInput from '../src/shared/ui/BaseInput.vue';
//...importera resten av era komponenter

const showcaseApp = {
   setup() {
       const currentTheme = ref('dark'); // 'dark' eller 'light'

       const themeClass = computed(() => {
           return currentTheme.value === 'dark'? 'dark-theme' : 'light-theme';
       });

       const otherTheme = computed(() => {
           return currentTheme.value === 'dark'? 'ljust' : 'mörkt';
       });

       function toggleTheme() {
           currentTheme.value = currentTheme.value === 'dark'? 'light' : 'dark';
           // Applicera temat på body för globala stilar
           document.body.className = themeClass.value;
       }

       // Initiera temat vid start
       document.body.className = themeClass.value;

       return {
           themeClass,
           otherTheme,
           toggleTheme
       };
   }
};

const app = createApp(showcaseApp);

// Registrera alla komponenter globalt
app.component('BaseButton', BaseButton);
app.component('BaseInput', BaseInput);
//...registrera resten

app.mount('#showcase-app');
```
### Del 3: Arbetsflödet - Hur du ger AI tillgång

Detta är den exakta processen för att använda showcase.html för att instruera din AI. Processen är designad för att vara repetitiv och säker.

### Steg 1: Förbered Kontexten

Innan du ger en uppgift till AI:n, samla ihop all nödvändig information. Detta är det absolut viktigaste steget för att få ett bra resultat. Du behöver:

Hela innehållet i showcase.html.

Hela innehållet i showcase.js.

Den relevanta delen av er komponentspecifikation. Kopiera tabellen för den komponent du vill bygga från ert designdokument.

### Steg 2: Ge en Isolerad och Detaljerad Prompt

Nu kombinerar du kontexten med en mycket specifik instruktion.

Exempelprompt för att lägga till Inmatningsfält:

"Jag bygger en komponent-showcase. Här är den nuvarande koden och kontexten:
showcase.html:


<!-- Din showcase.html-kod här -->


showcase.js:


// Din showcase.js-kod här


Komponentspecifikation för Inmatningsfält (från Appendix, sektion 2.1 & 2.2):

Din uppgift:
Uppdatera showcase.html. I sektionen för "INMATNINGSFÄLT", lägg till kod för att visa komponenten BaseInput. Du ska, precis som för knapparna, visa upp alla dess tillstånd: Default, Hover, Focus och Disabled. Använd placeholder-text för att visa fälten. Skapa en grid för att visa alla tillstånd sida vid sida. Se till att det fungerar med temaväxlaren."

### Steg 3: Granska och Verifiera

När AI:n returnerar den uppdaterade koden för `showcase.html`:
1.  Kopiera och klistra in den i din lokala `showcase.html`-fil (t.ex. i Notepad++).
2.  Öppna filen i din webbläsare.
3.  Verifiera visuellt:
    *   Ser `BaseInput` korrekt ut i alla sina tillstånd?
    *   Fungerar temaväxlaren? Ändras färgerna enligt specifikationen för ljust/mörkt läge?
    *   Jämför med specifikationstabellerna du klistrade in i prompten.

### Steg 4: Iterera eller Godkänn

*   Om något är fel: Ge en korrigerande prompt. Var specifik. "Fokus-tillståndet för `BaseInput` i ljust läge är fel. Kanten ska vara 2px solid `$interactive-accent`. Uppdatera koden."
*   Om allt är korrekt: Du har nu en visuellt verifierad komponent. Du kan checka in den uppdaterade `showcase.html` och `showcase.js` till ditt GitHub-repository.

Genom att följa denna process blir `showcase.html` ert mest kraftfulla verktyg för att bygga ett robust och konsekvent UI-bibliotek, perfekt anpassat för ett AI-drivet arbetsflöde.
