// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * Denna fil ansvarar för all datainhämtning för Data Explorer.
 * Den hämtar alla nödvändiga JSON-filer parallellt för maximal effektivitet.
 *
 * KORRIGERING (Slutgiltig): Denna version säkerställer att alla URL:er
 * exakt matchar de faktiska filnamnen i /public/data, med särskild
 * uppmärksamhet på singularis vs. pluralis. Returobjektets nycklar
 * är också verifierade mot kontraktet i explorerStore.
 */

export async function fetchExplorerData() {
  try {
    // Exakta filnamn som de finns i repositoryt.
    const urls = [
      '/data/pickups-data.json',            // Plural
      '/data/pickups-classifications.json', // Plural
      '/data/tonearm-data.json',            // <<< SINGULAR
      '/data/tonearms-classifications.json' // Plural
    ];

    const responses = await Promise.all(
      urls.map(url => fetch(url))
    );

    // Kontrollera att alla anrop lyckades
    for (const response of responses) {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} for url: ${response.url}`);
      }
    }

    const data = await Promise.all(
      responses.map(response => response.json())
    );

    // Returnera ett objekt med nycklar som exakt matchar vad explorerStore förväntar sig.
    return {
      pickups: data[0],
      pickupClassifications: data[1],
      tonearms: data[2],
      tonearmsClassifications: data[3],
    };

  } catch (error) {
    console.error("Error fetching explorer data:", error);
    // Kasta om felet så att anropande kod (store) kan hantera det.
    throw error;
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
