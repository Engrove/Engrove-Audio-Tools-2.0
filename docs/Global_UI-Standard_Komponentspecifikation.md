# Global UI-Standard Komponentspecifikation.md

# **Appendix: Fullständig Komponentspecifikation**

Detta appendix utökar den globala UI-standarden med detaljerade,
utvecklar-redo specifikationer för alla primära interaktiva komponenter.
Varje tabell definierar de visuella attributen för komponentens olika
tillstånd (Default, Hover, Focus, Active, Disabled) för både mörkt och
ljust tema. Alla specifikationer bygger på de grundläggande
design-tokens och principer som etablerats i huvudstandarden.

**Notering om UI-Densitet**: Samtliga komponenter som specificeras i
detta dokument måste vara \"densitetsmedvetna\". Utöver de grundläggande
stilarna ska varje komponent implementera specifika CSS-regler som
aktiveras när den globala .compact-theme-klassen är närvarande. Dessa
regler ska justera interna mått som padding, margin och font-size för
att skapa en mer informationstät layout i enlighet med \"Compact
Mode\"-specifikationen.

## **1. Knappar (Buttons)**

### **1.1 Mörkt Läge (Standard)**

  -----------------------------------------------------------------------------------------------------------------------------
  Komponent    Status      Bakgrundsfärg                Textfärg                 Kant                         Skugga
  ------------ ----------- ---------------------------- ------------------------ ---------------------------- -----------------
  **Primär     Default     \$interactive-accent         \$text-high-emphasis     Ingen                        box-shadow: 0 2px
  Knapp**                                                                                                     4px
                                                                                                              rgba(0,0,0,0.2)

               Hover       \$interactive-accent-hover   \$text-high-emphasis     Ingen                        box-shadow: 0 4px
                                                                                                              8px
                                                                                                              rgba(0,0,0,0.3)

               Focus       \$interactive-accent         \$text-high-emphasis     2px solid                    box-shadow: 0 2px
                                                                                 \$interactive-accent-hover   4px
                                                                                                              rgba(0,0,0,0.2)

               Active      \$interactive-accent-hover   \$text-high-emphasis     Ingen                        box-shadow: inset
                                                                                                              0 2px 4px
                                                                                                              rgba(0,0,0,0.2)

               Disabled    \$surface-tertiary           \$text-low-emphasis      1px solid \$border-primary   Ingen

  **Sekundär   Default     transparent                  \$text-medium-emphasis   1px solid \$border-primary   Ingen
  Knapp**                                                                                                     

               Hover       \$surface-tertiary           \$text-high-emphasis     1px solid \$border-primary   Ingen

               Focus       transparent                  \$text-high-emphasis     2px solid                    Ingen
                                                                                 \$interactive-accent         

               Active      \$surface-tertiary           \$text-high-emphasis     1px solid                    Ingen
                                                                                 \$interactive-accent         

               Disabled    transparent                  \$text-low-emphasis      1px solid \$border-primary   Ingen
  -----------------------------------------------------------------------------------------------------------------------------

### **1.2 Ljust Läge**

  ------------------------------------------------------------------------------------------------------------------------------
  Komponent    Status      Bakgrundsfärg                Textfärg                 Kant                         Skugga
  ------------ ----------- ---------------------------- ------------------------ ---------------------------- ------------------
  **Primär     Default     \$interactive-accent         \$surface-primary        Ingen                        box-shadow: 0 2px
  Knapp**                                                                                                     4px
                                                                                                              rgba(0,0,0,0.15)

               Hover       \$interactive-accent-hover   \$surface-primary        Ingen                        box-shadow: 0 4px
                                                                                                              8px
                                                                                                              rgba(0,0,0,0.2)

               Focus       \$interactive-accent         \$surface-primary        2px solid                    box-shadow: 0 2px
                                                                                 \$interactive-accent-hover   4px
                                                                                                              rgba(0,0,0,0.15)

               Active      \$interactive-accent-hover   \$surface-primary        Ingen                        box-shadow: inset
                                                                                                              0 2px 4px
                                                                                                              rgba(0,0,0,0.15)

               Disabled    \$surface-tertiary           \$text-low-emphasis      1px solid \$border-primary   Ingen

  **Sekundär   Default     transparent                  \$text-medium-emphasis   1px solid \$border-primary   Ingen
  Knapp**                                                                                                     

               Hover       \$surface-tertiary           \$text-high-emphasis     1px solid \$border-primary   Ingen

               Focus       transparent                  \$text-high-emphasis     2px solid                    Ingen
                                                                                 \$interactive-accent         

               Active      \$surface-tertiary           \$text-high-emphasis     1px solid                    Ingen
                                                                                 \$interactive-accent         

               Disabled    transparent                  \$text-low-emphasis      1px solid \$border-primary   Ingen
  ------------------------------------------------------------------------------------------------------------------------------

