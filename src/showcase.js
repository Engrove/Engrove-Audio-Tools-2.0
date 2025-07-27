// src/showcase.js
// Detta är JavaScript-ingångspunkten för vår komponent-showcase.
// Denna version är slutgiltigt korrigerad från alla tidigare syntaxfel.

import { createApp, ref, computed } from 'vue';

// STEG 1: Importera globala stilar.
import './app/styles/_tokens.css';
import './app/styles/_global.css';

// STEG 2: Importera alla baskomponenter.
import BaseButton from './shared/ui/BaseButton.vue';
import BaseInput from './shared/ui/BaseInput.vue';
import BaseSelect from './shared/ui/BaseSelect.vue';
import BaseToggle from './shared/ui/BaseToggle.vue';
import BaseCheckbox from './shared/ui/BaseCheckbox.vue';
import BaseRadio from './shared/ui/BaseRadio.vue';

// STEG 3: Definiera och montera Vue-appen.
const showcaseApp = {
  setup() {
    const currentTheme = ref('dark');

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

    function toggleTheme() {
      currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark';
      document.documentElement.className = themeClass.value;
    }

    document.documentElement.className = themeClass.value;

    return {
      themeClass,
      otherTheme,
      toggleTheme,
    };
  }
};

const app = createApp(showcaseApp);

// Registrera alla komponenter globalt.
// Varje rad har nu verifierats för korrekta variabelnamn.
app.component('BaseButton', BaseButton);
app.component('BaseInput', BaseInput);
app.component('BaseSelect', BaseSelect);
app.component('BaseToggle', BaseToggle);
app.component('BaseCheckbox', BaseCheckbox);
app.component('BaseRadio', BaseRadio);

app.mount('#showcase-app');
// src/showcase.js
