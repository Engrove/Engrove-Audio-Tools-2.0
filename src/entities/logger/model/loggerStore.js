// src/entities/logger/model/loggerStore.js
// Denna Pinia-store fungerar som en centraliserad loggningsmekanism för hela
// applikationen. Den är designad för att användas under utveckling som ett
// alternativ till webbläsarens konsol, särskilt på enheter där F12-verktyg
// inte är tillgängliga.
//
// Funktioner:
// - Samlar loggmeddelanden från hela appen.
// - Tidsstämplar varje meddelande.
// - Håller automatiskt logghistoriken begränsad till 2000 rader.
// - Kan gruppera loggar i namngivna sessioner med unika ID:n.
// - Är helt inaktiv i produktionsläge för att spara minne och prestanda.
//
// Historik:
// - 2025-08-07: (Frankensteen) Lade till funktionalitet för logg-sessioner (startLogSession, endLogSession).
// - 2025-08-07: (Frankensteen) Ökade MAX_LOG_ENTRIES från 300 till 2000 enligt specifikation.
// - 2025-08-07: (Frankensteen) KRITISK FIX: Aktiverade persistens genom att lägga till `{ persist: true }`.
// - 2025-08-06: (Frankensteen - KRITISK FIX) Tog bort det initiala `addLog`-anropet.

import { ref } from 'vue';
import { defineStore } from 'pinia';

// --- GLOBAL DEBUG FLAGGA ---
export const IS_DEBUG_MODE = true;
const MAX_LOG_ENTRIES = 2000;

export const useLoggerStore = defineStore('logger', () => {
  // --- STATE ---
  const logs = ref([]);
  const activeSession = ref({ id: null, name: null });

  // --- ACTIONS ---

  /**
   * Startar en ny loggningssession. Alla efterföljande loggar kommer att taggas
   * med detta sessions-ID och namn.
   * @param {string} sessionName - Ett beskrivande namn för sessionen.
   */
  function startLogSession(sessionName) {
    if (!IS_DEBUG_MODE) return;
    const sessionId = `session-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
    activeSession.value = { id: sessionId, name: sessionName };
    addLog(`Log session started: "${sessionName}"`, 'Logger', { sessionId, sessionName });
  }

  /**
   * Avslutar den nuvarande loggningssessionen.
   */
  function endLogSession() {
    if (!IS_DEBUG_MODE || !activeSession.value.id) return;
    addLog(`Log session ended: "${activeSession.value.name}"`, 'Logger', { sessionId: activeSession.value.id });
    activeSession.value = { id: null, name: null };
  }

  /**
   * Lägger till ett nytt loggmeddelande i storen och skriver till konsolen.
   * @param {string} message - Det huvudsakliga loggmeddelandet.
   * @param {string} [context='Global'] - Kontexten där loggen skapades.
   * @param {any} [data=null] - Valfri extra data som ska loggas.
   */
  function addLog(message, context = 'Global', data = null) {
    if (!IS_DEBUG_MODE) return;

    const newLogEntry = {
      timestamp: new Date().toISOString(),
      message: message,
      context: context,
      data: data ? JSON.stringify(data, null, 2) : null,
      sessionId: activeSession.value.id,
      sessionName: activeSession.value.name,
    };

    logs.value.unshift(newLogEntry);
    if (logs.value.length > MAX_LOG_ENTRIES) {
      logs.value.pop();
    }

    const groupTitle = `%c[Engrove Inspector | ${context}]%c ${message}`;
    const titleStyle = 'color: #82AAFF; font-weight: bold;';
    const messageStyle = 'color: #E0E0E0;';
    
    console.groupCollapsed(groupTitle, titleStyle, messageStyle);
    console.log(`Timestamp: ${newLogEntry.timestamp}`);
    if (newLogEntry.sessionId) {
      console.log(`Session: ${newLogEntry.sessionName} (${newLogEntry.sessionId})`);
    }
    if (data) {
      console.log('Data:', data);
    }
    console.groupEnd();
  }

  /**
   * Rensar alla meddelanden från loggen.
   */
  function clearLogs() {
    if (!IS_DEBUG_MODE) return;
    logs.value = [];
    addLog('Log cleared.', 'Logger');
  }

  return {
    logs,
    activeSession,
    addLog,
    clearLogs,
    startLogSession,
    endLogSession,
  };
}, {
  persist: true,
});
// src/entities/logger/model/loggerStore.js
