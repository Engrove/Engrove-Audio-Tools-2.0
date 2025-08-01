<!-- src/shared/ui/BaseButton.vue -->
<!-- Detta är en grundläggande, återanvändbar knappkomponent. Den är en del av -->
<!-- det centrala UI-biblioteket och dess stil styrs helt av design-tokens -->
<!-- och den globala komponentspecifikationen. -->
<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
  >
    <slot></slot>
  </button>
</template>

<script setup>
import { computed } from 'vue';

// Definierar komponentens props (API)
const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary'].includes(value),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

// Beräknar en array av CSS-klasser baserat på props
const buttonClasses = computed(() => [
  'base-button',
  props.variant === 'primary' ? 'base-button--primary' : 'base-button--secondary'
]);
</script>

<style scoped>
/* ========================================================================== */
/* GRUNDLÄGGANDE KNAPPSTILAR (GEMENSAMT FÖR ALLA VARIANTER)                    */
/* ========================================================================== */
.base-button {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-family: var(--font-family-primary);
  font-size: var(--font-size-label);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  border: 1px solid transparent;
  user-select: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.base-button:focus-visible {
  outline-offset: 2px;
  outline: 2px solid var(--color-interactive-accent);
}

.base-button:disabled {
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

/* ========================================================================== */
/* PRIMÄR KNAPP (SPECIFIKATION 1.1 & 1.2)                                     */
/* ========================================================================== */
.base-button--primary {
  background-color: var(--color-interactive-accent);
  color: #FFFFFF;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.base-button--primary:hover:not(:disabled) {
  background-color: var(--color-interactive-accent-hover);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-1px);
}

.base-button--primary:active:not(:disabled) {
  background-color: var(--color-interactive-accent-hover);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
  transform: translateY(0);
}

.base-button--primary:disabled {
  background-color: var(--color-surface-tertiary);
  color: var(--color-text-low-emphasis);
  border: 1px solid var(--color-border-primary);
}


/* ========================================================================== */
/* SEKUNDÄR KNAPP (SPECIFIKATION 1.1 & 1.2)                                   */
/* ========================================================================== */
.base-button--secondary {
  background-color: transparent;
  color: var(--color-text-medium-emphasis);
  border: 1px solid var(--color-border-primary);
}

.base-button--secondary:hover:not(:disabled) {
  background-color: var(--color-surface-tertiary);
  color: var(--color-text-high-emphasis);
  border-color: var(--color-border-primary);
}

.base-button--secondary:active:not(:disabled) {
  background-color: var(--color-surface-tertiary);
  color: var(--color-text-high-emphasis);
  border-color: var(--color-interactive-accent);
}

.base-button--secondary:disabled {
  background-color: transparent;
  color: var(--color-text-low-emphasis);
  border-color: var(--color-border-primary);
}
</style>
<!-- src/shared/ui/BaseButton.vue -->
