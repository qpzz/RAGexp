"""Replaceable real-LLM interface. No synthetic experiment adapter is shipped."""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod


class LLMError(RuntimeError):
    def __init__(self, message, raw=None, status=None):
        super().__init__(message)
        self.raw, self.status = raw, status


class Adapter(ABC):
    @abstractmethod
    def build_request(self, messages, seed, phase):
        pass

    @abstractmethod
    def complete(self, request):
        """Return {text, raw_response, finish_reason, elapsed_seconds}."""
        pass

    def metadata(self):
        return {"adapter": type(self).__name__}


class ChatCompletionsAdapter(Adapter):
    def __init__(self, config):
        self.config = config
        self.base_url = os.environ.get(config["base_url_env"], "").rstrip("/")
        self.model = os.environ.get(config["model_env"], "")
        self.key = os.environ.get(config["api_key_env"], "")
        missing = [name for name, value in [(config["base_url_env"], self.base_url),
                                            (config["model_env"], self.model)] if not value]
        if config.get("require_api_key", True) and not self.key:
            missing.append(config["api_key_env"])
        if missing:
            raise ValueError("Set environment variables: " + ", ".join(missing))
        parsed = urllib.parse.urlparse(self.base_url)
        if parsed.scheme not in ("https", "http") or not parsed.netloc or parsed.username or parsed.password or parsed.query:
            raise ValueError("Use an http(s) base URL without embedded credentials or query parameters")
        parameters = config.get("parameters", {})
        if any(k in parameters for k in ["model", "messages", "seed", "stream", "tools", "tool_choice", "response_format"]):
            raise ValueError("Reserved adapter parameter")

    def metadata(self):
        return {"adapter": "chat_completions", "base_url": self.base_url, "model": self.model,
                "seed_sent": bool(self.config.get("send_seed", False)),
                "parameters": self.config.get("parameters", {})}

    def build_request(self, messages, seed, phase):
        payload = {"model": self.model, "messages": messages, "stream": False,
                   **self.config.get("parameters", {})}
        if self.config.get("send_seed", False):
            payload["seed"] = seed
        if self.config.get("json_mode", False):
            payload["response_format"] = {"type": "json_object"}
        return payload

    def complete(self, request):
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = "Bearer " + self.key
        endpoint = self.base_url + self.config.get("chat_path", "/chat/completions")
        req = urllib.request.Request(endpoint, data=json.dumps(request).encode("utf-8"), headers=headers, method="POST")
        started = time.monotonic()
        try:
            with urllib.request.urlopen(req, timeout=self.config.get("timeout_seconds", 90)) as response:
                wire = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if self.key:
                body = body.replace(self.key, "[REDACTED]")
            raise LLMError("HTTP %s" % exc.code, raw=body, status=exc.code) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise LLMError(type(exc).__name__) from exc
        try:
            raw = json.loads(wire)
            choice = raw["choices"][0]
            content = choice["message"].get("content")
            if not isinstance(content, str):
                raise ValueError("Expected a text content field")
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMError("Unexpected response schema", raw=wire) from exc
        return {"text": content, "raw_response": raw,
                "finish_reason": choice.get("finish_reason"),
                "elapsed_seconds": time.monotonic() - started}
