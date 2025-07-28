<!-- src/pages/license/LicensePage.vue -->
<!-- Denna sidkomponent är dedikerad till att visa programvarulicensen. -->
<!-- Den hämtar licenstexten och renderar den med hjälp av den återanvändbara -->
<!-- BaseCanvasTextViewer-komponenten för en enhetlig och stiliserad visning. -->
<template>
  <main class="license-page">
    <div class="page-container">
      <h1 class="page-title">Software License</h1>
      <p class="page-subtitle">
        Engrove Audio Toolkit is distributed under the GNU Affero General Public License v3.0.
      </p>
      <div class="license-viewer-wrapper">
        <BaseCanvasTextViewer :text="licenseText" />
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import BaseCanvasTextViewer from '../../shared/ui/BaseCanvasTextViewer.vue';

// --- STATE ---
// En reaktiv referens för att hålla licenstexten.
// Initialt visas ett meddelande medan texten laddas.
const licenseText = ref('Laddar licenstext...');

// --- LIFECYCLE HOOKS ---
// När komponenten har monterats i DOM, körs denna funktion för att
// hämta licenstexten från den statiska filen i /public-mappen.
onMounted(async () => {
  try {
    // Använder fetch API för att hämta filen.
    const response = await fetch('/LICENSE');
    if (response.ok) {
      // Om hämtningen lyckades, uppdatera referensen med textinnehållet.
      licenseText.value = await response.text();
    } else {
      // Om filen inte hittades (t.ex. 404-fel), visa ett felmeddelande.
      licenseText.value = 'Kunde inte ladda licenstexten. Kontrollera att filen /LICENSE finns i projektets rot.';
    }
  } catch (error) {
    // Om ett nätverksfel eller annat fel inträffar, logga det och visa ett felmeddelande.
    console.error('Fel vid hämtning av licens:', error);
    licenseText.value = 'Ett fel uppstod vid hämtning av licensfilen.';
  }
});
</script>

<style scoped>
/* Allmänna stilar för sidan för att säkerställa konsekvent layout */
.license-page {
  padding: 2rem;
}

.page-container {
  max-width: 900px;
  margin: 0 auto;
}

.page-title {
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: var(--color-text-medium-emphasis);
  margin-bottom: 2rem;
}

/* Denna wrapper är nödvändig för att ge canvas-komponenten en definierad höjd, */
/* vilket i sin tur gör att dess interna scroll-funktion fungerar korrekt. */
.license-viewer-wrapper {
  height: 70vh; /* Använder 70% av viewport-höjden för flexibilitet */
  max-height: 800px; /* Sätter ett max-tak på höjden */
}
</style>
<!-- src/pages/license/LicensePage.vue -->
