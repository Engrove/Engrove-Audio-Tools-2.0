// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * Denna API-modul är ansvarig för all datainhämtning för Data Explorer-funktionen.
 * Den hämtar alla nödvändiga JSON-filer parallellt för maximal effektivitet.
 *
 * KORRIGERING:
 * 1. Import-sökvägen till loggerStore har korrigerats till den korrekta
 *    relativa sökvägen för att lösa byggfelet "Could not resolve".
 * 2. Nyckeln i returobjektet är `tonearmsClassifications` för att matcha
 *    API-kontraktet som definieras av konsumenten (explorerStore.js).
 */

// KORRIGERING: Korrekt relativ sökväg från /api -> /data-explorer -> /entities -> /logger/model/
import { useLoggerStore } from '@/entities/logger/model/loggerStore.js';

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
    tonearmsData: '/data/tonearm-data.json',
    tonearmsClassifications: '/data/tonearms-classifications.json'
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
    const [pickupsData, pickupClassifications, tonearmsData, tonearmsClassifications] = await Promise.all(dataPromises);

    logger.addLog('All data hämtad och parsrad framgångsrikt.', 'fetchExplorerData', {
      pickups: pickupsData.length,
      tonearms: tonearmsData.length,
      pickupClassificationsKeys: Object.keys(pickupClassifications),
      tonearmsClassificationsKeys: Object.keys(tonearmsClassifications)
    });

    // Returnerar ett objekt med tydligt namngivna nycklar
    return {
      pickupsData: pickupsData || [],
      pickupClassifications: pickupClassifications || {},
      tonearmsData: tonearmsData || [],
      tonearmsClassifications: tonearmsClassifications || {}
    };

  } catch (error) {
    logger.addLog(`Ett fel inträffade i fetchExplorerData: ${error.message}`, 'fetchExplorerData', error);
    // Vid fel, kasta felet vidare så att anropande kod (storen) kan hantera det.
    throw new Error(`Failed to fetch explorer data: ${error.message}`);
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
