// src/showcase.js
/**
 * @file Detta är den centrala "motorn" för showcase-sidan (showcase.html).
 * Den skapar en fristående Vue-app, importerar och registrerar alla UI-komponenter,
 * och hanterar logiken för att växla mellan olika teman (ljust/mörkt och densitet).
 * Modul: UI Showcase
 */

import { createApp, ref, computed } from 'vue';

// --- Importera Pinia och Stores ---
import { createPinia } from 'pinia';
import piniaPluginPersistedState from 'pinia-plugin-persistedstate';
import { useThemeStore } from './entities/theme/model/themeStore.js';
import { useSettingsStore } from './entities/settings/model/settingsStore.js';

// --- Importera alla UI-komponenter och Features ---
import BaseButton from './shared/ui/BaseButton.vue';
import BaseInput from './shared/ui/BaseInput.vue';
import BaseSelect from './shared/ui/BaseSelect.vue';
import BaseToggle from './shared/ui/BaseToggle.vue';
import BaseCheckbox from './shared/ui/BaseCheckbox.vue';
import BaseRadio from './shared/ui/BaseRadio.vue';
import BaseModal from './shared/ui/BaseModal.vue';
import LicenseModal from './features/license-modal/ui/LicenseModal.vue';
import DensityToggle from './features/density-toggle/ui/DensityToggle.vue'; // Ny import

// --- Skapa Pinia-instans ---
const pinia = createPinia();
pinia.use(piniaPluginPersistedState);

const showcaseApp = {
  setup() {
    // Använd de centraliserade stores för att hantera teman
    const themeStore = useThemeStore();
    const settingsStore = useSettingsStore();

    // --- REAKTIVT STATE FÖR SHOWCASE-SPECIFIKA ELEMENT ---
    const isLicenseModalOpen = ref(false);
    const selectedValue = ref('option2');
    const toggleValueOff = ref(false);
    const toggleValueOn = ref(true);
    const checkboxUnchecked = ref(false);
    const checkboxChecked = ref(true);
    const radioValue = ref('val2');
    const selectOptions = ref([
      { value: 'option1', label: 'Första Alternativet' },
      { value: 'option2', label: 'Andra Alternativet' },
      { value: 'option3', label: 'Tredje Alternativet' },
      { value: 'disabled', label: 'Inaktiverat', disabled: true },
    ]);

    // --- BERÄKNADE EGENSKAPER FÖR KLASSER ---
    const otherTheme = computed(() => (themeStore.isDarkTheme ? 'ljust' : 'mörkt'));

    // Kombinerar klasser för både färg och densitet
    const containerClasses = computed(() => {
      const classes = [];
      if (!themeStore.isDarkTheme) {
        classes.push('light-theme');
      }
      if (settingsStore.isCompact) {
        classes.push('compact-theme');
      }
      return classes;
    });

    // Applicera klasserna på <html>-elementet för global styling
    watch(containerClasses, (newClasses) => {
      document.documentElement.className = newClasses.join(' ');
    }, { immediate: true }); // Kör direkt vid laddning

    return {
      // Stores
      themeStore,
      settingsStore,
      // State
      isLicenseModalOpen,
      selectedValue,
      toggleValueOff,
      toggleValueOn,
      checkboxUnchecked,
      checkboxChecked,
      radioValue,
      selectOptions,
      // Computed
      otherTheme,
      containerClasses,
    };
  }
};

const app = createApp(showcaseApp);

// Använd Pinia i appen
app.use(pinia);

// --- Registrera alla komponenter globalt ---
app.component('BaseButton', BaseButton);
app.component('BaseInput', BaseInput);
app.component('BaseSelect', BaseSelect);
app.component('BaseToggle', BaseToggle);
app.component('BaseCheckbox', BaseCheckbox);
app.component('BaseRadio', BaseRadio);
app.component('BaseModal', BaseModal);
app.component('LicenseModal', LicenseModal);
app.component('DensityToggle', DensityToggle); // Ny registrering

app.mount('#showcase-app');
// src/showcase.js
