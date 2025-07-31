// src/entities/settings/model/settingsStore.js
/**
 * @file Denna fil definierar en Pinia-store för att hantera globala användarinställningar.
 * Den första inställningen som hanteras är UI-densiteten ('comfortable' vs 'compact').
 * Storens tillstånd sparas automatiskt i webbläsarens localStorage.
 * Modul: Globala Inställningar
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useSettingsStore = defineStore('settings', () => {
  // --- STATE ---

  /**
   * @type {import('vue').Ref<'comfortable' | 'compact'>}
   * @description Lagrar den valda UI-densiteten.
   */
  const density = ref('comfortable');

  // --- GETTERS ---

  /**
   * @type {import('vue').ComputedRef<boolean>}
   * @description En beräknad egenskap som returnerar true om det kompakta temat är aktivt.
   */
  const isCompact = computed(() => density.value === 'compact');

  // --- ACTIONS ---

  /**
   * Sätter UI-densiteten till ett specifikt värde.
   * @param {'comfortable' | 'compact'} newDensity - Den nya densiteten att sätta.
   */
  function setDensity(newDensity) {
    if (['comfortable', 'compact'].includes(newDensity)) {
      density.value = newDensity;
    }
  }

  /**
   * Växlar mellan 'comfortable' och 'compact' densitet.
   */
  function toggleDensity() {
    // Om density.value är 'compact', sätt den till 'comfortable'.
    // Om density.value är något annat, sätt den till 'compact'.
    density.value = density.value === 'compact' ? 'comfortable' : 'compact';
  }

  return {
    // State
    density,
    // Getters
    isCompact,
    // Actions
    setDensity,
    toggleDensity,
  };
}, {
  // Konfiguration för pinia-plugin-persistedstate
  // Detta säkerställer att hela storens tillstånd sparas i localStorage
  // under nyckeln 'settings' och återställs vid sidladdning.
  persist: true,
});
// src/entities/settings/model/settingsStore.js
