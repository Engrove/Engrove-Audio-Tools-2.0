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
// - setDataType(type): Växlar mellan 'tonarmar' och 'cartridges'.
// - resetFilters(): Återställer alla filter.
// - setSort(key): Hanterar sortering av tabellen.
// - setPage(page): Hanterar paginering.
//
// === HISTORIK ===
// * 2025-08-05: (Definitiv Fix av Frankensteen) Infört robusta skyddsvillkor med optional chaining (`?.`) i getters `availableFilters` och `availableNumericFilters`. Detta förhindrar `TypeError` om `data-filters-map.json` har en ofullständig struktur för en viss datatyp.
// * 2025-08-05: (Fix av Frankensteen) Infört robust hantering av initial state. `dataType` sätts nu som standard efter dataladdning, och `computed` properties skyddas mot `null` värden för att förhindra `TypeError`.
// * 2025-08-05: (Fix av Frankensteen) Korrigerat `TypeError` i `availableFilters`. Logiken hanterar nu `undefined` klassificeringar och pekar korrekt på den nästlade `categories`-arrayen.
// * 2025-08-05: (Fix av Frankensteen) Korrigerat import från `filters.js`. Importerar och använder nu de två separata funktionerna `applyFilters` och `applySorting` korrekt.
// * 2025-08-05: (Fix av Frankensteen) Korrigerat importnamnet för transformationsfunktionen från `transformer.js` för att matcha den exporterade funktionen `transformAndClassifyData`.
// * 2025-08-05: (Fix av Frankensteen) Korrigerat ett kritiskt byggfel. Filen hade av misstag blivit helt överskriven med Vue-komponentkod från `DataFilterPanel.vue`. Innehållet har återställts till sin korrekta Pinia store-implementation.
// * 2024-08-04: (UPPDRAG 22) Helt refaktorerad för att centralisera all logik för headers, filter och resultatberäkning.
// * 2024-08-04: (UPPDRAG 20) Initial skapelse.
//
// === TILLÄMPADE REGLER (Frankensteen v3.7) ===
// - "Help me God"-protokollet har använts för att identifiera den latenta, underliggande buggen.
// - Felresiliens: Getters är nu immuna mot krascher orsakade av ofullständig datastruktur.
// - Kontrakts- och förväntningsmatchning: Getters returnerar nu alltid en giltig array (`[]`), vilket uppfyller kontraktet mot UI-komponenterna.

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchExplorerData } from '../api/fetchExplorerData.js';
import { transformAndClassifyData } from '../lib/transformer.js';
import { applyFilters, applySorting } from '../lib/filters.js';

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
    if (page > 0 && page <= totalPages.value) {
      currentPage.value = page;
    }
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
    // KORRIGERING: Använder optional chaining (?.) för att säkert komma åt 'categorical'.
    // Om någon del av kedjan är null eller undefined, kraschar den inte, utan returnerar undefined.
    // Fallback till en tom array (|| []) säkerställer att gettern ALLTID returnerar en array.
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
    // KORRIGERING: Samma robusta skydd som ovan appliceras här.
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
    // KORRIGERING: Samma robusta skydd som ovan appliceras här.
    return filtersMap.value[dataType.value]?.tableHeaders || [];
  });
  
  const isPristine = computed(() => {
    if (isLoading.value) return false;
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
