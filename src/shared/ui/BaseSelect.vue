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
      <!-- Inbäddad SVG-ikon för pilen för maximal stilkontroll -->
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue';

// Defines the component's props (API) and emitted events.
// This component supports v-model for two-way data binding.
const props = defineProps({
  // Värdet för dropdown, används med v-model
  modelValue: {
    type: [String, Number],
    default: '',
  },
  // Inaktiverar dropdown om satt till true
  disabled: {
    type: Boolean,
    default: false,
  },
  // Array av alternativ att visa i dropdown.
  // Varje objekt måste ha 'value' och 'label'.
  options: {
    type: Array,
    default: () => [],
    validator: (options) => {
      // Validerar att varje alternativ är ett objekt med 'value' och 'label'
      return options.every(opt => typeof opt === 'object' && 'value' in opt && 'label' in opt);
    },
  },
});

// Deklarerar händelsen som krävs för att v-model ska fungera
defineEmits(['update:modelValue']);

// Beräknar en CSS-klass för wrappern när komponenten är inaktiverad
const wrapperClasses = computed(() => (
  // Om props.disabled är sant, returnera 'is-disabled'.
  // Om props.disabled är falskt, returnera en tom sträng.
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
  
  /* Default-tillstånd från specifikationen */
  background-color: var(--color-surface-tertiary);
  border: 1px solid var(--color-border-primary);
}

.base-select-arrow {
  position: absolute;
  top: 50%;
  right: 0.75rem; /* 12px */
  transform: translateY(-50%);
  pointer-events: none; /* Låter klick gå igenom till <select> */
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-medium-emphasis); /* Färg på SVG-ikonen */
  transition: color 0.2s;
}

/* ========================================================================== */
/* DET NATIVA <select>-ELEMENTET                                              */
/* ========================================================================== */
.base-select {
  /* Utseende och dimensioner */
  width: 100%;
  appearance: none; /* Tar bort all standardstyling från webbläsaren */
  -webkit-appearance: none;
  -moz-appearance: none;
  padding: 0.75rem 2.5rem 0.75rem 1rem; /* 12px 40px 12px 16px. Mer padding till höger för pilen. */

  /* Typografi och färger */
  font-family: var(--font-family-primary);
  font-size: var(--font-size-body);
  color: var(--color-text-high-emphasis);
  
  /* Övrigt */
  background-color: transparent; /* Wrappern sköter bakgrunden */
  border: none; /* Wrappern sköter kanten */
  cursor: pointer;
}

.base-select:focus {
  outline: none; /* Wrappern sköter focus-stilen */
}

/* ========================================================================== */
/* INTERAKTIVA TILLSTÅND (STYLS PÅ WRAPPERN)                                  */
/* ========================================================================== */

/* Hover-tillstånd */
.base-select-wrapper:hover:not(.is-disabled) {
  border-color: var(--color-text-medium-emphasis);
}
.base-select-wrapper:hover:not(.is-disabled) .base-select-arrow {
  color: var(--color-text-high-emphasis);
}

/* Focus & Active (Open)-tillstånd. :focus-within är perfekt för detta. */
.base-select-wrapper:focus-within:not(.is-disabled) {
  border-width: 2px;
  padding: 0; /* Nollställ för att undvika dubbel padding */
  border-color: var(--color-interactive-accent);
  box-shadow: 0 0 0 2px rgba(51, 145, 255, 0.3);
}
/* Justera padding på det inre elementet när wrappern har en tjockare kant */
.base-select-wrapper:focus-within:not(.is-disabled) .base-select {
    padding: calc(0.75rem - 1px) calc(2.5rem - 1px) calc(0.75rem - 1px) calc(1rem - 1px);
}
.base-select-wrapper:focus-within:not(.is-disabled) .base-select-arrow {
  color: var(--color-interactive-accent);
}

/* Disabled-tillstånd */
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
  /* I ljust läge ska bakgrunden förbli primär-ytan, inte sekundär, enligt spec. */
  background-color: var(--color-surface-primary);
}

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR KOMPAKT LÄGE                                         */
/* ========================================================================== */
:global(.compact-theme) .base-select-wrapper {
  border-radius: 6px;
}

:global(.compact-theme) .base-select {
  padding: 0.5rem 2.25rem 0.5rem 0.75rem; /* Minskad padding */
}

:global(.compact-theme) .base-select-wrapper:focus-within:not(.is-disabled) .base-select {
  /* Justerar focus-padding för att matcha den nya standard-paddingen */
  padding: calc(0.5rem - 1px) calc(2.25rem - 1px) calc(0.5rem - 1px) calc(0.75rem - 1px);
}
</style>
<!-- src/shared/ui/BaseSelect.vue -->
