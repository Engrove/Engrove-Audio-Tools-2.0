// src/app/main.js
// Detta är applikationens huvud-startpunkt (entry point).
// Den skapar Vue-appen, importerar globala stilar och plugins,
// och monterar appen på DOM-trädet.

import { createApp } from 'vue';

// Importerar rotkomponenten App.vue
import App from '../App.vue';

// Importerar de globala stilarna. Vite kommer att hantera dessa.
import './styles/_tokens.css';
import './styles/_global.css';

// Importerar den nyligen skapade routern.
import router from './router.js';


// Skapar Vue-applikationsinstansen med App.vue som rotkomponent.
const app = createApp(App);

// Talar om för Vue-appen att den ska använda vår router-konfiguration.
// Detta är steget som aktiverar all navigering.
app.use(router);

// Monterar den färdigkonfigurerade appen på HTML-elementet med id="app".
// Detta element finns i /index.html.
app.mount('#app');
// src/app/main.js
