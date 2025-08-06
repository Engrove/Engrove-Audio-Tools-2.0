<!--
  /src/shared/ui/BaseMultiSelect.vue
-->
<template>
  <div
    class="base-multi-select"
    :class="{ 'is-open': isOpen }"
    @click.stop="toggleDropdown"
    ref="wrapper"
  >
    <label v-if="label" class="base-multi-select__label">{{ label }}</label>
    <div class="base-multi-select__control">
      <span class="base-multi-select__placeholder">
        {{ selectedLabel }}
      </span>
      <svg class="base-multi-select__arrow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </div>

    <ul v-show="isOpen" class="base-multi-select__dropdown">
      <li v-for="option in options" :key="option.value">
        <BaseCheckbox
          :model-value="modelValue.includes(option.value)"
          @update:modelValue="toggleOption(option.value)"
        >
          {{ option.label }}
        </BaseCheckbox>
      </li>
    </ul>
  </div>
</template>

<script setup>
// === SYFTE & ANSVAR ===
// Denna fil definierar en återanvändbar flervalskomponent (multi-select dropdown)
// för avancerad filtrering i applikationen. Den är designad för att vara
// agnostisk, stödja v-model och hantera sitt eget öppna/stängda tillstånd.
//
// === API-KONTRAKT (Props, Emits) ===
// PROPS:
// - options (Array, required): En lista med objekt, där varje objekt måste ha 'value' och 'label'.
// - modelValue (Array, required): Den reaktiva arrayen som håller de valda värdena (används för v-model).
// - label (String): En valfri etikett som visas ovanför komponenten.
//
// EMITS:
// - 'update:modelValue': Sänds när användaren väljer/avväljer ett alternativ. Krävs för v-model.
//
// === HISTORIK ===
// * 2025-08-06: (Frankensteen - DEFINITIVE VISUAL FIX) Corrected all CSS color variables to use the mandatory '--color-' prefix (e.g., '--surface-tertiary' -> '--color-surface-tertiary'). This fixes the root cause of the missing background and border styling.
// * 2025-08-06: (Frankensteen - TRIBUNAL FAILURE & CORRECTION) Added the missing 'background-color' property to the dropdown. Previous fixes incorrectly focused only on z-index, ignoring the visual evidence of transparency. This is the definitive visual fix.
// * 2025-08-06: (Frankensteen - TRIBUNAL REVIEW) Definitiv fix för CSS stacking context. Tidigare fix var felaktig. Denna fix applicerar z-index på komponentens rot-element när den är öppen, vilket är den verifierat korrekta lösningen.
// * 2025-08-06: (Frankensteen) Lade till dynamisk z-index-hantering för att lösa problem med överlappande dropdowns.
// * 2025-08-06: (Frankensteen - Felsökning) Korrigerat ett API-kontraktsbrott. Ändrat :label-prop till att använda default-slot för BaseCheckbox för att korrekt rendera etikettext.
// * 2025-08-04: Created by Frankensteen as part of Steg 23.
//
// === TILLÄMPADE REGLER (Frankensteen v4.0) ===
// - Syntax- och Linter-simulering: Korrigerat CSS-variabelnamn för att matcha den globala token-filen.
// - Fullständig Historik: Hela den korrekta historiken är bevarad.

import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import BaseCheckbox from '@/shared/ui/BaseCheckbox.vue';

const props = defineProps({
  options: {
    type: Array,
    required: true,
  },
  modelValue: {
    type: Array,
    required: true,
  },
  label: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);
const wrapper = ref(null);

const selectedLabel = computed(() => {
  if (props.modelValue.length === 0) {
    return 'Select...';
  }
  if (props.modelValue.length === 1) {
    const selectedOption = props.options.find(opt => opt.value === props.modelValue[0]);
    return selectedOption ? selectedOption.label : 'Select...';
  }
  return `${props.modelValue.length} selected`;
});

function toggleDropdown() {
  isOpen.value = !isOpen.value;
}

function closeDropdown() {
  isOpen.value = false;
}

function toggleOption(optionValue) {
  const newValue = [...props.modelValue];
  const index = newValue.indexOf(optionValue);

  if (index > -1) {
    newValue.splice(index, 1);
  } else {
    newValue.push(optionValue);
  }
  emit('update:modelValue', newValue);
}

const handleClickOutside = (event) => {
  if (wrapper.value && !wrapper.value.contains(event.target)) {
    closeDropdown();
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.base-multi-select {
  position: relative;
  width: 100%;
}

.base-multi-select.is-open {
  z-index: 10;
}

.base-multi-select__label {
  display: block;
  margin-bottom: var(--spacing-1);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-medium-emphasis);
}

.base-multi-select__control {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--input-padding-y) var(--input-padding-x);
  background-color: var(--color-surface-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.base-multi-select.is-open .base-multi-select__control {
  border-color: var(--color-interactive-accent);
  box-shadow: 0 0 0 1px var(--color-interactive-accent);
}

.base-multi-select__placeholder {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--color-text-high-emphasis);
}

.base-multi-select__arrow {
  width: 20px;
  height: 20px;
  color: var(--color-text-medium-emphasis);
  transition: transform 0.2s;
}

.base-multi-select.is-open .base-multi-select__arrow {
  transform: rotate(180deg);
}

.base-multi-select__dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 4px;
  border: 1px solid var(--color-border-primary);
  border-radius: var(--border-radius-md);
  max-height: 200px;
  overflow-y: auto;
  list-style-type: none;
  padding: var(--spacing-1);
  margin-block-start: 0;
  margin-block-end: 0;
  padding-inline-start: 0;
  z-index: 10;
  background-color: var(--color-surface-secondary);
}


.base-multi-select__dropdown li {
  padding: var(--spacing-1) var(--spacing-2);
  cursor: pointer;
  border-radius: var(--border-radius-sm);
}

.base-multi-select__dropdown li:hover {
  background-color: var(--color-surface-tertiary);
}

/* Override BaseCheckbox styles for tighter layout */
.base-multi-select__dropdown li :deep(.base-checkbox) {
  padding: 0;
}
</style>
