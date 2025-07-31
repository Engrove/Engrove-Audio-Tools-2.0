// src/entities/data-explorer/api/fetchExplorerData.js
// Denna modul ansvarar för all datainhämtning för Data Explorer.
// Den hämtar alla nödvändiga JSON-filer parallellt för maximal effektivitet.
//
// FELRÄTTNING (Regression från Steg 11):
// - Sökvägen för tonarmsdata har korrigerats från 'tonearms-data.json' (plural)
//   tillbaka till 'tonearm-data.json' (singular) för att exakt matcha det
//   faktiska filnamnet i /public/data-mappen. Detta löser det underliggande
//   404-felet som orsakade kraschen i explorerStore.

/**
 * Hämtar all nödvändig data för Data Explorer från de statiska JSON-filerna.
 * Använder Promise.all för att köra nätverksanropen parallellt.
 * @returns {Promise<Object>} Ett objekt som innehåller all data.
 */
export async function fetchExplorerData() {
  // Funktion för att förenkla fetch-anrop och JSON-parsning.
  const fetchData = async (url) => {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch ${url}: ${response.statusText}`);
    }
    return response.json();
  };

  // Definierar sökvägarna till alla datafiler.
  const paths = {
    pickupsData: '/data/pickups-data.json',
    pickupsClassifications: '/data/pickups-classifications.json',
    // KORRIGERING: Använder 'tonearm-data.json' (singular)
    tonearmsData: '/data/tonearm-data.json',
    tonearmsClassifications: '/data/tonearms-classifications.json',
  };

  // Utför alla fetch-anrop parallellt.
  const [
    pickupsData,
    pickupsClassifications,
    tonearmsData,
    tonearmsClassifications,
  ] = await Promise.all([
    fetchData(paths.pickupsData),
    fetchData(paths.pickupsClassifications),
    fetchData(paths.tonearmsData),
    fetchData(paths.tonearmsClassifications),
  ]);

  // Returnerar ett samlat objekt med all data.
  return {
    pickupsData,
    pickupsClassifications,
    tonearmsData,
    tonearmsClassifications,
  };
}
// src/entities/data-explorer/api/fetchExplorerData.js
