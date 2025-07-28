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
import { ref, onMounted, watch } from 'vue';
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

// --- STATE ---
let animationFrameId = null; // För att hantera omritning vid storleksändring

// --- RENDERING LOGIC ---

/**
 * Bryter en lång textsträng till en array av rader.
 * @param {CanvasRenderingContext2D} context - Canvasens 2D-kontext.
 * @param {string} text - Texten som ska brytas.
 * @param {number} maxWidth - Maximal bredd en rad får ha.
 * @returns {Array} En array av textrader.
 */
const wrapText = (context, text, maxWidth) => {
  const lines = [];
  const paragraphs = text.split('\n');

  paragraphs.forEach(paragraph => {
    if (paragraph === '') {
      lines.push(''); // Behåll tomma rader mellan paragrafer
    } else {
      const words = paragraph.split(' ');
      let currentLine = words[0];

      for (let i = 1; i < words.length; i++) {
        const word = words[i];
        const width = context.measureText(currentLine + ' ' + word).width;
        if (width < maxWidth) {
          currentLine += ' ' + word;
        } else {
          lines.push(currentLine);
          currentLine = word;
        }
      }
      lines.push(currentLine);
    }
  });
  return lines;
};


/**
 * Huvudfunktion för att rendera texten på canvasen.
 */
const renderCanvasContent = () => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }

  animationFrameId = requestAnimationFrame(() => {
    const canvas = canvasRef.value;
    const container = containerRef.value;
    if (!canvas || !container) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    // Hämta stilvärden från CSS-variabler
    const styles = getComputedStyle(document.documentElement);
    const fontColor = styles.getPropertyValue('--color-text-medium-emphasis').trim();
    const fontFamily = styles.getPropertyValue('--font-family-monospace').trim();
    const fontSize = 14;
    const lineHeight = fontSize * 1.6;

    // Sätt canvasens dimensioner baserat på containern och DPI
    const rect = container.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    ctx.scale(dpr, dpr);
    
    // Sätt textstil
    ctx.font = `${fontSize}px ${fontFamily}`;
    
    // Bryt texten till rader
    const lines = wrapText(ctx, props.text, rect.width - 40);

    // Beräkna total höjd och justera canvas
    const totalHeight = lines.length * lineHeight + 40;
    canvas.height = totalHeight * dpr;

    // Skala om för den nya höjden och sätt stilarna igen
    ctx.scale(dpr, dpr);
    ctx.font = `${fontSize}px ${fontFamily}`;
    ctx.fillStyle = fontColor;
    ctx.textBaseline = 'top';
    
    // Rensa och rita texten
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    lines.forEach((line, index) => {
      ctx.fillText(line, 20, 20 + index * lineHeight);
    });
  });
};


// --- LIFECYCLE & WATCHERS ---

onMounted(() => {
  renderCanvasContent();
  window.addEventListener('resize', renderCanvasContent);
});

watch(() => props.text, renderCanvasContent);

watch(() => themeStore.isDarkTheme, () => {
  // En kort fördröjning för att låta CSS-variabler uppdateras
  setTimeout(renderCanvasContent, 50);
});

</script>

<style scoped>
.canvas-viewer-container {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background-color: var(--color-surface-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
  padding: 0;
}

canvas {
  display: block;
  width: 100%;
}
</style>
// src/shared/ui/BaseCanvasTextViewer.vue
