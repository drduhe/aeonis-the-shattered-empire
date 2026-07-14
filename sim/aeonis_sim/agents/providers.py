"""Provider adapters for qualitative playtest agents.

Providers return JSON objects only. They never see or mutate the Game object.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Protocol


class ProviderError(RuntimeError):
    """A model provider failed or returned an unusable response."""


class CompletionProvider(Protocol):
    name: str

    def complete(self, messages: list[dict], json_schema: dict) -> dict:
        """Return one JSON object matching json_schema."""
        ...


def _parse_json_object(value) -> dict:
    if isinstance(value, dict):
        return value
    if not isinstance(value, str):
        raise ProviderError(f"provider returned {type(value).__name__}, expected JSON object")
    text = value.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        text = text.rsplit("```", 1)[0].strip()
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ProviderError("provider response did not contain a JSON object")
    try:
        parsed = json.loads(text[start:end + 1])
    except json.JSONDecodeError as exc:
        raise ProviderError(f"invalid provider JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ProviderError("provider JSON root must be an object")
    return parsed


class OllamaProvider:
    """Local Ollama /api/chat adapter using only the Python standard library."""

    name = "ollama"

    def __init__(
        self,
        model: str,
        *,
        base_url: str = "http://127.0.0.1:11434",
        timeout_seconds: int = 180,
        temperature: float = 0.2,
        seed: int = 1,
        num_ctx: int = 8192,
        num_predict: int = 512,
    ):
        if not model:
            raise ValueError("Ollama provider requires a model")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = int(timeout_seconds)
        self.temperature = float(temperature)
        self.seed = int(seed)
        self.num_ctx = int(num_ctx)
        self.num_predict = int(num_predict)

    def complete(self, messages: list[dict], json_schema: dict) -> dict:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "format": json_schema,
            "options": {
                "temperature": self.temperature,
                "seed": self.seed,
                "num_ctx": self.num_ctx,
                "num_predict": self.num_predict,
            },
        }
        request = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:1000]
            raise ProviderError(f"Ollama request failed: HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ProviderError(f"Ollama request failed: {exc}") from exc
        content = (result.get("message") or {}).get("content")
        return _parse_json_object(content)


class DeterministicProvider:
    """CI/dry-run provider. Exercises the M5 pipeline but is not qualitative evidence."""

    name = "deterministic"

    def __init__(self, action_index: int = 0):
        self.action_index = int(action_index)

    def complete(self, messages: list[dict], json_schema: dict) -> dict:
        title = json_schema.get("title")
        if title == "AeonisDecision":
            return {
                "action_index": self.action_index,
                "reason": "Deterministic M5 pipeline choice.",
                "highlight": "Legal-choice contract exercised.",
                "frustration": "",
                "rules_question": "",
            }
        if title == "AeonisRoundReflection":
            return {
                "summary": "Deterministic round-reflection pipeline exercised.",
                "highlight": "Round snapshot received.",
                "frustration": "",
                "rules_question": "",
            }
        if title == "AeonisExitInterview":
            return {
                "pacing": "Dry-run only; no subjective pacing claim.",
                "map_flow": "Dry-run only.",
                "politics": "Dry-run only.",
                "combat": "Dry-run only.",
                "economy_pressure": "Dry-run only.",
                "best_moment": "The qualitative record completed.",
                "biggest_friction": "No model was used.",
                "rules_questions": [],
                "play_again": True,
                "hypotheses": [],
            }
        raise ProviderError(f"unsupported deterministic schema: {title}")


def provider_from_config(config: dict, *, seed: int = 1) -> CompletionProvider:
    kind = str(config.get("type", "deterministic")).lower()
    if kind == "deterministic":
        return DeterministicProvider(action_index=int(config.get("action_index", 0)))
    if kind == "ollama":
        return OllamaProvider(
            str(config.get("model", "")),
            base_url=str(config.get("base_url", "http://127.0.0.1:11434")),
            timeout_seconds=int(config.get("timeout_seconds", 180)),
            temperature=float(config.get("temperature", 0.2)),
            seed=int(config.get("seed", seed)),
            num_ctx=int(config.get("num_ctx", 8192)),
            num_predict=int(config.get("num_predict", 512)),
        )
    raise ValueError(f"unknown qualitative-agent provider: {kind}")
