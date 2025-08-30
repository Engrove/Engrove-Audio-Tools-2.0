<!-- src/widgets/GlobalFooter/GlobalFooter.vue -->
<!-- Denna widget är den globala sidfoten för hela applikationen. -->
<!-- Den visas längst ner på varje sida och innehåller länkar till -->
<!-- sekundära sidor som "About" och "License". -->
<template>
  <footer class="global-footer">
    <div class="footer-container">
      <div class="footer-links">
        <router-link to="/" class="footer-link">Home</router-link>
        <span class="link-divider">|</span>
        <router-link to="/about" class="footer-link">About & License</router-link>
      </div>
      <div class="footer-text">
        <span v-if="gitHash !== 'N/A'" class="git-hash" title="Build Version (Git Commit)">{{ gitHash }}</span>
        <span v-if="gitHash !== 'N/A'" class="link-divider">&nbsp;•&nbsp;</span>
        © {{ currentYear }} Engrove. All rights reserved.
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';
import { RouterLink } from 'vue-router';

// Beräknar det nuvarande året dynamiskt för copyright-meddelandet.
const currentYear = computed(() => new Date().getFullYear());

// Hämtar Git commit-hashen som injicerats av Vite vid byggtillfället.
const gitHash = import.meta.env.VITE_APP_GIT_HASH;
</script>

<style scoped>
.global-footer {
  width: 100%;
  padding: 2rem 1rem;
  background-color: var(--color-surface-secondary);
  border-top: 1px solid var(--color-border-primary);
  flex-shrink: 0; /* Förhindrar att fotern krymper om huvudinnehållet är litet */
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  text-align: center;
}

@media (min-width: 768px) {
  .footer-container {
    flex-direction: row;
    justify-content: space-between;
  }
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.footer-link {
  font-size: var(--font-size-label);
  color: var(--color-text-medium-emphasis);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: var(--color-text-high-emphasis);
  text-decoration: underline;
}

.link-divider {
  color: var(--color-text-low-emphasis);
}

.footer-text {
  font-size: var(--font-size-small);
  color: var(--color-text-low-emphasis);
  display: flex;
  align-items: center;
}

.git-hash {
  font-family: var(--font-family-mono);
  color: var(--color-text-low-emphasis);
  cursor: help;
}
</style>
<!-- src/widgets/GlobalFooter/GlobalFooter.vue -->
