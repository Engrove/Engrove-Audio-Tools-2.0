<!-- src/shared/ui/BaseInput.vue -->
<!-- Grundläggande, återanvändbar inmatningsfältskomponent. -->
<!-- Implementerad enligt Global UI-Standard Komponentspecifikation (Sektion 2.1 & 2.2). -->
<template>
  <input
    class="base-input"
    :value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<script setup>
// Defines the component's props (API) and emitted events.
// This component supports v-model for two-way data binding.

defineProps({
  // Värdet för inmatningsfältet, används med v-model
  modelValue: {
    type: [String, Number],
    default: '',
  },
  // Platshållartext som visas när fältet är tomt
  placeholder: {
    type: String,
    default: '',
  },
  // Inaktiverar fältet om satt till true
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
/* GRUNDLÄGGANDE STILAR                                                       */
/* ========================================================================== */
.base-input {
  width: 100%;
  border-radius: 8px;
  font-family: var(--font-family-primary);
  font-size: var(--font-size-body);
  transition: border-color 0.2s, background-color 0.2s, box-shadow 0.2s;

  /* Default state styles (gäller för båda teman) */
  background-color: var(--color-surface-tertiary);
  color: var(--color-text-high-emphasis);
  border: 1px solid var(--color-border-primary);
  padding: 0.75rem 1rem; /* 12px 16px */
}

/* Specifik styling för platshållartexten */
.base-input::placeholder {
  color: var(--color-text-low-emphasis);
  opacity: 1; /* Nödvändigt för att säkerställa konsekvens i Firefox */
}

/* ========================================================================== */
/* INTERAKTIVA TILLSTÅND                                                      */
/* ========================================================================== */

/* Hover-tillstånd (när fältet inte är inaktiverat) */
.base-input:hover:not(:disabled) {
  border-color: var(--color-text-medium-emphasis);
}

/* Focus-tillstånd */
.base-input:focus {
  outline: none; /* Tar bort standard-outline från webbläsaren */
  
  /* Justerar padding för att kompensera för den tjockare kanten, förhindrar layout-hopp */
  border-width: 2px;
  padding: calc(0.75rem - 1px) calc(1rem - 1px);

  /* Mörkt tema (standard) för focus-tillstånd */
  background-color: var(--color-surface-secondary);
  border-color: var(--color-interactive-accent);
  box-shadow: 0 0 0 2px rgba(51, 145, 255, 0.3);
}

/* Inaktiverat tillstånd */
.base-input:disabled {
  background-color: var(--color-surface-secondary);
  color: var(--color-text-low-emphasis);
  border-color: var(--color-border-primary);
  cursor: not-allowed;
}

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR LJUST LÄGE                                           */
/* Denna :global-selektor är nödvändig för att applicera överstyrningar       */
/* baserat på .light-theme-klassen på ett förälderelement (<html> eller <body>)*/
/* från ett scoped style-block.                                               */
/* ========================================================================== */
:global(.light-theme) .base-input:focus {
  background-color: var(--color-surface-primary);
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}
</style>
<!-- src/shared/ui/BaseInput.vue -->
