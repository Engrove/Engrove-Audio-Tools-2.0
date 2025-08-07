// src/debug.js
// Detta är JavaScript-motorn för den fristående felsökningssidan debug.html.
// Den skapar en minimal Vue-applikation vars enda syfte är att ansluta till
// loggerStore och rendera de insamlade loggarna.
//
// HISTORIK:
// - 2025-08-07: (Frankensteen) Fas 4 Upgrade: Lade till "Select from here" och
//   klickbara session-ID:n för avancerat urval.
// - 2025-08-07: (Frankensteen) Fas 3 Upgrade: Lade till datum-gruppering,
//   kollapserbara sektioner och datumfiltrering.
// - 2025-08-07: (Frankensteen) Fas 2 Upgrade: Lade till funktionalitet för att
//   välja, kopiera och ladda ner specifika logg-rader.
// - 2025-08-07: (Frankensteen) KRITISK FIX: Lade till `pinia-plugin-persistedstate`.

import { createApp, ref, computed } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { useLoggerStore } from './entities/logger/model/loggerStore.js';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const DebugApp = {
  setup() {
    const loggerStore = useLoggerStore();
    
    const selectedLogs = ref([]);
    const selectedDate = ref('');

    const isAnythingSelected = computed(() => selectedLogs.value.length > 0);

    const groupedLogs = computed(() => {
      const filtered = selectedDate.value
        ? loggerStore.logs.filter(log => log.timestamp.startsWith(selectedDate.value))
        : loggerStore.logs;

      const groups = filtered.reduce((acc, log) => {
        const date = log.timestamp.split('T')[0];
        if (!acc[date]) {
          acc[date] = [];
        }
        acc[date].push(log);
        return acc;
      }, {});

      return Object.keys(groups)
        .sort((a, b) => b.localeCompare(a))
        .map(date => ({
          date,
          logs: groups[date]
        }));
    });

    function handleClearLogs() {
      loggerStore.clearLogs();
      selectedLogs.value = [];
    }
    
    function selectAll() {
        selectedLogs.value = loggerStore.logs.map(log => log.timestamp);
    }

    function unselectAll() {
        selectedLogs.value = [];
    }

    function selectFrom(timestamp) {
        const flatLogs = groupedLogs.value.flatMap(g => g.logs);
        const startIndex = flatLogs.findIndex(log => log.timestamp === timestamp);
        if (startIndex === -1) return;

        const logsToSelect = flatLogs.slice(0, startIndex + 1).map(log => log.timestamp);
        const currentSelection = new Set(selectedLogs.value);
        logsToSelect.forEach(ts => currentSelection.add(ts));
        selectedLogs.value = Array.from(currentSelection);
    }
    
    function selectBySessionId(sessionId) {
        if (!sessionId) return;
        const logsInSession = loggerStore.logs
            .filter(log => log.sessionId === sessionId)
            .map(log => log.timestamp);
        
        const currentSelection = new Set(selectedLogs.value);
        logsInSession.forEach(ts => currentSelection.add(ts));
        selectedLogs.value = Array.from(currentSelection);
    }

    function getSelectedLogObjects() {
      return loggerStore.logs.filter(log => selectedLogs.value.includes(log.timestamp));
    }

    function copySelectedJSON() {
      if (!isAnythingSelected.value) return;
      const jsonString = JSON.stringify(getSelectedLogObjects(), null, 2);
      navigator.clipboard.writeText(jsonString).then(() => alert(`${selectedLogs.value.length} log entries copied.`));
    }

    function downloadSelectedJSON() {
      if (!isAnythingSelected.value) return;
      const jsonString = JSON.stringify(getSelectedLogObjects(), null, 2);
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
      selectedDate,
      groupedLogs,
      selectFrom,
      selectBySessionId,
    };
  },
  template: `
    <div class="log-header">
      <h1>Engrove Inspector</h1>
      <div class="log-controls">
        <button @click="clearLogs">Clear Log</button>
        <button @click="selectAll">Select All</button>
        <button @click="unselectAll" :disabled="!isAnythingSelected">Unselect All</button>
        <button @click="copySelectedJSON" :disabled="!isAnythingSelected">Copy Selected JSON</button>
        <button @click="downloadSelectedJSON" :disabled="!isAnythingSelected">Download Selected JSON</button>
        <input type="date" v-model="selectedDate" style="margin-left: 10px;" />
      </div>
    </div>
    <div v-if="logs.length === 0" class="log-list">
        <div class="log-entry">
            <div class="entry-message">No log entries yet. Interact with the main app to generate logs.</div>
        </div>
    </div>
    <div v-for="group in groupedLogs" :key="group.date" class="date-group">
        <details open>
            <summary class="date-header">{{ group.date }} ({{ group.logs.length }} entries)</summary>
            <ul class="log-list">
                <li v-for="(log, index) in group.logs" :key="log.timestamp + '-' + index" class="log-entry">
                    <div class="entry-header">
                        <label class="entry-selection">
                            <input type="checkbox" :value="log.timestamp" v-model="selectedLogs" />
                        </label>
                        <button class="select-from-btn" @click="selectFrom(log.timestamp)" title="Select this and all newer entries">▼</button>
                        <span class="entry-context">
                            {{ log.context }}
                            <a href="#" v-if="log.sessionId" @click.prevent="selectBySessionId(log.sessionId)" class="session-link" :title="'Select all logs in session: ' + log.sessionName">
                                 #{{ log.sessionName }}
                            </a>
                        </span>
                        <span class="entry-timestamp">{{ new Date(log.timestamp).toLocaleTimeString('sv-SE', { hour12: false }) }}.{{ new Date(log.timestamp).getMilliseconds().toString().padStart(3, '0') }}</span>
                    </div>
                    <div class="entry-message">{{ log.message }}</div>
                    <div v-if="log.data" class="entry-data">
                    <pre>{{ log.data }}</pre>
                    </div>
                </li>
            </ul>
        </details>
    </div>
  `
};

const app = createApp(DebugApp);
app.use(pinia);
app.mount('#debug-app');
// src/debug.js
