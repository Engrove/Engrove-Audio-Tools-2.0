<!-- src/pages/home/HomePage.vue -->
<!-- Detta är applikationens landningssida. Den är strukturerad i sektioner -->
<!-- för att introducera projektets syfte, verktyg och filosofi. -->
<!-- Denna version använder de korrekta .webp-bilderna för att visualisera innehållet. -->
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
          <img src="/images/placeholders/tool-alignment.webp" alt="A screenshot of the Alignment Calculator interface, showing setup controls and optimal values." class="tool-image" loading="lazy">
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
          <img src="/images/placeholders/tool-resonance.webp" alt="A screenshot of the Resonance Calculator, showing sliders for mass and compliance." class="tool-image" loading="lazy">
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
          <img src="/images/placeholders/tool-compliance.webp" alt="A screenshot of the Compliance Estimator tool, displaying an estimated result and a confidence level." class="tool-image" loading="lazy">
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
          <img src="/images/placeholders/tool-data-explorer.webp" alt="A screenshot of the Data Explorer, showing a table of cartridges with filter controls." class="tool-image" loading="lazy">
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

<!-- ====================================================================== -->
<!-- SEKTION 3: PHILOSOPHY                                                  -->
<!-- ====================================================================== -->
<section class="philosophy-section page-section">
  <div class="section-container philosophy-layout">
    <div class="philosophy-text">
      <h2 class="section-title">An Open and Transparent Approach</h2>
      <p>These tools were born from a desire for accuracy. No magic formulas, just established audio engineering principles applied in a clean, predictable interface.</p>
      <p>The goal is to transform complex calculations into clear, understandable visualizations. The 'how' is just as important as the 'what', turning black boxes into glass boxes.</p>
      <p>This is a free and open-source project under the MIT License. The methodology is documented, the data is explorable, and community feedback is always welcome.</p>
    </div>
    <div class="philosophy-visual">
       <!-- Denna bild är en platshållare och behöver laddas upp till public/images/ -->
       <img src="/images/engrove-avatar.jpg" alt="An illustration of Jan-Eric Enlund, the creator of the Engrove Audio Toolkit." class="philosophy-avatar">
    </div>
  </div>
</section>

<!-- ====================================================================== -->
<!-- SEKTION 4: FINAL INVITATION                                            -->
<!-- ====================================================================== -->
<section class="final-cta-section page-section">
   <div class="section-container">
    <h2 class="section-title">Ready to Begin?</h2>
    <p>Select a tool to get started, or dive into the source code to see how it all works.</p>
    <div class="final-cta-buttons">
      <router-link to="/alignment-calculator" custom v-slot="{ navigate }">
        <BaseButton variant="primary" @click="navigate">Start with the Alignment Calculator</BaseButton>
      </router-link>
      <a href="https://github.com/Engrove/Engrove-Audio-Tools-2.0" target="_blank" rel="noopener noreferrer">
        <BaseButton variant="secondary">View Project on GitHub</BaseButton>
      </a>
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

// Här kommer vi senare att lägga till `useHead` för SEO-meta-taggar
</script>

<style scoped>
/* Generella stilar för sektioner och containers för konsistens */
.page-section {
padding: 6rem 1rem;
border-bottom: 1px solid var(--color-border-primary);
}
.page-section:last-child {
border-bottom: none;
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
border-bottom: none;
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
align-self: flex-start; /* Knappen justeras till vänster i kortet */
}


/* Sektion 3: Philosophy */
.philosophy-section .section-title {
text-align: left;
}
.philosophy-layout {
display: grid;
grid-template-columns: 1fr;
gap: 3rem;
align-items: center;
}
.philosophy-text p {
margin-bottom: 1.5rem;
line-height: 1.7;
max-width: 60ch;
}
.philosophy-text p:last-child {
margin-bottom: 0;
}
.philosophy-visual {
display: flex;
justify-content: center;
align-items: center;
}
.philosophy-avatar {
width: 100%;
max-width: 350px;
height: auto;
border-radius: 50%; /* Gör avataren cirkulär */
box-shadow: 0 10px 30px rgba(0,0,0,0.2);
border: 3px solid var(--color-surface-tertiary);
}

/* Sektion 4: Final Invitation */
.final-cta-section {
background-color: var(--color-surface-secondary);
}
.final-cta-section .section-container {
display: flex;
flex-direction: column;
align-items: center;
text-align: center;
}
.final-cta-section p {
max-width: 500px;
margin-bottom: 2rem;
color: var(--color-text-medium-emphasis);
}
.final-cta-buttons {
display: flex;
flex-wrap: wrap;
justify-content: center;
gap: 1rem;
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

@media (min-width: 992px) {
.philosophy-layout {
grid-template-columns: 2fr 1fr;
gap: 5rem;
}
}
</style>

<!-- src/pages/home/HomePage.vue -->
