<!-- src/widgets/DataFilterPanel/ui/DataFilterPanel.vue -->
<!--
  Denna widget-komponent representerar hela filterpanelen i Data Explorer.
  Den är en "smart" komponent som använder explorerStore för att hantera
  sitt tillstånd och bygger upp sitt gränssnitt med hjälp av agnostiska
  "Base"-komponenter från /shared/ui.
  
  KORRIGERING (Regression): Denna version åtgärdar ett race condition där
  komponenten försökte rendera filter innan klassificeringsdatan hade laddats.
  `availableFilters` har nu ett skyddsvillkor för att säkerställa att datan finns.
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
import { storeToRefs } from 'pinia';
import { useExplorerStore } from '../../../entities/data-explorer/model/explorerStore.js';
import { useLoggerStore } from '../../../entities/logger/model/loggerStore.js';
import BaseButton from '../../../shared/ui/BaseButton.vue';
import BaseInput from '../../../shared/ui/BaseInput.vue';
import BaseSelect from '../../../shared/ui/BaseSelect.vue';
import RangeFilter from '../../../shared/ui/RangeFilter.vue';

const store = useExplorerStore();
const logger = useLoggerStore();

const { setDataType, resetFilters } = store;

const {
  dataType,
  searchTerm,
  categoryFilters,
  numericFilters,
  pickupClassifications,
  tonearmClassifications,
} = storeToRefs(store);

/**
 * Mappar klassificeringsdata till ett format som BaseSelect-komponenten kan använda.
 * @param {Object} classifications - Objektet med klassificeringsdata.
 * @returns {Array} En array av filterobjekt.
 */
function mapClassificationsToFilters(classifications) {
  // SKYDDSVILLKOR: Om klassificeringsobjektet är tomt eller ogiltigt, returnera en tom array direkt.
  if (!classifications || Object.keys(classifications).length === 0) {
    logger.addLog('mapClassificationsToFilters received empty or invalid classifications. Returning 0 filters.', 'DataFilterPanel');
    return [];
  }
  
  const result = Object.entries(classifications).map(([key, value]) => ({
    key: key,
    label: value.name,
    options: [
      { value: '', label: `All ${value.name}` }, // Uppdaterad för bättre UX
      ...value.categories.map(cat => ({
        value: cat.id,
        label: cat.name ? cat.name : cat.id
      }))
    ]
  }));

  logger.addLog(`mapClassificationsToFilters returned ${result.length} filters.`, 'DataFilterPanel', result);
  return result;
}

const availableFilters = computed(() => {
  logger.addLog('`availableFilters` computed property is running.', 'DataFilterPanel');
  if (dataType.value === 'tonearms') {
    logger.addLog('Current classifications for dataType \'tonearms\'', 'DataFilterPanel', tonearmClassifications.value);
    return mapClassificationsToFilters(tonearmClassifications.value);
  } else if (dataType.value === 'cartridges') {
    logger.addLog('Current classifications for dataType \'cartridges\'', 'DataFilterPanel', pickupClassifications.value);
    return mapClassificationsToFilters(pickupClassifications.value);
  }
  return [];
});

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
  top: 88px;
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

.filter-controls {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.reset-button {
  width: 100%;
  margin-top: 1rem;
}

@media (max-width: 900px) {
  .filter-panel {
    position: static;
    top: auto;
  }
}

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR KOMPAKT LÄGE (REVIDERAD)                             */
/* ========================================================================== */
:global(.compact-theme) .filter-panel {
  padding: 1rem;
  gap: 1rem; /* Minskad huvud-gap */
}

:global(.compact-theme) h3 {
  padding-bottom: 0.75rem;
  margin-bottom: 0.25rem;
}

:global(.compact-theme) .filter-controls {
  gap: 1rem; /* Minskad gap mellan filtergrupper */
}

:global(.compact-theme) .reset-button {
  margin-top: 0.5rem;
}

:global(.compact-theme) .control-label {
  margin-bottom: 0.25rem;
}
</style>
<!-- src/widgets/DataFilterPanel/ui/DataFilterPanel.vue -->
