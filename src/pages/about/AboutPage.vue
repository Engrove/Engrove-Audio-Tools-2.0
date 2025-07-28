<!-- src/pages/about/AboutPage.vue -->
<!-- Denna sida fungerar som ett nav för all metainformation om projektet. -->
<!-- Den förklarar filosofin, presenterar skaparen och ger länkar till -->
<!-- källkod och licens (via en modal). -->

<template>
  <main class="about-page">
    <div class="page-container">
      
      <!-- Sektion 1: Filosofi (Flyttad från HomePage) -->
      <section class="page-section philosophy-section">
        <div class="philosophy-layout">
          <div class="philosophy-text">
            <h1 class="page-title">An Open and Transparent Approach</h1>
            <p>These tools were born from a desire for accuracy. No magic formulas, just established audio engineering principles applied in a clean, predictable interface.</p>
            <p>The goal is to transform complex calculations into clear, understandable visualizations. The 'how' is just as important as the 'what', turning black boxes into glass boxes.</p>
            <p>This is a free and open-source project. The methodology is documented, the data is explorable, and community feedback is always welcome.</p>
          </div>
          <div class="philosophy-visual">
            <img src="/images/engrove.webp" alt="An illustration of Jan-Eric Enlund, the creator of the Engrove Audio Toolkit." class="philosophy-avatar">
          </div>
        </div>
      </section>

      <!-- Sektion 2: Källkod och Licens -->
      <section class="page-section cta-section">
        <h2 class="section-title">Source Code & License</h2>
        <p class="section-subtitle">
          The complete source code is available on GitHub under the AGPLv3 License. Feel free to explore, contribute, or raise issues.
        </p>
        <div class="cta-buttons">
          <a href="https://github.com/Engrove/Engrove-Audio-Tools-2.0" target="_blank" rel="noopener noreferrer">
            <BaseButton variant="primary">View Project on GitHub</BaseButton>
          </a>
          <!-- Denna knapp kommer att öppna LicenseModal-komponenten -->
          <BaseButton variant="secondary" @click="isLicenseModalOpen = true">
            View Software License
          </BaseButton>
        </div>
      </section>

    </div>

    <!-- LicenseModal-komponenten. Den är alltid i DOM men visas bara när isLicenseModalOpen är true. -->
    <LicenseModal v-model:isOpen="isLicenseModalOpen" />

  </main>
</template>

<script setup>
import { ref } from 'vue';
import BaseButton from '../../shared/ui/BaseButton.vue';
import LicenseModal from '../../features/license-modal/ui/LicenseModal.vue';

// Lokalt state för att styra synligheten av licensmodalen.
const isLicenseModalOpen = ref(false);

</script>

<style scoped>
/* Allmänna stilar för sidan och sektioner */
.about-page {
  padding: 2rem 1rem;
}

@media (min-width: 768px) {
  .about-page {
    padding: 4rem 2rem;
  }
}

.page-container {
  max-width: 1000px;
  margin: 0 auto;
}

.page-section {
  padding: 4rem 0;
}

.page-section:first-child {
  padding-top: 2rem;
}

.page-section:not(:last-child) {
  border-bottom: 1px solid var(--color-border-primary);
}

.page-title {
  margin-bottom: 1.5rem;
}

.section-title {
  text-align: center;
  margin-bottom: 1rem;
}

.section-subtitle {
  text-align: center;
  color: var(--color-text-medium-emphasis);
  max-width: 60ch;
  margin: 0 auto 2.5rem auto;
}

/* Layout för Filosofi-sektionen */
.philosophy-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 3rem;
  align-items: center;
}

@media (min-width: 992px) {
  .philosophy-layout {
    grid-template-columns: 2fr 1fr;
    gap: 5rem;
  }
}

.philosophy-text p {
  margin-bottom: 1.5rem;
  line-height: 1.7;
  max-width: 65ch;
  color: var(--color-text-medium-emphasis);
}

.philosophy-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.philosophy-avatar {
  width: 100%;
  max-width: 300px;
  height: auto;
  border-radius: 50%;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  border: 3px solid var(--color-surface-tertiary);
}

/* Layout för CTA-sektionen */
.cta-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}
</style>
<!-- src/pages/about/AboutPage.vue -->
