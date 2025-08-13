# Code Style Guide v1.0

## 1. Syfte

Detta dokument samlar specifika, icke-förhandlingsbara regler för kodstil och formatering. Syftet är att hålla `AI_Core_Instruction.md` fokuserad på övergripande process och logik, medan denna fil hanterar rent stilistiska krav.

### Historik (obligatorisk)
- Alla styrdokument, protokollfiler och kodfiler **måste** innehålla en versionshistorik i toppen av filen.
- Historiken ska vara i kronologisk ordning, äldst först, med varje post på formen:
# \* vX.Y (YYYY-MM-DD): Kort beskrivning av ändring.
- Historiken **får aldrig** tas bort eller rensas; endast nya poster får läggas till längst ner i listan.
- Om filformatet inte stöder kommentarer (t.ex. JSON) ska motsvarande historik föras i en separat dokumentationsfil med identiskt namn och tillägget `.history.md`.

## 2. Regler
### 2.1 Inledande Fil-kommentarer (f.d. Kärndirektiv #8)
Varje ny eller modifierad kodfil som levereras måste inledas med en kommentar som tydligt anger filens fullständiga sökväg. JSON filer är ett undantag. JSON filer får inte innehålla kommentarer.
Vid segmenterad leverans ska filhuvudet (filstig) ingå i Del 1:s koddel, inte i ett separat meta-block.

**Exempel (Python):**
```python
# scripts/tools/new_utility.py
#
# Denna kommentar förklarar kortfattat syftet med filen.
...
```

**Exempel (JavaScript/Vue):**
```javascript
// src/components/NewComponent.vue
//
// Denna kommentar förklarar kortfattat syftet med filen.
...
```
