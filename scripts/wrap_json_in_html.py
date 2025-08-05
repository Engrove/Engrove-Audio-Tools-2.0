# scripts/wrap_json_in_html.py
#
# HISTORIK:
# * v1.0 (Initial): Första versionen.
# * v2.0 (Bug Fix): Felaktig implementation med str.format().
# * v3.0 (Definitive Fix): Implementerar html.escape() för att korrekt hantera
#   specialtecken (<, >, &) i JSON-datan. Detta förhindrar att webbläsaren
#   feltolkar innehållet som HTML-taggar. Omsluter även innehållet i en
#   <pre>-tagg för semantisk korrekthet.
#
# TILLÄMPADE REGLER (Frankensteen v3.7):
# - Denna fil följer principen om Single Responsibility.
# - Använder standardbibliotek (`html`) för robust och säker escaping.
# - Robust felhantering med try-except och tydliga felmeddelanden till stderr.

import sys
import html

def wrap_json_in_html(input_json_path, output_html_path):
    """
    Läser en JSON-fil, HTML-escapar dess innehåll och skriver det inuti en
    statisk HTML-sida, omslutet av en <pre>-tagg. Detta garanterar att
    innehållet alltid renderas som text, oavsett vilka tecken det innehåller.
    """

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Context Data</title>
    <style>body {{ margin: 0; }} pre {{ margin: 1em; font-family: monospace; white-space: pre-wrap; word-wrap: break-word; }}</style>
</head>
<body>
<pre>{escaped_content}</pre>
</body>
</html>"""

    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            json_content = f.read()

        # KÄRNAN I LÖSNINGEN: Escapa allt innehåll så att webbläsaren
        # renderar det som text och inte tolkar det som HTML.
        escaped_content = html.escape(json_content)

        # Använd .format() här är säkert eftersom den *escapade* texten
        # inte längre innehåller några tecken som .format() kan feltolka.
        final_html = html_template.format(escaped_content=escaped_content)

        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"[INFO] Wrapper: Skapade framgångsrikt och HTML-escapade '{output_html_path}'.")

    except FileNotFoundError:
        print(f"[ERROR] Wrapper: Kunde inte hitta indatafilen: {input_json_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Wrapper: Ett oväntat fel inträffade: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Användning: python wrap_json_in_html.py <sökväg-till-input.json> <sökväg-till-output.html>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    wrap_json_in_html(input_file, output_file)
