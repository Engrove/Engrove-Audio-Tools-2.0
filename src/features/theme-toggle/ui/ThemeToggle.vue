<!-- src/features/theme-toggle/ui/ThemeToggle.vue -->
<!-- Detta är UI-komponenten för temaväxlaren. Den visar en sol- eller -->
<!-- mån-ikon beroende på aktivt tema och anropar `toggleTheme`-actionen -->
<!-- från `themeStore` vid klick. -->

<template>
  <BaseButton
    variant="secondary"
    @click="themeStore.toggleTheme"
    :aria-label="themeStore.isDarkTheme ? 'Växla till ljust tema' : 'Växla till mörkt tema'"
    class="theme-toggle-button"
  >
    <transition name="fade" mode="out-in">
      <!-- Visar mån-ikonen om det är mörkt tema -->
      <svg v-if="themeStore.isDarkTheme" key="moon" class="theme-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      <!-- Annars, visa sol-ikonen -->
      <svg v-else key="sun" class="theme-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
    </transition>
  </BaseButton>
</template>

<script setup>

  
import { useThemeStore } from '@/entities/theme/model/themeStore.js';
import BaseButton from '../../../shared/ui/BaseButton.vue';

// Hämtar en instans av vår theme store.
const themeStore = useThemeStore();
</script>

<style scoped>
.theme-toggle-button {
  /* Säkerställer att knappen är cirkulär och har fast storlek */
  width: 44px;
  height: 44px;
  border-radius: 50%;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.theme-icon {
  color: var(--color-text-medium-emphasis);
  transition: color 0.2s ease-in-out;
}

.theme-toggle-button:hover .theme-icon {
  color: var(--color-text-high-emphasis);
}

/* Animation för in- och uttoning av ikonerna */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
<!-- src/features/theme-toggle/ui/ThemeToggle.vue -->