## **2. Inmatningsfält (Input Fields)**

### **2.1 Mörkt Läge (Standard)**

  ---------------------------------------------------------------------------------------------------
  Status         Bakgrundsfärg         Textfärg               Kant                     Skugga
  -------------- --------------------- ---------------------- ------------------------ --------------
  Default        \$surface-tertiary    \$text-high-emphasis   1px solid                Ingen
                                                              \$border-primary         

  Hover          \$surface-tertiary    \$text-high-emphasis   1px solid                Ingen
                                                              \$text-medium-emphasis   

  Focus          \$surface-secondary   \$text-high-emphasis   2px solid                box-shadow: 0
                                                              \$interactive-accent     0 0 2px
                                                                                       rgba(51, 145,
                                                                                       255, 0.3)

  Disabled       \$surface-secondary   \$text-low-emphasis    1px solid                Ingen
                                                              \$border-primary         
  ---------------------------------------------------------------------------------------------------

### **2.2 Ljust Läge**

  ---------------------------------------------------------------------------------------------------
  Status         Bakgrundsfärg         Textfärg               Kant                     Skugga
  -------------- --------------------- ---------------------- ------------------------ --------------
  Default        \$surface-tertiary    \$text-high-emphasis   1px solid                Ingen
                                                              \$border-primary         

  Hover          \$surface-tertiary    \$text-high-emphasis   1px solid                Ingen
                                                              \$text-medium-emphasis   

  Focus          \$surface-primary     \$text-high-emphasis   2px solid                box-shadow: 0
                                                              \$interactive-accent     0 0 2px
                                                                                       rgba(0, 123,
                                                                                       255, 0.25)

  Disabled       \$surface-secondary   \$text-low-emphasis    1px solid                Ingen
                                                              \$border-primary         
  ---------------------------------------------------------------------------------------------------

## **3. Dropdown-menyer (Selects)**

### **3.1 Mörkt Läge (Standard)**

  -------------------------------------------------------------------------------------------------------------
  Status         Bakgrundsfärg         Textfärg               Kant                     Ikonfärg
  -------------- --------------------- ---------------------- ------------------------ ------------------------
  Default        \$surface-tertiary    \$text-high-emphasis   1px solid                \$text-medium-emphasis
                                                              \$border-primary         

  Hover          \$surface-tertiary    \$text-high-emphasis   1px solid                \$text-high-emphasis
                                                              \$text-medium-emphasis   

  Focus          \$surface-secondary   \$text-high-emphasis   2px solid                \$text-high-emphasis
                                                              \$interactive-accent     

  Active (Öppen) \$surface-secondary   \$text-high-emphasis   2px solid                \$interactive-accent
                                                              \$interactive-accent     

  Disabled       \$surface-secondary   \$text-low-emphasis    1px solid                \$text-low-emphasis
                                                              \$border-primary         
  -------------------------------------------------------------------------------------------------------------

*Not: Den öppna menyn använder \$surface-secondary som bakgrund. Vald
post har \$interactive-accent som bakgrund och \$text-high-emphasis som
textfärg.*

### **3.2 Ljust Läge**

  -------------------------------------------------------------------------------------------------------------
  Status         Bakgrundsfärg         Textfärg               Kant                     Ikonfärg
  -------------- --------------------- ---------------------- ------------------------ ------------------------
  Default        \$surface-tertiary    \$text-high-emphasis   1px solid                \$text-medium-emphasis
                                                              \$border-primary         

  Hover          \$surface-tertiary    \$text-high-emphasis   1px solid                \$text-high-emphasis
                                                              \$text-medium-emphasis   

  Focus          \$surface-primary     \$text-high-emphasis   2px solid                \$text-high-emphasis
                                                              \$interactive-accent     

  Active (Öppen) \$surface-primary     \$text-high-emphasis   2px solid                \$interactive-accent
                                                              \$interactive-accent     

  Disabled       \$surface-secondary   \$text-low-emphasis    1px solid                \$text-low-emphasis
                                                              \$border-primary         
  -------------------------------------------------------------------------------------------------------------

*Not: Den öppna menyn använder \$surface-primary som bakgrund med en
lätt skugga. Vald post har \$interactive-accent som bakgrund och
\$surface-primary som textfärg.*

## **4. Växlare (Toggle Switches)**

### **4.1 Mörkt Läge (Standard)**

  -----------------------------------------------------------------------------------------------
  Status            Spår-bakgrund                Handtag-bakgrund         Kant/Skugga
  ----------------- ---------------------------- ------------------------ -----------------------
  **Av (Off)**                                                            

  Default           \$surface-tertiary           \$text-medium-emphasis   Ingen

  Hover             \$surface-tertiary           \$text-high-emphasis     Ingen

  **På (On)**                                                             

  Default           \$interactive-accent         \$surface-primary        Ingen

  Hover             \$interactive-accent-hover   \$surface-primary        Ingen

  **Alla**                                                                

  Focus             Samma som Default            Samma som Default        outline: 2px solid
                                                                          \$interactive-accent;
                                                                          outline-offset: 2px;

  Disabled          \$surface-secondary          \$text-low-emphasis      Ingen
  -----------------------------------------------------------------------------------------------

