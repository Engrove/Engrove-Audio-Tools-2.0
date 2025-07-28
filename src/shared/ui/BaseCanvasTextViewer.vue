// src/shared/ui/BaseCanvasTextViewer.vue
// Denna komponent är en återanvändbar, generell textvisare som renderar
// en given textsträng på ett HTML <canvas>-element. Den hanterar
// automatisk radbrytning och hämtar stilinformation (färg, typsnitt)
// från de globala design-tokens för att säkerställa visuell konsekvens.

<template>
  <div class="canvas-viewer-container" ref="containerRef">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { useThemeStore } from '../../features/theme-toggle/model/themeStore.js';

// --- PROPS ---
const props = defineProps({
  text: {
    type: String,
    required: true,
    default: 'Ingen text att visa.'
  }
});

// --- REFS ---
const canvasRef = ref(null);
const containerRef = ref(null);
const themeStore = useThemeStore();
let animationFrameId = null;

// --- RENDERING LOGIC ---

/**
 * Huvudfunktion för att rendera texten. Denna funktion är designad för att vara
 * säker att anropa flera gånger (idempotent).
 */
const renderCanvasContent = () => {
  // Avbryt eventuell pågående renderingsloop för att förhindra race conditions
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }

  // Använd requestAnimationFrame för att synka med webbläsarens renderingscykel
  animationFrameId = requestAnimationFrame(() => {
    const canvas = canvasRef.value;
    const container = containerRef.value;
    if (!canvas || !container) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    // Hämta stilvärden från CSS Custom Properties
    const styles = getComputedStyle(document.documentElement);
    const fontColor = styles.getPropertyValue('--color-text-medium-emphasis').trim();
    const fontFamily = styles.getPropertyValue('--font-family-monospace').trim();
    const fontSize = 14;
    const lineHeight = fontSize * 1.6;
    const padding = 20;

    // Sätt canvasens bredd baserat på containern
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    
    // Nollställ eventuella tidigare transformationer
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);

    // Sätt textstilar
    ctx.font = `${fontSize}px ${fontFamily}`;
    ctx.fillStyle = fontColor;
    ctx.textBaseline = 'top';

    // --- Textbrytningslogik ---
    const lines = [];
    const paragraphs = props.text.split('\n');
    paragraphs.forEach(paragraph => {
      const words = paragraph.split(' ');
      let currentLine = words[0] || '';

      for (let i = 1; i < words.length; i++) {
        const word = words[i];
        const width = ctx.measureText(currentLine + ' ' + word).width;
        if (width < rect.width - (padding * 2)) {
          currentLine += ' ' + word;
        } else {
          lines.push(currentLine);
          currentLine = word;
        }
      }
      lines.push(currentLine);
    });

    // --- Slutgiltig Rendering ---
    // Beräkna den totala höjden som texten kommer att uppta
    const totalHeight = lines.length * lineHeight + (padding * 2);
    canvas.height = totalHeight * dpr; // Justera canvas-höjden
    
    // Skala om igen efter höjdjustering
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
    
    // Applicera stilar på nytt (viktigt efter setTransform)
    ctx.font = `${fontSize}px ${fontFamily}`;
    ctx.fillStyle = fontColor;
    ctx.textBaseline = 'top';
    
    // Rensa hela canvasen inför ny utritning
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Rita ut varje rad
    lines.forEach((line, index) => {
      ctx.fillText(line, padding, padding + (index * lineHeight));
    });
  });
};

// --- LIFECYCLE & WATCHERS ---
const resizeObserver = new ResizeObserver(() => {
    renderCanvasContent();
});

onMounted(() => {
  renderCanvasContent();
  if (containerRef.value) {
    resizeObserver.observe(containerRef.value);
  }
});

onBeforeUnmount(() => {
  if (containerRef.value) {
    resizeObserver.unobserve(containerRef.value);
  }
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
});

// Se till att rendera om när texten eller temat ändras
watch(() => props.text, renderCanvasContent);
watch(() => themeStore.isDarkTheme, () => {
  // Liten fördröjning för att säkerställa att CSS-variablerna har uppdaterats
  setTimeout(renderCanvasContent, 50);
});

</script>

<style scoped>
.canvas-viewer-container {
  width: 100%;
  height: 100%;
  overflow-y: auto; /* Gör innehållet (den dynamiskt storleksändrade canvasen) scrollbart */
  background-color: var(--color-surface-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
}

canvas {
  display: block;
  /* Canvasens faktiska bredd och höjd sätts via JS för DPI-skalning, */
  /* men CSS-bredden säkerställer att den fyller sin container. */
  width: 100%; 
}
</style>
// src/shared/ui/BaseCanvasTextViewer.vue
