

# **Uppförandekoden: En djupgående analys av JSON-kodade ramverk för AI-styrning**

### 

### **Sammanfattning**

Denna rapport syftar till att leverera en definitiv analys av användningen av JSON (JavaScript Object Notation) som ett medium för att implementera och upprätthålla ramverk för AI-styrning. I takt med att artificiell intelligens integreras allt djupare i kritiska samhälls- och affärsfunktioner, blir behovet av transparenta, granskningsbara och maskinläsbara styrningsprotokoll av yttersta vikt. Rapporten undersöker övergången från traditionella, textbaserade policyer till strukturerade, beräkningsmässiga format som kan tolkas och verkställas direkt av AI-system.

De centrala slutsatserna i denna analys är mångfacetterade. För det första är JSON Schema en oumbärlig förutsättning för att använda JSON i styrningssyfte; utan ett formellt schema förblir data bräcklig och opålitlig. För det andra råder det en betydande "standardiseringslucka" – avsaknaden av ett universellt, maskinläsbart styrningsschema utgör ett hinder för interoperabilitet och effektiv tillsyn. För det tredje har framväxten av "strukturerade utdata" i moderna språkmodeller skapat ett paradigmskifte som gör det tekniskt möjligt att tvinga AI-system att följa ett definierat protokoll. Slutligen, och kanske viktigast, är kodifieringen av etik i ett maskinläsbart format inte bara en teknisk övning, utan en djupgående socio-juridisk utmaning som omdefinierar roller och maktstrukturer.

Genom en detaljerad fallstudie av ett hypotetiskt styrnings-JSON för en AI-agent som godkänner lån, utvärderar rapporten både den tekniska arkitekturen och den materiella tillräckligheten i ett sådant system. Baserat på denna analys presenteras strategiska rekommendationer för organisationer som vill implementera robust, försvarbar och automatiserad AI-styrning. Rapportens centrala tes är att även om beräkningsstyrning nu är tekniskt genomförbar, ligger den primära utmaningen i den socio-juridiska översättningen och standardiseringen av komplexa etiska principer, snarare än i tekniken i sig.

---

### **Del I: Kontrollens syntax: Att strukturera styrning i JSON**

Detta avsnitt lägger den tekniska grunden och argumenterar för att även om JSON är ett livskraftigt format, är dess användbarhet för styrning helt beroende av en rigorös tillämpning av scheman och bästa praxis. Analysen rör sig från grundläggande principer till de specifika kraven i ett styrningssammanhang.

#### **1.1 Från tvetydighet till precision: Skälen för strukturerad styrning**

Traditionella, textbaserade policydokument är till sin natur mottagliga för tvetydighet. Juridiskt och etiskt språk är ofta nyanserat och öppet för tolkning, vilket är en styrka i mänskliga sammanhang men en betydande svaghet när det gäller att instruera maskiner. Ett AI-system som styrs av enbart naturligt språk står inför samma problem som en människa som får "vägbeskrivningar i ett fullsatt rum" – instruktionerna är oklara, oprecisa och leder till inkonsekventa resultat.1 För kritiska tillämpningar inom finans, medicin eller rättsväsende är denna brist på förutsägbarhet en oacceptabel operativ och juridisk risk.

Övergången till maskinläsbara format som JSON är ett direkt svar på detta problem. Genom att organisera instruktioner som nyckel-värdepar, arrayer och objekt eliminerar JSON tvetydighet och möjliggör konsekventa resultat.1 Detta skifte från traditionella prompter till JSON-baserade instruktioner är inte bara en teknisk uppgradering; det är en fundamental förändring i hur vi kontrollerar AI. Studier har visat att AI-modeller följer instruktioner 40-60 % bättre när de presenteras i ett strukturerat format.1 Denna förbättring är inte bara en prestandamätning utan en avgörande riskreducerande faktor. När AI-system i allt högre grad hanterar reglerade data och driver automatiserade beslut blir behovet av granskningsbara, konsekventa och förutsägbara AI-handlingar en tvingande nödvändighet.2 Denna affärs- och efterlevnadslogik gör att införandet av strukturerade format som JSON för AI-kontroll inte är en fråga om

*om*, utan *när och hur*. Det minskar den "kognitiva belastningen" för AI:n genom att tillhandahålla tydliga, GPS-liknande koordinater istället för vaga vägbeskrivningar.1

#### **1.2 Regelverkets ritning: Den oumbärliga rollen för JSON Schema**

Rå JSON, i sin enklaste form, är otillräckligt för att implementera ett robust styrningsramverk. Dess flexibilitet blir en svaghet utan en formell mekanism för att upprätthålla struktur och dataintegritet. Denna mekanism är **JSON Schema**, en standard för att definiera och validera strukturen i JSON-dokument.3 JSON Schema fungerar som ett formellt kontrakt som specificerar hur styrningsdata måste se ut, vilket förvandlar en lös samling data till ett rigoröst protokoll.

Med JSON Schema kan en organisation definiera exakta regler för sitt styrningsdokument. Detta inkluderar:

* **Obligatoriska fält:** Genom att använda nyckelordet "required" säkerställs att kritiska policyparametrar, som "modelId" eller "policyOwner", alltid finns med.3  
* **Datatyper:** Nyckelordet "type" tvingar fält att ha korrekta datatyper, till exempel "integer" för numeriska tröskelvärden eller "boolean" för flaggor, vilket förhindrar felaktiga data från att tolkas felaktigt.4  
* **Värdebegränsningar:** Schemat kan specificera begränsningar som att ett numeriskt värde måste vara positivt ("minimum": 0\) eller att en sträng måste följa ett visst format (t.ex. ett e-postformat).3

