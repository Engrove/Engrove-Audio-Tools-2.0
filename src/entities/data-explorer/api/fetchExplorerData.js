// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * Denna fil är en dedikerad API-modul för Data Explorer-entiteten.
 * Dess enda ansvar är att hämta all nödvändig data från de statiska JSON-filerna.
 * Genom att centralisera datainhämtningen här säkerställer vi att korrekta,
 * absoluta sökvägar används och att felhanteringen är robust och konsekvent.
 */

/**
 * Hämtar all nödvändig data för Data Explorer-modulen parallellt.
 * Använder absoluta sökvägar för att undvika SPA-routing-problem.
 * @returns {Promise<Object>} Ett promise som resolverar till ett objekt innehållande all data.
 * @throws {Error} Kastar ett fel om någon av nätverksbegärandena misslyckas.
 */
export async function fetchExplorerData() {
  try {
    // Använder Promise.all för att starta alla fetch-anrop samtidigt för maximal prestanda.
    const responses = await Promise.all([
      fetch('/data/pickups-data.json'),
      fetch('/data/pickups-classifications.json'),
      fetch('/data/tonearms-data.json'),
      fetch('/data/tonearms-classifications.json')
    ]);

    // Kontrollerar varje svar individuellt för att säkerställa att de lyckades (status 200-299).
    for (const response of responses) {
      if (!response.ok) {
        // Om ett svar misslyckades, kasta ett specifikt fel.
        throw new Error(`Failed to fetch data from ${response.url}: ${response.status} ${response.statusText}`);
      }
    }

    // Om alla svar är ok, konvertera dem från JSON till JavaScript-objekt, också parallellt.
    const [
      pickupsData,
      pickupClassifications,
      tonearmsData,
      tonearmClassifications
    ] = await Promise.all(responses.map(res => res.json()));

    // Returnera ett prydligt strukturerat objekt med all data.
    return {
      pickupsData,
      pickupClassifications,
      tonearmsData,
      tonearmClassifications
    };

  } catch (error) {
    // Logga det specifika felet till konsolen för felsökning.
    console.error('Data Explorer API Error:', error);
    // Kasta om felet så att den anropande funktionen (i Pinia-storen) kan fånga det
    // och uppdatera applikationens error-state.
    throw error;
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
