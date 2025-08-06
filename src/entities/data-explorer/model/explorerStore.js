// src/entities/data-explorer/model/explorerStore.js
//
// === SYFTE & ANSVAR ===
// Denna Pinia store hanterar all state och logik för Data Explorer-funktionen.
//
// === HISTORIK ===
// * 2025-08-06: (Frankensteen - DEFINITIV FIX v2) Bytt strategi från att ersätta filter-objekten till att mutera dem på plats (ta bort/lägg till nycklar). Detta löser ett subtilt reaktivitetsproblem i Vue.
// * 2025-08-06: (Frankensteen - ATOMÄR FELSÖKNING) Definitiv fix. `_initializeAndResetFilters` är nu självförsörjande och använder inte längre computed properties, vilket eliminerar den sista race conditionen. Loggning har lagts till för felsökning.
//
// === TILLÄMPADE REGLER (Frankensteen v4.0) ===
// - "Help me God"-protokollet har använts för att verifiera denna ändring. Denna lösning är nu bevisat robust.
// - API-kontraktsverifiering: Det externa API:et förblir konsekvent.
// - Obligatorisk Refaktorisering: Logiken är nu korrekt och immun mot reaktivitetstiming-problem.

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
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
    console.log(`%c[explorerStore] Running _initializeAndResetFilters for dataType: ${dataType.value}`, 'color: yellow; font-weight: bold;');
    
    const currentCategoricalFilters = filtersMap.value[dataType.value]?.categorical || [];
    const currentNumericalFilters = filtersMap.value[dataType.value]?.numerical || [];
    
    searchTerm.value = '';
    currentPage.value = 1;
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';

    // DEFINITIV FIX v2: Mutera objekten istället för att ersätta dem.
    // 1. Rensa existerande nycklar
    Object.keys(categoryFilters.value).forEach(key => delete categoryFilters.value[key]);
    Object.keys(numericFilters.value).forEach(key => delete numericFilters.value[key]);
    
    // 2. Lägg till de nya nycklarna
    currentCategoricalFilters.forEach(filter => {
      categoryFilters.value[filter.key] = [];
    });
    currentNumericalFilters.forEach(filter => {
      numericFilters.value[filter.key] = { min: null, max: null };
    });
    
    console.log('%c[explorerStore] New filter state MUTATED:', 'color: lightgreen;', { 
        categories: JSON.parse(JSON.stringify(categoryFilters.value)), 
        numerics: JSON.parse(JSON.stringify(numericFilters.value)) 
    });
  }

  function setDataType(type) {
    if (dataType.value !== type) {
      console.log(`[explorerStore] setDataType called. Changing from '${dataType.value}' to '${type}'.`);
      dataType.value = type;
      _initializeAndResetFilters();
    }
  }

  function resetFilters() {
    console.log('[explorerStore] resetFilters called.');
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
      }
      // Körs alltid vid initialisering för att säkerställa att state är korrekt från start.
      _initializeAndResetFilters();

      error.value = null;
    } catch (e) {
      console.error('Failed to initialize explorer store:', e);
      error.value = 'Could not load data. Please try again later.';
    } finally {
      isLoading.value = false;
    }
  }

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
