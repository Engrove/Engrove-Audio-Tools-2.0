// vite.config.js
// Uppdaterad konfiguration för att reflektera den nya filstrukturen.

import { resolve } from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [
    vue(),
  ],
  build: {
    rollupOptions: {
      input: {
        // Huvudingången är oförändrad.
        main: resolve(__dirname, 'index.html'),

        // Ingången för showcase pekar nu till filen i projektets rot.
        showcase: resolve(__dirname, 'showcase.html'),
      },
    },
  },
});
// vite.config.js
