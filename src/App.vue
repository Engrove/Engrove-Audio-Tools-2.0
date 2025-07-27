<!-- /src/App.vue -->
<script setup>
// Denna fil är rotkomponenten för hela Vue-applikationen.
// För tillfället importerar och renderar den endast vår HomePage
// för att verifiera att hela byggkedjan fungerar.
// Senare kommer denna fil att innehålla <router-view> för att hantera sidnavigation.
import HomePage from './pages/home/HomePage.vue'
</script>

<template>
  <HomePage />
</template>

<style scoped>
/* Här kan globala, men scopade, stilar för app-ramverket läggas till senare. */
</style>
<!-- /src/App.vue -->
