// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * @file fetchExplorerData.js
 * @description Denna API-funktion ansvarar för att hämta all nödvändig data
 * för Data Explorer-modulen från de statiska JSON-filerna.
 * Denna korrigerade version använder absoluta sökvägar för att säkerställa
 * att filerna hittas oavsett vilken sida användaren befinner sig på.
 */

// KORRIGERING: Sökvägarna måste vara absoluta från webbplatsens rot.
// De pekar nu korrekt till /public/data/-mappen som serveras.
const PICKUPS_URL = '/data/pickups-data.json';
const TONEARMS_URL = '/data/tonearms-data.json';
const PICKUP_CLASSIFICATIONS_URL = '/data/pickups-classifications.json';
const TONEARM_CLASSIFICATIONS_URL = '/data/tonearms-classifications.json';

/**
 * Hämtar och parsar en enskild JSON-fil.
 * @param {string} url - Sökvägen till JSON-filen.
 * @returns {Promise<Object>} - Ett löfte som resolverar med den parsade JSON-datan.
 * @throws {Error} - Kastar ett fel om nätverksanropet eller parsningen misslyckas.
 */
const fetchJSON = async (url) => {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Network response was not ok for ${url}`);
  }
  return response.json();
};

/**
 * Asynkron funktion som hämtar alla databaser och klassificeringar som
 * Data Explorer är beroende av. Använder Promise.all för att köra
 * anropen parallellt för maximal effektivitet.
 *
 * @returns {Promise<Object>} Ett objekt som innehåller all hämtad data.
 * @throws {Error} Kastar ett fel om något av de individuella anropen misslyckas.
 */
export async function fetchExplorerData() {
  try {
    const [
      pickupsData,
      tonearmsData,
      pickupClassifications,
      tonearmClassifications,
    ] = await Promise.all([
      fetchJSON(PICKUPS_URL),
      fetchJSON(TONEARMS_URL),
      fetchJSON(PICKUP_CLASSIFICATIONS_URL),
      fetchJSON(TONEARM_CLASSIFICATIONS_URL),
    ]);

    // Returnerar ett prydligt objekt med all data
    return {
      pickupsData,
      tonearmsData,
      pickupClassifications,
      tonearmClassifications,
    };
  } catch (error) {
    console.error('Failed to fetch explorer data:', error);
    // Skickar felet vidare så att anropande kod (Pinia store) kan hantera det.
    throw new Error('Could not load the component databases.');
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
