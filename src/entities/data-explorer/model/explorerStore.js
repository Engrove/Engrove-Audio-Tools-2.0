<!-- src/widgets/DataFilterPanel/ui/DataFilterPanel.vue -->
<template>
  <aside class="data-filter-panel">
    <div class="filter-panel-header">
      <h2 class="filter-panel-title">Filters</h2>
      <BaseButton 
        @click="explorerStore.resetFilters" 
        variant="secondary" 
        size="small"
        :disabled="!explorerStore.hasActiveFilters"
      >
        Reset All
      </BaseButton>
    </div>

    <div class="filter-controls">
      <!-- General Text Search -->
      <BaseInput
        v-model="explorerStore.activeFilters.searchQuery"
        label="Search Model"
        placeholder="e.g. DL-103, RB300..."
      />
      
      <!-- Dynamic Filters from Map -->
      <div v-for="filter in explorerStore.filters" :key="filter.key" class="filter-group">
        
        <!-- Render Multi-Select for specified keys -->
        <BaseMultiSelect
          v-if="multiSelectFilters.includes(filter.key)"
          :label="filter.label"
          :options="filter.options"
          v-model="explorerStore.activeFilters[filter.key]"
        />

        <!-- Render regular Select for other keys -->
        <BaseSelect
          v-else
          :label="filter.label"
          :options="filter.options"
          v-model="explorerStore.activeFilters[filter.key]"
        />

      </div>
    </div>
  </aside>
</template>

<script setup>
// =============================================
// File history
// =============================================
// 2025-08-04: Updated by Frankensteen for Steg 23.
//             - Imported and implemented the new `BaseMultiSelect.vue` component.
//             - Replaced `BaseSelect` for 'manufacturer' and 'tags' with `BaseMultiSelect`.
//             - `v-model` is now correctly bound to array properties in the explorerStore.
//             - Added a simple array `multiSelectFilters` to control which filters use the new component.
//

// =============================================
// Instruktioner vid skapande av fil
// =============================================
// Kärndirektiv: Fullständig kod, alltid. Inga genvägar.
// Principen "Explicit Alltid": Villkorlig rendering av filtertyper är explicit.
// API-kontraktsverifiering: Kontraktet med explorerStore (förväntar sig arrayer för vissa filter) och BaseMultiSelect (v-model) är uppfyllt.
// Red Team Alter Ego-granskning: Panelen är nu mer flexibel och kan hantera olika filtertyper dynamiskt.
//

import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore.js';
import BaseInput from '@/shared/ui/BaseInput.vue';
import BaseSelect from '@/shared/ui/BaseSelect.vue';
import BaseButton from '@/shared/ui/BaseButton.vue';
import BaseMultiSelect from '@/shared/ui/BaseMultiSelect.vue';

const explorerStore = useExplorerStore();

// Define which filters should use the new multi-select component.
// This makes it easy to add more multi-select filters in the future.
const multiSelectFilters = ['manufacturer', 'tags'];

</script>

<style scoped>
.data-filter-panel {
  background-color: var(--surface-secondary);
  border-radius: var(--border-radius-large);
  padding: var(--spacing-5);
  height: 100%;
  overflow-y: auto;
}

.filter-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-primary);
  padding-bottom: var(--spacing-4);
  margin-bottom: var(--spacing-5);
}

.filter-panel-title {
  font-size: var(--font-size-h2);
  color: var(--text-high-emphasis);
  font-weight: var(--font-weight-bold);
}

.filter-controls {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-5);
}
</style>
<!-- src/widgets/DataFilterPanel/ui/DataFilterPanel.vue -->
```---
**Fil 3/3 Sista**
```javascript
// src/entities/data-explorer/model/explorerStore.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchExplorerData } from '../api/fetchExplorerData';

// Helper function to create the initial state for filters
const createInitialFiltersState = () => ({
  searchQuery: '',
  type: 'all',
  manufacturer: [], // Changed from string to array
  tags: [],         // Changed from string to array
});

