from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardrailResult:
    allowed: bool
    reason: str = ""


class Guardrails:
    def __init__(self, max_chars: int = 4000) -> None:
        self.max_chars = max_chars

    def check(self, text: str) -> GuardrailResult:
        if not text.strip():
            return GuardrailResult(False, "Input is empty.")
        if len(text) > self.max_chars:
            return GuardrailResult(False, "Input exceeds the configured size limit.")
        return GuardrailResult(True, "")
