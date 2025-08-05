# docs/AR_Protractor_Teknisk_Dokumentation.md
#
# === SYFTE & ANSVAR ===
# Detta dokument är den huvudsakliga tekniska specifikationen för AR Protractor-modulen.
# Det täcker allt från den övergripande arkitekturen och de tekniska valen till detaljerade
# kodexempel för kärnfunktionalitet som kamerakalibrering och markördetektion.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-05): Initial skapelse. Sammanslagen och rekonstruerad från flera
#   korrupta OCR-bilder till en enhetlig, strukturerad Markdown-fil.
#
# === TILLÄMPADE REGLER (Frankensteen v3.7) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har rekonstruerats och konverterats.

# Teknisk Dokumentation: Engrove Audio Toolkit – AR Protractor
Version: 3.2
Datum: 2025-07-28

---

## 1. Introduktion

Engrove Audio Toolkit – AR Protractor är en banbrytande webbaserad applikation designad för att revolutionera precisionsjustering av skivspelare. Genom att utnyttja Augmented Reality (AR) direkt i webbläsaren adresserar verktyget ett av de mest kända och utmanande problemen inom hifi-hobbyn: att uppnå en matematiskt korrekt och verifierbar inställning av en tonarms pickup-geometri.

### Syfte:
Denna modul tillhandahåller en komplett svit av verktyg för realtidsmätning och visualisering av både statisk geometri och dynamisk prestanda. Målet är att eliminera gissningar och mänskliga felkällor (som parallaxfel) som är vanliga med traditionella, fysiska justeringsmallar.

### Målgrupp:
Tekniskt kunniga audiofiler, hifi-tekniker, utvecklare och DIY-entusiaster som söker högsta möjliga precision och objektiv verifiering av sina justeringar.

### Kärnfilosofi i AR-kontexten:
*   **Precision:** Manifesteras genom realtidsdata som presenteras med flera decimalers noggrannhet.
*   **Tydlighet:** Uppnås genom en minimalistisk och kontextkänslig HUD som presenterar kritisk information omedelbart läsbar.
*   **Förtroende:** Byggs genom transparens i mätdata (inklusive explicita felmarginaler och konfidensscore).

## 2. Systemarkitektur & Teknisk Stack

AR-modulen är en integrerad del av Engrove Audio Toolkit v2.0, som är en helt fristående lösning som körs direkt i en modern webbläsare.

**Kärnbibliotek för AR-funktionalitet:**
*   `Three.js`: För att skapa och rendera all visuell AR-feedback.
*   `AR.js` (ARToolKit Port): För att i realtid detektera och spåra position och rotation av de fysiska AR-markörerna.
*   `OpenCV.js`: För den avancerade engångsprocessen att kalibrera kamerans linsgeometri.

## 3. AR-Koncept och Funktionalitet

AR-modulen överlagrar virtuella 3D-modeller och information på en live-videoström från användarens kamera.

**Huvudsyfte: Realtidsanalys av Tonarmsgeometri och Prestanda:**
*   **Statisk Geometri:** Spindle-to-Pivot (S2P) Avstånd, Effektiv Tonarmslängd, Överhängsfel, Vinkelfel (Zenith), Offsetvinkel.
*   **Dynamisk Prestanda (Live Monitor):** Kontinuerlig realtidsövervakning av rotationshastighet (RPM), hastighetsvariationer (Wow & Flutter).

## 4. AR-Komponenter (Markörer)

AR-modulen förlitar sig på en samling av fyra specialdesignade fiducial markers.

**Specifikationer för Markörer:**
1.  **Markör 1:** 100mm Scale & Stability Anchor (`anchor_marker.png`)
2.  **Markör 2:** Turntable Spindle Center (Origin) (`spindle_marker.png`)
3.  **Markör 3:** Tonearm Pivot Point (`pivot_marker.png`)
4.  **Markör 4:** Multifunctional Stylus & Target Marker (`stylus_marker.png`)

## 5. AR-Guidat Justeringsflöde (3 Steg)

Systemet guidar användaren genom en logisk trestegsprocess för en komplett geometrisk inställning.
*   **Steg 1:** Överhäng & Nollpunktsinställning
*   **Steg 2:** Justering av Offsetvinkel
*   **Steg 3:** Dynamisk Verifiering (Valfri Slutkontroll)

## 6. Dynamisk Prestanda-Monitor (Live Mätning)

För att analysera skivspelarens prestanda under uppspelning erbjuder verktyget två lägen:
*   **Metod D:** Fullständig Realtidsanalys (PC/Desktop)
*   **Metod E:** Snapshot-Analys (Mobiltelefon)

## 7. Kamerakalibrering för Högprecision

En noggrann kamerakalibrering är den absolut viktigaste förutsättningen för att uppnå de millimeternivåmätningar som verktyget utlovar.

### 7.1 Teoretisk grund

Kalibreringsprocessen beräknar koefficienterna för radiell och tangentiell förvrängning samt kamerans intrinsiska matris (brännvidd och optisk mittpunkt).

### 7.2 Implementering av kalibreringsflödet med `OpenCV.js`

Användaren guidas genom en engångsprocess för att kalibrera sin enhets kamera.

1.  **Förberedelser:** Användaren skriver ut ett schackbräde med kända dimensioner.
2.  **Datainsamling:** Applikationen instruerar användaren att ta 20-30 bilder av schackbrädet från olika vinklar.
3.  **Hörn-detektion:** För varje bild anropas `cv.findChessboardCorners()`.
4.  **Beräkning:** `cv.calibrateCamera()` anropas med de insamlade punkterna.

```javascript
// ... (logik för att fylla objectPoints och imagePoints) ...

try {
  // Huvudanrop för kalibrering
  const reprojectionError = cv.calibrateCamera(
    objectPoints,
    imagePoints,
    imageSize,
    cameraMatrix,
    distCoeffs,
    rvecs,
    tvecs,
    cv.CALIB_FIX_ASPECT_RATIO
  );
  // ... (hantera resultat) ...
} catch (error) {
  console.error("Kunde inte initiera applikationen:", error);
  // Visa felmeddelande för användaren
}

## 8. Användargränssnitt (HUD) och Visualisering

**Design:**  
- Hög kontrast för läsbarhet.  
- Realtidsfeedback med visuella hjälpmedel (bågar, rutnät).  
- Felmarginaler och konfidensscore visas.  

---

## 9. Utmaningar och Framtida Överväganden

**Utmaningar:**  
- Precision i WebAR.  
- Nålspetsdetektion via bildanalys är opraktiskt.  

**Framtida Teknik:**  
- Migrering till WebXR Device API för högre precision.  
