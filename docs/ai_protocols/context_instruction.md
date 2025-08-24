# docs/ai_protocols/context_instruction.md
# Kontext- och Rekonstruktionsprotokoll (ENHETLIG) v3.0
#
# === HISTORIK ===
# * v3.0 (2025-08-24): Enhetlig, motsägelsefri ersättare. Konsoliderar och ersätter
#   - /docs/ai_protocols/context_bootstrap_instruction_FINAL_v2.8.md
#   - /docs/ai_protocols/P-RECONSTRUCT-v1.0.md
#
# === OMFÅNG & ERSÄTTNING ===
# Detta dokument är den ENDA normkällan för sessionsavslutning (bootstrap) och
# historisk rekonstruktion. Det ersätter samtliga tidigare varianter och bilagor.
#
# === AKTIVERINGSLÄGEN ===
# A) Sessionsavslutning (Bootstrap): när uppdragsgivaren begär avslut.
# B) Historisk rekonstruktion: när äldre sessioner återskapas från loggar.
#
# === OUTPUT-KONTRAKT (gäller båda lägen) ===
# 1) Exakt EN fil per session: [SESSIONID].json
# 2) Rotobjekt MÅSTE innehålla: sessionId, createdAt, artifacts
# 3) artifacts MÅSTE innehålla:
#    - ByggLogg           (obligatorisk)
#    - Chatthistorik      (obligatorisk)
#    - ai_protocol_performance (obligatorisk)
#    - frankensteen_learning_db (VALFRI; inkluderas ENDAST om en ny heuristik föreslås)
# 4) Filnamn: [SESSIONID].json. Om sessionId saknas → använd "999".
#
# === OBLIGATORISKA DATAREGLER ===
# 1) No-Guess & No-Self-Report för modellmetadata
#    - provider|name|version får aldrig gissas. Endast explicit källa tillåten.
#    - saknas värde → sätt strängen "unknown" (ej null/tomt).
#    - AI:ns egen runtime-identitet får inte användas som default utan explicit källa.
# 2) Speaker-format (ALLTID)
#    speaker = "<speakerName> (<provider>:<name>@<version>)"
#    - MÅSTE spegla de maskinläsbara fälten speakerName + model{provider,name,version}.
#    - Regexkrav: ^[^()]+ \([^:]+:[^@]+@[^)]+\)$
# 3) Chatthistorik = alla turer
#    - Varje faktisk tur (inkl. System/Tooling) i kronologisk ordning.
#    - En interaction per tur. Ingen hopslagning.
#    - Rekommenderade extra fält per tur: turnIndex (1-baserad), timestamp (ISO8601 eller "unknown").
# 4) Tider och format
#    - createdAt/date: ISO 8601 (YYYY-MM-DDTHH:mm:ssZ).
#    - Endast giltig JSON (ingen trailing comma). Inga null för model/speaker.
#
# === VALIDERINGSGATE (måste passeras före leverans) ===
# - Varje speaker matchar regexen ovan.
# - model.provider|name|version är icke-tomma strängar ("unknown" tillåten).
# - Self-report-block: om model.* matchar AI-runtime utan källa → tvinga "unknown" på alla tre.
# - interactions-längd = antalet turer i sessionen. Osäker? Begär källa; endast vid uttrycklig begäran leverera med coverage:"partial" + coverageReason.
# - Scorecard-värden numeriska (0–100); finalScore ska vara korrekt sammanvägd siffra.
#
# === JSON SCHEMAN (normativa) ===
# 1) Chatthistorik (krav på talare/metadata)
# {
#   "type": "object",
#   "required": ["sessionId", "interactions"],
#   "properties": {
#     "sessionId": {"type": "string", "minLength": 1},
#     "interactions": {
#       "type": "array",
#       "items": {
#         "type": "object",
#         "required": ["speakerName", "model", "speaker", "summary"],
#         "properties": {
#           "speakerName": {"type": "string", "minLength": 1},
#           "model": {
#             "type": "object",
#             "required": ["provider", "name", "version"],
#             "properties": {
#               "provider": {"type": "string", "minLength": 1},
#               "name": {"type": "string", "minLength": 1},
#               "version": {"type": "string", "minLength": 1}
#             }
#           },
#           "speaker": {"type": "string", "pattern": "^[^()]+ \\([^:]+:[^@]+@[^)]+\\)$"},
#           "summary": {"type": "string", "minLength": 1}
#         }
#       }
#     }
#   }
# }
#
# 2) ai_protocol_performance (exempelstruktur, numeriska krav på scorecard)
# {
#   "type": "object",
#   "required": ["sessionId", "date", "aiQualitativeSummary", "scorecard", "detailedMetrics"],
#   "properties": {
#     "sessionId": {"type": "string", "minLength": 1},
#     "date": {"type": "string", "minLength": 1},
#     "aiQualitativeSummary": {"type": "string"},
#     "scorecard": {
#       "type": "object",
#       "required": ["efficacy", "efficiency", "robustness", "finalScore"],
#       "properties": {
#         "efficacy": {"type": "object", "properties": {"score": {"type": "number"}, "weight": {"type": "number"}, "weightedScore": {"type": "number"}}},
#         "efficiency": {"type": "object", "properties": {"score": {"type": "number"}, "weight": {"type": "number"}, "weightedScore": {"type": "number"}}},
#         "robustness": {"type": "object", "properties": {"score": {"type": "number"}, "weight": {"type": "number"}, "weightedScore": {"type": "number"}}},
#         "finalScore": {"type": "number"}
#       }
#     },
#     "detailedMetrics": {"type": "object"},
#     "improvementSuggestion": {"type": ["object", "null"]}
#   }
# }
#
# === EXEMPELOUTPUT (minimalt, formkontroll) ===
# {
#   "sessionId": "1",
#   "createdAt": "2025-01-01T12:00:00Z",
#   "artifacts": {
#     "ByggLogg": {
#       "sessionId": "1",
#       "date": "2025-01-01T12:00:00Z",
#       "summary": "…",
#       "actions": [{"title":"…","files":[{"path":"…","changeDescription":"…"}],"result":"…"}],
#       "projectStatus": "…"
#     },
#     "Chatthistorik": {
#       "sessionId": "1",
#       "interactions": [
#         {
#           "speakerName": "Engrove",
#           "model": {"provider": "human", "name": "operator", "version": "unknown"},
#           "speaker": "Engrove (human:operator@unknown)",
#           "summary": "…",
#           "turnIndex": 1,
#           "timestamp": "2025-01-01T12:00:00Z"
#         }
#       ]
#     },
#     "ai_protocol_performance": {
#       "sessionId": "1",
#       "date": "2025-01-01T12:00:00Z",
#       "aiQualitativeSummary": "…",
#       "scorecard": {
#         "efficacy": {"score": 0, "weight": 0.4, "weightedScore": 0.0},
#         "efficiency": {"score": 0, "weight": 0.3, "weightedScore": 0.0},
#         "robustness": {"score": 0, "weight": 0.3, "weightedScore": 0.0},
#         "finalScore": 0.0
#       },
#       "detailedMetrics": {
#         "missionCompleted": true,
#         "debuggingCycles": 0,
#         "selfCorrections": 0,
#         "externalCorrections": 0,
#         "protocolActivations": {"psv": 0, "helpMeGod": 0, "stalemate": 0}
#       },
#       "improvementSuggestion": {"pattern": "…", "proposedHeuristicId": "H-YYYYMMDD-seq"}
#     },
#     "frankensteen_learning_db": null
#   }
# }
#
# === EXEKVERING ===
# 1) Läs hela chatten / källloggar.
# 2) Bygg samtliga artefakter enligt kontraktet ovan.
# 3) Skriv en fil: [SESSIONID].json (eller 999.json om okänt).
#
# === BATCH-KONSOLIDERING (separat verktyg) ===
# - Läs en mapp med filer av typen [SESSIONID].json
# - Skriv sammanlagda standardfiler:
#   docs/ByggLogg.json
#   docs/Chatthistorik.json
#   docs/ai_protocol_performance.json
#   tools/frankensteen_learning_db.json
#
# Referensskript (fulltext, produktionsklart):
# ```python
# !/usr/bin/env python3
# historical_reconstruction_builder.py
# Konsolidera [SESSIONID].json → fyra standardfiler.
# import sys, json, re
# from pathlib import Path
# from typing import Dict, Any, List
#
# SPEAKER_PATTERN = re.compile(r'^([^()]+) \(([^:]+):([^@]+)@([^\)]+)\)$')
#
# def normalize_speaker(entry: Dict[str, Any]) -> Dict[str, Any]:
#     name = (entry.get("speakerName") or "unknown").strip() or "unknown"
#     model = entry.get("model") or {}
#     provider = (model.get("provider") or "unknown").strip() or "unknown"
#     mname = (model.get("name") or "unknown").strip() or "unknown"
#     version = (model.get("version") or "unknown").strip() or "unknown"
#     entry["speakerName"] = name
#     entry["model"] = {"provider": provider, "name": mname, "version": version}
#     entry["speaker"] = f"{name} ({provider}:{mname}@{version})"
#     return entry
#
# def ensure_chat_schema(chat_obj: Dict[str, Any]) -> Dict[str, Any]:
#     interactions = chat_obj.get("interactions") or []
#     fixed: List[Dict[str, Any]] = []
#     for it in interactions:
#         # Stöd för äldre format: "speaker" utan metadata
#         if "speakerName" not in it or "model" not in it:
#             speaker = it.get("speaker", "")
#             m = SPEAKER_PATTERN.match(speaker) if isinstance(speaker, str) else None
#             if m:
#                 name, provider, mname, version = m.groups()
#                 it.setdefault("speakerName", name.strip())
#                 it.setdefault("model", {"provider": provider.strip(), "name": mname.strip(), "version": version.strip()})
#             else:
#                 if isinstance(speaker, str) and speaker.strip():
#                     it.setdefault("speakerName", speaker.strip())
#                 else:
#                     it.setdefault("speakerName", "unknown")
#                 it.setdefault("model", {"provider": "unknown", "name": "unknown", "version": "unknown"})
#         fixed.append(normalize_speaker(it))
#     chat_obj["interactions"] = fixed
#     return chat_obj
#
# def load_session_file(p: Path) -> Dict[str, Any]:
#     try:
#         obj = json.loads(p.read_text(encoding="utf-8"))
#         if not isinstance(obj, dict) or "artifacts" not in obj:
#             raise ValueError("fel format: saknar 'artifacts'")
#         return obj
#     except Exception as e:
#         sys.stderr.write(f"[SKIP] {p.name}: {e}\n")
#         return {}
#
# def main():
#     if len(sys.argv) < 2:
#         print("Användning: python3 historical_reconstruction_builder.py /path/to/sessions_dir [/output_root]")
#         sys.exit(2)
#     sessions_dir = Path(sys.argv[1])
#     out_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
#     docs_dir = out_root / "docs"
#     tools_dir = out_root / "tools"
#     docs_dir.mkdir(parents=True, exist_ok=True)
#     tools_dir.mkdir(parents=True, exist_ok=True)
#
#     files = [p for p in sessions_dir.glob("*.json") if p.is_file()]
#     def session_key(p: Path):
#         m = re.match(r'^(\d+)\.json$', p.name)
#         return int(m.group(1)) if m else float("inf")
#     files.sort(key=session_key)
#
#     bygglogg: List[Dict[str, Any]] = []
#     chathistorik: List[Dict[str, Any]] = []
#     perf: List[Dict[str, Any]] = []
#     heuristics: List[Dict[str, Any]] = []
#
#     for p in files:
#         data = load_session_file(p)
#         if not data:
#             continue
#         art = data.get("artifacts") or {}
#         bl = art.get("ByggLogg")
#         if isinstance(bl, dict):
#             bygglogg.append(bl)
#         ch = art.get("Chatthistorik")
#         if isinstance(ch, dict):
#             chathistorik.append(ensure_chat_schema(ch))
#         ap = art.get("ai_protocol_performance")
#         if isinstance(ap, dict):
#             perf.append(ap)
#         lg = art.get("frankensteen_learning_db")
#         if isinstance(lg, dict):
#             heuristics.append(lg)
#
#     (docs_dir / "ByggLogg.json").write_text(json.dumps(bygglogg, ensure_ascii=False, indent=2), encoding="utf-8")
#     (docs_dir / "Chatthistorik.json").write_text(json.dumps(chathistorik, ensure_ascii=False, indent=2), encoding="utf-8")
#     (docs_dir / "ai_protocol_performance.json").write_text(json.dumps(perf, ensure_ascii=False, indent=2), encoding="utf-8")
#     (tools_dir / "frankensteen_learning_db.json").write_text(json.dumps(heuristics, ensure_ascii=False, indent=2), encoding="utf-8")
#
# if __name__ == "__main__":
#     main()
# ```
#
# === CHECKLISTA FÖRE LEVERANS ===
# - [ ] Alla fyra artefakter finns (ev. frankensteen_learning_db = null eller objekt).
# - [ ] Källor för modellmetadata verifierade; okända = "unknown"; INGEN självrapport.
# - [ ] Alla speaker-strängar följer visningsformatet och regexen.
# - [ ] ISO-datum, giltig JSON, ett (1) JSON-kodblock som slutoutput vid generering.
#
# === DEPRECATION (bindande) ===
# - "AI Identity Declaration" och "Metadata Injection Protocol" är AVSKRIVADE och FÖRBJUDNA.
# - Ingen automatisk metadata-injektion. All metadata måste komma från känd, spårbar källa.
#
# === LICENS/STATUS ===
# - Detta dokument är normativt och ersätter tidigare instruktioner från och med 2025-08-24.
