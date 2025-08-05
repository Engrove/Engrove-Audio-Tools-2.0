# docs/AR_Protractor_Teknisk_Analys.md
#
# === SYFTE & ANSVAR ===
# Detta dokument utgör en djupgående teknisk analys av AR Protractor-systemet.
# Det utvärderar den tekniska realiserbarheten, prestanda, tillförlitlighet och
# underhållbarhet för den föreslagna lösningen baserad på Three.js och OpenCV.js.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-05): Initial skapelse. Konverterad från OCR-bilder av ett textdokument
#   till en formell, strukturerad Markdown-fil.
#
# === TILLÄMPADE REGLER (Frankensteen v3.7) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och konverterats.

# Utvärdering av AR Protractor-systemet

## Teknisk realiserbarhet

AR Protractor-systemet är i hög grad tekniskt genomförbart med de föreslagna verktygen. `Three.js` används som 3D-motor för att rendera den virtuella scenen och överlagrade mätverktyg, vilket är en beprövad och öppen källkodsbaserad plattform för `WebGL`-grafik. `OpenCV.js` står för bildbehandlingen – bland annat den viktiga kamerakalibreringen och detektering av AR-markörer via `ArUco`-biblioteket. `ArUco`-markörer (tillgängliga via OpenCV:s `aruco`-modul) har valts för att uppnå högsta precision och stabilitet, då de ger robust spårning med mindre jitter och inbyggd felkorrigering jämfört med äldre `ARToolKit`-baserade lösningar. Dessa komponenter är alla tillgängliga som öppen källkod och anses vara stabila inom sina respektive områden.

En praktisk aspekt är att `OpenCV.js` i standardutförande inte alltid inkluderar alla behövda moduler. För att kunna nyttja kamerakalibrering (`calib3d`-modulen för t.ex. `solvePnP`) och `ArUco`-detektion måste man göra en specialkompilering av `OpenCV.js` där `calib3d`- och `aruco`-modulerna ingår. Detta är dock genomförbart – OpenCV är designat för att kunna skräddarsys för `WebAssembly`, och det finns etablerade metoder och guider för att bygga in just `ArUco`- och kalibreringsfunktionaliteten i en webbmiljö. Sammanfattningsvis finns alla nödvändiga tekniska byggstenar tillgängliga som stabila open source-bibliotek, och det beskrivna systemet går att implementera med dessa verktyg. Den extra komplexiteten med en egen OpenCV-build är motiverad av kraven på prestanda och precision.

## Prestanda

Prestandamässigt bedöms lösningen kunna fungera rimligt snabbt på moderna enheter, men det krävs optimeringar. `Three.js`-renderingen av 3D-överläggen sker på GPU:n och kan normalt hantera 60+ FPS utan problem. Den potentiella flaskhalsen är den kontinuerliga bildanalysen i `OpenCV.js`, som körs på CPU (via `WebAssembly`) och kan vara krävande. På mobila enheter kan analysen ta längre tid än tidsbudgeten per bildruta (~16,7 ms för 60 FPS), vilket riskerar att sänka bildfrekvensen.

För att hantera detta föreslås konceptet “Snapshot-Analys", där systemet inte analyserar varje inkommande videobild utan hoppar över vissa bildrutor. Detta intermittent-läge minskar CPU-belastningen och ger ändå tillräckligt uppdaterad spårning för mätändamål.

En annan viktig optimering är användning av Web Workers. Genom att flytta `OpenCV`-beräkningarna till en bakgrundstråd kan man förhindra att huvudtråden (UI) blockeras av tunga operationer. Därmed kan kamerans videoström och `Three.js`-renderingen fortsätta mjukt, medan bildanalysen sker parallellt. Att implementera detta innebär extra komplexitet (t.ex. dataöverföring av varje kamerabild till workern), men det kan dramatiskt förbättra upplevd prestanda genom att eliminera UI-frysningar.

## Tillförlitlighet

Systemets tillförlitlighet och mätnoggrannhet vilar till stor del på kamerakalibreringen samt spårningsalgoritmernas kvalitet. En korrekt utförd kamerakalibrering är absolut avgörande för att uppnå millimeternoggrann mätning. Kalibreringen etablerar den metriska skalan och korrigerar linsdistortion.

När det gäller själva AR-spårningen erbjuder `ArUco`-baserade markörer en robust grund. `ArUco`-algoritmen är känd för pålitlig detektion även under varierande ljusförhållanden och för sin stabilitet tack vare inbyggd felkorrigering. Genom `solvePnP` (i OpenCV:s `calib3d`-modul) beräknas markörens position och orientering relativt kameran. Dock bör man ha realistiska förväntningar: **millimeternoggrannhet** är en hög ambition som i praktiken förutsätter korta avstånd och högupplösta kamerabilder. Små avvikelser i hörndetektering (subpixel-fel) kan lätt motsvara ett par millimeter i verkligheten.

Sammantaget kan systemet anses tillförlitligt för precisionsmätning om användaren genomför kalibreringen korrekt och markörerna används under goda förhållanden. Vi rekommenderar att systemet inkluderar tydliga indikatorer på spårningskvalitet (t.ex. varningar vid dålig markörsikt eller hög osäkerhet).

## Underhållsbarhet

Underhållsbarheten för AR Protractor-kodbasen påverkas av dess komplexitet och beroendet av specialbyggda komponenter. Särskilt integrationen av `OpenCV.js` med custom-moduler innebär att utvecklaren har avvikit från standard-CDN-versioner och själv kompilerat in `ArUco`- och `calib3d`-funktionaliteten. Detta leder till ett par underhållsmässiga konsekvenser:

*   **Specialkompilerat bibliotek:** Den skräddarsydda `OpenCV.js`-builden måste underhållas vid uppdateringar. Om OpenCV släpper nya versioner kan det kräva att man återigen bygger en ny version med rätt moduler. För en användare utan erfarenhet av `Emscripten` och C++-byggmiljö kan detta vara avskräckande.
*   **Komplex kodbas:** Kombinationen av `Three.js` och `OpenCV` innebär att koden spänner över både grafisk 3D-logik och matematisk bildbehandling. Att översätta kamerans parametrar till `Three.js`-kameror och virtuella objekt kräver kunskap om linjär algebra och koordinattransformationer.

Sammanfattningsvis är kodbasen möjlig att underhålla, men den kräver en relativt avancerad kompetensprofil. För att öka underhållsbarheten bör projektet dokumenteras väl, och kanske kan koden modulariseras så att `OpenCV`/`WASM`-delen är inkapslad och kan bytas ut utan att röra 3D-delen.
