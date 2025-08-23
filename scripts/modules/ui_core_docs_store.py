# scripts/modules/ui_core_docs_store.py
# -*- coding: utf-8 -*-
#
# SYFTE
#   Hanterar localStorage-listan över "kärndokument" (core docs) i webbläsaren.
#   Python-filen exponerar inkapslad, körbar JS-kod som skrivs till core_store.js.
#
# FÖRKLARING
#   - STORAGE_KEY = 'coreDocs'
#   - API (på window.CoreDocsStore):
#       loadCoreDocs():  -> list[str]
#       saveCoreDocs(list[str]): -> list[str] | null
#       isCoreDoc(path: str): -> bool
#       selectCoreInTree(): -> markerar sparade kärndok i filträdet om addPathsToSelection finns
#
# HISTORIK
#   v1.0  (2025-08-23): Första versionen.
JS_CORE_DOCS_STORE = r"""(function() {
  'use strict';
  const STORAGE_KEY = 'coreDocs';

  function _read() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return [];
      const arr = JSON.parse(raw);
      return Array.isArray(arr) ? Array.from(new Set(arr.filter(Boolean))) : [];
    } catch (e) {
      console.warn('Kunde inte läsa coreDocs från localStorage:', e);
      return [];
    }
  }

  function _write(list) {
    try {
      const clean = Array.isArray(list) ? Array.from(new Set(list.filter(Boolean))) : [];
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

  function selectCoreInTree() {
    const staticList = _read();
    if (staticList.length && typeof window.addPathsToSelection === 'function') {
      window.addPathsToSelection(staticList, []);
    }
  }

  window.CoreDocsStore = Object.freeze({
    loadCoreDocs,
    saveCoreDocs,
    isCoreDoc,
    selectCoreInTree,
    STORAGE_KEY,
  });
})();"""
