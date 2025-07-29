<!-- src/shared/ui/RangeFilter.vue -->
<!--
  Detta är en agnostisk och återanvändbar komponent för att filtrera på ett numeriskt intervall.
  Den består av två inmatningsfält (för min och max) och är byggd med BaseInput-komponenten
  för att säkerställa visuell konsekvens med den globala UI-standarden.
  Den stödjer v-model för tvåvägs databindning.
-->
<template>
  <div class="range-filter-group">
    <label v-if="label" class="filter-label">{{ label }}</label>
    <div class="inputs-wrapper">
      <BaseInput
        :model-value="minValue"
        @update:modelValue="updateValue('min', $event)"
        :placeholder="minPlaceholder"
        type="number"
      />
      <span class="separator">–</span>
      <BaseInput
        :model-value="maxValue"
        @update:modelValue="updateValue('max', $event)"
        :placeholder="maxPlaceholder"
        type="number"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import BaseInput from './BaseInput.vue';

// --- PROPS & EMITS ---

/**
 * @props {Object} modelValue - Det bundna värdet via v-model. Ska vara ett objekt
 *   med 'min' och 'max'-egenskaper, t.ex. { min: null, max: 10 }.
 * @props {String} label - Etiketten som visas ovanför filterkomponenten.
 * @props {String} unit - Enheten som visas som en del av platshållartexten.
 */
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: () => ({ min: null, max: null }),
    validator: (value) => 
      typeof value === 'object' && 'min' in value && 'max' in value,
  },
  label: {
    type: String,
    default: '',
  },
  unit: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['update:modelValue']);


// --- COMPUTED PROPERTIES ---

// Beräknade platshållare för inmatningsfälten.
const minPlaceholder = computed(() => `Min ${props.unit}`.trim());
const maxPlaceholder = computed(() => `Max ${props.unit}`.trim());

// Säkrar att vi inte muterar props direkt. Används för att binda till BaseInput.
const minValue = computed(() => props.modelValue.min);
const maxValue = computed(() => props.modelValue.max);


// --- FUNKTIONER ---

/**
 * Uppdaterar värdet och skickar en 'update:modelValue'-händelse.
 * Konverterar tomma strängar till null för att representera avsaknad av värde.
 * @param {'min' | 'max'} key - Vilken del av intervallet som ska uppdateras.
 * @param {string | number} value - Det nya värdet från BaseInput.
 */
const updateValue = (key, value) => {
  const newRange = { ...props.modelValue };
  
  // Om värdet är en tom sträng, sätt det till null. Annars, konvertera till flyttal.
  const numericValue = value === '' || value === null ? null : parseFloat(value);
  
  newRange[key] = numericValue;
  
  emit('update:modelValue', newRange);
};
</script>

<style scoped>
.range-filter-group {
  width: 100%;
}

.filter-label {
  display: block;
  font-weight: var(--font-weight-medium);
  color: var(--color-text-medium-emphasis);
  margin-bottom: 0.75rem;
  font-size: var(--font-size-label);
}

.inputs-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.separator {
  color: var(--color-text-low-emphasis);
  font-weight: var(--font-weight-bold);
}

/* Överstyr BaseInput för att ta bort webbläsarens nummerpilar (spinners) */
:deep(input[type="number"]::-webkit-outer-spin-button),
:deep(input[type="number"]::-webkit-inner-spin-button) {
  -webkit-appearance: none;
  margin: 0;
}

:deep(input[type="number"]) {
  -moz-appearance: textfield;
}
</style>
<!-- src/shared/ui/RangeFilter.vue -->
