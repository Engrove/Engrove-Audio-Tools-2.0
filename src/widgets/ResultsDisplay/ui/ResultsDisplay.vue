<!-- src/widgets/ResultsDisplay/ui/ResultsDisplay.vue -->
<!--
  Historik:
  - 2024-08-04: (UPPDRAG 20) Uppdaterad för att peka på de nya `_name`-fälten för tabellvisning.
  - 2024-08-04: (UPPDRAG 22) Helt refaktorerad för att ta bort lokal logik för tabell-headers och istället konsumera dem från storen.
-->
<!--
  Viktiga implementerade regler:
  - Fullständig kod, alltid: Filen är komplett.
  - Obligatorisk Refaktorisering: Lokal UI-logik (headers) har tagits bort. Komponenten är nu en "dummare" presentationskomponent.
  - Alter Ego-granskning: Verifierat att komponenten korrekt binder till de nya centraliserade getters och actions från storen.
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
        <h3>Found {{ totalResultsCount }} {{ dataType === 'cartridges' ? 'cartridges' : 'tonearms' }}</h3>
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

      <!-- Resultattabell som styrs från storen -->
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
import { storeToRefs } from 'pinia';
import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore.js';
import BaseTable from '@/shared/ui/BaseTable.vue';
import BaseButton from '@/shared/ui/BaseButton.vue';

// --- PROPS & EMITS ---
const emit = defineEmits(['item-selected']);

// --- STORE INTEGRATION ---
const store = useExplorerStore();

// Destrukturera actions direkt från storen.
const { setSortKey, nextPage, prevPage, exportToCSV } = store;

// Destrukturera state och getters med storeToRefs för att behålla reaktiviteten.
const {
  dataType,
  searchTerm,
  categoryFilters,
  numericFilters,
  totalResultsCount,
  paginatedResults,
  currentPage,
  sortKey,
  sortOrder,
  totalPages,
  currentHeaders, // NY: Importerad från store
} = storeToRefs(store);


// --- COMPUTED PROPERTIES ---

// BORTTAGEN: Den lokala computed propertyn `currentHeaders` har raderats.
// Logiken finns nu centraliserad i explorerStore.

// Avgör om filterpanelen är i sitt "ursprungliga" tillstånd.
const isPristine = computed(() => {
  const isSearchTermEmpty = searchTerm.value === '';
  const areCategoriesEmpty = Object.values(categoryFilters.value).every(v => v === undefined || v === '');
  const areNumericsEmpty = Object.values(numericFilters.value).every(v => v.min === null && v.max === null);

  // Pristine är när INGEN sökning har gjorts OCH inga resultat finns.
  // Detta förhindrar att platshållaren visas när man återställer filter men det fortfarande finns resultat.
  return totalResultsCount.value === 0 && isSearchTermEmpty && areCategoriesEmpty && areNumericsEmpty;
});

// Beräkningar för paginering
const canGoPrev = computed(() => currentPage.value > 1);
const canGoNext = computed(() => currentPage.value < totalPages.value);

</script>

<style scoped>
.results-area {
  min-height: 500px; /* Förhindrar layout-hopp vid laddning */
  overflow-x: auto; /* Fångar upp tabellens bredd och förhindrar att den spräcker sidlayouten. */
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
  /* Gör texten okänslig för markering för att undvika textval vid dubbelklick. */
  user-select: none;
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
  user-select: none;
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

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR KOMPAKT LÄGE                                         */
/* ========================================================================== */
:global(.compact-theme) .results-header {
  margin-bottom: 1rem;
}

:global(.compact-theme) .pagination-controls {
  margin-bottom: 1rem;
}

:global(.compact-theme) .pagination-controls.bottom {
  margin-top: 1rem;
}
</style>
<!-- src/widgets/ResultsDisplay/ui/ResultsDisplay.vue -->
