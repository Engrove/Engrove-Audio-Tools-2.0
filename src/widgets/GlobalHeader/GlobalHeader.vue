<!-- src/widgets/GlobalHeader/GlobalHeader.vue -->
<!-- Denna widget är den primära, globala headern för hela applikationen. -->
<!-- Den är nu fullt responsiv och inkluderar den fungerande temaväxlaren. -->
<!-- Den har nu uppdaterats för att även inkludera densitetsväxlaren och -->
<!-- en villkorlig felsökningsknapp. -->

<template>
  <div>
    <header class="global-header">
      <div class="header-container">
        
        <!-- Vänster sektion: Logotyp -->
        <div class="header-left">
          <Logo />
        </div>

        <!-- Mitten sektion: Traditionell navigering för desktop -->
        <nav class="header-nav-desktop">
          <!-- TODO: Lägg till länk för Alignment Calculator här -->
          <!-- TODO: Lägg till länk för Compliance Estimator här -->
          
          <router-link to="/data-explorer" class="nav-link">Data Explorer</router-link>

        </nav>

        <!-- Höger sektion: Knappar och kontroller -->
        <div class="header-right">
          <!-- Felsökningsknapp, visas ENDAST i utvecklingsläge -->
          <a v-if="IS_DEBUG_MODE" href="/debug.html" target="_blank" rel="noopener noreferrer">
            <BaseButton variant="secondary" class="debug-button">Debug</BaseButton>
          </a>

          <!-- Densitetsväxlaren, visas endast på desktop. -->
          <DensityToggle class="density-toggle-desktop" />

          <!-- Den fungerande temaväxlaren, visas endast på desktop. -->
          <ThemeToggle class="theme-toggle-desktop" />
          
          <!-- Hamburgar-knappen, visas endast på mobil -->
          <MobileMenuToggle class="mobile-menu-toggle-button" />
        </div>

      </div>
    </header>

    <!-- Mobilmeny-overlay (utanför header-elementet för korrekt stackning) -->
    <Transition name="fade">
      <MobileNavMenu v-if="isMenuOpen" />
    </Transition>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import { useMobileMenu } from '../../features/mobile-menu-toggle/model/useMobileMenu.js';
// Importerar nu konstanten direkt för en mer robust kontroll.
import { IS_DEBUG_MODE } from '../../entities/logger/model/loggerStore.js';
import Logo from '../../shared/ui/Logo.vue';
import MobileMenuToggle from '../../features/mobile-menu-toggle/ui/MobileMenuToggle.vue';
import MobileNavMenu from '../MobileNavMenu/MobileNavMenu.vue';
import ThemeToggle from '../../features/theme-toggle/ui/ThemeToggle.vue';
import DensityToggle from '../../features/density-toggle/ui/DensityToggle.vue';
import BaseButton from '../../shared/ui/BaseButton.vue';

// FELSÖKNING: Logga värdet av IS_DEBUG_MODE direkt när komponenten skapas.
console.log(`[GlobalHeader] IS_DEBUG_MODE is: ${IS_DEBUG_MODE}`);

// Hämtar meny-tillståndet för att styra visningen av mobilmenyn
const { isMenuOpen } = useMobileMenu();

</script>

<style scoped>
/* Grundläggande stilar för header-elementet. */
.global-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: var(--color-surface-secondary);
  border-bottom: 1px solid var(--color-border-primary);
  z-index: 1000;
}

/* Container för att centrera och begränsa innehållets bredd. */
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 64px;
}

.header-left {
  flex-shrink: 0;
}

/* Navigering för desktop */
.header-nav-desktop {
  display: flex;
  gap: 2rem;
  margin-left: auto; /* Skjuter navigeringen åt vänster */
  padding-right: 2rem; /* Ger utrymme till kontrollerna */
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

.nav-link.router-link-exact-active {
  color: var(--color-text-high-emphasis);
}

.nav-link.router-link-exact-active::after {
  transform: scaleX(1);
}

/* Höger sektion */
.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.debug-button {
  /* Lite extra styling för att göra den mindre framträdande */
  padding: 0.4rem 0.8rem;
  font-size: var(--font-size-small);
  border-color: var(--color-status-error);
  color: var(--color-status-error);
}

.debug-button:hover {
    background-color: var(--color-status-error);
    color: var(--color-text-high-emphasis);
}

/* Initialt döljs hamburgar-knappen på större skärmar */
.mobile-menu-toggle-button {
  display: none;
}

/* ========================================================================== */
/* RESPONSIVITET                                                              */
/* ========================================================================== */

/* Brytpunkt för när mobil-layouten ska aktiveras (t.ex. surfplattor och mindre) */
@media (max-width: 900px) {
  .header-nav-desktop,
  .theme-toggle-desktop,
  .density-toggle-desktop {
    display: none; /* Dölj desktop-navigering och alla kontroller */
  }
  
  /* Dölj debug-knappen även på mobil för att spara utrymme */
  .header-right a[href="/debug.html"] {
    display: none;
  }

  .mobile-menu-toggle-button {
    display: flex; /* Visa hamburgar-knappen */
  }
  
  .header-left {
    margin-right: auto; /* Säkerställer att loggan stannar till vänster */
  }

  .header-container {
    padding: 0 1rem; /* Minska padding på mindre skärmar */
  }
}

/* ========================================================================== */
/* ÖVERGÅNGSANIMATION FÖR MOBILMENY                                            */
/* ========================================================================== */

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
<!-- src/widgets/GlobalHeader/GlobalHeader.vue -->
