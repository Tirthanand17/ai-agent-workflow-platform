from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from .agent import ToolUsingAgent
from .tools import CSVSummaryTool, CalculatorTool, TextSearchTool

DATA_DIR = Path(__file__).resolve().parents[1] / "knowledge"

app = FastAPI(title="AI Agent Workflow API", version="0.1.0")
agent = ToolUsingAgent(
    tools=[
        CalculatorTool(),
        TextSearchTool(corpus_dir=DATA_DIR),
        CSVSummaryTool(),
    ]
)


class AgentRequest(BaseModel):
    request: str
    session_id: str = "default"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/agent")
def run_agent(payload: AgentRequest) -> dict:
    result = agent.run(payload.request, payload.session_id)
    return {
        "response": result.response,
        "tool_used": result.tool_used,
        "rationale": result.rationale,
        "memory": agent.memory.get(payload.session_id),
    }
