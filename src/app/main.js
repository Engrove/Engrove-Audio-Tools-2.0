// /src/app/main.js
// Detta är applikationens huvudsakliga startpunkt.
// Koden här importerar 'createApp' från Vue och vår rotkomponent 'App.vue'.
// Därefter skapar den en ny Vue-applikation med App.vue som grund
// och monterar den på DOM-elementet med id="app" i vår index.html.

import { createApp } from 'vue'
// KORRIGERING: Sökvägen har ändrats från '../../App.vue' till '../App.vue'
// för att korrekt peka från /src/app/ till /src/.
import App from '../App.vue'

createApp(App).mount('#app')
// /src/app/main.js
