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
// Dessa skapas en gång när datan laddas för snabb uppslagning av läsbara namn.
let pickupClassificationMaps = {};
let tonearmClassificationMaps = {};

/**
 * Hjälpfunktion för att skapa uppslagstabeller från klassificeringsdata.
 * @param {Object} classifications - Klassificeringsobjektet från JSON.
 * @returns {Object} Ett objekt där nycklarna är klassificerings-ID:n (t.ex. 'compliance_level')
 *                   och värdena är Maps för snabb uppslagning av namn.
 */
function createLookupMaps(classifications) {
  const maps = {};
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

  /**
   * Initialiserar storen genom att hämta all nödvändig data.
   * Denna funktion ska anropas en gång när komponenten monteras.
   */
  async function initialize() {
    // Undvik att hämta data flera gånger om den redan finns.
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

      // Skapa de privata uppslagstabellerna
      pickupClassificationMaps = createLookupMaps(data.pickupClassifications);
      tonearmClassificationMaps = createLookupMaps(data.tonearmClassifications);

    } catch (e) {
      error.value = e.message;
    } finally {
      isLoading.value = false;
    }
  }

  // --- Beräknade Egenskaper (Computed Properties) ---

  // Väljer den aktuella datamängden baserat på `dataType`.
  const currentItems = computed(() => {
    return dataType.value === 'tonearms' ? allTonearms.value : allPickups.value;
  });

  // Berikar den aktuella datamängden med läsbara namn från klassificeringarna.
  const enrichedItems = computed(() => {
    const maps = dataType.value === 'tonearms' ? tonearmClassificationMaps : pickupClassificationMaps;
    
    return currentItems.value.map(item => {
      const enrichedItem = { ...item };
      for (const key in maps) {
        if (item[key] && maps[key].has(item[key])) {
          // Lägg till en ny egenskap med det läsbara namnet.
          enrichedItem[`${key}_name`] = maps[key].get(item[key]);
        }
      }
      return enrichedItem;
    });
  });

  // Applicerar först filter och sökning på den berikade datan.
  const filteredResults = computed(() => {
    return applyFilters(enrichedItems.value, searchTerm.value, categoryFilters.value, numericFilters.value);
  });
  
  // Applicerar sedan sortering på det filtrerade resultatet.
  const filteredAndSortedResults = computed(() => {
    return applySorting(filteredResults.value, sortKey.value, sortOrder.value);
  });

  // Hanterar paginering av det sorterade och filtrerade resultatet.
  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return filteredAndSortedResults.value.slice(start, end);
  });
  
  // Återställer pagineringen när filter eller sökterm ändras.
  watch([searchTerm, categoryFilters, numericFilters, dataType], () => {
    currentPage.value = 1;
  });

  // Returnerar enbart den publika API:n för storen.
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
    
    // Getters
    paginatedResults,
    totalResultsCount: computed(() => filteredResults.value.length),

    // Actions
    initialize,
  };
}
// src/entities/data-explorer/model/explorerStore.js
