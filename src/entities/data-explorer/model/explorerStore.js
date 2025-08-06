// src/entities/data-explorer/model/explorerStore.js
//
// === SYFTE & ANSVAR ===
// Denna Pinia store hanterar all state och logik för Data Explorer-funktionen.
//
// === HISTORIK ===
// * 2025-08-06: (Frankensteen - Operation: Synkroniserad Initialisering) Infört en intern 'watch' för att atomiskt synkronisera filter-state (categoryFilters, numericFilters) med den valda datatypen. Detta löser en kritisk race condition-krasch.
// * 2025-08-06: (Frankensteen) Uppdaterat `isPristine`-gettern för att korrekt hantera array-baserade värden i `categoryFilters` för multi-select-funktionalitet.
// * 2025-08-05: (CODE RED FIX by Frankensteen) Tog bort det felaktiga beroendet av `isLoading` från `isPristine`-gettern.
// * 2025-08-05: (Definitiv Fix av Frankensteen) Infört robusta skyddsvillkor med optional chaining (`?.`) i getters.
//
// === TILLÄMPADE REGLER (Frankensteen v4.0) ===
// - "Help me God"-protokollet har använts för att verifiera denna ändring.
// - API-kontraktsverifiering: Den interna logiken är förbättrad, men det externa API:et (actions, getters) förblir konsekvent.
// - Obligatorisk Refaktorisering: Logiken för state-initialisering är nu centraliserad, robust och borttagen från komponentlagret.

import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue'; // Ny import: watch
import { fetchExplorerData } from '../api/fetchExplorerData.js';
import { transformAndClassifyData } from '../lib/transformer.js';
import { applyFilters, applySorting } from '../lib/filters.js';

export const useExplorerStore = defineStore('explorer', () => {
  // --- State ---
  const isLoading = ref(true);
  const error = ref(null);

  const allItems = ref([]);
  const filtersMap = ref({});
  const translationMap = ref({});
  const classifications = ref({});

  const dataType = ref(null);
  const searchTerm = ref('');
  const categoryFilters = ref({});
  const numericFilters = ref({});
  const sortKey = ref('manufacturer');
  const sortOrder = ref('asc');
  const currentPage = ref(1);
  const itemsPerPage = ref(25);

  // --- Getters (Computed) ---
  const currentItems = computed(() => {
    if (!dataType.value) return [];
    return allItems.value.filter(item => item.item_type === dataType.value);
  });

  const availableFilters = computed(() => {
    return filtersMap.value[dataType.value]?.categorical || [];
  });

  const availableNumericFilters = computed(() => {
    return filtersMap.value[dataType.value]?.numerical || [];
  });
  
  // --- Actions ---
  function _resetFilterValues() {
    searchTerm.value = '';
    currentPage.value = 1;
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';

    // Istället för att radera objekten, nollställ deras värden
    for (const key in categoryFilters.value) {
        categoryFilters.value[key] = [];
    }
    for (const key in numericFilters.value) {
        numericFilters.value[key] = { min: null, max: null };
    }
  }

  function setDataType(type) {
    if (dataType.value !== type) {
      dataType.value = type;
      // Anrop till _resetAllFilters tas bort härifrån. Watchern hanterar det.
    }
  }

  function resetFilters() {
    _resetFilterValues();
  }

  function setSort(key) {
    if (sortKey.value === key) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey.value = key;
      sortOrder.value = 'asc';
    }
    currentPage.value = 1;
  }

  function setPage(page) {
    if (page > 0 && page <= totalPages.value) {
      currentPage.value = page;
    }
  }

  async function initializeData() {
    if (!isLoading.value && allItems.value.length > 0) {
      return;
    }

    try {
      isLoading.value = true;
      const data = await fetchExplorerData();
      
      const cartridges = transformAndClassifyData(data.cartridgesData, data.cartridgesClassifications);
      const tonearms = transformAndClassifyData(data.tonearmsData, data.tonearmsClassifications);
      allItems.value = [...cartridges, ...tonearms];

      filtersMap.value = data.filtersMap;
      translationMap.value = data.translationMap;
      classifications.value = { ...data.cartridgesClassifications, ...data.tonearmsClassifications };

      if (!dataType.value) {
        dataType.value = 'cartridges';
      }

      error.value = null;
    } catch (e) {
      console.error('Failed to initialize explorer store:', e);
      error.value = 'Could not load data. Please try again later.';
    } finally {
      isLoading.value = false;
    }
  }

  // --- NY WATCHER FÖR SYNKRONISERING ---
  // Denna watcher är lösningen. Den garanterar att när `availableFilters` ändras
  // (som ett resultat av att `dataType` ändras), så är filter-staten omedelbart
  // synkroniserad och korrekt initialiserad INNAN UI kan försöka rendera.
  watch(availableFilters, (newFilters, oldFilters) => {
      _resetFilterValues(); // Nollställ alla filtervärden

      // Bygg om state-objekten från grunden för att matcha de nya filtren
      const newCategoryFilters = {};
      availableFilters.value.forEach(filter => {
          newCategoryFilters[filter.key] = [];
      });
      categoryFilters.value = newCategoryFilters;

      const newNumericFilters = {};
      availableNumericFilters.value.forEach(filter => {
          newNumericFilters[filter.key] = { min: null, max: null };
      });
      numericFilters.value = newNumericFilters;

  }, { deep: true });


  // --- Getters (Computed) Forts. ---
  const currentResults = computed(() => {
    if (!dataType.value) return [];
    
    const filtered = applyFilters(
      currentItems.value,
      searchTerm.value,
      categoryFilters.value,
      numericFilters.value
    );
    
    return applySorting(filtered, sortKey.value, sortOrder.value);
  });

  const totalResults = computed(() => currentResults.value.length);
  const totalPages = computed(() => Math.ceil(totalResults.value / itemsPerPage.value));

  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return currentResults.value.slice(start, end);
  });
  
  const currentHeaders = computed(() => {
    return filtersMap.value[dataType.value]?.tableHeaders || [];
  });
  
  const isPristine = computed(() => {
    const hasActiveSearch = searchTerm.value.trim() !== '';
    const hasActiveCategoryFilters = Object.values(categoryFilters.value).some(v => Array.isArray(v) && v.length > 0);
    const hasActiveNumericFilters = Object.values(numericFilters.value).some(v => v.min != null || v.max != null);
    
    return !hasActiveSearch && !hasActiveCategoryFilters && !hasActiveNumericFilters;
  });

  return {
    // State
    isLoading, error, dataType, searchTerm, categoryFilters, numericFilters,
    sortKey, sortOrder, currentPage, itemsPerPage, allItems,
    
    // Getters
    paginatedResults, totalResults, totalPages, currentHeaders, isPristine,
    availableFilters, availableNumericFilters, currentItems, classifications,
    
    // Actions
    initializeData, setDataType, resetFilters, setSort, setPage,
  };
});
// src/entities/data-explorer/model/explorerStore.js
