from __future__ import annotations

from dataclasses import dataclass

from .guardrails import Guardrails
from .memory import SessionMemory
from .planner import RulePlanner
from .tools import Tool


@dataclass(frozen=True)
class AgentResult:
    response: str
    tool_used: str | None
    rationale: str


class ToolUsingAgent:
    def __init__(
        self,
        tools: list[Tool],
        planner: RulePlanner | None = None,
        memory: SessionMemory | None = None,
        guardrails: Guardrails | None = None,
    ) -> None:
        self.tools = {tool.name: tool for tool in tools}
        self.planner = planner or RulePlanner()
        self.memory = memory or SessionMemory()
        self.guardrails = guardrails or Guardrails()

    def run(self, request: str, session_id: str = "default") -> AgentResult:
        check = self.guardrails.check(request)
        if not check.allowed:
            return AgentResult(
                response=f"Request blocked: {check.reason}",
                tool_used=None,
                rationale="Guardrail blocked the request before planning.",
            )

        self.memory.add(session_id, "user", request)
        plan = self.planner.plan(request)

        if plan.tool_name is None:
            response = (
                "No external tool was needed. "
                "For production, this branch can be connected to an LLM provider."
            )
        else:
            tool = self.tools.get(plan.tool_name)
            if tool is None:
                response = f"Requested tool '{plan.tool_name}' is not available."
            else:
                response = tool.run(plan.argument)

        self.memory.add(session_id, "assistant", response)
        return AgentResult(
            response=response,
            tool_used=plan.tool_name,
            rationale=plan.rationale,
        )
