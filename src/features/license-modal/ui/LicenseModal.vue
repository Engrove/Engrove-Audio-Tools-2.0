<!-- src/features/license-modal/ui/LicenseModal.vue -->
<!-- Denna feature-komponent representerar den kompletta "Licensmodal"-funktionen. -->
<!-- Denna korrigerade version använder en enkel och robust <pre>-tagg för att -->
<!-- visa den förformaterade licenstexten, istället för canvas. -->
<template>
  <BaseModal v-model:isOpen="isModalOpen">
    <template #header>
      Software License
    </template>
    
    <template #default>
      <div class="license-content">
        <p class="license-preamble">
          Engrove Audio Toolkit is distributed under the GNU Affero General Public License v3.0.
          The full license text is provided below.
        </p>
        <!-- Använder en <pre>-tagg för att visa texten. -->
        <!-- Den bevarar radbrytningar och mellanslag från textfilen. -->
        <pre class="license-text-container">{{ licenseText }}</pre>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue';
import BaseModal from '../../../shared/ui/BaseModal.vue';

// --- PROPS & EMITS ---
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  }
});

const emit = defineEmits(['update:isOpen']);

// --- STATE ---
const isModalOpen = ref(props.isOpen);
watch(() => props.isOpen, (newValue) => {
  isModalOpen.value = newValue;
});
watch(isModalOpen, (newValue) => {
  emit('update:isOpen', newValue);
});

const licenseText = ref('Laddar licenstext...');
const hasFetched = ref(false);

// --- DATA FETCHING ---
const fetchLicense = async () => {
  if (hasFetched.value) return;

  try {
    const response = await fetch('/LICENSE'); // Hämtar från /public/LICENSE
    if (response.ok) {
      licenseText.value = await response.text();
    } else {
      licenseText.value = 'Kunde inte ladda licenstexten.';
    }
  } catch (error) {
    console.error('Fel vid hämtning av licens:', error);
    licenseText.value = 'Ett fel uppstod vid hämtning av licensfilen.';
  } finally {
    hasFetched.value = true;
  }
};

// --- LOGIC ---
// Hämtar texten när modalen öppnas för första gången.
watch(isModalOpen, (newValue) => {
  if (newValue && !hasFetched.value) {
    fetchLicense();
  }
});
</script>

<style scoped>
.license-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.license-preamble {
  color: var(--color-text-medium-emphasis);
  font-size: var(--font-size-label);
  margin-bottom: 0.5rem;
  white-space: normal; /* Tillåt radbrytning i ingressen */
}

.license-text-container {
  /* Styling för <pre>-taggen */
  background-color: var(--color-surface-primary); /* Något mörkare bakgrund för kontrast */
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
  padding: 1rem;
  
  /* Typsnitt och textformatering */
  font-family: var(--font-family-monospace);
  font-size: 13px; /* Något mindre för att få plats med mer text */
  line-height: 1.6;
  color: var(--color-text-medium-emphasis);
  
  /* Scroll-beteende */
  white-space: pre-wrap; /* Tillåter webbläsaren att bryta långa rader */
  overflow-y: auto; /* Lägger till en scrollbar om innehållet är för högt */

  /* Höjd-begränsningar */
  height: 60vh;
  max-height: 500px;
}
</style>
<!-- src/features/license-modal/ui/LicenseModal.vue -->
