// src/entities/data-explorer/model/explorerStore.js
/**
 * Detta är Pinia-storen för Data Explorer-entiteten. Den fungerar som den centrala
 * "sanningskällan" och hjärnan för hela modulen. Den hanterar:
 * - Datainhämtning och tillstånd (laddning, fel).
 * - All affärslogik för sökning, filtrering, sortering och paginering.
 * - Alla användarinteraktioner från filterpanelen.
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { fetchExplorerData } from '../api/fetchExplorerData.js';

// Helper-funktion för att skapa en nedladdningsbar fil (används för CSV-export)
function downloadFile(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(link.href);
}

export const useExplorerStore = defineStore('explorer', () => {
  // --- STATE ---
  // Rådata och tillstånd
  const isLoading = ref(false);
  const error = ref(null);
  const allPickups = ref([]);
  const pickupClassifications = ref(null);
  const allTonearms = ref([]);
  const tonearmClassifications = ref(null);

  // Filter- och UI-tillstånd
  const dataType = ref(null); // 'cartridges' or 'tonearms'
  const searchTerm = ref('');
  const categoryFilters = ref({});
  const numericFilters = ref({});
  const sortKey = ref('manufacturer');
  const sortOrder = ref('asc');
  const currentPage = ref(1);
  const itemsPerPage = ref(25);

  // --- ACTIONS ---

  /**
   * Initierar storen genom att hämta all nödvändig data.
   */
  async function initialize() {
    isLoading.value = true;
    error.value = null;
    try {
      const data = await fetchExplorerData();
      allPickups.value = data.pickupsData;
      pickupClassifications.value = data.pickupClassifications;
      allTonearms.value = data.tonearmsData;
      tonearmClassifications.value = data.tonearmClassifications;
    } catch (e) {
      error.value = e.message || 'An unknown error occurred while fetching data.';
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Återställer alla filter och paginering till deras ursprungliga tillstånd.
   */
  function resetFilters() {
    searchTerm.value = '';
    categoryFilters.value = {};
    numericFilters.value = {};
    currentPage.value = 1;
    sortKey.value = 'manufacturer';
    sortOrder.value = 'asc';
  }

  /**
   * Sätter den aktiva datatypen och återställer alla filter.
   * @param {'cartridges' | 'tonearms'} type - Den nya datatypen.
   */
  function setDataType(type) {
    if (dataType.value !== type) {
      dataType.value = type;
      resetFilters();
    }
  }

  /**
   * Hanterar sorteringslogiken. Växlar ordning om samma nyckel klickas igen.
   * @param {string} key - Nyckeln för kolumnen som ska sorteras.
   */
  function setSortKey(key) {
    if (sortKey.value === key) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey.value = key;
      sortOrder.value = 'asc';
    }
    currentPage.value = 1; // Återställ till första sidan vid ny sortering
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

  // --- GETTERS (Computed Properties) ---

  // Väljer den aktiva datamängden baserat på dataType.
  const currentDataSet = computed(() => {
    return dataType.value === 'cartridges' ? allPickups.value : allTonearms.value;
  });

  // Väljer de aktiva klassificeringarna baserat på dataType.
  const currentClassifications = computed(() => {
    return dataType.value === 'cartridges' ? pickupClassifications.value : tonearmClassifications.value;
  });

  // Berikar datamängden med läsbara namn från klassificeringarna.
  // Detta är en kritisk optimering som görs en gång.
  const enrichedDataSet = computed(() => {
    if (!currentDataSet.value || !currentClassifications.value) return [];
    
    const classificationMap = {};
    for (const key in currentClassifications.value) {
      classificationMap[key] = new Map(
        currentClassifications.value[key].categories.map(cat => [cat.id, cat.name])
      );
    }
    
    return currentDataSet.value.map(item => {
      const enrichedItem = { ...item };
      for (const key in classificationMap) {
        if (item[key]) {
          enrichedItem[`${key}_name`] = classificationMap[key].get(item[key]) || item[key];
        }
      }
      if(dataType.value === 'cartridges' && item.type) {
        enrichedItem.type_name = item.type;
      }
      return enrichedItem;
    });
  });

  // Filtrerar den berikade datan baserat på söktermen.
  const searchedResults = computed(() => {
    if (!searchTerm.value) return enrichedDataSet.value;
    const lowerCaseSearch = searchTerm.value.toLowerCase();
    return enrichedDataSet.value.filter(item =>
      item.manufacturer?.toLowerCase().includes(lowerCaseSearch) ||
      item.model?.toLowerCase().includes(lowerCaseSearch)
    );
  });

  // Filtrerar resultaten från sökningen baserat på kategori- och numeriska filter.
  const filteredResults = computed(() => {
    return searchedResults.value.filter(item => {
      // Kategori-filter
      for (const key in categoryFilters.value) {
        const filterValue = categoryFilters.value[key];
        if (filterValue !== undefined && item[key] !== filterValue) {
          return false;
        }
      }
      // Numeriska filter
      for (const key in numericFilters.value) {
        const { min, max } = numericFilters.value[key];
        const itemValue = item[key];
        if (itemValue === null || itemValue === undefined) return false;
        if (min !== null && itemValue < min) return false;
        if (max !== null && itemValue > max) return false;
      }
      return true;
    });
  });

  // Sorterar de filtrerade resultaten.
  const sortedResults = computed(() => {
    return [...filteredResults.value].sort((a, b) => {
      let valA = a[sortKey.value];
      let valB = b[sortKey.value];

      if (valA === null || valA === undefined) valA = -Infinity;
      if (valB === null || valB === undefined) valB = -Infinity;

      if (typeof valA === 'string') {
        return sortOrder.value === 'asc'
          ? valA.localeCompare(valB)
          : valB.localeCompare(valA);
      } else {
        return sortOrder.value === 'asc' ? valA - valB : valB - valA;
      }
    });
  });

  // Paginering
  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return sortedResults.value.slice(start, end);
  });

  const totalResultsCount = computed(() => sortedResults.value.length);
  const totalPages = computed(() => Math.ceil(totalResultsCount.value / itemsPerPage.value));

  // --- CSV EXPORT ---
  function exportToCSV() {
    if (sortedResults.value.length === 0) return;

    const headers = Object.keys(sortedResults.value[0]);
    const csvRows = [headers.join(',')];

    for (const row of sortedResults.value) {
      const values = headers.map(header => {
        const escaped = ('' + row[header]).replace(/"/g, '""');
        return `"${escaped}"`;
      });
      csvRows.push(values.join(','));
    }
    
    const filename = `engrove_data_export_${dataType.value}_${new Date().toISOString().split('T')[0]}.csv`;
    downloadFile(filename, csvRows.join('\n'), 'text/csv');
  }

  // Exponera allt som ska användas av komponenterna
  return {
    isLoading, error, dataType, searchTerm, categoryFilters, numericFilters,
    sortKey, sortOrder, currentPage, itemsPerPage,
    allPickups, pickupClassifications, allTonearms, tonearmClassifications,
    initialize, setDataType, resetFilters, setSortKey, nextPage, prevPage,
    paginatedResults, totalResultsCount, totalPages, exportToCSV
  };
});
// src/entities/data-explorer/model/explorerStore.js
