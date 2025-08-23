# BEGIN FILE: scripts/modules/ui_protocol_packager.py
# scripts/modules/ui_protocol_packager.py
#
# === SYFTE & ÖVERSIKT ===
# Exponerar innehållet i den motsvarande JS-filen (ui_protocol_packager.js)
# som en Python-sträng för att kunna bäddas in/packas av Python-skript,
# t.ex. engrove_audio_tools_creator.py. Detta gör att byggkedjan kan läsa
# in JS-modulen utan att kräva Node vid importtillfället.
#
# === ANVÄNDNING ===
# from modules.ui_protocol_packager import JS_PROTOCOL_PACKAGER
# # ... eller vid behov:
# from modules.ui_protocol_packager import get_js_protocol_packager
#
# === BEROENDEN & RUNTIME ===
# - Ingen nätverksåtkomst.
# - Läser lokalt filsystem: syskonfilen "ui_protocol_packager.js".
#
# === FELHANTERING ===
# - FilNotFoundError höjs om .js-filen saknas.
# - Alla filoperationer sker med explicit UTF-8.
#
# === LICENS & HISTORIK ===
# Denna modul följer samma struktur och kommentarstil som övriga filer
# i scripts/modules/ för enkel historik och underhåll.

from __future__ import annotations

from pathlib import Path

__all__ = [
    "JS_PROTOCOL_PACKAGER",
    "get_js_protocol_packager",
]

# Absolut sökväg till denna .py-fil och den tillhörande .js-filen
_THIS_FILE = Path(__file__).resolve()
_JS_FILE = _THIS_FILE.with_suffix(".js")


def get_js_protocol_packager() -> str:
    """
    Läser in syskonfilen "ui_protocol_packager.js" och returnerar innehållet.

    Returns:
        str: Hela filinnehållet (UTF-8) från .js-filen.

    Raises:
        FileNotFoundError: Om .js-filen inte finns i samma katalog.
    """
    if not _JS_FILE.exists():
        raise FileNotFoundError(
            f"Hittar inte {_JS_FILE.name} i katalogen {_THIS_FILE.parent}."
        )
    return _JS_FILE.read_text(encoding="utf-8")


# Exportera direkt som konstant för konsumenter som förväntar sig ett värde
JS_PROTOCOL_PACKAGER: str = get_js_protocol_packager()

# END FILE: scripts/modules/ui_protocol_packager.py
