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
 *   Exempel (Single-select): { compliance_level: 'high' }
 *   Exempel (Multi-select): { manufacturer: ['Ortofon', 'Rega'], stylus_family: ['Elliptical'] }
 * @param {Object} numericFilters - Ett objekt med numeriska intervallfilter.
 *   Exempel: { effective_mass_g: { min: 10, max: 15 } }
 * @returns {Array<Object>} En ny array med de filtrerade objekten.
 */
export function applyFilters(items, searchTerm, categoryFilters, numericFilters) {
  const normalizedSearchTerm = searchTerm.toLowerCase().trim();

  return items.filter(item => {
    // --- Söktermsfiltrering (Text Search) ---
    const manufacturerMatch = item.manufacturer ? item.manufacturer.toLowerCase().includes(normalizedSearchTerm) : false;
    const modelMatch = item.model ? item.model.toLowerCase().includes(normalizedSearchTerm) : false;
    const searchMatch = normalizedSearchTerm === '' ? true : (manufacturerMatch || modelMatch);
    if (!searchMatch) {
      return false;
    }

    // --- Kategorisk Filtrering (Dropdowns & Multi-Select) ---
    for (const key in categoryFilters) {
      const filterValues = categoryFilters[key];
      
      // Hoppa över om filtret är null, undefined eller en tom array.
      if (!filterValues || filterValues.length === 0) {
        continue;
      }
      
      const itemValue = item[key];
      const filterValuesArray = Array.isArray(filterValues) ? filterValues : [filterValues];

      // Hantera "tags" speciellt, eftersom det är en array i datan.
      if (key === 'tags' && Array.isArray(itemValue)) {
        // Om någon av item's tags finns i filter-arrayen, är det en match.
        const tagMatch = itemValue.some(tag => filterValuesArray.includes(tag));
        if (!tagMatch) {
          return false;
        }
      } else {
        // För alla andra fält, kontrollera om item's värde finns i filter-arrayen.
        if (!filterValuesArray.includes(itemValue)) {
          return false;
        }
      }
    }

    // --- Numerisk Intervallfiltrering (Range Filters) ---
    for (const key in numericFilters) {
      const { min, max } = numericFilters[key];
      const itemValue = item[key];
      
      if (itemValue === null || itemValue === undefined) {
        continue;
      }

      if (min !== null && min !== undefined && itemValue < min) {
        return false;
      }
      if (max !== null && max !== undefined && itemValue > max) {
        return false;
      }
    }

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
  if (!sortKey) {
    return items;
  }

  return [...items].sort((a, b) => {
    const valA = a[sortKey];
    const valB = b[sortKey];

    if (valA === null || valA === undefined) return 1;
    if (valB === null || valB === undefined) return -1;

    let comparison = 0;
    if (typeof valA === 'number' && typeof valB === 'number') {
      comparison = valA - valB;
    } else {
      comparison = String(valA).toLowerCase().localeCompare(String(valB).toLowerCase());
    }
    
    return sortOrder === 'desc' ? -comparison : comparison;
  });
}
// src/entities/data-explorer/lib/filters.js
