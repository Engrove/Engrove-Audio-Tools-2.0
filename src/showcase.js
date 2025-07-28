// src/showcase.js
// Denna fil fungerar som JavaScript-motorn för den fristående testmiljön showcase.html.
// Den skapar en liten Vue-applikation, importerar och registrerar alla delade UI-komponenter,
// hanterar temaväxling och förbereder data som komponenterna behöver för att visas korrekt.

import { createApp, ref, computed } from 'vue';

// Importera globala stilar och design-tokens.
import './app/styles/_tokens.css';
import './app/styles/_global.css';

// Importera alla delade UI-komponenter
import BaseButton from './shared/ui/BaseButton.vue';
import BaseInput from './shared/ui/BaseInput.vue';
import BaseSelect from './shared/ui/BaseSelect.vue';
import BaseToggle from './shared/ui/BaseToggle.vue';
import BaseCheckbox from './shared/ui/BaseCheckbox.vue';
import BaseRadio from './shared/ui/BaseRadio.vue';
import BaseModal from './shared/ui/BaseModal.vue'; // Importerar BaseModal

// Importera feature-komponenten vi vill testa
import LicenseModal from './features/license-modal/ui/LicenseModal.vue';

const showcaseApp = {
  setup() {
    // --- Logik för Temaväxling ---
    const currentTheme = ref('dark');

    const otherTheme = computed(() => {
        return currentTheme.value === 'dark' ? 'ljust' : 'mörkt';
    });

    function toggleTheme() {
      currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark';
      document.documentElement.className = currentTheme.value === 'dark' ? '' : 'light-theme';
    }

    // --- Reaktiva Modeller för Komponenter ---
    const selectedValue = ref('option2');
    const selectOptions = ref([
      { value: 'option1', label: 'Alternativ 1' },
      { value: 'option2', label: 'Alternativ 2' },
      { value: 'option3', label: 'Alternativ 3 (inaktivt)', disabled: true },
    ]);
    const toggleValueOff = ref(false);
    const toggleValueOn = ref(true);
    const checkboxUnchecked = ref(false);
    const checkboxChecked = ref(true);
    const radioValue = ref('val2');

    // --- Logik för Modal-test ---
    const isLicenseModalOpen = ref(false);

    // Exponera allt som behövs av template-delen i showcase.html
    return {
      otherTheme,
      toggleTheme,
      selectedValue,
      selectOptions,
      toggleValueOff,
      toggleValueOn,
      checkboxUnchecked,
      checkboxChecked,
      radioValue,
      isLicenseModalOpen,
    };
  }
};

// Skapa och montera Vue-appen
const app = createApp(showcaseApp);

// Registrera alla komponenter globalt
app.component('BaseButton', BaseButton);
app.component('BaseInput', BaseInput);
app.component('BaseSelect', BaseSelect);
app.component('BaseToggle', BaseToggle);
app.component('BaseCheckbox', BaseCheckbox);
app.component('BaseRadio', BaseRadio);
app.component('BaseModal', BaseModal);
app.component('LicenseModal', LicenseModal); // Registrerar vår nya feature

app.mount('#showcase-app');
// src/showcase.js
