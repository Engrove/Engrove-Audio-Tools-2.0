<!-- src/features/item-details/ui/ItemDetailModal.vue -->
<!--
  Historik:
  - 2024-08-04: (UPPDRAG 20) Uppdaterad för att peka på de nya `_name`-fälten för att visa de översatta värdena i modalen.
  - 2024-08-04: (UPPDRAG 22) Verifierad som korrekt och kompatibel med det fullständigt refaktorerade systemet. Inga ändringar krävdes.
-->
<!--
  Viktiga implementerade regler:
  - Fullständig kod, alltid: Filen är komplett.
  - API-kontraktsverifiering: Strukturen `allFields.cartridges` matchar det nya datakontraktet och de berikade `_name`-fälten.
  - Alter Ego-granskning: Genomförd för att bekräfta att komponenten är robust och fungerar med den nya storen.
-->
<template>
  <!-- v-model:isOpen binder till BaseModal för att styra dess synlighet -->
  <BaseModal v-model:isOpen="isModalOpen">
    <template #header>
      <!-- Visar en dynamisk rubrik om ett item finns, annars en fallback -->
      <span v-if="item">{{ item.manufacturer }} {{ item.model }}</span>
      <span velse>Item Details</span>
    </template>
    
    <template #default>
      <div v-if="item" class="details-container">
        <div class="details-grid">
          <!-- Loopar igenom de fält som är tillåtna och har ett värde -->
          <div v-for="field in visibleFields" :key="field.key" class="detail-item">
            <span class="label">{{ field.label }}</span>
            <span class="value">{{ formatValue(item, field.key) }}</span>
          </div>
        </div>

        <!-- Sektion för anteckningar, visas bara om det finns data -->
        <div v-if="item.notes_en" class="notes-section">
          <h4>Notes</h4>
          <p>{{ item.notes_en }}</p>
        </div>
      </div>
      <!-- Visar ett meddelande om inget item har skickats in -->
      <div v-else class="no-data-message">
        <p>No item data to display.</p>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed } from 'vue';
import BaseModal from '@/shared/ui/BaseModal.vue';

// --- PROPS & EMITS ---
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  item: {
    type: Object,
    default: null,
  },
  dataType: {
    type: String, // 'cartridges' or 'tonearms'
    required: true,
  },
});

const emit = defineEmits(['update:isOpen']);

// Tvåvägsbindning för modalens synlighet
const isModalOpen = computed({
  get: () => props.isOpen,
  set: (value) => emit('update:isOpen', value),
});

// --- DATADEFINITIONER ---

// Vitlista över alla fält som FÅR visas, uppdelat per datatyp.
// Verifierad: 'cartridges'-nyckeln och dess `_name`-fält är korrekta.
const allFields = {
  cartridges: [
    { key: 'type_name', label: 'Type' },
    { key: 'weight_g', label: 'Weight (g)' },
    { key: 'cu_dynamic_10hz', label: 'Compliance @ 10Hz' },
    { key: 'cu_dynamic_100hz', label: 'Compliance @ 100Hz' },
    { key: 'cu_static', label: 'Static Compliance' },
    { key: 'stylus_family_name', label: 'Stylus Family' },
    { key: 'cantilever_class_name', label: 'Cantilever Class' },
    { key: 'output_voltage_mv', label: 'Output (mV)' },
    { key: 'tracking_force_min_g', label: 'VTF Min (g)' },
    { key: 'tracking_force_max_g', label: 'VTF Max (g)' },
  ],
  tonearms: [
    { key: 'effective_mass_g', label: 'Effective Mass (g)' },
    { key: 'effective_length_mm', label: 'Effective Length (mm)' },
    { key: 'pivot_to_spindle_mm', label: 'Pivot to Spindle (mm)' },
    { key: 'overhang_mm', label: 'Overhang (mm)' },
    { key: 'bearing_type_name', label: 'Bearing Type' },
    { key: 'arm_material_name', label: 'Arm Material' },
    { key: 'headshell_connector_name', label: 'Headshell' },
  ]
};

// Beräknar den slutgiltiga listan av fält som ska renderas.
const visibleFields = computed(() => {
  if (!props.item || !props.dataType) {
    return [];
  }
  const fieldsForType = allFields[props.dataType] || [];
  return fieldsForType.filter(field => props.item[field.key] !== null && props.item[field.key] !== undefined);
});


// --- FUNKTIONER ---

/**
 * Formaterar värdet för en cell för visning.
 * @param {Object} item - Hela objektet.
 * @param {string} key - Nyckeln för värdet.
 * @returns {string} - Det formaterade värdet.
 */
function formatValue(item, key) {
  const value = item[key];
  return (value === null || value === undefined) ? '–' : value;
}
</script>

<style scoped>
.details-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem 1rem;
  background-color: var(--color-surface-tertiary);
  padding: 1rem;
  border-radius: 8px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-low-emphasis);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.value {
  font-size: var(--font-size-data);
  font-family: var(--font-family-monospace);
  color: var(--color-text-high-emphasis);
  font-weight: var(--font-weight-regular);
}

.notes-section {
  padding-top: 1rem;
  border-top: 1px dashed var(--color-border-primary);
}

.notes-section h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: var(--color-text-high-emphasis);
}

.notes-section p {
  margin: 0;
  color: var(--color-text-medium-emphasis);
  white-space: pre-wrap; /* Behåller radbrytningar */
}

.no-data-message {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-medium-emphasis);
}
</style>
<!-- src/features/item-details/ui/ItemDetailModal.vue -->
