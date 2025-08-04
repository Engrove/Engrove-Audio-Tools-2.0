// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * Historik:
 * - 2024-08-04: (UPPDRAG 20) Utökad för att hämta de nya, centraliserade kartorna för filter och översättningar.
 * - 2024-08-04: (UPPDRAG 22) Refaktorerad för att hämta 'cartridges' istället för 'pickups' enligt nytt datakontrakt.
 */

/**
 * Viktiga implementerade regler:
 * - Fullständig kod, alltid: Filen är komplett.
 * - API-kontraktsverifiering: Returvärdet matchar det nya, förväntade kontraktet med `cartridgesData` och `cartridgesClassifications`.
 * - Alter Ego-granskning: Genomförd för att säkerställa robusthet och korrekthet.
 */

/**
 * Hämtar all nödvändig data för Data Explorer parallellt.
 * Använder absoluta sökvägar för att vara robust mot SPA-routingproblem.
 * @returns {Promise<Object>} Ett objekt som innehåller all data.
 */
export async function fetchExplorerData() {
  const urls = [
    '/data/cartridges-data.json',           // ÄNDRAD: Peka på den nya cartridge-datan
    '/data/cartridges-classifications.json',// ÄNDRAD: Peka på de nya cartridge-klassificeringarna
    '/data/tonearm-data.json',
    '/data/tonearms-classifications.json',
    '/data/data-filters-map.json',
    '/data/data-translation-map.json'
  ];

  try {
    const responses = await Promise.all(urls.map(url => fetch(url)));

    // Kontrollera om alla svar är OK
    for (const response of responses) {
      if (!response.ok) {
        throw new Error(`Failed to fetch ${response.url}: ${response.statusText}`);
      }
    }

    const [
      cartridgesData,         // ÄNDRAD: Namnbyte för konsekvens
      cartridgesClassifications, // ÄNDRAD: Namnbyte för konsekvens
      tonearmsData,
      tonearmsClassifications,
      filtersMap,
      translationMap
    ] = await Promise.all(responses.map(res => res.json()));

    // Kontrakt verifierat. Det nya kontraktet inkluderar nu filtersMap och translationMap
    // och använder 'cartridges' terminologi.
    return {
      cartridgesData,
      cartridgesClassifications,
      tonearmsData,
      tonearmsClassifications,
      filtersMap,
      translationMap
    };

  } catch (error) {
    console.error('Error fetching explorer data:', error);
    // Kasta om felet så att det kan fångas upp av anropande kod (t.ex. i Pinia store)
    throw error;
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