export const useExplorerStore = defineStore('explorer', () => {
  // =============================================
  // File history
  // =============================================
  // 2025-08-04: Updated by Frankensteen for Steg 23.
  //             - Changed `activeFilters.manufacturer` and `activeFilters.tags` to handle arrays for multi-select.
  //             - Updated `resetFilters` to reset these to empty arrays.
  //             - Modified the filtering logic in `filteredAndSortedResults` to handle both string and array filter values.
  //             - Added specific logic for `tags` to perform an "any-to-any" array match.
  //

  // =============================================
  // Instruktioner vid skapande av fil
  // =============================================
  // Kärndirektiv: Fullständig kod, alltid. Inga genvägar.
  // Principen "Explicit Alltid": Filterlogiken kollar explicit om filtervärdet är en array.
  // API-kontraktsverifiering: Storen exponerar nu arrayer för de filter som förväntar sig det.
  // Red Team Alter Ego-granskning: Filterlogiken är nu mer robust och generell.
  // Obligatorisk Refaktorisering: Logiken är centraliserad och kommenterad.
  //

  // =============================================
  // State
  // =============================================
  const allItems = ref([]);
  const filters = ref([]);
  const translations = ref({});
  const isLoading = ref(true);
  const error = ref(null);
  
  const activeFilters = ref(createInitialFiltersState());

  // =============================================
  // Getters & Computed Properties
  // =============================================
  const hasActiveFilters = computed(() => {
    const initial = createInitialFiltersState();
    return Object.keys(activeFilters.value).some(key => {
      if (Array.isArray(activeFilters.value[key])) {
        return activeFilters.value[key].length > 0;
      }
      return activeFilters.value[key] !== initial[key];
    });
  });
  
  const filteredAndSortedResults = computed(() => {
    if (isLoading.value) return [];
    
    let results = [...allItems.value];

    // Apply active filters
    results = results.filter(item => {
      // 1. Free text search on model and manufacturer
      if (activeFilters.value.searchQuery) {
        const query = activeFilters.value.searchQuery.toLowerCase();
        const inModel = item.model?.toLowerCase().includes(query);
        const inManufacturer = item.manufacturer?.toLowerCase().includes(query);
        if (!inModel && !inManufacturer) return false;
      }

      // 2. Dynamic filters from the panel
      for (const key in activeFilters.value) {
        if (key === 'searchQuery') continue; // Already handled

        const filterValue = activeFilters.value[key];

        // Skip if filter is not set (for strings, arrays, or 'all')
        if (filterValue === '' || filterValue === 'all' || (Array.isArray(filterValue) && filterValue.length === 0)) {
          continue;
        }

        const itemValue = item[key];
        
        // --- NEW LOGIC: Handle Array-based filters ---
        if (Array.isArray(filterValue)) {
          // Special case for 'tags' where both item and filter can be arrays
          if (key === 'tags' && Array.isArray(itemValue)) {
            // "Any-to-any" match: return true if any filter tag is in the item's tags
            if (!filterValue.some(tag => itemValue.includes(tag))) {
              return false;
            }
          } 
          // Standard case for multi-select: check if item's value is in the selected array
          else if (!filterValue.includes(itemValue)) {
            return false;
          }
        } 
        // --- LEGACY LOGIC: Handle String-based filters ---
        else if (itemValue !== filterValue) {
          return false;
        }
      }

      return true;
    });

    // Default sort: by manufacturer then model
    results.sort((a, b) => {
      const manufacturerA = a.manufacturer || '';
      const manufacturerB = b.manufacturer || '';
      const modelA = a.model || '';
      const modelB = b.model || '';

      if (manufacturerA < manufacturerB) return -1;
      if (manufacturerA > manufacturerB) return 1;
      if (modelA < modelB) return -1;
      if (modelA > modelB) return 1;
      return 0;
    });

    return results;
  });

  // =============================================
  // Actions
  // =============================================
  async function initialize() {
    try {
      isLoading.value = true;
      const data = await fetchExplorerData();
      allItems.value = data.allItems;
      filters.value = data.filters;
      translations.value = data.translations;
      error.value = null;
    } catch (e) {
      console.error("Failed to initialize explorer store:", e);
      error.value = "Could not load data. Please try again later.";
      allItems.value = [];
    } finally {
      isLoading.value = false;
    }
  }

  function resetFilters() {
    activeFilters.value = createInitialFiltersState();
  }

  return {
    // State
    allItems,
    filters,
    translations,
    isLoading,
    error,
    activeFilters,
    // Getters
    filteredAndSortedResults,
    hasActiveFilters,
    // Actions
    initialize,
    resetFilters,
  };
});
// src/entities/data-explorer/model/explorerStore.js
