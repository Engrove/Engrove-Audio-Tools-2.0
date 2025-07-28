<!-- src/shared/ui/Logo.vue -->
<!-- Denna fil definierar en enkel, återanvändbar logotyp-komponent. -->
<!-- Den renderar projektets namn som en länk till startsidan. -->
<!-- Den är designad för att användas i GlobalHeader-widgeten. -->

<template>
  <router-link to="/" class="logo-link">
    <span class="logo-text">Engrove Audio</span>
    <!-- En platshållare för en framtida SVG-logotyp kan läggas till här -->
  </router-link>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
/* Stilar för logotyp-länken, säkerställer korrekt utseende och beteende. */
.logo-link {
  display: inline-flex;
  align-items: center;
  text-decoration: none; /* Tar bort standard-understrykning från länken */
  padding: 0.5rem 0; /* Ger lite vertikalt utrymme för klickbarhet */
}

/* Stilar för själva logotyp-texten */
.logo-text {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-h3); /* 20px, en passande storlek för en header-logotyp */
  font-weight: var(--font-weight-semibold); /* Ger texten lite extra vikt utan att vara fet */
  color: var(--color-text-high-emphasis);
  transition: color 0.2s ease-in-out;
}

/* Visuell feedback vid hover, i linje med standard-länkbeteende */
.logo-link:hover .logo-text {
  color: var(--color-interactive-accent);
}
</style>
<!-- src/shared/ui/Logo.vue -->
