<!-- src/features/density-toggle/ui/DensityToggle.vue -->
<!--
  Detta är en ny feature-komponent som renderar en kontroll för att byta
  mellan UI-densitetsteman ('Comfortable' och 'Compact').
  Den interagerar med settingsStore för att hantera sitt tillstånd.
-->
<template>
  <div class="density-toggle-group">
    <BaseButton
      :variant="settingsStore.density === 'comfortable' ? 'primary' : 'secondary'"
      @click="settingsStore.setDensity('comfortable')"
      class="density-button"
    >
      Comfortable
    </BaseButton>
    <BaseButton
      :variant="settingsStore.density === 'compact' ? 'primary' : 'secondary'"
      @click="settingsStore.setDensity('compact')"
      class="density-button"
    >
      Compact
    </BaseButton>
  </div>
</template>

<script setup>
import { useSettingsStore } from '../../../entities/settings/model/settingsStore.js';
import BaseButton from '../../../shared/ui/BaseButton.vue';

// Hämtar en instans av vår settings store.
const settingsStore = useSettingsStore();
</script>

<style scoped>
.density-toggle-group {
  display: flex;
  background-color: var(--color-surface-tertiary);
  border-radius: 8px;
  padding: 4px;
  border: 1px solid var(--color-border-primary);
}

.density-button {
  /* Nollställ grundläggande knappstilar som inte behövs här */
  box-shadow: none;
  border: none;
  padding: 0.4rem 0.8rem; /* Lite mindre padding för ett kompaktare utseende */
  font-size: var(--font-size-small); /* Mindre textstorlek */
}

/* Överstyr hover-effekter för sekundärknappen för att passa denna specifika komponent */
.density-button.base-button--secondary:hover:not(:disabled) {
  background-color: var(--color-surface-secondary);
}
</style>
<!-- src/features/density-toggle/ui/DensityToggle.vue -->```
