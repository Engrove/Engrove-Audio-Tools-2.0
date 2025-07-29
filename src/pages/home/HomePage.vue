<!-- src/pages/home/HomePage.vue -->
<!-- Detta är applikationens landningssida. Denna uppdaterade version är mer -->
<!-- fokuserad på att direkt presentera verktygen för användaren. -->
<template>
<main class="home-page">
<!-- ====================================================================== -->
<!-- SEKTION 1: HERO -->
<!-- ====================================================================== -->
<section class="hero-section page-section">
<div class="section-container">
<h1 class="hero-title">Precision Tools for the Analog Enthusiast.</h1>
<p class="hero-subtitle">
An open-source toolkit for calculating tonearm alignment, resonance, compliance, and more.
Built by an audiophile, for audiophiles.
</p>
<BaseButton variant="primary" @click="scrollToToolkit">
Explore the Tools
</BaseButton>
</div>
</section>


<!-- ====================================================================== -->
<!-- SEKTION 2: TOOL SHOWCASE                                               -->
<!-- ====================================================================== -->
<section ref="toolkitSection" class="toolkit-section page-section">
  <div class="section-container">
    <h2 class="section-title">The Toolkit</h2>
    <div class="toolkit-grid">

      <!-- Kort 1: Alignment Calculator -->
      <div class="tool-card">
        <div class="tool-image-wrapper">
          <img src="/images/placeholders/preview-alignment.webp" alt="A screenshot of the Alignment Calculator interface, showing setup controls and optimal values." class="tool-image" loading="lazy">
        </div>
        <h3>Alignment Calculator</h3>
        <p>Visualize tracking error and distortion for different alignment geometries (Lofgren, Baerwald, Stevenson).</p>
        <router-link to="/alignment-calculator" custom v-slot="{ navigate }">
          <BaseButton variant="secondary" @click="navigate">Open Calculator</BaseButton>
        </router-link>
      </div>

      <!-- Kort 2: Resonance Calculator -->
      <div class="tool-card">
        <div class="tool-image-wrapper">
          <img src="/images/placeholders/preview-resonance.webp" alt="A screenshot of the Resonance Calculator, showing sliders for mass and compliance." class="tool-image" loading="lazy">
        </div>
        <h3>Resonance Calculator</h3>
        <p>Determine the resonant frequency of your tonearm and cartridge combination to avoid audible colorations.</p>
        <router-link to="/resonance-calculator" custom v-slot="{ navigate }">
          <BaseButton variant="secondary" @click="navigate">Open Calculator</BaseButton>
        </router-link>
      </div>

      <!-- Kort 3: Compliance Estimator -->
      <div class="tool-card">
        <div class="tool-image-wrapper">
          <img src="/images/placeholders/preview-compliance.webp" alt="A screenshot of the Compliance Estimator tool, displaying an estimated result and a confidence level." class="tool-image" loading="lazy">
        </div>
        <h3>Compliance Estimator</h3>
        <p>Estimate 10Hz compliance from 100Hz values using a statistical model from our open dataset.</p>
        <router-link to="/compliance-estimator" custom v-slot="{ navigate }">
          <BaseButton variant="secondary" @click="navigate">Open Estimator</BaseButton>
        </router-link>
      </div>
      
      <!-- Kort 4: Data Explorer -->
      <div class="tool-card">
         <div class="tool-image-wrapper">
          <img src="/images/placeholders/preview-explorer.webp" alt="A screenshot of the Data Explorer, showing a table of cartridges with filter controls." class="tool-image" loading="lazy">
        </div>
        <h3>Data Explorer</h3>
        <p>Search, filter, and explore the complete database of tonearms and cartridges used by the toolkit.</p>
        <router-link to="/data-explorer" custom v-slot="{ navigate }">
          <BaseButton variant="secondary" @click="navigate">Explore Data</BaseButton>
        </router-link>
      </div>
      
    </div>
  </div>
</section>

</main>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import BaseButton from '../../shared/ui/BaseButton.vue';

// Ref för att kunna scrolla till verktygssektionen
const toolkitSection = ref(null);

// Funktion för att mjukt scrolla ner till verktygen
const scrollToToolkit = () => {
toolkitSection.value?.scrollIntoView({ behavior: 'smooth' });
};

</script>

<style scoped>
/* Generella stilar för sektioner och containers för konsistens */
.page-section {
padding: 6rem 1rem;
}
.page-section:first-child {
  border-bottom: 1px solid var(--color-border-primary);
}
.page-section:last-child {
  padding-bottom: 8rem; /* Ge lite extra utrymme mot sidfoten */
}

.section-container {
max-width: 1200px;
margin: 0 auto;
}
.section-title {
text-align: center;
margin-bottom: 3rem;
}

/* Sektion 1: Hero */
.hero-section {
min-height: 80vh;
display: flex;
align-items: center;
justify-content: center;
text-align: center;
padding-top: 0;
padding-bottom: 4rem;
}
.hero-title {
font-size: clamp(2rem, 5vw, 3.5rem);
margin-bottom: 1.5rem;
}
.hero-subtitle {
font-size: clamp(1rem, 2vw, 1.25rem);
max-width: 650px;
margin: 0 auto 2.5rem auto;
color: var(--color-text-medium-emphasis);
line-height: 1.6;
}

/* Sektion 2: Tool Showcase */
.toolkit-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
gap: 2rem;
}
.tool-card {
background-color: var(--color-surface-secondary);
border: 1px solid var(--color-border-primary);
border-radius: 12px;
display: flex;
flex-direction: column;
overflow: hidden;
transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.tool-image-wrapper {
aspect-ratio: 16 / 9;
background-color: var(--color-surface-tertiary);
border-bottom: 1px solid var(--color-border-primary);
}
.tool-image {
width: 100%;
height: 100%;
object-fit: cover;
}
.tool-card h3 {
margin: 1.5rem 1.5rem 1rem 1.5rem;
}
.tool-card p {
padding: 0 1.5rem;
flex-grow: 1;
margin-bottom: 2rem;
color: var(--color-text-medium-emphasis);
}
.tool-card .base-button {
margin: 0 1.5rem 1.5rem 1.5rem;
align-self: flex-start;
}

/* Responsivitet för större skärmar */
@media (min-width: 768px) {
.page-section {
padding: 8rem 2rem;
}
.hero-section {
  padding-top: 4rem;
}
}
</style>
<!-- src/pages/home/HomePage.vue -->
