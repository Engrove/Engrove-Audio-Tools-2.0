<!-- src/App.vue -->
<!-- Detta är applikationens rotkomponent. Den fungerar som den huvudsakliga layout-behållaren, -->
<!-- renderar olika sidor via Vue Router, och inkluderar nu även den globala sidfoten. -->
<!-- Den har uppdaterats för att hantera både färgtema och densitetstema. -->


<template>
  <div id="app-container" :class="containerClasses">
    <!-- Den globala headern är en permanent del av layouten. -->
    <GlobalHeader />

    <main class="main-content">
      <!-- Vue Router kommer att rendera den aktuella sidans komponent här. -->
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Den globala sidfoten, nu en permanent del av layouten. -->
    <GlobalFooter />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { RouterView } from 'vue-router';
import { useThemeStore } from './features/theme-toggle/model/themeStore.js';
import { useSettingsStore } from './entities/settings/model/settingsStore.js'; // Importerar den nya storen
import GlobalHeader from './widgets/GlobalHeader/GlobalHeader.vue';
import GlobalFooter from './widgets/GlobalFooter/GlobalFooter.vue';

// Hämtar instanser av våra stores.
const themeStore = useThemeStore();
const settingsStore = useSettingsStore();

// Skapar en beräknad egenskap som returnerar en array av CSS-klasser.
// Detta kombinerar logiken för både färgtema och densitetstema.
const containerClasses = computed(() => {
  const classes = [];
  
  // Om isDarkTheme är falskt, lägg till 'light-theme'.
  if (!themeStore.isDarkTheme) {
    classes.push('light-theme');
  }

  // Om isCompact är sant, lägg till 'compact-theme'.
  if (settingsStore.isCompact) {
    classes.push('compact-theme');
  }

  return classes;
});
</script>

<style scoped>
/* Scoped-stilar som endast appliceras på denna App.vue-komponent. */
/* De definierar den övergripande layouten för applikationen. */

#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--color-surface-primary);
  color: var(--color-text-medium-emphasis);
  transition: background-color 0.3s, color 0.3s;
}

.main-content {
  flex-grow: 1; /* Säkerställer att huvudinnehållet tar upp allt tillgängligt utrymme */
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
