<!-- src/shared/ui/BaseCheckbox.vue -->
<!-- Grundläggande, återanvändbar kryssrutekomponent. -->
<!-- Implementerad enligt Global UI-Standard Komponentspecifikation (Sektion 5.1 & 5.2). -->
<template>
  <label class="base-checkbox-wrapper">
    <input
      type="checkbox"
      class="base-checkbox-input"
      :checked="modelValue"
      :disabled="disabled"
      @change="$emit('update:modelValue', $event.target.checked)"
    />
    <span class="base-checkbox-custom">
      <svg class="base-checkbox-checkmark" viewBox="0 0 16 16" fill="currentColor">
        <path d="M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z"/>
      </svg>
    </span>
    <span v-if="$slots.default" class="base-checkbox-label">
      <slot></slot>
    </span>
  </label>
</template>

<script setup>
// Defines the component's props (API) and emitted events.
// This component supports v-model for two-way data binding.

defineProps({
  // Status för kryssrutan (true = markerad), används med v-model
  modelValue: {
    type: Boolean,
    default: false,
  },
  // Inaktiverar kryssrutan om satt till true
  disabled: {
    type: Boolean,
    default: false,
  },
});

// Deklarerar händelsen som krävs för att v-model ska fungera
defineEmits(['update:modelValue']);
</script>

<style scoped>
/* ========================================================================== */
/* GRUNDSTRUKTUR OCH LAYOUT                                                   */
/* ========================================================================== */
.base-checkbox-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem; /* Mellanrum mellan ruta och etikett */
  cursor: pointer;
}

/* Den faktiska checkboxen är dold, men funktionell för tillgänglighet */
.base-checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

/* Den anpassade visuella kryssrutan */
.base-checkbox-custom {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  transition: all 0.2s ease-in-out;

  /* Omarkerat tillstånd */
  background-color: transparent;
  border: 2px solid var(--color-text-medium-emphasis);
}

/* Bocken (SVG-ikonen) är initialt osynlig */
.base-checkbox-checkmark {
  width: 16px;
  height: 16px;
  color: var(--color-surface-primary); /* Färg på bocken */
  opacity: 0;
  transform: scale(0.5);
  transition: all 0.2s ease-in-out;
}

/* Etikett-texten */
.base-checkbox-label {
  color: var(--color-text-medium-emphasis);
  user-select: none; /* Förhindrar textmarkering vid klick på etiketten */
}

/* ========================================================================== */
/* INTERAKTIVA TILLSTÅND                                                      */
/* ========================================================================== */

/* --- MARKERAT TILLSTÅND --- */
.base-checkbox-input:checked + .base-checkbox-custom {
  background-color: var(--color-interactive-accent);
  border-color: var(--color-interactive-accent);
}
.base-checkbox-input:checked + .base-checkbox-custom .base-checkbox-checkmark {
  opacity: 1;
  transform: scale(1);
}

/* --- HOVER TILLSTÅND --- */
/* Omarkerad + Hover */
.base-checkbox-input:hover:not(:disabled):not(:checked) + .base-checkbox-custom {
  background-color: var(--color-surface-tertiary);
  border-color: var(--color-text-high-emphasis);
}
/* Markerad + Hover */
.base-checkbox-input:hover:not(:disabled):checked + .base-checkbox-custom {
  background-color: var(--color-interactive-accent-hover);
  border-color: var(--color-interactive-accent-hover);
}

/* --- FOCUS TILLSTÅND (ENDAST TANGENTBORD) --- */
.base-checkbox-input:focus-visible + .base-checkbox-custom {
  outline: 2px solid var(--color-interactive-accent);
  outline-offset: 2px;
}

/* --- DISABLED TILLSTÅND --- */
.base-checkbox-wrapper:has(.base-checkbox-input:disabled) {
  cursor: not-allowed;
}
.base-checkbox-input:disabled + .base-checkbox-custom {
  background-color: var(--color-surface-secondary);
  border-color: var(--color-text-low-emphasis);
}
.base-checkbox-input:disabled:checked + .base-checkbox-custom .base-checkbox-checkmark {
  color: var(--color-text-low-emphasis);
  opacity: 1;
  transform: scale(1);
}
.base-checkbox-input:disabled ~ .base-checkbox-label {
  color: var(--color-text-low-emphasis);
}
</style>
<!-- src/shared/ui/BaseCheckbox.vue -->```
