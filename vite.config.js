// vite.config.js
// === SYFTE & ANSVAR ===
// Denna fil konfigurerar Vite, vårt byggverktyg. Den definierar plugins,
// sökvägs-alias och, viktigast av allt, alla HTML-ingångspunkter för projektet.
//
// === HISTORIK ===
// * v1.0 (Initial): Grundläggande konfiguration för Vue-appen.
// * v1.1: Lade till alias för 'vue/dist/vue.esm-bundler.js' för att stödja showcase.html.
// * v1.2: Lade till 'debug.html' som en ingångspunkt.
// * v1.3 (2025-08-15): Lade till 'index2.html' (Engrove Audio Tools Creator) som en ingångspunkt.
//
// === TILLÄMPADE REGLER (Frankensteen v5.4) ===
// - API-kontraktsverifiering: build.rollupOptions.input är korrekt formaterat.

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
        debug: resolve(__dirname, 'debug.html'),
        // NYTT: Lägger till vårt nya UI-verktyg som en fristående sida.
        engrove_tools: resolve(__dirname, 'index2.html'),
      }
    }
  }
});
// vite.config.js
