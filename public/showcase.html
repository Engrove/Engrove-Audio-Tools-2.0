// public/showcase.js
// Detta skript är "motorn" för showcase.html. Det skapar en fristående Vue-app,
// importerar ALLA UI-komponenter från /src/shared/ui, registrerar dem globalt (endast
// för denna sida) och hanterar interaktivitet som temaväxling.

import { createApp, ref, computed } from 'vue';

// Importera ALLA baskomponenter från källkodsmappen.
import BaseButton from '../src/shared/ui/BaseButton.vue';
import BaseInput from '../src/shared/ui/BaseInput.vue';
import BaseSelect from '../src/shared/ui/BaseSelect.vue';
import BaseToggle from '../src/shared/ui/BaseToggle.vue';
import BaseCheckbox from '../src/shared/ui/BaseCheckbox.vue';
import BaseRadio from '../src/shared/ui/BaseRadio.vue';

// Vue-appens definition för showcase-sidan.
const showcaseApp = {
  setup() {
    // === Reaktiva Variabler ===
    const currentTheme = ref('dark'); // 'dark' eller 'light'.

    // === Beräknade Egenskaper (Computed Properties) ===
    const themeClass = computed(() => {
      // Om currentTheme.value är 'dark', returnera 'dark-theme'.
      // Annars, returnera 'light-theme'.
      return currentTheme.value === 'dark' ? 'dark-theme' : 'light-theme';
    });

    const otherTheme = computed(() => {
      // Om currentTheme.value är 'dark', returnera 'ljust'.
      // Annars, returnera 'mörkt'.
      return currentTheme.value === 'dark' ? 'ljust' : 'mörkt';
    });

    // === Funktioner ===
    function toggleTheme() {
      currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark';
      // Applicera klassen direkt på <html>-taggen för global effekt.
      document.documentElement.className = themeClass.value;
    }

    // === Initialisering ===
    // Sätt det initiala temat när appen startar.
    document.documentElement.className = themeClass.value;

    // Exponera till templaten i showcase.html
    return {
      themeClass,
      otherTheme,
      toggleTheme,
    };
  }
};

// Skapa Vue-appen
const app = createApp(showcaseApp);

// Registrera ALLA komponenter globalt så de kan användas i showcase.html
app.component('BaseButton', BaseButton);
app.component('BaseInput', BaseInput);
app.component('BaseSelect', BaseSelect);
app.component('BaseToggle', BaseToggle);
app.component('BaseCheckbox', BaseCheckbox);
app.component('BaseRadio', BaseRadio);

// Montera appen
app.mount('#showcase-app');
// public/showcase.js
