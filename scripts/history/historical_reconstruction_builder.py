#!/usr/bin/env python3
# historical_reconstruction_builder.py
# Läs en mapp med [SESSIONID].json och konsolidera till fyra standardfiler.
#
# OUTPUT:
#   docs/ByggLogg.json                (array)
#   docs/Chatthistorik.json           (array)
#   docs/ai_protocol_performance.json (array)
#   tools/frankensteen_learning_db.json (array)
#
# Regler:
# - Sortera kronologiskt utifrån SESSIONID i filnamnet (numerisk).
# - Normalisera talare: säkerställ maskinläsbar model + visningssträngen speaker.
# - Var defensiv: hoppa över trasiga filer men logga stderr.
#
# Användning:
#   python3 historical_reconstruction_builder.py /path/to/sessions_dir  [/output_root]
#
# sessions_dir: mapp som innehåller filer som '12.json', '31.json', ...
# output_root: rot där 'docs' och 'tools' skapas (default: current working dir).

import sys, json, re
from pathlib import Path
from typing import Dict, Any, List

SPEAKER_PATTERN = re.compile(r'^([^()]+) \(([^:]+):([^@]+)@([^\)]+)\)$')

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
        # Stöd för äldre format: "speaker" utan metadata
        if "speakerName" not in it or "model" not in it:
            speaker = it.get("speaker", "")
            # Heuristik för att extrahera, annars fallback till unknown
            m = SPEAKER_PATTERN.match(speaker) if isinstance(speaker, str) else None
            if m:
                name, provider, mname, version = m.groups()
                it.setdefault("speakerName", name.strip())
                it.setdefault("model", {"provider": provider.strip(), "name": mname.strip(), "version": version.strip()})
            else:
                # Om bara ett namn fanns (t.ex. 'Engrove' / 'Frankensteen')
                if isinstance(speaker, str) and speaker.strip():
                    it.setdefault("speakerName", speaker.strip())
                else:
                    it.setdefault("speakerName", "unknown")
                it.setdefault("model", {"provider": "unknown", "name": "unknown", "version": "unknown"})
        fixed.append(normalize_speaker(it))
    chat_obj["interactions"] = fixed
    return chat_obj

def load_session_file(p: Path) -> Dict[str, Any]:
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(obj, dict) or "artifacts" not in obj:
            raise ValueError("fel format: saknar 'artifacts'")
        return obj
    except Exception as e:
        sys.stderr.write(f"[SKIP] {p.name}: {e}\n")
        return {}

def main():
    if len(sys.argv) < 2:
        print("Användning: python3 historical_reconstruction_builder.py /path/to/sessions_dir [/output_root]")
        sys.exit(2)
    sessions_dir = Path(sys.argv[1])
    out_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
    docs_dir = out_root / "docs"
    tools_dir = out_root / "tools"
    docs_dir.mkdir(parents=True, exist_ok=True)
    tools_dir.mkdir(parents=True, exist_ok=True)

    files = [p for p in sessions_dir.glob("*.json") if p.is_file()]
    # sortera efter numerisk sessionId i filnamnet
    def session_key(p: Path):
        m = re.match(r'^(\d+)\.json$', p.name)
        return int(m.group(1)) if m else float("inf")
    files.sort(key=session_key)

    bygglogg: List[Dict[str, Any]] = []
    chathistorik: List[Dict[str, Any]] = []
    perf: List[Dict[str, Any]] = []
    heuristics: List[Dict[str, Any]] = []

    for p in files:
        data = load_session_file(p)
        if not data: 
            continue
        art = data.get("artifacts") or {}

        # 1) ByggLogg
        bl = art.get("ByggLogg")
        if isinstance(bl, dict):
            bygglogg.append(bl)

        # 2) Chatthistorik (normalisera talare)
        ch = art.get("Chatthistorik")
        if isinstance(ch, dict):
            chathistorik.append(ensure_chat_schema(ch))

        # 3) AI protocol performance
        ap = art.get("ai_protocol_performance")
        if isinstance(ap, dict):
            perf.append(ap)

        # 4) Learning DB (om finns)
        lg = art.get("frankensteen_learning_db")
        if isinstance(lg, dict):
            heuristics.append(lg)

    # Skriv ut
    (docs_dir / "ByggLogg.json").write_text(json.dumps(bygglogg, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "Chatthistorik.json").write_text(json.dumps(chathistorik, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "ai_protocol_performance.json").write_text(json.dumps(perf, ensure_ascii=False, indent=2), encoding="utf-8")
    (tools_dir / "frankensteen_learning_db.json").write_text(json.dumps(heuristics, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] Skrev {len(bygglogg)} ByggLogg-poster, {len(chathistorik)} chattposter, {len(perf)} performance-poster, {len(heuristics)} heuristik-poster.")
    print(f"[UT] {docs_dir / 'ByggLogg.json'}")
    print(f"[UT] {docs_dir / 'Chatthistorik.json'}")
    print(f"[UT] {docs_dir / 'ai_protocol_performance.json'}")
    print(f"[UT] {tools_dir / 'frankensteen_learning_db.json'}")

if __name__ == "__main__":
    main()
