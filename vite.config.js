// vite.config.js
// Denna fil konfigurerar Vite. Den slutgiltiga korrigeringen är att
// tvinga Vite att använda den fullständiga versionen av Vue (med mall-kompilator)
// för att kunna hantera in-DOM-mallar som den i showcase.html.

import { resolve } from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [
    vue(),
  ],

  // NYTT OCH KRITISKT AVSNITT
  resolve: {
    alias: {
      // Detta alias tvingar Vite att använda "full build" av Vue som inkluderar
      // runtime-kompilatorn. Detta är nödvändigt eftersom showcase.html använder
      // en in-DOM-mall som måste kompileras i webbläsaren.
      'vue': 'vue/dist/vue.esm-bundler.js',
    }
  },

  build: {
    rollupOptions: {
      input: {
        // Huvudingången är oförändrad.
        main: resolve(__dirname, 'index.html'),

        // Ingången för showcase är oförändrad.
        showcase: resolve(__dirname, 'showcase.html'),
      },
    },
  },
});
// vite.config.js
