<!-- src/App.vue -->
<!-- Detta är applikationens rotkomponent. Den fungerar som den huvudsakliga layout-behållaren, -->
<!-- renderar olika sidor via Vue Router, och applicerar nu dynamiskt temaklassen. -->

<template>
  <div id="app-container" :class="themeClass">
    <!-- Den globala headern är nu en permanent del av layouten. -->
    <GlobalHeader />

    <main class="main-content">
      <!-- Vue Router kommer att rendera den aktuella sidans komponent här. -->
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

  </div>
</template>

<script setup>
import { computed } from 'vue';
import { RouterView } from 'vue-router';
import { useThemeStore } from './features/theme-toggle/model/themeStore.js';
import GlobalHeader from './widgets/GlobalHeader/GlobalHeader.vue';

// Hämtar en instans av vår theme store.
const themeStore = useThemeStore();

// Skapar en beräknad egenskap som returnerar CSS-klassen för temat.
const themeClass = computed(() => (
  // Om isDarkTheme är sant, returnera en tom sträng (eftersom mörkt tema är standard).
  // Om isDarkTheme är falskt, returnera 'light-theme'.
  themeStore.isDarkTheme ? '' : 'light-theme'
));
</script>

<style scoped>
/* Scoped-stilar som endast appliceras på denna App.vue-komponent. */
/* De definierar den övergripande layouten för applikationen. */

#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  /* Applicerar grundläggande bakgrunds- och textfärg från tokens. */
  /* Detta säkerställer att övergången mellan teman är mjuk. */
  background-color: var(--color-surface-primary);
  color: var(--color-text-medium-emphasis);
  transition: background-color 0.3s, color 0.3s;
}

.main-content {
  flex-grow: 1;
  width: 100%;
  padding-top: 64px; /* Kompenserar för den fasta headerns höjd. */
}

/* Övergångsanimation för sidbyten */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
<!-- src/App.vue -->
