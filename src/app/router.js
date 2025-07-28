// src/app/router.js
// Denna fil definierar all navigering (routing) för applikationen.
// Den mappar URL-sökvägar till specifika sidkomponenter.

import { createRouter, createWebHistory } from 'vue-router';
// Korrigerade sökvägar: Går upp en nivå från /app till /src, sedan ner till /pages.
import HomePage from '../pages/home/HomePage.vue';
import AboutPage from '../pages/about/AboutPage.vue';

// Definition av alla applikationens rutter.
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/about',
    name: 'About',
    component: AboutPage,
  },
  // TODO: Ersätt dessa platshållar-komponenter när de faktiska sidorna skapas.
  // Just nu pekar de till HomePage för att undvika 404-fel från länkarna i headern.
  {
    path: '/alignment-calculator',
    name: 'AlignmentCalculator',
    component: HomePage, // Platshållare
  },
  {
    path: '/compliance-estimator',
    name: 'ComplianceEstimator',
    component: HomePage, // Platshållare
  },
  {
    path: '/data-explorer',
    name: 'DataExplorer',
    component: HomePage, // Platshållare
  },
  // En "catch-all"-rutt för att hantera okända sökvägar, omdirigerar till startsidan.
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  }
];

// Skapar en router-instans.
// createWebHistory används för ren URL-hantering utan #-tecken.
const router = createRouter({
  history: createWebHistory(),
  routes,
  // Denna funktion säkerställer att man alltid scrollar till toppen av sidan vid sidbyte.
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// Exporterar router-instansen så att den kan användas i main.js.
export default router;
// src/app/router.js
