<!-- src/shared/ui/BaseMultiSelect.vue -->
<!--
  === SYFTE & ANSVAR ===
  Denna fil definierar en återanvändbar flervalskomponent (multi-select dropdown)
  för avancerad filtrering i applikationen. Den är designad för att vara
  agnostisk, stödja v-model och hantera sitt eget öppna/stängda tillstånd.

  === API-KONTRAKT (Props, Emits) ===
  PROPS:
  - options (Array, required): En lista med objekt, där varje objekt måste ha 'value' och 'label'.
  - modelValue (Array, required): Den reaktiva arrayen som håller de valda värdena (används för v-model).
  - label (String): En valfri etikett som visas ovanför komponenten.

  EMITS:
  - 'update:modelValue': Sänds när användaren väljer/avväljer ett alternativ. Krävs för v-model.

  === HISTORIK ===
  * 2025-08-06: (Frankensteen) Lade till dynamisk z-index-hantering för att lösa problem med överlappande dropdowns.
  * 2025-08-06: (Frankensteen - Felsökning) Korrigerat ett API-kontraktsbrott. Ändrat :label-prop till att använda default-slot för BaseCheckbox för att korrekt rendera etikettext.
  * 2025-08-04: Created by Frankensteen as part of Steg 23.
              - A reusable multi-select component for advanced filtering.
              - Compatible with v-model via `modelValue` prop and `update:modelValue` emit.
              - Uses BaseCheckbox for consistent UI.
              - Manages its own open/closed state and handles outside clicks.

  === TILLÄMPADE REGLER (Frankensteen v4.0) ===
  - Fullständig kod, alltid: Hela filen, inklusive fullständig historik, levereras.
  - API-kontraktsverifiering: Korrigerat API-brott mot BaseCheckbox.
  - Obligatorisk Refaktorisering: z-index-lösningen är implementerad på ett rent och underhållbart sätt.
  - Fullständig Historik: All tidigare historik har bevarats och ny har lagts till.
  - Inledande fil-kommentarer: Denna header har lagts till enligt standard.
-->
<template>
  <div class="base-multi-select" ref="multiSelectRef" :class="{ 'is-open': isOpen }">
    <label v-if="label" :for="id" class="base-multi-select__label">{{ label }}</label>
    <div class="base-multi-select__control">
      <button
        :id="id"
        type="button"
        class="base-multi-select__button"
        :class="{ 'base-multi-select__button--open': isOpen }"
        @click="isOpen = !isOpen"
        aria-haspopup="listbox"
        :aria-expanded="isOpen"
      >
        <span class="base-multi-select__selected-text">{{ selectedText }}</span>
        <span class="base-multi-select__arrow-wrapper">
          <svg
            class="base-multi-select__arrow-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </span>
      </button>

      <transition name="fade-in-up">
        <div v-if="isOpen" class="base-multi-select__dropdown">
          <ul class="base-multi-select__options-list" role="listbox">
            <li
              v-for="option in options"
              :key="option.value"
              class="base-multi-select__option-item"
              role="option"
              :aria-selected="isSelected(option.value)"
            >
              <BaseCheckbox
                :model-value="isSelected(option.value)"
                @update:modelValue="toggleOption(option.value)"
                :id="`option-${id}-${option.value}`"
              >
                {{ option.label }}
              </BaseCheckbox>
            </li>
          </ul>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import BaseCheckbox from '@/shared/ui/BaseCheckbox.vue';

const props = defineProps({
  options: {
    type: Array,
    required: true,
    validator: (value) => value.every(opt => 'value' in opt && 'label' in opt),
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

const id = `base-multi-select-${Math.random().toString(36).substring(2, 9)}`;
const isOpen = ref(false);
const multiSelectRef = ref(null);

const selectedText = computed(() => {
  if (props.modelValue.length === 0) {
    return `Select ${props.label || 'options'}...`;
  }
  if (props.modelValue.length === 1) {
    const selectedOption = props.options.find(opt => opt.value === props.modelValue[0]);
    return selectedOption ? selectedOption.label : '1 selected';
  }
  return `${props.modelValue.length} selected`;
});

const isSelected = (optionValue) => {
  return props.modelValue.includes(optionValue);
};

const toggleOption = (optionValue) => {
  const newModelValue = [...props.modelValue];
  const index = newModelValue.indexOf(optionValue);

  if (index === -1) {
    newModelValue.push(optionValue);
  } else {
    newModelValue.splice(index, 1);
  }
  
  emit('update:modelValue', newModelValue);
};

const handleClickOutside = (event) => {
  if (multiSelectRef.value && !multiSelectRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

watch(isOpen, (newValue) => {
  // Logic to run when dropdown opens/closes can be added here.
});
</script>

<style scoped>
.base-multi-select {
  position: relative;
  width: 100%;
}

.base-multi-select.is-open {
  /* Höjer den aktiva dropdownen över sina syskon för att förhindra överlappning */
  z-index: 20;
}

.base-multi-select__label {
  display: block;
  margin-bottom: var(--spacing-2);
  font-size: var(--font-size-label);
  color: var(--text-medium-emphasis);
  font-weight: var(--font-weight-medium);
}

.base-multi-select__control {
  position: relative;
}

.base-multi-select__button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: var(--spacing-2) var(--spacing-3);
  background-color: var(--surface-tertiary);
  border: 1px solid var(--border-primary);
  border-radius: var(--border-radius-medium);
  color: var(--text-medium-emphasis);
  font-family: var(--font-family-body);
  font-size: var(--font-size-body);
  text-align: left;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.base-multi-select__button:hover {
  border-color: var(--interactive-accent-hover);
}

.base-multi-select__button:focus,
.base-multi-select__button--open {
  outline: none;
  border-color: var(--interactive-accent);
  box-shadow: 0 0 0 2px var(--interactive-accent-translucent);
}

.base-multi-select__selected-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.base-multi-select__arrow-wrapper {
  display: flex;
  align-items: center;
  margin-left: var(--spacing-2);
}

.base-multi-select__arrow-icon {
  width: 20px;
  height: 20px;
  color: var(--text-low-emphasis);
  transition: transform 0.2s ease-in-out;
}

.base-multi-select__button--open .base-multi-select__arrow-icon {
  transform: rotate(180deg);
}

.base-multi-select__dropdown {
  position: absolute;
  top: calc(100% + var(--spacing-1));
  left: 0;
  right: 0;
  z-index: 10;
  background-color: var(--surface-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--border-radius-medium);
  box-shadow: var(--shadow-medium);
  max-height: 250px;
  overflow-y: auto;
}

.base-multi-select__options-list {
  list-style: none;
  padding: var(--spacing-2);
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-1);
}

.base-multi-select__option-item {
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--border-radius-small);
}

.base-multi-select__option-item :deep(label) {
  width: 100%;
  cursor: pointer;
  padding: var(--spacing-1) 0;
}

.fade-in-up-enter-active,
.fade-in-up-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-in-up-enter-from,
.fade-in-up-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
