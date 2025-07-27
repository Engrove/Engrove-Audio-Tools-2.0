// src/showcase.js
// Denna fil agerar som "motorn" för den fristående showcase.html.
// Den skapar en liten Vue-app, importerar och registrerar alla baskomponenter
// globalt, och hanterar tillstånd som temaväxling.

import { createApp, ref, computed } from 'vue';

// Importera globala stilar FÖRST för att säkerställa att de appliceras korrekt.
import './app/styles/_tokens.css';
import './app/styles/_global.css';

// Importera alla grundläggande UI-komponenter
import BaseButton from './shared/ui/BaseButton.vue';
import BaseInput from './shared/ui/BaseInput.vue';
import BaseSelect from './shared/ui/BaseSelect.vue';
import BaseToggle from './shared/ui/BaseToggle.vue';
import BaseCheckbox from './shared/ui/BaseCheckbox.vue';
import BaseRadio from './shared/ui/BaseRadio.vue';


const showcaseApp = {
  setup() {
    // --- TEMAHANTERING ---
    const currentTheme = ref('dark'); // 'dark' eller 'light'

    const themeClass = computed(() => {
      return currentTheme.value === 'dark' ? 'dark-theme' : 'light-theme';
    });
    const otherTheme = computed(() => {
      return currentTheme.value === 'dark' ? 'ljust' : 'mörkt';
    });

    function toggleTheme() {
      currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark';
      document.documentElement.className = themeClass.value; // Applicera på <html>-elementet
    }
    // Initiera temat vid start
    document.documentElement.className = themeClass.value;

    // --- TILLSTÅND FÖR KOMPONENTER ---
    // Detta är avgörande för att kunna testa v-model och interaktivitet.

    // För BaseSelect
    const selectOptions = ref([
      { value: 'opt1', label: 'Första Alternativet' },
      { value: 'opt2', label: 'Andra Alternativet' },
      { value: 'opt3', label: 'Tredje Alternativet' },
      { value: 'opt4', label: 'Ett mycket längre alternativ för att testa bredd', disabled: true },
    ]);
    const selectedValue = ref('opt2');

    // För BaseToggle
    const toggleValueOff = ref(false);
    const toggleValueOn = ref(true);
    
    // För BaseCheckbox
    const checkboxUnchecked = ref(false);
    const checkboxChecked = ref(true);

    // För BaseRadio
    const radioValue = ref('val2');


    return {
      // Temahantering
      otherTheme,
      toggleTheme,

      // Komponenttillstånd
      selectOptions,
      selectedValue,
      toggleValueOff,
      toggleValueOn,
      checkboxUnchecked,
      checkboxChecked,
      radioValue,
    };
  }
};

const app = createApp(showcaseApp);

// Registrera alla komponenter globalt för enkel användning i showcase.html
app.component('BaseButton', BaseButton);
app.component('BaseInput', BaseInput);
app.component('BaseSelect', BaseSelect);
app.component('BaseToggle', BaseToggle);
app.component('BaseCheckbox', BaseCheckbox);
app.component('BaseRadio', BaseRadio);

app.mount('#showcase-app');