Denna validering är avgörande. Den förhindrar att felaktiga eller ofullständiga policyer propagerar genom systemet och automatiserar en kontrollprocess som annars skulle vara manuell, tidskrävande och felbenägen.3 Att anamma "schemadriven utveckling" blir därmed en bästa praxis. Det innebär att JSON-schemat definieras från början och används för att säkerställa att varje komponent i AI-systemet – från datainmatning och modellträning till prediktion och utdata – följer ett konsekvent och validerat dataformat.3 Det finns en mogen ekosystem av verktyg för att generera, validera och arbeta med JSON-scheman, vilket gör detta tillvägagångssätt praktiskt genomförbart.6

#### **1.3 Att arkitektera styrning: Avancerade JSON-struktureringstekniker**

Att utforma ett JSON-baserat styrningsprotokoll kräver medvetna arkitektoniska beslut som balanserar läsbarhet, prestanda och underhållbarhet.

**Datatyper och konsistens:** En grundläggande princip är att använda lämpliga och enhetliga datatyper. Numeriska värden bör loggas som heltal eller flyttal för att möjliggöra korrekta matematiska operationer som aggregering och jämförelse. Att använda en sträng för att representera ett nummer förhindrar effektiv analys.5 Konsistens över alla fält är avgörande för att förenkla filtrering och sökning i loggar och policyer.

**Hantera komplexitet – Plattning kontra nästling:** Djupt nästlade JSON-objekt kan vara logiska för att representera hierarkiska policyer men kan bli svåra att tolka och fråga med standardsverktyg.5 En vanlig teknik för att hantera detta är "plattning", där nästlade nycklar slås samman till en enda nyckel med en avgränsare (t.ex. blir

{"user": {"name": "John"}} till {"user\_name": "John"}).5 Detta gör datan mer tillgänglig för tabellbaserade analysverktyg. Valet mellan nästling och plattning är en designavvägning. För styrningsprotokoll kan en viss grad av nästling vara nödvändig för att logiskt gruppera relaterade policyer (t.ex. alla rättviserelaterade parametrar under ett enda

fairnessMonitoring-objekt), medan plattning kan vara mer lämpligt för loggdata som genereras från protokollet.9

**Utökningsbarhet och versionering:** Ett styrningsramverk är ett levande dokument som utvecklas i takt med att tekniken, regelverken och organisationens mål förändras. Därför måste schemat utformas med framtiden i åtanke.5 Detta innebär att JSON-scheman bör behandlas som kod: de ska versionshanteras (t.ex. med Git), och alla ändringar ska dokumenteras noggrant.3 Nyckelorden

$id och $schema i JSON Schema är centrala för detta. $id ger schemat en unik URI, vilket möjliggör referenser, medan $schema anger vilken version av standarden som följs, vilket säkerställer förutsägbar tolkning över tid.4 Att inkludera ett explicit versionsnummer direkt i JSON-datan (t.ex.

"version": "1.1.0") är också en kritisk bästa praxis.

#### **1.4 Granskningsspåret: Loggning och datahantering i ett styrningssammanhang**

Ett styrnings-JSON är inte bara en statisk uppsättning regler; det är grunden för en dynamisk gransknings- och efterlevnadsprocess. Principerna för effektiv JSON-loggning är direkt tillämpliga här: loggar måste vara både mänskligt läsbara och maskinellt tolkbara för att vara användbara.5

Ett styrningsprotokoll bör specificera vad som ska loggas för att möjliggöra meningsfull granskning. Detta inkluderar inkommande förfrågningar, AI-modellens beslut, de specifika policyregler som tillämpades, eventuella felkoder och systemets tillstånd vid beslutstillfället.5 Sådana detaljerade loggar är ovärderliga vid felsökning, analys av oväntat beteende och för att kunna visa efterlevnad för tillsynsmyndigheter.

En central del av all AI-styrning är hanteringen av känslig information. Styrningsprotokollet och dess tillhörande loggningsmekanismer måste ha robusta skydd för personuppgifter och annan konfidentiell data. Detta uppnås genom flera tekniska kontroller:

* **Datamaskering:** Känsliga fält som lösenord, personnummer eller kreditkortsinformation ska maskeras innan de skrivs till en logg. Värdet ersätts med asterisker eller en hash-representation (t.ex. "password": "\*\*\*\*\*\*\*\*").5  
* **Kryptering:** Loggdata som innehåller känslig information bör krypteras, både under överföring (in transit) och vid lagring (at rest).  
* **Åtkomstkontroll:** Åtkomsten till loggar som innehåller känslig information måste vara strikt begränsad till behörig personal genom rollbaserad åtkomstkontroll (RBAC).2

Genom att integrera dessa tekniska metoder kopplas den praktiska logghanteringen direkt till de juridiska och etiska principerna om integritet och dataskydd, vilket är en hörnsten i ansvarsfull AI.

---

### **Del II: Styrningens grammatik: Kärnprinciper och internationella ramverk**

Detta avsnitt syntetiserar en universell uppsättning styrningsprinciper från ledande globala ramverk och etablerar därmed den måttstock mot vilken fallstudien i Del III kommer att mätas. Det argumenterar för att trots olika ursprung har en tydlig konsensus kring kärnprinciper vuxit fram.

#### **2.1 Pelarna för pålitlig AI: En syntes av kärnprinciper**

En granskning av de mest inflytelserika globala ramverken för AI-styrning avslöjar en anmärkningsvärd konvergens kring en uppsättning grundläggande principer. Dessa principer utgör tillsammans "grammatiken" för ansvarsfull AI och fungerar som grunden för att bygga förtroende hos användare, tillsynsmyndigheter och samhället i stort.

