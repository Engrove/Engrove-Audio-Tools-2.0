<!-- src/pages/data-explorer/DataExplorerPage.vue -->
<template>
  <div class="data-explorer-container">
    <div v-if="isLoading" class="loading-placeholder">
      <p>Loading data...</p>
    </div>
    <div v-else class="data-explorer-page">
      <DataFilterPanel />

      <!-- Platshållare när inga filter har applicerats -->
      <div v-if="isPristine" class="results-placeholder-wrapper">
        <div class="results-placeholder">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><path d="M20 17.58A5 5 0 0 0 15 8l-6.4 6.4a5 5 0 1 0 7.8 7.8L20 17.58z"></path></svg>
          <p>Use the filters to begin your search.</p>
        </div>
      </div>
      
      <ResultsDisplay
        v-else
        :items="paginatedResults"
        :headers="currentHeaders"
        :data-type="dataType"
        :total-results="totalResults"
        :total-pages="totalPages"
        :current-page="currentPage"
        :sort-key="sortKey"
        :sort-order="sortOrder"
        @sort="explorerStore.setSort"
        @page-change="explorerStore.setPage"
        @row-click="handleRowClick"
        :show-selection="true"
        :is-item-selected="isItemSelected"
        :selection-limit-reached="comparisonStore.isLimitReached"
        :all-visible-items-selected="allVisibleSelected"
        @toggle-item-selection="handleToggleItem"
        @toggle-select-all-visible="handleSelectAllVisible"
      />
      
      <ItemDetailModal
        :item="selectedItem"
        :show="isModalVisible"
        @close="isModalVisible = false"
      />
      <ComparisonModal :show="showComparisonModal" @close="showComparisonModal = false" />
    </div>
  </div>
</template>

<script setup>
// =============================================
// File history
// =============================================
// * 2025-08-05: (CODE RED FIX by Frankensteen) Tog bort det felaktiga `if (isPristine.value)`-villkoret som orsakade en logisk deadlock och hindrade data från att laddas. `initializeData()` anropas nu ovillkorligt.
// * 2025-08-05: (Fix by Frankensteen) Total omstrukturering. Lade till `v-if` på `isLoading` för att definitivt lösa race condition-felet.
//
// === TILLÄMPADE REGLER (Frankensteen v3.7) ===
// - "Help me God"-protokollet har använts för att identifiera och lösa en kritisk logisk deadlock.
// - Felresiliens: Deadlocken är bruten, vilket garanterar att data nu laddas.

import { ref, onMounted, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore.js';
import { useComparisonStore } from '@/entities/comparison/model/comparisonStore.js';
import DataFilterPanel from '@/widgets/DataFilterPanel/ui/DataFilterPanel.vue';
import ResultsDisplay from '@/widgets/ResultsDisplay/ui/ResultsDisplay.vue';
import ItemDetailModal from '@/features/item-details/ui/ItemDetailModal.vue';
import ComparisonModal from '@/features/comparison-modal/ui/ComparisonModal.vue';

// =============================================
// Store Initialization
// =============================================
const explorerStore = useExplorerStore();
const comparisonStore = useComparisonStore();

const { 
  isLoading, 
  dataType,
  paginatedResults, 
  currentHeaders,
  totalResults, 
  totalPages, 
  currentPage, 
  sortKey, 
  sortOrder,
  isPristine
} = storeToRefs(explorerStore);

// =============================================
// Local State
// =============================================
const selectedItem = ref(null);
const isModalVisible = ref(false);
const showComparisonModal = ref(false);

// =============================================
// Lifecycle Hooks
// =============================================
onMounted(() => {
  // KORRIGERING: Det felaktiga villkoret har tagits bort.
  // Anropet MÅSTE ske ovillkorligt för att bryta deadlocken.
  explorerStore.initializeData();
});

// =============================================
// Computed Properties for Selection
// =============================================
const isItemSelected = (item) => {
  return comparisonStore.isSelected(item.id);
};

const allVisibleSelected = computed(() => {
  if (paginatedResults.value.length === 0) {
    return false;
  }
  return paginatedResults.value.every(item => comparisonStore.isSelected(item.id));
});

// =============================================
// Event Handlers
// =============================================
function handleRowClick(item) {
  selectedItem.value = item;
  isModalVisible.value = true;
}

function handleToggleItem(item) {
  comparisonStore.toggleItem(item.id);
}

function handleSelectAllVisible() {
  const visibleItemIds = paginatedResults.value.map(item => item.id);
  
  if (allVisibleSelected.value) {
    visibleItemIds.forEach(id => {
      if (comparisonStore.isSelected(id)) {
        comparisonStore.toggleItem(id);
      }
    });
  } else {
    visibleItemIds.forEach(id => {
      if (!comparisonStore.isSelected(id) && !comparisonStore.isLimitReached) {
        comparisonStore.toggleItem(id);
      }
    });
  }
}
</script>

<style scoped>
.data-explorer-container {
  height: calc(100vh - var(--header-height));
  padding: var(--spacing-5);
  box-sizing: border-box;
}

.loading-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: var(--font-size-h3);
  color: var(--color-text-medium-emphasis);
}

.data-explorer-page {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: var(--spacing-5);
  height: 100%;
  overflow: hidden;
}

.results-placeholder-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.results-placeholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 400px;
  width: 100%;
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


@media (max-width: 1024px) {
  .data-explorer-page {
    grid-template-columns: 250px 1fr;
  }
}

@media (max-width: 768px) {
  .data-explorer-container {
    height: auto;
  }
  .data-explorer-page {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
    height: auto;
    overflow-y: auto;
  }
}
</style>
<!-- src/pages/data-explorer/DataExplorerPage.vue -->
