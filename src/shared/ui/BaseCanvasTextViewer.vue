// src/shared/ui/BaseCanvasTextViewer.vue
// Denna komponent är en återanvändbar, generell textvisare som renderar
// en given textsträng på ett HTML <canvas>-element. Den hanterar
// automatisk radbrytning och hämtar stilinformation (färg, typsnitt)
// från de globala design-tokens för att säkerställa visuell konsekvens.

<template>
<div class="canvas-viewer-container">
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
const themeStore = useThemeStore();

// --- RENDERING LOGIC ---

/**
* Huvudfunktion för att rendera texten på canvasen.
* Denna funktion orkestrerar hela processen från att hämta kontext
* till att rita ut den radbrutna texten.
*/
const renderCanvasContent = () => {
const canvas = canvasRef.value;
if (!canvas) return;

const ctx = canvas.getContext('2d');
const dpr = window.devicePixelRatio || 1;

// Hämta stilvärden från CSS-variabler för att säkerställa designkonsekvens
const styles = getComputedStyle(document.documentElement);
const fontColor = styles.getPropertyValue('--color-text-medium-emphasis').trim();
const fontFamily = styles.getPropertyValue('--font-family-monospace').trim();
const fontSize = 14; // Fast storlek för läsbarhet i detta sammanhang
const lineHeight = fontSize * 1.6;

// Skala canvas för hög-DPI skärmar (t.ex. Retina) för skarp text
const rect = canvas.parentElement.getBoundingClientRect();
canvas.width = rect.width * dpr;
canvas.height = rect.height * dpr; // Starta med förälderns höjd, justeras sen
ctx.scale(dpr, dpr);

// Sätt typsnitt och färg för texten
ctx.font = `${fontSize}px ${fontFamily}`;
ctx.fillStyle = fontColor;
ctx.textBaseline = 'top';

// Rensa canvas inför ny rendering
ctx.clearRect(0, 0, canvas.width, canvas.height);

// Anropa funktionen som bryter och ritar texten
wrapAndRenderText(ctx, props.text, 20, 20, rect.width - 40, lineHeight);
};

/**
* Bryter en lång textsträng till flera rader och ritar dem på canvasen.
* @param {CanvasRenderingContext2D} context - Canvasens 2D-kontext.
* @param {string} text - Texten som ska ritas.
* @param {number} x - Startposition på X-axeln.
* @param {number} y - Startposition på Y-axeln.
* @param {number} maxWidth - Maximal bredd en rad får ha innan den bryts.
* @param {number} lineHeight - Höjden på varje rad (radavstånd).
*/
const wrapAndRenderText = (context, text, x, y, maxWidth, lineHeight) => {
const paragraphs = text.split('\n'); // Hantera manuella radbrytningar
let currentY = y;
let totalHeight = 0;

paragraphs.forEach(paragraph => {
const words = paragraph.split(' ');
let line = '';

for (let n = 0; n < words.length; n++) {
const testLine = line + words[n] + ' ';
const metrics = context.measureText(testLine);
const testWidth = metrics.width;

if (testWidth > maxWidth && n > 0) {
context.fillText(line, x, currentY);
line = words[n] + ' ';
currentY += lineHeight;
} else {
line = testLine;
}
}
context.fillText(line, x, currentY);
currentY += lineHeight;
});

// Beräkna den totala höjden som texten upptar
totalHeight = currentY;

// Justera canvasens faktiska höjd för att rymma all text.
// Detta möjliggör att förälder-diven kan scrolla innehållet.
const canvas = context.canvas;
const dpr = window.devicePixelRatio || 1;
canvas.height = totalHeight * dpr;

// Skala om och rita om allt på den nyskalade canvasen
context.scale(dpr, dpr);
context.font = `${fontSize}px ${fontFamily}`;
context.fillStyle = fontColor;
context.textBaseline = 'top';
wrapAndRenderText(context, text, x, y, maxWidth, lineHeight); // Anropa rekursivt för att rita på den nya storleken
};


// --- LIFECYCLE & WATCHERS ---

// När komponenten har monterats, gör en första rendering.
onMounted(() => {
renderCanvasContent();
});

// Om text-propen ändras, rendera om canvasen.
watch(() => props.text, () => {
renderCanvasContent();
});

// Om temat ändras, rendera om canvasen för att hämta nya färg-tokens.
watch(() => themeStore.isDarkTheme, () => {
// Vänta en kort stund för att CSS-variablerna ska hinna uppdateras i DOM.
setTimeout(renderCanvasContent, 50);
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
padding: 0;
}

canvas {
display: block;
width: 100%;
}
</style>


// src/shared/ui/BaseCanvasTextViewer.vue
