// vite.config.js
// Denna fil konfigurerar Vite, vårt byggverktyg.
//
// ÄNDRING:
// - Lade till 'debug.html' i `build.rollupOptions.input`. Detta instruerar Vite
//   att behandla `debug.html` som en ytterligare ingångspunkt under byggprocessen,
//   vilket gör den tillgänglig som en separat sida i den färdiga applikationen.

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // Denna alias är kritisk för att säkerställa att Vue-mallar kan kompileras
      // i webbläsaren, vilket är nödvändigt för showcase.html och debug.html.
      'vue': 'vue/dist/vue.esm-bundler.js',
      // Standard-alias för att förenkla import-sökvägar.
      '@': resolve(__dirname, 'src'),
    }
  },
  build: {
    rollupOptions: {
      // Definierar de olika HTML-filerna som ska agera som ingångspunkter.
      // Vite kommer att bygga varje fil och dess beroenden separat.
      input: {
        main: resolve(__dirname, 'index.html'),
        showcase: resolve(__dirname, 'showcase.html'),
        // NYTT: Lägger till vår nya felsökningssida.
        debug: resolve(__dirname, 'debug.html'),
      }
    }
  }
});
// vite.config.js
