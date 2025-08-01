// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * Denna API-modul är ansvarig för all datainhämtning för Data Explorer-funktionen.
 * Den hämtar alla nödvändiga JSON-filer parallellt för maximal effektivitet.
 *
 * KORRIGERING:
 * 1. Löst ett kritiskt `ReferenceError`. Variabeln som håller tonarmsklassificeringar
 *    heter `tonearmClassifications` (singular), men användes felaktigt som
 *    `tonearmsClassifications` (plural) i returobjektet. Detta är nu korrigerat.
 *    Nyckeln i returobjektet är `tonearmsClassifications` (plural) för att matcha
 *    API-kontraktet, och värdet är den korrekta variabeln.
 * 2. Använder absolut sökväg för import av loggerStore för att lösa byggfel.
 */

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
    const responses = await Promise.all(Object.values(urls).map(url => fetch(url)));

    for (const response of responses) {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} for URL: ${response.url}`);
      }
    }

    const dataPromises = responses.map(res => res.json());
    // Destruktureringen skapar en lokal variabel 'tonearmClassifications' (singular)
    const [pickupsData, pickupClassifications, tonearmsData, tonearmClassifications] = await Promise.all(dataPromises);

    logger.addLog('All data hämtad och parsrad framgångsrikt.', 'fetchExplorerData', {
      pickups: pickupsData.length,
      tonearms: tonearmsData.length,
      pickupClassificationsKeys: Object.keys(pickupClassifications),
      tonearmsClassificationsKeys: Object.keys(tonearmClassifications)
    });

    // KORRIGERING: Nyckeln (plural) måste matcha värdet från den existerande variabeln (singular).
    return {
      pickupsData: pickupsData || [],
      pickupClassifications: pickupClassifications || {},
      tonearmsData: tonearmsData || [],
      tonearmsClassifications: tonearmClassifications || {}
    };

  } catch (error) {
    logger.addLog(`Ett fel inträffade i fetchExplorerData: ${error.message}`, 'fetchExplorerData', error);
    throw new Error(`Failed to fetch explorer data: ${error.message}`);
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
