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

  function resetFilters() {
    searchTerm.value = '';
    categoryFilters.value = {};
    numericFilters.value = {};
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';
    currentPage.value = 1;
  }

  function setDataType(newDataType) {
    if (dataType.value !== newDataType) {
      dataType.value = newDataType;
      resetFilters();
    }
  }

  function updateNumericFilter(key, value) {
    // Vue 3's reaktivitet behöver en ny objekt-referens för att upptäcka ändringen.
    numericFilters.value = { ...numericFilters.value, [key]: value };
  }

  /**
   * Hanterar logiken för att byta sorteringskolumn och ordning.
   * @param {string} newSortKey - Nyckeln för kolumnen som klickades.
   */
  function setSortKey(newSortKey) {
    // Om man klickar på samma kolumn igen, byt sorteringsordning.
    // Om man klickar på en ny kolumn, sätt den som aktiv med stigande ordning.
    if (sortKey.value === newSortKey) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey.value = newSortKey;
      sortOrder.value = 'asc';
    }
  }

  // Paginering
  function nextPage() {
    const totalPages = Math.ceil(filteredResults.value.length / itemsPerPage.value);
    if (currentPage.value < totalPages) {
      currentPage.value++;
    }
  }

  function prevPage() {
    if (currentPage.value > 1) {
      currentPage.value--;
    }
  }

  /**
   * Genererar och laddar ner den filtrerade datan som en CSV-fil.
   */
  function exportToCSV() {
    const itemsToExport = filteredAndSortedResults.value;
    if (itemsToExport.length === 0) return;

    // Använd headers från den första raden för att bestämma kolumner.
    const headers = Object.keys(itemsToExport[0]);
    const csvRows = [headers.join(',')];

    for (const item of itemsToExport) {
      const values = headers.map(header => {
        let value = item[header];
        if (value === null || value === undefined) {
          return '';
        }
        // Hantera värden som innehåller kommatecken genom att sätta dem inom citattecken.
        value = String(value);
        if (value.includes(',')) {
          return `"${value}"`;
        }
        return value;
      });
      csvRows.push(values.join(','));
    }

    const csvString = csvRows.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `engrove_data_export_${dataType.value}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
        // Om ett ID existerar och det finns en match i uppslagstabellen, lägg till det läsbara namnet.
        if (itemValue && maps[key] && maps[key].has(itemValue)) {
          enrichedItem[`${key}_name`] = maps[key].get(itemValue);
        } else if (itemValue) {
          // Fallback: om det inte finns någon match, använd ID:t som det är (bättre än inget).
          enrichedItem[`${key}_name`] = itemValue;
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
  
  watch([searchTerm, categoryFilters, numericFilters, dataType], () => {
    if (currentPage.value !== 1) {
      currentPage.value = 1;
    }
  }, { deep: true });

  // --- Publika API:et för storen ---
  return {
    isLoading, error, dataType, searchTerm, categoryFilters, numericFilters,
    sortKey, sortOrder, currentPage, itemsPerPage, pickupClassifications,
    tonearmClassifications,
    
    paginatedResults,
    totalResultsCount: computed(() => filteredResults.value.length),

    initialize, resetFilters, setDataType, updateNumericFilter,
    setSortKey, nextPage, prevPage, exportToCSV
  };
}
// src/entities/data-explorer/model/explorerStore.js
