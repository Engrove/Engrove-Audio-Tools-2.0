# FILE: scripts/modules/ui_core_docs_store.py
# === SYFTE ===
# Innehåller inkapslad JS-modul som hanterar localStorage för "kärndokument".
# === HISTORIK ===
# * v1.0 (2025-08-23): Första versionen.
JS_CORE_DOCS_STORE = r"""/**
 * scripts/modules/ui_core_docs_store.py (embedded JS)
 * Exponerar en enkel wrapper kring localStorage för "kärndokument".
 * Nyckel: 'coreDocs'
 */
(function() {
  const STORAGE_KEY = 'coreDocs';

  function _read() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return [];
      const arr = JSON.parse(raw);
      return Array.isArray(arr) ? Array.from(new Set(arr)) : [];
    } catch (e) {
      console.warn('Kunde inte läsa coreDocs från localStorage:', e);
      return [];
    }
  }

  function _write(list) {
    try {
      const clean = Array.isArray(list) ? Array.from(new Set(list)) : [];
      localStorage.setItem(STORAGE_KEY, JSON.stringify(clean));
      return clean;
    } catch (e) {
      console.warn('Kunde inte skriva coreDocs till localStorage:', e);
      return null;
    }
  }

  function loadCoreDocs() { return _read(); }
  function saveCoreDocs(list) { return _write(list); }
  function isCoreDoc(path) {
    if (!path) return false;
    const set = new Set(_read());
    return set.has(path);
  }

  // Hjälp: markera i trädet genom att återanvända addPathsToSelection
  function selectCoreInTree() {
    const staticList = _read();
    if (staticList.length && window.addPathsToSelection) {
      window.addPathsToSelection(staticList, []); // inga dynamiska mappar här
    }
  }

  window.CoreDocsStore = {
    loadCoreDocs,
    saveCoreDocs,
    isCoreDoc,
    selectCoreInTree,
    STORAGE_KEY,
  };
})();
"""
# END FILE
