// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * Denna API-modul är ansvarig för all datainhämtning för Data Explorer-funktionen.
 * Den hämtar alla nödvändiga JSON-filer parallellt för maximal effektivitet.
 * 
 * KORRIGERING: Nyckeln i returobjektet har ändrats från `tonearmClassifications` till
 * `tonearmsClassifications` för att exakt matcha API-kontraktet som definieras av
 * konsumenten (explorerStore.js). Detta åtgärdar felet där tonarmsfilter inte laddades.
 */

import { useLoggerStore } from '../model/loggerStore.js';

/**
 * Hämtar all data som krävs för Data Explorer-modulen.
 * Detta inkluderar data och klassificeringar för både pickuper och tonarmar.
 * @returns {Promise<Object>} Ett objekt som innehåller all hämtad data.
 */
export async function fetchExplorerData() {
  const logger = useLoggerStore();
  logger.addLog('fetchExplorerData anropad.', 'fetchExplorerData');

  const urls = {
    pickupsData: '/data/pickups-data.json',
    pickupClassifications: '/data/pickups-classifications.json',
    tonearmsData: '/data/tonearm-data.json', // Korrekt singularform för datafil
    tonearmsClassifications: '/data/tonearms-classifications.json' // Korrekt pluralform för klassificeringsfil
  };

  try {
    // Använder Promise.all för att hämta alla filer parallellt
    const responses = await Promise.all(Object.values(urls).map(url => fetch(url)));

    // Kontrollerar om alla anrop lyckades
    for (const response of responses) {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} for URL: ${response.url}`);
      }
    }

    // Konverterar alla svar till JSON
    const dataPromises = responses.map(res => res.json());
    const [pickupsData, pickupClassifications, tonearmsData, tonearmClassifications] = await Promise.all(dataPromises);

    logger.addLog('All data hämtad och parsrad framgångsrikt.', 'fetchExplorerData', {
      pickups: pickupsData.length,
      tonearms: tonearmsData.length,
      pickupClassificationsKeys: Object.keys(pickupClassifications),
      tonearmsClassificationsKeys: Object.keys(tonearmClassifications)
    });

    // Returnerar ett objekt med tydligt namngivna nycklar
    // KORRIGERING: Nyckeln 'tonearmClassifications' är nu 'tonearmsClassifications'
    return {
      pickupsData: pickupsData || [],
      pickupClassifications: pickupClassifications || {},
      tonearmsData: tonearmsData || [],
      tonearmsClassifications: tonearmClassifications || {}
    };

  } catch (error) {
    logger.addLog(`Ett fel inträffade i fetchExplorerData: ${error.message}`, 'fetchExplorerData', error);
    // Vid fel, kasta felet vidare så att anropande kod (storen) kan hantera det.
    throw new Error(`Failed to fetch explorer data: ${error.message}`);
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
