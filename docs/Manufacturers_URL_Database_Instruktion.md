# docs/Manufacturers_URL_Database_Instruktion.md
#
# === SYFTE & ANSVAR ===
# Detta dokument förklarar syftet, strukturen och den automatiska underhållsprocessen
# för filen `manufacturers.json`. Filen fungerar som en central kunskapsbas för
# verifierade, officiella URL:er för varje unik tillverkare i systemet.
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

# Dokumentation: manufacturers.json

## 1. Syfte

Filen `manufacturers.json` agerar som en central och auktoritativ kunskapsbas för skriptet `ai_[version].py`. Dess primära syfte är att lagra en verifierad, officiell URL för varje unik tillverkare av pickuper och tonarmar som finns i systemets databaser (`pickup_data.json`, `tonearm_data.json`).

Genom att underhålla denna "golden record"-lista säkerställer skriptet att AI:n, vid databerikning, alltid utgår från den mest pålitliga källan (tillverkarens officiella hemsida), vilket minimerar risken för att felaktig eller föråldrad information hämtas från mindre tillförlitliga källor som forum eller inofficiella wikis.

## 2. Struktur

Filen är en JSON-array (`[]`) där varje element är ett JSON-objekt (`{}`) som representerar en enskild tillverkare. Varje objekt har följande fält:

*   **`name` (Sträng):** Det kanoniska namnet på tillverkaren. Detta namn måste exakt matcha `manufacturer`-fältet som används i `pickup_data.json` och `tonearm_data.json` för att koppling ska kunna ske.
*   **`official_url` (Sträng | null):** Den fullständiga, verifierade URL:en till tillverkarens officiella hemsida. Värdet är `null` om URL:en ännu inte har hittats. Det kan också ha det speciella värdet `"NOT_FOUND"` om AI:n har sökt men fastställt att ingen officiell sida verkar finnas.
*   **`last_verified` (Sträng | null):** En tidsstämpel i ISO 8601-format (t.ex. `"2025-07-30T19:00:00Z"`) som anger när `official_url` senast verifierades av skriptet. `null` om den aldrig har verifierats.

### Exempel:

```json
[
  {
    "name": "Ortofon",
    "official_url": "https://www.ortofon.com/",
    "last_verified": "2025-07-30T19:01:00Z"
  },
  {
    "name": "Soundsmith",
    "official_url": null,
    "last_verified": null
  }
]
```

## 3. Automatisk Berikningsprocess

Filen är designad för att skapas och underhållas automatiskt av `ai_[version].py` genom en process som körs i början av varje körning.

1.  **Identifiering av Saknade Tillverkare:**
    *   Skriptet skannar först igenom `pickup_data.json` och `tonearm_data.json` för att skapa en komplett lista över alla unika tillverkarnamn.
    *   Denna lista jämförs mot namnen som redan finns i `manufacturers.json`.
    *   Om en tillverkare saknas, läggs den automatiskt till med `official_url` satt till `null`.

2.  **URL-Hämtning för Ofullständiga Poster:**
    *   Skriptet identifierar därefter alla poster i `manufacturers.json` där `official_url` är `null`. Dessa poster utgör en "att-göra-lista".

3.  **Specialiserat AI-Anrop:**
    *   En högt specialiserad prompt (`PROMPT_FIND_MANUFACTURER_URL`) skickas till AI:n med det enda målet: "Hitta den officiella hemsidans URL för tillverkaren X".
    *   Denna fokuserade uppgift minimerar risken för felaktiga länkar.

4.  **Uppdatering och Lagring:**
    *   När AI:n returnerar en giltig URL, uppdaterar skriptet omedelbart den relevanta posten i `manufacturers.json`.
    *   `official_url` fylls i och `last_verified`-fältet får en aktuell tidsstämpel.
    *   Hela filen sparas omedelbart.

## 4. Manuell Interaktion

Även om processen är helautomatisk, kan en användare enkelt "kickstarta" sökandet efter en ny tillverkare genom att manuellt lägga till ett nytt objekt i `manufacturers.json` med ett `null`-värde för URL:en:

```json
{
  "name": "Namnet På Ny Tillverkare",
  "official_url": null,
  "last_verified": null
}
```

Vid nästa körning kommer `ai_[version].py` automatiskt att upptäcka denna nya post och påbörja processen för att hitta den officiella URL:en.
