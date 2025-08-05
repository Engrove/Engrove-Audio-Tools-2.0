<!-- src/shared/ui/BaseTable.vue -->
<template>
  <div class="base-table-container">
    <table>
      <thead>
        <tr>
          <!-- New: Selection Header -->
          <th v-if="showSelection" class="selection-header">
            <BaseCheckbox
              :model-value="allVisibleItemsSelected"
              @update:modelValue="$emit('toggle-select-all-visible')"
              title="Select all visible items"
            />
          </th>
          <!-- Existing: Data Headers -->
          <th
            v-for="header in headers"
            :key="header.key"
            @click="header.sortable ? emitSort(header.key) : null"
            :class="{ 
              sortable: header.sortable, 
              active: sortKey === header.key 
            }"
            :aria-sort="getAriaSort(header)"
          >
            {{ header.label }}
            <span v-if="sortKey === header.key" class="sort-arrow">
              {{ sortOrder === 'asc' ? '▲' : '▼' }}
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="items.length === 0">
          <td :colspan="headers.length + (showSelection ? 1 : 0)" class="no-results">
            No items match the current criteria.
          </td>
        </tr>
        <tr
          v-else
          v-for="item in items"
          :key="item.id"
          @click="$emit('row-click', item)"
          class="clickable-row"
          tabindex="0"
          @keydown.enter="$emit('row-click', item)"
          @keydown.space.prevent="$emit('row-click', item)"
        >
          <!-- New: Selection Cell -->
          <td v-if="showSelection" class="selection-cell" @click.stop>
             <BaseCheckbox
              :model-value="isItemSelected(item)"
              @update:modelValue="$emit('toggle-item-selection', item)"
              :disabled="!isItemSelected(item) && selectionLimitReached"
              :title="!isItemSelected(item) && selectionLimitReached ? 'Comparison limit reached' : `Select item for comparison`"
            />
          </td>
          <!-- Existing: Data Cells -->
          <td
            v-for="header in headers"
            :key="`${item.id}-${header.key}`"
            :data-label="header.label"
            :class="getCellClass(header.key, item)"
          >
            {{ formatValue(item, header.key) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
// =============================================
// File history
// =============================================
// Previously: A robust, styleable, and sortable table component.
// 2025-08-04: Merged by Frankensteen for Steg 23, Fas 3.
//             - Integrated selection functionality for item comparison.
//             - This is a corrected merge, based on the full-featured original file.
//             - Added new props: `showSelection`, `isItemSelected`, `selectionLimitReached`, `allVisibleItemsSelected`.
//             - Added new emits: `toggle-item-selection`, `toggle-select-all-visible`.
//             - All previous functionality (`formatValue`, `getCellClass`, etc.) is preserved.
//

// =============================================
// Instruktioner vid skapande av fil
// =============================================
// Kärndirektiv: Fullständig kod, alltid. Inga genvägar.
// Principen "Explicit Alltid": v-if används för tydlig villkorlig rendering.
// API-kontraktsverifiering: Befintligt och nytt kontrakt är sammanslagna och tydliga.
// Red Team Alter Ego-granskning: Sammanslagningen är verifierad. Inga funktioner har tagits bort.
// Obligatorisk Refaktorisering: Ingen, befintlig logik var redan välstrukturerad.
//

import BaseCheckbox from '@/shared/ui/BaseCheckbox.vue';

// =============================================
// Component Interface (Props & Emits)
// =============================================
const props = defineProps({
  // Existing Props
  headers: {
    type: Array,
    required: true,
  },
  items: {
    type: Array,
    required: true,
  },
  sortKey: {
    type: String,
    default: '',
  },
  sortOrder: {
    type: String,
    default: 'asc',
    validator: (value) => ['asc', 'desc'].includes(value),
  },
  // New Props for Selection
  showSelection: {
    type: Boolean,
    default: false,
  },
  isItemSelected: {
    type: Function,
    default: () => false,
  },
  selectionLimitReached: {
    type: Boolean,
    default: false,
  },
  allVisibleItemsSelected: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['sort', 'row-click', 'toggle-item-selection', 'toggle-select-all-visible']);

// =============================================
// Existing Logic (Preserved)
// =============================================

// Lista över nycklar som innehåller ID:n och bör formateras.
const keysToFormat = [
  'type_name', 'stylus_family_name', 'bearing_type_name', 
  'arm_shape_name', 'arm_material_name'
];

const emitSort = (key) => {
  emit('sort', key);
};

const getCellClass = (key, item) => {
  const value = item[key];
  if (value === null || value === undefined) {
    return null;
  }

  switch (key) {
    case 'cu_dynamic_10hz':
      if (value < 12) return 'value--low';
      if (value > 20) return 'value--high';
      break;
    case 'effective_mass_g':
      if (value < 10) return 'value--low';
      if (value > 20) return 'value--high';
      break;
    default:
      return null;
  }
  return null;
};

const formatValue = (item, key) => {
  const value = item[key];

  if (value === null || value === undefined) {
    return '–';
  }
  
  if (typeof value === 'string' && keysToFormat.includes(key)) {
    const formatted = value.replace(/_/g, ' ');
    return formatted.replace(/\b\w/g, l => l.toUpperCase());
  }

  return value;
};

const getAriaSort = (header) => {
  if (!header.sortable) {
    return null;
  }
  if (props.sortKey !== header.key) {
    return 'none';
  }
  return props.sortOrder === 'asc' ? 'ascending' : 'descending';
};
</script>

<style scoped>
/* Grundläggande container och tabellstyling */
.base-table-container {
  overflow-x: auto;
  width: 100%;
  border: 1px solid var(--border-primary);
  border-radius: var(--border-radius-large);
  background-color: var(--surface-primary);
}

table {
  width: 100%;
  border-collapse: collapse;
}

/* Tabellhuvud (thead) */
thead tr {
  background-color: var(--surface-secondary);
}

th {
  padding: 12px 15px;
  text-align: left;
  white-space: nowrap;
  font-family: var(--font-family-body);
  font-size: var(--font-size-label);
  font-weight: var(--font-weight-semibold);
  color: var(--text-high-emphasis);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border-primary);
}

th.sortable {
  cursor: pointer;
  transition: color 0.2s ease;
}

th.sortable:hover {
  color: var(--interactive-accent);
}

th.active {
  color: var(--interactive-accent);
}

.sort-arrow {
  font-size: 0.8em;
  margin-left: 6px;
  vertical-align: middle;
}

/* Tabellkropp (tbody) */
td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid var(--border-primary);
  color: var(--text-medium-emphasis);
  font-family: var(--font-family-data);
  font-size: var(--font-size-data);
}

tbody tr:last-child td {
  border-bottom: none;
}

.clickable-row {
  transition: background-color 0.2s ease;
}

.clickable-row:hover {
  background-color: var(--surface-tertiary);
  cursor: pointer;
}

.clickable-row:focus {
    outline: 2px solid var(--interactive-accent);
    outline-offset: -2px;
}

.no-results {
  text-align: center;
  padding: 3rem;
  font-style: italic;
  font-family: var(--font-family-body);
}

/* Styling för datakonditionering */
.value--low {
  color: var(--color-graph-series-4, #FFCB6B); /* Amber/Yellow, with fallback */
}

.value--high {
  color: var(--color-status-error, #F44336); /* Red, with fallback */
}

/* New: Selection Column Styling */
.selection-header,
.selection-cell {
  width: 1%;
  padding: 0 5px 0 15px; /* Tighter padding for checkbox column */
}

.selection-cell {
  cursor: default;
}

.selection-header :deep(.base-checkbox-container),
.selection-cell :deep(.base-checkbox-container) {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  margin: 0;
}


/* Responsiv "Fixed-Column Scroll" layout för mindre skärmar */
@media (max-width: 768px) {
  /* This selector makes the first column sticky. If selection is shown, it's the selection.
     If not, it's the first data column. */
  th:first-child,
  td:first-child {
    position: sticky;
    left: 0;
    z-index: 1;
    background-color: var(--surface-secondary);
  }

  th:first-child {
    background-color: var(--surface-tertiary);
  }

  th:first-child,
  td:first-child {
    box-shadow: inset -4px 0 4px -4px rgba(0, 0, 0, 0.2);
  }
}
</style>
<!-- src/shared/ui/BaseTable.vue -->
