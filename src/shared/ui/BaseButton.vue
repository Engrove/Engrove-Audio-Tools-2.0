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
// variant: styr knappens utseende ('primary' eller 'secondary')
// disabled: inaktiverar knappen
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
  // Om props.variant är 'primary', lägg till klassen 'base-button--primary'.
  // Om props.variant är något annat (dvs 'secondary'), lägg till klassen 'base-button--secondary'.
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
  border: 1px solid transparent; /* Grund-border för att undvika layout-hopp */
  user-select: none; /* Förhindrar textmarkering vid klick */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1; /* Säkerställer vertikal centrering av text */
}

.base-button:focus-visible {
  /* Använder outline för fokus för att inte påverka layouten. */
  /* :focus-visible säkerställer att detta bara visas vid tangentbordsnavigering. */
  outline-offset: 2px;
  outline: 2px solid var(--color-interactive-accent);
}

.base-button:disabled {
  cursor: not-allowed;
  box-shadow: none; /* Nollställ skugga för alla inaktiverade knappar */
}

/* ========================================================================== */
/* PRIMÄR KNAPP (SPECIFIKATION 1.1 & 1.2)                                     */
/* ========================================================================== */
.base-button--primary {
  background-color: var(--color-interactive-accent);
  color: var(--color-text-high-emphasis);
  /* Ljustema: $surface-primary, Mörktema: $text-high-emphasis */
  color: var(--color-surface-primary, var(--color-text-high-emphasis));
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.base-button--primary:hover:not(:disabled) {
  background-color: var(--color-interactive-accent-hover);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-1px);
}

.base-button--primary:active:not(:disabled) {
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
  transform: translateY(0);
}

.base-button--primary:disabled {
  background-color: var(--color-surface-tertiary);
  color: var(--color-text-low-emphasis);
  border: 1px solid var(--color-border-primary);
}

/* Anpassning för ljust tema för att textfärgen ska bli rätt (vit) */
.light-theme .base-button--primary {
    color: #FFFFFF;
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
