# scripts/wrap_json_in_html.py
#
# HISTORIK:
# * v1.0 (Initial): Första versionen.
# * v2.0 (Bug Fix): Ersatt den felaktiga `str.format()`-metoden, som kraschade på grund av
#   klammerparenteser i JSON-datan. Använder nu enkel strängkonkatenering, vilket är
#   fullständigt robust oavsett innehållet i datan.
#
# TILLÄMPADE REGLER (Frankensteen v3.7):
# - Denna fil följer principen om Single Responsibility. Dess enda uppgift är att formatera.
# - Använder `sys.argv` för att ta emot filnamn, vilket gör skriptet återanvändbart och testbart.
# - Robust felhantering med try-except och tydliga felmeddelanden till stderr.

import sys

def wrap_json_in_html(input_json_path, output_html_path):
    """
    Läser en JSON-fil och skriver dess innehåll inuti en enkel, statisk HTML-sida.
    Detta gör innehållet läsbart för AI-verktyg som förväntar sig 'text/html'.
    """

    # Att definiera header och footer separat och använda konkatenering är det
    # mest robusta sättet. Det undviker alla problem med specialtecken (som {})
    # i källdatan, vilket metoder som .format() eller f-strings lider av.
    html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Context Data</title>
    <style>body { font-family: monospace; white-space: pre; word-wrap: break-word; }</style>
</head>
<body>
"""
    html_footer = """
</body>
</html>"""

    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            json_content = f.read()

        # Enkel, säker och robust konkatenering.
        final_html = html_header + json_content + html_footer

        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"[INFO] Wrapper: Skapade framgångsrikt '{output_html_path}' från '{input_json_path}'.")

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
