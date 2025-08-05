// src/entities/data-explorer/model/explorerStore.js
//
// === SYFTE & ANSVAR ===
// Denna Pinia store hanterar all state och logik för Data Explorer-funktionen.
//
// === HISTORIK ===
// * 2025-08-05: (CODE RED FIX by Frankensteen) Tog bort det felaktiga beroendet av `isLoading` från `isPristine`-gettern. Detta var den andra delen av den logiska deadlocken.
// * 2025-08-05: (Definitiv Fix av Frankensteen) Infört robusta skyddsvillkor med optional chaining (`?.`) i getters.
// * 2025-08-05: (Fix av Frankensteen) Diverse tidigare korrigeringar för att hantera race conditions och API-fel.
//
// === TILLÄMPADE REGLER (Frankensteen v3.7) ===
// - "Help me God"-protokollet har använts för att identifiera och lösa en kritisk logisk deadlock.
// - Felresiliens: Deadlocken är bruten, vilket garanterar att data nu laddas.
// - Semantik och läsbarhet: `isPristine` betyder nu vad den heter - är filtren orörda?

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchExplorerData } from '../api/fetchExplorerData.js';
import { transformAndClassifyData } from '../lib/transformer.js';
import { applyFilters, applySorting } from '../lib/filters.js';

export const useExplorerStore = defineStore('explorer', () => {
  // --- State ---
  const isLoading = ref(true);
  const error = ref(null);

  const cartridgesData = ref([]);
  const tonearmsData = ref([]);
  const cartridgesClassifications = ref({});
  const tonearmsClassifications = ref({});
  const filtersMap = ref({});
  const translationMap = ref({});

  const dataType = ref(null);
  const searchTerm = ref('');
  const categoryFilters = ref({});
  const numericFilters = ref({});
  const sortKey = ref('manufacturer');
  const sortOrder = ref('asc');
  const currentPage = ref(1);
  const itemsPerPage = ref(25);

  // --- Actions ---
  function _resetAllFilters() {
    searchTerm.value = '';
    categoryFilters.value = {};
    numericFilters.value = {};
    currentPage.value = 1;
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';
  }

  function setDataType(type) {
    if (dataType.value !== type) {
      dataType.value = type;
      _resetAllFilters();
    }
  }

  function resetFilters() {
    _resetAllFilters();
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
    // Förhindra onödiga omladdningar om en annan komponent skulle anropa igen.
    if (!isLoading.value && cartridgesData.value.length > 0) {
        return;
    }

    try {
      isLoading.value = true;
      const data = await fetchExplorerData();
      
      cartridgesData.value = data.cartridgesData;
      tonearmsData.value = data.tonearmsData;
      cartridgesClassifications.value = data.cartridgesClassifications;
      tonearmsClassifications.value = data.tonearmsClassifications;
      filtersMap.value = data.filtersMap;
      translationMap.value = data.translationMap;

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

  // --- Getters (Computed) ---
  const currentRawData = computed(() => {
    if (!dataType.value) return [];
    return dataType.value === 'tonearms' ? tonearmsData.value : cartridgesData.value;
  });

  const currentClassifications = computed(() => {
    if (!dataType.value) return {};
    return dataType.value === 'tonearms' ? tonearmsClassifications.value : cartridgesClassifications.value;
  });

  const availableFilters = computed(() => {
    const categoricalFilters = filtersMap.value[dataType.value]?.categorical || [];
    
    return categoricalFilters.map(filter => {
      const classificationGroup = currentClassifications.value[filter.key];
      
      return {
        ...filter,
        options: [
          { value: '', text: `Any ${filter.label}` },
          ...(classificationGroup ? classificationGroup.categories : [])
        ]
      };
    });
  });
  
  const availableNumericFilters = computed(() => {
    return filtersMap.value[dataType.value]?.numerical || [];
  });

  const currentTransformedData = computed(() => {
    if (!dataType.value) return [];
    return transformAndClassifyData(currentRawData.value, currentClassifications.value);
  });
  
  const currentResults = computed(() => {
    if (!dataType.value) return [];
    
    const filtered = applyFilters(
      currentTransformedData.value,
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
    // KORRIGERING: Det felaktiga beroendet av `isLoading` har tagits bort.
    const hasActiveSearch = searchTerm.value.trim() !== '';
    const hasActiveCategoryFilters = Object.values(categoryFilters.value).some(v => v);
    const hasActiveNumericFilters = Object.values(numericFilters.value).some(v => v.min != null || v.max != null);
    
    return !hasActiveSearch && !hasActiveCategoryFilters && !hasActiveNumericFilters;
  });

  return {
    // State
    isLoading, error, dataType, searchTerm, categoryFilters, numericFilters,
    sortKey, sortOrder, currentPage, itemsPerPage,
    
    // Getters
    paginatedResults, totalResults, totalPages, currentHeaders, isPristine,
    availableFilters, availableNumericFilters,
    
    // Actions
    initializeData, setDataType, resetFilters, setSort, setPage,
  };
});
// src/entities/data-explorer/model/explorerStore.js
