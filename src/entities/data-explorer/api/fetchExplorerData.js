// src/entities/data-explorer/api/fetchExplorerData.js
// Denna fil centraliserar all datainhämtning för Data Explorer-modulen.
// Den exporterar en enda funktion som hämtar all nödvändig data parallellt
// och returnerar den i ett strukturerat format.

/**
 * Hämtar all nödvändig data för Data Explorer (pickups, tonarmar och deras klassifikationer).
 * Använder absoluta sökvägar för att garantera korrekta anrop oavsett SPA-routing.
 * 
 * @returns {Promise<Object>} Ett löfte som resolverar med ett objekt innehållande all data.
 * @throws {Error} Kastar ett fel om någon av nätverksförfrågningarna misslyckas.
 */
export async function fetchAllExplorerData() {
  // Definierar de absoluta sökvägarna till alla nödvändiga JSON-filer.
  // Detta är avgörande för att undvika routing-fel i en SPA.
  const dataUrls = [
    '/data/pickups-data.json',
    '/data/pickups-classifications.json',
    '/data/tonearms-data.json',
    '/data/tonearms-classifications.json'
  ];

  try {
    // Använder Promise.all för att göra alla fetch-anrop parallellt för maximal effektivitet.
    const responses = await Promise.all(
      dataUrls.map(url => fetch(url))
    );

    // Kontrollerar att alla svar från servern är OK (status 200-299).
    // Om något svar inte är ok, kastas ett fel som avbryter hela processen.
    for (const response of responses) {
      if (!response.ok) {
        throw new Error(`Failed to fetch ${response.url}: ${response.statusText}`);
      }
    }

    // När alla svar är verifierade som OK, parsas JSON-datan från varje svar, även detta parallellt.
    const [
      pickups,
      pickupClassifications,
      tonearms,
      tonearmClassifications
    ] = await Promise.all(responses.map(res => res.json()));

    // Returnerar ett välorganiserat objekt med all hämtad data.
    return {
      pickups,
      pickupClassifications,
      tonearms,
      tonearmClassifications
    };

  } catch (error) {
    // Fångar upp eventuella fel som kan uppstå under nätverksanrop eller JSON-parsning.
    console.error("Data Explorer API Error:", error);
    // Kastar felet vidare så att den anropande funktionen (i Pinia store) kan hantera det.
    throw new Error('Could not load the component databases.');
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
