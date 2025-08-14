#!/usr/bin/env python3
# historical_reconstruction_builder.py (v4, 2025-08-12)
# Läs en mapp med [SESSIONID].json och konsolidera till standardfiler.
# v4 UPGRADERING: Introducerat konfigurationsdriven, automatisk arkivering av
# underutnyttjade heuristiker för att hålla databasen relevant.

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple
from datetime import datetime, timedelta
from collections import OrderedDict

try:
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError
except ImportError:
    print("ERROR: jsonschema is not installed. Please run: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

SPEAKER_PATTERN = re.compile(r'^([^()]+) \\(([^:]+):([^@]+)@([^\\)]+)\\)$')

def normalize_speaker(entry: Dict[str, Any]) -> Dict[str, Any]:
    name = (entry.get("speakerName") or "unknown").strip() or "unknown"
    model = entry.get("model") or {}
    provider = (model.get("provider") or "unknown").strip() or "unknown"
    mname = (model.get("name") or "unknown").strip() or "unknown"
    version = (model.get("version") or "unknown").strip() or "unknown"
    display = f"{name} ({provider}:{mname}@{version})"
    entry["speakerName"] = name
    entry["model"] = {"provider": provider, "name": mname, "version": version}
    entry["speaker"] = display
    return entry

def ensure_chat_schema(chat_obj: Dict[str, Any]) -> Dict[str, Any]:
    interactions = chat_obj.get("interactions") or []
    fixed: List[Dict[str, Any]] = []
    for it in interactions:
        if "speakerName" not in it or "model" not in it:
            speaker = it.get("speaker", "")
            m = SPEAKER_PATTERN.match(speaker) if isinstance(speaker, str) else None
            if m:
                name, provider, mname, version = m.groups()
                it.setdefault("speakerName", name.strip())
                it.setdefault("model", {"provider": provider.strip(), "name": mname.strip(), "version": version.strip()})
            else:
                it.setdefault("speakerName", (speaker or "unknown").strip())
                it.setdefault("model", {"provider": "unknown", "name": "unknown", "version": "unknown"})
        fixed.append(normalize_speaker(it))
    chat_obj["interactions"] = fixed
    return chat_obj

def load_json_file(p: Path) -> Any:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        sys.stderr.write(f"[SKIP] {p.name}: {e}\\n")
        return None

def get_session_sort_key(p: Path) -> Tuple[float, int]:
    name = p.name
    if name.startswith('S-'):
        try:
            parts = name.replace('.json', '').split('-')
            date_part = datetime.strptime(parts[1], '%Y%m%d')
            seq_part = ord(parts[2])
            return (date_part.timestamp(), seq_part)
        except (ValueError, IndexError):
            return (float('inf'), 0)
    else:
        m = re.match(r'^(\\d+\\.?\\d*)\\.json$', name)
        return (float(m.group(1)), 0) if m else (float("inf"), 0)

def main():
    if len(sys.argv) < 2:
        print("Användning: python3 historical_reconstruction_builder.py /path/to/sessions_dir [/output_root]")
        sys.exit(2)
    sessions_dir = Path(sys.argv[1])
    out_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
    
    scripts_dir = out_root / "scripts"
    history_dir = scripts_dir / "history"
    docs_dir = out_root / "docs"
    ai_protocols_dir = docs_dir / "ai_protocols"
    tools_dir = out_root / "tools"
    dynamic_protocols_path = ai_protocols_dir / "DynamicProtocols.json"

    for d in [ai_protocols_dir, tools_dir, history_dir]:
        d.mkdir(parents=True, exist_ok=True)

    files = sorted([p for p in sessions_dir.glob("*.json") if p.is_file()], key=get_session_sort_key)
    
    bygglogg, chathistorik, perf, all_heuristics = [], [], [], []
    heuristic_usage_stats: Dict[str, List[datetime]] = {}

    # Läs in befintliga dynamiska protokoll
    dynamic_protocols_map = OrderedDict()
    if dynamic_protocols_path.exists():
        protocols_list = load_json_file(dynamic_protocols_path)
        if isinstance(protocols_list, list):
            for proto in protocols_list:
                if isinstance(proto, dict) and 'protocolId' in proto:
                    dynamic_protocols_map[proto['protocolId']] = proto

    for p in files:
        data = load_json_file(p)
        if not data or not isinstance(data, dict): continue
        
        session_date_str = data.get("createdAt")
        session_date = datetime.fromisoformat(session_date_str.replace('Z', '+00:00')) if session_date_str else None

        artifacts = data.get("artifacts") or {}
        if isinstance(artifacts.get("ByggLogg"), dict): bygglogg.append(artifacts["ByggLogg"])
        if isinstance(artifacts.get("Chatthistorik"), dict): chathistorik.append(ensure_chat_schema(artifacts["Chatthistorik"]))
        
        perf_data = artifacts.get("ai_protocol_performance")
        if isinstance(perf_data, dict):
            perf.append(perf_data)
            if session_date:
                for triggered_id in perf_data.get("detailedMetrics", {}).get("heuristicsTriggered", []):
                    heuristic_usage_stats.setdefault(triggered_id, []).append(session_date)
        
        lg = artifacts.get("frankensteen_learning_db")
        if isinstance(lg, list): all_heuristics.extend([h for h in lg if isinstance(h, dict)])
        elif isinstance(lg, dict): all_heuristics.append(lg)

        # Bearbeta godkända dynamiska protokoll
        approved_protocols = data.get("approvedNewDynamicProtocols")
        if isinstance(approved_protocols, list):
            for proto in approved_protocols:
                if isinstance(proto, dict) and 'protocolId' in proto:
                    dynamic_protocols_map[proto['protocolId']] = proto
                    print(f"[INFO] Iscensatt uppdatering för dynamiskt protokoll: {proto['protocolId']}")

    # --- Sanering och Harmonisering av Heuristiker ---
    maintenance_conf_path = history_dir / "heuristics_maintenance.json"
    active_heuristics = all_heuristics

    if maintenance_conf_path.exists():
        maint_conf = load_json_file(maintenance_conf_path)
        if maint_conf:
            # Steg 1: Automatisk Arkivering
            policy = maint_conf.get("autoArchivePolicy", {})
            if policy.get("enabled"):
                if files:
                    latest_session_date = datetime.fromisoformat(load_json_file(files[-1]).get("createdAt").replace('Z', '+00:00'))
                    start_date = latest_session_date - timedelta(days=policy.get("analysisWindowDays", 21))
                    
                    active_within_window_ids: Set[str] = set()
                    for heu_id, dates in heuristic_usage_stats.items():
                        if any(d >= start_date for d in dates):
                            active_within_window_ids.add(heu_id)
                    
                    protected_ids = set(policy.get("protectedHeuristics", []))
                    
                    pre_auto_archive_count = len(all_heuristics)
                    active_heuristics = [h for h in all_heuristics if h.get('heuristicId') in protected_ids or h.get('heuristicId') in active_within_window_ids]
                    archived_count = pre_auto_archive_count - len(active_heuristics)
                    print(f"[INFO] Auto-arkivering: {archived_count} heuristiker arkiverades p.g.a. inaktivitet.")

            # Steg 2: Manuell Arkivering
            to_archive_keys = {(item.get('heuristicId'), item.get('originSessionId')) for item in maint_conf.get('archiveHeuristics', [])}
            active_heuristics = [h for h in active_heuristics if (h.get('heuristicId'), h.get('metadata', {}).get('originSessionId')) not in to_archive_keys]

            # Steg 3: Manuella Tillägg
            existing_ids = {h.get('heuristicId') for h in active_heuristics}
            for new_h in maint_conf.get('addHeuristics', []):
                if new_h.get('heuristicId') not in existing_ids:
                    active_heuristics.append(new_h)
    
    # Steg 4: Hantera 'deprecates'-nyckeln
    ids_to_deprecate = {h['metadata']['deprecates'] for h in active_heuristics if h.get('metadata', {}).get('deprecates')}
    final_active_heuristics = [h for h in active_heuristics if h.get('heuristicId') not in ids_to_deprecate]
    final_active_heuristics.sort(key=lambda x: (x.get('metadata', {}).get('createdAt', '')))

    # --- (Resten av skriptet förblir oförändrat) ---

    (tools_dir / "frankensteen_learning_db.json").write_text(json.dumps(final_active_heuristics, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "ByggLogg.json").write_text(json.dumps(bygglogg, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "Chatthistorik.json").write_text(json.dumps(chathistorik, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "ai_protocol_performance.json").write_text(json.dumps(perf, ensure_ascii=False, indent=2), encoding="utf-8")

    (ai_protocols_dir / "DynamicProtocols.json").write_text(json.dumps(list(dynamic_protocols_map.values()), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] Skrev {len(bygglogg)} ByggLogg-poster, {len(chathistorik)} chattposter, {len(perf)} performance-poster.")
    print(f"[OK] Sanerade Learning DB: {len(final_active_heuristics)} aktiva heuristiker kvarstår.")
    print(f"[UT] {docs_dir / 'ByggLogg.json'}")
    print(f"[UT] {docs_dir / 'Chatthistorik.json'}")
    print(f"[UT] {docs_dir / 'ai_protocol_performance.json'}")
    print(f"[UT] {tools_dir / 'frankensteen_learning_db.json'}")
    print(f"[UT] {ai_protocols_dir / 'DynamicProtocols.json'}")

if __name__ == "__main__":
    main()
