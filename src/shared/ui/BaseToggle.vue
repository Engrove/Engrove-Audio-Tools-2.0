<!-- src/shared/ui/BaseToggle.vue -->
<!-- Detta är en grundläggande, återanvändbar växlarekomponent (toggle switch). -->
<!-- Den är en del av det centrala UI-biblioteket. -->
<!-- IMPLEMENTATION VÄNTAR. -->
<template>
  <label class="base-toggle">
    <input type="checkbox" class="base-toggle-input">
    <span class="base-toggle-slider"></span>
  </label>
</template>

<script setup>
// Props och logik för komponenten kommer att definieras här.
// Exempel på props kan vara: disabled, modelValue.
</script>

<style scoped>
/* Stilar för komponenten, enligt komponentspecifikationen, kommer här. */
.base-toggle {
  /* Tillfällig stil för att vara synlig i showcase */
  position: relative;
  display: inline-block;
  width: 50px;
  height: 28px;
}

.base-toggle-input {
  opacity: 0;
  width: 0;
  height: 0;
}

.base-toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #555;
  border-radius: 28px;
  transition: .4s;
}

.base-toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  border-radius: 50%;
  transition: .4s;
}

.base-toggle-input:checked + .base-toggle-slider {
  background-color: #3391FF; /* Tillfällig 'på'-färg */
}

.base-toggle-input:checked + .base-toggle-slider:before {
  transform: translateX(22px);
}
</style>
<!-- src/shared/ui/BaseToggle.vue -->
