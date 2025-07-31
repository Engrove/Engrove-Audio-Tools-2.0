// src/entities/data-explorer/model/explorerStore.js
// Denna Pinia-store hanterar all state och affärslogik för Data Explorer-modulen.
// Den ansvarar för att hämta, filtrera, sortera och paginera data för både
// tonarmar och pickuper.
//
// ÄNDRINGAR (Problem 0.1 & 0.2):
// 1. `dataType` är nu förvald till 'tonearms' för en tydlig startvy.
// 2. `filteredResults`-gettern har uppdaterats för att korrekt ignorera
//    kategorifilter som inte har ett aktivt val (dvs. värdet är `undefined`),
//    vilket löser en bugg där "All..."-alternativet filtrerade bort all data.

import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { fetchExplorerData } from '../api/fetchExplorerData.js';

export const useExplorerStore = defineStore('explorer', () => {
  // --- STATE ---
  // All rådata och UI-tillstånd lagras här som reaktiva referenser.

  const allData = ref({ pickups: [], tonearms: [] });
  const pickupClassifications = ref({});
  const tonearmClassifications = ref({});
  const isLoading = ref(true);
  const error = ref(null);

  // ÄNDRING 0.1: 'tonearms' är nu standard för en tydlig initialvy.
  const dataType = ref('tonearms');

  const searchTerm = ref('');
  const categoryFilters = ref({});
  const numericFilters = ref({});

  const sortKey = ref('manufacturer');
  const sortOrder = ref('asc');
  const currentPage = ref(1);
  const itemsPerPage = ref(15);

  // --- GETTERS (Computed Properties) ---
  // Beräknade egenskaper som härleder state från den grundläggande datan.

  const allItems = computed(() => {
    return dataType.value === 'tonearms' ? allData.value.tonearms : allData.value.pickups;
  });

  const filteredResults = computed(() => {
    if (!allItems.value) return [];

    return allItems.value.filter(item => {
      // Sökfilter (matchar mot tillverkare och modell)
      const searchLower = searchTerm.value.toLowerCase();
      const searchMatch = searchLower === '' ||
        item.manufacturer?.toLowerCase().includes(searchLower) ||
        item.model?.toLowerCase().includes(searchLower);

      // ÄNDRING 0.2: Kategorifilter (ignorerar filter med `undefined` värde)
      const categoryMatch = Object.keys(categoryFilters.value).every(key => {
        const filterValue = categoryFilters.value[key];
        // Om inget värde är valt för detta filter (undefined), räknas det som en match.
        if (filterValue === undefined || filterValue === null) {
          return true;
        }
        return item[key] === filterValue;
      });

      // Numeriskt filter (intervall)
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
  // Funktioner som kan anropas för att ändra på state.

  async function initialize() {
    isLoading.value = true;
    error.value = null;
    try {
      const data = await fetchExplorerData();
      allData.value = {
        pickups: data.pickupsData,
        tonearms: data.tonearmsData,
      };
      pickupClassifications.value = data.pickupsClassifications;
      tonearmClassifications.value = data.tonearmsClassifications;
    } catch (e) {
      error.value = e.message || 'An unknown error occurred.';
    } finally {
      isLoading.value = false;
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
    // CSV export logic remains unchanged
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

  // Exponerar all state, getters och actions som ska användas av komponenterna.
  return {
    // State
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
    // Getters
    allItems,
    filteredResults,
    sortedResults,
    totalResultsCount,
    totalPages,
    paginatedResults,
    // Actions
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
