// src/entities/data-explorer/model/explorerStore.js
//
// === SYFTE & ANSVAR ===
// Denna Pinia store hanterar all state och logik för Data Explorer-funktionen.
//
// === HISTORIK ===
// * 2025-08-06: (Frankensteen - DEFINITIV FIX) Helt refaktorerad för att säkerställa atomära state-övergångar. 'watch'-logiken har tagits bort och all filter-initialisering sker nu synkront inuti 'setDataType'-åtgärden. Detta löser en subtil race condition som orsakade tomma dropdowns.
// * 2025-08-06: (Frankensteen - Operation: Synkroniserad Initialisering) Infört en intern 'watch' för att atomiskt synkronisera filter-state (categoryFilters, numericFilters) med den valda datatypen. Detta löser en kritisk race condition-krasch.
// * 2025-08-06: (Frankensteen) Uppdaterat `isPristine`-gettern för att korrekt hantera array-baserade värden i `categoryFilters` för multi-select-funktionalitet.
//
// === TILLÄMPADE REGLER (Frankensteen v4.0) ===
// - "Help me God"-protokollet har använts för att verifiera denna ändring.
// - API-kontraktsverifiering: Det externa API:et förblir konsekvent, men beteendet hos 'setDataType' är nu mer robust.
// - Obligatorisk Refaktorisering: Logiken är nu korrekt placerad för att garantera atomära state-uppdateringar.

import { defineStore } from 'pinia';
import { ref, computed } from 'vue'; // 'watch' har tagits bort
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
  function _initializeAndResetFilters() {
    searchTerm.value = '';
    currentPage.value = 1;
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';

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
  }

  function setDataType(type) {
    if (dataType.value !== type) {
      dataType.value = type;
      // All logik körs nu här, synkront och atomärt
      _initializeAndResetFilters();
    }
  }

  function resetFilters() {
    // Anropar samma funktion för att säkerställa konsekvens
    _initializeAndResetFilters();
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
        // Initialisera filter för start-datatypen
        _initializeAndResetFilters();
      }

      error.value = null;
    } catch (e) {
      console.error('Failed to initialize explorer store:', e);
      error.value = 'Could not load data. Please try again later.';
    } finally {
      isLoading.value = false;
    }
  }

  // --- Watcher har tagits bort ---

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
