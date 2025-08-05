# docs/Interaktiva_Animationer_för_Verktygskort.md
#
# === SYFTE & ANSVAR ===
# Detta dokument specificerar designen och den tekniska implementationen för en
# interaktiv hover/touch-animation för verktygskorten på landningssidan.
# Det fungerar som en konkret teknisk guide för en specifik UI-förbättring.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-05): Initial skapelse. Konverterad från ett ostrukturerat textdokument
#   till en formell, strukturerad Markdown-fil.
#
# === TILLÄMPADE REGLER (Frankensteen v3.7) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och konverterats.

# Interaktiva Animationer för Verktygskort

**Projekt:** Engrove Audio Toolkit
**Funktion:** Hover- och touch-animationer för "The Toolkit"
**Datum:** 28 juli 2025

---

## 1. Målsättning

Målet var att implementera en subtil och informativ "sneak peek"-animation för verktygskorten på webbplatsen. Animationen ska aktiveras vid hover med mus på desktop och via en motsvarande interaktion på touch-enheter. Lösningen ska vara elegant, performant och i linje med varumärkets estetik av precision och kvalitet.

## 2. Vald Lösning: Vertikal Panorering med CSS

Den valda lösningen är en animerad vertikal panorering av förhandsvisningsbilden inuti varje kort. En högre bild placeras i en container med fast höjd och `overflow: hidden`. Vid interaktion (hover/touch) animeras bilden långsamt uppåt med en CSS `transform`, vilket avslöjar mer av gränssnittet på ett mjukt och elegant sätt.

**Motivering:**
*   **Visuellt tilltalande:** Skapar en subtil och professionell effekt.
*   **Lättviktigt & Performant:** Använder endast CSS och en statisk bild, vilket minimerar laddningstid och prestandapåverkan jämfört med video eller tunga GIF-animationer.
*   **Informativt:** Ger användaren en utökad förhandsvisning av verktygets funktionalitet.

## 3. Teknisk Implementation

Implementationen är uppdelad i tre delar: HTML-struktur, CSS för styling och animation, samt JavaScript för att hantera interaktion på touch-enheter.

### 3.1 HTML-struktur

Varje kort struktureras med en dedikerad container för bilden, vilket är nödvändigt för att `overflow: hidden` ska fungera korrekt.

```html
<div class="tool-card">
 <div class="tool-image-container">
   <img src="path/to/your/tall-image.jpg" alt="Tool Preview">
 </div>

 <h3>Verktygets Namn</h3>
 <p>Beskrivning av verktyget...</p>
 <a href="#" class="button">Öppna Verktyg</a>
</div>
```

### 3.2 CSS-implementation

CSS används för att skapa masken, definiera bildens startposition och animera den vid interaktion. En klass `.is-active` används för att kunna styra animationen via JavaScript.

```css
/* Container som beskär bilden */
.tool-image-container {
 height: 200px; /* Anpassningsbar höjd */
 overflow: hidden;
 border-radius: 8px;
}

/* Bilden som ska animeras */
.tool-image-container img {
 width: 100%;
 height: auto;
 /* Mjuk övergång för alla transformationer */
 transition: transform 5s ease-in-out;
}

/* Triggar animationen vid hover på desktop ELLER när .is-active klassen finns på mobilt */
.tool-card:hover .tool-image-container img,
.tool-card.is-active .tool-image-container img {
 /* Flytta bilden uppåt. Justera värdet efter bildens höjd. */
 transform: translateY(-150px);
}
```

### 3.3 Interaktivitet för Mobila Enheter (JavaScript)

Eftersom touch-enheter saknar `:hover`, används JavaScript för att skapa en "två-stegs-interaktion".
1.  **Första trycket:** Lägger till klassen `.is-active` för att starta animationen och förhindrar att länken följs.
2.  **Andra trycket (på samma kort):** Tar användaren till länken. Ett tryck utanför kortet avaktiverar animationen.

```javascript
document.addEventListener('DOMContentLoaded', () => {
 const toolCards = document.querySelectorAll('.tool-card');

 // Funktion för att avaktivera alla kort
 const deactivateAllCards = () => {
   document.querySelectorAll('.tool-card.is-active').forEach(activeCard => {
     activeCard.classList.remove('is-active');
   });
 };

 toolCards.forEach(card => {
   card.addEventListener('click', function(event) {
     const isAlreadyActive = this.classList.contains('is-active');
     
     // Om kortet är aktivt, låt klicket gå igenom (följ länk)
     if (isAlreadyActive) return;

     // Om inte, avaktivera först andra kort
     deactivateAllCards();
     
     // Förhindra navigation på första klicket och aktivera kortet
     event.preventDefault();
     this.classList.add('is-active');
   });
 });

 // Lyssna efter klick på hela dokumentet för att avaktivera
 document.addEventListener('click', function(event) {
   // Om klicket inte sker inuti ett kort, avaktivera
   if (!event.target.closest('.tool-card')) {
     deactivateAllCards();
   }
 });
});
```

## 4. Slutsats

Denna lösning uppfyller alla krav i målsättningen. Den levererar en högkvalitativ användarupplevelse på alla enheter genom en kombination av effektiv CSS och smart, standardiserad JavaScript-logik för touch-interaktion.

**Status:** Rekommenderad för implementering.
