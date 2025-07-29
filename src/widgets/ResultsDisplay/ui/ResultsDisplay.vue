<!-- src/widgets/ResultsDisplay/ui/ResultsDisplay.vue -->
<!--
  Denna widget-komponent ansvarar för att rendera hela resultatsektionen
  i Data Explorer, inklusive rubrik, tabell och pagineringskontroller.
  Den hämtar all sin data från explorerStore och använder Base-komponenter
  för att bygga sitt gränssnitt.
-->
<template>
  <main class="results-area">
    <!-- Platshållare när inga filter har applicerats -->
    <div v-if="isPristine" class="results-placeholder">
      <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><path d="M20 17.58A5 5 0 0 0 15 8l-6.4 6.4a5 5 0 1 0 7.8 7.8L20 17.58z"></path></svg>
      <p>Use the filters to begin your search.</p>
    </div>

    <!-- Huvudinnehållet när filter är aktiva eller sökning gjorts -->
    <div v-else>
      <div class="results-header">
        <h3>Found {{ totalResultsCount }} {{ dataType }}</h3>
        <BaseButton 
          variant="primary"
          @click="exportToCSV" 
          :disabled="totalResultsCount === 0"
        >
          Download CSV
        </BaseButton>
      </div>

      <!-- Paginering (topp) -->
      <div v-if="totalPages > 1" class="pagination-controls">
        <BaseButton variant="secondary" @click="prevPage" :disabled="!canGoPrev">‹ Prev</BaseButton>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <BaseButton variant="secondary" @click="nextPage" :disabled="!canGoNext">Next ›</BaseButton>
      </div>

      <!-- Resultattabell -->
      <BaseTable
        :items="paginatedResults"
        :headers="currentHeaders"
        :sort-key="sortKey"
        :sort-order="sortOrder"
        @sort="setSortKey"
        @row-click="emit('item-selected', $event)"
      />

      <!-- Paginering (botten) -->
      <div v-if="totalPages > 1" class="pagination-controls bottom">
        <BaseButton variant="secondary" @click="prevPage" :disabled="!canGoPrev">‹ Prev</BaseButton>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <BaseButton variant="secondary" @click="nextPage" :disabled="!canGoNext">Next ›</BaseButton>
      </div>
    </div>
  </main>
</template>

<script setup>
import { computed } from 'vue';
import { useExplorerStore } from '../../../entities/data-explorer/model/explorerStore.js';
import BaseTable from '../../../shared/ui/BaseTable.vue';
import BaseButton from '../../../shared/ui/BaseButton.vue';

// --- PROPS & EMITS ---
const emit = defineEmits(['item-selected']);

// --- STORE INTEGRATION ---
const store = useExplorerStore();
const {
  dataType,
  searchTerm,
  categoryFilters,
  numericFilters,
  totalResultsCount,
  paginatedResults,
  currentPage,
  itemsPerPage,
  sortKey,
  sortOrder,
  setSortKey,
  nextPage,
  prevPage,
  exportToCSV
} = store;


// --- COMPUTED PROPERTIES ---

// Headers för tabellen, baserat på vald datatyp.
const currentHeaders = computed(() => {
  if (dataType.value === 'cartridges') {
    return [
      { key: 'manufacturer', label: 'Manufacturer', sortable: true },
      { key: 'model', label: 'Model', sortable: true },
      { key: 'type_name', label: 'Type', sortable: true },
      { key: 'cu_dynamic_10hz', label: 'Compliance @ 10Hz', sortable: true },
      { key: 'weight_g', label: 'Weight (g)', sortable: true },
      { key: 'stylus_family_name', label: 'Stylus', sortable: true }
    ];
  } else { // tonearms
    return [
      { key: 'manufacturer', label: 'Manufacturer', sortable: true },
      { key: 'model', label: 'Model', sortable: true },
      { key: 'effective_mass_g', label: 'Effective Mass (g)', sortable: true },
      { key: 'effective_length_mm', label: 'Length (mm)', sortable: true },
      { key: 'bearing_type_name', label: 'Bearing', sortable: true },
      { key: 'arm_shape_name', label: 'Shape', sortable: true }
    ];
  }
});

// Avgör om filterpanelen är i sitt "ursprungliga" tillstånd.
const isPristine = computed(() => {
  return totalResultsCount.value === 0 &&
         searchTerm.value === '' &&
         Object.values(categoryFilters.value).every(v => v === undefined) &&
         Object.values(numericFilters.value).every(v => v.min === null && v.max === null);
});

// Beräkningar för paginering
const totalPages = computed(() => Math.ceil(totalResultsCount.value / itemsPerPage.value));
const canGoPrev = computed(() => currentPage.value > 1);
const canGoNext = computed(() => currentPage.value < totalPages.value);

</script>

<style scoped>
.results-area {
  min-height: 500px; /* Förhindrar layout-hopp vid laddning */
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.results-header h3 {
  margin: 0;
  color: var(--color-text-high-emphasis);
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.pagination-controls.bottom {
    margin-top: 1.5rem;
    margin-bottom: 0;
}

.pagination-controls span {
  font-size: var(--font-size-label);
  color: var(--color-text-medium-emphasis);
  font-weight: var(--font-weight-medium);
  font-family: var(--font-family-monospace);
}

.results-placeholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 400px;
  border: 2px dashed var(--color-border-primary);
  border-radius: 12px;
  color: var(--color-text-low-emphasis);
  text-align: center;
}

.results-placeholder svg {
  margin-bottom: 1rem;
  color: var(--color-text-low-emphasis);
  opacity: 0.5;
}

.results-placeholder p {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-medium);
  margin: 0;
}
</style>
<!-- src/widgets/ResultsDisplay/ui/ResultsDisplay.vue -->
