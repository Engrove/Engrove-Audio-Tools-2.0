# scripts/modules/ui_performance_dashboard.py
# Frankensteen v1.0 (2025-08-28)
#
# Denna modul ansvarar för att rendera en HTML-baserad dashboard
# för att visualisera AI-prestanda och projektdata.

import customtkinter as ctk
import tkinter.ttk as ttk
import json
from .ui_styles import UI_STYLES

# Definiera konstanta sökvägar till datakällorna
SESSION_MANIFEST_PATH = "docs/session_manifest.json"
LEARNING_DB_PATH = "tools/frankensteen_learning_db.json"

class PerformanceDashboardUI(ttk.Frame):
    """
    En UI-komponent som läser in prestandadata, genererar en HTML-rapport
    och visar den i en textruta.
    """
    def __init__(self, parent, app_logic, **kwargs):
        super().__init__(parent, **kwargs)
        self.app_logic = app_logic
        self.styles = UI_STYLES

        self.configure_styles()
        self.create_widgets()
        self.load_and_display_dashboard()

    def configure_styles(self):
        """Konfigurerar stilar för denna Frame."""
        self.style = ttk.Style()
        self.style.configure("Performance.TFrame", background=self.styles["colors"]["bg_primary"])
        self.configure(style="Performance.TFrame")

    def create_widgets(self):
        """Skapar de primära widgetarna för dashboard-vyn."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.html_view = ctk.CTkTextbox(
            self,
            wrap="word",
            fg_color=self.styles["colors"]["bg_secondary"],
            text_color=self.styles["colors"]["text_main"],
            font=(self.styles["font"]["family"], self.styles["font"]["size_normal"])
        )
        self.html_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.html_view.insert("1.0", "Laddar prestandadata...")
        self.html_view.configure(state="disabled")

    def _load_and_process_data(self):
        """
        PLATSHÅLLARE: Laddar in och transformerar data från JSON-filer.
        Detta är nästa steg i implementationen.
        """
        # TODO: Läs session_manifest.json och frankensteen_learning_db.json
        # TODO: Aggregera och beräkna KPIs (Antal sessioner, medelpoäng etc.)
        # TODO: Formatera data för Chart.js (listor med labels och data)
        # TODO: Extrahera data för tabellerna
        
        # Simulerar en datastruktur för nu
        processed_data = {
            "kpis": {
                "total_sessions": 77,
                "average_score": 66.98,
                "median_cycles": 2,
                "correction_ratio": 0.53
            },
            "charts": {},
            "tables": {}
        }
        return processed_data

    def _generate_html_content(self, data):
        """
        PLATSHÅLLARE: Genererar den fullständiga HTML-strängen för dashboarden.
        """
        # TODO: Inkludera CDN-länk för Chart.js
        # TODO: Skapa CSS Grid-layout
        # TODO: Skapa HTML för KPI-kort, canvas-element och tabeller
        # TODO: Skapa JavaScript-blocket för att rendera grafer och data
        
        # Temporär HTML för att visa att data laddats
        html_output = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Performance Dashboard</title>
        </head>
        <body>
            <h1>Dashboard Renders Here</h1>
            <pre>{json.dumps(data, indent=2)}</pre>
        </body>
        </html>
        """
        return html_output

    def load_and_display_dashboard(self):
        """Orkestrerar dataladdning och rendering."""
        try:
            processed_data = self._load_and_process_data()
            html_content = self._generate_html_content(processed_data)
            
            self.html_view.configure(state="normal")
            self.html_view.delete("1.0", "end")
            # CTkTextbox stöder inte full HTML-rendering, så vi visar en representation.
            # Den verkliga renderingen kommer att ske i en webbläsare via den genererade filen.
            # För applikationens syfte visar vi en formaterad text.
            
            info_text = "Dashboard Content Generated (visas som text i denna vy):\\n\\n"
            info_text += f"Antal Sessioner: {processed_data['kpis']['total_sessions']}\\n"
            info_text += f"Medelpoäng: {processed_data['kpis']['average_score']}\\n"
            info_text += f"Median Cykler: {processed_data['kpis']['median_cycles']}\\n"
            info_text += f"Korrigeringsgrad: {processed_data['kpis']['correction_ratio']}\\n"

            self.html_view.insert("1.0", info_text)
            self.html_view.configure(state="disabled")

        except Exception as e:
            error_message = f"Kunde inte ladda dashboard-data: {e}"
            self.html_view.configure(state="normal")
            self.html_view.delete("1.0", "end")
            self.html_view.insert("1.0", error_message, ("error",))
            self.html_view.configure(state="disabled")
