<!-- src/shared/ui/BaseCheckbox.vue -->
<!-- Detta är en grundläggande, återanvändbar kryssrutekomponent. -->
<!-- Den är en del av det centrala UI-biblioteket. -->
<!-- IMPLEMENTATION VÄNTAR. -->
<template>
  <label class="base-checkbox-wrapper">
    <input type="checkbox" class="base-checkbox-input">
    <span class="base-checkbox-custom"></span>
    <span class="base-checkbox-label"><slot></slot></span>
  </label>
</template>

<script setup>
// Props och logik för komponenten kommer att definieras här.
// Exempel på props kan vara: label, disabled, modelValue.
</script>

<style scoped>
/* Stilar för komponenten, enligt komponentspecifikationen, kommer här. */
.base-checkbox-wrapper {
  /* Tillfällig stil för att vara synlig i showcase */
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  gap: 0.75rem;
}

.base-checkbox-input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.base-checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #888;
  border-radius: 4px;
  display: inline-block;
  position: relative;
}

.base-checkbox-input:checked ~ .base-checkbox-custom {
  background-color: #3391FF; /* Tillfällig 'markerad'-färg */
  border-color: #3391FF;
}

.base-checkbox-custom::after {
  content: "";
  position: absolute;
  display: none;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 3px 3px 0;
  transform: rotate(45deg);
}

.base-checkbox-input:checked ~ .base-checkbox-custom::after {
  display: block;
}

.base-checkbox-label {
  color: var(--color-text-medium-emphasis);
}
</style>
<!-- src/shared/ui/BaseCheckbox.vue -->
