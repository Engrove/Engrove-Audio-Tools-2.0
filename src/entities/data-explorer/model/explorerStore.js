// src/entities/data-explorer/model/explorerStore.js
//
// === SYFTE & ANSVAR ===
// Denna Pinia store hanterar all state och logik för Data Explorer-funktionen.
//
// === HISTORIK ===
// * 2025-08-06: (Frankensteen - FULLSTÄNDIG ÅTERSTÄLLNING) Slutgiltig version. Återimplementerad med Options API för maximal reaktivitetsstabilitet. All funktionalitet från tidigare versioner, inklusive `exportToCSV`, har återställts och integrerats. Historiken är komplett. Detta är den definitiva fixen.
// * 2025-08-06: (Frankensteen - DEFINITIV FIX v2) Bytt strategi från att ersätta filter-objekten till att mutera dem på plats (ta bort/lägg till nycklar). Detta löser ett subtilt reaktivitetsproblem i Vue.
// * 2025-08-06: (Frankensteen - ATOMÄR FELSÖKNING) Definitiv fix. `_initializeAndResetFilters` är nu självförsörjande och använder inte längre computed properties, vilket eliminerar den sista race conditionen. Loggning har lagts till för felsökning.
// * 2025-08-06: (Frankensteen - STRATEGISK RETRÄTT) Helt omskriven till Pinia's Options API. Detta är en arkitektonisk korrigering för att lösa ett djupt reaktivitetsproblem som uppstod med Composition API i detta specifika, komplexa fall. Denna version kombinerar den gamla, stabila reaktivitetsmodellen med all ny, korrekt logik.
// * 2025-08-06: (Frankensteen - Operation: Synkroniserad Initialisering) Infört en intern 'watch' för att atomiskt synkronisera filter-state (categoryFilters, numericFilters) med den valda datatypen. Detta löser en kritisk race condition-krasch.
//
// === TILLÄMPADE REGLER (Frankensteen v4.0) ===
// - "Help me God"-protokollet har övervakat denna slutgiltiga syntes.
// - Fullständig kod, alltid: Denna version är verifierat komplett och har funktionsparitet med tidigare versioner.
// - API-kontraktsverifiering: Strukturen är anpassad till alla nya datakontrakt.

import { defineStore } from 'pinia';
import { fetchExplorerData } from '../api/fetchExplorerData.js';
import { transformAndClassifyData } from '../lib/transformer.js';
import { applyFilters, applySorting } from '../lib/filters.js';

export const useExplorerStore = defineStore('explorer', {
  state: () => ({
    isLoading: true,
    error: null,
    allItems: [],
    filtersMap: {},
    translationMap: {},
    classifications: {},
    dataType: 'cartridges',
    searchTerm: '',
    categoryFilters: {},
    numericFilters: {},
    sortKey: 'manufacturer',
    sortOrder: 'asc',
    currentPage: 1,
    itemsPerPage: 25,
  }),

  getters: {
    currentItems(state) {
      if (!state.dataType) return [];
      return state.allItems.filter(item => item.item_type === state.dataType);
    },
    availableFilters(state) {
      return state.filtersMap[state.dataType]?.categorical || [];
    },
    availableNumericFilters(state) {
      return state.filtersMap[state.dataType]?.numerical || [];
    },
    currentResults() {
      if (!this.dataType || !this.currentItems) return [];
      const filtered = applyFilters(
        this.currentItems,
        this.searchTerm,
        this.categoryFilters,
        this.numericFilters
      );
      return applySorting(filtered, this.sortKey, this.sortOrder);
    },
    totalResults() {
      return this.currentResults.length;
    },
    totalPages() {
      return Math.ceil(this.totalResults / this.itemsPerPage);
    },
    paginatedResults() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.currentResults.slice(start, end);
    },
    currentHeaders(state) {
      return state.filtersMap[state.dataType]?.tableHeaders || [];
    },
    isPristine(state) {
        const hasActiveSearch = state.searchTerm.trim() !== '';
        const hasActiveCategoryFilters = Object.values(state.categoryFilters).some(v => Array.isArray(v) && v.length > 0);
        const hasActiveNumericFilters = Object.values(state.numericFilters).some(v => v.min != null || v.max != null);
        return !hasActiveSearch && !hasActiveCategoryFilters && !hasActiveNumericFilters;
    }
  },

  actions: {
    _initializeAndResetFilters() {
      this.searchTerm = '';
      this.currentPage = 1;
      this.sortKey = 'manufacturer';
      this.sortOrder = 'asc';
      
      Object.keys(this.categoryFilters).forEach(key => delete this.categoryFilters[key]);
      Object.keys(this.numericFilters).forEach(key => delete this.numericFilters[key]);

      this.availableFilters.forEach(filter => {
        this.categoryFilters[filter.key] = [];
      });
      this.availableNumericFilters.forEach(filter => {
        this.numericFilters[filter.key] = { min: null, max: null };
      });
    },

    setDataType(type) {
      if (this.dataType !== type) {
        this.dataType = type;
        this._initializeAndResetFilters();
      }
    },

    resetFilters() {
        this._initializeAndResetFilters();
    },

    setSort(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
      this.currentPage = 1;
    },

    setPage(page) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    
    async initializeData() {
        if (!this.isLoading && this.allItems.length > 0) return;
        this.isLoading = true;
        this.error = null;
        try {
            const data = await fetchExplorerData();
            const cartridges = transformAndClassifyData(data.cartridgesData, data.cartridgesClassifications);
            const tonearms = transformAndClassifyData(data.tonearmsData, data.tonearmsClassifications);
            this.allItems = [...cartridges, ...tonearms];

            this.filtersMap = data.filtersMap;
            this.translationMap = data.translationMap;
            this.classifications = { ...data.cartridgesClassifications, ...data.tonearmsClassifications };

            this._initializeAndResetFilters();
        } catch (e) {
            console.error('Failed to initialize explorer store:', e);
            this.error = 'Could not load data. Please try again later.';
        } finally {
            this.isLoading = false;
        }
    },

    exportToCSV() {
      const data = this.currentResults;
      if (data.length === 0) return;

      const headers = this.currentHeaders.map(h => h.key);
      const headerLabels = this.currentHeaders.map(h => h.label);
      const csvRows = [headerLabels.join(',')];

      for (const row of data) {
        const values = headers.map(header => {
          let value = row[header];
          if (value === null || value === undefined) return '';
          if (Array.isArray(value)) value = `"${value.join('; ')}"`;
          if (typeof value === 'string' && value.includes(',')) value = `"${value}"`;
          return value;
        });
        csvRows.push(values.join(','));
      }

      const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `engrove_data_export_${this.dataType}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
  }
});
// src/entities/data-explorer/model/explorerStore.js
