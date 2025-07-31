// src/debug.js
// Detta är JavaScript-motorn för den fristående felsökningssidan debug.html.
// Den skapar en minimal Vue-applikation vars enda syfte är att ansluta till
// loggerStore och rendera de insamlade loggarna.

import { createApp, ref, onMounted } from 'vue';
import { createPinia } from 'pinia';
import { useLoggerStore } from './entities/logger/model/loggerStore.js';

// Skapa en Pinia-instans för denna fristående app.
const pinia = createPinia();

// Definierar Vue-komponenten som ska rendera loggarna.
const DebugApp = {
  setup() {
    // Anslut till loggerStore för att få tillgång till loggarna.
    const loggerStore = useLoggerStore();

    // En funktion för att manuellt uppdatera vyn.
    // Används för att tvinga fram en omrendering om loggar läggs till
    // i en annan flik och LocalStorage uppdateras.
    function refreshLogs() {
        // Detta är en platshållare för framtida logik om vi väljer att
        // synkronisera loggar mellan flikar via LocalStorage.
        // För nu räcker det att den finns.
    }

    // En funktion för att rensa loggarna via storen.
    function handleClearLogs() {
      loggerStore.clearLogs();
    }

    return {
      // Exponerar loggarna och funktionerna till mallen i debug.html
      logs: loggerStore.logs,
      clearLogs: handleClearLogs,
      refreshLogs,
    };
  },
  // Mallen för hur loggarna ska renderas.
  // Denna kommer att renderas inuti `<div id="debug-app">`.
  template: `
    <div class="log-header">
      <h1>Engrove Inspector</h1>
      <div class="log-controls">
        <button @click="clearLogs">Clear Log</button>
      </div>
    </div>
    <ul class="log-list">
      <li v-if="logs.length === 0" class="log-entry">
        <div class="entry-message">No log entries yet. Interact with the main app to generate logs.</div>
      </li>
      <li v-for="(log, index) in logs" :key="log.timestamp + '-' + index" class="log-entry">
        <div class="entry-header">
          <span class="entry-context">{{ log.context }}</span>
          <span class="entry-timestamp">{{ new Date(log.timestamp).toLocaleTimeString('sv-SE', { hour12: false }) }}.{{ new Date(log.timestamp).getMilliseconds().toString().padStart(3, '0') }}</span>
        </div>
        <div class="entry-message">{{ log.message }}</div>
        <div v-if="log.data" class="entry-data">
          <pre>{{ log.data }}</pre>
        </div>
      </li>
    </ul>
  `
};

// Skapa och montera Vue-applikationen.
const app = createApp(DebugApp);
app.use(pinia);
app.mount('#debug-app');
// src/debug.js
