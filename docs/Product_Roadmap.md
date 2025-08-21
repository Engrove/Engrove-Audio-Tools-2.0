# Produktvision & Roadmap: Engrove Audio Tools

**Dokumentversion:** 1.0
**Datum:** 2025-08-21

## 1. Produktvision

**Att skapa det definitiva, datadrivna och community-förankrade verktyget för "overthinkers" inom Hi-Fi.**

Engrove Audio Tools ska vara den självklara destinationen för tekniskt orienterade audiofiler och DIY-entusiaster som vill gå bortom subjektiva åsikter och istället fatta beslut baserade på data, beräkningar och väldokumenterade principer. Vi ersätter osäkerhet med precision.

## 2. Målgrupp

Vår primära målgrupp är de passionerade och kunskapstörstande medlemmarna i online-communities som **Lenco Heaven** och **DiyAudio**.

*   **Arketyp:** "The Analyzer". En person som inte nöjer sig med att något låter "bra", utan vill förstå *varför* det låter bra. De värdesätter teknisk data, exakta beräkningar (t.ex. tonarmsgeometri) och möjligheten att jämföra komponenter objektivt.
*   **Behov:** De behöver ett centraliserat, tillförlitligt och lättanvänt verktyg som samlar den fragmenterade kunskap som idag är utspridd över forumtrådar, datablad och personliga kalkylark.

## 3. Kärnfunktionalitet (MVP & Framåt)

Kärnan i EAT är att tillhandahålla en svit av specialiserade "miniverktyg" byggda på en gemensam, högkvalitativ databas.

*   **Databasen:** En berikad och ständigt växande databas över pickuper och tonarmar.
*   **Data Explorer:** Ett gränssnitt för att söka, filtrera och jämföra produkter i databasen. Detta är det primära verktyget i nuvarande utvecklingsfas.
*   **Kalkylatorer & Verktyg:** Interaktiva verktyg som utnyttjar databasen, t.ex. för att beräkna tonarmsgeometri, pickup/tonarm-resonans och impedansmatchning.

## 4. Fasindelad Roadmap

Projektet utvecklas i tre tydliga, överlappande faser.

### **Fas 1: Grundinfrastruktur & AI-Samarbete (Nuvarande Fokus)**
*   **Mål:** Slutföra och stabilisera **Frankensteen-systemet** och **AI Context Builder** (`index2.html`).
*   **Varför:** En effektiv AI-pipeline är en förutsättning för att kunna bygga och underhålla den komplexa huvudapplikationen på ett snabbt och tillförlitligt sätt.
*   **Klart när:** AI Context Builder är fullt funktionell, inklusive RAG-sökning och manifest-hantering, och CI/CD-pipelinen är stabil.

### **Fas 2: Data Explorer MVP**
*   **Mål:** Återuppta utvecklingen av Vue-appen (`data-explorer`) och nå paritet med de centrala funktionerna i konceptsajten `engrove.pages.dev`.
*   **Nyckelfunktioner:**
    1.  Robust sökning och filtrering av databasen.
    2.  Detaljerad vy för enskilda produkter.
    3.  "Jämför"-funktion för 2+ produkter.
    4.  Integration av den första kalkylatorn (t.ex. resonansberäkning).
*   **Klart när:** `engrove-audio.pages.dev` kan ersättas av den nya applikationen.

### **Fas 3: Expansion & Nya Verktyg**
*   **Mål:** Utöka verktygslådan med ny, avancerad funktionalitet baserad på feedback och visionen från `engrove.pages.dev`.
*   **Potentiella Funktioner:**
    *   AR Protractor (det ursprungliga "wow-faktor"-konceptet).
    *   Fler och mer avancerade kalkylatorer.
    *   Community-bidrag till databasen.
    *   Visualisering av data.
