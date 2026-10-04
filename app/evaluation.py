from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvalCase:
    request: str
    expected_tool: str | None


def tool_selection_accuracy(agent, cases: list[EvalCase]) -> float:
    if not cases:
        return 0.0
    correct = 0
    for case in cases:
        result = agent.run(case.request, session_id="eval")
        correct += int(result.tool_used == case.expected_tool)
    return correct / len(cases)
