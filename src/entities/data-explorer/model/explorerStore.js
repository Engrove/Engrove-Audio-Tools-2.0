// src/entities/data-explorer/model/explorerStore.js
// Kärnan för Data Explorer. Hanterar state, filtrering, sortering och datainhämtning.
// UPPDRAG 20: Omfattande refaktorisering för att använda de nya centraliserade datafilerna.

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchExplorerData } from '@/entities/data-explorer/api/fetchExplorerData.js';
import { useLoggerStore } from '@/entities/logger/model/loggerStore.js';

export const useExplorerStore = defineStore('explorer', () => {
  // === STATE ===
  const isLoading = ref(true);
  const error = ref(null);
  const dataType = ref(null); // 'cartridges' or 'tonearms'

  // Rådata
  const allPickups = ref([]);
  const allTonearms = ref([]);
  const pickupClassifications = ref({});
  const tonearmClassifications = ref({});

  // NYTT STATE: Centraliserade kartor
  const filtersMap = ref({});
  const translationMap = ref({});

  // Filter-state
  const searchTerm = ref('');
  const categoryFilters = ref({});
  const numericFilters = ref({
    weight_g: { min: null, max: null },
    cu_dynamic_10hz: { min: null, max: null },
    effective_mass_g: { min: null, max: null },
    effective_length_mm: { min: null, max: null },
  });

  // Sortering & Paginering
  const sortKey = ref('manufacturer');
  const sortOrder = ref('asc');
  const currentPage = ref(1);
  const itemsPerPage = ref(20);

  // === ACTIONS ===

  /**
   * Privat funktion för att berika rådata med översatta namn.
   * Använder translationMap för att skapa nya _name-fält.
   * @param {Array} data - Array med rådataobjekt.
   * @param {string} type - 'pickups' eller 'tonearms'.
   * @returns {Array} Den berikade data-arrayen.
   */
  const _normalizeAndTranslateData = (data, type) => {
    const typeMap = translationMap.value[type] || {};
    return data.map(item => {
      const newItem = { ...item };
      for (const key in typeMap) {
        const value = item[key];
        if (value !== null && value !== undefined) {
          // Skapa ett nytt fält, t.ex. type_name
          // Faller tillbaka till originalvärdet om ingen översättning finns.
          newItem[`${key}_name`] = typeMap[key][value] || value;
        } else {
          newItem[`${key}_name`] = null;
        }
      }
      return newItem;
    });
  };

  /**
   * Sätter den aktuella datan som ska visas och återställer filter.
   * @param {string} type - 'cartridges' or 'tonearms'
   */
  const setDataType = (type) => {
    if (dataType.value !== type) {
      dataType.value = type;
      resetFilters();
    }
  };

  /**
   * Återställer alla filter till sina ursprungsvärden.
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
   * Hanterar sorteringslogik.
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
   */
  const initialize = async () => {
    const logger = useLoggerStore();
    isLoading.value = true;
    error.value = null;
    try {
      const data = await fetchExplorerData();
      
      // Lagra de nya kartorna i state
      filtersMap.value = data.filtersMap;
      translationMap.value = data.translationMap;

      // Berika rådatan med de översatta namnen
      allPickups.value = _normalizeAndTranslateData(data.pickupsData, 'pickups');
      allTonearms.value = _normalizeAndTranslateData(data.tonearmsData, 'tonearms');
      
      pickupClassifications.value = data.pickupsClassifications;
      tonearmClassifications.value = data.tonearmsClassifications;

      logger.addLog('Explorer store initialized successfully.', 'ExplorerStore', {
        pickupCount: allPickups.value.length,
        tonearmCount: allTonearms.value.length,
        filtersLoaded: !!filtersMap.value,
        translationsLoaded: !!translationMap.value
      });

    } catch (e) {
      error.value = 'Could not load component database. Please try again later.';
      logger.addLog(`Failed to initialize explorer store: ${e.message}`, 'ExplorerStore', e);
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

  // === GETTERS ===

  const currentData = computed(() => {
    return dataType.value === 'cartridges' ? allPickups.value : allTonearms.value;
  });

  /**
   * REFAKTORERAD: Returnerar nu direkt den för-genererade filterlistan från state.
   */
  const availableFilters = computed(() => {
    if (!dataType.value || !filtersMap.value) return [];
    return filtersMap.value[dataType.value === 'cartridges' ? 'cartridges' : 'tonearms'] || [];
  });

  const filteredResults = computed(() => {
    if (!currentData.value) return [];

    let results = [...currentData.value];

    // 1. Sökfilter
    if (searchTerm.value) {
      const lowerCaseSearch = searchTerm.value.toLowerCase();
      results = results.filter(item =>
        item.manufacturer?.toLowerCase().includes(lowerCaseSearch) ||
        item.model?.toLowerCase().includes(lowerCaseSearch)
      );
    }

    // 2. Kategorifilter
    for (const [key, value] of Object.entries(categoryFilters.value)) {
      if (value) {
        results = results.filter(item => item[key] === value);
      }
    }

    // 3. Numeriska filter
    for (const [key, range] of Object.entries(numericFilters.value)) {
      if (range.min !== null) {
        results = results.filter(item => item[key] >= range.min);
      }
      if (range.max !== null) {
        results = results.filter(item => item[key] <= range.max);
      }
    }

    // 4. Sortering
    results.sort((a, b) => {
      const valA = a[sortKey.value];
      const valB = b[sortKey.value];

      if (valA === null || valA === undefined) return 1;
      if (valB === null || valB === undefined) return -1;

      if (typeof valA === 'string') {
        return sortOrder.value === 'asc'
          ? valA.localeCompare(valB)
          : valB.localeCompare(valA);
      } else {
        return sortOrder.value === 'asc' ? valA - valB : valB - valA;
      }
    });

    return results;
  });

  const totalResultsCount = computed(() => filteredResults.value.length);
  const totalPages = computed(() => Math.ceil(totalResultsCount.value / itemsPerPage.value));

  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return filteredResults.value.slice(start, end);
  });

  // Exporterar allt som behövs av UI-komponenterna
  return {
    isLoading, error, dataType, searchTerm, categoryFilters, numericFilters,
    sortKey, sortOrder, currentPage, itemsPerPage,
    totalResultsCount, totalPages, paginatedResults,
    availableFilters, pickupClassifications, tonearmClassifications,
    initialize, setDataType, resetFilters, setSortKey, nextPage, prevPage,
  };
});
// src/entities/data-explorer/model/explorerStore.js
