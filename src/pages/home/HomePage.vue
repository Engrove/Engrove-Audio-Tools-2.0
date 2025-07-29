<!-- src/pages/home/HomePage.vue -->
<!-- Detta är landningssidan som presenterar verktygen och projektets filosofi. -->
<!-- Den har nu också en subtil bakgrundsbild som anpassas efter valt tema. -->
<template>
<main class="home-page">
<!-- Bakgrundsbildssektion -->
<div class="background-image-container"></div>

<!-- Hero-sektion -->
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

<!-- TOOL SHOWCASE SEKTION -->
<section ref="toolkitSection" class="toolkit-section page-section">
  <div class="section-container">
    <h2 class="section-title">The Toolkit</h2>
    <div class="toolkit-grid">

      <!-- Kort 1: Alignment Calculator -->
      <div class="tool-card">
        <div class="tool-image-wrapper">
          <img src="/images/preview-alignment.webp" alt="A screenshot of the Alignment Calculator interface, showing setup controls and optimal values." class="tool-image" loading="lazy" width="320" height="200">
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
          <img src="/images/preview-resonance.webp" alt="A screenshot of the Resonance Calculator, showing sliders for mass and compliance." class="tool-image" loading="lazy" width="320" height="200">
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
          <img src="/images/preview-compliance.webp" alt="A screenshot of the Compliance Estimator tool, displaying an estimated result and a confidence level." class="tool-image" loading="lazy" width="320" height="200">
        </div>
        <h3>Compliance Estimator</h3>
        <p>Estimate a cartridge's dynamic compliance at 10Hz using a statistical model from our open dataset.</p>
        <router-link to="/compliance-estimator" custom v-slot="{ navigate }">
          <BaseButton variant="secondary" @click="navigate">Open Estimator</BaseButton>
        </router-link>
      </div>

      <!-- Kort 4: Data Explorer -->
      <div class="tool-card">
        <div class="tool-image-wrapper">
          <img src="/images/preview-explorer.webp" alt="A screenshot of the Data Explorer, showing a table of cartridges with filter controls." class="tool-image" loading="lazy" width="320" height="200">
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

</div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import BaseButton from '../../shared/ui/BaseButton.vue';

// Ref för att kunna scrolla ner till verktygssektionen
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
position: relative; /* Nödvändigt för absolut positionering av bakgrundsbilden */
overflow: hidden; /* Säkerställer att bakgrundsbilden inte läcker utanför sektionen */
}

.page-section:first-child {
padding-top: 2rem; /* Liten justering för att ge plats åt headern */
}
.page-section:not(:last-child) {
border-bottom: 1px solid var(--color-border-primary);
}
.page-section:last-child {
padding-bottom: 8rem; /* Ge lite extra utrymme mot sidfoten */
}

.section-container {
max-width: 1200px;
margin: 0 auto;
position: relative; /* Viktigt för att bakgrundsbilden ska vara bakom innehållet */
z-index: 1; /* Se till att innehållet ligger ovanpå bakgrunden */
}

.section-title {
font-size: clamp(1.8rem, 4vw, 2.5rem); /* Responsiv rubrikstorlek */
margin-bottom: 3rem;
}

/* Sektion 1: Hero */
.hero-section {
min-height: 80vh; /* Håller hero-sektionen stor */
display: flex;
align-items: center;
justify-content: center;
text-align: center;
padding-top: 4rem; /* Justerar för att headern inte ska skymma innehållet */
color: var(--color-text-high-emphasis); /* Vit text på mörk bakgrund */
}

.hero-title {
font-size: clamp(2rem, 5vw, 3.5rem); /* Responsiv rubrikstorlek */
margin-bottom: 1.5rem;
line-height: 1.2;
}
.hero-subtitle {
font-size: clamp(1rem, 2vw, 1.25rem);
max-width: 650px;
margin: 0 auto 2.5rem auto;
color: var(--color-text-medium-emphasis);
line-height: 1.7;
}

/* Sektion 2: Tool Showcase */
.toolkit-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); /* Responsivt rutnät */
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
box-shadow: 0 8px 20px rgba(0,0,0,0.1); /* Subtil skugga */
}
.tool-image-wrapper {
aspect-ratio: 16 / 9; /* Behåller bildförhållandet */
background-color: var(--color-surface-tertiary);
border-bottom: 1px solid var(--color-border-primary);
}
.tool-image {
width: 100%;
height: 100%;
object-fit: cover; /* Skalar bilden för att täcka behållaren */
}
.tool-card h3 {
margin: 1.5rem 1.5rem 1rem 1.5rem;
color: var(--color-interactive-accent); /* Använder accentfärgen för rubrikerna */
}
.tool-card p {
padding: 0 1.5rem;
flex-grow: 1; /* Låter texten ta upp tillgängligt utrymme */
margin-bottom: 2rem;
color: var(--color-text-medium-emphasis);
line-height: 1.6;
}
.tool-card .base-button {
margin: 0 1.5rem 1.5rem 1.5rem;
align-self: flex-start; /* Knappen ska linjera med texten */
}

/* Bakgrundsbildshantering */
.background-image-container {
position: absolute;
top: 0;
left: 0;
width: 100%;
height: 100%;
background-size: cover;
background-position: center;
z-index: -1; /* Placera bakgrunden bakom allt annat */
opacity: 0.6; /* Subtil visning */
transition: background-image 0.3s ease-in-out;
}

/* Byt bakgrundsbild baserat på temat */
/* Använder :global för att kunna komma åt klassen på body/html, eftersom detta är en scoped-stil */
:global(.dark-theme) .background-image-container {
background-image: url('/images/bg_black.webp');
}

:global(.light-theme) .background-image-container {
background-image: url('/images/bg_white.webp');
}

/* Responsivitet för mobil */
@media (max-width: 768px) {
.hero-section {
min-height: 60vh; /* Lite mindre höjd på mobil */
}
.section-container {
padding: 0 1rem; /* Mer padding på sidorna på mobil */
}
.toolkit-grid {
grid-template-columns: 1fr; /* Stapla korten på en kolumn */
}
.tool-card {
width: 100%;
}
.home-footer {
text-align: center;
}
}

/* ----- SEMANTISK KOD & ACCESSIBILITET ----- */
/* Även om ingen specifik kodändring krävs här, säkerställer vi att */
/* `main`, `section`, `h1`, `p`, `div`, `img` etc. är korrekt använda. */
/* Detaljerad ARIA-hantering sker i baskomponenterna (t.ex. BaseButton). */

/* Lägger till en liten förbättring för bilders responsivitet (om de skulle vara utanför korten) */
img {
max-width: 100%;
height: auto;
display: block; /* Tar bort extra marginaler */
}
</style>

<!-- src/pages/home/HomePage.vue -->
