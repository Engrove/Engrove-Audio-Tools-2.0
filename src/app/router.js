// src/app/router.js
// Denna fil konfigurerar all navigering (routing) för applikationen.
// Den mappar URL-sökvägar till specifika Vue-komponenter (sidor).

import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../pages/home/HomePage.vue';

// Definierar en array av ruttobjekt. Varje objekt representerar en sida.
const routes = [
  {
    path: '/', // Rot-URL (t.ex. https://engrove-audio.pages.dev/)
    name: 'Home',
    component: HomePage, // Komponenten som ska visas för denna sökväg
  },
  // --- PLATSHÅLLARE FÖR FRAMTIDA SIDOR ---
  // Dessa rutter är förberedda men pekar för närvarande på startsidan.
  // De kommer att uppdateras när sidorna för kalkylatorerna skapas.
  {
    path: '/alignment-calculator',
    name: 'AlignmentCalculator',
    component: HomePage, // TODO: Byt ut mot AlignmentCalculatorPage.vue
  },
  {
    path: '/compliance-estimator',
    name: 'ComplianceEstimator',
    component: HomePage, // TODO: Byt ut mot ComplianceEstimatorPage.vue
  },
  {
    path: '/data-explorer',
    name: 'DataExplorer',
    component: HomePage, // TODO: Byt ut mot DataExplorerPage.vue
  },
];

// Skapar en router-instans.
const router = createRouter({
  // `createWebHistory` möjliggör rena URL:er utan hashbang (#).
  // Detta är standard för moderna SPA-applikationer.
  history: createWebHistory(),
  routes, // Använder rutt-definitionerna från ovan.

  // Funktion som säkerställer att användaren alltid scrollas till toppen
  // av sidan vid navigering till en ny sida.
  scrollBehavior(to, from, savedPosition) {
    // Om det finns en sparad position (från webbläsarens bakåt/framåt-knappar),
    // återgå till den. Annars, scrolla till toppen.
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

export default router;
// src/app/router.js
