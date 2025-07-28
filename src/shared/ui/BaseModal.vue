<!-- src/shared/ui/BaseModal.vue -->
<!-- En generell och återanvändbar modal-komponent. Den är "dum" och -->
<!-- hanterar endast det visuella och grundläggande interaktioner (visa/dölj, stängning). -->
<!-- Innehållet i modalen injiceras via slots. -->
<template>
  <transition name="modal-fade">
    <div
      v-if="isOpen"
      class="modal-overlay"
      @click.self="close"
    >
      <div class="modal-panel">
        <header class="modal-header">
          <!-- Använder en slot för titeln för flexibilitet -->
          <h3 class="modal-title">
            <slot name="header">Standardrubrik</slot>
          </h3>
          <button @click="close" class="close-button" aria-label="Stäng modal">
            ×
          </button>
        </header>
        <main class="modal-content">
          <!-- Standardslot för huvudinnehållet -->
          <slot></slot>
        </main>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue';

// --- PROPS & EMITS ---
const props = defineProps({
  // Styr synligheten av modalen. Stödjer v-model:isOpen.
  isOpen: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['update:isOpen']);

// --- FUNKTIONER ---
const close = () => {
  emit('update:isOpen', false);
};

// Hanterar tangentbordstryckningar, specifikt för 'Escape'-tangenten.
const handleKeyDown = (event) => {
  if (event.key === 'Escape' && props.isOpen) {
    close();
  }
};

// --- LIFECYCLE & WATCHERS ---
// När modalen öppnas (props.isOpen blir true), lås scroll på body.
// När den stängs, lås upp.
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    document.body.classList.add('body-scroll-lock');
  } else {
    document.body.classList.remove('body-scroll-lock');
  }
});

// Lägg till och ta bort eventlyssnare för tangentbordet när komponenten
// monteras och avmonteras för att undvika minnesläckor.
onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
  // Säkerställ att scroll-lock tas bort om komponenten avmonteras medan den är öppen.
  document.body.classList.remove('body-scroll-lock');
});
</script>

<style scoped>
/* Övergång för in- och uttoning av hela modalen */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Bakgrunds-overlay som täcker hela skärmen */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000; /* Högt z-index för att ligga över allt annat */
}

/* Panelen som innehåller själva modalens innehåll */
.modal-panel {
  display: flex;
  flex-direction: column;
  background-color: var(--color-surface-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 800px;
  max-height: 90vh; /* Begränsar höjden så den inte tar över hela skärmen */
  overflow: hidden; /* Förhindrar att innehåll går utanför rundade hörn */
}

/* Header-sektionen av modalen */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--color-border-primary);
  flex-shrink: 0; /* Förhindrar att headern krymper */
}

.modal-title {
  color: var(--color-text-high-emphasis);
  font-size: var(--font-size-h3);
  margin: 0;
}

/* Stängningsknappen (X) */
.close-button {
  background: none;
  border: none;
  font-size: 2rem;
  font-weight: 300;
  line-height: 1;
  color: var(--color-text-medium-emphasis);
  cursor: pointer;
  padding: 0.5rem;
  margin: -0.5rem; /* Negativ marginal för att öka klickytan */
  transition: color 0.2s, transform 0.2s;
}
.close-button:hover {
  color: var(--color-text-high-emphasis);
  transform: rotate(90deg);
}

/* Innehållssektionen av modalen */
.modal-content {
  padding: 1.5rem;
  overflow-y: auto; /* Gör innehållet scrollbart om det är för högt */
}
</style>
<!-- src/shared/ui/BaseModal.vue -->
