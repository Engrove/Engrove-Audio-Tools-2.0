<!-- src/App.vue -->
<!-- Detta är applikationens rotkomponent. Den fungerar som den huvudsakliga layout-behållaren -->
<!-- och kommer att rendera olika sidor via Vue Router. Den inkluderar nu den globala headern. -->

<template>
  <div id="app-container">
    <!-- Den globala headern är nu en permanent del av layouten. -->
    <GlobalHeader />

    <main class="main-content">
      <!-- Vue Router kommer att rendera den aktuella sidans komponent här. -->
      <!-- Den tidigare platshållartexten är borttagen. -->
      <router-view />
    </main>

  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import GlobalHeader from './widgets/GlobalHeader/GlobalHeader.vue';
</script>

<style scoped>
/* Scoped-stilar som endast appliceras på denna App.vue-komponent. */
/* De definierar den övergripande layouten för applikationen. */

#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex-grow: 1;
  width: 100%;
  
  /* Viktigt: Lägger till padding-top som motsvarar headerns höjd (64px). */
  /* Detta förhindrar att innehållet på sidan döljs bakom den fasta headern. */
  padding-top: 64px; 
}

/* Anpassningar för att sidinnehållet ska vara centrerat */
/* Denna del av koden kan tas bort eller justeras när sidorna får mer innehåll. */
:deep(.main-content > *) {
  width: 100%;
  max-width: 1200px; /* Sätter en maxbredd för innehållet */
  margin: 0 auto; /* Centrerar innehållet horisontellt */
  padding: 2rem; /* Ger lite luft runt innehållet */
}
</style>
<!-- src/App.vue -->