* **Ansvarsskyldighet och rollägarskap (Accountability & Role Ownership):** Denna princip kräver en tydlig tilldelning av ansvar för AI-systemets beslut och resultat. Det är inte tillräckligt att systemet fungerar; det måste finnas en identifierbar mänsklig eller organisatorisk enhet som är ansvarig.2 Implementeringen av detta innefattar att etablera formella AI-styrningsråd (AI Governance Boards) och att definiera roller och ansvar över juridiska, säkerhetsmässiga och tekniska team.2  
* **Transparens och förklarbarhet (Transparency & Explainability):** Systemets funktion och beslutsprocesser måste vara begripliga. Transparens innebär att det finns tydlig dokumentation om modellens utveckling, datakällor och beslutsgrunder.11 Förklarbarhet går ett steg längre och kräver förmågan att kunna förklara  
  *varför* ett visst beslut fattades, inklusive att kunna ge förklaringar på individnivå när så krävs, till exempel vid ett nekat lånebeslut.12  
* **Rättvisa och bias-hantering (Fairness & Bias Management):** AI-system måste utformas för att behandla individer och grupper på ett rättvist och opartiskt sätt. Detta kräver proaktiva åtgärder för att identifiera, mäta och mildra skadlig bias som kan uppstå från partiska träningsdata eller algoritmiska val.2 Regelbundna utvärderingar av bias är en central del av denna princip.2  
* **Motståndskraft, säkerhet och trygghet (Resilience, Safety & Security):** Systemen måste vara tekniskt robusta och säkra. De ska kunna fungera tillförlitligt under förväntade förhållanden och hantera oväntade scenarier utan att orsaka skada.11 Detta inkluderar att skydda systemen mot illvilliga attacker som modellförgiftning (model poisoning), prompt-injektioner och andra adversariella angrepp.2  
* **Integritet och ansvarsfull dataanvändning (Privacy & Responsible Data Use):** Grunden för effektiv AI-styrning är ansvarsfull datahantering. Detta innebär att följa tillämpliga dataskyddslagar som GDPR, tillämpa principer som dataminimering (att endast använda nödvändiga data) och säkerställa att modellerna tränas på högkvalitativ och relevant data.11 Anonymiseringstekniker och tydliga samtyckesprocesser är avgörande för att skydda känslig information.11

#### **2.2 Globala ritningar för AI-styrning**

Flera inflytelserika organisationer har utvecklat ramverk som ger vägledning för att implementera dessa principer. Även om de har olika fokusområden, förstärker de den globala konsensusen.

* **NIST AI Risk Management Framework (AI RMF):** Utvecklat av U.S. National Institute of Standards and Technology, är detta ramverk känt för sin praktiska och riskbaserade strategi. Det är strukturerat kring fyra kärnfunktioner: **Govern (Styra), Map (Kartlägga), Measure (Mäta) och Manage (Hantera)**.14  
  Govern är en övergripande funktion som syftar till att odla en kultur av riskhantering. Map handlar om att förstå kontexten och identifiera risker. Measure fokuserar på att analysera och spåra dessa risker, och Manage handlar om att agera på dem. Ramverket är frivilligt, icke-sektorsspecifikt och utformat för att vara anpassningsbart.18 Noterbart är att NIST har publicerat en  
  Playbook som finns tillgänglig i JSON-format, vilket är ett viktigt första steg mot ett standardiserat, maskinläsbart ramverk.20  
* **IEEE Ethically Aligned Design & P7000-standarder:** Institute of Electrical and Electronics Engineers (IEEE) har ett starkt fokus på en människocentrerad och värdebaserad design. Deras ramverk bygger på principer som mänskliga rättigheter, välbefinnande, datasuveränitet (Data Agency), transparens och ansvarsskyldighet.12 IEEE P7000-standarden är särskilt betydelsefull eftersom den erbjuder en process för att proaktivt införliva etiska värderingar i systemdesign från allra första början, istället för att bara reagera på problem i efterhand.22  
* **OECD:s principer för AI:** Organisationen for ekonomiskt samarbete och utveckling (OECD) var en av de första mellanstatliga organisationerna att anta principer för AI. Deras fem principer, som inkluderar inkluderande tillväxt, människocentrerade värderingar och robusthet, har varit mycket inflytelserika för att forma den internationella policyn och skapa en gemensam grund för medlemsländerna.11  
* **EU:s AI-förordning (principer):** Även om det är en lagstiftning snarare än ett frivilligt ramverk, bygger EU:s AI-förordning (AI Act) på samma kärnprinciper: mänskligt handlingsutrymme, teknisk robusthet, integritet, transparens och icke-diskriminering. Dess riskbaserade tillvägagångssätt, där kraven skalas efter AI-systemets potentiella risk, representerar en övergång från vägledande principer till juridiskt bindande krav och sätter en global standard.11

Den starka överlappningen mellan dessa ramverk visar att det finns en robust global konsensus om vad som utgör ansvarsfull AI. Detta gör det möjligt att syntetisera en uppsättning universella "bästa praxis"-principer som kan användas för att utvärdera vilket AI-styrningssystem som helst, oavsett dess specifika implementering.

| Tabell 1: Jämförande analys av globala ramverk för AI-styrning |  |  |  |  |  |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Ramverk** | **Kärnfokus** | **Ansvarsskyldighet** | **Transparens** | **Rättvisa** | **Tillvägagångssätt** |
| **NIST AI RMF** | Riskhantering genom hela livscykeln | Ja | Ja | Ja | Riskbaserat, Frivilligt |
| **IEEE EAD** | Människocentrerad, etisk design | Ja | Ja | Ja | Värdebaserat, Frivilligt |
| **OECD Principles** | Internationell policykonsensus | Ja | Ja | Ja | Principbaserat, Frivilligt |
| **EU AI Act** | Juridiskt bindande reglering | Ja | Ja | Ja | Riskbaserat, Lagstadgat |

---

### **Del III: Fallstudie: Att dekonstruera ett hypotetiskt AI-styrnings-JSON**

