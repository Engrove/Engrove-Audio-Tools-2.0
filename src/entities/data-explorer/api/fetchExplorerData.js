// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * Denna fil ansvarar för all datainhämtning för Data Explorer-modulen.
 * Den exporterar en enda funktion som hämtar alla nödvändiga JSON-filer
 * från den publika /data/-mappen.
 */

/**
 * Hämtar all data som krävs för Data Explorer.
 * Detta inkluderar listor över produkter (pickuper, tonarmar) och deras
 * respektive klassificeringar som används för att bygga filter.
 * Använder Promise.all för att hämta filerna parallellt för bättre prestanda.
 *
 * @returns {Promise<Object>} Ett löfte som resolverar till ett objekt innehållande all data.
 * @throws {Error} Kastar ett fel om någon av nätverksförfrågningarna misslyckas.
 */
export async function fetchExplorerData() {
  // Array med sökvägar till de JSON-filer som ska hämtas.
  // Notera användningen av den nya, standardiserade namnkonventionen.
  const dataUrls = [
    '/data/pickups-data.json',
    '/data/tonearms-data.json',
    '/data/pickups-classifications.json',
    '/data/tonearms-classifications.json',
  ];

  try {
    // Utför alla fetch-anrop parallellt.
    const responses = await Promise.all(dataUrls.map(url => fetch(url)));

    // Kontrollera att alla anrop lyckades. Om inte, kasta ett fel.
    for (const response of responses) {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} for URL: ${response.url}`);
      }
    }

    // Konvertera alla lyckade svar till JSON.
    const jsonData = await Promise.all(responses.map(res => res.json()));

    // Returnera ett strukturerat objekt med den hämtade datan.
    return {
      pickups: jsonData[0],
      tonearms: jsonData[1],
      pickupClassifications: jsonData[2],
      tonearmClassifications: jsonData[3],
    };
  } catch (error) {
    // Logga det ursprungliga felet till konsolen för felsökning.
    console.error("Failed to fetch explorer data:", error);
    // Kasta ett nytt, mer informativt fel som kan fångas upp av anropande kod (t.ex. en Pinia store).
    throw new Error("Could not load the component databases. Please try refreshing the page.");
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
