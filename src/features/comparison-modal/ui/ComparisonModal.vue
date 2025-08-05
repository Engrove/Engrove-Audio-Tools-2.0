<!-- src/features/comparison-modal/ui/ComparisonModal.vue -->
<template>
  <BaseModal :show="show" @close="emit('close')" :max-width="'max-w-6xl'">
    <div class="comparison-modal" v-if="selectedItems.length > 0">
      <header class="comparison-modal__header">
        <h1 class="comparison-modal__title">Item Comparison</h1>
        <p class="comparison-modal__subtitle">
          Comparing {{ selectedItems.length }} {{ selectedItems.length === 1 ? 'item' : 'items' }}
        </p>
      </header>

      <main class="comparison-modal__content">
        <BaseTable
          :headers="tableHeaders"
          :items="transposedData"
        >
          <!-- Custom cell rendering for values -->
          <template v-for="item in selectedItems" :key="item.id" v-slot:[`cell-${item.id}`]="{ item: row }">
            {{ row[item.id] !== undefined ? row[item.id] : '–' }}
          </template>
        </BaseTable>
      </main>

    </div>
  </BaseModal>
</template>

<script setup>
// =============================================
// File history
// =============================================
// 2025-08-04: Created by Frankensteen for Steg 23, Fas 3.
//             - Final component for the comparison feature.
//             - Fetches selected item data from explorerStore and comparisonStore.
//             - Contains the core logic to transpose data for side-by-side comparison.
//             - Dynamically generates headers and rows for BaseTable.
//

// =============================================
// Instruktioner vid skapande av fil
// =============================================
// Kärndirektiv: Fullständig kod, alltid. Inga genvägar.
// Principen "Explicit Alltid": Logiken hanterar fall där data saknas explicit.
// API-kontraktsverifiering: Interagerar korrekt med två stores och har ett enkelt yttre API.
// Red Team Alter Ego-granskning: Datatransponeringen är den mest komplexa delen och har granskats för att vara robust mot saknad data.
//

import { computed } from 'vue';
import { useComparisonStore } from '@/entities/comparison/model/comparisonStore';
import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore';
import BaseModal from '@/shared/ui/BaseModal.vue';
import BaseTable from '@/shared/ui/BaseTable.vue';

// =============================================
// Component Interface (Props & Emits)
// =============================================
const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['close']);

// =============================================
// Store Initialization
// =============================================
const comparisonStore = useComparisonStore();
const explorerStore = useExplorerStore();

// =============================================
// Data Fetching and Transformation
// =============================================

// A curated list of properties to compare.
const propertiesToCompare = [
  { key: 'manufacturer', label: 'Manufacturer' },
  { key: 'model', label: 'Model' },
  { key: 'type', label: 'Type' },
  { key: 'weight_g', label: 'Weight (g)' },
  { key: 'effective_mass_g', label: 'Effective Mass (g)' },
  { key: 'output_voltage_mv', label: 'Output (mV)' },
  { key: 'compliance_dynamic_10hz', label: 'Compliance (10Hz)' },
  { key: 'tracking_force_g', label: 'Tracking Force (g)' },
  { key: 'internal_impedance_ohms', label: 'Impedance (Ω)' },
  { key: 'stylus_type', label: 'Stylus' },
  { key: 'tags', label: 'Tags' },
];

// Get the full data objects for the selected items.
const selectedItems = computed(() => {
  return comparisonStore.selectedItemIds
    .map(id => explorerStore.allItems.find(item => item.id === id))
    .filter(item => item !== undefined); // Filter out any potential undefined items
});

// Dynamically generate the table headers for BaseTable.
const tableHeaders = computed(() => {
  if (selectedItems.value.length === 0) {
    return [];
  }
  const itemHeaders = selectedItems.value.map(item => ({
    key: item.id,
    label: `${item.manufacturer} ${item.model}`,
    sortable: false,
  }));
  return [
    { key: 'property', label: 'Specification', sortable: false },
    ...itemHeaders,
  ];
});

// The core logic: transpose the data for side-by-side view.
const transposedData = computed(() => {
  if (selectedItems.value.length === 0) {
    return [];
  }

  return propertiesToCompare.map(propInfo => {
    const row = {
      id: propInfo.key, // Use key as a unique ID for the row
      property: propInfo.label,
    };

    selectedItems.value.forEach(item => {
      let value = item[propInfo.key];
      // Handle array values like 'tags'
      if (Array.isArray(value)) {
        value = value.join(', ');
      }
      row[item.id] = value;
    });

    return row;
  });
});

</script>

<style scoped>
.comparison-modal {
  padding: var(--spacing-6);
  color: var(--text-medium-emphasis);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-5);
}

.comparison-modal__header {
  border-bottom: 1px solid var(--border-primary);
  padding-bottom: var(--spacing-4);
}

.comparison-modal__title {
  color: var(--text-high-emphasis);
  font-size: var(--font-size-h2);
  font-weight: var(--font-weight-bold);
}

.comparison-modal__subtitle {
  font-size: var(--font-size-body);
  color: var(--text-low-emphasis);
  margin-top: var(--spacing-1);
}

.comparison-modal__content {
  max-height: 70vh;
  overflow-y: auto;
}

/* Make the BaseTable header sticky inside the modal */
.comparison-modal__content :deep(thead th) {
  position: sticky;
  top: 0;
  z-index: 2; /* Needs to be higher than table content */
}
</style>
<!-- src/features/comparison-modal/ui/ComparisonModal.vue -->