Detta är rapportens analytiska hjärta. En detaljerad, realistisk JSON-fil presenteras och utsätts sedan för en rigorös tvådelad utvärdering, vilket visar hur koncepten från Del I och II tillämpas i praktiken.

#### **3.1 Artefakten: Ett styrningsprotokoll för en AI-agent som godkänner lån**

För att konkretisera analysen presenteras här ett hypotetiskt men omfattande styrningsprotokoll i JSON-format. Protokollet är utformat för en AI-agent vars uppgift är att fatta beslut om låneansökningar. Strukturen är inspirerad av verkliga konfigurationsformat från plattformar som IBM Watson OpenScale och Collibra för att säkerställa realism och relevans.23 Filen är avsiktligt detaljerad för att kunna genomgå en meningsfull utvärdering.

**loan\_approval\_governance\_v1.2.json:**

JSON

{  
  "governanceMetadata": {  
    "policyId": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",  
    "policyVersion": "1.2.1",  
    "policyName": "AI Loan Approval Governance Protocol",  
    "policyOwner": "Chief Risk Officer",  
    "lastUpdated": "2024-08-15T10:00:00Z",  
    "scope": "Applies to AI Loan Approval Model v2.3 and subsequent minor versions."  
  },  
  "modelDetails": {  
    "modelId": "loan-approver-v2.3-prod",  
    "description": "Binary classification model to predict loan default risk.",  
    "problemType": "binary\_classification",  
    "modelCardUrl": "https://internal.examplebank.com/model-cards/loan-approver-v2.3"  
  },  
  "dataHandlingPolicy": {  
    "allowedDataSources": \["internal\_credit\_history\_db", "verified\_income\_api"\],  
    "prohibitedDataFields": \["race", "religion", "national\_origin", "gender\_identity"\],  
    "dataRetentionPeriodDays": 1825,  
    "anonymizationStandard": {  
      "method": "k-anonymity",  
      "parameters": {  
        "k\_value": 5  
      }  
    }  
  },  
  "evaluationProtocols": {  
    "fairnessMonitoring": {  
      "enabled": true,  
      "protectedAttributes": \["age\_group", "postal\_code\_area"\],  
      "fairnessMetric": "Disparate Impact",  
      "metricThreshold": 1.25,  
      "favourableOutcome": "loan\_approved",  
      "mitigationStrategy": {  
        "method": "reweighing",  
        "trigger": "on\_threshold\_breach"  
      }  
    },  
    "explainabilityConfig": {  
      "enabled": true,  
      "method": "SHAP",  
      "outputFormat": "feature\_importance\_list",  
      "userFacingExplanationRequired": true,  
      "explanationTemplateId": "expl\_template\_v3"  
    },  
    "transparencyRequirements": {  
      "decisionLog": {  
        "enabled": true,  
        "logLevel": "full",  
        "logFormat": "json"  
      },  
      "humanReviewTriggers": \[  
        {  
          "condition": "model\_confidence\_score \< 0.65",  
          "action": "flag\_for\_level1\_review"  
        },  
        {  
          "condition": "loan\_amount \> 500000",  
          "action": "flag\_for\_senior\_underwriter\_review"  
        }  
      \]  
    },  
    "robustnessAndSecurity": {  
      "dataDriftMonitoring": {  
        "enabled": true,  
        "metric": "Population Stability Index",  
        "threshold": 0.1  
      },  
      "adversarialAttackTests": {  
        "requiredTests":,  
        "frequency": "quarterly"  
      }  
    }  
  }  
}

#### **3.2 Teknisk utvärdering: Bedömning av den arkitektoniska sundheten**

En teknisk granskning av JSON-filen utvärderar dess struktur, tydlighet och underhållbarhet, baserat på principerna i Del I.

**Tydlighet och läsbarhet:** Namngivningskonventionerna (t.ex. policyId, fairnessMonitoring) är tydliga och följer en konsekvent camelCase-stil, vilket rekommenderas för att underlätta för utvecklare.25 Den logiska grupperingen av policyer under huvudobjekt som

dataHandlingPolicy och evaluationProtocols skapar en hierarki som är intuitiv och lätt att navigera. Detta är att föredra framför en platt struktur med ett stort antal fält på toppnivå, vilket kan öka förvirringen.5

**Schemaeffektivitet:** Filen använder datatyper på ett korrekt sätt. Tröskelvärden som metricThreshold och threshold är definierade som tal (number), vilket möjliggör direkta numeriska jämförelser. Flaggor som enabled är booleans (boolean), vilket är effektivt och entydigt. Detta följer bästa praxis för att säkerställa att data tolkas korrekt av analysverktyg.5 Användningen av en array för

humanReviewTriggers är också lämplig, eftersom den tillåter flera, oberoende regler att definieras på ett flexibelt sätt.9

**Skalbarhet och underhållbarhet:** Strukturen är väl lämpad för framtida utökningar. Att lägga till ett nytt övervakningsprotokoll, till exempel för energieffektivitet, skulle vara så enkelt som att lägga till ett nytt objekt (energyEfficiencyMonitoring) under evaluationProtocols utan att störa den befintliga strukturen. Den tydliga versioneringen i governanceMetadata (policyVersion) är en kritisk styrka. Den gör det möjligt att hantera ändringar över tid på ett kontrollerat sätt och säkerställer att äldre system inte bryts när nya policyer införs, vilket är en grundläggande princip för att behandla scheman som kod.3 Nästlingsdjupet är måttligt och motiverat av den logiska grupperingen, vilket undviker de prestandaproblem som kan uppstå med överdrivet komplexa, djupt nästlade objekt.5

#### **3.3 Materiell utvärdering: Mätning av efterlevnad och etisk integritet**

Denna utvärdering granskar innehållet i JSON-filen mot de etiska principerna och ramverken som definierades i Del II.

