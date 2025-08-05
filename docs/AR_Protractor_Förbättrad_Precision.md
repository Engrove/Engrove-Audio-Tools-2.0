# docs/AR_Protractor_Förbättrad_Precision.md
#
# === SYFTE & ANSVAR ===
# Detta dokument utforskar och specificerar potentiella förbättringar för att utöka
# precisionen och robustheten i AR Protractor-systemets spårningsförmåga. Det fokuserar
# på mer avancerade markörsystem och förbättrade kalibreringsmetoder.
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

# Förbättringar för Utökad Precision i AR-Spårning

Den befintliga implementeringen av "Engrove Audio Toolkit – AR Protractor" använder en robust metodik baserad på fiducial markers och kamerakalibrering via `AR.js` och `OpenCV.js`. För att ytterligare höja precisionen och robustheten kan följande områden utforskas:

## 1. Mer Robusta Fiducial Markers (`AprilTags` / `ArUco`)

### Översikt:
Fiducial markers är visuella mönster som systemet kan detektera för att bestämma sin position och orientering. Medan `AR.js` (baserad på `ARToolKit`) erbjuder en funktionell lösning, finns det nyare generationens markörsystem som `AprilTags` och `ArUco` som är designade för förbättrad robusthet.

### Teknisk Förklaring och Fördelar:

**`AprilTags`:** Utvecklade vid University of Michigan, är `AprilTags` kända för sin förmåga att motstå bildförvrängning, ocklusion och variationer i belysning.

**`ArUco` Markers:** Dessa markörer är en del av `OpenCV`-biblioteket. De är optimerade för snabb detektion och robusthet, särskilt i scenarier där flera markörer är närvarande.

Båda dessa system använder mer avancerade algoritmer än äldre `ARToolKit`-markörer, vilket kan leda till:
*   **Minskad "Jitter":** Stabilare 3D-positionering.
*   **Ökad Detektionshastighet:** Snabbare igenkänning i realtid.
*   **Bättre prestanda under svåra förhållanden:** Robusthet mot dålig belysning och skuggor.

### Implementeringsöverväganden:
Eftersom `OpenCV.js` redan är integrerat skulle en övergång till `ArUco`-markörer vara den mest naturliga vägen. Detta skulle innebära att man ersätter `AR.js`:s inbyggda detektion med en anpassad implementering som använder `OpenCV.js`:s `ArUco`-modul.

## 2. Förbättrad Kamerakalibrering och Förvrängningskorrigering

### Översikt:
Kamerakalibrering är en kritisk process som beräknar en kameras inre parametrar och linsförvrängning. Den befintliga modulen baserad på `OpenCV.js` och ett schackbräde är en standardiserad och effektiv metod.

### Teknisk Förklaring och Fördelar:
En kameras lins introducerar alltid en viss grad av optisk förvrängning. Utan korrekt kompensation blir 3D-mätningar felaktiga. Kalibreringsprocessen skapar en matematisk modell av denna förvrängning.

För att optimera kalibreringens noggrannhet:

*   **Utökad Bildinsamling:** Att samla in ett större antal kalibreringsbilder (20-30+) från ett brett spektrum av vinklar och avstånd är avgörande.
*   **Exakt Fysisk Rutstorlek:** Precisionen i 3D-mätningarna är direkt proportionell mot hur exakt den fysiska storleken på schackbrädets rutor (i millimeter) matas in i verktyget.
*   **Individuell Enhetskalibrering:** Varje specifik kamera/lins-kombination bör kalibreras individuellt för att uppnå högsta möjliga precision.
