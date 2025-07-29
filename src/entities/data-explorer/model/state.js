// src/entities/data-explorer/model/state.js
/**
 * Denna fil definierar och exporterar det reaktiva tillståndet (state)
 * för Data Explorer-modulen. Enligt hypergranularitetsprincipen innehåller
 * denna fil endast state-deklarationer, ingen logik.
 */

import { ref } from 'vue';

// --- Globalt Modul-State ---

/**
 * @type {import('vue').Ref<boolean>}
 * Flagga för att indikera om datan håller på att laddas.
 */
export const isLoading = ref(true);

/**
 * @type {import('vue').Ref<string|null>}
 * Håller ett eventuellt felmeddelande om datainhämtningen misslyckas.
 */
export const error = ref(null);

// --- Rådata (Hämtad från API) ---

/**
 * @type {import('vue').Ref<Array<Object>>}
 * Rådata för alla pickuper.
 */
export const allPickups = ref([]);

/**
 * @type {import('vue').Ref<Array<Object>>}
 * Rådata för alla tonarmar.
 */
export const allTonearms = ref([]);

/**
 * @type {import('vue').Ref<Object|null>}
 * Rådata för alla pickup-klassificeringar (filterkategorier).
 */
export const pickupClassifications = ref(null);

/**
 * @type {import('vue').Ref<Object|null>}
 * Rådata för alla tonarms-klassificeringar (filterkategorier).
 */
export const tonearmClassifications = ref(null);


// --- Användarinteraktion och Filter-State ---

/**
 * @type {import('vue').Ref<'tonearms' | 'cartridges'>}
 * Vilken typ av data som för närvarande visas.
 */
export const dataType = ref('tonearms');

/**
 * @type {import('vue').Ref<string>}
 * Den aktuella söktermen från användarens textinmatning.
 */
export const searchTerm = ref('');

/**
 * @type {import('vue').Ref<Object>}
 * Ett objekt som håller de valda värdena för de kategoriska filtren.
 * Exempel: { compliance_level: 'high', bearing_type: 'unipivot' }
 */
export const categoryFilters = ref({});

/**
 * @type {import('vue').Ref<Object>}
 * Ett objekt som håller de valda värdena för de numeriska intervallfiltren.
 * Exempel: { effective_mass_g: { min: 10, max: 15 } }
 */
export const numericFilters = ref({});

// --- Sortering och Paginering-State ---

/**
 * @type {import('vue').Ref<string>}
 * Nyckeln för den kolumn som datan för närvarande sorteras efter.
 */
export const sortKey = ref('manufacturer');

/**
 * @type {import('vue').Ref<'asc' | 'desc'>}
 * Sorteringsordningen.
 */
export const sortOrder = ref('asc');

/**
 * @type {import('vue').Ref<number>}
 * Den aktuella sidan i pagineringen.
 */
export const currentPage = ref(1);

/**
 * @type {import('vue').Ref<number>}
 * Antal objekt som ska visas per sida.
 */
export const itemsPerPage = ref(20);
// src/entities/data-explorer/model/state.js
