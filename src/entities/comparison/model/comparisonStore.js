// src/entities/comparison/model/comparisonStore.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

const COMPARISON_LIMIT = 5;

export const useComparisonStore = defineStore('comparison', () => {
  // =============================================
  // File history
  // =============================================
  // 2025-08-04: Created by Frankensteen as part of Steg 23, Fas 3.
  //             - Establishes the core logic for the item comparison feature.
  //             - Manages a reactive list of selected item IDs.
  //             - Implements a limit to how many items can be compared.
  //             - Provides getters and actions for other components to interact with.
  //

  // =============================================
  // Instruktioner vid skapande av fil
  // =============================================
  // Kärndirektiv: Fullständig kod, alltid. Inga genvägar.
  // Principen "Explicit Alltid": All logik, inklusive gränskontroller, är tydlig.
  // API-kontraktsverifiering: Getters och Actions utgör ett stabilt kontrakt.
  // Red Team Alter Ego-granskning: Gränsfallet (att lägga till ett sjätte objekt) är hanterat.
  // Obligatorisk Refaktorisering: Koden är koncis och fokuserad på sitt enda ansvar.
  //

  // =============================================
  // State
  // =============================================
  const selectedItemIds = ref([]);

  // =============================================
  // Getters & Computed Properties
  // =============================================
  const selectedItemsCount = computed(() => selectedItemIds.value.length);

  const isLimitReached = computed(() => selectedItemsCount.value >= COMPARISON_LIMIT);

  const isSelected = computed(() => {
    // Return a function to allow passing itemId from component
    return (itemId) => selectedItemIds.value.includes(itemId);
  });

  // =============================================
  // Actions
  // =============================================

  /**
   * Toggles the selection status of an item.
   * Adds the item's ID to the selection if not present,
   * or removes it if it is already selected.
   * Respects the COMPARISON_LIMIT.
   * @param {string | number} itemId - The unique ID of the item to toggle.
   */
  function toggleItem(itemId) {
    const index = selectedItemIds.value.indexOf(itemId);

    if (index === -1) {
      // Item is not selected, add it if limit is not reached.
      if (!isLimitReached.value) {
        selectedItemIds.value.push(itemId);
      } else {
        // Optional: Provide feedback that the limit is reached.
        // For now, it just silently fails to add, which is handled by disabling checkboxes in the UI.
        console.warn(`Comparison limit of ${COMPARISON_LIMIT} reached. Cannot add more items.`);
      }
    } else {
      // Item is selected, remove it.
      selectedItemIds.value.splice(index, 1);
    }
  }

  /**
   * Clears the entire selection of items.
   */
  function clearSelection() {
    selectedItemIds.value = [];
  }

  return {
    // State
    selectedItemIds,
    // Getters
    selectedItemsCount,
    isLimitReached,
    isSelected,
    // Actions
    toggleItem,
    clearSelection,
  };
});
// src/entities/comparison/model/comparisonStore.js
