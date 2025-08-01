// src/entities/data-explorer/lib/transformer.js
/**
 * Denna fil innehåller hjälpfunktioner för att transformera och berika rådata
 * som hämtas från de statiska JSON-filerna. Den är en central del av Data Explorer-entiteten.
 */

/**
 * Tar en array av dataobjekt (t.ex. tonearmar) och ett klassificeringsobjekt,
 * och slår ihop dem för att skapa "display-ready" data.
 *
 * @param {Array<Object>} items - En array av råa dataobjekt (t.ex. från tonearm-data.json).
 * @param {Object} classifications - Ett objekt med klassificeringsmappningar (t.ex. från tonearms-classifications.json).
 * @returns {Array<Object>} En ny array med berikade objekt.
 */
export function transformAndClassifyData(items, classifications) {
  if (!Array.isArray(items) || !classifications) {
    return [];
  }

  // Skapa en snabb uppslagsmapp för att undvika att loopa i en loop (för prestanda).
  const classificationMaps = {};
  for (const key in classifications) {
    classificationMaps[key] = new Map(
      classifications[key].categories.map(cat => [cat.id, cat.name])
    );
  }

  return items.map(item => {
    const enrichedItem = { ...item };

    for (const key in classificationMaps) {
      const newKey = `${key}_name`;
      const valueId = item[key];

      if (valueId !== null && valueId !== undefined) {
        const map = classificationMaps[key];
        if (map.has(valueId)) {
          enrichedItem[newKey] = map.get(valueId);
        } else {
          // Fallback om ett ID finns i datan men inte i klassificeringarna
          enrichedItem[newKey] = String(valueId);
        }
      } else {
        enrichedItem[newKey] = null;
      }
    }
    return enrichedItem;
  });
}
// src/entities/data-explorer/lib/transformer.js
