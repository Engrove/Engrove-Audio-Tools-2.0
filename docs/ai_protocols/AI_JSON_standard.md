# Kompakt, interoperabel “AI-JSON v1.0” som mappar rent mot OpenAI, **Google Gemini**, LangChain och JSON-LD.

# 1) JSON Schema (Draft 2020-12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/schemas/ai-json/v1.0",
  "title": "AI-JSON v1.0",
  "type": "object",
  "required": ["version", "id", "timestamp", "actor", "model", "action", "params"],
  "properties": {
    "version": { "const": "1.0" },
    "id": { "type": "string", "description": "ULID/UUID" },
    "timestamp": { "type": "string", "format": "date-time" },
    "actor": { "$ref": "#/$defs/Actor" },
    "model": { "$ref": "#/$defs/ModelSpec" },
    "action": { "type": "string", "description": "Semantic name of operation/tool/function" },
    "params": { "type": "object", "additionalProperties": true },
    "intent": { "type": "string" },
    "context": { "$ref": "#/$defs/Context" },
    "input": { "type": "object", "additionalProperties": true },
    "output": { "type": "object", "additionalProperties": true },
    "tool": { "$ref": "#/$defs/ToolRef" },
    "trace": { "$ref": "#/$defs/Trace" },
    "safety": { "$ref": "#/$defs/Safety" },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "sources": {
      "type": "array",
      "items": { "$ref": "#/$defs/Source" }
    },
    "cost": { "$ref": "#/$defs/Cost" },
    "metrics": { "$ref": "#/$defs/Metrics" },
    "policy": { "$ref": "#/$defs/Policy" },
    "error": { "$ref": "#/$defs/Error" },
    "extensions": { "type": "object", "additionalProperties": true }
  },
  "$defs": {
    "Actor": {
      "type": "object",
      "required": ["role"],
      "properties": {
        "role": { "type": "string", "enum": ["system", "user", "assistant", "tool", "orchestrator"] },
        "name": { "type": "string" },
        "session": { "type": "string" }
      }
    },
    "ModelSpec": {
      "type": "object",
      "required": ["provider", "name"],
      "properties": {
        "provider": { "type": "string", "enum": ["openai", "google", "anthropic", "azure-openai", "local", "other"] },
        "name": { "type": "string" },
        "mode": { "type": "string", "enum": ["chat", "tool", "embedding", "vision", "audio", "other"] },
        "parameters": {
          "type": "object",
          "properties": {
            "temperature": { "type": "number" },
            "top_p": { "type": "number" },
            "top_k": { "type": "integer" },
            "max_tokens": { "type": "integer" },
            "frequency_penalty": { "type": "number" },
            "presence_penalty": { "type": "number" },
            "safety_settings": { "type": "object" }
          },
          "additionalProperties": true
        }
      }
    },
    "ToolRef": {
      "type": "object",
      "properties": {
        "kind": { "type": "string", "enum": ["function", "rest", "rpc", "graph", "other"] },
        "name": { "type": "string" },
        "schema": { "type": "object", "additionalProperties": true },
        "version": { "type": "string" }
      }
    },
    "Context": {
      "type": "object",
      "properties": {
        "conversation_id": { "type": "string" },
        "parent_id": { "type": "string" },
        "locale": { "type": "string" },
        "audience": { "type": "string" },
        "tags": { "type": "array", "items": { "type": "string" } }
      }
    },
    "Trace": {
      "type": "object",
      "properties": {
        "span_id": { "type": "string" },
        "parent_span_id": { "type": "string" },
        "samples": {
          "type": "array",
          "items": { "$ref": "#/$defs/TraceSample" }
        }
      }
    },
    "TraceSample": {
      "type": "object",
      "properties": {
        "step": { "type": "integer" },
        "message": { "type": "string" },
        "data": { "type": "object", "additionalProperties": true }
      }
    },
    "Safety": {
      "type": "object",
      "properties": {
        "ratings": {
          "type": "array",
          "items": { "$ref": "#/$defs/SafetyRating" }
        },
        "filters_triggered": { "type": "array", "items": { "type": "string" } }
      }
    },
    "SafetyRating": {
      "type": "object",
      "properties": {
        "category": { "type": "string" },
        "probability": { "type": "number", "minimum": 0, "maximum": 1 },
        "action": { "type": "string", "enum": ["allow", "block", "monitor", "redact"] }
      }
    },
    "Source": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "uri": { "type": "string" },
        "snippet": { "type": "string" }
      }
    },
    "Cost": {
      "type": "object",
      "properties": {
        "input_tokens": { "type": "integer" },
        "output_tokens": { "type": "integer" },
        "currency": { "type": "string", "default": "USD" },
        "amount": { "type": "number" }
      }
    },
    "Metrics": {
      "type": "object",
      "properties": {
        "latency_ms": { "type": "integer" },
        "cache_hit": { "type": "boolean" }
      }
    },
    "Policy": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "version": { "type": "string" },
        "applied_rules": { "type": "array", "items": { "type": "string" } }
      }
    },
    "Error": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" },
        "retryable": { "type": "boolean" }
      }
    }
  },
  "additionalProperties": false
}
```

# 2) Exempel

## 2.1 Din struktur (”action/params”)

```json
{
  "version": "1.0",
  "id": "01J7ZK1ZQ3W3Q1R8H19P1E3G7V",
  "timestamp": "2025-08-24T09:12:33Z",
  "actor": { "role": "assistant", "name": "mapper" },
  "model": { "provider": "local", "name": "llama-3.1", "mode": "tool" },
  "action": "map_content_structure",
  "params": { "target": "in_memory_files" },
  "intent": "structure_extraction",
  "context": { "conversation_id": "conv-123", "tags": ["mapping","ingest"] }
}
```

## 2.2 OpenAI function calling → AI-JSON

```json
{
  "version": "1.0",
  "id": "01J7ZK2XCF4Q2SYQW0G0C3N6AC",
  "timestamp": "2025-08-24T09:14:02Z",
  "actor": { "role": "assistant" },
  "model": {
    "provider": "openai",
    "name": "gpt-4o-mini",
    "mode": "tool",
    "parameters": { "temperature": 0.2, "max_tokens": 512 }
  },
  "action": "map_content_structure",
  "params": { "target": "in_memory_files" },
  "tool": {
    "kind": "function",
    "name": "map_content_structure",
    "schema": { "type": "object", "properties": { "target": { "type": "string" } }, "required": ["target"] },
    "version": "1.0.0"
  },
  "trace": { "span_id": "span-a" }
}
```

## 2.3 **Google Gemini** function calling/tools → AI-JSON

(Gemini returnerar `functionCalls` i kandidat; mappas till `action`/`params`. Säkerhetsbetyg mappas till `safety.ratings`.)

```json
{
  "version": "1.0",
  "id": "01J7ZK4HRRGZ9G9G1BAY5JWC2F",
  "timestamp": "2025-08-24T09:16:11Z",
  "actor": { "role": "assistant" },
  "model": {
    "provider": "google",
    "name": "gemini-1.5-pro",
    "mode": "tool",
    "parameters": { "temperature": 0, "top_p": 0.95, "top_k": 40, "max_tokens": 512,
      "safety_settings": { "HATE": "BLOCK_MEDIUM_AND_ABOVE" }
    }
  },
  "action": "map_content_structure",
  "params": { "target": "in_memory_files" },
  "tool": {
    "kind": "function",
    "name": "map_content_structure",
    "schema": { "type": "object", "properties": { "target": { "type": "string" } }, "required": ["target"] }
  },
  "safety": {
    "ratings": [
      { "category": "HARM_CATEGORY_HATE_SPEECH", "probability": 0.0, "action": "allow" }
    ],
    "filters_triggered": []
  }
}
```

## 2.4 LangChain Tool → AI-JSON

```json
{
  "version": "1.0",
  "id": "01J7ZK5Z5ZQCT1QW9Q2M8V2H4S",
  "timestamp": "2025-08-24T09:17:40Z",
  "actor": { "role": "assistant" },
  "model": { "provider": "openai", "name": "gpt-4o", "mode": "tool" },
  "action": "map_content_structure",
  "params": { "target": "in_memory_files" },
  "tool": {
    "kind": "function",
    "name": "map_content_structure",
    "version": "lc:Tool-v0"
  },
  "trace": { "span_id": "lc-run-7812" }
}
```

# 3) JSON-LD (valfritt, för W3C/semantik)

```json
{
  "@context": {
    "ai": "https://schema.example/ai-json#",
    "action": "ai:action",
    "params": "ai:params",
    "model": "ai:model",
    "confidence": "ai:confidence",
    "source": "ai:source"
  },
  "action": "map_content_structure",
  "params": { "target": "in_memory_files" },
  "model": { "provider": "google", "name": "gemini-1.5-pro" },
  "confidence": 0.91
}
```

# 4) Rekommenderade fält (praktik)

* Obligatoriskt: `version,id,timestamp,actor,model,action,params`.
* Spårbarhet: `trace.span_id`, `context.conversation_id`.
* Auditering: `sources[]`, `safety.ratings[]`, `policy`.
* Drift: `cost`, `metrics`, `error`.

# 5) Namnrymder/kompatibilitet

* OpenAI: `tool.kind="function"`, `action=<function.name>`, `params=<arguments>`.
* **Gemini**: mappa `functionCall.name`→`action`, `functionCall.args`→`params`, `safetyRatings`→`safety.ratings`.
* LangChain: `tool.version="lc:Tool-v0"` eller liknande.
