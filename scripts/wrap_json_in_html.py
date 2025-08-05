# scripts/wrap_json_in_html.py
#
# HISTORIK:
# * v1.0 (Initial): Första versionen.
# * v2.0 (Bug Fix): Felaktig implementation med str.format().
# * v3.0 (Definitive Fix): Implementerar html.escape() för att korrekt hantera
#   specialtecken (<, >, &). Omsluter innehållet i en <pre>-tagg.
# * v4.0 (UI Enhancement): Lade till två knappar ("Kopiera", "Ladda ner") och
#   inbäddad JavaScript för att förbättra användarvänligheten.
#   - "Ladda ner JSON" använder en data-URI för att skapa en nedladdningsbar fil direkt i webbläsaren.
#   - "Kopiera till urklipp" använder navigator.clipboard API för ett modernt och säkert sätt att kopiera.
#
# TILLÄMPADE REGLER (Frankensteen v3.7):
# - Denna fil följer principen om Single Responsibility.
# - Använder standardbibliotek (`html`, `urllib.parse`) för robust hantering.
# - Robust felhantering med try-except och tydliga felmeddelanden till stderr.

import sys
import html
import urllib.parse

def wrap_json_in_html(input_json_path, output_html_path):
    """
    Läser en JSON-fil, bäddar in den på två sätt i en HTML-sida:
    1. HTML-escapad för säker visning i en <pre>-tagg.
    2. Som en rå data-URI för en nedladdningsknapp.
    Sidan innehåller knappar för att kopiera den visade datan och ladda ner den råa JSON-filen.
    """

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Context Data</title>
    <style>
        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
        }}
        .controls {{
            position: sticky;
            top: 0;
            background: #ffffff;
            padding: 12px 1em;
            border-bottom: 1px solid #ddd;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            gap: 10px;
            z-index: 10;
        }}
        button, .download-btn {{
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 6px;
            border: 1px solid #ccc;
            cursor: pointer;
            background-color: #fff;
            color: #333;
            text-decoration: none;
            display: inline-block;
            transition: background-color 0.2s, border-color 0.2s;
        }}
        button:hover, .download-btn:hover {{
            background-color: #f0f0f0;
            border-color: #bbb;
        }}
        button:active, .download-btn:active {{
            background-color: #e0e0e0;
        }}
        pre {{
            margin: 1em;
            font-family: "JetBrains Mono", "SF Mono", "Consolas", "Liberation Mono", "Menlo", monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: #fff;
            padding: 1em;
            border-radius: 6px;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>

<div class="controls">
    <button id="copy-btn">Copy to Clipboard</button>
    <a id="download-btn" class="download-btn" href="{data_uri}" download="context.json">Download JSON</a>
</div>

<pre id="context-pre">{escaped_content}</pre>

<script>
    document.getElementById('copy-btn').addEventListener('click', function() {{
        const preElement = document.getElementById('context-pre');
        const button = this;

        // Använder det moderna och säkra Clipboard API
        navigator.clipboard.writeText(preElement.textContent).then(function() {{
            button.textContent = 'Copied!';
            button.style.backgroundColor = '#d4edda'; // Grön feedback
            button.style.borderColor = '#c3e6cb';
            setTimeout(function() {{
                button.textContent = 'Copy to Clipboard';
                button.style.backgroundColor = '';
                button.style.borderColor = '';
            }}, 2000);
        }}, function(err) {{
            button.textContent = 'Failed to copy';
            button.style.backgroundColor = '#f8d7da'; // Röd feedback
            button.style.borderColor = '#f5c6cb';
            console.error('Could not copy text: ', err);
            setTimeout(function() {{
                button.textContent = 'Copy to Clipboard';
                button.style.backgroundColor = '';
                button.style.borderColor = '';
            }}, 3000);
        }});
    }});
</script>

</body>
</html>"""

    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            json_content = f.read()

        # 1. Escapa innehållet för säker visning i <pre>-taggen
        escaped_content = html.escape(json_content)

        # 2. Skapa en data-URI för nedladdningsknappen
        # URL-enkodar den råa JSON-datan för att den ska vara giltig i en länk.
        encoded_json_for_uri = urllib.parse.quote(json_content)
        data_uri = f"data:application/json;charset=utf-8,{encoded_json_for_uri}"

        # Fyll i mallen med den förberedda datan
        final_html = html_template.format(
            escaped_content=escaped_content,
            data_uri=data_uri
        )

        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"[INFO] Wrapper: Skapade framgångsrikt '{output_html_path}' med UI-förbättringar.")

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
