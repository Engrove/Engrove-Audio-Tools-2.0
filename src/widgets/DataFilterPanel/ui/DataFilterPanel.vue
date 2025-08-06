<!-- src/widgets/DataFilterPanel/ui/DataFilterPanel.vue -->
<!--
  Historik:
  - 2025-08-06: (Frankensteen - Operation: Strategisk Reträtt) Slutförd. Komponenten är nu anpassad till den nya Options API-storen. `storeToRefs` används inte längre för state-objekt, och v-model är direkt bundet till `store.property`. Detta löser den kritiska TypeError-kraschen.
  - 2025-08-06: (Frankensteen - Operation: Synkroniserad Initialisering) All lokal logik för filter-initialisering (watch, onMounted) har tagits bort. Komponenten förlitar sig nu helt på att storen tillhandahåller ett synkroniserat och korrekt state, vilket löser race condition-kraschen.
  - 2025-08-06: (Frankensteen) Bytte ut BaseSelect mot BaseMultiSelect för alla kategorifilter för att möjliggöra flervalsfiltrering.
  - 2024-08-04: (UPPDRAG 22) Förenklad genom att ta bort lokal logik och konsumera filterdefinitioner från storen.
-->
<!--
  Viktiga implementerade regler:
  - API-kontraktsverifiering: Komponenten konsumerar nu korrekt en Pinia Options API-store, vilket är en fundamental ändring av dess interna API-kontrakt.
  - Obligatorisk Refaktorisering: Genom att ta bort felaktig state-hantering och anpassa till den nya arkitekturen är komponenten nu både enklare och korrekt.
  - Felresiliens: Grundorsaken till en kritisk krasch har eliminerats.
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

      <!-- Dynamiskt genererade kategorifilter (nu med multi-select) -->
      <div v-for="filter in availableFilters" :key="filter.key" class="control-group">
        <BaseMultiSelect
          :label="filter.label"
          :options="getOptionsForFilter(filter.key)"
          v-model="store.categoryFilters[filter.key]"
        />
      </div>

      <!-- Dynamiskt genererade numeriska filter från storen -->
      <div v-for="filter in availableNumericFilters" :key="filter.key" class="control-group">
        <RangeFilter
          :label="filter.label"
          :unit="filter.unit"
          v-model="store.numericFilters[filter.key]"
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
import { storeToRefs } from 'pinia';
import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore.js';
import BaseButton from '@/shared/ui/BaseButton.vue';
import BaseInput from '@/shared/ui/BaseInput.vue';
import BaseMultiSelect from '@/shared/ui/BaseMultiSelect.vue';
import RangeFilter from '@/shared/ui/RangeFilter.vue';

const store = useExplorerStore();
const { setDataType, resetFilters } = store;

// categoryFilters och numericFilters tas bort från storeToRefs, då de är vanliga
// objekt i Options API-storen och inte refs. Vi binder direkt till dem via 'store'.
const {
  dataType,
  searchTerm,
  availableFilters,
  availableNumericFilters,
  classifications,
} = storeToRefs(store);

// Funktion för att bygga options-arrayen för BaseMultiSelect
const getOptionsForFilter = (filterKey) => {
  const classificationGroup = classifications.value[filterKey];
  if (!classificationGroup || !Array.isArray(classificationGroup.categories)) {
    return [];
  }
  return classificationGroup.categories.map(cat => ({
    value: cat.id,
    label: cat.name
  }));
};

</script>

<style scoped>
.filter-panel {
  background: var(--surface-secondary);
  padding: var(--spacing-5);
  border-radius: var(--border-radius-large);
  border: 1px solid var(--border-primary);
  position: sticky;
  top: calc(var(--header-height) + var(--spacing-5));
  align-self: start;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
}

h3 {
  margin: 0;
  color: var(--text-high-emphasis);
  border-bottom: 1px solid var(--border-primary);
  padding-bottom: var(--spacing-4);
  margin-bottom: 0;
  font-size: var(--font-size-h3);
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.control-label {
  display: block;
  font-weight: var(--font-weight-bold);
  color: var(--text-medium-emphasis);
  margin-bottom: var(--spacing-3);
  font-size: var(--font-size-body);
}

.button-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-2);
}

.filter-controls {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-5);
}

.reset-button {
  width: 100%;
  margin-top: var(--spacing-4);
}

@media (max-width: 900px) {
  .filter-panel {
    position: static;
    top: auto;
  }
}
</style>
