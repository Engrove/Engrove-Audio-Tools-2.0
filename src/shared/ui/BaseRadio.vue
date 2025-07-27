<!-- src/shared/ui/BaseRadio.vue -->
<!-- Detta är en grundläggande, återanvändbar radioknappkomponent. -->
<!-- Den är en del av det centrala UI-biblioteket. -->
<!-- IMPLEMENTATION VÄNTAR. -->
<template>
  <label class="base-radio-wrapper">
    <input type="radio" class="base-radio-input" :name="name" :value="value">
    <span class="base-radio-custom"></span>
    <span class="base-radio-label"><slot></slot></span>
  </label>
</template>

<script setup>
// Props och logik för komponenten kommer att definieras här.
// Exempel på props kan vara: name, value, disabled, modelValue.
defineProps({
  name: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  }
})
</script>

<style scoped>
/* Stilar för komponenten, enligt komponentspecifikationen, kommer här. */
.base-radio-wrapper {
  /* Tillfällig stil för att vara synlig i showcase */
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  gap: 0.75rem;
}

.base-radio-input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.base-radio-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #888;
  border-radius: 50%;
  display: inline-block;
  position: relative;
}

.base-radio-input:checked ~ .base-radio-custom {
  border-color: #3391FF; /* Tillfällig 'vald'-färg */
}

.base-radio-custom::after {
  content: "";
  position: absolute;
  display: none;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #3391FF;
}

.base-radio-input:checked ~ .base-radio-custom::after {
  display: block;
}

.base-radio-label {
  color: var(--color-text-medium-emphasis);
}
</style>
<!-- src/shared/ui/BaseRadio.vue -->
