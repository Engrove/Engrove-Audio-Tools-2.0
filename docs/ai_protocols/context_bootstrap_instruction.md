# context_bootstrap_instruction.md

## Fristående klartext-instruktion för sessionsstart med bifogad JSON-kontext

### 1. Syfte
Den bifogade `.json`-filen innehåller **hela sessionskontexten**, inklusive:
- AI-protokoll som definierar arbetsprocess, regler och artefaktformat.
- Inbäddade dokument och filer som är relevanta för uppdraget.
- Metadata och instruktioner för hur denna session ska köras.

### 2. Krav vid start
1. Läs **hela** den bifogade `.json`-filen innan du försöker svara på några frågor.  
2. Tolka varje inbäddad fil (nycklar med filnamn som `docs/...` eller `src/...`) som om filen hade laddats upp separat.  
3. Tolka även rena textnycklar (`ai_instructions_input`, `context_description` etc.) som direkt instruktion.  
4. **Ingen del av kontexten får hoppas över.**  
5. Kombinera alla dessa delar till en **samlad arbetskontext** som styr hur sessionen ska genomföras.

### 3. Handlingsprotokoll vid mottagande
- **Steg 1:** Ladda och tolka `.json`.
- **Steg 2:** Bekräfta att alla nycklar och inbäddade dokument är lästa och förstådda.
- **Steg 3:** Lista explicit vilka protokoll och regler som kommer att följas.
- **Steg 4:** Begär omedelbart eventuell saknad fil eller bristfällig kontext istället för att anta eller hallucinera.
- **Steg 5:** Börja utföra uppgiften med `.json`-filens innehåll som primär källa, utan att anta annan tidigare kunskap.

### 4. Viktig regel
Om instruktionerna i `.json`-filen innehåller protokoll (t.ex. avslutningsprotokoll, AI-protokoll, intern testprocess) **måste dessa följas ordagrant**. Vid konflikt mellan interna standardrutiner och bifogad `.json` gäller alltid `.json`-filens innehåll.
