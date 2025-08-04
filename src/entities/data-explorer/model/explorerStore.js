// src/entities/data-explorer/model/explorerStore.js
/**
 * Historik:
 * - 2024-08-04: (UPPDRAG 20) Omfattande refaktorisering för att använda de nya centraliserade datafilerna.
 * - 2024-08-04: (UPPDRAG 22) Fullständig refaktorering: Bytte 'pickup' till 'cartridge', centraliserade UI-logik (headers, filter),
 *               och la till prestandaoptimeringar samt robust felhantering i datanormalisering.
 */

/**
 * Viktiga implementerade regler:
 * - Fullständig kod, alltid: Filen är komplett.
 * - Alter Ego-granskning: Genomförd för att säkerställa robusthet, prestanda och korrekt centralisering av logik.
 * - Obligatorisk Refaktorisering: Hela storen är omskriven för att vara mer underhållbar och agera som "single source of truth".
 * - "Misstro och Verifiera": Logiken för `_normalizeAndTranslateData` verifierar nu översättningar och loggar vid fel.
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchExplorerData } from '@/entities/data-explorer/api/fetchExplorerData.js';
import { useLoggerStore } from '@/entities/logger/model/loggerStore.js';

export const useExplorerStore = defineStore('explorer', () => {
  // === STATE ===
  const isLoading = ref(true);
  const error = ref(null);
  const dataType = ref('tonearms'); // NYTT STARTLÄGE

  // Rådata (refaktorerad terminologi)
  const allCartridges = ref([]);
  const allTonearms = ref([]);
  const cartridgeClassifications = ref({});
  const tonearmClassifications = ref({});

  // Centraliserade kartor
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
   * @param {Array} data - Array med rådataobjekt.
   * @param {string} type - 'cartridges' eller 'tonearms'.
   * @returns {Array} Den berikade data-arrayen.
   */
  const _normalizeAndTranslateData = (data, type) => {
    const logger = useLoggerStore();
    const typeMap = translationMap.value[type] || {};
    return data.map(item => {
      const newItem = { ...item };
      for (const key in typeMap) {
        const originalValue = item[key];
        if (originalValue !== null && originalValue !== undefined) {
          const translatedValue = typeMap[key][originalValue];
          if (translatedValue !== undefined) {
            newItem[`${key}_name`] = translatedValue;
          } else {
            // Fallback och loggning om översättning saknas
            newItem[`${key}_name`] = originalValue;
            logger.addLog(
              `Missing translation for type '${type}', key '${key}', value '${originalValue}'. Falling back to original value.`,
              'ExplorerStore',
              { item: item.model }
            );
          }
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
   * Stubbfunktion för CSV-export.
   */
  const exportToCSV = () => {
      console.warn('exportToCSV function called but is not yet implemented.');
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
      
      filtersMap.value = data.filtersMap;
      translationMap.value = data.translationMap;

      // Prestandaoptimering: Filtrera bort oönskad data EN gång vid initiering.
      const cleanCartridges = data.cartridgesData.filter(item => item.rectype !== 'U');
      const cleanTonearms = data.tonearmsData.filter(item => item.rectype !== 'U');

      allCartridges.value = _normalizeAndTranslateData(cleanCartridges, 'cartridges');
      allTonearms.value = _normalizeAndTranslateData(cleanTonearms, 'tonearms');
      
      cartridgeClassifications.value = data.cartridgesClassifications;
      tonearmClassifications.value = data.tonearmsClassifications;

      logger.addLog('Explorer store initialized successfully.', 'ExplorerStore', {
        cartridgeCount: allCartridges.value.length,
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
  const nextPage = () => { if (currentPage.value < totalPages.value) { currentPage.value++; } };
  const prevPage = () => { if (currentPage.value > 1) { currentPage.value--; } };

  // === GETTERS ===

  const currentData = computed(() => {
    return dataType.value === 'cartridges' ? allCartridges.value : allTonearms.value;
  });

  const availableFilters = computed(() => {
    if (!dataType.value || !filtersMap.value[dataType.value]) return [];
    return filtersMap.value[dataType.value];
  });

  // NY, CENTRALISERAD GETTER: Definierar numeriska filter baserat på datatyp.
  const availableNumericFilters = computed(() => {
    if (dataType.value === 'tonearms') {
      return [
        { key: 'effective_mass_g', label: 'Effective Mass', unit: 'g' },
        { key: 'effective_length_mm', label: 'Effective Length', unit: 'mm' },
      ];
    } else if (dataType.value === 'cartridges') {
      return [
        { key: 'weight_g', label: 'Cartridge Weight', unit: 'g' },
        { key: 'cu_dynamic_10hz', label: 'Compliance @ 10Hz', unit: 'cu' },
      ];
    }
    return [];
  });

  // NY, CENTRALISERAD GETTER: Definierar tabellheaders baserat på datatyp.
  const currentHeaders = computed(() => {
    if (dataType.value === 'cartridges') {
      return [
        { key: 'manufacturer', label: 'Manufacturer', sortable: true },
        { key: 'model', label: 'Model', sortable: true },
        { key: 'type_name', label: 'Type', sortable: true },
        { key: 'cu_dynamic_10hz', label: 'Compliance @ 10Hz', sortable: true },
        { key: 'weight_g', label: 'Weight (g)', sortable: true },
        { key: 'stylus_family_name', label: 'Stylus', sortable: true }
      ];
    } else { // tonearms
      return [
        { key: 'manufacturer', label: 'Manufacturer', sortable: true },
        { key: 'model', label: 'Model', sortable: true },
        { key: 'effective_mass_g', label: 'Effective Mass (g)', sortable: true },
        { key: 'effective_length_mm', label: 'Length (mm)', sortable: true },
        { key: 'bearing_type_name', label: 'Bearing', sortable: true },
        { key: 'arm_shape_name', label: 'Shape', sortable: true }
      ];
    }
  });


  const filteredResults = computed(() => {
    if (!currentData.value) return [];
    let results = [...currentData.value];

    // Sökfilter
    if (searchTerm.value) {
      const lowerCaseSearch = searchTerm.value.toLowerCase();
      results = results.filter(item =>
        item.manufacturer?.toLowerCase().includes(lowerCaseSearch) ||
        item.model?.toLowerCase().includes(lowerCaseSearch)
      );
    }
    // Kategorifilter
    for (const [key, value] of Object.entries(categoryFilters.value)) {
      if (value) {
        results = results.filter(item => item[key] === value);
      }
    }
    // Numeriska filter
    for (const [key, range] of Object.entries(numericFilters.value)) {
      if (range.min !== null) { results = results.filter(item => item[key] >= range.min); }
      if (range.max !== null) { results = results.filter(item => item[key] <= range.max); }
    }
    // Sortering
    results.sort((a, b) => {
      const valA = a[sortKey.value];
      const valB = b[sortKey.value];
      if (valA === null || valA === undefined) return 1;
      if (valB === null || valB === undefined) return -1;
      if (typeof valA === 'string') {
        return sortOrder.value === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
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
    allCartridges, allTonearms, cartridgeClassifications, tonearmClassifications,
    availableFilters, availableNumericFilters, currentHeaders,
    initialize, setDataType, resetFilters, setSortKey, nextPage, prevPage, exportToCSV,
  };
});
// src/entities/data-explorer/model/explorerStore.js
