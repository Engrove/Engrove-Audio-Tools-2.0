// src/features/mobile-menu-toggle/model/useMobileMenu.js
// Detta är en Vue Composable som hanterar tillståndet och logiken för mobilmenyn.
// Den inkapslar logiken för att öppna/stänga menyn och för att låsa/låsa upp
// scrollning på sidan, vilket skapar en ren och återanvändbar "feature model".

import { ref, watch } from 'vue';

// Vi skapar en enda instans av state (singleton) för att delas över hela appen.
// Detta säkerställer att både knappen och menyn refererar till samma tillstånd.
const isMenuOpen = ref(false);

/**
 * En Vue Composable för att hantera mobilmenyns globala tillstånd.
 * @returns {object} Ett objekt med reaktivt state och funktioner.
 */
export function useMobileMenu() {

  /**
   * Växlar meny-tillståndet mellan öppet och stängt.
   */
  function toggleMenu() {
    isMenuOpen.value = !isMenuOpen.value;
  }

  /**
   * Stänger menyn. Används t.ex. vid klick på en navigeringslänk.
   */
  function closeMenu() {
    isMenuOpen.value = false;
  }

  // Använder en 'watcher' för att reagera på ändringar i `isMenuOpen`.
  // Detta är en sidoeffekt (side effect) som låser sidans scroll-funktion
  // när menyn är öppen för en bättre mobilupplevelse.
  watch(isMenuOpen, (isOpen) => {
    // Om `isOpen` är sant, lägg till CSS-klassen 'body-scroll-lock' på body-elementet.
    // Om `isOpen` är falskt, ta bort CSS-klassen 'body-scroll-lock'.
    if (isOpen) {
      document.body.classList.add('body-scroll-lock');
    } else {
      document.body.classList.remove('body-scroll-lock');
    }
  });

  return {
    isMenuOpen,
    toggleMenu,
    closeMenu,
  };
}
// src/features/mobile-menu-toggle/model/useMobileMenu.js
