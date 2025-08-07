// src/debug.js
// Detta är JavaScript-motorn för den fristående felsökningssidan debug.html.
// Den skapar en minimal Vue-applikation vars enda syfte är att ansluta till
// loggerStore och rendera de insamlade loggarna.
//
// HISTORIK:
// - 2025-08-07: (Frankensteen) Fas 2 Upgrade: Lade till komplett funktionalitet för att
//   välja, avmarkera, kopiera och ladda ner specifika logg-rader som JSON.
// - 2025-08-07: (Frankensteen) KRITISK FIX: Lade till och applicerade `pinia-plugin-persistedstate`.
//   Utan detta plugin kunde Pinia-instansen i denna app inte läsa det state
//   som huvudapplikationen hade sparat till localStorage. Detta var grundorsaken
//   till att logg-visaren var tom trots att data fanns.

import { createApp, ref, computed } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { useLoggerStore } from './entities/logger/model/loggerStore.js';

// Skapa en Pinia-instans för denna fristående app.
const pinia = createPinia();

// KRITISK FIX: Registrera persistens-pluginet.
pinia.use(piniaPluginPersistedstate);

// Definierar Vue-komponenten som ska rendera loggarna.
const DebugApp = {
  setup() {
    const loggerStore = useLoggerStore();
    
    // --- State för urval ---
    const selectedLogs = ref([]);
    
    // --- Computed Properties ---
    const isAnythingSelected = computed(() => selectedLogs.value.length > 0);

    // --- Funktioner ---
    function handleClearLogs() {
      loggerStore.clearLogs();
      selectedLogs.value = []; // Rensa även urvalet
    }
    
    function selectAll() {
        selectedLogs.value = loggerStore.logs.map(log => log.timestamp);
    }

    function unselectAll() {
        selectedLogs.value = [];
    }

    function getSelectedLogObjects() {
        return loggerStore.logs.filter(log => selectedLogs.value.includes(log.timestamp));
    }

    function copySelectedJSON() {
        if (!isAnythingSelected.value) return;
        const selectedData = getSelectedLogObjects();
        const jsonString = JSON.stringify(selectedData, null, 2);
        navigator.clipboard.writeText(jsonString).then(() => {
            alert(`${selectedLogs.value.length} log entries copied to clipboard.`);
        }).catch(err => {
            console.error('Failed to copy logs:', err);
            alert('Failed to copy logs to clipboard.');
        });
    }

    function downloadSelectedJSON() {
        if (!isAnythingSelected.value) return;
        const selectedData = getSelectedLogObjects();
        const jsonString = JSON.stringify(selectedData, null, 2);
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `engrove_inspector_log_${new Date().toISOString()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }


    return {
      logs: loggerStore.logs,
      clearLogs: handleClearLogs,
      selectedLogs,
      isAnythingSelected,
      selectAll,
      unselectAll,
      copySelectedJSON,
      downloadSelectedJSON,
    };
  },
  // Mallen för hur loggarna ska renderas.
  template: `
    <div class="log-header">
      <h1>Engrove Inspector</h1>
      <div class="log-controls">
        <button @click="clearLogs">Clear Log</button>
        <button @click="selectAll">Select All</button>
        <button @click="unselectAll" :disabled="!isAnythingSelected">Unselect All</button>
        <button @click="copySelectedJSON" :disabled="!isAnythingSelected">Copy Selected JSON</button>
        <button @click="downloadSelectedJSON" :disabled="!isAnythingSelected">Download Selected JSON</button>
      </div>
    </div>
    <ul class="log-list">
      <li v-if="logs.length === 0" class="log-entry">
        <div class="entry-message">No log entries yet. Interact with the main app to generate logs.</div>
      </li>
      <li v-for="(log, index) in logs" :key="log.timestamp + '-' + index" class="log-entry">
        <div class="entry-header">
          <label class="entry-selection">
            <input type="checkbox" :value="log.timestamp" v-model="selectedLogs" />
          </label>
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