**Styrkor i konkretisering:** Protokollet är starkt där det översätter högnivåprinciper till konkreta, mätbara och automatiserbara regler. Till exempel:

* **Rättvisa:** Principen om rättvisa implementeras direkt genom fairnessMonitoring-objektet. Genom att specificera skyddade attribut (protectedAttributes), en exakt mätmetod (fairnessMetric: "Disparate Impact") och ett kvantitativt tröskelvärde (metricThreshold: 1.25), omvandlas ett abstrakt etiskt mål till en verifierbar teknisk specifikation.  
* **Ansvarsskyldighet:** governanceMetadata-objektet etablerar tydlig ansvarsskyldighet genom att definiera en policyOwner. Tillsammans med modelCardUrl i modelDetails skapas en tydlig koppling mellan protokollet och den mänskliga dokumentationen och ägarskapet.  
* **Motståndskraft:** robustnessAndSecurity-objektet specificerar konkreta krav, såsom obligatoriska tester mot adversariella attacker och övervakning av datadrift med ett definierat tröskelvärde, vilket gör principen om robusthet mätbar och granskningsbar.

**Svagheter och översättningsluckan:** Protokollets svagheter uppstår där översättningen från princip till kod blir ofullständig. Processen att omvandla en rik etisk princip som "transparens" till en begränsad uppsättning nyckel-värdepar medför oundvikligen en förlust av nyanser. JSON kan kräva att en förklaring finns ("userFacingExplanationRequired": true), men det kämpar med att koda *kvaliteten* på den förklaringen. Är den verkligen begriplig för en lekman? Är den potentiellt vilseledande? Detta illustrerar en fundamental begränsning: maskinläsbara policyer är utmärkta på att upprätthålla kvantifierbara, strukturella regler, men de har svårt att fånga kvalitativa, nyanserade krav. Denna "översättningslucka" är en primär källa till risk i beräkningsstyrning. Även om explanationTemplateId pekar på en mall, är innehållet och kvaliteten på den mallen utanför JSON-protokollets direkta kontroll. Detta visar att även med ett robust protokoll finns det ett beroende av externa, mänskligt skapade artefakter vars kvalitet inte kan garanteras av schemat självt.

| Tabell 2: AI Governance Compliance Scorecard (baserat på NIST AI RMF) |  |  |  |
| :---- | :---- | :---- | :---- |
| **RMF-funktion** | **Motsvarande JSON-objekt** | **Implementeringsstyrka (1-5)** | **Kommentar/Luckor** |
| **Govern (Styra)** | governanceMetadata | 4 | Mycket stark på ägarskap och versionering. Saknar dock en explicit koppling till en etisk granskningsnämnds stadgar eller mötesprotokoll. |
| **Map (Kartlägga)** | modelDetails, dataHandlingPolicy | 5 | Utmärkt. Definierar tydligt kontext, omfattning, datakällor och begränsningar, vilket ger en solid grund för riskidentifiering. |
| **Measure (Mäta)** | evaluationProtocols | 4 | Utmärkta kvantitativa mätvärden för rättvisa, drift och robusthet. Saknar dock mätvärden för kvalitativa aspekter som förklarbarhetens kvalitet. |
| **Manage (Hantera)** | humanReviewTriggers, mitigationStrategy | 3 | Har tydliga utlösare för riskhantering (mänsklig granskning). Svars- och åtgärdsprotokollen är dock inte detaljerade i själva JSON-filen, utan hänvisas till externt. |

Denna scorecard operationaliserar utvärderingen och omvandlar en narrativ kritik till en strukturerad bedömning mot ett respekterat branschramverk. Den ger en snabb överblick över styrningsprotokollets styrkor och svagheter och erbjuder en tydlig färdplan för förbättringar genom att belysa specifika luckor.

---

### **Del IV: Från kod till efterlevnad: Implementering och automatiserat verkställande**

Detta avsnitt utforskar den praktiska mekaniken för hur ett AI-system skulle ta emot, tolka och begränsas av styrnings-JSON, och därmed övergå från ett statiskt dokument till en dynamisk kontrollmekanism.

#### **4.1 Verkställighetsmekanismen: Att tvinga fram schemaefterlevnad**

Möjligheten att automatiskt verkställa ett JSON-baserat styrningsprotokoll vilar på moderna teknologier i stora språkmodeller (LLM). Den mest betydelsefulla av dessa är funktionen "Structured Outputs" (strukturerade utdata), som erbjuds av ledande plattformar som OpenAI och Google Vertex AI.26

Denna funktion är en avgörande utveckling från den äldre "JSON-läget". Medan JSON-läget endast garanterade att modellens utdata var syntaktiskt korrekt JSON, går Structured Outputs ett steg längre: det garanterar att utdatan följer ett specificerat **JSON Schema**.26 Detta är den kritiska tekniska möjliggöraren som gör robust beräkningsstyrning praktiskt genomförbar. Det eliminerar behovet av att manuellt validera eller göra om felaktigt formaterade svar, eftersom utdatan per definition kommer att vara kompatibel med schemat.26

Implementeringen sker vanligtvis genom att man i API-anropet inkluderar en response\_format-parameter som pekar på ett JSON Schema. Utvecklare kan definiera detta schema direkt eller använda bibliotek som Pydantic i Python eller Zod i JavaScript för att skapa schemat från kodbaserade klassdefinitioner.

Exempel med Python och Pydantic 26:

Python

from openai import OpenAI  
from pydantic import BaseModel

client \= OpenAI()

\# Definiera ett schema med Pydantic som motsvarar en del av styrningsprotokollet  
class DecisionResponse(BaseModel):  
    decision: str  
    confidence\_score: float  
    flag\_for\_review: bool

