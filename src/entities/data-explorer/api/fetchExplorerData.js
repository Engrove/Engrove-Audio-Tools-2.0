// src/entities/data-explorer/api/fetchExplorerData.js
// Denna fil centraliserar all datainhämtning för Data Explorer-modulen.
// UPPDRAG 20: Utökad för att hämta de nya, centraliserade kartorna för filter och översättningar.

/**
 * Hämtar all nödvändig data för Data Explorer parallellt.
 * Använder absoluta sökvägar för att vara robust mot SPA-routingproblem.
 * @returns {Promise<Object>} Ett objekt som innehåller all data.
 */
export async function fetchExplorerData() {
  const urls = [
    '/data/pickups-data.json',
    '/data/pickups-classifications.json',
    '/data/tonearm-data.json',
    '/data/tonearms-classifications.json',
    '/data/data-filters-map.json',       // NY: Hämtar den centrala filterkartan
    '/data/data-translation-map.json'  // NY: Hämtar den centrala översättningskartan
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
      pickupsData,
      pickupsClassifications,
      tonearmsData,
      tonearmsClassifications,
      filtersMap,
      translationMap
    ] = await Promise.all(responses.map(res => res.json()));

    // Kontrakt verifierat. Det nya kontraktet inkluderar nu filtersMap och translationMap.
    return {
      pickupsData,
      pickupsClassifications,
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
