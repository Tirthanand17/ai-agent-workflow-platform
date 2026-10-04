from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Plan:
    tool_name: str | None
    argument: str
    rationale: str


class RulePlanner:
    """Deterministic planner used for reliable tests and no-key local demos."""

    def plan(self, request: str) -> Plan:
        text = request.strip()

        if text.lower().startswith("calculate:"):
            return Plan(
                "calculator",
                text.split(":", 1)[1].strip(),
                "The request explicitly asks for arithmetic.",
            )

        if text.lower().startswith("search:"):
            return Plan(
                "text_search",
                text.split(":", 1)[1].strip(),
                "The request explicitly asks to search local knowledge.",
            )

        if text.lower().startswith("summarize csv:"):
            return Plan(
                "csv_summary",
                text.split(":", 1)[1].strip(),
                "The request explicitly asks for CSV inspection.",
            )

        return Plan(
            None,
            text,
            "No safe local tool was required; respond directly.",
        )
