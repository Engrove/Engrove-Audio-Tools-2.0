// src/entities/data-explorer/api/fetchExplorerData.js
// This file centralizes all data fetching for the Data Explorer module.
// It fetches the main data files and their corresponding classification files in parallel.
// UPDATED: Implements cache busting to ensure the latest data is always fetched on a new deployment.

// --- CACHE BUSTING ---
// A unique timestamp is generated each time the app is loaded.
// This is appended to the fetch URLs to bypass browser and CDN caches,
// ensuring users always get the latest version of the data files after a new build.
const cacheBuster = new Date().getTime();

/**
 * Fetches a JSON file from the specified path with a cache-busting parameter.
 * Throws an error if the network response is not ok.
 * @param {string} path - The path to the JSON file (e.g., '/data/pickups-data.json').
 * @returns {Promise<Object>} A promise that resolves to the parsed JSON data.
 */
const fetchData = async (path) => {
  // Append the cache buster query parameter to the path.
  const urlWithCacheBuster = `${path}?v=${cacheBuster}`;
  const response = await fetch(urlWithCacheBuster);
  if (!response.ok) {
    throw new Error(`Network response was not ok for ${path}: ${response.statusText}`);
  }
  return response.json();
};

/**
 * Fetches all necessary data for the Data Explorer.
 * This function runs all fetch operations in parallel for maximum efficiency.
 * @returns {Promise<Object>} A promise that resolves to an object containing all fetched data.
 */
export const fetchExplorerData = async () => {
  try {
    // Using Promise.all to fetch all data sources concurrently.
    const [
      pickupsData,
      pickupsClassifications,
      tonearmsData,
      tonearmsClassifications,
    ] = await Promise.all([
      fetchData('/data/pickups-data.json'),
      fetchData('/data/pickups-classifications.json'),
      fetchData('/data/tonearm-data.json'),
      fetchData('/data/tonearms-classifications.json'),
    ]);

    // Return a single object containing all the fetched data.
    return {
      pickupsData,
      pickupsClassifications,
      tonearmsData,
      tonearmsClassifications,
    };
  } catch (error) {
    console.error('Failed to fetch explorer data:', error);
    // Re-throw the error so the calling store (explorerStore) can handle it
    // and update its state accordingly (e.g., setting an error message).
    throw error;
  }
};
// src/entities/data-explorer/api/fetchExplorerData.js
