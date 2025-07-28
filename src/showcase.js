// src/showcase.js
// Denna fil fungerar som JavaScript-motorn för den fristående testmiljön showcase.html.
// Den skapar en liten Vue-applikation, importerar och registrerar alla delade UI-komponenter,
// hanterar temaväxling och förbereder data som komponenterna behöver för att visas korrekt.

import { createApp, ref, computed, onMounted } from 'vue';

// Importera globala stilar och design-tokens.
// Vite säkerställer att detta injiceras som en <style>-tagg i showcase.html.
import './app/styles/_tokens.css';
import './app/styles/_global.css';

// Importera alla delade UI-komponenter
import BaseButton from './shared/ui/BaseButton.vue';
import BaseInput from './shared/ui/BaseInput.vue';
import BaseSelect from './shared/ui/BaseSelect.vue';
import BaseToggle from './shared/ui/BaseToggle.vue';
import BaseCheckbox from './shared/ui/BaseCheckbox.vue';
import BaseRadio from './shared/ui/BaseRadio.vue';
import BaseCanvasTextViewer from './shared/ui/BaseCanvasTextViewer.vue'; // Den nya komponenten

const showcaseApp = {
  setup() {
    // --- Logik för Temaväxling ---
    const currentTheme = ref('dark'); // 'dark' är standard

    const otherTheme = computed(() => {
        // Om currentTheme är 'dark', returnera 'ljust'. Annars, returnera 'mörkt'.
        return currentTheme.value === 'dark' ? 'ljust' : 'mörkt';
    });

    function toggleTheme() {
      currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark';
      // Applicerar temaklassen direkt på <html>-elementet för global effekt.
      document.documentElement.className = currentTheme.value === 'dark' ? '' : 'light-theme';
    }

    // --- Reaktiva Modeller för Komponenter ---
    // Denna data behövs för att v-model ska fungera på komponenterna i showcase.html
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

    // --- Logik för Licenstext ---
    const licenseText = ref('Laddar licenstext...');

    // När appen monteras, hämta texten från LICENSE-filen i /public mappen
    onMounted(async () => {
      try {
        const response = await fetch('/LICENSE');
        if (response.ok) {
          licenseText.value = await response.text();
        } else {
          licenseText.value = 'Kunde inte ladda licenstexten. Kontrollera att filen /LICENSE finns i projektets rot.';
        }
      } catch (error) {
        console.error('Fel vid hämtning av licens:', error);
        licenseText.value = 'Ett fel uppstod vid hämtning av licensfilen.';
      }
    });

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
      licenseText,
    };
  }
};

// Skapa och montera Vue-appen
const app = createApp(showcaseApp);

// Registrera alla komponenter globalt så de kan användas med sina tagg-namn
app.component('BaseButton', BaseButton);
app.component('BaseInput', BaseInput);
app.component('BaseSelect', BaseSelect);
app.component('BaseToggle', BaseToggle);
app.component('BaseCheckbox', BaseCheckbox);
app.component('BaseRadio', BaseRadio);
app.component('BaseCanvasTextViewer', BaseCanvasTextViewer);

app.mount('#showcase-app');
// src/showcase.js
