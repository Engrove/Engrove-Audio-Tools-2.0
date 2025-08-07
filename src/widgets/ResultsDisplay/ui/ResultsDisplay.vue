<!-- src/widgets/ResultsDisplay/ui/ResultsDisplay.vue -->
<!--
  Historik:
  - 2025-08-07: (Frankensteen) Slutfört integrationen för jämförelsefunktionen. Komponenten agerar nu som en transparent mellanhand för all urvalslogik genom att acceptera och skicka vidare nya props och emits.
  - 2025-08-05: (Fix av Frankensteen) Total ombyggnad till en ren presentationskomponent. Alla direkta store-beroenden har tagits bort.
  - 2024-08-04: (UPPDRAG 22) Helt refaktorerad för att ta bort lokal logik för tabell-headers.
  - 2024-08-04: (UPPDRAG 20) Uppdaterad för att peka på de nya `_name`-fälten.
-->
<!--
  Viktiga implementerade regler:
  - API-kontraktsverifiering: Det utökade kontraktet med nya props och emits är nu fullständigt implementerat.
  - Obligatorisk Refaktorisering: Komponenten bibehåller sin status som en "dum" presentationskomponent.
-->
<template>
  <div class="results-display-wrapper">
    <header class="results-header">
      <div class="results-summary">
        <h2>Found {{ totalResults }} {{ dataType }}</h2>
        <p v-if="totalPages > 1">Showing page {{ currentPage }} of {{ totalPages }}</p>
      </div>
      <BaseButton 
        variant="secondary" 
        @click="$emit('export-csv')" 
        :disabled="items.length === 0"
        title="Export current results to CSV file"
      >
        Export CSV
      </BaseButton>
    </header>

    <div class="table-wrapper">
      <BaseTable
        :items="items"
        :headers="headers"
        :sortKey="sortKey"
        :sortOrder="sortOrder"
        :showSelection="showSelection"
        :isItemSelected="isItemSelected"
        :selectionLimitReached="selectionLimitReached"
        :allVisibleItemsSelected="allVisibleItemsSelected"
        @row-click="$emit('row-click', $event)"
        @sort="$emit('sort', $event)"
        @toggle-item-selection="$emit('toggle-item-selection', $event)"
        @toggle-select-all-visible="$emit('toggle-select-all-visible', $event)"
      />
    </div>

    <footer v-if="totalPages > 1" class="results-footer">
      <BaseButton @click="$emit('page-change', currentPage - 1)" :disabled="currentPage <= 1">
        Previous
      </BaseButton>
      <span>Page {{ currentPage }} / {{ totalPages }}</span>
      <BaseButton @click="$emit('page-change', currentPage + 1)" :disabled="currentPage >= totalPages">
        Next
      </BaseButton>
    </footer>
  </div>
</template>

<script setup>
import BaseTable from '@/shared/ui/BaseTable.vue';
import BaseButton from '@/shared/ui/BaseButton.vue';

// PROPS & EMITS ---
defineProps({
  items: Array,
  headers: Array,
  dataType: String,
  totalResults: Number,
  totalPages: Number,
  currentPage: Number,
  sortKey: String,
  sortOrder: String,
  // Props för val-funktionalitet
  showSelection: {
    type: Boolean,
    default: false,
  },
  isItemSelected: {
    type: Function,
    default: () => false,
  },
  selectionLimitReached: {
    type: Boolean,
    default: false,
  },
  allVisibleItemsSelected: {
    type: Boolean,
    default: false,
  },
});

defineEmits([
    'row-click', 
    'sort', 
    'page-change', 
    'export-csv',
    'toggle-item-selection',
    'toggle-select-all-visible'
]);
</script>

<style scoped>
.results-display-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0; /* Förhindrar layout-hopp vid laddning */
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-4);
  padding-bottom: var(--spacing-4);
  border-bottom: 1px solid var(--border-primary);
  flex-shrink: 0;
}

.results-summary h2 {
  font-size: var(--font-size-h2);
  color: var(--text-high-emphasis);
  margin: 0;
}

.results-summary p {
  font-size: var(--font-size-body);
  color: var(--text-medium-emphasis);
  margin: 0;
  margin-top: var(--spacing-1);
}

.table-wrapper {
  flex-grow: 1;
  overflow-y: auto; /* Fångar upp tabellens bredd och förhindrar att den spräcker sidlayouten. */
}

.results-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-4);
  margin-top: var(--spacing-4);
  border-top: 1px solid var(--border-primary);
  user-select: none; /* Gör texten okänslig för markering för att undvika textval vid dubbelklick. */
  flex-shrink: 0;
}

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR KOMPAKT LÄGE                                         */
/* ========================================================================== */
.compact-theme .results-header {
  margin-bottom: var(--spacing-3);
  padding-bottom: var(--spacing-3);
}

.compact-theme .results-footer {
  margin-top: var(--spacing-3);
  padding-top: var(--spacing-3);
}
</style>
<!-- src/widgets/ResultsDisplay/ui/ResultsDisplay.vue -->
