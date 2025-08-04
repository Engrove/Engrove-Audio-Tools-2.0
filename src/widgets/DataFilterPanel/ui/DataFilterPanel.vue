<!-- src/widgets/DataFilterPanel/ui/DataFilterPanel.vue -->
<!--
  Historik:
  - 2024-08-04: (UPPDRAG 20) Refaktorerad för att konsumera den färdiga filterstrukturen från explorerStore.
  - 2024-08-04: (UPPDRAG 22) Ytterligare förenklad genom att ta bort lokal logik för numeriska filter och konsumera den från storen.
-->
<!--
  Viktiga implementerade regler:
  - Fullständig kod, alltid: Filen är komplett.
  - Obligatorisk Refaktorisering: Lokal UI-logik har tagits bort och komponenten är nu en ren "consumer" av storen.
  - Alter Ego-granskning: Genomförd för att verifiera förenklingen och korrekt bindning till storen.
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

      <!-- Dynamiskt genererade numeriska filter från storen -->
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
import { storeToRefs } from 'pinia';
import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore.js';
import BaseButton from '@/shared/ui/BaseButton.vue';
import BaseInput from '@/shared/ui/BaseInput.vue';
import BaseSelect from '@/shared/ui/BaseSelect.vue';
import RangeFilter from '@/shared/ui/RangeFilter.vue';

const store = useExplorerStore();

// Hämta actions direkt från storen
const { setDataType, resetFilters } = store;

// Hämta state och getters med storeToRefs för att behålla reaktiviteten
const {
  dataType,
  searchTerm,
  categoryFilters,
  numericFilters,
  availableFilters,
  availableNumericFilters, // NY: Importerad från store
} = storeToRefs(store);

// BORTTAGEN: Den lokala computed propertyn `availableNumericFilters` har raderats.
// Logiken finns nu centraliserad i explorerStore.
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
</style>
<!-- src/widgets/DataFilterPanel/ui/DataFilterPanel.vue -->
