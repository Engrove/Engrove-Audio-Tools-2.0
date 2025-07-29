// src/entities/data-explorer/model/explorerStore.js
/**
 * Denna fil fungerar som den centrala "fabriken" eller "dirigenten" för
 * Data Explorer-entiteten. Den skapar en Vue 3 composable (`useExplorerStore`)
 * som sammanställer state, API-anrop och ren affärslogik till en
 * sammanhållen och lättanvänd enhet.
 */

import { computed, watch } from 'vue';
import {
  isLoading, error, allPickups, allTonearms, pickupClassifications,
  tonearmClassifications, dataType, searchTerm, categoryFilters,
  numericFilters, sortKey, sortOrder, currentPage, itemsPerPage
} from './state.js';
import { fetchExplorerData } from '../api/fetchExplorerData.js';
import { applyFilters, applySorting } from '../lib/filters.js';

// --- Privata "Lookup Maps" ---
let pickupClassificationMaps = {};
let tonearmClassificationMaps = {};

function createLookupMaps(classifications) {
  const maps = {};
  if (!classifications) return maps;
  for (const key in classifications) {
    const map = new Map();
    if (classifications[key] && classifications[key].categories) {
      for (const category of classifications[key].categories) {
        map.set(category.id, category.name);
      }
    }
    maps[key] = map;
  }
  return maps;
}

/**
 * En Vue 3 composable som tillhandahåller all reaktiv data och alla metoder
 * som behövs för att driva Data Explorer-gränssnittet.
 */
export function useExplorerStore() {
  
  // --- Metoder (Actions) ---

  async function initialize() {
    if (allPickups.value.length > 0) {
      isLoading.value = false;
      return;
    }
    try {
      isLoading.value = true;
      error.value = null;
      const data = await fetchExplorerData();
      
      allPickups.value = data.pickups;
      allTonearms.value = data.tonearms;
      pickupClassifications.value = data.pickupClassifications;
      tonearmClassifications.value = data.tonearmClassifications;

      pickupClassificationMaps = createLookupMaps(data.pickupClassifications);
      tonearmClassificationMaps = createLookupMaps(data.tonearmClassifications);

    } catch (e) {
      error.value = e.message;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Återställer alla filter till sina ursprungliga värden.
   */
  function resetFilters() {
    searchTerm.value = '';
    categoryFilters.value = {};
    numericFilters.value = {};
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';
    currentPage.value = 1;
  }

  /**
   * Sätter vilken typ av data som ska visas och återställer filter.
   * @param {'tonearms' | 'cartridges'} newDataType - Den nya datatypen.
   */
  function setDataType(newDataType) {
    if (dataType.value !== newDataType) {
      dataType.value = newDataType;
      // Återställ alla filter vid byte av datatyp för en ren start.
      resetFilters();
    }
  }

  /**
   * Uppdaterar ett numeriskt filter.
   * @param {string} key - Nyckeln för filtret.
   * @param {{min: number|null, max: number|null}} value - Det nya intervallvärdet.
   */
  function updateNumericFilter(key, value) {
    numericFilters.value[key] = value;
  }


  // --- Beräknade Egenskaper (Computed Properties) ---

  const currentItems = computed(() => {
    return dataType.value === 'tonearms' ? allTonearms.value : allPickups.value;
  });

  const enrichedItems = computed(() => {
    const maps = dataType.value === 'tonearms' ? tonearmClassificationMaps : pickupClassificationMaps;
    
    return currentItems.value.map(item => {
      const enrichedItem = { ...item };
      for (const key in maps) {
        const itemValue = item[key];
        if (itemValue && maps[key] && maps[key].has(itemValue)) {
          enrichedItem[`${key}_name`] = maps[key].get(itemValue);
        } else if (itemValue) {
          enrichedItem[`${key}_name`] = itemValue; // Fallback om id inte finns i map
        }
      }
      return enrichedItem;
    });
  });

  const filteredResults = computed(() => {
    return applyFilters(enrichedItems.value, searchTerm.value, categoryFilters.value, numericFilters.value);
  });
  
  const filteredAndSortedResults = computed(() => {
    return applySorting(filteredResults.value, sortKey.value, sortOrder.value);
  });

  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return filteredAndSortedResults.value.slice(start, end);
  });
  
  watch([searchTerm, categoryFilters, numericFilters], () => {
    if (currentPage.value !== 1) {
      currentPage.value = 1;
    }
  }, { deep: true });

  // --- Publika API:et för storen ---
  return {
    // State
    isLoading,
    error,
    dataType,
    searchTerm,
    categoryFilters,
    numericFilters,
    sortKey,
    sortOrder,
    currentPage,
    itemsPerPage,
    pickupClassifications,
    tonearmClassifications,
    
    // Getters
    paginatedResults,
    totalResultsCount: computed(() => filteredResults.value.length),

    // Actions
    initialize,
    resetFilters,
    setDataType,
    updateNumericFilter,
  };
}
// src/entities/data-explorer/model/explorerStore.js
