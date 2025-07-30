// src/entities/data-explorer/model/explorerStore.js
/**
 * Detta är Pinia-storen för Data Explorer-entiteten.
 * Den fungerar som den centrala "sanningskällan" för all data och all UI-state
 * relaterad till utforskaren. Den hanterar datainhämtning, filtrering,
 * sökning, sortering, paginering och CSV-export.
 */

import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { fetchExplorerData } from '../api/fetchExplorerData.js';

export const useExplorerStore = defineStore('explorer', () => {
  // --- STATE ---
  // Rådata från API
  const allPickups = ref([]);
  const allTonearms = ref([]);
  const pickupClassifications = ref(null);
  const tonearmClassifications = ref(null);

  // UI & Filter State
  const isLoading = ref(true);
  const error = ref(null);
  const dataType = ref(null); // 'cartridges' or 'tonearms'
  const searchTerm = ref('');
  const categoryFilters = ref({});
  const numericFilters = ref({});
  const sortKey = ref('manufacturer');
  const sortOrder = ref('asc');
  const currentPage = ref(1);
  const itemsPerPage = ref(25);

  // --- GETTERS (Computed Properties) ---

  // Väljer den aktiva datamängden baserat på `dataType`
  const activeDataSource = computed(() => {
    // Om dataType är 'cartridges', returnera allPickups.value.
    // Om dataType är något annat, returnera allTonearms.value.
    return dataType.value === 'cartridges' ? allPickups.value : allTonearms.value;
  });

  // Filtrerar datan baserat på sökterm och filter
  const filteredResults = computed(() => {
    if (!dataType.value) return [];

    let results = [...activeDataSource.value];

    // 1. Sökfiltrering (text)
    if (searchTerm.value.trim()) {
      const lowerCaseSearch = searchTerm.value.toLowerCase();
      results = results.filter(item =>
        item.manufacturer.toLowerCase().includes(lowerCaseSearch) ||
        item.model.toLowerCase().includes(lowerCaseSearch)
      );
    }

    // 2. Kategorifiltrering (dropdowns)
    Object.entries(categoryFilters.value).forEach(([key, value]) => {
      if (value) {
        results = results.filter(item => item[key] === value);
      }
    });

    // 3. Numerisk filtrering (intervall)
    Object.entries(numericFilters.value).forEach(([key, range]) => {
      if (range.min !== null) {
        results = results.filter(item => item[key] >= range.min);
      }
      if (range.max !== null) {
        results = results.filter(item => item[key] <= range.max);
      }
    });

    return results;
  });

  // Sorterar de filtrerade resultaten
  const sortedResults = computed(() => {
    const results = [...filteredResults.value];
    const key = sortKey.value;
    const order = sortOrder.value;

    results.sort((a, b) => {
      let valA = a[key];
      let valB = b[key];

      if (typeof valA === 'string') {
        valA = valA.toLowerCase();
        valB = valB.toLowerCase();
      }

      if (valA < valB) return order === 'asc' ? -1 : 1;
      if (valA > valB) return order === 'asc' ? 1 : -1;
      return 0;
    });

    return results;
  });

  // Paginering av de sorterade resultaten
  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return sortedResults.value.slice(start, end);
  });

  // Totalt antal resultat efter filtrering
  const totalResultsCount = computed(() => filteredResults.value.length);

  // --- ACTIONS ---

  // Återställer alla filter till deras ursprungliga tillstånd
  const resetFilters = () => {
    searchTerm.value = '';
    categoryFilters.value = {};
    numericFilters.value = {};
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';
    currentPage.value = 1;
  };

  // Sätter datatyp och återställer filter
  const setDataType = (type) => {
    if (dataType.value !== type) {
      dataType.value = type;
      resetFilters();
    }
  };

  // Sätter sorteringsnyckel och ordning
  const setSortKey = (key) => {
    if (sortKey.value === key) {
      // Om samma nyckel klickas, växla ordning
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
    } else {
      // Annars, sätt ny nyckel och återställ till stigande ordning
      sortKey.value = key;
      sortOrder.value = 'asc';
    }
    currentPage.value = 1; // Återställ till första sidan vid sortering
  };

  // Paginering
  const nextPage = () => {
    const totalPages = Math.ceil(totalResultsCount.value / itemsPerPage.value);
    if (currentPage.value < totalPages) {
      currentPage.value++;
    }
  };
  const prevPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--;
    }
  };

  // CSV-export
  const exportToCSV = () => {
    // Logik för CSV-export här...
  };

  // Initialiserar storen genom att hämta all data
  const initialize = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      const data = await fetchExplorerData();
      allPickups.value = data.pickupsData;
      allTonearms.value = data.tonearmsData;
      pickupClassifications.value = data.pickupClassifications;
      tonearmClassifications.value = data.tonearmClassifications;
    } catch (e) {
      error.value = e.message || 'An unknown error occurred while fetching data.';
    } finally {
      isLoading.value = false;
    }
  };

  // Returnerar allt som ska vara publikt tillgängligt från storen
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
