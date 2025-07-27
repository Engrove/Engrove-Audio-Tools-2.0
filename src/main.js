// src/main.js
// Detta är applikationens huvudsakliga startpunkt.
// Den skapar Vue-appen, importerar globala stilar och monterar applikationen.

import { createApp } from 'vue'
import App from './App.vue'

// Importera de nya globala stilarna och design-tokens.
// Ordningen är viktig: tokens först, sedan de globala stilarna som använder dem.
import './app/styles/_tokens.css'
import './app/styles/_global.css'


createApp(App).mount('#app')
// src/main.js
