// src/showcase.js
// Detta är JavaScript-ingångspunkten för vår komponent-showcase.
// Eftersom den nu är en del av källkoden (`src`), kan Vite bearbeta den
// och dess importer korrekt.

import { createApp, ref, computed } from 'vue';

// STEG 1: Importera globala stilar.
// Vite kommer att se dessa importer och säkerställa att CSS-filerna inkluderas
// i den slutgiltiga bygget för showcase.html.
import './app/styles/_tokens.css';
import './app/styles/_global.css';

// STEG 2: Importera alla baskomponenter.
// Sökvägarna är nu relativa till /src.
import BaseButton from './shared/ui/BaseButton.vue';
import BaseInput from './shared/ui/BaseInput.vue';
import BaseSelect from './shared/ui/BaseSelect.vue';
import BaseToggle from './shared/ui/BaseToggle.vue';
import BaseCheckbox from './shared/ui/BaseCheckbox.vue';
import BaseRadio from './shared/ui/BaseRadio.vue';

// STEG 3: Definiera och montera Vue-appen.
// Denna logik är oförändrad.
const showcaseApp = {
  setup() {
    const currentTheme = ref('dark');

    const themeClass = computed(() => {
      return currentTheme.value === 'dark' ? 'dark-theme' : 'light-theme';
    });

    const otherTheme = computed(() => {
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

// Registrera alla komponenter globalt
app.component('BaseButton', BaseButton);
app.component('BaseInput', Base-Input);
app.component('BaseSelect', BaseSelect);
app.component('BaseToggle', BaseToggle);
app.component('BaseCheckbox', BaseCheckbox);
app.component('BaseRadio', BaseRadio);

app.mount('#showcase-app');
// src/showcase.js
