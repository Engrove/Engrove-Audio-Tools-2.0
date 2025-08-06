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
// Historik:
// - 2025-08-06: (Frankensteen - KRITISK FIX) Tog bort det initiala `addLog`-anropet
//   från modulens rot för att lösa en race condition-krasch vid app-start.
// - 2025-08-06: (Frankensteen - Felsökning)
//   Miljövariabler via Vite/Cloudflare fungerar inte tillförlitligt.
//   Flaggan är nu hårdkodad för att garantera att felsökningsläget är aktivt.

import { ref } from 'vue';
import { defineStore } from 'pinia';

// --- GLOBAL DEBUG FLAGGA ---
//
// ==========================================================================
// === VIKTIGT FÖR RELEASE ==================================================
// ==========================================================================
//
// Denna flagga är hårdkodad till `true` för att möjliggöra felsökning.
// Innan en slutgiltig produktionsrelease måste detta värde
// manuellt ändras till `false`.
//
export const IS_DEBUG_MODE = true;
//
// ==========================================================================

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

  return {
    logs,
    addLog,
    clearLogs,
  };
});
// src/entities/logger/model/loggerStore.js
