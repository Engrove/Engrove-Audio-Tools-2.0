<!-- src/widgets/ResultsDisplay/ui/ResultsDisplay.vue -->
<!--
  Historik:
  - 2025-08-05: (Fix av Frankensteen) Total ombyggnad till en ren presentationskomponent. Alla direkta store-beroenden har tagits bort. Komponenten tar nu emot all data via props och kommunicerar via emits, vilket löser flera API-brott.
  - 2024-08-04: (UPPDRAG 22) Helt refaktorerad för att ta bort lokal logik för tabell-headers och istället konsumera dem från storen.
  - 2024-08-04: (UPPDRAG 20) Uppdaterad för att peka på de nya `_name`-fälten för tabellvisning.
-->
<!--
  Viktiga implementerade regler:
  - Fullständig kod, alltid: Filen är komplett.
  - Obligatorisk Refaktorisering: Komponenten är nu en "dum" presentationskomponent, vilket är en betydande arkitektonisk förbättring.
  - API-kontraktsverifiering: Det nya kontraktet med props och emits är tydligt och robust.
  - Felresiliens: Komponenten är inte längre sårbar för race conditions i storen.
-->
<template>
  <main class="results-area">
    <div class="results-header">
      <h3>Found {{ totalResults }} {{ dataType === 'cartridges' ? 'cartridges' : 'tonearms' }}</h3>
      <!-- Lade till @click-event för CSV-export -->
      <BaseButton 
        variant="primary"
        @click="$emit('export-csv')"
        :disabled="totalResults === 0"
      >
        Download CSV
      </BaseButton>
    </div>

    <!-- Paginering (topp) -->
    <div v-if="totalPages > 1" class="pagination-controls">
      <BaseButton variant="secondary" @click="$emit('page-change', currentPage - 1)" :disabled="currentPage === 1">‹ Prev</BaseButton>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <BaseButton variant="secondary" @click="$emit('page-change', currentPage + 1)" :disabled="currentPage === totalPages">Next ›</BaseButton>
    </div>

    <!-- Resultattabell -->
    <BaseTable
      :items="items"
      :headers="headers"
      :sort-key="sortKey"
      :sort-order="sortOrder"
      @sort="$emit('sort', $event)"
      @row-click="$emit('row-click', $event)"
      :show-selection="showSelection"
      :is-item-selected="isItemSelected"
      :selection-limit-reached="selectionLimitReached"
      :all-visible-items-selected="allVisibleItemsSelected"
      @toggle-item-selection="$emit('toggle-item-selection', $event)"
      @toggle-select-all-visible="$emit('toggle-select-all-visible')"
    />

    <!-- Paginering (botten) -->
    <div v-if="totalPages > 1" class="pagination-controls bottom">
      <BaseButton variant="secondary" @click="$emit('page-change', currentPage - 1)" :disabled="currentPage === 1">‹ Prev</BaseButton>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <BaseButton variant="secondary" @click="$emit('page-change', currentPage + 1)" :disabled="currentPage === totalPages">Next ›</BaseButton>
    </div>
  </main>
</template>

<script setup>
import BaseTable from '@/shared/ui/BaseTable.vue';
import BaseButton from '@/shared/ui/BaseButton.vue';

// --- PROPS & EMITS ---

defineProps({
  items: { type: Array, required: true },
  headers: { type: Array, required: true },
  dataType: { type: String, required: true },
  totalResults: { type: Number, required: true },
  totalPages: { type: Number, required: true },
  currentPage: { type: Number, required: true },
  sortKey: { type: String, required: true },
  sortOrder: { type: String, required: true },
  // Props för val-funktionalitet
  showSelection: { type: Boolean, default: false },
  isItemSelected: { type: Function, default: () => false },
  selectionLimitReached: { type: Boolean, default: false },
  allVisibleItemsSelected: { type: Boolean, default: false },
});

defineEmits([
  'sort',
  'page-change',
  'row-click',
  'export-csv',
  'toggle-item-selection',
  'toggle-select-all-visible'
]);
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
