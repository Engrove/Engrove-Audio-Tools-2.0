// src/entities/data-explorer/model/explorerStore.js
// Denna fil definierar Pinia-storen för Data Explorer. Den agerar som den
// centrala "hjärnan" för modulen, hanterar all state, datainhämtning,
// filtrering, sortering och pagineringslogik.

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchAllExplorerData } from '../api/fetchExplorerData.js';

// --- Helper Functions ---

/**
 * Mappar klassificeringsdata till dataobjekten för enklare filtrering och visning.
 * Denna funktion berikar varje pickup/tonarm med läsbara namn från klassificeringsfilerna.
 * Exempel: 'bearing_type: "unipivot"' blir 'bearing_type_name: "Unipivot"'.
 * @param {Array} data - Array av dataobjekt (t.ex. allPickups).
 * @param {Object} classifications - Objektet med klassificeringar (t.ex. pickupClassifications).
 * @returns {Array} En ny array med berikade dataobjekt.
 */
function mapClassificationsToData(data, classifications) {
  if (!data || !classifications) return [];
  
  return data.map(item => {
    const newItem = { ...item };
    for (const key in classifications) {
      const classification = classifications[key];
      const itemValue = item[key];
      if (itemValue) {
        const category = classification.categories.find(c => c.id === itemValue);
        // Lägg till en ny nyckel med "_name" för det läsbara namnet.
        newItem[`${key}_name`] = category ? category.name : itemValue;
      }
    }
    // Specifikt för pickups, mappa `type` till `type_name`.
    if (item.type) {
        newItem.type_name = item.type;
    }
    return newItem;
  });
}


export const useExplorerStore = defineStore('explorer', () => {
  // --- STATE ---
  // Status för datainhämtning
  const isLoading = ref(false);
  const error = ref(null);
  const hasInitialized = ref(false);

  // Rådata från JSON-filer
  const allPickups = ref([]);
  const allTonearms = ref([]);
  const pickupClassifications = ref({});
  const tonearmClassifications = ref({});

  // State för filter och kontroller
  const dataType = ref(null); // 'cartridges' or 'tonearms'
  const searchTerm = ref('');
  const categoryFilters = ref({});
  const numericFilters = ref({});

  // State för sortering och paginering
  const sortKey = ref('manufacturer');
  const sortOrder = ref('asc');
  const currentPage = ref(1);
  const itemsPerPage = ref(15);
  
  // --- COMPUTED / GETTERS ---

  // Beräknar den aktuella datamängden baserat på vald `dataType`
  const currentDataSet = computed(() => {
    return dataType.value === 'cartridges' ? allPickups.value : allTonearms.value;
  });

  // Kärnlogik för filtrering
  const filteredResults = computed(() => {
    let results = [...currentDataSet.value];

    // 1. Söktermsfilter
    if (searchTerm.value) {
      const term = searchTerm.value.toLowerCase();
      results = results.filter(item =>
        item.manufacturer?.toLowerCase().includes(term) ||
        item.model?.toLowerCase().includes(term)
      );
    }

    // 2. Kategorifilter
    for (const [key, value] of Object.entries(categoryFilters.value)) {
      if (value !== undefined) {
        results = results.filter(item => item[key] === value);
      }
    }

    // 3. Numeriska filter
    for (const [key, range] of Object.entries(numericFilters.value)) {
      if (range.min !== null) {
        results = results.filter(item => item[key] !== null && item[key] >= range.min);
      }
      if (range.max !== null) {
        results = results.filter(item => item[key] !== null && item[key] <= range.max);
      }
    }
    
    return results;
  });

  // Kärnlogik för sortering
  const sortedResults = computed(() => {
    if (!sortKey.value) return filteredResults.value;

    return [...filteredResults.value].sort((a, b) => {
      let valA = a[sortKey.value];
      let valB = b[sortKey.value];
      
      const order = sortOrder.value === 'asc' ? 1 : -1;

      // Hantera null/undefined-värden så de hamnar sist
      if (valA == null) return 1;
      if (valB == null) return -1;

      // Numerisk eller alfabetisk sortering
      if (typeof valA === 'number' && typeof valB === 'number') {
        return (valA - valB) * order;
      } else {
        return String(valA).localeCompare(String(valB)) * order;
      }
    });
  });

  const totalResultsCount = computed(() => sortedResults.value.length);
  
  // Kärnlogik för paginering
  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return sortedResults.value.slice(start, end);
  });
  
  // --- ACTIONS ---
  
  // Återställer alla filter till deras ursprungliga tillstånd
  function resetFilters() {
    searchTerm.value = '';
    categoryFilters.value = {};
    numericFilters.value = {};
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';
    currentPage.value = 1;
  }
  
  // Sätter vilken datatyp som ska visas och återställer filter
  function setDataType(type) {
    if (dataType.value !== type) {
      dataType.value = type;
      resetFilters();
    }
  }

  // Sätter sorteringsnyckel och riktning
  function setSortKey(key) {
    if (sortKey.value === key) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey.value = key;
      sortOrder.value = 'asc';
    }
    currentPage.value = 1; // Återgå till första sidan vid ny sortering
  }

  function nextPage() {
    const totalPages = Math.ceil(totalResultsCount.value / itemsPerPage.value);
    if (currentPage.value < totalPages) {
      currentPage.value++;
    }
  }

  function prevPage() {
    if (currentPage.value > 1) {
      currentPage.value--;
    }
  }

  // CSV Export
  function exportToCSV() {
    const headers = Object.keys(sortedResults.value[0] || {});
    const csvRows = [
      headers.join(','), // Header row
      ...sortedResults.value.map(row => 
        headers.map(header => JSON.stringify(row[header], (key, value) => value === null ? '' : value)).join(',')
      )
    ];

    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `${dataType.value}_export.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // Initialiserar storen genom att hämta all data
  async function initialize() {
    if (hasInitialized.value) return;

    isLoading.value = true;
    error.value = null;
    try {
      const data = await fetchAllExplorerData();

      // Mappa klassificeringsnamn till datan
      allPickups.value = mapClassificationsToData(data.pickups, data.pickupClassifications);
      allTonearms.value = mapClassificationsToData(data.tonearms, data.tonearmClassifications);

      pickupClassifications.value = data.pickupClassifications;
      tonearmClassifications.value = data.tonearmClassifications;
      
      hasInitialized.value = true;
    } catch (err) {
      error.value = err.message || 'An unknown error occurred.';
    } finally {
      isLoading.value = false;
    }
  }

  return {
    // State & Getters
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
    paginatedResults,
    totalResultsCount,
    // Actions
    initialize,
    setDataType,
    resetFilters,
    setSortKey,
    nextPage,
    prevPage,
    exportToCSV,
  };
});
// src/entities/data-explorer/model/explorerStore.js
