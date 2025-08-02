<!-- src/shared/ui/BaseTable.vue -->
<!--
  Detta är en grundläggande, agnostisk och återanvändbar tabellkomponent.
  Den är en del av det centrala UI-biblioteket och är designad för att visa
  godtycklig data. Komponenten är fullt responsiv och anpassar sig nu till en
  "fixed-column scroll"-layout på mindre skärmar. Den hanterar sortering och radklick
  via events.

  UPPDATERING (Steg 2):
  - Lade till en ny metod `getCellClass` och motsvarande CSS för att visuellt
    färgkoda specifika datavärden (t.ex. hög/låg compliance), vilket ökar
    tydligheten i datatabellen.

  KORRIGERING (Alter Ego):
  - `formatValue`-funktionen har refaktorerats för att vara mer intelligent.
  - Den applicerar inte längre en generell versaliseringsregel på all text.
  - Egennamn som 'manufacturer' och 'model' lämnas nu orörda.
  - Formatering (ersätta '_' och versalisera första bokstaven) appliceras
    endast på specifika, kända klassificeringsnycklar för att undvika
    felaktig formatering av namn som "Schröder".
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
          @keydown.enter="$emit('row-click', item)"
          @keydown.space.prevent="$emit('row-click', item)"
        >
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

const emit = defineEmits(['sort', 'row-click']);

// Lista över nycklar som innehåller ID:n och bör formateras.
const keysToFormat = [
  'type_name', 'stylus_family_name', 'bearing_type_name', 
  'arm_shape_name', 'arm_material_name'
];

const emitSort = (key) => {
  emit('sort', key);
};

/**
 * Returnerar en CSS-klass för en cell baserat på dess nyckel och värde.
 * Används för visuell datakonditionering.
 * @param {string} key - Kolumnens nyckel.
 * @param {Object} item - Hela dataobjektet för raden.
 * @returns {string|null} CSS-klassen som ska appliceras, eller null.
 */
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
  
  // Om värdet är en sträng och nyckeln finns i vår formateringslista,
  // applicera den specifika transformeringslogiken.
  if (typeof value === 'string' && keysToFormat.includes(key)) {
    // Ersätt understreck och versalisera första bokstaven i varje ord.
    const formatted = value.replace(/_/g, ' ');
    return formatted.replace(/\b\w/g, l => l.toUpperCase());
  }

  // För alla andra värden (inklusive 'manufacturer' och 'model'),
  // returnera dem oförändrade.
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

/* Styling för datakonditionering */
.value--low {
  color: var(--color-graph-series-4); /* Amber/Yellow */
}

.value--high {
  color: var(--color-status-error); /* Red */
}

/* Responsiv "Fixed-Column Scroll" layout för mindre skärmar */
@media (max-width: 768px) {
  /* Gör den första kolumnen (både header och data) "sticky" */
  th:first-child,
  td:first-child {
    position: sticky;
    left: 0;
    z-index: 1;
    
    /*
      Sätt en solid bakgrundsfärg för att dölja innehållet som scrollar under.
      Vi använder --color-surface-secondary för datakolumnen för att matcha radens färg
      och --color-surface-tertiary för header-kolumnen för att matcha headerns färg.
    */
    background-color: var(--color-surface-secondary);
  }

  th:first-child {
    background-color: var(--color-surface-tertiary);
  }

  /* Lägg till en subtil skugga för att visuellt indikera att mer innehåll finns till höger */
  th:first-child,
  td:first-child {
    box-shadow: inset -4px 0 4px -4px rgba(0, 0, 0, 0.2);
  }
}
</style>
<!-- src/shared/ui/BaseTable.vue -->
