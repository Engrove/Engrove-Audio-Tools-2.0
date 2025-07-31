<!-- src/shared/ui/BaseTable.vue -->
<!--
  Detta är en grundläggande, agnostisk och återanvändbar tabellkomponent.
  Den är en del av det centrala UI-biblioteket och är designad för att visa
  godtycklig data. Komponenten är fullt responsiv och anpassar sig till en
  "stackable"-layout på mindre skärmar. Den hanterar sortering och radklick
  via events.
-->
<template>
  <div class="base-table-container">
    <table>
      <thead>
        <tr>
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
          <td :colspan="headers.length" class="no-results">
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
        >
          <td
            v-for="header in headers"
            :key="`${item.id}-${header.key}`"
            :data-label="header.label"
          >
            {{ formatValue(item, header.key) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
// --- PROPS & EMITS ---

/**
 * @props {Array} headers - Konfiguration för tabellens kolumner.
 *   Exempel: [{ key: 'name', label: 'Name', sortable: true }]
 * @props {Array} items - Datan som ska visas i tabellen. Varje objekt måste ha en unik 'id'.
 * @props {String} sortKey - Nyckeln för den kolumn som för närvarande är sorterad.
 * @props {String} sortOrder - Sorteringsordningen ('asc' eller 'desc').
 */
const props = defineProps({
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
});

/**
 * @emits sort - Utlöses när en sorterbar kolumnrubrik klickas. Skickar med kolumnens nyckel.
 * @emits row-click - Utlöses när en rad i tabellen klickas. Skickar med hela radens item-objekt.
 */
const emit = defineEmits(['sort', 'row-click']);


// --- FUNKTIONER ---

/**
 * Skickar en 'sort'-händelse när en sorterbar rubrik klickas.
 * @param {string} key - Nyckeln för kolumnen som ska sorteras.
 */
const emitSort = (key) => {
  emit('sort', key);
};

/**
 * Formaterar värdet för en cell. Hanterar null/undefined och
 * specifika formateringsregler.
 * @param {Object} item - Hela objektet för den aktuella raden.
 * @param {string} key - Nyckeln för det specifika värdet i objektet.
 * @returns {string|number} - Det formaterade värdet.
 */
const formatValue = (item, key) => {
  const value = item[key];
  if (value === null || value === undefined) {
    return '–';
  }
  
  // Exempel på specifik formatering, kan expanderas vid behov.
  if (typeof value === 'string') {
    return value.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }

  return value;
};

/**
 * Ställer in aria-sort attributet för tillgänglighet.
 * @param {Object} header - Header-objektet.
 * @returns {string|null} - Värdet för aria-sort.
 */
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
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
  background-color: var(--color-surface-secondary);
}

table {
  width: 100%;
  border-collapse: collapse;
}

/* Tabellhuvud (thead) */
thead tr {
  background-color: var(--color-surface-tertiary);
}

th {
  padding: 12px 15px;
  text-align: left;
  white-space: nowrap;
  font-family: var(--font-family-primary);
  font-size: var(--font-size-label);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-high-emphasis);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--color-border-primary);
}

th.sortable {
  cursor: pointer;
  transition: color 0.2s ease;
}

th.sortable:hover {
  color: var(--color-interactive-accent);
}

th.active {
  color: var(--color-interactive-accent);
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
  border-bottom: 1px solid var(--color-border-primary);
  color: var(--color-text-medium-emphasis);
  font-family: var(--font-family-monospace);
  font-size: var(--font-size-data);
}

tbody tr:last-child td {
  border-bottom: none;
}

.clickable-row {
  transition: background-color 0.2s ease;
}

.clickable-row:hover {
  background-color: var(--color-surface-tertiary);
  cursor: pointer;
}

.clickable-row:focus {
    outline: 2px solid var(--color-interactive-accent);
    outline-offset: -2px;
}

.no-results {
  text-align: center;
  padding: 3rem;
  font-style: italic;
  font-family: var(--font-family-primary);
}

/* Responsiv "Stackable" layout för mindre skärmar */
@media (max-width: 768px) {
  thead {
    display: none;
  }

  tr {
    display: block;
    border-bottom: 2px solid var(--color-border-primary);
  }
  
  tr:last-child {
      border-bottom: none;
  }

  td {
    display: block;
    text-align: right;
    padding-left: 50%;
    position: relative;
    border-bottom: 1px solid var(--color-border-primary);
  }
  
  td:last-child {
      border-bottom: none;
  }

  td::before {
    content: attr(data-label);
    position: absolute;
    left: 15px;
    width: calc(50% - 30px);
    text-align: left;
    font-weight: var(--font-weight-medium);
    font-family: var(--font-family-primary);
    color: var(--color-text-high-emphasis);
  }
}

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR KOMPAKT LÄGE                                         */
/* ========================================================================== */
:global(.compact-theme) th,
:global(.compact-theme) td {
  padding: 8px 12px;
}

@media (max-width: 768px) {
  :global(.compact-theme) td::before {
    left: 12px; /* Matchar den nya horisontella paddingen */
  }
}
</style>
<!-- src/shared/ui/BaseTable.vue -->
