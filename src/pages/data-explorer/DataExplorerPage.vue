<!-- src/pages/data-explorer/DataExplorerPage.vue -->
<!--
  Detta är sidkomponenten för "Data Explorer". Dess primära ansvar är att
  arrangera layouten för de olika widgetarna och att initiera datainhämtningen
  när sidan laddas. Den hanterar även state för modal-fönstret.

  FELRÄTTNING (Regression från Steg 11):
  - Importerar och använder `storeToRefs` från Pinia för att säkerställa att
    state-variabler som `isLoading`, `error`, och `dataType` förblir reaktiva.
    Detta löser buggen där sidan fastnade permanent i laddningsläget.
-->
<template>
  <div class="page-container">
    <header class="page-header">
      <h1>Data Explorer</h1>
      <p class="page-description">
        Search, filter, and explore the complete database of tonearms and cartridges. Use the controls to start a search.
      </p>
    </header>

    <!-- Visar laddningsindikator medan datan hämtas -->
    <div v-if="isLoading" class="status-container loading">
      <p>Loading Component Databases...</p>
    </div>

    <!-- Visar felmeddelande om något går fel vid datainhämtning -->
    <div v-else-if="error" class="status-container error">
      <h2>Failed to load data</h2>
      <p>{{ error }}</p>
    </div>

    <!-- Huvudlayouten när datan är laddad -->
    <div v-else class="explorer-layout">
      <DataFilterPanel />
      <ResultsDisplay @item-selected="showItemDetails" />
    </div>

    <!-- Modal-fönstret för att visa detaljer. Den ligger i DOM:en men är bara synlig när isModalOpen är true. -->
    <ItemDetailModal
      v-model:isOpen="isModalOpen"
      :item="selectedItem"
      :data-type="dataType"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useHead } from '@unhead/vue';
import { storeToRefs } from 'pinia'; // KORRIGERING: Importera storeToRefs
import { useExplorerStore } from '../../entities/data-explorer/model/explorerStore.js';
import DataFilterPanel from '../../widgets/DataFilterPanel/ui/DataFilterPanel.vue';
import ResultsDisplay from '../../widgets/ResultsDisplay/ui/ResultsDisplay.vue';
import ItemDetailModal from '../../features/item-details/ui/ItemDetailModal.vue';

// --- SEO & METADATA ---
useHead({
  title: 'Component Database Explorer | Engrove Audio Toolkit',
  meta: [
    { 
      name: 'description', 
      content: 'Search and filter a comprehensive database of tonearms and phono cartridges. Find specifications, compliance data, effective mass, and more.' 
    },
    { property: 'og:title', content: 'Component Database Explorer | Engrove Audio Toolkit' },
    { property: 'og:description', content: 'Search and filter a comprehensive database of tonearms and phono cartridges.' },
  ],
});


// --- STORE INTEGRATION ---
const store = useExplorerStore();
// KORRIGERING: Använd storeToRefs för att extrahera reaktiva variabler.
// Detta säkerställer att komponenten uppdateras när värdena i storen ändras.
const { isLoading, error, dataType } = storeToRefs(store);


// --- MODAL STATE & LOGIC ---
const isModalOpen = ref(false);
const selectedItem = ref(null);

/**
 * Funktion som anropas när en rad i tabellen klickas.
 * Den sätter det valda objektet och öppnar modal-fönstret.
 * @param {Object} item - Dataobjektet för den klickade raden.
 */
function showItemDetails(item) {
  selectedItem.value = item;
  isModalOpen.value = true;
}


// --- LIFECYCLE HOOKS ---
onMounted(() => {
  // Anropa initialize-funktionen från storen för att starta datainhämtningen.
  store.initialize();
});
</script>

<style scoped>
.page-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
}

.page-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-border-primary);
  padding-bottom: 1rem;
}

.page-header h1 {
  font-size: var(--font-size-h1);
  color: var(--color-text-high-emphasis);
  margin: 0;
}

.page-description {
  margin-top: 0.5rem;
  margin-bottom: 0;
  color: var(--color-text-medium-emphasis);
  max-width: 80ch;
}

.explorer-layout {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  gap: 2rem;
  align-items: flex-start;
}

.status-container {
  padding: 4rem 2rem;
  text-align: center;
  background-color: var(--color-surface-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: 12px;
}

.status-container.error {
  background-color: var(--color-status-error);
  color: var(--color-text-high-emphasis);
  border-color: var(--color-status-error);
}

.status-container p {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-medium);
}

/* Responsivitet */
@media (max-width: 900px) {
  .explorer-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
    .page-container {
        padding: 1rem;
    }
}
</style>
<!-- src/pages/data-explorer/DataExplorerPage.vue -->
