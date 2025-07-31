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

import { ref } from 'vue';
import { defineStore } from 'pinia';

// Definierar den maximala storleken på logg-bufferten.
const MAX_LOG_ENTRIES = 300;

export const useLoggerStore = defineStore('logger', () => {
  // --- STATE ---
  // En reaktiv array som kommer att innehålla alla våra loggobjekt.
  const logs = ref([]);

  // --- ACTIONS ---

  /**
   * Lägger till ett nytt loggmeddelande i storen.
   * Om loggen överskrider MAX_LOG_ENTRIES, tas det äldsta meddelandet bort.
   * @param {string} message - Det huvudsakliga loggmeddelandet.
   * @param {string} [context='Global'] - Kontexten där loggen skapades (t.ex. 'explorerStore', 'DataFilterPanel').
   * @param {any} [data=null] - Valfri extra data (t.ex. ett objekt) som ska loggas. Konverteras till en JSON-sträng.
   */
  function addLog(message, context = 'Global', data = null) {
    // Skapa ett tidsstämplat loggobjekt.
    const newLogEntry = {
      timestamp: new Date().toISOString(),
      message: message,
      context: context,
      // Om data finns, formatera det som en läsbar JSON-sträng.
      data: data ? JSON.stringify(data, null, 2) : null,
    };

    // Lägg till det nya meddelandet i början av arrayen.
    logs.value.unshift(newLogEntry);

    // Om arrayen blir för stor, ta bort det sista (äldsta) elementet.
    if (logs.value.length > MAX_LOG_ENTRIES) {
      logs.value.pop();
    }
  }

  /**
   * Rensar alla meddelanden från loggen.
   */
  function clearLogs() {
    logs.value = [];
    addLog('Log cleared.', 'Logger');
  }

  // Initialiserar loggen med ett startmeddelande.
  addLog('Logger initialized.', 'System');

  // Exponerar state och actions för användning i andra delar av appen.
  return {
    logs,
    addLog,
    clearLogs,
  };
});
// src/entities/logger/model/loggerStore.js
