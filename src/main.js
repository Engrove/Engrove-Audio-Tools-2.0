// src/app/main.js
// === DIAGNOSTISK VERSION ===
// Denna fil har instrumenterats med console.log för att spåra initialiseringsprocessen
// och identifiera den exakta punkten där kraschen inträffar.
console.log('[DEBUG] main.js: Initial imports.');

import { createApp } from 'vue';
console.log('[DEBUG] main.js: Imported vue');

import { createPinia } from 'pinia';
console.log('[DEBUG] main.js: Imported pinia');

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
console.log('[DEBUG] main.js: Imported pinia-plugin-persistedstat');

import { createHead } from '@unhead/vue';
console.log('[DEBUG] main.js: Imported @unhead/vue');

import App from '../App.vue';
console.log('[DEBUG] main.js: Imported ../App.vue');

import router from './router.js';
console.log('[DEBUG] main.js: Imported ./router.js');

import './styles/_tokens.css';
console.log('[DEBUG] main.js: Imported ./styles/_tokens.css');

import './styles/_global.css';
console.log('[DEBUG] main.js: Imported ./styles/_global.css');

console.log('[DEBUG] main.js: Start of script execution.');

// 1. Skapa Vue-applikationens instans.
const app = createApp(App);
console.log('[DEBUG] main.js: 1. createApp(App) - SUCCESS.');

// 2. Skapa en Pinia-instans för state management.
const pinia = createPinia();
console.log('[DEBUG] main.js: 2. createPinia() - SUCCESS.');

// Registrera pluginet som hanterar persistent state (sparar i localStorage).
try {
  pinia.use(piniaPluginPersistedstate);
  console.log('[DEBUG] main.js: 2a. pinia.use(piniaPluginPersistedstate) - SUCCESS.');
} catch (e) {
  console.error('[DEBUG] main.js: 2a. pinia.use(piniaPluginPersistedstate) - FAILED.', e);
  throw e; // Kasta om felet för att se hela stacktracen
}


// 3. Skapa en instans för att hantera dokumentets <head> (för SEO).
const head = createHead();
console.log('[DEBUG] main.js: 3. createHead() - SUCCESS.');

// 4. Registrera alla plugins med Vue-appen.
try {
  console.log('[DEBUG] main.js: 4a. Attempting app.use(pinia)...');
  app.use(pinia);
  console.log('[DEBUG] main.js: 4a. app.use(pinia) - SUCCESS.');

  console.log('[DEBUG] main.js: 4b. Attempting app.use(router)...');
  app.use(router);
  console.log('[DEBUG] main.js: 4b. app.use(router) - SUCCESS.');

  console.log('[DEBUG] main.js: 4c. Attempting app.use(head)...');
  app.use(head);
  console.log('[DEBUG] main.js: 4c. app.use(head) - SUCCESS.');
} catch (e) {
    console.error('[DEBUG] main.js: 4. app.use() block - FAILED.', e);
    throw e;
}


// 5. Montera den färdigkonfigurerade appen till DOM-elementet med id="app".
try {
  console.log('[DEBUG] main.js: 5. Attempting app.mount(\'#app\')...');
  app.mount('#app');
  console.log('[DEBUG] main.js: 5. app.mount(\'#app\') - SUCCESS.');
} catch (e) {
    console.error('[DEBUG] main.js: 5. app.mount() - FAILED.', e);
    throw e;
}

console.log('[DEBUG] main.js: End of script execution.');
