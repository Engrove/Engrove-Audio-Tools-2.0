# scripts/modules/ui_performance_dashboard.py
# Frankensteen v2.1 (2025-08-28) - Korrigerad för UIStyles klass-import
#
# Denna modul ansvarar för att rendera en HTML-baserad dashboard
# för att visualisera AI-prestanda och projektdata.

import customtkinter as ctk
import tkinter.ttk as ttk
import json
import os
from datetime import datetime
from collections import defaultdict
from .ui_styles import UIStyles # <-- KORRIGERING: Importerar klassen, inte en konstant

# Definiera konstanta sökvägar till datakällorna
SESSION_MANIFEST_PATH = "docs/session_manifest.json"
LEARNING_DB_PATH = "tools/frankensteen_learning_db.json"
CHARTJS_CDN = "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"

class PerformanceDashboardUI(ttk.Frame):
    """
    En UI-komponent som läser in prestandadata, genererar en HTML-rapport
    och visar den i en textruta.
    """
    def __init__(self, parent, app_logic, **kwargs):
        super().__init__(parent, **kwargs)
        self.app_logic = app_logic
        self.styles = UIStyles() # <-- KORRIGERING: Instansierar klassen
        self.configure_styles()
        self.create_widgets()
        self.load_and_display_dashboard()

    def configure_styles(self):
        self.style = ttk.Style()
        # KORRIGERING: Använder objekt-notation för att komma åt attribut
        self.style.configure("Performance.TFrame", background=self.styles.colors["bg_primary"])
        self.configure(style="Performance.TFrame")

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.html_view = ctk.CTkTextbox(
            self,
            wrap="word",
            # KORRIGERING: Använder objekt-notation
            fg_color=self.styles.colors["bg_secondary"],
            text_color=self.styles.colors["text_main"],
            font=(self.styles.font["family"], self.styles.font["size_normal"])
        )
        self.html_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.html_view.configure(state="disabled")

    def _safe_load_json(self, path):
        """Hjälpfunktion för att säkert läsa JSON-filer."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"KRITISKT FEL: Filen {path} kunde inte hittas.")
            return None
        except json.JSONDecodeError:
            print(f"KRITISKT FEL: Filen {path} är ogiltig JSON.")
            return None

    def _process_sessions(self, sessions):
        """Bearbetar sessionsdata för KPI:er och grafer."""
        if not sessions:
            return None

        total_sessions = len(sessions)
        total_score = 0
        cycle_data = defaultdict(lambda: defaultdict(int))
        provider_counts = defaultdict(int)
        model_counts = defaultdict(int)
        correction_self_sum = 0
        correction_ext_sum = 0
        
        score_over_time = []
        
        for session in sessions:
            score = session.get('final_score', 0)
            total_score += score
            timestamp_str = session.get('start_time', '')
            if timestamp_str:
                date_only = timestamp_str.split('T')[0]
                score_over_time.append({"t": timestamp_str, "y": score})
                
                self_c = session.get('cycles', {}).get('self_corrections', 0)
                ext_c = session.get('cycles', {}).get('external_corrections', 0)
                correction_self_sum += self_c
                correction_ext_sum += ext_c
                
                cycle_data[date_only]['self'] += self_c
                cycle_data[date_only]['external'] += ext_c
                cycle_data[date_only]['debug'] += session.get('cycles', {}).get('debugging_cycles', 0)

            provider = session.get('provider', 'unknown')
            model = session.get('model', 'unknown')
            provider_counts[provider] += 1
            model_counts[model] += 1

        all_cycles = [s.get('cycles', {}).get('debugging_cycles', 0) for s in sessions]
        all_cycles.sort()
        median_cycles = all_cycles[len(all_cycles) // 2] if all_cycles else 0
        
        total_corrections = correction_self_sum + correction_ext_sum
        correction_ratio = round(correction_self_sum / total_corrections, 2) if total_corrections > 0 else 0

        chart_labels = sorted(cycle_data.keys())
        chart_cycles = {
            'labels': chart_labels,
            'debug_data': [cycle_data[d]['debug'] for d in chart_labels],
            'self_data': [cycle_data[d]['self'] for d in chart_labels],
            'external_data': [cycle_data[d]['external'] for d in chart_labels],
        }

        return {
            "kpis": { "total_sessions": total_sessions, "average_score": round(total_score / total_sessions, 2) if total_sessions > 0 else 0, "median_cycles": median_cycles, "correction_ratio": correction_ratio, },
            "charts": { "score_over_time": score_over_time, "cycles_per_session": chart_cycles, "providers": dict(provider_counts), "models": dict(model_counts) }
        }

    def _process_learning_db(self, db_content):
        """Extraherar data för Heuristics-tabellen."""
        if not db_content or 'items' not in db_content: return []
        return [{
            "ID": item['id'], "Risk": item.get('risk_level', 'NA'),
            "Mitigation": item['mitigation'].get('description', 'Missing'),
            "Trigger_Keywords": ', '.join(item.get('trigger_keywords', []))
        } for item in db_content['items']]

    def _load_and_process_data(self):
        """Laddar och bearbetar all rådata."""
        session_manifest = self._safe_load_json(SESSION_MANIFEST_PATH)
        learning_db = self._safe_load_json(LEARNING_DB_PATH)

        if not session_manifest or not learning_db:
            raise Exception("Kritiska manifestfiler saknas eller är korrupta.")

        session_data = self._process_sessions(session_manifest.get('sessions', []))
        session_data['tables'] = {
            "heuristics": self._process_learning_db(learning_db),
            "raw_sessions": session_manifest.get('sessions', [])
        }
        return session_data

    def _generate_html_content(self, data):
        """Genererar den fullständiga, Chart.js-drivna HTML-strukturen."""
        css_styles = self.styles.css_dashboard
        js_data = json.dumps(data)
        js_logic = self.app_logic.js_performance_logic
        
        return f"""
        <!DOCTYPE html><html lang="sv"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Performance Dashboard</title><script src="{CHARTJS_CDN}"></script><style>{css_styles}</style></head>
        <body><div id="dashboard-container">
            <div class="header-kpis grid-container-4">
                <div class="kpi-card"><span class="kpi-label">Antal sessioner</span><span class="kpi-value">{data['kpis']['total_sessions']}</span><span class="kpi-subtext">2025-08-11T08:00Z - {datetime.now().strftime('%Y-%m-%dT%H:%MZ')}</span></div>
                <div class="kpi-card"><span class="kpi-label">Medelpoäng</span><span class="kpi-value">{data['kpis']['average_score']}</span><span class="kpi-subtext">Final score (medel)</span></div>
                <div class="kpi-card"><span class="kpi-label">Median cykler</span><span class="kpi-value">{data['kpis']['median_cycles']}</span><span class="kpi-subtext">Debugging cycles (median)</span></div>
                <div class="kpi-card"><span class="kpi-label">Korrigeringsgrad</span><span class="kpi-value">{data['kpis']['correction_ratio']}</span><span class="kpi-subtext">Self/External ratio</span></div>
            </div>
            <div class="chart-section grid-container-2">
                <div class="chart-card"><h3>Final Score Over Time</h3><canvas id="scoreChart"></canvas></div>
                <div class="chart-card"><h3>Session Metrics (Cycles)</h3><canvas id="cycleChart"></canvas></div>
                <div class="chart-card small-chart"><h3>Sessions Per Provider</h3><canvas id="providerChart"></canvas></div>
                <div class="chart-card small-chart"><h3>Sessions Per Model</h3><canvas id="modelChart"></canvas></div>
            </div>
            <div class="table-section"><h2>Learning Database (Heuristics)</h2><table id="heuristicsTable" class="data-table"><thead><tr><th>ID</th><th>Risk</th><th>Mitigation</th><th>Trigger Keywords</th></tr></thead><tbody></tbody></table></div>
            <div class="table-section"><h2>Sessions</h2><table id="sessionsTable" class="data-table"><thead><tr><th>Session</th><th>Tid</th><th>Provider</th><th>Modell</th><th>Final</th><th>Cycles</th><th>Self</th><th>External</th></tr></thead><tbody></tbody></table></div>
        </div><script>const dashboardData = {js_data};{js_logic}</script></body></html>
        """

    def load_and_display_dashboard(self):
        """Orkestrerar dataladdning och rendering."""
        try:
            processed_data = self._load_and_process_data()
            html_content = self._generate_html_content(processed_data)
            
            # Skriv HTML-innehållet till en temporär fil för att kunna ladda i WebView
            temp_html_path = os.path.join("dist", "dashboard_view.html")
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            self.app_logic.html_for_dashboard = html_content

            self.html_view.configure(state="normal")
            self.html_view.delete("1.0", "end")
            info_text = "Dashboard genererad. Använd den globala 'Uppdatera Data'-knappen för att visa i huvudfönstret."
            self.html_view.insert("1.0", info_text)
            self.html_view.configure(state="disabled")

        except Exception as e:
            error_message = f"KRITISKT FEL I DATALADDNINGEN (FL-D T3 Varning):\n\nKunde inte ladda dashboard-data: {e}"
            self.html_view.configure(state="normal")
            self.html_view.delete("1.0", "end")
            self.html_view.insert("1.0", error_message, ("error",))
            self.html_view.configure(state="disabled")

