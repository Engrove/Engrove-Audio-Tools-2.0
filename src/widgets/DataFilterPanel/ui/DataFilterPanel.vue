<!-- src/widgets/DataFilterPanel/ui/DataFilterPanel.vue -->
<!--
  Denna widget-komponent representerar hela filterpanelen i Data Explorer.
  Den är en "smart" komponent som använder explorerStore för att hantera
  sitt tillstånd och bygger upp sitt gränssnitt med hjälp av agnostiska
  "Base"-komponenter från /shared/ui.
-->
<template>
  <aside class="filter-panel">
    <h3>Controls</h3>

    <!-- 1. Val av Datatyp -->
    <div class="control-group">
      <label class="control-label">1. Select Data Type</label>
      <div class="button-group">
        <BaseButton
          :variant="dataType === 'tonearms' ? 'primary' : 'secondary'"
          @click="setDataType('tonearms')"
        >
          Tonearms
        </BaseButton>
        <BaseButton
          :variant="dataType === 'cartridges' ? 'primary' : 'secondary'"
          @click="setDataType('cartridges')"
        >
          Cartridges
        </BaseButton>
      </div>
    </div>

    <!-- 2. Filterkontroller (visas när datatyp är vald) -->
    <div v-if="dataType" class="filter-controls">
      <label class="control-label">2. Filter Results</label>

      <!-- Sökfält -->
      <div class="control-group">
        <BaseInput
          v-model="searchTerm"
          placeholder="Search by manufacturer or model..."
        />
      </div>

      <!-- Dynamiskt genererade kategorifilter -->
      <div v-for="filter in availableFilters" :key="filter.key" class="control-group">
        <BaseSelect
          v-model="categoryFilters[filter.key]"
          :options="filter.options"
        />
      </div>

      <!-- Dynamiskt genererade numeriska filter -->
      <div v-for="filter in availableNumericFilters" :key="filter.key" class="control-group">
        <RangeFilter
          :label="filter.label"
          :unit="filter.unit"
          v-model="numericFilters[filter.key]"
        />
      </div>

      <!-- Återställningsknapp -->
      <BaseButton variant="secondary" @click="resetFilters" class="reset-button">
        Reset All Filters
      </BaseButton>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import { useExplorerStore } from '../../../entities/data-explorer/model/explorerStore.js';
import BaseButton from '../../../shared/ui/BaseButton.vue';
import BaseInput from '../../../shared/ui/BaseInput.vue';
import BaseSelect from '../../../shared/ui/BaseSelect.vue';
import RangeFilter from '../../../shared/ui/RangeFilter.vue';

// --- STORE INTEGRATION ---
const store = useExplorerStore();

// Exponera state och metoder som template behöver, med "destructuring"
const {
  dataType,
  searchTerm,
  categoryFilters,
  numericFilters,
  setDataType, // Dessa metoder kommer vi skapa i storen härnäst
  resetFilters,
  pickupClassifications,
  tonearmClassifications,
} = store;


// --- DYNAMISK FILTERGENERERING ---

/**
 * Hjälpfunktion för att omvandla klassificeringsdata till ett format
 * som BaseSelect-komponenten kan använda.
 * @param {Object} classifications - Klassificeringsobjektet.
 * @returns {Array<Object>} En array av filterkonfigurationsobjekt.
 */
function mapClassificationsToFilters(classifications) {
  if (!classifications) return [];
  return Object.entries(classifications).map(([key, value]) => ({
    key: key,
    label: value.name,
    options: [
      { value: undefined, label: `All ${value.name}` },
      ...value.categories.map(cat => ({ value: cat.id, label: cat.name }))
    ]
  }));
}

// Beräknar vilka filter som ska visas baserat på vald datatyp.
const availableFilters = computed(() => {
  const currentClassifications = dataType.value === 'tonearms' ? tonearmClassifications.value : pickupClassifications.value;
  return mapClassificationsToFilters(currentClassifications);
});

// Hårdkodad konfiguration för numeriska filter (kan göras mer dynamisk i framtiden).
const availableNumericFilters = computed(() => {
  if (dataType.value === 'tonearms') {
    return [
      { key: 'effective_mass_g', label: 'Effective Mass', unit: 'g' },
      { key: 'effective_length_mm', label: 'Effective Length', unit: 'mm' },
    ];
  } else if (dataType.value === 'cartridges') {
    return [
      { key: 'weight_g', label: 'Cartridge Weight', unit: 'g' },
      { key: 'cu_dynamic_10hz', label: 'Compliance @ 10Hz', unit: 'cu' },
    ];
  }
  return [];
});
</script>

<style scoped>
.filter-panel {
  background: var(--color-surface-secondary);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--color-border-primary);
  position: sticky;
  top: 88px; /* Höjd för header + lite marginal */
  align-self: start;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

h3 {
  margin: 0;
  color: var(--color-text-high-emphasis);
  border-bottom: 1px solid var(--color-border-primary);
  padding-bottom: 1rem;
  margin-bottom: 0.5rem;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.control-label {
  display: block;
  font-weight: var(--font-weight-medium);
  color: var(--color-text-medium-emphasis);
  margin-bottom: 0.5rem;
  font-size: var(--font-size-label);
}

.button-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.reset-button {
  width: 100%;
  margin-top: 1rem;
}

/* Responsivitet */
@media (max-width: 900px) {
  .filter-panel {
    position: static;
    top: auto;
  }
}
</style>
<!-- src/widgets/DataFilterPanel/ui/DataFilterPanel.vue -->
