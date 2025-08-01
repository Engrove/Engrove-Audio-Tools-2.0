// src/entities/data-explorer/api/fetchExplorerData.js
/**
 * Denna fil ansvarar för all datainhämtning för Data Explorer.
 * Den hämtar alla nödvändiga JSON-filer parallellt för maximal effektivitet.
 *
 * KORRIGERING: Denna version säkerställer att alla URL:er exakt matchar
 * filnamnen i /public/data och att nycklarna i det returnerade objektet
 * är konsekvent pluraliserade för att matcha hur explorerStore förväntar sig dem.
 */

export async function fetchExplorerData() {
  try {
    // Standardisera alla filnamn till plural där det är logiskt.
    // Detta måste exakt matcha filsystemet.
    const urls = [
      '/data/pickups-data.json',           // plural
      '/data/pickups-classifications.json',// plural
      '/data/tonearm-data.json',           // singular (som i filsystemet)
      '/data/tonearms-classifications.json' // plural
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

    // Returnera ett objekt med konsekventa, pluraliserade nycklar
    // som explorerStore förväntar sig.
    return {
      pickups: data[0],
      pickupClassifications: data[1],
      tonearms: data[2],
      tonearmsClassifications: data[3], // Använder pluralform
    };

  } catch (error) {
    console.error("Error fetching explorer data:", error);
    // Kasta om felet så att anropande kod (store) kan hantera det.
    throw error;
  }
}
// src/entities/data-explorer/api/fetchExplorerData.js
