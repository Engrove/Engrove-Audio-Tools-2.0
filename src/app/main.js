// src/app/main.js
// Detta är applikationens primära startpunkt. Den ansvarar för att
// skapa och konfigurera Vue-instansen, samt att montera den i DOM.
//
// KORRIGERING:
// - Korrekt initialisering av Pinia har lagts till. En Pinia-instans skapas
//   och registreras med `app.use(pinia)` innan appen monteras. Detta är
//   avgörande för att alla Pinia-stores (inklusive den nya loggerStore)
//   ska vara tillgängliga för komponenterna.

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { createHead } from '@unhead/vue';

import App from '../App.vue';
import router from './router.js';

// Importera globala stilar för att säkerställa att de appliceras först.
import './styles/_tokens.css';
import './styles/_global.css';

// 1. Skapa Vue-applikationens instans.
const app = createApp(App);

// 2. Skapa en Pinia-instans för state management.
const pinia = createPinia();
// Registrera pluginet som hanterar persistent state (sparar i localStorage).
pinia.use(piniaPluginPersistedstate);

// 3. Skapa en instans för att hantera dokumentets <head> (för SEO).
const head = createHead();

// 4. Registrera alla plugins med Vue-appen.
// Ordningen här är viktig. Pinia måste vara tillgängligt för komponenterna.
app.use(pinia);
app.use(router);
app.use(head);

// 5. Montera den färdigkonfigurerade appen till DOM-elementet med id="app".
app.mount('#app');
// src/app/main.js```
