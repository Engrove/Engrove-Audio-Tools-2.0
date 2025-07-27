<!-- src/shared/ui/BaseRadio.vue -->
<!-- Grundläggande, återanvändbar radioknappkomponent. -->
<!-- Implementerad enligt Global UI-Standard Komponentspecifikation (Sektion 5.1 & 5.2). -->
<template>
  <label class="base-radio-wrapper">
    <input
      type="radio"
      class="base-radio-input"
      :name="name"
      :value="value"
      :checked="isChecked"
      :disabled="disabled"
      @change="$emit('update:modelValue', value)"
    />
    <span class="base-radio-custom"></span>
    <span v-if="$slots.default" class="base-radio-label">
      <slot></slot>
    </span>
  </label>
</template>

<script setup>
import { computed } from 'vue';

// Defines the component's props (API) and emitted events.
// This component supports v-model for two-way data binding.

const props = defineProps({
  // Det delade värdet för radiogruppen, används med v-model
  modelValue: {
    type: [String, Number],
    default: '',
  },
  // Det unika värdet för just denna radioknapp
  value: {
    type: [String, Number],
    required: true,
  },
  // Gruppnamnet, obligatoriskt för att radioknappar ska fungera korrekt
  name: {
    type: String,
    required: true,
  },
  // Inaktiverar radioknappen om satt till true
  disabled: {
    type: Boolean,
    default: false,
  },
});

// Deklarerar händelsen som krävs för att v-model ska fungera
defineEmits(['update:modelValue']);

// Beräknar om denna specifika radioknapp är vald
const isChecked = computed(() => props.modelValue === props.value);
</script>

<style scoped>
/* ========================================================================== */
/* GRUNDSTRUKTUR OCH LAYOUT                                                   */
/* ========================================================================== */
.base-radio-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem; /* Mellanrum mellan knapp och etikett */
  cursor: pointer;
}

/* Den faktiska radioknappen är dold, men funktionell för tillgänglighet */
.base-radio-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

/* Den anpassade visuella radioknappen */
.base-radio-custom {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%; /* Rund form */
  transition: all 0.2s ease-in-out;
  position: relative;

  /* Ovalt tillstånd */
  background-color: transparent;
  border: 2px solid var(--color-text-medium-emphasis);
}

/* Den inre pricken för "vald" status */
.base-radio-custom::after {
  content: "";
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--color-interactive-accent);
  transform: scale(0); /* Gömmer pricken initialt */
  transition: all 0.2s ease-in-out;
}

/* Etikett-texten */
.base-radio-label {
  color: var(--color-text-medium-emphasis);
  user-select: none;
}

/* ========================================================================== */
/* INTERAKTIVA TILLSTÅND                                                      */
/* ========================================================================== */

/* --- VALT TILLSTÅND --- */
.base-radio-input:checked + .base-radio-custom {
  border-color: var(--color-interactive-accent);
}
.base-radio-input:checked + .base-radio-custom::after {
  transform: scale(1); /* Visar pricken */
}

/* --- HOVER TILLSTÅND --- */
/* Ovald + Hover */
.base-radio-input:hover:not(:disabled):not(:checked) + .base-radio-custom {
  background-color: var(--color-surface-tertiary);
  border-color: var(--color-text-high-emphasis);
}
/* Vald + Hover */
.base-radio-input:hover:not(:disabled):checked + .base-radio-custom {
  background-color: var(--color-surface-tertiary);
  border-color: var(--color-interactive-accent-hover);
}
.base-radio-input:hover:not(:disabled):checked + .base-radio-custom::after {
  background-color: var(--color-interactive-accent-hover);
}

/* --- FOCUS TILLSTÅND (ENDAST TANGENTBORD) --- */
.base-radio-input:focus-visible + .base-radio-custom {
  outline: 2px solid var(--color-interactive-accent);
  outline-offset: 2px;
}

/* --- DISABLED TILLSTÅND --- */
.base-radio-wrapper:has(.base-radio-input:disabled) {
  cursor: not-allowed;
}
.base-radio-input:disabled + .base-radio-custom {
  background-color: var(--color-surface-secondary);
  border-color: var(--color-text-low-emphasis);
}
.base-radio-input:disabled:checked + .base-radio-custom::after {
  background-color: var(--color-text-low-emphasis);
  transform: scale(1);
}
.base-radio-input:disabled ~ .base-radio-label {
  color: var(--color-text-low-emphasis);
}
</style>
<!-- src/shared/ui/BaseRadio.vue -->