### **4.2 Ljust Läge**

  -----------------------------------------------------------------------------------------------
  Status            Spår-bakgrund                Handtag-bakgrund         Kant/Skugga
  ----------------- ---------------------------- ------------------------ -----------------------
  **Av (Off)**                                                            

  Default           \$surface-tertiary           \$text-medium-emphasis   Ingen

  Hover             \$surface-tertiary           \$text-high-emphasis     Ingen

  **På (On)**                                                             

  Default           \$interactive-accent         \$surface-primary        Ingen

  Hover             \$interactive-accent-hover   \$surface-primary        Ingen

  **Alla**                                                                

  Focus             Samma som Default            Samma som Default        outline: 2px solid
                                                                          \$interactive-accent;
                                                                          outline-offset: 2px;

  Disabled          \$surface-secondary          \$text-low-emphasis      Ingen
  -----------------------------------------------------------------------------------------------

## **5. Kryssrutor & Radioknappar (Checkboxes & Radio Buttons)**

### **5.1 Mörkt Läge (Standard)**

  ----------------------------------------------------------------------------------------------------------------------
  Komponent        Status         Bakgrund                     Kant                         Innehåll (Bock/Prick)
  ---------------- -------------- ---------------------------- ---------------------------- ----------------------------
  **Kryssruta**    Omarkerad      transparent                  2px solid                    Ingen
                                                               \$text-medium-emphasis       

                   Omarkerad      \$surface-tertiary           2px solid                    Ingen
                   (Hover)                                     \$text-high-emphasis         

                   Markerad       \$interactive-accent         2px solid                    \$surface-primary
                                                               \$interactive-accent         

                   Markerad       \$interactive-accent-hover   2px solid                    \$surface-primary
                   (Hover)                                     \$interactive-accent-hover   

  **Radioknapp**   Ovald          transparent                  2px solid                    Ingen
                                                               \$text-medium-emphasis       

                   Ovald (Hover)  \$surface-tertiary           2px solid                    Ingen
                                                               \$text-high-emphasis         

                   Vald           transparent                  2px solid                    \$interactive-accent
                                                               \$interactive-accent         

                   Vald (Hover)   \$surface-tertiary           2px solid                    \$interactive-accent-hover
                                                               \$interactive-accent-hover   

  **Alla**         Focus          Samma som Default            Samma som Default            Samma som Default, med
                                                                                            outline: 2px solid
                                                                                            \$interactive-accent;
                                                                                            outline-offset: 2px;

                   Disabled       \$surface-secondary          2px solid                    \$text-low-emphasis
                                                               \$text-low-emphasis          
  ----------------------------------------------------------------------------------------------------------------------

### **5.2 Ljust Läge**

  ----------------------------------------------------------------------------------------------------------------------
  Komponent        Status         Bakgrund                     Kant                         Innehåll (Bock/Prick)
  ---------------- -------------- ---------------------------- ---------------------------- ----------------------------
  **Kryssruta**    Omarkerad      transparent                  2px solid                    Ingen
                                                               \$text-medium-emphasis       

                   Omarkerad      \$surface-tertiary           2px solid                    Ingen
                   (Hover)                                     \$text-high-emphasis         

                   Markerad       \$interactive-accent         2px solid                    \$surface-primary
                                                               \$interactive-accent         

                   Markerad       \$interactive-accent-hover   2px solid                    \$surface-primary
                   (Hover)                                     \$interactive-accent-hover   

  **Radioknapp**   Ovald          transparent                  2px solid                    Ingen
                                                               \$text-medium-emphasis       

                   Ovald (Hover)  \$surface-tertiary           2px solid                    Ingen
                                                               \$text-high-emphasis         

                   Vald           transparent                  2px solid                    \$interactive-accent
                                                               \$interactive-accent         

                   Vald (Hover)   \$surface-tertiary           2px solid                    \$interactive-accent-hover
                                                               \$interactive-accent-hover   

  **Alla**         Focus          Samma som Default            Samma som Default            Samma som Default, med
                                                                                            outline: 2px solid
                                                                                            \$interactive-accent;
                                                                                            outline-offset: 2px;

                   Disabled       \$surface-secondary          2px solid                    \$text-low-emphasis
                                                               \$text-low-emphasis          
  ----------------------------------------------------------------------------------------------------------------------

#### Citerade verk

1.  Användarvänlig UI för Justeringskalkylator
