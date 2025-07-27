<!-- src/shared/ui/BaseSelect.vue -->
<!-- Detta är en grundläggande, återanvändbar dropdown-menykomponent (select). -->
<!-- Den är en del av det centrala UI-biblioteket. -->
<!-- IMPLEMENTATION VÄNTAR. -->
<template>
  <div class="base-select-wrapper">
    <select class="base-select">
      <option>Alternativ 1</option>
      <option>Alternativ 2</option>
    </select>
    <span class="base-select-arrow"></span>
  </div>
</template>

<script setup>
// Props och logik för komponenten kommer att definieras här.
// Exempel på props kan vara: options (array), disabled, modelValue.
</script>

<style scoped>
/* Stilar för komponenten, enligt komponentspecifikationen, kommer här. */
.base-select-wrapper {
  position: relative;
  width: 100%;
}

.base-select {
  /* Tillfällig stil för att vara synlig i showcase */
  border: 1px dashed #555;
  padding: 0.75rem 1rem;
  background-color: #222;
  color: #fff;
  border-radius: 8px;
  width: 100%;
  appearance: none; /* Tar bort webbläsarens standard-pil */
}

.base-select-arrow {
  /* Tillfällig pil-indikator */
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid #888;
  pointer-events: none;
}
</style>
<!-- src/shared/ui/BaseSelect.vue -->
