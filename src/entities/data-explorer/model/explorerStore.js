// src/entities/data-explorer/model/explorerStore.js
//
// === SYFTE & ANSVAR ===
// Denna Pinia store hanterar all state och logik för Data Explorer-funktionen.
// Den ansvarar för att hämta, transformera, filtrera och sortera data (tonarmar/pickuper)
// samt hantera användarens alla interaktioner med filter och tabell.
//
// === API-KONTRAKT (Getters, Actions) ===
// GETTERS:
// - isLoading, error: Standard state-hantering.
// - dataType, searchTerm, categoryFilters, numericFilters: Reaktiva state-variabler för filter.
// - sortKey, sortOrder, currentPage, itemsPerPage: Reaktiva state-variabler för tabellsortering/paginering.
// - availableFilters, availableNumericFilters, currentHeaders: Beräknade listor för UI-komponenter.
// - currentResults, paginatedResults, totalResults, totalPages: Beräknade resultat för visning.
// ACTIONS:
// - initializeData(): Hämtar all initial data.
// - setDataType(type): Växlar mellan 'tonearms' och 'cartridges'.
// - resetFilters(): Återställer alla filter.
// - setSort(key): Hanterar sortering av tabellen.
// - setPage(page): Hanterar paginering.
//
// === HISTORIK ===
// * 2025-08-05: (Fix av Frankensteen) Korrigerat import från `filters.js`. Importerar och använder nu de två separata funktionerna `applyFilters` och `applySorting` korrekt.
// * 2025-08-05: (Fix av Frankensteen) Korrigerat importnamnet för transformationsfunktionen från `transformer.js` för att matcha den exporterade funktionen `transformAndClassifyData`.
// * 2025-08-05: (Fix av Frankensteen) Korrigerat ett kritiskt byggfel. Filen hade av misstag blivit helt överskriven med Vue-komponentkod från `DataFilterPanel.vue`. Innehållet har återställts till sin korrekta Pinia store-implementation.
// * 2024-08-04: (UPPDRAG 22) Helt refaktorerad för att centralisera all logik för headers, filter och resultatberäkning.
// * 2024-08-04: (UPPDRAG 20) Initial skapelse.
//
// === TILLÄMPADE REGLER (Frankensteen v3.7) ===
// - Fullständig kod, alltid: Filen är komplett och återställd.
// - Obligatorisk Refaktorisering: Den korrekta, refaktorerade Pinia-logiken har återinförts.
// - API-kontraktsverifiering: Kontraktet med `filters.js` och `transformer.js` är nu uppfyllt.

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchExplorerData } from '../api/fetchExplorerData.js';
import { transformAndClassifyData } from '../lib/transformer.js';
import { applyFilters, applySorting } from '../lib/filters.js'; // Korrigerad import

export const useExplorerStore = defineStore('explorer', () => {
  // --- State ---
  const isLoading = ref(true);
  const error = ref(null);

  // Rådata
  const cartridgesData = ref([]);
  const tonearmsData = ref([]);
  const cartridgesClassifications = ref({});
  const tonearmsClassifications = ref({});
  const filtersMap = ref({});
  const translationMap = ref({});

  // UI State
  const dataType = ref(null); // 'tonearms' or 'cartridges'
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
    currentPage.value = page;
  }

  async function initializeData() {
    try {
      isLoading.value = true;
      const data = await fetchExplorerData();
      
      cartridgesData.value = data.cartridgesData;
      tonearmsData.value = data.tonearmsData;
      cartridgesClassifications.value = data.cartridgesClassifications;
      tonearmsClassifications.value = data.tonearmsClassifications;
      filtersMap.value = data.filtersMap;
      translationMap.value = data.translationMap;

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
    return dataType.value === 'tonearms' ? tonearmsData.value : cartridgesData.value;
  });

  const currentClassifications = computed(() => {
    return dataType.value === 'tonearms' ? tonearmsClassifications.value : cartridgesClassifications.value;
  });

  const availableFilters = computed(() => {
    if (!dataType.value || !filtersMap.value[dataType.value]) return [];
    return filtersMap.value[dataType.value].categorical.map(filter => ({
      ...filter,
      options: [
        { value: '', text: `Any ${filter.label}` },
        ...currentClassifications.value[filter.key]
      ]
    }));
  });
  
  const availableNumericFilters = computed(() => {
    if (!dataType.value || !filtersMap.value[dataType.value]) return [];
    return filtersMap.value[dataType.value].numerical;
  });

  const currentTransformedData = computed(() => {
    if (!dataType.value) return [];
    return transformAndClassifyData(currentRawData.value, currentClassifications.value);
  });
  
  const currentResults = computed(() => {
    if (!dataType.value) return [];
    
    // Korrigerad logik: applicera filter först, sedan sortering
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
    if (!dataType.value || !filtersMap.value[dataType.value]) return [];
    return filtersMap.value[dataType.value].tableHeaders;
  });
  
  const isPristine = computed(() => {
    return !searchTerm.value && 
           Object.keys(categoryFilters.value).length === 0 && 
           Object.keys(numericFilters.value).length === 0 &&
           currentResults.value.length === 0;
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
