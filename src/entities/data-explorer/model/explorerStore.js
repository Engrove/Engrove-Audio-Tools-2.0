// src/entities/data-explorer/model/explorerStore.js
// Denna Pinia-store hanterar all state och affärslogik för Data Explorer-modulen.
// Den ansvarar för att hämta, filtrera, sortera och paginera data för både
// tonarmar och pickuper.
//
// FELSÖKNING:
// - Importerar och använder loggerStore för att spåra initialize-processen.
// - Loggningsanropet har gjorts mer robust med en null-kontroll för att
//   förhindra krascher om en datakälla saknas.

import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { fetchExplorerData } from '../api/fetchExplorerData.js';
import { useLoggerStore } from '../../logger/model/loggerStore.js';

export const useExplorerStore = defineStore('explorer', () => {
  // Felsökning: Hämta en instans av loggerStore.
  const logger = useLoggerStore();

  // --- STATE ---
  const allData = ref({ pickups: [], tonearms: [] });
  const pickupClassifications = ref({});
  const tonearmClassifications = ref({});
  const isLoading = ref(true);
  const error = ref(null);
  const dataType = ref('tonearms');
  const searchTerm = ref('');
  const categoryFilters = ref({});
  const numericFilters = ref({});
  const sortKey = ref('manufacturer');
  const sortOrder = ref('asc');
  const currentPage = ref(1);
  const itemsPerPage = ref(15);

  // --- GETTERS (Computed Properties) ---
  const allItems = computed(() => {
    return dataType.value === 'tonearms' ? allData.value.tonearms : allData.value.pickups;
  });

  const filteredResults = computed(() => {
    if (!allItems.value) return [];

    return allItems.value.filter(item => {
      const searchLower = searchTerm.value.toLowerCase();
      const searchMatch = searchLower === '' ||
        item.manufacturer?.toLowerCase().includes(searchLower) ||
        item.model?.toLowerCase().includes(searchLower);

      const categoryMatch = Object.keys(categoryFilters.value).every(key => {
        const filterValue = categoryFilters.value[key];
        if (filterValue === undefined || filterValue === null) {
          return true;
        }
        return item[key] === filterValue;
      });

      const numericMatch = Object.keys(numericFilters.value).every(key => {
        const range = numericFilters.value[key];
        const itemValue = item[key];
        if (itemValue === null || itemValue === undefined) return false;
        const minMatch = range.min === null || itemValue >= range.min;
        const maxMatch = range.max === null || itemValue <= range.max;
        return minMatch && maxMatch;
      });

      return searchMatch && categoryMatch && numericMatch;
    });
  });

  const sortedResults = computed(() => {
    if (!sortKey.value) return filteredResults.value;

    return [...filteredResults.value].sort((a, b) => {
      let valA = a[sortKey.value];
      let valB = b[sortKey.value];

      if (typeof valA === 'string') valA = valA.toLowerCase();
      if (typeof valB === 'string') valB = valB.toLowerCase();

      if (valA === null || valA === undefined) return 1;
      if (valB === null || valB === undefined) return -1;

      if (valA < valB) return sortOrder.value === 'asc' ? -1 : 1;
      if (valA > valB) return sortOrder.value === 'asc' ? 1 : -1;
      return 0;
    });
  });

  const totalResultsCount = computed(() => sortedResults.value.length);
  const totalPages = computed(() => Math.ceil(totalResultsCount.value / itemsPerPage.value));

  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return sortedResults.value.slice(start, end);
  });

  // --- ACTIONS ---
  async function initialize() {
    logger.addLog('initialize() called.', 'explorerStore');
    isLoading.value = true;
    error.value = null;
    try {
      const data = await fetchExplorerData();
      logger.addLog('fetchExplorerData() completed successfully.', 'explorerStore', data);

      allData.value = {
        pickups: data.pickupsData,
        tonearms: data.tonearmsData,
      };
      pickupClassifications.value = data.pickupsClassifications;
      tonearmClassifications.value = data.tonearmsClassifications;
      
      logger.addLog('State has been populated with fetched data.', 'explorerStore', {
        tonearmsCount: allData.value.tonearms.length,
        pickupsCount: allData.value.pickups.length,
        // KORRIGERING: Lade till en null-kontroll för att förhindra krasch.
        // Om tonearmClassifications.value är null/undefined, logga 'N/A'.
        // Om tonearmClassifications.value har ett värde, logga dess nycklar.
        tonearmClassificationsKeys: tonearmClassifications.value ? Object.keys(tonearmClassifications.value) : 'N/A',
      });

    } catch (e) {
      error.value = e.message || 'An unknown error occurred.';
      logger.addLog('An error occurred during initialize().', 'explorerStore', e);
    } finally {
      isLoading.value = false;
      logger.addLog('isLoading set to false.', 'explorerStore');
    }
  }

  function setDataType(type) {
    dataType.value = type;
    resetFilters();
  }

  function resetFilters() {
    searchTerm.value = '';
    categoryFilters.value = {};
    numericFilters.value = {};
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';
    currentPage.value = 1;
  }

  function setSortKey(key) {
    if (sortKey.value === key) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey.value = key;
      sortOrder.value = 'asc';
    }
    currentPage.value = 1;
  }

  function nextPage() {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
    }
  }

  function prevPage() {
    if (currentPage.value > 1) {
      currentPage.value--;
    }
  }

  function exportToCSV() {
    const itemsToExport = sortedResults.value;
    if (itemsToExport.length === 0) return;

    const headers = Object.keys(itemsToExport[0]);
    const csvRows = [
      headers.join(','),
      ...itemsToExport.map(row =>
        headers.map(fieldName => JSON.stringify(row[fieldName], (key, value) => value === null ? '' : value)).join(',')
      )
    ];

    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `engrove_data_export_${dataType.value}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  return {
    allData,
    pickupClassifications,
    tonearmClassifications,
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
    allItems,
    filteredResults,
    sortedResults,
    totalResultsCount,
    totalPages,
    paginatedResults,
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
