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

// Skapar en Pinia-instans för global state management.
const pinia = createPinia();
// Registrerar persistens-pluginet för att spara state till localStorage.
pinia.use(piniaPluginPersistedState);

// Skapar Vue-applikationsinstansen med App.vue som rotkomponent.
const app = createApp(App);

// Registrerar Pinia-instansen i appen.
app.use(pinia);
// Registrerar routern i appen.
app.use(router);

// Monterar den färdigkonfigurerade appen på HTML-elementet med id="app".
// Detta element finns i /index.html.
app.mount('#app');
// src/app/main.js
