// src/app/main.js
// Detta är applikationens centrala startpunkt.
// Den skapar Vue-instansen och installerar alla globala plugins
// som Pinia för state management och Vue Router för navigering.

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedState from 'pinia-plugin-persistedstate';

import App from '../App.vue';
import router from './router'; // Importerar vår nyskapade router

// Importerar globala CSS-filer för att säkerställa att de appliceras överallt.
import './styles/_tokens.css';
import './styles/_global.css';

// Skapar en Vue-app-instans baserad på rotkomponenten App.vue.
const app = createApp(App);

// Skapar en Pinia-instans för state management.
const pinia = createPinia();
// Lägger till pluginet för att spara state i localStorage.
pinia.use(piniaPluginPersistedState);

// Använder Pinia-instansen i vår Vue-app.
app.use(pinia);
// Använder den importerade routern i vår Vue-app.
app.use(router);

// Monterar den färdigkonfigurerade appen till DOM-elementet med id="app".
app.mount('#app');
// src/app/main.js
