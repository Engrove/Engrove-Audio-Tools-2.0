// src/features/theme-toggle/model/themeStore.js
// Denna Pinia store hanterar det globala tematillståndet för applikationen.
// Den är konfigurerad att spara temat i localStorage för att bibehålla
// användarens val mellan sessioner.

import { defineStore } from 'pinia';

// Definierar en ny Pinia store med namnet 'theme'.
export const useThemeStore = defineStore('theme', {
  // `state` är en funktion som returnerar det initiala tillståndet.
  state: () => ({
    // Temat är som standard 'dark'.
    currentTheme: 'dark',
  }),

  // `getters` är beräknade egenskaper baserade på state.
  getters: {
    // En getter för att enkelt kunna kontrollera om det mörka temat är aktivt.
    // Returnerar true om currentTheme är 'dark', annars false.
    isDarkTheme: (state) => state.currentTheme === 'dark',
  },

  // `actions` är funktioner som kan mutera (ändra) tillståndet.
  actions: {
    /**
     * Växlar temat mellan 'dark' och 'light'.
     */
    toggleTheme() {
      // Om this.currentTheme är 'dark', sätt det till 'light'.
      // Annars, sätt det till 'dark'.
      this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
    },

    /**
     * Sätter temat till ett specifikt värde.
     * @param {'dark' | 'light'} theme - Temat som ska sättas.
     */
    setTheme(theme) {
      if (theme === 'dark' || theme === 'light') {
        this.currentTheme = theme;
      }
    },
  },

  // Konfiguration för `pinia-plugin-persistedstate`.
  // Detta säkerställer att hela storens state sparas automatiskt
  // i webbläsarens localStorage under nyckeln 'theme'.
  persist: true,
});
// src/features/theme-toggle/model/themeStore.js
