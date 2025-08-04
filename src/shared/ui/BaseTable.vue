<!-- src/shared/ui/BaseTable.vue -->
<template>
  <div class="base-table-container">
    <table>
      <thead>
        <tr>
          <th v-if="showSelection" class="selection-header">
            <BaseCheckbox
              :model-value="allVisibleItemsSelected"
              @update:modelValue="$emit('toggle-select-all-visible')"
              title="Select all visible items"
              aria-label="Select all visible items"
            />
          </th>
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
          <td v-if="showSelection" class="selection-cell" @click.stop>
             <BaseCheckbox
              :model-value="isItemSelected(item.id)"
              @update:modelValue="$emit('toggle-item-selection', item)"
              :disabled="!isItemSelected(item.id) && selectionLimitReached"
              :title="!isItemSelected(item.id) && selectionLimitReached ? 'Comparison limit reached' : `Select ${item.manufacturer} ${item.model}`"
              :aria-label="`Select ${item.manufacturer} ${item.model}`"
            />
          </td>
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
// 2025-08-05: Corrected by Frankensteen after faulty implementation.
//             - Merged selection functionality with the correct, advanced base version.
//             - Preserved all existing logic: `formatValue`, `getCellClass`, sticky columns, etc.
//             - Added props: `showSelection`, `isItemSelected`, `selectionLimitReached`, `allVisibleItemsSelected`.
//             - Added emits: `toggle-item-selection`, `toggle-select-all-visible`.
//

// =============================================
// Instruktioner vid skapande av fil
// =============================================
// Kärndirektiv: Fullständig kod, alltid. Inga genvägar.
// Principen "Explicit Alltid": Villkorlig rendering och klasser är tydliga.
// API-kontraktsverifiering: Nya props och emits är additiva och bryter inga gamla kontrakt.
// Red Team Alter Ego-granskning: Denna version är en korrekt sammanslagning, inte en ersättning.
//

import BaseCheckbox from '@/shared/ui/BaseCheckbox.vue';

const props = defineProps({
  headers: { type: Array, required: true },
  items: { type: Array, required: true },
  sortKey: { type: String, default: '' },
  sortOrder: {
    type: String,
    default: 'asc',
    validator: (value) => ['asc', 'desc'].includes(value),
  },
  // --- New props for selection ---
  showSelection: { type: Boolean, default: false },
  isItemSelected: { type: Function, default: () => false },
  selectionLimitReached: { type: Boolean, default: false },
  allVisibleItemsSelected: { type: Boolean, default: false },
});

const emit = defineEmits(['sort', 'row-click', 'toggle-item-selection', 'toggle-select-all-visible']);

const keysToFormat = ['type_name', 'stylus_family_name', 'bearing_type_name', 'arm_shape_name', 'arm_material_name'];

const emitSort = (key) => {
  emit('sort', key);
};

const getCellClass = (key, item) => {
  const value = item[key];
  if (value === null || value === undefined) return null;
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
  if (value === null || value === undefined) return '–';
  if (typeof value === 'string' && keysToFormat.includes(key)) {
    const formatted = value.replace(/_/g, ' ');
    return formatted.replace(/\b\w/g, l => l.toUpperCase());
  }
  return value;
};

const getAriaSort = (header) => {
  if (!header.sortable) return null;
  if (props.sortKey !== header.key) return 'none';
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
  background-color: var(--surface-secondary);
}

table {
  width: 100%;
  border-collapse: collapse;
}

/* Tabellhuvud (thead) */
thead tr {
  background-color: var(--surface-tertiary);
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
  color: var(--graph-series-4); /* Amber/Yellow */
}

.value--high {
  color: var(--status-error); /* Red */
}

/* Styling för urvalskolumn */
.selection-header, .selection-cell {
  width: 1%;
  padding-right: var(--spacing-2);
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
  th:first-child,
  td:first-child {
    position: sticky;
    left: 0;
    z-index: 1;
    background-color: var(--surface-secondary);
  }

  /* Justera för urvalskolumnen om den visas */
  th.selection-header + th,
  td.selection-cell + td {
    position: sticky;
    left: 50px; /* Bredd på urvalskolumnen, kan behöva justeras */
    z-index: 1;
    background-color: var(--surface-secondary);
  }

  th:first-child {
    background-color: var(--surface-tertiary);
  }
  
  th.selection-header + th {
    background-color: var(--surface-tertiary);
  }

  th:first-child,
  td:first-child {
    box-shadow: inset -4px 0 4px -4px rgba(0, 0, 0, 0.2);
  }
}
</style>
<!-- src/shared/ui/BaseTable.vue -->
