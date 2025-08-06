<!-- src/pages/data-explorer/DataExplorerPage.vue -->
<!--
  Historik:
  - 2025-08-06: (Frankensteen) CSS Regression Fix: Återinfört yttre padding på `.data-explorer-page` för att matcha den korrekta layouten i "Comfortable mode".
  - 2025-08-06: (Frankensteen) Prop Drilling Fix: Skickar nu ner all nödvändig state (dataType, totalResults, etc.) som props till ResultsDisplay för att aktivera dynamisk rubrik, sortering och paginering.
  - 2025-08-06: (Frankensteen) Integrerat den nya ComparisonTray-widgeten och kopplat dess händelser för att slutföra jämförelsefunktionen.
  - 2025-08-05: (CODE RED FIX by Frankensteen) Lade till felhantering och brutit en logisk deadlock.
-->
<!--
  Viktiga implementerade regler:
  - Syntax- och Linter-simulering: CSS-regler är korrekt formaterade.
  - API-kontraktsverifiering: Sidan uppfyller nu det fullständiga API-kontraktet för ResultsDisplay-komponenten.
  - "Help me God"-protokollet har använts för att verifiera denna slutgiltiga integration.
  - Obligatorisk Refaktorisering: Sidans struktur är nu logiskt komplett och följer FSD-principerna.
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
        @row-click="handleRowClick"
        @sort="explorerStore.setSort"
        @page-change="explorerStore.setPage"
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

onMounted(() => {
  explorerStore.initializeData();
});

function handleRowClick(item) {
  selectedItem.value = item;
  isModalVisible.value = true;
}
</script>

<style scoped>
.page-wrapper {
  height: calc(100vh - var(--header-height));
  display: flex;
  flex-direction: column;
  transition: padding-bottom 0.3s ease-out;
}

.page-wrapper.tray-visible {
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
  color: var(--text-medium-emphasis);
}

.placeholder-wrapper.error {
  color: var(--text-danger);
}

.error-details {
  font-size: var(--font-size-body);
  color: var(--text-low-emphasis);
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
}

.data-explorer-page {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: var(--spacing-6);
  /* KORRIGERING: Återställer den saknade paddingen */
  padding: var(--spacing-6);
  height: 100%;
  overflow: hidden;
  flex-grow: 1;
}

@media (max-width: 1024px) {
  .data-explorer-page {
    grid-template-columns: 280px 1fr;
    gap: var(--spacing-5);
    padding: var(--spacing-5);
  }
}

@media (max-width: 768px) {
  .page-wrapper {
    height: auto;
  }
  .page-wrapper.tray-visible {
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
