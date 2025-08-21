# Teststrategi: Engrove Audio Tools

**Dokumentversion:** 1.0
**Datum:** 2025-08-21

## SYFTE & ANSVAR
Detta dokument definierar den pragmatiska teststrategin för EAT-projektet. Det beskriver vilka typer av tester som ska användas, var de ska placeras i FSD-arkitekturen, och hur de integreras i CI/CD-pipelinen. Målet är att säkerställa hög kodkvalitet och stabilitet med en rimlig arbetsinsats.

## 1. Filosofi

Vår teststrategi är **pragmatisk och värdedriven**. Målet är inte 100% kodtäckning, utan att med rimlig ansträngning säkerställa att de mest kritiska delarna av applikationen fungerar korrekt och förblir stabila över tid. Vi prioriterar tester för:

1.  **Komplex affärslogik:** (t.ex. beräkningar, state management).
2.  **Återanvändbara UI-komponenter:** (t.ex. knappar, input-fält).
3.  **Kritiska användarflöden:** (t.ex. sök -> val -> jämförelse).

Vi använder **Vitest** för enhets- och komponenttester och **Cypress** för E2E-tester.

## 2. Testtyper & Placering (FSD)

Testerna organiseras enligt FSD-principerna och samlokaliseras med koden de testar.

### **2.1 Enhetstester (Unit Tests)**
*   **Verktyg:** Vitest
*   **Syfte:** Testa isolerade funktioner och logik utan beroenden till UI eller externa system.
*   **Fokusområden:**
    *   **Pinia Stores:** Testa actions, mutations och getters. Särskilt viktig för att verifiera komplex state-logic.
        *   *Placering:* `src/entities/{entity}/model/{storeName}.spec.ts`
    *   **Shared Libraries/Utilities:** Testa rena funktioner.
        *   *Placering:* `src/shared/lib/{funktion}.spec.ts`
*   **Exempel:** Ett test för en Pinia-action som verifierar att state uppdateras korrekt när en ny låt väljs.

### **2.2 Komponenttester (Component Tests)**
*   **Verktyg:** Vitest + Vue Test Utils
*   **Syfte:** Testa enskilda Vue-komponenter i isolation.
*   **Fokusområden:**
    *   **Props & Events:** Verifiera att komponenten renderar korrekt baserat på inkommande props och att den skickar ut korrekta events vid användarinteraktion.
    *   **Slots:** Säkerställa att slots renderas som förväntat.
    *   **Grundläggande UI-logik:** Testa villkorlig rendering (`v-if`) och loopar (`v-for`).
*   **Placering:** Testfilen ligger i samma mapp som komponenten.
    *   *Exempel:* `src/shared/ui/BaseButton/BaseButton.spec.ts`

### **2.3 End-to-End-tester (E2E Tests)**
*   **Verktyg:** Cypress
*   **Syfte:** Simulera kompletta användarflöden genom hela applikationen för att verifiera att olika delar integrerar korrekt.
*   **Fokusområden:**
    *   **Kritiska användarresor:**
        1.  Starta appen -> Sök efter en pickup -> Klicka på ett resultat -> Verifiera att detaljvyn visas med rätt data.
        2.  Välj två pickuper från listan -> Klicka på "Jämför" -> Verifiera att jämförelsevyn innehåller båda.
*   **Placering:** I en dedikerad mapp på rotnivå.
    *   *Exempel:* `tests/e2e/data-explorer.cy.ts`

## 3. CI/CD-Integration

*   Enhetstester och komponenttester (`vitest run`) ska köras automatiskt som ett obligatoriskt steg i CI/CD-pipelinen innan varje build.
*   E2E-tester kan initialt köras manuellt inför större releaser, men bör på sikt också integreras i CI/CD.
