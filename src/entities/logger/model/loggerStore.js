// src/entities/logger/model/loggerStore.js
// Denna Pinia-store fungerar som en centraliserad loggningsmekanism för hela
// applikationen. Den är designad för att användas under utveckling som ett
// alternativ till webbläsarens konsol, särskilt på enheter där F12-verktyg
// inte är tillgängliga.
//
// Funktioner:
// - Samlar loggmeddelanden från hela appen.
// - Tidsstämplar varje meddelande.
// - Håller automatiskt logghistoriken begränsad till 300 rader.
// - Är helt inaktiv i produktionsläge för att spara minne och prestanda.
// - Skriver ut formaterade meddelanden till webbläsarens konsol i debug-läge.
//
// ÄNDRING:
// - Läser nu den explicita miljövariabeln `VITE_FORCE_DEBUG` som sätts i
//   Cloudflare Pages bygginställningar. Detta är den mest robusta metoden
//   för att styra felsökningsläget i produktionsmiljön.

import { ref } from 'vue';
import { defineStore } from 'pinia';

// --- GLOBAL DEBUG FLAGGA ---
// Denna konstant styr all loggningsfunktionalitet.
// `import.meta.env.VITE_FORCE_DEBUG` läses från miljövariabeln som sätts
// i Cloudflare (eller en lokal .env-fil).
// Jämförelsen med strängen 'true' är viktig eftersom miljövariabler
// alltid är strängar.
export const IS_DEBUG_MODE = import.meta.env.VITE_FORCE_DEBUG === 'true';

// Definierar den maximala storleken på logg-bufferten.
const MAX_LOG_ENTRIES = 300;

export const useLoggerStore = defineStore('logger', () => {
  // --- STATE ---
  const logs = ref([]);

  // --- ACTIONS ---

  /**
   * Lägger till ett nytt loggmeddelande i storen och skriver till konsolen.
   * Funktionen gör ingenting om IS_DEBUG_MODE är false.
   * @param {string} message - Det huvudsakliga loggmeddelandet.
   * @param {string} [context='Global'] - Kontexten där loggen skapades.
   * @param {any} [data=null] - Valfri extra data som ska loggas.
   */
  function addLog(message, context = 'Global', data = null) {
    if (!IS_DEBUG_MODE) {
      return;
    }

    // 1. Skapa det interna loggobjektet för debug.html
    const newLogEntry = {
      timestamp: new Date().toISOString(),
      message: message,
      context: context,
      data: data ? JSON.stringify(data, null, 2) : null,
    };

    logs.value.unshift(newLogEntry);
    if (logs.value.length > MAX_LOG_ENTRIES) {
      logs.value.pop();
    }

    // 2. Skriv ut till webbläsarens F12-konsol
    const groupTitle = `%c[Engrove Inspector | ${context}]%c ${message}`;
    const titleStyle = 'color: #82AAFF; font-weight: bold;';
    const messageStyle = 'color: #E0E0E0;';

    // Använder en hopfälld grupp för att hålla konsolen ren.
    console.groupCollapsed(groupTitle, titleStyle, messageStyle);
    console.log(`Timestamp: ${newLogEntry.timestamp}`);
    
    // Om det finns extra data, logga det som ett interaktivt objekt.
    if (data) {
      console.log('Data:', data);
    }
    
    console.groupEnd();
  }

  /**
   * Rensar alla meddelanden från loggen.
   */
  function clearLogs() {
    if (!IS_DEBUG_MODE) {
      return;
    }
    logs.value = [];
    addLog('Log cleared.', 'Logger');
  }

  // Initialiserar loggen med ett startmeddelande (endast i debug-läge).
  addLog('Logger initialized.', 'System');

  return {
    logs,
    addLog,
    clearLogs,
  };
});
// src/entities/logger/model/loggerStore.js
