<!-- src/features/mobile-menu-toggle/ui/MobileMenuToggle.vue -->
<!-- Detta är UI-komponenten för hamburgar-knappen. Den renderar en animerad -->
<!-- ikon (hamburgare -> kryss) och använder `useMobileMenu`-logiken för att -->
<!-- växla meny-tillståndet vid klick. -->

<template>
  <button
    class="mobile-menu-toggle"
    :class="{ 'is-active': isMenuOpen }"
    @click="toggleMenu"
    :aria-label="isMenuOpen ? 'Stäng meny' : 'Öppna meny'"
    aria-controls="mobile-nav-menu"
    :aria-expanded="isMenuOpen"
  >
    <svg class="toggle-icon" viewBox="0 0 100 100" width="32" height="32">
      <!-- Topplinjen -->
      <path
        class="line line1"
        d="M 20,29.000046 H 80.000231 C 80.000231,29.000046 94.498839,28.817352 94.532987,66.711331 94.543142,87.969843 90.46731,88.455299 80.740277,88.455299 L 19.259723,88.455299 C -0.478602,88.455299 -0.959981,67.674186 19.259723,29.000046 Z"
      ></path>
      <!-- Mittenlinjen -->
      <path
        class="line line2"
        d="M 20,50 H 80"
      ></path>
      <!-- Bottnenlinjen -->
      <path
        class="line line3"
        d="M 20,70.999954 H 80.000231 C 80.000231,70.999954 94.498839,71.182648 94.532987,33.288669 94.543142,12.030157 90.46731,11.544701 80.740277,11.544701 L 19.259723,11.544701 C -0.478602,11.544701 -0.959981,32.325814 19.259723,70.999954 Z"
      ></path>
    </svg>
  </button>
</template>

<script setup>
import { useMobileMenu } from '../model/useMobileMenu.js';

// Hämtar det reaktiva tillståndet och funktionerna från vår composable.
const { isMenuOpen, toggleMenu } = useMobileMenu();
</script>

<style scoped>
.mobile-menu-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1011; /* Måste vara högre än header (1000) och meny-overlay (1010) */
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.mobile-menu-toggle:hover {
  background-color: var(--color-surface-tertiary);
}

.toggle-icon .line {
  fill: none;
  stroke: var(--color-text-high-emphasis);
  stroke-width: 6;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: stroke-dasharray 0.4s cubic-bezier(0.4, 0, 0.2, 1),
              stroke-dashoffset 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Definition av linjernas ursprungliga utseende (hamburgare) */
.toggle-icon .line1 { stroke-dasharray: 90 207; }
.toggle-icon .line2 { stroke-dasharray: 60 60; }
.toggle-icon .line3 { stroke-dasharray: 90 207; }

/* När knappen är aktiv (meny öppen), animera till ett kryss (X) */
.mobile-menu-toggle.is-active .toggle-icon .line1 {
  stroke-dasharray: 90 207;
  stroke-dashoffset: -134;
}
.mobile-menu-toggle.is-active .toggle-icon .line2 {
  stroke-dasharray: 1 60;
  stroke-dashoffset: -30;
}
.mobile-menu-toggle.is-active .toggle-icon .line3 {
  stroke-dasharray: 90 207;
  stroke-dashoffset: -134;
}
</style>
<!-- src/features/mobile-menu-toggle/ui/MobileMenuToggle.vue -->