response \= client.responses.parse(  
    model="gpt-4o-2024-08-06",  
    input\=\[  
        {"role": "system", "content": "Analyze the loan application and provide a decision based on the governance protocol."},  
        {"role": "user", "content": "Application data..."},  
    \],  
    text\_format=DecisionResponse, \# Tvinga utdatan att följa schemat  
)

\# 'decision\_output' är garanterad att vara ett giltigt DecisionResponse-objekt  
decision\_output \= response.output\_parsed

Denna mekanism säkerställer att AI-systemets svar alltid är strukturerade på ett förutsägbart och validerbart sätt, vilket är grunden för automatiserad efterlevnad.

#### **4.2 Att integrera styrning i AI-livscykeln**

Styrnings-JSON är inte en engångskontroll utan en persistent kontrollmekanism som är aktiv under hela AI-systemets livscykel.

* **Modellträning:** Redan innan modellen tränas kan dataHandlingPolicy-sektionen i JSON-protokollet användas för att automatiskt filtrera träningsdata. Ett skript kan läsa prohibitedDataFields-arrayen och säkerställa att fält som "ras" eller "religion" avlägsnas från datasetet, vilket proaktivt förhindrar att modellen lär sig från otillåtna data.3  
* **Realtidsinferens:** Under drift valideras varje in- och utdata kontinuerligt mot reglerna i protokollet. När en låneansökan behandlas, loggas beslutet i enlighet med decisionLog-inställningarna. Om modellens konfidenspoäng är lägre än tröskelvärdet som anges i humanReviewTriggers (t.ex. \< 0.65), kan systemet automatiskt flagga ärendet för mänsklig granskning av en kredithandläggare. Detta skapar en omedelbar och automatiserad riskhanteringsprocess.2  
* **Kontinuerlig övervakning och granskning:** evaluationProtocols fungerar som konfigurationsfilen för automatiserade övervakningsverktyg. En separat process kan kontinuerligt analysera modellens utdata i produktion för att mäta rättvisa och datadrift mot de specificerade tröskelvärdena. Om "Disparate Impact" överstiger 1.25, kan en varning genereras och skickas till policyOwner. Detta skapar ett slutet kretslopp av policy, handling, mätning och verifiering, vilket är kärnan i ett levande styrningssystem.2

#### **4.3 Automationens gränser: Att tolka "lagens anda"**

Trots de kraftfulla möjligheterna med automatisering, kvarstår betydande utmaningar. Den "översättningslucka" som identifierades i Del III, där kvalitativa principer blir bräckliga när de kodifieras, har djupa praktiska konsekvenser. Ett automatiserat system kan verifiera att en regel följs, men det kan inte förstå den djupare avsikten – "lagens anda".

Ett exempel är hanteringen av oförutsedda indata. Om en användare matar in data som är helt oförenlig med det förväntade schemat, måste modellen ha instruktioner för hur den ska agera. Utan sådana instruktioner kan den försöka tvinga fram ett svar som passar schemat men som är helt felaktigt eller hallucinerat. Bästa praxis är att i prompten inkludera instruktioner för att hantera dessa fall, till exempel genom att returnera ett tomt objekt eller ett specifikt felmeddelande.26

Detta leder till en central iakttagelse: att automatisera efterlevnad via ett JSON-protokoll skapar nya, komplexa felscenarier som kräver mänsklig tillsyn. Systemet kan flagga att ett rättvisemått har överskridits, men det kan inte förklara *varför*. En människa behövs fortfarande för att undersöka grundorsaken – är det en förändring i indatadistributionen, ett fel i modellen eller ett problem med själva policyn? Styrnings-JSON-filen i sig är en mänsklig artefakt som kräver kontinuerlig granskning, tolkning och uppdatering av experter. Ramverken kräver uttryckligen mänsklig tillsyn och tydliga eskaleringsprocesser.11 Automatiseringen ersätter alltså inte behovet av mänsklig styrning; den flyttar fokus från manuell kontroll av varje transaktion till styrning av själva automationssystemet och dess regler. Detta innebär att implementeringen av maskinläsbar styrning paradoxalt nog ökar behovet av en mer sofistikerad och kontinuerlig mänsklig styrningsfunktion, inte minskar den.

---

### **Del V: Strategiska rekommendationer och framtiden för beräkningsstyrning**

Detta sista avsnitt sammanfattar rapportens resultat till handlingsbara råd för organisationer och erbjuder ett framåtblickande perspektiv på utvecklingen inom detta fält.

#### **5.1 Handlingsbara rekommendationer för ett robust styrningsprotokoll**

För organisationer som strävar efter att implementera ett effektivt och försvarbart maskinläsbart styrningsramverk, framträder flera strategiska rekommendationer från denna analys.

* **Börja med ett schema, inte bara data:** Grundprincipen för schemadriven utveckling måste vara vägledande. Försök inte att härleda styrningsregler från befintliga data eller loggar; detta leder ofta till överanpassade och ofullständiga scheman.28 Definiera istället policyerna preskriptivt och formellt i ett JSON Schema från början. Detta säkerställer att ramverket är byggt på avsiktliga, genomtänkta principer snarare än på tillfälliga mönster i data.3  
* **Anamma ett hybridtillvägagångssätt:** Ett JSON-protokoll kan inte och bör inte stå ensamt. Den mest robusta lösningen är en hybridmodell där den maskinläsbara JSON-filen kompletteras med mänskligt läsbar dokumentation. JSON-filen verkställer de kvantifierbara reglerna, medan ett länkat dokument (t.ex. ett "Model Card") förklarar resonemanget bakom policyerna, de kvalitativa aspekterna som inte kan kodifieras, och de detaljerade processerna för åtgärder och eskalering.29  
* **Etablera ett tvärfunktionellt styrningsråd:** Skapandet och underhållet av ett styrnings-JSON är inte enbart en ingenjörsuppgift. Det kräver ett dedikerat, tvärfunktionellt styrningsråd med expertis från juridik, etik, affärsverksamhet och teknik. Detta råd ansvarar för att tolka regelverk, fatta beslut om policyer och granska prestandan hos det automatiserade systemet, vilket säkerställer att både "lagens bokstav" och "lagens anda" efterlevs.2  
* **Investera i gransknings- och övervakningsverktyg:** JSON-protokollet är bara så effektivt som de system som övervakar efterlevnaden av det. Organisationer måste investera i en verktygskedja för automatiserad loggning, bias-detektering, prestandamätning och säkerhetsanalys. Verktyg som Microsofts Responsible AI Toolbox visar på den typ av kapacitet som krävs för att ge en helhetsbild av modellens beteende och identifiera avvikelser från det fastställda protokollet.5

