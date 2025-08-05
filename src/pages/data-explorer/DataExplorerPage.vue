<!-- src/pages/data-explorer/DataExplorerPage.vue -->
<template>
  <div class="data-explorer-page">
    <DataFilterPanel />
    <ResultsDisplay
      :items="explorerStore.filteredAndSortedResults"
      :is-loading="explorerStore.isLoading"
      @row-click="handleRowClick"
      @sort="handleSort"
      :sort-key="sortKey"
      :sort-order="sortOrder"
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
    <ComparisonTray @compare="showComparisonModal = true" />
    <!-- Placeholder for the final component -->
    <!-- <ComparisonModal :show="showComparisonModal" @close="showComparisonModal = false" /> -->
  </div>
</template>

<script setup>
// =============================================
// File history
// =============================================
// 2025-08-04: Modified by Frankensteen for Steg 23, Fas 3.
//             - Integrated `comparisonStore` and `ComparisonTray`.
//             - Implemented the logic to pass selection props and handle events from `BaseTable`.
//             - Added logic for "select all visible" functionality.
//             - Now acts as the central conductor for all explorer interactions.
//

// =============================================
// Instruktioner vid skapande av fil
// =============================================
// Kärndirektiv: Fullständig kod, alltid. Inga genvägar.
// Principen "Explicit Alltid": Props till `ResultsDisplay` är alla explicit bundna.
// API-kontraktsverifiering: Uppfyller det nya, utökade kontraktet för `ResultsDisplay`/`BaseTable`.
// Red Team Alter Ego-granskning: Logiken för "select all" hanterar både val och av-val korrekt.
//

import { ref, onMounted, computed } from 'vue';
import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore.js';
import { useComparisonStore } from '@/entities/comparison/model/comparisonStore.js';
import DataFilterPanel from '@/widgets/DataFilterPanel/ui/DataFilterPanel.vue';
import ResultsDisplay from '@/widgets/ResultsDisplay/ui/ResultsDisplay.vue';
import ItemDetailModal from '@/features/item-details/ui/ItemDetailModal.vue';
import ComparisonTray from '@/widgets/ComparisonTray/ui/ComparisonTray.vue';
// import ComparisonModal from '@/features/comparison-modal/ui/ComparisonModal.vue';

// =============================================
// Store Initialization
// =============================================
const explorerStore = useExplorerStore();
const comparisonStore = useComparisonStore();

// =============================================
// Local State
// =============================================
const selectedItem = ref(null);
const isModalVisible = ref(false);
const showComparisonModal = ref(false); // For the next step
const sortKey = ref('manufacturer');
const sortOrder = ref('asc'); // 'asc' or 'desc'

// =============================================
// Lifecycle Hooks
// =============================================
onMounted(() => {
  if (explorerStore.allItems.length === 0) {
    explorerStore.initialize();
  }
});

// =============================================
// Computed Properties for Selection
// =============================================
const isItemSelected = (item) => {
  return comparisonStore.isSelected(item.id);
};

const allVisibleSelected = computed(() => {
  const visibleItems = explorerStore.filteredAndSortedResults;
  if (visibleItems.length === 0) {
    return false;
  }
  return visibleItems.every(item => comparisonStore.isSelected(item.id));
});

// =============================================
// Event Handlers
// =============================================
function handleRowClick(item) {
  selectedItem.value = item;
  isModalVisible.value = true;
}

function handleSort(key) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
}

function handleToggleItem(item) {
  comparisonStore.toggleItem(item.id);
}

function handleSelectAllVisible() {
  const visibleItemIds = explorerStore.filteredAndSortedResults.map(item => item.id);
  
  if (allVisibleSelected.value) {
    // If all are selected, deselect all of them
    visibleItemIds.forEach(id => {
      if (comparisonStore.isSelected(id)) {
        comparisonStore.toggleItem(id);
      }
    });
  } else {
    // If not all are selected, select all available ones
    visibleItemIds.forEach(id => {
      if (!comparisonStore.isSelected(id) && !comparisonStore.isLimitReached) {
        comparisonStore.toggleItem(id);
      }
    });
  }
}

</script>

<style scoped>
.data-explorer-page {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: var(--spacing-5);
  padding: var(--spacing-5);
  height: calc(100vh - var(--header-height)); /* Full height minus header */
  overflow: hidden; /* Prevent body scroll */
}

@media (max-width: 1024px) {
  .data-explorer-page {
    grid-template-columns: 250px 1fr;
  }
}

@media (max-width: 768px) {
  .data-explorer-page {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr; /* Filters on top, results below */
    height: auto;
    overflow-y: auto;
  }
}
</style>
<!-- src/pages/data-explorer/DataExplorerPage.vue -->
