<!-- src/shared/ui/BaseCanvasTextViewer.vue -->
<!-- Denna komponent är en återanvändbar, generell textvisare som renderar -->
<!-- en given textsträng på ett HTML <canvas>-element. Den hanterar -->
<!-- automatisk radbrytning och hämtar stilinformation (färg, typsnitt) -->
<!-- från de globala design-tokens för att säkerställa visuell konsekvens. -->

<template>
  <div class="canvas-viewer-container" ref="containerRef">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
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

// --- RENDERING LOGIC ---

/**
 * Bryter en lång textsträng till en array av rader baserat på en maximal bredd.
 * Hanterar även manuella radbrytningar (`\n`).
 * @param {CanvasRenderingContext2D} ctx - Canvasens 2D-kontext.
 * @param {string} text - Texten som ska brytas.
 * @param {number} maxWidth - Maximal bredd en rad får ha.
 * @returns {Array<string>} En array av textrader.
 */
const getWrappedLines = (ctx, text, maxWidth) => {
  const lines = [];
  const paragraphs = text.split('\n'); // Splitta på manuella radbrytningar

  paragraphs.forEach(paragraph => {
    if (paragraph.trim() === '') {
      lines.push(''); // Behåll tomma rader som avstånd mellan paragrafer
      return;
    }

    const words = paragraph.split(' ');
    let currentLine = words[0];

    for (let i = 1; i < words.length; i++) {
      const word = words[i];
      const testLine = currentLine + ' ' + word;
      const metrics = ctx.measureText(testLine);
      const testWidth = metrics.width;

      // Om testlinjen blir för bred, pusha den aktuella raden och starta en ny
      if (testWidth > maxWidth && i > 0) {
        lines.push(currentLine);
        currentLine = word;
      } else {
        currentLine = testLine;
      }
    }
    lines.push(currentLine); // Lägg till den sista raden i varje paragraf
  });
  return lines;
};

/**
 * Huvudfunktion för att rendera texten på canvasen.
 * Denna funktion initierar canvas och dess kontext, beräknar textlayout,
 * justerar canvasens dimensioner dynamiskt och ritar sedan ut texten.
 */
const renderCanvasContent = () => {
  const canvas = canvasRef.value;
  const container = containerRef.value;
  if (!canvas || !container) {
    return; // Säkerställ att elementen finns
  }

  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1; // Hämta enhetens pixelratio för skärpa

  // Hämta stilvärden från CSS-variabler (design-tokens)
  const styles = getComputedStyle(document.documentElement);
  const fontColor = styles.getPropertyValue('--color-text-medium-emphasis').trim();
  const fontFamily = styles.getPropertyValue('--font-family-monospace').trim();
  const fontSize = 14; // Definierad fontstorlek för licenstext
  const lineHeight = fontSize * 1.6; // Radavstånd baserat på fontstorlek

  // --- 1. Konfigurera canvasens interna dimensioner och skala för DPI ---
  // Rätt bredd för canvasen, baserad på förälder-containerns faktiska bredd
  const containerWidth = container.clientWidth;
  const paddingX = 20; // Padding på sidorna av texten
  const drawableWidth = containerWidth - (2 * paddingX);

  canvas.width = containerWidth * dpr; // Sätt canvasens interna pixelbredd
  canvas.style.width = `${containerWidth}px`; // Sätt canvasens visuella bredd
  
  ctx.scale(dpr, dpr); // Skala kontexten för att rita med logiska pixlar

  // --- 2. Sätt textstil för beräkningar och rendering ---
  ctx.font = `${fontSize}px ${fontFamily}`;
  ctx.fillStyle = fontColor;
  ctx.textBaseline = 'top'; // Justera textens baslinje för enklare Y-positionering

  // --- 3. Beräkna radbrytningar och total höjd ---
  const lines = getWrappedLines(ctx, props.text, drawableWidth);
  const totalTextHeight = lines.length * lineHeight;
  const paddingY = 20; // Padding upptill och nedtill
  const requiredCanvasHeight = totalTextHeight + (2 * paddingY);

  // --- 4. Justera canvasens höjd dynamiskt ---
  // Sätt canvasens interna pixelhöjd och visuella höjd
  canvas.height = requiredCanvasHeight * dpr;
  canvas.style.height = `${requiredCanvasHeight}px`;

  // --- 5. Rensa och rita ut all text ---
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Rensa hela canvasen

  // Rita ut varje rad
  lines.forEach((line, index) => {
    ctx.fillText(line, paddingX, paddingY + index * lineHeight);
  });
};

// --- LIFECYCLE HOOKS & WATCHERS ---

// Vid montering: Rendera innehållet och lägg till resize-lyssnare
onMounted(() => {
  renderCanvasContent();
  window.addEventListener('resize', renderCanvasContent);
});

// Vid uppdatering av textprop: Rendera om innehållet
watch(() => props.text, renderCanvasContent);

// Vid temabyte: Vänta på att CSS-variabler uppdateras och rendera sedan om
watch(() => themeStore.isDarkTheme, () => {
  nextTick(() => { // Säkerställ att DOM har uppdaterats med de nya CSS-variablerna
    renderCanvasContent();
  });
});
</script>

<style scoped>
.canvas-viewer-container {
  width: 100%;
  height: 100%; /* Tar upp all tillgänglig höjd från sin förälder */
  overflow-y: auto; /* Gör innehållet (canvasen) scrollbart */
  background-color: var(--color-surface-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
}

canvas {
  display: block; /* Tar bort extra marginaler under canvas */
}
</style>
<!-- src/shared/ui/BaseCanvasTextViewer.vue -->
