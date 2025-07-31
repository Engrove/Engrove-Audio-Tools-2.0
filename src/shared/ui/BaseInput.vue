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
defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

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
  background-color: var(--color-surface-tertiary);
  color: var(--color-text-high-emphasis);
  border: 1px solid var(--color-border-primary);
  padding: 0.75rem 1rem;
}

.base-input::placeholder {
  color: var(--color-text-low-emphasis);
  opacity: 1;
}

/* ========================================================================== */
/* INTERAKTIVA TILLSTÅND                                                      */
/* ========================================================================== */
.base-input:hover:not(:disabled) {
  border-color: var(--color-text-medium-emphasis);
}

.base-input:focus {
  outline: none;
  border-width: 2px;
  padding: calc(0.75rem - 1px) calc(1rem - 1px);
  background-color: var(--color-surface-secondary);
  border-color: var(--color-interactive-accent);
  box-shadow: 0 0 0 2px rgba(51, 145, 255, 0.3);
}

.base-input:disabled {
  background-color: var(--color-surface-secondary);
  color: var(--color-text-low-emphasis);
  border-color: var(--color-border-primary);
  cursor: not-allowed;
}

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR LJUST LÄGE                                           */
/* ========================================================================== */
:global(.light-theme) .base-input:focus {
  background-color: var(--color-surface-primary);
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

/* ========================================================================== */
/* TEMA-ÖVERSTYRNING FÖR KOMPAKT LÄGE (REVIDERAD)                             */
/* ========================================================================== */
:global(.compact-theme) .base-input {
  /* Signifikant minskad padding för ett mycket lägre fält */
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
}

:global(.compact-theme) .base-input:focus {
  /* Justerar focus-padding för att matcha den nya standard-paddingen */
  padding: calc(0.4rem - 1px) calc(0.75rem - 1px);
}
</style>
<!-- src/shared/ui/BaseInput.vue -->
