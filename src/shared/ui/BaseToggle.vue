<!-- src/shared/ui/BaseToggle.vue -->
<!-- Grundläggande, återanvändbar växlarekomponent (toggle switch). -->
<!-- Implementerad enligt Global UI-Standard Komponentspecifikation (Sektion 4.1 & 4.2). -->
<template>
  <label class="base-toggle">
    <input
      type="checkbox"
      class="base-toggle-input"
      :checked="modelValue"
      :disabled="disabled"
      @change="$emit('update:modelValue', $event.target.checked)"
    />
    <span class="base-toggle-slider"></span>
  </label>
</template>

<script setup>
// Defines the component's props (API) and emitted events.
// This component supports v-model for two-way data binding.

defineProps({
  // Status för växlaren (true = på, false = av), används med v-model
  modelValue: {
    type: Boolean,
    default: false,
  },
  // Inaktiverar växlaren om satt till true
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
/* GRUNDSTRUKTUR OCH POSITIONERING                                            */
/* ========================================================================== */
.base-toggle {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 28px;
  cursor: pointer;
}

/* Den faktiska checkboxen är dold, men funktionell för tillgänglighet */
.base-toggle-input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

/* Det visuella spåret (slider) för växlaren */
.base-toggle-slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 28px;
  background-color: var(--color-surface-tertiary);
  transition: background-color 0.2s ease-in-out;
}

/* Det visuella handtaget för växlaren */
.base-toggle-slider::before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 4px;
  bottom: 4px;
  border-radius: 50%;
  background-color: var(--color-text-medium-emphasis);
  transition: transform 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

/* ========================================================================== */
/* INTERAKTIVA TILLSTÅND                                                      */
/* ========================================================================== */

/* --- PÅ (ON) TILLSTÅND --- */
.base-toggle-input:checked + .base-toggle-slider {
  background-color: var(--color-interactive-accent);
}

.base-toggle-input:checked + .base-toggle-slider::before {
  background-color: var(--color-surface-primary);
  transform: translateX(22px);
}

/* --- HOVER TILLSTÅND --- */
/* Hover när AV */
.base-toggle-input:hover:not(:disabled):not(:checked) + .base-toggle-slider::before {
  background-color: var(--color-text-high-emphasis);
}
/* Hover när PÅ */
.base-toggle-input:hover:not(:disabled):checked + .base-toggle-slider {
  background-color: var(--color-interactive-accent-hover);
}

/* --- FOCUS TILLSTÅND (ENDAST TANGENTBORD) --- */
.base-toggle-input:focus-visible + .base-toggle-slider {
  outline: 2px solid var(--color-interactive-accent);
  outline-offset: 2px;
}

/* --- DISABLED TILLSTÅND --- */
.base-toggle-input:disabled + .base-toggle-slider {
  background-color: var(--color-surface-secondary);
}

.base-toggle-input:disabled + .base-toggle-slider::before {
  background-color: var(--color-text-low-emphasis);
}

.base-toggle-input:disabled ~ .base-toggle-slider {
    cursor: not-allowed;
}

.base-toggle {
    cursor: pointer;
}

.base-toggle-input:disabled {
    cursor: not-allowed;
}

.base-toggle-input:disabled + .base-toggle-slider {
    cursor: not-allowed;
}
</style>
<!-- src/shared/ui/BaseToggle.vue -->
