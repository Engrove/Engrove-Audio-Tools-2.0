// src/entities/data-explorer/model/explorerStore.js
// Denna Pinia-store hanterar all state och logik för Data Explorer-modulen.
// UPPDRAG 20: Genomgår en stor refaktorisering för att använda de nya centraliserade
// datafilerna för filter och översättningar.

import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue';
import { fetchExplorerData } from '../api/fetchExplorerData.js';
import { useLoggerStore } from '../../../entities/logger/model/loggerStore.js';

export const useExplorerStore = defineStore('explorer', () => {
  const logger = useLoggerStore();

  // --- STATE ---

  // Laddnings- och felhantering
  const isLoading = ref(false);
  const error = ref(null);
  const isInitialized = ref(false);

  // Rådata och klassificeringar
  const allPickups = ref([]);
  const allTonearms = ref([]);
  const pickupClassifications = ref({});
  const tonearmClassifications = ref({});

  // NYTT STATE: Centraliserade kartor för filter och översättningar
  const filtersMap = ref({});
  const translationMap = ref({});

  // Filter- och sökparametrar
  const dataType = ref('cartridges'); // 'cartridges' or 'tonearms'
  const searchTerm = ref('');
  const categoryFilters = ref({});
  const numericFilters = ref({
    weight_g: { min: null, max: null },
    cu_dynamic_10hz: { min: null, max: null },
    effective_mass_g: { min: null, max: null },
    effective_length_mm: { min: null, max: null },
  });

  // Sortering och paginering
  const sortKey = ref('manufacturer');
  const sortOrder = ref('asc');
  const currentPage = ref(1);
  const itemsPerPage = ref(20);

  // --- ACTIONS ---

  /**
   * Privat funktion för att normalisera och översätta rådata.
   * Använder translationMap för att skapa nya `_name`-fält för visning.
   * @param {Array} data - Array med rådata (pickups eller tonearms).
   * @param {string} type - 'pickups' eller 'tonearms'.
   * @returns {Array} Den berikade data-arrayen.
   */
  const _normalizeAndTranslateData = (data, type) => {
    if (!translationMap.value[type]) return data;

    const typeTranslations = translationMap.value[type];

    return data.map(item => {
      const newItem = { ...item };
      for (const key in typeTranslations) {
        if (item[key]) {
          const value = item[key];
          // Skapa ett nytt fält, t.ex. type_name, baserat på översättningen.
          newItem[`${key}_name`] = typeTranslations[key][value] || value;
        } else {
          newItem[`${key}_name`] = null;
        }
      }
      return newItem;
    });
  };

  /**
   * Sätter den aktiva datatypen och återställer alla filter.
   * @param {'cartridges' | 'tonearms'} type - Den nya datatypen.
   */
  const setDataType = (type) => {
    if (dataType.value !== type) {
      dataType.value = type;
      resetFilters();
      // Sätt en standard sorteringsnyckel baserat på den nya datatypen
      sortKey.value = 'manufacturer';
      sortOrder.value = 'asc';
    }
  };

  /**
   * Återställer alla filterparametrar till sina ursprungsvärden.
   */
  const resetFilters = () => {
    searchTerm.value = '';
    categoryFilters.value = {};
    numericFilters.value = {
      weight_g: { min: null, max: null },
      cu_dynamic_10hz: { min: null, max: null },
      effective_mass_g: { min: null, max: null },
      effective_length_mm: { min: null, max: null },
    };
    currentPage.value = 1;
  };

  /**
   * Sätter sorteringsnyckel och ordning.
   * @param {string} key - Nyckeln att sortera efter.
   */
  const setSortKey = (key) => {
    if (sortKey.value === key) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey.value = key;
      sortOrder.value = 'asc';
    }
    currentPage.value = 1;
  };

  /**
   * Initierar storen genom att hämta all nödvändig data.
   * Körs bara en gång.
   */
  const initialize = async () => {
    if (isInitialized.value) return;

    isLoading.value = true;
    error.value = null;
    logger.addLog('ExplorerStore: Initializing and fetching data...', 'explorerStore');

    try {
      const data = await fetchExplorerData();
      
      // Lagra de nya kartorna i state
      filtersMap.value = data.filtersMap;
      translationMap.value = data.translationMap;
      logger.addLog('ExplorerStore: Translation and Filter maps loaded.', 'explorerStore', { filters: Object.keys(data.filtersMap), translations: Object.keys(data.translationMap) });

      // Normalisera och översätt rådatan innan den lagras
      allPickups.value = _normalizeAndTranslateData(data.pickupsData, 'pickups');
      allTonearms.value = _normalizeAndTranslateData(data.tonearmsData, 'tonearms');
      logger.addLog('ExplorerStore: Raw data normalized and translated.', 'explorerStore');

      pickupClassifications.value = data.pickupsClassifications;
      tonearmClassifications.value = data.tonearmsClassifications;

      isInitialized.value = true;
      logger.addLog('ExplorerStore: Initialization complete.', 'explorerStore');
    } catch (e) {
      error.value = e.message || 'An unknown error occurred.';
      logger.addLog(`ExplorerStore: Initialization failed: ${error.value}`, 'explorerStore');
    } finally {
      isLoading.value = false;
    }
  };

  // Paginering
  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
    }
  };
  const prevPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--;
    }
  };

  // --- GETTERS ---

  /**
   * REFAKTORERAD: Returnerar nu direkt den färdiga filterstrukturen från state.
   */
  const availableFilters = computed(() => {
    const key = dataType.value === 'cartridges' ? 'cartridges' : 'tonearms';
    return filtersMap.value[key] || [];
  });

  const currentDataset = computed(() => {
    return dataType.value === 'cartridges' ? allPickups.value : allTonearms.value;
  });

  const filteredResults = computed(() => {
    let results = [...currentDataset.value];

    // 1. Sökfilter (text)
    if (searchTerm.value) {
      const lowerCaseSearch = searchTerm.value.toLowerCase();
      results = results.filter(item =>
        item.manufacturer?.toLowerCase().includes(lowerCaseSearch) ||
        item.model?.toLowerCase().includes(lowerCaseSearch)
      );
    }

    // 2. Kategorifilter (dropdowns)
    Object.entries(categoryFilters.value).forEach(([key, value]) => {
      if (value) {
        results = results.filter(item => item[key] === value);
      }
    });

    // 3. Numeriska filter (intervall)
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

  const sortedResults = computed(() => {
    const results = [...filteredResults.value];
    const key = sortKey.value;
    const order = sortOrder.value;

    results.sort((a, b) => {
      let valA = a[key];
      let valB = b[key];

      if (typeof valA === 'string') valA = valA.toLowerCase();
      if (typeof valB === 'string') valB = valB.toLowerCase();

      if (valA < valB) return order === 'asc' ? -1 : 1;
      if (valA > valB) return order === 'asc' ? 1 : -1;
      return 0;
    });

    return results;
  });

  const totalResultsCount = computed(() => sortedResults.value.length);
  const totalPages = computed(() => Math.ceil(totalResultsCount.value / itemsPerPage.value));

  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return sortedResults.value.slice(start, end);
  });

  // Återställ till sida 1 om filtrering/sortering gör nuvarande sida ogiltig
  watch([sortedResults], () => {
    if (currentPage.value > totalPages.value) {
      currentPage.value = Math.max(1, totalPages.value);
    }
  });

  // Funktion för CSV-export (oförändrad)
  const exportToCSV = () => {
    const items = sortedResults.value;
    if (items.length === 0) return;

    const headers = Object.keys(items[0]);
    const csvRows = [headers.join(',')];

    for (const item of items) {
      const values = headers.map(header => {
        const escaped = ('' + item[header]).replace(/"/g, '\\"');
        return `"${escaped}"`;
      });
      csvRows.push(values.join(','));
    }

    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', `${dataType.value}_export.csv`);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

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
    availableFilters,
    totalResultsCount,
    paginatedResults,
    totalPages,
    pickupClassifications, // Exponeras fortfarande för DataFilterPanel
    tonearmClassifications, // Exponeras fortfarande för DataFilterPanel

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
