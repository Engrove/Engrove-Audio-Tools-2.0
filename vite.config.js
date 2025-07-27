// vite.config.js
// Denna fil konfigurerar Vite, vårt byggverktyg.
// Vi definierar här att projektet har flera "applikationer" som ska byggas:
// 1. Huvudapplikationen (index.html)
// 2. Vår komponent-showcase (public/showcase.html)

import { resolve } from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(), // Aktiverar Vites Vue-plugin för att hantera .vue-filer
  ],
  build: {
    rollupOptions: {
      input: {
        // Huvudingången för den vanliga applikationen
        main: resolve(__dirname, 'index.html'),

        // Ingången för vår showcase-sida.
        // Vite kommer nu att bygga denna HTML-fil och dess beroenden (JS/CSS)
        // som en separat enhet i dist-mappen.
        showcase: resolve(__dirname, 'public/showcase.html'),
      },
    },
  },
});
// vite.config.js
