# Scorecard Protocol v1.0
# docs/ai_protocols/Scorecard_Protocol.md
#
# === HISTORIK ===
# * v1.0 (2025-08-14): Initial skapelse för att formalisera en objektiv och
#   verifierbar poängsättningsprocess för AI-prestanda.
#
## SYFTE & ANSVAR
Detta dokument definierar den officiella poängsättningsmatrisen (rubric) och beräkningsmetoden för `ai_protocol_performance.scorecard`-artefakten. Syftet är att ersätta subjektiva bedömningar med en strukturerad, evidensbaserad utvärdering av AI-partnerns prestation under en session.

## 1. Grundprinciper
*   **Skala:** Alla poäng (`score`) anges på en skala från **0 till 100**.
*   **Objektivitet:** Poängen ska så långt som möjligt baseras på mätbara händelser från sessionen (t.ex. antal korrigeringscykler, aktiverade protokoll).
*   **Transparens:** Den kvalitativa sammanfattningen (`aiQualitativeSummary`) ska reflektera och motivera den slutgiltiga poängen.

## 2. Poängsättningsmatris (Rubric)

| Kategori | Beskrivning (Vad mäts?) | Poängkriterier (Exempel) |
| :--- | :--- | :--- |
| **Efficacy** (Måluppfyllelse) `weight: 0.4` | Hur väl löste AI:n det definierade huvuduppdraget? | **100:** Perfekt lösning som uppfyller alla explicita och implicita krav på första försöket.<br>**75:** Lösningen är korrekt och komplett, men krävde mindre förtydliganden eller missade en nyans.<br>**50:** Uppdraget slutfördes, men krävde betydande korrigeringar eller misstolkade en central del av kravet initialt.<br>**0:** Misslyckades med att slutföra huvuduppdraget. |
| **Efficiency** (Effektivitet) `weight: 0.3` | Hur mycket ansträngning (turer, korrigeringar) krävdes för att nå målet? | **100:** Minimala interaktioner. Planen godkändes direkt och lösningen var korrekt på första leveransen.<br>**75:** Några få (`1-2`) `externalCorrections` krävdes.<br>**50:** Krävde flera (`3+`) `externalCorrections` eller en `debuggingCycle`.<br>**0:** Krävde aktivering av `Help_me_God_Protokoll` eller hamnade i en felsökningsloop (FL-D). |
| **Robustness** (Robusthet & Kvalitet) `weight: 0.3` | Hur hög var den tekniska kvaliteten på den slutgiltiga leveransen och hur väl följdes protokollen? | **100:** Koden är inte bara korrekt, utan även elegant, underhållbar, och följer alla kärndirektiv och bästa praxis utan anmärkning.<br>**75:** Lösningen är robust och säker, men har mindre skönhetsfel eller kunde ha varit mer elegant.<br>**50:** Lösningen fungerar, men bryter mot mindre viktiga direktiv (t.ex. `Obligatorisk Refaktorisering`) eller är onödigt komplex.<br>**0:** Lösningen introducerade nya buggar, bröt mot kritiska direktiv, eller ignorerade säkerhetsaspekter. |
