// src/entities/data-explorer/model/explorerStore.js
//
// === SYFTE & ANSVAR ===
// Denna Pinia store hanterar all state och logik för Data Explorer-funktionen.
//
// === HISTORIK ===
// * 2025-08-06: (Frankensteen) Uppdaterat `isPristine`-gettern för att korrekt hantera array-baserade värden i `categoryFilters` för multi-select-funktionalitet.
// * 2025-08-05: (CODE RED FIX by Frankensteen) Tog bort det felaktiga beroendet av `isLoading` från `isPristine`-gettern.
// * 2025-08-05: (Definitiv Fix av Frankensteen) Infört robusta skyddsvillkor med optional chaining (`?.`) i getters.
//
// === TILLÄMPADE REGLER (Frankensteen v4.0) ===
// - "Help me God"-protokollet har använts för att verifiera denna ändring.
// - API-kontraktsverifiering: Ändringen är internt konsekvent och påverkar inte storens externa API.
// - Obligatorisk Refaktorisering: Logiken i `isPristine` är nu mer robust och generell.

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
