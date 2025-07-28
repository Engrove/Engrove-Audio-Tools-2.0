// src/app/main.js
// Detta är applikationens huvud-startpunkt (entry point).
// Den skapar Vue-appen, importerar globala stilar och plugins,
// och monterar appen på DOM-trädet.

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedState from 'pinia-plugin-persistedstate';

// Importerar rotkomponenten App.vue
import App from '../App.vue';

// Importerar de globala stilarna. Vite kommer att hantera dessa.
import './styles/_tokens.css';
import './styles/_global.css';

// Importerar routern.
import router from './router.js';

// 1. Skapa Vue-applikationsinstansen.
const app = createApp(App);

// 2. Skapa en Pinia-instans.
const pinia = createPinia();

// 3. Registrera persistens-pluginet på Pinia-instansen.
// Detta måste göras innan Pinia registreras i Vue-appen.
pinia.use(piniaPluginPersistedState);

// 4. Registrera den färdigkonfigurerade Pinia-instansen i appen.
app.use(pinia);

// 5. Registrera routern i appen.
app.use(router);

// 6. Monterar den fullt konfigurerade appen på HTML-elementet med id="app".
// Detta element finns i /index.html.
app.mount('#app');
// src/app/main.js
