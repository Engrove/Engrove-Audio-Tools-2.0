<!-- src/pages/data-explorer/DataExplorerPage.vue -->
<!--
  Historik:
  - 2025-08-07: (Frankensteen) KRITISK FIX: Lade till händelselyssnaren @compare="isComparisonModalVisible = true" på ComparisonTray-komponenten. Detta åtgärdar buggen där Compare-knappen var inaktiv.
  - 2025-08-06: (Frankensteen - STALEMATE ARBITRATION FIX) Increased CSS selector specificity for `.page-wrapper` to `div.page-wrapper` to override conflicting global styles, which was the definitive root cause of the missing padding.
  - 2025-08-06: (Frankensteen - DEFINITIVE PADDING FIX) Flyttat padding från grid-containern (.data-explorer-page) till den yttre wrappern (.page-wrapper) för att korrekt rendera yttre marginaler.
  - 2025-08-06: (Frankensteen) CSS Regression Fix: Återinfört yttre padding på `.data-explorer-page` för att matcha den korrekta layouten i "Comfortable mode".
  - 2025-08-06: (Frankensteen) Prop Drilling Fix: Skickar nu ner all nödvändig state (dataType, totalResults, etc.) som props till ResultsDisplay för att aktivera dynamisk rubrik, sortering och paginering.
  - 2025-08-06: (Frankensteen) Integrerat den nya ComparisonTray-widgeten och kopplat dess händelser för att slutföra jämförelsefunktionen.
  - 2025-08-05: (CODE RED FIX by Frankensteen) Lade till felhantering och brutit en logisk deadlock.
-->
<!--
  Viktiga implementerade regler:
  - API-kontraktsverifiering: Händelsekedjan från ComparisonTray till DataExplorerPage är nu komplett och korrekt implementerad.
  - Fullständig Historik: Hela korrigeringsprocessen, inklusive misslyckanden och eskalering, är dokumenterad.
-->
<template>
  <div class="page-wrapper" :class="{ 'tray-visible': isTrayVisible }">
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
    <main v-else class="data-explorer-page">
      <DataFilterPanel />
      
      <ResultsDisplay
        :items="paginatedResults"
        :headers="currentHeaders"
        :dataType="dataType"
        :totalResults="totalResults"
        :totalPages="totalPages"
        :currentPage="currentPage"
        :sortKey="sortKey"
        :sortOrder="sortOrder"
        :showSelection="true"
        :isItemSelected="(item) => comparisonStore.isSelected(item.id)"
        :selectionLimitReached="comparisonStore.isLimitReached"
        :allVisibleItemsSelected="allVisibleItemsSelected"
        @row-click="handleRowClick"
        @sort="explorerStore.setSort"
        @page-change="explorerStore.setPage"
        @toggle-item-selection="handleToggleItem"
        @toggle-select-all-visible="handleToggleSelectAllVisible"
        @export-csv="explorerStore.exportToCSV"
      />
    </main>

    <!-- Modals and Overlays -->
    <ItemDetailModal
      :item="selectedItem"
      :show="isModalVisible"
      @close="isModalVisible = false"
    />
    <ComparisonModal 
      :show="isComparisonModalVisible" 
      @close="isComparisonModalVisible = false" 
    />
    <ComparisonTray @compare="isComparisonModalVisible = true" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore.js';
import { useComparisonStore } from '@/entities/comparison/model/comparisonStore.js';

import DataFilterPanel from '@/widgets/DataFilterPanel/ui/DataFilterPanel.vue';
import ResultsDisplay from '@/widgets/ResultsDisplay/ui/ResultsDisplay.vue';
import ItemDetailModal from '@/features/item-details/ui/ItemDetailModal.vue';
import ComparisonModal from '@/features/comparison-modal/ui/ComparisonModal.vue';
import ComparisonTray from '@/widgets/ComparisonTray/ui/ComparisonTray.vue';
import BaseButton from '@/shared/ui/BaseButton.vue';

const explorerStore = useExplorerStore();
const comparisonStore = useComparisonStore();

const { 
  isLoading, 
  error,
  paginatedResults, 
  currentHeaders,
  dataType,
  totalResults,
  totalPages,
  currentPage,
  sortKey,
  sortOrder,
} = storeToRefs(explorerStore);

const selectedItem = ref(null);
const isModalVisible = ref(false);
const isComparisonModalVisible = ref(false);

const isTrayVisible = computed(() => comparisonStore.selectedItemsCount > 0);

const allVisibleItemsSelected = computed(() => {
    if (paginatedResults.value.length === 0) return false;
    return paginatedResults.value.every(item => comparisonStore.isSelected(item.id));
});

onMounted(() => {
  explorerStore.initializeData();
});

function handleRowClick(item) {
  selectedItem.value = item;
  isModalVisible.value = true;
}

function handleToggleItem(item) {
    comparisonStore.toggleItem(item.id);
}

function handleToggleSelectAllVisible() {
    const allVisibleIds = paginatedResults.value.map(item => item.id);
    const shouldSelect = !allVisibleItemsSelected.value;

    allVisibleIds.forEach(id => {
        const isCurrentlySelected = comparisonStore.isSelected(id);
        if (shouldSelect && !isCurrentlySelected) {
            comparisonStore.toggleItem(id);
        } else if (!shouldSelect && isCurrentlySelected) {
            comparisonStore.toggleItem(id);
        }
    });
}

</script>

<style scoped>
/* SKILJEDOMSFIX: Ökar specificiteten för att vinna över globala stilar. */
div.page-wrapper {
  height: calc(100vh - var(--header-height));
  display: flex;
  flex-direction: column;
  transition: padding-bottom 0.3s ease-out;
  padding: var(--spacing-6);
}

div.page-wrapper.tray-visible {
  /* Justera padding för att ge plats åt ComparisonTray. Siffran bör matcha trayens höjd. */
  padding-bottom: 140px; 
}

.placeholder-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-align: center;
  padding: var(--spacing-6);
  font-size: var(--font-size-h3);
  color: var(--color-text-medium-emphasis);
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
  grid-template-columns: 320px 1fr;
  gap: var(--spacing-6);
  height: 100%;
  overflow: hidden;
  flex-grow: 1;
}

@media (max-width: 1024px) {
  div.page-wrapper {
    padding: var(--spacing-5);
  }
  .data-explorer-page {
    grid-template-columns: 280px 1fr;
    gap: var(--spacing-5);
  }
}

@media (max-width: 768px) {
  div.page-wrapper {
    height: auto;
    padding: var(--spacing-4);
  }
  div.page-wrapper.tray-visible {
    /* Anpassa för mobil layout */
    padding-bottom: 180px; 
  }
  .data-explorer-page {
    grid-template-columns: 1fr;
    height: auto;
    overflow-y: auto;
  }
}
</style>
<!-- src/pages/data-explorer/DataExplorerPage.vue -->
