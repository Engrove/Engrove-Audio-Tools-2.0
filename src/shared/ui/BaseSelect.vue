<!-- src/shared/ui/BaseSelect.vue -->
<!-- Grundläggande, återanvändbar dropdown-menykomponent (select). -->
<!-- Implementerad enligt Global UI-Standard Komponentspecifikation (Sektion 3.1 & 3.2). -->
<template>
  <div class="base-select-wrapper" :class="wrapperClasses">
    <select
      :value="modelValue"
      :disabled="disabled"
      class="base-select"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
        :disabled="option.disabled"
      >
        {{ option.label }}
      </option>
    </select>
    <span class="base-select-arrow">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  options: {
    type: Array,
    default: () => [],
    validator: (options) => {
      return options.every(opt => typeof opt === 'object' && 'value' in opt && 'label' in opt);
    },
  },
});

defineEmits(['update:modelValue']);

const wrapperClasses = computed(() => (
  props.disabled ? 'is-disabled' : ''
));
</script>

<style scoped>
/* ========================================================================== */
/* WRAPPER OCH POSITIONERING                                                  */
/* ========================================================================== */
.base-select-wrapper {
  position: relative;
  display: block;
  border-radius: 8px;
  transition: border-color 0.2s, background-color 0.2s, box-shadow 0.2s;
  background-color: var(--color-surface-tertiary);
  border: 1px solid var(--color-border-primary);
}

.base-select-arrow {
  position: absolute;
  top: 50%;
  right: 0.75rem;
  transform: translateY(-50%);
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-medium-emphasis);
  transition: color 0.2s;
}

/* ========================================================================== */
/* DET NATIVA <select>-ELEMENTET                                              */
/* ========================================================================== */
.base-select {
  width: 100%;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  font-family: var(--font-family-primary);
  font-size: var(--font-size-body);
  color: var(--color-text-high-emphasis);
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.base-select:focus {
  outline: none;
}

/* Korrigering för dropdown-listans textfärg i båda teman */
.base-select option {
  color: rgba(0, 0, 0, 0.87);
  background-color: #FFFFFF;
}

/* ========================================================================== */
/* INTERAKTIVA TILLSTÅND (STYLS PÅ WRAPPERN)                                  */
/* ========================================================================== */
.base-select-wrapper:hover:not(.is-disabled) {
  border-color: var(--color-text-medium-emphasis);
}
.base-select-wrapper:hover:not(.is-disabled) .base-select-arrow {
  color: var(--color-text-high-emphasis);
}

.base-select-wrapper:focus-within:not(.is-disabled) {
  border-width: 2px;
  padding: 0;
  border-color: var(--color-interactive-accent);
  box-shadow: 0 0 0 2px rgba(51, 145, 255, 0.3);
}
.base-select-wrapper:focus-within:not(.is-disabled) .base-select {
    padding: calc(0.75rem - 1px) calc(2.5rem - 1px) calc(0.75rem - 1px) calc(1rem - 1px);
}
.base-select-wrapper:focus-within:not(.is-disabled) .base-select-arrow {
  color: var(--color-interactive-accent);
}

.base-select-wrapper.is-disabled {
  background-color: var(--color-surface-secondary);
  border-color: var(--color-border-primary);
  cursor: not-allowed;
}
.base-select-wrapper.is-disabled .base-select {
  color: var(--color-text-low-emphasis);
  cursor: not-allowed;
}
.base-select-wrapper.is-disabled .base-select-arrow {
  color: var(--color-text-low-emphasis);
}

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR LJUST LÄGE                                           */
/* ========================================================================== */
:global(.light-theme) .base-select-wrapper:focus-within:not(.is-disabled) {
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  background-color: var(--color-surface-primary);
}

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR KOMPAKT LÄGE (REVIDERAD)                             */
/* ========================================================================== */
:global(.compact-theme) .base-select-wrapper {
  border-radius: 6px;
}

:global(.compact-theme) .base-select {
  /* Minskad padding för ett lägre fält */
  padding: 0.4rem 2.25rem 0.4rem 0.75rem;
}

:global(.compact-theme) .base-select-wrapper:focus-within:not(.is-disabled) .base-select {
  /* Justerar focus-padding för att matcha den nya standard-paddingen */
  padding: calc(0.4rem - 1px) calc(2.25rem - 1px) calc(0.4rem - 1px) calc(0.75rem - 1px);
}
</style>
<!-- src/shared/ui/BaseSelect.vue -->