#### **5.2 Standardiseringsimperativet: En uppmaning till ett universellt styrningsschema**

Analysen har belyst en betydande "standardiseringslucka". För närvarande utvecklar plattformar som IBM och Collibra sina egna, proprietära format för att definiera AI-styrning och datalinje.23 Även om dessa är kraftfulla inom sina respektive ekosystem, skapar denna fragmentering ett hinder för interoperabilitet, tredjepartsgranskning och effektiv regulatorisk tillsyn.

Det finns ett trängande behov av att branschorgan och standardiseringsorganisationer, såsom NIST, IEEE och ISO/IEC, samarbetar för att utveckla ett standardiserat, öppen källkods-baserat JSON Schema för AI-styrning. Ett sådant universellt schema skulle erbjuda enorma fördelar:

* **Interoperabilitet:** Det skulle göra det möjligt för organisationer att använda en gemensam uppsättning verktyg för styrning och granskning, oavsett vilken AI-plattform de använder.  
* **Regulatorisk effektivitet:** Tillsynsmyndigheter skulle kunna utveckla standardiserade metoder för att granska efterlevnad, vilket skulle förenkla och effektivisera tillsynen.  
* **Ekosystem för verktyg:** En gemensam standard skulle stimulera utvecklingen av ett brett ekosystem av tredjepartsverktyg för validering, övervakning och rapportering.

NIST:s Playbook.json är ett steg i rätt riktning, men ett mer formellt och omfattande JSON Schema, utvecklat genom en öppen och konsensusdriven process, är det nödvändiga nästa steget.20

#### **5.3 Framtiden för beräkningsjuridik: När JSON-filen är policyn**

Den långsiktiga implikationen av att kodifiera styrning i format som JSON är djupgående och sträcker sig långt bortom tekniken. Vi står inför en fundamental förändring i hur policy, lag och etik uttrycks och verkställs.

Detta skapar en förskjutning i yrkesroller och maktstrukturer. Om en JSON-fil blir den juridiskt bindande definitionen av ett företags efterlevnad av, till exempel, en antidiskrimineringslag, blir själva handlingen att skriva och versionshantera den filen en juridisk funktion. En tillsynsmyndighet kan i framtiden begära governance.json-filen och dess fullständiga Git-historik istället för ett 50-sidigt PDF-dokument.29 Detta innebär att efterlevnadsansvariga måste bli "JSON-litterata", och utvecklarna som skriver schemat utövar i praktiken en form av juridik. Gränserna mellan juridiska och tekniska domäner suddas ut, vilket skapar ett behov av nya hybridyrken som kombinerar djup teknisk förståelse med juridisk och etisk expertis. Makten att definiera vad som är "rättvist" eller "transparent" i praktiken flyttas till dem som kan skriva schemat, vilket representerar en omvälvande förändring i företags- och regleringsmaktstrukturer.

Sammanfattningsvis befinner vi oss i början av en långsiktig trend mot "beräkningsjuridik" (computational law), där juridiska och etiska regler i allt högre grad uttrycks i format som är direkt exekverbara av maskiner. Att navigera denna övergång på ett ansvarsfullt, rättvist och transparent sätt är en av de centrala utmaningarna i AI-eran. Denna rapport har syftat till att belysa både de tekniska möjligheterna och de djupa socio-juridiska frågor som denna framtid medför.

#### **Citerade verk**

