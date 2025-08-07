<!-- src/widgets/ComparisonTray/ui/ComparisonTray.vue -->
<!--
  Historik:
  - 2025-08-07: (Frankensteen) Instrumenterad med loggerStore för att spåra Compare-knappens klick-händelse.
  - 2025-08-07: (Frankensteen) KRITISK FIX: Korrigerat alla CSS-variabelnamn för att matcha den globala _tokens.css-filen.
  - 2025-08-06: (Frankensteen) Skapad från grunden som en del av "Operation Återimplementering".
-->
<!--
  Viktiga implementerade regler:
  - "Help me God"-protokollet har använts för att verifiera denna nya komponents design och implementation.
  - API-kontraktsverifiering: Interagerar med comparisonStore och explorerStore, och emitterar tydligt definierade händelser ('compare', 'clear').
  - Felresiliens: Hanterar fallet där ett objekt inte hittas och renderar inget om korgen är tom.
  - Semantik och läsbarhet: Tydlig BEM-liknande klassnamngivning och en logisk struktur.
-->
<template>
  <div v-if="comparisonStore.selectedItemsCount > 0" class="comparison-tray">
    <div class="tray-header">
      <span class="tray-title">Comparison Tray ({{ comparisonStore.selectedItemsCount }}/{{ COMPARISON_LIMIT }})</span>
      <div class="tray-actions">
        <BaseButton 
          variant="primary" 
          @click="handleCompareClick"
          :disabled="comparisonStore.selectedItemsCount < 2"
          title="Compare selected items"
        >
          Compare
        </BaseButton>
        <BaseButton 
          variant="secondary" 
          @click="comparisonStore.clearSelection()"
          title="Clear all selected items"
        >
          Clear
        </BaseButton>
      </div>
    </div>

    <ul class="selected-items-list">
      <li v-for="item in selectedItems" :key="item.id" class="selected-item">
        <div class="item-info">
          <span class="item-manufacturer">{{ item.manufacturer }}</span>
          <span class="item-model">{{ item.model }}</span>
        </div>
        <button @click="comparisonStore.toggleItem(item.id)" class="remove-item-btn" title="Remove item">
          ×
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useComparisonStore } from '@/entities/comparison/model/comparisonStore.js';
import { useExplorerStore } from '@/entities/data-explorer/model/explorerStore.js';
import { useLoggerStore, IS_DEBUG_MODE } from '@/entities/logger/model/loggerStore.js'; // NYTT: Importera logger
import BaseButton from '@/shared/ui/BaseButton.vue';

const COMPARISON_LIMIT = 5;

const comparisonStore = useComparisonStore();
const explorerStore = useExplorerStore();
const logger = useLoggerStore(); // NYTT: Initiera logger

const emit = defineEmits(['compare', 'clear']);

const selectedItems = computed(() => {
  return comparisonStore.selectedItemIds
    .map(id => explorerStore.allItems.find(item => item.id === id))
    .filter(item => item !== undefined); 
});

// NYTT: Lokal metod för att hantera klick och loggning
function handleCompareClick() {
  if (IS_DEBUG_MODE) {
    logger.startLogSession('Compare Button Click');
    logger.addLog(
      'Compare button clicked. Emitting @compare event.', 
      'ComparisonTray'
    );
  }
  
  emit('compare');

  if (IS_DEBUG_MODE) {
    logger.endLogSession();
  }
}
</script>

<style scoped>
.comparison-tray {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: var(--color-surface-secondary);
  border-top: 1px solid var(--color-border-primary);
  box-shadow: 0 -4px 12px -2px rgba(0, 0, 0, 0.2);
  padding: var(--spacing-4) var(--spacing-6);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  transform: translateY(100%);
  animation: slide-up 0.3s ease-out forwards;
}

@keyframes slide-up {
  to {
    transform: translateY(0);
  }
}

.tray-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tray-title {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-high-emphasis);
}

.tray-actions {
  display: flex;
  gap: var(--spacing-3);
}

.selected-items-list {
  display: flex;
  gap: var(--spacing-3);
  list-style: none;
  margin: 0;
  padding: 0;
  overflow-x: auto;
  padding-bottom: var(--spacing-2); /* For scrollbar spacing */
}

.selected-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  background-color: var(--color-surface-tertiary);
  padding: var(--spacing-2) var(--spacing-3);
  border-radius: var(--border-radius-full);
  border: 1px solid var(--color-border-primary);
  white-space: nowrap;
  flex-shrink: 0;
}

.item-info {
  display: flex;
  flex-direction: column;
}

.item-manufacturer {
  font-size: var(--font-size-small);
  color: var(--color-text-low-emphasis);
}

.item-model {
  font-size: var(--font-size-body);
  color: var(--color-text-medium-emphasis);
  font-weight: var(--font-weight-medium);
}

.remove-item-btn {
  background: none;
  border: none;
  color: var(--color-text-low-emphasis);
  cursor: pointer;
  font-size: 1.5rem;
  line-height: 1;
  padding: 0 var(--spacing-1);
  margin-left: var(--spacing-2);
  transition: color 0.2s;
}

.remove-item-btn:hover {
  color: var(--color-text-high-emphasis);
}
</style>
<!-- src/widgets/ComparisonTray/ui/ComparisonTray.vue -->
