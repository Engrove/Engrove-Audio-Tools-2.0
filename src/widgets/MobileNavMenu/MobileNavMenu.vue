<!-- src/widgets/MobileNavMenu/MobileNavMenu.vue -->
<!-- Denna widget är den "off-canvas" navigeringsmeny som visas på mobila enheter. -->
<!-- Den visas som en helskärms-overlay när hamburgar-knappen aktiveras. -->

<template>
  <nav id="mobile-nav-menu" class="mobile-nav-menu">
    <div class="menu-container">
      <router-link to="/alignment-calculator" class="menu-link" @click="closeMenu">
        Alignment Calculator
      </router-link>
      <router-link to="/compliance-estimator" class="menu-link" @click="closeMenu">
        Compliance Estimator
      </router-link>
      <router-link to="/data-explorer" class="menu-link" @click="closeMenu">
        Data Explorer
      </router-link>

      <!-- Platshållare för framtida länkar eller funktioner -->
      <div class="menu-divider"></div>

      <a href="https://github.com/Engrove/Engrove-Audio-Tools-2.0" target="_blank" rel="noopener noreferrer" class="menu-link" @click="closeMenu">
        View on GitHub
      </a>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useMobileMenu } from '../../features/mobile-menu-toggle/model/useMobileMenu.js';

// Hämtar funktionen för att stänga menyn.
// Menyn stängs när användaren klickar på en länk för en smidig upplevelse.
const { closeMenu } = useMobileMenu();
</script>

<style scoped>
/* Grundläggande stilar för overlay-menyn */
.mobile-nav-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  
  /* Använder en lätt genomskinlig primär ytfärg för en modern känsla */
  background-color: rgba(18, 18, 18, 0.95);
  /* 'backdrop-filter' skapar en suddig effekt på innehållet bakom menyn */
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);

  z-index: 1010; /* Lägre än hamburgarknappen, men högre än headern */

  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

/* Container för länkarna */
.menu-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Stilar för varje enskild navigeringslänk */
.menu-link {
  font-family: var(--font-family-primary);
  /* Använder en större fontstorlek för enkel klickbarhet på mobil */
  font-size: var(--font-size-h2); /* 24px */
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-medium-emphasis);
  text-decoration: none;
  padding: 1rem;
  border-radius: 8px;
  transition: color 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

.menu-link:hover {
  color: var(--color-text-high-emphasis);
  background-color: var(--color-surface-tertiary);
}

/* Vue Routers aktiva länk-klass för att markera den nuvarande sidan. */
.menu-link.router-link-exact-active {
  color: var(--color-interactive-accent);
}

.menu-divider {
  height: 1px;
  width: 80%;
  margin: 1rem auto;
  background-color: var(--color-border-primary);
}
</style>
<!-- src/widgets/MobileNavMenu/MobileNavMenu.vue -->
