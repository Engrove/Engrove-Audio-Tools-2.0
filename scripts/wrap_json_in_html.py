# scripts/wrap_json_in_html.py
#
# HISTORIK:
# * v1.0 (Initial): Skapad för att på ett robust och dedikerat sätt omsluta en JSON-fil i
#   en statisk HTML-wrapper. Detta separerar ansvaret från datagenerering och från
#   komplexa shell-kommandon i CI/CD-flöden.
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

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Context Data</title>
    <style>body {{ font-family: monospace; white-space: pre; word-wrap: break-word; }}</style>
</head>
<body>
{json_content}
</body>
</html>"""

    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            json_content = f.read()

        final_html = html_template.format(json_content=json_content)

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
