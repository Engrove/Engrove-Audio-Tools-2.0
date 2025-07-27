// /vite.config.js
// Denna fil konfigurerar Vite, vårt byggverktyg.
// Den talar om för Vite att vi använder Vue och specificerar
// pluginet som behövs för att kompilera .vue-filer.

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
})
// /vite.config.js
