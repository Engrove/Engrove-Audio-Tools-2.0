<!-- src/App.vue -->
<!-- Detta är applikationens rotkomponent. Den fungerar som den huvudsakliga layout-behållaren -->
<!-- och kommer att rendera olika sidor via Vue Router. -->

<template>
  <div id="app-container">
    <!-- En platshållare för den globala headern som kommer att byggas senare -->
    <!-- <GlobalHeader /> -->

    <main class="main-content">
      <!-- Innehållet nedan är temporärt för att visa att de globala stilarna fungerar. -->
      <!-- Det kommer att ersättas av <router-view /> när navigering implementeras. -->
      <h1>Engrove Audio Toolkit 2.0</h1>
      <p>Applikationens grund med de nya globala stilarna är nu på plats.</p>
    </main>

  </div>
</template>

<script setup>
// Detta är rotkomponenten för applikationen.
// För närvarande krävs ingen specifik JavaScript-logik här.
// Den kommer senare att interagera med globala system som temaväxlaren.
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
  max-width: 1200px; /* Sätter en maxbredd för innehållet */
  margin: 0 auto; /* Centrerar innehållet horisontellt */
  padding: 2rem; /* Ger lite luft runt innehållet */
  
  /* Temporär centrering för platshållartexten */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

h1 {
  /* Använder de globala typografi-tokens som ärvts via _global.css */
  margin-bottom: 1rem;
}

p {
  /* Använder de globala typografi-tokens */
  color: var(--color-text-medium-emphasis);
}
</style>
<!-- src/App.vue -->
