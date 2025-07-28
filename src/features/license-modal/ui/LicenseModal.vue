<!-- src/features/license-modal/ui/LicenseModal.vue -->
<!-- Denna feature-komponent representerar den kompletta "Licensmodal"-funktionen. -->
<!-- Den använder den generella BaseModal-komponenten och fyller den med -->
<!-- BaseCanvasTextViewer, samt hanterar sin egen synlighet och datahämtning. -->
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
        <div class="license-viewer-wrapper">
          <BaseCanvasTextViewer :text="licenseText" />
        </div>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue';
import BaseModal from '../../../shared/ui/BaseModal.vue';
import BaseCanvasTextViewer from '../../../shared/ui/BaseCanvasTextViewer.vue';

// --- PROPS & EMITS ---
// Denna komponent använder v-model:isOpen för att låta föräldern styra
// när den ska visas.
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  }
});

const emit = defineEmits(['update:isOpen']);

// --- STATE ---
// En lokal reaktiv referens för att synkronisera med prop.
// Detta är standardpraxis för v-model i en Composition API-komponent.
const isModalOpen = ref(props.isOpen);
watch(() => props.isOpen, (newValue) => {
  isModalOpen.value = newValue;
});
watch(isModalOpen, (newValue) => {
  emit('update:isOpen', newValue);
});

const licenseText = ref('Laddar licenstext...');
const hasFetched = ref(false); // Flagga för att undvika onödiga hämtningar

// --- DATA FETCHING ---
const fetchLicense = async () => {
  // Hämta bara texten en gång.
  if (hasFetched.value) return;

  try {
    const response = await fetch('/LICENSE');
    if (response.ok) {
      licenseText.value = await response.text();
    } else {
      licenseText.value = 'Kunde inte ladda licenstexten.';
    }
  } catch (error) {
    console.error('Fel vid hämtning av licens:', error);
    licenseText.value = 'Ett fel uppstod vid hämtning av licensfilen.';
  } finally {
    hasFetched.value = true; // Markera att hämtning har försökts
  }
};

// --- LOGIC ---
// Använd en watcher för att trigga datahämtning endast när modalen öppnas
// för första gången. Detta är mer effektivt än att hämta data onMounted.
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
}

/* Denna wrapper är nödvändig för att ge canvas-komponenten en definierad höjd, */
/* vilket i sin tur gör att dess interna scroll-funktion fungerar korrekt. */
.license-viewer-wrapper {
  /* Höjden sätts relativt till viewporten för att fungera bra i en modal */
  height: 60vh;
  max-height: 500px; /* Sätter ett max-tak på höjden */
}
</style>
<!-- src/features/license-modal/ui/LicenseModal.vue -->
