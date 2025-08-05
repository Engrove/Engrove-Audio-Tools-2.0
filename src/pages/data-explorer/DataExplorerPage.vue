<!-- src/pages/data-explorer/DataExplorerPage.vue -->
<template>
  <div class="data-explorer-container">
    <!-- 1. Laddningsläge -->
    <div v-if="isLoading" class="placeholder-wrapper">
      <p>Loading data...</p>
    </div>
    
    <!-- 2. Felläge -->
    <div v-else-if="error" class="placeholder-wrapper error">
      <p>Failed to load data.</p>
      <p class="error-details">{{ error }}</p>
      <BaseButton @click="explorerStore.initializeData()">Try Again</BaseButton>
    </div>

    <!-- 3. Normalläge -->
    <div v-else class="data-explorer-page">
      <DataFilterPanel />

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
// * 2025-08-05: (CODE RED FIX by Frankensteen) Lade till ett `v-else-if="error"` block för att visa ett felmeddelande om dataladdningen misslyckas. Detta gör UI:t robust och informativt.
// * 2025-08-05: Tog bort deadlock-villkor från onMounted.
//
// === TILLÄMPADE REGLER (Frankensteen v3.7) ===
// - "Help me God"-protokollet har använts för att hitta grundorsaken.
// - Felresiliens: UI:t hanterar nu tre tillstånd korrekt: laddning, fel och framgång.

import { ref, onMounted, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore.js';
import { useComparisonStore } from '@/entities/comparison/model/comparisonStore.js';
import DataFilterPanel from '@/widgets/DataFilterPanel/ui/DataFilterPanel.vue';
import ResultsDisplay from '@/widgets/ResultsDisplay/ui/ResultsDisplay.vue';
import ItemDetailModal from '@/features/item-details/ui/ItemDetailModal.vue';
import ComparisonModal from '@/features/comparison-modal/ui/ComparisonModal.vue';
import BaseButton from '@/shared/ui/BaseButton.vue';

const explorerStore = useExplorerStore();
const comparisonStore = useComparisonStore();

const { 
  isLoading, 
  error,
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

const selectedItem = ref(null);
const isModalVisible = ref(false);
const showComparisonModal = ref(false);

onMounted(() => {
  explorerStore.initializeData();
});

const isItemSelected = (item) => {
  return comparisonStore.isSelected(item.id);
};

const allVisibleSelected = computed(() => {
  if (paginatedResults.value.length === 0) {
    return false;
  }
  return paginatedResults.value.every(item => comparisonStore.isSelected(item.id));
});

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

.placeholder-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: var(--font-size-h3);
  color: var(--color-text-medium-emphasis);
  text-align: center;
}

.placeholder-wrapper.error {
  color: var(--color-text-danger);
}

.error-details {
  font-size: var(--font-size-body);
  color: var(--color-text-low-emphasis);
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
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
