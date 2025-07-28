<!-- src/widgets/GlobalHeader/GlobalHeader.vue -->
<!-- Denna widget är den primära, globala headern för hela applikationen. -->
<!-- Den är en sammansatt komponent som innehåller logotyp, primär navigering -->
<!-- och en platshållare för temaväxlaren. -->

<template>
  <header class="global-header">
    <div class="header-container">
      
      <!-- Vänster sektion: Logotyp -->
      <div class="header-left">
        <Logo />
      </div>

      <!-- Mitten sektion: Primär navigering -->
      <nav class="header-nav">
        <router-link to="/alignment-calculator" class="nav-link">Alignment Calculator</router-link>
        <router-link to="/compliance-estimator" class="nav-link">Compliance Estimator</router-link>
        <router-link to="/data-explorer" class="nav-link">Data Explorer</router-link>
      </nav>

      <!-- Höger sektion: Platshållare för framtida funktioner -->
      <div class="header-right">
        <!-- Platshållare för den framtida theme-toggle-featuren. -->
        <!-- För tillfället används en BaseButton för att visualisera platsen. -->
        <BaseButton variant="secondary">
          Theme
        </BaseButton>
      </div>

    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import Logo from '../../shared/ui/Logo.vue';
import BaseButton from '../../shared/ui/BaseButton.vue';
</script>

<style scoped>
/* Grundläggande stilar för header-elementet. */
.global-header {
  width: 100%;
  background-color: var(--color-surface-secondary);
  border-bottom: 1px solid var(--color-border-primary);
  /* z-index säkerställer att headern alltid ligger överst. */
  z-index: 1000; 

  /* Initialt är den statisk, kommer att göras 'fixed' vid integration i App.vue */
  position: relative;
}

/* En container för att centrera och begränsa innehållets bredd. */
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px; /* En lite bredare max-width för headern */
  margin: 0 auto;
  padding: 0 2rem;
  height: 64px; /* Standardhöjd för en header */
}

/* Vänster sektion (Logotyp) */
.header-left {
  flex-shrink: 0; /* Förhindrar att logotypen krymper */
}

/* Mitten sektion (Navigering) */
.header-nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-label);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-medium-emphasis);
  text-decoration: none;
  padding: 0.5rem 0;
  position: relative;
  transition: color 0.2s ease-in-out;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--color-interactive-accent);
  transform: scaleX(0);
  transform-origin: center;
  transition: transform 0.3s ease;
}

.nav-link:hover {
  color: var(--color-text-high-emphasis);
}

/* Vue Routers aktiva länk-klass för att markera den nuvarande sidan. */
.nav-link.router-link-exact-active {
  color: var(--color-text-high-emphasis);
}

.nav-link.router-link-exact-active::after {
  transform: scaleX(1);
}

/* Höger sektion (Platshållare) */
.header-right {
  flex-shrink: 0;
}

/* Responsivitet: Dölj navigationslänkarna på mindre skärmar */
/* Detta är en enkel lösning; en framtida "hamburgermeny" skulle vara mer robust. */
@media (max-width: 768px) {
  .header-nav {
    display: none;
  }
}
</style>
<!-- src/widgets/GlobalHeader/GlobalHeader.vue -->