1. JSON Prompt: The Ultimate Guide to Perfect AI Outputs \- MPG ONE, hämtad augusti 6, 2025, [https://mpgone.com/json-prompt-guide/](https://mpgone.com/json-prompt-guide/)  
2. AI Governance Framework: Secure AI with Policy & Controls \- Strobes Security, hämtad augusti 6, 2025, [https://strobes.co/blog/ai-governance-framework-for-security-leaders/](https://strobes.co/blog/ai-governance-framework-for-security-leaders/)  
3. Introducing JSON Schemas for AI Data Integrity \- DEV Community, hämtad augusti 6, 2025, [https://dev.to/stephenc222/introducing-json-schemas-for-ai-data-integrity-611](https://dev.to/stephenc222/introducing-json-schemas-for-ai-data-integrity-611)  
4. Creating your first schema \- JSON Schema, hämtad augusti 6, 2025, [https://json-schema.org/learn/getting-started-step-by-step](https://json-schema.org/learn/getting-started-step-by-step)  
5. JSON Logging Best Practices | Loggly, hämtad augusti 6, 2025, [https://www.loggly.com/use-cases/json-logging-best-practices/](https://www.loggly.com/use-cases/json-logging-best-practices/)  
6. JSON to JSON Schema Converter \- Liquid Technologies, hämtad augusti 6, 2025, [https://www.liquid-technologies.com/infer-json-schema](https://www.liquid-technologies.com/infer-json-schema)  
7. Free Online JSON to JSON Schema Converter \- Liquid Technologies, hämtad augusti 6, 2025, [https://www.liquid-technologies.com/online-json-to-schema-converter](https://www.liquid-technologies.com/online-json-to-schema-converter)  
8. Tools \- JSON Schema, hämtad augusti 6, 2025, [https://json-schema.org/tools](https://json-schema.org/tools)  
9. JSON: Data Format for AI & Machine Learning | Ultralytics, hämtad augusti 6, 2025, [https://www.ultralytics.com/glossary/json](https://www.ultralytics.com/glossary/json)  
10. Mastering API Responses: The Definitive Guide to JSON Formatting \- Apidog, hämtad augusti 6, 2025, [https://apidog.com/blog/json-api-responses/](https://apidog.com/blog/json-api-responses/)  
11. AI Governance Framework: Key Principles & Best Practices \- MineOS, hämtad augusti 6, 2025, [https://www.mineos.ai/articles/ai-governance-framework](https://www.mineos.ai/articles/ai-governance-framework)  
12. ETHICALLY ALIGNED DESIGN \- of IEEE Standards Working Groups, hämtad augusti 6, 2025, [https://sagroups.ieee.org/global-initiative/wp-content/uploads/sites/542/2023/01/ead1e.pdf](https://sagroups.ieee.org/global-initiative/wp-content/uploads/sites/542/2023/01/ead1e.pdf)  
13. Artificial Intelligence Playbook for the UK Government (HTML) \- GOV.UK, hämtad augusti 6, 2025, [https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government/artificial-intelligence-playbook-for-the-uk-government-html](https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government/artificial-intelligence-playbook-for-the-uk-government-html)  
14. Navigating the NIST AI Risk Management Framework \- Hyperproof, hämtad augusti 6, 2025, [https://hyperproof.io/navigating-the-nist-ai-risk-management-framework/](https://hyperproof.io/navigating-the-nist-ai-risk-management-framework/)  
15. NIST AI Risk Management Framework (AI RMF) \- Palo Alto Networks, hämtad augusti 6, 2025, [https://www.paloaltonetworks.com/cyberpedia/nist-ai-risk-management-framework](https://www.paloaltonetworks.com/cyberpedia/nist-ai-risk-management-framework)  
16. What is AI Governance? \- IBM, hämtad augusti 6, 2025, [https://www.ibm.com/think/topics/ai-governance](https://www.ibm.com/think/topics/ai-governance)  
17. Navigating the NIST AI Risk Management Framework with confidence | Blog \- OneTrust, hämtad augusti 6, 2025, [https://www.onetrust.com/blog/navigating-the-nist-ai-risk-management-framework-with-confidence/](https://www.onetrust.com/blog/navigating-the-nist-ai-risk-management-framework-with-confidence/)  
18. AI Risk Management Framework | NIST, hämtad augusti 6, 2025, [https://www.nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)  
19. Artificial Intelligence Risk Management Framework (AI RMF 1.0) \- NIST Technical Series Publications, hämtad augusti 6, 2025, [https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)  
20. Playbook \- AIRC, hämtad augusti 6, 2025, [https://airc.nist.gov/airmf-resources/playbook/](https://airc.nist.gov/airmf-resources/playbook/)  
21. AI Ethics 101: Comparing IEEE, EU and OECD Guidelines \- Zendata, hämtad augusti 6, 2025, [https://www.zendata.dev/post/ai-ethics-101](https://www.zendata.dev/post/ai-ethics-101)  
22. What to Expect From IEEE 7000: The First Standard for Building Ethical Systems, hämtad augusti 6, 2025, [https://technologyandsociety.org/what-to-expect-from-ieee-7000-the-first-standard-for-building-ethical-systems/](https://technologyandsociety.org/what-to-expect-from-ieee-7000-the-first-standard-for-building-ethical-systems/)  
23. Configure asset deployments using JSON configuration files \- Docs ..., hämtad augusti 6, 2025, [https://dataplatform.cloud.ibm.com/docs/content/wsj/model/wos-config-file.html](https://dataplatform.cloud.ibm.com/docs/content/wsj/model/wos-config-file.html)  
24. Custom technical lineage JSON file examples, hämtad augusti 6, 2025, [https://productresources.collibra.com/docs/collibra/latest/Content/CollibraDataLineage/CustomTechnicalLineage/ref\_custom-lineage-json-file\_example.htm](https://productresources.collibra.com/docs/collibra/latest/Content/CollibraDataLineage/CustomTechnicalLineage/ref_custom-lineage-json-file_example.htm)  
25. JSON:API — Recommendations, hämtad augusti 6, 2025, [https://jsonapi.org/recommendations/](https://jsonapi.org/recommendations/)  
26. Structured Outputs \- OpenAI API \- OpenAI Platform, hämtad augusti 6, 2025, [https://platform.openai.com/docs/guides/structured-outputs](https://platform.openai.com/docs/guides/structured-outputs)  
27. Generative AI on Vertex AI \- Structured output \- Google Cloud, hämtad augusti 6, 2025, [https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output)  
28. Improving JSON Schema Inference by Incorporating User Inputs \- CEUR-WS.org, hämtad augusti 6, 2025, [https://ceur-ws.org/Vol-3941/BENEVOL2024\_TECH\_paper14.pdf](https://ceur-ws.org/Vol-3941/BENEVOL2024_TECH_paper14.pdf)  
29. microsoft/responsible-ai-toolbox \- GitHub, hämtad augusti 6, 2025, [https://github.com/microsoft/responsible-ai-toolbox](https://github.com/microsoft/responsible-ai-toolbox)  
30. Global Landscape of Responsible AI in Healthcare: A Comprehensive Guide \- GitHub, hämtad augusti 6, 2025, [https://github.com/nliulab/Global-Responsible-AI](https://github.com/nliulab/Global-Responsible-AI)  
31. nlohmann/json: JSON for Modern C++ \- GitHub, hämtad augusti 6, 2025, [https://github.com/nlohmann/json](https://github.com/nlohmann/json)