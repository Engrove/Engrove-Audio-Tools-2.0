// public/showcase.js
// Detta skript är "motorn" för showcase.html. Det skapar en fristående Vue-app,
// importerar UI-komponenter från /src/shared/ui, registrerar dem globalt (endast
// för denna sida) och hanterar interaktivitet som temaväxling.

import { createApp, ref, computed } from 'vue';

// Importera baskomponenter från källkodsmappen.
// Denna relativa sökväg fungerar eftersom Vite's dev-server serverar från projektets rot.
import BaseButton from '../src/shared/ui/BaseButton.vue';
// ... framtida komponenter importeras här, t.ex. BaseInput ...

// Vue-appens definition för showcase-sidan.
const showcaseApp = {
  setup() {
    // === Reaktiva Variabler ===
    // 'dark' eller 'light'. Startar som mörkt tema.
    const currentTheme = ref('dark');

    // === Beräknade Egenskaper (Computed Properties) ===

    // Returnerar den CSS-klass som ska appliceras på body-elementet.
    const themeClass = computed(() => {
      // Om currentTheme.value är 'dark', returnera 'dark-theme'.
      // Annars, returnera 'light-theme'.
      return currentTheme.value === 'dark' ? 'dark-theme' : 'light-theme';
    });

    // Returnerar texten för temaväxlarknappen.
    const otherTheme = computed(() => {
      // Om currentTheme.value är 'dark', returnera 'ljust'.
      // Annars, returnera 'mörkt'.
      return currentTheme.value === 'dark' ? 'ljust' : 'mörkt';
    });

    // === Funktioner ===

    // Växlar det nuvarande temat och uppdaterar CSS-klassen på body.
    function toggleTheme() {
      currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark';
      // Applicera klassen direkt på <html>-taggen för att säkerställa
      // att alla CSS-variabler uppdateras korrekt över hela sidan.
      document.documentElement.className = themeClass.value;
    }

    // === Initialisering ===

    // Sätt det initiala temat när komponenten monteras.
    document.documentElement.className = themeClass.value;


    // Exponera variabler och funktioner till templaten.
    return {
      themeClass,
      otherTheme,
      toggleTheme
    };
  }
};

// Skapa en ny Vue app-instans med vår definition.
const app = createApp(showcaseApp);

// Registrera alla importerade baskomponenter globalt så att de
// kan användas direkt i showcase.html utan att behöva importeras där.
app.component('BaseButton', BaseButton);
// ... app.component('BaseInput', Base-Input) ...

// Montera Vue-appen på div-elementet med id="showcase-app".
app.mount('#showcase-app');
// public/showcase.js
