// src/entities/data-explorer/lib/filters.js
/**
 * Denna fil innehåller rena, "pure" JavaScript-funktioner för att filtrera,
 * söka och sortera listor med data (tonarmar eller pickuper).
 * Dessa funktioner är helt frikopplade från Vue's reaktivitetssystem,
 * vilket gör dem enkla att testa och återanvända.
 */

/**
 * Filtrerar en lista av objekt baserat på en sökterm och ett antal filter.
 * 
 * @param {Array<Object>} items - Listan med objekt som ska filtreras (t.ex. alla tonarmar).
 * @param {string} searchTerm - Söksträngen som användaren har matat in.
 * @param {Object} categoryFilters - Ett objekt med kategoriska filter. 
 *   Exempel: { compliance_level: 'high', bearing_type: 'unipivot' }
 * @param {Object} numericFilters - Ett objekt med numeriska intervallfilter.
 *   Exempel: { effective_mass_g: { min: 10, max: 15 } }
 * @returns {Array<Object>} En ny array med de filtrerade objekten.
 */
export function applyFilters(items, searchTerm, categoryFilters, numericFilters) {
  // Normalisera söktermen för skiftlägesokänslig sökning.
  const normalizedSearchTerm = searchTerm.toLowerCase().trim();

  return items.filter(item => {
    // --- Söktermsfiltrering (Text Search) ---
    // Söker i 'manufacturer' och 'model'. Om söktermen är tom, godkänns alla.
    const manufacturerMatch = item.manufacturer ? item.manufacturer.toLowerCase().includes(normalizedSearchTerm) : false;
    const modelMatch = item.model ? item.model.toLowerCase().includes(normalizedSearchTerm) : false;
    const searchMatch = normalizedSearchTerm === '' ? true : (manufacturerMatch || modelMatch);
    if (!searchMatch) {
      return false;
    }

    // --- Kategorisk Filtrering (Dropdowns) ---
    // Loopar igenom alla aktiva kategorifilter.
    for (const key in categoryFilters) {
      const filterValue = categoryFilters[key];
      // Om ett filter är satt (inte null/undefined) och objektets värde inte matchar, uteslut det.
      if (filterValue && item[key] !== filterValue) {
        return false;
      }
    }

    // --- Numerisk Intervallfiltrering (Range Filters) ---
    // Loopar igenom alla aktiva numeriska filter.
    for (const key in numericFilters) {
      const { min, max } = numericFilters[key];
      const itemValue = item[key];
      
      // Hoppa över om objektet saknar värde för detta filter.
      if (itemValue === null || itemValue === undefined) {
        continue;
      }

      // Om ett min-värde är satt och objektets värde är mindre, uteslut det.
      if (min !== null && itemValue < min) {
        return false;
      }
      // Om ett max-värde är satt och objektets värde är större, uteslut det.
      if (max !== null && itemValue > max) {
        return false;
      }
    }

    // Om objektet klarade alla kontroller, inkludera det i resultatet.
    return true;
  });
}

/**
 * Sorterar en lista av objekt baserat på en nyckel och ordning.
 * 
 * @param {Array<Object>} items - Listan med objekt som ska sorteras.
 * @param {string} sortKey - Nyckeln (egenskapen) att sortera efter.
 * @param {'asc' | 'desc'} sortOrder - Sorteringsordningen.
 * @returns {Array<Object>} En ny, sorterad array.
 */
export function applySorting(items, sortKey, sortOrder) {
  // Om ingen sorteringsnyckel är angiven, returnera listan som den är.
  if (!sortKey) {
    return items;
  }

  // Skapa en kopia av arrayen för att undvika att mutera originalet.
  return [...items].sort((a, b) => {
    const valA = a[sortKey];
    const valB = b[sortKey];

    // Hantera null/undefined-värden så att de alltid hamnar sist.
    if (valA === null || valA === undefined) return 1;
    if (valB === null || valB === undefined) return -1;

    let comparison = 0;
    // Jämför baserat på datatyp.
    if (typeof valA === 'number' && typeof valB === 'number') {
      comparison = valA - valB;
    } else {
      comparison = String(valA).toLowerCase().localeCompare(String(valB).toLowerCase());
    }
    
    // Om sortOrder är 'desc', invertera jämförelseresultatet.
    // Om sortOrder är 'asc', returnera comparison direkt.
    return sortOrder === 'desc' ? -comparison : comparison;
  });
}
// src/entities/data-explorer/lib/filters.js
