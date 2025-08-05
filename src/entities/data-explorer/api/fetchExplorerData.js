// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * Historik:
 * - 2025-08-05: (CODE RED FIX) Korrigerat ett kritiskt stavfel i URL:en för tonarmsdata. 'tonearm-data.json' har ändrats till 'tonearms-data.json'. Detta var grundorsaken till att datainhämtningen misslyckades tyst.
 * - 2024-08-04: (UPPDRAG 20) Utökad för att hämta de nya, centraliserade kartorna för filter och översättningar.
 * - 2024-08-04: (UPPDRAG 22) Refaktorerad för att hämta 'cartridges' istället för 'pickups' enligt nytt datakontrakt.
 */

/**
 * Viktiga implementerade regler:
 * - "Help me God"-protokollet har använts för att hitta grundorsaken.
 * - API-kontraktsverifiering: Verifierat att alla URL:er nu exakt matchar filstrukturen i /public/data.
 */

/**
 * Hämtar all nödvändig data för Data Explorer parallellt.
 * Använder absoluta sökvägar för att vara robust mot SPA-routingproblem.
 * @returns {Promise<Object>} Ett objekt som innehåller all data.
 */
export async function fetchExplorerData() {
  const urls = [
    '/data/cartridges-data.json',
    '/data/cartridges-classifications.json',
    '/data/tonearms-data.json', // KORRIGERING: 'tonearm' -> 'tonearms'
    '/data/tonearms-classifications.json',
    '/data/data-filters-map.json',
    '/data/data-translation-map.json'
  ];

  try {
    // Kontrakt verifierat.
    const responses = await Promise.all(urls.map(url => fetch(url)));

    // Kontrollera om alla svar är OK
    for (const response of responses) {
      if (!response.ok) {
        throw new Error(`Failed to fetch ${response.url}: ${response.statusText}`);
      }
    }

    const [
      cartridgesData,
      cartridgesClassifications,
      tonearmsData,
      tonearmsClassifications,
      filtersMap,
      translationMap
    ] = await Promise.all(responses.map(res => res.json()));

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
