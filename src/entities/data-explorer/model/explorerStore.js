// src/entities/data-explorer/model/explorerStore.js
/**
 * Denna Pinia-store är hjärnan i Data Explorer-modulen.
 * Den hanterar all state, inklusive datainhämtning, filtrering, sortering,
 * paginering och CSV-export.
 *
 * KORRIGERING:
 * - Nycklarna som används för att destrukturera data från `fetchExplorerData` har
 *   korrigerats för att exakt matcha det API-kontrakt som producenten levererar.
 *   Detta löser felet där både data och klassificeringar inte laddades korrekt.
 * - Import-sökvägar har refaktorerats till absoluta sökvägar.
 */
import { defineStore } from 'pinia';
import { fetchExplorerData } from '@/entities/data-explorer/api/fetchExplorerData.js';
import { transformAndClassifyData } from '@/entities/data-explorer/lib/transformer.js';

export const useExplorerStore = defineStore('explorer', {
  // State: Definierar all reaktiv data för modulen.
  state: () => ({
    dataType: 'tonearms', // 'tonearms' or 'cartridges'
    
    // Berikad data och klassificeringar som hämtas från API
    pickupsData: [],
    tonearmsData: [],
    pickupClassifications: {},
    tonearmClassifications: {},

    // Filter-state
    searchTerm: '',
    categoryFilters: {}, // ex: { bearing_type: 'unipivot', arm_shape: 's_shape' }
    numericFilters: {
      effective_mass_g: { min: null, max: null },
      effective_length_mm: { min: null, max: null },
      weight_g: { min: null, max: null },
      cu_dynamic_10hz: { min: null, max: null },
    },

    // Sortering och paginering
    sortKey: 'manufacturer',
    sortOrder: 'asc',
    currentPage: 1,
    itemsPerPage: 20,

    // Laddning och felhantering
    isLoading: true,
    error: null,
  }),

  // Getters: Beräknade värden baserade på state.
  getters: {
    // Returnerar den aktiva datamängden baserat på dataType.
    activeData(state) {
      return state.dataType === 'tonearms' ? state.tonearmsData : state.pickupsData;
    },

    // Den centrala gettern som utför all filtrering och sortering.
    filteredResults(state) {
      if (!this.activeData) return [];

      let results = this.activeData;

      // 1. Sökfiltrering (Sökterm)
      if (state.searchTerm) {
        const term = state.searchTerm.toLowerCase();
        results = results.filter(item =>
          item.manufacturer?.toLowerCase().includes(term) ||
          item.model?.toLowerCase().includes(term)
        );
      }

      // 2. Kategorifiltrering
      for (const key in state.categoryFilters) {
        const value = state.categoryFilters[key];
        if (value) {
          results = results.filter(item => item[key] === value);
        }
      }

      // 3. Numerisk filtrering
      for (const key in state.numericFilters) {
        const { min, max } = state.numericFilters[key];
        if (min !== null || max !== null) {
          results = results.filter(item => {
            const value = item[key];
            if (value === null || value === undefined) return false;
            const isAboveMin = min === null || value >= min;
            const isBelowMax = max === null || value <= max;
            return isAboveMin && isBelowMax;
          });
        }
      }

      // 4. Sortering
      if (state.sortKey) {
        results.sort((a, b) => {
          let valA = a[state.sortKey];
          let valB = b[state.sortKey];

          if (valA === null || valA === undefined) return 1;
          if (valB === null || valB === undefined) return -1;

          if (typeof valA === 'string') {
            valA = valA.toLowerCase();
            valB = valB.toLowerCase();
          }

          if (valA < valB) return state.sortOrder === 'asc' ? -1 : 1;
          if (valA > valB) return state.sortOrder === 'asc' ? 1 : -1;
          return 0;
        });
      }

      return results;
    },

    // Beräknar totalt antal sidor för paginering.
    totalPages(state) {
      return Math.ceil(this.filteredResults.length / state.itemsPerPage);
    },

    // Returnerar den del av resultaten som ska visas på den aktuella sidan.
    paginatedResults(state) {
      const start = (state.currentPage - 1) * state.itemsPerPage;
      const end = start + state.itemsPerPage;
      return this.filteredResults.slice(start, end);
    },

    // Räknar totalt antal träffar.
    totalResultsCount() {
      return this.filteredResults.length;
    }
  },

  // Actions: Funktioner som kan ändra state.
  actions: {
    // Initierar hela modulen genom att hämta all nödvändig data.
    async initialize() {
      this.isLoading = true;
      this.error = null;
      try {
        const data = await fetchExplorerData();
        
        // KORRIGERING: Använder korrekta nycklar från `data`-objektet.
        this.pickupsData = transformAndClassifyData(data.pickupsData, data.pickupClassifications);
        this.tonearmsData = transformAndClassifyData(data.tonearmsData, data.tonearmsClassifications);
        
        this.pickupClassifications = data.pickupClassifications;
        this.tonearmClassifications = data.tonearmsClassifications;

      } catch (err) {
        this.error = 'Failed to load component data. Please try again later.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    // Sätter den aktiva datatypen och återställer filter.
    setDataType(type) {
      if (this.dataType !== type) {
        this.dataType = type;
        this.resetFilters();
        this.sortKey = 'manufacturer';
        this.sortOrder = 'asc';
      }
    },

    // Hanterar sorteringslogik.
    setSortKey(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
    },

    // Navigerar till nästa sida.
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },

    // Navigerar till föregående sida.
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },

    // Återställer alla filter till deras ursprungliga värden.
    resetFilters() {
      this.searchTerm = '';
      this.categoryFilters = {};
      for (const key in this.numericFilters) {
        this.numericFilters[key] = { min: null, max: null };
      }
      this.currentPage = 1;
    },

    // Exporterar den filtrerade datan till en CSV-fil.
    exportToCSV() {
      const data = this.filteredResults;
      if (data.length === 0) return;

      const headers = Object.keys(data[0]);
      const csvRows = [headers.join(',')];

      for (const row of data) {
        const values = headers.map(header => {
          let value = row[header];
          if (value === null || value === undefined) {
            return '';
          }
          if (typeof value === 'string') {
            value = `"${value.replace(/"/g, '""')}"`;
          }
          if (Array.isArray(value)) {
            value = `"${value.join('; ')}"`;
          }
          return value;
        });
        csvRows.push(values.join(','));
      }

      const blob = new Blob([csvRows.join('\n')], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('hidden', '');
      a.setAttribute('href', url);
      a.setAttribute('download', `engrove_data_export_${this.dataType}.csv`);
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
  },
});
// src/entities/data-explorer/model/explorerStore.js
