// src/app/router.js
/**
 * Denna fil konfigurerar Vue Router för hela applikationen.
 * Den definierar alla tillgängliga "sidor" (routes) och kopplar dem
 * till deras respektive sidkomponenter från /src/pages/.
 */
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../pages/home/HomePage.vue';
import AboutPage from '../pages/about/AboutPage.vue';
import DataExplorerPage from '../pages/data-explorer/DataExplorerPage.vue'; // <-- NY IMPORT

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
  {
    // --- NY ROUTE FÖR DATA EXPLORER ---
    path: '/data-explorer',
    name: 'DataExplorer',
    component: DataExplorerPage,
  },
  // TODO: Lägg till routes för Alignment Calculator och Compliance Estimator här.
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  // Funktion för att scrolla till toppen av sidan vid varje sidbyte.
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

export default router;
// src/app/router.js
