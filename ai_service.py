import os
import json
import re
from typing import Any, Dict, List
import httpx

# ---------------------------------------------------------------------------
# Configuration – read once at import time
# ---------------------------------------------------------------------------
_INFERENCE_KEY = os.getenv("DIGITALOCEAN_INFERENCE_KEY")
_MODEL = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")
_ENDPOINT = "https://inference.do-ai.run/v1/chat/completions"

# ---------------------------------------------------------------------------
# Helper – extract raw JSON from LLM wrapped responses
# ---------------------------------------------------------------------------
def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

# ---------------------------------------------------------------------------
# Core inference request – handles timeout, errors and JSON extraction
# ---------------------------------------------------------------------------
async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    payload = {
        "model": _MODEL,
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "stream": False,
    }
    headers = {
        "Authorization": f"Bearer {_INFERENCE_KEY}",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            resp = await client.post(_ENDPOINT, json=payload, headers=headers)
            resp.raise_for_status()
        data = resp.json()
        # Expected OpenAI‑style response
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        raw_json = _extract_json(content)
        try:
            return json.loads(raw_json)
        except json.JSONDecodeError:
            # Return raw string as note if JSON cannot be parsed
            return {"note": "Failed to parse JSON from LLM response", "raw": raw_json}
    except Exception as exc:
        # Graceful fallback – never raise to route handler
        return {"note": f"AI service unavailable: {str(exc)}"}

# ---------------------------------------------------------------------------
# Public helpers used by the API routes
# ---------------------------------------------------------------------------
async def generate_tags(url: str) -> Dict[str, Any]:
    messages = [
        {
            "role": "user",
            "content": f"Generate up to 5 concise, lower‑case tags for the web page at {url}. Return a JSON object with a key 'generated_tags' containing a list of strings.",
        }
    ]
    result = await _call_inference(messages)
    # Ensure expected shape
    if "generated_tags" not in result:
        result = {"generated_tags": [], "note": result.get("note", "AI did not return tags")}
    return result

async def semantic_search(query: str) -> Dict[str, Any]:
    messages = [
        {
            "role": "user",
            "content": f"Perform a semantic search for the query '{query}' over the stored bookmarks. Return a JSON object with a key 'results' that is a list of objects each containing 'id' (int), 'title' (string), 'url' (string) and 'similarity_score' (float between 0 and 1).",
        }
    ]
    result = await _call_inference(messages)
    if "results" not in result:
        result = {"results": [], "note": result.get("note", "AI did not return results")}
    return result